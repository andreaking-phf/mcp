"""Generate src/respmcp/store/crosswalks/state_fips.csv.

Source: the `us` Python package (version pinned in pyproject.toml), which carries
Census FIPS codes and USPS abbreviations. Covers the 50 states, DC, and the five
inhabited territories that appear in NHSN data (AS, GU, MP, PR, VI).
To confirm against the Census reference file once census.gov is reachable
(docs/open-questions.md).

Run: uv run python scripts/gen_state_fips.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import us  # type: ignore[import-untyped]

OUT = Path(__file__).resolve().parents[1] / "src/respmcp/store/crosswalks/state_fips.csv"
TERRITORIES = ["AS", "GU", "MP", "PR", "VI"]


def main() -> None:
    rows = []
    for s in us.states.STATES_AND_TERRITORIES + [us.states.DC]:
        if s.is_territory and s.abbr not in TERRITORIES:
            continue
        kind = "territory" if s.is_territory else ("district" if s.abbr == "DC" else "state")
        rows.append((s.fips, s.abbr, s.name, kind))
    rows = sorted(set(rows))
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["state_fips", "usps_abbr", "name", "kind"])
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
