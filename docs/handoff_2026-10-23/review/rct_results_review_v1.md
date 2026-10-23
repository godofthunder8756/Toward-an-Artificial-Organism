# Independent review: recurrent-core transfer results, PR #7 (v1)

**Scope.** This review covers draft PR #7 (branch `cursor/recurrent-core-transfer-2669`), freeze `d118ae1` (2026-10-21 01:21 UTC, i.e. 9:21 PM ET Oct 20) and results `5157f5d` (10:02 PM ET).

**Method.** This was a read-only review. I worked in a scratch clone at `/workspace/scratch/pr7/clone`. The analysis scripts are in `/workspace/scratch/pr7/analysis/` (`recompute.py`, `grid.py`) and read only the committed raw JSON. Nothing was retrained, rerun, frozen, committed or pushed. There are no C4 and no consciousness claims. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate.

## 0. Bottom line

- **Protocol:** byte-identical to FINAL (sha256 `63c463c7…`; `cmp` reports identical).
- **The verdict code is correct.** Recomputed from the raw seed JSON, the joint transfer + SPECIFIC passes are:

  | k | joint passes | invalid | passing seeds |
  | --- | --- | --- | --- |
  | r | **1/10** | 0 | 102 |
  | z | **3/10** | 0 | 101, 102, 104 |
  | n | **3/10** | 0 | 101, 106, 107 |

  These match the code's `specific_pass` flags exactly. The "1/10", "3/10" and "3/10" in RESULTS.md are **pass counts**. They are not counts of seeds failing SPECIFIC, and the cloud agent's summary table invited that misreading. No matrix reaches 8/10, so **SPECIFIC(k) NOT DEMONSTRATED for r, z and n is the correct literal label**.
- **Transfer.** TRANSFER SHOWN 10/10, E1 REPLICATED 10/10, F-INIT A-FIT 0/10, F-TUNED32 A-FIT 0/10. All were recomputed and confirmed.
- **Advantage over the tuned rival.** ADVANTAGE OVER TUNED FROZEN GRU-8 (843 TRAINABLE) OBSERVED holds in 10/10 seeds, with ratio843 between 0.029 and 0.103. "TUNED FROZEN GRU-8 MEETS A-FIT AT THIS BUDGET" is not met (0/10). Both were recomputed and confirmed.
- **The claim text is garbled by a cosmetic assembly bug.** The corrected literal text is in §2. An additive erratum is needed. No rerun is needed.
- **The grid-edge problem is real.** g* = 2, the **upper** g bound, in **10/10** seeds. b* = −2, the lower b bound, in 9/10. The tuned rival is plausibly under-tuned within its family. The advantage label (i) is very unlikely to be grid-limited, but label (ii) could be (§3). This needs a qualifier erratum. A wider-grid robustness study is proposed; it is new training and needs separate approval.
- **Approval.** Aidan approved the training directly at **8:55 PM ET**, after Astra had cleared the protocol and before the freeze at 9:21 PM ET. The approval was therefore in place. The hashed header's "pending" line is stale documentation (§5). It needs a provenance erratum, not a rerun.

## 1. SPECIFIC recomputation (FINAL §5 rules)

**Rules applied.** For each seed and each k, the seed passes only if all of the following hold:
- it passes transfer;
- B = E(F-INIT) − E(F-TRAINED) > 1e-12;
- ‖δ_k‖_F > 1e-12;
- **ΔE_k > every one of the 32 matched-norm ΔE_rand** (a directional comparison);
- ΔE_k > 1e-12 and ΔE_k ≥ B/4;
- sham ≤ 1e-12, restore ≤ 1e-9, and outputs finite.

If more than 2 seeds are invalid, the verdict is UNRESOLVED.

**Validity.** Every seed has transfer = True and B equal to the recorded `benefit_B`. All sham and restore gaps are exactly 0, so 0 seeds are invalid.

In the table, "beat" counts how many of the 32 random draws the reversion ΔE exceeded, "dir" is the directional condition, and "≥B/4" is the materiality condition.

