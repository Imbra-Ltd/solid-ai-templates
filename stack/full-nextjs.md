# Stack — Next.js Application
[DEPENDS ON: base/git.md, base/docs.md, base/quality.md, frontend/ux.md, frontend/quality.md, stack/spa-react.md, backend/config.md, backend/http.md, backend/api.md, backend/auth.md]

Extends the React SPA stack with Next.js-specific rules. Covers the App
Router, Server and Client Components, data fetching, API routes, metadata,
and deployment.

---

## Stack
[ID: nextjs-stack]

- Language: TypeScript (strict mode)
- Framework: Next.js 14+ (App Router)
- React: 18+ (Server Components by default)
- Styling: [Tailwind CSS / CSS Modules / plain CSS]
- State: [Zustand / Jotai / React context — client state only]
- Server state: [TanStack Query (client) / fetch in Server Components]
- Auth: [NextAuth.js / Clerk / custom JWT]
- Package manager: [npm / pnpm]
- Deployment: [Vercel / Docker / self-hosted Node]

---

## Project structure
[ID: nextjs-structure]

```
src/
  app/                       # App Router root
    layout.tsx               # root layout — fonts, providers, metadata
    page.tsx                 # home page
    [route]/
      page.tsx               # route page component
      layout.tsx             # optional nested layout
      loading.tsx            # Suspense boundary fallback
      error.tsx              # error boundary
  api/                       # Route handlers (if not in app/api/)
  components/
    ui/                      # pure, reusable UI components (no data fetching)
    [Feature]/               # feature-specific components
  lib/                       # shared utilities, helpers, constants
  server/                    # server-only code (db, services, auth)
    db.ts
    auth.ts
  hooks/                     # client-side custom hooks only
  types/                     # shared TypeScript types
public/
next.config.ts
tsconfig.json
package.json
README.md
CLAUDE.md
```

---

## Server vs. Client Components
[ID: nextjs-components]

- **Default to Server Components** — they run on the server, have no client
  JS bundle cost, and can access server-only resources directly
- Add `"use client"` only when the component needs:
  - Browser APIs (`window`, `document`, `localStorage`)
  - React hooks (`useState`, `useEffect`, event handlers)
  - Third-party client libraries
- Push `"use client"` as far down the tree as possible — keep parent
  components on the server
- Never import server-only code (db, secrets) into a Client Component —
  use the `server-only` package to enforce the boundary at build time

---

## Data fetching
[ID: nextjs-data]

- **Server Components**: fetch data directly using `async/await` — no
  useEffect, no loading spinners at the route level
- Use `fetch()` with Next.js cache semantics:
  - `cache: 'force-cache'` — static data, revalidated by tag or time
  - `cache: 'no-store'` — always-fresh data (dynamic rendering)
  - `next: { revalidate: N }` — ISR (incremental static regeneration)
- **Client Components**: use TanStack Query or SWR for client-side fetching;
  never use bare `useEffect` + `fetch` for data loading
- Never expose server-only data fetching logic to the client — put it in
  `src/server/` and import from Server Components only
- Use `loading.tsx` files and React Suspense for streaming — do not block
  the entire page on slow data

---

## API routes
[ID: nextjs-api]

- Route handlers live in `app/api/[resource]/route.ts`
- Follow `backend/http.md` conventions: correct HTTP methods, status codes,
  RFC 9457 error format
- Authenticate every protected route handler — check session/token at the
  top of the handler before any business logic
- Do not put database queries in route handlers — delegate to functions in
  `src/server/`
- Return typed responses — use Zod or a schema library to validate input
  and shape output

---

## Metadata and SEO
[ID: nextjs-seo]

- Export `metadata` (static) or `generateMetadata` (dynamic) from every
  `page.tsx` — never leave title or description empty
- Use the Next.js `<Image>` component for all images — automatic optimisation,
  lazy loading, and correct `alt` attributes required
- Use the Next.js `<Link>` component for all internal navigation — never bare
  `<a>` tags for internal links
- `robots.txt` and `sitemap.xml` generated via Next.js route handlers or
  static files in `public/`

---

## Configuration
[EXTEND: backend-config]

- Environment variables in `.env.local` (local dev) and platform env (production)
- `NEXT_PUBLIC_` prefix only for variables the browser must access —
  all other vars are server-only and never shipped to the client bundle
- Validate required env vars at startup using a schema (Zod or equivalent)
  in `src/lib/env.ts` — import this file at the top of `next.config.ts`

---

## TypeScript conventions
[EXTEND: react-spa-typescript]

- Strict mode enforced — `tsconfig.json` inherits the React SPA conventions
- No `any` in Server Components or API routes — these are production code paths
  with no runtime type safety net
- Type all `fetch` responses — use Zod `parse()` at the API boundary, not
  `as SomeType` casts

---

## Testing
[EXTEND: base-testing]

- Unit tests (Vitest): pure utility functions, hooks, schema validators
- Component tests (React Testing Library + Vitest): Client Components only —
  Server Components are tested via integration or E2E
- Integration tests: API route handlers tested with `next/test-utils` or
  direct fetch against a local server
- System/E2E tests: Playwright — cover critical user journeys
  (auth flow, checkout, key forms)
- Component test naming: Given/When/Then (consistent with react-spa.md)
- Run before every commit: `npm run test && tsc --noEmit`

---

## Git conventions
[EXTEND: base-git]

- Do not commit `node_modules/`, `.next/`, `.env.local`, `out/`
- Lock file (`package-lock.json` / `pnpm-lock.yaml`) is committed
- Always run `npm run build` to verify no type or build errors before a PR

---

## Commands
```
npm run dev          # develop — hot reload at localhost:3000
npm run build        # production build (also runs type check)
npm run start        # serve production build locally
npm run test         # run tests (Vitest)
tsc --noEmit         # type check without building
npx playwright test  # run E2E tests
```