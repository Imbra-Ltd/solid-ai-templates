# Static Site — CLAUDE.md Template

<!--
INSTRUCTIONS FOR CLAUDE
========================
This is an interview-driven template. When a user provides this file,
ask them the questions in each REQUIRED section before generating CLAUDE.md.
For DEFAULTED sections, use the pre-filled values unless the user says otherwise.
Ask all REQUIRED questions first, grouped by section, before writing anything.
-->

---

## SECTION 1 — Project identity [REQUIRED]

<!--
Ask the user:
1. What is the project name?
2. What is it for, and who is it for? (one sentence)
3. Who is the owner? (name, GitHub handle, contact email)
4. Where will it be deployed? (GitHub Pages, Netlify, Vercel, etc.)
5. What is the live URL, if known?
-->

- Name: ???
- Description: ???
- Owner: ???
- GitHub: ???
- Contact: ???
- Deployed to: ??? via GitHub Actions on push to `main`

---

## SECTION 2 — Stack [REQUIRED]

<!--
Ask the user:
1. Which static site framework? (Astro, Eleventy, Hugo, Jekyll, Next.js static, etc.)
2. Is this a purely static site, or does it need server-side rendering?
3. Will any components need client-side JavaScript (toggles, forms, sliders)?
   If yes, which framework — React, Vue, Svelte, or plain JS?
4. CSS approach — plain CSS, Tailwind, CSS modules, or other?
5. Is content driven by JSON files, a CMS, Markdown, or hardcoded?
-->

- Framework: ??? (static site generator)
- Interactive components: ??? (React / Vue / Svelte / plain JS / none)
- CSS: ??? (plain CSS / Tailwind / CSS modules)
- Content: ??? (JSON files / CMS / Markdown / hardcoded)
- Deployed via GitHub Actions on push to `main`

---

## SECTION 3 — Design [REQUIRED]

<!--
Ask the user:
1. How would you describe the visual aesthetic? (e.g. minimal, bold, playful)
2. What is the background colour, or colour scheme?
3. What is the primary accent colour?
4. What fonts are you using? (Google Fonts, self-hosted, system fonts?)
5. Where does all CSS live? (single file, per-component, etc.)
-->

- Aesthetic: ???
- Background: `???`
- Accent: `???`
- Typography: ???
- All CSS lives in `???` — no inline styles except dynamic/computed values
- Responsive breakpoints:
  - Tablet: max-width 1024px
  - Mobile: max-width 768px
  - Small mobile: max-width 480px

---

## SECTION 4 — Brand voice [REQUIRED]

<!--
Ask the user:
1. What is the tagline or brand name?
2. How would you describe the tone? (e.g. direct, friendly, technical, formal)
3. What name should be used in body copy?
-->

- Tagline: "???"
- Tone: ???
- Use "???" in body copy
- No emojis in content, code, or documentation unless explicitly requested

---

## SECTION 5 — Content structure [REQUIRED]

<!--
Ask the user:
1. What sections or pages does the site have?
2. For each section, is the content driven by a data file or hardcoded?
List them as rows in the table below.
-->

All editable content lives in `[data path]/` as [format].

| File | Controls |
|------|----------|
| `???` | Nav links, hero text, contact links, footer |
| `???` | ??? |

---

## SECTION 6 — Pages [REQUIRED]

<!--
Ask the user:
1. What pages does the site have beyond the homepage?
   (e.g. privacy policy, about, 404, blog)
-->

| Page     | Path    | Notes             |
|----------|---------|-------------------|
| Homepage | `/`     | All main sections |
| ???      | `/???/` | ???               |

---

## SECTION 7 — Third-party services [REQUIRED]

<!--
Ask the user:
1. Will the site use any analytics? (Plausible, Google Analytics, etc.)
2. Will there be a contact form? (Formspree, Netlify Forms, etc.)
3. Any other external services? (search indexing, CDN, etc.)
-->

| Service | Purpose | Config |
|---------|---------|--------|
| ???     | ???     | ???    |

---

## SECTION 8 — Assets [DEFAULTED]

<!--
Default asset locations. Ask the user only if they use a different structure.
-->

- Images live in `public/images/` — reference as `/images/filename.ext`
- Documents (PDFs, etc.) live in `public/docs/` — reference as `/docs/filename.ext`
- No assets outside `public/` — static files are served from there only

---

## SECTION 9 — Component architecture [DEFAULTED]

<!--
Default: static components, interactive framework only when JS state is needed.
Ask the user only if they want a different default.
-->

See `README.md` for the full project structure.

**Rule:** default to static components. Only reach for the chosen JS framework
when client-side state is required.

---

## SECTION 10 — Git conventions [DEFAULTED]

<!--
These are pre-filled with sensible defaults. Only ask the user if they want
to deviate.
-->

