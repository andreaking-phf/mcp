# 0007 Where preliminary status comes from

Status: Accepted in principle (review item B6, approved 2026-10-31). Final choice waits on the live check.

Context. The Provisional component of the quality score needs to know which values are preliminary. The plan points to NHSN's preliminary dataset mpgq-jmmr, but no phase ingests it, and its rows were last updated 2026-09-30 although it says it updates weekly on Wednesdays. Delphi also publishes NHSN signals with a `_prelim` suffix (per PopHIVE processing documentation; not yet confirmed on Delphi's V5 signal page).

Decision. `scripts/verify_endpoints.py` checks (a) whether mpgq-jmmr has been updated in the last 14 days and (b) whether Delphi V5 lists `confirmed_admissions_covid_ew_prelim` and its flu and RSV versions. Use whichever is current, Delphi first if both are. If neither is current, the Provisional component is marked unavailable for NHSN with the flag `component_unavailable:provisional`, and the reason is recorded here.

Consequences. Preliminary values are stored with `value_status = 'preliminary'` and are replaced in `observation` when the final value arrives. Both versions stay in `revision`.
