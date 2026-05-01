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
3. Check which branch you are on — if not `main`, ask why before
   proceeding
4. Check `git status` — if uncommitted changes exist, resolve before
   starting new work
5. Confirm the scope with the user before making changes
6. If the task is ambiguous, ask: "What is the specific deliverable for
   this session?"
7. Write down the agreed scope — refer back to it when the session
   drifts
8. Review open issues related to the agreed scope before writing code

## Mandatory startup block
Every project CLAUDE.md MUST include a prominent startup block at the
top of the file listing all referenced template files with an explicit
instruction to read them before the first response. This applies to both
reference mode and hybrid mode.

The startup block MUST:
- Appear before section 1 (Project)
- List every template file the project depends on
- Use imperative language: "You MUST read every file listed below IN
  FULL using the Read tool before you respond"
- State the consequence: "If you respond without reading them, you are
  violating project rules"

This requirement exists because `base/scope.md` says "read all documents
referenced in CLAUDE.md" — but `scope.md` is one of the files that needs
to be read first. The startup block breaks this chicken-and-egg problem
by placing the instruction directly in CLAUDE.md, the one file that is
always loaded into context automatically.

## During work
- If a task grows beyond the original scope, flag it explicitly:
  "This is expanding beyond the original task — should I continue or
  finish the current work first?"
- Do not silently absorb new requests into the current work stream
- Finishing and committing the current work SHOULD take priority over
  starting something new
- Build after every change — do not accumulate multiple changes without
  verifying the build still passes

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
When the user signals end of session ("wrap up", "let's finish",
"end session", "close out", or similar), the agent MUST print the full
checklist below and execute each item sequentially. Mark each item done
(with result) before moving to the next. Do not batch, skip, or
summarize — visible sequential execution prevents missed steps.

1. **Commits and push** — all changes committed and pushed (via PR if
   branch-protected)
2. **Close issues** — close completed issues (verify auto-close worked)
3. **Epic checklists** — update epic checklists if relevant
4. **Dev journal** — add a session entry to `docs/dev-journal.md`
   (date, tool, key changes, PRs merged, issues closed/created)
5. **ADRs** — record any architectural decisions in `docs/decisions/`
6. **CLAUDE.md** — update if project structure or conventions changed
7. **README.md** — update if public-facing info changed
8. **ONBOARDING.md** — update `docs/ONBOARDING.md` if prerequisites,
   setup steps, or project structure changed
9. **PLAYBOOK.md** — update `docs/PLAYBOOK.md` if operational
   workflows or file paths changed
10. **Submodules** — check if upstream submodules need updates
    (`git submodule update --remote`); commit the pointer bump if needed
11. **Template feedback** — flag any conventions discovered or changed
    during the session that should be contributed back to
    solid-ai-templates
12. **Flag gaps** — if any of the above cannot be completed, flag it
    to the user before closing
13. **Summary** — summarize what was done and what's next
