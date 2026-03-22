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

### MANIF

| Code | Component |
|------|-----------|
| `MF` | Manifest entries — file paths, IDs, depends_on references |

### OUT

| Code | Component |
|------|-----------|
| `FA` | FastAPI output — python-fastapi stack interview flow |
| `GE` | Go Echo output — go-echo stack interview flow |

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
| `SAIT-INT-COMP-DO001A` | Integration — composition — DEPENDS ON chain — spec 1, version A |
| `SAIT-INT-COMP-EX001A` | Integration — composition — EXTEND directive — spec 1, version A |
| `SAIT-INT-COMP-OV001A` | Integration — composition — OVERRIDE directive — spec 1, version A |
| `SAIT-INT-MANIF-MF001A` | Integration — manifest — manifest entries — spec 1, version A |
| `SAIT-E2E-OUT-FA001A` | E2E — output — FastAPI flow — spec 1, version A |
| `SAIT-E2E-OUT-GE001A` | E2E — output — Go Echo flow — spec 1, version A |