# Base — Scope Guard
[ID: base-scope]

## Purpose
Prevent scope creep during agent-assisted work sessions. Agents tend to
agree with expansions rather than pushing back, leading to sessions that
start with one task and end with five unrelated changes — none fully
finished.

## Before starting work
- Confirm the scope with the user before making changes
- If the task is ambiguous, ask: "What is the specific deliverable for
  this session?"
- Write down the agreed scope — refer back to it when the session drifts

## During work
- If a task grows beyond the original scope, flag it explicitly:
  "This is expanding beyond the original task — should I continue or
  finish the current work first?"
- Do not silently absorb new requests into the current work stream
- Finishing and committing the current work SHOULD take priority over
  starting something new

## Default scope boundaries
- One logical unit of work per session (one feature, one chapter, one
  component, one bug fix)
- Changes that support the current unit (tests, docs, formatting) are
  in scope
- Restructuring unrelated code, creating new projects, or adding
  infrastructure is out of scope unless explicitly requested

## When in doubt
- Finish the current task
- Commit the current work
- Then ask whether to start the new task

## Scope expansion protocol
When the user requests something out of scope:
1. Acknowledge the request
2. State what the current scope is
3. Ask: "Should I finish the current work first, or switch to this?"
4. If switching, commit current progress before starting the new task
