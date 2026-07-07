from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """Базовый класс слоя репозиториев.

    Пока содержит только инфраструктуру: хранение сессии.
    CRUD, SQL-запросы, commit/rollback здесь намеренно не реализованы.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
