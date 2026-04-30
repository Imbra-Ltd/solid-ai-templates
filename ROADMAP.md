# Roadmap

Single source of truth for project status and planned work.
See `SPEC.md` for design decisions and `README.md` for an overview.

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
- [x] `stack/static-site-astro.md` — Astro islands, client directives (extends static-site)
- [x] `INTERVIEW.md` — agent-driven project setup interview

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

## Phase 3 — Frontend layer

- [x] `frontend/ux.md` — enriched: design system, component-driven development
- [x] `frontend/quality.md` — enriched: linting on save, Core Web Vitals, design patterns

## Phase 4 — Stack expansion

- [x] `stack/python-lib.md` — Python library / CLI (packaging, mypy, ruff, pytest)
- [x] `stack/python-flask.md` — Flask web app (factory pattern, blueprints, migrations)
- [x] `stack/python-fastapi.md` — FastAPI (async, Pydantic v2, DI, OpenAPI)
- [x] `stack/spa-react.md` — React + TypeScript (components, state, RTL, a11y, E2E)
- [x] `stack/go-service.md` — Go service (packages, interfaces, concurrency) — refactored in Phase 8

## Phase 5 — Agent output coverage

- [x] `formats/claude.md` — Claude Code → `CLAUDE.md`
- [x] `formats/cursorrules.md` — Cursor → `.cursor/rules/project.mdc`
- [x] `formats/copilot.md` — GitHub Copilot → `.github/copilot-instructions.md`
- [x] `formats/codex.md` — OpenAI Codex CLI → `AGENTS.md`
- [x] `formats/generic.md` — fallback → `AI_CONTEXT.md`

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
- [x] ~`CONCEPTS.md`~ — removed; `manifest.yaml` serves as the concept-to-file index
- [x] `examples/` — new: three complete generated context files (FastAPI, React SPA, Astro)

## Phase 7 — Quality improvements (post-assessment)

- [x] `backend/messaging.md` — new: brokers, producers, consumers, schema, DLQ, observability, testing
- [x] `stack/python-fastapi.md` — added Feature flags and Messaging sections; updated DEPENDS ON
- [x] `stack/python-flask.md` — added Feature flags and Messaging sections; updated DEPENDS ON
- [x] `stack/go-service.md` — added Feature flags and Messaging sections; updated DEPENDS ON
- [x] `stack/static-site.md` — added ID tags to all sections (required by astro.md OVERRIDE directives)
- [x] `stack/python-django.md` — new: Django 4.2/5.x, DRF, ORM, migrations, admin, pytest-django
- [x] `stack/full-nextjs.md` — new: App Router, Server/Client Components, data fetching, API routes
- [x] `examples/flask-api/CLAUDE.md` — new: InventoryAPI example (Flask + Celery + PostgreSQL)
- [x] `examples/go-service/CLAUDE.md` — new: MetricsHub example (Go + chi + PostgreSQL + Redis)
- [x] `manifest.yaml` — new: machine-readable dependency graph for composition engines

## Phase 8 — Stack expansion (backend, frontend, mobile, DevOps, libraries)

- [x] `frontend/static-site.md` — new: abstract SSG layer (moved from stack/static-site.md)
- [x] `backend/grpc.md` — new: abstract gRPC layer (proto design, status codes, interceptors, buf)
- [x] `stack/python-service.md` — new: abstract Python web service layer (SQLAlchemy, Alembic, pydantic-settings)
- [x] `stack/go-lib.md` — new: base Go library/CLI conventions (packages, errors, quality, tooling)
- [x] `stack/go-service.md` — refactored to extend go-lib; DEPENDS ON simplified
- [x] `stack/spa-vue.md` — new: Vue 3 + Composition API + Pinia + Vitest
- [x] `stack/spa-svelte.md` — new: Svelte 5 runes + Vitest + Playwright
- [x] `stack/full-sveltekit.md` — new: file-based routing, form actions, SSR, Nitro
- [x] `stack/static-site-hugo.md` — new: Go templates, archetypes, content structure
- [x] `stack/node-nestjs.md` — new: modules, controllers, providers, guards, pipes, DI
- [x] `stack/node-express.md` — new: minimal Node.js REST API, Zod validation, Supertest
- [x] `stack/java-spring-boot.md` — new: Java/Kotlin, JPA, Spring Security, Flyway, Testcontainers
- [x] `stack/python-celery-worker.md` — new: standalone Celery worker, retry/backoff, Beat scheduling
- [x] `stack/go-grpc.md` — new: extends go-service + backend/grpc (bufconn, errgroup)
- [x] `stack/python-grpc.md` — new: extends python-lib + backend/grpc (grpcio-aio, pytest-asyncio)
- [x] `stack/java-grpc.md` — new: extends backend/grpc (InProcessServerBuilder, grpc-java lifecycle)
- [x] `stack/mobile-react-native.md` — new: Expo, file-based routing, offline, permissions, Maestro/Detox
- [x] `stack/mobile-flutter.md` — new: Dart 3, Riverpod, go_router, freezed, json_serializable
- [x] `stack/iac-terraform.md` — new: HCL, modules, remote state, workspaces, tfsec, terratest
- [x] `stack/nodejs-lib.md` — new: TypeScript npm library/CLI, tsup, package exports, Vitest
- [x] `stack/rust-lib.md` — new: Rust crate/CLI, thiserror/anyhow, clippy, proptest, crates.io
- [x] `base/deployment.md` — new: deployment targets (cloud/hybrid/offline), certs, LB, service discovery, registries, secrets
- [x] `backend/templating.md` — new: server-side rendering — partials, escaping, caching, CSRF, forms, testing
- [x] `stack/htmx.md` — new: HTMX 2.x, Alpine.js, SSE, OOB swaps, partial responses, Playwright testing
- [x] `stack/go-echo.md` — new: Echo v4 routing, middleware, validation, error handling
- [x] `manifest.yaml` — updated: all new stacks registered with dependency graph
- [x] `SPEC.md` — updated: stack list, backend/ list, frontend/ list

