# PR #5 results erratum B: K-EXACT quantized-oracle phase mismatch (DRAFT v1)

**Status:** DRAFT. Nothing is committed or frozen. The bug is **CONFIRMED** by reading the code and by a scratch reproduction. The fix and the rerun below are proposals.
**Proposed repo path when adopted:** `acquisition_results_v1_errata/ERRATUM_B_KEXACT_PRECISION_v1.md`, plus the additive code and test files in §5. No frozen file is edited.
**Applies to:** PR #5 head `b25a30a`. The frozen `twostream_acquisition_metrics.py` has sha256 `bb7f0440d08ea52faf01dc0e1764189a3f4629a991e60a08ff9cbb465abc5302`, and the frozen `acquisition_results_v1/reference_arms.json` has sha256 `c6b8afa3cb3dcfebb502d62b7d762c397afbc1ef017584f898796396c20a91c7`.
**Source:** Astra consult #11, "One concrete correction before resource claims".

---

## 1. The bug

`quantized_exact_forecasts` is in `twostream_acquisition_metrics.py`, L947–967 at `b25a30a`:

```python
for stage in range(8):
    ...
    mx, my, c = _observe_f(mx, my, c, variable, bit)
    if stage < 7:
        mx, my, c = _transit_f(mx, my, c)          # <- transition applied here
    reconstructed, outside, _constant = quantize_coordinates(
        np.array([mx, my, c]), ranges[stage][0], ranges[stage][1], bits)   # <- quantized after transit
```

The ranges come from `exact_ranges(world)` (L936–944), which takes the min and max of `_prefix_chart(prefix, stage)` over TRAIN prefixes. `_prefix_chart` calls `filter_prefix(prefix, stage)`. That is the belief **after observing reading `stage`, with no trailing transition**: `twostream_filter.py`, "Observe, then transition, with no transition after the last reading".

So at stages 1–7 the code quantizes the post-transition chart, but against post-observation ranges. Only stage 8 is phase-matched. The transition contracts the marginals toward ½ (by a·b_x and a·b_y) and mixes the covariance. The post-transition chart therefore falls outside the post-observation box for many histories, and those values are **clipped**.

That clipping error does not shrink as b grows. It is why the TRAIN error plateaus and why "K-EXACT fails even at 24 bits".

**The learner arms are not affected.** In `rollout_quantized` and `state_ranges` (L699–731), the ranges are built from `states[stage-1]`, the state after `model.step` for reading `stage`, and quantization is applied right after the same `model.step`. The phases match.

## 2. Evidence (scratch reproduction; frozen code imported unmodified)

