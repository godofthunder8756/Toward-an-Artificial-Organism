# Independent review: graded joint recurrent reversion results, PR #8 (v1)

**Scope.**
- Draft PR #8, branch `cursor/graded-joint-reversion-ddeb`.
- Commits:
  - freeze `018f2a7` (2026-10-21 02:55:41 UTC = **10:55 PM ET**, Oct 20);
  - phase A `9808759` (10:56 PM ET);
  - phase B `7008026` (11:04 PM ET).
- Base: `379bb01`, the PR #7 errata E-1 to E-6, which is also the current head of PR #7.

**Method.** This was a read-only review in the scratch clone `/workspace/scratch/pr8/clone`.
- The analysis uses only committed JSON. The scripts and logs are in `/workspace/scratch/pr8/analysis/` (`recompute.py`, `recompute.log`, `recompute.json`, `shape.py`, `shape.log`).
- Nothing was retrained, re-evaluated, frozen, committed or pushed.
- There are no C4 and no consciousness claims. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate.

## 0. Bottom line

- **The protocol is byte-identical to FINAL.** `GRADED_REVERSION_PROTOCOL_FINAL.md` has sha256 `1a5e62bd…89bfa3`, and `cmp` reports it identical to `/workspace/review/graded_reversion_protocol_FINAL.md`.
- **The raw file is verified.** `phase_b_results.json` has sha256 `3a69ae1b7e1d45b0af1af4d0e12f8a9b5bf70e31a3571cf0fdffc854c4bdabe1`. Each `seeds/s20x.json` is content-identical to its record in that file.
- **The independent recomputation matches the PR exactly, with zero mismatches.**
  - **Primary label: GRADED JOINT RECURRENT REVERSION EXCEEDS MATCHED RANDOM PERTURBATION (PREFIX FUNCTION): REPLICATED.** 9/10 seeds passed (directional 9/10, materiality 10/10, eligible 10/10, invalid 0). E1 is 10/10 and transfer is 10/10. Seed 200 fails D.
  - **Secondary (block-wise) labels: CRITERION NOT MET for all three blocks.** r passed 0/10 (directional 7, materiality 0); z passed 0/10 (directional 5, materiality 0); n passed 5/10 (directional 7, materiality 8).
- **Claim wording is the frozen text, verbatim.** "increased oracle-referenced prefix-function loss" is Astra's own consult #15 success paragraph, frozen in FINAL §8. Consult #15 removed "increasingly disrupts", not "increased". This is **not drift**.
- **The margins are fragile (descriptive; the label does not change).**
  - Four passing seeds clear the best random path by less than 10% of that path's AUC: 202 (+1.5%), 208 (+6.4%), 209 (+6.3%) and 206 (+8.1%).
  - At the α = 1 endpoint, at least one random path is more damaging than reversion in 7/10 seeds.
- **Two report-labeling defects need additive errata (§4).** The freeze SHA is recorded as `9808759`, and the secondary bullets lack their block letters. Neither affects any computed value.
- **Integrity holds.**
  - PR #8 only adds files (79 added, 0 modified, 0 deleted relative to `379bb01`), so all PR #4–#7 artifacts are byte-identical.
  - The code is unchanged after the freeze, and all 13 manifest code hashes match at HEAD.
  - Phase A and phase B are in separate directories, and phase B aggregates read only seeds 200–209.
- **The approval was in place before training.**
  - Aidan's answer to the Specialist's widget question "Approve fresh-seed GRU-8 training for the graded reversion confirmation once Astra clears the protocol?" was "Yes, approve it once Astra clears it", at **10:38 PM ET** on Oct 20, in Grok Bot chat (Specialist transcript).
  - Astra consult #15 had already cleared the protocol (~10:29 PM ET).
  - The approval note is committed **in the freeze commit (10:55 PM ET)**, with date, time (ET), source and exact words. Phase B results were committed at 11:04 PM ET.
  - **The approval predates phase B training.** Appendix A is correctly recorded as not approved and not run.

## 1. Recomputation of the phase B verdict (FINAL rules)

