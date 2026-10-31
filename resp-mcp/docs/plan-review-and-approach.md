# Respiratory Virus Surveillance MCP: Plan Review and Build Approach

Reviewed 2026-10-31 against two Google Docs:

- `respiratory-mcp-technical-plan.md` (the plan)
- `endpoint-verification.md` (the verified facts the plan relies on)

This review did not re-open any external API or documentation page. Every finding below comes from reading the two documents against each other. Items that need a live check are marked **check in Phase 0**.

---

## 1. Bottom line

The plan is sound and ready to build once about a dozen gaps are closed. The architecture (adapters, DuckDB store, read-only MCP server), the schema, the scoring approach, and the decision to keep Jev out of numeric confidence are all well reasoned. Most problems are places where two sections of the plan do not quite agree, or where a rule is named but not defined. None requires redesign.

Recommended path: amend the plan through a short set of decision records at the start of Phase 0, then build in the phase order already in the plan, with a review checkpoint and your sign-off at the end of each phase.

---

## 2. What is strong (keep as is)

- Data flows one way, and the MCP server never calls the internet. This makes answers reproducible and auditable.
- Raw responses are saved before parsing, and there is a separate revision table. Together these give full provenance.
- Suppressed values are kept as null with a status, never dropped or zeroed.
- The plan recognizes that Delphi `nssp` and `nhsn` republish the same CDC data. It does not count that pair as independent agreement.
- The quality score is a simple, explainable average of named components, and it never hides data.
- Jev is limited to shadow-mode text classification, which matches what its own documentation says it is bad at (arithmetic, dates).
- Every PR gets a review against eight named dimensions.

---

## 3. Issues to resolve before or during Phase 0

### 3.1 Blocking (would cause wrong data or failed runs if not fixed)

| # | Issue | Where | Recommended fix |
|---|---|---|---|
| B1 | **Raw files get overwritten.** The raw file path is `data/raw/<source_id>/<YYYY-MM-DD>/<measure_id>_<geo_type>.json`. A second run on the same day writes to the same path, which breaks "raw files are never modified." | Sec. 5 | Add the run ID to the path: `.../<YYYY-MM-DD>/<ingest_run_id>/<measure_id>_<geo_type>.json`. |
| B2 | **`report_date` for SODA sources is the download date, not the publish date.** That makes the Freshness score always near perfect for S2 to S7, even when CDC has not updated in weeks. Example from the verification doc: r8kw-7aab (NCHS deaths) is described as weekly, but its rows were last updated 2026-10-08. | Sec. 4 (Revisions), Sec. 6.1 | Use the dataset's `rowsUpdatedAt` from `/api/views/<id>.json` (already confirmed available) as `report_date` for SODA rows. Keep `retrieved_at` as the download time. |
| B3 | **Same-day re-runs collide in `revision`.** The revision primary key ends in `report_date`. Two runs that see the same `report_date` will fail on insert. | Sec. 4 | Insert only when the value or status changed for that key and `report_date` (insert-or-ignore). Update the Phase 2 reconciliation rule to match: "every raw row maps to one revision row or is a documented unchanged duplicate." |
| B4 | **Adapter protocol has no method for Delphi history.** The protocol says "this and nothing else," but Sec. 5 and Phase 3a require pulling Delphi `archive/`. | Sec. 5 | Add an optional `fetch_history(measure_id, geo_type, start, end)` to the protocol. Sources without history return nothing. |
| B5 | **Weighted ILI likely does not exist at state level.** In CDC FluView, weighted ILI (`wili`) is published for nation and HHS regions; states get unweighted ILI only. The pilot pulls Phase 1 measures at state level. **Check in Phase 0** by querying `fluview_ilinet/wili` at `geo_type=state`. | Sec. 3.1 | If confirmed, record that `ili_pct_weighted` is national and HHS only, and set the expected geographies accordingly. |
| B6 | **NHSN preliminary data is in the scoring rule but not in the build.** The Provisional component relies on the preliminary dataset `mpgq-jmmr`, but no phase ingests it. Also, its rows were last updated 2026-09-30 even though it says it updates weekly, so it may be paused. | Sec. 3, 6.1, 8 | **Check in Phase 0** whether `mpgq-jmmr` is current. Delphi also has `_prelim` NHSN signals (noted in the PopHIVE documentation). Pick one source for preliminary status and record the choice. |

### 3.2 Should fix (rules named but not defined)

