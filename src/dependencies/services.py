from fastapi import Depends

from src.dependencies.repositories import get_user_repository, get_workflow_repository
from src.repositories.user_repository import UserRepository
from src.repositories.workflow_repository import WorkflowRepository
from src.services.user_service import UserService
from src.services.workflow_service import WorkflowService


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Сервис пользователей поверх UserRepository."""
    return UserService(repository)


def get_workflow_service(
    repository: WorkflowRepository = Depends(get_workflow_repository),
) -> WorkflowService:
    """Сервис рабочих процессов поверх WorkflowRepository."""
    return WorkflowService(repository)
