"""Generate src/respmcp/store/crosswalks/mmwr_weeks.csv for MMWR years 2015 through 2030.

MMWR weeks run Sunday through Saturday. Week 1 of an MMWR year is the first week
that has at least four days in the calendar year, which is the same as the week
that contains January 4. A year has 52 or 53 weeks.

The output is committed. tests/unit/test_mmwr.py checks it against the independent
`epiweeks` package.

Run: uv run python scripts/gen_mmwr.py
"""

from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

FIRST_YEAR = 2015
LAST_YEAR = 2030
OUT = Path(__file__).resolve().parents[1] / "src/respmcp/store/crosswalks/mmwr_weeks.csv"


def week1_start(year: int) -> date:
    """Return the Sunday that starts MMWR week 1 of `year`."""
    jan4 = date(year, 1, 4)
    days_since_sunday = (jan4.weekday() + 1) % 7  # Python: Monday=0 ... Sunday=6
    return jan4 - timedelta(days=days_since_sunday)


def mmwr_weeks(year: int) -> list[tuple[str, int, int, date, date]]:
    start = week1_start(year)
    next_start = week1_start(year + 1)
    rows = []
    week = 1
    while start < next_start:
        rows.append((f"MMWR-{year}-{week:02d}", year, week, start, start + timedelta(days=6)))
        start += timedelta(days=7)
        week += 1
    return rows


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["period_id", "mmwr_year", "mmwr_week", "week_start", "week_end"])
        for year in range(FIRST_YEAR, LAST_YEAR + 1):
            for row in mmwr_weeks(year):
                w.writerow([row[0], row[1], row[2], row[3].isoformat(), row[4].isoformat()])
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
