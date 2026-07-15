# FEATURE-007 — HTTP Step Type

## Цель

Шаги workflow перестают быть только LLM-промптами. Новый тип шага `http`
позволяет забирать данные из внешних API и передавать их следующим шагам
через переменные контекста — базовый паттерн всех automation-платформ.

## Что сделано

- `WorkflowStep.step_type` (`llm` | `http`, default `llm`) + миграция
  с `server_default='llm'` для существующих строк
- Схемы: `step_type` в Create/Update/Response (`Literal["llm", "http"]`)
- ExecutionEngine: диспетчеризация `_execute_step` по типу шага
  - `http`: GET по URL из поля `prompt` (после подстановки переменных),
    тело ответа уходит в контекст; таймаут 30 c, ответ обрезается
    до 10 000 символов
  - `llm`: как раньше, через `BaseLLMProvider`
- Новая явная зависимость: `httpx`

### SSRF-защита (по итогам security-review)

URL шага задаётся пользователем, поэтому перед запросом валидируем
(`validate_http_step_url`):
- только схемы `http`/`https`;
- резолвим хост и отклоняем loopback / private / link-local
  (метадата облака 169.254.169.254) / multicast / reserved;
- редиректы отключены (иначе редирект на внутренний адрес обошёл бы проверку);
- отклонённый URL → HTTP 400 (`UnsafeUrlError`).
Тесты: `tests/engine/test_url_validation.py`.

## Не менялось

Repository, Service, WorkflowRun, API-роутеры (кроме проброса поля).

## Критерии готовности

- [x] Миграция применяется, существующие шаги получают тип `llm`
- [x] `uv run pytest` зелёный, ruff по изменённым файлам чистый
- [x] Живой e2e: workflow «HTTP (api.github.com/zen) → LLM (объясни
  {{previous_response}})» выполняется, оба ответа в истории запуска
