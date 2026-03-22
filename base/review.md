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

1. **Security exposure** — anything that could be exploited, any credential
   or license problem
2. **Functional correctness** — paths that produce wrong results, unhandled
   failures, or race conditions
3. **Clarity** — obscure names, deep nesting, high cognitive complexity,
   boolean flag parameters
4. **Convention compliance** — code that deviates from agreed project patterns

## MUST checklist
- [ ] No credentials, tokens, or sensitive values appear anywhere in the
  committed files
- [ ] Every failure path is explicitly handled — no silent catches, no
  swallowed exceptions
- [ ] Any new dependency carries a license compatible with the project policy
- [ ] Significant logic or architectural decisions are captured in documentation
- [ ] Existing documentation reflects the state of the code after this change

## SHOULD checklist
- [ ] Non-trivial functions have a unit test for each relevant variant
- [ ] Code coverage does not decrease
- [ ] Lint errors/warnings do not increase
- [ ] Third-party dependencies are necessary, understood, and well-maintained
- [ ] Code is simple — no new abstraction without two or more call sites,
  no new dependency without a documented reason

## Deviations
- Deviating from a SHOULD rule requires a written explanation in the pull
  request
- Deviating from a MUST rule requires explicit sign-off from a designated
  approver before the change can land