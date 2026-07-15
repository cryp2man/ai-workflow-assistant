# AI Workflow Assistant — Tasks

Правило: одна задача → один коммит → проверка (ruff + pytest) → следующая.
Детальные спеки задач — в `prompts/`.

## Done

### Инфраструктура и фундамент
- [x] Структура проекта (uv), Ruff, pytest, .gitignore, .env.example
- [x] FastAPI-приложение, конфигурация (Pydantic Settings), логирование, lifespan
- [x] Health endpoint, версионирование API (`/api/v1`)
- [x] PostgreSQL + Docker Compose, SQLAlchemy 2.0 (async), Alembic
- [x] Dockerfile приложения + one-command deploy, GitHub Actions CI

### Архитектура
- [x] Repository layer (BaseRepository + репозитории сущностей)
- [x] Service layer (границы транзакций в сервисах)
- [x] Dependency Injection (`src/dependencies`)

### Домен и API
- [x] Модели: User, Workflow, WorkflowStep, WorkflowRun
- [x] CRUD API: users, workflows, workflow steps
- [x] Провайдер-архитектура LLM (облачные API + Ollama fallback)

### Движок
- [x] ExecutionEngine: последовательное выполнение шагов, история запусков
- [x] Шаблонные переменные контекста (`{{previous_response}}`, `{{stepN}}`, `{{workflow_name}}`)
- [x] Типы шагов: llm, http (с SSRF-защитой), condition (ворота)

### Качество
- [x] Тесты: unit (prompt builder, conditions, url validation) + integration (engine, repo)
- [x] Чистый ruff по src и tests, CI зелёный

## Next
- [ ] Telegram-бот как интерфейс (`src/bot`)
- [ ] Двусторонние связи Workflow.steps / Workflow.runs
- [ ] Расширение condition (числовые операторы, ветвление)
- [ ] Деплой на хостинг (Railway / Render) + публичная демо-ссылка
