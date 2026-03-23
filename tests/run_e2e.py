#!/usr/bin/env python3
"""
E2E test runner for solid-ai-templates.

Calls `claude -p` with prepared interview answers and stack templates,
then asserts required strings are present (and forbidden strings absent).

Usage:
  py tests/run_e2e.py                    # run all non-skipped tests
  py tests/run_e2e.py STK-01             # run one test by short ID
  py tests/run_e2e.py STK-01 FMT-01      # run multiple
  py tests/run_e2e.py --dry-run          # print prompt, skip claude call
"""

import datetime
import io
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(rel_path):
    with io.open(os.path.join(ROOT, rel_path), encoding="utf-8") as f:
        return f.read()


def build_prompt(stack_file, answers, output_file="output/CLAUDE.md",
                 extra_files=()):
    interview = read("INTERVIEW.md")
    stack = read(stack_file)
    output_fmt = read(output_file)
    answers_text = "\n".join(f"- {k}: {v}" for k, v in answers.items())
    extra_sections = "".join(
        f"--- {f} ---\n{read(f)}\n\n" for f in extra_files
    )
    return (
        f"You are generating a context file for a software project.\n\n"
        "Use the templates and interview answers below to compose the output.\n"
        f"Follow the output format rules in the output format file exactly.\n"
        "Output ONLY the file content — no preamble, no explanation, "
        "no markdown fences around the whole document.\n\n"
        f"--- INTERVIEW.md ---\n{interview}\n\n"
        f"--- Stack template ({stack_file}) ---\n{stack}\n\n"
        f"{extra_sections}"
        f"--- Output format ({output_file}) ---\n{output_fmt}\n\n"
        f"--- Interview answers ---\n{answers_text}\n\n"
        f"Generate the output file now."
    )


def run_claude(prompt, timeout=180):
    # Pass the prompt via stdin to avoid shell quoting issues on Windows.
    # `claude -p` reads stdin when no positional prompt argument is given.
    result = subprocess.run(
        "claude -p --no-session-persistence",
        input=prompt,
        capture_output=True,
        timeout=timeout,
        encoding="utf-8",
        errors="replace",
        shell=True,
    )
    return result.stdout


def check_assertions(output, required=(), forbidden=()):
    failures = []
    lower = output.lower()
    for s in required:
        if s.lower() not in lower:
            failures.append(f"  MISSING   : {s!r}")
    for s in forbidden:
        if s.lower() in lower:
            failures.append(f"  UNEXPECTED: {s!r}")
    return failures


# ---------------------------------------------------------------------------
# Test cases
#
# Each test entry has these fields:
#   id          short ID used on the command line (e.g. STK-01)
#   spec        the spec file this test implements
#   stack       stack template file fed to the agent
#   answers     interview answers the agent receives
#   output_file output format template (defaults to output/CLAUDE.md)
#   extra_files additional template files to include in the prompt
#   required    strings that MUST appear in the output — the test fails if any
#               are missing; used to assert that key sections and rules are
#               present
#   forbidden   strings that MUST NOT appear in the output — the test fails if
#               any are found; used to assert that:
#               - unfilled template placeholders were replaced by real values
#               - rules from a different output format did not leak in
#               - sections that do not apply to this stack are absent
#   skip        if present, the test is skipped with this message
# ---------------------------------------------------------------------------

