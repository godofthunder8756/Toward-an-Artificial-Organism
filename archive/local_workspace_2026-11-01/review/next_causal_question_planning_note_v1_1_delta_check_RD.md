# Delta check: planning note v1.1 against my adversarial review

Research Delegate, 2026-10-22 (ET). **Review only.** Nothing was run, loaded or computed. No existing file was edited.

- **Checked:** `/workspace/review/next_causal_question_planning_note_v1_1.md`, sha256 `7ecc9c8434918f8467db09b2b8038410a3d9c04f4dc077b840bb34d33c7965de`. This matches the hash the parent reported, with mtime 2026-10-22 00:01:03 ET.
- **Against:** my review `next_causal_question_planning_note_v1_adversarial_review_RD.md` (`81e2ac54…`), and Astra #34 (`bf724ca2…`).
- **Approval record cited in v1.1 §E:** `PI_STANDING_APPROVAL_2026-10-21_1515.md`, sha256 `5cc6f12a91d0…`. It matches the standing-approval prefix `5cc6f12a…`.

**Revision-in-place notice.** This file was revised in place under the same filename. Its first announced hash was `48f4cdc6c3b407c660e8ab003920d46695af1781d1487f5835533b56045f2fd9`; it is now `7ecc9c84…`.
- No copy of the `48f4cdc6…` content exists anywhere on the box (filesystem search by name), so the two versions cannot be diffed.
- This check covers **only `7ecc9c84…`**.
- The standing approval's stated conditions include "records are additive only". See N5.

## Verdict

**PASS WITH NOTES FOR CONSULT #35.**

B1 and B2 are resolved in substance. The major items are resolved or partial, and none of the partial ones blocks a consult. One drafting slip, N1, must be corrected before or alongside the consult. It is a one-line additive fix, or a flag in the consult text. As literally written, it would make every stage ineligible.

## Per-item status