**Inputs.** For each seed, the recomputation recalculates the following from the committed per-dose values:
- L_prefix(F-TRAINED), L_prefix(F-INIT) and PD(q_star). PD was recomputed independently from `world.q`: 0.0138386222.
- B_prefix and C_prefix.
- The REV curve and all 32 random curves Delta(α) at α = 0, 1/8, 1/4, 1/2, 3/4, 1.
- The trapezoidal AUCs with weights (1/16, 1/8, 3/16, 1/4, 1/4, 1/8).

**Rules applied.**
- D: AUC_REV − max_j AUC_rand,j > eps0.
- M: AUC_REV > eps0 and AUC_REV ≥ B_prefix/4.
- Eligibility: transfer, B_prefix > eps0, C_prefix > eps0, and ‖delta‖_F > eps0 (‖delta_k‖_F for the blocks). There are no zero blocks: block norms are 1.74–2.96 and full norms 3.74–4.66.
- Validity: sham, restore and α = 0 gaps, outputs, the checkpoint sha, the endpoint, and the draw sha against the manifest.
- Precedence: E1 first, then more than 2 invalid seeds, then the count, with the denominator fixed at 10.

**Results.**
- No mismatch in any per-seed D, M, eligibility or joint flag, AUC, Delta curve, B, C, or saturation value. Tolerance is 1e-15, or 1e-12 for ratios.
- L_prefix equals the sum of its X, Y and XOR components, so no /3 was applied, as FINAL §5 requires.

| target | E1 | invalid | eligible | D | M | **joint passes** | label (recomputed = reported) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **weight_hh (primary)** | 10/10 | 0 | 10 | 9 | 10 | **9/10** | **REPLICATED** |
| r (secondary) | — | 0 | 10 | 7 | 0 | 0/10 | CRITERION NOT MET |
| z (secondary) | — | 0 | 10 | 5 | 0 | 0/10 | CRITERION NOT MET |
| n (secondary) | — | 0 | 10 | 7 | 8 | 5/10 (202, 203, 204, 205, 209) | CRITERION NOT MET |

**Baselines.**
- B_prefix/PD ranges from 0.898 to 1.042 and C_prefix/PD from 0.901 to 0.960. Every seed's intact trained core is far better than the prefix-blind reference.
- F-INIT is at about the prefix-blind level: L_prefix(F-INIT) ≈ PD(q_star).

**Phase A (exploratory; context only; not pooled).** D held in 8/10 seeds (it failed on 100 and 103) and M in 10/10. This is consistent with the PR, and it is not evidence for the claim.

## 2. Claim wording

- The JSON `claim` field equals FINAL §8's success paragraph plus its limitation sentence, character for character. Both strings appear verbatim in `/workspace/astra_consult15_response.txt`. PHASE_B_RESULTS.md contains the same text.
- "increased oracle-referenced prefix-function loss over the predeclared dose grid" is **the frozen wording**, taken from Astra's own consult #15 success paragraph. The edit replaced "increasingly disrupts" (the draft's monotonic-sounding question wording) and removed "selectively". Neither "increasingly" nor "selectively" appears in the results.
- "increased" is supported at seed level: AUC_REV > 0 in 10/10 seeds. The paragraph's "at least eight of ten" is met at 9/10. "The intact trained cores also outperformed the prefix-blind reference" is met with C_prefix > 0 in 10/10.
- **Finding: no drift. No erratum is needed for the claim.**

## 3. Margin fragility (descriptive only; no label change)

The columns are:
- **margin** = AUC_REV − max_j AUC_rand,j;
- **m/B** = margin / B_prefix, and **m/PD** = margin / PD(q_star);
- **m/maxR** = margin as a fraction of the best random AUC;
- **rank** = rank of REV among the 33 paths by AUC (1 = most damaging);
- **M/(B/4)** = AUC_REV divided by the materiality threshold;
- **per-dose rank** = REV's rank among the 33 paths at α = 1/8, 1/4, 1/2, 3/4, 1.

