# Output Format — Shared Agent Structure
[ID: output-agent]

Shared structure for all agent output formats. Each format file
(`claude.md`, `codex.md`, etc.) references this file for the content
model and adds format-specific rules (filename, placement, tone,
frontmatter).

---

## Choosing a model

| | Inline | Reference |
|---|---|---|
| **Runtime** | Rules always in context — applied immediately | Agent must read template files first — may skip them |
| **Maintenance** | Rules drift from templates over time | Single source of truth across projects |
| **Best for** | Single project, reliable rule application | Multi-project consistency, shared conventions |

**Recommendation:** default to inline for reliable agent behaviour. Use
reference when maintaining conventions across multiple projects, and
consider a hybrid — inline the most critical project-specific rules,
reference the templates for the full quality framework.

---

## Inline model (default)

All rules are inlined — the output file is self-contained. Use numbered
headings for groups and subsections to enable cross-referencing between
documents (e.g. "see CLAUDE.md section 2.3").

Separate project rules (1–4) from agent instructions (5). Project rules
describe *what the rules are*. The review process describes *how to check
them*.

```
# [Project Name]

[One-sentence description from interview]
[IDENTITY answers: owner, repo URL, live URL if applicable]

## 1. Project
### 1.1 Stack
[Stack template — Stack section]
### 1.2 Project structure
[Stack template — architecture/structure sections]
### 1.3 Commands
[Stack template — Commands section]

## 2. Code conventions
### 2.1 Git
[base/git.md + any stack EXTEND/OVERRIDE]
### 2.2 [Language]
[Language-specific conventions from stack template]
### 2.3 [Additional code sections as needed]
[Components, styling, data rules — project-specific]

## 3. Quality
### 3.1 Testing
[Stack template — Testing section]
### 3.2 [Additional quality sections as needed]
[SEO, performance, accessibility — project-specific]

## 4. Identity
### 4.1 Design
[Interview DESIGN answers, if applicable]
### 4.2 Brand voice
[Interview BRAND answers, if applicable]

## 5. Review process
### 5.1 Code review
[base/review.md priority order + checklists to apply]
### 5.2 Structure audit
[Which templates to verify, when to run]
```

Omit sections that are not applicable to the project (e.g. omit section 4
for a backend service, omit 3.2+ if only testing applies).

---

## Reference model

Use when the project vendors solid-ai-templates as a submodule. The agent
file is leaner — it references the templates for base rules and only inlines
project-specific overrides. Same grouped structure and numbering as the
inline model.

```
# [Project Name]

[One-sentence description from interview]
[Link to architecture docs if applicable]

Quality conventions defined in `docs/solid-ai-templates/` (submodule).
Key references:
- [List the relevant base and layer templates for this stack]

Project-specific overrides and additions follow below.

## 1. Project
### 1.1 Stack
[Stack template — Stack section]
### 1.2 Project structure
[Planned or actual directory tree]
### 1.3 Commands
[Stack template — Commands section]

## 2. Code conventions
[PROJECT-SPECIFIC SECTIONS ONLY — e.g. Type design, Data rules,
Component conventions. Omit anything already covered by the
referenced templates.]

## 3. Quality
[PROJECT-SPECIFIC SECTIONS ONLY — e.g. SEO, Performance targets.
Omit anything already covered by the referenced templates.]

## 4. Identity
### 4.1 Design
[Interview DESIGN answers, if applicable]
### 4.2 Brand voice
[Interview BRAND answers, if applicable]

## 5. Review process
### 5.1 Code review
Follow base/review.md priority order, apply base/quality.md and
language-specific templates as the standard.
### 5.2 Structure audit
Verify MUSTs from base/docs.md, base/readme.md, base/git.md, and
relevant layer/stack templates. Run after: new project, migration,
new layer, or pre-release.
```

---

## Companion documents

Both models MUST also generate:
- `docs/ONBOARDING.md` — following the structure in `base/docs.md`
- `docs/PLAYBOOK.md` — following the structure in `base/docs.md`
- `docs/dev-journal.md` — following the structure in `base/docs.md`

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