## Phase 9 — Automated testing

- [x] Structural smoke checks — `run_smoke.py` (SYS-01/02, TPL-01/02/03/04, MNF-01)
- [x] E2E stack tests — `run_e2e.py` (STK-01..20, all 20 stacks)
- [x] E2E format tests — `run_e2e.py` (FMT-01..05, all output formats)
- [x] E2E interview tests — `run_e2e.py` (ITV-02/03)
- [x] E2E deployment target tests — `run_e2e.py` (DPL-01..03)
- [x] Timestamped Markdown reports written after every run

## Phase 10 — Agents testing

- [x] Test end-to-end with Claude Code (`CLAUDE.md` output) — automated via `run_e2e.py` (FMT-01)
- [ ] Test end-to-end with OpenAI Codex CLI — automated via `run_e2e.py` (FMT-02)
- [ ] Test end-to-end with Cursor (`.mdc` output) — automated via `run_e2e.py` (FMT-03)
- [ ] Test end-to-end with GitHub Copilot — automated via `run_e2e.py` (FMT-04)
- [ ] Document agent-specific quirks and workarounds

## Phase 11 — Interview UX

- [x] Stack selection table enriched with one-line descriptions
- [x] `README.md` quick start: two paths — direct (stack template only) and interview
- [x] `INTERVIEW.md` rewritten: explore → clarify → propose → generate flow

## Phase 12 — Stack expansion (embedded)

- [x] `stack/c-embedded.md` — new: bare-metal C, GCC + CMake, Unity, HAL, binary + static lib

## Phase 13 — Language-specific base templates

- [x] `base/typescript.md` — new: type design, discriminated unions, naming, strictness

## Phase 14 — Content stacks

- [x] `stack/static-site-tutorial.md` — new: multi-chapter tutorial site (chapters, diagrams, CI split, CC BY-NC-SA 4.0)
- [x] `base/data-quality.md` — new: data sourcing, completeness, freshness, scoring, validation for data-heavy projects

## Phase 15 — Skills

### Generative (produce new artifacts)

- [ ] `/scaffold <stack>` — generate project boilerplate from interview answers + stack template
- [ ] `/generate-context <stack> <format>` — produce CLAUDE.md / AGENTS.md / .cursor/rules from interview + stack + format
- [ ] `/interview` — run the setup interview interactively

### Transformation (change existing code)

- [ ] `/refactor <target-stack>` — refactor code to match a stack template
- [ ] `/migrate <from> <to>` — diff two stacks, produce migration plan
- [ ] `/upgrade` — check code against latest template version, suggest updates

### Review (analyze, don't change)

- [ ] `/review-security` — check code against `base/security.md` + `base/devsecops.md`
- [ ] `/review-quality` — check against `base/quality.md` + `base/review.md`
- [ ] `/review-api` — check against `backend/api.md` + `backend/http.md`
- [ ] `/review-db` — check against `backend/database.md`
- [ ] `/review-a11y` — check against `frontend/ux.md` accessibility rules

### Ops (infrastructure)

- [ ] `/add-ci <platform>` — generate CI config from `platform/` templates
- [ ] `/add-docker` — generate Dockerfile from `base/containers.md`
- [ ] `/add-monitoring` — generate dashboards/alerts from `backend/monitoring.md`

### Infrastructure

- [ ] Define skill wrapper format (thin shell that references existing templates)
- [ ] Claude Code skill integration (first target)
- [ ] Document skill authoring in `docs/PLAYBOOK.md`

## Phase 16 — Assessment and governance

- [x] `base/360.md` — new: four-category project assessment (Value, Quality, Viability, Discovery)
- [x] `base/issues.md` — updated: platform-agnostic issue types and priorities
- [x] `platform/github.md` — updated: canonical label set (12 labels, Atlassian colors)
- [x] `base/readme.md` — updated: capability list requirement, dual-audience
- [x] `docs/decisions/` — new: 3 ADRs (inheritance, labels, 360 analysis)
- [x] `LICENSE` — new: CC BY 4.0
- [x] `docs/ONBOARDING.md` — updated: bus factor documentation
- [x] `README.md` — updated: capability list, structure, links

## Phase 17 — Validation

- [ ] Use the system on a real new project end-to-end (see examples)
- [ ] Use the system on a real refactoring project end-to-end
- [ ] Refine templates based on gaps found during real use
