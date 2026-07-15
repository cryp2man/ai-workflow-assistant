from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.api.v1.users import router as users_router
from src.api.v1.workflow_steps import router as workflow_steps_router
from src.api.v1.workflows import router as workflows_router
from src.core.lifespan import lifespan

app = FastAPI(
    title="AI Workflow Assistant API",
    version="1.0.0",
    description=(
        "Backend engine for multi-step AI workflows (llm / http / condition). "
        "Try it live in the interactive docs below."
    ),
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    """Корень ведёт на интерактивную документацию (удобно для демо-ссылки)."""
    return RedirectResponse(url="/docs")

app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(
    workflows_router, prefix="/api/v1/workflows", tags=["Workflows"]
)
app.include_router(
    workflow_steps_router, prefix="/api/v1/workflow-steps", tags=["Workflow Steps"]
)


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}