# Output Format — AI_CONTEXT.md
[ID: output-generic]
[DEPENDS ON: formats/agent.md]

Used by: any agent not covered by a specific format (Copilot Workspace,
Gemini, custom agents, etc.)
Output filename: `AI_CONTEXT.md`
Write to: `generated/AI_CONTEXT.md` (inside this repo)
Place in: project root (copy from `generated/` to the target project)

---

## Structure

Use the inline or reference model from `formats/agent.md`. Prefer clarity and
completeness over brevity — generic agents have no assumed knowledge of the
project. Include all sections — do not omit even if sparse; mark as "N/A" if
empty.

Additionally include these sections if applicable:

```
## Quality attributes
[base/quality.md — relevant sections]

## Browser support
[Interview BROWSERS answers, if applicable]

## Third-party services
[Interview SERVICES answers, if applicable]
```

---

## Formatting rules

- Use ATX headings (`##` for sections, `###` for subsections)
- Include all sections — do not omit even if sparse; mark as "N/A" if empty
- See `formats/agent.md` for shared formatting rules

---

## Tone

- See `formats/agent.md` for shared tone
- Include brief rationale where a rule might otherwise be ignored by an
  unfamiliar agent (unlike CLAUDE.md, which assumes an opinionated agent)
