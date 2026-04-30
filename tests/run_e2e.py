#!/usr/bin/env python3
"""
E2E test runner for solid-ai-templates.

Calls `claude -p` with prepared interview answers and stack templates,
then asserts required strings are present (and forbidden strings absent).

Usage:
  py tests/run_e2e.py                    # run all non-skipped tests
  py tests/run_e2e.py STK-01             # run one test by short ID
  py tests/run_e2e.py STK-01 FMT-01      # run multiple
  py tests/run_e2e.py --area=STK          # run all stack tests
  py tests/run_e2e.py --dry-run          # print prompt, skip claude call
  py tests/run_e2e.py --offline          # validate test infrastructure without API
  py tests/run_e2e.py --fail-fast        # stop on first failure

Offline mode validates:
  - All referenced template files exist and are non-empty
  - Each test has required fields (id, spec, stack, answers, required)
  - Prompts build successfully from templates + answers
  - No structural issues in the test suite

API cost estimate (live mode): ~$0.50–1.00 per full run (30 tests,
each sending ~10–20K tokens to Claude).
"""

import datetime
import os
import subprocess
import sys
import time

from lib import ROOT, PASS, FAIL, SKIP, ERR, REPORT_TRUNCATION, read, parse_args
from cases import ALL_TESTS


def build_prompt(stack_file, answers, output_file="formats/agents.md",
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


def validate_test_offline(test):
    """Validate test infrastructure without calling Claude."""
    failures = []

    for field in ("id", "spec", "stack", "answers", "required"):
        if field not in test:
            failures.append(f"  missing field: {field!r}")

    if failures:
        return FAIL, "\n".join(failures)

    stack_file = os.path.join(ROOT, test["stack"])
    if not os.path.isfile(stack_file):
        failures.append(f"  stack file missing: {test['stack']}")
    elif os.path.getsize(stack_file) == 0:
        failures.append(f"  stack file empty: {test['stack']}")

    output_file = test.get("output_file", "formats/agents.md")
    out_path = os.path.join(ROOT, output_file)
    if not os.path.isfile(out_path):
        failures.append(f"  output format missing: {output_file}")

    for ef in test.get("extra_files", ()):
        ef_path = os.path.join(ROOT, ef)
        if not os.path.isfile(ef_path):
            failures.append(f"  extra file missing: {ef}")

    if not test.get("required"):
        failures.append("  required list is empty")

    if not failures:
        try:
            prompt = build_prompt(
                test["stack"], test["answers"],
                output_file, test.get("extra_files", ()),
            )
            if len(prompt) < 100:
                failures.append(f"  prompt suspiciously short: {len(prompt)} chars")
        except Exception as e:
            failures.append(f"  prompt build failed: {e}")

    if failures:
        return FAIL, "\n".join(failures)
    return PASS, f"prompt {len(prompt)} chars, {len(test['required'])} assertions"


def run_test(test, dry_run=False, offline=False):
    tid = test["id"]

    if "skip" in test:
        return SKIP, test["skip"], None, None

    if offline:
        status, detail = validate_test_offline(test)
        return status, detail, None, None

    prompt = build_prompt(
        test["stack"], test["answers"],
        test.get("output_file", "formats/agents.md"),
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


def render_fail(r):
    lines = []
    elapsed_str = f"  ({r['elapsed']:.1f}s)" if r["elapsed"] else ""
    lines.append(f"### {r['status']}  {r['id']}{elapsed_str}")
    lines.append("")
    lines.append("**Expected**:")
    lines.append("")
    lines.append("```")
    for line in r["detail"].splitlines():
        lines.append(line)
    lines.append("```")
    lines.append("")
    lines.append(f"**Observed** (first {REPORT_TRUNCATION} chars of model output):")
    lines.append("")
    lines.append("```")
    observed = (r["output"] or "")[:REPORT_TRUNCATION].replace("```", "~~~")
    lines.append(observed)
    lines.append("```")
    lines.append("")
    return lines


def render_err(r):
    return [f"### {r['status']}  {r['id']}", "", f"**Error**: {r['detail']}", ""]


def render_skip(r):
    return [f"### {r['status']}  {r['id']}", "", f"**Skipped**: {r['detail']}", ""]


def render_pass(r):
    elapsed_str = f"  ({r['detail']})" if r["detail"] else ""
    return [f"### {r['status']}  {r['id']}{elapsed_str}", ""]


def write_report(run_results, started_at, dry_run):
    from lib import write_report as _write_report
    _write_report(run_results, started_at, "e2e", {
        PASS: render_pass,
        FAIL: render_fail,
        SKIP: render_skip,
        ERR: render_err,
    })


def main():
    started_at = datetime.datetime.now()

    filter_ids, flags, area = parse_args(sys.argv[1:])
    dry_run = "dry-run" in flags
    offline = "offline" in flags
    fail_fast = "fail-fast" in flags

    tests = ALL_TESTS
    if filter_ids:
        tests = [t for t in ALL_TESTS if t["id"] in filter_ids]
        if not tests:
            print(f"No tests matched: {filter_ids}")
            sys.exit(1)
    elif area:
        tests = [t for t in ALL_TESTS if t["id"].startswith(area)]
        if not tests:
            print(f"No tests matched area: {area}")
            sys.exit(1)

    results = {PASS: 0, FAIL: 0, SKIP: 0, ERR: 0}
    run_results = []

    total = len(tests)
    print(f"Running {total} test(s)...\n")

    for i, test in enumerate(tests, 1):
        tid = test["id"]
        if not dry_run and not offline:
            print(f"  [{i}/{total}] {tid} running...", end="\r", flush=True)

        status, detail, elapsed, output = run_test(test, dry_run=dry_run, offline=offline)
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

        if fail_fast and status in (FAIL, ERR):
            print("\n  --fail-fast: stopping after first failure")
            break

    elapsed = (datetime.datetime.now() - started_at).total_seconds()
    total_run = sum(results.values())
    print(
        f"\n{total_run} tests — "
        f"{results[PASS]} passed  "
        f"{results[FAIL]} failed  "
        f"{results[SKIP]} skipped  "
        f"{results[ERR]} errors"
        f"  ({elapsed:.1f}s)"
    )

    write_report(run_results, started_at, dry_run or offline)

    sys.exit(0 if results[FAIL] == 0 and results[ERR] == 0 else 1)


if __name__ == "__main__":
    main()
