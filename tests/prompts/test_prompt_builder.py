from src.prompts.builder import PromptBuilder


class TestPromptBuilder:
    def setup_method(self) -> None:
        self.builder = PromptBuilder()

    def test_no_variables_returns_prompt_unchanged(self) -> None:
        assert self.builder.build_prompt("Hello world") == "Hello world"

    def test_none_variables_returns_prompt_unchanged(self) -> None:
        assert self.builder.build_prompt("Hello {{name}}", None) == "Hello {{name}}"

    def test_replaces_single_variable(self) -> None:
        result = self.builder.build_prompt("Hello {{name}}", {"name": "John"})
        assert result == "Hello John"

    def test_replaces_multiple_variables(self) -> None:
        result = self.builder.build_prompt(
            "Workflow: {{workflow_name}}\n\nText: {{previous_response}}",
            {"workflow_name": "Demo", "previous_response": "Hello world"},
        )
        assert result == "Workflow: Demo\n\nText: Hello world"

    def test_replaces_repeated_variable(self) -> None:
        result = self.builder.build_prompt("{{x}} and {{x}}", {"x": "A"})
        assert result == "A and A"

    def test_unknown_variable_left_as_is(self) -> None:
        result = self.builder.build_prompt("Hello {{unknown}}", {"name": "John"})
        assert result == "Hello {{unknown}}"

    def test_step_variables(self) -> None:
        result = self.builder.build_prompt(
            "Compare {{step1}} with {{step2}}",
            {"step1": "first", "step2": "second"},
        )
        assert result == "Compare first with second"
