# SOLID-AI Templates

Composable, SOLID-inspired templates for generating AI agent context files.

## Overview

Most AI context files (`CLAUDE.md`, `AGENTS.md`, `.cursor/rules/project.mdc`)
are written from scratch for each project and quickly fall out of sync.
This repository provides a reusable template system — structured like
object-oriented design — where base rules are defined once and composed with
stack-specific extensions to produce a complete, consistent context file for
any project type.

The system is agent-agnostic: the same templates produce output for Claude
Code, Cursor, GitHub Copilot, or OpenAI Codex CLI by applying a different
output format guide.

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

**Available output formats:** `CLAUDE.md`, `AGENTS.md`,
`.cursor/rules/project.mdc`, `.github/copilot-instructions.md`,
`AI_CONTEXT.md`

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
├── stack/          # Concrete stacks — extend base + layer templates
├── formats/        # Output format guides per agent tool
├── examples/       # Complete generated context files (reference)
├── INTERVIEW.md    # Agent-driven project setup interview
├── SPEC.md         # System design, composition rules, precedence
├── CONCEPTS.md     # Concept-to-file navigation index
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
3. Add the stack to the supported stacks table in this README.
4. Add an entry to `CONCEPTS.md`.
5. Add a `examples/<name>/CLAUDE.md` to demonstrate the output.

**To verify your changes:** open your agent, attach the new template alongside
`INTERVIEW.md`, run through the interview, and confirm the generated output
is coherent and complete.

## Supported stacks

| Template                        | Layer      | Extends                                       |
|---------------------------------|------------|-----------------------------------------------|
| `stack/python-lib.md`           | library    | base                                          |
| `stack/python-service.md`       | abstract   | base + backend + python-lib                   |
| `stack/python-flask.md`         | backend    | python-service                                |
| `stack/python-fastapi.md`       | backend    | python-service + backend/concurrency          |
| `stack/python-django.md`        | backend    | python-service + backend/api + backend/auth   |
| `stack/python-celery-worker.md` | backend    | base + backend/jobs + python-lib              |
| `stack/go-lib.md`               | library    | base                                          |
| `stack/go-service.md`           | abstract   | base + backend + go-lib                       |
| `stack/go-echo.md`              | backend    | go-service                                    |
| `stack/go-grpc.md`              | backend    | go-service + backend/grpc                     |
| `stack/python-grpc.md`          | backend    | python-lib + backend/grpc                     |
| `stack/java-grpc.md`            | backend    | base + backend/grpc                           |
| `stack/node-express.md`         | backend    | base + backend                                |
| `stack/node-nestjs.md`          | backend    | base + backend                                |
| `stack/java-spring-boot.md`     | backend    | base + backend                                |
| `stack/spa-react.md`            | frontend   | base + frontend                               |
| `stack/spa-vue.md`              | frontend   | base + frontend                               |
| `stack/spa-svelte.md`           | frontend   | base + frontend                               |
| `stack/full-nextjs.md`          | full-stack | base + frontend + react-spa + backend partial |
| `stack/full-sveltekit.md`       | full-stack | base + frontend + svelte + backend partial    |
| `stack/static-site-astro.md`    | static     | base + frontend + frontend/static-site        |
| `stack/static-site-hugo.md`     | static     | base + frontend + frontend/static-site        |
| `stack/static-site-tutorial.md` | static     | static-site-astro + base/issues + base/scope  |
| `stack/mobile-react-native.md`  | mobile     | base + react-spa + backend/auth               |
| `stack/mobile-flutter.md`       | mobile     | base                                          |
| `stack/iac-terraform.md`        | DevOps     | base                                          |
| `stack/nodejs-lib.md`           | library    | base                                          |
| `stack/rust-lib.md`             | library    | base                                          |
| `stack/c-embedded.md`           | embedded   | base                                          |
| `stack/htmx.md`                 | hypermedia | backend/templating                            |

## Supported agents

| Agent            | Output file                       | Format guide             |
|------------------|-----------------------------------|--------------------------|
| Claude Code      | `CLAUDE.md`                       | `formats/claude.md`      |
| Cursor           | `.cursor/rules/project.mdc`       | `formats/cursorrules.md` |
| GitHub Copilot   | `.github/copilot-instructions.md` | `formats/copilot.md`     |
| OpenAI Codex CLI | `AGENTS.md`                       | `formats/codex.md`       |
| Generic / other  | `AI_CONTEXT.md`                   | `formats/generic.md`     |

## Links

- [System design and composition rules](SPEC.md)
- [Concept-to-file navigation index](CONCEPTS.md)
- [Project status and roadmap](ROADMAP.md)
- [Example generated context files](examples/)

## License

No license has been declared for this repository yet. All rights reserved
until a license is added.

## Author

[Branimir Georgiev](https://github.com/braboj) — [Imbra.io](https://imbra.io)
