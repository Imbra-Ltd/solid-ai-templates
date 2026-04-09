# Output Format — Shared Agent Structure
[ID: output-agent]

Shared structure for all agent output formats. Each format file
(`claude.md`, `codex.md`, etc.) references this file for the content
model and adds format-specific rules (filename, placement, tone,
frontmatter).

---

## Inline model (default)

All rules are inlined — the output file is self-contained. Render the
composed content in this order:

```
# [Project Name]

[One-sentence description from interview]

## Project identity
[IDENTITY answers: owner, repo URL, live URL if applicable]

## Stack
[Stack template — Stack section]

## Project structure
[Stack template — architecture/structure sections]

## Commands
[Stack template — Commands section]

## Git conventions
[base/git.md + any stack EXTEND/OVERRIDE]

## Code conventions
[Stack template — conventions sections]

## Testing
[Stack template — Testing section]

## Documentation
[base/docs.md]

## Design
[Interview DESIGN answers, if applicable]

## Brand voice
[Interview BRAND answers, if applicable]
```

Omit sections that are not applicable to the project (e.g. omit Design
and Brand for a backend service).

---

## Reference model

Use when the project vendors solid-ai-templates as a submodule. The agent
file is leaner — it references the templates for base rules and only inlines
project-specific overrides.

```
# [Project Name]

[One-sentence description from interview]

[Link to architecture docs if applicable]

Quality conventions defined in `docs/solid-ai-templates/` (submodule).
Key references:
- [List the relevant base and layer templates for this stack]

Before quality work, read the relevant templates above. Two scopes:
- **Code review**: follow base/review.md priority order, apply
  base/quality.md and language-specific templates as the standard.
- **Structure audit**: verify MUSTs from base/docs.md, base/readme.md,
  base/git.md, and relevant layer/stack templates. Run after: new project,
  migration, new layer, or pre-release.

Project-specific overrides and additions follow below.

## Stack
[Stack template — Stack section]

## Project structure
[Planned or actual directory tree]

## Commands
[Stack template — Commands section]

[PROJECT-SPECIFIC SECTIONS ONLY — e.g. Type design, Data rules,
Component conventions, SEO, Performance. Omit anything already
covered by the referenced templates.]

## Design
[Interview DESIGN answers, if applicable]

## Brand voice
[Interview BRAND answers, if applicable]
```

---

## Companion documents

Both models MUST also generate:
- `docs/ONBOARDING.md` — following the structure in `base/docs.md`
- `docs/PLAYBOOK.md` — following the structure in `base/docs.md`

---

## Shared formatting rules

- Use fenced code blocks with a language tag for all commands and code samples
- Use bullet lists for rules; avoid prose paragraphs inside rule sections
- Keep lines under 80 characters where possible
- No HTML — Markdown only

---

## Shared tone

- Imperative and direct: "Use X", "Never do Y", "Always Z"
- No explanatory prose unless a rule needs context to be followed correctly
- Rules are instructions to the agent, not documentation for humans
