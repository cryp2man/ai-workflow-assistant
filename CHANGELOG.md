# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by Keep a Changelog.

---

## [0.1.0] - 2026-07-06

### Added

- Initialized project structure using uv.
- Configured Python development environment.
- Added FastAPI application entry point.
- Configured Swagger UI and ReDoc.
- Added centralized application configuration.
- Added application lifecycle management (lifespan).
- Configured application logging.
- Implemented API routing structure with versioning (`/api/v1`).
- Added Health endpoint (`GET /api/v1/health`).
- - Added asynchronous SQLAlchemy infrastructure.
- Added centralized database session management.
- Added DeclarativeBase for ORM models.
- Added DATABASE_URL configuration.
- Added database environment template.
- Added asynchronous SQLAlchemy infrastructure.
- Configured Alembic for asynchronous migrations.
- Connected Alembic to application settings.
- Added Docker Compose development environment.
- Added PostgreSQL 16 service.
- Added pgAdmin service.
- Added persistent Docker volume for PostgreSQL.
- Added isolated Docker network.
## [Unreleased]

### Changed

- Refactored Alembic configuration to use `Settings` as the single source of truth for `DATABASE_URL`.
- Removed redundant `.env` loading logic from `alembic/env.py`.
- Centralized SQLAlchemy model registration through `src/db/models/__init__.py`.
- Simplified Alembic model imports while preserving autogenerate functionality.

### Internal

- Improved maintainability of the Database Layer without changing application behavior.
### Added

- Introduced Repository Layer foundation.
- Added `BaseRepository`.
- Added `UserRepository`.
- Added `WorkflowRepository`.
- Prepared project structure for Service Layer implementation.
### Added
- Added `telegram_id` field to `User` model.
- Added UNIQUE constraint for Telegram ID.
- Added database index for Telegram ID.
- Added Alembic migration `feat_add_telegram_id_to_users`.

### Notes
- Telegram ID becomes the primary external identifier of a user.
- Internal UUID remains the primary database key.

## REP-002 - UserRepository CRUD

### Added
- Implemented create().
- Implemented get_by_id().
- Implemented get_by_telegram_id().
- Implemented list().
- Implemented delete().

### Notes
- Repository uses SQLAlchemy 2.0 style.
- Repository uses flush() instead of commit().
- Transaction boundaries remain outside the repository.

## DI-001 - Dependency Injection Foundation

### Added
- Added centralized dependency injection package.
- Added database dependency.
- Added repository providers.
- Added service providers.

### Architecture
FastAPI → Services → Repositories → AsyncSession

## [SER-002] User Service CRUD

### Added
- Реализован CRUD слой UserService.
- Управление транзакциями перенесено в Service.
- Добавлены commit() и rollback() для операций создания и удаления пользователя.
- Методы чтения делегируют работу репозиторию без открытия новых транзакций.

### Architecture
- Repository отвечает только за доступ к данным.
- Service управляет бизнес-операцией и жизненным циклом транзакции.

## SCHEMA-001 - Synchronize User Schemas

### Added
- Added required `telegram_id` field to `UserCreate`.
- Added `telegram_id` field to `UserResponse`.

### Changed
- Updated User API to pass `telegram_id` when creating a new user.
- User creation endpoint is fully functional again.
- GET endpoints now return `telegram_id`.

### Fixed
- Fixed mismatch between SQLAlchemy model and Pydantic schemas.
- Fixed user creation after DB-004 migration.

## TEST-001 - Pytest Foundation

### Added
- Created `tests` package.
- Added base `conftest.py` for future fixtures.

### Verified
- Pytest configuration is already present.
- Test discovery works correctly.
- Project is ready for test implementation.

## TEST-002 - Database Test Fixtures

### Added

- Created dedicated async testing engine.
- Added TestingSessionLocal.
- Added base db_session fixture.

### Notes

- Test database creation is intentionally postponed.
- Rollback strategy will be implemented separately.

## FEATURE-006 - Template Variables in Workflow Steps

### Added

- PromptBuilder substitutes `{{variables}}` in step prompts.
- Execution context variables: `{{previous_response}}`, `{{stepN}}`, `{{workflow_name}}`.
- Per-step responses are persisted in `WorkflowRun.result["steps"]`.
- Unit tests for PromptBuilder.

### Changed

- ExecutionEngine no longer hard-appends "Previous response:" to prompts;
  context passing is explicit via template variables in step prompts.

### Fixed

- Unreliable context passing between steps (~50% of runs lost context
  with llama-3.3 due to the implicit prompt format).

## FEATURE-007 - HTTP Step Type

### Added

- `step_type` field on workflow steps: `llm` (default) or `http`.
- HTTP steps perform a GET request to the URL in `prompt` (with variable
  substitution) and pass the response body to the execution context.
- Alembic migration with a server default of `llm` for existing rows.
- Explicit `httpx` dependency.

### Security

- SSRF protection for HTTP steps: URL scheme restricted to http/https;
  hostname resolved and rejected if it maps to a loopback, private,
  link-local (blocks cloud metadata 169.254.169.254), multicast or
  reserved address. Redirects disabled to prevent validation bypass.
  Rejected URLs return HTTP 400.

### Fixed

- Repository `list` annotations crashed on Python 3.13 (builtin shadowed
  by the `list()` method); deferred annotations via `__future__` import.

## FEATURE-008 - Condition Step Type

### Added

- `condition` step type: a gate that evaluates an expression against the
  execution context and stops the workflow when it is false.
- Safe condition evaluator (no `eval`): `LEFT <op> RIGHT` with operators
  `contains`, `not_contains`, `==`, `!=`; operands support `{{variables}}`.
- Runs stopped by a condition get status `stopped` and a `stopped_reason`.
- Unit tests for the condition evaluator.

## Infrastructure

### Added

- Multi-stage Dockerfile (uv build stage, slim runtime).
- `app` service in Docker Compose: one-command deployment with automatic
  migrations on start.
- `.dockerignore`.