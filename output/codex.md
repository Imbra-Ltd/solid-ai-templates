# Output Format — OpenAI Codex CLI
[ID: output-codex]

Used by: OpenAI Codex CLI
Output filename: `AGENTS.md`
Place in: project root

Interop note: Claude Code reads `AGENTS.md` as a fallback when no `CLAUDE.md`
is present. If the project uses both Codex CLI and Claude Code, a single
`AGENTS.md` can serve both — no separate `CLAUDE.md` needed unless
Claude-specific rules are required.

---

## Structure

```
# [Project Name]

[One-sentence description from interview]
Owner: [owner from interview]

---

## Stack
[Stack template — Stack section]

## Project structure
[Stack template — structure section]

---

## Commands
[Stack template — Commands section]

---

## Code conventions
[Stack template — conventions sections]

## Git conventions
[base/git.md + any stack EXTEND/OVERRIDE]

## Testing
[Stack template — Testing section]

---

## Security
[base/quality.md — Security section]
```

---

## Formatting rules

- No required structure — Codex imposes no schema
- Full Markdown is supported; use headings, bullets, and fenced code blocks
- Include all sections relevant to the project — Codex benefits from complete context
- Keep lines under 80 characters where possible
- No HTML — plain Markdown only
- No frontmatter required

## What to include

- Exact commands for building, testing, linting, and running the project
- Code style and naming conventions
- Security constraints (never hardcode secrets, input validation rules)
- Git workflow conventions
- Project structure overview

## What to omit

- Secrets, API keys, credentials — never in this file
- UI/design/brand rules unless the project has a frontend
- Lengthy rationale — Codex reads this as task context, not documentation

---

## Monorepo support (optional)

Codex walks the directory tree from the project root to the current working
directory, reading `AGENTS.md` at each level. For monorepos, add package-level
`AGENTS.md` files with package-specific rules:

```
AGENTS.md              # root — shared conventions
packages/
  api/
    AGENTS.md          # API-specific rules (extends root)
  web/
    AGENTS.md          # frontend-specific rules (extends root)
```

Package-level files should only contain rules that differ from or extend the root.

---

## Tone

- Imperative and direct: "Use X", "Never do Y", "Always Z"
- Include brief rationale only where a rule requires context to be followed correctly