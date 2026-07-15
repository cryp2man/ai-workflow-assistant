MODEL-002 - создать модель WorkflowStep

Контекст проекта

В проекте уже существуют:

- Workflow
- WorkflowRun
- ExecutionEngine
- PromptBuilder
- LLMProvider

Теперь необходимо подготовить модель шагов Workflow.

========================================

Работаем строго по принципу Surgical.

Разрешается изменить только

src/db/models/workflow_step.py

src/db/models/__init__.py

========================================

Не изменять

Workflow

WorkflowRun

Repositories

Services

API

Schemas

Engine

Alembic

Tests

========================================

Создать новую модель

WorkflowStep

таблица

workflow_steps

========================================

Поля

id

workflow_id

step_order

title

prompt

created_at

========================================

Типы

id

Primary Key

workflow_id

ForeignKey("workflows.id")

nullable=False

index=True

step_order

Integer

nullable=False

title

String(255)

nullable=False

prompt

Text

nullable=False

created_at

DateTime(timezone=True)

default=datetime.utcnow

nullable=False

========================================

Добавить relationship

workflow

без back_populates

(аналогично WorkflowRun)

========================================

Экспортировать WorkflowStep

через

src/db/models/__init__.py

========================================

После выполнения проверить

import src.main

uv run ruff check src/db/models

========================================

В отчёте указать

1. Какие поля созданы.

2. Почему пока нет back_populates.

3. Почему prompt хранится в БД.

4. Проходит ли импорт.

5. Результат Ruff.

Никаких дополнительных улучшений не выполнять.