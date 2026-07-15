ENGINE-005 - подключить LLM к ExecutionEngine

Контекст проекта

Уже существуют:

- ExecutionEngine
- PromptBuilder
- BaseLLMProvider
- OllamaProvider
- WorkflowService
- WorkflowRunService

Сейчас Engine формирует prompt, но никуда его не отправляет.

Необходимо впервые подключить LLM.

========================================

Работаем строго по принципу Surgical.

Разрешается изменить только

src/engine/execution_engine.py

========================================

Не изменять

Repositories

Services

Models

Schemas

API

Alembic

Tests

PromptBuilder

LLM

========================================

Изменить конструктор ExecutionEngine.

Добавить зависимость

llm_provider: BaseLLMProvider

и сохранить её в

self.llm_provider

========================================

После

prompt = self.prompt_builder.build_prompt(...)

вызвать

response = await self.llm_provider.generate(prompt)

========================================

При завершении WorkflowRun

вместо

result={
    "message": "Workflow executed successfully"
}

сохранить

result={
    "response": response
}

========================================

Больше ничего не менять.

Статусы running/completed остаются прежними.

Логика commit остаётся прежней.

Обработка ошибок не добавляется.

========================================

После выполнения проверить

import src.main

uv run ruff check src/engine

========================================

В отчёте указать

1. Какие изменения внесены.

2. Как теперь проходит полный цикл выполнения Workflow.

3. Почему Engine зависит от BaseLLMProvider, а не OllamaProvider.

4. Почему response сохраняется в WorkflowRun.result.

5. Проходит ли импорт.

6. Результат Ruff.

Если для выполнения потребуется менять другие файлы - остановиться и сообщить об этом, ничего не изменяя.

Никаких дополнительных улучшений не выполнять.