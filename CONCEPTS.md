# Concept Index

Maps engineering concerns to the template files that cover them.
Use this to find the right file when searching for a specific topic.

---

## Cross-cutting (applies to all projects)

| Concern | File |
|---------|------|
| Commit messages, branching, PR workflow | `base/git.md` |
| Documentation standards, ADRs, docs-as-code | `base/docs.md` |
| Architecture principles, SOLID, code style | `base/quality.md` |
| Code review process and checklists | `base/review.md` |
| Test pyramid, coverage thresholds, naming | `base/testing.md` |
| SAST, SCA, secret scanning, SBOM | `base/devsecops.md` |
| Semantic versioning, release process | `base/release.md` |
| CI/CD pipeline stages, environments | `base/cicd.md` |
| Docker, container security, Kubernetes | `base/containers.md` |

---

## Frontend

| Concern | File |
|---------|------|
| UX principles, WCAG 2.1 AA, responsive breakpoints | `frontend/ux.md` |
| Accessibility testing (axe, Lighthouse, screen readers, keyboard) | `frontend/ux.md` |
| CSS conventions, web vitals, SEO, design patterns | `frontend/quality.md` |
| State management decision guide (local, global, server, form, URL) | `frontend/quality.md` |

---

## Backend

| Concern | File |
|---------|------|
| Environment variables, secrets, config validation | `backend/config.md` |
| HTTP methods, URI design, status codes, HATEOAS | `backend/http.md` |
| API-first, OpenAPI, versioning, deprecation, pagination | `backend/api.md` |
| Migrations, queries, indexing, N+1, connection pooling | `backend/database.md` |
| Authentication, JWT, sessions, API keys | `backend/auth.md` |
| Error classification, propagation, recovery, external failures | `backend/errors.md` |
| Feature flags, rollout strategy, A/B experiments, kill switches | `backend/features.md` |
| Log levels, log format, distributed tracing, health checks | `backend/observability.md` |
| Metrics, dashboards, alerting, incident response | `backend/monitoring.md` |
| Cache-aside, TTL, invalidation, stampede prevention | `backend/caching.md` |
| Background jobs, idempotency, retry, DLQ, scheduling | `backend/jobs.md` |
| Threads vs. async, shared state, structured concurrency | `backend/concurrency.md` |
| Service boundaries, inter-service comms, saga, contracts | `backend/microservices.md` |
| Layered architecture, design patterns, API stability | `backend/quality.md` |

---

## Stack templates

| Stack | File |
|-------|------|
| Generic static site (HTML/CSS/JS) | `stack/static-site.md` |
| Astro (static, islands) | `stack/astro.md` |
| React SPA (TypeScript, Vite) | `stack/react-spa.md` |
| Python library / SDK | `stack/python-lib.md` |
| Flask web application | `stack/flask.md` |
| FastAPI async service | `stack/fastapi.md` |
| Go HTTP service | `stack/go-service.md` |

---

## Output formats

| Target agent | File |
|--------------|------|
| Claude Code → `CLAUDE.md` | `output/claude.md` |
| Cursor → `.cursor/rules/project.mdc` | `output/cursorrules.md` |
| GitHub Copilot → `.github/copilot-instructions.md` | `output/copilot.md` |
| OpenAI Codex CLI → `AGENTS.md` | `output/codex.md` |
| Any other agent → `AI_CONTEXT.md` | `output/generic.md` |

---

## Common questions

| Question | Where to look |
|----------|---------------|
| How do I handle secrets in production? | `backend/config.md` — Secrets management |
| What log level should I use? | `backend/observability.md` — Log levels |
| When should I use a background job? | `backend/jobs.md` — When to use |
| How do I prevent N+1 queries? | `backend/database.md` — Queries |
| What's the correct HTTP status code for X? | `backend/http.md` — Status codes |
| How do I version a breaking API change? | `backend/api.md` — Versioning |
| When should I cache? | `backend/caching.md` — When to cache |
| How do I write a test name? | `base/testing.md` — Naming conventions |
| What naming convention for unit tests? | `base/testing.md` — Naming; stack template for language-specific pattern |
| What naming convention for integration/system tests? | `imbra-knowledge/standards/` — codification scheme |
| What goes in a commit message? | `base/git.md` — Commit message format |
| How do I document an architecture decision? | `base/docs.md` — ADR |
| When should I use async vs. threads? | `backend/concurrency.md` — Decision table |
| How do I design a service boundary? | `backend/microservices.md` — Service boundaries |
| What accessibility standard should I meet? | `frontend/ux.md` — Accessibility |
| How do I structure a Docker image? | `base/containers.md` — Dockerfile |
| What does the generated output look like? | `examples/` — three worked examples |

---

## System files

| File | Purpose |
|------|---------|
| `SPEC.md` | System architecture, inheritance model, override mechanism |
| `INTERVIEW.md` | Questions an agent asks before generating a context file |
| `ROADMAP.md` | Delivery phases and completion status |
| `CONCEPTS.md` | This file — concept-to-file navigation index |
| `examples/` | Complete generated context files for three representative projects |