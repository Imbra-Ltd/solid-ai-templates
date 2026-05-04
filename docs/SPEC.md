# Template System Specification

## Goal

A composable, inheritance-based template system that any LLM agent can use
to generate a project context file (`CLAUDE.md` or `AGENTS.md`) for any
type of project — from a static portfolio to a Python SDK to a React SPA.

Designed to be agent-agnostic: works with Claude Code, Codex CLI, Devin,
Cursor, or any agent that reads a Markdown context file.

Inspired by SOLID principles: each template has a single responsibility,
is open for extension, and can be composed without modification.

---

## Core concepts

### 1. Base templates (abstract, cross-cutting)

Reusable building blocks covering one concern each. Apply to every project
regardless of stack. Never used directly — always composed into a higher layer.

### 2. Platform templates (CI and security integration)

CI and security tool mappings specific to a hosting platform. Orthogonal
to the stack choice — a Python project on GitHub and a Python project on
GitLab use the same tools; only the CI config and SAST tool differ.

### 3. Frontend templates (abstract, frontend layer)

Concerns that apply to all frontend projects but not to backend or library
projects. Extend base templates. Never used directly by a project.

### 4. Backend templates (abstract, backend layer)

Concerns shared by all backend services but not by frontend or pure libraries.
Extend base templates. Never used directly by a project.

### 5. Stack templates (concrete)

Technology-specific rules. Each stack declares which layers it depends on.

### Directory listings

Generated from `templates/manifest.yaml` — run `py tools/sync.py` to refresh.

<!-- generated:spec-directories -->
```
base/
├── core/
│   ├── git.md          # Committer identity, commits, branching, PR workflow, versioning
│   ├── docs.md         # Rule language, documentation standards, ADR, diagrams, docs-as-code
│   ├── quality.md      # Architecture, code style, security, testing
│   ├── review.md       # Peer review priority, MUST/SHOULD checklists, deviation rules
│   ├── testing.md      # Test pyramid, coverage thresholds, naming conventions
│   ├── agents.md       # Output structure, models (inline/reference/hybrid), formatting rules
│   └── readme.md       # README structure, badges, quick start, contribution guide
├── security/
│   ├── devsecops.md    # SAST, SCA, SBOM, secret detection, license compliance
│   └── security.md     # Application security rules — input, output, injection, auth, sessions, TLS, headers
├── infra/
│   ├── release.md      # Semver, version bump propagation, backward compat, cut-over
│   ├── cicd.md         # Pipeline stages, triggers, environments, IaC, deployment
│   ├── containers.md   # Dockerfile, runtime security, resource limits, Kubernetes
│   └── deployment.md   # Deployment targets (cloud/hybrid/offline), certs, LB, registries, secrets
├── language/
│   ├── typescript.md   # Type design, naming, strictness — applies to all TypeScript projects
│   └── data-quality.md # Data sourcing, completeness, freshness, scoring — data-heavy projects
└── workflow/
    ├── issues.md       # Issue templates — epic, task, bug, incident, spike
    ├── scope.md        # Scope guard, session protocol, drift prevention
    ├── quality-gates.md # Three-layer gate model (editor, pre-commit, CI), thresholds
    ├── ai-workflow.md  # AI-assisted development lifecycle, work item hierarchy
    └── 360.md          # 360-degree project analysis — four stakeholder perspectives, grading
```

```
platform/
├── github.md       # CodeQL, GitHub Actions, gitleaks action, push protection
└── gitlab.md       # Semgrep OSS, GitLab CI/CD, gitleaks CLI
```

```
frontend/
├── ux.md           # UX principles, WCAG 2.1 AA, responsive breakpoints
├── quality.md      # CSS conventions, performance, SEO & analytics
└── static-site.md  # Abstract SSG rules — content, assets, SEO
```

```
backend/
├── config.md       # Env vars, secrets, fail-fast validation
├── http.md         # URI design, methods, headers, HATEOAS, auth, errors
├── api.md          # API-first, OpenAPI, versioning, deprecation, pagination
├── database.md     # Migrations, transactions, no raw SQL, connection pooling
├── caching.md      # Cache-aside, TTL, invalidation, resilience, stampede
├── auth.md         # Authn/authz, JWT, RBAC, sessions, API keys
├── jobs.md         # Background jobs, idempotency, retry, DLQ, scheduling
├── concurrency.md  # Threads vs. processes vs. async, shared state, structured concurrency
├── messaging.md    # Brokers, producers, consumers, schema, DLQ, observability
├── grpc.md         # Proto design, status codes, interceptors, health check
├── microservices.md # Service boundaries, inter-service comms, saga, contract testing
├── errors.md       # Classification, propagation, recovery, external failures
├── features.md     # Feature flags, rollout strategy, experimentation
├── observability.md # Log levels, log format, health check, error visibility
├── monitoring.md   # Key metrics, thresholds, alerts, dashboards, incidents
├── quality.md      # Layered architecture, security, performance, API stability
└── templating.md   # Server-side rendering, partials, escaping, caching, forms, testing
```

