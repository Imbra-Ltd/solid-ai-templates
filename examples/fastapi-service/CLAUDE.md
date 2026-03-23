# TaskFlow API

REST API for managing tasks, projects, and team assignments.

---

## Project identity

- **Name**: TaskFlow API
- **Owner**: Platform team
- **Repo**: github.com/acme/taskflow-api
- **Deployment**: Docker → Railway (production), Docker Compose (local)
- **Stack source**: `stack/python-fastapi.md` + `backend/auth.md` + `backend/caching.md`
- **Output format**: `formats/claude.md`

---

## Stack

- Language: Python 3.12
- Framework: FastAPI
- Runtime: asyncio (async/await throughout)
- Validation: Pydantic v2
- Package manager: uv
- Linter / formatter: ruff + ruff format
- Type checker: mypy (strict mode)
- Test runner: pytest + httpx (AsyncClient)
- Database: PostgreSQL 16 via SQLAlchemy 2 async + Alembic
- Cache: Redis 7 via `redis-py` async client
- ASGI server (production): uvicorn + gunicorn
- Deployment: Docker image pushed to GHCR, deployed on Railway

---

## Architecture

```
src/
  taskflow/
    __init__.py
    main.py              # FastAPI app, lifespan, router includes
    config.py            # pydantic-settings BaseSettings
    dependencies.py      # Shared Depends() — db session, current user, cache
    routers/
      tasks.py           # /tasks endpoints
      projects.py        # /projects endpoints
      users.py           # /users endpoints
      health.py          # /health, /ready
    schemas/
      tasks.py           # TaskCreate, TaskUpdate, TaskResponse
      projects.py
      users.py
    services/
      tasks.py           # business logic — pure async functions
      projects.py
      users.py
    models/              # SQLAlchemy ORM models
      task.py
      project.py
      user.py
    db.py                # async engine, session factory
    cache.py             # Redis client, cache helpers
tests/
  conftest.py            # async client, test DB, fixtures
  unit/
    test_services.py
  integration/
    test_tasks.py
    test_projects.py
    test_auth.py
pyproject.toml
.env.example
Dockerfile
docker-compose.yml
README.md
CLAUDE.md
```

---

## Commands

```bash
uv run uvicorn taskflow.main:app --reload   # develop — hot reload at :8000
uv run alembic upgrade head                 # apply migrations
uv run alembic revision --autogenerate -m "describe change"
uv run pytest                               # run tests
uv run mypy src/ --strict                   # type check
uv run gunicorn taskflow.main:app -w 4 -k uvicorn.workers.UvicornWorker
docker compose up                           # start full stack locally
```

---

## Git conventions

- Branch: `main` (protected), feature branches as `feat/<scope>`, fixes as `fix/<scope>`
- Commits: `<type>(<scope>): <summary>` — types: feat, fix, chore, docs, test, refactor
- PRs require one approval and passing CI before merge
- Do not commit `.env`, `*.db`, `__pycache__/`, `.mypy_cache/`, `dist/`
- Alembic migrations are committed — never regenerate a migration already merged

---

## Code conventions

### Application setup

- One `FastAPI` instance in `main.py` — no global state elsewhere
- Use `lifespan` context manager for startup/shutdown hooks
- `title`, `version`, and `description` set on the app instance
- All routers registered via `app.include_router()` in `main.py`

### Configuration

- `pydantic-settings` `BaseSettings` in `config.py`
- `Settings` instantiated once, injected as `Depends(get_settings)` — never imported globally
- `.env.example` committed; `.env` in `.gitignore`
- Required vars: `DATABASE_URL`, `SECRET_KEY`, `REDIS_URL`, `ALLOWED_ORIGINS`
- Fail fast on startup if any required var is missing

### Routing

- One `APIRouter` per feature domain, prefixed and tagged
- Routes thin — delegate all business logic to service functions
- Auth, DB session, current user via `Depends()` with `Annotated` syntax
- Return type annotations on all route handlers

### Schemas

- Separate request and response schemas — ORM models never returned directly
- `model_config = ConfigDict(from_attributes=True)` on ORM-backed response schemas
- `Field(...)` for all validation constraints (min/max, regex, ge/le)
- No bare `Any` — all fields explicitly typed

### Error handling

- Raise `HTTPException` with explicit `status_code` and `detail`
- Domain exceptions mapped to HTTP errors via custom exception handlers in `main.py`
- Errors logged with request ID for traceability

### Authentication

- JWT bearer tokens — issued at `/users/login`, validated via `Depends(get_current_user)`
- Tokens stored in `Authorization: Bearer <token>` header only — never in cookies or query params
- Role checked in service layer, not in route handlers
- Token expiry: 15 min access, 7 day refresh

### Caching

- Cache-aside pattern for read-heavy endpoints (project lists, user profiles)
- Cache keys: `taskflow:<resource>:<id>` — namespaced, never bare IDs
- TTL: 5 min for lists, 15 min for single resources
- Invalidate on write — delete affected keys after a successful mutation
- Never cache responses that contain user-specific data without scoping the key

### Database

- SQLAlchemy 2.x with async engine (`create_async_engine`)
- Session injected per request via `Depends(get_db)` — never a global session
- Migrations managed by Alembic — one migration per logical change
- `select()` style queries only — no legacy `Query` API
- No N+1 queries — use `selectinload` or `joinedload` for related data
- Foreign key indexes added explicitly in migrations

### Async conventions

- All route handlers and service functions `async def`
- Blocking I/O runs in `asyncio.to_thread()`
- `asyncio.gather()` for concurrent independent awaits — not sequential awaits in a loop

---

## Testing

- `httpx.AsyncClient` with `ASGITransport` for all route tests
- Test DB: isolated PostgreSQL schema, truncated between test runs
- No database mocking — integration tests use a real test database
- `app.dependency_overrides` for injecting test fixtures
- Name tests: `test_<function>_<state>_<expected>`
  - e.g. `test_create_task_missing_title_returns_422`
- Each route tested for: 2xx success, 422 validation error, 401/403 auth error
- Unit tests in `tests/unit/`, integration tests in `tests/integration/`
- Run before every commit: `pytest && mypy src/ --strict`

---

## Observability

- Structured JSON logs — `structlog` with request ID injected per request
- Log levels: DEBUG (dev only), INFO (normal ops), WARNING (degraded), ERROR (failures)
- Never log passwords, tokens, or PII
- `/health` — shallow liveness check (returns 200 if process is alive)
- `/ready` — deep readiness check (verifies DB + Redis connectivity)
- Prometheus metrics exposed at `/metrics` (request count, latency, error rate)

---

## Documentation

- Single source of truth: this file + OpenAPI at `/docs` (disabled in production)
- All routes have `summary`, `tags`, and explicit `response_model`
- Architecture decisions recorded in `docs/adr/` as numbered Markdown files
- `README.md`: setup steps, env var reference, and common commands only