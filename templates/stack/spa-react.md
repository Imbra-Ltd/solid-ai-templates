# Stack — React Single-Page Application
[DEPENDS ON: templates/base/core/git.md, templates/base/core/docs.md, templates/base/core/quality.md, templates/base/language/typescript.md, templates/frontend/ux.md, templates/frontend/quality.md]

A client-side React application with TypeScript. Covers component model,
state management, routing, API integration, and tooling.

---

## Stack
[ID: react-spa-stack]

- Language: TypeScript (strict mode)
- Framework: React 18+
- Bundler: [Vite / Create React App / Next.js]
- Routing: [React Router v6 / TanStack Router]
- State: [Zustand / Redux Toolkit / React Query + local state]
- Styling: [CSS Modules / Tailwind / plain CSS]
- HTTP client: [fetch / axios / TanStack Query]
- Test runner: Vitest + React Testing Library
- Package manager: [npm / pnpm / yarn]
- Deployment: [Vercel / Netlify / GitHub Pages / Docker]

---

## Project structure
[ID: react-spa-structure]

```
src/
  components/
    [Feature]/
      [Feature].tsx
      [Feature].test.tsx
      [Feature].module.css   # if using CSS Modules
  pages/                     # or routes/ — one file per route
  hooks/                     # custom hooks (use[Name].ts)
  services/                  # API calls (no business logic in components)
  store/                     # global state slices
  types/                     # shared TypeScript types and interfaces
  utils/                     # pure utility functions
  App.tsx
  main.tsx
public/
tsconfig.json
vite.config.ts               # or equivalent
package.json
README.md
CLAUDE.md
```

---

## TypeScript conventions
[ID: react-spa-typescript]

- Follow the **TypeScript ESLint** recommended ruleset
  (`@typescript-eslint/recommended`) — enforced by ESLint; do not suppress
  lint errors without a documented reason
- **Prettier** owns all formatting decisions — no style discussions in code
  review; configure once and commit the config
- `strict: true` in `tsconfig.json` — no exceptions
- No `any` — use `unknown` and narrow, or define a proper type
- Explicit return types on all non-trivial functions
- Use `interface` for object shapes, `type` for unions and aliases
- Import types with `import type { ... }` to keep runtime bundle clean
- Enums avoided — use `as const` objects or string literal unions instead

---

## Component conventions
[ID: react-spa-components]

- One component per file — filename matches component name (PascalCase)
- Functional components only — no class components
- Props typed with an explicit `interface` or `type` in the same file
- No prop drilling beyond two levels — lift state or use context/store
- Extract reusable logic into custom hooks (`use[Name].ts` in `hooks/`)
- Keep components small: if a component exceeds ~150 lines, split it

---

## State management
[ID: react-spa-state]

- Local state (`useState`, `useReducer`) for component-scoped concerns
- Shared/global state in the chosen store (Zustand slice or Redux slice)
- Server state (fetched data) managed by React Query / TanStack Query —
  never duplicate server state in the global store
- No direct DOM manipulation — all state flows through React

---

## API integration
[ID: react-spa-api]

- All API calls in `src/services/` — never inline `fetch` in components
- Return typed response objects — no untyped `any` from API boundaries
- Handle loading, error, and empty states explicitly in every data-dependent view
- Never store tokens in `localStorage` — prefer `httpOnly` cookies or memory

---

## Styling
[ID: react-spa-styling]

- No inline styles except for dynamic/computed values
- No hardcoded colour or spacing values — use CSS custom properties or
  design tokens from the chosen system
- Responsive styles follow a mobile-first approach (per `templates/frontend/ux.md`)
- Global styles in `src/index.css` only; component styles co-located

---

## Testing
[EXTEND: base-testing]

- React Testing Library for component tests — test behaviour, not implementation
- No `getByTestId` as a first resort — prefer accessible queries
  (`getByRole`, `getByLabelText`, `getByText`)
- Vitest for component tests on utils, hooks, and services
- Mock API calls at the network boundary (`msw`) — not inside components
- Component test naming: Given/When/Then
  e.g. `given a logged-out user, when they submit the form, then an error is shown`
- System tests MUST cover critical user journeys (login, checkout, key flows)
- System tests SHOULD use Playwright or Cypress — colocated in `tests/system/`
  at project root
- Run before every commit: `npm test && tsc --noEmit`

---

## Accessibility
[EXTEND: frontend-ux]

- All interactive elements must be keyboard-accessible
- Use semantic HTML — prefer `<button>` over `<div onClick>`
- Every form input has an associated `<label>`
- Modals and dialogs trap focus and restore it on close
- Test with a screen reader before shipping new interactive components

---

## Git conventions
[EXTEND: base-git]

- Do not commit `node_modules/`, `dist/`, `.env`, `.env.local`
- Lock file (`package-lock.json` / `pnpm-lock.yaml`) is committed — do not delete it
- Always run `npm test && tsc --noEmit` before committing

---

## Commands
```
npm run dev       # develop — hot reload
npm run build     # production build
npm run preview   # preview production build locally
npm test          # run tests (watch mode)
tsc --noEmit      # type check without emitting files
```