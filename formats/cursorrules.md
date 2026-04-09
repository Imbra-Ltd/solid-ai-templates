# Output Format — Cursor
[ID: output-cursor]
[DEPENDS ON: formats/agent.md]

Used by: Cursor IDE
Output filename: `project.mdc`
Write to: `generated/project.mdc` (inside this repo)
Place in: `.cursor/rules/` (copy from `generated/` to the target project)

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

Use the inline or reference model from `formats/agent.md`. Wrap the content
in the `.mdc` frontmatter block shown above.

---

## Formatting rules

- Keep content short — Cursor injects it into every prompt when `alwaysApply: true`
- Short, direct bullet points — no prose paragraphs
- Remove rationale and background — rules only
- No nested lists beyond one level
- Omit sections with no applicable rules
- Target total file length: under 150 lines
- See `formats/agent.md` for shared formatting rules

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
