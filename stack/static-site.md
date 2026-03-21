# Stack — Static Site
[DEPENDS ON: base/git.md, base/docs.md, base/quality.md, frontend/ux.md, frontend/quality.md]

A static site generated at build time and served as plain HTML, CSS, and
minimal JavaScript. No backend, no database, no login.

---

## Stack
- Framework: [static site generator — Astro, Eleventy, Hugo, Jekyll, etc.]
- Interactive components: [JS framework or plain JS — only where state is needed]
- CSS: [plain CSS / Tailwind / CSS modules]
- Content: [JSON files / CMS / Markdown / hardcoded]
- Deployed via CI/CD on push to `main`

---

## Architecture principle

```
data files  →  components  →  build output (HTML)
    ↑                               ↓
Edit here                    Deployed here
```

- Separation of content and code — editable content lives in a data directory
- Default to static components; only reach for interactive framework when
  client-side state is genuinely required
- One stylesheet — no inline styles except dynamic/computed values

---

## Content structure
[EXTEND: base-docs]

All editable content lives in a data directory as structured files (JSON,
YAML, or Markdown). Never hardcode content that a non-developer might want
to change.

| File | Controls |
|------|----------|
| `[data path]/site.[ext]` | Nav links, hero text, contact links, footer |
| `[data path]/[section].[ext]` | [what it controls] |

---

## Assets
- Images: `public/images/` — reference as `/images/filename.ext`
- Documents: `public/docs/` — reference as `/docs/filename.ext`
- No assets outside `public/` — only files in `public/` are served statically

---

## Pages

| Page     | Path    | Notes             |
|----------|---------|-------------------|
| Homepage | `/`     | All main sections |
| 404      | `/404`  | Custom error page |

---

## Code conventions

- **ESLint** for any JS/TS code — configured in `eslint.config.js`, run on save
- **Prettier** owns all formatting — commit `.prettierrc`; no style debates
  in code review
- If no JS/TS is present in the project, skip ESLint

---

## CSS conventions
[EXTEND: frontend-quality]

- All CSS in a single global stylesheet
- Use CSS custom properties from `:root` for all colours and spacing
- BEM-like naming: `.component-element` (e.g. `.hero-grid`, `.nav-link`)
- No CSS-in-JS, no utility frameworks unless explicitly chosen in stack

---

## Performance
[EXTEND: frontend-quality]

- Preload critical above-the-fold assets (hero image, primary font)
- Static generation by default — no client-side rendering unless necessary
- Defer non-critical scripts

---

## SEO
[EXTEND: frontend-quality]

- `robots.txt` required
- Open Graph and Twitter Card meta tags required
- Canonical URLs required
- Privacy-friendly analytics only (no consent banner required)