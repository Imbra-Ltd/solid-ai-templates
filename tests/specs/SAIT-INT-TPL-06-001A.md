---
id: SAIT-INT-TPL-06-001A
title: EXTEND and OVERRIDE targets are reachable in the resolved chain
product: sait
type: integration
area: TPL
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-05-06
author: Branimir Georgiev
product-version: "2.x"
tags: [chain, extend, override, reachability]
---

## Short description

> **Given** the manifest is loaded and all stacks are resolved
> **When** every `[EXTEND: <id>]` and `[OVERRIDE: <id>]` directive in every
> file of a stack's resolved chain is collected
> **Then** each referenced ID matches an `[ID: <id>]` tag declared in a file
> that is also part of that same resolved chain

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every EXTEND/OVERRIDE target in every chain file is declared by another file in the same chain |
| FAILED | One or more targets reference an ID declared in a file outside the resolved chain |
| SKIPPED | PyYAML not installed |
| BLOCKED | `SAIT-INT-MNF-02-001A` is failing |
| ERROR | File system or manifest is inaccessible |

## Steps

### Prerequisites

- Repository cloned locally
- `pyyaml` installed (`pip install pyyaml`)

### Setup

1. Load `templates/manifest.yaml`
2. Resolve the dependency chain for every stack entry

### Execution

1. For each stack, collect all `[ID: X]` declarations from every
   file in its resolved chain into a set `chain_ids`
2. For each file in the chain, collect all `[EXTEND: X]` and
   `[OVERRIDE: X]` references
3. For each reference, check that the target ID is in `chain_ids`

### Assertions

1. Assert every EXTEND/OVERRIDE target is present in the chain's
   collected IDs

### Teardown

None.

## Related

- Supersedes gap in: `SAIT-SMK-TPL-04-001A` (checks global existence only)
- Depends on: `SAIT-INT-MNF-02-001A` (chains must resolve first)
- Context: issue #283, discovered via #276
