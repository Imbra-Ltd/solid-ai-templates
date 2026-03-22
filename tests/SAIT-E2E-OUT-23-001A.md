---
id: SAIT-E2E-OUT-23-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567837
title: Full interview produces a correct CLAUDE.md for a Rust library project
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
tags: [e2e, output, rust, library, crates-io]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/rust-lib.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing Rust library–specific rules
> without server or deployment sections

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains Rust library rules (crate API design, `pub` surface discipline, rustdoc, semver, `cargo test`); base rules present; no Actix or Axum rules present |
| FAILED | Output includes HTTP server or async runtime rules inappropriate for a library; Rust-specific packaging conventions absent |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/rust-lib.md`, `output/claude.md`
3. Interview answers:
   - Project name: byteparser
   - Language: Rust
   - Distribution: crates.io
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists Rust with no HTTP framework
2. Assert `pub` surface discipline rules present (minimal public API, re-export from lib root)
3. Assert rustdoc conventions documented (every public item documented)
4. Assert semantic versioning rules with Rust edition compatibility noted
5. Assert `cargo test` and `cargo clippy` referenced
6. Assert no Tokio runtime or async HTTP server rules present
7. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-OUT-14-001A`, `SAIT-E2E-OUT-22-001A`