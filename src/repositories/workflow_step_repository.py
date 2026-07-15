from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.workflow_step import WorkflowStep
from src.repositories.base import BaseRepository


class WorkflowStepRepository(BaseRepository):
    """Репозиторий шагов workflow: минимальный CRUD.

    Транзакциями (commit/rollback) управляет вызывающий слой,
    репозиторий делает только flush.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, step: WorkflowStep) -> WorkflowStep:
        """Добавить шаг в сессию и получить его id через flush."""
        self.session.add(step)
        await self.session.flush()
        return step

    async def get_by_id(self, step_id: int) -> WorkflowStep | None:
        """Найти шаг по первичному ключу."""
        result = await self.session.execute(
            select(WorkflowStep).where(WorkflowStep.id == step_id)
        )
        return result.scalar_one_or_none()

    async def list(self) -> list[WorkflowStep]:
        """Вернуть все шаги."""
        result = await self.session.execute(select(WorkflowStep))
        return list(result.scalars().all())

    async def list_by_workflow(self, workflow_id: int) -> list[WorkflowStep]:
        """Вернуть шаги конкретного workflow в порядке step_order ASC."""
        result = await self.session.execute(
            select(WorkflowStep)
            .where(WorkflowStep.workflow_id == workflow_id)
            .order_by(WorkflowStep.step_order)
        )
        return list(result.scalars().all())

    async def delete(self, step: WorkflowStep) -> None:
        """Удалить шаг из сессии с немедленным flush."""
        await self.session.delete(step)
        await self.session.flush()
