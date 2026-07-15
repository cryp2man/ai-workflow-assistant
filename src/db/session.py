from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings

# Создаем движок (Engine), который будет использовать правильный URL из настроек
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False
)

# Функция для FastAPI, которая выдает сессию на время запроса и потом закрывает её
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session