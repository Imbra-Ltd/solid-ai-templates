---
id: SAIT-E2E-STK-05-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567820
title: Full interview produces a correct CLAUDE.md for a React SPA project
product: sait
type: e2e
area: STK
priority: p1
status: ready
environment: [local]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [e2e, output, react, spa, frontend]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/spa-react.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing React-specific rules
> alongside frontend layer and base rules

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains React-specific rules (components, hooks, RTL, a11y); frontend layer rules present (UX, accessibility, CSS); base rules present |
| FAILED | React-specific rules absent; frontend layer rules absent; output resembles a backend service |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/spa-react.md`, `base/core/agents.md`
3. Interview answers:
   - Project name: DashboardApp
   - Language: TypeScript
   - State management: Zustand
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists React, TypeScript, Zustand
2. Assert component rules present (composition, single responsibility)
3. Assert React Testing Library referenced in testing section
4. Assert accessibility rules present (from `frontend/ux.md`)
5. Assert CSS conventions present (from `frontend/quality.md`)
6. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-06-001A`