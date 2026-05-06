# Stack — Svelte Single-Page Application
[DEPENDS ON: templates/base/core/git.md, templates/base/core/docs.md, templates/base/core/quality.md, templates/base/core/oop.md, templates/base/language/typescript.md, templates/base/security/security.md, templates/frontend/ux.md, templates/frontend/quality.md]

A client-side Svelte application with TypeScript. Svelte compiles components
to vanilla JS at build time — no virtual DOM, minimal runtime overhead.
Covers the runes reactivity model, component conventions, state, routing,
and tooling.

---

## Stack
[ID: svelte-stack]

- Language: TypeScript (strict mode)
- Framework: Svelte 5 (runes)
- Bundler: Vite
- Routing: [SvelteKit routing (if SSR needed) / svelte-routing / TanStack Router]
- State: Svelte stores / runes (`$state`, `$derived`, `$effect`)
- Styling: [plain CSS / Tailwind / CSS Modules]
- HTTP client: [fetch / TanStack Query]
- Test runner: Vitest + Svelte Testing Library
- Package manager: [npm / pnpm]
- Deployment: [Vercel / Netlify / Docker / static host]

---

## Project structure
[ID: svelte-structure]

```
src/
  lib/
    components/
      [Feature]/
        [Feature].svelte
        [Feature].test.ts
    stores/                  # shared state (Svelte stores or runes modules)
    services/                # API calls
    utils/                   # pure utility functions
    types/                   # shared TypeScript types
  routes/                    # route-level components (one per route)
  App.svelte
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
[ID: svelte-typescript]
[EXTEND: base-typescript]

- Type component props explicitly: `let { label, onClick }: { label: string; onClick: () => void } = $props()`

---

## Component conventions
[ID: svelte-components]

- One component per `.svelte` file — filename matches component name (PascalCase)
- Use Svelte 5 runes (`$props()`, `$state()`, `$derived()`, `$effect()`) —
  not the legacy Options API (`export let`, reactive statements)
- Props declared via `$props()` at the top of `<script>`
- No prop drilling beyond two levels — use a store or context
- Keep components small: if a component exceeds ~150 lines, split it
- `$effect()` is for synchronising with external systems only —
  do not use it as a general-purpose watcher for derived values;
  use `$derived()` instead

---

## State management
[ID: svelte-state]

- Component-local state: `$state()` rune — replaces `let` + reactive declarations
- Derived values: `$derived()` — replaces `$:` reactive statements
- Shared state: Svelte writable/readable stores or a `$state` object exported
  from a `.svelte.ts` module
- Server state (fetched data): TanStack Query or a dedicated async store —
  do not duplicate server state in a writable store

---

## API integration
[ID: svelte-api]

- All API calls in `src/lib/services/` — never inline `fetch` in components
- Return typed response objects — no untyped `any` from API boundaries
- Handle loading, error, and empty states explicitly in every data-dependent view
- Never store tokens in `localStorage` — prefer `httpOnly` cookies or memory

---

## Styling
[ID: svelte-styling]

- Styles in `<style>` blocks are scoped by default — use `:global()` sparingly
  and only when a global override is genuinely required
- No inline styles except for dynamic/computed values
- No hardcoded colour or spacing values — use CSS custom properties from `:root`
- Global styles in `src/app.css` only; import once in `App.svelte`

---

## Testing
[EXTEND: base-testing]

- Svelte Testing Library for component tests — test behaviour, not implementation
- Vitest for unit tests on stores, services, and utilities
- Mock API calls at the network boundary (`msw`)
- Component test naming: Given/When/Then
  e.g. `given an empty cart, when the user adds an item, then the count shows 1`
- System tests MUST cover critical user journeys — use Playwright,
  colocated in `tests/system/` at project root
- Run before every commit: `npm test && tsc --noEmit`

---

## Accessibility
[EXTEND: frontend-ux]

- All interactive elements must be keyboard-accessible
- Use semantic HTML — prefer `<button>` over `<div on:click>`
- Every form input has an associated `<label>`
- Svelte's built-in `a11y` warnings are enabled — do not suppress them

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