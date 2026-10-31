"""Enumerate every geography label used by S1 to S3 and map it to a geo_id.

Writes:
  src/respmcp/store/crosswalks/geo_aliases.csv   one row per (source_id, label_field, source_label)
  src/respmcp/store/crosswalks/county_hsa.csv    NSSP county FIPS -> HSA (decision 0011, proposed)
  docs/phase0/geography-check.md                 counts, unmapped labels, county versus state check

Inputs are files already on disk, so the result can be reproduced and audited:
  --nssp          rdmq-nq56 rows (CSV, CSV.xz, or SODA JSON)
  --nhsn          ua7e-t2fy rows (CSV export with display labels, or SODA JSON)
  --delphi-nhsn   Delphi nhsn rows with geo_type and geo_value columns
  --fluview       Delphi FluView rows with a region or geo_value column
  --evidence      short text saved with every row to say where the labels came from

Any label that cannot be mapped is written to the report and to docs/open-questions.md
by hand. This script never guesses a mapping.

Run (live raw files, once hosts are reachable):
  uv run python scripts/enumerate_geographies.py --nssp data/raw/... --evidence "live 2026-11-02"
"""

from __future__ import annotations

import argparse
import csv
import json
import lzma
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CROSSWALKS = ROOT / "src/respmcp/store/crosswalks"
REPORT = ROOT / "docs/phase0/geography-check.md"

ALIAS_COLUMNS = [
    "source_id",
    "source_signal_group",
    "label_field",
    "source_label",
    "geo_id",
    "geo_type",
    "evidence",
]


def read_any(path: Path) -> pd.DataFrame:
    """Read CSV, CSV.xz or JSON (a list of records) as all-text columns."""
    if path.suffix == ".json":
        return pd.DataFrame(json.loads(path.read_text())).astype("string")
    opener = lzma.open if path.suffix == ".xz" else open
    with opener(path, "rt") as f:  # type: ignore[operator]
        return pd.read_csv(f, dtype="string", keep_default_na=False)


def load_states() -> pd.DataFrame:
    return pd.read_csv(CROSSWALKS / "state_fips.csv", dtype="string")


def map_state_name(label: str, states: pd.DataFrame) -> tuple[str, str] | None:
    if label == "United States":
        return "US", "nation"
    hit = states[states["name"] == label]
    return (str(hit["state_fips"].iloc[0]), "state") if len(hit) == 1 else None


def map_state_abbr(label: str, states: pd.DataFrame) -> tuple[str, str] | None:
    up = label.upper()
    if up in {"USA", "US"}:
        return "US", "nation"
    if up.startswith("REGION "):
        number = up.removeprefix("REGION ").strip()
        if number.isdigit() and 1 <= int(number) <= 10:
            return f"hhs_{int(number)}", "hhs"
        return None
    hit = states[states["usps_abbr"] == up]
    return (str(hit["state_fips"].iloc[0]), "state") if len(hit) == 1 else None


def alias_rows(
    labels: list[str],
    source_id: str,
    group: str,
    field: str,
    mapper: str,
    states: pd.DataFrame,
    evidence: str,
) -> tuple[list[dict[str, str]], list[str]]:
    rows, unmapped = [], []
    for label in sorted(set(labels)):
        mapped = (map_state_name if mapper == "name" else map_state_abbr)(label, states)
        if mapped is None:
            unmapped.append(label)
            continue
        rows.append(
            {
                "source_id": source_id,
                "source_signal_group": group,
                "label_field": field,
                "source_label": label,
                "geo_id": mapped[0],
                "geo_type": mapped[1],
                "evidence": evidence,
            }
        )
    return rows, unmapped


def clean_fips(value: str, width: int) -> str:
    """CDC CSV exports print FIPS with thousands separators (for example "1,007")."""
    digits = value.replace(",", "").strip()
    return digits.zfill(width) if digits.isdigit() else ""


