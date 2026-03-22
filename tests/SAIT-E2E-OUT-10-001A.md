---
id: SAIT-E2E-OUT-10-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567821
title: Full interview produces a correct CLAUDE.md for a Next.js project
product: sait
type: e2e
area: OUT
priority: p1
status: draft
environment: [local]
automatable: manual
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [e2e, output, nextjs, fullstack, react]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/full-nextjs.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing Next.js-specific rules
> alongside frontend layer and base rules

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains Next.js-specific rules (App Router, Server Components, Route Handlers, ISR); frontend and base rules present |
| FAILED | Next.js-specific rules absent; output indistinguishable from a generic React SPA |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-CMP-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/full-nextjs.md`, `output/claude.md`
3. Interview answers:
   - Project name: StorefrontApp
   - Language: TypeScript
   - Rendering strategy: App Router with Server Components
   - Database: Prisma + PostgreSQL
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists Next.js, React, TypeScript, Prisma
2. Assert App Router conventions present (no `pages/` directory references)
3. Assert Server Components vs Client Components distinction documented
4. Assert Route Handlers referenced for API endpoints
5. Assert ISR or SSG caching strategy referenced
6. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-OUT-09-001A`, `SAIT-E2E-OUT-11-001A`