import asyncio
import contextlib
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.config import settings
from src.core.logging import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Application started")

    # Telegram-бот стартует в фоне только при заданном BOT_TOKEN.
    # Отдельная задача: её падение не должно ронять API.
    bot_task: asyncio.Task | None = None
    if settings.BOT_TOKEN:
        from src.bot.main import run_bot

        bot_task = asyncio.create_task(run_bot())
        logger.info("Telegram bot task scheduled")

    yield

    if bot_task is not None:
        bot_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await bot_task

    logger.info("Application stopped")
