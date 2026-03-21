# Base — Testing
[ID: base-testing]

## Test pyramid
Execute in this order — each layer builds on the one before:

1. **Unit** — individual functions/methods in isolation
2. **Integration** — multiple modules interacting
3. **Load** — behaviour under concurrent and high-traffic conditions
4. **Regression** — verify existing functionality after every change
5. **Smoke** — quick check of the most critical paths after deployment
6. **Acceptance** — manual verification of changed functionality in the target environment
7. **E2E** — full system from UI to backend in an automated scenario

## Unit tests
- MUST cover all happy paths for functional requirements
- SHOULD cover negative scenarios and edge cases
- MUST cover at least 90% of new code
- SHOULD cover at least 80% of the overall codebase
- Overall coverage MUST NOT decrease over time
- Tests MUST be runnable from CI without human intervention

### Naming
Backend: `UnitOfWork_StateUnderTest_ExpectedBehavior`
```
Sum_NegativeNumberAs1stParam_ExceptionThrown
Sum_SimpleValues_Calculated
```

Frontend: Gherkin syntax (`Given / When / Then`)
```
Given the FAQ page is loaded
  When the user is logged in
    Then it renders all questions in the accordion
```

## Integration tests
- MUST cover the happy path
- SHOULD cover "only" scenarios — cases where behaviour is valid only under
  specific conditions
- SHOULD cover special/recurring issue scenarios

## Load tests
- MUST implement the happy path scenario
- MUST define error tolerance thresholds
- MUST monitor resource consumption (CPU, memory)
- SHOULD monitor for behavioural deviations under load
- SHOULD cover non-happy and edge case scenarios

## Regression tests
- MUST cover the happy case
- SHOULD cover non-happy cases and edge cases
- SHOULD run automatically after every change

## Smoke tests
- MUST cover the happy case
- SHOULD cover the most critical non-happy cases
- Scope is intentionally narrow — fast feedback only

## E2E tests
- MUST cover the happy case scenario
- SHOULD cover non-happy cases and edge cases
- COULD provide data-agnostic testing

## General rules
- Test behaviour, not implementation details
- Do not mock at the wrong boundary — integration tests should use real
  dependencies or contract-verified fakes, not hand-written mocks
- Each test must be independent — no shared mutable state between tests
- A failing test is a bug — treat it with the same priority as a production issue