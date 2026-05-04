# solid-ai-templates

Composable, SOLID-inspired template system for generating AI agent context
files (CLAUDE.md, AGENTS.md, .cursor/rules/project.mdc, etc.) for any
project type.

## 1. Project

### 1.1 Overview

- **Name**: solid-ai-templates
- **Owner**: Imbra Ltd — Branimir Georgiev
- **Repo**: github.com/braboj/solid-ai-templates
- **Stack**: plain Markdown — no build step, no runtime dependencies
- **Output**: context files for Claude Code, Cursor, GitHub Copilot,
  Codex CLI
- **Model**: inline — all rules are self-contained in this file

### 1.2 Architecture

```
templates/          # All template source files
  base/             # Cross-cutting rules (core, security, infra, workflow, language)
  backend/          # Backend layer — HTTP, API, database, observability
  frontend/         # Frontend layer — UX, accessibility, CSS, SSG
  platform/         # CI and security tool mappings per hosting platform
  stack/            # Concrete stacks — extend base + layer templates
  INTERVIEW.md      # Agent-driven project setup interview
  manifest.yaml     # Machine-readable dependency graph
docs/               # Onboarding, playbook, decision logs, SPEC.md
examples/           # Complete generated context files (reference)
tests/              # Smoke and e2e test runners, specs, reports
tools/              # sync.py — generates tables from manifest
```

### 1.3 Commands

```bash
# No build step — all templates are plain Markdown
git clone https://github.com/braboj/solid-ai-templates.git

# Sync generated sections after editing templates/manifest.yaml
py tools/sync.py            # update SPEC.md, README.md, INTERVIEW.md
py tools/sync.py --check    # exit 1 if any file is out of sync

# To generate a context file for a project:
# 1. Open your agent
# 2. Attach templates/INTERVIEW.md and the relevant stack template
# 3. Ask the agent to generate CLAUDE.md (or AGENTS.md, etc.)
```

## 2. Code conventions

### 2.1 Git

- Branch: `main` (protected) — never commit directly
- Branch naming: `feat/<scope>`, `fix/<scope>`, `docs/<scope>`,
  `chore/<scope>`
- Commits: `<type>(<scope>): <summary>` — types: feat, fix, chore,
  docs, refactor
- PRs are small and focused — one concern per PR; one approval
  required to merge
- After a PR is merged, delete branch and pull main before starting
  new work
- Do not commit `.idea/`, editor config, or any generated output

### 2.2 Issue labels

Every issue MUST have exactly one type label and one priority label.
Triage labels are terminal — applied when closing without action.

#### Type labels (pick one)

| Label | Color | When to use |
|-------|-------|-------------|
| `bug` | `#C9372C` | Defect in existing functionality |
| `epic` | `#9F8FEF` | Large initiative spanning multiple tasks |
| `task` | `#579DFF` | Atomic implementable work |
| `spike` | `#6CC3E0` | Research or exploration — output is a decision |
| `incident` | `#AE2E24` | Production outage or degradation affecting users now |

#### Priority labels (pick one)

| Label | Color | Meaning |
|-------|-------|---------|
| `P0` | `#E06C00` | Critical — blocks everything |
| `P1` | `#FCA700` | High — must fix before next milestone |
| `P2` | `#EED12B` | Medium — important but not blocking |
| `P3` | `#4BCE97` | Low — nice to have |
| `P4` | `#8590A2` | Backlog — someday |

#### Triage labels

| Label | Color | When to use |
|-------|-------|-------------|
| `duplicate` | `#C1C7D0` | Already tracked by another issue |
| `wontdo` | `#C1C7D0` | Acknowledged but will not be addressed |

### 2.3 Template naming convention

Stack files follow a `<prefix>-<name>.md` pattern:

| Prefix | Examples |
|--------|---------|
| `python-` | python-flask, python-fastapi, python-django, python-grpc, python-celery-worker |
| `go-` | go-lib, go-service, go-echo, go-grpc |
| `java-` | java-spring-boot, java-grpc |
| `node-` | node-express, node-nestjs |
| `nodejs-` | nodejs-lib |
| `spa-` | spa-react, spa-vue, spa-svelte |
| `full-` | full-nextjs, full-sveltekit |
| `mobile-` | mobile-flutter, mobile-react-native |
| `static-site-` | static-site-astro, static-site-hugo, static-site-tutorial |
| `iac-` | iac-terraform |
| `rust-` | rust-lib |
| `c-` | c-embedded |

