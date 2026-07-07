from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """Репозиторий пользователей. Пока только конструктор."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
