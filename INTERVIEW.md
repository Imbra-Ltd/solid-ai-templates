# Interview Template

<!--
INSTRUCTIONS FOR THE AGENT
============================
This file drives the project setup interview. Attach this file together
with the stack/ directory and the relevant formats/ file.

Follow these steps exactly:

1. Ask ALL [REQUIRED] questions below, in order, grouped by section.
2. For [DEFAULTED] sections, present the defaults and ask for deviations only.
3. For [OPTIONAL] sections, ask only if the user has not already answered.
4. After collecting all answers, select the matching stack template from
   stack/ based on the language and framework answers. Confirm your choice:
   "Based on your answers I will use stack/python-fastapi.md — correct?"
5. Load the confirmed stack template and its DEPENDS ON chain.
6. Apply any OVERRIDE answers from Step 6 over the stack rules.
7. Generate the output context file using the confirmed stack + format template.

Ask all REQUIRED questions before generating anything.
Do not generate partial output or ask follow-up questions mid-generation.
-->

## Step 1 — Project identity [REQUIRED]

1. What is the project name?
2. What is it for, and who is it for? (one sentence)
3. Who is the owner? (person, team, or organisation)
4. Where is the repository hosted? (e.g. github.com/acme/my-service)

---

## Step 2 — Technical choices [REQUIRED]

1. What is the primary language and runtime?
   (e.g. Python 3.12, Go 1.22, TypeScript / Node 20, Java 21, Rust stable, Dart 3)
2. What framework or stack are you using, if any?
   (e.g. FastAPI, Flask, Django, Echo, Spring Boot, React, Next.js, SvelteKit,
   NestJS, Express, Flutter, HTMX, Astro, Hugo, Terraform)
3. What is the deployment target?
   - `cloud` — public cloud, managed services, external CA
   - `hybrid` — on-premises + cloud, private CA for internal traffic
   - `offline` — air-gapped, no internet access
4. How is the project distributed or deployed?
   (e.g. Docker image, PyPI package, npm package, crates.io crate, Helm chart, binary)

---

## Step 3 — Data and integrations [REQUIRED]

1. Does the project use a database? If yes, which one and via which library?
   (e.g. PostgreSQL via SQLAlchemy 2, MySQL via GORM, MongoDB via Motor)
2. Does the project use a message broker or event bus?
   (e.g. RabbitMQ via aio-pika, Kafka via confluent-kafka, none)
3. Does the project use a cache?
   (e.g. Redis via redis-py, Memcached, none)
4. Does the project expose or consume an API? If yes, which style?
   (e.g. REST/OpenAPI, gRPC, GraphQL, none)

---

## Step 4 — Auth [REQUIRED]

1. Does the project require authentication or authorisation?
   If yes, which mechanism?
   (e.g. JWT bearer tokens, OAuth 2.0 / OIDC, API keys, session cookies, mTLS, none)

---

## Step 5 — Git conventions [DEFAULTED]

Defaults from `base/git.md`:
- Commit prefixes: `feat`, `fix`, `chore`, `docs`, `refactor`
- Branch naming: `feat/<scope>`, `fix/<scope>`, `chore/<scope>`
- Versioning: semver `vA.B.C` with git tags

Any deviations from these defaults?

---

## Step 6 — Overrides [OPTIONAL]

Are there any rules from the standard stack or base templates that this project
should override? For example:

- Different test runner than the stack default
- Different linter or formatter
- Non-standard branch naming
- Any team-specific conventions not covered above

List each override explicitly. Interview answers always take precedence over
stack template rules.

---

## Step 7 — Stack selection [AGENT]

Based on the answers above, select the matching stack template from stack/:

| If language + framework is... | Use... |
|-------------------------------|--------|
| Python + FastAPI | `stack/python-fastapi.md` |
| Python + Flask | `stack/python-flask.md` |
| Python + Django | `stack/python-django.md` |
| Python + gRPC | `stack/python-grpc.md` |
| Python + Celery | `stack/python-celery-worker.md` |
| Python library / CLI | `stack/python-lib.md` |
| Python service (no framework) | `stack/python-service.md` |
| Go + Echo | `stack/go-echo.md` |
| Go + gRPC | `stack/go-grpc.md` |
| Go service / API | `stack/go-service.md` |
| Go library / CLI | `stack/go-lib.md` |
| Java + Spring Boot | `stack/java-spring-boot.md` |
| Java + gRPC | `stack/java-grpc.md` |
| Node.js + NestJS | `stack/node-nestjs.md` |
| Node.js + Express | `stack/node-express.md` |
| Node.js library / CLI | `stack/nodejs-lib.md` |
| React SPA | `stack/spa-react.md` |
| Vue SPA | `stack/spa-vue.md` |
| Svelte SPA | `stack/spa-svelte.md` |
| Next.js (full-stack) | `stack/full-nextjs.md` |
| SvelteKit (full-stack) | `stack/full-sveltekit.md` |
| HTMX + server rendering | `stack/htmx.md` |
| Flutter (mobile) | `stack/mobile-flutter.md` |
| React Native (mobile) | `stack/mobile-react-native.md` |
| Astro (static site) | `stack/static-site-astro.md` |
| Hugo (static site) | `stack/static-site-hugo.md` |
| Rust library / CLI / crate | `stack/rust-lib.md` |
| Terraform (IaC) | `stack/iac-terraform.md` |

Confirm the selection with the user before proceeding.

---

## Step 8 — Output format [REQUIRED]

Which AI tool will use this context file?

| Choice | Output file | Location | Format guide |
|--------|-------------|----------|--------------|
| Claude Code | `CLAUDE.md` | project root | `formats/claude.md` |
| Cursor | `.cursor/rules/project.mdc` | `.cursor/rules/` | `formats/cursorrules.md` |
| GitHub Copilot | `copilot-instructions.md` | `.github/` | `formats/copilot.md` |
| OpenAI Codex CLI | `AGENTS.md` | project root | `formats/codex.md` |
| Other / generic | `AI_CONTEXT.md` | project root | `formats/generic.md` |

Load the corresponding file in `formats/` and apply its structure and
formatting rules when rendering the final context file.