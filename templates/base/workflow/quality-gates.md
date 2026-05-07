# Base — Quality Gates

[ID: base-quality-gates]
[DEPENDS ON: templates/base/core/quality.md, templates/base/core/git.md, templates/base/core/testing.md, templates/base/core/config.md]

Stack-agnostic quality gate model. Defines the layers, categories,
thresholds, and constraints. Stack templates extend with concrete tools.
Platform templates extend with CI-specific integration.

---

## Shift-left principle

[ID: quality-gates-principle]

The earlier a defect is caught, the cheaper it is to fix. Every check
that can run locally MUST run locally. CI is the backstop, not the first
line of defense.

```
Editor (0s) → Pre-commit (1-5s) → CI (1-5min) → Code review (hours)
```

---

## Three-layer gate model

[ID: quality-gates-layers]

### Layer 1 — Editor (instant feedback)

Runs in the developer's IDE as they type. Zero friction.

- Every project MUST provide config files that enable checks automatically
  when the project is opened in a supported editor
- Checks: lint, format, type check

### Layer 2 — Pre-commit hooks (1–5 seconds)

Runs automatically before every commit. Blocks bad commits locally.

- Every project MUST have pre-commit hooks
- The hook framework is stack-specific (see stack template)
- Checks: lint, format, type check, secret detection, file hygiene
  (trailing whitespace, merge conflict markers, large files)

### Layer 3 — CI (1–5 minutes)

Runs on every PR. The final gate before merge.

- Every project MUST have a CI workflow that runs on PRs
- CI checks MUST be configured as required status checks in branch
  protection — a passing CI run that does not block merge is
  informational, not a gate
- CI MUST duplicate Layer 2 checks — pre-commit hooks can be bypassed
  with `--no-verify`
- CI adds checks that cannot run locally: deep security analysis (SAST),
  test suite, coverage measurement, build verification
- The CI platform is project-specific (see platform template)

---

## Gate categories

[ID: quality-gates-categories]

Every project MUST enforce checks in the following categories. Stack
templates map each category to a concrete tool.

| Category         | Layer 1 | Layer 2 | Layer 3 | Description                                          |
| ---------------- | ------- | ------- | ------- | ---------------------------------------------------- |
| Lint             | MUST    | MUST    | MUST    | Code smells, unused variables, complexity            |
| Format           | MUST    | MUST    | MUST    | Consistent style (indentation, spacing, line length) |
| Type check       | SHOULD  | SHOULD  | MUST    | Type errors before runtime                           |
| Secret detection | —       | MUST    | MUST    | API keys, tokens, passwords                          |
| File hygiene     | —       | MUST    | —       | Trailing whitespace, merge conflicts, large files    |
| Security (SAST)  | —       | —       | MUST    | Static analysis for vulnerabilities                  |
| Tests            | —       | —       | MUST    | Unit and integration tests                           |
| Coverage         | —       | —       | MUST    | Percentage of code exercised by tests                |
| Build            | —       | —       | MUST    | Does it compile / build successfully                 |

Stack templates MAY add additional categories (e.g. link checking, site
quality scoring for web projects, docstring enforcement for Python).

### Recommended lint plugins

- **eslint-plugin-sonarjs** — detects cognitive complexity, duplicate
  branches, identical expressions, and other code smells that standard
  ESLint rules miss; SHOULD be added to any TypeScript/JavaScript project

---

## Thresholds

[ID: quality-gates-thresholds]

| Metric                   | Threshold | Enforcement                  |
| ------------------------ | --------- | ---------------------------- |
| Lint errors              | 0         | CI fails                     |
| Format compliance        | 100%      | CI fails                     |
| Type errors              | 0         | CI fails                     |
| Security (high/critical) | 0         | CI fails                     |
| Secrets detected         | 0         | Pre-commit blocks + CI fails |
| Build                    | Success   | CI fails                     |

### Coverage policy

- **New projects** — 80% from day one; CI fails below threshold
- **Legacy projects** — coverage reported as warning only; CI shows the
  number but never blocks; flip to error when the team has the mandate
  to invest in testing

Stack templates MAY add additional thresholds (e.g. Lighthouse scores).

---

## What NOT to gate

[ID: quality-gates-exclusions]

- **Docstring coverage for non-public functions** — enforcing docs on
  internal helpers creates busywork
- **Cyclomatic complexity thresholds** — too many false positives on
  legitimate complex logic; rely on lint warnings instead
- **100% test coverage** — incentivizes meaningless tests; 80% is the
  practical sweet spot
- **Commit message format** — enforce in PR title via repository settings,
  not per-commit hooks; allow messy WIP commits on feature branches

---

## Tool constraints

[ID: quality-gates-constraints]

- All tools MUST be free for private repositories
- Prefer open-source tools over SaaS — no vendor lock-in
- Prefer tools with CI integration for the project's platform
- Prefer one tool per category — no redundant linters
- Stack templates define the specific tool per category
- Platform templates define the CI integration and SAST tool
