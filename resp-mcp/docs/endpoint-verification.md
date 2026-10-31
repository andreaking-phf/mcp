# Verified endpoint and package facts for the respiratory surveillance pipeline

Verified 2026-10-31 by opening each page listed. Every fact is followed by the URL it was read from. Items marked **unverified** could not be confirmed from a page that was opened. Catalog searches on data.cdc.gov and health.data.ny.gov were run through the Socrata Discovery API (api.us.socrata.com/api/catalog/v1), and each dataset was then opened through its /api/views/\<id\>.json metadata page, so IDs, titles, column names and update frequencies come from the platform itself.

## 1. Delphi Epidata (CMU Delphi)

### API versions and base URLs

- **V5 is the current, recommended API.** The intro page states: "The legacy V4 API (including the COVIDcast endpoint and other /epidata/ endpoint) is being phased out" and "We recommend using the Delphi V5 API for active and new projects." [https://cmu-delphi.github.io/delphi-epidata/](https://cmu-delphi.github.io/delphi-epidata/)

- **V5 base URL:** https://delphi.cmu.edu/epidata/v5/ with routes snapshot/, archive/, metadata/, aux_data/. Interactive docs: https://delphi.cmu.edu/epidata/v5/docs. [https://cmu-delphi.github.io/delphi-epidata/api/v5_api_queries.html](https://cmu-delphi.github.io/delphi-epidata/api/v5_api_queries.html) [https://cmu-delphi.github.io/delphi-epidata/api/v5.html](https://cmu-delphi.github.io/delphi-epidata/api/v5.html)

- **Legacy V4 COVIDcast base URL:** https://api.delphi.cmu.edu/epidata/covidcast/. Legacy V3 endpoints live at https://api.delphi.cmu.edu/epidata/\<endpoint\>/. [https://cmu-delphi.github.io/delphi-epidata/api/v5_migration.html](https://cmu-delphi.github.io/delphi-epidata/api/v5_migration.html)

- **Migration timeline:** "The V3/V4 to V5 migration is tentatively scheduled for October 2026." V3/V4 sources keep running until migration completes; endpoints that stop being updated remain accessible on V3/V4. No hard shutdown date is published. [https://cmu-delphi.github.io/delphi-epidata/api/v5_migration.html](https://cmu-delphi.github.io/delphi-epidata/api/v5_migration.html)

- **V4 -\> V5 parameter mapping:** data_source -\> source; as_of -\> snapshot_date (snapshot route); issues -\> report_time_query (archive route); covidcast_meta -\> metadata/; lag has no V5 equivalent (compute report_time - reference_time client-side). [https://cmu-delphi.github.io/delphi-epidata/api/v5_migration.html](https://cmu-delphi.github.io/delphi-epidata/api/v5_migration.html)

- **V5 snapshot required parameters:** source, signal, geo_type. Example: https://delphi.cmu.edu/epidata/v5/snapshot/?source=nhsn&signal=confirmed_admissions_covid_ew&geo_type=state&snapshot_date=2024-12-07 Archive example: https://delphi.cmu.edu/epidata/v5/archive/?source=nssp&signal=pct_ed_visits_influenza&geo_type=state&report_time_query=\<2025-10-16 [https://cmu-delphi.github.io/delphi-epidata/api/v5_api_queries.html](https://cmu-delphi.github.io/delphi-epidata/api/v5_api_queries.html) [https://cmu-delphi.github.io/delphi-epidata/api/v5_migration.html](https://cmu-delphi.github.io/delphi-epidata/api/v5_migration.html)

### Python clients

- **Current client: epidatpy.** The clients page says to install from GitHub (pip install "git+https://github.com/cmu-delphi/epidatpy.git#egg=epidatpy") and that it "will soon be available on PyPI as" epidatpy. [https://cmu-delphi.github.io/delphi-epidata/api/client_libraries.html](https://cmu-delphi.github.io/delphi-epidata/api/client_libraries.html)

- PyPI already has epidatpy 0.5.1, released June 18, 2026 (pip install epidatpy). Whether that PyPI release supports V5 routes is **unverified** (the migration guide says only that the *legacy* client will not get V5 updates; see [https://cmu-delphi.github.io/epidatpy/migration-guide.html](https://cmu-delphi.github.io/epidatpy/migration-guide.html), not opened). [https://pypi.org/project/epidatpy/](https://pypi.org/project/epidatpy/)

- **Legacy client: delphi-epidata** (pip install delphi-epidata), PyPI version 4.1.44 released Aug 18, 2026. The clients page says legacy clients are "discouraged"; the migration guide says the legacy Python client "supports only V4 and won't receive V5 updates." [https://cmu-delphi.github.io/delphi-epidata/api/client_libraries.html](https://cmu-delphi.github.io/delphi-epidata/api/client_libraries.html) [https://pypi.org/project/delphi-epidata/](https://pypi.org/project/delphi-epidata/) [https://cmu-delphi.github.io/delphi-epidata/api/v5_migration.html](https://cmu-delphi.github.io/delphi-epidata/api/v5_migration.html)

### API keys and rate limits

- Request a free key at https://api.delphi.cmu.edu/epidata/admin/registration_form (email required). [https://cmu-delphi.github.io/delphi-epidata/api/api_keys.html](https://cmu-delphi.github.io/delphi-epidata/api/api_keys.html)

- Without a key: 60 requests per hour; V5 adds 5/minute on /archive/ and 3/minute on /snapshot/; anonymous access is restricted to public datasets and "a maximum of two of the requested parameters having multiple selections." With a key: no rate limit and unlimited multiple selections. [https://cmu-delphi.github.io/delphi-epidata/api/api_keys.html](https://cmu-delphi.github.io/delphi-epidata/api/api_keys.html) [https://cmu-delphi.github.io/delphi-epidata/api/v5.html](https://cmu-delphi.github.io/delphi-epidata/api/v5.html) [https://cmu-delphi.github.io/delphi-epidata/](https://cmu-delphi.github.io/delphi-epidata/)

- Pass the key as query parameter api_key=..., or HTTP Basic auth (user epidata, password = key), or header Authorization: Bearer \<key\>. [https://cmu-delphi.github.io/delphi-epidata/api/api_keys.html](https://cmu-delphi.github.io/delphi-epidata/api/api_keys.html)

### Sources and signals (V5 names, exactly as documented)

| **Need**                 | **V5 source**  | **Example signal values**                                                                                                                                                                                                           | **geo_type values**                                                                      | **URL**                                                                                                                                                                 |
|--------------------------|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FluView ILINet           | fluview_ilinet | wili, ili, num_ili, num_providers, num_patients                                                                                                                                                                                     | state, census_division, hhs, nation                                                      | [https://cmu-delphi.github.io/delphi-epidata/api/v5-signals/fluview_ilinet.html](https://cmu-delphi.github.io/delphi-epidata/api/v5-signals/fluview_ilinet.html) |
| NSSP ED visit %          | nssp           | pct_ed_visits_covid, pct_ed_visits_influenza, pct_ed_visits_rsv, plus smoothed_pct_ed_visits_covid / \_influenza / \_rsv                                                                                                            | county, hsa_nci, hrr, msa, state, hhs, census_division, census_region, nation            | [https://cmu-delphi.github.io/delphi-epidata/api/v5-signals/nssp.html](https://cmu-delphi.github.io/delphi-epidata/api/v5-signals/nssp.html)                     |
| NWSS wastewater          | nwss           | Signals are \<pathogen\>\_\<metric\>: prefixes covid, flu, flu_h5, rsv, measles, mpox_all, mpox_clade_i, mpox_clade_ii, mpox_nvo; suffixes avg_conc, avg_conc_lin, flowpop_lin, mic_lin (e.g. covid_avg_conc_lin, rsv_avg_conc_lin) | sewershed only; site metadata at https://delphi.cmu.edu/epidata/v5/aux_data/?source=nwss | [https://cmu-delphi.github.io/delphi-epidata/api/v5-signals/nwss.html](https://cmu-delphi.github.io/delphi-epidata/api/v5-signals/nwss.html)                     |
| NHSN hospital admissions | nhsn           | confirmed_admissions_covid_ew, confirmed_admissions_flu_ew, confirmed_admissions_rsv_ew                                                                                                                                             | state, hhs, census_division, census_region, nation                                       | [https://cmu-delphi.github.io/delphi-epidata/api/v5-signals/nhsn.html](https://cmu-delphi.github.io/delphi-epidata/api/v5-signals/nhsn.html)                     |

- Legacy V3 FluView endpoint (still up, marked as being phased out): https://api.delphi.cmu.edu/epidata/fluview/?regions=nat&epiweeks=201501 with required params epiweeks, regions. [https://cmu-delphi.github.io/delphi-epidata/api/fluview.html](https://cmu-delphi.github.io/delphi-epidata/api/fluview.html)

- Legacy V4 COVIDcast data_source=nssp uses the same six signal names as V5 and is labelled "part of the legacy V4 API, which is being phased out." [https://cmu-delphi.github.io/delphi-epidata/api/covidcast-signals/nssp.html](https://cmu-delphi.github.io/delphi-epidata/api/covidcast-signals/nssp.html)

- Other V5 respiratory sources listed in the nav (not opened): nchs_mortality, flusurv, fluview_resp_lab_clinical, fluview_resp_lab_ph, nrevss. Exact source identifiers for those are **unverified**. [https://cmu-delphi.github.io/delphi-epidata/api/v5_migration.html](https://cmu-delphi.github.io/delphi-epidata/api/v5_migration.html) (link list)

## 2. data.cdc.gov (Socrata / SODA)

### API pattern

- Dataset identifier is a 4x4 code (abcd-1234). SODA 2.x endpoint: https://\<domain\>/resource/\<id\>.json (also .csv). SODA 3.0 (due 2025 per the page) moves to /api/v3/views/\<id\>/query.json; 2.1 remains the documented, backwards-compatible version. [https://dev.socrata.com/docs/endpoints.html](https://dev.socrata.com/docs/endpoints.html)

- Confirmed live by query (SODA 2.x form works today on data.cdc.gov): https://data.cdc.gov/resource/ua7e-t2fy.json?\$select=jurisdiction,weekendingdate,totalconfc19newadm,totalconfflunewadm,totalconfrsvnewadm&\$order=weekendingdate DESC&\$limit=2 returned rows for week ending 2026-10-24. https://data.cdc.gov/resource/rdmq-nq56.json?\$select=week_end,geography,percent_visits_covid,percent_visits_influenza,percent_visits_rsv&\$where=county='All'&\$order=week_end DESC&\$limit=2 returned rows for week ending 2026-10-24.

- \$limit default 1000; max 50,000 on 2.0 endpoints, unlimited on 2.1. \$offset default 0, no maximum. [https://dev.socrata.com/docs/paging.html](https://dev.socrata.com/docs/paging.html)

- App token: header X-App-Token, or query parameter \$\$app_token (SODA 2.x). Without a token, requests share an IP-based pool with "a much lower throttling limit"; with a token, "we do not throttle API requests ... unless those requests are determined to be abusive or malicious." Throttled responses return HTTP 429. **No numeric limits are published** on that page. [https://dev.socrata.com/docs/app-tokens.html](https://dev.socrata.com/docs/app-tokens.html)

- Dataset metadata (columns, custom fields, rowsUpdatedAt) is available at https://data.cdc.gov/api/views/\<id\>.json (used below).

### Datasets (opened via /api/views/\<id\>.json)

**NWSS wastewater**

| **ID**               | **Title**                                                               | **Update frequency**    | **Key columns**                                                                                                              | **Notes**                                                                                                                                                                                                                                                                                                                                                      |
|----------------------|-------------------------------------------------------------------------|-------------------------|------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2ew6-ywp6            | NWSS Public SARS-CoV-2 Wastewater Metric Data                           | Weekly (metadata)       | wwtp_jurisdiction, key_plot_id, date_end, ptc_15d, detect_prop_15d, percentile                                               | Description says **archived September 12, 2025; no new data will be added**. [https://data.cdc.gov/api/views/2ew6-ywp6.json](https://data.cdc.gov/api/views/2ew6-ywp6.json)                                                                                                                                                                             |
| g653-rqe2            | NWSS Public SARS-CoV-2 Concentration in Wastewater Data                 | not opened              | not opened                                                                                                                   | Companion to 2ew6-ywp6; likely also archived (**unverified**). Listed at [https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&search_context=data.cdc.gov&only=datasets&limit=10&q=NWSS%20wastewater](https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&search_context=data.cdc.gov&only=datasets&limit=10&q=NWSS%20wastewater) |
| atcp-73re            | CDC Wastewater Viral Activity Level for SARS-CoV-2, Influenza A and RSV | R/P1W (weekly, Fridays) | state_territory, site, week_end, pathogen_target, site_wval, site_wval_category, date_updated                                | Current multi-pathogen WVAL dataset; rows updated 2026-10-30. [https://data.cdc.gov/api/views/atcp-73re.json](https://data.cdc.gov/api/views/atcp-73re.json)                                                                                                                                                                                            |
| j9g8-acpt            | CDC Wastewater Data for SARS-CoV-2                                      | R/P1W (weekly, Fridays) | site, state_territory, sample_collect_date, pcr_target, pcr_target_avg_conc, pcr_target_avg_conc_lin, pcr_target_flowpop_lin | Sample-level data; rows updated 2026-10-30. [https://data.cdc.gov/api/views/j9g8-acpt.json](https://data.cdc.gov/api/views/j9g8-acpt.json)                                                                                                                                                                                                              |
| ymmh-divb            | CDC Wastewater Data for Influenza A                                     | not opened              | not opened                                                                                                                   | Catalog listing only; updated 2026-10-30. Same catalog URL as above.                                                                                                                                                                                                                                                                                           |
| akvg-8vrb, mtpu-urpp | CDC Wastewater Data for Measles / for Avian Influenza A (H5)            | not opened              | not opened                                                                                                                   | Catalog listing only.                                                                                                                                                                                                                                                                                                                                          |

Note: there is no single "RSV wastewater" sample-level dataset in the catalog search results; RSV appears in atcp-73re via pathogen_target (**which values that column takes is unverified**).

**NSSP emergency department visits**

| **ID**    | **Title**                                                                                                             | **Update frequency** | **Key columns**                                                                                                                                             | **Notes**                                                                                                                                                                                    |
|-----------|-----------------------------------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rdmq-nq56 | NSSP Emergency Department Visit Trajectories by State and Sub State Regions- COVID-19, Flu, RSV, Combined             | R/P1W                | week_end, geography, county, percent_visits_covid, percent_visits_influenza, percent_visits_rsv, percent_visits_combined, ed_trends_covid, hsa_nci_id, fips | Current dataset; rows updated 2026-10-27. [https://data.cdc.gov/api/views/rdmq-nq56.json](https://data.cdc.gov/api/views/rdmq-nq56.json)                                              |
| 7mra-9cq9 | 2023 Respiratory Virus Response - NSSP Emergency Department Visit Trajectories by State- COVID-19, Flu, RSV, Combined | R/P1W (metadata)     | week_end, pathogen, geography, percent_visits, trend_on_date, recent_trend                                                                                  | Long format, but rows last updated 2024-10-18, so effectively stale; prefer rdmq-nq56. [https://data.cdc.gov/api/views/7mra-9cq9.json](https://data.cdc.gov/api/views/7mra-9cq9.json) |
| vjzj-u7u8 | NSSP Emergency Department Respiratory Daily                                                                           | not opened           | not opened                                                                                                                                                  | Catalog listing, updated 2026-10-31.                                                                                                                                                         |
| 7xva-uux8 | NSSP Emergency Department Visits - COVID-19, Flu, RSV, Combined – by Demographic Category                             | not opened           | not opened                                                                                                                                                  | Catalog listing, updated 2026-10-30.                                                                                                                                                         |

Catalog URL: [https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&search_context=data.cdc.gov&only=datasets&limit=10&q=NSSP%20Emergency%20Department%20Visit%20Trajectories](https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&search_context=data.cdc.gov&only=datasets&limit=10&q=NSSP%20Emergency%20Department%20Visit%20Trajectories)

**NHSN Weekly Hospital Respiratory Data (HRD)**

| **ID**    | **Title**                                                                                                               | **Update frequency**                                         | **Key columns**                                                                                                                                                                               | **Notes**                                                                                                                                                                                                        |
|-----------|-------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ua7e-t2fy | Weekly Hospital Respiratory Data (HRD) Metrics by Jurisdiction, National Healthcare Safety Network (NHSN)               | Not in custom_fields; release notes reference weekly reports | jurisdiction, weekendingdate, totalconfc19newadm, totalconfflunewadm, totalconfrsvnewadm (all five confirmed by live query), totalconfc19hosppats, totalconffluhosppats, totalconfrsvhosppats | Rows updated 2026-10-30; data through week ending 2026-10-24. [https://data.cdc.gov/api/views/ua7e-t2fy.json](https://data.cdc.gov/api/views/ua7e-t2fy.json) and the /resource/ua7e-t2fy.json query above |
| mpgq-jmmr | Weekly Hospital Respiratory Data (HRD) Metrics by Jurisdiction, National Healthcare Safety Network (NHSN) (Preliminary) | Description: "updates weekly on Wednesdays"                  | same schema family (columns not fully listed)                                                                                                                                                 | Rows updated 2026-09-30. [https://data.cdc.gov/api/views/mpgq-jmmr.json](https://data.cdc.gov/api/views/mpgq-jmmr.json)                                                                                   |

**RESP-NET**

| **ID**               | **Title**                                                           | **Update frequency** | **Key columns**                                                                                                                                      | **Notes**                                                                                                                                                                                                                                                                                                                                                                |
|----------------------|---------------------------------------------------------------------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| kvib-3txy            | RESP-NET Rates and Clinical Data                                    | Weekly               | surveillance_network, season, date, age_category, state, rate_type, estimate (12 columns total: also date_type, race, sex, data_type, estimate_type) | Rows updated 2026-10-23. [https://data.cdc.gov/api/views/kvib-3txy.json](https://data.cdc.gov/api/views/kvib-3txy.json)                                                                                                                                                                                                                                           |
| 29hc-w46k, 6jg4-xsqq | RSV-NET Rates and Clinical Data / COVID-NET Rates and Clinical Data | not opened           | not opened                                                                                                                                           | Catalog listing. [https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&search_context=data.cdc.gov&only=datasets&limit=10&q=RESP-NET%20laboratory-confirmed%20hospitalizations](https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&search_context=data.cdc.gov&only=datasets&limit=10&q=RESP-NET%20laboratory-confirmed%20hospitalizations) |

**NCHS provisional deaths**

| **ID**    | **Title**                                                       | **Update frequency**                         | **Key columns**                                                                                                                                      | **Notes**                                                                                                                                                                          |
|-----------|-----------------------------------------------------------------|----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| r8kw-7aab | Provisional COVID-19 Death Counts by Week Ending Date and State | R/P1W / "Weekly" (Thursdays per description) | week_ending_date, state, group, covid_19_deaths, pneumonia_deaths, influenza_deaths, pneumonia_influenza_or_covid_19_deaths, total_deaths, mmwr_week | Rows updated 2026-10-08. This is the live weekly COVID/flu/pneumonia series. [https://data.cdc.gov/api/views/r8kw-7aab.json](https://data.cdc.gov/api/views/r8kw-7aab.json) |
| ynw2-4viq | Provisional Death Counts for Influenza, Pneumonia, and COVID-19 | "Irregular"                                  | week_ending_date, jurisdiction, age_group, covid_19_deaths, influenza_deaths, pneumonia_deaths, pneumonia_influenza_or_covid                         | Rows last updated 2023-11-02; treat as historical. [https://data.cdc.gov/api/views/ynw2-4viq.json](https://data.cdc.gov/api/views/ynw2-4viq.json)                           |

## 3. PopHIVE (pophive.org, Yale School of Public Health)

- **Download options:** A Data Catalog with per-file "Download" buttons (73 sources, 163 files). **File formats are not stated on the page** (unverified). Per-dataset data dictionaries are at https://pophive.github.io/Ingest/, and the processed data lives in the GitHub repo https://github.com/PopHIVE/Ingest under data/\<dataset\>/standard. [https://www.pophive.org/data-catalog](https://www.pophive.org/data-catalog)

- **No public REST API is mentioned** on the home page or catalog page. The catalog links out to the Delphi V5 API (https://delphi.cmu.edu/epidata/v5/) and Kinsa Insights API for some sources. [https://www.pophive.org/](https://www.pophive.org/) and [https://www.pophive.org/data-catalog](https://www.pophive.org/data-catalog)

- **"AI connector":** An MCP-based connector ("in testing") that gives an AI assistant access to the same data pipeline that powers the dashboards. Listed as an official Claude connector at https://claude.ai/directory/connectors/pophive; works with "any AI assistant that supports MCP" (setup guide PDF: https://www.pophive.org/docs/pophive-mcp-guide.pdf). No account, API key or password required. **The MCP server URL is not shown on the page** (unverified). [https://www.pophive.org/ai-access](https://www.pophive.org/ai-access)

- **Respiratory signals published:** dashboards for RSV, Influenza, COVID-19, Pneumococcus (plus Measles). Catalog respiratory sources: CDC Epidemic Trends and Rt (COVID, flu, RSV); CDC NWSS (SARS-CoV-2, Influenza A, RSV wastewater, state level); NSSP ED visit percentages and commercial lab data for COVID/flu/RSV; Epic Cosmos Respiratory Infections (RSV/flu/COVID ED encounters, RSV test positivity); CMU Delphi COVIDcast (Doctor Visits, Hospital Admissions, NHSN, FluView ILINet); NHSN Hospital Capacity and Admissions; RESP-NET; NREVSS; Kinsa ILI; Google Health Trends; flu/RSV vaccination datasets. [https://www.pophive.org/](https://www.pophive.org/) and [https://www.pophive.org/data-catalog](https://www.pophive.org/data-catalog)

- Processing documentation for COVID lists sources: NWSS (via cdc.gov), Delphi Epidata (doctor-visits, hospital-admissions, nhsn with \_prelim suffix for preliminary signals), Epic Cosmos SlicerDicer, and links the NHSN datasets ua7e-t2fy and mpgq-jmmr. [https://pophive.github.io/processing-documentation/Pages/respiratory-diseases/covid.html](https://pophive.github.io/processing-documentation/Pages/respiratory-diseases/covid.html)

- **Terms / citation:** Data and outputs are provided "as is" without warranty; "research tools intended for use in the fields of public health and medicine," "not intended for clinical decision making." Footer "© 2025 All Rights Reserved"; Terms & Privacy link goes to https://ysph.yale.edu/privacy/. **No citation requirement or data license is stated** on the pages opened (unverified whether one exists in the GitHub repo). [https://www.pophive.org/](https://www.pophive.org/) and [https://www.pophive.org/data-catalog](https://www.pophive.org/data-catalog) and [https://www.pophive.org/ai-access](https://www.pophive.org/ai-access)

## 4. Health Data NY (health.data.ny.gov)

- **Socrata confirmed:** the domain answers the Socrata Discovery API (api.us.socrata.com/api/catalog/v1?domains=health.data.ny.gov) and the Socrata metadata endpoint /api/views/\<id\>.json. [https://api.us.socrata.com/api/catalog/v1?domains=health.data.ny.gov&search_context=health.data.ny.gov&only=datasets&limit=10&q=influenza](https://api.us.socrata.com/api/catalog/v1?domains=health.data.ny.gov&search_context=health.data.ny.gov&only=datasets&limit=10&q=influenza)

- **Dataset:** jr8b-6gh6, "Influenza Laboratory-Confirmed Cases by County: Beginning 2009-10 Season". Posting frequency: **Weekly** (custom field "Dataset Summary \> Posting Frequency"). Columns: season, region, county, cdcweek, weekendingdate, disease, count, fips. Rows last updated 2026-05-29 (end of 2025-26 season). [https://health.data.ny.gov/api/views/jr8b-6gh6.json](https://health.data.ny.gov/api/views/jr8b-6gh6.json)

- Other candidates from the same catalog search (not opened): iye6-rifr "Influenza Hospitalizations: Beginning October 2020"; cpxv-79jk "Influenza Laboratory-Confirmed Cases by Age Group: Beginning 2023-24 Season"; xrhr-cy84 "New York State COVID-19 and Influenza Vaccination Data" (updated 2026-10-29).

## 5. MCP Python SDK

- **PyPI package:** mcp. Latest version **2.3.0**, released October 2, 2026. Install pip install mcp or pip install "mcp\[cli\]" (adds the mcp CLI); uv add "mcp\[cli\]". PyPI says Python \>= 3.10; the v2 docs site says Python 3.11+. [https://pypi.org/project/mcp/](https://pypi.org/project/mcp/) [https://github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) [https://py.sdk.modelcontextprotocol.io/](https://py.sdk.modelcontextprotocol.io/)

- **Current major version is v2** ("This is v2 of the MCP Python SDK, the current stable release line"), supporting the 2026-07-28 MCP spec and earlier. v1.x lives on the v1.x branch with critical fixes only; README recommends pinning mcp\>=1.28,\<2 until migrated. [https://github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)

- **FastMCP was renamed to MCPServer in v2.** v1: from mcp.server.fastmcp import FastMCP; v2: from mcp.server import MCPServer (or from mcp.server.mcpserver import MCPServer, Context). Importing mcp.server.fastmcp raises ModuleNotFoundError in v2. [https://py.sdk.modelcontextprotocol.io/migration/](https://py.sdk.modelcontextprotocol.io/migration/)

- **Decorators (unchanged in signature from v1):** @mcp.tool(), @mcp.resource("greeting://{name}") (URI template), @mcp.prompt(), @mcp.completion().

from mcp.server import MCPServer

mcp = MCPServer("Demo")

@mcp.tool()

def add(a: int, b: int) -\> int:

"""Add two numbers."""

return a + b

@mcp.resource("greeting://{name}")

def greeting(name: str) -\> str:

"""Greet someone by name."""

return f"Hello, {name}!"

@mcp.prompt()

def review_code(code: str) -\> str:

"""Review a piece of code."""

return f"Please review this code:\n\n{code}"



> [https://py.sdk.modelcontextprotocol.io/](https://py.sdk.modelcontextprotocol.io/) and [https://py.sdk.modelcontextprotocol.io/servers/prompts/](https://py.sdk.modelcontextprotocol.io/servers/prompts/) and [https://py.sdk.modelcontextprotocol.io/migration/](https://py.sdk.modelcontextprotocol.io/migration/)

- **Transports:** "stdio" (default: mcp.run() or mcp.run(transport="stdio")), "streamable-http" (mcp.run(transport="streamable-http", port=3001), default host 127.0.0.1, default port 8000, default path /mcp via streamable_http_path), and "sse" (documented as superseded by Streamable HTTP; not for new builds). Transport options moved from the constructor to run(), sse_app(), streamable_http_app() in v2. [https://py.sdk.modelcontextprotocol.io/run/](https://py.sdk.modelcontextprotocol.io/run/) [https://py.sdk.modelcontextprotocol.io/migration/](https://py.sdk.modelcontextprotocol.io/migration/)

## 6. DuckDB Python

- **PyPI:** package duckdb, latest version **2.0.0**, released October 21, 2026, requires Python \>= 3.11.0. [https://pypi.org/project/duckdb/](https://pypi.org/project/duckdb/)

- **httpfs:** enables reading remote files over plain HTTP(S) (read only) and S3-compatible object storage (read/write/glob). It is "autoloaded on first use of any functionality exposed by this extension"; manual form is INSTALL AND LOAD httpfs;. So reading a remote CSV by URL works without an explicit LOAD in a standard distribution, but the page does not use the word "autoinstall" (whether a fresh environment downloads it silently is **unverified** from that page). [https://duckdb.org/docs/2.0/core_extensions/httpfs/overview.html](https://duckdb.org/docs/2.0/core_extensions/httpfs/overview.html)

- **json:** "shipped with most DuckDB distributions and is auto-loaded on first use." Function read_json(...); implicit SELECT \* FROM 'file.json' also works. read_json_auto is not mentioned on the overview page (**unverified**). Reading JSON from a remote URL is not covered on that page. [https://duckdb.org/docs/2.0/data/json/overview.html](https://duckdb.org/docs/2.0/data/json/overview.html)

- Note: https://duckdb.org/docs/stable/... now redirects to https://duckdb.org/docs/2.0/....

## Items left unverified

- Whether epidatpy 0.5.1 on PyPI already supports the V5 routes.

- Exact V5 source identifiers for NCHS mortality, FluSurv-NET, NREVSS and FluView lab sources (pages not opened).

- Numeric Socrata throttling limits (not published on the app-tokens page).

- Columns and status of g653-rqe2, ymmh-divb, vjzj-u7u8, 7xva-uux8, 29hc-w46k, 6jg4-xsqq (catalog listing only).

- The set of values in atcp-73re.pathogen_target.

- PopHIVE download file formats, MCP server URL, and any data license/citation text.

- DuckDB read_json_auto name and silent auto-install of httpfs on a fresh machine.

## 7. Jev (TypeSafe AI), secondary sources only

TypeSafe's own documentation (https://docs.typesafe.ai) was not opened. The facts below come from three secondary pages opened on 2026-10-31 and should be confirmed against TypeSafe's documentation in Phase 0 or before Phase 5.

- Jev is a decision model that does not generate text; it takes a "state" (text or JSON) plus typed questions and returns probabilities. Question types: yes/no (returns probability of yes), score (2 to 10 ordered rubric levels, returns a probability-weighted position plus a confidence field), choice (up to 255 options, probability per option). Text input only; a request holds up to 64k tokens, 32k for state plus the longest question. Model aliases jev-latest and pinned jev-1.13.0; pricing quoted at \$0.042 per million input tokens with free output. TypeSafe states Jev is not trained on customer requests; enterprise accounts get zero retention; retention for other accounts is not stated on the page. [https://www.promptfoo.dev/docs/providers/typesafe/](https://www.promptfoo.dev/docs/providers/typesafe/)

- The same page quotes TypeSafe: "Jev 1.13 is unreliable at arithmetic, counting, and date comparisons"; score values are not calibrated for interpolating between levels; Jev gives no rationale; outputs that claim to satisfy a rubric can inflate scores. [https://www.promptfoo.dev/docs/providers/typesafe/](https://www.promptfoo.dev/docs/providers/typesafe/)

- confidence on choice and score answers describes how concentrated the probabilities are (1.0 when all weight is on one option), not the probability of any single option; calibration is described as population-level (answers given 0.8 are right about 80 percent of the time across many answers). Suggested use is threshold bands (act, confirm, hand off) tuned on labeled data with the model version pinned, after a shadow-mode period. [https://flaviocopes.com/jev-confidence/](https://flaviocopes.com/jev-confidence/)

- Maker TypeSafe AI; public release reported as September 2026; a cited accuracy figure of 67.8 percent appears in the article without a task definition. [https://zapier.com/blog/jev/](https://zapier.com/blog/jev/)

- jevapi on PyPI (0.1.0, September 24, 2026, single maintainer, "JevScope project") is unrelated to TypeSafe. It calibrates a model's stated confidence against labeled outcomes with isotonic regression and a Wilson lower bound for document-extraction fields. [https://pypi.org/project/jevapi/](https://pypi.org/project/jevapi/)

Unverified: everything above against TypeSafe's primary documentation; the exact API endpoint paths; current model version; retention terms for non-enterprise accounts.

------------------------------------------------------------------------

## 8. Phase 0 additions (2026-10-31)

Checked from the build session on 2026-10-31. The session could not reach the data hosts (data.cdc.gov, delphi.cmu.edu, health.data.ny.gov, census.gov all refused by the environment's network policy), so items that need a live query are still open in `docs/open-questions.md`. Evidence that comes from PopHIVE's copies of source files is labeled as secondhand.

### Packages (PyPI JSON API, 2026-10-31)

- mcp 2.3.0 installed; `from mcp.server import MCPServer` imports without error. This confirms the v2 rename in Section 5 by running it.
- duckdb 2.0.0 installs and imports under Python 3.13.
- epidatpy on PyPI is now 0.7.0 (released 2026-09-23), not 0.5.1. Not used (decision 0009).
- pandas latest is 3.1.0 (2026-10-22), a new major version. Pinned (decision 0008).

### PopHIVE (git clone of github.com/PopHIVE/Ingest, commit 9efff24, 2026-10-31)

- **File formats, now verified.** Dashboard files are Parquet under `data/bundle_*/dist/` (for example `data/bundle_respiratory/dist/covid_overall_trends.parquet`). Per-source processed files are gzip CSV at `data/<source>/standard/data.csv.gz`, with a `datapackage.json` data dictionary beside them. Raw copies of the source pulls are in `data/<source>/raw/` as `.csv.xz` plus the Socrata metadata `.json`. One file (`data/census/standard/data.csv.gz`) is stored with Git LFS. Source: the repository README and directory listing.
- The README says the `value` column is generally the source value, and `value_smooth` and `value_smooth_scale` are derived.
- Respiratory sources present include `nssp`, `delphi_nhsn`, `delphi_ili_fluview`, `nhsn_hospital_capacity`, `respnet`, `wastewater`, `nchs_mortality`, `NREVSS`, `epic_resp_infections`, `pep_population`.

### Secondhand findings from PopHIVE's raw copies (confirm live)

- rdmq-nq56 (BuildNumber 2026-10-21, weeks 2022-10-01 to 2026-10-17): all `week_end` values are Saturdays. County rows have `trend_source = 'HSA'` and repeat the Health Service Area value for every county (decision 0011). State labels are full names for 50 states, DC, and "United States"; no territories and no "New York City" label in this copy. In the CSV export, `fips` has thousands separators ("1,007").
- ua7e-t2fy (CSV export, display column labels): all week ending dates are Saturdays. 67 jurisdiction labels: 50 states, DC, AS, GU, MP, PR, VI, "USA", and "Region 1" to "Region 10". The dataset also publishes "Percent Hospitals Reporting" columns, which can feed the Coverage score.
- Delphi nhsn (legacy pull): state `geo_value` labels are lowercase USPS codes, including as, gu, mp, pr, vi.
- Delphi FluView (legacy V3 pull): state `wili` equals `ili` in every row (decision 0006).
