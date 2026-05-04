# Base — Quality Attributes

[ID: base-quality]

## Architecture

- All editable content in a data directory — never hardcoded in components
- Never hardcode derived counts or statistics — compute them from the data
  source; a hardcoded number is a stale number
- Default to the simplest component type; only reach for heavier abstractions
  when genuinely needed
- No dead code — remove unused components, styles, and data files promptly
- No over-engineering — build the minimum needed for the current requirement

## Core principles

- **DRY — Don't Repeat Yourself**: every piece of knowledge must have
  a single, authoritative representation; the third copy is a bug
- **KISS — Keep It Simple**: prefer the simplest solution that works;
  complexity must be justified by a requirement, not by elegance
- **YAGNI — You Aren't Gonna Need It**: do not build for hypothetical
  future requirements; build what is needed now, refactor when the
  need is real

## SOLID principles

Apply SOLID at the class, module, and service level:

- **S — Single Responsibility**: every class or module has exactly one reason
  to change; split anything that serves more than one concern
- **O — Open/Closed**: extend behaviour by adding new code, not by modifying
  existing code; use interfaces, abstract base classes, or composition
- **L — Liskov Substitution**: subtypes must be fully substitutable for their
  base type without altering correctness; never override a method in a way
  that weakens its contract
- **I — Interface Segregation**: prefer many small, focused interfaces over
  one large general-purpose one; callers should not depend on methods they
  do not use
- **D — Dependency Inversion**: depend on abstractions, not concretions;
  inject dependencies rather than instantiating them inside a class

## OOP

- Prefer **composition over inheritance** — inherit only to model a true
  is-a relationship; compose for code reuse
- **Encapsulate** implementation details — expose behaviour through a public
  interface, hide state and implementation
- Design to interfaces (or protocols / abstract base classes), not concrete types
- Keep class hierarchies shallow — more than two levels of inheritance is a
  signal to refactor towards composition

## Design patterns

- Apply established **GoF design patterns** where they fit the problem —
  do not invent ad-hoc solutions for problems that have named solutions
- Favour **behavioural patterns** for algorithm variation:
  Strategy, Command, Observer, Template Method
- Favour **structural patterns** for object composition:
  Adapter, Decorator, Facade, Proxy
- Use **creational patterns** to decouple object creation:
  Factory Method, Abstract Factory, Builder
- Use **Singleton** only for stateless services or infrastructure objects
  (logger, config) — never for mutable shared state
- Name the pattern in code when you use one: a class named `OrderExportStrategy`
  communicates intent; a class named `OrderHelper` does not

## Aspect-Oriented Programming (AOP)

- **Do not use AOP frameworks** — hidden cross-cutting behaviour (method
  interception, bytecode weaving, runtime proxies) makes code hard to read,
  debug, and test
- Implement cross-cutting concerns explicitly:
  - Logging → call the logger directly in the function
  - Auth → explicit middleware or guard in the call chain
  - Transactions → explicit context manager or decorator with visible call site
  - Validation → explicit call at the boundary
- Transparent decorators (a decorator that wraps and clearly delegates) are
  acceptable; opaque interceptors that inject hidden behaviour are not

## Readability

- **Names are the primary documentation** — a name that requires a comment to
  explain is a name that needs to be changed
- Functions and methods: verb or verb phrase (`calculateTotal`, `fetchUser`)
- Classes and modules: noun or noun phrase (`OrderRepository`, `AuthService`)
- Booleans: prefix with `is`, `has`, or `can` (`isActive`, `hasPermission`)
- No single-letter names except loop counters (`i`, `j`) and well-established
  conventions (`err` in Go, `e` in except clauses)
- No abbreviations unless universally understood in the domain (`url`, `id`,
  `http` are fine; `mgr`, `proc`, `obj` are not)
- A function's name must make reading its body unnecessary — if you need to
  read the implementation to understand what a call site does, the function
  needs a better name or needs to be split
- Cognitive complexity ≤ 15 per function — enforced by static analysis
  (SonarQube, Codacy, or equivalent); each nesting level and decision point
  increases the score
- Maximum nesting depth of three levels — use early returns and guard clauses
  to reduce indentation rather than adding else branches
- No boolean flag parameters — they force the caller to read the implementation
  to understand what `true` means; use an enum or two named functions instead
- Avoid negative conditions in `if` statements where possible —
  `if isEnabled` reads better than `if !isDisabled`

## Maintainability

- No circular dependencies between modules or packages — dependency graphs
  must be acyclic; restructure or introduce an interface to break cycles
- Keep the dependency graph shallow — if changing module A requires reading
  modules B, C, and D to understand the impact, the coupling is too high