| seed | AUC_REV | max random | margin | m/B | m/PD | m/maxR | rank | M/(B/4) | per-dose rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 200 | 0.005149 | 0.007231 | −0.002083 | −0.156 | −0.150 | −28.8% | **4/33** | 1.54 | 1, 1, 2, 4, 8 |
| 201 | 0.003925 | 0.003282 | +0.000644 | +0.046 | +0.047 | +19.6% | 1/33 | **1.13** | 1, 1, 1, 1, 2 |
| **202** | 0.004729 | 0.004659 | **+0.000070** | **+0.005** | **+0.005** | **+1.5%** | 1/33 | 1.48 | 1, 1, 1, 1, 2 |
| 203 | 0.005614 | 0.003653 | +0.001961 | +0.154 | +0.142 | +53.7% | 1/33 | 1.76 | 1, 1, 1, 1, 1 |
| 204 | 0.005994 | 0.005100 | +0.000894 | +0.066 | +0.065 | +17.5% | 1/33 | 1.76 | 1, 1, 1, 1, 3 |
| 205 | 0.006243 | 0.003811 | +0.002432 | +0.184 | +0.176 | +63.8% | 1/33 | 1.89 | 1, 1, 1, 1, 1 |
| 206 | 0.004681 | 0.004331 | +0.000351 | +0.024 | +0.025 | +8.1% | 1/33 | 1.30 | 1, 1, 1, 1, 2 |
| **207** | 0.005177 | 0.003866 | +0.001311 | +0.100 | +0.095 | +33.9% | 1/33 | 1.58 | 1, 1, 1, 1, 1 |
| **208** | 0.005168 | 0.004856 | **+0.000312** | +0.025 | +0.023 | **+6.4%** | 1/33 | 1.66 | 1, 1, 1, 1, **4** |
| **209** | 0.005876 | 0.005527 | **+0.000350** | +0.025 | +0.025 | **+6.3%** | 1/33 | 1.67 | 1, 1, 1, 1, **3** |

**Reading (descriptive):**
- **202** is the thinnest pass: 0.004729 against 0.004659, a margin of 0.5% of B_prefix and 1.5% of the best random AUC. One more random draw could plausibly have exceeded it. Consult #14/O11 notes that more draws make "beat every draw" stricter.
- **208 and 209** are thin as well: about 6% over the best random path, about 2.5% of B_prefix. At α = 1, 3 and 2 random paths respectively are more damaging than reversion (per-dose ranks 4 and 3).
- **207 is robust**: +34% over the best random path, rank 1 at every dose, and no random path more damaging at the endpoint.
- **Sensitivity.** Four passing seeds (202, 206, 208, 209) are within 10% of the best random path. If any **two** had failed, the count would be 7/10 and the label would read CRITERION NOT MET. This is a hypothetical robustness statement, not a relabel.
- **Materiality is not fragile**: M/(B/4) ranges from 1.13 (seed 201) to 1.89.

**Curve shape (descriptive).** This explains how the AUC margins arise.
- REV's saturation index Delta(½)/Delta(1) is 0.43–0.58, close to linear in α. The median random path's is 0.25–0.29, close to quadratic, as expected for a near-orthogonal displacement around a trained point.
- So REV dominates at low and mid doses. At α = 1, a random path exceeds REV's loss in 7/10 seeds (counts per seed 7, 1, 1, 0, 2, 0, 1, 0, 3, 2).
- The AUC criterion, as frozen, weights the whole path. The pass is therefore driven by the early-dose regime, which fits a **first-order (gradient-aligned) effect of the learned displacement against mostly second-order random effects**. This is an interpretive hypothesis, not established.
- The pattern is consistent with the claim as frozen. It is relevant to what "beyond matched random perturbation" means (§7, Astra questions).
- All REV curves are non-decreasing (5/5 steps). Monotonicity is still **not established** in the frozen sense (FINAL §6: descriptive only, not tested).

## 4. Draft additive errata (report-labeling only; frozen outputs preserved)

