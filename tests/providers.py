"""LLM provider backends for e2e tests.

Select via E2E_PROVIDER env var: anthropic, gemini, claude-cli.
Default: gemini (free tier available).
"""

import os
import subprocess


MAX_TOKENS = 8192
TIMEOUT = 180


def _anthropic(prompt):
    """Call Anthropic Messages API. Requires ANTHROPIC_API_KEY."""
    import anthropic
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
        timeout=TIMEOUT,
    )
    return response.content[0].text


def _gemini(prompt):
    """Call Google Gemini API. Requires GEMINI_API_KEY."""
    from google import genai
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"max_output_tokens": MAX_TOKENS, "temperature": 0},
    )
    return response.text


def _claude_cli(prompt):
    """Call Claude via CLI. Uses Pro subscription, no API credits."""
    result = subprocess.run(
        "claude -p --no-session-persistence",
        input=prompt,
        capture_output=True,
        timeout=TIMEOUT,
        encoding="utf-8",
        errors="replace",
        shell=True,
    )
    if not result.stdout.strip():
        raise RuntimeError(
            "claude CLI returned empty output — "
            "check that Claude Code is installed and authenticated"
        )
    return result.stdout


PROVIDERS = {
    "anthropic": _anthropic,
    "gemini": _gemini,
    "claude-cli": _claude_cli,
}

DEFAULT_PROVIDER = "gemini"


def get_provider():
    """Return the configured provider function."""
    name = os.environ.get("E2E_PROVIDER", DEFAULT_PROVIDER)
    if name not in PROVIDERS:
        raise ValueError(
            f"Unknown E2E_PROVIDER={name!r}. "
            f"Options: {', '.join(PROVIDERS)}"
        )
    return name, PROVIDERS[name]
