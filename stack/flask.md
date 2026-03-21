# Stack — Flask Web Application
[DEPENDS ON: base/git.md, base/docs.md, base/quality.md, backend/config.md, backend/http.md, backend/database.md, backend/observability.md, backend/quality.md, stack/python-lib.md]

Extends the Python library stack with Flask-specific rules for web
applications and APIs. Covers application factory, blueprints, config,
extensions, and deployment.

---

## Stack
[OVERRIDE: python-lib-stack]

- Language: Python 3.11+
- Framework: Flask
- Package manager: [pip / uv / poetry]
- Linter: ruff
- Formatter: ruff format
- Type checker: mypy (strict mode)
- Test runner: pytest + pytest-flask
- WSGI server (production): gunicorn
- Distribution: Docker image / [platform]

---

## Project structure
[OVERRIDE: python-lib-structure]

```
src/
  [app_name]/
    __init__.py          # application factory (create_app)
    config.py            # Config classes (Dev, Test, Prod)
    extensions.py        # extension instances (db, login_manager, etc.)
    blueprints/
      [feature]/
        __init__.py
        routes.py
        models.py
        schemas.py
    templates/           # Jinja2 templates (if serving HTML)
    static/              # static assets (if serving directly)
tests/
  conftest.py            # app fixture, test client
  test_[feature].py
pyproject.toml
.env.example             # committed — never .env
Dockerfile
README.md
CLAUDE.md
```

---

## Application factory
[ID: flask-factory]

- Always use the application factory pattern (`create_app(config=None)`)
- Never use the global `app` object outside of `create_app`
- Register all blueprints and extensions inside `create_app`
- Extensions instantiated in `extensions.py`, initialised with `ext.init_app(app)`

---

## Configuration
[EXTEND: backend-config]

- Three config classes: `DevelopmentConfig`, `TestingConfig`, `ProductionConfig`
- `FLASK_ENV` / `FLASK_DEBUG` must be `False` in production

---

## Blueprints
[ID: flask-blueprints]

- One blueprint per feature domain (e.g. `auth`, `api`, `admin`)
- Blueprint registered with a URL prefix (`/api/v1`, `/auth`, etc.)
- No cross-blueprint imports — shared logic goes in a service module
- Routes thin — business logic delegated to service functions, not in route handlers

---

## Request / response
[EXTEND: backend-http]

- Use `abort()` with HTTP status codes rather than raising raw exceptions

---

## Database (if applicable)
[EXTEND: backend-database]

- Use Flask-SQLAlchemy or SQLAlchemy Core — no raw SQL strings
- Migrations managed by Flask-Migrate (Alembic)

---

## Testing
[EXTEND: base-testing]

- `pytest-flask` for the test client and app fixture
- One `app` fixture in `conftest.py` — uses `TestingConfig`
- Test each route for: success, validation error, auth error (if applicable)
- No mocking of the database in integration tests — use a test database
- Name tests using the pattern: `test_<route_or_function>_<state>_<expected>`
  e.g. `test_create_user_duplicate_email_returns_409`
- Unit tests in `tests/unit/`, integration tests in `tests/integration/`
- Run before every commit: `pytest && mypy src/ --strict`

---

## Git conventions
[EXTEND: base-git]

- Do not commit `.env`, `instance/`, `*.db`, `__pycache__/`, `.mypy_cache/`
- Migrations are committed — never regenerate a migration that is already merged

---

## Commands
```
flask run                  # develop — hot reload
flask db upgrade           # apply migrations
flask db migrate -m "..."  # generate a migration
pytest                     # run tests
gunicorn "app:create_app()" # production server
```