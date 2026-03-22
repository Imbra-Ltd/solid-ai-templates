---
id: SAIT-SMK-SYS-02-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567802
title: All section IDs are unique across all templates
product: sait
type: smoke
area: SYS
priority: p0
status: draft
environment: [local, ci]
automatable: semi-manual
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [structure, ids, uniqueness]
---

## Short description

> **Given** the repository is cloned and all template files are present
> **When** all `[ID: ...]` tags across every template file are collected
> **Then** no two tags share the same ID value

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every `[ID: ...]` value is unique across all files in `base/`, `backend/`, `frontend/`, and `stack/` |
| FAILED | Two or more templates declare the same `[ID: ...]` value |
| SKIPPED | Repository cannot be cloned or accessed |
| BLOCKED | — |
| ERROR | File system is inaccessible; `grep` or equivalent tool fails |

## Steps

### Prerequisites

- Repository cloned locally
- Shell access with `grep` and `sort` available

### Setup

1. Change to the repository root

### Execution

1. Extract all `[ID: ...]` values from all template files:
   ```bash
   grep -rh "\[ID:" base/ backend/ frontend/ stack/ | sort
   ```
2. Identify duplicates:
   ```bash
   grep -rh "\[ID:" base/ backend/ frontend/ stack/ | sort | uniq -d
   ```

### Assertions

1. Assert the output of the duplicate check is empty — no duplicates exist
2. Assert every `[EXTEND: <id>]` and `[OVERRIDE: <id>]` reference matches
   an `[ID: ...]` that exists somewhere in the template tree

### Teardown

— (read-only check, no teardown required)

## Notes

Semi-manual because cross-file ID resolution requires a script.
A future CI step should automate this using `manifest.yaml`.

## Related

- Related procedures: `SAIT-SMK-SYS-01-001A`, `SAIT-INT-CMP-02-001A`, `SAIT-INT-CMP-03-001A`