from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.user import User
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """Репозиторий пользователей: минимальный CRUD.

    Транзакциями (commit/rollback) управляет вызывающий слой,
    репозиторий делает только flush.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, user: User) -> User:
        """Добавить пользователя в сессию и получить его id через flush."""
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        """Найти пользователя по первичному ключу."""
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Найти пользователя по Telegram ID."""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def list(self) -> list[User]:
        """Вернуть всех пользователей."""
        result = await self.session.execute(select(User))
        return list(result.scalars().all())

    async def delete(self, user: User) -> None:
        """Удалить пользователя из сессии с немедленным flush."""
        await self.session.delete(user)
        await self.session.flush()
