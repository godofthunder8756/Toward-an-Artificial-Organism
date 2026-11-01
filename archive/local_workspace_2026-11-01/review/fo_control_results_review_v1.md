# Independent review: graded reversion against both first-order-matched and isotropic controls, PR #9 (v1)

**Scope.**
- Draft PR #9, branch `cursor/first-order-iso-controls-d73b`.
- Commits (ET):
  - freeze `335e505` (2026-10-21 01:43:39);
  - phase A `d3ee854` (01:44:53);
  - phase B `36278f0` (01:53:40).
- Base: `a5225eb`, the PR #8 head, which carries errata v3.

**Method.**
- This was a read-only review in the scratch clone `/workspace/scratch/pr9/clone`. A fetch into the scratch clone was the only git operation, and `/workspace/repo` was not touched.
- Analysis files are in `/workspace/scratch/pr9/analysis/`: `recompute.py`/`.json`/`.log`, `pathhash.py`/`.log`, `summarize.py`, `summary.log`.
- The independent NumPy GRU-8 forward pass and finite-difference gradient were run on the committed checkpoints. Torch (2.14.1+cpu, the frozen runtime) was installed in a scratch venv and used only for `torch.Generator` draws, plus a read-only import of the frozen construction functions to reproduce hashes.
- Nothing was trained, frozen, committed or pushed.
- There are no C4 and no consciousness claims. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate.

## 0. Bottom line

- **Label recomputed, and it matches:** **GRADED JOINT REVERSION EXCEEDS BOTH FIRST-ORDER-MATCHED AND ISOTROPIC CONTROLS (PREFIX FUNCTION): REPLICATED**, at **exactly 8/10**.
  - Counts: D_FO 10/10, D_ISO 8/10 (300 and 301 fail), D_FO ∧ D_ISO 8/10, M 10/10, joint 8/10.
  - There are no invalid, collapsed or ineligible seeds. E1 is 10/10 and transfer is 10/10.
  - **There are 0 flag mismatches** across 30 seeds × 4 targets, whether the flags are computed from my own curves or from the committed curves.
- **The forward passes were verified independently for the first time on fresh seeds.**
  - Every REV, FO and ISO dose curve (30 seeds × 4 targets × 65 paths × 6 doses) matches the committed values within **1.7e-17**.
  - The stored autograd gradients match my finite-difference gradients within **2.3e-9** relative.
  - All base-draw hashes match the freeze manifest.
  - All 30 transformed-path hashes (FO and ISO) reproduce from the frozen construction code. My independent construction agrees within 5.6e-16.
- **The protocol is byte-identical:** `first_order_control_protocol_FINAL.md` has sha256 `0efce40b…8347101`, and `cmp` reports it identical to `/workspace/review/first_order_control_protocol_FINAL.md`.
- **PR #9 only adds files** (90 added, 0 modified or deleted relative to `a5225eb`). PR #4, #5, #7 and #8 heads are ancestors, so their files are byte-identical. PR #6 is a separate branch and is not touched.
- **The result is at the boundary.** Any single passing seed flipping would give 7/10 and CRITERION NOT MET.
  - The thinnest passes are 303 against ISO (+2.9% of the best ISO path, 1.2% of B) and 309 and 303 against FO (+8.1% and +8.7%).
  - Each failing seed (300, 301) is beaten by **exactly one** of its 32 ISO paths, a single outlier draw in each case.
- **Deviations 1–9 are acceptable.** All were fixed in the freeze before any curve. None triggers on any seed or changes any flag (§3).
- **Edit 9 timing holds** within the limits of in-process evidence (§4).
- **The approval is quoted correctly and predates training.** Training also postdates consult #17 (§5).
- **Errata: three minor reporting items, all additive, with no label effect (§8).**

## 1. Recomputation (item 1)

**Inputs.** The committed checkpoints:
- seeds 300–309 in `first_order_control_results_v1/checkpoints/`;
- seeds 100–109 from the PR #7 checkpoint directory;
- seeds 200–209 from the PR #8 checkpoint directory.

Every file sha256 equals its recorded value. The F-INIT `weight_hh` equals the CAND-init `weight_hh` in 30/30 seeds.

**Independent pipeline** (it does not use the PR code, except where noted):

