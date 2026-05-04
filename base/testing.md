# Base — Testing

[ID: base-testing]

## Patterns

- See `base/testing-patterns.md` for reusable test patterns:
  factory, AAA, builder, parameterized, fixtures, mock boundary,
  snapshot, contract testing

## Taxonomy

Test types are classified by the **boundary crossed during execution** — not by
who runs them, what tools are used, or what assets drive the test content.

| Type            | Boundary crossed                     | Primary focus                                   |
| --------------- | ------------------------------------ | ----------------------------------------------- |
| **Unit**        | None — single component in isolation | Correctness of individual functions and classes |
| **Integration** | Process or component boundary        | Behaviour and interaction across components     |
| **System**      | System boundary                      | End-to-end behaviour from a user perspective    |
| **Regression**  | Any — reuses existing tests          | Protection against unintended change            |
| **Exploratory** | Any — unscripted                     | Discovery of unexpected behaviour               |

---

## Unit tests

Unit tests verify the correctness of individual functions and classes in
isolation. Dependencies MUST be replaced with mocks or stubs. The primary
driver is TDD — tests are written alongside or before the code.

- MUST cover all happy paths defined by functional requirements
- MUST achieve 90% coverage of new code before merging
- SHOULD cover negative scenarios and edge cases
- The total codebase SHOULD maintain 80% unit test coverage — see
  `base/quality-gates.md` for the coverage policy (80% for new projects,
  warn-only for legacy)
- Coverage MUST NOT regress between releases
- MUST be runnable from CI without human intervention
- Names are not part of any external report or traceability system — they
  SHOULD be chosen freely, provided the name alone communicates the unit under
  test, the input condition, and the expected outcome; each stack template
  defines its own naming convention

---

## Integration tests

Integration tests verify behaviour and interactions across a process or
component boundary using real dependencies (database, message queue, filesystem,
communication partner). Mocks MUST NOT substitute the dependency being
integrated — they MAY be used for unrelated dependencies outside the scope
of the test.

Configuration MAY be sourced from the product manual when the integration
requires a formally defined input (e.g. a communication configuration packet).
This does not change the classification — the boundary crossed determines the
type, not the asset used.

- MUST verify the primary interaction path between the integrated components
- SHOULD cover fault scenarios — dependency unavailable, malformed response,
  timeout, boundary violations
- SHOULD cover cases where a behaviour is only valid under specific conditions
- MUST NOT rely on shared mutable state between test runs
- Names MUST follow the codification scheme defined in the Imbra knowledge
  repository under `standards/` — the scheme provides a structured format
  that enables filtering, traceability, and maintenance across projects

---

## System tests

System tests verify the complete product against its documented requirements
from a user perspective, crossing the system boundary (interacting with
external systems, users, or interfaces).

- MUST be driven by the product manual or system specification
- MUST cover the primary user scenarios defined in the requirements
- SHOULD cover fault and degraded-mode scenarios at the system level
- MUST be executed in an environment representative of production

### E2E tests (subset of system)

E2E tests are automated system tests that simulate complete user journeys
through the full product stack.

- MUST cover the critical user journeys defined in the product requirements
- SHOULD cover non-happy paths and system-level edge cases
- MAY provide data-agnostic scenarios to reduce environment coupling

### Acceptance tests (subset of system)

Acceptance tests are always executed manually, typically by the QA department
or the customer, to determine whether the product satisfies its acceptance
criteria.

- MUST be executed in the target environment with production-representative
  configuration
- MUST be driven by documented acceptance criteria — not improvised
- Automated tests MAY support acceptance testing but MUST NOT replace manual
  sign-off

---

## Regression tests

Regression tests protect against unintended change by re-executing a defined
subset of existing tests after a modification. They reuse unit, integration,
and system tests — they are not a separate test type.

Regression suites are divided by scope and execution time:

| Variant   | Scope               | Trigger             | Target duration |
| --------- | ------------------- | ------------------- | --------------- |
| **Smoke** | Critical paths only | Every commit        | < 15 minutes    |
| **Quick** | Core functionality  | Every merge request | < 60 minutes    |
| **Full**  | Complete suite      | Release candidate   | Unrestricted    |

- Smoke and Quick regression MUST be fully automated
- Full regression SHOULD be fully automated; manual steps MUST be documented
- A regression failure MUST trigger an investigation:
  1. Review the test logic first — if incorrect, refactor the test
  2. If the test logic is correct, investigate the code under test

---

## Exploratory tests

Exploratory testing is unscripted, experience-driven investigation with no
predefined expected outcome. It is not part of any regression suite.

- MAY be triggered by a discovered bug, a release candidate, or intuition
- Findings that reveal a defect SHOULD result in a new regression test to
  prevent recurrence
- Results SHOULD be documented informally (session notes, bug reports)

---

## General rules

- Code MUST be designed for testability from the start — see the
  Testability section in `base/quality.md` for architectural patterns
  (pure functions, boundary architecture, SOLID, design patterns)
- Test behaviour, not implementation details
- Each test MUST be independent — no shared mutable state between tests
- A failing test MUST trigger an investigation before any other action —
  never suppress or skip a failing test without a documented reason
- Tests are code and MUST be treated as such — they MAY contain bugs; when
  a test behaves unexpectedly, the test logic MUST be verified before
  concluding the code under test is at fault
- Integration tests MUST use real dependencies for the boundary under test —
  not hand-written mocks
- Test factory defaults for optional fields MUST be `undefined` (omitted),
  not convenient values like `false` or `0` — explicit defaults mask bugs
  that only appear with real data shapes
- Data validation tests SHOULD flag boolean fields where one branch (`true`
  or `false`) has zero occurrences across the dataset — this is a data
  smell that can silently break sorting, filtering, and UI logic
