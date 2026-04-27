# AdminFlow

Analytics dashboard for monitoring SaaS subscription metrics and customer health.

---

## Project identity

- **Name**: AdminFlow
- **Owner**: Growth engineering
- **Repo**: github.com/acme/adminflow
- **Deployment**: Vercel (production + preview per PR)
- **Stack source**: `stack/spa-react.md`
- **Output format**: `formats/agents.md`

---

## Stack

- Language: TypeScript (strict mode)
- Framework: React 18
- Bundler: Vite 5
- Routing: TanStack Router
- Server state: TanStack Query v5
- Client state: Zustand
- Styling: Tailwind CSS v3
- HTTP client: TanStack Query + native fetch
- Test runner: Vitest + React Testing Library
- E2E: Playwright
- Package manager: pnpm
- Deployment: Vercel — automatic on merge to `main`

---

## Architecture

```
src/
  components/
    Charts/
      LineChart.tsx
      LineChart.test.tsx
    Filters/
      DateRangePicker.tsx
      DateRangePicker.test.tsx
    UI/               # shared design system components
      Button.tsx
      Badge.tsx
      Table.tsx
  pages/
    Dashboard.tsx     # /
    Customers.tsx     # /customers
    Subscriptions.tsx # /subscriptions
    Settings.tsx      # /settings
  hooks/
    useMetrics.ts
    useCustomers.ts
    useAuth.ts
  services/
    api.ts            # base fetch wrapper, auth headers, error handling
    metrics.ts
    customers.ts
  store/
    authStore.ts      # Zustand — current user, session
    uiStore.ts        # Zustand — sidebar state, active filters
  types/
    api.ts            # API response types
    domain.ts         # Customer, Subscription, Metric shapes
  utils/
    formatters.ts     # currency, date, percentage formatters
    validators.ts
  App.tsx
  main.tsx
e2e/
  dashboard.spec.ts
  customers.spec.ts
tsconfig.json
vite.config.ts
tailwind.config.ts
package.json
README.md
CLAUDE.md
```

---

## Commands

```bash
pnpm dev            # develop — hot reload at localhost:5173
pnpm build          # production build
pnpm preview        # preview production build locally
pnpm test           # run unit tests (watch mode)
pnpm test:run       # run unit tests once (CI)
pnpm e2e            # run Playwright E2E tests
tsc --noEmit        # type check without emitting
pnpm lint           # ESLint check
```

---

## Git conventions

- Branch: `main` (protected), feature branches as `feat/<scope>`
- Commits: `<type>(<scope>): <summary>` — types: feat, fix, chore, style, test
- PRs require one approval + passing CI (lint, type check, tests) before merge
- Do not commit `node_modules/`, `dist/`, `.env`, `.env.local`
- Lock file (`pnpm-lock.yaml`) is committed — do not delete it
- Run `pnpm test:run && tsc --noEmit` before every commit

---

## Code conventions

### TypeScript

- `strict: true` in `tsconfig.json` — no exceptions
- No `any` — use `unknown` and narrow, or define a proper type
- Explicit return types on all non-trivial functions
- `interface` for object shapes, `type` for unions and aliases
- Import types with `import type { ... }` to keep runtime bundle clean
- No enums — use `as const` objects or string literal unions

### Components

- One component per file — filename matches component name (PascalCase)
- Functional components only — no class components
- Props typed with an explicit `interface` or `type` in the same file
- No prop drilling beyond two levels — use Zustand store or TanStack Query
- Extract reusable logic into custom hooks in `src/hooks/`
- Keep components under ~150 lines — split if larger

### State management

- **Server state** (API data): TanStack Query — `useQuery`, `useMutation`
- **Client/global state** (auth, UI): Zustand slices in `src/store/`
- **Local state** (component-scoped): `useState`, `useReducer`
- Never duplicate server state in Zustand — TanStack Query is the cache
- No direct DOM manipulation — all state flows through React

### API integration

- All API calls in `src/services/` — never inline `fetch` in components
- `src/services/api.ts` is the only place that sets auth headers and handles
  401 responses (redirect to login)
- Return typed response objects — no untyped `any` at API boundaries
- Handle loading, error, and empty states explicitly in every data-dependent view
- Tokens stored in memory (Zustand `authStore`) — never in `localStorage`

### Styling

- Tailwind utility classes only — no custom CSS files except `src/index.css`
  for base resets and CSS custom properties
- No inline styles except for dynamic computed values (e.g. chart widths)
- No hardcoded colour or spacing values outside of `tailwind.config.ts`
- Mobile-first: base styles for mobile, `md:` / `lg:` for larger breakpoints

---

## Testing

- React Testing Library for component tests — test behaviour, not implementation
- Prefer accessible queries: `getByRole`, `getByLabelText`, `getByText`
  over `getByTestId`
- Mock API calls at the network boundary with `msw` — not inside components
- Vitest for unit tests on utils, hooks, and services
- Name component tests using Given/When/Then:
  `given an unauthenticated user, when they visit the dashboard, then they are redirected to login`
- E2E tests MUST cover: login, dashboard load, customer search, date filter
- Run before every commit: `pnpm test:run && tsc --noEmit`

---

## Accessibility

- All interactive elements keyboard-accessible
- Semantic HTML — `<button>` not `<div onClick>`, `<nav>` for navigation
- Every form input has an associated `<label>` or `aria-label`
- Charts include a `<title>` and accessible text fallback for screen readers
- Modals trap focus and restore it on close
- WCAG 2.1 AA compliance — colour contrast ratio ≥ 4.5:1 for normal text

---

## Documentation

- Single source of truth: this file + inline JSDoc on exported utilities
- Architecture decisions in `docs/adr/` — numbered Markdown files
- `README.md`: setup steps, env var reference, and test instructions only
- No wiki or external docs — everything lives in the repo