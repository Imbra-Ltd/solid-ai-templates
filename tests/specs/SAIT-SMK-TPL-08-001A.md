---
id: SAIT-SMK-TPL-08-001A
title: Every base template has at least one [ID:] tag
product: sait
type: smoke
area: TPL
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-05-07
author: Branimir Georgiev
product-version: "2.x"
tags: [structure, id-tag, base, core]
---

## Short description

> **Given** the repository is cloned and all template files are present
> **When** every `.md` file in `templates/base/` subdirectories is checked
> **Then** each file contains at least one `[ID: ...]` tag

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every base template has at least one `[ID:]` tag |
| FAILED | One or more base templates have no `[ID:]` tag |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | File system is inaccessible |

## Steps

### Prerequisites

- Repository cloned locally

### Setup

1. Change to the repository root

### Execution

1. Collect all `.md` files from `templates/base/` subdirectories
   (core, security, infra, workflow, language, data)
2. Search each file for `[ID: ...]` pattern

### Assertions

1. Assert every base template contains at least one `[ID:]` tag

### Teardown

— (read-only check, no teardown required)

## Notes

Base templates are the foundation of the inheritance model. Every
section must be tagged so that stack templates can EXTEND or OVERRIDE
it. A missing `[ID:]` makes the section unreachable.

## Related

- Related procedures: `SAIT-SMK-SYS-02-001A`
