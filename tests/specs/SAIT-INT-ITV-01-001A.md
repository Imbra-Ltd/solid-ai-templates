---
id: SAIT-INT-ITV-01-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567815
title: Agent asks all REQUIRED questions before generating output
product: sait
type: int
area: INTVW
priority: p0
status: draft
environment: [local]
automatable: manual
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [interview, required, questions]
---

## Short description

> **Given** `INTERVIEW.md` and a stack template are attached to an agent
> **When** the agent starts the interview
> **Then** the agent asks every question marked REQUIRED in `INTERVIEW.md`
> before generating any output, and does not generate output until all
> REQUIRED questions are answered

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Agent asks all REQUIRED questions; refuses to generate output if any REQUIRED question is unanswered |
| FAILED | Agent skips one or more REQUIRED questions; or agent generates output before all REQUIRED questions are answered |
| SKIPPED | No agent available |
| BLOCKED | — |
| ERROR | Agent fails to load `INTERVIEW.md` |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md` and `stack/python-fastapi.md`
3. Read `INTERVIEW.md` and note every question marked `REQUIRED`

### Execution

1. Ask the agent:
   ```
   Start the interview for a new project using stack/python-fastapi.md.
   ```
2. Track which questions the agent asks
3. When the agent asks for output format, respond with: "Generate CLAUDE.md"
4. Deliberately skip one REQUIRED question — respond "skip" or leave blank
5. Observe whether the agent proceeds or asks again

### Assertions

1. Assert the agent asks every question marked `REQUIRED` in `INTERVIEW.md`
2. Assert the agent does not generate output until all REQUIRED questions
   have a non-empty answer
3. Assert the agent re-prompts or clarifies when a REQUIRED question is skipped

### Teardown

— (no files generated)

## Related

- Related procedures: `SAIT-INT-ITV-02-001A`, `SAIT-INT-ITV-03-001A`
- Implements: SPEC.md §Interview template structure

## Notes

Requires multi-turn conversation to test the re-prompt behaviour
(agent must ask again when a REQUIRED question is skipped). Not
automatable with single-turn `claude -p`.
