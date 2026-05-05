"""LLM provider backends for e2e tests.

Select via E2E_PROVIDER env var: anthropic, gemini, claude-cli.
Default: gemini (free tier available).
"""

import os
import subprocess
import time


MAX_TOKENS = 65536
TIMEOUT = 180
MAX_RETRIES = 3
INITIAL_DELAY = 10


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


def _is_rate_limit(exc):
    """Check if an exception is a rate limit or temporary overload."""
    msg = str(exc).lower()
    return any(k in msg for k in ("429", "503", "rate", "overloaded", "unavailable"))


def _with_retry(fn):
    """Wrap a provider function with exponential backoff on rate limits."""
    def wrapper(prompt):
        delay = INITIAL_DELAY
        for attempt in range(MAX_RETRIES + 1):
            try:
                return fn(prompt)
            except Exception as exc:
                if attempt < MAX_RETRIES and _is_rate_limit(exc):
                    print(f"  rate limited, retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise
    return wrapper


def get_provider():
    """Return the configured provider function (with retry)."""
    name = os.environ.get("E2E_PROVIDER", DEFAULT_PROVIDER)
    if name not in PROVIDERS:
        raise ValueError(
            f"Unknown E2E_PROVIDER={name!r}. "
            f"Options: {', '.join(PROVIDERS)}"
        )
    return name, _with_retry(PROVIDERS[name])
