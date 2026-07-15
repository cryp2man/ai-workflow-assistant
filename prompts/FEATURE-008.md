# FEATURE-008 — Condition Step Type

## Цель

Третий тип шага — `condition`. Работает как «ворота»/фильтр в n8n:
проверяет выражение против контекста выполнения и, если условие ложно,
останавливает workflow (оставшиеся шаги пропускаются).

Это делает движок ветвящимся, а не строго линейным — базовый паттерн
любой automation-платформы.

## Что сделано

- `src/engine/conditions.py` — безопасное вычисление условий без `eval`:
  выражение `LEFT <op> RIGHT`, операторы `contains`, `not_contains`,
  `==`, `!=`; операнды поддерживают `{{переменные}}` контекста
- ExecutionEngine: condition-шаг обрабатывается до generic-ветки;
  при провале — `break`, статус запуска `stopped`, в `result.stopped_reason`
  записывается номер шага
- Схема: `condition` добавлен в `StepType` (Literal)

## Не менялось

БД/модель (step_type — открытая строка, миграция не нужна),
Repository, Service, HTTP/LLM-логика.

## Критерии готовности

- [x] Юнит-тесты `tests/engine/test_conditions.py` (contains/not_contains/==/!=,
  приоритет not_contains над contains, отсутствие оператора → ошибка)
- [x] `uv run pytest` зелёный (31 тест), ruff по изменённым файлам чистый
- [x] Живой e2e — условие ложно: workflow останавливается (`stopped`),
  следующий шаг пропущен
- [x] Живой e2e — условие истинно: workflow доходит до конца (`completed`)
