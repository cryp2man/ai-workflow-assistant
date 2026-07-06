# ADR-001 - Database Architecture

## Status

Accepted

## Context

The project requires a scalable and modern database layer compatible with FastAPI.

## Decision

The project uses:

- PostgreSQL
- SQLAlchemy 2.x
- AsyncEngine
- AsyncSession
- DeclarativeBase
- Alembic for migrations

Repository Pattern is intentionally not used in the first version of the project to keep the architecture simple.

## Consequences

Advantages:

- modern FastAPI stack;
- asynchronous database access;
- easy to scale;
- easy to explain during interviews.

Trade-offs:

- async code is slightly more complex;
- requires understanding of await.