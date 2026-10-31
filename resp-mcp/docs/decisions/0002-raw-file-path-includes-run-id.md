# 0002 Raw file path includes the ingest run ID

Status: Accepted (review item B1, approved 2026-10-31)

Context. Plan Section 5 saves raw files to `data/raw/<source_id>/<YYYY-MM-DD>/<measure_id>_<geo_type>.json`. Two runs on the same day would write to the same path, which breaks the rule that raw files are never modified.

Decision. Raw files go to `data/raw/<source_id>/<YYYY-MM-DD>/<ingest_run_id>/<request_name>.json`, where `request_name` names the request (for example `rdmq-nq56_state` or `nssp_pct_ed_visits_covid_state`). Next to each raw file the adapter writes `<request_name>.meta.json` with the request URL, HTTP status, elapsed time, `retrieved_at`, `ingest_run_id`, and, for Socrata, the dataset's `rowsUpdatedAt`. `normalize` reads both files, so it stays a pure function of what is on disk (review item S5).

Consequences. Raw files are write-once. The adapter refuses to write if the path already exists.
