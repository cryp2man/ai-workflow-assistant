from openai import AsyncOpenAI

from src.core.config import Settings
from src.llm.base import BaseLLMProvider


class OpenAICompatibleProvider(BaseLLMProvider):
    """LLM-провайдер для любого OpenAI-совместимого облачного API.

    Работает с бесплатными провайдерами (Groq, Google AI Studio,
    GitHub Models и др.) — конкретный сервис задаётся через
    LLM_BASE_URL / LLM_API_KEY / LLM_MODEL в настройках.
    """

    def __init__(self, settings: Settings) -> None:
        if not settings.LLM_API_KEY:
            raise ValueError(
                "LLM_API_KEY is not set. "
                "Add it to .env or switch LLM_PROVIDER to 'ollama'."
            )
        self.settings = settings
        self.client = AsyncOpenAI(
            base_url=settings.LLM_BASE_URL,
            api_key=settings.LLM_API_KEY,
            timeout=settings.LLM_TIMEOUT,
        )

    async def generate(
        self,
        prompt: str,
    ) -> str:
        """Сгенерировать ответ LLM на переданный prompt."""
        response = await self.client.chat.completions.create(
            model=self.settings.LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        content = response.choices[0].message.content
        if content is None:
            return ""
        return content
