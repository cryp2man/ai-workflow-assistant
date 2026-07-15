from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Workflow Assistant"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Мы убрали хардкод. Теперь Pydantic ОБЯЗАН найти эту переменную в окружении
    DATABASE_URL: str

    # Ollama (OpenAI-совместимый локальный LLM)
    OLLAMA_BASE_URL: str = "http://localhost:11434/v1"
    OLLAMA_MODEL: str = "qwen3:8b"
    OLLAMA_TIMEOUT: int = 120

    # Эта настройка говорит Pydantic: "Иди и прочитай файл .env в корне проекта"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()