| Item | Status | Reason (v1.1 location) |
|---|---|---|
| B1 roster | **RESOLVED** | §A L8–L12: PR #5 is out with no retrain. Primary roster is PR #7 s100–109 (cand_final, F-TRAINED, F-INIT); PR #8–#10 optional. The CAND XOR range CNA says was "not re-read" (L11) was verified by me from `recurrent_core_results_v1/seeds/s100–s109.json` @ `379bb01`. It still needs a citation in the spec. |
| B2 construction-guaranteed separation | **RESOLVED** (in substance; see N1–N3) | §B.1 L16–L20: the primary is a nested, held-out comparison of a marginal-only map against the full map, with its own floor and a rank rule. §B.3 L25 demotes the κ-edit, null(B) and marginal edits to descriptive. The test can fail on its own: the full map nests the marginal map, so its in-sample gain is never negative, but its held-out gain can be zero or negative. |
| M1 identification / mean-field | **RESOLVED** | §D L35–L39: three rivals are kept apart, the positive reads "κ-aligned local influence geometry" and bears at most on (iii) if Astra admits it, and "irreducible joint state" stays not established. The rival-L panel (my Q3) is not adopted, and it remains an open question for Astra. This is acceptable because "κ-aligned" wording is what I asked for in its absence. |
| M2 accuracy implies result | **PARTIAL** | §C L30 adds a triviality check, but its ineligibility rule is mis-stated (N1). Chord edits re-open the trap (N2). |
| M3 comparator by construction | **RESOLVED** | §A L10, L13 and §D L47: F-INIT and F-TRAINED are used, all contrasts are descriptive, and there is no Q-LEARN claim. Still unstated: whether cand_final or F-TRAINED is the primary edit target (PR #7 L186 used F-TRAINED). That is Q4 for Astra. |
| M4 E34-6 bounds | **PARTIAL** (non-blocking) | §C L31–L32: the stage is chosen from headroom, and every statistic gets a bound, an assessment stage and an unattainable-floor rule. But the bounds are not *named*. Fix: adopt the three from my review. (a) The nested gain is at most the held-out residual of the marginal-only map; this is checkpoint-dependent and outcome-dependent. (b) The forward-pass κ effect is at most ‖ε·L·e_κ‖ within the F-H3 ε bound; this is oracle-only. (c) Specificity is bounded by the conditioning of L; oracle-only. |
| M5 outcome map | **RESOLVED** | §D L41–L48: POSITIVE, NOT SHOWN, UNRESOLVED, NONLINEAR, MIXED, COMPARATOR ALSO PASSES and NEAR-ZERO. NOT SHOWN is never "outside a recurrently carried coupling" or "not causal", and E2 is untouched (L43). Wording nit in N4. |
| M6 holdout | **PARTIAL** (non-blocking) | §B.1 L17: orbit-respecting prefix holdout, with fits frozen before scoring. Still missing: how the split relates to the source TRAIN/TEST rule (my M6, bullet 3). Orbit-count feasibility is also new (N3). |

## Minor items (spot check)

| Item | Status | Note |
|---|---|---|
| m1 B wording | RESOLVED | §D L40, verbatim phrases adopted. |
| m2 edit size and saturation | **DEFERRAL ACCEPTABLE, with a condition** | See below. |
| m3 κ convention | PARTIAL | §B.3 L25 reports both the minimum-norm δ_κ and its affine class. The convention itself ("κ varies with μ_x and μ_y fixed, spin chart") is not stated, so state it in the spec. |
| m4 observables | RESOLVED | §D L40. |
| m5 4E[c²] scale | RESOLVED | §D L36. 4E[c²\|TEST] is still UNVERIFIED and is not needed. |
| m6 citations | PARTIAL | §F L74 fixes S12, S15 and E2. v1 §0's attribution of the chart-decoder argument to Astra #34 L46 is not superseded. One line in v1.2 or the consult text would fix it. |
| m7 S15 link | RESOLVED | §A L12, §F L75. |
| m8 oracle checks are computations | RESOLVED | §C L28, §E L53–L54. |
| m9 Q-CAUSE only | RESOLVED | §D L40 and §A L13. No Q-EXIST, Q-LEARN or Q-NECESSITY claim appears. |
| m10 multiplicity | RESOLVED (deferred to spec) | §F L78 and §D L41. That is right for a planning note. |

**Judgement on m2.** Deferring m2 to the spec is acceptable for a planning note going to Astra. The primary statistic, the nested held-out Jacobian comparison in §B.1, is ε-free and does not depend on the edit-size unit. ε matters only for the §B.2 edit families, the NONLINEAR branch and the oracle headroom and validity bounds.

The condition is that the ε unit (belief or state norm), the ε value and the saturation guard must be fixed in the **oracle-only scope record, before the prechecks are computed**. They should not be fixed later in the inference spec, for two reasons:
- The headroom precheck ‖ε·L·e_κ‖ and the F-H3 Fréchet validity bound cannot be defined without them.
- Fixing ε after seeing checkpoint Jacobians would make it outcome-dependent.

v1.1 should say so in one line. It need not set the numbers.

## Specific questions

**Can the nested comparison still pass by construction?** No, as specified. The full map always fits at least as well *in sample*, but the statistic is the gain *held out by prefix, respecting orbits* (§B.1 L17–L19). That gain can be at most zero. A floor set separately from headroom and a rank rule are both required (L19), though their values are deferred, which is acceptable.

Two caveats:
1. The only by-construction pass route left is an accurate network that is near-affine over the reachable cloud. §C's triviality check is meant to catch this, but it is mis-stated (N1).
2. "Without the κ row" in §B.2 L23 must mean the separately fitted marginal-only map B_μ. Deleting the κ row from the full B is not the nested model (N2b).

**Are the controls defined without using B?** Partly:
- **Full-state random edits:** B-free. ✔
- **Chord edits ε·(z_k(b) − z_k(a)):** data-defined and B-free. ✔ But see N2.
- **Equal-impact edits:** scaled by the network's own ‖J·δ‖, so B-free. ✔ The pattern-specificity score still needs a definition in the spec.
- **"Random edits within range(B)":** these **use B**, by construction. The state-space set is also mis-named: B is 3×H, so range(B) ⊂ ℝ³; the state-space set is row(B) = range(Bᵀ). These edits should be descriptive only. They should not count among the "edits it did not construct" in L24 (N2c).

**Are the oracle-only prechecks clearly not authorized to run yet?** Yes:
- §E L54: "Nothing runs until Astra rules on Q1–Q3, including the oracle-only computations".
- §E L53: the standing approval covers them only after "a written scope record and a freeze before any computation".
- §C L28 labels them computations.

This matches the Specialist's ruling, and the approval record's hash matches. ✔

**Is the wording in bounds?** Yes:
- "κ-aligned local influence geometry" (L39);
- Q-CAUSE characterization only (L40);
- "Irreducible joint state" stays not established (L39);
- no "not causal" or negative-mechanism reading (L43);
- no consciousness, C4/C5, "alive" or "autopoietic" language.

One nit in N4.

## New issues introduced by v1.1

- **N1 (MAJOR; one-line fix, must accompany the consult).** §C L30 says: "take an exact filter written in arbitrary affine coordinates, and a near-affine accurate surrogate … Check whether the test passes by construction. If it does, the stage is ineligible."
  - An exact filter in affine coordinates z = A·b + c has J(u) = L(u)·A⁻¹ exactly. It therefore *always* passes the κ-row test wherever L·e_κ is not collinear with the marginal responses.
  - Read literally, every eligible stage would be ruled ineligible.
  - **Fix:** the exact-affine filter is a **positive control**. It must pass, and if it fails the pipeline is invalid (UNRESOLVED). Only a pass by the **near-affine reachable-set surrogate** marks a stage as ineligible (low-information).
  - The surrogate's construction (its fitting class and the "accurate" tolerance) must be in the oracle-only scope record.
- **N2 (MAJOR, for the spec; can travel as a consult note).**
  - **(a)** Chord edits move along reachable differences. At ε = 1, an accurate network's response equals q*(b·u) − q*(a·u), so small-ε chord responses are largely implied by A-FIT plus near-affinity. This is the M2 trap again, inside the "edits B did not construct" criterion (L24). **Fix:** apply the §C triviality check to chord edits too. Do not let chord edits alone satisfy L24. Gate on full-state random and equal-impact edits; keep chords as an informative but non-gating family unless the surrogate fails on them.
  - **(b)** In L23, "without the κ row" must name the separately fitted B_μ.
  - **(c)** row(B) edits use B, so they are descriptive only. Correct "range(B)" to row(B) = range(Bᵀ).
- **N3 (MINOR, feasibility).** Orbit-respecting prefix holdout has very few groups at low k. The X-flip and Y-flip group {id, F_X, F_Y, F_XF_Y} acts freely once both streams have been read, so there are 2^k/4 orbits:
  - k = 3: **2 orbits**, so only a 2-fold, 4-versus-4 prefix split;
  - k = 4: 4 orbits;
  - k = 5: 8 orbits.

  This is my own group-order arithmetic and has not been checked against an enumeration. Add holdout capacity to the §C stage-eligibility criteria alongside headroom. Also say whether a single B is assumed to be shared across base points z_k(a) (stronger claim), or whether B is fitted per fold.
- **N4 (MINOR, wording).** "a pass in F-INIT means the geometry is not attributable to learned recurrence" (L47) reads like a Q-LEARN conclusion. Prefer: "…the geometry is **not attributed** to learned recurrence by this study (descriptive)."
- **N5 (MINOR, process).** v1.1 calls itself "additive" (L1), but it was revised in place under the same filename, and the `48f4cdc6…` content is not preserved. **Fix:** CNA adds a one-line additive record, for example in a v1.2 or a short revision note, saying `48f4cdc6…` was superseded in place by `7ecc9c84…`, with what changed. Consult #35 should cite `7ecc9c84…` explicitly. Future revisions should use new filenames.

## For consult #35

Send v1.1 (`7ecc9c84…`) with the following:
- an N1 correction line;
- the N2 notes;
- the m2 condition;
- my open questions: Q1 (off-manifold admissibility), Q2 (the nested test as primary, and which edit family gates), Q3 (the rival-L panel and the R-MF-A excess) and Q4 (the primary target, cand_final or F-TRAINED).

Q5 is settled by the Specialist under the standing approval (§E).
