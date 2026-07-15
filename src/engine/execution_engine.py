import logging
import time
from datetime import datetime

from src.db.models.workflow_run import WorkflowRun
from src.llm.base import BaseLLMProvider
from src.prompts.builder import PromptBuilder
from src.services.workflow_run_service import WorkflowRunService
from src.services.workflow_service import WorkflowService
from src.services.workflow_step_service import WorkflowStepService

logger = logging.getLogger(__name__)


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
        try:
            for step in steps:
                logger.info("Executing step %s: %s", step.step_order, step.title)
                if previous_response == "":
                    prompt = self.prompt_builder.build_prompt(step.prompt)
                else:
                    prompt = self.prompt_builder.build_prompt(
                        f"{step.prompt}\n\nPrevious response:\n\n{previous_response}"
                    )
                start_time = time.perf_counter()
                response = await self.llm_provider.generate(prompt)
                elapsed = time.perf_counter() - start_time
                previous_response = response
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

        workflow_run.status = "completed"
        workflow_run.finished_at = datetime.utcnow()
        workflow_run.result = {"response": previous_response}
        await self.workflow_run_service.repository.session.commit()

        return workflow_run
