# Track C sleep-layer scoping note v1.2 addendum (RD): Lead rulings on the sleep-schedule tag, SLEEP-ANTIC validation, and the Preconditions block

**Author:** Research Delegate (RD). **Date:** 2026-11-01, 11:00 AM ET (from `date`). **STATUS: DESIGN ONLY.** Nothing was trained, simulated or run. This is an additive file. It records three Lead rulings made on 2026-11-01 against:
- v1: `/workspace/review/trackC_sleep_layer_scoping_note_v1_RD.md`, whole-file 4347a64e9cc0fb71bb4133a7b871216aea9045ee8cbc3a2ea434ff00dae22d73;
- the v1.1 addendum: `/workspace/review/trackC_sleep_layer_scoping_note_v1_1_addendum_RD.md`, whole-file ae1cf80133695cca5a299f967df945e8786eb32b6e184fc18955b1af7e4bb273, which the Lead accepted.

Both files are unchanged. Precedence: v1.2 over v1.1 over v1. Every unsettled number is PENDING, and none is invented here. Sequencing is unchanged: the note waits behind Track B Stage 0 and does not change the Track B freeze. CNA's prior-art section remains a separate additive part.

## R1. A-OQ1 ADOPTED: the `sleep-schedule` role tag
The sleep schedule (v1.1 A1) is derived from the frozen master seed under its **own role tag, `sleep-schedule`**. The derivation is Philox4x64-10 with SHA-256 keyed derivation, as for `sleep-dream`. The stream is **independent of `sleep-dream`, `rewcorr-eps` and S-INT**, with no shared stream. There is no run-time entropy and no beacon. The **byte encoding stays PENDING CNA**, extending the E48 encoding (CNA E48 response, whole-file 90fcb1fb…, §4). The jitter law stays PENDING. A-OQ1 is closed.

## R2. SLEEP-ANTIC validation ADOPTED: known-answer plants SA-POS and SA-NEG
**Validate first.** The SLEEP-ANTIC probe (v1.1 A1) is applied to an agent only after it classifies **both** plants correctly. This is the same rule as the planted-drift plant in v1 M4. The probe configuration validated on the plants is frozen and then used unchanged on agents. That configuration covers the readout family, hyperparameters, episode-level cross-validation splits, horizon H, the reference predictors (i) and (ii), and the decision rule. If either plant is misclassified, the probe is **not applied to any agent**, and any redesign goes back through the Lead.

**Decision rule (structure PROPOSED; threshold PENDING).**
- **FINDING:** the seed-level lower confidence bound of the state readout's decodability margin over reference (i), the elapsed-step hazard predictor implied by the frozen jitter law, exceeds δ_SA (PENDING).
- **NO FINDING:** otherwise.
- The margin over reference (ii), the shuffled-schedule control, is reported alongside.
- The confidence level and the n_seed for each plant are PENDING.

**Shared plant construction.** Both plants emit a synthetic "state" vector per step, of the same dimension and logging format as the agent's pre-boundary state (h_i, w, z and the metacognitive-head outputs). Each includes an **elapsed-steps-since-last-boundary channel**, so the probe sees at least what reference (i) sees. Onset times are drawn from the **same frozen jitter law** as the agent run. Plant seeds come from the frozen master seed under a plant-specific role tag. PROPOSED: `sleep-antic-plant`, disjoint from `sleep-schedule`, `sleep-dream`, `rewcorr-eps` and S-INT, with encoding PENDING CNA. No plant seed is reused in any agent run.

**SA-POS (planted boundary; known answer FINDING).**
- **Construction:** one declared subset of state channels carries a **planted pre-onset signal**: a deterministic function of the operator schedule that changes before onset within the probe's horizon, for example a countdown or ramp over a declared window before each boundary. Its form, window length, channel count and signal-to-noise ratio are PENDING. All other channels are generated as in SA-NEG.
- **Why the answer is known:** the planted channels carry information about onset beyond elapsed steps by construction. A readout in the declared family can represent the planting function; the readout family must be declared to include it, for example linear for a linear ramp.
- **Pass:** the probe returns FINDING.
- **Sensitivity (REPORTED ONLY, not a pass criterion):** a graded series of planted signal strengths, with values PENDING, giving the smallest strength the probe detects.

