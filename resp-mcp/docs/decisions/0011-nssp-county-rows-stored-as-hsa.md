# 0011 NSSP county rows are stored once per Health Service Area

Status: Proposed. Needs Andrea's decision (follows from "include county data, check for duplication with state data").

Context. In rdmq-nq56, county rows have `trend_source = 'HSA'`. In the PopHIVE copy (676,916 rows through week ending 2026-10-17), every county in the same Health Service Area (HSA) has the same value in every week: 0 differences across 160,908 HSA-weeks with more than one county. So the county value is the HSA value repeated. There are 3,141 counties in 949 HSAs; no county belongs to more than one HSA. State rows (`county = 'All'`) are separate numbers and do not duplicate county rows.

Options.
1. Store one observation per HSA (`geo_type = 'hsa'`, `geo_id = 'hsa_<hsa_nci_id>'`), and keep `county_hsa.csv` so a user can look up any county. Recommended: no repeated values, honest about the true geography.
2. Store one observation per county with a flag `value_is_hsa_level`. Easy county lookups, but repeated numbers and a risk of someone summing or averaging them.

Decision (proposed). Option 1. `query_measure` accepts a county FIPS and answers with that county's HSA row, labeled as HSA level. Delphi's `nssp` county signals are checked the same way on the first live pull.

Consequences. Adds `hsa` to `geo_type`, and adds `county_hsa.csv` with fields county_fips, county_name, state_name, hsa_nci_id, hsa_name.
