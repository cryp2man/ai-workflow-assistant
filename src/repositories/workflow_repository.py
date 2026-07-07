from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.base import BaseRepository


class WorkflowRepository(BaseRepository):
    """Репозиторий рабочих процессов. Пока только конструктор."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