| seed | B/4 | r: ΔE | r: beat | r: dir | r: ≥B/4 | r: **SPEC** | z: ΔE | z: beat | z: dir | z: ≥B/4 | z: **SPEC** | n: ΔE | n: beat | n: dir | n: ≥B/4 | n: **SPEC** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | 0.01182 | 0.00313 | 32 | ✔ | ✘ | ✘ | 0.00627 | 32 | ✔ | ✘ | ✘ | 0.05233 | 29 | ✘ | ✔ | ✘ |
| 101 | 0.01118 | 0.00438 | 32 | ✔ | ✘ | ✘ | 0.02131 | 32 | ✔ | ✔ | **✔** | 0.05352 | 32 | ✔ | ✔ | **✔** |
| 102 | 0.01298 | 0.01896 | 32 | ✔ | ✔ | **✔** | 0.01550 | 32 | ✔ | ✔ | **✔** | 0.08633 | 31 | ✘ | ✔ | ✘ |
| 103 | 0.01586 | 0.00708 | 32 | ✔ | ✘ | ✘ | 0.00655 | 32 | ✔ | ✘ | ✘ | 0.07581 | 31 | ✘ | ✔ | ✘ |
| 104 | 0.00865 | 0.00498 | 32 | ✔ | ✘ | ✘ | 0.01051 | 32 | ✔ | ✔ | **✔** | 0.05285 | 30 | ✘ | ✔ | ✘ |
| 105 | 0.01422 | 0.00320 | 32 | ✔ | ✘ | ✘ | 0.00917 | 32 | ✔ | ✘ | ✘ | 0.04056 | 24 | ✘ | ✔ | ✘ |
| 106 | 0.00970 | 0.00207 | 32 | ✔ | ✘ | ✘ | 0.00741 | 32 | ✔ | ✘ | ✘ | 0.04698 | 32 | ✔ | ✔ | **✔** |
| 107 | 0.01404 | 0.00373 | 32 | ✔ | ✘ | ✘ | 0.00537 | 31 | ✘ | ✘ | ✘ | 0.03711 | 32 | ✔ | ✔ | **✔** |
| 108 | 0.01537 | 0.00219 | 31 | ✘ | ✘ | ✘ | 0.01086 | 32 | ✔ | ✘ | ✘ | 0.05698 | 24 | ✘ | ✔ | ✘ |
| 109 | 0.01293 | 0.00195 | 31 | ✘ | ✘ | ✘ | 0.00706 | 32 | ✔ | ✘ | ✘ | 0.05810 | 31 | ✘ | ✔ | ✘ |

**Condition counts (out of 10 seeds):**

| k | directional | materiality (≥ B/4) | joint SPECIFIC | label |
| --- | --- | --- | --- | --- |
| r | 8 | 1 | **1** | NOT DEMONSTRATED |
| z | 9 | 3 | **3** | NOT DEMONSTRATED |
| n | 3 | 10 | **3** | NOT DEMONSTRATED |

ΔE and B/4 values are TEST E_total. The full values are in `specific_recompute.json`.

**Code check.** `recurrent_core_transfer_verdicts.specific_joint` implements exactly these rules. `label_specific` applies the ≥ 8/10 rule and the more-than-2-invalid rule correctly. **There is no verdict-code bug.**

**Descriptive reading (no label effect; not a causal claim):**
- **r and z.** Reverting r or z to its initialization hurts more than random perturbations of the same norm in most seeds: 8/10 for r and 9/10 for z. But the loss is small next to the transfer benefit B, so the materiality bar fails in most seeds.
- **n.** Reverting n always causes a material loss, larger than B/4 in 10/10 seeds. But matched-norm random perturbations of W_hn are often just as damaging, so the directional bar fails in 7/10 seeds. That pattern fits generic sensitivity of W_hn. It does not show anything specific to the learned direction.
- **n variation statistic.** n's per-seed variation condition holds in 9/10 seeds: PR is 0.01–0.10, and CR is ≥ ¾ except in seed 101, where it is 0.736. This is descriptive only. The label requires REPLICATED SPECIFIC(n), so it is correctly "selective variation reduction not demonstrated" (deviation #13). The "(9/10)" in RESULTS.md should be marked as a descriptive count.

