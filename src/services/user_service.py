from sqlalchemy.exc import IntegrityError

from src.db.models.user import User
from src.repositories.user_repository import UserRepository


class UserService:
    """Сервис пользователей: бизнес-логика и управление транзакциями.

    Repository только выполняет операции с данными (flush),
    границы транзакции (commit/rollback) — ответственность сервиса.
    """

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def create_user(self, user: User) -> User:
        """Создать пользователя и зафиксировать транзакцию."""
        try:
            user = await self.repository.create(user)
            await self.repository.session.commit()
        except IntegrityError:
            await self.repository.session.rollback()
            raise
        return user

    async def get_user(self, user_id: int) -> User | None:
        """Получить пользователя по id."""
        return await self.repository.get_by_id(user_id)

    async def get_user_by_telegram(self, telegram_id: int) -> User | None:
        """Получить пользователя по Telegram ID."""
        return await self.repository.get_by_telegram_id(telegram_id)

    async def list_users(self) -> list[User]:
        """Получить всех пользователей."""
        return await self.repository.list()

    async def delete_user(self, user: User) -> None:
        """Удалить пользователя и зафиксировать транзакцию."""
        try:
            await self.repository.delete(user)
            await self.repository.session.commit()
        except IntegrityError:
            await self.repository.session.rollback()
            raise
