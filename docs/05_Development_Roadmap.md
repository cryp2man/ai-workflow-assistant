# AI Workflow Assistant

## Development Roadmap

---

## Document Information

| Field | Value |
|-------|-------|
| Status | Approved |
| Version | 1.0 |
| Project | AI Workflow Assistant |
| Document | Development Roadmap |
| Author | Dmitry |
| Last Updated | 2026-07-05 |

---

# 1. Purpose

Документ описывает последовательность разработки проекта AI Workflow Assistant.

Основная цель - разбить проект на небольшие завершенные этапы, каждый из которых можно реализовать, протестировать и закоммитить отдельно.

---

# 2. Development Principles

Во время разработки придерживаемся следующих правил:

- одна задача - один коммит;
- каждый этап должен быть рабочим;
- новый функционал начинается только после успешного тестирования предыдущего;
- документация обновляется вместе с кодом;
- изменения фиксируются в CHANGELOG.md.

---

# 3. Project Milestones

| Milestone | Status |
|------------|--------|
| Documentation | ✅ |
| Backend | ⏳ |
| Database | ⏳ |
| Telegram Bot | ⏳ |
| AI Integration | ⏳ |
| Dashboard | ⏳ |
| Docker | ⏳ |
| Testing | ⏳ |
| Release v1.0 | ⏳ |

---

# 4. Sprint 1 - Project Setup

## Goal

Подготовить проект к разработке.

## Tasks

- создать Git-репозиторий;
- создать структуру проекта;
- настроить виртуальное окружение;
- установить зависимости;
- настроить Ruff;
- настроить Black;
- настроить Pytest;
- создать `.env.example`;
- создать `.gitignore`.

### Result

Проект запускается локально.

---

# 5. Sprint 2 - Backend

## Goal

Запустить FastAPI.

## Tasks

- создать приложение;
- настроить роутинг;
- создать `/health`;
- проверить Swagger;
- настроить конфигурацию.

### Result

Работает FastAPI.

---

# 6. Sprint 3 - PostgreSQL

## Goal

Подключить базу данных.

## Tasks

- установить PostgreSQL;
- подключить SQLAlchemy;
- настроить Alembic;
- создать модели;
- выполнить первую миграцию.

### Result

Backend работает с PostgreSQL.

---

# 7. Sprint 4 - Telegram Bot

## Goal

Создать интерфейс пользователя.

## Tasks

- создать бота;
- реализовать команды;
- реализовать диалог;
- подключить Backend.

### Result

Пользователь может создать заявку.

---

# 8. Sprint 5 - AI Integration

## Goal

Интегрировать LLM.

## Tasks

- подключить AI API;
- реализовать сервис анализа;
- сохранять результаты анализа.

### Result

После создания заявки появляется AI-анализ.

---

# 9. Sprint 6 - Dashboard

## Goal

Создать веб-интерфейс менеджера.

## Tasks

- список заявок;
- карточка заявки;
- просмотр AI Summary;
- изменение статуса.

### Result

Менеджер может работать с заявками.

---

# 10. Sprint 7 - Docker

## Goal

Контейнеризация проекта.

## Tasks

- Dockerfile;
- docker-compose;
- запуск всех сервисов.

### Result

Проект запускается одной командой.

---

# 11. Sprint 8 - Testing

## Goal

Проверить работоспособность проекта.

## Tasks

- Unit Tests;
- API Tests;
- Integration Tests;
- ручное тестирование.

### Result

Все основные функции работают корректно.

---

# 12. Sprint 9 - Release

## Goal

Подготовить первую публичную версию.

## Tasks

- обновить README;
- обновить документацию;
- обновить CHANGELOG;
- проверить структуру проекта;
- создать Release v1.0.

### Result

Проект опубликован на GitHub.

---

# 13. Git Workflow

Для разработки используется следующая схема:

main

↓

feature/...

↓

Pull Request

↓

Merge

Каждый новый функционал разрабатывается в отдельной ветке.

---

# 14. Definition of Done

Задача считается завершенной, если:

- код работает;
- код протестирован;
- документация обновлена;
- изменения закоммичены;
- нет известных критических ошибок.

---

# Approval

Status: Approved

Version: 1.0