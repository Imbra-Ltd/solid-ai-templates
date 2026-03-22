---
id: SAIT-E2E-FMT-05-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567812
title: Full interview produces a correct .cursor/rules/project.mdc for a FastAPI project
product: sait
type: e2e
area: FMT
priority: p1
status: ready
environment: [local]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [e2e, output, cursor, mdc]
---

## Short description

> **Given** `INTERVIEW.md`, `stack/python-fastapi.md`, and `output/cursorrules.md`
> are attached to an agent
> **When** the agent conducts the interview and generates output
> **Then** the result is a valid `.cursor/rules/project.mdc` formatted per
> `output/cursorrules.md` containing all required sections

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output is formatted as `.mdc` per `output/cursorrules.md`; all required sections present; Cursor-specific frontmatter present |
| FAILED | Output uses CLAUDE.md format; Cursor frontmatter absent; required sections missing |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-E2E-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/python-fastapi.md`, `output/cursorrules.md`

### Execution

1. Ask the agent:
   ```
   Using INTERVIEW.md and stack/python-fastapi.md, generate a
   .cursor/rules/project.mdc for this project.
   Use output/cursorrules.md for formatting rules.
   ```
2. Provide interview answers (OrderService / FastAPI)
3. Save the generated output

### Assertions

1. Assert output follows `.mdc` format as defined in `output/cursorrules.md`
2. Assert Cursor-specific frontmatter is present
3. Assert all required content sections are present
4. Assert FastAPI-specific rules are present

### Teardown

1. Delete the generated file

## Related

- Related procedures: `SAIT-E2E-TPL-01-001A`, `SAIT-E2E-FMT-05-001A`