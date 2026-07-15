"""Безопасное вычисление условий для condition-шагов workflow.

Выражение имеет форму `LEFT <op> RIGHT`, где LEFT/RIGHT могут содержать
переменные контекста ({{previous_response}}, {{stepN}}, {{workflow_name}}).
Никакого eval: только явный набор операторов над строками.
"""

from src.prompts.builder import PromptBuilder

# Порядок важен: более длинные/специфичные операторы проверяем первыми,
# чтобы "not_contains" не перепутался с "contains", а "!=" с "=".
_OPERATORS = ["not_contains", "contains", "==", "!="]

_prompt_builder = PromptBuilder()


class ConditionError(Exception):
    """Некорректное выражение condition-шага."""


def evaluate_condition(expression: str, variables: dict[str, str]) -> bool:
    """Вычислить условие вида `LEFT <op> RIGHT` против контекста.

    Поддерживаемые операторы: contains, not_contains, ==, !=.
    Операнды могут содержать {{переменные}}. Бросает ConditionError,
    если оператор не найден.
    """
    for op in _OPERATORS:
        token = f" {op} "
        if token in expression:
            raw_left, raw_right = expression.split(token, 1)
            left = _prompt_builder.build_prompt(raw_left, variables).strip()
            right = _prompt_builder.build_prompt(raw_right, variables).strip()
            return _apply(op, left, right)
    raise ConditionError(
        f"No supported operator found in condition: {expression!r}"
    )


def _apply(op: str, left: str, right: str) -> bool:
    if op == "contains":
        return right in left
    if op == "not_contains":
        return right not in left
    if op == "==":
        return left == right
    if op == "!=":
        return left != right
    raise ConditionError(f"Unsupported operator: {op!r}")
