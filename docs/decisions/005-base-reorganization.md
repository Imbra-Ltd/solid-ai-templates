# ADR-005: Reorganize base/ into subfolders

**Status:** Accepted
**Date:** 2026-05-04

## Context

`base/` contains 23 files covering concerns from git conventions to
360-degree analysis. A newcomer opening the folder sees a flat list
with no indication of which files matter or how they relate.

Usage analysis of the 23 files against all 29 stacks:

| Tier | Files | Stack usage |
|------|-------|-------------|
| Universal (all 29 stacks) | git, docs, quality | 3 |
| Language (11 stacks) | typescript | 1 |
| Single stack | testing, devsecops, cicd, issues, scope | 5 |
| Never resolved (extras only) | 14 remaining files | 0 |

14 of 23 files are never pulled in by any stack's dependency chain.
They exist as opt-in extras, but nothing in the folder structure
signals this.

### Cognitive load

Miller's law (7±2): humans can hold roughly 7 items in working
memory. A 23-item flat list exceeds this by 3x, forcing sequential
scanning instead of recognition. Subfolders that stay within the
7±2 range allow instant orientation.

## Decision

Split `base/` into 5 subfolders grouped by concern. The `base/`
parent directory is retained — no top-level explosion.

```
base/
  core/       # Foundation — applies to every project
  security/   # Application and pipeline security
  infra/      # CI/CD, containers, deployment, release
  workflow/   # Session protocol, issues, analysis, gates
  language/   # Language-specific and data concerns
```

### File mapping

#### core/ (6 files)

| File | Description |
|------|-------------|
| `git.md` | Committer identity, commits, branching, PR workflow |
| `docs.md` | Rule language, documentation standards, ADR |
| `quality.md` | Architecture, code style, testing |
| `testing.md` | Test pyramid, coverage, naming conventions |
| `readme.md` | README structure, badges, quick start |
| `review.md` | Peer review priority, checklists |

#### security/ (4 files, 2 after ADR-004 pattern move)

| File | Description |
|------|-------------|
| `security.md` | Application security rules |
| `security-patterns.md` | Application security patterns |
| `devsecops.md` | Pipeline security (SAST, SCA, SBOM) |
| `devsecops-patterns.md` | Pipeline security patterns |

#### infra/ (5 files, 3 after ADR-004 pattern move)

| File | Description |
|------|-------------|
| `cicd.md` | Pipeline stages, triggers, environments |
| `cicd-patterns.md` | Reusable CI/CD patterns |
| `containers.md` | Dockerfile, runtime security, Kubernetes |
| `deployment.md` | Deploy targets, certs, LB, registries |
| `release.md` | Semver, version bump, backward compat |

#### workflow/ (5 files)

| File | Description |
|------|-------------|
| `scope.md` | Scope guard, session protocol |
| `issues.md` | Issue templates (epic, task, bug, spike) |
| `quality-gates.md` | Three-layer gate model, thresholds |
| `ai-workflow.md` | AI-assisted development lifecycle |
| `360.md` | 360-degree project analysis |

#### language/ (2 files)

| File | Description |
|------|-------------|
| `typescript.md` | Type design, naming, strictness |
| `data-quality.md` | Data sourcing, completeness, scoring |

### Subfolder sizes

| Subfolder | Now | After ADR-004 |
|-----------|-----|---------------|
| core | 6 | 6 |
| security | 4 | 2 |
| infra | 5 | 3 |
| workflow | 5 | 5 |
| language | 2 | 2 |
| **Total** | **22** | **18** |

All subfolders stay within the 7±2 range.

### Impact on manifest.yaml

All `base-*` entries update their `file:` path:

```yaml
# Before
- id: base-git
  file: base/git.md

# After
- id: base-git
  file: base/core/git.md
```

IDs stay the same. Only `file:` fields change. The `depends_on`
lists reference IDs, not paths, so they need no changes.

### Impact on file headers

`[DEPENDS ON: ...]` headers in template files reference file paths.
These update to the new paths:

```markdown
# Before
[DEPENDS ON: base/quality.md]

# After
[DEPENDS ON: base/core/quality.md]
```

### Impact on agents

Agents resolve files from `manifest.yaml` using the `file:` field.
The resolution algorithm is unchanged — only the path strings differ.
Agents never browse folders directly.

## Alternatives considered

1. **Option A — Top-level split** (`core/`, `security/`, `infra/`
   as top-level folders). Rejected: explodes the top level from 12
   to 16+ directories. Moves the cognitive load problem up one level.

2. **Option B — core/ + extras/** (two-way split). Rejected:
   `extras/` is a junk drawer. "Everything else" provides no
   navigational signal. A reader still has to scan 17 files to find
   what they need.

3. **Keep flat, rely on naming** (prefix files like
   `security-*.md`). Rejected: prefixes help sorting but don't
   reduce the item count. 23 files is still 23 files.

4. **Nest under templates/** (Option A from spike discussion).
   Orthogonal to this decision — can be done independently later
   if the top level grows. Not needed now.

## Consequences

- `base/` goes from 23 items to 5 subfolders — within 7±2
- All manifest `file:` paths for base entries change (mechanical)
- All `[DEPENDS ON]` headers referencing base files change
  (mechanical)
- `SPEC.md` directory listing updates (generated by sync.py)
- `tools/sync.py` needs no logic changes — it reads manifest paths
- Smoke tests pass without changes — they validate manifest paths
  against filesystem
- If ADR-004 lands first, pattern files move to `docs/patterns/`
  before this reorganization, reducing the file count to 18
- If this lands first, ADR-004 moves patterns from their new
  subfolder paths — order doesn't matter