## 2. Correct earned claim (FINAL §6, the "TRANSFER SHOWN, no REPLICATED SPECIFIC(k)" branch)

The garble comes from `assemble_claim`. It writes `"Tuned-rival results: %s. %s (%d/10)."` and fills the second slot with the bare constant `RIVAL_AFIT_NOT = "not met"`, so the label being negated is never named. The variation line also lacks a final period.

**Corrected literal claim:**

> In W2, recurrent training produced a GRU-8 core whose predictive advantage over its matched initialization survived replacement and retraining of the readout. Hidden-to-hidden matrix reversion did not meet the prespecified joint criterion for any matrix.
>
> Tuned-rival results (reported independently): ADVANTAGE OVER TUNED FROZEN GRU-8 (843 TRAINABLE) OBSERVED (10/10). TUNED FROZEN GRU-8 MEETS A-FIT AT THIS BUDGET: not met (0/10). F-TUNED32 A-FIT on TEST: 0/10 (descriptive). Within the declared 3×3 grid, g* was at the upper g bound in 10/10 seeds (§3).
>
> Variation results: r, z, n: selective variation reduction not demonstrated.

## 3. Grid-edge assessment (tuned rival)

**Observed.**
- (g*, b*) = (2, −2) in 9/10 seeds and (2, 0) in seed 100. **g = 2 is selected in 10/10.**
- In every seed, VAL risk falls monotonically along g at b = −2: the ratio crit(1,−2)/crit(0.5,−2) is 0.78–0.97, and crit(2,−2)/crit(1,−2) is 0.65–0.88.
- Moving b from 0 to −2 at g = 2 helps in 9/10 seeds (ratio 0.56–0.99).
- The best VAL risk is 0.030–0.044, against 0.038–0.057 at the centre point (1, 0). So the 3×3 search bought only about 10–40%.

**The optimum is very likely outside the grid**, toward larger g and possibly more negative b. The rival is under-tuned within its declared family.

**How much this matters for each result:**
- **(i) Advantage label: unlikely to be grid-limited.** CAND TEST E is 0.0012–0.0045 and R-TUNED843 is 0.037–0.051, so ratio843 is 0.029–0.103. For the rival to defeat (i), its error must fall to at most 2 × CAND, roughly a **10–34× improvement**. The 3×3 grid's whole gain was about 1.1–1.7×. This cannot be excluded, but it would take a qualitatively different regime.
- **(ii) Rival A-FIT: plausibly grid-limited.** The TEST A-FIT total gate is about 0.0204, and the rival sits at about 0.037–0.051. Roughly a **1.8–2.5× improvement** would flip some seeds. A wider grid is a meaningful robustness check for (ii) and for the descriptive F-TUNED32.
- **Primary transfer verdict: unaffected.** Transfer is tested against F-INIT, the untuned matched initialization, which the grid does not touch.

**Deviation #2.** It defines "edge" as any point other than (1, 0). That is literal, but on a 3×3 grid it makes the flag uninformative, because 8 of the 9 points are edges. Results should state *which* bound was hit (g upper, 10/10).

