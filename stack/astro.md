# Stack — Astro (Static Site)
[DEPENDS ON: base/git.md, base/docs.md, base/quality.md, frontend/ux.md, frontend/quality.md, stack/static-site.md]

Extends the static site stack with Astro-specific rules.

---

## Stack
[OVERRIDE: static-site-stack]

- Framework: Astro (static site generator, output: static / GitHub Pages)
- Interactive components: [React / Vue / Svelte / plain JS / none] — islands only
- CSS: [plain CSS / Tailwind / CSS modules]
- Content: [JSON files in `src/data/` / CMS / Markdown / hardcoded]
- Deployed via GitHub Actions on push to `main`

---

## Component architecture
[OVERRIDE: static-site-architecture]

- Default to `.astro` components — they are static by default, zero JS shipped
- Only reach for the chosen JS framework (React, Vue, Svelte) when client-side
  state is genuinely required
- Interactive components live in `src/components/interactive/`
- See `README.md` for the full project structure

## Astro islands (client directives)
- `client:visible` — below-the-fold components, defers hydration until in view
- `client:load` — above-the-fold components that must be interactive immediately
- `client:only` — avoid unless SSR is enabled; skips server rendering entirely
- Never hydrate a component that does not need interactivity

---

## Content structure
[OVERRIDE: static-site-content]

All editable content lives in `src/data/` as JSON.

| File | Controls |
|------|----------|
| `src/data/site.json` | Nav links, hero text, contact links, footer |
| `src/data/[section].json` | [what it controls] |

Note: `src/content/` is intentionally avoided — Astro reserves that path
for Content Collections.

---

## Assets
[OVERRIDE: static-site-assets]

- Images: `public/images/` — reference as `/images/filename.ext`
- Documents: `public/docs/` — reference as `/docs/filename.ext`
- No assets outside `public/` — Astro only serves static files from there

---

## Reveal animations
- Use a single `IntersectionObserver` script in the base layout for
  `.reveal` → `.reveal.visible` transitions
- Do not add per-component reveal scripts

---

## Code conventions

- **ESLint** with `@typescript-eslint/recommended` for any `.ts` / `.tsx`
  files — configured in `eslint.config.js`, run on save
- **Prettier** owns all formatting — commit `.prettierrc`; no style debates
  in code review
- `.astro` files formatted with the official Prettier Astro plugin

---

## Git conventions
[EXTEND: base-git]

- Do not commit `dist/` or `node_modules/`
- Always test with `npm run dev` before committing

---

## Commands
```
npm run dev      # develop — hot reload at localhost:4321
npm run build    # compile — production build to dist/
npm run preview  # verify — preview the production build locally
```