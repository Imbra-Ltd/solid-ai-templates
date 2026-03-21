# Output Format — GitHub Copilot
[ID: output-copilot]

Used by: GitHub Copilot Chat (VS Code, JetBrains, GitHub.com)
Output filename: `copilot-instructions.md`
Place in: `.github/` (project root)

---

## Structure

```
# [Project Name]

[One-sentence description from interview]

## Stack
[Stack template — Stack section, condensed]

## Code conventions
[Stack template — conventions sections, condensed]

## Git conventions
[base/git.md + any stack EXTEND/OVERRIDE, condensed]

## Testing
[Stack template — Testing section, condensed]

## Commands
[Stack template — Commands section]
```

---

## Formatting rules

- Natural language is acceptable — Copilot handles prose well
- Whitespace and blank lines are ignored by Copilot; use them freely for readability
- Bullet lists preferred for rules; short prose acceptable for context
- No HTML — plain Markdown only
- No frontmatter required
- Omit sections that have no rules applicable to this project
- Keep the file concise — Copilot adds it to every Chat session

---

## What to include

- Project purpose and stack (Copilot has no other project context by default)
- Code style rules that differ from language defaults
- Testing approach and required commands
- Git conventions (commit style, branch naming)
- Any terms, names, or patterns to avoid

## What to omit

- Secrets, API keys, credentials — never in this file
- Information derivable from the code (e.g. listing every file)
- UI/UX or brand rules — Copilot is a coding assistant, not a design tool
- Lengthy rationale — state the rule, not the history behind it

---

## Path-specific instructions (optional)

For rules that apply only to specific parts of the codebase, create additional
files with an `applyTo` frontmatter field:

```
# .github/[concern].instructions.md
---
applyTo: "src/api/**"
---
[API-specific rules]
```

---

## Tone

- Direct and instructional: "Use X", "Always Y", "Never Z"
- Short sentences — one rule per bullet point