def nssp_checks(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Return the county -> HSA crosswalk and report lines for the county versus state check."""
    lines: list[str] = []
    state_rows = df[df["county"] == "All"]
    county_rows = df[df["county"] != "All"]
    lines.append(
        f"- Rows: {len(df):,} total; {len(state_rows):,} state or national (county = 'All'); "
        f"{len(county_rows):,} county."
    )
    if "trend_source" in df.columns:
        counts = df.groupby("trend_source").size().to_dict()
        lines.append(f"- trend_source values and row counts: {counts}.")

    key = ["geography", "county", "week_end"]
    dupes = int(df.duplicated(subset=key).sum())
    lines.append(f"- Duplicate rows on (geography, county, week_end): {dupes}.")

    value_cols = [c for c in df.columns if c.startswith("percent_visits_") and "smoothed" not in c]
    grouped = county_rows.groupby(["hsa_nci_id", "week_end"])[value_cols].nunique(dropna=False)
    sizes = county_rows.groupby(["hsa_nci_id", "week_end"]).size()
    multi = grouped[sizes > 1]
    differing = int((multi > 1).any(axis=1).sum())
    lines.append(
        f"- HSA-weeks with more than one county: {len(multi):,}. Of these, HSA-weeks where any "
        f"county's value differs from the others in the same HSA: {differing}."
    )
    if differing == 0:
        lines.append(
            "- Conclusion: county rows carry the value of their Health Service Area (HSA), "
            "repeated for every county in the HSA. Storing them as separate county observations "
            "would count the same number several times. See decision 0011."
        )

    cw = county_rows[["fips", "county", "geography", "hsa_nci_id", "hsa"]].drop_duplicates().copy()
    cw["county_fips"] = cw["fips"].map(lambda v: clean_fips(str(v), 5))
    cw = cw.rename(columns={"county": "county_name", "geography": "state_name", "hsa": "hsa_name"})
    cw = cw[["county_fips", "county_name", "state_name", "hsa_nci_id", "hsa_name"]]
    cw = cw.sort_values(["county_fips"]).drop_duplicates()
    bad = cw[cw["county_fips"] == ""]
    lines.append(
        f"- Distinct counties: {cw['county_fips'].nunique():,}; distinct HSAs: "
        f"{cw['hsa_nci_id'].nunique():,}; counties without a usable FIPS: {len(bad)}."
    )
    multi_hsa = cw.groupby("county_fips")["hsa_nci_id"].nunique()
    lines.append(f"- Counties assigned to more than one HSA: {int((multi_hsa > 1).sum())}.")
    dow = pd.to_datetime(df["week_end"]).dt.day_name().value_counts().to_dict()
    lines.append(f"- Day of week of week_end: {dow}.")
    lines.append(f"- week_end range: {df['week_end'].min()} to {df['week_end'].max()}.")
    return cw, lines


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--nssp", type=Path)
    ap.add_argument("--nhsn", type=Path)
    ap.add_argument("--delphi-nhsn", type=Path)
    ap.add_argument("--fluview", type=Path)
    ap.add_argument("--evidence", required=True)
    args = ap.parse_args()

    states = load_states()
    aliases: list[dict[str, str]] = []
    report = ["# Phase 0 geography check", "", f"Evidence: {args.evidence}", ""]
    unmapped_all: dict[str, list[str]] = {}

    if args.nssp:
        df = read_any(args.nssp)
        labels = df.loc[df["county"] == "All", "geography"].tolist()
        rows, unmapped = alias_rows(
            labels, "cdc_socrata", "rdmq-nq56", "geography", "name", states, args.evidence
        )
        aliases += rows
        unmapped_all["cdc_socrata rdmq-nq56.geography"] = unmapped
        cw, lines = nssp_checks(df)
        cw.to_csv(CROSSWALKS / "county_hsa.csv", index=False)
        report += ["## NSSP (rdmq-nq56): county versus state", ""] + lines + [""]

    if args.nhsn:
        df = read_any(args.nhsn)
        field = "jurisdiction" if "jurisdiction" in df.columns else "Geographic aggregation"
        rows, unmapped = alias_rows(
            df[field].tolist(),
            "cdc_socrata",
            "ua7e-t2fy",
            "jurisdiction",
            "abbr",
            states,
            args.evidence,
        )
        aliases += rows
        unmapped_all["cdc_socrata ua7e-t2fy.jurisdiction"] = unmapped
        date_field = "weekendingdate" if "weekendingdate" in df.columns else "Week Ending Date"
        dow = pd.to_datetime(df[date_field]).dt.day_name().value_counts().to_dict()
        report += [
            "## NHSN (ua7e-t2fy)",
            "",
            f"- Distinct jurisdiction labels: {df[field].nunique()}.",
            f"- Day of week of {date_field}: {dow}.",
            "",
        ]

    for path, group in ((args.delphi_nhsn, "nhsn"), (args.fluview, "fluview_ilinet")):
        if not path:
            continue
        df = read_any(path)
        field = "geo_value" if "geo_value" in df.columns else "region"
        labels = [v for v in df[field].tolist() if v != "nat"]
        rows, unmapped = alias_rows(
            labels, "delphi_v5", group, field, "abbr", states, args.evidence
        )
        if "nat" in set(df[field]):
            rows.append(
                {
                    "source_id": "delphi_v5",
                    "source_signal_group": group,
                    "label_field": field,
                    "source_label": "nat",
                    "geo_id": "US",
                    "geo_type": "nation",
                    "evidence": args.evidence,
                }
            )
        aliases += rows
        unmapped_all[f"delphi_v5 {group}.{field}"] = unmapped

    report += ["## Unmapped labels", ""]
    for where, labels in unmapped_all.items():
        report.append(f"- {where}: {', '.join(labels) if labels else 'none'}")

    out = CROSSWALKS / "geo_aliases.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ALIAS_COLUMNS)
        w.writeheader()
        w.writerows(sorted(aliases, key=lambda r: tuple(r[c] for c in ALIAS_COLUMNS)))
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(report) + "\n")
    print(f"Wrote {len(aliases)} aliases to {out}\nWrote {REPORT}")


if __name__ == "__main__":
    main()
