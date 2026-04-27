# Platform — GitHub
[ID: platform-github]
[DEPENDS ON: base/quality-gates.md]

GitHub-specific CI and security integration. Maps quality gate categories
to GitHub Actions workflows and GitHub-native features.

---

## CI
[ID: platform-github-ci]

- Pipeline definitions: `.github/workflows/*.yml`
- Trigger: `on: pull_request` for validation, `on: push` for main branch
- Actions marketplace for reusable steps

---

## SAST
[ID: platform-github-sast]

- **CodeQL** — GitHub-native, free for all repositories (public and private)
- Enable via Settings → Code security → CodeQL analysis
- Runs as a GitHub Actions workflow or as automatic analysis
- Supports: JavaScript, TypeScript, Python, Go, Java, C/C++, C#, Ruby
- Stack-specific SAST supplements (Bandit, govulncheck) run as CI steps

---

## Secret detection
[ID: platform-github-secrets]

- **GitHub push protection** — native, blocks pushes containing known
  secret patterns; enable via Settings → Code security
- **gitleaks** — `gitleaks/gitleaks-action` in CI for additional coverage
- Both SHOULD be enabled — push protection catches on push, gitleaks
  catches in PR validation

---

## Quality gate integration
[ID: platform-github-gates]

| Category | Tool / Integration |
|----------|--------------------|
| SAST | CodeQL (GitHub-native) |
| SAST (Python) | + Bandit (CI step) |
| SAST (Go) | + govulncheck (CI step) |
| Secret detection | GitHub push protection + gitleaks action |
| Site quality | `treosh/lighthouse-ci-action` |
| Link checking | `lycheeverse/lychee-action` |
| All lint/format/type/test | Language-specific CLI in CI steps |
