from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.workflow_run import WorkflowRun
from src.repositories.base import BaseRepository


class WorkflowRunRepository(BaseRepository):
    """Репозиторий запусков workflow: минимальный CRUD.

    Транзакциями (commit/rollback) управляет вызывающий слой,
    репозиторий делает только flush.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, workflow_run: WorkflowRun) -> WorkflowRun:
        """Добавить запуск в сессию и получить его id через flush."""
        self.session.add(workflow_run)
        await self.session.flush()
        return workflow_run

    async def get_by_id(self, run_id: int) -> WorkflowRun | None:
        """Найти запуск по первичному ключу."""
        result = await self.session.execute(
            select(WorkflowRun).where(WorkflowRun.id == run_id)
        )
        return result.scalar_one_or_none()

    async def list(self) -> list[WorkflowRun]:
        """Вернуть все запуски."""
        result = await self.session.execute(select(WorkflowRun))
        return list(result.scalars().all())

    async def list_by_workflow(self, workflow_id: int) -> list[WorkflowRun]:
        """Вернуть все запуски конкретного workflow."""
        result = await self.session.execute(
            select(WorkflowRun).where(WorkflowRun.workflow_id == workflow_id)
        )
        return list(result.scalars().all())

    async def delete(self, workflow_run: WorkflowRun) -> None:
        """Удалить запуск из сессии с немедленным flush."""
        await self.session.delete(workflow_run)
        await self.session.flush()