Everything is in `/workspace/scratch/pr5/` (a clone of PR #5 head; the repo is untouched). The main files are:
- `repro/repro.py` and `repro/repro_results.json`
- `repro/overshoot.py` and `repro/overshoot.log`
- `repro/verify_fixed.py`, `repro/verify_fixed.log` and `repro/fixed_reference_precision.json`

Torch is not installed on the box, so a stub (`repro/torchstub`) satisfies the module-level imports. None of the code paths exercised touch torch.

**(i) Clipping size under exact, unquantized propagation.** The table gives the maximum overshoot of the value that each ordering quantizes, relative to `ranges[stage]`:

| reading | frozen order (post-transit), TRAIN | fixed order (post-obs), TRAIN | fixed order, TEST |
| --- | --- | --- | --- |
| 1 | 0 | 3.0e-9 | 3.0e-9 |
| 2 | **3.03e-2** | 3.0e-9 | 3.0e-9 |
| 3 | **3.15e-2** | 1.1e-8 | 1.1e-8 |
| 4 | **3.31e-2** | 2.2e-8 | 2.2e-8 |
| 5 | **2.06e-2** | 1.8e-8 | 1.8e-8 |
| 6 | **1.38e-2** | 2.8e-8 | 6.5e-2 |
| 7 | **2.18e-3** | 2.0e-8 | 1.7e-2 |
| 8 | 1.0e-8 | 1.0e-8 | 3.0e-2 |

The frozen ordering clips TRAIN histories by about 0.03 in chart units at readings 2–5. The fixed ordering clips TRAIN histories only at the float32 endpoint-rounding level (≤ 3e-8). The fixed ordering does clip TEST histories, and that clipping is real: TEST prefixes from reading 6 onward lie outside the TRAIN ranges, as the TRAIN-only range rule intends.

**(ii) Isolation check.** The frozen ordering with unbounded ranges (±10, so nothing clips) at 52 bits matches the exact forecasts to a maximum |Δq| of **2.1e-14**. The dynamics `_observe_f` and `_transit_f` are correct. The clipping caused by the phase mismatch is the only error source.

**(iii) Precision curves on TRAIN (A-FIT TRAIN gate: total ≤ 0.018995707, XOR ≤ 0.0018827238).**

| b | frozen TRAIN E_total | frozen TRAIN E_XOR | frozen A-FIT TRAIN | fixed TRAIN E_total | fixed TRAIN E_XOR | fixed A-FIT TRAIN | fixed TEST E_total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2.56e-2 | 9.31e-3 | no | 3.33e-2 | 1.67e-2 | no | 4.48e-2 |
| 3 | 8.84e-3 | 3.85e-3 | no | 5.57e-3 | 2.71e-3 | no | 6.78e-3 |
| 4 | 4.99e-3 | 3.13e-3 | no | **1.19e-3** | **5.90e-4** | **yes** | 1.65e-3 |
| 5 | 3.32e-3 | 2.32e-3 | no | 2.76e-4 | 1.27e-4 | yes | 1.12e-3 |
| 6 | 2.88e-3 | 2.10e-3 | no | 5.39e-5 | 2.54e-5 | yes | 7.03e-4 |
| 8 | 2.89e-3 | 2.11e-3 | no | 3.89e-6 | 1.63e-6 | yes | 6.88e-4 |
| 12 | 2.86e-3 | 2.09e-3 | no | 1.65e-8 | 8.70e-9 | yes | 6.70e-4 |
| 16 | 2.86e-3 | 2.09e-3 | no | 5.11e-11 | 2.15e-11 | yes | 6.70e-4 |
| 24 | **2.86e-3** | **2.09e-3** | no | **9.43e-16** | **4.36e-16** | yes | 6.70e-4 |

The frozen numbers reproduce `reference_arms.json` exactly; for example, b=24 TRAIN gives E_total 0.0028588145 and XOR 0.0020859595. The frozen curve **plateaus at a TRAIN XOR excess of 2.09e-3**, which is above the XOR gate of 1.88e-3. That plateau is why no b in the grid qualifies.

The fixed curve converges to the exact TRAIN forecasts as b grows: at b=24 the maximum TRAIN |Δq| is 4.6e-8, the float32 endpoint floor. Under the frozen selection rule it gives **b_sel = 4, CONFIRMED on TEST** (TEST E_total 1.65e-3 ≤ 0.0203873 and XOR within its gate). The TEST plateau of 6.7e-4 comes from real TEST out-of-range clipping. It is below the gate and is reported descriptively.

**(iv) Alternative fix for comparison only (not proposed).** Keep the frozen ordering and build the ranges from post-transition TRAIN charts. This also converges: b_sel = 4, TRAIN E_total 1.06e-15 at b=24, TEST plateau 2.74e-4. It is rejected because it charges a different object: a predicted pre-observation chart, not the post-observation state. It also does not match Astra's specification or the learner arms, whose stored state has already absorbed reading k.

## 3. The fix (diff against the scratch copy)

The diff is in `/workspace/scratch/pr5/fix.diff` (sha256 `bddf949f…`). The patched scratch file is `/workspace/scratch/pr5/fixed/twostream_acquisition_metrics.py` (sha256 `152b1563…`).

```diff
@@ -953,9 +953,13 @@
         for stage in range(8):
             bit = (history >> stage) & 1
             variable = "X" if stage % 2 == 0 else "Y"
-            mx, my, c = _observe_f(mx, my, c, variable, bit)
-            if stage < 7:
+            if stage > 0:
+                # Transition for this step is applied to the previous stage's repaired,
+                # quantized post-observation chart, before the next reading.
                 mx, my, c = _transit_f(mx, my, c)
+            mx, my, c = _observe_f(mx, my, c, variable, bit)
+            # Quantize the post-observation chart: ranges[stage] are post-observation
+            # TRAIN charts after reading stage+1 (filter_prefix, no trailing transition).
             reconstructed, outside, _constant = quantize_coordinates(
                 np.array([mx, my, c]), ranges[stage][0], ranges[stage][1], bits
             )
```

The corrected order per step is: transition the previous repaired chart, observe, quantize against post-observation ranges, then repair. The retained state between steps is still the three indices. The transition is part of the next step's deterministic update, so the protocol §5.2 "charged state = three quantization indices only" still holds. This matches Astra's specification: "transition before the next observation, then quantize the post-observation chart against matching ranges." Nothing else changes: not the grid, the ranges rule, float32 endpoints, rounding, repair, the selection rule or the confirmation rule.

**For adoption, the frozen file is not edited.** §5 adds a new module that defines the corrected function.

## 4. Effect on E1, E2, E3 and the study verdict: none

- E1 and E2 score learner forecasts with `component_excess(preds, world)` against `world.q`. That is the frozen K-EXACT forecast loaded from `twostream_results_v1/results.json` (`twostream_acquisition_oracle.World`), not the quantized oracle.
- The A-FIT thresholds come from `world.e_cur` and `world.e_prod`. They do not depend on quantization.
- `twostream_acquisition_verdicts.py` does not reference precision. `summary.json` takes only `reference_afit_test` from the reference arms, which is the unquantized K-EXACT and is True.
- Learner b_sel values are unaffected, because their phases match (§1).
- **Superseded frozen outputs (two items):**
  - `RESULTS.md` L2339: "K-EXACT b_sel: no qualifying precision in the declared grid. Confirmation: NOT CONFIRMED."
  - The `K-EXACT.precision` block of `acquisition_results_v1/reference_arms.json`.

  Both stay in place and are marked superseded by the erratum.

## 5. Corrected precision rerun plan (preregistered; analytic, no training)

The rerun is analytic only. It needs no neural training and no torch: it is pure numpy on exact references.

**Files to add (new; nothing frozen is edited):**
1. `twostream_acquisition_precision_fix_v1.py` imports the frozen helpers (`_observe_f`, `_transit_f`, `_repair`, `quantize_coordinates`, `exact_ranges`, `component_excess`, `afit_holds`, `B_GRID`). It defines `quantized_exact_forecasts_v1_1` (the §3 ordering) and `kexact_precision_v1_1(world)`, which uses the same selection and confirmation logic as `reference_arm_report`.
2. `test_twostream_precision_fix_v1.py` contains these checks:
   - (T1) Fixed ordering with ±10 ranges at b=52 matches `world.q` with max |Δq| ≤ 1e-12.
   - (T2) Fixed ordering with frozen ranges: the maximum TRAIN overshoot at every stage is ≤ 1e-7 (float32 endpoint rounding only).
   - (T3) TRAIN E_total(b) is strictly decreasing over b ∈ {8, 12, 16, 20, 24}, and E_total(24) ≤ 1e-12.
   - (T4) The frozen `quantized_exact_forecasts` still reproduces `reference_arms.json` exactly, as a regression and provenance check.
   - (T5) The sha256 of the frozen `twostream_acquisition_metrics.py` equals `bb7f0440…`.
3. `acquisition_results_v1_errata/reference_precision_v1_1.json` holds the full curve: b, TRAIN/TEST errors, `train_afit`, repairs, clip counts, plus new per-stage **maximum clip overshoot** columns (descriptive), b_sel, confirmation, and stage-wise charged bits.
4. `acquisition_results_v1_errata/ERRATUM_B_KEXACT_PRECISION_v1.md` contains §§1–4 and the rerun outputs.

**Preregistered expectations and decision rules:**
- The frozen selection rule is applied unchanged: b_sel is the smallest b in the grid where TRAIN meets A-FIT, with confirmation on TEST.
- Expected from the scratch reproduction: **b_sel = 4, CONFIRMED**. Charged state is 3 × 4 = 12 bits nominal. Stage-wise, constant coordinates are charged 0 bits. m_y and c are constant at stage 1, and c is constant at stage 2, so the charge is 4, 8, 12, 12, 12, 12, 12, 12 bits for stages 1–8. Metadata is 64·3·8 bits.
- If the rerun disagrees with the expectation, the rerun's value is reported. No re-tuning is allowed.
- T1–T5 must all pass before the corrected values are reported. If any fails, report **UNRESOLVED** with the failing test.
- Clip counts are additionally reported with their overshoot size. Under the corrected ordering most TRAIN "clips" are float32 endpoint-rounding events of ≤ 3e-8, and the raw counts overstate them. This is descriptive only; the frozen clip rule is unchanged.

**Interpretation limits:**
- The corrected K-EXACT b_sel is a **descriptive resource reference**: a 12-bit indexed exact chart reaches A-FIT on TRAIN and is confirmed on TEST.
- It is not a learner result, not a claim that GRU-8 "uses" a chart, and not an input to any verdict.
- Any comparison with learner state bits (CAND GRU-8 b_sel = 4 on 8 seeds, so 32 bits nominal) is descriptive, and only after the rerun is committed. Consult #11 says "before resource claims", so no resource claim should be made from the scratch numbers.

## 6. Open points for Astra

- **B-1.** Should the erratum also make a "maximum clip overshoot" column a standing descriptive field for learner arms? This would be additive and would leave learner b_sel unchanged.
- **B-2.** The rule that casts float32 endpoints to nearest gives about 1e-8 TRAIN micro-clips. Rounding outward instead (lo down, hi up) would remove them. That would change the frozen quantizer, so it is **not** proposed here. Is it worth flagging for future protocols?
