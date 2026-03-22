# Frontend — Quality Attributes
[ID: frontend-quality]

## Design patterns

Prefer these patterns for frontend concerns:

- **Container / Presentational** — separate data-fetching and state logic
  (container) from rendering (presentational); presentational components
  receive only props, have no side effects, and are easy to test in isolation
- **Custom Hook** — extract reusable stateful logic into a named hook
  (`use[Name]`); hooks are the frontend equivalent of a service or strategy
- **Compound Component** — expose a set of related sub-components that share
  implicit state via context (e.g. `<Tabs>`, `<Tab>`, `<TabPanel>`);
  prefer over deeply nested prop drilling
- **Render Props / Slot** — pass render logic as a prop or slot to invert
  control over what is rendered; use sparingly — prefer custom hooks where possible
- **Observer** — subscribe to external state changes (store, event bus,
  WebSocket) via a single subscription point; unsubscribe on component unmount
- **Facade** — wrap third-party libraries (analytics, maps, payment SDKs)
  behind a thin project-owned interface; never scatter SDK calls across components
- **Optimistic Update** — apply the expected result of a mutation immediately
  in the UI and roll back on failure; document the rollback path

Avoid:
- **Mediator / Event Bus** between components — use shared state or lifting
  state up instead; an event bus between components creates invisible coupling

## State management

Choose the right tool for the scope of the state — do not use a global store
for state that is local to a component or a server cache for state that is
never fetched from a server.

| State type | Tool | When to use |
|------------|------|-------------|
| **Local UI state** | `useState`, `useReducer` | Scoped to one component — form inputs, toggles, counters |
| **Shared UI state** | Zustand / Redux Toolkit | Needed by multiple unrelated components — auth session, sidebar open, active filters |
| **Server state** | TanStack Query / SWR | Data fetched from an API — lists, detail views, paginated results |
| **Form state** | React Hook Form / Formik | Complex forms with validation, field arrays, multi-step flows |
| **URL state** | Router search params | Shareable or bookmarkable UI state — filters, pagination, selected tab |

Rules:
- Never duplicate server state in a global store — TanStack Query or SWR is
  the cache; the store holds only client-owned state
- Never put derived state in the store — compute it from existing state with
  a selector or `useMemo`
- Prefer URL state for anything the user should be able to bookmark or share
- Keep global store slices small and focused — one slice per domain concern,
  not one slice for everything

## Linting and formatting
- A linter MUST be configured for all JS/TS code
- Linter and formatter SHOULD run on save in the IDE — never rely on CI
  alone to catch style issues
- No warnings or errors MUST appear in the browser console or test output
  before a PR is merged — start every review on a clean slate
- Lint error count SHOULD go down over time — never increase it

## CSS
- All CSS in a single stylesheet — no inline styles except dynamic/computed values
- No hardcoded colour or spacing values — always use CSS custom properties
  from `:root` or design tokens
- Consistent naming convention (e.g. BEM-like `.component-element`)
- Maximum line length: 80 characters (exempt: prose strings, third-party URLs)

## Performance
- Preload critical above-the-fold assets
- Keep client-side JS minimal — every dependency adds to bundle size
- Avoid unnecessary dependencies
- Defer non-critical scripts
- Monitor Core Web Vitals (LCP, CLS, INP) — treat regressions as bugs

## SEO & analytics
- `robots.txt`, Open Graph, and Twitter Card meta tags required
- Canonical URLs required
- Privacy-friendly analytics only — no consent banner required
- No third-party tracking scripts without explicit user consent