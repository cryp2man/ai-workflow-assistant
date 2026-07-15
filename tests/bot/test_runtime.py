"""Тесты логики бота на in-memory SQLite (без Telegram)."""

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.bot.runtime import create_demo_workflow, get_or_create_user
from src.db.base import Base
from src.db.models import User, Workflow, WorkflowStep  # noqa: F401


@pytest.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with factory() as s:
        yield s
    await engine.dispose()


class TestGetOrCreateUser:
    async def test_creates_new_user(self, session: AsyncSession):
        user = await get_or_create_user(session, telegram_id=42, username="neo")
        assert user.id is not None
        assert user.telegram_id == 42
        assert user.username == "neo"

    async def test_returns_existing_user(self, session: AsyncSession):
        first = await get_or_create_user(session, telegram_id=42, username="neo")
        again = await get_or_create_user(session, telegram_id=42, username="neo")
        assert again.id == first.id

    async def test_synthesizes_username_when_missing(
        self, session: AsyncSession
    ):
        user = await get_or_create_user(session, telegram_id=7, username=None)
        assert user.username == "tg_7"


class TestCreateDemoWorkflow:
    async def test_creates_workflow_with_steps(self, session: AsyncSession):
        user = await get_or_create_user(session, telegram_id=1, username="u")
        workflow = await create_demo_workflow(session, user.id)

        assert workflow.id is not None
        assert workflow.user_id == user.id
