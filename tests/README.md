# Tests

Procedure specifications for solid-ai-templates following the
[Imbra Procedure Specification Standard](https://github.com/Imbra-Ltd/imbra-knowledge/blob/main/standards/PROCEDURE-SPECIFICATION.md).

See `CODIFICATION.md` for the ID scheme, area codes, and component group registry.

## Specs

| ID | Type | Priority | Title |
|----|------|----------|-------|
| `SAIT-SMOKE-SYS-FS001A` | SMOKE | P0 | All DEPENDS ON file paths resolve to existing files |
| `SAIT-SMOKE-SYS-ID001A` | SMOKE | P0 | All section IDs are unique across all templates |
| `SAIT-INT-COMP-DO001A` | INT | P0 | DEPENDS ON chain assembles a complete rule set |
| `SAIT-INT-COMP-EX001A` | INT | P1 | EXTEND adds rules without removing base rules |
| `SAIT-INT-COMP-OV001A` | INT | P1 | OVERRIDE replaces parent section entirely |
| `SAIT-INT-MANIF-MF001A` | INT | P0 | All manifest entries reference valid paths and IDs |
| `SAIT-E2E-OUT-FA001A` | E2E | P0 | Full interview → CLAUDE.md for a FastAPI project |
| `SAIT-E2E-OUT-GE001A` | E2E | P0 | Full interview → CLAUDE.md for a Go Echo project |