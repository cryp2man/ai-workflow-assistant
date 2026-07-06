# DB-001 - Database Foundation

## Контекст

Проект AI Workflow Assistant.

Уже реализовано:

- Project Setup
- FastAPI
- Application Core
- API Structure
- Health Endpoint

Архитектурные решения уже утверждены и изменению не подлежат.

Используем:

- PostgreSQL
- SQLAlchemy 2.x (Async)
- AsyncSession
- pydantic-settings

Repository Pattern НЕ использовать.

---

## Цель

Подготовить инфраструктуру для работы с PostgreSQL.

На данном этапе НЕ выполнять подключение к реальной базе данных и НЕ создавать модели.

---

## Необходимо выполнить

### 1. Создать структуру

src/db/

base.py

session.py

__init__.py

---

### 2. base.py

Создать общий базовый класс:

Base(DeclarativeBase)

Без моделей.

---

### 3. session.py

Создать:

- Async Engine
- async_sessionmaker
- функцию получения AsyncSession

Использовать SQLAlchemy 2.x.

Подключение должно использовать DATABASE_URL из Settings.

---

### 4. config.py

Добавить новое поле:

DATABASE_URL

используя pydantic-settings.

---

### 5. .env.example

Добавить пример:

DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/database

---

### 6. Проверить импорт

Проект должен запускаться:

uv run uvicorn src.main:app --reload

Без подключения к реальной БД.

Engine создается, но соединение не открывается до первого запроса.

---

## Не делать

НЕ создавать:

- модели
- таблицы
- Alembic
- CRUD
- запросы
- репозитории
- тестовые данные

---

## Acceptance Criteria

После выполнения:

✔ приложение запускается

✔ Swagger работает

✔ ошибок импорта нет

✔ DATABASE_URL читается из Settings

✔ AsyncSession создается корректно

---

## Отчет

После выполнения предоставить:

1. Какие файлы созданы.
2. Какие файлы изменены.
3. Какие библиотеки использованы.
4. Были ли отклонения.
5. Что можно улучшить позже.