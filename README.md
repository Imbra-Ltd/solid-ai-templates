# solid-ai-templates

SOLID-inspired composable project templates for LLM agents.

Generate a context file (`CLAUDE.md`, `AGENTS.md`, `.cursor/rules/project.mdc`,
`copilot-instructions.md`, or `AI_CONTEXT.md`) for any project by combining
reusable base templates with framework-specific stack templates — structured
like object-oriented design, built for AI-augmented engineering.

---

## Concept

Most AI context files are written from scratch for every project. This
repository provides a composable system inspired by SOLID principles:

- **S** — Each template covers one concern (git, UX, docs, quality)
- **O** — Base templates are open for extension, closed for modification
- **L** — A specific template (Astro) can replace the base (static site) without breaking anything
- **I** — Projects only answer questions relevant to their type
- **D** — Projects depend on base abstractions, not concrete implementations

---

## Structure

```
base/          # cross-cutting — git, docs, quality (all projects)
frontend/      # frontend layer — UX, CSS, SEO (UI projects only)
backend/       # backend layer — config, HTTP, database, observability
stack/         # concrete stacks — extend base + frontend or backend
output/        # rendering rules per AI tool
INTERVIEW.md   # agent-driven project setup interview
SPEC.md        # design decisions and system architecture
ROADMAP.md     # project status and planned work
```

---

## Supported stacks

| Template | Extends |
|----------|---------|
| `stack/static-site.md` | base |
| `stack/astro.md` | static-site |
| `stack/python-lib.md` | base |
| `stack/flask.md` | python-lib |
| `stack/fastapi.md` | python-lib |
| `stack/react-spa.md` | base |
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

## Roadmap

See `ROADMAP.md`.

---

## Author

[Branimir Georgiev](https://github.com/braboj) — [Imbra.io](https://imbra.io)