# Track B scope v3.2 — ADDENDUM (RD): Lead rulings on v3.1 (R26, R39, R2)

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY.** Nothing runs. Astra #42, verbatim: "No Stage-0 execution, training, simulation or checkpoint inspection is authorized by this review." (#42 L249) P3 CLOSED (#42 L251).

- **What this file is.** A new, additive addendum to merged v3.1. It edits nothing. **It is not merged v3.2.** Merged v3.2 waits for CNA's erratum and seam pass; this addendum enters that merge (§4).
- **Base:** merged v3.1, `/workspace/review/trackB_instrument_validation_scope_v3_1_merged_RD.md`, sha256 `9817c33b92ab776ab1703f3de4789ec8417bc2fb0a4d0cc9173295e18b02dcb0`, footer `84a5449b39c8926d71df4634ed3a76eeb02c461a8846dabbac1d5839cd594ff9` (reproduced). "v3.1 Lnn" means a line of that file.
- **Governing:** Astra #42 raw (`e438e329cff272bfd174a88dd917da6d7eb5560436fee06c39d0d46fd719c847`); Astra #41 raw (`3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43`) where #42 is silent; Lead rulings of 2026-10-23, about 3:05 PM ET.
- **Carried unchanged:** m = 14 (FINAL), α = 0.05 controlling false MET only, the per-claim level 0.996429, #43 as a design review, and every other v3.1 decision.
- **Written:** 2026-10-23, about 3:05–3:15 PM ET, by RD. Arithmetic uses proposed values only, never data.

---

## 1. R26: Lead adopts option (a). Budget for 67 seeds, not 20

**Ruling (Lead, about 3:05 PM ET).** Option (a) of v3.1 R26 is adopted. The declared between-seed heterogeneity range stays **σ_s/margin ∈ [0.25, 1.0]**, and the frozen §5.7 step 3 rule stays: n_seed is the smallest count meeting the §5.5 targets at the **upper end** of that range. The Lead's 2:54 PM ET figure of about 20 was only a planning value at the mid-range point σ_s/margin = 0.5.

**Stated plainly:** calibration may not change the rule afterwards. At the upper end, the rule can select **n_seed = 67** (noncentral-t power at level 0.996429, power 0.90 at the 1.5× positive; v3.1 R30). **The resource plan must therefore budget for 67 seeds, not 20.** The figure 20 stays only as a description of the mid-range point. It is never a budget figure, and never a certified or selected n_seed. The hard floor of 9 is unchanged (0.5⁸ = 0.003906 > α/m = 0.003571 ≥ 0.5⁹ = 0.001953; v3.1 R31).

### 1.1 Places in v3.1 that use 20 as a budget or planning figure, with corrected values

