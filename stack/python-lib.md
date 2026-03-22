# Stack — Python Library / CLI
[DEPENDS ON: base/git.md, base/docs.md, base/quality.md]

A Python library, CLI tool, or shared package intended to be imported or
installed. No web server, no frontend. May be published to PyPI.

---

## Stack
[ID: python-lib-stack]

- Language: Python 3.11+
- Package manager: [pip / uv / poetry]
- Build backend: [hatchling / setuptools / flit]
- Linter: ruff
- Formatter: ruff format
- Type checker: mypy (strict mode)
- Test runner: pytest
- Distribution: [PyPI / internal / not distributed]

---

## Project structure
[ID: python-lib-structure]

```
src/
  [package]/
    __init__.py
    [module].py
tests/
  test_[module].py
pyproject.toml
README.md
CLAUDE.md
```

- Source layout (`src/`) — prevents accidental imports of the uninstalled package
- All public API exported from `__init__.py`
- No `setup.py` — use `pyproject.toml` only

---

## Code conventions
[ID: python-lib-conventions]

- Follow **PEP 8** for style — enforced by `ruff`; do not override ruff rules
  to work around style issues, fix the code instead
- Follow **PEP 257** for docstrings — Google docstring style; every public
  symbol MUST have a docstring
- Follow **PEP 484** and **PEP 526** for type annotations — all public
  functions and class members must be annotated
- No `Any` in public API — use specific types or `TypeVar`
- Keep functions small and single-purpose
- Raise specific exceptions — never bare `except:` or `except Exception:`
- No mutable default arguments

---

## Typing
[ID: python-lib-typing]

- Run mypy in strict mode: `mypy src/ --strict`
- Use `from __future__ import annotations` for forward references
- Prefer `collections.abc` types (`Sequence`, `Mapping`) over `list`, `dict`
  in public signatures
- Use `TypeAlias` for complex type aliases

---

## Testing
[EXTEND: base-testing]

- pytest for all tests
- Aim for 100% coverage of public API; use `# pragma: no cover` sparingly
- Use `pytest.mark.parametrize` for data-driven cases
- No mocks for pure functions — test with real inputs
- Component test naming: `test_<unit_of_work>_<state>_<expected>`
  e.g. `test_sum_negative_first_param_raises_value_error`
- Component tests in `tests/component/`, component integration tests in
  `tests/integration/`
- Run before every commit: `pytest && mypy src/ --strict`

---

## Packaging
[ID: python-lib-packaging]

- All metadata in `pyproject.toml` — no `setup.cfg`, no `setup.py`
- Pin minimum Python version in `requires-python`
- Do not pin exact versions in `dependencies` — use ranges (`>=`, `<`)
- Dev/test dependencies in `[project.optional-dependencies]` or `[dependency-groups]`
- Lock file for reproducibility: `requirements-dev.lock` or equivalent

---

## Git conventions
[EXTEND: base-git]

- Do not commit `.venv/`, `__pycache__/`, `*.egg-info/`, `dist/`, `.mypy_cache/`
- Tag releases and publish to PyPI from CI only — never from a local machine

---

## Commands
```
pip install -e ".[dev]"   # install with dev dependencies
pytest                    # run tests
mypy src/ --strict        # type check
ruff check src/ tests/    # lint
ruff format src/ tests/   # format
python -m build           # build distribution
```