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

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIRS = ["base", "backend", "frontend", "stack"]

PASS = "PASS"
FAIL = "FAIL"
ERR  = "ERR "


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
    seen = {}  # id -> first file

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

    # collect all declared IDs
    declared = set()
    for filepath in all_template_files():
        content = read(filepath)
        for match in id_pattern.finditer(content):
            declared.add(match.group(1).strip())

    # check all refs
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

    manifest_path = os.path.join(ROOT, "manifest.yaml")
    if not os.path.isfile(manifest_path):
        return ["  manifest.yaml not found"]

    with io.open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    failures = []
    declared_ids = set()
    entries = []

    # collect all entries
    for section in manifest.values():
        if isinstance(section, list):
            for entry in section:
                if isinstance(entry, dict):
                    entries.append(entry)
                    if "id" in entry:
                        declared_ids.add(entry["id"])

    # check file paths exist
    for entry in entries:
        path = entry.get("file", "")
        if path and not os.path.isfile(os.path.join(ROOT, path)):
            failures.append(f"  file not found: '{path}' (id: {entry.get('id', '?')})")

    # check depends_on references resolve to declared IDs
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
    """Recursively collect all files reachable via DEPENDS ON."""
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
    chain = _collect_chain("stack/python-fastapi.md")
    required = [
        "stack/python-lib.md",
        "stack/python-service.md",
        "base/git.md",
        "base/docs.md",
        "base/quality.md",
        "backend/config.md",
        "backend/http.md",
        "backend/database.md",
        "backend/observability.md",
        "backend/quality.md",
        "backend/features.md",
        "backend/messaging.md",
    ]
    for req in required:
        if req not in chain:
            failures.append(f"  python-fastapi.md chain missing: '{req}'")
    return failures


# ---------------------------------------------------------------------------
# TPL-02 — EXTEND adds rules without removing base rules
# Verify that [EXTEND: base-testing] in python-flask.md has non-empty content
# and that base/testing.md [ID: base-testing] also has non-empty content.
# ---------------------------------------------------------------------------

def _extract_section(filepath, section_id):
    """Extract content lines immediately following an [ID: X] or [EXTEND: X] tag."""
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
            # stop at next heading or next [ID/EXTEND/OVERRIDE] or end
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
        os.path.join(ROOT, "base/testing.md"), "base-testing"
    )
    if not base_content:
        failures.append("  base/testing.md [ID: base-testing] section is empty")

    flask_content = _extract_section(
        os.path.join(ROOT, "stack/python-flask.md"), "base-testing"
    )
    if not flask_content:
        failures.append(
            "  stack/python-flask.md [EXTEND: base-testing] section is empty "
            "— base rules may have been lost"
        )

    return failures


# ---------------------------------------------------------------------------
# TPL-03 — OVERRIDE replaces parent section entirely
# Verify that go-service.md [OVERRIDE: go-lib-stack] has different content
# than go-lib.md [ID: go-lib-stack] — the parent section is truly replaced.
# ---------------------------------------------------------------------------

def check_tpl_03():
    failures = []

    original = _extract_section(
        os.path.join(ROOT, "stack/go-lib.md"), "go-lib-stack"
    )
    override = _extract_section(
        os.path.join(ROOT, "stack/go-service.md"), "go-lib-stack"
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
# Test registry
# ---------------------------------------------------------------------------

CHECKS = [
    {
        "id": "SYS-01",
        "spec": "SAIT-SMK-SYS-01-001A",
        "title": "DEPENDS ON paths resolve to existing files",
        "fn": check_sys_01,
    },
    {
        "id": "SYS-02",
        "spec": "SAIT-SMK-SYS-02-001A",
        "title": "All section IDs unique across templates",
        "fn": check_sys_02,
    },
    {
        "id": "TPL-04",
        "spec": "SAIT-SMK-TPL-04-001A",
        "title": "All EXTEND/OVERRIDE refs point to existing IDs",
        "fn": check_tpl_04,
    },
    {
        "id": "MNF-01",
        "spec": "SAIT-INT-MNF-01-001A",
        "title": "Manifest entries reference valid paths and IDs",
        "fn": check_mnf_01,
    },
    {
        "id": "TPL-01",
        "spec": "SAIT-INT-TPL-01-001A",
        "title": "DEPENDS ON chain from python-fastapi.md is complete",
        "fn": check_tpl_01,
    },
    {
        "id": "TPL-02",
        "spec": "SAIT-INT-TPL-02-001A",
        "title": "EXTEND adds rules without removing base rules",
        "fn": check_tpl_02,
    },
    {
        "id": "TPL-03",
        "spec": "SAIT-INT-TPL-03-001A",
        "title": "OVERRIDE replaces parent section with different content",
        "fn": check_tpl_03,
    },
]


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def write_report(run_results, started_at):
    reports_dir = os.path.join(ROOT, "tests", "reports")
    os.makedirs(reports_dir, exist_ok=True)

    ts = started_at.strftime("%Y-%m-%dT%H-%M-%S")
    report_path = os.path.join(reports_dir, f"{ts}-smoke.md")

    passed  = sum(1 for r in run_results if r["status"] == PASS)
    failed  = sum(1 for r in run_results if r["status"] == FAIL)
    errored = sum(1 for r in run_results if r["status"] == ERR)
    total   = len(run_results)

    lines = [
        "# Smoke Test Report",
        "",
        f"**Date**: {started_at.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Runner**: run_smoke.py  ",
        f"**Checks run**: {total}",
        "",
        "## Summary",
        "",
        f"{total} checks — {passed} passed  {failed} failed  {errored} errors",
        "",
        "---",
        "",
        "## Results",
        "",
    ]

    for r in run_results:
        lines.append(f"### {r['status']}  {r['id']} — {r['title']}")
        lines.append("")
        if r["status"] == FAIL:
            lines.append("**Expected**: all assertions pass with no violations")
            lines.append("")
            lines.append("**Observed**:")
            lines.append("")
            lines.append("```")
            for line in r["failures"]:
                lines.append(line)
            lines.append("```")
            lines.append("")
        elif r["status"] == ERR:
            lines.append(f"**Error**: {r['error']}")
            lines.append("")

    with io.open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nReport: {os.path.relpath(report_path, ROOT)}")


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

    total = sum(results.values())
    print(
        f"\n{total} checks — "
        f"{results[PASS]} passed  "
        f"{results[FAIL]} failed  "
        f"{results[ERR]} errors"
    )

    write_report(run_results, started_at)

    sys.exit(0 if results[FAIL] == 0 and results[ERR] == 0 else 1)


if __name__ == "__main__":
    main()