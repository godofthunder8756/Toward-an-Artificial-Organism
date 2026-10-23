# Delta check: C-κ oracle-only scope record v1.1 against my review

Research Delegate, 2026-10-22 (ET). **Review only.** I ran nothing, loaded nothing and edited no existing file.

- **Checked:** `ckappa_oracle_scope_record_v1_1.md`, sha256 `e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c` (verified).
- **v1 unchanged:** `ckappa_oracle_scope_record_v1.md` is still `1b450bcf231324c6fc3c686cc2daa819ed5f09cd5725c7c3283a1b3e2c39c5bf` (verified).
- **Against:** my review `6dbf3deb…` and Astra #35 (`563e070c…`).

## Verdict

**PASS WITH NOTES FOR CONSULT #36.**

All six MAJOR items are resolved or resolved in substance. v1.1 introduces two new items, D-1 and D-2. Each needs a one-line fix, and either can be carried as a note in the consult text. Neither needs a redesign. There are five MINOR notes.

## MAJOR items S-M1 to S-M6

| Item | Status | Where in v1.1 |
|---|---|---|
| S-M1 transition count | **RESOLVED** | §1 L42 now has four transitions and four readings. §4 O1 L77 requires Φ(b_a,u) to reproduce all 256 stored terminal forecasts. |
| S-M2 headroom vs fitted comparator | **RESOLVED** (see D-1) | §4 O6 L88, L92: H\* is the held-out loss of the separately fitted fixed-κ comparator Pred_μ. O5 is demoted at L111 to "Not a headroom or a bound". §5 L115–L121 uses H\* and R\*. |
| S-M3 dry run | **RESOLVED** (see D-2) | §7 L151–L152: there is no pre-freeze dry run. Step 0 runs after the seal and the filed application, inside the cap, and halts; L151 forbids retries. |
| S-M4 two poor predictions | **RESOLVED** at the declared level | §6 L138–L147. Arithmetic is in (b) below. |
| S-M5 ε range | **RESOLVED** | §6 L129–L130: ε = 0.25 is added. {0.1, 0.25} count, {0.02, 0.05} are descriptive, and a positive needs both counted ε (L143). |
| S-M6 an ALL pass driven by XOR | **RESOLVED** | §6 L147: cross-stream marginal wording needs MARG to be available *and* MARG POSITIVE by the same quota. Otherwise "ALL-group response prediction; marginal component not shown". |

## MINOR items S-m1 to S-m10

| Item | Status | Note |
|---|---|---|
| S-m1 results.json | RESOLVED | L36 cites commit `5d9d8a7`, and the freeze re-hashes it. L77 verifies beliefs through the terminal forecasts. |
| S-m2 thresholds | RESOLVED | L114 declares them conventions. L121 adds R\*_MARG ≥ 0.02. 10⁻⁴ still has no rationale, which is acceptable for a declared convention. |
| S-m3 weighting | RESOLVED | L62 and L110. |
| S-m4 rank rule | RESOLVED | L68–L73: three bands; an unresolved cell is counted, not dropped. |
| S-m5 compute counts | PARTIAL | L153–L157 are still slightly low. See D-6. Harmless. |
| S-m6 accounting | RESOLVED | L132–L136: one rule, and pre-saturated units are handled. One ambiguity remains (D-5). |
| S-m7 VAL tabulation | RESOLVED | L53. The UNVERIFIED label is kept. |
| S-m8 MARG label | RESOLVED | L58. |
| S-m9 order | RESOLVED | L65: O1→O2→O6→O7→O3→O4→O5. |
| S-m10 O7 | RESOLVED | L98 reports the symmetry reduction rather than assuming it. L102 has the disclaimer. |

## Previously partial E35 items

