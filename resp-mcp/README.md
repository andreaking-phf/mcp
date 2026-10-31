# resp-mcp

Public respiratory virus surveillance data (COVID-19, influenza, RSV) from CDC and Delphi,
harmonized into one DuckDB file with provenance and a quality score on every value, and served
to Claude or any MCP client.

Status: **Phase 0 (verify and scaffold).** No data is ingested yet. See
`docs/plan-review-and-approach.md` for the build plan and `docs/open-questions.md` for what is
waiting on a decision.

## Quick start

Requires Python 3.11 or newer and [uv](https://docs.astral.sh/uv/).

```bash
cd resp-mcp
uv sync
cp .env.example .env    # then add your Delphi key and Socrata token
uv run respmcp --help
uv run pytest
```

## Where things are

| Path | What it is |
|---|---|
| `docs/technical-plan.md` | The full design. Start here. |
| `docs/decisions/` | Changes to the plan, one file each. These override the plan. |
| `docs/endpoint-verification.md` | Every source identifier, with the page it was confirmed on. |
| `docs/phase0/` | Phase 0 check results. |
| `docs/open-questions.md` | Anything waiting on a person. |
| `src/respmcp/store/crosswalks/` | Reference files: MMWR weeks, state FIPS codes, source geography labels, county to Health Service Area. |
| `scripts/` | One-off generators and the live verification script. |

## Phase 0 scripts

```bash
uv run python scripts/gen_mmwr.py            # MMWR week table, 2015 to 2030
uv run python scripts/gen_state_fips.py      # state and territory FIPS codes
RESPMCP_LIVE=1 uv run python scripts/verify_endpoints.py   # live checks; needs network access
```

## Data use

All sources are public aggregate data. No personal health information is collected. Values are
provided as published by each source, with that source's definitions and caveats.
