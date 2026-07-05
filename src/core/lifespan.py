from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from src.core.logging import setup_logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Application started")
    print("Application started")
    yield
    logger.info("Application stopped")
    print("Application stopped")
