# 0012 Phase 5 uses the Jev connector in Claude

Status: Accepted (Andrea King, 2026-10-31: "acceptable to use public data for TypeSafe; use the Jev connector in Claude")

Context. Plan Section 6.2 planned to call TypeSafe's API from the pipeline with `TYPESAFE_API_KEY`.

Decision. Phase 5 classifies source notices through the Jev connector in Claude, not from pipeline code. Only public source notice text is sent. A script exports unlabeled notices to a file; a Claude session with the Jev connector classifies them; a second script loads the results into `source_notice.structured_flag`, `classifier_model`, and `classifier_prob`. Shadow mode is unchanged: nothing in the pipeline reads these fields.

Open items before Phase 5. The connector was not available in the Phase 0 session, so its tool names, the model version it reports, and TypeSafe's retention terms are still to confirm (docs/open-questions.md). `TYPESAFE_API_KEY` stays in `.env.example` only until this is confirmed, then is removed.

Consequences. No TypeSafe credentials in the pipeline. Classification runs are manual and logged.