```
stack/
├── htmx.md                     # HTMX 2.x, Alpine.js, SSE, OOB swaps, partial responses
├── static-site-astro.md        # Islands architecture, client directives, content collections
├── static-site-tutorial.md     # Multi-chapter tutorial, diagrams, CC BY-NC-SA
├── spa-react.md                # Client-side app, TypeScript, RTL, a11y
├── full-nextjs.md              # App Router, Server/Client Components, API routes
├── python-lib.md               # Installable package or CLI tool, mypy, ruff, pytest
├── python-service.md           # Generic Python web service, SQLAlchemy, Alembic
├── python-flask.md             # Sync REST API, factory pattern, blueprints
├── python-fastapi.md           # Async REST API, Pydantic v2, DI, OpenAPI
├── python-django.md            # Full web framework, ORM, DRF, admin
├── go-lib.md                   # Importable library or CLI binary
├── go-service.md               # Generic Go HTTP service, chi, structured logging
├── go-echo.md                  # REST API, Echo v4, middleware, validation
├── spa-vue.md                  # Client-side app, Composition API, Pinia, Vitest
├── spa-svelte.md               # Client-side app, Svelte 5 runes, Vitest
├── full-sveltekit.md           # File-based routing, form actions, SSR
├── static-site-hugo.md         # Go templates, archetypes, content structure
├── node-express.md             # Minimal REST API, Zod validation, Supertest
├── node-nestjs.md              # Modules, controllers, providers, guards, pipes, DI
├── java-spring-boot.md         # REST API, JPA, Spring Security, Flyway
├── python-celery-worker.md     # Background tasks, retry/backoff, Beat scheduling
├── go-grpc.md                  # gRPC service, bufconn, errgroup
├── python-grpc.md              # gRPC service, grpcio-aio, proto design
├── java-grpc.md                # gRPC service, grpc-java lifecycle
├── mobile-react-native.md      # iOS/Android, Expo, file-based routing, Maestro
├── mobile-flutter.md           # iOS/Android, Riverpod, go_router, freezed
├── iac-terraform.md            # Infrastructure as code, modules, remote state
├── nodejs-lib.md               # TypeScript npm package or CLI, tsup, Vitest
├── rust-lib.md                 # Rust crate or CLI, thiserror/anyhow, crates.io
└── c-embedded.md               # GCC + CMake, Unity tests, HAL, binary + .a
```
<!-- /generated:spec-directories -->

### 6. Output format template

Rendering rules for the generated output. Describes structure, model
selection (inline/reference/hybrid), and formatting constraints.

```
formats/
└── agents.md    # Output structure, models, formatting rules
```

### 7. Interview template (orchestrator)

A single file any agent uses to ask the user the required questions before
generating the output context file. Questions are grouped by concern and
reference the relevant base/stack templates.

```
INTERVIEW.md
```

### 8. Profile (generated output)

The context file generated for a specific project by combining interview
answers + base templates + stack template + output format template.

| Agent | Output file | Location |
|-------|-------------|----------|
| Claude Code | `CLAUDE.md` | project root |
| Codex CLI, Devin, Cursor, Windsurf | `AGENTS.md` | project root |

Interop: `AGENTS.md` is read by Claude Code as a fallback when no
`CLAUDE.md` is present.

---

## Inheritance model

```
templates/base/core/git.md ────────────────────────────────────────────┐
templates/base/core/docs.md ───────────────────────────────────────────┤
templates/base/core/quality.md ────────────────────────────────────────┤
                                                        ▼
frontend/ux.md ─────────────────────────────► frontend/static-site.md
frontend/quality.md ────────────────────────►          │
                                                        ▼
                                             templates/stack/static-site-astro.md
                                                        │
                                             + templates/INTERVIEW.md answers
                                                        │
                                             + templates/base/core/agents.md rules
                                                        │
                                                        ▼
                                                   CLAUDE.md
```

Rules:
- A stack template MUST reference which base templates it depends on
- A stack template MAY override a base rule — overrides must be explicit
- A stack template MAY add new rules not present in the base
- The agent assembles the final output by merging base defaults + stack
  overrides + interview answers, then applies the output format template

---

## Composition model

Stacks compose only the modules they need — no transitive surprises.
See ADR-004 for the full rationale.

