MODEL-001 - создать модель WorkflowRun.

ВАЖНО.

Работаем строго по принципу Surgical.

========================================

Разрешается изменить только

- src/db/models/workflow_run.py
- src/db/models/__init__.py

========================================

Запрещается менять

- Workflow
- User
- Repository
- Services
- API
- Dependencies
- Alembic
- Schemas
- Tests

========================================

Цель

Добавить новую модель WorkflowRun.

========================================

Создать файл

src/db/models/workflow_run.py

========================================

Модель должна содержать

id
    Integer
    primary_key=True

workflow_id
    ForeignKey("workflows.id")
    nullable=False
    index=True

status
    String(50)
    nullable=False

started_at
    DateTime(timezone=True)
    nullable=False
    default=datetime.utcnow

finished_at
    DateTime(timezone=True)
    nullable=True

result
    JSON
    nullable=True

error
    Text
    nullable=True

========================================

Связь

WorkflowRun

должен иметь relationship

workflow

back_populates="runs"

НЕ изменять Workflow.

Связь в Workflow будет добавлена отдельной задачей.

========================================

Обновить

src/db/models/__init__.py

добавив экспорт

WorkflowRun

========================================

После выполнения проверить

- import src.main

- uv run ruff check src/db/models

========================================

В отчёте указать

1. Какие поля добавлены.

2. Какие типы SQLAlchemy используются.

3. Почему relationship пока односторонний.

4. Проходит ли импорт проекта.

5. Результат Ruff.

Никаких дополнительных улучшений не делать.