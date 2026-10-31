"""Phase 0 live checks. Run once the environment can reach the data hosts.

Every response is saved under data/raw/phase0/<date>/ before it is read, and the
findings are written to docs/phase0/live-verification-<date>.md. Nothing here is
loaded into DuckDB.

Checks (plan Sections 3, 4, 6 and decisions 0006, 0007, 0011):
  1. Socrata metadata for each pilot dataset: rowsUpdatedAt and column names versus the plan.
  2. rdmq-nq56: day of week of week_end; county versus HSA duplication in the latest 8 weeks.
  3. ua7e-t2fy: day of week of weekendingdate; jurisdiction labels.
  4. mpgq-jmmr: updated in the last 14 days?
  5. atcp-73re: distinct pathogen_target values.
  6. r8kw-7aab: column list (looking for a provisional flag).
  7. Delphi V5 metadata: whether *_prelim NHSN signals exist.
  8. Delphi V5 fluview_ilinet at state level: is wili equal to ili?

Run: RESPMCP_LIVE=1 uv run python scripts/verify_endpoints.py
"""

from __future__ import annotations

import json
import os
import time
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()
RAW = ROOT / "data/raw/phase0" / TODAY
REPORT = ROOT / f"docs/phase0/live-verification-{TODAY}.md"

PLAN_COLUMNS = {
    ("data.cdc.gov", "rdmq-nq56"): [
        "week_end",
        "geography",
        "county",
        "fips",
        "hsa_nci_id",
        "percent_visits_covid",
        "percent_visits_influenza",
        "percent_visits_rsv",
        "percent_visits_combined",
        "ed_trends_covid",
    ],
    ("data.cdc.gov", "ua7e-t2fy"): [
        "jurisdiction",
        "weekendingdate",
        "totalconfc19newadm",
        "totalconfflunewadm",
        "totalconfrsvnewadm",
        "totalconfc19hosppats",
        "totalconffluhosppats",
        "totalconfrsvhosppats",
    ],
    ("data.cdc.gov", "mpgq-jmmr"): [],
    ("data.cdc.gov", "atcp-73re"): [
        "state_territory",
        "site",
        "week_end",
        "pathogen_target",
        "site_wval",
        "site_wval_category",
        "date_updated",
    ],
    ("data.cdc.gov", "kvib-3txy"): [
        "surveillance_network",
        "season",
        "date",
        "date_type",
        "age_category",
        "race",
        "sex",
        "state",
        "rate_type",
        "data_type",
        "estimate_type",
        "estimate",
    ],
    ("data.cdc.gov", "r8kw-7aab"): [
        "week_ending_date",
        "state",
        "group",
        "mmwr_week",
        "covid_19_deaths",
        "influenza_deaths",
        "pneumonia_deaths",
        "pneumonia_influenza_or_covid_19_deaths",
        "total_deaths",
    ],
    ("health.data.ny.gov", "jr8b-6gh6"): [
        "season",
        "region",
        "county",
        "fips",
        "cdcweek",
        "weekendingdate",
        "disease",
        "count",
    ],
}

DELPHI = "https://delphi.cmu.edu/epidata/v5"