Stacks without a variant use a bare name (e.g. `htmx.md`).

### 2.4 Inheritance model

```
base/ ──┬── frontend/ ──┐
        ├── backend/  ──┼── stack/
        └── platform/ ──┘
```

- Every stack declares `[DEPENDS ON: ...]` at the top
- Sections are tagged `[ID: ...]`, extended with `[EXTEND: ...]`,
  replaced with `[OVERRIDE: ...]`
- Platform templates are orthogonal to the stack chain — a project
  picks one platform regardless of stack
- `templates/manifest.yaml` is the machine-readable dependency graph

### 2.5 Adding a new stack template

1. Create `templates/stack/<prefix>-<name>.md` following an existing
   file of the same category
2. Add `[DEPENDS ON: ...]` at the top — list every template this
   extends
3. Tag every section with `[ID: <name>]` or `[EXTEND: <id>]` /
   `[OVERRIDE: <id>]`
4. Register in `templates/manifest.yaml` under `stacks:` with
   `depends_on`, `description`, `label`, and `layer` fields
5. Run `py tools/sync.py` — updates SPEC.md, README.md, INTERVIEW.md
6. Add an example in `examples/<name>/CLAUDE.md` if the stack is
   concrete

### 2.6 Adding a new base or layer template

1. Create the file in the correct directory:
   - `templates/base/core/` — foundation (git, docs, quality, etc.)
   - `templates/base/security/` — security rules
   - `templates/base/infra/` — CI/CD, containers, deployment
   - `templates/base/workflow/` — session protocol, issues, gates
   - `templates/base/language/` — language-specific rules
   - `templates/base/data/` — data modeling, quality, governance, migration
   - `templates/backend/` — backend services
   - `templates/frontend/` — frontend/UI projects
   - `templates/platform/` — CI platform mappings
2. Tag the file with `[ID: <layer>-<name>]`
3. Tag every section with a unique `[ID: ...]`
4. Register in `templates/manifest.yaml` under the correct layer
   key with a `description` field
5. Run `py tools/sync.py` — updates SPEC.md directory listings
6. Reference from dependent stack templates via `[DEPENDS ON: ...]`

### 2.7 Template authoring rules

- Sections use imperative, direct language: "Use X", "Never Y",
  "Always Z"
- No explanatory prose in rule lists — rules only
- Use `[ID: ...]` on every section that another template might
  EXTEND or OVERRIDE
- Optional sections are marked `(if applicable)` in the heading
- Keep line length under 80 characters
- No HTML — Markdown only

### 2.8 manifest.yaml

- Every template file MUST have a corresponding entry in
  `templates/manifest.yaml`
- IDs MUST be unique across all layers
- `depends_on` lists MUST reference valid IDs — no dangling
  references
- Stack entries go under `stacks:`, base under `base:`, layer under
  `backend:`, `frontend:`, or `platform:`

### 2.9 Documentation

#### Standard documents

| File | Purpose |
|------|---------|
| `README.md` | Public-facing overview, quick start, stacks table, agents table |
| `CLAUDE.md` | AI agent context and project rules (this file) |
| `docs/SPEC.md` | System design, composition rules, inheritance model, precedence |
| `templates/manifest.yaml` | Machine-readable dependency graph for all templates (single source of truth for descriptions, labels, layers) |
| `docs/ONBOARDING.md` | Onboarding guide for new contributors |
| `docs/PLAYBOOK.md` | Operational reference — how to add templates, run interviews, validate output |

#### Documentation rules

- Before every PR, update all relevant documents:
  - `CLAUDE.md` — if architecture, naming conventions, or authoring
    rules change
  - `README.md` — if the stacks table, project structure, or quick
    start change
  - `docs/SPEC.md` — if the composition model, inheritance rules,
    or ID system change
  - `templates/manifest.yaml` — if any template is added, removed,
    renamed, or re-depended
  - `docs/PLAYBOOK.md` — if the workflow for generating or
    validating changes
  - `docs/ONBOARDING.md` — if prerequisites or first steps change
- Do not duplicate content across documents — cross-reference
  instead
