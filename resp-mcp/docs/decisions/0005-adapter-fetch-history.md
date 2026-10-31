# 0005 Adapter protocol gains an optional fetch_history method

Status: Accepted (review item B4, approved 2026-10-31)

Context. Plan Section 5 limits adapters to `fetch`, `normalize`, `describe`, but Phase 3a needs Delphi's `archive/` route for revision volatility.

Decision. Add `fetch_history(measure_id, geo_type, start, end) -> RawResponse | None`. Delphi implements it with `archive/` and `report_time_query`. Socrata adapters return `None` because Socrata keeps no history.

Consequences. Revision volatility is computable for Delphi signals from day one and for Socrata only after enough ingest runs accumulate (as the plan already says).
