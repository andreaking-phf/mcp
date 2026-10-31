# Phase 0 geography check

Evidence: PopHIVE/Ingest copy, commit 9efff24 (2026-10-31); not a live pull

## NSSP (rdmq-nq56): county versus state

- Rows: 676,916 total; 11,024 state or national (county = 'All'); 665,892 county.
- trend_source values and row counts: {'HSA': 665892, 'State': 10812, 'United States': 212}.
- Duplicate rows on (geography, county, week_end): 0.
- HSA-weeks with more than one county: 160,908. Of these, HSA-weeks where any county's value differs from the others in the same HSA: 0.
- Conclusion: county rows carry the value of their Health Service Area (HSA), repeated for every county in the HSA. Storing them as separate county observations would count the same number several times. See decision 0011.
- Distinct counties: 3,141; distinct HSAs: 949; counties without a usable FIPS: 0.
- Counties assigned to more than one HSA: 0.
- Day of week of week_end: {'Saturday': 676916}.
- week_end range: 2022-10-01 to 2026-10-17.

## NHSN (ua7e-t2fy)

- Distinct jurisdiction labels: 67.
- Day of week of Week Ending Date: {'Saturday': 21775}.

## Unmapped labels

- cdc_socrata rdmq-nq56.geography: none
- cdc_socrata ua7e-t2fy.jurisdiction: none
- delphi_v5 nhsn.geo_value: none
- delphi_v5 fluview_ilinet.region: none
