# Tests

Procedure specifications for solid-ai-templates following the
[Imbra Procedure Specification Standard](https://github.com/Imbra-Ltd/imbra-knowledge/blob/main/standards/PROCEDURE-SPECIFICATION.md).

See `CODIFICATION.md` for the ID scheme, area codes, and component group registry.

## Specs

| ID | Type | Priority | Title |
|----|------|----------|-------|
| `SAIT-SMOKE-SYS-01-001A` | SMOKE | P0 | All DEPENDS ON file paths resolve to existing files |
| `SAIT-SMOKE-SYS-02-001A` | SMOKE | P0 | All section IDs are unique across all templates |
| `SAIT-SMOKE-COMP-04-001A` | SMOKE | P1 | All EXTEND and OVERRIDE directives reference existing IDs |
| `SAIT-INT-COMP-01-001A` | INT | P0 | DEPENDS ON chain assembles a complete rule set |
| `SAIT-INT-COMP-02-001A` | INT | P1 | EXTEND adds rules without removing base rules |
| `SAIT-INT-COMP-03-001A` | INT | P1 | OVERRIDE replaces parent section entirely |
| `SAIT-INT-COMP-05-001A` | INT | P1 | Conflicting OVERRIDEs on the same ID are flagged or resolved |
| `SAIT-INT-MANIF-01-001A` | INT | P0 | All manifest entries reference valid paths and IDs |
| `SAIT-INT-INTVW-01-001A` | INT | P0 | All REQUIRED interview questions are asked before output is generated |
| `SAIT-INT-INTVW-02-001A` | INT | P1 | DEFAULTED sections are pre-filled from the selected stack template |
| `SAIT-INT-INTVW-03-001A` | INT | P0 | Interview answers override stack and base template rules in the output |
| `SAIT-E2E-OUT-01-001A` | E2E | P0 | Full interview → CLAUDE.md for a FastAPI project |
| `SAIT-E2E-OUT-02-001A` | E2E | P0 | Full interview → CLAUDE.md for a Go Echo project |
| `SAIT-E2E-OUT-03-001A` | E2E | P1 | Full interview → AGENTS.md output format |
| `SAIT-E2E-OUT-04-001A` | E2E | P1 | Full interview → Cursor .mdc output format |
| `SAIT-E2E-OUT-05-001A` | E2E | P1 | Full interview → Copilot output format |
| `SAIT-E2E-OUT-06-001A` | E2E | P1 | Full interview → generic AI_CONTEXT.md output format |
| `SAIT-E2E-OUT-07-001A` | E2E | P1 | Full interview → CLAUDE.md for a Django project |
| `SAIT-E2E-OUT-08-001A` | E2E | P1 | Full interview → CLAUDE.md for a Node Express project |
| `SAIT-E2E-OUT-09-001A` | E2E | P1 | Full interview → CLAUDE.md for a React SPA project |
| `SAIT-E2E-OUT-10-001A` | E2E | P1 | Full interview → CLAUDE.md for a Next.js project |
| `SAIT-E2E-OUT-11-001A` | E2E | P1 | Full interview → CLAUDE.md for an Astro static site project |
| `SAIT-E2E-OUT-12-001A` | E2E | P1 | Full interview → CLAUDE.md for a Go gRPC service |
| `SAIT-E2E-OUT-13-001A` | E2E | P1 | Full interview → CLAUDE.md for a Flutter mobile project |
| `SAIT-E2E-OUT-14-001A` | E2E | P1 | Full interview → CLAUDE.md for a Go library project |
| `SAIT-E2E-OUT-15-001A` | E2E | P1 | Full interview → CLAUDE.md for a Flask project |
| `SAIT-E2E-OUT-16-001A` | E2E | P2 | Full interview → CLAUDE.md for a generic Python service |
| `SAIT-E2E-OUT-17-001A` | E2E | P1 | Full interview → CLAUDE.md for a Python gRPC service |
| `SAIT-E2E-OUT-18-001A` | E2E | P1 | Full interview → CLAUDE.md for a Python Celery worker |
| `SAIT-E2E-OUT-19-001A` | E2E | P1 | Full interview → CLAUDE.md for a Python library project |
| `SAIT-E2E-OUT-20-001A` | E2E | P2 | Full interview → CLAUDE.md for a generic Go service |
| `SAIT-E2E-OUT-21-001A` | E2E | P1 | Full interview → CLAUDE.md for a Hugo static site project |
| `SAIT-E2E-OUT-22-001A` | E2E | P1 | Full interview → CLAUDE.md for a Node.js library project |
| `SAIT-E2E-OUT-23-001A` | E2E | P1 | Full interview → CLAUDE.md for a Rust library project |
| `SAIT-E2E-OUT-24-001A` | E2E | P1 | Full interview → CLAUDE.md for an HTMX project |
| `SAIT-E2E-DEP-01-001A` | E2E | P1 | Cloud deployment target produces correct deployment rules |
| `SAIT-E2E-DEP-02-001A` | E2E | P1 | Hybrid deployment target produces correct deployment rules |
| `SAIT-E2E-DEP-03-001A` | E2E | P1 | Offline deployment target produces correct deployment rules |