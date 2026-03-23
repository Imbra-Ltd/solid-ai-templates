# Interview Template

<!--
INSTRUCTIONS FOR THE AGENT
============================
Follow the four phases below in order. Ask one question at a time.
Always state your preference when asking a clarifying question.
Do not generate partial output. Do not skip phases.
-->

---

## Phase 1 — Explore

Understand what the user wants to build. Do not ask about technology yet.
Focus on the problem, the users, and the goals.

Ask one question at a time. Suggested questions (pick the most relevant):

- What are you building, and who is it for?
- What problem does it solve?
- What are the key things the system needs to do?

---

## Phase 2 — Clarify

Ask 2–3 targeted follow-up questions to resolve ambiguity before proposing
a stack. Always state your preference as the default. Examples:

- "Will this be deployed to the cloud, or do you have on-prem constraints?
  I'd default to cloud."
- "Do you have a language or framework preference, or should I choose?
  I'd go with Python + FastAPI for a backend service like this."
- "Solo project or a team? I ask because it affects how much convention
  detail to include — I'd assume solo for now."

---

## Phase 3 — Propose

Based on what you learned, propose a complete setup:

- Language and version
- Framework
- Database and libraries (if applicable)
- Auth mechanism (if applicable)
- Deployment target and distribution
- Key conventions: testing, linting, git

Present the proposal as a short summary and ask the user to confirm or
adjust. Proceed to Phase 4 once the user approves.

---

## Phase 4 — Generate

Select the matching stack template from the table below and load its
DEPENDS ON chain. Apply any adjustments from Phase 3.
Generate the output file using the format rules in `formats/claude.md`.

| If language + framework is... | Use...                          | What it covers                                   |
|-------------------------------|---------------------------------|--------------------------------------------------|
| Python + FastAPI              | `stack/python-fastapi.md`       | Async REST API, Pydantic v2, DI, OpenAPI         |
| Python + Flask                | `stack/python-flask.md`         | Sync REST API, factory pattern, blueprints       |
| Python + Django               | `stack/python-django.md`        | Full web framework, ORM, DRF, admin              |
| Python + gRPC                 | `stack/python-grpc.md`          | gRPC service, grpcio-aio, proto design           |
| Python + Celery               | `stack/python-celery-worker.md` | Background tasks, retry/backoff, Beat scheduling |
| Python library / CLI          | `stack/python-lib.md`           | Installable package or CLI tool, PyPI            |
| Python service (no framework) | `stack/python-service.md`       | Generic Python web service, SQLAlchemy, Alembic  |
| Go + Echo                     | `stack/go-echo.md`              | REST API, Echo v4, middleware, validation        |
| Go + gRPC                     | `stack/go-grpc.md`              | gRPC service, bufconn, errgroup                  |
| Go service / API              | `stack/go-service.md`           | Generic Go HTTP service, chi, structured logging |
| Go library / CLI              | `stack/go-lib.md`               | Importable library or CLI binary                 |
| Java + Spring Boot            | `stack/java-spring-boot.md`     | REST API, JPA, Spring Security, Flyway           |
| Java + gRPC                   | `stack/java-grpc.md`            | gRPC service, grpc-java lifecycle                |
| Node.js + NestJS              | `stack/node-nestjs.md`          | Structured REST API, modules, guards, pipes      |
| Node.js + Express             | `stack/node-express.md`         | Minimal REST API, Zod validation                 |
| Node.js library / CLI         | `stack/nodejs-lib.md`           | TypeScript npm package or CLI, tsup              |
| React SPA                     | `stack/spa-react.md`            | Client-side app, TypeScript, RTL, a11y           |
| Vue SPA                       | `stack/spa-vue.md`              | Client-side app, Composition API, Pinia          |
| Svelte SPA                    | `stack/spa-svelte.md`           | Client-side app, Svelte 5 runes, Vitest          |
| Next.js (full-stack)          | `stack/full-nextjs.md`          | App Router, Server/Client Components, API routes |
| SvelteKit (full-stack)        | `stack/full-sveltekit.md`       | File-based routing, form actions, SSR            |
| HTMX + server rendering       | `stack/htmx.md`                 | Server-rendered HTML, HTMX 2.x, Alpine.js        |
| Flutter (mobile)              | `stack/mobile-flutter.md`       | iOS/Android, Riverpod, go_router, freezed        |
| React Native (mobile)         | `stack/mobile-react-native.md`  | iOS/Android, Expo, file-based routing, Maestro   |
| Astro (static site)           | `stack/static-site-astro.md`    | Islands architecture, client directives, MDX     |
| Hugo (static site)            | `stack/static-site-hugo.md`     | Go templates, archetypes, content structure      |
| Rust library / CLI / crate    | `stack/rust-lib.md`             | Rust crate or CLI, thiserror/anyhow, crates.io   |
| Terraform (IaC)               | `stack/iac-terraform.md`        | Infrastructure as code, modules, remote state    |
