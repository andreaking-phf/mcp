"""Check the committed MMWR week table against the independent `epiweeks` package."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from epiweeks import Week

TABLE = Path(__file__).resolve().parents[2] / "src/respmcp/store/crosswalks/mmwr_weeks.csv"


def test_every_week_matches_epiweeks() -> None:
    with TABLE.open() as f:
        rows = list(csv.DictReader(f))
    assert rows, "mmwr_weeks.csv is empty"
    for row in rows:
        week = Week(int(row["mmwr_year"]), int(row["mmwr_week"]), system="CDC")
        assert week.startdate().isoformat() == row["week_start"], row
        assert week.enddate().isoformat() == row["week_end"], row


def test_weeks_are_contiguous_and_end_on_saturday() -> None:
    with TABLE.open() as f:
        rows = list(csv.DictReader(f))
    for prev, cur in zip(rows, rows[1:], strict=False):
        assert date.fromisoformat(cur["week_start"]).toordinal() == (
            date.fromisoformat(prev["week_end"]).toordinal() + 1
        )
    assert all(date.fromisoformat(r["week_end"]).weekday() == 5 for r in rows)


def test_known_week() -> None:
    # Week ending 2026-10-24 is the latest week in the 2026-10-31 live queries (plan Section 4).
    with TABLE.open() as f:
        match = [r for r in csv.DictReader(f) if r["week_end"] == "2026-10-24"]
    assert len(match) == 1
    expected = Week.fromdate(date(2026, 10, 24), system="CDC")
    assert match[0]["period_id"] == f"MMWR-{expected.year}-{expected.week:02d}" == "MMWR-2026-42"
