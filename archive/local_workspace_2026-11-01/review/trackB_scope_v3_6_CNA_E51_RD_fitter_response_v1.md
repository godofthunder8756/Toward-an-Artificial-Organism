# Track B v3.6 freeze prep: CNA response to RD's E51-2 / E51-3-fitter file (R-1 to R-9, including RD's R-4 t_r rule) (CNA v1)

- **Author:** CNA. **Written:** 2026-11-01 13:22:25 EST (America/New_York, from `date` at write time). Additive; no read-only file is rewritten.
- **Status:** PLANNING ONLY. Nothing stochastic, no optimizer and no timing were run.
  - The only computations were SHA-256, exact binomial sums, and deterministic **noise-free** (σ = 0) float64 evaluation of the frozen recursion and bisection (`/workspace/scratch/cna_e51/r36.py`, system `python3`, no RNG).
  - Floats are from the box libm and are **UNVERIFIED for the pinned libm (P6)**.
- X1–X5 unchanged. Astra not contacted. No consciousness claims.
- **Inputs (sha256 recomputed, MATCH):**
  - RDF = review/trackB_freezeprep_v2_7_E51_2_E51_3fitter_RD.md: **b59b5a14640c54cf279904adfc0eefa134ba2ee1db586d056b58a5338877033d**, footer **1d99454ad1165544…** (recomputed, MATCH), 443 lines, read in full.
  - CE51 bc27d6959e90…; CNA hysteresis v2 (HY2) 2df5d27eb166…; V26 ff03eb81c158…; A50 59e93cfffa8f…; A51 f7f35ec21d37…; M ab80afa56ac1…; MP 1d5458e3319b…
- δ = s_c/4 = 0.133209993838388 throughout.

## 1. R-3: LIM noise-free transition, verified independently
**Method.** Frozen recursion x ← x + h·(−x + tanh(2x + s)): h = 1/100, n_EM ∈ {200, 300, 500} integers, x_0 = x_lo = −x\* = −0.9575040240772688, grid s = fl(s_c·m)/4.
- s_nf(t_r) := inf{s : x_nf ≥ 0}. It is unique because the map is increasing in x and in s (RDF L73).
- I found it by 80-step bisection on s in float64.

| t_r | s_nf (mine, float64) | s_nf/δ | RDF L82–L84 (50-digit) | Match |
|---|---|---|---|---|
| 2 | 1.060092665585969 | 7.958 | 1.0600926655859691 | yes (17 sig.) |
| 3 | 0.8770182657054675 | 6.584 | 0.87701826570546710 | yes |
| 5 | 0.7235713606755455 | 5.432 | 0.72357136067554556 | yes |

**Noise-free class per grid point (H iff x_nf ≥ 0), as LO/HI strings over the 9 points:**

| Offset | t_r = 2 | t_r = 3 | t_r = 5 | Margin to s_nf (δ), t_r = 2 / 3 / 5 | min \|x_nf\| |
|---|---|---|---|---|---|
| LIM/0, −7 | LLLLLLLLL | LLLLLLLLL | LLLLLLLLL | 6.958 / 5.584 / 4.432 below | 0.9416 |
| LIM/1, +7 (frozen) | **LHHHHHHHH** | HHHHHHHHH | HHHHHHHHH | **−0.958** / 0.416 / 1.568 | 0.0161 |
| LIM/1, +11 (RD) | HHHHHHHHH | HHHHHHHHH | HHHHHHHHH | **3.042 / 4.416 / 5.568** | 0.5525 |

- **LIM/0 at −7 cannot move the other way.** RDF L74 (fact 2) shows x_nf < 0 for every s ≤ s_c at every n_EM. Finite-time lag only **delays** ignition, so s_nf(t_r) > s_c, and LIM/0's top point δ = s_c − 3δ keeps its 3δ guarantee; the actual margins are 4.43–6.96δ. Confirmed on the box: all 27 classes LO, with min |x_nf| = 0.9416 ≫ 10⁻⁶ (RDF L68 robustness assertion).
- **LIM/1 at +11:** the margins 3.042 / 4.416 / 5.568δ reproduce RDF L82–L84. max |u| = fl(s_c·19)/4 = **2.5309898829293718 ≤ S_max = 8**. Min |x_nf| = 0.5525 passes the 10⁻⁶ assertion.
- **Final offsets (CNA, PROPOSED for Lead ruling): LIM/0 = −7, LIM/1 = +11.** This supersedes PP L81–L82's ±7 and makes "3 steps outside" a claim about the finite-time recursion (RDF L144). The stochastic and fitted location stays measured, not asserted (A51 L123; RDF §3.3). I adopt RDF §3.3's claim text.
- **Knock-on to HY2 L30:** the LIM/1 hysteresis offset becomes o = +11, so m′ = 2m + 11 ∈ {3,…,19}, max |u| = 19δ. LIM/0 keeps o = −7.
- **Cost:** none. FX-LIM is 18,000 noise-free steps, once (RDF L69).

