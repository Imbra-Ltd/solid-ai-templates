# Dev Journal

## 2026-05-04 — Composition model, folder restructuring, roadmap removal

**Tool:** Claude Code (Opus 4.6, 1M context)

**PRs:** #157, #158, #159, #160, #161

**Issues closed:** #153, #154, #155

**Key changes:**
- Removed `ROADMAP.md` — planned work tracked via GitHub milestones
- Added consumption model section to SPEC.md (declaration block,
  resolution algorithm, lifecycle diagram, two worked examples)
- ADR-005: apply Miller's law (7±2) to repo structure
- Implemented composition model from ADR-004: trimmed quality-gates
  deps, added `core:` tier to manifest, moved 5 pattern files to
  `docs/patterns/`, fixed 3 stale file headers, added explicit
  cicd+devsecops to 13 backend stacks
- Implemented ADR-005 folder restructuring: created `templates/`
  parent (root 12→6 dirs), split `base/` into 5 subfolders
  (core, security, infra, workflow, language), moved SPEC.md to
  `docs/`, moved INTERVIEW.md and manifest.yaml to `templates/`
- Removed `generated/` directory from tracking
- Fixed remote URL (Imbra-Ltd → braboj)
- Enabled auto-merge on repo
- Triaged 6 unlabeled issues with priority labels

**Key decisions:**
- ROADMAP.md replaced by GitHub milestones (no closed milestones
  for completed phases — dev journal covers history)
- Miller's law as organizing principle for folder structure
- SPEC.md belongs in docs/ (documentation, not template source)
- INTERVIEW.md and manifest.yaml belong in templates/ (part of
  the template system)
- Pattern files are human reference docs, not agent context

---

## 2026-05-04 — Pattern templates and quick wins batch

**Tool:** Claude Code (Opus 4.6, 1M context)

**PRs:** #141, #142, #143, #144, #145, #148

**Issues closed:** #117, #104, #131, #135, #136, #137, #132, #130,
#133, #140, #139, #138

**Issues created:** #146, #147, #149, #150, #151

**Key changes:**
- New `base/cicd-patterns.md` — 8 reusable CI/CD patterns (gate job,
  path filtering, fan-out, artifact promotion, caching, matrix,
  auto-merge, deploy preview)
- New `base/testing-patterns.md` — 8 test patterns (factory, AAA,
  builder, parameterized, fixtures, mock boundary, snapshot, contract)
- New `frontend/patterns.md` — 8 UI patterns (error boundary, skeleton,
  optimistic update, virtual scroll, debounced search, form validation,
  responsive switch, URL state sync)
- New `base/security.md` — application security rules (12 sections:
  input, output, injection, auth, sessions, secrets, TLS, headers,
  errors, logging, CORS, uploads)
- New `base/security-patterns.md` — 8 app security patterns (slim,
  structural only)
- Rewrote `base/devsecops-patterns.md` — 8 pipeline security patterns
  (break-build gate, triage, SBOM, secret rotation, dep updates,
  security smoke, pre-merge gate, hardening loop)
- Expanded grading scale in `base/360.md` to include +/- modifiers
- Added audit tracking section to `base/360.md`
- Added remediation references section to `base/360.md`
- Batch quick wins: focus-visible, Dependabot, lychee root-dir,
  3 review checks, post-mortems, test factory defaults, sonarjs,
  boolean sort, explicit audit steps, ONBOARDING verify check

**Key decisions:**
- Pattern files are separate from rules files (rules say what,
  patterns say how) — different purposes, different audiences
- Security split: `security.md` (app rules) vs `devsecops.md`
  (pipeline rules), each with its own patterns companion
