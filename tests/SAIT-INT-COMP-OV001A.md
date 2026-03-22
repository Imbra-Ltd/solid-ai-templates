---
id: SAIT-INT-COMP-OV001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567805
title: OVERRIDE directive replaces parent section entirely in the assembled output
product: sait
type: int
area: COMP
priority: p1
status: draft
environment: [local]
automatable: manual
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [composition, override, inheritance]
---

## Short description

> **Given** a stack template section marked `[OVERRIDE: <id>]` referencing a
> parent section tagged `[ID: <id>]`
> **When** an agent assembles the rule set for that section
> **Then** the output contains only the rules from the OVERRIDE section —
> the parent section rules are fully replaced

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Assembled section contains only the OVERRIDE rules; no rules from the parent section appear |
| FAILED | Parent section rules appear alongside or instead of the OVERRIDE rules |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-COMP-DO001A` is failing |
| ERROR | Agent fails to load or process the template files |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code or equivalent agent available
- Test pair: `stack/go-lib.md` (contains `[ID: go-lib-stack]`) and
  `stack/go-service.md` (contains `[OVERRIDE: go-lib-stack]` in its Stack section)

### Setup

1. Open Claude Code in the repository root
2. Attach `stack/go-lib.md` and `stack/go-service.md`

### Execution

1. Ask the agent:
   ```
   Show me the assembled Stack section for a Go service project.
   stack/go-service.md overrides the Stack section from stack/go-lib.md.
   Which rules appear?
   ```
2. Record the assembled output

### Assertions

1. Assert the assembled Stack section contains the rules from
   `stack/go-service.md` `[OVERRIDE: go-lib-stack]`
2. Assert the rules from `stack/go-lib.md` `[ID: go-lib-stack]` do NOT appear
3. Assert the section is not empty

### Teardown

— (read-only check, no teardown required)

## Related

- Related procedures: `SAIT-INT-COMP-DO001A`, `SAIT-INT-COMP-EX001A`
- Implements: SPEC.md §Override mechanism