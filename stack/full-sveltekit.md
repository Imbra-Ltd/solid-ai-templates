# Stack — SvelteKit Application
[DEPENDS ON: base/git.md, base/docs.md, base/quality.md, frontend/ux.md, frontend/quality.md, stack/spa-svelte.md, backend/config.md, backend/http.md, backend/api.md, backend/auth.md]

Extends the Svelte stack with SvelteKit-specific rules. Covers file-based
routing, server-side rendering, API routes, form actions, and deployment
adapters.

---

## Stack
[ID: sveltekit-stack]

- Language: TypeScript (strict mode)
- Framework: SvelteKit (latest stable)
- Runtime: Svelte 5 (runes)
- Bundler: Vite (built-in)
- Routing: file-based (`src/routes/`)
- State: Svelte runes + stores (per `stack/spa-svelte.md`)
- Styling: [plain CSS / Tailwind / CSS Modules]
- HTTP client: SvelteKit `fetch` (server) / TanStack Query (client)
- Test runner: Vitest + Playwright
- Package manager: [npm / pnpm]
- Adapter: [`@sveltejs/adapter-vercel` / `adapter-node` / `adapter-static`]
- Deployment: [Vercel / Node server / Docker / static host]

---

## Project structure
[ID: sveltekit-structure]

```
src/
  routes/
    +layout.svelte         # root layout — wraps all pages
    +layout.server.ts      # root server layout (session, shared data)
    +page.svelte           # home page
    +page.server.ts        # home page load function
    [section]/
      +page.svelte
      +page.server.ts      # load() — server data fetching
      +server.ts           # API route handlers (GET, POST, etc.)
  lib/
    components/            # shared components (per svelte.md)
    stores/                # shared state
    services/              # server-side data access (db, external APIs)
    utils/                 # pure utilities
    types/                 # shared TypeScript types
  app.html                 # HTML shell
  app.css                  # global styles
static/                    # files served as-is
svelte.config.js
vite.config.ts
tsconfig.json
package.json
README.md
CLAUDE.md
```

---

## Routing conventions
[ID: sveltekit-routing]

- File-based routing under `src/routes/` — directory name = URL segment
- `+page.svelte` renders the page; `+page.server.ts` provides its data via `load()`
- `+layout.svelte` wraps child routes; `+layout.server.ts` provides shared data
- `+server.ts` for pure API endpoints — follow `backend/http.md` conventions
  (correct methods, status codes, RFC 9457 errors)
- `+error.svelte` for custom error pages per route segment

---

## Data loading
[ID: sveltekit-data]

- Server data fetching in `+page.server.ts` `load()` — never in `onMount()`
  for data that should be available on first render
- `load()` returns a plain object — typed via `PageServerLoad` / `LayoutServerLoad`
- Use `$page.data` in components to access loaded data — do not re-fetch
  on the client what was already loaded on the server
- Client-side fetching (TanStack Query) only for data that must update
  without a page navigation (polls, live feeds)
- Streaming: use `Promise` values in `load()` return to stream deferred data
  to the client without blocking the initial render

---

## Form actions
[ID: sveltekit-actions]

- Prefer form actions (`+page.server.ts` `actions`) over API routes for
  form submissions — they work without JavaScript and degrade gracefully
- Validate form data server-side in the action — never trust client input
- Use `fail()` to return validation errors to the form; use `redirect()` on success
- Progressive enhancement via `use:enhance` — do not ship forms that require JS
  to function

---

## API routes
[EXTEND: backend-http]

- `+server.ts` files export named functions: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
- Authenticate every protected handler — check session at the top before
  any business logic
- Delegate to functions in `src/lib/services/` — keep handlers thin
- Return typed `Response` objects using SvelteKit's `json()` and `error()` helpers

---

## Configuration
[EXTEND: backend-config]

- Environment variables via SvelteKit's env modules:
  - `$env/static/private` — server-only, inlined at build time
  - `$env/dynamic/private` — server-only, read at runtime
  - `$env/static/public` — client-safe, `PUBLIC_` prefix required
- Never import a private env module in a `.svelte` file or client-side code —
  SvelteKit will error at build time

---

## TypeScript conventions
[EXTEND: svelte-typescript]

- Use generated types from `.svelte-kit/types/` for `PageData`, `ActionData`,
  `PageServerLoad` — never write these by hand
- Run `svelte-kit sync` to regenerate types after adding routes

---

## Testing
[EXTEND: base-testing]

- Unit tests (Vitest): stores, services, utilities, form action logic
- Component tests (Svelte Testing Library + Vitest): isolated UI components
- System/E2E tests: Playwright — cover full user journeys including form
  submissions and navigation
- Run before every commit: `npm test && tsc --noEmit`

---

## Git conventions
[EXTEND: base-git]

- Do not commit `node_modules/`, `.svelte-kit/`, `build/`, `.env`
- Lock file committed — do not delete it
- Run `npm run build` before a PR to catch adapter and type errors

---

## Commands
```
npm run dev           # develop — hot reload at localhost:5173
npm run build         # production build
npm run preview       # preview production build locally
npm test              # run Vitest tests
npx playwright test   # run E2E tests
tsc --noEmit          # type check
```