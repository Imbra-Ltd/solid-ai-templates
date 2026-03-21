# solid-ai-templates

SOLID-inspired composable project templates for LLM agents.

Generate a `CLAUDE.md`, `.cursorrules`, or `AI_CONTEXT.md` for any project
by combining reusable base templates with framework-specific stack templates —
structured like object-oriented design, built for AI-augmented engineering.

---

## Status

Early design phase. Specification in progress.

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

## Roadmap

- [ ] Base templates (git, ux, docs, quality)
- [ ] Stack templates (static-site, astro, python-lib, react-spa)
- [ ] Interview template (agent-driven project setup)
- [ ] Agent output mapping (CLAUDE.md, .cursorrules, AI_CONTEXT.md)

---

## Author

[Branimir Georgiev](https://github.com/braboj) — [Imbra.io](https://imbra.io)