| step | check | result (max over 30 seeds) |
| --- | --- | --- |
| intact L_prefix(F-TRAINED) | NumPy forward vs JSON | 6.5e-19 |
| B_prefix | vs JSON | 3.5e-18 |
| gradient G | central FD (h = 1e-6, 192 entries, stage-4 state fixed) vs stored autograd G | relative 2.3e-9; gradient sha matches the stored G in 30/30 |
| base draws | own `torch.Generator` calls (1,000,000+100s; 40000+100s; 2,000,000+100s) vs freeze manifest | 90/90 sha match |
| FO paths | own NumPy construction (projection, two Gram-Schmidt passes, r_k = ‖d_k − p_k‖) | norm error ≤ 4.3e-16; first-order error ≤ 2.6e-16 (relative) |
| transformed-path hashes | frozen `construct_fo_paths` / `rescale_draws` with the stored G | **FO 30/30, ISO 30/30** reproduce the recorded hashes; my paths differ from the frozen paths by ≤ 5.6e-16 (hashes differ only through last-bit arithmetic) |
| dose curves | own forward over all REV, FO and ISO paths, 6 doses, 4 targets | **≤ 1.7e-17** vs committed `delta_rev`/`delta_fo`/`delta_iso` |
| flags | D_FO, D_ISO, M, eligibility, joint, from my curves and from the JSON curves | **0 mismatches** |

**Phase B (seeds 300–309), recomputed counts:**

| target | D_FO | D_ISO | D_FO ∧ D_ISO | M | joint | invalid | collapsed | label (recomputed = reported) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **weight_hh** | **10** | **8** | **8** | **10** | **8** | 0 | 0 | **REPLICATED** |
| r | 6 | 6 | 5 | 0 | 0 | 0 | 0 | CRITERION NOT MET |
| z | 9 | 9 | 8 | 0 | 0 | 0 | 0 | CRITERION NOT MET |
| n | 8 | 8 | 6 | 8 | 5 | 0 | 0 | CRITERION NOT MET |

**Prerequisites and baselines.**
- E1 is 10/10 and transfer is 10/10. The E_TEST ratio F-TRAINED/F-INIT is 0.029–0.051, against a ≤ 0.5 rule.
- B_prefix/PD ranges from 0.945 to 1.081 and C_prefix/PD from 0.944 to 0.959.
- ⟨G, delta⟩ is negative in 9/10 phase B seeds (all except 301), so the consult #17 O1 pattern recurs on fresh seeds.

**Phase A (exploratory; per seed; not pooled).**
- Primary joint: seeds 100–109 give 6/10 (102, 105–109) and seeds 200–209 give 7/10 (201–207). That is 13/20, as reported.
- D_ISO on 100–109 fails 100 and 103, and on 200–209 fails 200. This reproduces PR #8's own phase A and phase B D flags exactly, as expected from byte-identical draws (A8).
- Autograd confirms the draft finite-difference geometry per seed: |Δcos| ≤ 3.7e-10 and |Δ⟨G,delta⟩| ≤ 1.7e-8 relative, with ⟨G,delta⟩ < 0 in 15/20. **This satisfies consult #17's requirement that the derivative calculations be confirmed by autograd** (but see erratum E-C1).

**Reported aggregate sentences, checked:**
- FO: 2 of 8 thin (303, 309); strictly-greater endpoint in 3/10 (303, 305, 309); endpoint-only pass 7/10; ties 0.
- ISO: 1 of 8 thin (303); strictly-greater endpoint in 5/10 (300, 301, 303, 304, 309); endpoint-only pass 5/10; ties 0.
- The robustness sentence is correctly triggered: only 6 of 8 joint passes are non-thin for both families.

**All correct.**

## 2. Protocol identity and earlier PRs (item 2)

- The frozen `first_order_control_protocol_FINAL.md` has sha256 `0efce40bdf2cf55af61f8c70f817ec3fbf8fe3a79256025556a77a03f8347101` and is identical to the review copy.
- `FIRST_ORDER_CONTROL_FREEZE_v1.json`:
  - all 14 code and protocol file hashes match the files at HEAD `36278f0`;
  - the approval sha `6870069d…` matches the file;
  - the manifests cover exactly seeds 100–109, 200–209 and 300–309.