### Core tier

Five base templates apply to every project. They are declared in
`templates/manifest.yaml` under `core:` and loaded automatically during
resolution — stacks do not need to list them in `depends_on`:

- `templates/base/core/quality.md`
- `templates/base/core/git.md`
- `templates/base/core/docs.md`
- `templates/base/core/readme.md`
- `templates/base/core/testing.md`

### Opt-in tiers

Everything else is explicit. Stacks declare what they need:

| Tier | Modules |
|------|---------|
| Language | typescript |
| CI | cicd, quality-gates |
| Security (app) | security |
| Security (pipeline) | devsecops |
| Infrastructure | containers, deployment, release |
| Session | scope, issues, review |
| Specialized | data-quality, 360, ai-workflow |
| Platform | github, gitlab |

### File header policy

`[DEPENDS ON: ...]` headers MUST list direct dependencies only —
matching the manifest's `depends_on` for that entry. Headers MUST NOT
expand transitive dependencies. The manifest is the source of truth.

### Pattern files

Pattern files (`docs/patterns/`) are human reference documentation.
They are NOT part of the dependency graph or agent context. Parent
rules files list which patterns to use as one-line conventions.

---

## Override mechanism

Each base template section is tagged with a unique ID:

```markdown
## Git conventions [ID: base-git]
...
```

A stack template overrides a section by referencing its ID:

```markdown
## Git conventions [OVERRIDE: base-git]
- Always test with `npm run dev` before committing  ← replaces base rule
```

A stack template extends a section by referencing its ID:

```markdown
## Git conventions [EXTEND: base-git]
- Do not commit `dist/` or `node_modules/`  ← added on top of base rules
```

If no override or extend is declared, the base section is used as-is.

---

## Precedence rules

When multiple templates reference the same section ID, the following order
applies — higher numbers win:

1. **Base template** — the default; always the lowest precedence
2. **Layer template** (frontend / backend) — overrides or extends the base
3. **Stack template** — overrides or extends the layer or base
4. **Interview answers** — the highest precedence; always win over any template

Example: `templates/base/core/testing.md` defines the test naming convention. `templates/stack/python-fastapi.md`
extends it with a Python-specific pattern. The interview answer "use BDD-style
names" overrides both. The final output uses the interview answer.

---

## Conflict resolution

A conflict occurs when two templates at the same layer reference the same
section ID with different directives (`OVERRIDE` vs `EXTEND`).

**Rule: the more specific directive wins.**

| Situation | Resolution |
|-----------|------------|
| One template `EXTEND`s, another `OVERRIDE`s the same ID | `OVERRIDE` wins — it replaces the base; the `EXTEND` is applied on top of the overridden content |
| Two templates both `OVERRIDE` the same ID | Error — the agent MUST surface this conflict to the user and ask which override to apply |
| Two templates both `EXTEND` the same ID | Both extensions are applied; order follows the dependency declaration in the stack template |

**When a conflict cannot be resolved automatically**, the agent must:

1. Show the user both conflicting rules
2. Ask which takes precedence
3. Record the decision in the `[OVERRIDES]` section of the interview output

---

## Interview template structure

The interview template groups questions by concern:

```
[IDENTITY]     Project name, owner, URL, deployment target
[STACK]        Framework, JS interactivity, CSS approach, content format
[DESIGN]       Aesthetic, colours, typography
[BRAND]        Tagline, tone, copy rules
[CONTENT]      Sections, data files, pages
[SERVICES]     Analytics, forms, third-party integrations
[BROWSERS]     Supported browsers and versions
[OVERRIDES]    Any base rules the user wants to change
[OUTPUT]       Target AI tool and output file format
```

The agent asks all REQUIRED questions before generating anything.
DEFAULTED sections are pre-filled from the selected base + stack templates.

---

## How an agent uses the system

1. User provides `templates/INTERVIEW.md` and a stack template (e.g. `templates/stack/python-fastapi.md`)
2. Agent reads the stack template, identifies its base dependencies
3. Agent loads the referenced base templates
4. Agent runs the interview (REQUIRED questions only)
5. Agent merges: base defaults + stack overrides + interview answers
6. Agent loads the output format template for the chosen AI tool
7. Agent renders and outputs the final context file

The interview instructions use neutral language ("ask the user") so any
agent can follow them without tool-specific interpretation.

---

## Consumption model (target)

The current workflow (above) requires the agent to manually navigate
template files. The target model replaces hand-curated file lists with
a declarative header that the agent resolves automatically.

### Lifecycle