## 2. R-6: IGN-P1 grid rescaled (an offset suffices)
- **Problem (RDF L238).** On S = (0…8δ), s_nf(2) = 7.958δ sits 0.042δ below s_9, inside NL-7's EDGE zone.
- **Proposal:** keep 9 points, keep δ and keep the pinned rounding rule. **Shift the offset to o = +3**, i.e. S′ = {fl(s_c·m)/4 : m = 3…11} = [0.39963, 1.46531].

| Offset o | Grid [s_1, s_9] | t_r = 2 (from s_1 / to s_9) | t_r = 3 | t_r = 5 | Min margin |
|---|---|---|---|---|---|
| 0 (current) | [0, 1.06568] | 7.958 / **0.042** | 6.584 / 1.416 | 5.432 / 2.568 | 0.042 |
| +2 | [0.26642, 1.33210] | 5.958 / 2.042 | 4.584 / 3.416 | 3.432 / 4.568 | 2.042 |
| **+3 (PROPOSED)** | **[0.39963, 1.46531]** | 4.958 / 3.042 | 3.584 / 4.416 | 2.432 / 5.568 | **2.432** |

- At o = +3 every noise-free transition sits ≥ 2.43δ inside both ends; +3 is the integer offset that maximises the minimum margin.
- MP L62 "spanning floor to saturation" still holds for P1:
  - s_1 = 3δ < s_c, so the trial stays on the low branch;
  - s_9 = 11δ, where all t_r are HI.
- **S′ hex (m = 3…11):** 3fd99389a146f52b, 3fe10d066b84a372, 3fe550480665cc4e, 3fe99389a146f52b, 3fedd6cb3c281e08, 3ff10d066b84a372, 3ff32ea738f537e0, 3ff550480665cc4e, 3ff771e8d3d660bd.

**Shared-grid rows move together (PROPOSED).** N1, NC1, NC2 and NC2r are P1's matched rows (MP L84–L87), so they take S′ as well.
- NC1 thresholds shift with the centre (s_c = 4δ → 7δ): m_θ ∈ {6, 8} (Δs = 2) and {5, 9} (Δs = 4).
  - max |θ| = 9δ = 1.19889. That exceeds CE50 L131's "|θ| ≤ 1", which is my own proposal, so I **amend it to |θ| ≤ 1.25**. S_max = 8 still governs |u|.
  - New NC1 x_lo values: m_θ = 8 → −0.9087031524247506 (bfed1418a22df70c); m_θ = 9 → −0.930792199865659 (bfedc90cb9396fd4). m_θ = 5 and 6 are as in CE51 §6.
- Graded rows no longer start at their own floor: N1's x_nf(s_1) is 0.44–0.58 across t_r. That is acceptable for a matched negative, but I flag it (L-C3).
  - Noise-free mid-range crossing (an interpolation proxy, not ŝ\*): 4.97–5.17δ. That is mid-grid, so EDGE is not implied.
- **max |u| recheck.** S′ ≤ 1.46531; LIM/1 ≤ 2.53099; NC1 |s − θ| ≤ 6δ; |u_null| ≤ 9δ = 1.19889. All are ≤ 8, so the (i′) sweep passes.
- **NC2 ceilings: the CE51 §8 table and its 27 readouts are SUPERSEDED** if S′ is adopted. New values (UNVERIFIED for P6):

| t_r | c_{4/5} (j = 8) | hex | c_{3/5} (j = 6) | hex |
|---|---|---|---|---|
| 2 | 0.8030739364436792 | 3fe9b2c81ca9756e | 0.7576921175511115 | 3fe83f038a2a3558 |
| 3 | 0.891638588128624 | 3fec884da5fba654 | 0.8480978820585415 | 3feb239e2b67f215 |
| 5 | 0.9391077255978645 | 3fee0d2ba51ba401 | 0.898999438497354 | 3fecc49a786efdf1 |

- **Hysteresis grid H (HY2 L28):** H = fl(s_c·m′)/4 over [−2s_c, 2s_c] is independent of the probe grid, so it is **unaffected** for P1 and the graded rows. Only LIM/1's offset changes (§1).
- **Cost:** none. Counts are unchanged.

## 3. R-9: LIM scoring, PI-SSTAR-NL causes, H0 skew
- **Adopted (RDF L199–L207):** a LIM replicate is **correct** only if every selection fit is non-locatable for an acceptable reason:
  - NL-6 in the expected direction (OUTSIDE-HIGH for LIM/0, OUTSIDE-LOW for LIM/1), NL-3/NL-4, or NL-5;
  - **and**, under R-4 (§5), this holds at all three t_r.
