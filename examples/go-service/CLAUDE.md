# MetricsHub

Lightweight metrics ingestion and aggregation service. Receives time-series
data points from client SDKs over HTTP, aggregates them in memory, and
flushes to a PostgreSQL time-series table on a configurable interval.

---

## Project identity

- **Name**: MetricsHub
- **Owner**: Observability platform team
- **Repo**: github.com/acme/metricshub
- **Deployment**: Docker → Kubernetes (production), Docker Compose (local)
- **Stack source**: `stack/go-service.md` + `backend/caching.md` + `backend/jobs.md`
- **Output format**: `formats/agents.md`

---

## Stack

- Language: Go 1.22+
- HTTP router: chi
- Database: PostgreSQL 16 via `pgx/v5` (direct, no ORM)
- Cache: Redis 7 via `go-redis/v9`
- Config: `github.com/caarlos0/env` (struct tags, no Viper)
- Test runner: go test (stdlib)
- Containerisation: Docker (multi-stage)
- Distribution: Docker image pushed to GHCR, deployed on Kubernetes

---

## Architecture

```
cmd/
  metricshub/
    main.go              # wires dependencies, starts HTTP server + flush worker
internal/
  ingest/
    handler.go           # POST /v1/metrics — thin, decodes and validates
    service.go           # aggregation logic
    model.go             # DataPoint, AggregatedMetric types
  flush/
    worker.go            # periodic flush goroutine
    repository.go        # PostgreSQL write
  health/
    handler.go           # GET /health, GET /ready
  config/
    config.go            # Config struct, loaded from env at startup
  server/
    server.go            # chi router setup, middleware, graceful shutdown
migrations/              # SQL migration files (goose)
Makefile
Dockerfile
docker-compose.yml
go.mod
go.sum
README.md
CLAUDE.md
```

---

## Commands

```bash
go run ./cmd/metricshub           # develop
go build -o bin/metricshub ./cmd/metricshub  # build binary
go test ./...                     # run all tests
go test -tags integration ./...   # run integration tests (requires Docker)
go vet ./...                      # static analysis
goimports -w .                    # format imports
make migrate-up                   # apply DB migrations (goose up)
make migrate-down                 # roll back last migration
docker compose up                 # full local stack
```

---

## Git conventions

- Branch: `main` (protected), feature branches as `feat/<scope>`, fixes as `fix/<scope>`
- Commits: `<type>(<scope>): <summary>` — types: feat, fix, chore, docs, test, refactor
- PRs require one approval and passing CI before merge
- Do not commit compiled binaries, `*.test` files, or `.env`
- `go.sum` is committed — do not delete or regenerate without cause
- Tag releases with `vX.Y.Z` — Go module proxy uses these

---

## Code conventions

### Package and interface design

- `internal/` for all application code — external packages cannot import it
- `cmd/metricshub/main.go` is thin: load config, construct dependencies, start server
- Interfaces defined in the calling package — `ingest.Repository` is defined in
  `internal/ingest/`, not in `internal/flush/`
- Interfaces have 1–3 methods — large interfaces indicate a design problem
- Accept interfaces, return concrete types

### Error handling

- Never discard errors — no `_` on error returns
- Wrap errors with context: `fmt.Errorf("flushing metrics: %w", err)`
- Use `errors.Is()` and `errors.As()` for inspection
- Sentinel errors (`var ErrNoData = errors.New(...)`) defined in the owning package
- Log errors once at the top of the call stack — not at every level

### HTTP handlers

- Decode request body explicitly with `json.NewDecoder` — validate before use
- All error responses in JSON: `{"error": "description"}`
- Use chi middleware for: request ID injection, structured logging, recovery

### Configuration

- One `Config` struct in `internal/config/config.go` — loaded from env vars at startup
- Passed explicitly through the dependency graph — no global config
- Fail fast if required vars are missing: `env.Parse` returns an error on startup

### Concurrency

- Flush worker runs as a goroutine started in `main.go` under `errgroup`
- `context.Context` is the first argument to all functions that may block
- Shared aggregation map protected by `sync.RWMutex` — documented on the struct
- Clean shutdown: HTTP server drains in-flight requests, flush worker drains
  remaining data before exit

### Caching

- Redis used for deduplication of ingest requests (idempotency key TTL: 5 min)
- Cache key: `metricshub:ingest:<client_id>:<metric_name>:<timestamp_bucket>`
- Cache failure does not block ingestion — log at WARN and continue

---

## Testing

- Stdlib `testing` package — no third-party assertion libraries
- Table-driven tests with `t.Run()` for parameterised cases
- Test the public API of each package — not unexported functions
- Use interfaces to inject dependencies — no monkey-patching
- Integration tests in `*_integration_test.go` behind `//go:build integration`
- Integration tests require Docker Compose (`make test-integration`)
- Component test naming: `Test<UnitOfWork>_<State>_<Expected>`
  e.g. `TestIngestHandler_MalformedJSON_Returns400`
- Run before every commit: `go test ./... && go vet ./...`

---

## Observability

- Structured JSON logs via `log/slog` (stdlib) — request ID in every log line
- Log levels: DEBUG (dev only), INFO (normal ops), WARN (degraded), ERROR (failures)
- `/health` — liveness: returns 200 if process is alive
- `/ready` — readiness: verifies DB and Redis connectivity
- Prometheus metrics at `/metrics`:
  - `metricshub_ingest_requests_total` (by status)
  - `metricshub_flush_duration_seconds` (histogram)
  - `metricshub_aggregation_buffer_size` (gauge)

---

## Documentation

- Single source of truth: this file
- `README.md`: local setup, env var reference, Makefile targets
- Architecture decisions in `docs/adr/` as numbered Markdown files
- API contract in `docs/openapi.yaml` — maintained by hand, validated in CI