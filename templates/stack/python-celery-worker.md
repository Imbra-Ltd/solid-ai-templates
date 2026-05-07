# Stack — Celery Worker
[DEPENDS ON: templates/base/core/git.md, templates/base/core/docs.md, templates/base/core/quality.md, templates/base/core/config.md, templates/backend/jobs.md, templates/backend/observability.md, templates/backend/quality.md, templates/stack/python-lib.md, templates/base/infra/cicd.md, templates/base/security/devsecops.md]

A standalone Celery worker process. No HTTP layer — purely a background task
processor. Covers task design, retry/backoff, scheduling, observability,
and testing.

---

## Stack
[ID: celery-stack]

- Language: Python 3.11+
- Task framework: Celery 5+
- Broker: [Redis / RabbitMQ / SQS]
- Result backend: [Redis / PostgreSQL / none]
- Scheduler: Celery Beat (for periodic tasks)
- Package manager: [pip / uv / poetry]
- Linter: ruff
- Formatter: ruff format
- Type checker: mypy (strict mode)
- Test runner: pytest
- Distribution: Docker image / [platform]

---

## Project structure
[ID: celery-structure]

```
src/
  [app_name]/
    __init__.py
    celery.py            # Celery app instance and configuration
    config.py            # settings via pydantic-settings or dataclass
    tasks/
      [domain].py        # task definitions grouped by domain
    services/
      [domain].py        # business logic — pure functions, no Celery imports
    db.py                # database session (if tasks write to a DB)
tests/
  conftest.py
  test_tasks_[domain].py
  test_services_[domain].py
pyproject.toml
.env.example
Dockerfile
README.md
CLAUDE.md
```

---

## Celery app setup
[ID: celery-app]

- One `Celery` instance in `celery.py` — imported by tasks, never re-created
- Configuration via a typed settings object — never read `os.environ` directly
  in task code
- Set `task_serializer = 'json'` and `result_serializer = 'json'` — avoid
  pickle serialization (security risk)
- Set `task_always_eager = True` in test config — executes tasks synchronously
  without a broker in unit tests

---

## Task design
[EXTEND: backend-jobs]

- Bind tasks with `@app.task(bind=True)` only when the task needs access
  to `self` (e.g. for retry logic) — avoid `bind=True` by default
- Never pass ORM model instances as task arguments — pass primitive IDs
  and reload from the database inside the task
- Never chain tasks that must all succeed atomically — use the Saga pattern
  or a single task with explicit rollback logic

---

## Retry and backoff
[ID: celery-retry]

- Set `max_retries`, `default_retry_delay`, and `autoretry_for` on every task
  that calls external systems
- Use exponential backoff: `retry_backoff=True, retry_backoff_max=600`
- On final failure (max retries exhausted), log at ERROR level with full
  context and route to the dead-letter queue or a failure handler task
- Transient errors (network timeouts, rate limits) are retriable;
  permanent errors (invalid input, not found) are not — distinguish them

---

## Scheduling (Celery Beat)
[ID: celery-beat]

- Define schedules in code (`beat_schedule` config) — never via the database
  scheduler in production (it requires a persistent backend and adds complexity)
- One Beat instance runs at a time — enforce with a distributed lock if
  deploying multiple replicas
- Periodic tasks MUST be idempotent — Beat may fire a task more than once
  under clock drift or restart conditions

---

## Configuration
[EXTEND: base-config]

- All Celery config and application config read from environment variables
  via a typed settings class
- Broker URL, result backend URL, and any API keys read from env — never
  hardcoded

---

## Observability
[EXTEND: backend-observability]

- Log at task entry: task name, task ID, arguments summary, correlation ID
- Log at task exit: task ID, outcome (success / retry / failure), duration
- Emit metrics per task: execution time (p50/p95/p99), success rate, retry
  rate, failure rate
- Track queue depth and DLQ depth — alert when DLQ grows
- Use Flower or a custom Prometheus exporter for broker-level visibility

---

## Testing
[EXTEND: base-testing]

- Unit-test service functions independently of Celery — no broker, no worker
- Test task functions with `task.apply()` (synchronous execution) using
  `CELERY_TASK_ALWAYS_EAGER = True` in test config
- Integration tests run against a real broker (Redis in Docker) to verify
  task routing, serialisation, and retry behaviour
- Test the retry path: mock the external call to raise a retriable exception
  and assert `task.retry()` is called with correct arguments
- Test idempotency: call the task function twice with the same arguments
  and assert the outcome is identical with no duplicate side effects
- Component test naming: `test_<task_or_function>_<state>_<expected>`
  e.g. `test_send_invoice_email_smtp_timeout_retries`
- Run before every commit: `pytest && mypy src/ --strict`

---

## Git conventions
[EXTEND: base-git]

- Do not commit `.env`, `__pycache__/`, `.mypy_cache/`
- Do not commit Celery Beat schedule database (`celerybeat-schedule`)

---

## Commands
```
celery -A [app_name].celery worker --loglevel=info   # start worker
celery -A [app_name].celery beat --loglevel=info     # start scheduler
celery -A [app_name].celery flower                   # task monitor UI
pytest                                               # run tests
mypy src/ --strict                                   # type check
```