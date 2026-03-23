---
id: SAIT-E2E-STK-09-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567824
title: Full interview produces a correct CLAUDE.md for a Flutter mobile project
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
tags: [e2e, output, flutter, mobile, dart]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/mobile-flutter.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing Flutter-specific rules
> alongside frontend layer and base rules

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains Flutter-specific rules (widgets, state management, platform channels, golden tests); frontend and base rules present |
| FAILED | Flutter-specific rules absent; output resembles a web frontend project |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/mobile-flutter.md`, `formats/claude.md`
3. Interview answers:
   - Project name: FieldSurveyApp
   - Language: Dart
   - State management: Riverpod
   - Platforms: iOS and Android
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists Flutter, Dart, Riverpod
2. Assert widget composition rules present (prefer composition over inheritance)
3. Assert Riverpod provider patterns documented
4. Assert platform channel usage documented for native integrations
5. Assert golden test or widget test approach referenced
6. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-05-001A`