from sqlalchemy.exc import IntegrityError

from src.db.models.workflow import Workflow
from src.repositories.workflow_repository import WorkflowRepository


class WorkflowService:
    """Сервис рабочих процессов: бизнес-логика и управление транзакциями.

    Repository только выполняет операции с данными (flush),
    границы транзакции (commit/rollback) — ответственность сервиса.
    """

    def __init__(self, repository: WorkflowRepository) -> None:
        self.repository = repository

    async def create_workflow(self, workflow: Workflow) -> Workflow:
        """Создать workflow и зафиксировать транзакцию."""
        try:
            workflow = await self.repository.create(workflow)
            await self.repository.session.commit()
        except IntegrityError:
            await self.repository.session.rollback()
            raise
        return workflow

    async def get_workflow(self, workflow_id: int) -> Workflow | None:
        """Получить workflow по id."""
        return await self.repository.get_by_id(workflow_id)

    async def list_workflows(self) -> list[Workflow]:
        """Получить все workflows."""
        return await self.repository.list()

    async def list_user_workflows(self, user_id: int) -> list[Workflow]:
        """Получить все workflows пользователя."""
        return await self.repository.list_by_user(user_id)

    async def delete_workflow(self, workflow: Workflow) -> None:
        """Удалить workflow и зафиксировать транзакцию."""
        try:
            await self.repository.delete(workflow)
            await self.repository.session.commit()
        except IntegrityError:
            await self.repository.session.rollback()
            raise
