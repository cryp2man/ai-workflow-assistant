"""Тесты UserRepository: create, get_by_id, get_by_telegram_id, list.

Требуется существующая test_db (см. TEST_DATABASE_URL в conftest.py).
delete() пока не тестируется — по заданию TEST-004.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.user import User
from src.repositories.user_repository import UserRepository


def make_user() -> User:
    """Уникальный пользователь: в conftest нет rollback/truncate,
    поэтому значения уникальных полей не должны повторяться между запусками."""
    suffix = uuid.uuid4().hex[:12]
    return User(
        username=f"user_{suffix}",
        email=f"{suffix}@test.com",
        telegram_id=int(uuid.uuid4().int % 10**12),
    )


async def test_create_assigns_id(db_session: AsyncSession):
    repo = UserRepository(db_session)
    user = make_user()

    created = await repo.create(user)

    assert created.id is not None
    assert created.username == user.username
    assert created.email == user.email
    assert created.telegram_id == user.telegram_id


async def test_get_by_id_returns_user(db_session: AsyncSession):
    repo = UserRepository(db_session)
    created = await repo.create(make_user())

    found = await repo.get_by_id(created.id)

    assert found is not None
    assert found.id == created.id
    assert found.email == created.email


async def test_get_by_id_returns_none_for_missing(db_session: AsyncSession):
    repo = UserRepository(db_session)

    found = await repo.get_by_id(-1)

    assert found is None


async def test_get_by_telegram_id_returns_user(db_session: AsyncSession):
    repo = UserRepository(db_session)
    created = await repo.create(make_user())

    found = await repo.get_by_telegram_id(created.telegram_id)

    assert found is not None
    assert found.id == created.id


async def test_get_by_telegram_id_returns_none_for_missing(
    db_session: AsyncSession,
):
    repo = UserRepository(db_session)

    found = await repo.get_by_telegram_id(-1)

    assert found is None


async def test_list_contains_created_user(db_session: AsyncSession):
    repo = UserRepository(db_session)
    created = await repo.create(make_user())

    users = await repo.list()

    assert isinstance(users, list)
    assert any(u.id == created.id for u in users)
