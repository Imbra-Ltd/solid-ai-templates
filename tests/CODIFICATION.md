# Test Codification Scheme

Defines the procedure ID scheme for solid-ai-templates test specifications.
Follows the Imbra Procedure Specification Standard
(`imbra-knowledge/standards/PROCEDURE-SPECIFICATION.md`).

---

## ID format

```
{PRODUCT}-{TYPE}-{AREA}-{GG}{NNN}{VER}
```

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

## Component groups (GG)

Component group codes are fixed per area. Once assigned, a code is never
reused for a different component within the same area.

### SYS

| Code | Component |
|------|-----------|
| `FS` | File structure — DEPENDS ON path resolution, file existence |
| `ID` | ID uniqueness — section IDs across all templates |

### COMP

| Code | Component |
|------|-----------|
| `DO` | DEPENDS ON — dependency chain assembly |
| `EX` | EXTEND — additive directive behaviour |
| `OV` | OVERRIDE — replacement directive behaviour |
| `ER` | Reference resolution — EXTEND/OVERRIDE refs point to existing IDs |
| `CF` | Conflict resolution — two templates OVERRIDE the same section ID |

### MANIF

| Code | Component |
|------|-----------|
| `MF` | Manifest entries — file paths, IDs, depends_on references |

### OUT

| Code | Component |
|------|-----------|
| `FA` | FastAPI output — python-fastapi stack interview flow |
| `GE` | Go Echo output — go-echo stack interview flow |
| `AG` | AGENTS.md output — OpenAI Codex CLI format |
| `CU` | Cursor output — .cursor/rules/project.mdc format |
| `CP` | Copilot output — .github/copilot-instructions.md format |
| `GN` | Generic output — AI_CONTEXT.md fallback format |
| `DJ` | Django output — python-django stack interview flow |
| `NE` | Express output — node-express stack interview flow |
| `SR` | React SPA output — spa-react stack interview flow |
| `NJ` | Next.js output — full-nextjs stack interview flow |
| `AS` | Astro output — static-site-astro stack interview flow |
| `GR` | gRPC Go output — go-grpc stack interview flow |
| `MB` | Flutter output — mobile-flutter stack interview flow |
| `LB` | Node lib output — nodejs-lib stack interview flow |

### INTVW

| Code | Component |
|------|-----------|
| `RQ` | Required questions — all REQUIRED questions asked before generation |
| `DF` | Default sections — DEFAULTED sections pre-filled from templates |
| `PR` | Precedence — interview answers override stack and base rules |

### DEP

| Code | Component |
|------|-----------|
| `CL` | Cloud — public cloud deployment target output |
| `HY` | Hybrid — on-premises + cloud deployment target output |
| `OF` | Offline — air-gapped deployment target output |

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
| `SAIT-SMOKE-SYS-FS001A` | Smoke — system — file structure — spec 1, version A |
| `SAIT-SMOKE-SYS-ID001A` | Smoke — system — ID uniqueness — spec 1, version A |
| `SAIT-SMOKE-COMP-ER001A` | Smoke — composition — ref resolution — spec 1, version A |
| `SAIT-INT-COMP-DO001A` | Integration — composition — DEPENDS ON chain — spec 1, version A |
| `SAIT-INT-COMP-EX001A` | Integration — composition — EXTEND directive — spec 1, version A |
| `SAIT-INT-COMP-OV001A` | Integration — composition — OVERRIDE directive — spec 1, version A |
| `SAIT-INT-COMP-CF001A` | Integration — composition — conflict resolution — spec 1, version A |
| `SAIT-INT-MANIF-MF001A` | Integration — manifest — manifest entries — spec 1, version A |
| `SAIT-INT-INTVW-RQ001A` | Integration — interview — required questions — spec 1, version A |
| `SAIT-INT-INTVW-DF001A` | Integration — interview — default sections — spec 1, version A |
| `SAIT-INT-INTVW-PR001A` | Integration — interview — answer precedence — spec 1, version A |
| `SAIT-E2E-OUT-FA001A` | E2E — output — FastAPI flow — spec 1, version A |
| `SAIT-E2E-OUT-GE001A` | E2E — output — Go Echo flow — spec 1, version A |
| `SAIT-E2E-OUT-AG001A` | E2E — output — AGENTS.md format — spec 1, version A |
| `SAIT-E2E-OUT-CU001A` | E2E — output — Cursor format — spec 1, version A |
| `SAIT-E2E-OUT-CP001A` | E2E — output — Copilot format — spec 1, version A |
| `SAIT-E2E-OUT-GN001A` | E2E — output — Generic format — spec 1, version A |
| `SAIT-E2E-OUT-DJ001A` | E2E — output — Django flow — spec 1, version A |
| `SAIT-E2E-OUT-NE001A` | E2E — output — Express flow — spec 1, version A |
| `SAIT-E2E-OUT-SR001A` | E2E — output — React SPA flow — spec 1, version A |
| `SAIT-E2E-OUT-NJ001A` | E2E — output — Next.js flow — spec 1, version A |
| `SAIT-E2E-OUT-AS001A` | E2E — output — Astro flow — spec 1, version A |
| `SAIT-E2E-OUT-GR001A` | E2E — output — gRPC Go flow — spec 1, version A |
| `SAIT-E2E-OUT-MB001A` | E2E — output — Flutter flow — spec 1, version A |
| `SAIT-E2E-OUT-LB001A` | E2E — output — Node lib flow — spec 1, version A |
| `SAIT-E2E-DEP-CL001A` | E2E — deployment — cloud scenario — spec 1, version A |
| `SAIT-E2E-DEP-HY001A` | E2E — deployment — hybrid scenario — spec 1, version A |
| `SAIT-E2E-DEP-OF001A` | E2E — deployment — offline scenario — spec 1, version A |