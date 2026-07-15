"""Общая логика бота: сборка движка и работа с пользователями/workflow.

Бот — тонкий интерфейс к тому же ядру, что и REST API: переиспользует
сервисы, репозитории и ExecutionEngine, работая напрямую через сессию БД.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.db.models import User, Workflow, WorkflowStep
from src.engine.execution_engine import ExecutionEngine
from src.llm.base import BaseLLMProvider
from src.llm.openai_compatible_provider import OpenAICompatibleProvider
from src.llm.openai_provider import OllamaProvider
from src.prompts.builder import PromptBuilder
from src.repositories.user_repository import UserRepository
from src.repositories.workflow_repository import WorkflowRepository
from src.repositories.workflow_run_repository import WorkflowRunRepository
from src.repositories.workflow_step_repository import WorkflowStepRepository
from src.services.user_service import UserService
from src.services.workflow_service import WorkflowService

DEMO_STEPS = [
    ("Extract the request", "llm",
     "Extract the client's key request in one sentence: a client is looking "
     "for a 2-bedroom apartment near the sea, budget 150k"),
    ("Gate: is it real estate", "condition",
     "{{previous_response}} contains apartment"),
    ("Build an action checklist", "llm",
     "Turn this request into a 3-item action checklist for an agent:\n\n"
     "{{previous_response}}"),
]


def _llm_provider() -> BaseLLMProvider:
    if settings.LLM_PROVIDER == "ollama":
        return OllamaProvider(settings)
    return OpenAICompatibleProvider(settings)


def build_engine(session: AsyncSession) -> ExecutionEngine:
    """Собрать ExecutionEngine на переданной сессии (как в DI API)."""
    from src.services.workflow_run_service import WorkflowRunService
    from src.services.workflow_step_service import WorkflowStepService

    return ExecutionEngine(
        workflow_service=WorkflowService(WorkflowRepository(session)),
        workflow_run_service=WorkflowRunService(WorkflowRunRepository(session)),
        workflow_step_service=WorkflowStepService(WorkflowStepRepository(session)),
        prompt_builder=PromptBuilder(),
        llm_provider=_llm_provider(),
    )


async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    username: str | None,
) -> User:
    """Найти пользователя по Telegram ID или создать нового."""
    service = UserService(UserRepository(session))
    user = await service.get_user_by_telegram(telegram_id)
    if user is not None:
        return user
    user = User(
        username=username or f"tg_{telegram_id}",
        email=f"{telegram_id}@telegram.local",
        telegram_id=telegram_id,
    )
    return await service.create_user(user)


async def create_demo_workflow(session: AsyncSession, user_id: int) -> Workflow:
    """Создать демонстрационный workflow (LLM → condition → LLM) для пользователя."""
    workflow = Workflow(
        title="Real estate lead → action checklist",
        description="Demo: LLM extract → condition gate → LLM checklist",
        user_id=user_id,
    )
    session.add(workflow)
    await session.flush()
    for order, (title, step_type, prompt) in enumerate(DEMO_STEPS, start=1):
        session.add(
            WorkflowStep(
                workflow_id=workflow.id,
                title=title,
                prompt=prompt,
                step_order=order,
                step_type=step_type,
            )
        )
    await session.commit()
    return workflow
