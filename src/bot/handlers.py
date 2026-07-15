"""Обработчики Telegram-бота (aiogram v3).

Бот — интерфейс к workflow-движку: регистрация по Telegram ID, список
workflow пользователя, запуск по кнопке с показом результата по шагам.
"""

import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.runtime import (
    build_engine,
    create_demo_workflow,
    get_or_create_user,
)
from src.db.session import AsyncSessionLocal
from src.repositories.workflow_repository import WorkflowRepository
from src.services.workflow_service import WorkflowService

logger = logging.getLogger(__name__)
router = Router()

HELP_TEXT = (
    "AI Workflow Assistant — бот-интерфейс к движку workflow.\n\n"
    "/workflows — мои workflow (запуск по кнопке)\n"
    "/demo — создать демо-workflow (LLM → условие → LLM)\n"
    "/help — помощь"
)

MAX_STEP_CHARS = 500


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        await get_or_create_user(
            session, message.from_user.id, message.from_user.username
        )
    await message.answer(
        "Привет! Я запускаю AI-workflow прямо из Telegram.\n\n" + HELP_TEXT
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT)


@router.message(Command("demo"))
async def cmd_demo(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        user = await get_or_create_user(
            session, message.from_user.id, message.from_user.username
        )
        workflow = await create_demo_workflow(session, user.id)
    await message.answer(
        f"Создан демо-workflow «{workflow.title}».\n"
        "Открой /workflows и запусти его кнопкой."
    )


@router.message(Command("workflows"))
async def cmd_workflows(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        user = await get_or_create_user(
            session, message.from_user.id, message.from_user.username
        )
        service = WorkflowService(WorkflowRepository(session))
        workflows = await service.list_user_workflows(user.id)

    if not workflows:
        await message.answer(
            "У тебя пока нет workflow. Создай демо командой /demo."
        )
        return

    builder = InlineKeyboardBuilder()
    for wf in workflows:
        builder.button(text=f"▶️ {wf.title}", callback_data=f"run:{wf.id}")
    builder.adjust(1)
    await message.answer("Твои workflow:", reply_markup=builder.as_markup())


@router.callback_query(lambda c: c.data and c.data.startswith("run:"))
async def run_workflow(callback: CallbackQuery) -> None:
    workflow_id = int(callback.data.split(":", 1)[1])
    await callback.answer()
    await callback.message.answer(f"Запускаю workflow #{workflow_id}…")
    try:
        async with AsyncSessionLocal() as session:
            # callback_data подделываема, поэтому проверяем владельца:
            # пользователь может запускать только свои workflow (защита от IDOR).
            user = await get_or_create_user(
                session, callback.from_user.id, callback.from_user.username
            )
            service = WorkflowService(WorkflowRepository(session))
            workflow = await service.get_workflow(workflow_id)
            if workflow is None or workflow.user_id != user.id:
                await callback.message.answer("Workflow не найден.")
                return
            engine = build_engine(session)
            run = await engine.execute_workflow(workflow_id)
    except ValueError:
        await callback.message.answer("Workflow не найден.")
        return
    except Exception:
        logger.exception("Workflow %s execution failed", workflow_id)
        await callback.message.answer(
            "Во время выполнения произошла ошибка. Проверь настройки LLM."
        )
        return

    lines = [f"Статус: {run.status}"]
    for step in run.result.get("steps", []):
        response = step["response"]
        if len(response) > MAX_STEP_CHARS:
            response = response[:MAX_STEP_CHARS] + "…"
        lines.append(f"\n[{step['step_order']}] {step['title']}:\n{response}")
    await callback.message.answer("\n".join(lines))
