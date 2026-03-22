# Test Codification Scheme

Defines the procedure ID scheme for solid-ai-templates test specifications.
Follows the Imbra Procedure Specification Standard
(`imbra-knowledge/standards/PROCEDURE-SPECIFICATION.md`).

---

## ID format

```
{PRODUCT}-{TYPE}-{AREA}-{NN}-{NNN}{VER}
```

| Segment | Description |
|---------|-------------|
| `PRODUCT` | Product code — always `SAIT` |
| `TYPE` | Procedure type — `SMOKE`, `INT`, `E2E` |
| `AREA` | Functional area — `SYS`, `COMP`, `MANIF`, `OUT`, `INTVW`, `DEP` |
| `NN` | Two-digit component group number — unique within an area |
| `NNN` | Three-digit sequence number within the group |
| `VER` | Version letter — `A` original, `B` first major revision |

---

## Product code

| Code | Product |
|------|---------|
| `SAIT` | solid-ai-templates |

---

## Procedure types

| Code | Type | Description |
|------|------|-------------|
| `SMOKE` | Smoke test | Quick structural health check — files exist, IDs unique, paths resolve |
| `INT` | Integration test | Verify two or more templates work together correctly |
| `E2E` | End-to-end test | Verify a complete interview → output generation flow |

---

## Areas

| Code | Area | Description |
|------|------|-------------|
| `SYS` | System | Cross-cutting structural checks spanning multiple concerns |
| `COMP` | Composition | Template composition — DEPENDS ON chain, EXTEND, OVERRIDE directives |
| `MANIF` | Manifest | manifest.yaml consistency — IDs, file paths, dependency references |
| `OUT` | Output | Context file generation — interview → CLAUDE.md / AGENTS.md / etc. |
| `INTVW` | Interview | Interview flow — required questions, defaults, answer precedence |
| `DEP` | Deployment | Deployment target scenarios — cloud, hybrid, offline |

---

## Component groups

Component group numbers are fixed per area. Once assigned, a number is never
reused for a different component within the same area.

### SYS

| Number | Component |
|--------|-----------|
| `01` | File structure — DEPENDS ON path resolution, file existence |
| `02` | ID uniqueness — section IDs across all templates |

### COMP

| Number | Component |
|--------|-----------|
| `01` | DEPENDS ON — dependency chain assembly |
| `02` | EXTEND — additive directive behaviour |
| `03` | OVERRIDE — replacement directive behaviour |
| `04` | Reference resolution — EXTEND/OVERRIDE refs point to existing IDs |
| `05` | Conflict resolution — two templates OVERRIDE the same section ID |

### MANIF

| Number | Component |
|--------|-----------|
| `01` | Manifest entries — file paths, IDs, depends_on references |

### OUT

| Number | Component |
|--------|-----------|
| `01` | FastAPI output — python-fastapi stack interview flow |
| `02` | Go Echo output — go-echo stack interview flow |
| `03` | AGENTS.md output — OpenAI Codex CLI format |
| `04` | Cursor output — .cursor/rules/project.mdc format |
| `05` | Copilot output — .github/copilot-instructions.md format |
| `06` | Generic output — AI_CONTEXT.md fallback format |
| `07` | Django output — python-django stack interview flow |
| `08` | Express output — node-express stack interview flow |
| `09` | React SPA output — spa-react stack interview flow |
| `10` | Next.js output — full-nextjs stack interview flow |
| `11` | Astro output — static-site-astro stack interview flow |
| `12` | gRPC Go output — go-grpc stack interview flow |
| `13` | Flutter output — mobile-flutter stack interview flow |
| `14` | Go lib output — go-lib stack interview flow |
| `15` | Flask output — python-flask stack interview flow |
| `16` | Python service output — python-service base stack |
| `17` | Python gRPC output — python-grpc stack interview flow |
| `18` | Celery worker output — python-celery-worker stack |
| `19` | Python lib output — python-lib stack interview flow |
| `20` | Go service output — go-service base stack |
| `21` | Hugo output — static-site-hugo stack interview flow |
| `22` | Node.js lib output — nodejs-lib stack interview flow |
| `23` | Rust lib output — rust-lib stack interview flow |
| `24` | HTMX output — htmx stack interview flow |

### INTVW

| Number | Component |
|--------|-----------|
| `01` | Required questions — all REQUIRED questions asked before generation |
| `02` | Default sections — DEFAULTED sections pre-filled from templates |
| `03` | Precedence — interview answers override stack and base rules |

### DEP

| Number | Component |
|--------|-----------|
| `01` | Cloud — public cloud deployment target output |
| `02` | Hybrid — on-premises + cloud deployment target output |
| `03` | Offline — air-gapped deployment target output |

