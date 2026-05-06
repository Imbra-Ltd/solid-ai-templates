# Stack — Vue Single-Page Application
[DEPENDS ON: templates/base/core/git.md, templates/base/core/docs.md, templates/base/core/quality.md, templates/base/core/oop.md, templates/base/language/typescript.md, templates/base/security/security.md, templates/frontend/ux.md, templates/frontend/quality.md]

A client-side Vue application with TypeScript. Covers the Composition API,
component model, state management with Pinia, routing, API integration,
and tooling.

---

## Stack
[ID: vue-stack]

- Language: TypeScript (strict mode)
- Framework: Vue 3 (Composition API)
- Bundler: Vite
- Routing: Vue Router 4
- State: Pinia
- Styling: [CSS Modules / Tailwind / plain CSS]
- HTTP client: [fetch / axios / TanStack Query]
- Test runner: Vitest + Vue Testing Library
- Package manager: [npm / pnpm]
- Deployment: [Vercel / Netlify / Docker]

---

## Project structure
[ID: vue-structure]

```
src/
  components/
    [Feature]/
      [Feature].vue
      [Feature].test.ts
  views/                     # route-level components (one per route)
  composables/               # reusable composition functions (use[Name].ts)
  stores/                    # Pinia store modules
  services/                  # API calls — no business logic in components
  types/                     # shared TypeScript types and interfaces
  utils/                     # pure utility functions
  router/
    index.ts                 # Vue Router configuration
  App.vue
  main.ts
public/
tsconfig.json
vite.config.ts
package.json
README.md
CLAUDE.md
```

---

## TypeScript conventions
[ID: vue-typescript]
[EXTEND: base-typescript]

- Use `defineProps<T>()` and `defineEmits<T>()` for typed component APIs —
  never the options-style `props: {}` object

---

## Component conventions
[ID: vue-components]

- One component per `.vue` file — filename matches component name (PascalCase)
- Composition API with `<script setup>` — no Options API, no class components
- Props typed via `defineProps<{ ... }>()` in the same `<script setup>` block
- No prop drilling beyond two levels — lift state to Pinia or use `provide/inject`
- Extract reusable logic into composables (`use[Name].ts` in `composables/`)
- Keep components small: if a component exceeds ~150 lines, split it

---

## State management (Pinia)
[ID: vue-state]

- One Pinia store per domain — define with `defineStore()`
- Use the Setup Store style (`defineStore('id', () => { ... })`) for
  consistency with the Composition API
- Local state (`ref`, `computed`) for component-scoped concerns
- Server state (fetched data) managed by TanStack Query or a dedicated
  composable — do not duplicate server state in Pinia
- No direct DOM manipulation — all state flows through Vue reactivity

---

## API integration
[ID: vue-api]

- All API calls in `src/services/` — never inline `fetch` in components
- Return typed response objects — no untyped `any` from API boundaries
- Handle loading, error, and empty states explicitly in every data-dependent view
- Never store tokens in `localStorage` — prefer `httpOnly` cookies or memory

---

## Styling
[ID: vue-styling]

- No inline styles except for dynamic/computed values
- No hardcoded colour or spacing values — use CSS custom properties or
  design tokens from the chosen system
- Scoped styles in `.vue` files with `<style scoped>` — prevents unintended
  global style leakage
- Global styles in `src/assets/main.css` only

---

## Testing
[EXTEND: base-testing]

- Vue Testing Library for component tests — test behaviour, not implementation
- Vitest for unit tests on composables, stores, and services
- Mock API calls at the network boundary (`msw`) — not inside components
- Component test naming: Given/When/Then
  e.g. `given a logged-out user, when they submit the form, then an error is shown`
- System tests MUST cover critical user journeys (login, key flows)
- System tests SHOULD use Playwright — colocated in `tests/system/` at project root
- Run before every commit: `npm test && tsc --noEmit`

---

## Accessibility
[EXTEND: frontend-ux]

- All interactive elements must be keyboard-accessible
- Use semantic HTML — prefer `<button>` over `<div @click>`
- Every form input has an associated `<label>`
- Modals and dialogs trap focus and restore it on close

---

## Git conventions
[EXTEND: base-git]

- Do not commit `node_modules/`, `dist/`, `.env`, `.env.local`
- Lock file (`package-lock.json` / `pnpm-lock.yaml`) is committed
- Always run `npm test && tsc --noEmit` before committing

---

## Commands
```
npm run dev       # develop — hot reload
npm run build     # production build
npm run preview   # preview production build locally
npm test          # run tests (Vitest)
tsc --noEmit      # type check without emitting files
```