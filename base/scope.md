# Base — Scope Guard
[ID: base-scope]

## Purpose
Prevent scope creep during agent-assisted work sessions. Agents tend to
agree with expansions rather than pushing back, leading to sessions that
start with one task and end with five unrelated changes — none fully
finished.

## Session startup
Before starting any work, the agent MUST:
1. Read all documents referenced in the project's CLAUDE.md (e.g.
   `docs/solid-ai-templates/base/git.md`, `base/docs.md`, etc.)
2. These contain binding conventions that CLAUDE.md inherits — do not
   proceed until you have read and understood them
3. Confirm the scope with the user before making changes
4. If the task is ambiguous, ask: "What is the specific deliverable for
   this session?"
5. Write down the agreed scope — refer back to it when the session
   drifts

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

## End of session audit
Before ending a session, verify all of the following:
1. **Dev journal** — add a session entry to `docs/dev-journal.md`
   (date, tool, key changes, PRs merged, issues closed/created, open issues)
2. **CLAUDE.md** — update if project structure or conventions changed
3. **README.md** — update if public-facing info (setup, links, structure) changed
4. **ONBOARDING.md** — update `docs/ONBOARDING.md` if prerequisites,
   setup steps, or project structure changed
5. **PLAYBOOK.md** — update `docs/PLAYBOOK.md` if operational
   workflows or file paths changed
6. **ADRs** — record any decisions made during the session in
   `docs/decisions/`
7. **Open issues** — close resolved issues, create issues for remaining work
8. **Submodules** — check if upstream submodules need updates
   (`git submodule update --remote`); commit the pointer bump if needed
9. **Template feedback** — flag any conventions discovered or changed
   during the session that should be contributed back to
   solid-ai-templates
10. **Flag gaps** — if any of the above cannot be completed, flag it
    to the user before closing
