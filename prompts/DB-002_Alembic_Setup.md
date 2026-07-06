# DB-002 - Alembic Setup

## Контекст

Проект AI Workflow Assistant.

Уже реализовано:

- Project Setup
- FastAPI
- Application Core
- API Structure
- Health Endpoint
- Database Foundation

Архитектура базы данных утверждена.

Используем:

- PostgreSQL
- SQLAlchemy 2.x
- AsyncEngine
- AsyncSession
- Alembic

Repository Pattern НЕ использовать.

---

## Цель

Подготовить Alembic для дальнейших миграций.

На этом этапе НЕ создавать модели и НЕ выполнять миграции.

---

## Необходимо выполнить

### 1. Инициализировать Alembic

Если каталог уже существует - использовать его.

---

### 2. Настроить alembic.ini

Использовать DATABASE_URL из Settings.

Не дублировать URL вручную.

---

### 3. Настроить env.py

Использовать Base.metadata.

Подготовить поддержку AsyncEngine.

---

### 4. Проверить

Команда:

alembic current

должна запускаться без ошибок.

Если миграций ещё нет - это нормально.

---

## Не делать

НЕ создавать:

- модели
- таблицы
- миграции
- revision
- upgrade
- downgrade
- тестовые данные

---

## Acceptance Criteria

После выполнения:

✔ Alembic настроен.

✔ env.py использует Base.metadata.

✔ DATABASE_URL читается из Settings.

✔ alembic current работает.

---

## Отчет

После выполнения предоставить:

1. Какие файлы созданы.
2. Какие изменены.
3. Какие команды были выполнены.
4. Были ли отклонения.
5. Какие рекомендации для следующего этапа.