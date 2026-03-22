# Roadmap

Single source of truth for project status and planned work.
See `SPEC.md` for design decisions and `README.md` for an overview.

---

## Phase 1 — Foundation

- [x] `base/git.md` — committer identity, commits, branching, PR workflow, versioning
- [x] `base/docs.md` — rule language, documentation standards, ADR, diagrams, docs-as-code
- [x] `base/quality.md` — architecture, code style, security, testing
- [x] `base/review.md` — peer review priority, MUST/SHOULD checklists
- [x] `base/devsecops.md` — SAST, SCA, SBOM, secret detection, license compliance
- [x] `base/release.md` — semver, version bump propagation, backward compat, cut-over
- [x] `base/testing.md` — test pyramid, coverage thresholds, naming conventions
- [x] `base/cicd.md` — pipeline stages, triggers, environments, IaC, deployment
- [x] `base/containers.md` — Dockerfile, runtime security, resource limits, Kubernetes
- [x] `frontend/ux.md` — UX principles, WCAG 2.1 AA, responsive breakpoints
- [x] `frontend/quality.md` — CSS conventions, performance, SEO
- [x] `stack/static-site.md` — generic static site (any generator)
- [x] `stack/astro.md` — Astro islands, client directives (extends static-site)
- [x] `INTERVIEW.md` — agent-driven project setup interview

---

## Phase 2 — Backend layer

- [x] `backend/http.md` — URI design, headers, HATEOAS, auth, RFC 9457 errors
- [x] `backend/observability.md` — log levels with examples, JSON format, distributed tracing
- [x] `backend/api.md` — API-first, OpenAPI, versioning, deprecation headers, pagination
- [x] `backend/monitoring.md` — key metrics, thresholds, alerts, dashboards, incidents
- [x] `backend/caching.md` — cache-aside, keys, TTL, invalidation, resilience, stampede
- [x] `backend/auth.md` — authn/authz, JWT, RBAC, sessions, API keys, token transport
- [x] `backend/jobs.md` — idempotency, retry/backoff, DLQ, scheduling-as-code, observability
- [x] `backend/concurrency.md` — when-to-use table, shared state, structured concurrency
- [x] `backend/microservices.md` — boundaries, inter-service comms, saga, contract testing
- [x] `backend/config.md` — env vars, validation, secrets management, environment separation
- [x] `backend/database.md` — migrations, queries, indexing, N+1, connection pooling

---

## Phase 3 — Frontend layer

- [x] `frontend/ux.md` — enriched: design system, component-driven development
- [x] `frontend/quality.md` — enriched: linting on save, Core Web Vitals, design patterns

---

## Phase 4 — Stack expansion

- [x] `stack/python-lib.md` — Python library / CLI (packaging, mypy, ruff, pytest)
- [x] `stack/flask.md` — Flask web app (factory pattern, blueprints, migrations)
- [x] `stack/fastapi.md` — FastAPI (async, Pydantic v2, DI, OpenAPI)
- [x] `stack/react-spa.md` — React + TypeScript (components, state, RTL, a11y, E2E)
- [x] `stack/go-service.md` — Go service / CLI (packages, interfaces, concurrency)

---

## Phase 5 — Agent output coverage

- [x] `output/claude.md` — Claude Code → `CLAUDE.md`
- [x] `output/cursorrules.md` — Cursor → `.cursor/rules/project.mdc`
- [x] `output/copilot.md` — GitHub Copilot → `.github/copilot-instructions.md`
- [x] `output/codex.md` — OpenAI Codex CLI → `AGENTS.md`
- [x] `output/generic.md` — fallback → `AI_CONTEXT.md`

---

## Phase 6 — Quality pass

- [x] `base/quality.md` — added Readability and Maintainability sections
- [x] `base/review.md` — sharpened readability and simplicity criteria with measurable rules
- [x] `backend/config.md` — expanded validation, secrets management, environment separation
- [x] `backend/database.md` — expanded indexing, N+1 prevention, soft deletes, testing
- [x] `backend/errors.md` — new: error classification, propagation, recovery, external failures
- [x] `backend/features.md` — new: feature flags, rollout strategy, experimentation, kill switches
- [x] `frontend/quality.md` — added state management decision guide
- [x] `frontend/ux.md` — added accessibility testing (axe, Lighthouse, screen reader, keyboard)
- [x] `SPEC.md` — documented precedence rules and OVERRIDE/EXTEND conflict resolution
- [x] `CONCEPTS.md` — new: concept-to-file navigation index
- [x] `examples/` — new: three complete generated context files (FastAPI, React SPA, Astro)

---

## Phase 7 — Testing

- [ ] Test end-to-end with Claude Code (`CLAUDE.md` output)
- [ ] Test end-to-end with Cursor (`.mdc` output)
- [ ] Test end-to-end with GitHub Copilot
- [ ] Test end-to-end with OpenAI Codex CLI
- [ ] Document agent-specific quirks and workarounds

---

## Phase 8 — Validation

- [ ] Use the system on a real new project end-to-end
- [ ] Use the system on a real refactoring project end-to-end
- [ ] Refine templates based on gaps found during real use