
Контекст проекта

Python 3.12
FastAPI
SQLAlchemy 2.x
Async
Ollama
ExecutionEngine уже умеет:
- создавать WorkflowRun
- выполнять шаги
- передавать ответ предыдущего шага
- сохранять completed / failed

Нужно реализовать логирование выполнения каждого шага.

=========================
ЗАДАЧА
=========================

Изменять можно ТОЛЬКО:

src/engine/execution_engine.py

Больше ничего менять нельзя.

=========================
Что нужно сделать
=========================

Перед выполнением каждого шага вывести лог:

Executing step {step.step_order}: {step.title}

После успешного выполнения:

Step completed: {step.step_order}

При ошибке:

Step failed: {step.step_order}

Использовать обычный logging.

НЕ использовать print().

Если logger в файле отсутствует - создать

logger = logging.getLogger(__name__)

Импортировать logging.

=========================
Важно
=========================

Не менять:

WorkflowRun

Repository

Service

PromptBuilder

LLM Provider

Schemas

Database

API

Tests

=========================
После выполнения предоставить отчет

1. Какие строки изменены

2. Где создается logger

3. Какие сообщения теперь появляются

4. Почему используется logging вместо print

5. Проходит ли

import src.main

6. uv run ruff check src/engine

Никаких дополнительных улучшений не делать.