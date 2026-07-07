from fastapi import FastAPI
from src.api.v1.users import router as users_router # <--- ИМПОРТИРУЕМ РОУТЕР

app = FastAPI(
    title="AI Workflow Assistant API",
    version="1.0.0",
)

# Регистрируем роутер
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"]) # <--- ПОДКЛЮЧАЕМ ЕГО

@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}