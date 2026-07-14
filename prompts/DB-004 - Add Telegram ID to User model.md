
## Цель

Добавить поддержку Telegram ID в модель User.

Это единственное изменение модели.

---

## Изменить

src/db/models/user.py

---

## Добавить поле

telegram_id

Тип:

int

Использовать:

BigInteger

Поле должно иметь:

- unique=True
- nullable=False
- index=True

Использовать современный стиль SQLAlchemy 2.0:

```python
telegram_id: Mapped[int] = mapped_column(
    BigInteger,
    unique=True,
    nullable=False,
    index=True,
)
```

---

## После изменения модели

Создать новую миграцию Alembic.

Имя:

```
feat_add_telegram_id_to_users
```

Использовать:

```
uv run alembic revision --autogenerate -m "feat_add_telegram_id_to_users"
```

---

## Затем

Применить миграцию:

```
uv run alembic upgrade head
```

---

## Проверить

В PostgreSQL:

таблица users

должна содержать колонку

telegram_id

с индексом

и UNIQUE constraint.

---

## Ограничения

Не менять:

- Workflow
- Repository
- Services
- API
- Schemas

---

## После выполнения предоставить отчет

1. Что изменено в модели.
2. Какая миграция создана.
3. Какие SQL-команды Alembic сгенерировал.
4. Успешно ли применена миграция.
5. Вывод команды:

```
uv run alembic current
```