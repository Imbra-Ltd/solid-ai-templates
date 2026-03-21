# Output Format — CLAUDE.md
[ID: output-claude]

Used by: Claude / Claude Code
Output filename: `CLAUDE.md`
Place in: project root

---

## Structure

Render the composed content in this order:

```
# [Project Name]

[One-sentence description from interview]

---

## Project identity
[IDENTITY answers]

---

## Stack
[Stack template — Stack section]

## Architecture
[Stack template — architecture/structure sections]

---

## Commands
[Stack template — Commands section]

---

## Git conventions
[base/git.md + any stack EXTEND/OVERRIDE]

---

## Code conventions
[Stack template — conventions sections]

---

## Testing
[Stack template — Testing section]

---

## Documentation
[base/docs.md]

---

## Design
[Interview DESIGN answers, if applicable]

## Brand voice
[Interview BRAND answers, if applicable]
```

---

## Formatting rules

- Use ATX headings (`##` for sections, `###` for subsections)
- Use fenced code blocks with a language tag for all commands and code samples
- Use bullet lists for rules; avoid prose paragraphs inside rule sections
- Keep lines under 80 characters where possible
- No HTML — Markdown only
- Omit sections that are not applicable to the project (e.g. omit Design
  and Brand for a backend service)

---

## Tone

- Imperative and direct: "Use X", "Never do Y", "Always Z"
- No explanatory prose unless a rule needs context to be followed correctly
- Rules are instructions to the agent, not documentation for humans