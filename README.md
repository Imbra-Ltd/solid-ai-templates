# SOLID-AI Templates

Composable, SOLID-inspired templates for generating AI agent context files.

## What it does

- Generate consistent `CLAUDE.md` or `AGENTS.md` files for any project
- Compose rules from reusable layers — base, backend/frontend, stack
- Cover 30+ technology stacks (Python, Go, Java, Node, Rust, mobile, DevOps)
- Output for any agent — Claude Code, Cursor, Copilot, Codex CLI
- Run a 360-degree project assessment across four perspectives (user,
  engineer, analyst, marketer)
- Enforce standardized issue labels, quality gates, and review processes

## Overview

Most AI context files are written from scratch for each project and quickly
fall out of sync. This repository provides a reusable template system —
structured like object-oriented design — where base rules are defined once
and composed with stack-specific extensions to produce a complete, consistent
context file for any project type.

Works for new projects and refactoring alike — the generated context file
describes how code *should be written*, giving your agent a consistent target
to work toward whether starting from scratch or improving existing code.

## Quick start

**Prerequisites:** an AI agent that accepts a Markdown context file
(Claude Code, Cursor, GitHub Copilot, or OpenAI Codex CLI).

```bash
git clone https://github.com/Imbra-Ltd/solid-ai-templates.git
```

### Direct — attach a stack template

Attach the stack template, e.g. for a Go service:

```
solid-ai-templates/stack/go-service.md
```

Then provide an instruction with your project details:

> "Generate a CLAUDE.md. Name: my-service, owner: Acme,
> repo: github.com/acme/my-service, database: PostgreSQL, auth: JWT."

To save typing for a setup your team uses repeatedly, create a Markdown file
with pre-filled answers and attach it alongside the stack template:

```markdown
# My project defaults

- Language: Go 1.22
- Framework: Echo
- Deployment target: cloud
- Distribution: Docker image
- Database: PostgreSQL via pgx v5
- Cache: Redis via go-redis
- API style: REST / OpenAPI
- Auth: JWT bearer tokens
```

Attach both files and say: *"Generate a CLAUDE.md. Name: X, owner: Y, repo: Z."*

### Interview — let the agent guide you

To explore your project requirements interactively, attach the interview 
template:

```
solid-ai-templates/INTERVIEW.md
```

The agent explores what you want to build, proposes a stack, and generates
the file once you confirm.

**Available output formats:** `CLAUDE.md` (Claude Code),
`AGENTS.md` (Codex CLI, Devin, Cursor, Windsurf)

## Usage

### Generate a context file via interview

1. Open your agent (Claude Code, Cursor, etc.).
2. Attach `INTERVIEW.md`.
3. The agent explores what you want to build, asks a few clarifying questions,
   proposes a stack, and generates the file once you confirm.

Expected output: a `CLAUDE.md` (or equivalent) ready to place at your project root.

### Generate a context file directly

1. Open your agent.
2. Attach the relevant stack template (e.g. `stack/python-fastapi.md`).
3. Provide your answers inline:

```
Generate a CLAUDE.md. Name: my-service, owner: Acme,
repo: github.com/acme/my-service, database: PostgreSQL, auth: JWT.
```

No questions asked — the agent generates immediately.

### Vendor as a git submodule

Check the templates into your project so your agent file can reference them
directly:

```bash
git submodule add https://github.com/Imbra-Ltd/solid-ai-templates.git docs/solid-ai-templates
```

Then reference the base rules from your `CLAUDE.md` (or equivalent) and add
project-specific overrides inline:

```markdown
Quality conventions defined in `docs/solid-ai-templates/base/quality.md`.
```

To pull template updates across all projects: `git submodule update --remote`.

### Compose templates manually

Each template declares its dependencies with `DEPENDS ON` and can override
base rules with `OVERRIDE`. See `SPEC.md` for the full composition rules.


## Examples

The examples below use Claude Code. For other agents, replace the `Attach:` step
with the equivalent file attachment mechanism for your tool.

### Start a new project

```
Attach: INTERVIEW.md

I want to build a new project. Guide me through the setup and generate a CLAUDE.md.
```

Or directly if you already know your stack:

```
Attach: stack/python-fastapi.md

Generate a CLAUDE.md for a new project.
Name: my-service, owner: Acme, repo: github.com/acme/my-service,
database: PostgreSQL, auth: JWT.
```

### Refactor an existing project

```
Attach: stack/python-fastapi.md

Generate a CLAUDE.md for an existing project I want to refactor.
Name: my-service, owner: Acme, repo: github.com/acme/my-service,
database: PostgreSQL, auth: JWT.
```

### Apply a hotfix

If the project already has a `CLAUDE.md`:

```
Read the repository and fix the following bug: <describe the bug>.
Follow the conventions in CLAUDE.md — keep the change minimal,
add a regression test, and use the correct error handling and git conventions.
```

If the project has no `CLAUDE.md` yet (legacy code):

```
Attach: stack/<your-stack>.md

Generate a CLAUDE.md for this project first.
Name: <name>, owner: <owner>, repo: <repo>.
Then read the repository and fix the following bug: <describe the bug>.
Keep the change minimal and add a regression test.
```

### Review code against project conventions

If the project already has a `CLAUDE.md`:

```
Review this file against the conventions in CLAUDE.md and list any violations.
```

If the project has no `CLAUDE.md` yet (legacy code):

```
Attach: stack/<your-stack>.md

Generate a CLAUDE.md for this project first.
Name: <name>, owner: <owner>, repo: <repo>.
Then review this file against the generated conventions and list any violations.
```

### Migrate to a new stack

