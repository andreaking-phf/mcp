# 0008 Exact package pins and a lockfile

Status: Proposed (review item S8). Implemented in pyproject.toml; reverse if declined.

Context. duckdb 2.0.0 (released 2026-10-21) and mcp 2.3.0 (2026-10-02) are new major lines. Open version ranges can pull in breaking changes between runs.

Decision. Pin exact versions in `pyproject.toml` and commit `uv.lock`. Versions resolved from PyPI on 2026-10-31: duckdb 2.0.0, mcp 2.3.0, httpx 0.28.1, pandas 3.1.0, pyarrow 26.0.0, python-dotenv 1.2.4, pydantic 2.14.2. Dev: pytest 9.2.0, ruff 0.17.3, mypy 2.4.1, epiweeks 2.4.0, us 4.0.0.

Note. pandas 3.1.0 is a new major version. The plan's pin was `pandas>=2.2`, which allows it. pandas 3 changes default string handling; adapters read all source columns as text and convert explicitly, so this does not affect results.

Consequences. Upgrades happen one package at a time in their own PR.
