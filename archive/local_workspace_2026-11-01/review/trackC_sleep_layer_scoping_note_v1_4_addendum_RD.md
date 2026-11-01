# Track C sleep-layer scoping note v1.4 addendum (RD): the "lost" case by construction, and SA-NEG scored on every cycle

**Author:** Research Delegate (RD). **Date:** 2026-11-01, 11:08 AM ET (from `date`). **STATUS: DESIGN ONLY.** Nothing was trained, simulated or run. This is an additive file, and every earlier file is unchanged. Precedence: v1.4 over v1.3 over v1.2 over v1.1 over v1. Every unsettled number is PENDING, and none is invented here. Sequencing is unchanged: this waits behind Track B Stage 0 and does not change the Track B freeze.

**Amends:**
- v1.3: `/workspace/review/trackC_sleep_layer_scoping_note_v1_3_addendum_RD.md`, whole-file 2990c36b16b97ba57615d6aa2d7c1c5d4f84e7837a156acd48581d8afb4af7ef (footer 3764f85a…), specifically §F F6 and F10/F11 and G5.
- It also cites CNA's governing part: `/workspace/review/trackC_sleep_layer_prior_art_safety_CNA_v1.md`, whole-file 0c3568fda0e0a6344dcd05a60e54aa318d6185fe8a5192e2c1535087240bc11e, §5.

## D1. Planted-drift plant: the "lost" case by construction (amends v1.3 F6 (P))
**Status:** CNA accepted the three-transform change in v1.3 F6, namely (R) rotation, (G) general invertible map and (P) projection. This item makes (P) hold by construction.

**Construction (replacement text for (P)).**
- The plant state x is generated in a declared basis as x = (x_T, x_R).
- The readout target y depends on x only through the block x_T, which spans the **removed subspace**.
- The remaining block x_R is drawn from its own seeded stream, **jointly independent of y**, and also of x_T where x_T carries y.
- Independence must be joint across the whole block, not coordinate by coordinate. Coordinate-wise independence alone would let a nonlinear readout recover y from combinations of coordinates.
- (P) is the exact projection that deletes x_T and keeps x_R, with no mixing or noise added across the blocks.
- The dimensions of x_T and x_R, the target function, the noise laws and the seed derivation are PENDING. The seed role tag is PENDING CNA, under the domain-separation rules of CNA §4.

**Why "lost" holds for any readout class.** After (P), the remaining state x_R is independent of y. So for **any** refit readout class, linear or nonlinear, no readout has lower expected loss than the best constant predictor, which uses the marginal of y. The frozen readout fails as well. The known answer, frozen-fail / refit-fail, therefore does not depend on how expressive the readout is. Finite-sample excess over the constant predictor is overfitting, and it is controlled by held-out, episode-level splits.
- **Pass criterion (structure PROPOSED, tolerance PENDING):** the refit readout's seed-level upper confidence bound does not exceed the constant-predictor baseline by more than δ_lost (PENDING).
- (R) and (G) act on the same plant before projection and are non-trivial on x_T, with known answer "recoded". Their parameters are unchanged from v1.3 and remain PENDING.

**Linear-case statement (credited to CNA).** When a plant or representation is **not** built this way, CNA's condition applies: to get "lost" for **linear** readouts, (P) must also remove every direction that is linearly correlated with the target in the probe set. That condition guarantees failure only for linear refit readouts. A nonlinear readout may still recover y from the surviving directions. So any "lost" label from a non-constructed plant, or from an agent, must state which readout class it covers. Only the by-construction plant above certifies "lost" for every class.

## D2. SA-NEG scored on every cycle, including P-0 failures (amends v1.3 G5, F10 and F11; CNA's catch, accepted)
**The problem (CNA).** v1.3 F10 made cycles with a wake segment shorter than the minimum valid wake length m invalid under P-0. If SLEEP-ANTIC scoring dropped those cycles, every surviving cycle would have **zero onset hazard in its first m steps**. The gap floor that G5 removed would come back through selection. Time since the last reset would then predict onset, and reference (i) (constant base rate h) would no longer be the right baseline. SA-NEG's known answer, "undecodable", would fail for a reason that has nothing to do with the probe.

**Rule (replacement text).**
- **Scoring on every cycle.** SA-NEG is scored on **every cycle, P-0 failures included**. The same applies to SA-POS and SA-NEG-0, and to SLEEP-ANTIC on every agent arm (A0–A4, and A5 if run), so plants and agents are scored under one frozen configuration with the same cycle set.
- **The schedule ignores P-0.** The sleep schedule is generated **without regard to P-0**. Gaps are drawn from the `sleep-schedule` stream under the geometric law of G5 (hazard h, PENDING), with no rejection, resampling, reordering or truncation based on P-0, on m, or on any other validity check. The freeze record states this.
- **P-0 still applies to persistence.** P-0 still **invalidates short cycles for the persistence metrics** (P5-R, P5-B, P5-S, F1, F2) and for forgetting (M5). This is the only use of P-0. It is applied after the fact and never feeds back into the schedule or into SLEEP-ANTIC's cycle set.
- **Alternative (noted, not adopted).** Score only steps at least m after each reset, in every cycle, with no cycle-level exclusion. By memorylessness, the hazard on those steps is still the constant h, so reference (i) stays the base rate. This discards the early steps of every cycle, and it is recorded in case the Lead or CNA prefer it.

**Consequence for v1.3.** v1.3 F10's P-0 addition (minimum valid wake length m, PENDING) stands for persistence only. v1.3 F11's statements under G5 (reference (i) = h; SA-NEG margin over (ii) ≈ 0) hold only under the every-cycle rule above, or under the noted alternative.

## D3. Unchanged
Everything else in v1–v1.3 stands. That includes the CNA part as governing (v1.3 G1), the Lead rulings G2–G5 as amended here, safety S1–S10 with the standard string in no-period form, X1–X5, simulated computation only, the claim ceiling and Q-separation, and no claims of consciousness, C4/C5, "alive" or "autopoietic". Credit: the D1 linear-case condition and the D2 selection catch are CNA's. The joint-independence wording in D1 and the extension of D2 to all plants and agent arms are RD's.
---
sha256 of all bytes above this line (every byte from the start of the file through the newline that ends the '---' line; UTF-8): a470afa05dcbd14acaa26e7ddd984868219239dd657a957d2229a54caf56fdf8
