from fastapi import FastAPI
from src.api.v1.users import router as users_router
from src.api.v1.workflows import router as workflows_router # <--- ДОБАВИЛИ ИМПОРТ
from src.api.v1.workflow_steps import router as workflow_steps_router

app = FastAPI(
    title="AI Workflow Assistant API",
    version="1.0.0",
)

app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(workflows_router, prefix="/api/v1/workflows", tags=["Workflows"]) # <--- ПОДКЛЮЧИЛИ РОУТЕР
app.include_router(
    workflow_steps_router, prefix="/api/v1/workflow-steps", tags=["Workflow Steps"]
)

@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}