
## Цель

Реализовать бизнес-логику UserService.

Service отвечает за:

- управление транзакциями;
- commit;
- rollback;
- вызов Repository.

Repository не должен заниматься транзакциями.

---

## Что нужно реализовать

Файл:

src/services/user_service.py

---

### Методы

Реализовать следующие методы:

```python
async def create_user(self, user: User) -> User
```

```python
async def get_user(self, user_id: UUID) -> User | None
```

```python
async def get_user_by_telegram(self, telegram_id: int) -> User | None
```

```python
async def list_users(self) -> list[User]
```

```python
async def delete_user(self, user: User) -> None
```

---

## create_user()

Алгоритм:

1.

```python
user = await repository.create(user)
```

2.

```python
await repository.session.commit()
```

3.

вернуть user

---

Если возникает

```python
IntegrityError
```

нужно выполнить

```python
await repository.session.rollback()
```

после чего повторно выбросить исключение:

```python
raise
```

Никаких собственных Exception пока создавать не нужно.

---

## delete_user()

Алгоритм аналогичный:

```
repository.delete()

commit()

rollback() при ошибке
```

---

## get_user()

Просто вызвать Repository.

Никаких commit.

---

## get_user_by_telegram()

Просто вызвать Repository.

---

## list_users()

Просто вызвать Repository.

---

## Ограничения

Не изменять:

- Repository
- API
- Dependencies
- Database
- Models
- Schemas
- Alembic

---

## Использовать

```python
from sqlalchemy.exc import IntegrityError
```

---

## После выполнения предоставить отчёт

1.

Какие методы реализованы.

2.

Где используется commit().

3.

Где rollback().

4.

Почему commit находится в Service.

5.

Какие исключения сейчас обрабатываются.

6.

Импортируется ли проект.

7.

Результат Ruff.

---

## После выполнения

Никаких дополнительных улучшений самостоятельно не делать.

Не менять архитектуру.

Не менять другие файлы.

Только выполнить требования данного задания.