ENGINE-002 - первая реализация ExecutionEngine

Контекст проекта

FastAPI
SQLAlchemy 2.x

Уже существуют:

- WorkflowService
- WorkflowRunService
- WorkflowRun model
- ExecutionEngine

Необходимо реализовать первую рабочую бизнес-логику движка.

========================================

Работаем строго по принципу Surgical.

Разрешается изменить только

src/engine/execution_engine.py

========================================

Метод

execute_workflow()

больше не должен быть заглушкой.

========================================

Пока никакого LLM.

Никаких HTTP-запросов.

Никаких AI.

========================================

Алгоритм

1. Получить Workflow через workflow_service.get_workflow() если Workflow отсутствует - raise ValueError("Workflow not found")

========================================

2. Создать объект WorkflowRun со значениями workflow_id = workflow.id

status = "running"

started_at = datetime.utcnow()

finished_at = None

result = None

error = None

========================================

3. Передать его в

workflow_run_service.create_workflow_run()

========================================

4. После успешного создания вернуть созданный WorkflowRun

========================================

Сейчас

никаких completed

никаких failed

никаких update

никаких LLM

никаких try/except

никакой обработки ошибок.

========================================

Использовать существующие модели.

Никаких изменений

Repository

Service

Models

Schemas

Alembic

API

не делать.

========================================

После выполнения проверить

import src.main

uv run ruff check src/engine

========================================

В отчёте указать

1. Что изменилось.

2. Как теперь работает execute_workflow().

3. Почему пока используется только статус running.

4. Почему пока нет try/except.

5. Почему WorkflowRun сразу сохраняется в БД.

6. Проходит ли импорт.

7. Результат Ruff.

Никаких дополнительных улучшений не выполнять.