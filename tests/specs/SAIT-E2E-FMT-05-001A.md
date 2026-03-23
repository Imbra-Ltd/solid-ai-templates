---
id: SAIT-E2E-FMT-05-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567814
title: Full interview produces a correct AI_CONTEXT.md for a FastAPI project
product: sait
type: e2e
area: FMT
priority: p2
status: ready
environment: [local]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [e2e, output, generic, ai-context]
---

## Short description

> **Given** `INTERVIEW.md`, `stack/python-fastapi.md`, and `output/generic.md`
> are attached to an agent
> **When** the agent conducts the interview and generates output
> **Then** the result is a valid `AI_CONTEXT.md` formatted per
> `output/generic.md` usable by any AI agent

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output filename is `AI_CONTEXT.md`; formatting follows `output/generic.md`; all required sections present; no tool-specific formatting |
| FAILED | Output uses CLAUDE.md or Cursor-specific formatting; required sections missing |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-E2E-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/python-fastapi.md`, `output/generic.md`

### Execution

1. Ask the agent:
   ```
   Using INTERVIEW.md and stack/python-fastapi.md, generate an AI_CONTEXT.md
   for this project. Use output/generic.md for formatting rules.
   ```
2. Provide interview answers (OrderService / FastAPI)
3. Save the generated output

### Assertions

1. Assert output filename is `AI_CONTEXT.md`
2. Assert formatting follows `output/generic.md` — no tool-specific syntax
3. Assert all required sections are present
4. Assert content is agent-agnostic (no Claude-specific or Cursor-specific directives)

### Teardown

1. Delete the generated file

## Related

- Related procedures: `SAIT-E2E-FMT-05-001A`