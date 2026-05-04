# InventoryAPI

REST API for warehouse inventory management — stock levels, locations,
suppliers, and purchase orders.

---

## Project identity

- **Name**: InventoryAPI
- **Owner**: Warehouse platform team
- **Repo**: github.com/acme/inventory-api
- **Deployment**: Docker → Fly.io (production), Docker Compose (local)
- **Stack source**: `stack/python-flask.md` + `backend/auth.md` + `backend/jobs.md`
- **Output format**: `base/core/agents.md`

---

## Stack

- Language: Python 3.12
- Framework: Flask 3.x
- Package manager: uv
- Linter / formatter: ruff + ruff format
- Type checker: mypy (strict mode)
- Test runner: pytest + pytest-flask
- Database: PostgreSQL 16 via SQLAlchemy 2 + Flask-Migrate (Alembic)
- Task queue: Celery 5 with Redis broker
- WSGI server (production): gunicorn
- Deployment: Docker image, deployed on Fly.io

---

## Architecture

```
src/
  inventory/
    __init__.py          # create_app factory
    config.py            # DevelopmentConfig, TestingConfig, ProductionConfig
    extensions.py        # db, migrate, celery instances
    blueprints/
      stock/
        __init__.py
        routes.py        # /api/v1/stock
        models.py        # StockItem, Location
        schemas.py       # marshmallow or dataclass schemas
        services.py      # business logic
      suppliers/
        routes.py        # /api/v1/suppliers
        models.py
        schemas.py
        services.py
      orders/
        routes.py        # /api/v1/orders
        models.py
        schemas.py
        services.py
        tasks.py         # Celery tasks (PO processing, notifications)
    auth/
      routes.py          # /auth/token
      middleware.py      # JWT verification decorator
tests/
  conftest.py            # app fixture (TestingConfig), test client, test DB
  component/
    test_stock.py
    test_suppliers.py
    test_orders.py
  integration/
    test_order_workflow.py
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
flask run                           # develop — hot reload
flask db upgrade                    # apply migrations
flask db migrate -m "description"   # generate migration
celery -A inventory.celery worker   # start Celery worker (local)
pytest                              # run tests
mypy src/ --strict                  # type check
gunicorn "inventory:create_app()"   # production server
docker compose up                   # full local stack (Flask + Postgres + Redis)
```

---

## Git conventions

- Branch: `main` (protected), feature branches as `feat/<scope>`, fixes as `fix/<scope>`
- Commits: `<type>(<scope>): <summary>` — types: feat, fix, chore, docs, test, refactor
- PRs require one approval and passing CI before merge
- Do not commit `.env`, `instance/`, `*.db`, `__pycache__/`, `.mypy_cache/`
- Migrations are committed — never regenerate a migration already merged

---

## Code conventions

### Application factory

- `create_app(config=None)` in `inventory/__init__.py`
- All blueprints and extensions registered inside `create_app`
- Extensions instantiated in `extensions.py`, initialised with `ext.init_app(app)`
- No global `app` object used outside of `create_app`

### Configuration

- Three config classes in `config.py`: `DevelopmentConfig`, `TestingConfig`,
  `ProductionConfig`
- All env-specific values from environment variables — no hardcoded secrets
- `DEBUG=False` enforced in `ProductionConfig`
- Required vars: `DATABASE_URL`, `SECRET_KEY`, `REDIS_URL`, `CELERY_BROKER_URL`

### Blueprints

- One blueprint per domain (`stock`, `suppliers`, `orders`, `auth`)
- All registered with a URL prefix: `/api/v1/stock`, `/api/v1/suppliers`, etc.
- No cross-blueprint imports — shared logic goes in a service module
- Routes are thin: decode input, call service, return response

### Authentication

- JWT bearer tokens — issued at `/auth/token`, verified via a decorator
- Token expiry: 15 min access, 7 day refresh
- Role stored in JWT claims — checked in service functions, not route handlers

### Database

- SQLAlchemy 2 ORM — no raw SQL strings
- Migrations via Flask-Migrate (Alembic) — one migration per logical change
- `select()` style queries — no legacy `Query` API
- No N+1 queries — use `selectinload` or `joinedload` for relations
- Foreign key indexes added explicitly in migrations

### Background tasks (Celery)

- Tasks defined in `tasks.py` per blueprint — keep task functions thin,
  delegate to service functions
- All tasks are idempotent — safe to re-run on retry
- Retry with exponential backoff — max 3 retries then route to DLQ
- Log task start, completion, and failure with task ID and correlation ID

---

## Testing

- `pytest-flask` for the test client and app fixture
- One `app` fixture in `conftest.py` — uses `TestingConfig` and a test database
- Test each route for: success (2xx), validation error (400), auth error (401/403)
- No mocking of the database — integration tests use a real PostgreSQL test DB
- Celery tasks tested with `task.apply()` (synchronous, no broker needed for unit tests)
- Component test naming: `test_<route_or_function>_<state>_<expected>`
  e.g. `test_create_stock_item_missing_sku_returns_400`
- Run before every commit: `pytest && mypy src/ --strict`

---

## Observability

- Structured JSON logs via `structlog` — request ID injected per request
- Log levels: DEBUG (dev only), INFO (normal ops), WARNING (degraded), ERROR (failures)
- Never log passwords, tokens, or PII
- `/health` — liveness check (200 if process alive)
- `/ready` — readiness check (verifies DB + Redis connectivity)
- Celery task metrics: queue depth and DLQ depth tracked via Flower or custom metrics

---

## Documentation

- Single source of truth: this file
- All API endpoints documented in `README.md` with request/response examples
- Architecture decisions recorded in `docs/adr/` as numbered Markdown files