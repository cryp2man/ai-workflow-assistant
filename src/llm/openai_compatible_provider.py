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
        self.settings = settings
        self._client: AsyncOpenAI | None = None

    def _get_client(self) -> AsyncOpenAI:
        """Ленивая инициализация клиента.

        Ключ проверяется здесь, а не в __init__: workflow из одних
        http/condition-шагов должен выполняться без LLM_API_KEY.
        """
        if self._client is None:
            if not self.settings.LLM_API_KEY:
                raise ValueError(
                    "LLM_API_KEY is not set. "
                    "Add it to the environment or switch LLM_PROVIDER to 'ollama'."
                )
            self._client = AsyncOpenAI(
                base_url=self.settings.LLM_BASE_URL,
                api_key=self.settings.LLM_API_KEY,
                timeout=self.settings.LLM_TIMEOUT,
            )
        return self._client

    async def generate(
        self,
        prompt: str,
    ) -> str:
        """Сгенерировать ответ LLM на переданный prompt."""
        response = await self._get_client().chat.completions.create(
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