| v3.1 location | v3.1 text (as written) | Corrected budgeting value (R26 option (a)) |
|---|---|---|
| L5 header ("What this file is") | "n_seed planning value 20" | **Budget n_seed = 67.** 20 is the mid-range description only |
| L465 §14 D13 (merge tag and planning sentence) | "planning value 20 (Lead)"; "Planning value: 20 (Lead ruling, M4)" | **Budget n_seed = 67** (upper end, noncentral t, m = 14). The planning arithmetic 8 / 20 / 67 is unchanged as arithmetic. D13's original "the 16 / the 20 is a budgeting figure" is replaced by "67 is the budgeting figure; the calibrated n_seed is whatever §5.7 selects, ≤ 67 by construction of the declared range" |
| L1455 §17.1 R20 | "The planning point 0.5 gives 20 …, which is the planning value (Lead ruling, M4)" | **Budget 67**; 20 is the mid-range point only |
| L1461 §17.1 R26 | "Lead ruling (M4): planning value 20"; option (a) "budget 20 as planning only, accepting that calibration will select up to 67" | **Option (a) adopted with budget 67** (this addendum). Status: DECIDED (Lead), ASTRA TO CONFIRM (§3) |
| L1470 §17.2 R30 | "Adopted (Lead ruling): planning value 20." | **Budget 67.** The method and the values 8 / 20 / 67 stand |
| L1527 §18 item 3 | "n_seed planning value 20 (Lead); the upper-end rule can select up to 67" | "**budget n_seed = 67** (rule-selected maximum at the upper end); 20 is the mid-range description" |
| L1545 §19 R26 bullet | "n_seed planning 20 vs the upper-end rule (67): (a) or (b), OPEN FOR LEAD" | **Closed:** option (a), budget 67 (moves from §19 to §18 as ASTRA TO CONFIRM) |
| §5.9 / R30 candidate grid {9, 12, 16, 20, 24, 32, 48, 64, 67} | 20 is a grid point | **No change.** The grid already contains 67, and 20 stays a candidate. Sample-size calibration evaluates every grid point, so its per-replicate seed-unit load is Σgrid = 9 + 12 + 16 + 20 + 24 + 32 + 48 + 64 + 67 = **292 seed-units** per replicate per generator × dose. That is independent of the planning value |
| §17.2 R25 stage caps (workload) and §5.8 count formula | No literal 20. Caps are 1.5 × N_work × u, with u measured in the S0 preflight | For **seed-structured** generators (those whose outer replicate contains n_seed simulated seed units, §5.7 step 2), the per-replicate unit cost u scales linearly with n_seed. **Caps are computed at n_seed = 67**: confirmation load per generator × dose = 200 × 67 = **13,400 seed-units** (it would be 4,000 at 20; ratio 67/20 = **3.35×**). Sample-size calibration: 200 × 292 = **58,400 seed-units** per generator × dose (unchanged by this ruling). Replicate counts for non-seed-structured rows (≈ 15,000 + 15,000 + ≤ 3,750, R25) are unchanged |
| §17.1 R5 / Appendix L LP-5 / D31 observer costs | "2 × 48 = 96 pathway trainings per agent seed" (×n_seed for an arm) | Per arm with SELF: **96 × 67 = 6,432** pathway-matched observer trainings (1,920 at 20). With action-ignoring candidates as a separate factor (the LP-5 alternative): **144 × 67 = 9,648** (2,880 at 20). Each is at full agent exposure (CNA v3 §6.2) |
| D31 agent tuning and final training | 16 configurations × 3 seeds (tuning); n_seed final runs | Tuning: 48 runs per arm, **independent of n_seed** (unchanged). Final training runs per arm: **67** (20 at the planning value). Trajectory archiving (D31) scales the same way: 67 seeds' trajectories per arm |
| R6 dissociation-set episodes | 1,100 episodes per seed (800 donors + 100 selection + 200 recipients) | **1,100 × 67 = 73,700** episodes per arm (22,000 at 20) |
| D8 S-INT executed stops | 452 executed stops; ≥ 904 audit episodes (R34) | **Not n_seed-dependent as declared** (a pooled count from the decode TOST). No change |

