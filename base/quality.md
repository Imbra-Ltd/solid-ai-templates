# Base — Quality Attributes
[ID: base-quality]

## Content & architecture
- All editable content in a data directory — never hardcoded in components
- Default to the simplest component type; only reach for heavier abstractions
  when genuinely needed
- No dead code — remove unused components, styles, and data files promptly
- No over-engineering — build the minimum needed for the current requirement

## CSS
- All CSS in a single stylesheet — no inline styles except dynamic/computed values
- No hardcoded colour or spacing values — always use CSS custom properties
  from `:root`
- Consistent naming convention (e.g. BEM-like `.component-element`)
- Maximum line length: 80 characters (exempt: prose strings, third-party URLs)

## Performance
- Preload critical above-the-fold assets
- Keep client-side JS minimal
- Avoid unnecessary dependencies

## SEO & analytics
- `robots.txt`, Open Graph, and Twitter Card meta tags required
- Privacy-friendly analytics only — no consent banner required
- No third-party tracking scripts without explicit user consent

## Security
- Never hardcode secrets, API keys, or credentials in source files
- Validate all user input at system boundaries
- No `eval()`, no `innerHTML` with unsanitised input
- Keep dependencies up to date — review for known vulnerabilities regularly

## Testing
- Write tests for business logic and edge cases
- Do not test implementation details — test behaviour
- Tests must pass before merging to `main`