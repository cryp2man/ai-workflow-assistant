# FEATURE-006 — Template Variables in Workflow Steps

## Мотивация

Живой тест (2026-07-15, Groq / llama-3.3-70b-versatile) показал: захардкоженный
в ExecutionEngine формат `{prompt}\n\nPrevious response:\n\n{response}`
модель игнорирует примерно в 50% прогонов — фраза «previous answer» в
инструкции заставляет её искать контекст в истории чата, а не в теле промпта.

Решение — явные шаблонные переменные: автор шага сам решает, куда вставить
контекст. Так работают все современные workflow-платформы (n8n, Dify, Langflow).

## Цель

Шаги могут использовать в тексте промпта переменные:

- `{{previous_response}}` — ответ предыдущего шага
- `{{stepN}}` — ответ шага с step_order = N (например `{{step1}}`)
- `{{workflow_name}}` — название workflow

Перед отправкой в LLM PromptBuilder заменяет переменные на значения.
Неизвестные переменные остаются в тексте без изменений.

## Объём изменений

Изменять только:

- `src/prompts/builder.py` — `build_prompt(prompt, variables: dict[str, str] | None) -> str`
- `src/engine/execution_engine.py` — словарь `variables` в цикле выполнения;
  автоматическое приклеивание «Previous response:» удалить

Дополнительно (решение при выполнении): сохранять ответ каждого шага в
`WorkflowRun.result["steps"]` — колонка уже JSON, миграция не нужна.

Не менять: API, Repository, Service, Models, Database.
Никаких новых библиотек — только стандартный Python.

## Критерии готовности

- [x] Юнит-тесты PromptBuilder (`tests/prompts/`)
- [x] `uv run pytest` зелёный
- [x] `uv run ruff check` — новые файлы без ошибок
- [x] Живой прогон: 5/5 запусков workflow передают контекст (до фикса — ~50%)
- [x] `WorkflowRun.result` содержит ответы всех шагов