TESTS = [
    # -------------------------------------------------------------------------
    # FastAPI
    # -------------------------------------------------------------------------
    {
        "id": "STK-01",
        "spec": "SAIT-E2E-STK-01-001A",
        "stack": "stack/python-fastapi.md",
        "answers": {
            "Project name": "OrderService",
            "Owner": "Platform team",
            "Repo": "github.com/acme/order-service",
            "Deployment": "Docker to Kubernetes (cloud)",
            "Database": "PostgreSQL via SQLAlchemy 2 + Alembic",
            "Auth": "JWT bearer tokens",
            "Feature flags": "no",
            "Messaging": "no",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Python 3.11", "FastAPI", "SQLAlchemy",
            "pytest",
            "async def",
            "pydantic-settings",
            "feat/",
        ],
        # these are raw template placeholders — if any appear, the agent
        # failed to substitute the interview answers into the output
        "forbidden": ["[your project]", "[owner]", "[repo]", "[platform]"],
    },
    # -------------------------------------------------------------------------
    # Go Echo
    # -------------------------------------------------------------------------
    {
        "id": "STK-02",
        "spec": "SAIT-E2E-STK-02-001A",
        "stack": "stack/go-echo.md",
        "answers": {
            "Project name": "MetricsHub",
            "Owner": "Infrastructure team",
            "Repo": "github.com/acme/metricshub",
            "Deployment": "Docker to Kubernetes (cloud)",
            "Database": "PostgreSQL via sqlc + pgx",
            "Auth": "JWT bearer tokens",
            "Feature flags": "yes — OpenFeature Go SDK",
            "Messaging": "no",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Go 1.22", "Echo v4", "sqlc", "pgx",
            "cmd/", "internal/",
            "errgroup", "SIGTERM",
            "OpenFeature",
            "go.sum",
            "feat/",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # Django
    # -------------------------------------------------------------------------
    {
        "id": "STK-03",
        "spec": "SAIT-E2E-STK-03-001A",
        "stack": "stack/python-django.md",
        "answers": {
            "Project name": "CatalogService",
            "Framework": "Django 5.x + Django REST Framework",
            "Database": "PostgreSQL via Django ORM",
            "Auth": "JWT via djangorestframework-simplejwt",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Django", "REST framework",
            "select_related", "prefetch_related",
            "migration",
            "simplejwt",
            "pytest-django", "django_db",
            "feat/",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # Node Express
    # -------------------------------------------------------------------------
    {
        "id": "STK-04",
        "spec": "SAIT-E2E-STK-04-001A",
        "stack": "stack/node-express.md",
        "answers": {
            "Project name": "NotificationService",
            "Language": "TypeScript",
            "Database": "PostgreSQL",
            "Auth": "JWT",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Node", "Express", "TypeScript", "Zod",
            "middleware",
            "supertest",
            "feat/",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # React SPA
    # -------------------------------------------------------------------------
    {
        "id": "STK-05",
        "spec": "SAIT-E2E-STK-05-001A",
        "stack": "stack/spa-react.md",
        "answers": {
            "Project name": "DashboardApp",
            "Language": "TypeScript",
            "State management": "Zustand",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "React", "TypeScript", "Zustand",
            "component",
            "React Testing Library",
            "accessibility",
            "feat/",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # Next.js
    # -------------------------------------------------------------------------
    {
        "id": "STK-06",
        "spec": "SAIT-E2E-STK-06-001A",
        "stack": "stack/full-nextjs.md",
        "answers": {
            "Project name": "StorefrontApp",
            "Language": "TypeScript",
            "Rendering strategy": "App Router with Server Components",
            "Database": "Prisma + PostgreSQL",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Next.js", "React", "TypeScript", "Prisma",
            "App Router", "Server Component",
            "Route Handler",
            "feat/",
        ],
        # Next.js App Router project — pages/ is the old Pages Router convention
        # and must not appear; its presence means the model used the wrong routing model
        "forbidden": ["pages/"],
    },
    # -------------------------------------------------------------------------
    # Astro
    # -------------------------------------------------------------------------
    {
        "id": "STK-07",
        "spec": "SAIT-E2E-STK-07-001A",
        "stack": "stack/static-site-astro.md",
        "answers": {
            "Project name": "TechBlog",
            "Language": "TypeScript",
            "Content": "Markdown + MDX",
            "Integrations": "React islands for interactive components",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Git conventions", "## Code conventions",
            "Astro", "TypeScript", "MDX",
            "src/content",
            "client:",
            "feat/",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # Go gRPC
    # -------------------------------------------------------------------------
    {
        "id": "STK-08",
        "spec": "SAIT-E2E-STK-08-001A",
        "stack": "stack/go-grpc.md",
        "answers": {
            "Project name": "PaymentGateway",
            "Language": "Go",
            "Communication": "gRPC (internal service-to-service)",
            "Auth": "mTLS",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Go", "gRPC", "proto",
            "interceptor",
            "status code",
            "feat/",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # Flutter
    # -------------------------------------------------------------------------
    {
        "id": "STK-09",
        "spec": "SAIT-E2E-STK-09-001A",
        "stack": "stack/mobile-flutter.md",
        "answers": {
            "Project name": "FieldSurveyApp",
            "Language": "Dart",
            "State management": "Riverpod",
            "Platforms": "iOS and Android",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Flutter", "Dart", "Riverpod",
            "widget",
            "feat/",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # Go library
    # -------------------------------------------------------------------------
    {
        "id": "STK-10",
        "spec": "SAIT-E2E-STK-10-001A",
        "stack": "stack/go-lib.md",
        "answers": {
            "Project name": "retrykit",
            "Language": "Go",
            "Distribution": "Go module (pkg.go.dev)",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Go",
            "doc comment",
            "vX.Y.Z",
            "go.sum",
            "feat/",
        ],
        # go-lib is a library, not a deployable service — Dockerfile and a
        # Deployment section have no place here
        "forbidden": ["Dockerfile", "## Deployment"],
    },
    # -------------------------------------------------------------------------
    # Flask
    # -------------------------------------------------------------------------
    {
        "id": "STK-11",
        "spec": "SAIT-E2E-STK-11-001A",
        "stack": "stack/python-flask.md",
        "answers": {
            "Project name": "ReportingAPI",
            "Language": "Python",
            "Database": "PostgreSQL via Flask-SQLAlchemy",
            "Auth": "JWT",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Flask", "Python", "SQLAlchemy",
            "create_app",
            "blueprint",
            "pytest-flask",
            "feat/",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # Generic Python service
    # -------------------------------------------------------------------------
    {
        "id": "STK-12",
        "spec": "SAIT-E2E-STK-12-001A",
        "stack": "stack/python-service.md",
        "answers": {
            "Project name": "DataPipelineWorker",
            "Language": "Python",
            "Framework": "none (plain Python service)",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Python",
            "ruff",
            "pytest",
            "feat/",
        ],
        # python-service is framework-agnostic — if a specific framework name
        # appears, the model pulled rules from the wrong template
        "forbidden": ["FastAPI", "Flask", "Django"],
    },
    # -------------------------------------------------------------------------
    # Python gRPC
    # -------------------------------------------------------------------------
    {
        "id": "STK-13",
        "spec": "SAIT-E2E-STK-13-001A",
        "stack": "stack/python-grpc.md",
        "answers": {
            "Project name": "MLInferenceService",
            "Language": "Python",
            "Communication": "gRPC (internal service-to-service)",
            "Auth": "mTLS",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Python", "gRPC", "proto",
            "grpcio",
            "servicer",
            "interceptor",
            "feat/",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # Celery worker
    # -------------------------------------------------------------------------
    {
        "id": "STK-14",
        "spec": "SAIT-E2E-STK-14-001A",
        "stack": "stack/python-celery-worker.md",
        "answers": {
            "Project name": "EmailDispatchWorker",
            "Language": "Python",
            "Broker": "Redis",
            "Result backend": "Redis",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Python", "Celery", "Redis",
            "idempoten",
            "retry", "max_retries",
            "Celery Beat",
            "feat/",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # Python library
    # -------------------------------------------------------------------------
    {
        "id": "STK-15",
        "spec": "SAIT-E2E-STK-15-001A",
        "stack": "stack/python-lib.md",
        "answers": {
            "Project name": "validify",
            "Language": "Python",
            "Distribution": "PyPI package",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Python",
            "pyproject.toml",
            "docstring",
            "feat/",
        ],
        # python-lib is a library, not a deployable service — Dockerfile and a
        # Deployment section have no place here
        "forbidden": ["Dockerfile", "## Deployment"],
    },
    # -------------------------------------------------------------------------
    # Generic Go service (stdlib)
    # -------------------------------------------------------------------------
    {
        "id": "STK-16",
        "spec": "SAIT-E2E-STK-16-001A",
        "stack": "stack/go-service.md",
        "answers": {
            "Project name": "HealthCheckService",
            "Language": "Go",
            "HTTP framework": "none (standard library only)",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Go",
            "net/http",
            "graceful shutdown",
            "go.sum",
            "feat/",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # Hugo
    # -------------------------------------------------------------------------
    {
        "id": "STK-17",
        "spec": "SAIT-E2E-STK-17-001A",
        "stack": "stack/static-site-hugo.md",
        "answers": {
            "Project name": "DocumentationSite",
            "Language": "Markdown + Go templates",
            "Theme": "custom",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Git conventions", "## Code conventions",
            "Hugo",
            "archetype",
            "shortcode",
            "feat/",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # Node.js library
    # -------------------------------------------------------------------------
    {
        "id": "STK-18",
        "spec": "SAIT-E2E-STK-18-001A",
        "stack": "stack/nodejs-lib.md",
        "answers": {
            "Project name": "parsekit",
            "Language": "TypeScript",
            "Distribution": "npm package",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Node", "TypeScript",
            "exports",
            "vitest",
            "feat/",
        ],
        # node-lib is a library, not a deployable service — Dockerfile and a
        # Deployment section have no place here
        "forbidden": ["Dockerfile", "## Deployment"],
    },
    # -------------------------------------------------------------------------
    # Rust library
    # -------------------------------------------------------------------------
    {
        "id": "STK-19",
        "spec": "SAIT-E2E-STK-19-001A",
        "stack": "stack/rust-lib.md",
        "answers": {
            "Project name": "byteparser",
            "Language": "Rust",
            "Distribution": "crates.io",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Commands",
            "## Git conventions", "## Code conventions", "## Testing",
            "Rust",
            "pub",
            "doc comment",
            "cargo test", "cargo clippy",
            "feat/",
        ],
        # rust-lib is a library — web frameworks are service concerns and must
        # not appear here; Tokio is excluded because the model may reference it
        # in a negative context ("do not add Tokio unless async is needed")
        "forbidden": ["axum", "actix"],
    },
    # -------------------------------------------------------------------------
    # HTMX
    # -------------------------------------------------------------------------
    {
        "id": "STK-20",
        "spec": "SAIT-E2E-STK-20-001A",
        "stack": "stack/htmx.md",
        "answers": {
            "Project name": "AdminDashboard",
            "Backend language": "Python (Flask)",
            "Templating engine": "Jinja2",
            "Client-side state": "Alpine.js",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Commands",
            "## Git conventions", "## Code conventions",
            "HTMX", "Jinja2",
            "hx-",
            "fragment",
            "Alpine",
            "feat/",
        ],
        # HTMX is a server-rendered hypermedia approach — JSON APIs and SPA
        # routing patterns belong to a different architecture and must not appear
        "forbidden": ["JSON API", "SPA routing"],
    },
    # -------------------------------------------------------------------------
    # FMT-01  CLAUDE.md (Claude Code)
    # -------------------------------------------------------------------------
    {
        "id": "FMT-01",
        "spec": "SAIT-E2E-FMT-01-001A",
        "stack": "stack/python-fastapi.md",
        "output_file": "output/claude.md",
        "answers": {
            "Project name": "OrderService",
            "Database": "PostgreSQL via SQLAlchemy 2",
            "Auth": "JWT bearer tokens",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Code conventions", "## Git conventions", "## Testing",
            "Python", "FastAPI",
            "feat/",
        ],
        # CLAUDE.md has no frontmatter or tool-specific directives — these
        # keywords belong to Cursor (.mdc) format and must not appear here
        "forbidden": ["alwaysApply", "applyTo", "globs:"],
    },
    # -------------------------------------------------------------------------
    # FMT-02  AGENTS.md (Codex CLI)
    # -------------------------------------------------------------------------
    {
        "id": "FMT-02",
        "spec": "SAIT-E2E-FMT-02-001A",
        "stack": "stack/python-fastapi.md",
        "output_file": "output/codex.md",
        "answers": {
            "Project name": "OrderService",
            "Database": "PostgreSQL via SQLAlchemy 2",
            "Auth": "JWT bearer tokens",
            "Output format": "AGENTS.md",
        },
        "required": [
            "## Stack", "## Commands", "## Code conventions",
            "## Git conventions", "## Testing",
            "Python", "FastAPI",
            "feat/",
        ],
        # AGENTS.md has no frontmatter or Cursor-specific directives — these
        # keywords would indicate the model applied the wrong output format
        "forbidden": ["alwaysApply", "applyTo", "frontmatter"],
    },
    # -------------------------------------------------------------------------
    # FMT-03  Cursor .mdc
    # -------------------------------------------------------------------------
    {
        "id": "FMT-03",
        "spec": "SAIT-E2E-FMT-03-001A",
        "stack": "stack/python-fastapi.md",
        "output_file": "output/cursorrules.md",
        "answers": {
            "Project name": "OrderService",
            "Database": "PostgreSQL via SQLAlchemy 2",
            "Auth": "JWT bearer tokens",
            "Output format": "Cursor .mdc",
        },
        "required": [
            "alwaysApply",
            "description:",
            "## Stack", "## Code conventions",
            "## Git conventions", "## Testing",
            "Python", "FastAPI",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # FMT-04  GitHub Copilot
    # -------------------------------------------------------------------------
    {
        "id": "FMT-04",
        "spec": "SAIT-E2E-FMT-04-001A",
        "stack": "stack/python-fastapi.md",
        "output_file": "output/copilot.md",
        "answers": {
            "Project name": "OrderService",
            "Database": "PostgreSQL via SQLAlchemy 2",
            "Auth": "JWT bearer tokens",
            "Output format": "copilot-instructions.md",
        },
        "required": [
            "## Stack", "## Code conventions",
            "## Git conventions", "## Testing", "## Commands",
            "Python", "FastAPI",
            "feat/",
        ],
        # copilot-instructions.md has no frontmatter or glob patterns — these
        # keywords belong to Cursor (.mdc) format and must not appear here
        "forbidden": ["alwaysApply", "globs:"],
    },
    # -------------------------------------------------------------------------
    # FMT-05  Generic AI_CONTEXT.md
    # -------------------------------------------------------------------------
    {
        "id": "FMT-05",
        "spec": "SAIT-E2E-FMT-05-001A",
        "stack": "stack/python-fastapi.md",
        "output_file": "output/generic.md",
        "answers": {
            "Project name": "OrderService",
            "Database": "PostgreSQL via SQLAlchemy 2",
            "Auth": "JWT bearer tokens",
            "Output format": "AI_CONTEXT.md",
        },
        "required": [
            "## Stack", "## Architecture", "## Commands",
            "## Code conventions", "## Git conventions", "## Testing",
            "Python", "FastAPI",
            "feat/",
        ],
        # generic format has no tool-specific directives — alwaysApply is a
        # Cursor keyword and must not appear in a tool-agnostic output
        "forbidden": ["alwaysApply"],
    },
    # -------------------------------------------------------------------------
    # ITV-02  DEFAULTED sections pre-filled without user input
    # Provide only REQUIRED project identity answers — no git convention
    # answers. Assert that git conventions appear in output anyway (pre-filled
    # from base/git.md via the stack dependency chain).
    # -------------------------------------------------------------------------
    {
        "id": "ITV-02",
        "spec": "SAIT-INT-ITV-02-001A",
        "stack": "stack/python-fastapi.md",
        "answers": {
            "Project name": "InventoryService",
            "Owner": "Backend team",
            "Deployment": "Docker",
            "Database": "PostgreSQL via SQLAlchemy 2",
            "Auth": "JWT bearer tokens",
            "Output format": "CLAUDE.md",
            # Deliberately omit git convention answers — should be pre-filled
        },
        "required": [
            "## Git conventions",
            "feat/",         # from base/git.md DEFAULTED section
            "## Stack", "## Commands", "## Code conventions", "## Testing",
            "Python", "FastAPI",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # ITV-03  Interview answer overrides stack template rule
    # Provide a contradicting answer for the test runner. Assert the override
    # wins. Note: pytest may still appear in ## Commands — that is acceptable;
    # the Testing *section* must use unittest.
    # -------------------------------------------------------------------------
    {
        "id": "ITV-03",
        "spec": "SAIT-INT-ITV-03-001A",
        "stack": "stack/python-fastapi.md",
        "answers": {
            "Project name": "InventoryService",
            "Owner": "Backend team",
            "Deployment": "Docker",
            "Database": "PostgreSQL via SQLAlchemy 2",
            "Auth": "JWT bearer tokens",
            "Test runner override": "Use unittest instead of pytest for all tests",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Stack", "## Commands", "## Git conventions",
            "## Code conventions", "## Testing",
            "unittest",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # DPL-01  Cloud deployment target
    # -------------------------------------------------------------------------
    {
        "id": "DPL-01",
        "spec": "SAIT-E2E-DPL-01-001A",
        "stack": "stack/node-express.md",
        "extra_files": ["base/deployment.md"],
        "answers": {
            "Project name": "PublicAPIService",
            "Owner": "Platform team",
            "Language": "TypeScript",
            "Deployment target": "cloud",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Deployment",
            "cloud",
        ],
        # cloud target means public infrastructure only — private CA and
        # air-gap/offline assumptions must not appear in the output
        "forbidden": ["private CA", "air-gap", "offline"],
    },
    # -------------------------------------------------------------------------
    # DPL-02  Hybrid deployment target
    # -------------------------------------------------------------------------
    {
        "id": "DPL-02",
        "spec": "SAIT-E2E-DPL-02-001A",
        "stack": "stack/java-spring-boot.md",
        "extra_files": ["base/deployment.md"],
        "answers": {
            "Project name": "InternalPlatformAPI",
            "Owner": "Platform team",
            "Language": "Java",
            "Deployment target": "hybrid (on-premises + cloud)",
            "Output format": "CLAUDE.md",
        },
        "required": [
            "## Deployment",
            "hybrid",
        ],
        "forbidden": [],
    },
    # -------------------------------------------------------------------------
    # DPL-03  Offline / air-gapped deployment target
    # -------------------------------------------------------------------------
    {
        "id": "DPL-03",
        "spec": "SAIT-E2E-DPL-03-001A",
        "stack": "stack/python-fastapi.md",
        "extra_files": ["base/deployment.md"],
        "answers": {
            "Project name": "SecureIngestService",
            "Owner": "Platform team",
            "Language": "Python",
            "Deployment target": "offline (air-gapped, no internet access)",
            "Output format": "CLAUDE.md",
        },
        "required": [
            # model may embed deployment info in project identity rather than
            # a dedicated ## Deployment section — check for the target keyword
            "offline",
            "air-gap",
        ],
        # offline/air-gapped target means no public internet — public
        # registries must not appear; ACM removed because model may reference
        # it negatively ("do not use ACM in air-gapped environments")
        "forbidden": ["Let's Encrypt", "Docker Hub"],
    },
]

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

PASS = "PASS"
FAIL = "FAIL"
SKIP = "SKIP"
ERR  = "ERR "


def run_test(test, dry_run=False):
    tid = test["id"]

    if "skip" in test:
        return SKIP, test["skip"], None

    prompt = build_prompt(
        test["stack"], test["answers"],
        test.get("output_file", "output/CLAUDE.md"),
        test.get("extra_files", ()),
    )

    if dry_run:
        print(f"\n{'='*60}")
        print(f"[{tid}] DRY RUN — prompt length: {len(prompt)} chars")
        print(prompt[:400], "...")
        return SKIP, "dry-run", None, None

    t0 = time.time()
    try:
        output = run_claude(prompt)
    except subprocess.TimeoutExpired:
        return ERR, "claude timed out after 180s", None, None
    except FileNotFoundError:
        return ERR, "claude not found — is Claude Code installed?", None, None
    elapsed = time.time() - t0

    failures = check_assertions(
        output,
        required=test.get("required", []),
        forbidden=test.get("forbidden", []),
    )

    if failures:
        return FAIL, "\n".join(failures), elapsed, output
    return PASS, f"{elapsed:.1f}s", elapsed, None


def write_report(run_results, started_at, dry_run):
    reports_dir = os.path.join(ROOT, "tests", "reports")
    os.makedirs(reports_dir, exist_ok=True)

    ts = started_at.strftime("%Y-%m-%dT%H-%M-%S")
    report_path = os.path.join(reports_dir, f"{ts}-e2e.md")

    passed  = sum(1 for r in run_results if r["status"] == PASS)
    failed  = sum(1 for r in run_results if r["status"] == FAIL)
    skipped = sum(1 for r in run_results if r["status"] == SKIP)
    errored = sum(1 for r in run_results if r["status"] == ERR)
    total   = len(run_results)

    lines = [
        "# E2E Test Report",
        "",
        f"**Date**: {started_at.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Runner**: run_e2e.py  ",
        f"**Mode**: {'dry-run' if dry_run else 'live'}  ",
        f"**Tests run**: {total}",
        "",
        "## Summary",
        "",
        (f"{total} tests — {passed} passed  {failed} failed  "
         f"{skipped} skipped  {errored} errors"),
        "",
        "---",
        "",
        "## Results",
        "",
    ]

    for r in run_results:
        elapsed_str = f"  ({r['elapsed']:.1f}s)" if r["elapsed"] else ""
        lines.append(f"### {r['status']}  {r['id']}{elapsed_str}")
        lines.append("")
        if r["status"] == FAIL:
            lines.append("**Expected**:")
            lines.append("")
            lines.append("```")
            for line in r["detail"].splitlines():
                lines.append(line)
            lines.append("```")
            lines.append("")
            lines.append("**Observed** (first 1000 chars of model output):")
            lines.append("")
            lines.append("```")
            # replace triple backticks in model output so they don't close
            # the report's own code fence
            observed = (r["output"] or "")[:1000].replace("```", "~~~")
            lines.append(observed)
            lines.append("```")
            lines.append("")
        elif r["status"] == ERR:
            lines.append(f"**Error**: {r['detail']}")
            lines.append("")
        elif r["status"] == SKIP:
            lines.append(f"**Skipped**: {r['detail']}")
            lines.append("")

    with io.open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nReport: {os.path.relpath(report_path, ROOT)}")


def main():
    started_at = datetime.datetime.now()

    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    filter_ids = [a for a in args if not a.startswith("--")]

    tests = TESTS
    if filter_ids:
        tests = [t for t in TESTS if t["id"] in filter_ids]
        if not tests:
            print(f"No tests matched: {filter_ids}")
            sys.exit(1)

    results = {PASS: 0, FAIL: 0, SKIP: 0, ERR: 0}
    run_results = []

    print(f"Running {len(tests)} test(s)...\n")

    for test in tests:
        tid = test["id"]
        status, detail, elapsed, output = run_test(test, dry_run=dry_run)
        results[status] += 1
        run_results.append({
            "id": tid, "status": status,
            "detail": detail, "elapsed": elapsed, "output": output,
        })

        if status == PASS:
            print(f"  {status}  {tid}  ({detail})")
        elif status == SKIP:
            print(f"  {status}  {tid}  — {detail}")
        else:
            print(f"  {status}  {tid}")
            print(detail)

    total = sum(results.values())
    print(
        f"\n{total} tests — "
        f"{results[PASS]} passed  "
        f"{results[FAIL]} failed  "
        f"{results[SKIP]} skipped  "
        f"{results[ERR]} errors"
    )

    write_report(run_results, started_at, dry_run)

    sys.exit(0 if results[FAIL] == 0 and results[ERR] == 0 else 1)


if __name__ == "__main__":
    main()