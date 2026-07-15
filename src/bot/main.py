"""Точка входа Telegram-бота.

Запускается двумя способами:
- как фоновая задача внутри FastAPI (см. lifespan), если задан BOT_TOKEN;
- как отдельный процесс: `python -m src.bot.main`.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.bot.handlers import router
from src.core.config import settings

logger = logging.getLogger(__name__)


async def run_bot() -> None:
    """Запустить long-polling бота. Ошибки логируются, но не пробрасываются,
    чтобы падение бота не роняло основное приложение."""
    if not settings.BOT_TOKEN:
        logger.warning("BOT_TOKEN is not set — Telegram bot disabled.")
        return
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    try:
        logger.info("Starting Telegram bot polling")
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        raise
    except Exception:
        logger.exception("Telegram bot stopped with an error")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(run_bot())