| # | Issue | Where | Recommended fix |
|---|---|---|---|
| S1 | "Expected geographies" for Completeness is not defined. | Sec. 6.1 | Add an `expected_geo` reference list per source and measure, built in Phase 0 from the enumerated labels (50 states + DC, plus listed territories where the source carries them). Needs your approval as a new table or file. |
| S2 | Coverage `documented_threshold` is not defined, and neither source in Phases 1 to 3 publishes one. | Sec. 6.1 | Mark Coverage as unavailable for the pilot until Phase 4 (NWSS site counts). Say so in the plan. |
| S3 | Revision volatility uses percent change, which blows up for small counts (for example 1 admission revised to 3 is +200%). The text also mixes "per signal" and "per row." | Sec. 6.1 | Compute it per source, measure, geography type, and lag. Skip or floor values below a minimum count, set as a parameter. |
| S4 | A score built from 2 components is compared directly with one built from 5. | Sec. 6.1 | Return `components_used` with every score so users can see what went into it. |
| S5 | `normalize` must be a pure function of the raw file, yet its output includes `ingest_run_id` and `retrieved_at`, which are not in the file. | Sec. 5 | Write a small metadata sidecar (`.meta.json`) next to each raw file with run ID, URL, and timestamps. `normalize` reads both. |
| S6 | SODA datasets return all measures in one call, but `fetch` is per measure. This repeats the same download 3 to 6 times. | Sec. 5 | Allow a SODA adapter to fetch once per dataset and normalize to many measures. |
| S7 | Phase 3b tests depend on scores from Phase 3a, so they are not fully parallel. | Sec. 8 | Run 3a first, or let 3b's tests accept null scores. |
| S8 | Two very new packages. `duckdb` 2.0.0 was released 2026-10-21 and `mcp` 2.3.0 on 2026-10-02. Open-ended ranges can pull in breaking fixes. | Sec. 5 | Commit a lockfile (`uv.lock`) and pin exact versions for the pilot. |
| S9 | `epidatpy` support for V5 is unverified. | Sec. 3 | Use `httpx` directly against V5. Fewer dependencies and nothing left to verify. |

### 3.3 Minor (missing files or housekeeping)

- `scripts/gen_mmwr.py` is used but not in the repository layout.
- No `.gitignore`. `.env`, `data/raw/`, and `data/respmcp.duckdb` should not be committed.
- No CI file. Sec. 9 lists automated checks (ruff, mypy, pytest, schema drift) but there is no `.github/workflows/` entry.
- The MMWR rule ("week 1 contains January 4", Sunday start) is correct. Validate the generated table against an independent reference (for example the `epiweeks` Python package) in a unit test.
- The layout is rooted at `resp-mcp/`, but this repository is `andreaking-phf/mcp`. Recommend putting the layout at the repository root.

---

## 4. Build approach

### Phase 0, broken into checkpoints

| Step | Work | Checkpoint |
|---|---|---|
| 0.1 | Scaffold at repo root: layout from Sec. 2 plus `scripts/gen_mmwr.py`, `.gitignore`, CI workflow, `CLAUDE.md` (Sec. 11), `pyproject.toml` with exact pins and a lockfile. Copy the plan and verification docs into `docs/`. | `respmcp --help` runs; CI green on an empty test. |
| 0.2 | Write decision records 0001 to 0009 for fixes B1 to B6 and S1, S8, S9 above (only the ones you approve). | You approve the records. |
| 0.3 | Live verification script (`scripts/verify_endpoints.py`) that queries each Phase 1 endpoint once and saves the result. It resolves: day of week for `week_end` and `weekendingdate`; `wili` at state level; `mpgq-jmmr` currency; `epidatpy` (skipped if S9 approved); NCHS provisional flag. | Results added to `docs/endpoint-verification.md` with the URL and date for each. |
| 0.4 | Enumerate every distinct state-level geography label from S1 to S3 into `geo_aliases.csv`. Any label that cannot be mapped goes to `docs/open-questions.md`. | Every label maps, or is listed for your review. |
| 0.5 | Obtain the Delphi key and Socrata token (needs your answer to question 1 below). | Keys in local `.env` only. |

### Phases 1 to 6

Follow the plan's phase table as written, with these additions:

- **One PR per phase**, with the Sec. 9 multi-agent review run before it is opened. Each PR lists the "Done when" criteria and shows evidence.
- **Your sign-off** at the end of Phases 0, 2, 3b, and 6. These are the points where data definitions or user-facing behavior get locked in.
- **Accuracy checkpoint after Phase 2:** for one state and one week, hand-compare 5 values in DuckDB against the raw file and the CDC page. This is a small version of the Phase 6 audit, done early.
- **Phase 3a before 3b** (see S7), unless you want speed over a cleaner dependency.

Estimated effort stays at the plan's 14 to 19 sessions, plus about 1 session for the Phase 0 fixes.

---

## 5. Decisions needed from you

From the plan (Sec. 12):

1. Register the Delphi key and Socrata token under PHF, or under PubHealth Commons? (The plan names PubHealth Commons. Please confirm that name should be used.)
2. State level only for the pilot, or include NSSP county level now?
3. Test the PopHIVE MCP connector in Claude before building S8?
4. Is sending public source notice text to TypeSafe acceptable once their retention terms are confirmed? (Phase 5 only. Optional.)

From this review:

5. Approve the blocking fixes B1 to B6 as described?
6. Approve adding an `expected_geo` reference list (S1)? This is a new table or file, so it needs your sign-off.
7. Put the build at the repository root of `andreaking-phf/mcp`, rather than in a `resp-mcp/` subfolder?

---

## 6. Decisions received (2026-10-31)

| # | Answer | Recorded in |
|---|---|---|
| 1 | Register keys under PubHealth Commons | decision 0001 |
| 2 | Include county data; check for duplication with state data | decision 0011 (proposed: store once per Health Service Area) |
| 3 | Test the PopHIVE connector | open question 7 (connector not available in the build session) |
| 4 | Public notice text may go to TypeSafe; use the Jev connector in Claude | decision 0012 |
| 5 | Blocking fixes B1 to B6 approved | decisions 0002 to 0007 |
| 6 | Add the geography reference list, with populations covered | decision 0010 (field names to confirm) |
| 7 | Build in a `resp-mcp/` subfolder | done |
