from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Workflow Assistant"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Обязательная переменная окружения (без хардкода)
    DATABASE_URL: str

    @field_validator("DATABASE_URL")
    @classmethod
    def use_asyncpg_driver(cls, value: str) -> str:
        """Приводим URL к async-драйверу asyncpg.

        Хостинги (Railway, Heroku) выдают DATABASE_URL в формате
        `postgres://` или `postgresql://` — SQLAlchemy async требует
        явного `postgresql+asyncpg://`.
        """
        if value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql+asyncpg://", 1)
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+asyncpg://", 1)
        return value

    # Выбор LLM-провайдера: "openai_compatible" (облачный API) или "ollama"
    LLM_PROVIDER: str = "openai_compatible"

    # Облачный OpenAI-совместимый API (Groq, Google AI Studio, GitHub Models)
    LLM_BASE_URL: str = "https://api.groq.com/openai/v1"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    LLM_TIMEOUT: int = 120

    # Ollama (OpenAI-совместимый локальный LLM, fallback для офлайн-работы)
    OLLAMA_BASE_URL: str = "http://localhost:11434/v1"
    OLLAMA_MODEL: str = "qwen3:8b"
    OLLAMA_TIMEOUT: int = 120

    # Telegram-бот: если пусто — бот не запускается (например, локально и в CI)
    BOT_TOKEN: str = ""

    # Читаем .env из корня проекта
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()