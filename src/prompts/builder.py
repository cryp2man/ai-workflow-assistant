class PromptBuilder:
    """Слой формирования промптов для LLM.

    Пока passthrough: шаблоны, контекст workflow и системные
    инструкции появятся в следующих задачах.
    """

    def build_prompt(
        self,
        prompt: str,
    ) -> str:
        """Собрать итоговый prompt из пользовательского ввода."""
        return prompt
