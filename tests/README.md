# Tests

Procedure specifications for solid-ai-templates following the
[Imbra Procedure Specification Standard](https://github.com/Imbra-Ltd/imbra-knowledge/blob/main/standards/PROCEDURE-SPECIFICATION.md).

See `CODIFICATION.md` for the ID scheme, area codes, and component group registry.

## Specs

| ID | Type | Priority | Title |
|----|------|----------|-------|
| `SAIT-SMOKE-SYS-FS001A` | SMOKE | P0 | All DEPENDS ON file paths resolve to existing files |
| `SAIT-SMOKE-SYS-ID001A` | SMOKE | P0 | All section IDs are unique across all templates |
| `SAIT-SMOKE-COMP-ER001A` | SMOKE | P1 | All EXTEND and OVERRIDE directives reference existing IDs |
| `SAIT-INT-COMP-DO001A` | INT | P0 | DEPENDS ON chain assembles a complete rule set |
| `SAIT-INT-COMP-EX001A` | INT | P1 | EXTEND adds rules without removing base rules |
| `SAIT-INT-COMP-OV001A` | INT | P1 | OVERRIDE replaces parent section entirely |
| `SAIT-INT-COMP-CF001A` | INT | P1 | Conflicting OVERRIDEs on the same ID are flagged or resolved |
| `SAIT-INT-MANIF-MF001A` | INT | P0 | All manifest entries reference valid paths and IDs |
| `SAIT-INT-INTVW-RQ001A` | INT | P0 | All REQUIRED interview questions are asked before output is generated |
| `SAIT-INT-INTVW-DF001A` | INT | P1 | DEFAULTED sections are pre-filled from the selected stack template |
| `SAIT-INT-INTVW-PR001A` | INT | P0 | Interview answers override stack and base template rules in the output |
| `SAIT-E2E-OUT-FA001A` | E2E | P0 | Full interview → CLAUDE.md for a FastAPI project |
| `SAIT-E2E-OUT-GE001A` | E2E | P0 | Full interview → CLAUDE.md for a Go Echo project |
| `SAIT-E2E-OUT-AG001A` | E2E | P1 | Full interview → AGENTS.md output format |
| `SAIT-E2E-OUT-CU001A` | E2E | P1 | Full interview → Cursor .mdc output format |
| `SAIT-E2E-OUT-CP001A` | E2E | P1 | Full interview → Copilot output format |
| `SAIT-E2E-OUT-GN001A` | E2E | P1 | Full interview → generic AI_CONTEXT.md output format |
| `SAIT-E2E-OUT-DJ001A` | E2E | P1 | Full interview → CLAUDE.md for a Django project |
| `SAIT-E2E-OUT-NE001A` | E2E | P1 | Full interview → CLAUDE.md for a Node Express project |
| `SAIT-E2E-OUT-SR001A` | E2E | P1 | Full interview → CLAUDE.md for a React SPA project |
| `SAIT-E2E-OUT-NJ001A` | E2E | P1 | Full interview → CLAUDE.md for a Next.js project |
| `SAIT-E2E-OUT-AS001A` | E2E | P1 | Full interview → CLAUDE.md for an Astro static site project |
| `SAIT-E2E-OUT-GR001A` | E2E | P1 | Full interview → CLAUDE.md for a Go gRPC service |
| `SAIT-E2E-OUT-MB001A` | E2E | P1 | Full interview → CLAUDE.md for a Flutter mobile project |
| `SAIT-E2E-OUT-LB001A` | E2E | P1 | Full interview → CLAUDE.md for a Go library project |
| `SAIT-E2E-OUT-FL001A` | E2E | P1 | Full interview → CLAUDE.md for a Flask project |
| `SAIT-E2E-OUT-PY001A` | E2E | P2 | Full interview → CLAUDE.md for a generic Python service |
| `SAIT-E2E-OUT-PG001A` | E2E | P1 | Full interview → CLAUDE.md for a Python gRPC service |
| `SAIT-E2E-OUT-CW001A` | E2E | P1 | Full interview → CLAUDE.md for a Python Celery worker |
| `SAIT-E2E-OUT-PL001A` | E2E | P1 | Full interview → CLAUDE.md for a Python library project |
| `SAIT-E2E-OUT-GS001A` | E2E | P2 | Full interview → CLAUDE.md for a generic Go service |
| `SAIT-E2E-OUT-HG001A` | E2E | P1 | Full interview → CLAUDE.md for a Hugo static site project |
| `SAIT-E2E-OUT-NL001A` | E2E | P1 | Full interview → CLAUDE.md for a Node.js library project |
| `SAIT-E2E-OUT-RL001A` | E2E | P1 | Full interview → CLAUDE.md for a Rust library project |
| `SAIT-E2E-DEP-CL001A` | E2E | P1 | Cloud deployment target produces correct deployment rules |
| `SAIT-E2E-DEP-HY001A` | E2E | P1 | Hybrid deployment target produces correct deployment rules |
| `SAIT-E2E-DEP-OF001A` | E2E | P1 | Offline deployment target produces correct deployment rules |