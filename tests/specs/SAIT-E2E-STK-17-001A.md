---
id: SAIT-E2E-STK-17-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567835
title: Full interview produces a correct CLAUDE.md for a Hugo static site project
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
tags: [e2e, output, hugo, static-site]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/static-site-hugo.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing Hugo-specific rules
> alongside frontend layer and base rules

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains Hugo-specific rules (content types, archetypes, shortcodes, taxonomies, Go templates); frontend and base rules present |
| FAILED | Hugo-specific rules absent; output resembles a JavaScript-based static site generator |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/static-site-hugo.md`, `output/claude.md`
3. Interview answers:
   - Project name: DocumentationSite
   - Language: Markdown + Go templates
   - Theme: custom
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists Hugo
2. Assert content type and archetype conventions present (`hugo new --kind`)
3. Assert Go template rules documented (no JavaScript template syntax)
4. Assert shortcode authoring guidelines present
5. Assert taxonomy configuration referenced
6. Assert no npm or Node.js build step assumed
7. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-07-001A`