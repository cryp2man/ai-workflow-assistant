from openai import AsyncOpenAI

from src.core.config import Settings
from src.llm.base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    """LLM-провайдер на базе локального Ollama (OpenAI-совместимый API)."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = AsyncOpenAI(
            base_url=settings.OLLAMA_BASE_URL,
            api_key="ollama",
            timeout=settings.OLLAMA_TIMEOUT,
        )

    async def generate(
        self,
        prompt: str,
    ) -> str:
        """Сгенерировать ответ LLM на переданный prompt."""
        response = await self.client.chat.completions.create(
            model=self.settings.OLLAMA_MODEL,
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
