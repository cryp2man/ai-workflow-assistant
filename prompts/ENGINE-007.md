
Работаем строго по спецификации проекта.

Контекст:

Сейчас ExecutionEngine выполняет шаги последовательно:

for step in steps:
    prompt = prompt_builder.build_prompt(step.prompt)
    response = await llm_provider.generate(prompt)

Но каждый шаг ничего не знает о предыдущем.

Необходимо реализовать передачу предыдущего результата между шагами.

Техническое задание:

Изменить только:

- src/engine/execution_engine.py

Больше ничего не изменять.

Что необходимо сделать:

1. Перед циклом создать переменную: previous_response = ""

2. Во время каждой итерации: если previous_response пустой - использовать prompt без изменений. если previous_response не пустой - формировать новый prompt следующим образом:

step.prompt

пустая строка

Previous response:

<previous_response>

То есть итоговый prompt должен выглядеть так:

<step.prompt>

Previous response:

<ответ предыдущего шага>

3. Получив ответ модели:

response = await llm_provider.generate(prompt)

сразу выполнить

previous_response = response

4. После окончания цикла в WorkflowRun.result по-прежнему сохранять

{
    "response": previous_response
}

Никаких других изменений.

Не добавлять:

- память
- список сообщений
- chat history
- conversation objects
- context manager
- PromptBuilder менять нельзя
- OllamaProvider менять нельзя
- WorkflowStep менять нельзя

Почему так:

Это первая версия "pipeline".

Каждый следующий шаг получает результат предыдущего.

Именно так строятся большинство workflow-систем (LangGraph, Haystack Pipelines, CrewAI Pipeline и т.д.).

Проверки:

1. import src.main проходит.

2. uv run ruff check src/engine без ошибок.

После выполнения предоставить отчёт:

1. Какие строки изменены.
2. Как теперь выглядит цикл выполнения.
3. Почему previous_response хранится отдельно от PromptBuilder.
4. Почему PromptBuilder не знает историю.
5. Проходит ли import.
6. Результат Ruff.

Никаких дополнительных улучшений не делать.