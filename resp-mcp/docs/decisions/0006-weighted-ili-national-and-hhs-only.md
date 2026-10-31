# 0006 Weighted ILI is national and HHS region only

Status: Accepted (review item B5, approved 2026-10-31). Evidence below is secondhand; confirm on the first live pull.

Context. CDC weights ILI by state population only when combining states into regions and the nation. Delphi's FluView data carries a `wili` value for states anyway.

Evidence. In the PopHIVE/Ingest copy of Delphi FluView data (legacy endpoint, commit 9efff24, pulled 2026-10-31), `wili` equals `ili` in 100% of 41,425 state rows and in 0% of 1,422 national rows. So the state `wili` is a copy of unweighted ILI, not a separate measure.

Decision. `ili_pct_weighted` is loaded for `nation` and `hhs` geographies only. At state level only `ili_pct_unweighted` and `ili_count` are loaded. `scripts/verify_endpoints.py` repeats the check on the V5 `fluview_ilinet` source.

Consequences. No state-level row ever claims to be weighted. Expected geographies for `ili_pct_weighted` are US plus hhs_1 to hhs_10.
