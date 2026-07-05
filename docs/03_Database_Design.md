# AI Workflow Assistant

## Database Design Document (DDD)

---

## Document Information

| Field | Value |
|-------|-------|
| Status | Approved |
| Version | 1.0 |
| Project | AI Workflow Assistant |
| Document | Database Design |
| Author | Dmitry |
| Last Updated | 2026-07-05 |

---

# 1. Purpose

Документ описывает структуру базы данных проекта AI Workflow Assistant, назначение таблиц, связи между ними и правила хранения данных.

---

# 2. Database Overview

Тип базы данных:

**PostgreSQL**

Архитектура построена по принципам нормализации данных и минимизации дублирования информации.

---

# 3. Entity Relationship Diagram

```
Users
   │
   │ 1:N
   ▼
Leads
   │
   ├──────────────┐
   │              │
   │1:1           │1:N
   ▼              ▼
AI_Analysis   Lead_History
```

---

# 4. Tables

## 4.1 users

Хранит информацию о пользователях Telegram.

| Column | Type | Description |
|---------|------|-------------|
| id | SERIAL PK | Идентификатор |
| telegram_id | BIGINT | Telegram ID |
| username | VARCHAR(100) | Username |
| first_name | VARCHAR(100) | Имя |
| last_name | VARCHAR(100) | Фамилия |
| created_at | TIMESTAMP | Дата регистрации |

---

## 4.2 leads

Основная таблица заявок.

| Column | Type | Description |
|---------|------|-------------|
| id | SERIAL PK | Идентификатор |
| user_id | INTEGER FK | Пользователь |
| full_name | VARCHAR(255) | Имя клиента |
| phone | VARCHAR(50) | Телефон |
| email | VARCHAR(255) | Email |
| company | VARCHAR(255) | Компания |
| request | TEXT | Текст заявки |
| status | VARCHAR(30) | Статус |
| created_at | TIMESTAMP | Дата создания |

---

## 4.3 ai_analysis

Хранит результаты анализа LLM.

| Column | Type | Description |
|---------|------|-------------|
| id | SERIAL PK | Идентификатор |
| lead_id | INTEGER FK | Заявка |
| summary | TEXT | Краткое описание |
| category | VARCHAR(100) | Категория |
| priority | VARCHAR(30) | Приоритет |
| recommended_action | TEXT | Рекомендация |
| model | VARCHAR(100) | Используемая модель |
| created_at | TIMESTAMP | Дата анализа |

---

## 4.4 lead_history

История изменения статусов.

| Column | Type | Description |
|---------|------|-------------|
| id | SERIAL PK | Идентификатор |
| lead_id | INTEGER FK | Заявка |
| status | VARCHAR(30) | Новый статус |
| comment | TEXT | Комментарий |
| changed_at | TIMESTAMP | Время изменения |

---

# 5. Relationships

## Users → Leads

Тип связи:

**One-to-Many**

Один пользователь может создать несколько заявок.

---

## Leads → AI Analysis

Тип связи:

**One-to-One**

Каждая заявка имеет один актуальный результат анализа.

---

## Leads → Lead History

Тип связи:

**One-to-Many**

Для каждой заявки хранится история изменения статусов.

---

# 6. Status Values

Допустимые значения поля `status`:

| Status | Description |
|---------|-------------|
| NEW | Новая заявка |
| IN_PROGRESS | В обработке |
| COMPLETED | Завершена |
| REJECTED | Отклонена |

---

# 7. Priority Values

Допустимые значения поля `priority`:

| Priority | Description |
|----------|-------------|
| HIGH | Высокий |
| MEDIUM | Средний |
| LOW | Низкий |

---

# 8. Indexes

Планируемые индексы:

- users.telegram_id
- leads.user_id
- leads.status
- leads.created_at
- ai_analysis.lead_id
- lead_history.lead_id

---

# 9. Data Integrity

Используются следующие ограничения:

- Primary Keys
- Foreign Keys
- NOT NULL
- UNIQUE (telegram_id)
- CHECK (priority)
- CHECK (status)

---

# 10. Future Extensions

Возможные дополнительные таблицы:

- companies
- managers
- tags
- notes
- attachments
- audit_log
- conversations

Добавление новых сущностей не потребует изменения существующих связей.

---

# Approval

Status: Approved

Version: 1.0