**Proposed wider-grid robustness check.** This is a proposal only, with no runs. It is **new training and requires Aidan's separate approval** plus an Astra review.
- **Family unchanged.** Frozen GRU-8 at each seed's own init W^0, using the same two knobs: g scales `weight_hh_l0`, and b is the update-gate preactivation offset.
- **Grid.** g ∈ {1, √2, 2, 2√2, 4, 4√2, 8} × b ∈ {−6, −4, −3, −2, −1, 0}, giving 42 configurations per seed. The b ≥ +1 region is dropped: b = +2 was worst at every g in 9/10 seeds (seed 101 is the exception), with VAL risk 0.051–0.105.
- **Procedure, as FINAL §2.** Per-seed selection on the same balanced 48-history VAL set, the 8→70→3 readout (843 trainable), 4000 steps, and the 6000+s readout seed. Refit on all 192 TRAIN histories, evaluate TEST once, and keep the same tie-break (smaller |log₂g|, then |b|, then b, then g).
- **Preregistered edge rule.** If g* = 8 or b* = −6 in ≥ 3/10 seeds, report "TUNED RIVAL STILL EDGE-LIMITED", with no further extension inside the study.
- **Outputs.** The labels (i) and (ii) under the new grid, reported alongside, not replacing, the PR #7 labels. Selection compute is charged separately: 420 selection runs plus 10 refits.
- **Optional.** Add the matched 8→32→3 head on the selected configuration as a new F-TUNED32′ (descriptive).

## 4. Meaning of "P1 not met 0/10 for every arm"

- **What the label is.** P1 is "DECODER PREDICTIVE AND CROSS-FOLD STABLE". It requires held-out R² ≥ 0.9 on m_x, m_y and c on both parity folds, **and** a largest inter-fold principal angle ≤ 30°. That was met in 0/10 seeds for CAND, F-TRAINED and F-INIT.
- **Why it fails.** It fails on **both** criteria in every seed:

  | core | held-out R²(c), median (min) | R²(m_x), median | R²(m_y), median | largest inter-fold angle |
  | --- | --- | --- | --- | --- |
  | trained | −0.59 (−7.85) | 0.83 | 0.985 | 50–83° (median 72°) |
  | init | −1.49 | 0.60 | 0.97 | 42–89° (median 67°) |

  In words, the cross-fitted linear stage-4 chart decoder does not predict the covariance coordinate, which is the joint-information part, on held-out prefixes, and the two folds pick very different 3-d subspaces.
- **Why CAND is included.** CAND and F-TRAINED share the same trained recurrent core, and P1 depends only on the stage-4 states, not on the readout. Their P1 records are **identical in every seed** (verified). So there are really two cores per seed, trained and init, not three independent arms.
- **Label effect: none.** P1 is additive and descriptive (FINAL §7.1). It gates no transfer, SPECIFIC, variation or rival label, and no E3 test was run on these cores.
- **Interpretation.** The PR #5-style linear chart-decoder intervention would be **decoder-limited** on these cores. That supports Astra's consult #11 reading that PR #5's E3 null does not establish the absence of a low-dimensional mechanism. It does not show any representation is absent, and it is not causal evidence.
- **P2 PIPELINE VALID.** This shows the E3-v2 instrument detects a known linear 3-d code. Together with P1, the tool works in principle, but its linear decoder does not fit these networks. P2 says nothing about the networks' own mechanism.

## 5. Deviations review (25 items)

All 25 are in the freeze commit `d118ae1`, so they were logged **before** training. Their sha256 `bc734055…` is identical at freeze and at results.

