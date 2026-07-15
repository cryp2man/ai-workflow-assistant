"""
Project test fixtures.

Database fixtures
API fixtures
Repository fixtures

будут добавляться постепенно.
"""

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.db.base import Base
from src.db.models import (  # noqa: F401 — регистрируют таблицы в Base.metadata
    User,
    Workflow,
    WorkflowRun,
    WorkflowStep,
)

# Отдельная строка подключения для тестов — production Settings не используются.
# Тестовые креды, не имеющие отношения к production .env.
TEST_DATABASE_URL = (
    "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"
)


@pytest.fixture
async def test_engine():
    """Engine на время одного теста.

    Создается внутри event loop конкретного теста и утилизируется после него:
    пул asyncpg-соединений не переживает свой loop, иначе следующие тесты
    падают с "Event loop is closed" / "another operation is in progress".
    Схема создается идемпотентно (checkfirst) — тесты не зависят от ручной
    подготовки БД и работают в чистом контейнере CI.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine):
    """Открывает AsyncSession, отдает её тесту и закрывает после завершения."""
    session_factory = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    async with session_factory() as session:
        yield session
