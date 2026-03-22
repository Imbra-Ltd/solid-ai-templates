---
id: SAIT-INT-ITV-03-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567817
title: Interview answers override stack and base template rules in the output
product: sait
type: int
area: INTVW
priority: p0
status: ready
environment: [local]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [interview, precedence, override]
---

## Short description

> **Given** a stack template defines a rule and the interview answer contradicts it
> **When** the agent generates the output
> **Then** the interview answer takes precedence over the stack rule in the
> final output — the stack rule does not appear

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Interview answer appears in the output; contradicted stack rule does not appear; no contradiction exists in the output |
| FAILED | Stack rule appears instead of or alongside the interview answer; output contains a contradiction |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-ITV-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md` and `stack/python-fastapi.md`
3. Note that `stack/python-fastapi.md` specifies `pytest` as the test runner

### Execution

1. Start the interview:
   ```
   Start the interview for a new project using stack/python-fastapi.md.
   ```
2. Answer all REQUIRED questions
3. When asked about testing (or in the OVERRIDES section), provide a
   contradicting answer:
   ```
   Use unittest instead of pytest for all tests.
   ```
4. Generate `CLAUDE.md`

### Assertions

1. Assert the Testing section in the output specifies `unittest`
2. Assert `pytest` does not appear in the Testing section
3. Assert no contradiction exists between the Testing section and any
   other section in the output

### Teardown

— (no files to clean up unless output was saved)

## Notes

This tests the highest precedence level defined in SPEC.md:
"Interview answers — the highest precedence; always win over any template."

## Related

- Related procedures: `SAIT-INT-ITV-01-001A`, `SAIT-INT-ITV-02-001A`
- Implements: SPEC.md §Precedence rules