# solid-ai-templates

Composable, SOLID-inspired template system for generating AI agent context
files (CLAUDE.md, AGENTS.md, .cursor/rules/project.mdc, etc.) for any
project type.

## Project identity

- **Name**: solid-ai-templates
- **Owner**: Imbra Ltd — Branimir Georgiev
- **Repo**: github.com/Imbra-Ltd/solid-ai-templates
- **Stack**: plain Markdown — no build step, no runtime dependencies
- **Output**: context files for Claude Code, Cursor, GitHub Copilot, Codex CLI

## Architecture

```
base/           # Cross-cutting rules — apply to every project
backend/        # Backend layer — HTTP, API, database, observability, etc.
frontend/       # Frontend layer — UX, accessibility, CSS, SSG
stack/          # Concrete stacks — extend base + layer templates
formats/         # Rendering rules per AI agent tool
examples/       # Complete generated context files (reference)
INTERVIEW.md    # Agent-driven project setup interview
SPEC.md         # System design, composition rules, precedence
ROADMAP.md      # Project status and planned work
manifest.yaml   # Machine-readable dependency graph
CONCEPTS.md     # Concept-to-file navigation index
```

### Template naming convention

Stack files follow a `<prefix>-<name>.md` pattern:

| Prefix | Examples |
|--------|---------|
| `python-` | python-flask, python-fastapi, python-django, python-grpc |
| `go-` | go-lib, go-service, go-echo, go-grpc |
| `java-` | java-spring-boot, java-grpc |
| `node-` | node-express, node-nestjs |
| `spa-` | spa-react, spa-vue, spa-svelte |
| `full-` | full-nextjs, full-sveltekit |
| `mobile-` | mobile-flutter, mobile-react-native |
| `static-site-` | static-site-astro, static-site-hugo |
| `iac-` | iac-terraform |

### Inheritance model

```
base/ → frontend/ or backend/ → stack/
```

- Every stack declares `[DEPENDS ON: ...]` at the top
- Sections are tagged `[ID: ...]`, extended with `[EXTEND: ...]`,
  replaced with `[OVERRIDE: ...]`
- `manifest.yaml` is the machine-readable dependency graph

## Commands

```bash
# No build step — all templates are plain Markdown
git clone https://github.com/Imbra-Ltd/solid-ai-templates.git

# To generate a context file for a project:
# 1. Open your agent
# 2. Attach INTERVIEW.md and the relevant stack template
# 3. Ask the agent to generate CLAUDE.md (or AGENTS.md, etc.)
```

## Git conventions

- Branch: `main` (protected) — never commit directly
- Branch naming: `feat/<scope>`, `fix/<scope>`, `docs/<scope>`, `chore/<scope>`
- Commits: `<type>(<scope>): <summary>` — types: feat, fix, chore, docs, refactor
- PRs are small and focused — one concern per PR; one approval required to merge
- After a PR is merged, delete branch and pull main before starting new work
- Do not commit `.idea/`, editor config, or any generated output

## Code conventions

### Adding a new stack template

1. Create `stack/<prefix>-<name>.md` following an existing file of the same category
2. Add `[DEPENDS ON: ...]` at the top — list every template this extends
3. Tag every section with `[ID: <name>]` or `[EXTEND: <id>]` / `[OVERRIDE: <id>]`
4. Register in `manifest.yaml` under `stacks:` with a `depends_on` list
5. Add to the stack list in `SPEC.md`
6. Add to the stacks table in `README.md`
7. Add to `ROADMAP.md` under the current phase
8. Add an example in `examples/<name>/CLAUDE.md` if the stack is concrete

### Adding a new base or layer template

1. Create `base/<name>.md`, `backend/<name>.md`, or `frontend/<name>.md`
2. Tag the file with `[ID: <layer>-<name>]`
3. Tag every section with a unique `[ID: ...]`
4. Register in `manifest.yaml` under the correct layer key
5. Update `SPEC.md` — add to the relevant directory listing
6. Reference from dependent stack templates via `[DEPENDS ON: ...]`

### Template authoring rules

- Sections use imperative, direct language: "Use X", "Never Y", "Always Z"
- No explanatory prose in rule lists — rules only
- Use `[ID: ...]` on every section that another template might EXTEND or OVERRIDE
- Optional sections are marked `(if applicable)` in the heading
- Keep line length under 80 characters
- No HTML — Markdown only

### manifest.yaml

- Every template file MUST have a corresponding entry in `manifest.yaml`
- IDs MUST be unique across all layers
- `depends_on` lists MUST reference valid IDs — no dangling references
- Stack entries go under `stacks:`, base under `base:`, layer under `backend:` or `frontend:`

## Testing

Two test runners live in `tests/`:

```bash
py tests/run_smoke.py              # 7 structural checks — no agent required
py tests/run_smoke.py SYS-01       # run one check by ID

py tests/run_e2e.py                # 30 agent-based tests via claude -p
py tests/run_e2e.py STK-01 FMT-01  # run specific tests
py tests/run_e2e.py --dry-run      # build prompts only, no agent call
```

Both runners write a timestamped Markdown report to `tests/reports/` after
every run. Reports are gitignored.

Spec files live in `tests/specs/`. See `tests/CODIFICATION.md` for the ID
scheme and `tests/INDEX.md` for the full list of specs.

- To validate a new template: run `py tests/run_smoke.py` and attach
  `INTERVIEW.md` + the new stack to an agent to confirm coherent output
- To validate a structural change: run `py tests/run_smoke.py` — it checks
  all `[DEPENDS ON: ...]`, `[EXTEND: ...]`, `[OVERRIDE: ...]`, and
  `manifest.yaml` references automatically

## Documentation

### Standard documents

| File | Purpose |
|------|---------|
| `README.md` | Public-facing overview, quick start, stacks table, agents table |
| `CLAUDE.md` | AI agent context and project rules (this file) |
| `SPEC.md` | System design, composition rules, inheritance model, precedence |
| `ROADMAP.md` | Project status and planned work — single source of truth for phase progress |
| `CONCEPTS.md` | Concept-to-file navigation index |
| `manifest.yaml` | Machine-readable dependency graph for all templates |
| `docs/ONBOARDING.md` | Onboarding guide for new contributors |
| `docs/PLAYBOOK.md` | Operational reference — how to add templates, run interviews, validate output |

### Documentation rules

- Before every commit, update all relevant documents:
  - `CLAUDE.md` — if architecture, naming conventions, or authoring rules change
  - `README.md` — if the stacks table, project structure, or quick start change
  - `SPEC.md` — if the composition model, inheritance rules, or ID system change
  - `ROADMAP.md` — if a template is added, removed, or renamed
  - `manifest.yaml` — if any template is added, removed, renamed, or re-depended
- Do not duplicate content across documents — cross-reference instead
- Write in present tense — past or future tense indicates out-of-sync documentation

### Decision logs

- Significant structural decisions (new layer, naming convention change, override
  model change) MUST be recorded as ADRs in `docs/decisions/`
- Each ADR documents: context, decision, alternatives considered, consequences
- ADRs are immutable once merged — create a new ADR to supersede an old one

### Rule language

All rules in templates use RFC 2119 keywords:

| Word | Meaning |
|------|---------|
| MUST | Absolute requirement |
| MUST NOT | Absolute prohibition |
| SHOULD | Recommended — deviations require justification |
| MAY | Optional |