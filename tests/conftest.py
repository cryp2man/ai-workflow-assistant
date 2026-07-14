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

# Отдельная строка подключения для тестов — production Settings не используются.
# test_user/test_db созданы вручную в контейнере ai-workflow-postgres (TEST-005),
# это локальные тестовые креды, не имеющие отношения к production .env.
TEST_DATABASE_URL = (
    "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"
)


@pytest.fixture
async def test_engine():
    """Engine на время одного теста.

    Создается внутри event loop конкретного теста и утилизируется после него:
    пул asyncpg-соединений не переживает свой loop, иначе следующие тесты
    падают с "Event loop is closed" / "another operation is in progress".
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
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
