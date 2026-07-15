from sqlalchemy.exc import IntegrityError

from src.db.models.workflow_step import WorkflowStep
from src.repositories.workflow_step_repository import WorkflowStepRepository


class WorkflowStepService:
    """Сервис шагов workflow: бизнес-логика и управление транзакциями.

    Repository только выполняет операции с данными (flush),
    границы транзакции (commit/rollback) — ответственность сервиса.
    """

    def __init__(self, repository: WorkflowStepRepository) -> None:
        self.repository = repository

    async def create_step(self, step: WorkflowStep) -> WorkflowStep:
        """Создать шаг и зафиксировать транзакцию."""
        try:
            step = await self.repository.create(step)
            await self.repository.session.commit()
        except IntegrityError:
            await self.repository.session.rollback()
            raise
        return step

    async def get_step(self, step_id: int) -> WorkflowStep | None:
        """Получить шаг по id."""
        return await self.repository.get_by_id(step_id)

    async def list_steps(self) -> list[WorkflowStep]:
        """Получить все шаги."""
        return await self.repository.list()

    async def list_workflow_steps(self, workflow_id: int) -> list[WorkflowStep]:
        """Получить шаги конкретного workflow в порядке step_order."""
        return await self.repository.list_by_workflow(workflow_id)

    async def delete_step(self, step: WorkflowStep) -> None:
        """Удалить шаг и зафиксировать транзакцию."""
        try:
            await self.repository.delete(step)
            await self.repository.session.commit()
        except IntegrityError:
            await self.repository.session.rollback()
            raise