```
Attach: stack/<target-stack>.md

Generate a CLAUDE.md for the target stack I am migrating to.
Name: <name>, owner: <owner>, repo: <repo>.
Then read the repository and migrate one module at a time toward
the conventions in the generated CLAUDE.md.
```

## Project structure

```
solid-ai-templates/
├── base/           # Cross-cutting rules — apply to every project
├── backend/        # Backend layer — HTTP, API, database, observability
├── frontend/       # Frontend layer — UX, accessibility, CSS, SEO
├── platform/       # CI and security tool mappings (GitHub, GitLab)
├── stack/          # Concrete stacks — extend base + layer templates
├── formats/        # Output format guides per agent tool
├── examples/       # Complete generated context files (reference)
├── tests/          # Smoke and E2E test runners and specs
├── tools/          # sync.py — generates tables from manifest.yaml
├── docs/           # Onboarding, playbook, decision logs
├── INTERVIEW.md    # Agent-driven project setup interview
├── SPEC.md         # System design, composition rules, precedence
└── ROADMAP.md      # Project status and planned work
```

## Development setup

```bash
git clone https://github.com/Imbra-Ltd/solid-ai-templates.git
cd solid-ai-templates
```

No build step or runtime dependencies — all templates are plain Markdown.

**To add a new stack template:**

1. Create `stack/<name>.md` following the structure of an existing stack.
2. Declare `DEPENDS ON` at the top referencing the base and layer templates
   it builds on.
3. Register in `manifest.yaml` under `stacks:`.
4. Run `py tools/sync.py` to update generated tables.
5. Add a `examples/<name>/CLAUDE.md` to demonstrate the output.

**To verify your changes:** open your agent, attach the new template alongside
`INTERVIEW.md`, run through the interview, and confirm the generated output
is coherent and complete.

## Supported stacks

<!-- generated:readme-stacks -->
| Template | Layer | Description |
|----------|-------|-------------|
| `stack/htmx.md` | hypermedia | HTMX 2.x, Alpine.js, SSE, OOB swaps, partial responses |
| `stack/static-site-astro.md` | static | Islands architecture, client directives, content collections |
| `stack/static-site-tutorial.md` | static | Multi-chapter tutorial, diagrams, CC BY-NC-SA |
| `stack/spa-react.md` | frontend | Client-side app, TypeScript, RTL, a11y |
| `stack/full-nextjs.md` | full-stack | App Router, Server/Client Components, API routes |
| `stack/python-lib.md` | library | Installable package or CLI tool, mypy, ruff, pytest |
| `stack/python-service.md` | abstract | Generic Python web service, SQLAlchemy, Alembic |
| `stack/python-flask.md` | backend | Sync REST API, factory pattern, blueprints |
| `stack/python-fastapi.md` | backend | Async REST API, Pydantic v2, DI, OpenAPI |
| `stack/python-django.md` | backend | Full web framework, ORM, DRF, admin |
| `stack/go-lib.md` | library | Importable library or CLI binary |
| `stack/go-service.md` | abstract | Generic Go HTTP service, chi, structured logging |
| `stack/go-echo.md` | backend | REST API, Echo v4, middleware, validation |
| `stack/spa-vue.md` | frontend | Client-side app, Composition API, Pinia, Vitest |
| `stack/spa-svelte.md` | frontend | Client-side app, Svelte 5 runes, Vitest |
| `stack/full-sveltekit.md` | full-stack | File-based routing, form actions, SSR |
| `stack/static-site-hugo.md` | static | Go templates, archetypes, content structure |
| `stack/node-express.md` | backend | Minimal REST API, Zod validation, Supertest |
| `stack/node-nestjs.md` | backend | Modules, controllers, providers, guards, pipes, DI |
| `stack/java-spring-boot.md` | backend | REST API, JPA, Spring Security, Flyway |
| `stack/python-celery-worker.md` | backend | Background tasks, retry/backoff, Beat scheduling |
| `stack/go-grpc.md` | backend | gRPC service, bufconn, errgroup |
| `stack/python-grpc.md` | backend | gRPC service, grpcio-aio, proto design |
| `stack/java-grpc.md` | backend | gRPC service, grpc-java lifecycle |
| `stack/mobile-react-native.md` | mobile | iOS/Android, Expo, file-based routing, Maestro |
| `stack/mobile-flutter.md` | mobile | iOS/Android, Riverpod, go_router, freezed |
| `stack/iac-terraform.md` | DevOps | Infrastructure as code, modules, remote state |
| `stack/nodejs-lib.md` | library | TypeScript npm package or CLI, tsup, Vitest |
| `stack/rust-lib.md` | library | Rust crate or CLI, thiserror/anyhow, crates.io |
| `stack/c-embedded.md` | embedded | GCC + CMake, Unity tests, HAL, binary + .a |
<!-- /generated:readme-stacks -->

## Supported agents

| Agent | Output file |
|-------|-------------|
| Claude Code | `CLAUDE.md` |
| Codex CLI, Devin, Cursor, Windsurf | `AGENTS.md` |

See `formats/agents.md` for structure, models, and formatting rules.

## Links

- [System design and composition rules](SPEC.md)
- [Project status and roadmap](ROADMAP.md)
- [Example generated context files](examples/)
- [Onboarding guide](docs/ONBOARDING.md)
- [Operational playbook](docs/PLAYBOOK.md)
- [Architecture decision records](docs/decisions/)

## License

[CC BY 4.0](LICENSE) — Creative Commons Attribution 4.0 International.
You are free to use, share, and adapt the templates for any purpose,
including commercial use, as long as you give attribution.

## Author

[Branimir Georgiev](https://github.com/braboj) — [Imbra.io](https://imbra.io)
