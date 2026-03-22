# Template System Specification

## Goal

A composable, inheritance-based template system that any LLM agent can use
to generate a project context file (`CLAUDE.md`, `AGENTS.md`, `AI_CONTEXT.md`,
or equivalent) for any type of project — from a static portfolio to a Python
SDK to a React SPA.

Designed to be agent-agnostic: works with Claude Code, Cursor, GitHub Copilot,
OpenAI Codex CLI, or any agent that accepts a Markdown context file. The
output filename is configurable, not hardcoded.

Inspired by SOLID principles: each template has a single responsibility,
is open for extension, and can be composed without modification.

---

## Core concepts

### 1. Base templates (abstract, cross-cutting)

Reusable building blocks covering one concern each. Apply to every project
regardless of stack. Never used directly — always composed into a higher layer.

```
base/
├── git.md         # Committer identity, commits, branching, PR workflow, versioning
├── docs.md        # Rule language, documentation standards, ADR, diagrams, docs-as-code
├── quality.md     # Architecture, code style, security, testing
├── review.md      # Peer review priority, MUST/SHOULD checklists, deviation rules
├── devsecops.md   # SAST, SCA, SBOM, secret detection, license compliance
├── release.md     # Semver, version bump propagation, backward compat, cut-over
├── testing.md     # Test pyramid, coverage thresholds, naming conventions
├── cicd.md        # Pipeline stages, triggers, environments, IaC, deployment
└── containers.md  # Dockerfile, runtime security, resource limits, Kubernetes
```

### 2. Frontend templates (abstract, frontend layer)

Concerns that apply to all frontend projects but not to backend or library
projects. Extend base templates. Never used directly by a project.

```
frontend/
├── ux.md          # UX principles, WCAG 2.1 AA, responsive breakpoints
└── quality.md     # CSS conventions, performance, SEO & analytics
```

### 3. Backend templates (abstract, backend layer)

Concerns shared by all backend services but not by frontend or pure libraries.
Extend base templates. Never used directly by a project.

```
backend/
├── config.md        # env vars, secrets, fail-fast validation
├── http.md          # URI design, methods, headers, HATEOAS, auth, errors
├── api.md           # API-first, OpenAPI, versioning, deprecation, pagination
├── database.md      # migrations, transactions, no raw SQL, connection pooling
├── caching.md       # cache-aside, TTL, invalidation, resilience, stampede
├── auth.md           # authn/authz, JWT, RBAC, sessions, API keys
├── jobs.md           # background jobs, idempotency, retry, DLQ, scheduling
├── concurrency.md    # threads vs. processes vs. async, shared state, structured concurrency
├── microservices.md  # service boundaries, inter-service comms, saga, contract testing
├── errors.md        # classification, propagation, recovery, external failures
├── features.md      # feature flags, rollout strategy, experimentation
├── observability.md # log levels, log format, health check, error visibility
├── monitoring.md    # key metrics, thresholds, alerts, dashboards, incidents
└── quality.md       # layered architecture, security, performance, API stability
```

### 4. Stack templates (concrete)

Technology-specific rules. Each stack declares which layers it depends on.

```
stack/
├── static-site.md    # extends base + frontend — generic static site
├── astro.md          # extends base + frontend + static-site
├── react-spa.md      # extends base + frontend — React + TypeScript
├── python-lib.md     # extends base — Python packaging, mypy, ruff, pytest
├── flask.md          # extends base + backend + python-lib
├── fastapi.md        # extends base + backend + python-lib
└── go-service.md     # extends base + backend
```

### 3. Interview template (orchestrator)

A single file any agent uses to ask the user the required questions before
generating the output context file. Questions are grouped by concern and
reference the relevant base/stack templates.

```
INTERVIEW.md
```

### 4. Output format templates

Rendering rules for each supported AI tool. Describe structure, formatting
constraints, and tone for that tool's context file format.

```
output/
├── claude.md         # Claude Code → CLAUDE.md
├── cursorrules.md    # Cursor → .cursor/rules/project.mdc
├── copilot.md        # GitHub Copilot → .github/copilot-instructions.md
├── codex.md          # OpenAI Codex CLI → AGENTS.md
└── generic.md        # fallback → AI_CONTEXT.md
```

### 5. Profile (generated output)

The context file generated for a specific project by combining interview
answers + base templates + stack template + output format template.

| Agent            | Output file                  | Location        |
|------------------|------------------------------|-----------------|
| Claude Code      | `CLAUDE.md`                  | project root    |
| Cursor           | `.cursor/rules/project.mdc`  | `.cursor/rules/`|
| GitHub Copilot   | `copilot-instructions.md`    | `.github/`      |
| OpenAI Codex CLI | `AGENTS.md`                  | project root    |
| Generic / other  | `AI_CONTEXT.md`              | project root    |

Interop: `AGENTS.md` is also read by Claude Code as a fallback when no
`CLAUDE.md` is present.

---

## Inheritance model

```
base/git.md ────────────────────────────────────────────┐
base/docs.md ───────────────────────────────────────────┤
base/quality.md ────────────────────────────────────────┤
                                                        ▼
frontend/ux.md ─────────────────────────────► stack/static-site.md
frontend/quality.md ────────────────────────►          │
                                                        ▼
                                             stack/astro.md
                                                        │
                                             + INTERVIEW.md answers
                                                        │
                                             + output/claude.md rules
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

Example: `base/testing.md` defines the test naming convention. `stack/fastapi.md`
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

1. User provides `INTERVIEW.md` and a stack template (e.g. `stack/fastapi.md`)
2. Agent reads the stack template, identifies its base dependencies
3. Agent loads the referenced base templates
4. Agent runs the interview (REQUIRED questions only)
5. Agent merges: base defaults + stack overrides + interview answers
6. Agent loads the output format template for the chosen AI tool
7. Agent renders and outputs the final context file

The interview instructions use neutral language ("ask the user") so any
agent can follow them without tool-specific interpretation.

---

## File naming conventions

```
base/[concern].md               # cross-cutting — applies to all projects
frontend/[concern].md           # frontend layer — UI projects only
backend/[concern].md            # backend layer — services and APIs only
stack/[framework].md            # concrete — extends base + frontend or backend
stack/[framework]-[variant].md  # variant of a framework (e.g. astro-ssr.md)
output/[agent].md               # rendering rules for a specific AI tool
INTERVIEW.md                    # orchestrator — always one file
SPEC.md                         # this file
ROADMAP.md                      # project status and planned work
```

---

## Roadmap

See `ROADMAP.md`.