| Item | Status | Note |
|---|---|---|
| E35-3 | **PARTIAL** (D-4) | The gain and absolute-accuracy floors are both there (L138–L139). §6 still does not define the *neural* Pred_full(δ,u) = Φ(b_a+Bδ,u) − Φ(b_a,u) with "B frozen before scoring". It also does not say that the nested Jacobian comparison is "reported separately and … not counted as independent replication" (E35-3, verbatim). |
| E35-4 | CONFORMS | L128–L136: frozen seeds, signs and magnitudes, no replacement, and the descriptive families listed (L131). |
| E35-6 | CONFORMS | H\* is labelled oracle-scale (L93). O5 is "not a bound" (L111). |
| E35-7 | CONFORMS, with one note | The rank bands are there, and L123 has no switching and no absence inference. There is no neural-side low-headroom guard (D-3). |
| E35-10 | CONFORMS | The claim unit is the F-TRAINED seed (L142). cand_final and F-INIT are descriptive (L148). The PR #5 scale is removed (L33). |

## Specific checks

**(a) Is H\* oracle-only and computed before any checkpoint? Is it comparable to the neural test?**

It is oracle-only. O6 uses a synthetic exact-filter state, z = Q·D⁻¹(chart − mean), and runs before any checkpoint exists. ✔

It is **not the same quantity as the neural test's achievable gain.** O6's ε acts on synthetic coordinates in which one unit equals one P-weighted chart standard deviation. A unit v ∈ ℝ⁸ moves the chart by D·Qᵀ·εv, about ε·√(3/8) ≈ 0.61ε standard deviations RMS. The neural ε acts on absolute GRU hidden-state units, and its chart effect goes through the checkpoint's fitted B, which is unknown.

So H\*(ε = 0.1) is an oracle-scale reference. It answers whether the oracle's κ response, beyond what a fitted fixed-κ comparator absorbs, is numerically resolvable and non-negligible at a declared chart-perturbation size. The neural test's floors are *relative* (½·L_μ, 0.25·Σ‖ΔF‖²), so its achievable gain is the checkpoint's own L_μ. L93 states this, and it is fine. See D-1 for the wording.

Using ε = 0.1, the smaller counted size, is the conservative choice, because H\* grows with perturbation size.

**(b) Does L_full ≤ ½·L_μ plus normalized error ≤ 0.25 close the two-poor-predictions case at R\* = 0.05?**

Write S = Σ‖ΔF‖². Split each model's loss into a shared non-κ error E_s and its own κ-part error: L_μ = E_s + K and L_full = E_s + e.

- Floor (a) gives E_s + e ≤ ½(E_s + K), so **e ≤ ½K − ½E_s**.
- At R\* = 0.05 with E_s ≈ 0: K ≈ 0.05·S. Floor (b) then binds the comparator only weakly (0.05 ≤ 0.25), and floor (a) requires e ≤ 0.025·S.
- So the full model must remove at least half of the κ-attributable squared error. Its RMS κ-part error is then at most about 71% of the comparator's.
- That rules out v1's "10% gain between two poor predictions" case. Shared error makes (a) *harder* (the −½E_s term), so the rule is conservative.

It does not guarantee *good* κ-part accuracy: up to about 50% of the κ energy, or 71% RMS, can stay unexplained. I accept it as a declared convention. It closes Astra's case at the declared level. Put this arithmetic to Astra in #36 and let her confirm that the level is adequate.

**(c) Are the quota and claim unit fixed in advance?** Yes. The claim unit is the F-TRAINED seed (L142), the quota is 8/10 at both counted ε (L143), and NOT SHOWN, UNRESOLVED and MIXED are pre-written (L144–L146). Precedence and seed-level aggregation are missing (D-3b).

**(d) Is step 0 sequenced correctly?** Partly:
- It runs after seal and filed application (L152), inside the 10-minute cap (L151), with no retries (L151), and halts. ✔
- The projection method is **not stated** (D-2).