- **Incorrect** if any fit is in-grid locatable, EDGE (NL-7), wrong-side OUTSIDE, FIT-FAIL (NL-1) or RESTART-DISAGREE (NL-2). A MET, NOT MET or BOUNDARY label at LIM is incorrect and reported individually.
- The carve-out is keyed only by the frozen row ID; a key-hash mismatch is B-INTEG (RDF L198).
- **Supersession:** CE51 L44's IGN-LIM clause ("it scores as a correct outcome there", plus the three-cause list) is **superseded** by RDF §4.1 NL-1…NL-7 and §4.4.
  - PI-SSTAR-NL now has the seven causes NL-1…NL-7. It is counted **once per replicate**, and non-finite values stay construction failures (RDF L170).
- **H0 skew: FLAG.** MP L65 writes "w | s ~ F(μ(s), σ(s), γ(s))", with γ(s) as a function of s, but gives no functional form ("γ is a skew-normal shape"). RDF L285 reads it as a constant per c-level, which is the minimal reading.
  - A constant γ makes H0 less flexible. That favours H1 (ΔLL), which is **anti-conservative on the false-MET rows**.
  - **CNA recommends linear γ(s)**, using the same endpoint parametrisation as σ: γ₁ and γ₉ at s_1 and s_9, linear in between, both in [−10, 10], so γ(s) stays in bounds by convexity. This matches the literal "γ(s)".
  - It adds 1 parameter and changes no fit count. RD's H0 gradient fixture (RDF L368) should use this form. Lead ruling L-C5.