- Architecture spikes created for composition-over-inheritance
  (#151), pattern resolution (#149), agent-side resolution (#150)

---

## 2026-05-01 — Convention hardening sweep

**Tool:** Claude Code (Opus 4.6, 1M context)

**PRs:** #120, #121, #122, #123, #124

**Issues closed:** #105, #106, #107, #108, #109, #110, #111, #112,
#113, #114, #115, #116, #118, #119

**Key changes:**
- Session protocol: mandatory startup block, startup hygiene (branch/
  status/issues), build-after-change, visible sequential audit execution
- formats/agents.md: all 3 models reference base/scope.md (no more
  incomplete inlined checklists)
- Quality: DRY/KISS/YAGNI core principles, Fail Fast/Law of Demeter/
  High Cohesion in maintainability, duplication erosion audit check
- Astro: View Transitions section with ClientRouter recommendation and
  DOMContentLoaded warning
- Docs: version bump in release process, session naming convention,
  milestone sync rule
- Added hybrid-mode example (examples/hybrid-astro/CLAUDE.md)
- Clarified extraction threshold: substantial logic blocks vs short
  inline repetition

**Also:** fixed 3 issue titles (removed commit-style prefixes), added
missing priority labels to #104, #105, #106

---

## 2026-05-01 — Session protocol hardening (superseded)

**Tool:** Claude Code (Opus 4.6, 1M context)

**PRs:** #120

**Issues closed:** #105, #106, #107, #110, #119

**Key changes:**
- Hardened `base/scope.md` session startup with branch check, git
  status, issue review, and mandatory startup block requirement
- Added build-after-change rule to during-work section
- End-of-session audit now requires visible sequential execution with
  documented trigger phrases
- `formats/agents.md` — all three models (inline, reference, hybrid)
  now reference `base/scope.md` instead of inlining an incomplete
  6-step checklist
- Added `examples/hybrid-astro/CLAUDE.md` — first reference/hybrid
  mode example demonstrating the startup block pattern

**Key decisions:**
- Startup block is only required for reference/hybrid modes — inline
  models are self-contained and exempt
- Examples use anonymized fictional projects to avoid maintenance burden

---

## 2026-04-30 — v1.0.0 release, repo transfer, CI hardening

**Tool:** Claude Code (Opus 4.6, 1M context)

**Key changes:**
- Tagged v1.0.0 release
- Transferred repo from Imbra-Ltd to braboj
- Added `base/quality.md` rule: never hardcode derived counts
- Added audit decomposition guidance to `base/review.md`
- Added SEO conventions to `frontend/static-site.md` and
  `stack/static-site-astro.md` (sitemap, description, JSON-LD)
- Fixed stale references in SPEC.md, ROADMAP.md, ONBOARDING.md,
  PLAYBOOK.md (CONCEPTS.md, format files, section ordering)
- Fixed e2e crash bug (3-tuple return on skipped tests)
- Added `base/360.md` to manifest.yaml
- Fixed test spec frontmatter ID mismatch
- Added `--offline` mode to e2e runner — validates test
  infrastructure without API calls
- Refactored test runners: extracted `tests/lib.py` (shared
  utilities) and `tests/cases.py` (30 test cases grouped by area)
- Added `--area` and `--fail-fast` flags to e2e runner
- CI hardened: enforce_admins, require PR before merge, gitleaks
  in smoke workflow, push protection enabled, e2e switched to
  offline mode in CI
- Updated label colors: task `#579DFF`, epic `#9F8FEF`
- Added 8 GitHub topics for discoverability
- Updated all in-repo URLs and submodule pointers after transfer

**PRs merged:** #80, #81, #91, #92, #93, #94, #95, #96, #97, #98, #99

**Issues closed:** #79, #78, #55, #15, #16, #82, #83, #84, #85,
#86, #87, #88, #89, #69, #72, #10

**Issues created:** #82–#90, #100

**Issues remaining (3):**
- #90 task P2 — Write launch post and submit to awesome lists
- #100 task P2 — Replace claude CLI with Anthropic SDK in e2e runner
- #13 task P3 — Regenerate examples

**Decisions:**
- Repo transferred to braboj for better OSS discoverability
- E2E CI runs offline mode — live mode is manual/nightly only
- gitleaks CLI preferred over gitleaks-action (no license key needed)
- Label colors updated for accessibility (task, epic were too dark)
- pytest adoption deferred — hand-rolled runners are sufficient

## 2026-04-28 — 360 analysis, labels, ADRs, license

**Tool:** Claude Code (Opus 4.6, 1M context)

**Key changes:**
- Created `base/360.md` — four-category project assessment template
  (Value, Quality, Viability, Discovery) with role prompts and parallel
  subagent execution model (19 sub-dimensions, 78 checklist items)
- Standardized issue labels to 12 canonical labels with Atlassian-style
  colors across 11 repos (10 Imbra-Ltd + braboj/tutorial-git)
- Split `base/issues.md` (platform-agnostic types) from
  `platform/github.md` (GitHub label implementation)
- Updated `base/readme.md` — capability list requirement, dual-audience
  clarification
- Created `docs/decisions/` with 3 ADRs: inheritance model, label
  standardization, 360 analysis
- Added CC BY 4.0 license (LICENSE file + README update)
- Documented bus factor mitigation in ONBOARDING.md
- Improved README: capability list, project structure, dev setup, links

**PRs merged:** #73, #74, #75, #76

**Issues closed:** #58 (duplicate), #66, #67, #68, #70, #71, #18

**Issues remaining (7):**
- #69 task P1 — Add offline E2E test mode
- #55 task P2 — Add SEO conventions
- #16 task P2 — Review e2e test pipeline
- #15 task P2 — Review smoke test pipeline
- #72 task P3 — Tag v1.0.0 release
- #13 task P3 — Regenerate examples
- #10 task P4 — Refactor test runners

**Decisions:**
- ADR-001: Three-layer inheritance model (base → layer → stack)
- ADR-002: 12 canonical labels, Atlassian colors, type/priority split
- ADR-003: 360-degree analysis as parallel subagent evaluation
- License: CC BY 4.0 — maximizes adoption funnel, requires attribution
- Labels split: types in base/ (platform-agnostic), colors in platform/
  (GitHub-specific)
- Severity stays in bug body text, not as label — solo project, priority
  drives triage order

## 2026-04-27 — Skills roadmap

- Added Phase 15 (Skills) to `ROADMAP.md` with four categories:
  generative, transformation, review, ops — plus infrastructure tasks
- Renamed existing Phase 15 (Validation) to Phase 16
- Key insight: skills (dynamic, on-demand actions) complement static
  context files (CLAUDE.md/AGENTS.md) — they don't replace them

## 2026-05-04 — Composition over inheritance

Issues closed: #151, #149, #150
Issues created: #154 (implementation), #155 (repo org spike)

Three architecture spikes resolved in a single session. All decisions
recorded in ADR-004.

**#151 — Composition over inheritance (P1):**
- quality-gates.md depends on devsecops + cicd but never references
  their content — ISP violation. Remove both from depends_on.
- Core tier (5 files: quality, git, docs, readme, testing) always loaded.
  Manifest gets a top-level `core:` list.
- Stacks compose opt-in tiers explicitly — no transitive surprises.
- Stack classification: deployed services need devsecops + cicd; static
  sites, libraries, and mobile do not.
- Platform templates are facades — platform-github does not depend on
  devsecops.
- File headers must match manifest (direct deps only). 3 stale headers
  found: astro, hugo, tutorial.

**#149 — Pattern file integration (P2):**
- Evaluated 4 options (forward ref, manifest includes, auto-convention,
  resolution depth). All add complexity to the resolution algorithm.
- Deeper question: do agents need pattern tutorials? No — LLMs know
  standard patterns from training data. Agent context needs conventions,
  not recipes.
- Decision: remove all 5 pattern files from manifest and dependency
  graph. Move to docs/patterns/ as human reference. Parent rules files
  keep one-line summaries.

**#150 — Agent-side dependency resolution (P2):**
- Resolution algorithm: core → stack deps → extras → platform. All
  steps use RESOLVE_DEPS (recursive). Extras are recursive for safety.
- Algorithm runs at build time (tools/sync.py, interview), not at agent
  startup. Generates explicit file lists for CLAUDE.md startup blocks.
- Full IDs everywhere — explicit over implicit.

**Decisions (all in ADR-004):**
- ADR-004: Composition over inheritance in dependency model
- Manifest `core:` field for core tier
- Pattern files removed from dependency graph (~1700 lines saved)
- Build-time resolution, not runtime
- No profiles, no auto-convention, no pattern resolution logic