- Write in present tense — past or future tense indicates
  out-of-sync documentation

#### Decision logs

- Significant structural decisions (new layer, naming convention
  change, override model change) MUST be recorded as ADRs in
  `docs/decisions/`
- Each ADR documents: context, decision, alternatives considered,
  consequences
- ADRs are immutable once merged — create a new ADR to supersede
  an old one

#### Rule language

All rules in templates use RFC 2119 keywords:

| Word | Meaning |
|------|---------|
| MUST | Absolute requirement |
| MUST NOT | Absolute prohibition |
| SHOULD | Recommended — deviations require justification |
| MAY | Optional |

## 3. Quality

### 3.1 Testing

Four files in `tests/`:

| File | Purpose |
|------|---------|
| `tests/lib.py` | Shared utilities (constants, file reading, report writing, arg parsing) |
| `tests/cases.py` | E2E test case definitions, grouped by area (STK, FMT, ITV, DPL) |
| `tests/run_smoke.py` | Smoke test runner (structural checks) |
| `tests/run_e2e.py` | E2E test runner (agent-based tests) |

```bash
py tests/run_smoke.py              # structural checks
py tests/run_smoke.py SYS-01       # run one check by ID

py tests/run_e2e.py                # agent-based tests (live, needs API key)
py tests/run_e2e.py --offline      # validate test infrastructure without API
py tests/run_e2e.py --area=STK     # run all stack tests
py tests/run_e2e.py STK-01 FMT-01  # run specific tests by ID
py tests/run_e2e.py --fail-fast    # stop on first failure
py tests/run_e2e.py --dry-run      # print prompts, skip execution
```

- Both runners write a timestamped Markdown report to
  `tests/reports/` after every run (gitignored)
- Spec files live in `tests/specs/` — see `tests/CODIFICATION.md`
  for the ID scheme and `tests/INDEX.md` for the full list
- CI runs smoke + gitleaks + e2e offline on PRs (and on push
  to main)
- Live e2e mode (without `--offline`) calls Claude via the API —
  run manually on the dev machine for functional validation
- To validate a new template: run `py tests/run_smoke.py` and
  attach `templates/INTERVIEW.md` + the new stack to an agent to
  confirm coherent output

## 4. Identity

Not applicable — this project has no design system or brand voice.

## 5. Review process

### 5.1 Code review

Priority order (highest first):
1. **Correctness** — do `[DEPENDS ON]`, `[EXTEND]`, `[OVERRIDE]`
   references resolve? Does the manifest entry match?
2. **Completeness** — are all required documents updated (see 2.9)?
3. **Clarity** — are rules imperative and unambiguous?
4. **Conventions** — does the template follow authoring rules
   (see 2.7)?

### 5.2 Structure audit

Run `py tests/run_smoke.py` before every PR. It checks:
- All `[DEPENDS ON: ...]` reference existing files
- All `[EXTEND: ...]` and `[OVERRIDE: ...]` reference valid IDs
- All manifest entries point to existing files
- All template files have a manifest entry
- No duplicate IDs across layers

## 6. Session protocol

### 6.1 Startup

1. Read `CLAUDE.md` (this file) and `docs/SPEC.md`
2. Check for stale branches: run `git branch --no-merged main`
   and flag any unmerged branches to the user — they may contain
   lost work
3. Confirm the scope with the user before making changes
4. If the task is ambiguous, ask: "What is the specific deliverable
   for this session?"

### 6.2 During the session

- Run `py tests/run_smoke.py` after any template or manifest change
- If a change affects multiple documents, update all in the same PR
- Do not drift from the agreed scope without checking with the user

### 6.3 End of session

Before ending a session, verify:

1. **Dev journal** — add a session entry to `docs/dev-journal.md`
2. **Smoke tests** — run `py tests/run_smoke.py` and confirm all
   checks pass
3. **CLAUDE.md** — update if architecture, naming, or authoring
   rules changed
4. **README.md** — update if the stacks table, structure, or quick
   start changed
5. **docs/SPEC.md** — update if composition model or ID system
   changed
6. **templates/manifest.yaml** — update if any template was added,
   removed, or re-depended
7. **Branch cleanup** — delete local branches that have been merged
   via PR: `git branch --merged main | grep -v main | xargs git
   branch -d`