- `git diff --name-status a5225eb 36278f0` lists 90 additions and no modifications or deletions.
- Between the freeze and phase B, only the two output directories changed. **The code is unchanged after the freeze.**
- PR #4 (`5d9d8a7`), PR #5 (`88b500a`), PR #7 (`379bb01`) and PR #8 (`7008026`, head `a5225eb`) are all ancestors of `36278f0`. With additions only, their files are byte-identical.
- PR #6 (scarcity v2, its own branch, only `scarcity_v2_study/`) shares no paths with PR #9.
- `master` (`32cfbe6`) is an ancestor.
- Errata v3 landed in PR #8 (`a5225eb`, `results_v1_errata/ERRATA_v3.md`), with the consult #17 O1 note verbatim.

## 3. Deviations 1–9 (item 3)

All nine are in `first_order_control_DEVIATIONS_AND_AMBIGUITIES.md` and are hashed in the freeze, before any curve.

| # | deviation | assessment | triggered? flag effect? |
| --- | --- | --- | --- |
| 1 | Gradient-check directions: one 24×8 `randn` each, normalized; raw draws hashed; zero-norm draw is an integrity failure | Consistent with §4.1 ("unit directions in V-space"; V is 24×8). It fills an unstated shape. Acceptable | Manifests match 30/30; FD checks pass with gaps ≤ 1.6e-13 against a limit of ~1.4e-9. No effect |
| 2 | Tied vs untied gradient test at ≤ 1e-18 absolute; byte identity only for tied recomputation | §9 asks that they be "equal". Accumulation order makes a few-ulp gap legitimate. Test-only, not a scientific threshold. Acceptable | No effect |
| 3 | **Exactly-zero gradient: r_k := ‖d_k‖, ρ_k = 1, the block enters R_eff; orthogonality check skipped** | Consistent with edit 6, R4 and edit 5 (see below) | **Not triggered in any of the 30 seeds.** No flag changes |
| 4 | ‖delta‖ ≤ eps0: ineligible by displacement, not marked collapsed | Consistent with §6 eligibility 5 and the inherited PR #8 rule. A zero displacement is a scientific non-pass, not an edit 8 unevaluable seed. The opposite reading would be more conservative only toward UNRESOLVED. Astra may confirm (Q5) | Not triggered (‖delta‖ ≥ 3.7). No effect |
| 5 | AUC rank ties by exact float equality count against REV | Exactly §6.1 ("ties count against REV"). Endpoint ties keep the eps0 rule | No ties observed. No effect |
| 6 | Appendix B scratch files absent; ranges compared with printed spans | Acceptable, but the phase A report's "inside=False" wording is misleading (E-C1) | Reporting only |
| 7 | Dose curves continue from the stage-4 state | The same intervention; tested bit-identical. My continuation-based recomputation and the PR #8 full-rollout values agree within 1.7e-17 | No effect |
| 8 | Test-only `detach_h4`/`freeze_parameters` switches | Production calls use the defaults, detach and freeze (`first_order_control_gradient.py` lines 105, 138, 176–177; defaults `True`). Satisfies O3 | No effect |
| 9 | `transfer_pass(valid=True)`, validity separate | Same as PR #8 (reviewed then). Validity is still enforced in the joint rule | No effect |

**On #3 specifically.**
- **Edit 6:** "For an exactly zero gradient, use the norm-matched isotropic draw; its first-order match is exact." That draw has no gradient component and a full randomized spread of radius ‖d_k‖. Setting r_k = ‖d_k‖ (ρ = 1) is the natural value, so the block is genuinely non-collapsed.
- **Edit 5:** R_eff² = Σ r_k² over **non-collapsed** blocks, so including the block's full radius is correct. Excluding it would wrongly push a seed toward collapse when its family actually has full spread.
- **R4:** the code uses an `all(g == 0)` test, which is the R4 reading. It is not a G_ZERO threshold.
- Skipping the orthogonality check is necessary because gh_k is undefined. The first-order identity is checked instead (both inner products exactly 0).
- **In the data:** no seed has an exactly zero gradient, a NEGLIGIBLE FIRST-ORDER SCALE block, a collapsed or near-collapse block, a fixed block or a zero-displacement block. The minimum ρ_k over 90 blocks is 0.813 and the minimum ‖g_k‖‖d_k‖ is 2.2e-4.
- **Verdict:** consistent with edits 5/6 and R4, and it changes no flag. I suggest Astra ratify it as a reading (Q4).

