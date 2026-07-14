from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_db
from src.repositories.user_repository import UserRepository
from src.repositories.workflow_repository import WorkflowRepository


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
