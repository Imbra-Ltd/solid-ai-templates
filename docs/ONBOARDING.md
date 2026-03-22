# Onboarding

Welcome to solid-ai-templates. This guide gets a new contributor from zero
to first PR.

## What this project is

A composable, SOLID-inspired template system for generating AI agent context
files. Instead of writing a `CLAUDE.md` or `AGENTS.md` from scratch for every
project, you compose templates from three layers:

```
base/       → rules that apply to every project
backend/    → rules for backend services and APIs
frontend/   → rules for frontend and UI projects
stack/      → concrete, technology-specific rules
```

An agent reads the relevant templates, asks a short interview, and outputs
a ready-to-use context file for Claude Code, Cursor, Copilot, or Codex CLI.

Read `SPEC.md` for the full composition model before contributing.

## Prerequisites

- Git
- A Markdown editor (any)
- An AI agent for validation (Claude Code recommended)

## First steps

```bash
git clone https://github.com/Imbra-Ltd/solid-ai-templates.git
cd solid-ai-templates
```

No build step, no dependencies to install. All templates are plain Markdown.

## Understand the structure

| File / folder | Read this to understand |
|---------------|------------------------|
| `SPEC.md` | The full composition model — inheritance, OVERRIDE, EXTEND, IDs |
| `CLAUDE.md` | Rules for contributing to this repo |
| `ROADMAP.md` | What has been done and what is planned |
| `manifest.yaml` | Machine-readable dependency graph |
| `CONCEPTS.md` | Concept-to-file navigation index |
| `examples/` | Complete generated CLAUDE.md files — the target output |

## How templates relate

Every stack template starts with `[DEPENDS ON: ...]` listing its parent
templates. Read those parent templates first — the stack only adds or overrides
what differs from the parent.

Example chain:
```
base/git.md + base/quality.md + ...
    ↓
stack/python-lib.md
    ↓
stack/python-service.md
    ↓
stack/python-flask.md
```

## Validate your understanding

Before writing any template, run the system end-to-end:

1. Open Claude Code in any project directory
2. Attach `INTERVIEW.md` and `stack/python-flask.md`
3. Ask: "Generate a CLAUDE.md for this project using output/claude.md format"
4. Review the output — this is what users get

## Making your first contribution

See `docs/PLAYBOOK.md` for step-by-step instructions on adding templates,
fixing content, and submitting a PR.

## Conventions to know before you write

- Rules use RFC 2119 keywords: MUST, MUST NOT, SHOULD, MAY
- Every section that another template might reference needs `[ID: ...]`
- Stack files follow the `<prefix>-<name>.md` naming convention (see `CLAUDE.md`)
- `manifest.yaml` must be updated whenever a file is added, removed, or renamed

## Getting help

- `SPEC.md` — answers most "how does X work" questions
- `CONCEPTS.md` — find which file covers a given concept
- Open a GitHub Discussion if something is unclear