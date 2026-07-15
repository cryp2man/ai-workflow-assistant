from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Абстракция LLM-провайдера.

    Engine и сервисы зависят только от этого контракта;
    конкретные провайдеры (OpenAI, Claude, Gemini) реализуют его отдельно.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
    ) -> str:
        """Сгенерировать ответ LLM на переданный prompt."""
