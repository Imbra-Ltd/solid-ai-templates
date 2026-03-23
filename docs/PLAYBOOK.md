# Playbook

Operational reference for common tasks. Each section is a self-contained
procedure. See `CLAUDE.md` for authoring rules and `SPEC.md` for the
composition model.

---

## Add a new stack template

1. Identify the parent template(s) — check `manifest.yaml` for the closest
   existing stack and trace its `depends_on` chain
2. Create `stack/<prefix>-<name>.md`:
   - First line: `# Stack — <Full Name>`
   - Second line: `[DEPENDS ON: <parent1>, <parent2>, ...]`
   - One section per concern, each tagged `[ID: <name>]`
   - Use `[EXTEND: <id>]` to add rules on top of a parent section
   - Use `[OVERRIDE: <id>]` to replace a parent section entirely
3. Register in `manifest.yaml`:
   ```yaml
   - id: stack-<name>
     file: stack/<prefix>-<name>.md
     depends_on:
       - <parent-id>
   ```
4. Add to the stack list in `SPEC.md` (alphabetical within category)
5. Add a row to the stacks table in `README.md`
6. Add an entry to `ROADMAP.md` under the current phase
7. Add to `CONCEPTS.md` if the stack introduces new concepts
8. Validate: attach `INTERVIEW.md` + new stack to an agent and confirm output

---

## Add a new base or layer template

1. Create the file in the correct layer directory:
   - `base/<name>.md` — cross-cutting, applies to all projects
   - `backend/<name>.md` — backend services only
   - `frontend/<name>.md` — frontend/UI projects only
2. Tag the file root with `[ID: <layer>-<name>]`
3. Tag every section with a unique `[ID: <layer>-<name>-<section>]`
4. Register in `manifest.yaml` under the correct layer key:
   ```yaml
   - id: <layer>-<name>
     file: <layer>/<name>.md
   ```
5. Update `SPEC.md` — add to the directory listing for the relevant layer
6. Add `backend/<name>.md` (or frontend/) references in dependent stack
   `[DEPENDS ON: ...]` headers as appropriate
7. Update `ROADMAP.md`

---

## Rename a template file

1. `git mv <old-path> <new-path>`
2. Update every `[DEPENDS ON: ...]` header that references the old path
3. Update `manifest.yaml` — change the `file:` field for the entry
4. Update `SPEC.md`, `README.md`, `ROADMAP.md`, `CONCEPTS.md`, `INTERVIEW.md`
   — search for the old filename and replace
5. Update any `examples/` files that reference the old path
6. Verify with `git status` that no old references remain

---

## Rename a section ID

1. Change `[ID: <old>]` to `[ID: <new>]` in the source template
2. Search all template files for `[EXTEND: <old>]` and `[OVERRIDE: <old>]`
   — update every occurrence
3. Update `manifest.yaml` if the ID is referenced in `depends_on` lists
4. Update `CONCEPTS.md` if the concept is indexed there

---

## Generate a context file for a project

1. Open your agent (Claude Code recommended)
2. Attach two files:
   - `INTERVIEW.md`
   - The relevant stack template (e.g. `stack/python-flask.md`)
3. For full-stack projects, attach additional layer templates if needed
   (e.g. `backend/auth.md`)
4. Ask the agent to generate the output:
   ```
   Generate a CLAUDE.md for this project using output/claude.md format.
   ```
5. Review the output — check that base rules and stack-specific rules are
   both present and consistent
6. Place the generated file at the project root as `CLAUDE.md`

---

## Validate a template change

1. **Smoke check**: run the automated structural checks — no agent required:
   ```bash
   py tests/run_smoke.py
   ```
   This verifies all `[DEPENDS ON: ...]` paths, unique IDs, `[EXTEND: ...]` /
   `[OVERRIDE: ...]` references, and `manifest.yaml` consistency in one pass.
2. **Agent check**: attach `INTERVIEW.md` + the changed template to an agent
   and confirm the generated output is coherent and complete; or run the
   relevant E2E test if one exists:
   ```bash
   py tests/run_e2e.py STK-01   # example — replace with the relevant ID
   ```
   Reports are written to `tests/reports/` after every run.

---

## Run the test suite

```bash
py tests/run_smoke.py              # 7 structural checks — seconds
py tests/run_e2e.py                # 30 agent tests — ~1-2 hours
py tests/run_e2e.py STK-01 FMT-01  # specific tests only
py tests/run_e2e.py --dry-run      # build prompts, skip agent calls
```

See `tests/CODIFICATION.md` for the ID scheme and `tests/INDEX.md` for the
full list of specs. Requires `py -m pip install pyyaml` for the manifest
check.

---

## Submit a pull request

1. Ensure you are on a feature branch — never commit to `main` directly
2. Run the validation steps above for every changed template
3. Update all affected documents (`SPEC.md`, `README.md`, `ROADMAP.md`,
   `manifest.yaml`, `CONCEPTS.md`) before committing
4. Commit with a conventional message:
   ```
   feat(stack): add python-celery-worker template
   docs(spec): update backend layer listing
   ```
5. Push and open a PR — one concern per PR
6. After merge: delete the branch and pull `main`

---

## Release a new version

1. Create a release branch: `git checkout -b chore/release-vA.B.C`
2. Update `ROADMAP.md` — mark the new phase complete
3. Commit: `git commit --allow-empty -m "chore: release vA.B.C"`
4. Push, open PR, merge
5. Tag on `main`: `git tag vA.B.C && git push origin vA.B.C`