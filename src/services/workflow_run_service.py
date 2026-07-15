from sqlalchemy.exc import IntegrityError

from src.db.models.workflow_run import WorkflowRun
from src.repositories.workflow_run_repository import WorkflowRunRepository


class WorkflowRunService:
    """Сервис запусков workflow: бизнес-логика и управление транзакциями.

    Repository только выполняет операции с данными (flush),
    границы транзакции (commit/rollback) — ответственность сервиса.
    """

    def __init__(self, repository: WorkflowRunRepository) -> None:
        self.repository = repository

    async def create_workflow_run(self, workflow_run: WorkflowRun) -> WorkflowRun:
        """Создать запуск и зафиксировать транзакцию."""
        try:
            workflow_run = await self.repository.create(workflow_run)
            await self.repository.session.commit()
        except IntegrityError:
            await self.repository.session.rollback()
            raise
        return workflow_run

    async def get_workflow_run(self, run_id: int) -> WorkflowRun | None:
        """Получить запуск по id."""
        return await self.repository.get_by_id(run_id)

    async def list_workflow_runs(self) -> list[WorkflowRun]:
        """Получить все запуски."""
        return await self.repository.list()

    async def list_workflow_runs_by_workflow(
        self,
        workflow_id: int,
    ) -> list[WorkflowRun]:
        """Получить все запуски конкретного workflow."""
        return await self.repository.list_by_workflow(workflow_id)

    async def delete_workflow_run(self, workflow_run: WorkflowRun) -> None:
        """Удалить запуск и зафиксировать транзакцию."""
        try:
            await self.repository.delete(workflow_run)
            await self.repository.session.commit()
        except IntegrityError:
            await self.repository.session.rollback()
            raise