---

## Version suffix

| Suffix | Meaning |
|--------|---------|
| `A` | Original version |
| `B` | First major revision (scope or assertions changed) |
| `C` | Second major revision |

Amend in place (no new suffix) for: typo fixes, wording clarifications,
corrected prerequisites where test intent is unchanged.

---

## Full ID examples

| ID | Meaning |
|----|---------|
| `SAIT-SMOKE-SYS-01-001A` | Smoke — system — file structure — spec 1, version A |
| `SAIT-SMOKE-SYS-02-001A` | Smoke — system — ID uniqueness — spec 1, version A |
| `SAIT-SMOKE-COMP-04-001A` | Smoke — composition — ref resolution — spec 1, version A |
| `SAIT-INT-COMP-01-001A` | Integration — composition — DEPENDS ON chain — spec 1, version A |
| `SAIT-INT-COMP-02-001A` | Integration — composition — EXTEND directive — spec 1, version A |
| `SAIT-INT-COMP-03-001A` | Integration — composition — OVERRIDE directive — spec 1, version A |
| `SAIT-INT-COMP-05-001A` | Integration — composition — conflict resolution — spec 1, version A |
| `SAIT-INT-MANIF-01-001A` | Integration — manifest — manifest entries — spec 1, version A |
| `SAIT-INT-INTVW-01-001A` | Integration — interview — required questions — spec 1, version A |
| `SAIT-INT-INTVW-02-001A` | Integration — interview — default sections — spec 1, version A |
| `SAIT-INT-INTVW-03-001A` | Integration — interview — answer precedence — spec 1, version A |
| `SAIT-E2E-OUT-01-001A` | E2E — output — FastAPI flow — spec 1, version A |
| `SAIT-E2E-OUT-02-001A` | E2E — output — Go Echo flow — spec 1, version A |
| `SAIT-E2E-OUT-03-001A` | E2E — output — AGENTS.md format — spec 1, version A |
| `SAIT-E2E-OUT-04-001A` | E2E — output — Cursor format — spec 1, version A |
| `SAIT-E2E-OUT-05-001A` | E2E — output — Copilot format — spec 1, version A |
| `SAIT-E2E-OUT-06-001A` | E2E — output — Generic format — spec 1, version A |
| `SAIT-E2E-OUT-07-001A` | E2E — output — Django flow — spec 1, version A |
| `SAIT-E2E-OUT-08-001A` | E2E — output — Express flow — spec 1, version A |
| `SAIT-E2E-OUT-09-001A` | E2E — output — React SPA flow — spec 1, version A |
| `SAIT-E2E-OUT-10-001A` | E2E — output — Next.js flow — spec 1, version A |
| `SAIT-E2E-OUT-11-001A` | E2E — output — Astro flow — spec 1, version A |
| `SAIT-E2E-OUT-12-001A` | E2E — output — gRPC Go flow — spec 1, version A |
| `SAIT-E2E-OUT-13-001A` | E2E — output — Flutter flow — spec 1, version A |
| `SAIT-E2E-OUT-14-001A` | E2E — output — Go lib flow — spec 1, version A |
| `SAIT-E2E-OUT-15-001A` | E2E — output — Flask flow — spec 1, version A |
| `SAIT-E2E-OUT-16-001A` | E2E — output — Python service flow — spec 1, version A |
| `SAIT-E2E-OUT-17-001A` | E2E — output — Python gRPC flow — spec 1, version A |
| `SAIT-E2E-OUT-18-001A` | E2E — output — Celery worker flow — spec 1, version A |
| `SAIT-E2E-OUT-19-001A` | E2E — output — Python lib flow — spec 1, version A |
| `SAIT-E2E-OUT-20-001A` | E2E — output — Go service flow — spec 1, version A |
| `SAIT-E2E-OUT-21-001A` | E2E — output — Hugo flow — spec 1, version A |
| `SAIT-E2E-OUT-22-001A` | E2E — output — Node.js lib flow — spec 1, version A |
| `SAIT-E2E-OUT-23-001A` | E2E — output — Rust lib flow — spec 1, version A |
| `SAIT-E2E-OUT-24-001A` | E2E — output — HTMX flow — spec 1, version A |
| `SAIT-E2E-DEP-01-001A` | E2E — deployment — cloud scenario — spec 1, version A |
| `SAIT-E2E-DEP-02-001A` | E2E — deployment — hybrid scenario — spec 1, version A |
| `SAIT-E2E-DEP-03-001A` | E2E — deployment — offline scenario — spec 1, version A |