# Output Format — Cursor
[ID: output-cursor]

Used by: Cursor IDE
Output filename: `.cursor/rules/project.mdc`
Place in: `.cursor/rules/` (project root)

Note: `.cursorrules` (flat file, project root) is the legacy format and is
deprecated. New projects should use `.mdc` files in `.cursor/rules/`.

---

## File format

Each `.mdc` file requires a YAML frontmatter block followed by Markdown content.

```
---
description: [one-line summary of what these rules cover]
alwaysApply: true
---

[rules content]
```

### Frontmatter fields

| Field | Values | Effect |
|-------|--------|--------|
| `alwaysApply` | `true` / `false` | If true, injected into every Cursor session |
| `description` | string | Shown in the rules list; used for AI relevance matching |
| `globs` | `"src/**/*.ts"` | Apply only when matching files are open (omit if `alwaysApply: true`) |

For a general project context file, use `alwaysApply: true` and omit `globs`.
For stack- or path-specific rules, set `alwaysApply: false` and define `globs`.

---

## Structure

```
---
description: Project rules for [Project Name]
alwaysApply: true
---

## Stack
[Stack template — Stack section, condensed]

## Project structure
[Stack template — structure section, condensed]

## Code conventions
[Stack template — conventions sections]

## Git conventions
[base/git.md + any stack EXTEND/OVERRIDE, condensed]

## Testing
[Stack template — Testing section]

## Commands
[Stack template — Commands section]
```

---

## Formatting rules

- Keep content short — Cursor injects it into every prompt when `alwaysApply: true`
- Short, direct bullet points — no prose paragraphs
- Remove rationale and background — rules only
- No nested lists beyond one level
- No HTML — plain Markdown only
- Omit sections with no applicable rules
- Target total file length: under 150 lines

---

## Splitting rules (optional)

For large projects, split into multiple `.mdc` files by concern:

```
.cursor/rules/
  project.mdc       # alwaysApply: true — identity, stack, commands
  conventions.mdc   # alwaysApply: true — code and git conventions
  tests.mdc         # globs: "tests/**" — testing rules only
```

---

## Tone

- Terse and imperative: "Use X", "No Y", "Always Z"
- No "you should" or "please" — direct commands only