| # | Assessment |
| --- | --- |
| 1 | Faithful. N(0, 1/5) means variance 1/5. |
| **2** | Literal but uninformative: on a 3×3 grid, 8/9 points are "edges". **Erratum:** report which bound was hit (g upper in 10/10; b lower in 9/10) and qualify label (ii) as "within the declared grid" (§3). |
| 3–6 | Faithful (#6 is the FINAL PD/CD exception). |
| **7** | Faithful. The §3 gate is the direct inequality, and E3-v2 is used only for the reported ratios, as FINAL §3/§7.0 intends. No label effect. |
| 8–11 | Faithful. #10 makes any sham or restore failure invalidate the seed for all of §5, which is conservative and moot because 0 seeds were invalid. |
| **12** | Faithful to FINAL §5: transfer, B or δ failures are non-passes, not invalid. It is also moot, because no seed failed transfer, B or δ. **This is not the source of the low counts**: the binding conditions are materiality (r, z) and directional (n) (§1). |
| **13** | Faithful. But RESULTS prints the per-seed variation counts, e.g. n "(9/10)", next to the failure label without saying they are descriptive. **Erratum (presentation):** mark them "descriptive per-seed condition count; label requires REPLICATED SPECIFIC". |
| 14–16 | Faithful. Readout initialization is identical across cores within a seed, and selection does not read TEST. |
| **17** | Faithful. Using the held-out mean as the R² baseline is the stricter choice, and "not met" for the negative label is acceptable. No label effect. A note that CAND and F-TRAINED P1 are identical by construction should be added. |
| 18 | Acceptable. Coverage and rank are not per-draw gates in P2, which matches the frozen suite's per-draw `localized`. Flag for Astra. |
| 19 | Faithful (s = 0 side state, as FINAL §7.2). |
| **20** | The P2− ψ caching (reusing the exact ψ when Rᵀz matches within 1e-8) makes the required zero-effect check **partly true by construction**: a Q-copy transplant leaves Rᵀz unchanged to roundoff, so the cached ψ is reused. P2− is descriptive and its validity gates only P2−, so there is no label effect. **Erratum (disclosure):** state this beside "P2− zero-effect: True (0.0)". |
| 21 | Faithful (the descriptive suite is not a gate). |
| **22** | **Approval provenance.** The hashed FINAL header still says "Approval gate (still pending)" and "nothing is committed or frozen in the repo". Both lines were written before the freeze, while approval was pending. The record of the approval is below this table. **Erratum:** add a dated provenance note. Do not edit the hashed protocol. No rerun is needed. |
| 23 | Faithful (the smoke test is not a result). |
| 24 | Faithful labelling, but it is the source of the claim-text garble (§2). **Erratum.** |
| 25 | Faithful. It applies only if a success occurs, so it is moot. |

**Approval record (#22).** I checked the Specialist's transcript:
- The Specialist asked Aidan, through a question widget, to approve the neural training for this study.
- At **8:55 PM ET on 2026-10-20, Aidan answered "Yes, approve it once Astra clears it."**
- Astra consult #12, FREEZE WITH NAMED EDITS, had already cleared the protocol, and the FINAL protocol (sha 63c463c7) applies its edits.
- The freeze commit then landed at 9:21 PM ET, and the results at 10:02 PM ET.

The approval therefore preceded the freeze and the training. Its condition (Astra clearance) was satisfied, and the freeze manifest records it. **Training did not run without approval.** The only defect is documentary:
- the manifest gives the date but not the time or source;
- the hashed header still reads "pending".

**Errata to add.** These are additive, for example in `recurrent_core_results_v1_errata/`. **No rerun is required for any of them.**
- E-1: the claim text (§2).
- E-2: grid-edge disclosure and the qualifier on (ii) (§3, #2).
- E-3: count semantics, with a per-condition failure table (§1) and #13 variation counts marked descriptive.
- E-4: P1 note that CAND = F-TRAINED by construction, plus the meaning of P1 (§4).
- E-5: P2− zero-effect constructed by caching (#20).
- E-6: approval provenance (#22). Proposed wording: "Neural training for this study was approved by Aidan Ahern on 2026-10-20 at 8:55 PM ET ('Yes, approve it once Astra clears it'). Astra consult #12 had cleared the protocol with named edits, which are applied in FINAL sha 63c463c7. The hashed header's 'pending' wording predates that approval and is retained unedited."

## 6. Corrected labels (no flips)

| label | value |
| --- | --- |
| E1 | E1 REPLICATED (10/10) |
| Transfer (primary) | **TRANSFER SHOWN** (10/10 passes, 0 invalid) |
| F-INIT / F-TUNED32 A-FIT on TEST | 0/10 and 0/10 (independent; F-TUNED32 descriptive) |
| §4 (i) | **ADVANTAGE OVER TUNED FROZEN GRU-8 (843 TRAINABLE) OBSERVED** (10/10). Within the declared 3×3 grid, g* was at the upper bound in 10/10 seeds |
| §4 (ii) | TUNED FROZEN GRU-8 MEETS A-FIT AT THIS BUDGET: **not met** (0/10), within the declared grid; possibly grid-limited |
| SPECIFIC(r) | **NOT DEMONSTRATED**: 1/10 joint passes; directional 8/10, materiality 1/10 |
| SPECIFIC(z) | **NOT DEMONSTRATED**: 3/10 joint passes; directional 9/10, materiality 3/10 |
| SPECIFIC(n) | **NOT DEMONSTRATED**: 3/10 joint passes; directional 3/10, materiality 10/10 |
| Variation r / z / n | selective variation reduction not demonstrated. The label requires REPLICATED SPECIFIC; the per-seed descriptive counts are 1/10, 1/10 and 9/10 |
| P1 (trained core = CAND = F-TRAINED; init core = F-INIT) | DECODER PREDICTIVE AND CROSS-FOLD STABLE: not met, 0/10 for both cores. Descriptive, no label effect |
| P2 | PIPELINE VALID (E3-v2): known-Q 100/100 and fitted 100/100 at every s. P2− zero-effect True, partly by construction (#20) |

## 7. Claim ceiling

> In W2, recurrent training produced a GRU-8 core whose predictive advantage over its matched initialization survived replacement and retraining of the readout (10/10 fresh seeds). Hidden-to-hidden matrix reversion did not meet the prespecified joint criterion for any matrix.

Tuned-rival and variation results are appended separately, as in §2.

| question | status |
| --- | --- |
| **Q-LEARN** | SUPPORTED_BOUNDED: a learned, transferable recurrent contribution. The advantage over a tuned frozen GRU-8 is observed within a 3×3 grid whose optimum lies at its edge. |
| **Q-CAUSE** | NOT_ESTABLISHED by the preregistered matrix-reversion criterion. The descriptive per-condition pattern (§1) is not causal evidence. |
| **Q-NECESSITY** | Not tested. Tuned-rival failure within this grid does not establish necessity. |
| **Q-EXIST** | Not addressed by this study. |

**Not established:**
- localized content, or that W_hk "stores" prefix or chart information;
- a gate-pathway mechanism;
- that the frozen-rival family cannot reach A-FIT;
- other architectures or budgets;
- C4 (internal evaluation dissociable from first-order inference) or C5;
- consciousness or sentience;
- organism claims.

## 8. Questions for Astra

1. Do you confirm SPECIFIC(k) NOT DEMONSTRATED for all three matrices, where the binding condition is materiality for r and z and the directional condition for n? May RESULTS report the per-condition pattern descriptively, e.g. "directional in 8/10 and 9/10 but immaterial for r and z; material but not beyond matched-norm perturbation for n"? Or is that too suggestive?
2. Is "generic sensitivity of W_hn" acceptable descriptive wording for n: large material loss, matched by random perturbations of the same norm? Or should the result simply be "not demonstrated"?
3. Grid edge: should label (ii) carry the qualifier "within the declared grid; g* at the upper bound in 10/10"? Is the proposed 7×6 wider-grid robustness study, with its edge rule, worth running? Is it still a "robustness rival" and not a capacity change?
4. P1 failed for both cores on both criteria, with c not decodable and folds unstable. Does that make any future linear-decoder E3 on these networks uninformative? Is a nonlinear or causal-subspace method (e.g. intervention-based subspace search, still in the GRU-8 family and below C4) the right next step, or should localization be deprioritized?
5. P2− ψ caching (#20): is a zero-effect check that is partly by construction acceptable for a descriptive control, or should P2− be re-specified, e.g. with a reversible encoding that avoids cube-root amplification?
6. P2 per-draw LOCALIZED without coverage and rank gates (#18): acceptable?
7. Is the approval-provenance erratum wording (E-6) sufficient, given that the hashed header cannot be edited?
8. Given TRANSFER SHOWN plus a non-demonstrated reversion, what is the single most valuable next step toward causally verified acquired structure, below C4? Options include the wider-grid rival, a different reversion target (e.g. full `weight_hh` or the input-to-hidden matrices), or a graded reversion-path (interpolation) design.