- Commit messages must use conventional commit prefixes:
  `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `style:`, `test:`
- Always work on a branch — never commit directly to `main`
- Exception: documentation-only changes (`docs/`, `README.md`, `CLAUDE.md`)
  may go directly to `main`
- Branch naming: `feat/description`, `fix/description`, `chore/description`,
  `docs/description`
- PRs should be small and focused — one concern per PR
- Always test locally before committing
- Do not commit build output or `node_modules/`
- **Before pushing or creating a PR**, check `git status` and `gh pr list`
- **After a PR is merged**, delete both remote and local branch, then pull main

---

## SECTION 11 — Versioning [DEFAULTED]

<!--
Default: vA.B.C.D with git tags only, release via PR.
Ask the user only if they want a different scheme.
-->

- Follows `vA.B.C.D` — A=major, B=minor, C=build, D=hotfix
- No VERSION file — git tags only
- Release process:
  1. `git checkout -b chore/release-vA.B.C.D`
  2. `git commit --allow-empty -m "chore: release vA.B.C.D"`
  3. Push, open PR, merge
  4. `git checkout main && git pull`
  5. `git tag vA.B.C.D && git push origin vA.B.C.D`

---

## SECTION 12 — UX principles [DEFAULTED]

<!--
Default UX principles for static sites. Ask the user only if they want
to add or change any.
-->

- Mobile-first — design for small screens first, enhance for larger ones
- Progressive disclosure — show only what the user needs at each step
- No dark patterns — no misleading UI, no forced actions, no hidden costs
- Consistency — same interaction patterns throughout the site
- Performance is UX — slow pages are bad user experience

---

## SECTION 13 — Accessibility [DEFAULTED]

<!--
Default: WCAG 2.1 AA. Ask the user only if they need a different level.
-->

- Target standard: WCAG 2.1 AA
- Minimum text contrast ratio: 4.5:1 (normal text), 3:1 (large text)
- All interactive elements reachable and operable by keyboard
- Focus indicators must be visible at all times
- No content that relies on colour alone to convey meaning
- Images must have descriptive `alt` text; decorative images use `alt=""`

---

## SECTION 14 — Browser support [REQUIRED]

<!--
Ask the user:
1. Which browsers must the site support?
2. Is there a minimum version requirement?
Common answer for public sites: last 2 versions of Chrome, Firefox, Safari, Edge.
-->

- Supported browsers: ???
- Minimum versions: ???
- Progressive enhancement: graceful degradation for unsupported features

---

## SECTION 15 — Quality attributes [DEFAULTED]

<!--
These are non-negotiable defaults. Only ask the user if they want to
add or remove any.
-->

**Content & architecture**
- All editable content in a data directory — never hardcoded in components
- Default to static components; only use interactive framework when client-side
  state is required
- No dead code — remove unused components, CSS rules, and data files promptly

**CSS**
- All CSS in a single stylesheet — no inline styles except dynamic/computed values
- No hardcoded colour or spacing values — always use CSS custom properties from `:root`
- Consistent naming convention (e.g. BEM-like `.component-element`)
- Maximum line length: 80 characters (exempt: prose strings, third-party URLs)

**Accessibility**
- Semantic HTML: correct landmark elements and heading hierarchy
- `aria-label` on all interactive elements (buttons, icon links, social links)
- All `<a>` elements with icon-only or ambiguous text must have a descriptive `aria-label`
- Keyboard navigation: menus must close on Escape and restore focus

**Performance**
- Preload critical above-the-fold assets
- Keep client-side JS minimal — static generation by default

**SEO & analytics**
- `robots.txt`, Open Graph, and Twitter Card meta tags required
- Privacy-friendly analytics only (no consent banner required)

**Documentation**
- `CLAUDE.md` and `README.md` must always reflect the actual codebase
- `docs/ONBOARDING.md` — onboarding guide for new contributors
- `docs/PLAYBOOK.md` — operational reference for common tasks
- `README.md` is the single source of truth for project structure
- No references to non-existent files, components, or services

---

## SECTION 16 — Commands [REQUIRED]

<!--
Ask the user which package manager they use (npm, pnpm, yarn, bun) and
confirm the dev/build/preview commands for their chosen framework.
-->

```
[dev command]      # develop — hot reload
[build command]    # compile — production build
[preview command]  # verify — preview production build locally
```

---

## Documentation rule [DEFAULTED]

Before every commit, update all relevant documentation:
- **`CLAUDE.md`** — update if architecture, stack, design rules, or conventions change
- **`README.md`** — update if project structure, stack, or onboarding steps change
- **`docs/PLAYBOOK.md`** — update if commands, workflow, or release process change
- **`docs/ONBOARDING.md`** — update if the contributor workflow changes