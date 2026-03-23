# MetricsHub

Infrastructure metrics collection and aggregation service. Owned by the
Infrastructure team.

---

## Project identity

- **Name**: MetricsHub
- **Owner**: Infrastructure team
- **Repo**: github.com/acme/metricshub
- **Deployment**: Docker → Kubernetes (cloud)

---

## Stack

- Language: Go 1.22+
- HTTP framework: Echo v4
- Database: PostgreSQL via sqlc + pgx
- Config: github.com/caarlos0/env
- Test runner: go test (stdlib)
- Containerisation: Docker
- Distribution: Docker image → Kubernetes
- Auth: JWT bearer tokens
- Feature flags: OpenFeature Go SDK

---

## Architecture

```
cmd/
  metricshub/
    main.go              # entry point — wires dependencies, starts server
internal/
  metrics/
    handler.go           # HTTP handlers (thin)
    service.go           # business logic
    repository.go        # data access
    model.go             # domain types
  config/
    config.go
  server/
    server.go            # Echo instance, middleware, routing
pkg/                     # code safe to import by external packages (if any)
migrations/              # SQL migration files
Dockerfile
Makefile
go.mod
go.sum
README.md
CLAUDE.md
```

- `internal/` enforces encapsulation — external packages cannot import it
- `cmd/` is thin — no business logic, only wiring

---

## Commands

```bash
go run ./cmd/metricshub           # develop
go build ./cmd/metricshub         # build binary
go test ./...                     # run all tests
go test -tags integration ./...   # run integration tests
go vet ./...                      # static analysis
goimports -w .                    # format imports
make migrate-up                   # apply DB migrations
docker build -t metricshub .      # build container image
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
- Do not commit compiled binaries, `*.test` files, or `vendor/` (unless
  vendoring is an explicit project decision — document it in README if so)
- `go.sum` is committed — do not delete or regenerate without cause
- Tag releases with `vX.Y.Z` — Go module proxy uses these
- Do not commit build output, secrets, or dependency directories

---

## Code conventions

### Application setup

- One `Echo` instance created in `internal/server/server.go`
- Register all routes and middleware in `server.go` — no scattered
  `e.GET(...)` calls across packages
- Use `lifespan` / `main.go` for startup and shutdown orchestration

### Configuration

- One `Config` struct in `internal/config/config.go` — loaded from env
  vars at startup; passed explicitly through the dependency graph
- Never read `os.Getenv` directly in application code outside of
  the config loader

### Routing

- Define all routes in `internal/server/server.go` — one place, no
  scattered `e.GET(...)` calls across packages
- Group routes by resource: `e.Group("/api/v1/metrics")` — apply
  middleware at group level, not per-route
- Use named path parameters: `e.GET("/metrics/:id", handler)` — access
  via `c.Param("id")`
- Version all API routes under a prefix: `/api/v1/`, `/api/v2/`

### Handlers

- Handler signature: `func (h *Handler) Create(c echo.Context) error`
- Bind and validate in one step: `c.Bind(&req)` then call a validator —
  never trust unbound input
- Return errors with `c.JSON(code, resp)` or by returning an
  `*echo.HTTPError` — never write directly to `c.Response()`
- Handlers are thin — all business logic belongs in the service layer
- Decode request body explicitly — never trust unvalidated input

### Request binding and validation

- Use `echo.Validator` interface — register a single validator at startup
  (e.g. `go-playground/validator`)
- Call `c.Validate(req)` after `c.Bind(req)` in every handler that
  receives a body
- Treat binding errors and validation errors as `400 Bad Request` —
  return a structured JSON body, not a plain string
- Never use `json.Decoder` directly in handlers — let Echo's binder
  handle it

### Middleware

- Use `echo/middleware` for: `RequestID`, `Logger`, `Recover`, `CORS`,
  `RateLimiter` — configure globally on the root `Echo` instance
- Write custom middleware as `echo.MiddlewareFunc` — keep it stateless;
  inject dependencies via closure
- Order matters: `Recover` → `RequestID` → `Logger` → auth → business
  middleware
- Never put business logic in middleware

### Error handling

- Register a custom `Echo.HTTPErrorHandler` — all errors flow through
  one place
- Map sentinel errors (e.g. `ErrNotFound`) to HTTP status codes in the
  error handler, not in individual handlers
- Return `*echo.HTTPError` for expected errors; let the error handler
  convert unexpected errors to `500`
- Include `request_id` in every error response body for traceability
- Always handle errors — never `_` discard an error return
- Wrap errors with context: `fmt.Errorf("creating metric: %w", err)`
- Use `errors.Is()` and `errors.As()` for inspection — never string
  matching

### Concurrency and graceful shutdown

- Protect shared state with `sync.Mutex` or `sync.RWMutex` — document
  which fields are guarded and by which lock
- Always use `context.Context` as the first argument in functions that
  may block
- Use `errgroup` for structured concurrency — all goroutines started in
  `main.go` under one group, stopped cleanly on context cancellation
- Never start a goroutine without a clear owner and a clear way to stop
  it
- Graceful shutdown: listen for `SIGTERM`, call server shutdown, drain
  in-flight requests, then cancel the root context
- Never hold a lock while performing I/O — risk of deadlock and
  contention

### Authentication

- JWT bearer tokens validated in a shared Echo middleware dependency
- Never log or expose token payloads in error responses

### Feature flags

- Use the OpenFeature Go SDK — wrap the provider behind an interface so
  the provider can be swapped in tests
- Pass the flag client through the dependency graph — constructor
  argument, not a package-level singleton
- In tests, use the in-memory OpenFeature provider
- Every flag has an owner and a removal date set at creation time —
  flags without a removal date are not allowed to merge
- Remove the flag and its dead branch as soon as the rollout is complete
- Never nest feature flags
- Flags are evaluated at runtime, not at startup — never cache a flag
  value for longer than one request lifecycle unless justified
- Evaluate flags at the entry point of the feature — handler or service
  layer, never deep inside domain logic

### Code quality

- Follow **Effective Go** for idioms and design decisions
- `gofmt` / `goimports` — code must be formatted; CI rejects unformatted
  code
- Run `go vet ./...` — fix all warnings before committing
- Run `staticcheck ./...` for additional static analysis
- No unused imports or variables — the compiler rejects these
- Exported symbols must have a doc comment

---

## Testing

- Use stdlib `testing` package — no third-party assertion libraries
- Table-driven tests with `t.Run()` for parameterised cases
- Test the public API of each package — not unexported functions
- Use interfaces to inject dependencies in tests — no monkey-patching
- Component test naming: `Test<UnitOfWork>_<State>_<Expected>`
  e.g. `TestGetMetric_NotFound_Returns404`
- Use `net/http/httptest` with `echo.New()` — no real server needed for
  unit tests
- Call handlers directly: `e.ServeHTTP(rec, req)` — assert on
  `rec.Code` and `rec.Body`
- Integration tests use a real Echo server on a random port — start in
  `TestMain`, share across test functions
- Integration tests in `internal/metrics/*_integration_test.go` behind
  a build tag: `//go:build integration`
- No mocking of the database in integration tests — use a test database
- Run before every commit: `go test ./... && go vet ./...`

---

## Documentation

- Keep `README.md` up to date with setup, run, and test instructions
- Every public module, class, and function has a doc comment
- Architecture decisions recorded as ADRs in `docs/decisions/`