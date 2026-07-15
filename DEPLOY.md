# Deployment (Railway)

The app is container-based and reads all configuration from environment
variables, so it deploys to Railway from this repo with no code changes.

## What Railway needs

- **Build:** the `Dockerfile` (declared in `railway.json`).
- **Port:** the app binds to `$PORT` (Railway injects it) — nothing to set.
- **Migrations:** run automatically on container start (`alembic upgrade head`).
- **Health check:** `/api/v1/health` (declared in `railway.json`).

## Steps

### 1. Create the project

Railway dashboard → **New Project** → **Deploy from GitHub repo** →
select `cryp2man/ai-workflow-assistant`.

### 2. Add a database

In the project: **New** → **Database** → **PostgreSQL**.
Railway creates a `DATABASE_URL` variable on the Postgres service.

### 3. Wire the app to the database

On the **app** service → **Variables** → add a reference:

```
DATABASE_URL = ${{Postgres.DATABASE_URL}}
```

The app normalizes the scheme (`postgresql://` → `postgresql+asyncpg://`)
automatically, so Railway's default URL works as-is.

### 4. Set the LLM variables (for `llm` steps to work)

On the **app** service → **Variables**:

```
LLM_PROVIDER = openai_compatible
LLM_BASE_URL = https://api.groq.com/openai/v1
LLM_MODEL    = llama-3.3-70b-versatile
LLM_API_KEY  = <your free Groq key from https://console.groq.com/keys>
```

> The key lives server-side in Railway and is never exposed to visitors.
> `http` and `condition` steps work without any key.

### 4a. (Optional) Enable the Telegram bot

Create a bot with [@BotFather](https://t.me/BotFather) (`/newbot`) and add its
token to the **app** service variables:

```
BOT_TOKEN = <token from BotFather>
```

The bot starts automatically inside the app process (long polling) and shares
the same engine. Without `BOT_TOKEN` the bot stays disabled — the API is
unaffected. In Telegram: `/start` → `/demo` → `/workflows` → tap to run.

### 5. Get the public URL

App service → **Settings** → **Networking** → **Generate Domain**.
The public URL opens the interactive API docs (`/` redirects to `/docs`).

### 6. (Optional) Seed a demo workflow

So visitors see a ready example immediately. From the app service shell
(Railway → service → **...** → **Shell**) or via the CLI:

```bash
railway run python -m scripts.seed_demo
```

This creates a demo user and a workflow "Real estate lead → action checklist"
(LLM → condition → LLM). Run it via `POST /api/v1/workflows/{id}/execute`.

## CLI alternative

```bash
railway login                 # opens browser (run this yourself)
railway link                  # or: railway init
railway up                    # deploy current repo
railway add --database postgres
railway variables --set LLM_API_KEY=... --set LLM_BASE_URL=... --set LLM_MODEL=...
railway domain                # generate public URL
```
