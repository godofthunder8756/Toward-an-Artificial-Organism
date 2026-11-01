# Track B freeze preparation v2.5: ERRATUM 2, CORRECTION 1 (Lead) — E2-1 absolute-deviation recomputation

**STATUS: DESIGN ONLY. DRAFT, NOT FROZEN. NOTHING RUNS.** A new, additive file. Under the binding no-rewrite rule (11:53 AM ET), it corrects `review/trackB_freezeprep_v2_5_erratum2_Lead.md` (whole-file sha256 `81bdfcf29ad81ac20b4effbdb8434664d82b67e0f96f3f0345504950079f4569`, read-only, not edited; "E2 Ln") by supersession only. Only computation: exact integer arithmetic (system `python3`) and SHA-256.
- **Written:** 2026-11-01, about 11:56 AM ET, by the Lead's executor.

## C1. E2 L10, "Executor recomputation" sentence — SUPERSEDED
E2 L10 states that the maximum of max(r, m − r)/(m·2^64), r = 2^64 mod m, is "5.4210e-20 at m = 256". **That is an executor arithmetic error:** for m a power of two (2, 4, …, 256), r = 0 and every residue has probability exactly 1/m, so the deviation is **0**; the script omitted the r = 0 case. Corrected (exact): over m = 2…508 the maximum absolute deviation |P(idx = i) − 1/m| = max(r, m − r)/(m·2^64) is **5.3999e-20 (≈ 5.40 × 10⁻²⁰), attained at m = 257**. The ruling's 5.42 × 10⁻²⁰ (CLP L53) equals 2^−64 = 5.4210 × 10⁻²⁰, the strict upper bound, not the attained maximum.
- Unchanged: the relative figures (exact max 2.6455 × 10⁻¹⁷ at m = 504; ruled bound 508/2^64 = 2.7539 × 10⁻¹⁷) and E2 §3's flag "5.42e-20 vs 5.40e-20 — CNA to confirm", which was already correct. No conclusion changes. All other E2 content stands.

*DESIGN ONLY. Draft, not frozen. No freeze or execution is authorized (A49 L147). X1–X5 and the claim ceiling unchanged. No consciousness claim is made or implied.*

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 62364a219985a9bb3adcb4da5833852d269d1b6bd90587a17215f8b9ac07d9b6
