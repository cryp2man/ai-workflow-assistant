# FEATURE-004 - Реальное выполнение Workflow через API

## Цель

Сделать так, чтобы проект можно было показать на собеседовании.

После выполнения задачи должно работать следующее:
POST /workflows/{id}/execute
        ↓
ExecutionEngine
        ↓
Workflow Steps
        ↓
PromptBuilder
        ↓
Ollama (qwen3:8b)
        ↓
WorkflowRun
        ↓
GET /workflows/{id}/runs

То есть весь pipeline должен реально выполняться.

## Что нужно сделать

### 1. Проверить интеграцию OllamaProvider

Убедиться, что:

```
await OllamaProvider.generate(...)
```

реально обращается к локальному Ollama.

Никаких mock.

Никаких заглушек.

Использовать текущий

```
OLLAMA_BASE_URL
OLLAMA_MODEL
```

из Settings.

---

### 2. Проверить PromptBuilder

Если сейчас build_prompt() просто возвращает строку —

ничего не менять.

Использовать как есть.
### 3. Проверить полный pipeline

Создать вручную через БД или через существующие API:

```
Workflow
```

например

```
Title:
Simple Test
```

и два шага

Step 1

```
Translate to English:
Привет мир
```

Step 2

```
Summarize previous answer in one sentence.
```

---

### 4. Выполнить

```
POST /api/v1/workflows/{id}/execute
```

---

### 5. Проверить

Убедиться что:

WorkflowRun создаётся

↓

становится running

↓

выполняются оба шага

↓

становится completed

↓

в result сохраняется ответ последнего шага

---

### 6. Проверить endpoint

```
GET /api/v1/workflows/{id}/runs
```

Должен вернуть этот запуск.

---

### 7. Если что-то не работает

Исправлять можно только реальные ошибки интеграции.

Не менять архитектуру.

Не добавлять новые классы.

Не менять Engine.

Не менять Repository.

Не менять Service.

Не добавлять retry.

Не менять PromptBuilder.

---

## Проверки

Обязательно выполнить

```
uv run ruff check src
```

```
import src.main
```

---

## Отчёт

После выполнения написать:

1. Получилось ли реально выполнить Workflow.
2. Какой prompt ушёл в Ollama.
3. Какой ответ вернула модель.
4. Что сохранилось в WorkflowRun.result.
5. Что вернул GET /runs.
6. Проходит ли import.
7. Результат Ruff.
8. Если что-то пришлось исправить — перечислить.