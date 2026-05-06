#!/usr/bin/env python3
"""
Smoke and integration test runner for solid-ai-templates structural checks.

Implements:
  SAIT-SMK-SYS-01-001A  — all DEPENDS ON paths resolve to existing files
  SAIT-SMK-SYS-02-001A  — all section IDs are unique across all templates
  SAIT-SMK-TPL-04-001A  — all EXTEND/OVERRIDE directives reference existing IDs
  SAIT-INT-MNF-01-001A  — all manifest entries reference valid paths and IDs

Usage:
  py tests/run_smoke.py              # run all checks
  py tests/run_smoke.py SYS-01       # run one check by short ID
  py tests/run_smoke.py SYS-01 MNF-01
"""

import datetime
import io
import os
import re
import sys

from lib import ROOT, PASS, FAIL, ERR, write_report
from cases import ALL_TESTS

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ---------------------------------------------------------------------------
# Manifest resolution helpers (shared by MNF-02, MNF-03, MNF-04)
# ---------------------------------------------------------------------------

def _load_manifest():
    """Load manifest.yaml and return (core_ids, entries, file_to_id)."""
    manifest_path = os.path.join(ROOT, "templates", "manifest.yaml")
    with io.open(manifest_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    entries = {}
    for section in ("base", "platform", "frontend", "backend", "stacks"):
        for entry in data.get(section, []):
            entries[entry["id"]] = entry

    file_to_id = {e["file"]: e["id"] for e in entries.values()}
    return data.get("core", []), entries, file_to_id


def _resolve_stack(stack_id, core_ids, entries):
    """Resolve full dependency chain for a stack.

    Returns (ordered_files, resolved_ids).
    """
    resolved = set()
    files = []

    def add(eid):
        if eid in resolved:
            return
        resolved.add(eid)
        entry = entries.get(eid)
        if entry:
            files.append(entry["file"])

    def resolve(eid):
        if eid in resolved:
            return
        entry = entries.get(eid)
        if not entry:
            return
        for dep in entry.get("depends_on", []):
            resolve(dep)
        add(eid)

    for cid in core_ids:
        add(cid)

    resolve(stack_id)
    return files, resolved

TEMPLATE_DIRS = [
    os.path.join("templates", "base", "core"),
    os.path.join("templates", "base", "security"),
    os.path.join("templates", "base", "infra"),
    os.path.join("templates", "base", "workflow"),
    os.path.join("templates", "base", "language"),
    os.path.join("templates", "base", "data"),
    os.path.join("templates", "backend"),
    os.path.join("templates", "frontend"),
    os.path.join("templates", "stack"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def all_template_files():
    files = []
    for d in TEMPLATE_DIRS:
        dirpath = os.path.join(ROOT, d)
        for name in os.listdir(dirpath):
            if name.endswith(".md"):
                files.append(os.path.join(dirpath, name))
    return files


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# SYS-01 — DEPENDS ON paths resolve to existing files
# ---------------------------------------------------------------------------

def check_sys_01():
    failures = []
    pattern = re.compile(r'\[DEPENDS ON:\s*([^\]]+)\]')

    for filepath in all_template_files():
        content = read(filepath)
        for match in pattern.finditer(content):
            refs = [r.strip() for r in match.group(1).split(',')]
            for ref in refs:
                ref_path = os.path.join(ROOT, ref)
                if not os.path.isfile(ref_path):
                    rel = os.path.relpath(filepath, ROOT)
                    failures.append(f"  {rel}: DEPENDS ON '{ref}' — file not found")

    return failures


# ---------------------------------------------------------------------------
# SYS-02 — all section IDs unique across all templates
# ---------------------------------------------------------------------------

def check_sys_02():
    failures = []
    pattern = re.compile(r'\[ID:\s*([^\]]+)\]')
    seen = {}

    for filepath in all_template_files():
        content = read(filepath)
        rel = os.path.relpath(filepath, ROOT)
        for match in pattern.finditer(content):
            sid = match.group(1).strip()
            if sid in seen:
                failures.append(
                    f"  Duplicate ID '{sid}': "
                    f"{seen[sid]} and {rel}"
                )
            else:
                seen[sid] = rel

    return failures


# ---------------------------------------------------------------------------
# TPL-04 — all EXTEND/OVERRIDE refs point to existing IDs
# ---------------------------------------------------------------------------

def check_tpl_04():
    failures = []
    id_pattern  = re.compile(r'\[ID:\s*([^\]]+)\]')
    ref_pattern = re.compile(r'\[(EXTEND|OVERRIDE):\s*([^\]]+)\]')

    declared = set()
    for filepath in all_template_files():
        content = read(filepath)
        for match in id_pattern.finditer(content):
            declared.add(match.group(1).strip())

    for filepath in all_template_files():
        content = read(filepath)
        rel = os.path.relpath(filepath, ROOT)
        for match in ref_pattern.finditer(content):
            directive = match.group(1)
            ref_id = match.group(2).strip()
            if ref_id not in declared:
                failures.append(
                    f"  {rel}: [{directive}: {ref_id}] — ID not declared"
                )

    return failures


# ---------------------------------------------------------------------------
# MNF-01 — manifest entries reference valid paths and IDs
# ---------------------------------------------------------------------------

def check_mnf_01():
    if not HAS_YAML:
        return ["  PyYAML not installed — run: pip install pyyaml"]

    manifest_path = os.path.join(ROOT, "templates", "manifest.yaml")
    if not os.path.isfile(manifest_path):
        return ["  manifest.yaml not found"]

    with io.open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    failures = []
    declared_ids = set()
    entries = []

    for section in manifest.values():
        if isinstance(section, list):
            for entry in section:
                if isinstance(entry, dict):
                    entries.append(entry)
                    if "id" in entry:
                        declared_ids.add(entry["id"])

    for entry in entries:
        path = entry.get("file", "")
        if path and not os.path.isfile(os.path.join(ROOT, path)):
            failures.append(f"  file not found: '{path}' (id: {entry.get('id', '?')})")

    for entry in entries:
        for dep in entry.get("depends_on", []):
            if dep not in declared_ids:
                failures.append(
                    f"  depends_on '{dep}' in '{entry.get('id', '?')}' "
                    f"— ID not declared in manifest"
                )

    return failures


# ---------------------------------------------------------------------------
# TPL-01 — DEPENDS ON chain from python-fastapi.md is complete
# ---------------------------------------------------------------------------

def _collect_chain(rel_path, visited=None):
    if visited is None:
        visited = set()
    if rel_path in visited:
        return visited
    visited.add(rel_path)
    abs_path = os.path.join(ROOT, rel_path)
    if not os.path.isfile(abs_path):
        return visited
    content = read(abs_path)
    pattern = re.compile(r'\[DEPENDS ON:\s*([^\]]+)\]')
    for match in pattern.finditer(content):
        for dep in [r.strip() for r in match.group(1).split(',')]:
            _collect_chain(dep, visited)
    return visited


def check_tpl_01():
    failures = []
    chain = _collect_chain("templates/stack/python-fastapi.md")
    required = [
        "templates/stack/python-lib.md",
        "templates/stack/python-service.md",
        "templates/base/core/git.md",
        "templates/base/core/docs.md",
        "templates/base/core/quality.md",
        "templates/base/core/config.md",
        "templates/backend/http.md",
        "templates/backend/database.md",
        "templates/backend/observability.md",
        "templates/backend/quality.md",
        "templates/backend/features.md",
        "templates/backend/messaging.md",
    ]
    for req in required:
        if req not in chain:
            failures.append(f"  python-fastapi.md chain missing: '{req}'")
    return failures


# ---------------------------------------------------------------------------
# TPL-02 — EXTEND adds rules without removing base rules
# ---------------------------------------------------------------------------

def _extract_section(filepath, section_id):
    content = read(filepath)
    lines = content.splitlines()
    result = []
    in_section = False
    tag = f"[ID: {section_id}]"
    extend_tag = f"[EXTEND: {section_id}]"
    override_tag = f"[OVERRIDE: {section_id}]"

    for i, line in enumerate(lines):
        if tag in line or extend_tag in line or override_tag in line:
            in_section = True
            continue
        if in_section:
            has_content = any(l.strip() for l in result)
            if re.match(r'^#{1,4} ', line) and has_content:
                break
            if re.match(r'^\[(ID|EXTEND|OVERRIDE|DEPENDS):', line) and has_content:
                break
            result.append(line)

    return [l for l in result if l.strip()]


def check_tpl_02():
    failures = []

    base_content = _extract_section(
        os.path.join(ROOT, "templates", "base", "core", "testing.md"), "base-testing"
    )
    if not base_content:
        failures.append("  base/core/testing.md [ID: base-testing] section is empty")

    flask_content = _extract_section(
        os.path.join(ROOT, "templates", "stack", "python-flask.md"), "base-testing"
    )
    if not flask_content:
        failures.append(
            "  stack/python-flask.md [EXTEND: base-testing] section is empty "
            "— base rules may have been lost"
        )

    return failures


# ---------------------------------------------------------------------------
# TPL-03 — OVERRIDE replaces parent section entirely
# ---------------------------------------------------------------------------

def check_tpl_03():
    failures = []

    original = _extract_section(
        os.path.join(ROOT, "templates", "stack", "go-lib.md"), "go-lib-stack"
    )
    override = _extract_section(
        os.path.join(ROOT, "templates", "stack", "go-service.md"), "go-lib-stack"
    )

    if not original:
        failures.append("  stack/go-lib.md [ID: go-lib-stack] section is empty")
    if not override:
        failures.append(
            "  stack/go-service.md [OVERRIDE: go-lib-stack] section is empty"
        )
    if original and override and original == override:
        failures.append(
            "  [OVERRIDE: go-lib-stack] content is identical to the original "
            "[ID: go-lib-stack] — override has no effect"
        )

    return failures


# ---------------------------------------------------------------------------
# MNF-02 — all stacks resolve to valid, non-empty file lists
# ---------------------------------------------------------------------------

def check_mnf_02():
    if not HAS_YAML:
        return ["  PyYAML not installed — run: pip install pyyaml"]

    core_ids, entries, _ = _load_manifest()
    failures = []

    stacks = [e for e in entries.values()
              if e["file"].startswith("templates/stack/")]

    for stack in stacks:
        sid = stack["id"]
        files, _ = _resolve_stack(sid, core_ids, entries)

        if not files:
            failures.append(f"  {sid}: resolution produced empty file list")
            continue

        for f in files:
            path = os.path.join(ROOT, f)
            if not os.path.isfile(path):
                failures.append(f"  {sid}: resolved file missing: {f}")
            elif os.path.getsize(path) == 0:
                failures.append(f"  {sid}: resolved file empty: {f}")

    return failures


# ---------------------------------------------------------------------------
# MNF-03 — all resolved chains include core tier files
# ---------------------------------------------------------------------------

def check_mnf_03():
    if not HAS_YAML:
        return ["  PyYAML not installed — run: pip install pyyaml"]

    core_ids, entries, _ = _load_manifest()
    failures = []

    stacks = [e for e in entries.values()
              if e["file"].startswith("templates/stack/")]

    for stack in stacks:
        sid = stack["id"]
        _, resolved_ids = _resolve_stack(sid, core_ids, entries)

        for cid in core_ids:
            if cid not in resolved_ids:
                failures.append(
                    f"  {sid}: core ID '{cid}' missing from "
                    f"resolved chain"
                )

    return failures


# ---------------------------------------------------------------------------
# MNF-04 — prompt builds for all stacks
# ---------------------------------------------------------------------------

def check_mnf_04():
    if not HAS_YAML:
        return ["  PyYAML not installed — run: pip install pyyaml"]

    core_ids, entries, _ = _load_manifest()
    failures = []

    output_file = "templates/base/core/agents.md"
    output_path = os.path.join(ROOT, output_file)
    if not os.path.isfile(output_path):
        return [f"  output format missing: {output_file}"]

    output_fmt = read(output_path)

    stacks = [e for e in entries.values()
              if e["file"].startswith("templates/stack/")]

    for stack in stacks:
        sid = stack["id"]
        files, _ = _resolve_stack(sid, core_ids, entries)

        try:
            parts = []
            for f in files:
                parts.append(read(os.path.join(ROOT, f)))
            prompt = "\n\n".join(parts) + "\n\n" + output_fmt
        except Exception as e:
            failures.append(f"  {sid}: prompt build failed: {e}")
            continue

        if len(prompt) < 500:
            failures.append(
                f"  {sid}: prompt suspiciously short "
                f"({len(prompt)} chars)"
            )

    return failures


# ---------------------------------------------------------------------------
# E2E-01 — all cases.py paths resolve to existing files
# ---------------------------------------------------------------------------

def check_e2e_01():
    failures = []

    interview = os.path.join(ROOT, "templates", "INTERVIEW.md")
    if not os.path.isfile(interview):
        failures.append("  INTERVIEW.md not found: templates/INTERVIEW.md")

    for test in ALL_TESTS:
        if "skip" in test:
            continue

        tid = test.get("id", "?")

        stack = test.get("stack", "")
        if stack:
            path = os.path.join(ROOT, stack)
            if not os.path.isfile(path):
                failures.append(f"  {tid}: stack file missing: {stack}")

        output_file = test.get("output_file", "templates/base/core/agents.md")
        path = os.path.join(ROOT, output_file)
        if not os.path.isfile(path):
            failures.append(f"  {tid}: output_file missing: {output_file}")

        for ef in test.get("extra_files", []):
            path = os.path.join(ROOT, ef)
            if not os.path.isfile(path):
                failures.append(f"  {tid}: extra_file missing: {ef}")

    return failures


# ---------------------------------------------------------------------------
# Test registry
# ---------------------------------------------------------------------------

CHECKS = [
    {"id": "SYS-01", "spec": "SAIT-SMK-SYS-01-001A",
     "title": "DEPENDS ON paths resolve to existing files", "fn": check_sys_01},
    {"id": "SYS-02", "spec": "SAIT-SMK-SYS-02-001A",
     "title": "All section IDs unique across templates", "fn": check_sys_02},
    {"id": "TPL-04", "spec": "SAIT-SMK-TPL-04-001A",
     "title": "All EXTEND/OVERRIDE refs point to existing IDs", "fn": check_tpl_04},
    {"id": "MNF-01", "spec": "SAIT-INT-MNF-01-001A",
     "title": "Manifest entries reference valid paths and IDs", "fn": check_mnf_01},
    {"id": "MNF-02", "spec": "SAIT-INT-MNF-02-001A",
     "title": "All stacks resolve to valid, non-empty file lists", "fn": check_mnf_02},
    {"id": "MNF-03", "spec": "SAIT-INT-MNF-03-001A",
     "title": "All resolved chains include core tier files", "fn": check_mnf_03},
    {"id": "MNF-04", "spec": "SAIT-INT-MNF-04-001A",
     "title": "Prompt builds for all stacks", "fn": check_mnf_04},
    {"id": "TPL-01", "spec": "SAIT-INT-TPL-01-001A",
     "title": "DEPENDS ON chain from python-fastapi.md is complete", "fn": check_tpl_01},
    {"id": "TPL-02", "spec": "SAIT-INT-TPL-02-001A",
     "title": "EXTEND adds rules without removing base rules", "fn": check_tpl_02},
    {"id": "TPL-03", "spec": "SAIT-INT-TPL-03-001A",
     "title": "OVERRIDE replaces parent section with different content", "fn": check_tpl_03},
    {"id": "E2E-01", "spec": "SAIT-SMK-E2E-01-001A",
     "title": "All cases.py paths resolve to existing files", "fn": check_e2e_01},
]


# ---------------------------------------------------------------------------
# Report renderers
# ---------------------------------------------------------------------------

def render_pass(r):
    return [f"### {r['status']}  {r['id']} — {r['title']}", ""]


def render_fail(r):
    lines = [f"### {r['status']}  {r['id']} — {r['title']}", "",
             "**Expected**: all assertions pass with no violations", "",
             "**Observed**:", "", "```"]
    lines.extend(r["failures"])
    lines.extend(["```", ""])
    return lines


def render_err(r):
    return [f"### {r['status']}  {r['id']} — {r['title']}", "",
            f"**Error**: {r['error']}", ""]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main():
    started_at = datetime.datetime.now()

    args = sys.argv[1:]
    filter_ids = [a for a in args if not a.startswith("--")]

    checks = CHECKS
    if filter_ids:
        checks = [c for c in CHECKS if c["id"] in filter_ids]
        if not checks:
            print(f"No checks matched: {filter_ids}")
            sys.exit(1)

    results = {PASS: 0, FAIL: 0, ERR: 0}
    run_results = []

    print(f"Running {len(checks)} check(s)...\n")

    for check in checks:
        try:
            failures = check["fn"]()
        except Exception as e:
            print(f"  {ERR}  {check['id']}  — {e}")
            results[ERR] += 1
            run_results.append({
                "id": check["id"], "title": check["title"],
                "status": ERR, "failures": [], "error": str(e),
            })
            continue

        if failures:
            print(f"  {FAIL}  {check['id']}")
            for line in failures:
                print(line)
            results[FAIL] += 1
            run_results.append({
                "id": check["id"], "title": check["title"],
                "status": FAIL, "failures": failures, "error": None,
            })
        else:
            print(f"  {PASS}  {check['id']}")
            results[PASS] += 1
            run_results.append({
                "id": check["id"], "title": check["title"],
                "status": PASS, "failures": [], "error": None,
            })

    elapsed = (datetime.datetime.now() - started_at).total_seconds()
    total = sum(results.values())
    print(
        f"\n{total} checks — "
        f"{results[PASS]} passed  "
        f"{results[FAIL]} failed  "
        f"{results[ERR]} errors"
        f"  ({elapsed:.1f}s)"
    )

    write_report(run_results, started_at, "smoke", {
        PASS: render_pass,
        FAIL: render_fail,
        ERR: render_err,
    })

    sys.exit(0 if results[FAIL] == 0 and results[ERR] == 0 else 1)


if __name__ == "__main__":
    main()
