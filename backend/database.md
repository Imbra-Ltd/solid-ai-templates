# Backend — Database Conventions
[ID: backend-database]

## Schema changes
- All schema changes via migrations — never edit the database manually
- Migrations are committed to source control
- Never regenerate or modify a migration that is already merged
- One migration per logical change — do not batch unrelated schema changes

## Queries
- No raw SQL strings — use an ORM or query builder
- Use parameterised queries if raw SQL is unavoidable — never string interpolation
- No unbounded queries — always apply a limit or filter

## Transactions
- Wrap multi-step writes in a transaction — commit only after all writes succeed
- Never leave a transaction open across an HTTP request boundary

## Connections
- Use a connection pool — never open a new connection per request
- Inject the database session/connection as a dependency — no global DB handles