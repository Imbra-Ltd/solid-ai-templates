# Stack — Go Echo Service
[DEPENDS ON: templates/stack/go-service.md]

Extends the Go service stack with Echo-specific rules. Covers routing,
middleware, request binding, validation, error handling, and graceful shutdown.

---

## Stack
[ID: go-echo-stack]
[OVERRIDE: go-service-stack]

- Language: Go 1.22+
- HTTP framework: Echo v4
- Database: [database/sql + pgx / sqlc / GORM]
- Config: [github.com/caarlos0/env / viper]
- Test runner: go test (stdlib)
- Containerisation: Docker
- Distribution: [binary / Docker image / GitHub Releases]

---

## Routing
[ID: go-echo-routing]

- Define all routes in `internal/server/server.go` — one place, no scattered
  `e.GET(...)` calls across packages
- Group routes by resource: `e.Group("/api/v1/users")` — apply middleware
  at group level, not per-route
- Use named path parameters: `e.GET("/users/:id", handler)` — access via
  `c.Param("id")`
- Version all API routes under a prefix: `/api/v1/`, `/api/v2/`

---

## Handlers
[EXTEND: go-service-http]

- Handler signature: `func (h *Handler) Create(c echo.Context) error`
- Bind and validate in one step: `c.Bind(&req)` then call a validator —
  never trust unbound input
- Return errors with `c.JSON(code, resp)` or by returning an `*echo.HTTPError`
  — never write directly to `c.Response()`

---

## Request binding and validation
[ID: go-echo-validation]

- Use `echo.Validator` interface — register a single validator at startup
  (e.g. `go-playground/validator`)
- Call `c.Validate(req)` after `c.Bind(req)` in every handler that receives
  a body
- Treat binding errors and validation errors as `400 Bad Request` — return
  a structured JSON body, not a plain string
- Never use `json.Decoder` directly in handlers — let Echo's binder handle it

---

## Middleware
[ID: go-echo-middleware]

- Use `echo/middleware` for: `RequestID`, `Logger`, `Recover`, `CORS`,
  `RateLimiter` — configure globally on the root `Echo` instance
- Write custom middleware as `echo.MiddlewareFunc` — keep it stateless;
  inject dependencies via closure
- Order matters: `Recover` → `RequestID` → `Logger` → auth → business
  middleware
- Never put business logic in middleware

---

## Error handling
[EXTEND: backend-errors]

- Register a custom `Echo.HTTPErrorHandler` — all errors flow through one place
- Map sentinel errors (e.g. `ErrNotFound`) to HTTP status codes in the error
  handler, not in individual handlers
- Return `*echo.HTTPError` for expected errors; let the error handler convert
  unexpected errors to `500`
- Include `request_id` in every error response body for traceability

---

## Testing
[EXTEND: go-service-testing]

- Use `net/http/httptest` with `echo.New()` — no real server needed for
  unit tests
- Call handlers directly: `e.ServeHTTP(rec, req)` — assert on
  `rec.Code` and `rec.Body`
- Integration tests use a real Echo server on a random port — start in
  `TestMain`, share across test functions

---

## Commands
```
go run ./cmd/[service]           # develop
go build ./cmd/[service]         # build binary
go test ./...                    # run all tests
go test -tags integration ./...  # run integration tests
go vet ./...                     # static analysis
goimports -w .                   # format imports
make migrate-up                  # apply DB migrations
docker build -t [name] .         # build container image
```