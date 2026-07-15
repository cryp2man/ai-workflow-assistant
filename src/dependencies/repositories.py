from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_db
from src.repositories.user_repository import UserRepository
from src.repositories.workflow_repository import WorkflowRepository
from src.repositories.workflow_run_repository import WorkflowRunRepository
from src.repositories.workflow_step_repository import WorkflowStepRepository


def get_user_repository(
    session: AsyncSession = Depends(get_db),
) -> UserRepository:
    """Репозиторий пользователей на сессии текущего запроса."""
    return UserRepository(session)


def get_workflow_repository(
    session: AsyncSession = Depends(get_db),
) -> WorkflowRepository:
    """Репозиторий рабочих процессов на сессии текущего запроса."""
    return WorkflowRepository(session)


def get_workflow_run_repository(
    session: AsyncSession = Depends(get_db),
) -> WorkflowRunRepository:
    """Репозиторий запусков workflow на сессии текущего запроса."""
    return WorkflowRunRepository(session)


def get_workflow_step_repository(
    session: AsyncSession = Depends(get_db),
) -> WorkflowStepRepository:
    """Репозиторий шагов workflow на сессии текущего запроса."""
    return WorkflowStepRepository(session)