class Checker:
    def __init__(self) -> None:
        load_dotenv(ROOT / ".env")
        headers = {}
        if token := os.getenv("SOCRATA_APP_TOKEN"):
            headers["X-App-Token"] = token
        self.socrata = httpx.Client(headers=headers, timeout=60)
        dh = {}
        if key := os.getenv("DELPHI_API_KEY"):
            dh["Authorization"] = f"Bearer {key}"
        self.delphi = httpx.Client(headers=dh, timeout=120)
        self.delphi_keyed = bool(dh)
        self.lines: list[str] = []
        RAW.mkdir(parents=True, exist_ok=True)

    def get(
        self, client: httpx.Client, name: str, url: str, params: dict[str, str] | None = None
    ) -> Any:
        path = RAW / f"{name}.json"
        if path.exists():
            raise FileExistsError(f"{path} already exists; raw files are write-once")
        resp = client.get(url, params=params)
        meta = {
            "url": str(resp.url),
            "status": resp.status_code,
            "retrieved_at": datetime.now(UTC).isoformat(),
        }
        path.write_bytes(resp.content)
        (RAW / f"{name}.meta.json").write_text(json.dumps(meta, indent=2))
        resp.raise_for_status()
        if client is self.delphi and not self.delphi_keyed:
            time.sleep(21)  # anonymous snapshot limit is 3 per minute
        return resp.json()

    def say(self, text: str) -> None:
        print(text)
        self.lines.append(text)

    def socrata_rows(self, domain: str, ds: str, name: str, **params: str) -> list[dict[str, Any]]:
        params.setdefault("$limit", "50000")
        rows: list[dict[str, Any]] = self.get(
            self.socrata, name, f"https://{domain}/resource/{ds}.json", params
        )
        return rows

    def run(self) -> None:
        self.say(f"# Phase 0 live verification, {TODAY}\n")
        self.say("## 1. Socrata metadata\n")
        for (domain, ds), expected in PLAN_COLUMNS.items():
            m = self.get(self.socrata, f"meta_{ds}", f"https://{domain}/api/views/{ds}.json")
            updated = datetime.fromtimestamp(m.get("rowsUpdatedAt", 0), UTC).date().isoformat()
            cols = [c["fieldName"] for c in m.get("columns", [])]
            missing = [c for c in expected if c not in cols]
            self.say(
                f"- {domain} {ds}: rowsUpdatedAt {updated}; columns missing versus plan: "
                f"{missing or 'none'}"
            )
            if ds in {"r8kw-7aab", "mpgq-jmmr"}:
                self.say(f"  - all columns: {', '.join(cols)}")
            if ds == "mpgq-jmmr":
                age = (date.today() - date.fromisoformat(updated)).days
                self.say(f"  - mpgq-jmmr last updated {age} days ago; current = {age <= 14}")

        self.say("\n## 2. rdmq-nq56 week day and county versus HSA\n")
        rows = self.socrata_rows(
            "data.cdc.gov",
            "rdmq-nq56",
            "rdmq-nq56_recent",
            **{"$where": "week_end >= '" + self._weeks_ago(8) + "'"},
        )
        days = {datetime.fromisoformat(r["week_end"][:10]).strftime("%A") for r in rows}
        self.say(f"- rows {len(rows)}; week_end days of week: {sorted(days)}")
        groups: dict[tuple[str, str], set[str]] = {}
        for r in rows:
            if r.get("county") != "All" and r.get("hsa_nci_id"):
                key = (r["hsa_nci_id"], r["week_end"])
                groups.setdefault(key, set()).add(str(r.get("percent_visits_covid")))
        differing = sum(1 for v in groups.values() if len(v) > 1)
        self.say(f"- HSA-weeks: {len(groups)}; with differing county values: {differing}")
        sample_fips = sorted({str(r.get("fips")) for r in rows})[:5]
        self.say(f"- sample fips values in JSON (check for thousands separators): {sample_fips}")

        self.say("\n## 3. ua7e-t2fy\n")
        rows = self.socrata_rows(
            "data.cdc.gov",
            "ua7e-t2fy",
            "ua7e-t2fy_recent",
            **{"$where": "weekendingdate >= '" + self._weeks_ago(8) + "'"},
        )
        days = {datetime.fromisoformat(r["weekendingdate"][:10]).strftime("%A") for r in rows}
        self.say(f"- weekendingdate days of week: {sorted(days)}")
        self.say(f"- jurisdictions: {' '.join(sorted({r['jurisdiction'] for r in rows}))}")

        self.say("\n## 5. atcp-73re pathogen_target values\n")
        rows = self.socrata_rows(
            "data.cdc.gov",
            "atcp-73re",
            "atcp-73re_targets",
            **{"$select": "pathogen_target, count(*)", "$group": "pathogen_target"},
        )
        self.say(f"- {rows}")

        self.say("\n## 7. Delphi V5 metadata (NHSN _prelim signals)\n")
        meta = self.get(self.delphi, "delphi_metadata", f"{DELPHI}/metadata/")
        text = json.dumps(meta)
        for sig in (
            "confirmed_admissions_covid_ew_prelim",
            "confirmed_admissions_flu_ew_prelim",
            "confirmed_admissions_rsv_ew_prelim",
        ):
            self.say(f"- {sig} listed: {sig in text}")

        self.say("\n## 8. Delphi V5 fluview_ilinet at state level: wili versus ili\n")
        out = {}
        for sig in ("wili", "ili"):
            data = self.get(
                self.delphi,
                f"delphi_fluview_{sig}_state",
                f"{DELPHI}/snapshot/",
                {"source": "fluview_ilinet", "signal": sig, "geo_type": "state"},
            )
            records = data if isinstance(data, list) else data.get("epidata", data.get("data", []))
            out[sig] = {(r.get("geo_value"), r.get("time_value")): r.get("value") for r in records}
        shared = set(out["wili"]) & set(out["ili"])
        same = sum(1 for k in shared if out["wili"][k] == out["ili"][k])
        self.say(f"- state rows compared: {len(shared)}; wili equal to ili: {same}")
        self.say(
            f"- Delphi state geo_value labels: {' '.join(sorted({str(k[0]) for k in out['ili']}))}"
        )

        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text("\n".join(self.lines) + "\n")
        print(f"\nWrote {REPORT}")

    @staticmethod
    def _weeks_ago(n: int) -> str:
        return date.fromordinal(date.today().toordinal() - 7 * n).isoformat()


if __name__ == "__main__":
    if os.getenv("RESPMCP_LIVE") != "1":
        raise SystemExit("Set RESPMCP_LIVE=1 to run live checks.")
    Checker().run()
