# AI Workflow Assistant

## System Design Document (SDD)

---

## Document Information

| Field | Value |
|-------|-------|
| Status | Approved |
| Version | 1.0 |
| Project | AI Workflow Assistant |
| Document | System Design Document |
| Author | Dmitry |
| Last Updated | 2026-07-05 |

---

# 1. Purpose

Документ описывает архитектуру системы AI Workflow Assistant, основные компоненты, их ответственность и взаимодействие между собой.

---

# 2. High-Level Architecture

```
                    ┌────────────────────┐
                    │    Telegram Bot    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │      FastAPI       │
                    │    Backend API     │
                    └─────────┬──────────┘
              ┌───────────────┼─────────────────┐
              ▼               ▼                 ▼
      ┌────────────┐  ┌──────────────┐  ┌────────────────┐
      │ PostgreSQL │  │ AI Service   │  │ Notification   │
      │            │  │ (LLM API)    │  │ Service        │
      └────────────┘  └──────────────┘  └────────────────┘
              │
              ▼
      ┌────────────────────┐
      │ Admin Dashboard    │
      └────────────────────┘
```

---

# 3. Architecture Principles

При проектировании используются следующие принципы:

- Single Responsibility
- Separation of Concerns
- Modular Architecture
- API First
- Scalability
- Maintainability

---

# 4. System Components

## 4.1 Telegram Bot

Назначение:

Пользовательский интерфейс системы.

Функции:

- принимает сообщения;
- собирает информацию;
- отображает ответы пользователю;
- отправляет данные Backend.

Бот не содержит бизнес-логики.

---

## 4.2 FastAPI Backend

Основной компонент системы.

Отвечает за:

- REST API;
- обработку запросов;
- бизнес-логику;
- взаимодействие с базой данных;
- взаимодействие с AI;
- обработку ошибок.

---

## 4.3 PostgreSQL

Основное хранилище данных.

Хранит:

- пользователей;
- заявки;
- AI-анализ;
- историю изменений.

---

## 4.4 AI Service

Отдельный сервис анализа данных.

Получает:

- текст заявки;
- параметры клиента.

Возвращает:

- Summary;
- Category;
- Priority;
- Recommended Action.

AI не взаимодействует с базой данных напрямую.

---

## 4.5 Notification Service

Используется после успешной обработки заявки.

Отвечает за отправку уведомлений менеджеру.

В будущем может поддерживать:

- Telegram;
- Email;
- Slack;
- Discord.

---

## 4.6 Admin Dashboard

Внутренний интерфейс менеджера.

Позволяет:

- просматривать заявки;
- искать заявки;
- фильтровать;
- изменять статус;
- просматривать результаты AI.

---

# 5. Data Flow

## Создание новой заявки

1. Пользователь открывает Telegram Bot.
2. Бот задает вопросы.
3. Пользователь отвечает.
4. Backend получает данные.
5. Выполняется валидация.
6. Заявка сохраняется в PostgreSQL.
7. Backend отправляет данные в AI Service.
8. AI возвращает анализ.
9. Backend сохраняет результаты анализа.
10. Notification Service отправляет уведомление менеджеру.
11. Dashboard отображает новую заявку.

---

# 6. Error Handling

Если AI недоступен:

- заявка сохраняется;
- создается запись в журнале;
- статус анализа устанавливается как Pending;
- возможна повторная обработка.

Если база данных недоступна:

- запрос завершается ошибкой;
- пользователю отображается сообщение;
- ошибка логируется.

---

# 7. Security

На первом этапе предусматриваются:

- хранение секретов в .env;
- серверная обработка API-ключей;
- проверка входящих данных;
- логирование ошибок;
- защита конфиденциальной информации.

---

# 8. Scalability

Архитектура допускает дальнейшее расширение.

Возможные направления:

- несколько Telegram-ботов;
- дополнительные AI-модели;
- очереди сообщений;
- Redis;
- Celery;
- внешние CRM;
- микросервисная архитектура.

---

# 9. Technology Responsibilities

| Technology | Responsibility |
|------------|----------------|
| FastAPI | Backend API |
| PostgreSQL | Data Storage |
| SQLAlchemy | ORM |
| Pydantic | Validation |
| Docker | Deployment |
| Git | Version Control |
| OpenAI Compatible API | AI Analysis |
| python-telegram-bot | Telegram Integration |

---

# 10. Architecture Decisions

Приняты следующие решения:

- Telegram используется как основной пользовательский интерфейс.
- FastAPI реализует всю бизнес-логику.
- PostgreSQL является единственным источником данных.
- AI работает как отдельный логический сервис.
- Dashboard использует Backend API и не обращается к базе напрямую.

---

# Approval

Status: Approved

Version: 1.0