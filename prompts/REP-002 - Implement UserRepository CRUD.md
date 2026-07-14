
## Цель

Реализовать минимальный CRUD для UserRepository.

---

## Изменить

src/repositories/user_repository.py

---

## Реализовать методы

create()

get_by_id()

get_by_telegram_id()

list()

delete()

---

## Использовать

SQLAlchemy 2.0

select()

await session.execute()

scalar_one_or_none()

scalars().all()

flush()

---

## После create()

session.add()

await session.flush()

---

## После delete()

await session.delete()

await session.flush()

---

## Не использовать

commit()

rollback()

refresh()

---

## Не менять

WorkflowRepository

Service Layer

API

Schemas

Migration

Models

---

## После выполнения предоставить отчет

1. Какие методы реализованы.

2. Какие SQLAlchemy конструкции используются.

3. Используется ли commit.

4. Используется ли flush.

5. Почему commit отсутствует.

6. Проверить импорт проекта.

7. Проверить Ruff.