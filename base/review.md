# Base — Peer Review
[ID: base-review]

## Principle
- All code MUST undergo a peer review before merging
- The reviewer is accountable for what gets merged
- The developer is responsible for the code they write
- Reviews have priority over your own development — a blocked reviewer
  blocks the team

## Priority order
Apply the following order when reviewing, from most to least critical:

1. **Security and compliance** — exploits, credentials in source, license violations
2. **Correctness** — logic errors, edge cases, unhandled errors, race conditions
3. **Readability** — code that is difficult to understand or follow
4. **Guideline adherence** — inconsistencies with project conventions

## MUST checklist
- [ ] No secrets, credentials, or tokens in source code
- [ ] All error paths handled — no unhandled exceptions or silent failures
- [ ] Dependencies have an acceptable license
- [ ] Critical flows are documented
- [ ] Documentation is in sync with the code changes

## SHOULD checklist
- [ ] Non-trivial functions have a unit test for each relevant variant
- [ ] Code coverage does not decrease
- [ ] Lint errors/warnings do not increase
- [ ] Third-party dependencies are necessary, understood, and well-maintained
- [ ] Code is simple — minimal abstraction, minimal dependencies

## Deviations
- If a SHOULD rule is not followed, the reason MUST be documented
  (e.g., as a PR comment)
- If a MUST rule is not followed, it MUST be escalated and explicitly approved
  before merging