# 0003 Socrata report_date comes from the dataset's rowsUpdatedAt

Status: Accepted (review item B2, approved 2026-10-31)

Context. The plan set `report_date` for Socrata rows to the day of download. That makes Freshness look perfect even when CDC has not updated the dataset for weeks (for example r8kw-7aab rows were last updated 2026-10-08 though described as weekly).

Decision. For Socrata sources, `report_date` is the date part of `rowsUpdatedAt` from `https://<domain>/api/views/<id>.json`, fetched in the same ingest run and saved in the meta file. `retrieved_at` remains the download time. Delphi rows keep the report time that Delphi returns.

Consequences. Freshness measures the publisher, not our schedule. If the metadata call fails, the ingest run is marked `partial` and rows are not loaded, rather than falling back to the download date.
