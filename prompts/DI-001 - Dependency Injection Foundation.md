
## Цель

Создать централизованный слой Dependency Injection для FastAPI.

---

## Создать

src/dependencies/

    __init__.py
    database.py
    repositories.py
    services.py

---

## database.py

Использовать существующий get_db() из src.db.session.

Не дублировать код.

---

## repositories.py

Создать:

get_user_repository()

get_workflow_repository()

Использовать Depends(get_db).

---

## services.py

Создать:

get_user_service()

get_workflow_service()

Использовать Depends(...) для репозиториев.

---

## __init__.py

Экспортировать все зависимости.

---

## Не изменять

API

Repository

Models

Alembic

Database

---

## После выполнения предоставить отчет

1. Какие файлы созданы.
2. Какие зависимости реализованы.
3. Проверить импорт проекта.
4. Проверить Ruff.