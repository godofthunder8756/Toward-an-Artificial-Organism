# Short delta check: C-κ oracle scope governing set (RL record + closure note + v1.4_N)

Research Delegate, 2026-10-22, about 02:15 ET. Read-only: nothing was run, no checkpoint was touched, and no existing file was edited. This is a new file. Prior check reused: `6a1c8168…` (B1, N-a, N-b).

## Hashes (verified with sha256sum)
- RL record `CKAPPA_SCOPE_GOVERNING_SET_RL.md`: `6a5e0f24995a1349664349713e1ee0a550267ac06ab0e4b462b121d931c15c63`
- Closure note: `4ad1d217aaab0bd45d2be6fd3e24872a4b22407d0c8abc2fa36a5a1ac7c45c9c`. Matches.
- v1.4_N: `3f0c5c129fbf290ab2ebf2661749ce64f2d0305670d385392aa3a3a6336ff359`. Matches.
- Unchanged: v1 `1b450bcf…`, v1.1 `e40c288f…`, v1.2 `7e15e812…`, v1.3 `f6263fb8…`.
- Governing order per RL L5–10: closure (4ad1d217) > v1.4_N > v1.3 > v1.2 > v1.1, with the verbatim E36 text above all. v1.5_final (177e62b6), v1.4 and the 05250543 note are non-governing. Not reviewed.

## Verdict: **NOT PASS. Two named blockers (B2, B3).** Each needs a one-line Research Lead clarification; no new scope file is required. Every other checked item is RESOLVED.

## Per-item status
| Item | Status | Ref / note |
|---|---|---|
| N3: rcond=1e-10 + rank check before every fit | **OPEN (B2)** | v1.4_N L33–35. The arithmetic is sound: after the pre-fit check, no ratio lies in [1e-10, 1e-6], so `lstsq` with s < 1e-10·s_max truncates exactly the resolved-zero set. But L35 ends "Rank-**deficient** or unresolved cells are unscored and counted as u". In rank-rule vocabulary (v1.1 L68–71), rank-deficient means *resolved* lower rank. That contradicts the same paragraph ("resolved-zero directions are never inverted"; "σ₁ = 0 … a zero fit"), and it contradicts E36-3 ("neither fit is constrained to attain a specified rank … minimum-norm") and E36-8 (rank 0 gets a zero fit). Under that reading, a resolved-lower-rank O6 fold would be unscored with no N1 label, because B1 covers only rank-UNRESOLVED, and pooled H* would be undefined. |
| O7 per-prefix void, ≥5 of 16 ⇒ NOT ADMISSIBLE | RESOLVED | v1.4_N L39–43. 25% of 16 = 4, so "more than 25%" means voided > 4, which is voided ≥ 5. Exact match. E36-6 is satisfied: g is never refitted and no prefix is replaced (L43), the label is RESTRICTED COMPARATOR NOT ADMISSIBLE, and the package continues to O3. Frozen folds: the six orbit splits are unchanged. Voiding drops prefixes the way E36-4 masks invalid edits ("never replaced"), and the N3 check reruns on each reduced design (L42). Note n-1, non-blocking: with 1–4 voids, label each voided prefix "RESTRICTED COMPARATOR NOT ADMISSIBLE" to use E36-6's wording. |
| σ at valid prefixes when O7 is NOT ADMISSIBLE (RL L11) | **OPEN (B3)** | "Descriptive only and … never a stop" conflicts with N4(i) (v1.4_N L38: σ₃/σ₁ > 1e-6 means STOP, PIPELINE INVALID). It also conflicts with E36-7 ("A resolved third direction … requires an integrity diagnosis") and Astra's verbatim note ("A demonstrated implementation contradiction should still stop it", v1.3 L47). The same evidence would stop the run with 1–4 voids but not with ≥5. It also overrides v1.4_N L41 ("no derivatives … evaluated") without saying which prefix set the stacked Jacobian uses. My own 6a1c8168 L48 suggested "no stop". I withdraw that wording: it predates the per-prefix rule and overlooked Astra's note. |
| Per-array hash file covers Q, Q₂, directions | RESOLVED | v1.4_N L71 and closure §4: Q, Q₂ and the O4/O6/O7 direction arrays. The §6 directions (36100–36109) are prospective and not drawn in this package. Note n-2, non-blocking: write `drawn_array_hashes.json` at draw time so a kill cannot lose it. |
| B1: REFERENCE RANK UNRESOLVED between N1 steps 2 and 3 | RESOLVED for rank-UNRESOLVED | Closure §2. Complete only once B2 is fixed. |
| N-a: kill at 595 s | RESOLVED | Closure §3. The 60 s reserve, the 540 s soft stop and the projection halt are unchanged. A kill at 595 s is reported as CAP REACHED. The index is written inside the 600 s cap (E36-14). |
| N-b: raw-byte sha256 with shape and dtype `<f8` in results.json | RESOLVED | Closure §4. The `.npz` is kept for convenience only. |
| Closure note vs E36 | No conflict | It changes only the governing order, B1, N-a, N-b and manifest item 1. The n3 numbers are stated as unchanged (§3). |
| RL record vs closure / v1.4_N | Consistent except B3 | The governing order matches closure §1. Listing v1 as non-governing is consistent: v1 was never in the chain and is hashed under manifest item 1. |

## Blockers and minimum fixes (one line each, for the RL record or the application)
- **B2.** "In N3, 'rank-deficient' means rank-UNRESOLVED only. A resolved lower-rank design (including σ₁ = 0) is fitted minimum-norm and scored, and its rank and σ₁ are reported (E36-3, E36-8)."
- **B3.** "The σ report at valid prefixes when O7 is NOT ADMISSIBLE uses the stacked Jacobian over the non-voided prefixes per fold. σ₃/σ₁ > 1e-6 there is handled as in N4(i): integrity diagnosis, STOP, PIPELINE INVALID. Otherwise it is descriptive."
  - Alternative if the RL keeps "never a stop": report a resolved σ₃ with an integrity diagnosis as E36-7 requires. In that case the RL must state explicitly that it is departing from Astra's note.

## Non-blocking note
- **n-3.** With rcond at the band edge (1e-10), gelsd's internal SVD and the pre-fit SVD can disagree by about ε·σ₁ for a ratio within about 1e-16 of 1e-10. To remove this, compute the fit from the same SVD used for the rank check, truncating at σᵢ/σ₁ < 1e-10. The result is identical to lstsq otherwise.

## Claim ceiling
Unchanged: oracle-only. Nothing runs until the application is filed and the manifest is sealed.
