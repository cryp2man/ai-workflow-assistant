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