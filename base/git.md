# Base — Git Conventions
[ID: base-git]

## Commit messages
- Use conventional commit prefixes:
  `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `style:`, `test:`
- Keep the subject line under 72 characters
- Use the imperative mood: "add feature" not "added feature"

## Branching
- Always work on a branch — never commit directly to `main`
- Exception: documentation-only changes (`docs/`, `README.md`, `CLAUDE.md`)
  may go directly to `main`
- Branch naming: `feat/description`, `fix/description`, `chore/description`,
  `docs/description`

## Pull requests
- PRs should be small and focused — one concern per PR
- Always test locally before committing
- **Before pushing or creating a PR**, check `git status` and list open PRs.
  If the previous PR is closed or merged, create a new branch rather than
  pushing to a stale one.
- **After a PR is merged**, delete both remote and local branch, then pull main:
  ```
  git branch -d <branch>
  git push origin --delete <branch>
  git checkout main && git pull
  ```

## Versioning
- Follows `vA.B.C.D` — A=major, B=minor, C=build, D=hotfix
- No VERSION file — git tags only
- Release process:
  1. `git checkout -b chore/release-vA.B.C.D`
  2. `git commit --allow-empty -m "chore: release vA.B.C.D"`
  3. Push, open PR, merge
  4. `git checkout main && git pull`
  5. `git tag vA.B.C.D && git push origin vA.B.C.D`

## General
- Do not commit build output, secrets, or dependency directories
- Do not commit generated files that can be reproduced by running a build command