**(e) Is Astra #35 compliance retained?** There are no regressions in substance:
- F-TRAINED is primary.
- Full-state random edits gate, with frozen signs and magnitudes and no replacement.
- The nested Jacobian comparison is not used as a gate.
- There is no surrogate veto, and O7 stays comparator-only (L102). E35-2, verbatim: "Any claim against a two-coordinate local factorization requires a separately specified test of that factorization."
- There is no stage substitution (L42, L123). Astra L190, verbatim: "Do not silently substitute another stage if k=4 lacks the declared headroom."
- The wording ceiling is Astra's closing paragraph (L148).

There is one wording-level slip against E35-9 (D-1).

## New issues in v1.1

- **D-1 (MAJOR, one-line fix). One ε symbol for two units.**
  - E35-9, verbatim: "Oracle-belief perturbation units and neural hidden-state perturbation units are distinct."
  - v1.1 uses the same symbol and the same values ε ∈ {0.02, 0.05, 0.1, 0.25} for the O6 synthetic edits (L85) and the neural edits (L129). §5 L115 calls O6's ε = 0.1 "the smallest counted size", which is a neural-side designation. That invites the reading that H\* is the neural headroom at neural ε = 0.1.
  - **Fix:** rename the oracle side ε_syn, in standardized synthetic-chart units. In §5, replace "(the smallest counted size)" with "(oracle-scale reference; not the neural achievable gain, which is the checkpoint's own L_μ; E35-9)".
- **D-2 (MAJOR, one-line fix). The step-0 projection method is undefined.**
  - O1 is an exact-rational (Fractions) replay. Its per-operation cost is not representative of the float64 propagations that make up about 99% of the work.
  - Scaling O1's time by "the declared propagation counts" could overestimate a lot. A false HALT under a no-retry rule would end the package.
  - **Fix:** freeze the formula. Time O1 plus a fixed float64 sample, for example the first 1,000 O6 propagations, which count as real work. Then use T_proj = T_elapsed + (N_remaining_float / 1000)·t_sample + T_O1-like-remaining. HALT if T_proj exceeds the *remaining* cap, 10 min − T_elapsed, rather than 10 min total.
- **D-3 (MINOR). Missing neural-side guards and aggregation.**
  - **(i)** If a checkpoint's held-out L_μ is near float noise, floor (a) is judged on noise. Add a resolvability band, for example L_μ ≤ 10⁻²⁰·ΣΔF² or below an absolute 1e-10-style band. That cell reads NEURAL HEADROOM NOT MET (E35-7), stays in the denominator, and is not a pass or a fail.
  - **(ii)** Seed status is undefined when cells are UNRESOLVED (is one cell enough to make the seed UNRESOLVED?). The labels also overlap: for example 2 passes and 3 UNRESOLVED meets both NOT SHOWN and UNRESOLVED. Freeze a precedence order: UNRESOLVED, then POSITIVE, then NOT SHOWN, then MIXED.
- **D-4 (MINOR, carried over from E35-3).** Add to §6 the neural Pred_full definition with B frozen before scoring, and the E35-3 sentence on Jacobian results, verbatim.
- **D-5 (MINOR).** "Both kinds count in the denominator as failed predictions" (L135) does not say how a failed edit enters the loss sums in (a) and (b). Freeze it as: excluded from the loss sums, counted toward the 25% UNRESOLVED rule, and counted as non-pass. Report the counts.
- **D-6 (MINOR). The compute counts are still low.**
  - O6 also needs the control's actual response, making 3 predictions per cell rather than 2 (about 5.9×10⁵).
  - O4 itself needs no propagations, but O5 needs about 3 per cell (about 3×10⁵).
  - The total is about 1×10⁶. Even so, at tens of microseconds each it is well under 10 minutes on paper (UNVERIFIED).

## For consult #36

Send v1.1 (`e40c288f…`) with:
- the D-1 and D-2 one-liners, as an additive v1.2 or as notes in the consult text;
- the (b) arithmetic, for Astra to confirm that ½·L_μ is adequate;
- D-3 to D-6 as notes for the freeze.

Nothing is authorized to run before the seal and the filed application (L11, L152).
