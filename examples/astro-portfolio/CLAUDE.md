# Maria Chen — Portfolio

Personal portfolio and blog for a product designer. Showcases selected work,
writing, and contact information.

---

## Project identity

- **Name**: maria-chen-portfolio
- **Owner**: Maria Chen
- **URL**: mariachen.design
- **Deployment**: GitHub Pages via GitHub Actions on push to `main`
- **Stack source**: `stack/static-site-astro.md`
- **Output format**: `formats/claude.md`

---

## Stack

- Framework: Astro 4 (output: static)
- Interactive components: none — zero client-side JS
- CSS: plain CSS with custom properties — no framework
- Content: JSON files in `src/data/`
- Package manager: npm
- Formatter: Prettier with `prettier-plugin-astro`
- Deployment: GitHub Actions → GitHub Pages

---

## Architecture

```
src/
  components/
    layout/
      BaseLayout.astro      # <html>, <head>, global styles, footer
      Header.astro
      Footer.astro
    ui/
      ProjectCard.astro
      PostCard.astro
      Tag.astro
  pages/
    index.astro             # Home — hero, featured work, about snippet
    work/
      index.astro           # All projects grid
      [slug].astro          # Individual project case study
    writing/
      index.astro           # All posts list
      [slug].astro          # Individual blog post
    contact.astro
  data/
    site.json               # Nav, hero text, social links, footer copy
    projects.json           # Work items — title, slug, tags, image, description
    posts.json              # Blog posts — title, slug, date, body (Markdown string)
  styles/
    global.css              # CSS custom properties, resets, typography scale
    tokens.css              # Colour, spacing, and font tokens
public/
  images/
    work/                   # Case study images — WebP, named by project slug
    og/                     # Open Graph images — 1200×630 WebP
  fonts/                    # Self-hosted variable fonts
astro.config.mjs
prettier.config.mjs
package.json
README.md
CLAUDE.md
```

---

## Commands

```bash
npm run dev      # develop — hot reload at localhost:4321
npm run build    # compile — production build to dist/
npm run preview  # verify — preview the production build locally
```

---

## Git conventions

- Branch: `main` (source of truth), deploys automatically on push
- Commits: `<type>: <summary>` — types: content, style, fix, chore
- Do not commit `dist/`, `node_modules/`, `.DS_Store`
- Always run `npm run build` locally to verify no build errors before pushing
- Do not commit unoptimised images — compress to WebP before adding to `public/`

---

## Code conventions

### Component rules

- Default to `.astro` components — zero JS shipped unless explicitly opted in
- No client-side JavaScript — this site has no interactive components
- Never use `client:*` directives — all pages are fully static
- One concern per component — layout, UI primitives, and page sections are
  separate files

### Content editing

- All editable text lives in `src/data/` JSON files — never hardcoded in `.astro`
- To add a project: add an entry to `projects.json` and its images to
  `public/images/work/`
- To add a post: add an entry to `posts.json` with the full Markdown body in
  the `body` field

| File | Controls |
|------|----------|
| `src/data/site.json` | Nav links, hero text, footer copy, social links |
| `src/data/projects.json` | Work items — title, slug, tags, thumbnail, body |
| `src/data/posts.json` | Blog posts — title, slug, date, excerpt, body |

### Styling

- All design tokens in `src/styles/tokens.css` as CSS custom properties —
  never use raw colour or spacing values in component styles
- Mobile-first: base styles for mobile, `@media (min-width: 768px)` for tablet,
  `@media (min-width: 1200px)` for desktop
- No Tailwind, no CSS-in-JS, no utility frameworks — plain CSS only
- Typography scale: use `--text-sm`, `--text-base`, `--text-lg`, etc. from tokens
- Animation: a single `IntersectionObserver` in `BaseLayout.astro` handles
  `.reveal` → `.reveal.visible` transitions — do not add per-component scripts

### Assets

- Images in `public/images/` — reference as `/images/filename.webp`
- All images must be WebP format, compressed before committing
- Provide `width` and `height` attributes on every `<img>` to prevent layout
  shift
- OG images in `public/og/` at 1200×630 — one per page

---

## Design

- Palette: off-white `#F9F8F6` background, near-black `#1A1A18` text,
  sage green `#6B8F71` accent
- Typography: "DM Sans" (variable, self-hosted) for body; "DM Serif Display"
  for headings
- Spacing scale: 4px base unit — spacing tokens in `tokens.css`
- Aesthetic: editorial, airy, generous whitespace — no heavy borders or shadows

---

## Brand voice

- Tone: warm, direct, thoughtful — never corporate or salesy
- Write in first person — "I designed", "I led", not "The designer"
- Project descriptions: lead with the problem, then the approach, then the
  outcome — no jargon
- Blog posts: conversational but substantive — aim for clarity over cleverness

---

## Documentation

- Single source of truth: this file + inline comments in complex `.astro` files
- `README.md`: local setup steps and content editing guide only
- No external wiki or docs site