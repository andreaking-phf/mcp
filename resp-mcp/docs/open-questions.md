# Open questions

Each item names who can answer it and what is blocked until then.

| # | Question | Blocks | Who | Status |
|---|---|---|---|---|
| 1 | The cloud build environment cannot reach data.cdc.gov, delphi.cmu.edu, health.data.ny.gov, or census.gov (proxy returns 403). Add these hosts to the environment's allowed domains, or run `scripts/verify_endpoints.py` on a local machine. | Phase 0 live checks; Phase 1 | Andrea | Open |
| 2 | Delphi API key and Socrata app token, registered under PubHealth Commons (decision 0001). | Phase 1 at full speed (anonymous Delphi limits work but are slow) | Andrea | Open |
| 3 | Approve field names for `expected_geo` (decision 0010). | Phase 2 schema | Andrea | Open |
| 4 | Approve storing NSSP county data once per Health Service Area (decision 0011). | Phase 1 NSSP adapter | Andrea | Open |
| 5 | Approve exact package pins (0008) and calling Delphi with httpx (0009). | Nothing (already in place; reversible) | Andrea | Open |
| 6 | Census population: which Population Estimates Program vintage and file to use for `geography.population` (state, county, HSA by summing counties). Confirm on census.gov once reachable. | Phase 2 population fields | Build agent, then Andrea | Open |
| 7 | PopHIVE MCP connector: not available in this Claude Code session. Test it in a claude.ai chat with the connector enabled: ask for NSSP ED visit percent and NHSN admissions for one state over 8 weeks, and note what it returns, its sources, and dates. | Decision on building S8 | Andrea (or a session with the connector) | Open |
| 8 | Jev connector: not available in this session. Confirm tool names, model version reported, and TypeSafe data retention terms (decision 0012). | Phase 5 | Andrea | Open |
| 9 | The geography labels in `geo_aliases.csv` came from PopHIVE's copies of the source files, not a live pull. For FluView, PopHIVE used Delphi's legacy endpoint, so the V5 `fluview_ilinet` labels still need a live check (does V5 split New York City from New York State?). | Phase 1 Delphi adapter | Build agent | Open |
| 10 | `state_fips.csv` comes from the `us` Python package. Cross-check against the Census FIPS reference file. | Low | Build agent | Open |
