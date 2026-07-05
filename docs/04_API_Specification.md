# AI Workflow Assistant

## API Specification

---

## Document Information

| Field | Value |
|-------|-------|
| Status | Approved |
| Version | 1.0 |
| Project | AI Workflow Assistant |
| Document | API Specification |
| Author | Dmitry |
| Last Updated | 2026-07-05 |

---

# 1. Purpose

Документ описывает REST API проекта AI Workflow Assistant.

API используется для взаимодействия между:

- Telegram Bot
- Backend
- Dashboard
- AI Service

---

# 2. Base URL

Development

http://localhost:8000/api/v1

Production

TBD

---

# 3. Authentication

На этапе MVP авторизация не используется.

В будущем планируется:

- JWT
- OAuth2

---

# 4. API Endpoints

## Health Check

### GET /health

Проверка доступности сервиса.

### Response

Status: 200 OK

```json
{
  "status": "ok"
}
```

---

# Leads

## Create Lead

### POST /leads

Создание новой заявки.

### Request

```json
{
  "telegram_id": 123456789,
  "full_name": "John Smith",
  "phone": "+123456789",
  "email": "john@example.com",
  "company": "Example Ltd",
  "request": "I need a CRM automation solution."
}
```

### Response

Status: 201 Created

```json
{
  "id": 15,
  "status": "NEW"
}
```

---

## Get Lead

### GET /leads/{id}

Получение информации о заявке.

### Response

```json
{
  "id": 15,
  "status": "NEW",
  "created_at": "2026-07-05T14:20:00Z"
}
```

---

## List Leads

### GET /leads

Получение списка заявок.

### Query Parameters

| Parameter | Description |
|-----------|-------------|
| status | Filter by status |
| limit | Number of records |
| offset | Pagination |

### Example

GET /leads?status=NEW&limit=20

---

## Update Lead Status

### PATCH /leads/{id}/status

### Request

```json
{
  "status": "IN_PROGRESS"
}
```

### Response

```json
{
  "success": true
}
```

---

# AI Analysis

## Generate Analysis

### POST /ai/analyze/{lead_id}

Запускает AI-анализ заявки.

### Response

```json
{
  "summary": "Client is looking for CRM automation.",
  "category": "Sales",
  "priority": "HIGH",
  "recommended_action": "Contact within 30 minutes."
}
```

---

## Get Analysis

### GET /ai/{lead_id}

Возвращает результат анализа.

---

# Users

## Get User

### GET /users/{telegram_id}

Получение информации о пользователе.

---

## Create User

### POST /users

Создание пользователя.

---

# Dashboard

Dashboard использует следующие методы:

- GET /leads
- GET /leads/{id}
- PATCH /leads/{id}/status
- GET /ai/{lead_id}

---

# Response Codes

| Code | Description |
|------|-------------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

# Validation Rules

## Phone

- обязательное поле;
- строка;
- максимальная длина 30 символов.

## Email

- валидный email;
- необязательное поле.

## Request

- обязательное поле;
- минимум 10 символов.

---

# Error Response

Пример ошибки.

```json
{
  "detail": "Validation Error"
}
```

---

# API Versioning

Используется версионирование.

```
/api/v1/
```

Следующие версии будут выпускаться без нарушения обратной совместимости.

---

# Future Endpoints

Планируется добавить:

- POST /notifications/send
- GET /statistics
- GET /metrics
- POST /attachments
- POST /auth/login

---

# Approval

Status: Approved

Version: 1.0