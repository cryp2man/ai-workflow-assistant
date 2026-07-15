from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.workflow import Workflow
from src.repositories.base import BaseRepository


class WorkflowRepository(BaseRepository):
    """Репозиторий рабочих процессов: минимальный CRUD.

    Транзакциями (commit/rollback) управляет вызывающий слой,
    репозиторий делает только flush.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, workflow: Workflow) -> Workflow:
        """Добавить workflow в сессию и получить его id через flush."""
        self.session.add(workflow)
        await self.session.flush()
        return workflow

    async def get_by_id(self, workflow_id: int) -> Workflow | None:
        """Найти workflow по первичному ключу."""
        result = await self.session.execute(
            select(Workflow).where(Workflow.id == workflow_id)
        )
        return result.scalar_one_or_none()

    async def list(self) -> list[Workflow]:
        """Вернуть все workflows."""
        result = await self.session.execute(select(Workflow))
        return list(result.scalars().all())

    async def list_by_user(self, user_id: int) -> list[Workflow]:
        """Вернуть все workflows пользователя."""
        result = await self.session.execute(
            select(Workflow).where(Workflow.user_id == user_id)
        )
        return list(result.scalars().all())

    async def delete(self, workflow: Workflow) -> None:
        """Удалить workflow из сессии с немедленным flush."""
        await self.session.delete(workflow)
        await self.session.flush()
