import pytest

from src.engine.conditions import ConditionError, evaluate_condition


class TestEvaluateCondition:
    def test_contains_true(self) -> None:
        assert evaluate_condition(
            "{{previous_response}} contains world",
            {"previous_response": "Hello world"},
        )

    def test_contains_false(self) -> None:
        assert not evaluate_condition(
            "{{previous_response}} contains error",
            {"previous_response": "Hello world"},
        )

    def test_not_contains_true(self) -> None:
        assert evaluate_condition(
            "{{previous_response}} not_contains error",
            {"previous_response": "Hello world"},
        )

    def test_not_contains_not_confused_with_contains(self) -> None:
        # "not_contains" must win over "contains" when both substrings present
        assert not evaluate_condition(
            "{{x}} not_contains a",
            {"x": "banana"},
        )

    def test_equals_true(self) -> None:
        assert evaluate_condition("{{status}} == yes", {"status": "yes"})

    def test_equals_false(self) -> None:
        assert not evaluate_condition("{{status}} == yes", {"status": "no"})

    def test_not_equals_true(self) -> None:
        assert evaluate_condition("{{status}} != yes", {"status": "no"})

    def test_operands_are_trimmed(self) -> None:
        assert evaluate_condition("{{status}} == yes", {"status": "  yes  "})

    def test_literal_operands_without_variables(self) -> None:
        assert evaluate_condition("foo == foo", {})

    def test_missing_operator_raises(self) -> None:
        with pytest.raises(ConditionError):
            evaluate_condition("just some text", {})
