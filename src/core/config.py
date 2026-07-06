from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Workflow Assistant"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/ai_workflow"

settings = Settings()
