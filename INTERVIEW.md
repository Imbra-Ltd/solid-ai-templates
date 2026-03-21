# Interview Template

<!--
INSTRUCTIONS FOR THE AGENT
============================
This file drives the project setup interview. When a user provides this
file along with a stack template, follow these steps:

1. Identify which stack template the user has selected
2. Load the stack template and its base dependencies
3. Ask ALL questions marked [REQUIRED] below, grouped by section
4. For [DEFAULTED] sections, confirm the defaults with the user or skip
5. Generate the output context file using the answers + loaded templates
6. Ask the user which output format they want:
   - CLAUDE.md (Claude / Claude Code)
   - .cursorrules (Cursor)
   - AI_CONTEXT.md (generic)

Ask all REQUIRED questions before generating anything.
-->

---

## Step 1 — Select stack [REQUIRED]

Which stack template applies to this project?

- `stack/static-site.md` — generic static site (any framework)
- `stack/astro.md` — Astro static site
- `stack/python-lib.md` — Python library or CLI tool
- `stack/flask.md` — Flask web application or API
- `stack/fastapi.md` — FastAPI backend
- `stack/react-spa.md` — React single-page application (TypeScript)
- `stack/go-service.md` — Go service, API server, or CLI tool

---

## Step 2 — Project identity [REQUIRED]

1. What is the project name?
2. What is it for, and who is it for? (one sentence)
3. Who is the owner? (name, GitHub handle, contact email)
4. Where will it be deployed? (GitHub Pages, Netlify, Vercel, PyPI, etc.)
5. What is the live URL or package name, if known?

---

## Step 3 — Stack details [REQUIRED]

*(Questions vary by selected stack template — see stack file for specifics)*

General questions:
1. Will any part of the project need client-side interactivity? If yes, which framework?
2. What is the CSS approach? (plain CSS, Tailwind, CSS modules, none)
3. How is content managed? (JSON files, CMS, Markdown, hardcoded)

---

## Step 4 — Design [REQUIRED]

1. How would you describe the visual aesthetic? (e.g. minimal, bold, playful, technical)
2. What is the background colour or colour scheme?
3. What is the primary accent colour?
4. What fonts are you using? (Google Fonts, self-hosted, system fonts)

---

## Step 5 — Brand voice [REQUIRED]

1. What is the tagline or brand name?
2. How would you describe the tone? (e.g. direct, friendly, technical, formal)
3. What name or handle should be used in body copy?
4. Are there any terms or variants to avoid?

---

## Step 6 — Content structure [REQUIRED]

1. What sections or pages does the project have?
2. For each section, is the content driven by a data file or hardcoded?
3. Are there pages beyond the homepage? (e.g. privacy policy, about, 404)

---

## Step 7 — Third-party services [REQUIRED]

1. Will the project use analytics? (Plausible, Google Analytics, etc.)
2. Will there be a contact form or external integrations?
3. Any other external services? (search indexing, CDN, payment, etc.)

---

## Step 8 — Browser support [REQUIRED]

1. Which browsers must the project support?
2. Is there a minimum version requirement?
   *(Default: last 2 versions of Chrome, Firefox, Safari, Edge)*

---

## Step 9 — Git conventions [DEFAULTED]

Defaults from `base/git.md`. Confirm or override:
- Conventional commit prefixes: `feat:`, `fix:`, `chore:`, `docs:`, etc.
- Branch naming: `feat/`, `fix/`, `chore/`, `docs/`
- Versioning: `vA.B.C.D` with git tags, release via PR

Any deviations?

---

## Step 10 — Output format [REQUIRED]

Which AI tool will use this context file?

| Choice | Output file | Location | Format guide |
|--------|-------------|----------|--------------|
| Claude Code | `CLAUDE.md` | project root | `output/claude.md` |
| Cursor | `.cursor/rules/project.mdc` | `.cursor/rules/` | `output/cursorrules.md` |
| GitHub Copilot | `copilot-instructions.md` | `.github/` | `output/copilot.md` |
| OpenAI Codex CLI | `AGENTS.md` | project root | `output/codex.md` |
| Other / generic | `AI_CONTEXT.md` | project root | `output/generic.md` |

Interop: `AGENTS.md` (Codex) is also read by Claude Code as a fallback.
If the project uses both, generating `AGENTS.md` alone may be sufficient.

Load the corresponding file in `output/` and apply its structure and
formatting rules when rendering the final context file.