**E-B1 (freeze commit field).**
> "PHASE_B_RESULTS.md (line 7) and `phase_b_results.json` field `freeze_commit` record `9808759ffd4dfd417014b22c6b63512c22a61c9f`. That is the phase A exploratory results commit. The freeze commit is `018f2a773e4d5fb897230e9ca1d6904c32c9fd78` (2026-10-20 10:55 PM ET), as PHASE_A_RESULTS.md correctly records. Cause: `graded_reversion_study.py` writes `git_head()` at phase B run time. No code or protocol file changed between `018f2a7` and `7008026` (all 13 freeze-manifest code hashes match at `7008026`), so the phase B results were produced by the frozen implementation. No computed value, flag, label or claim is affected. The frozen output files are retained unedited."

**E-B2 (secondary bullet labels).**
> "In PHASE_B_RESULTS.md, 'Secondary (block-wise)', the three bullets omit their block letters. They were rendered in loop order r, z, n (`graded_reversion_report.py` line 269), which the per-seed secondary table and an independent recomputation confirm. Corrected:
> - Secondary (block-wise), r: GRADED JOINT REVERSION CRITERION NOT MET. 0/10 seeds passed (directional 7/10, materiality 0/10; eligibility failures 0/10).
> - Secondary (block-wise), z: GRADED JOINT REVERSION CRITERION NOT MET. 0/10 seeds passed (directional 5/10, materiality 0/10; eligibility failures 0/10).
> - Secondary (block-wise), n: GRADED JOINT REVERSION CRITERION NOT MET. 5/10 seeds passed (directional 7/10, materiality 8/10; eligibility failures 0/10).
>
> Secondary results are correlated with the primary and with each other, and do not substitute for it."

**Optional E-B3 (descriptive disclosure, no label effect).** Add the §3 margin and per-dose rank table, and the sentence:
> "Four of nine passing seeds exceed the best random path by less than 10% of its AUC. At α = 1, at least one random path exceeds REV's loss in 7/10 seeds. The AUC criterion is met mainly through lower and intermediate doses."

## 5. Integrity and pooling

**Integrity.**
- `git diff --name-status 379bb01 7008026` lists only additions (79 files: freeze, phase A, phase B). No existing file is modified or deleted, so **all PR #4–#7 artifacts are byte-identical**, including the PR #7 results and errata.
- `5157f5d → 379bb01` is likewise additions only (the errata).
- PR #7's current head is `379bb01`, the base of PR #8.
- `git diff 018f2a7 7008026` touches only the two output directories, so no code changed after the freeze.
- The draw sha256 for every seed matches the freeze manifest (`draw_sha_matches_manifest` is true in 10/10). Checkpoint sha256 values are recorded and checked. Sham, restore and α = 0 gaps are exactly 0, and endpoint `w1_max_abs` is 0.

**Pooling.**
- Phase A outputs are in `graded_reversion_phaseA_exploratory/` (seeds 100–109; `development_only: true`, `confirmatory: false`, EXPLORATORY header).
- Phase B outputs are in `graded_reversion_results_v1/` (seeds 200–209 only).
- `run_phase_b` builds its aggregates from `PHASE_B_SEEDS` records only.
- The only mentions of 100–109 in PHASE_B_RESULTS.md are in the separately headed "Development history" section.
- **No pooling.**

**Not done.** I did not re-evaluate the networks from their checkpoints; this was JSON only, per the rules, and torch is not installed on the box. The recomputation verifies the verdict arithmetic and rules given the recorded per-dose losses. It does not independently verify the forward passes.

## 6. Approval

| item | finding |
| --- | --- |
| Required by | FINAL §2, §9 step 5.4: Aidan's explicit phase B approval with date, time (ET) and source |
| Record | `GRADED_REVERSION_PHASE_B_APPROVAL.md` (sha `c9db56ac…`, listed in the freeze manifest); also the `approval` field of `phase_b_results.json` |
| Content | Aidan Ahern; 2026-10-20; **10:38 PM ET**; source "Grok Bot chat"; words "Yes, approve it once Astra clears it"; Appendix A explicitly not approved |
| Transcript check | The Specialist's transcript shows the widget answer at 10:38 PM ET to question t20s2, "Approve fresh-seed GRU-8 training for the graded reversion confirmation once Astra clears the protocol?" This is specific to this study. It is not a reuse of the PR #7 approval at 8:55 PM, which used the same words. |
| Condition | "once Astra clears it": consult #15 (FREEZE WITH NAMED EDITS) was received about 10:29 PM ET, before the approval |
| Timing | approval 10:38 PM, then freeze commit (with the approval note) 10:55 PM, then phase A 10:56 PM, then phase B results 11:04 PM ET. **Training followed the approval.** |
| Verdict | **Approval recorded, specific to this study, and predates phase B training.** The only nit: the note does not quote the widget's question text. Adding it would strengthen provenance (optional). |

