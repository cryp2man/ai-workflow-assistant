import asyncio
import ipaddress
import logging
import time
from datetime import datetime
from urllib.parse import urlparse

import httpx

from src.db.models.workflow_run import WorkflowRun
from src.engine.conditions import evaluate_condition
from src.llm.base import BaseLLMProvider
from src.prompts.builder import PromptBuilder
from src.services.workflow_run_service import WorkflowRunService
from src.services.workflow_service import WorkflowService
from src.services.workflow_step_service import WorkflowStepService

logger = logging.getLogger(__name__)

# Ограничения HTTP-шагов: таймаут запроса и размер ответа,
# попадающего в контекст выполнения (защита БД и контекста LLM).
HTTP_STEP_TIMEOUT = 30
HTTP_STEP_MAX_RESPONSE_CHARS = 10_000


class UnsafeUrlError(Exception):
    """URL HTTP-шага не прошел SSRF-валидацию."""


async def validate_http_step_url(url: str) -> None:
    """Защита от SSRF: только http(s) и только публичные адреса.

    URL шага задается пользователем, поэтому без проверки сервер можно
    заставить обратиться к localhost, приватной сети или metadata-эндпоинту
    облака (169.254.169.254).
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise UnsafeUrlError(f"Unsupported URL scheme: {parsed.scheme!r}")
    if not parsed.hostname:
        raise UnsafeUrlError("URL has no hostname")

    try:
        addr_infos = await asyncio.get_running_loop().getaddrinfo(
            parsed.hostname, None
        )
    except OSError as e:
        raise UnsafeUrlError(f"Cannot resolve host: {parsed.hostname!r}") from e

    for info in addr_infos:
        ip = ipaddress.ip_address(info[4][0])
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        ):
            raise UnsafeUrlError(
                f"URL resolves to a non-public address: {parsed.hostname!r}"
            )


class ExecutionEngine:
    """Движок выполнения Workflow.

    Первая итерация: фиксирует факт запуска (WorkflowRun со статусом
    "running"). Завершение, ошибки и LLM-шаги — в следующих задачах.
    """

    def __init__(
        self,
        workflow_service: WorkflowService,
        workflow_run_service: WorkflowRunService,
        workflow_step_service: WorkflowStepService,
        prompt_builder: PromptBuilder,
        llm_provider: BaseLLMProvider,
    ) -> None:
        self.workflow_service = workflow_service
        self.workflow_run_service = workflow_run_service
        self.workflow_step_service = workflow_step_service
        self.prompt_builder = prompt_builder
        self.llm_provider = llm_provider

    async def execute_workflow(
        self,
        workflow_id: int,
    ) -> WorkflowRun:
        """Запустить workflow: создать WorkflowRun и довести его до completed."""
        workflow = await self.workflow_service.get_workflow(workflow_id)
        if workflow is None:
            raise ValueError("Workflow not found")

        steps = await self.workflow_step_service.list_workflow_steps(workflow.id)

        workflow_run = WorkflowRun(
            workflow_id=workflow.id,
            status="running",
            started_at=datetime.utcnow(),
            finished_at=None,
            result=None,
            error=None,
        )
        workflow_run = await self.workflow_run_service.create_workflow_run(
            workflow_run
        )

        previous_response = ""
        variables: dict[str, str] = {"workflow_name": workflow.title}
        step_results: list[dict] = []
        stopped_reason: str | None = None
        try:
            for step in steps:
                logger.info("Executing step %s: %s", step.step_order, step.title)

                # Condition-шаг — «ворота»: не производит контент, а решает,
                # продолжать ли выполнение. Обрабатываем до generic-ветки.
                if step.step_type == "condition":
                    passed = evaluate_condition(step.prompt, variables)
                    verdict = "passed" if passed else "failed"
                    step_results.append(
                        {
                            "step_order": step.step_order,
                            "title": step.title,
                            "response": f"condition {verdict}",
                        }
                    )
                    logger.info("Condition step %s: %s", step.step_order, verdict)
                    if not passed:
                        stopped_reason = (
                            f"stopped by condition at step {step.step_order}"
                        )
                        break
                    continue

                prompt = self.prompt_builder.build_prompt(step.prompt, variables)
                start_time = time.perf_counter()
                response = await self._execute_step(step.step_type, prompt)
                elapsed = time.perf_counter() - start_time
                previous_response = response
                variables["previous_response"] = response
                variables[f"step{step.step_order}"] = response
                step_results.append(
                    {
                        "step_order": step.step_order,
                        "title": step.title,
                        "response": response,
                    }
                )
                logger.info(
                    "Step completed: %s (%.3fs)", step.step_order, elapsed
                )
        except Exception as e:
            logger.error("Step failed: %s", step.step_order)
            workflow_run.status = "failed"
            workflow_run.finished_at = datetime.utcnow()
            workflow_run.error = str(e)
            await self.workflow_run_service.repository.session.commit()
            raise

        workflow_run.status = "stopped" if stopped_reason else "completed"
        workflow_run.finished_at = datetime.utcnow()
        workflow_run.result = {
            "response": previous_response,
            "steps": step_results,
            "stopped_reason": stopped_reason,
        }
        await self.workflow_run_service.repository.session.commit()

        return workflow_run

    async def _execute_step(self, step_type: str, prompt: str) -> str:
        """Выполнить один шаг в зависимости от его типа."""
        if step_type == "http":
            return await self._execute_http_step(prompt)
        return await self.llm_provider.generate(prompt)

    async def _execute_http_step(self, url: str) -> str:
        """HTTP-шаг: GET по URL (prompt шага), тело ответа — в контекст.

        Редиректы отключены: редирект на внутренний адрес обошел бы
        SSRF-валидацию исходного URL.
        """
        url = url.strip()
        await validate_http_step_url(url)
        async with httpx.AsyncClient(
            timeout=HTTP_STEP_TIMEOUT, follow_redirects=False
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
        return response.text[:HTTP_STEP_MAX_RESPONSE_CHARS]
