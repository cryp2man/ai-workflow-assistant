class PromptBuilder:
    """Слой формирования промптов для LLM.

    Подставляет переменные контекста выполнения в шаблон промпта:
    {{previous_response}}, {{stepN}}, {{workflow_name}}.
    """

    def build_prompt(
        self,
        prompt: str,
        variables: dict[str, str] | None = None,
    ) -> str:
        """Собрать итоговый prompt, заменив {{переменные}} на значения.

        Неизвестные переменные остаются в тексте без изменений.
        """
        if not variables:
            return prompt
        for name, value in variables.items():
            prompt = prompt.replace(f"{{{{{name}}}}}", value)
        return prompt
