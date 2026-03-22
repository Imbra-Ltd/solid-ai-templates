---
id: SAIT-E2E-FMT-05-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567813
title: Full interview produces a correct copilot-instructions.md for a FastAPI project
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
tags: [e2e, output, copilot, github]
---

## Short description

> **Given** `INTERVIEW.md`, `stack/python-fastapi.md`, and `output/copilot.md`
> are attached to an agent
> **When** the agent conducts the interview and generates output
> **Then** the result is a valid `.github/copilot-instructions.md` formatted
> per `output/copilot.md` containing all required sections

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output follows `output/copilot.md` formatting rules; all required sections present; file is valid Markdown for GitHub Copilot |
| FAILED | Output uses CLAUDE.md format; required sections missing; Copilot-specific formatting absent |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-E2E-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/python-fastapi.md`, `output/copilot.md`

### Execution

1. Ask the agent:
   ```
   Using INTERVIEW.md and stack/python-fastapi.md, generate a
   .github/copilot-instructions.md for this project.
   Use output/copilot.md for formatting rules.
   ```
2. Provide interview answers (OrderService / FastAPI)
3. Save the generated output

### Assertions

1. Assert output follows formatting rules from `output/copilot.md`
2. Assert all required sections are present
3. Assert FastAPI-specific rules are present

### Teardown

1. Delete the generated file

## Related

- Related procedures: `SAIT-E2E-TPL-01-001A`, `SAIT-E2E-FMT-05-001A`