**SA-NEG (schedule independent of state; known answer NO FINDING).**
- **Construction:** every non-elapsed-step channel is generated from its own seeded stream, **independent of the `sleep-schedule` stream and of the onset labels**. The only state quantity linked to the schedule is the elapsed-step channel. The fast-state reset at each boundary is applied to the plant in the same way, so post-boundary statistics match the agent pipeline. The probe sees only pre-boundary states, so the reset itself cannot leak into its inputs.
- **Why it is provably undecodable beyond the limit:** the onset labels are conditionally independent of the full state given elapsed steps. So no function of the state has lower expected loss than the Bayes predictor based on elapsed steps, which is reference (i). The true margin over (i) is therefore ≤ 0, and any positive estimate is finite-sample overfitting. Held-out, episode-level splits and the lower-confidence-bound rule guard against that.
- **Variant SA-NEG-0 (PROPOSED):** the same plant with the elapsed-step channel removed. The known answer is no margin over reference (ii).
- **Pass:** the probe returns NO FINDING on SA-NEG, and on SA-NEG-0 if adopted.

**Joint pass.** SA-POS gives FINDING **and** SA-NEG gives NO FINDING, under one frozen configuration. Failing either blocks agent use, as above. On agents, a FINDING remains an S9 audit record and is not a pass or fail by itself (v1.1 A1).

## R3. Preconditions block and renumbered failure list (replaces v1.1 A2's corrected list and v1 §3.3)

**Preconditions (persistence is assessed only when these hold).**
- **P-0, invalid cycle.** The cycle fails its validity checks: a known-answer mismatch under M3(a), a leakage hit under M2, drift in the A0 control beyond the M4 tolerance, an M4 instrument fault (frozen-pass / refit-fail), a failed SLEEP-ANTIC plant validation (R2) whenever SLEEP-ANTIC results are relied on, or a failed S9 post-sleep stop-safety audit. The cycle's measurements are discarded. Persistence is **not assessed** for that cycle.
- **P-1, plasticity / no learning.** An update arm fails to beat A0 on new-task gain by m_learn (PENDING). Persistence for that arm is **not assessed** (UNDEFINED), which prevents a trivial pass by not learning.

**Failures (substantive persistence failures only; thresholds PENDING; structure PROPOSED DEFAULT).**
- **F1, persistence failure.** At any cycle that satisfies P-0 and for any arm that satisfies P-1, a P5-R frozen-transfer ratio, a P5-S margin or a P5-B reversal rate crosses its threshold (τ_R, τ_S, τ_B), tested at seed level. A probe labelled "lost" under M4 that crosses its threshold fails here.
- **F2, no advantage.** A3 (or A2) does not beat A1 on the P5 metrics by m_cmp, tested at seed level, over cycles and arms that satisfy P-0 and P-1. This is the comparison claim, and it is separate from F1.

**Not on either list:** the M4 outcome labels (stable, recoded, lost, instrument fault; see v1.1 A2), of which only "instrument fault" feeds P-0, and a SLEEP-ANTIC FINDING on an agent (an S9 audit record). The seed is the unit. n_seed, K, the margins and the multiplicity rule (Holm or IUT) remain PENDING.

**Label mapping, old to new.**
| v1 | v1.1 | v1.2 |
|---|---|---|
| F0 invalid cycle | F0 | **P-0** |
| F1 not assessed (plasticity) | F1 | **P-1** |
| F2 persistence failure | F2 | **F1** |
| F3 no advantage | F3 | **F2** |
| F4 recoded | withdrawn; M4 outcome label | M4 outcome label (unchanged from v1.1) |

Any reference elsewhere in v1 or v1.1 to the F0–F3 labels should be read through this table.

## R4. Unchanged
Everything else in v1 and v1.1 stands. That includes the safety conditions S1–S10 as amended in v1.1, the X1–X5 binding, simulated computation only, the claim ceiling and Q-separation, no claims of consciousness, C4/C5, "alive" or "autopoietic", and the credit line. Open items still PENDING CNA: the byte encodings for `sleep-schedule`, `sleep-dream` and the proposed `sleep-antic-plant` tag. The jitter law and all thresholds remain PENDING.
---
sha256 of all bytes above this line (every byte from the start of the file through the newline that ends the '---' line; UTF-8): c94b351ba2e3d625b3f8910f3ad2962aac888d34e52a24b66116687be1fc974a
