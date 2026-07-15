"""Наполнение БД демо-данными: пользователь + пример workflow.

Идемпотентно: повторный запуск не плодит дубли (ищет демо-пользователя
по email). Удобно для публичного демо, чтобы посетитель сразу увидел
готовый workflow и мог его запустить.

Запуск:  uv run python -m scripts.seed_demo
"""

import asyncio

from sqlalchemy import select

from src.db.models import User, Workflow, WorkflowStep
from src.db.session import AsyncSessionLocal

DEMO_EMAIL = "demo@example.com"

DEMO_STEPS = [
    ("Extract the request", "llm",
     "Extract the client's key request in one sentence: "
     "a client is looking for a 2-bedroom apartment near the sea, budget 150k"),
    ("Gate: is it real estate", "condition",
     "{{previous_response}} contains apartment"),
    ("Build an action checklist", "llm",
     "Turn this request into a 3-item action checklist for an agent:\n\n"
     "{{previous_response}}"),
]


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        existing = await session.execute(
            select(User).where(User.email == DEMO_EMAIL)
        )
        if existing.scalar_one_or_none() is not None:
            print(f"Demo user {DEMO_EMAIL} already exists — skipping seed.")
            return

        user = User(username="demo", email=DEMO_EMAIL, telegram_id=1000000001)
        session.add(user)
        await session.flush()

        workflow = Workflow(
            title="Real estate lead → action checklist",
            description="Demo workflow: LLM extract → condition gate → LLM checklist",
            user_id=user.id,
        )
        session.add(workflow)
        await session.flush()

        for order, (title, step_type, prompt) in enumerate(DEMO_STEPS, start=1):
            session.add(
                WorkflowStep(
                    workflow_id=workflow.id,
                    title=title,
                    prompt=prompt,
                    step_order=order,
                    step_type=step_type,
                )
            )

        await session.commit()
        print(
            f"Seeded demo user id={user.id}, workflow id={workflow.id} "
            f"with {len(DEMO_STEPS)} steps.\n"
            f"Run it: POST /api/v1/workflows/{workflow.id}/execute"
        )


if __name__ == "__main__":
    asyncio.run(seed())
