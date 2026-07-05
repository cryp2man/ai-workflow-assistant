from fastapi import FastAPI
from src.core.config import settings
from src.core.lifespan import lifespan
from src.api.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for AI Workflow Assistant",
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(api_router)
