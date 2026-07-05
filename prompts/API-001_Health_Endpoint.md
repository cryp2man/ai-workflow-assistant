# API-001 - Health Endpoint

## Контекст

Использовать существующую структуру проекта.

Не изменять архитектуру.

## Цель

Добавить endpoint проверки состояния приложения.

## Требования

1. Создать файл:

src/api/v1/endpoints/health.py

2. Создать APIRouter.

3. Реализовать GET endpoint:

/health

4. Ответ должен иметь HTTP 200.

5. Ответ в JSON:

{
    "status": "ok"
}

6. Подключить endpoint к router.py уровня v1.

## Ограничения

Не использовать:

- БД
- зависимости
- middleware
- сервисы
- авторизацию

## Acceptance Criteria

После запуска:

GET /api/v1/health

возвращает:

{
    "status": "ok"
}

Swagger отображает новый endpoint.