---
id: SAIT-E2E-STK-14-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567832
title: Full interview produces a correct CLAUDE.md for a Python Celery worker
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
tags: [e2e, output, celery, python, async, worker]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/python-celery-worker.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing Celery-specific rules
> alongside python-service and base rules

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains Celery-specific rules (task definition, broker config, retry policy, idempotency, beat scheduler); python-service and base rules present |
| FAILED | Celery-specific rules absent; output resembles a web service rather than an async worker |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/python-celery-worker.md`, `output/claude.md`
3. Interview answers:
   - Project name: EmailDispatchWorker
   - Language: Python
   - Broker: Redis
   - Result backend: Redis
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists Python, Celery, Redis
2. Assert task idempotency rules present
3. Assert retry policy conventions documented (`max_retries`, exponential backoff)
4. Assert Celery Beat referenced for periodic tasks
5. Assert no HTTP endpoint conventions present (worker only)
6. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-12-001A`