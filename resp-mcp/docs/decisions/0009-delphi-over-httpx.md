# 0009 Call Delphi V5 directly with httpx

Status: Proposed (review item S9).

Context. Whether the `epidatpy` client supports V5 routes is unverified. PyPI now lists epidatpy 0.7.0 (2026-09-23), newer than the 0.5.1 in endpoint-verification.md.

Decision. Call `https://delphi.cmu.edu/epidata/v5/snapshot/` and `/archive/` with httpx. Do not depend on epidatpy or delphi-epidata.

Consequences. One fewer dependency to verify. The adapter owns retries and rate limiting, which the plan already requires.
