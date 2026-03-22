# solid-ai-templates

Composable, SOLID-inspired templates for generating AI agent context files.

---

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

---

## Quick start

**Prerequisites:** an AI agent that accepts a Markdown context file
(Claude Code, Cursor, GitHub Copilot, or OpenAI Codex CLI).

```bash
git clone https://github.com/Imbra-Ltd/solid-ai-templates.git
```

Open your agent and provide two files:

```
solid-ai-templates/INTERVIEW.md
solid-ai-templates/stack/<your-stack>.md
```

The agent will ask a short set of questions and generate a ready-to-use
context file for your project.

**Available stacks:** `fastapi`, `flask`, `python-lib`, `react-spa`,
`go-service`, `astro`, `static-site`

**Available output formats:** `CLAUDE.md`, `AGENTS.md`,
`.cursor/rules/project.mdc`, `.github/copilot-instructions.md`,
`AI_CONTEXT.md`

---

## Usage

### Generate a context file for a FastAPI project

1. Open Claude Code (or your preferred agent) in a new or existing project.
2. Attach `INTERVIEW.md` and `stack/fastapi.md` to the conversation.
3. The agent asks required questions (project name, database, auth method, etc.).
4. Specify the output format — for Claude Code:

```
Please generate a CLAUDE.md for this project.
```

The agent produces a complete context file that combines base rules (git,
quality, testing, security) with FastAPI-specific conventions (async handlers,
Pydantic v2, OpenAPI).

Expected output: a `CLAUDE.md` file ready to place at the project root.

### Generate for a React SPA

Same steps with `stack/react-spa.md`. The agent applies the frontend layer
(UX, accessibility, CSS conventions) on top of the base rules.

### Compose templates manually

Each template declares its dependencies with `DEPENDS ON` and can override
base rules with `OVERRIDE`. See `SPEC.md` for the full composition rules.

---

## Project structure

```
solid-ai-templates/
├── base/           # Cross-cutting rules — apply to every project
├── backend/        # Backend layer — HTTP, API, database, observability
├── frontend/       # Frontend layer — UX, accessibility, CSS, SEO
├── stack/          # Concrete stacks — extend base + layer templates
├── output/         # Output format guides per agent tool
├── examples/       # Complete generated context files (reference)
├── INTERVIEW.md    # Agent-driven project setup interview
├── SPEC.md         # System design, composition rules, precedence
├── CONCEPTS.md     # Concept-to-file navigation index
└── ROADMAP.md      # Project status and planned work
```

---

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

---

## Supported stacks

| Template | Extends |
|----------|---------|
| `stack/static-site.md` | base |
| `stack/astro.md` | static-site |
| `stack/python-lib.md` | base |
| `stack/flask.md` | python-lib |
| `stack/fastapi.md` | python-lib |
| `stack/react-spa.md` | base + frontend |
| `stack/go-service.md` | base |

## Supported agents

| Agent | Output file | Format guide |
|-------|-------------|--------------|
| Claude Code | `CLAUDE.md` | `output/claude.md` |
| Cursor | `.cursor/rules/project.mdc` | `output/cursorrules.md` |
| GitHub Copilot | `.github/copilot-instructions.md` | `output/copilot.md` |
| OpenAI Codex CLI | `AGENTS.md` | `output/codex.md` |
| Generic / other | `AI_CONTEXT.md` | `output/generic.md` |

---

## Links

- [System design and composition rules](SPEC.md)
- [Concept-to-file navigation index](CONCEPTS.md)
- [Project status and roadmap](ROADMAP.md)
- [Example generated context files](examples/)

---

## License

No license has been declared for this repository yet. All rights reserved
until a license is added.

---

## Author

[Branimir Georgiev](https://github.com/braboj) — [Imbra.io](https://imbra.io)