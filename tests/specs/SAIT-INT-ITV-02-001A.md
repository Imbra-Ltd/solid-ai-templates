---
id: SAIT-INT-ITV-02-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567816
title: DEFAULTED sections are pre-filled from the selected stack template
product: sait
type: int
area: INTVW
priority: p1
status: ready
environment: [local]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [interview, defaults, pre-filled]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/python-fastapi.md` are attached to an agent
> **When** the agent completes the interview
> **Then** sections marked DEFAULTED in `INTERVIEW.md` are automatically
> pre-filled from the stack template without requiring user input

## Results

| Result | Condition |
|--------|-----------|
| PASSED | All DEFAULTED sections appear in the output populated with values from the stack template; user was not asked to provide these values |
| FAILED | Agent asks the user to fill in DEFAULTED sections manually; or DEFAULTED sections are empty in the output |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-ITV-01-001A` is failing |
| ERROR | Agent fails to load template files |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available
- Read `INTERVIEW.md` and note all sections marked `DEFAULTED`

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md` and `stack/python-fastapi.md`

### Execution

1. Ask the agent:
   ```
   Start the interview for a new project using stack/python-fastapi.md.
   ```
2. Answer only the REQUIRED questions
3. After answering all REQUIRED questions, ask for the output:
   ```
   Generate CLAUDE.md now.
   ```
4. Review the generated output

### Assertions

1. Assert the agent did not ask questions for DEFAULTED sections during the interview
2. Assert all DEFAULTED sections appear in the generated output
3. Assert DEFAULTED section values match the corresponding rules in
   `stack/python-fastapi.md` and its dependency chain

### Teardown

— (no files to clean up unless output was saved)

## Related

- Related procedures: `SAIT-INT-ITV-01-001A`, `SAIT-INT-ITV-03-001A`
- Implements: SPEC.md §Interview template structure