# Backend — Server-Side Templating
[ID: backend-templating]

Rules for server-rendered HTML applications. Covers template organisation,
escaping, partials, layouts, caching, and testing. Applies to any backend
language or framework that renders HTML on the server.

See `stack/htmx.md` for hypermedia-driven (HTMX) conventions.
See `backend/api.md` for protocol selection guidance.

---

## When to use server-side templating
[ID: backend-templating-when]

- Choose server-side rendering when the UI is document-oriented, content-heavy,
  or primarily consumed by users who do not need rich client-side interactivity
- Prefer server-side rendering for SEO-critical pages, admin interfaces,
  dashboards, and form-heavy workflows
- Do NOT use server-side templating when the UI requires real-time updates,
  complex client state, or offline capability — use a SPA or PWA instead
- HTMX and Alpine.js can cover most interactivity needs without a full SPA;
  evaluate before reaching for React or Vue

---

## Template organisation
[ID: backend-templating-organisation]

```
templates/
  base.html            # root layout — defines blocks: head, body, scripts
  components/          # reusable partials — one file per component
    nav.html
    footer.html
    flash.html
  [feature]/           # feature-specific templates
    list.html
    detail.html
    form.html
```

- One template file per view — do not mix unrelated views in one file
- Extract repeated markup into partials — never copy-paste template fragments
- Layouts use block/slot inheritance — child templates override defined blocks
- Keep template logic minimal: conditionals and loops only — no business logic
- Business logic belongs in the view/handler, not the template

---

## Escaping and security
[ID: backend-templating-security]

- Auto-escaping MUST be enabled for all HTML templates — never disable it
- Never render user-supplied content as raw HTML — use the template engine's
  safe/mark-safe mechanism only for content you control entirely
- Set `Content-Security-Policy` headers — restrict inline scripts and styles
- Avoid `eval`, `innerHTML`, or `dangerouslySetInnerHTML` in any JS embedded
  in server-rendered pages
- CSRF protection MUST be enabled on all state-changing form submissions —
  use the framework's built-in CSRF middleware

---

## Partials and components
[ID: backend-templating-partials]

- Partials are self-contained — they do not depend on variables set outside
  their own render context; pass all required data explicitly
- Name partials by what they render, not where they are used:
  `user-card.html` not `sidebar-user.html`
- HTMX partial responses return the partial template only — not the full page
  layout; the layout is never re-rendered for fragment swaps

---

## Template caching
[ID: backend-templating-caching]

- Cache compiled templates in production — never recompile on every request
- Fragment caching: cache expensive partials (e.g. navigation trees, aggregated
  stats) with an explicit TTL; invalidate on relevant data changes
- Do NOT cache user-specific content in a shared cache — vary cache keys by
  user identity where personalisation is present

---

## Forms
[ID: backend-templating-forms]

- Every form MUST include a CSRF token
- Render validation errors inline, adjacent to the relevant field —
  never display a generic "form invalid" message without field context
- Re-render the form with submitted values on validation failure —
  never redirect to a blank form after a failed POST
- Use `POST` for all state-changing operations — never `GET` for mutations

---

## Testing
[EXTEND: base-testing]

- Test each template renders without error for its happy path
- Test that validation errors are displayed correctly
- Test that CSRF tokens are present on all forms
- Do not assert exact HTML — assert on meaningful content (headings,
  field labels, error messages) to avoid brittle tests tied to markup