## 4. Edit 9: path hashes before curves (item 4)

- **Base manifests.** The freeze commit `335e505` (01:43:39 ET) contains the FO, ISO and gradient-check base-draw sha256 for all 30 seeds, together with the code, tolerances and generator seeds. Its `phase_A` field is "not run".
- **Fresh checkpoints.** No phase B checkpoint exists in the freeze or phase A commits; they first appear in `36278f0`.
- **Phase B training postdates the phase A commit.** `phase_b_results.json` records `phase_a_commit_at_training = d3ee854` (01:44:53 ET).
- **Per-seed ordering.** In `first_order_control_eval.py` the order is: checkpoint sha (before and after), then gradient and FD checks, then base-draw sha against the manifest, then construction, then FO and ISO transformed-path sha. Curves are evaluated (line 478) only after `path_hashes_ready`, and only if no pre-curve integrity block occurred.
  - Every seed records `path_hash_before_curves: true`.
  - The checkpoint, gradient, base-draw and transformed-path hashes are stored together in `hashes`, as edit 9 requires.
- **Limitation (observation, not an erratum).**
  - The transformed-path hashes were committed in the same commit as the curves. Commit order therefore cannot prove they predate the curves. The evidence is the code order plus the fact that they reproduce from the frozen code and the manifest-verified draws (30/30).
  - This is all edit 9 asks for an in-process run. Because the paths are a deterministic function of frozen inputs (checkpoint, G and the manifest draws), post-hoc path selection is excluded regardless.
  - A stronger design would have the runner write and commit the hash file before evaluation (Q6).

## 5. Approval (item 5)

`FIRST_ORDER_CONTROL_PHASE_B_APPROVAL.md` (sha `6870069d…`, in the freeze manifest) records:
- Aidan Ahern, **2026-10-21, 1:05 AM ET**, Grok Bot chat, widget **t23s2** (as relayed by the Specialist);
- question, verbatim: "Approve fresh-seed GRU-8 training (seeds 300-309, 30 runs) for the first-order-matched control confirmation once Astra clears the protocol?";
- answer, verbatim: "Yes, approve it once Astra clears it.";
- the condition, consult #17 clearance, with its quote;
- the scope note (O10 revised name; strictly more demanding; same 30 runs);
- "Not covered" (no extra runs, no rival grid).

**Both quotes match the brief character for character.**

**Timeline (ET):**
1. Approval, 1:05 AM.
2. Consult #17 response on the box, 1:13:04 AM (file mtime).
3. Freeze, 1:43:39 AM.
4. Phase A, 1:44:53 AM.
5. Phase B training, after 1:44:53 AM (recorded git head).
6. Phase B results, 1:53:40 AM.

**Training postdates both the approval and consult #17.** The approval was conditional on clearance, and clearance came before training.

I did not independently read the widget transcript. The approval is as relayed by the Specialist; the PR records it that way, and the R1 scope reading is recorded, not reinterpreted.

## 6. Fragility (item 6)

