# Dev Journal

## 2026-05-01 — Session protocol hardening

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