```
┌─────────────────────────────────────────────────┐
│  1. SETUP (once)                                │
│     Agent runs INTERVIEW.md → generates         │
│     CLAUDE.md with a declaration block          │
├─────────────────────────────────────────────────┤
│  2. STARTUP (every session)                     │
│     Agent reads CLAUDE.md → reads               │
│     templates/manifest.yaml → resolves dependency chain   │
├─────────────────────────────────────────────────┤
│  3. DEVELOPMENT (during session)                │
│     Full context loaded — agent applies rules   │
│     and patterns without prompting              │
├─────────────────────────────────────────────────┤
│  4. UPDATE (on upstream change)                 │
│     git submodule update --remote               │
│     Next session resolves the same chain →      │
│     picks up new/changed rules automatically    │
└─────────────────────────────────────────────────┘
```

### Declaration block

The generated CLAUDE.md contains a machine-readable header instead of
a hand-curated file list:

```markdown
Stack: static-site-astro
Extras: data-quality, 360, issues, scope, review, readme
Platform: github
Resolution: full
```

| Field | Required | Description |
|-------|----------|-------------|
| `Stack` | MUST | Stack ID from `manifest.yaml` |
| `Extras` | MAY | Comma-separated base template IDs not in the stack's dependency chain |
| `Platform` | MAY | Platform ID (`github`, `gitlab`) |
| `Resolution` | MAY | `full` (rules + patterns) or `rules` (rules only); default: `rules` |

### Resolution algorithm

Input: declaration block + `templates/manifest.yaml`.
Output: ordered list of template files to load.

```
1. Look up Stack ID in templates/manifest.yaml
2. Recursively resolve depends_on → collect all
   transitive dependencies (depth-first, deduplicated)
3. Append Extras (skip if already in the resolved set)
4. Append Platform template (if declared)
5. If Resolution = full → for each resolved rules file,
   include its companion *-patterns.md (if it exists
   in manifest.yaml with a depends_on pointing to
   the rules file)
6. Append templates/base/core/agents.md
7. Return the ordered file list
```

Ordering: base → backend/frontend → stack (topological sort of
the dependency graph). Within the same depth level, order follows
the `depends_on` list declaration order.

### Example: static-site-astro (Resolution: full)

```
Declaration:
  Stack: stack-astro
  Extras: data-quality, 360, issues, scope
  Platform: github
  Resolution: full

Resolved (17 files):
  templates/base/core/git.md
  templates/base/core/docs.md
  templates/base/core/quality.md
  templates/base/workflow/quality-gates.md
  templates/base/core/testing.md
  base/testing-patterns.md        ← full resolution
  templates/base/language/typescript.md
  frontend/ux.md
  frontend/quality.md
  frontend/patterns.md            ← full resolution
  frontend/static-site.md
  templates/stack/static-site-astro.md
  base/data-quality.md            ← extra
  base/360.md                     ← extra
  base/issues.md                  ← extra
  base/scope.md                   ← extra
  platform/github.md              ← platform
```

### Example: python-flask (Resolution: rules)

```
Declaration:
  Stack: stack-flask
  Extras: scope, issues
  Platform: github
  Resolution: rules

Resolved (17 files):
  templates/base/core/git.md
  templates/base/core/docs.md
  templates/base/core/quality.md
  stack/python-lib.md
  backend/config.md
  backend/http.md
  backend/database.md
  backend/observability.md
  backend/quality.md
  backend/features.md
  backend/messaging.md
  stack/python-service.md
  stack/python-flask.md
  base/scope.md                   ← extra
  base/issues.md                  ← extra
  platform/github.md              ← platform
  templates/base/core/agents.md               ← output format
```

### Current vs target

| Step | Current | Target |
|------|---------|--------|
| Declaration | Hand-curated file list | `Stack: <id>` + extras |
| Resolution | None — flat list is the resolution | Agent resolves from manifest.yaml |
| Pattern inclusion | Manual — must list each file | Automatic via `Resolution: full` |
| Upstream changes | Must edit startup block manually | Submodule bump is sufficient |

---

## File naming conventions

```
templates/base/[concern].md               # cross-cutting — applies to all projects
templates/frontend/[concern].md           # frontend layer — UI projects only
templates/backend/[concern].md            # backend layer — services and APIs only
templates/stack/[framework].md            # concrete — extends base + frontend or backend
templates/stack/[framework]-[variant].md  # variant of a framework (e.g. astro-ssr.md)
templates/formats/[tool].md               # rendering rules for a specific output format
templates/INTERVIEW.md          # orchestrator — always one file
SPEC.md                         # this file
```

---

## Roadmap

See [GitHub milestones](https://github.com/braboj/solid-ai-templates/milestones).