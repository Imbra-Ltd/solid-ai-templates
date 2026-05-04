# Base — Configuration
[ID: base-config]

Follows the [12-factor app](https://12factor.net/config) principle:
store config in the environment, not in code.

## Rules

- All configuration from environment variables — no hardcoded values in source
- Validate all required config at startup — fail fast if anything is missing
  or invalid
- Never hardcode secrets, API keys, or credentials — environment only
- `.env.example` committed with placeholder values; `.env` in `.gitignore`
- Separate configuration per environment (development, testing, production)
- Pass config explicitly to components — no global config objects accessed
  from arbitrary locations
- Instantiate the config object once at startup — never re-read the environment
  on each call

## Validation

- Validate types, ranges, and formats at load time — not at first use
- Fail immediately on startup if any required variable is missing or malformed
- Use a typed config object — never scatter raw environment variable reads
  across the codebase
- Provide sensible defaults only for optional, non-sensitive settings
- Mark all secrets as required — no defaults for passwords, tokens, or keys

## Secrets management

- In production, source secrets from a dedicated secrets manager (AWS Secrets
  Manager, HashiCorp Vault, GCP Secret Manager) — not from flat `.env` files
- Design secret loading to support rotation without a full redeployment
- Never log config values — redact or omit secrets from startup logs and
  health-check responses
- Reference secrets by name or path, not by embedding them in config files

## Environment separation

| Environment | Logging  | Debug | Database         | Secrets source  |
|-------------|----------|-------|------------------|-----------------|
| development | verbose  | true  | local / Docker   | `.env` file     |
| testing     | minimal  | false | test DB or stub  | hardcoded stubs |
| production  | JSON     | false | managed service  | secrets manager |

## `.env.example` structure

```
# Required — database
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Required — security
SECRET_KEY=change-me
ALLOWED_ORIGINS=http://localhost:3000

# Optional — defaults shown
LOG_LEVEL=info
DEBUG=false
```