- Changes to one module's internals must not require changes in unrelated
  modules — if they do, the abstraction boundary is wrong
- Before removing or renaming a public symbol, mark it deprecated with a
  comment referencing the replacement; remove it in a follow-up change
- Magic numbers and magic strings must be named constants — unnamed literals
  scattered across the codebase are a maintenance hazard
- No substantial duplication across sibling modules — if the same code
  appears in two or more places, extract a shared module; the third
  copy is a bug
- Consistent naming across modules — the same concept must use the same
  name everywhere; divergent names for the same thing (e.g. `clearButton`
  vs `clearBtn`) signal missing abstraction
- When the same logic block repeats across three or more modules,
  extract a shared module; short inline repetition (e.g. three similar
  assignments) does not warrant extraction — only substantial
  duplicated logic
- **Fail Fast**: validate inputs at boundaries and throw immediately on
  invalid state; do not propagate bad data through the system
- **Law of Demeter**: a module should only talk to its direct
  dependencies; chaining through objects (`a.b.c.d`) signals missing
  abstraction
- **High Cohesion**: modules that change together should live together;
  a module whose parts serve unrelated concerns should be split

## Testability

Testability is a first-class design concern, not an afterthought. Code that
is hard to test is hard to test because it is poorly designed — fixing the
design fixes the testability.

### Pure functions over side effects

- Business logic SHOULD be implemented as pure functions — same input,
  same output, no side effects (no I/O, no mutation of external state)
- Side effects (database, API, filesystem, DOM) SHOULD be pushed to
  the boundary — thin adapters that call pure logic
- Pure functions are trivially unit-testable with no mocks, stubs, or setup
- A function that mixes logic and side effects is a signal to split it:
  extract the logic into a pure function, keep the side effect in a
  thin wrapper

### Architecture for testability

- Push side effects to the edges:
  `[boundary: I/O] → [pure: logic] → [boundary: I/O]`
- The pure center is unit-testable; the thin boundaries are
  integration-testable
- If a function needs more than two mocks to test, it has too many
  responsibilities — split it

### SOLID enables testability

- **SRP** — a function with one responsibility has one reason to test;
  multiple responsibilities require combinatorial test cases
- **OCP** — new behaviour via extension means existing tests stay green
- **LSP** — subtypes that honour contracts can be tested against the base
  type's tests
- **ISP** — small interfaces mean fewer dependencies to mock
- **DIP** — depend on abstractions, inject dependencies; code that
  instantiates its own dependencies cannot be tested in isolation

### Design patterns and composition

- Design patterns enable testability by enforcing separation of concerns,
  loose coupling, and clear contracts — any correctly applied pattern
  from the Design patterns section improves testability as a side effect
- Prefer composition over inheritance (see OOP section) — composed
  dependencies can be injected and swapped in tests; inherited behaviour
  drags the entire class hierarchy into every test

### Rules

- Design for testability from the start — do not write code first and
  struggle to test later
- If code is hard to test, treat it as a design problem, not a testing
  problem
- See `templates/base/core/testing.md` for test types, coverage targets, and execution
  rules

## Automated enforcement

- Quality conventions in this document are enforced automatically via
  quality gates — see `templates/base/workflow/quality-gates.md` for the three-layer model
  (editor → pre-commit → CI), categories, and thresholds

## Code style

- Encode all source files in UTF-8; content MUST be restricted to ASCII
  characters
- Line endings MUST be LF — CRLF is not acceptable in any committed file
- A linter SHOULD enforce formatting automatically on save; keep manual style
  rules to a minimum
- Prefer self-documenting code — if a comment feels necessary, treat it as a
  signal that the code needs restructuring before the comment is added
- Add comments only where the intent cannot be expressed in code

## Debug code

- No debug statements in committed code: no `print()`, `console.log()`,
  `fmt.Println()`, or equivalent used for debugging
- No hardcoded breakpoints (`debugger`, `pdb.set_trace()`) in committed code
- No commented-out code blocks — delete dead code; version control is the history
- Debug tooling (profilers, REPL helpers, verbose loggers) MUST be
  gated behind a flag or environment variable, never on by default

## Security

- See `templates/base/security/security.md` for comprehensive application security rules
  (input validation, output encoding, injection prevention, auth,
  sessions, TLS, headers, error handling, logging, CORS, uploads)
- See `base/security-patterns.md` for reusable security patterns

## Testing

- Write tests for business logic and edge cases
- Do not test implementation details — test behaviour
- Tests must pass before merging to `main`
- Tests MUST be runnable from CI without human intervention
