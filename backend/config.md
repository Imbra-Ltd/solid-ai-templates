# Backend — Configuration
[ID: backend-config]

## Rules
- All configuration from environment variables — no hardcoded values in source
- Validate all required config at startup — fail fast if anything is missing
- Never hardcode secrets, API keys, or credentials — environment only
- `.env.example` committed with placeholder values; `.env` in `.gitignore`
- Separate configuration per environment (development, testing, production)
- Pass config explicitly to components — no global config objects accessed
  from arbitrary locations