## 7. Ledger update (Astra's terms)

> **Q-CAUSE, organization level (bounded): SUPPORTED, BOUNDED.** In W2, interpolating the complete hidden-to-hidden matrix toward initialization during updates 5–8, with trained input weights, biases and a fresh readout held fixed, increased oracle-referenced prefix-function loss over the predeclared dose grid. In 9/10 fresh seeds (seeds 200–209), the trapezoidal excess exceeded every one of 32 block-norm-matched random paths and reached at least a quarter of the paired prefix-loss advantage over F-INIT. This supports a bounded causal contribution of the trained hidden-to-hidden parameters to accurate prefix-dependent prediction under the specified intervention and fixed surrounding computation. Directional margins are small in several seeds (§3).
>
> **Q-CAUSE, single blocks (secondary):** criterion not met; no reduction identified (r 0/10, z 0/10, n 5/10). These are correlated with the primary and are not independent replications.
>
> **Q-LEARN:** transfer replicated in 10/10 fresh seeds (prerequisite only).
>
> **Not established:** Q-NECESSITY (not tested); monotonicity; selectivity over continuation processing (L_cont is descriptive); an XOR-specific effect; localized content; a uniquely identified mechanism; superiority over non-isotropic or learned-like perturbations.
>
> **Q-EXIST:** not addressed. No C4, C5, consciousness or organism conclusion.

**Implications for the next study** (proposals only; any training needs approval; localization stays deprioritized):
1. **The bounded Q-CAUSE result is the earned step.** It should not be strengthened by reanalysis. The thin margins and the endpoint pattern argue for a **stricter control family**, not reinterpretation.
2. **The most informative next control** is a perturbation family that shares REV's first-order character but not its specific learned content. Options:
   - interpolation toward *another seed's* trained weight_hh (foreign-trained), or toward a trained solution from a different initialization;
   - random directions matched to REV's first-order effect, i.e. matched projection onto the gradient of L_prefix at W_T.

   Either would test whether "beyond isotropic random" reflects the specific learned transformation or any loss-aligned displacement.
3. **Single blocks do not carry the effect** (r and z are below the materiality threshold everywhere). The contribution is distributed across matrices or carried by n. This is consistent with Astra's "distributed contributions" rationale. Any block-level follow-up should be framed as distributed-contribution analysis, not localization.
4. **Q-NECESSITY stays a separate question.** Nothing here addresses whether recurrent training is required.

## 8. Questions for Astra

1. Do you confirm REPLICATED (9/10) as the literal label, together with errata E-B1 (freeze SHA) and E-B2 (block letters), and the optional disclosure E-B3?
2. Four passing seeds clear the best random path by less than 10%, and seed 202 by 1.5%. Should the ledger carry an explicit "thin directional margins" qualifier, or is the frozen claim enough with the margin table attached?
3. At α = 1, some random path exceeds REV in 7/10 seeds, and REV's curves are near-linear while random curves are near-quadratic. Is "beyond matched random perturbation" adequately characterized as an AUC-level, dose-path statement? Should results text note that the endpoint comparison alone would not have supported it?
4. Is a first-order-matched control the right next test of specificity, i.e. gradient-projection-matched random directions, or interpolation toward a foreign-seed trained weight_hh? Would either be a new protocol with fresh seeds?
5. n passed 5/10 while r and z passed 0/10. May this be described as "the primary effect was not reproduced by any single block at the declared criterion", with no localization language?
6. Should the approval note be amended additively to quote the widget's question text (t20s2) for provenance?
7. Does anything here move Q-NECESSITY or C-level assessments? Our reading is no.