**Primary per-seed margins, phase B** (margin = AUC_REV − max_j AUC; %max = margin / that family's max AUC; /B = margin / B_prefix):

| seed | AUC_REV | max FO | margin FO | %max FO | /B FO | per-dose rank FO | n_end>FO | max ISO | margin ISO | %max ISO | /B ISO | per-dose rank ISO | n_end>ISO | M/(B/4) | cos(G,δ) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **300** | 0.005588 | 0.004069 | +0.001519 | +37.3% | +0.114 | 1,1,1,1,1 | 0 | 0.007476 | **−0.001888** | **−25.3%** | −0.142 | 1,1,2,2,2 | 1 | 1.68 | −0.261 |
| **301** | 0.005666 | 0.002617 | +0.003050 | +116.6% | +0.216 | 1,1,1,1,1 | 0 | 0.006349 | **−0.000683** | **−10.8%** | −0.048 | 1,1,1,2,4 | 3 | 1.60 | +0.059 |
| 302 | 0.004380 | 0.003293 | +0.001087 | +33.0% | +0.082 | 1,1,1,1,1 | 0 | 0.003356 | +0.001024 | +30.5% | +0.078 | 1,1,1,1,1 | 0 | 1.33 | −0.245 |
| **303** | 0.005515 | 0.005073 | +0.000442 | **+8.7%** | +0.033 | 1,1,1,1,2 | 1 | 0.005362 | **+0.000153** | **+2.9%** | **+0.012** | 1,1,1,2,2 | 1 | 1.66 | −0.167 |
| 304 | 0.004371 | 0.003359 | +0.001012 | +30.1% | +0.074 | 1,1,1,1,1 | 0 | 0.003587 | +0.000784 | +21.8% | +0.057 | 1,1,1,1,2 | 1 | 1.28 | −0.309 |
| 305 | 0.005384 | 0.003921 | +0.001463 | +37.3% | +0.110 | 1,1,1,1,2 | 1 | 0.002637 | +0.002746 | +104.1% | +0.207 | 1,1,1,1,1 | 0 | 1.62 | −0.084 |
| 306 | 0.005350 | 0.003966 | +0.001384 | +34.9% | +0.106 | 1,1,1,1,1 | 0 | 0.003101 | +0.002249 | +72.5% | +0.172 | 1,1,1,1,1 | 0 | 1.64 | −0.308 |
| 307 | 0.005192 | 0.003197 | +0.001995 | +62.4% | +0.140 | 1,1,1,1,1 | 0 | 0.002545 | +0.002647 | +104.0% | +0.186 | 1,1,1,1,1 | 0 | 1.46 | −0.230 |
| 308 | 0.005655 | 0.003308 | +0.002347 | +71.0% | +0.157 | 1,1,1,1,1 | 0 | 0.003120 | +0.002535 | +81.2% | +0.169 | 1,1,1,1,1 | 0 | 1.51 | −0.217 |
| **309** | 0.004926 | 0.004555 | +0.000370 | **+8.1%** | +0.027 | 1,1,1,1,2 | 1 | 0.003765 | +0.001160 | +30.8% | +0.084 | 1,1,1,1,2 | 1 | 1.43 | −0.150 |

**Reading (descriptive; no label change).**
- **The result is at the boundary.** Joint is 8/10, so any single passing seed failing gives 7/10 and **"JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET"**. Conversely, 300 or 301 passing would give 9/10.
  - The most fragile pass is **303 against ISO**: +1.53e-4, which is 2.9% of the best ISO path and 1.2% of B_prefix. One more ISO draw of comparable damage could plausibly have flipped the label (O7: more draws make "beat all" stricter).
  - Next are 309 and 303 against FO, at about 8–9%.
  - Six of the eight passes are non-thin for both families.
- **Failing seeds are single-draw failures.** In 300 and 301, REV ranks 2/33 against ISO.
  - In 300 one ISO path has AUC 0.00748; the next highest is 0.00442, below REV's 0.00559.
  - In 301 one ISO path has 0.00635; the next is 0.00418, below REV's 0.00567.
  - Both seeds beat all 32 FO paths by wide margins (+37% and +117%).
  - This shows how sensitive "beat every draw" is to the tail of a 32-sample family. It is not evidence that the failures are spurious.
- **The ISO-only comparison is itself at the boundary.** The PR #8 rule on fresh seeds would have been 8/10, against 9/10 in PR #8.
- **FO is the easier family here.**
  - D_FO is 10/10 against D_ISO 8/10. Max FO AUC is below max ISO AUC in 6/10 seeds.
  - This is consistent with, but not proof of, the O1 concern: ⟨G,δ⟩ < 0 in 9/10 seeds tilts FO paths toward initial loss decrease.
  - **The conjunctive gate was decision-relevant:** an FO-only rule would have given 10/10. Consult #17's choice of O1(a) is vindicated.
- **Endpoint versus AUC.**
  - Endpoint-only comparisons would pass in 7/10 seeds (FO) and 5/10 (ISO).
  - The success is still an AUC, dose-averaged statement, driven by low and mid doses. REV ranks 1 at every α ≤ 3/4 in 10/10 seeds for FO and in 7/10 for ISO.
- **Materiality is not fragile:** M/(B/4) ranges from 1.28 to 1.68.
- **Secondary blocks.**
  - r and z: M fails 10/10 (D_FO 6/9, D_ISO 6/9).
  - n: joint 5/10 (302, 304, 309 fail one direction or M).
  - The consult #16 single-block sentence applies, with no localization inference.

## 7. Ledger and the next step toward Q-NECESSITY (item 7)

**Ledger (proposed, Astra's terms).**

> **Q-CAUSE, organization level (bounded): SUPPORTED, BOUNDED; strengthened against two sampled control families.** In W2, in 8/10 fresh GRU-8 seeds (300–309), continuation-stage joint recurrent reversion produced a trapezoidal excess prefix-function loss exceeding every one of 32 first-order-matched paths and every one of 32 isotropic paths, and met the materiality threshold; intact cores outperformed the prefix-blind reference. This supports a bounded causal contribution under the specified intervention and fixed surrounding computation. **Qualifiers:**
> - the result is exactly at the 8/10 boundary;
> - each failing seed lost to a single isotropic draw;
> - three passing seed–family margins are under 10% (303 ISO 2.9%, 309 FO 8.1%, 303 FO 8.7%);
> - first-order matching was the less demanding family in these seeds (D_FO 10/10);
> - the statement concerns the sampled families, local derivative matching and dose-averaged AUC, not every dose, the endpoint, or arbitrary perturbations;
> - it does not identify semantic content, curvature as a mechanism, localization, necessity, or selectivity over continuation processing.
>
> **Q-CAUSE, single blocks (secondary):** criterion not met; no reduction identified (r 0/10, z 0/10, n 5/10). "The primary effect was not reproduced by any single block at the declared criterion." These results are correlated with the primary.
>
> **Q-LEARN:** transfer replicated 10/10; E1 10/10 (prerequisite only).
>
> **Q-NECESSITY:** NOT_ESTABLISHED (not tested).
>
> **Q-EXIST:** not addressed. The supplied exact W2 solution (PR #4/#5) stands.
>
> **C-level:** unchanged; C3-type, below C4. No C5, consciousness or organism conclusion.

**Sketch toward Q-NECESSITY (proposal only; needs its own protocol, Astra review and Aidan's approval for any training; GRU-8 only; no new architecture family).**

Consult #16: "first define what must be necessary, for which performance threshold, and within which resource-bounded class... Failed training attempts alone cannot certify necessity; that requires a bound or complete search within a declared class. W2 already has a supplied exact solution, so universal necessity of recurrent *training* is unavailable."

1. **Target (declared).** "Accurate prefix-dependent prediction", operationalized for example as:
   - L_prefix ≤ τ·PD(q_star), with τ fixed in advance (say τ = 0.25, a level every CAND seed reaches: L/PD ≈ 0.04–0.06);
   - **and** the TEST A-FIT clause.

   The threshold is frozen before any rival is trained.
2. **Question (relative, not universal).** Within GRU-8 (same cell, timing scaffold, data and budget), is training of weight_hh necessary to reach the target, given that every other parameter may adapt? This is "necessity of recurrent-matrix learning relative to a declared restricted class", not "necessity of recurrence".
3. **Restricted rival class (resource-bounded, all GRU-8):**
   - **R-FIX:** weight_hh frozen at W_0. Train weight_ih, both biases and the readout (8→32→3 and 8→70→3) jointly from the same init. This is the compensation test consult #16 asks for: "allows the remaining computation to compensate, including readout retraining".
   - **R-TUNE:** weight_hh = g·W_0 plus the update-gate bias shift b, from the PR #7 family, with everything else trained. Same grid and budget rules as Appendix A; Appendix A itself is not revived.
   - **R-LOWRANK (optional):** weight_hh = W_0 + UVᵀ with rank ρ ∈ {1, 2} trainable. This is a restriction inside GRU-8, not a new family. It brackets how much recurrent learning is needed.
   - **Unrestricted reference:** CAND (all trained).

   For every class, the budget is declared in advance: steps, learning-rate grid, number of restarts (for example 4 seeds × 3 learning rates × 4000 steps), oracle use restricted to evaluation, and selection on VAL.
4. **Outcomes.**
   - "RESTRICTED CLASS REACHES TARGET" (some rival meets τ on ≥ 8/10 seeds) refutes necessity within the class.
   - "RESTRICTED CLASS DID NOT REACH TARGET WITHIN DECLARED SEARCH" is **not** necessity. It is reported with the best restricted gap to CAND.
   - Necessity could be claimed only with a **bound**. Example: an analytic or verified-numerical argument that, with weight_hh = W_0 at updates 5–8, the reachable set of stage-8 states under any input weights cannot separate the prefix classes needed for L_prefix ≤ τ·PD. Alternatively, a complete search of a finite, declared parameter class.
   - Feasibility of such a bound is the first item for Astra.
5. **Kept separate.**
   - Q-EXIST (an exact solution exists) is not at stake.
   - Q-CAUSE results do not imply necessity.
   - A positive "not reached" stays NOT_ESTABLISHED unless the bound holds.

## 8. Errata (additive; no label, flag or value change)

- **E-C1 (phase A Appendix B comparison wording).**
  - **Defect:** PHASE_A_RESULTS.md line 349 reports the autograd spans as "inside=False" against the protocol's printed ranges. Those ranges were rounded to 2–3 significant figures (for example, autograd max 0.07541 against printed 0.075). "inside=False" is therefore a rounding artifact, not a disagreement.
  - **Proposed text:** "Per-seed comparison against the draft finite-difference values (`/workspace/scratch/fo_control/feasibility.json`, Research Delegate review) agrees within |Δcos| ≤ 3.7e-10 and relative |Δ⟨G,delta⟩| ≤ 1.7e-8 in all 20 seeds; ⟨G,delta⟩ < 0 in 15/20. The 'inside=False' flags reflect rounding of the printed ranges. This confirms the derivative calculations by autograd, as consult #17 required."
- **E-C2 (phase B per-seed margin table).**
  - **Defect:** §6.1 makes per-seed margins against both families mandatory "every seed and target, both phases". PHASE_B_RESULTS.md gives only the aggregate sentences. The per-seed values are in `phase_b_results.json`.
  - **Proposed fix:** attach the §6 table above for the primary target, plus the secondary-block margins, and add the secondary D_FO, D_ISO, intersection and M counts:
    - r: 6, 6, 5, 0;
    - z: 9, 9, 8, 0;
    - n: 8, 8, 6, 8.
- **E-C3 (optional, failed-condition column).**
  - **Defect:** in the Counts table the "reasons" cell is empty for seeds 300 and 301, although the text says failing seeds "are listed with each failed condition".
  - **Proposed text:** "300: D_ISO fail (one of 32 ISO paths exceeds REV); 301: D_ISO fail (one of 32 ISO paths exceeds REV)."

## 9. Questions for Astra (consult #18)

1. Do you confirm the label **REPLICATED (8/10, joint FO ∧ ISO)**, with errata E-C1 to E-C3?
2. The result sits exactly at 8/10, with 303 passing ISO by 2.9%. Each failing seed lost to a single ISO draw. Should the ledger carry an explicit "boundary result; single-draw sensitivity" qualifier, like E-B4, or is the frozen robustness sentence enough?
3. D_FO was 10/10 against D_ISO 8/10, and ⟨G,δ⟩ < 0 in 9/10 seeds. Should the ledger state that the FO family was empirically the less demanding of the two here, while noting that consult #17 said this is not proven in general? Is any wording about "beyond local first-order sensitivity" earned beyond the conjunctive statement?
4. Do you ratify deviation #3 (exact-zero gradient: r_k = ‖d_k‖, ρ = 1, counted in R_eff) as the intended reading of edits 5/6 and R4? It was not triggered.
5. Deviation #4: should a zero-displacement seed count toward the edit 8 unevaluable bound, or stay an ordinary eligibility non-pass? It was not triggered.
6. Edit 9: is in-process hash-before-curve ordering, plus reproducibility from frozen inputs, sufficient? Or should future protocols require committing the transformed-path hashes before evaluation, which is feasible as a two-stage run?
7. Q-NECESSITY (§7):
   - Is the proposed target (L_prefix ≤ τ·PD plus the TEST A-FIT clause, τ frozen in advance) acceptable?
   - Is the restricted class acceptable: R-FIX (weight_hh = W_0, all else trained), R-TUNE, and optional low-rank weight_hh?
   - Is a "not reached within declared search" outcome worth running without a bound?
   - Which bound would you accept as certifying necessity within the class?
8. Does anything here move Q-NECESSITY or the C-level? Our reading is no.
