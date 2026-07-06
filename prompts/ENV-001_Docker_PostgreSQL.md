# ENV-001 - Docker PostgreSQL Environment

## Контекст

Проект AI Workflow Assistant.

Используется:

- FastAPI
- PostgreSQL
- SQLAlchemy Async
- Alembic

Архитектура утверждена.

---

## Цель

Подготовить локальное окружение разработки с использованием Docker.

---

## Необходимо выполнить

### 1.

Создать файл

compose.yaml

---

### 2.

Добавить сервис

postgres

Использовать

postgres:16

---

### 3.

Добавить Named Volume

postgres_data

---

### 4.

Создать отдельную Docker Network

ai-network

---

### 5.

Добавить сервис

pgadmin

Последняя стабильная версия.

---

### 6.

Использовать переменные окружения.

Не хранить логины и пароли внутри compose.yaml.

---

### 7.

Обновить

.env.example

Добавить:

POSTGRES_DB

POSTGRES_USER

POSTGRES_PASSWORD

PGADMIN_EMAIL

PGADMIN_PASSWORD

DATABASE_URL

---

### 8.

Создать файл

docker/.gitkeep

если каталог docker пустой.

---

## Не запускать контейнеры.

Не создавать Dockerfile.

Не изменять FastAPI.

Не изменять Alembic.

---

## Acceptance Criteria

После выполнения:

✔ compose.yaml существует

✔ используется PostgreSQL 16

✔ используется pgAdmin

✔ есть Named Volume

✔ есть отдельная Network

✔ compose использует .env

---

## Отчет

Предоставить:

1. Какие файлы созданы.

2. Какие изменены.

3. Какие сервисы добавлены.

4. Какие порты используются.

5. Какие рекомендации для следующего этапа.