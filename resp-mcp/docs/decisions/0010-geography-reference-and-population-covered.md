# 0010 Geography reference list with population and population covered

Status: Accepted in principle (review item S1, approved 2026-10-31, with "add populations covered"). Field names below need confirmation.

Context. The Completeness score needs to know which geographies a measure should have. Andrea also asked to record population, and the population each source actually covers.

Decision. Add one reference file and table, `expected_geo`, built in Phase 0 and loaded in Phase 2:

| Field | Type | Meaning |
|---|---|---|
| source_id | TEXT | as in `source` |
| measure_id | TEXT | as in `measure` |
| geo_id | TEXT | as in `geography` |
| expected_from | TEXT | first period_id the source is expected to report this geography |
| population_covered | BIGINT | people covered by the source in this geography, when the source publishes it; NULL otherwise |
| population_covered_basis | TEXT | what the number is, in the source's words (for example "sewershed population served", "RESP-NET catchment population") |
| population_covered_source | TEXT | URL or dataset and column the number came from |
| population_covered_as_of | DATE | date of that number |

Total population stays on `geography.population` with `geography.population_source`, as in the plan, from the Census Bureau Population Estimates Program (vintage to be confirmed when census.gov is reachable).

For S1 to S3 none of the sources publishes a population covered figure that has been verified, so `population_covered` is NULL with basis "not published" until one is found. NHSN publishes the percent of hospitals reporting, which is coverage of facilities, not people; it is recorded for the Coverage score, not here.

Consequences. Coverage and Completeness are both explainable. A per-capita comparison can use either total population or population covered, and the tool response says which.
