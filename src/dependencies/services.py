from fastapi import Depends

from src.dependencies.repositories import (
    get_user_repository,
    get_workflow_repository,
    get_workflow_run_repository,
    get_workflow_step_repository,
)
from src.repositories.user_repository import UserRepository
from src.repositories.workflow_repository import WorkflowRepository
from src.repositories.workflow_run_repository import WorkflowRunRepository
from src.repositories.workflow_step_repository import WorkflowStepRepository
from src.services.user_service import UserService
from src.services.workflow_run_service import WorkflowRunService
from src.services.workflow_service import WorkflowService
from src.services.workflow_step_service import WorkflowStepService


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


def get_workflow_run_service(
    repository: WorkflowRunRepository = Depends(get_workflow_run_repository),
) -> WorkflowRunService:
    """Сервис запусков workflow поверх WorkflowRunRepository."""
    return WorkflowRunService(repository)


def get_workflow_step_service(
    repository: WorkflowStepRepository = Depends(get_workflow_step_repository),
) -> WorkflowStepService:
    """Сервис шагов workflow поверх WorkflowStepRepository."""
    return WorkflowStepService(repository)
