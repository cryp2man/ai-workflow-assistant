# TASK-004 - Application Core

## Контекст

Проект AI Workflow Assistant.

Уже реализовано:

- структура проекта;
- настройка uv;
- FastAPI;
- Swagger;
- ReDoc.

Следующий этап - создание ядра приложения.

---

## Цель

Подготовить инфраструктуру приложения для дальнейшего подключения базы данных, API и сервисов.

---

## Необходимо выполнить

Создать директорию:

src/core/

Создать файлы:

config.py
logging.py
lifespan.py

---

### config.py

Использовать pydantic-settings.

Создать класс Settings.

Добавить настройки:

PROJECT_NAME

API_VERSION

DEBUG

HOST

PORT

Создать объект:

settings = Settings()

---

### logging.py

Настроить стандартный logging.

Создать функцию:

setup_logging()

Пока использовать только консольный вывод.

Без сторонних библиотек.

---

### lifespan.py

Создать lifespan для FastAPI.

При запуске приложения:

- вывести лог
  "Application started"

При остановке:

- вывести лог
  "Application stopped"

Использовать современный механизм lifespan.

Не использовать @app.on_event().

---

### main.py

Подключить:

- settings
- lifespan

Название приложения должно браться из Settings.

Версия API также должна браться из Settings.

---

## Не делать

Не создавать:

- БД
- SQLAlchemy
- Alembic
- роутеры
- middleware
- зависимости
- сервисы
- Docker

---

## Acceptance Criteria

После выполнения:

uv run uvicorn src.main:app --reload

успешно запускается.

При запуске появляется сообщение:

Application started

При остановке:

Application stopped

Swagger продолжает работать.

---

## Отчет

После выполнения предоставить:

1. Какие файлы были созданы.
2. Какие файлы были изменены.
3. Какие библиотеки были добавлены.
4. Были ли отклонения от задания.
5. Какие улучшения можно сделать позже (не реализовывая их сейчас).