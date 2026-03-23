# OrderService

HTTP API for order management. Owned by the Platform team.

---

## Project identity

- **Name**: OrderService
- **Owner**: Platform team
- **Repo**: github.com/acme/order-service
- **Deployment**: Docker → Kubernetes (cloud)

---

## Stack

- Language: Python 3.11+
- Framework: FastAPI
- Runtime: asyncio (async/await throughout)
- Validation: Pydantic v2
- Package manager: uv
- Linter: ruff
- Formatter: ruff format
- Type checker: mypy (strict mode)
- Test runner: pytest + httpx (AsyncClient)
- Database: PostgreSQL via SQLAlchemy 2 (async) + Alembic
- Auth: JWT bearer tokens
- ASGI server (production): uvicorn + gunicorn
- Distribution: Docker image → Kubernetes

---

## Architecture

```
src/
  order_service/
    __init__.py
    main.py              # FastAPI app instance, lifespan, router includes
    config.py            # Settings via pydantic-settings
    dependencies.py      # Shared FastAPI dependencies
    routers/
      [feature].py       # APIRouter per feature domain
    schemas/
      [feature].py       # Pydantic request/response models
    services/
      [feature].py       # Business logic (pure, async)
    models/              # SQLAlchemy ORM models
    db.py                # Async engine and session setup
tests/
  conftest.py            # async client fixture
  component/
    test_[feature].py
  integration/
    test_[feature].py
pyproject.toml
.env.example
Dockerfile
README.md
CLAUDE.md
```

---

## Commands

```bash
uvicorn order_service.main:app --reload   # develop — hot reload at localhost:8000
alembic upgrade head                      # apply migrations
alembic revision --autogenerate -m "..."  # generate a migration
pytest                                    # run tests
mypy src/ --strict                        # type check
gunicorn order_service.main:app -w 4 -k uvicorn.workers.UvicornWorker  # production
```

---

## Git conventions

- Use conventional commit prefixes: `feat:`, `fix:`, `chore:`, `docs:`,
  `refactor:`, `style:`, `test:`
- Keep the subject line under 80 characters
- Use the imperative mood: "add feature" not "added feature"
- Always work on a branch — never commit directly to `main`
- Branch naming: `feat/description`, `fix/description`, `chore/description`,
  `docs/description`
- PRs should be small and focused — one concern per PR
- After a PR is merged: delete branch, pull main before starting new work
- Do not commit `.env`, `*.db`, `__pycache__/`, `.mypy_cache/`
- Alembic migrations are committed — never regenerate a migration already merged

---

## Code conventions

### Application setup

- One `FastAPI` instance in `main.py` — no global state elsewhere
- Use `lifespan` context manager for startup/shutdown (not deprecated events)
- Include all routers via `app.include_router()` in `main.py`
- Set `title`, `version`, and `description` on the app instance

### Configuration

- Use `pydantic-settings` (`BaseSettings`) for all configuration
- `Settings` instantiated once and injected as a dependency — never imported
  globally
- Never read `os.Getenv` directly in application code outside the config loader

### Routing and dependencies

- One `APIRouter` per feature domain with a prefix and tags
- Routes thin — delegate business logic to service functions
- Shared logic (auth, DB session, current user) via `Depends()`
- Use `Annotated` for dependency injection — avoid bare `= Depends()` in
  signatures
- Return type annotations on all route functions

### Schemas

- Separate request and response schemas — never reuse ORM models as responses
- Use `model_config = ConfigDict(from_attributes=True)` for ORM-backed responses
- All fields explicitly typed — no bare `Any`
- Use `Field(...)` for validation constraints (min/max length, regex, ge/le)
- Validators via `@field_validator` — no custom `__init__`

### Async conventions

- All route handlers and service functions `async def`
- Blocking I/O (file reads, sync DB calls) must run in `asyncio.to_thread()`
- Never `await` inside a list comprehension — use `asyncio.gather()` for
  concurrency
- Use `asyncpg` for the async PostgreSQL driver

### Error handling

- Raise `HTTPException` with explicit `status_code` and `detail`
- Register custom exception handlers in `main.py` for domain exceptions

### Database

- SQLAlchemy 2.x with async engine (`create_async_engine`)
- Session injected per request via `Depends(get_db)` — never a global session
- Migrations managed by Alembic
- Use `select()` style queries — no legacy `Query` API

### Authentication

- JWT bearer tokens validated in a shared `Depends()` dependency
- Never log or expose token payloads in error responses

### OpenAPI

- All routes have `summary`, `tags`, and explicit `response_model`
- Disable OpenAPI in production if the API is not public: `openapi_url=None`
- Keep schema clean — avoid `include_in_schema=False` as a crutch

---

## Testing

- `httpx.AsyncClient` with `ASGITransport` for route tests — no `TestClient`
  (sync)
- One async `client` fixture in `conftest.py`
- Test each route for: success (2xx), validation error (422), auth error
  (401/403)
- No mocking of the database in component integration tests — use a test
  database
- Override dependencies with `app.dependency_overrides` in tests
- Component test naming: `test_<route_or_function>_<state>_<expected>`
  e.g. `test_create_order_invalid_payload_returns_422`
- Component tests in `tests/component/`, integration tests in
  `tests/integration/`
- Run before every commit: `pytest && mypy src/ --strict`
- Use `pytest-asyncio` for async test functions

---

## Documentation

- Keep `README.md` up to date with setup, run, and test instructions
- Every public module, class, and function has a docstring
- Architecture decisions recorded as ADRs in `docs/decisions/`