## 4. R-1 (worst-case false-MET screen, FM_wc) and R-2 (PI, not BLOCKING)
**Named amendment AM-FMWC (A-2026-10-24; PROPOSED; extends ROW0-FL v2's logic to MP L198 rows).** It applies per (row, dose) to IGN-N1, IGN-NC1/0–1, IGN-NC2/0–1 and the network confound rows BOTT/·, RINIT/·, ARCH/·.
- **Definitions.** n_MET = valid false METs; n_NM = valid NOT METs; n_PI = replicates without a valid label for any PI cause (PI-SSTAR-NL, PI-FIT-NC, PI-IGN-QUOTA, PI-CAP, PI-OPINT, PI-TR-SPLIT if adopted, or an IGN gate UNAVAILABLE such as G-iii). Each replicate counts once.
- **FM_wc = (n_MET + n_PI) / (n_MET + n_NM + n_PI).** **BINDING:** point ≤ 0.05 **and** one-sided 95% CP upper ≤ 0.08 (MP L198; AM-8).
- The literal false-MET rate n_MET/(n_MET + n_NM) is REPORTED. B-\* causes keep CE51 §5 / M L3422 treatment.
- **Hedge closed (exact; CP upper by bisection on the exact binomial):**

| Case | Count | Point | CP upper | Result |
|---|---|---|---|---|
| 20 false METs of 200 | 20/200 | 0.100 | 0.14199 | FAIL |
| 12 of the 20 recoded as NL, NL excluded | 8/188 | 0.0426 | 0.07547 | PASS (hedge) |
| 12 recoded as NL, NL as non-MET (M L3422) | 8/200 | 0.040 | 0.07101 | PASS (hedge; RDF L182) |
| **FM_wc** | (8 + 12)/200 | 0.100 | 0.14199 | **FAIL** |

- The boundary at 200 is unchanged: 9/200 passes (0.07721) and 10/200 fails (0.08334). FM_wc ≥ literal, because (a + x)/(b + x) ≥ a/b.
- **Consequence to disclose (L-C1).** The negatives now need a **valid NOT MET** to count as correct. That was already implicit in MP's design (MP L70: the dip test uses "the two grid levels nearest the fitted transition"), but M L3422 had hidden it by treating UNAVAILABLE as a favourable non-MET.
  - A graded negative whose H1 fit is often NL-5/NL-6 will now FAIL. That is the honest outcome ("cannot assess the negative"), and it is measured in calibration (N1, NC1 and NC2 are in C_cal).
- **R-2 opinion: PI, not BLOCKING.** NL-1…NL-7 and PI-FIT-NC (all F1 restarts failed; RDF L334) are data-dependent estimator outcomes, an "ordinary incomplete assessment allowed by the protocol" (A51 L31). They are not construction or integrity defects (A51 L30).
  - Counting them adverse in S_wc/FM_wc removes any incentive.
  - T-4 (non-finite) stays B-RUN and T-5 (non-reproducible) stays B-INTEG (RDF L324–L325).
  - This lifts CE51 L53's default for these codes (RDF C-1).
- **Cost:** none (counting only).

## 5. R-4: RD's t_r rule, assessed and amended
**Frozen text.** M L1128 names a **primary** readout delay: "t_r = 3τ in plants; 5 steps in networks".
- The {2, 3, 5}τ / {3, 5, 8}-step grid is V25 R7 "provisional" (V25 L26, L198). A50 L155 accepted it, but only with selection on selection data: "Selection among them must use selection data; final outcomes cannot choose the winning time."
- No t_r selection statistic exists in any text (RDF L225).
- **Per the brief, the frozen primary overrides RD's all-three rule for licence/power rows only.**

**Amended rule (CNA, PROPOSED; pre-nonlinearity readout only, M L314):**
- **Licence/power rows (IGN-P1 power, network licence labels):** the label is read at the **primary t_r** (3τ plants; 5 steps networks). Locatability is also required at the primary only. Other t_r are REPORTED.
  - Under S′, P1's primary margins are 3.584δ and 4.416δ.
- **False-MET rows (N1, NC1, NC2, network confounds): union over all three t_r.** Precedence per replicate:
  - (1) a valid MET at any t_r → false MET;
  - (2) otherwise, any t_r without a valid label → n_PI (FM_wc adverse);
  - (3) otherwise NOT MET.
  - Counted once per replicate.
- **LIM:** correct only if correct at all three t_r under §3.
- **Named amendment AM-TR:** M L376's "t_r" design-selection item is withdrawn for IGN, replaced by the fixed primary (licence rows), union (false-MET rows) and all-three (LIM) rules.
  - No final outcome chooses a time, so A50 L155 is respected.
  - R-4's missing selection statistic is no longer needed. The every-fit rule (RDF R-5) then binds over the t_r each rule uses.

**(i) Multiplicity.** Per-t_r false-MET probabilities p₂, p₃, p₅ give a union probability with **max p_t ≤ P(union) ≤ min(1, Σ p_t) ≤ 3·max p_t**.
- All t_r are read from one trajectory per trial (V25 L198) and share the selection fits, so the events are strongly positively correlated. The realised inflation should sit well below 3×, but **only the bound is claimed**; the actual ratio is unknown before data.
- MP L198's rate is the rate at **one** (selected) t_r. The union is a **stricter estimand**: a conservative choice, but a scope change. It is named under AM-TR and must be disclosed in #52.
- It cannot raise any licence and cannot lower any false-MET rate.
- **Recommendation:** adopt the union, because the instrument must be specific at every admissible readout time, which closes t_r cherry-picking (RDF H-3).

**(ii) PI-TR-SPLIT.** It is **not needed** under the amended rule:
- licence rows use one t_r;
- in false-MET rows a split is a false MET (valid, adverse);
- at LIM a split is incorrect.
- **Reserve the code:** if the Lead rejects the M L1128 primary and keeps RD's all-three rule for licence rows, add **PI-TR-SPLIT** to the CE51 §2 PI list (PI; pr_i = 0; adverse in S_wc/FM_wc; never PASS).

**(iii) S_wc.** S_wc applies to GA-1/AM-15 rows, which have no IGN t_r, so there is no interaction.
- For IGN rows the analogue is FM_wc (§4). A union-rule MET enters it as a literal false MET in numerator and denominator.
- A t_r without a valid label enters as n_PI. A replicate with several causes counts once (MET first, then PI).
- **Cost:** none in trials. The fits are the RDF L410–L411 worst case (F2 666,000 / 846,000 calls) whatever the rule, since every t_r is still fitted.

## 6. Needs the Lead's ruling
| # | Item | CNA position |
|---|---|---|
| L-C1 | AM-FMWC worst-case false-MET screen (R-1), including disclosure that negatives now need a valid NOT MET | Adopt |
| L-C2 | R-2: NL-1…NL-7 and PI-FIT-NC listed as PI; T-4/T-5 stay B-RUN/B-INTEG | Adopt |
| L-C3 | R-3: LIM/0 −7, LIM/1 +11, with FX-LIM and RDF §3.3 claim text; R-6: P1-matched grid S′ (o = +3) for P1/N1/NC1/NC2/NC2r; NC1 m_θ {6, 8}/{5, 9}; amend CE50 L131 to \|θ\| ≤ 1.25; NC2 ceilings superseded; LIM/1 hysteresis o = +11 | Adopt before calibration |
| L-C4 | R-9: RD's LIM scoring at all three t_r; CE51 L44 superseded | Adopt |
| L-C5 | H0 γ(s) linear in s (endpoint form) instead of a constant (MP L65) | Adopt (conservative) |
| L-C6 | AM-TR: primary t_r (M L1128) for licence rows; union for false-MET rows; all-three for LIM; M L376 t_r selection withdrawn for IGN; PI-TR-SPLIT reserved | Adopt; disclose the union scope change in #52 |
No item changes the scheduled 4,005,072,000 + 45,720,000·n or any fit count.

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 9fad9d8015a631f63c49d65866958cf5a039371a5bd5ebdd8a96b56370c96574
