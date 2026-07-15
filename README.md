# AI Workflow Assistant

A backend service for building and executing multi-step AI workflows: you define a chain of prompt-based steps via REST API, and the execution engine runs them sequentially through an LLM, passing each response to the next step and storing the run history in PostgreSQL.

Think of it as a simplified, self-hosted core of platforms like n8n AI / Dify — built from scratch to demonstrate clean backend architecture around LLM automation.

## Features

- **Workflow engine** — executes ordered chains of steps; template variables (`{{previous_response}}`, `{{stepN}}`, `{{workflow_name}}`) pass context between steps
- **Step types** — `llm` steps call the model, `http` steps fetch external data (GET) into the workflow context, `condition` steps gate execution and stop the run when a check fails
- **Run history** — every execution is persisted as a `WorkflowRun` with status, result, timings and errors
- **Full REST API** — CRUD for users, workflows and workflow steps, plus a run endpoint; interactive docs via Swagger
- **Pluggable LLM providers** — a `BaseLLMProvider` abstraction with two implementations:
  - `OpenAICompatibleProvider` — any OpenAI-compatible cloud API (Groq, Google AI Studio, GitHub Models), free tiers supported
  - `OllamaProvider` — local models as an offline fallback
- **Layered architecture** — Router → Service → Repository → AsyncSession, wired through FastAPI dependency injection

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI (async), Pydantic v2 |
| Database | PostgreSQL 16, SQLAlchemy 2.0 (asyncpg), Alembic migrations |
| LLM | OpenAI SDK against any compatible API (Groq / Gemini / GitHub Models / Ollama) |
| Tooling | uv, Ruff, Pytest, Docker Compose |

## Architecture

```
HTTP (FastAPI, /api/v1)
   │
   ▼
Routers ──► Services ──► Repositories ──► PostgreSQL
   │            │
   │            ▼
   └──►  ExecutionEngine ──► PromptBuilder ──► BaseLLMProvider
                │                                  │
                ▼                          ┌───────┴────────┐
          WorkflowRun (history)      Cloud API (Groq…)    Ollama
```

## Quickstart

Requirements: Python 3.13+, [uv](https://docs.astral.sh/uv/), Docker.

```bash
# 1. Clone and install dependencies
git clone https://github.com/cryp2man/ai-workflow-assistant.git
cd ai-workflow-assistant
uv sync

# 2. Configure environment
cp .env.example .env
# Edit .env: set POSTGRES_* passwords and LLM_API_KEY
# (free key: https://console.groq.com/keys — see options in .env.example)

# 3. Run everything (PostgreSQL + API + pgAdmin)
docker compose up -d --build
```

The `app` container applies migrations automatically on start.

For local development without the app container:

```bash
docker compose up -d postgres pgadmin
uv run alembic upgrade head
uv run uvicorn src.main:app --reload
```

Open Swagger UI at http://127.0.0.1:8000/docs

## Usage Example

```bash
# Create a user
curl -X POST http://127.0.0.1:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "email": "demo@example.com", "telegram_id": 1}'

# Create a workflow
curl -X POST http://127.0.0.1:8000/api/v1/workflows/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Lead analysis", "description": "Analyze incoming lead", "user_id": 1}'

# Add steps
curl -X POST http://127.0.0.1:8000/api/v1/workflows/1/steps \
  -H "Content-Type: application/json" \
  -d '{"title": "Extract facts", "prompt": "Extract key facts from: new client wants a 2-bedroom apartment", "step_order": 1}'

curl -X POST http://127.0.0.1:8000/api/v1/workflows/1/steps \
  -H "Content-Type: application/json" \
  -d '{"title": "Make checklist", "prompt": "Turn these facts into an action checklist for an agent", "step_order": 2}'

# Execute the workflow
curl -X POST http://127.0.0.1:8000/api/v1/workflows/1/execute

# Inspect the run history
curl http://127.0.0.1:8000/api/v1/workflows/1/runs
```

## Project Structure

```
src/
├── api/v1/          # Routers (users, workflows, workflow steps)
├── core/            # Settings, logging, lifespan
├── db/              # Engine, session, ORM models
├── dependencies/    # FastAPI DI providers
├── engine/          # ExecutionEngine — workflow runner
├── llm/             # BaseLLMProvider + implementations
├── prompts/         # PromptBuilder
├── repositories/    # Data access layer
├── schemas/         # Pydantic schemas
└── services/        # Business logic, transaction boundaries
alembic/             # Database migrations
docs/                # PRD, system design, ADRs
prompts/             # AI-assisted development task specs
tests/               # Pytest suite
```

## Development Approach

This project is developed with AI assistance (Claude Code) under strict task specifications: each task defines the goal, constraints, acceptance criteria and verification steps — the specs are kept in [`prompts/`](prompts/). Architecture decisions are documented in [`docs/adr/`](docs/adr/).

## Roadmap

- [x] Layered backend foundation (FastAPI, PostgreSQL, Alembic, DI)
- [x] Workflow / step / run domain model and CRUD API
- [x] End-to-end LLM execution pipeline with run history
- [x] Cloud LLM provider with free OpenAI-compatible APIs
- [x] Template variables between steps (`{{previous_response}}`, `{{stepN}}`, `{{workflow_name}}`)
- [x] Per-step responses persisted in run history
- [x] Dockerfile for the app + one-command deployment
- [x] HTTP request step type (fetch external data into the workflow context)
- [x] Condition step type (gate that stops the run when a check fails)
- [ ] Telegram bot interface

## License

[MIT](LICENSE.md)
