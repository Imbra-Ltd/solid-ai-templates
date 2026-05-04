# Backend — Quality Attributes
[ID: backend-quality]

## Layered architecture
- Enforce a strict handler → service → repository separation
- No database access in handlers — always go through the service layer
- No HTTP concerns in the service layer — services are framework-agnostic
- Domain logic lives in the service layer, not in models or schemas

## Design patterns

Prefer these patterns for backend concerns:

- **Repository** — abstract all data access behind a repository interface;
  the service layer never constructs queries directly
- **Service layer** — encapsulate business logic in stateless service objects;
  one service per domain aggregate
- **Unit of Work** — coordinate multiple repository operations in a single
  transaction; commit or roll back as one atomic unit
- **Factory / Factory Method** — centralise object construction, especially
  for domain objects with complex invariants
- **Strategy** — swap algorithms or business rules (pricing, validation,
  export format) at runtime without modifying the caller
- **Observer / Event** — decouple producers from consumers for domain events
  (user registered, order placed); use an internal event bus or message queue
- **Circuit Breaker** — wrap all outbound calls to external services;
  fail fast and recover gracefully rather than cascading timeouts
- **Outbox** — when publishing an event must be atomic with a DB write,
  write to an outbox table in the same transaction and relay asynchronously
- **CQRS** — separate read models from write models when query and command
  requirements diverge significantly; do not apply by default

## Security
- Validate and sanitise all input at the boundary before passing it inward
- Apply authentication and authorisation before any business logic executes
- Set security headers on all responses (CORS, HSTS if applicable)
- Rate-limit public endpoints — never expose unbounded write operations
- Rotate secrets regularly; invalidate compromised tokens immediately

## Performance
- Prefer async I/O for network-bound operations
- Cache only when there is a measured need — document cache invalidation strategy
- Avoid N+1 queries — use eager loading or batch fetching
- Set timeouts on all outbound calls (HTTP clients, DB queries)

## API stability
- Never remove or rename a field in a response without a deprecation period
- Increment the API version (`/v2/`) for breaking changes — keep the old version alive
- Document deprecated endpoints; set a removal date before retiring them