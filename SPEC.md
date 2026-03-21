# Template System Specification

## Goal

A composable, inheritance-based template system that any LLM agent can use
to generate a project context file (`CLAUDE.md`, `PROJECT.md`, `AI_CONTEXT.md`,
or equivalent) for any type of project — from a static portfolio to a Python
SDK to a React SPA.

Designed to be agent-agnostic: works with Claude, Cursor, Copilot Workspace,
Gemini, or any agent that accepts a Markdown context file. Claude-specific
conventions (e.g. `CLAUDE.md` naming) are configurable, not hardcoded.

Inspired by SOLID principles: each template has a single responsibility,
is open for extension, and can be composed without modification.

---

## Core concepts

### 1. Base templates (abstract)

Reusable building blocks covering one concern each. Framework-agnostic.
Never used directly — always composed into a profile.

```
templates/base/
├── git.md         # Conventional commits, branching, PR workflow, versioning
├── ux.md          # UX principles, WCAG 2.1 AA, browser support
├── docs.md        # Documentation rule, README, PLAYBOOK, ONBOARDING
└── quality.md     # CSS conventions, performance, SEO, architecture rules
```

### 2. Stack templates (concrete, extend base)

Technology-specific rules that extend one or more base templates.
Cover the stack, component model, and tooling for a specific framework.

```
templates/stack/
├── static-site.md    # extends base — generic static site concepts
├── astro.md          # extends static-site — Astro islands, client directives
├── react-spa.md      # extends base — React-specific rules
└── python-lib.md     # extends base — Python packaging, testing, typing
```

### 3. Interview template (orchestrator)

A single file Claude uses to ask the user the REQUIRED questions before
generating `CLAUDE.md`. Questions are grouped by concern and reference
the relevant base/stack templates.

```
templates/interview.md
```

### 4. Profile (output)

The generated context file for a specific project. The output filename
depends on the target agent:

| Agent             | Output file       |
|-------------------|-------------------|
| Claude / Claude Code | `CLAUDE.md`    |
| Cursor            | `.cursorrules`    |
| Generic / other   | `AI_CONTEXT.md`   |

Produced by the agent by combining interview answers + selected base
templates + selected stack template.

---

## Inheritance model

```
base/git.md ─────────────────────────────┐
base/ux.md ──────────────────────────────┤
base/docs.md ────────────────────────────┤──► stack/static-site.md
base/quality.md ─────────────────────────┘         │
                                                    ▼
                                         stack/astro.md
                                                    │
                                         + interview answers
                                                    │
                                                    ▼
                                              CLAUDE.md
```

Rules:
- A stack template MUST reference which base templates it depends on
- A stack template MAY override a base rule — overrides must be explicit
- A stack template MAY add new rules not present in the base
- Claude assembles the final `CLAUDE.md` by merging base + stack +
  interview answers, with stack overrides taking precedence

---

## Override mechanism

Each base template section is tagged with a unique ID:

```markdown
## Git conventions [ID: git-conventions]
...
```

A stack template overrides a section by referencing its ID:

```markdown
## Git conventions [OVERRIDE: git-conventions]
- Always test with `npm run dev` before committing  ← replaces base rule
```

A stack template extends a section by referencing its ID:

```markdown
## Git conventions [EXTEND: git-conventions]
- Do not commit `dist/` or `node_modules/`  ← added on top of base rules
```

If no override or extend is declared, the base section is used as-is.

---

## Interview template structure

The interview template groups questions by concern:

```
[IDENTITY]     Project name, owner, URL, deployment target
[STACK]        Framework, JS interactivity, CSS approach, content format
[DESIGN]       Aesthetic, colours, typography
[BRAND]        Tagline, tone, copy rules
[CONTENT]      Sections, data files, pages
[SERVICES]     Analytics, forms, third-party integrations
[BROWSERS]     Supported browsers and versions
[OVERRIDES]    Any base rules the user wants to change
```

Claude asks all REQUIRED questions before generating anything.
DEFAULTED sections are pre-filled from the selected base + stack templates.

---

## How an agent uses the system

1. User provides a stack template (e.g. `templates/stack/astro.md`)
2. Agent reads the stack template, identifies its base dependencies
3. Agent loads the referenced base templates
4. Agent runs the interview (REQUIRED questions only)
5. Agent merges: base defaults + stack overrides + interview answers
6. Agent outputs a complete context file (`CLAUDE.md`, `.cursorrules`, etc.)

The interview instructions use neutral language ("ask the user") so any
agent can follow them without Claude-specific interpretation.

---

## File naming conventions

```
base/[concern].md               # single responsibility
stack/[framework].md            # concrete, extends one or more base templates
stack/[framework]-[variant].md  # variant of a framework (e.g. astro-ssr.md)
interview.md                    # orchestrator — always one file
SPEC.md                         # this file
```

---

## Roadmap

### Phase 1 — Foundation (current)
- [ ] Write `base/git.md`
- [ ] Write `base/ux.md`
- [ ] Write `base/docs.md`
- [ ] Write `base/quality.md`
- [ ] Write `stack/static-site.md`
- [ ] Write `stack/astro.md`
- [ ] Write `interview.md`
- [ ] Delete `static-site.md` and `static-site-astro.md` (superseded)

### Phase 2 — Expansion
- [ ] `stack/python-lib.md`
- [ ] `stack/react-spa.md`
- [ ] `stack/fastapi.md`

### Phase 3 — Agent coverage
- [ ] Test with Cursor (`.cursorrules` output)
- [ ] Test with a generic agent (`AI_CONTEXT.md` output)
- [ ] Document agent-specific quirks and workarounds

### Phase 4 — Validation
- [ ] Use the system on a new project end-to-end
- [ ] Refine based on gaps found during real use