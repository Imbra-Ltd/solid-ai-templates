# Stack — Go Service / CLI
[DEPENDS ON: base/git.md, base/docs.md, base/quality.md, backend/config.md, backend/http.md, backend/database.md, backend/observability.md, backend/quality.md, backend/concurrency.md]

A Go service, API server, or CLI tool. Covers package design, error handling,
interfaces, concurrency, testing, and tooling.

---

## Stack
[ID: go-service-stack]

- Language: Go 1.22+
- HTTP router: [net/http (stdlib) / chi / gin / echo]
- Database: [database/sql + pgx / sqlc / GORM]
- CLI framework: [cobra / flag (stdlib)]
- Config: [viper / env / godotenv]
- Test runner: go test (stdlib)
- Containerisation: Docker
- Distribution: [binary / Docker image / GitHub Releases]

---

## Project structure
[ID: go-service-structure]

Standard layout for a service with one binary:

```
cmd/
  [service]/
    main.go              # entry point — wires dependencies, starts server
internal/
  [feature]/
    handler.go           # HTTP handlers (thin)
    service.go           # business logic
    repository.go        # data access
    model.go             # domain types
  config/
    config.go
  server/
    server.go            # HTTP server setup, middleware, routing
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
- No `utils/` or `helpers/` packages — name packages by domain

---

## Package and interface design
[ID: go-service-packages]

- Small, focused packages — one domain concern per package
- Define interfaces where the caller, not the implementer, owns them
- Keep interfaces small: prefer 1–3 methods
- Accept interfaces, return concrete types (in most cases)
- Avoid package-level `init()` — use explicit initialisation in `main`

---

## Error handling
[ID: go-service-errors]

- Always handle errors — never `_` discard an error return
- Wrap errors with context: `fmt.Errorf("creating user: %w", err)`
- Use `errors.Is()` and `errors.As()` for inspection — never string matching
- Define sentinel errors (`var ErrNotFound = errors.New(...)`) in the package
  that owns the concept
- Log errors once — at the top of the call stack, not at every level

---

## HTTP handlers (if applicable)
[EXTEND: backend-http]

- Decode request body explicitly — never trust unvalidated input
- Use `http.Error()` or a JSON encoder for all error responses

---

## Configuration
[EXTEND: backend-config]

- Use a `Config` struct loaded at startup; pass it explicitly, do not use globals

---

## Concurrency
[EXTEND: backend-concurrency]

- Do not share memory by communicating — communicate by sharing memory sparingly
- Protect shared state with `sync.Mutex` or `sync.RWMutex`; document which
  fields are guarded and by which lock
- Always use `context.Context` as the first argument in functions that may block
- Cancel contexts and clean up goroutines on shutdown — use `errgroup` for
  structured concurrency
- Never start a goroutine without a clear owner and a clear way to stop it

---

## Testing
[EXTEND: base-testing]

- Use stdlib `testing` package — no third-party assertion libraries
- Table-driven tests with `t.Run()` for parameterised cases
- Test the public API of each package — not unexported functions
- Use interfaces to inject dependencies in tests — no monkey-patching
- Component integration tests in `internal/[feature]/*_integration_test.go`
  behind a build tag: `//go:build integration`
- Component test naming: `Test<UnitOfWork>_<State>_<Expected>`
  e.g. `TestCreateUser_DuplicateEmail_ReturnsConflictError`
- Performance tests written with k6 — colocated in `tests/performance/` at
  project root
- Run before every commit: `go test ./... && go vet ./...`

---

## Code quality
[EXTEND: base-quality]

- Follow **Effective Go** (https://go.dev/doc/effective_go) for idioms and
  design decisions — the canonical Go style reference
- Follow **Go Code Review Comments** (https://go.dev/wiki/CodeReviewComments)
  for common pitfalls and reviewer expectations
- `gofmt` / `goimports` — code must be formatted; CI will reject unformatted code
- Run `go vet ./...` — fix all warnings before committing
- Run `staticcheck ./...` for additional static analysis
- No unused imports or variables — the compiler rejects these
- Exported symbols must have a doc comment

---

## Git conventions
[EXTEND: base-git]

- Do not commit compiled binaries, `*.test` files, or `vendor/` (unless vendoring intentionally)
- `go.sum` is committed — do not delete or regenerate without cause
- Tag releases with `vX.Y.Z` — Go module proxy uses these

---

## Commands
```
go run ./cmd/[service]    # develop
go build ./cmd/[service]  # build binary
go test ./...             # run all tests
go vet ./...              # static analysis
goimports -w .            # format imports
make migrate-up           # apply DB migrations (if using Makefile)
docker build -t [name] .  # build container image
```