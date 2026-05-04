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
- Python 3.x — for running the structural smoke tests
- An AI agent for validation (Claude Code recommended) — for E2E tests

## First steps

```bash
git clone https://github.com/braboj/solid-ai-templates.git
cd solid-ai-templates
```

No build step, no dependencies to install. All templates are plain Markdown.

## Understand the structure

| File / folder | Read this to understand |
|---------------|------------------------|
| `SPEC.md` | The full composition model — inheritance, OVERRIDE, EXTEND, IDs |
| `CLAUDE.md` | Rules for contributing to this repo |
| `manifest.yaml` | Machine-readable dependency graph |
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

First, run the structural smoke tests to confirm the repo is in good shape:

```bash
py tests/run_smoke.py
```

Then run the system end-to-end with an agent:

1. Open Claude Code in any project directory
2. Attach `INTERVIEW.md` and `stack/python-flask.md`
3. Ask: "Generate a CLAUDE.md for this project using formats/agents.md format"
4. Review the output — this is what users get

Or use the automated E2E runner:

```bash
py tests/run_e2e.py STK-11   # Flask stack
```

## Making your first contribution

See `docs/PLAYBOOK.md` for step-by-step instructions on adding templates,
fixing content, and submitting a PR.

## Conventions to know before you write

- Rules use RFC 2119 keywords: MUST, MUST NOT, SHOULD, MAY
- Every section that another template might reference needs `[ID: ...]`
- Stack files follow the `<prefix>-<name>.md` naming convention (see `CLAUDE.md`)
- `manifest.yaml` must be updated whenever a file is added, removed, or renamed

## Maintainership

This project has a bus factor of 1 — Branimir Georgiev is the sole
author and maintainer. The mitigation is documentation: everything
needed to understand, maintain, and extend the project is in the
repository (SPEC.md, CLAUDE.md, PLAYBOOK.md, ADRs in docs/decisions/,
dev journal). No oral knowledge transfer is required.

If the maintainer becomes unavailable, the project can be forked and
continued from the repository alone.

## Getting help

- `SPEC.md` — answers most "how does X work" questions
- Open a GitHub Discussion if something is unclear