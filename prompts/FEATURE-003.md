# FEATURE-003 - Просмотр истории запусков Workflow

## Цель

После выполнения workflow пользователь должен иметь возможность посмотреть историю всех запусков.

Не изменять существующую архитектуру проекта.

## Что необходимо реализовать

### 1. WorkflowRunRepository

Добавить метод:
list_by_workflow(workflow_id: int) -> list[WorkflowRun]

если его ещё нет — использовать существующий.
### 2. WorkflowRunService

Если метода нет — добавить:
list_workflow_runs_by_workflow(workflow_id: int)
Без новой бизнес-логики.

Только делегирование в Repository.

### 3. Новый endpoint

Добавить:
GET /api/v1/workflows/{workflow_id}/runs
### 4. Endpoint должен:

Получить Execution не нужно.

Использовать только:
WorkflowRunService
через Depends.
### 5. Возвращать

JSON-массив:
[
  {
    "id": 5,
    "status": "completed",
    "started_at": "...",
    "finished_at": "...",
    "result": {
      "response": "..."
    },
    "error": null
  },
  {
    "id": 6,
    "status": "failed",
    "started_at": "...",
    "finished_at": "...",
    "result": null,
    "error": "Connection timeout"
  }
]

Никаких Pydantic Schema пока не создавать.

Можно вернуть обычный список словарей.

### 6. Если запусков нет

Вернуть [] НЕ 404.

### 7. Исключения

Новых исключений не добавлять.

Никакой новой бизнес-логики.

### 8. Не изменять

Запрещено менять:

- Engine
- LLM
- PromptBuilder
- Models
- Alembic
- WorkflowRun

## Проверки

После выполнения предоставить отчёт:

1. Какие файлы изменены.
2. Какой endpoint появился.
3. Как выглядит JSON ответа.
4. Что возвращается при отсутствии запусков.
5. Проходит ли: import src.main
6. Результат: 
uv run ruff check src
Если есть старые ошибки Ruff - перечислить только новые (если появились).
