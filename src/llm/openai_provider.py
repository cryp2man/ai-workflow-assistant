from openai import AsyncOpenAI

from src.llm.base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    """LLM-провайдер на базе локального Ollama (OpenAI-совместимый API)."""

    def __init__(self, api_key: str) -> None:
        self.client = AsyncOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )

    async def generate(
        self,
        prompt: str,
    ) -> str:
        """Сгенерировать ответ LLM на переданный prompt."""
        response = await self.client.chat.completions.create(
            model="qwen3:8b",
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
