# Base — Application Security Patterns

[ID: base-security-patterns]
[DEPENDS ON: base/quality.md]

Reusable structural patterns for secure application code. Each
pattern describes a problem, solution structure, when to use it,
and examples.

See `base/devsecops.md` for pipeline security (SAST, SCA, secret
detection) and `base/devsecops-patterns.md` for pipeline security
patterns.

---

## 1. Input validation at boundaries

[ID: security-pattern-input-validation]

**Problem:** User input flows through multiple layers (controller,
service, repository) with validation scattered across each.
Some paths skip validation entirely. Invalid data reaches the
database or external service.

**Solution:** Validate all external input at the system boundary —
the first point where untrusted data enters. Internal code trusts
validated data. No redundant validation in inner layers.

```
[boundary: validate] → [service: trust] → [repository: trust]
         ↓ reject
     400 Bad Request
```

**When to use:**

- Every HTTP endpoint, CLI argument, message consumer, file import
- Any point where data crosses a trust boundary

**Example (TypeScript + Zod):**

```typescript
const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(["admin", "user"]),
});

app.post("/users", (req, res) => {
  const result = CreateUserSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ errors: result.error.issues });
  }
  // result.data is typed and validated — trust it downstream
  userService.create(result.data);
});
```

**Rules:**

- Validate at the boundary, trust internally — do not re-validate
  in service or repository layers
- Use schema validation libraries (Zod, Joi, Pydantic, JSON Schema)
  — never hand-write validation for complex inputs
- Reject invalid input with a clear error — do not silently coerce
  or strip invalid fields
- Allowlist, not blocklist — define what is valid, reject everything
  else

---

## 2. Output encoding

[ID: security-pattern-output-encoding]

**Problem:** Data stored in the database is rendered in HTML, JSON,
or SQL without encoding. An attacker stores `<script>alert(1)</script>`
as a username — it executes in every user's browser (XSS).

**Solution:** Encode output for its context at the point of
rendering. HTML context gets HTML encoding. URL context gets URL
encoding. JavaScript context gets JS encoding. Never encode on
input — store the raw value, encode on output.

```
Store:  <script>alert(1)</script>     (raw in database)
Render: &lt;script&gt;alert(1)&lt;/script&gt;  (HTML-encoded in page)
```

**When to use:**

- Every point where dynamic data is rendered in HTML, URLs,
  JSON, SQL, or shell commands
- Templates, API responses, log messages

**Rules:**

- Encode on output, not on input — input validation rejects bad
  data, output encoding prevents injection
- Use framework-provided encoding — React JSX, Jinja2 autoescape,
  Go `html/template` all encode by default
- Never use `innerHTML`, `set:html`, `dangerouslySetInnerHTML`,
  or `| safe` with user-supplied data
- Context matters — HTML encoding does not prevent URL injection;
  use the right encoding for the right context

---

## 3. Secret injection

[ID: security-pattern-secret-injection]

**Problem:** Secrets (API keys, database passwords, tokens) are
hardcoded in source files, baked into container images, or passed
as build-time environment variables. They end up in version
control, logs, or container layers.

**Solution:** Inject secrets at runtime from a dedicated vault.
The application reads secrets on startup from environment
variables or mounted files — never from source code or images.

```
Build time: no secrets — image is clean
Runtime:    vault → env var / mounted file → application reads
```

**When to use:**

- Every application that uses credentials, tokens, or API keys
- No exceptions

**Example (Kubernetes + Vault):**

```yaml
# Secret injected as env var from Kubernetes Secret
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: app-secrets
        key: database-url
```

**Example (Docker Compose):**

```yaml
services:
  app:
    environment:
      - DATABASE_URL # read from host env or .env file
    # .env file is in .gitignore — never committed
```

**Rules:**

- Secrets MUST NOT appear in source code, Dockerfiles, CI logs,
  or commit history
- Use `.env` files for local development — add to `.gitignore`
- Provide `.env.example` with placeholder values — never real
  secrets
- Rotate secrets regularly — automate rotation where possible
- If a secret is accidentally committed, rotate it immediately —
  removing from git history is not sufficient

---

## 4. CSRF token flow

[ID: security-pattern-csrf]

**Problem:** A malicious site submits a form to your application
using the user's browser session. The server cannot distinguish
between a legitimate form submission and a cross-site forgery.

**Solution:** Generate a unique token per session. Embed it in
every form as a hidden field. Verify the token on every state-
changing request. Reject requests with missing or invalid tokens.

```
Server generates token → stored in session
Page renders token     → hidden field in form
Form submits token     → server verifies against session
Mismatch               → 403 Forbidden
```

**When to use:**

- Every state-changing endpoint (POST, PUT, DELETE) in
  server-rendered applications
