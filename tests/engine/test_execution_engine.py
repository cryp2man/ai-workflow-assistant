"""Интеграционные тесты ExecutionEngine.

Самодостаточны: in-memory SQLite + фейковый LLM-провайдер, без внешней БД
и сети. Покрывают ядро проекта — выполнение цепочки шагов, передачу контекста,
условия-ворота и историю запусков.
"""

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.db.base import Base

# Импорт моделей регистрирует таблицы в Base.metadata для create_all
from src.db.models import User, Workflow, WorkflowStep  # noqa: F401
from src.engine.execution_engine import ExecutionEngine
from src.llm.base import BaseLLMProvider
from src.prompts.builder import PromptBuilder
from src.repositories.workflow_repository import WorkflowRepository
from src.repositories.workflow_run_repository import WorkflowRunRepository
from src.repositories.workflow_step_repository import WorkflowStepRepository
from src.services.workflow_run_service import WorkflowRunService
from src.services.workflow_service import WorkflowService
from src.services.workflow_step_service import WorkflowStepService


class EchoLLMProvider(BaseLLMProvider):
    """Фейковый LLM: детерминированно оборачивает промпт, пишет историю вызовов."""

    def __init__(self) -> None:
        self.prompts: list[str] = []

    async def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return f"echo:{prompt}"


@pytest.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with factory() as s:
        yield s
    await engine.dispose()


def build_engine(session: AsyncSession, provider: BaseLLMProvider) -> ExecutionEngine:
    return ExecutionEngine(
        workflow_service=WorkflowService(WorkflowRepository(session)),
        workflow_run_service=WorkflowRunService(WorkflowRunRepository(session)),
        workflow_step_service=WorkflowStepService(WorkflowStepRepository(session)),
        prompt_builder=PromptBuilder(),
        llm_provider=provider,
    )


async def seed_workflow(
    session: AsyncSession,
    steps: list[tuple[str, str, str]],
    title: str = "Test WF",
) -> Workflow:
    """Создать пользователя, workflow и его шаги. steps: (title, prompt, step_type)."""
    user = User(username="tester", email="t@test.com", telegram_id=1)
    session.add(user)
    await session.flush()
    workflow = Workflow(title=title, description=None, user_id=user.id)
    session.add(workflow)
    await session.flush()
    for order, (step_title, prompt, step_type) in enumerate(steps, start=1):
        session.add(
            WorkflowStep(
                workflow_id=workflow.id,
                title=step_title,
                prompt=prompt,
                step_order=order,
                step_type=step_type,
            )
        )
    await session.commit()
    return workflow


class TestExecutionEngine:
    async def test_missing_workflow_raises(self, session: AsyncSession):
        engine = build_engine(session, EchoLLMProvider())
        with pytest.raises(ValueError):
            await engine.execute_workflow(999)

    async def test_single_llm_step_completes(self, session: AsyncSession):
        workflow = await seed_workflow(session, [("s1", "hello", "llm")])
        engine = build_engine(session, EchoLLMProvider())

        run = await engine.execute_workflow(workflow.id)

        assert run.status == "completed"
        assert run.result["response"] == "echo:hello"
        assert len(run.result["steps"]) == 1

    async def test_context_variable_passed_between_steps(
        self, session: AsyncSession
    ):
        provider = EchoLLMProvider()
        workflow = await seed_workflow(
            session,
            [
                ("first", "start", "llm"),
                ("second", "use {{previous_response}}", "llm"),
            ],
        )
        engine = build_engine(session, provider)

        run = await engine.execute_workflow(workflow.id)

        # Второй промпт должен содержать ответ первого шага (подстановка переменной)
        assert provider.prompts[1] == "use echo:start"
        assert run.status == "completed"
        assert len(run.result["steps"]) == 2

    async def test_condition_stops_workflow(self, session: AsyncSession):
        provider = EchoLLMProvider()
        workflow = await seed_workflow(
            session,
            [
                ("gen", "hello", "llm"),
                ("gate", "{{previous_response}} contains MISSING", "condition"),
                ("never", "should not run", "llm"),
            ],
        )
        engine = build_engine(session, provider)

        run = await engine.execute_workflow(workflow.id)

        assert run.status == "stopped"
        assert run.result["stopped_reason"] == "stopped by condition at step 2"
        # Третий шаг пропущен: LLM вызван только для первого шага
        assert provider.prompts == ["hello"]
        assert len(run.result["steps"]) == 2

    async def test_condition_pass_continues_workflow(self, session: AsyncSession):
        workflow = await seed_workflow(
            session,
            [
                ("gen", "hello", "llm"),
                ("gate", "{{previous_response}} contains hello", "condition"),
                ("final", "done", "llm"),
            ],
        )
        engine = build_engine(session, EchoLLMProvider())

        run = await engine.execute_workflow(workflow.id)

        assert run.status == "completed"
        assert len(run.result["steps"]) == 3

    async def test_run_is_persisted_in_history(self, session: AsyncSession):
        workflow = await seed_workflow(session, [("s1", "hi", "llm")])
        run_service = WorkflowRunService(WorkflowRunRepository(session))
        engine = build_engine(session, EchoLLMProvider())

        run = await engine.execute_workflow(workflow.id)

        history = await run_service.list_workflow_runs_by_workflow(workflow.id)
        assert any(r.id == run.id for r in history)
