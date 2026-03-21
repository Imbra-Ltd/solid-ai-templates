# Base — Documentation
[ID: base-docs]

## Rule language
Use MUST / SHOULD / COULD to express the weight of every rule:

| Word | Meaning |
|------|---------|
| MUST | Absolute requirement — no exceptions without explicit rationale |
| MUST NOT | Absolute prohibition |
| SHOULD | Recommended — deviations require justification |
| SHOULD NOT | Not recommended — may be ignored with justification |
| COULD | Optional — developer decides without further discussion |

## Single source of truth
- `README.md` is the single source of truth for project structure
- Do not duplicate structure in other documents — reference `README.md` instead
- No references to non-existent files, components, or services

## Standard documents

| File | Purpose |
|------|---------|
| `README.md` | Project overview, structure, setup, commands |
| `CLAUDE.md` | AI agent context and project rules |
| `docs/ONBOARDING.md` | Onboarding guide for new contributors |
| `docs/PLAYBOOK.md` | Operational reference for common tasks |

## Documentation rule
Before every commit, update all relevant documentation:
- **`CLAUDE.md`** — update if architecture, stack, design rules, or conventions change
- **`README.md`** — update if project structure, stack, or setup steps change
- **`docs/PLAYBOOK.md`** — update if commands, workflow, or release process change
- **`docs/ONBOARDING.md`** — update if the contributor workflow changes

## Decision logs
- Significant architectural decisions MUST be recorded as Architecture Decision
  Records (ADR) in `docs/decisions/`
- Each ADR documents: context, decision, alternatives considered, consequences
- ADRs are immutable once merged — create a new ADR to supersede an old one

## Writing style
- Write in present tense — past or future tense indicates out-of-sync documentation
- Write as little as necessary but as much as needed — documentation that goes
  out of sync is worse than no documentation
- Remove redundant, inconsistent, or outdated documentation promptly
- Use full, grammatically correct sentences — enumerations are exempt

## Diagrams and assets
- Prefer text-based diagram formats: Mermaid for flowcharts, sequence diagrams,
  and Gantt charts; Draw.io for complex visual diagrams
- Commit all raw editable sources alongside rendered outputs
- Do not use proprietary formats (Word, Illustrator, Affinity Designer)
- Diagrams MUST be version-controlled — binary-only diagrams are not acceptable

## Docs-as-code
- Technical documentation lives in the repository alongside the code
- Documentation follows the same review process as code
- All documentation MUST be written in Markdown

## Output file by agent

| Agent | Context file |
|-------|-------------|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursor/rules/project.mdc` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| OpenAI Codex CLI | `AGENTS.md` |
| Generic / other | `AI_CONTEXT.md` |