- NOT needed for API-only backends using Bearer tokens — the
  token itself prevents CSRF
- NOT needed for SameSite=Strict cookies with no cross-origin
  forms

**Rules:**

- One token per session — do not generate per request unless
  the framework requires it
- Token MUST be unpredictable — use a cryptographic random
  generator
- Verify on all state-changing methods (POST, PUT, PATCH, DELETE)
  — never on GET
- Use the framework's built-in CSRF protection — do not implement
  from scratch
- Double-submit cookie pattern is acceptable for SPAs that cannot
  use server-side sessions

---

## 5. Rate limiting

[ID: security-pattern-rate-limit]

**Problem:** An attacker or misbehaving client sends thousands of
requests per second. Login endpoints are brute-forced. API
endpoints are scraped. The server is overwhelmed.

**Solution:** Limit the number of requests per client per time
window. Return `429 Too Many Requests` with a `Retry-After`
header when the limit is exceeded.

```
Client → [rate limiter] → allowed (under limit)
                        → 429 + Retry-After (over limit)
```

**When to use:**

- All public-facing endpoints
- Authentication endpoints (stricter limits)
- Expensive operations (search, export, report generation)

**Rules:**

- Apply rate limits at the reverse proxy or API gateway — not
  in application code
- Use sliding window or token bucket — fixed windows allow bursts
  at window boundaries
- Different limits for different endpoints: auth (5/min),
  API (100/min), static (1000/min)
- Identify clients by IP, API key, or authenticated user — not
  by session cookie alone
- Return `Retry-After` header — clients need to know when to
  retry
- Log rate limit hits — they may indicate an attack or a client
  bug

---

## 6. Dependency pinning

[ID: security-pattern-dependency-pinning]

**Problem:** A dependency uses a version range (`^1.2.3`). A
compromised or buggy patch release is published. The next
`npm install` or `pip install` pulls the bad version
automatically. Supply chain attack succeeds.

**Solution:** Pin exact versions in the lock file. Commit the lock
file. Review dependency updates explicitly through Dependabot or
Renovate PRs — never auto-install unknown versions.

```
package.json:     "lodash": "^4.17.0"   (range — dangerous alone)
package-lock.json: "lodash": "4.17.21"  (pinned — safe)
```

**When to use:**

- Every project with external dependencies
- No exceptions

**Rules:**

- Commit the lock file (`package-lock.json`, `poetry.lock`,
  `go.sum`, `Cargo.lock`)
- Use `npm ci` (not `npm install`) in CI — respects the lock file
  exactly
- Review Dependabot/Renovate PRs — do not auto-merge major
  updates without reading the changelog
- Pin base images in Dockerfiles: `node:22.1.0-alpine`, not
  `node:latest` or `node:22`
- Audit dependencies regularly: `npm audit`, `pip-audit`,
  `govulncheck`

---

## 7. Principle of least privilege

[ID: security-pattern-least-privilege]

**Problem:** A service account has admin access to the database.
A CI token can push to any branch. A container runs as root.
When one component is compromised, the attacker has full access
to everything.

**Solution:** Grant each component the minimum permissions it
needs to function. Database accounts get access to specific
tables. CI tokens are scoped to specific actions. Containers
run as non-root.

```
Service A → read-only access to orders table
Service B → read-write access to users table
CI token  → push to feature branches only
Container → non-root, read-only filesystem
```

**When to use:**

- Every service account, CI token, API key, IAM role, container,
  and database user
- No exceptions

**Rules:**

- Start with zero permissions and add only what is needed —
  never start with admin and try to restrict
- Separate read and write access — most services need only read
- Use short-lived tokens over long-lived credentials
- Review permissions regularly — remove what is no longer used
- Document what each credential can do and why

---

## 8. Security headers

[ID: security-pattern-headers]

**Problem:** The browser allows scripts from any origin, embeds
the page in frames, and sends credentials with cross-origin
requests. Default browser behavior is permissive — every missing
header is an attack surface.

**Solution:** Set security headers on every HTTP response. The
reverse proxy or framework middleware adds them globally — no
per-endpoint configuration needed.

**Essential headers:**

```
Content-Security-Policy: default-src 'self'; script-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

**When to use:**

- Every web application that serves HTML
- API-only backends benefit from a subset (HSTS, nosniff)

**Rules:**

- Set headers at the reverse proxy or middleware level — not
  per route
- Start with a strict CSP and relax only as needed — document
  every relaxation
- Never use `unsafe-inline` or `unsafe-eval` in CSP without
  a written justification
- Test headers with `securityheaders.com` or `observatory.mozilla.org`
- HSTS MUST be enabled on all production HTTPS sites — prevents
  SSL stripping
