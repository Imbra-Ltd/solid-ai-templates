# Dev Journal

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

## 2026-04-27 — Skills roadmap and commercialization spike

- Added Phase 15 (Skills) to `ROADMAP.md` with four categories:
  generative, transformation, review, ops — plus infrastructure tasks
- Renamed existing Phase 15 (Validation) to Phase 16
- Updated `SPIKE-IMCONTEXT-COMMERCIALIZATION.md` in `imbra-explore`:
  added "Skills as a marketplace dimension" subsection under Option 5
- Key insight: skills (dynamic, on-demand actions) complement static
  context files (CLAUDE.md/AGENTS.md) — they don't replace them
- Skills fit into the existing im-context product roadmap as an
  extension of the template marketplace (Year 3+), but should be
  designed into CLI/web app from the start
