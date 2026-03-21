# Base — Documentation
[ID: base-docs]

## Single source of truth
- `README.md` is the single source of truth for project structure
- Do not duplicate structure in other documents — reference `README.md` instead
- No references to non-existent files, components, or services

## Standard documents

| File                  | Purpose                                      |
|-----------------------|----------------------------------------------|
| `README.md`           | Project overview, structure, setup, commands |
| `CLAUDE.md`           | AI agent context and project rules           |
| `docs/ONBOARDING.md`  | Onboarding guide for new contributors        |
| `docs/PLAYBOOK.md`    | Operational reference for common tasks       |

## Documentation rule
Before every commit, update all relevant documentation:
- **`CLAUDE.md`** — update if architecture, stack, design rules, or
  conventions change
- **`README.md`** — update if project structure, stack, or setup steps change
- **`docs/PLAYBOOK.md`** — update if commands, workflow, or release process
  change
- **`docs/ONBOARDING.md`** — update if the contributor workflow changes

## Output file by agent

| Agent              | Context file      |
|--------------------|-------------------|
| Claude / Claude Code | `CLAUDE.md`     |
| Cursor             | `.cursorrules`    |
| Generic / other    | `AI_CONTEXT.md`   |