These figures are for budgeting only. Stage L remains unauthorized. Totals across arms multiply by the number of trained arms in the §5b arm table, and are recounted from the complete design at implementation (#42 L13). Arm totals are not stated here, because which §5b rows are separately trained arms (rather than evaluation conditions on A-FULL) is fixed in the training protocol, not in this addendum.

---

## 2. R39: proposed §2.3 wording (PROPOSED; adopted unless CNA's seam pass objects)

**What is open (v3.1 L108, R39).** v3.1 §2.3 ends: "proposed for the Lead: in v2-era result text, use "interoceptive estimate module (candidate internal representation)", adding "learned" only when the Q-LEARN "acquired" conditions of §5.6 hold (#41 L170) [merge R11, light-pass I1]; use of the phrase PENDING Lead ruling." The open item is the naming and licensing wording for our own module in result text. R39 recorded it as a Lead-pending wording item, not a scientific choice.

**PROPOSED replacement for v3.1 §2.3 (full text):**

> **2.3 Decodability is not a self-model (applies to our own module). [v3.2 PROPOSED, R39]**
>
> Astra, verbatim: "A decoded policy-layer pattern should count as a candidate internal representation under the same operational standard applied to your allostatic module. A separate module name is neither necessary nor sufficient for a self-model. Decodability alone does not establish predictive modeling or causal use in either system." (#41 L19)
>
> - **Name.** In all design text and result text, the module is called the **"interoceptive estimate module (candidate internal representation of simulated E/I)"**. The A1–A7 label phrase "learned interoceptive self-model" is retained only as frozen historical label text. It is never used in result text, and no label changes.
> - **"Learned".** The word "learned" (or "acquired") may be attached to a result only when all three Q-LEARN "acquired" conditions of §5.6 hold. Otherwise, verbatim: "Otherwise say "increased through training."" (#41 L168)
> - **Four questions, four licences, never merged.**
>   - **Q-EXIST MET** licenses only: "an accessible estimate of simulated E/I beyond the declared joint baseline (candidate internal representation)."
>   - **Q-LEARN MET** licenses only: the measured accessibility was acquired through training, within the tested comparisons.
>   - **Q-CAUSE MET** licenses only: "The declared intervention on this direction/state changed behavior." (#42 L55)
>   - **Q-NECESSITY MET** licenses only: dependence under the declared intervention, "in this declared system, intervention and task family", with the A-EXT veto not triggered.
>
>   MET on one question never implies MET on another. None of the four, singly or together, licenses "self-model", privileged access or introspection. Variable-attributed wording needs E-ATTR or I-ATTR (CNA v3 §4.4).
> - **Simulation only; no stop term.** E and I are simulated toy-world variables (X1). The module's training signal and every arm's reward carry **"no additional stop-associated reward, penalty or terminal return"** (#42 L223). The ordinary truncated return with its bootstrap term is permitted. The module's estimate is never an input to stop handling, and the stop is never an input to the module.
> - **Ceiling (verbatim, #41 L304):** "Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment."

**Constraint checks (script):**
- The #41 quotes match #41 L19, L168 and L304 exactly.
- The #42 quotes match L55 and L223 exactly.
- The banned terms (consciousness, C4, C5, autopoietic, alive) are absent.
- Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are each given a separate licence.

---

## 3. §18 addition: FLAGGED FOR ASTRA CONFIRMATION

11. **R26, option (a):** the declared range σ_s/margin ∈ [0.25, 1.0] and the frozen top-of-range §5.7 rule are kept, with the **resource plan budgeted at n_seed = 67** (noncentral t, m = 14, level 0.996429, power 0.90 at 1.5× margin). 20 is the mid-range planning description only. Lead adopted; ASTRA TO CONFIRM.

**§19 change:** R26 leaves OPEN FOR LEAD (now DECIDED by the Lead). R39 leaves OPEN FOR LEAD and becomes PROPOSED, pending CNA's seam pass (§2).

---

## 4. R2: status record and merge placeholder

- **R2(a), decision rule: ADOPTED by the Lead.** The generic-dependence half of each MIXED-CODE row is a required mechanism-present positive check. The target is the one-sided 95% Clopper–Pearson lower bound of the MET rate ≥ 0.90, for C-NEC-DEP and for C-CAUSE at each required ρ. A failure is a failed positive-control check (#42 L216), never a limitation and never silently CONFOUND NOT REALIZED (v3.1 R2).
- **R2(b), plant construction, and R2(c), the comparator question: CNA-owned. CNA's erratum is PENDING.** Nothing is decided here.
- **Placeholder, merged v3.2: PENDING.** It is to be built after CNA's erratum (R2(b), (c)) and CNA's seam pass (including any objection to §2's proposed wording). Merged v3.2 will carry this addendum's §1–§3 and replace R2's OPEN status with CNA's erratum text.

**Still open after this addendum (unchanged from v3.1 unless stated):**
- **CNA:** R2(b), R2(c) (erratum pending), R3, R5, R7, R11, R12.
- **Lead:** none newly. R26 is decided; R39 is PROPOSED, pending the seam pass.
- **Astra (§18):** items as in v3.1, plus item 11.

**DRAFT, NOT FROZEN, DESIGN ONLY.** P3 CLOSED (#42 L251). Addendum only; not merged v3.2.

---
sha256 of all content above this line: b7985f08bb8d5f1447c9343152778c2f64ad95c2ace5d22584facaeef0f2961f
