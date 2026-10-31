# 0004 Revision rows are inserted only when the value or status changes

Status: Accepted (review item B3, approved 2026-10-31)

Context. The `revision` primary key ends in `report_date`. Two runs that see the same `report_date` would fail on insert, and re-running a day would duplicate history.

Decision. `load.py` inserts a revision row only when no row exists for the same key and `report_date`. If a row exists with a different value or status for the same key and `report_date`, the load stops and the conflict is written to `docs/open-questions.md`, because a publisher changing a value without changing its update date needs a human look.

Consequences. Phase 2 reconciliation reads: every raw row maps to exactly one revision row, or to an existing identical row (counted and reported as "unchanged"). Re-running an ingest is safe.
