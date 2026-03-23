# Output Format — AI_CONTEXT.md
[ID: output-generic]

Used by: any agent not covered by a specific format (Copilot Workspace,
Gemini, custom agents, etc.)
Output filename: `AI_CONTEXT.md`
Write to: `generated/AI_CONTEXT.md` (inside this repo)
Place in: project root (copy from `generated/` to the target project)

---

## Structure

Render the composed content with full section coverage. Prefer clarity and
completeness over brevity — generic agents have no assumed knowledge of the
project.

```
# [Project Name]

[One-sentence description from interview]
Owner: [owner from interview]
Live URL / package: [URL or package name from interview]

---

## Stack
[Stack template — Stack section]

## Project structure
[Stack template — structure section]

## Architecture
[Stack template — architecture sections]

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

## Documentation standards
[base/docs.md]

## Quality attributes
[base/quality.md — relevant sections]

---

## Design
[Interview DESIGN answers, if applicable]

## Brand voice
[Interview BRAND answers, if applicable]

## Browser support
[Interview BROWSERS answers, if applicable]

## Third-party services
[Interview SERVICES answers, if applicable]
```

---

## Formatting rules

- Use ATX headings (`##` for sections, `###` for subsections)
- Use fenced code blocks with a language tag for all commands and code samples
- Use bullet lists for rules
- Include all sections — do not omit even if sparse; mark as "N/A" if empty
- No HTML — Markdown only
- Lines under 80 characters where possible

---

## Tone

- Imperative and direct: "Use X", "Never do Y", "Always Z"
- Include brief rationale where a rule might otherwise be ignored by an
  unfamiliar agent (unlike CLAUDE.md, which assumes an opinionated agent)