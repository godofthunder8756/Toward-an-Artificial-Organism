# ERRATUM v1 — K-EXACT quantized-oracle phase mismatch

**Status:** Adopted additive erratum. The bug is confirmed by the frozen code and by the rerun in this directory. The frozen function is not edited.
**Adopted path:** `acquisition_results_v1_errata/ERRATUM_v1_quantized_oracle.md`.
**Draft proposed path:** `acquisition_results_v1_errata/ERRATUM_B_KEXACT_PRECISION_v1.md`.
**Applies to:** PR #5 results commit `b25a30a`. The frozen `twostream_acquisition_metrics.py` has sha256 `bb7f0440d08ea52faf01dc0e1764189a3f4629a991e60a08ff9cbb465abc5302`, and the frozen `acquisition_results_v1/reference_arms.json` has sha256 `c6b8afa3cb3dcfebb502d62b7d762c397afbc1ef017584f898796396c20a91c7`. Both hashes were rechecked and match.
**Source:** Astra consult #11, "One concrete correction before resource claims".

The corrected function is `quantized_exact_forecasts_v2` in the new module `twostream_acquisition_precision_v2.py`. The draft named it `quantized_exact_forecasts_v1_1`. The ordering is the ordering in the attached `fix.diff`.

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

The draft located its scratch reproduction at `/workspace/scratch/pr5/`. That directory is not in this checkout. The numbers below were recomputed here by importing the frozen helpers and by running `quantized_exact_forecasts_v2`. Section 2 of the draft is kept. Where this rerun agrees, it says so. The one disagreement is in the adoption note.

**(i) Clipping size under exact, unquantized propagation.** The table gives the maximum overshoot of the value that each ordering quantizes, relative to `ranges[stage]`. This rerun reproduces it.

| reading | frozen order (post-transit), TRAIN | fixed order (post-obs), TRAIN | fixed order, TEST |
| --- | --- | --- | --- |
| 1 | 0 | 2.98e-9 | 2.98e-9 |
| 2 | 3.03e-2 | 2.98e-9 | 2.98e-9 |
| 3 | 3.15e-2 | 1.05e-8 | 1.05e-8 |
| 4 | 3.31e-2 | 2.22e-8 | 2.22e-8 |
| 5 | 2.06e-2 | 1.85e-8 | 1.85e-8 |
| 6 | 1.38e-2 | 2.80e-8 | 6.49e-2 |
| 7 | 2.18e-3 | 1.97e-8 | 1.67e-2 |
| 8 | 1.03e-8 | 1.03e-8 | 2.98e-2 |

The frozen ordering clips TRAIN histories by about 0.03 in chart units at readings 2–5. The fixed ordering clips exact TRAIN charts only at the float32 endpoint-rounding level (≤ 2.80e-8). The fixed ordering does clip TEST histories, and that clipping is real: TEST prefixes from reading 6 onward lie outside the TRAIN ranges, as the TRAIN-only range rule intends.

**(ii) Isolation check.** The corrected ordering with unbounded ranges (±10, so nothing clips) at 52 bits matches the exact forecasts to a maximum |Δq| of 1.89e-14. The draft reported 2.1e-14 for the frozen ordering on the same check. The dynamics `_observe_f` and `_transit_f` are correct. The clipping caused by the phase mismatch is the frozen function's error source.

**(iii) Precision curves.** TRAIN A-FIT gate: total ≤ 0.01899570718353314, XOR ≤ 0.0018827237797535974. TEST gate: total ≤ 0.020387327436991155, XOR ≤ 0.002289619941692226.

The draft table omitted grid points b=10 and b=20. The rerun uses the full frozen grid. The printed rows match the draft's rounding.

| b | frozen TRAIN E_total | frozen TRAIN E_XOR | frozen A-FIT TRAIN | fixed TRAIN E_total | fixed TRAIN E_XOR | fixed A-FIT TRAIN | fixed TEST E_total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2.56e-2 | 9.31e-3 | no | 3.332e-2 | 1.665e-2 | no | 4.481e-2 |
| 3 | 8.84e-3 | 3.85e-3 | no | 5.567e-3 | 2.708e-3 | no | 6.782e-3 |
| 4 | 4.99e-3 | 3.13e-3 | no | 1.191e-3 | 5.896e-4 | yes | 1.652e-3 |
| 5 | 3.32e-3 | 2.32e-3 | no | 2.757e-4 | 1.270e-4 | yes | 1.122e-3 |
| 6 | 2.88e-3 | 2.10e-3 | no | 5.394e-5 | 2.539e-5 | yes | 7.026e-4 |
| 8 | 2.89e-3 | 2.11e-3 | no | 3.892e-6 | 1.625e-6 | yes | 6.875e-4 |
| 10 | 2.85e-3 | 2.08e-3 | no | 2.022e-7 | 9.550e-8 | yes | 6.721e-4 |
| 12 | 2.86e-3 | 2.09e-3 | no | 1.653e-8 | 8.699e-9 | yes | 6.701e-4 |
| 16 | 2.86e-3 | 2.09e-3 | no | 5.107e-11 | 2.146e-11 | yes | 6.703e-4 |
| 20 | 2.86e-3 | 2.09e-3 | no | 2.215e-13 | 1.023e-13 | yes | 6.703e-4 |
| 24 | 2.859e-3 | 2.086e-3 | no | 9.430e-16 | 4.362e-16 | yes | 6.703e-4 |

The frozen numbers reproduce `reference_arms.json` exactly, including b=24 TRAIN E_total 0.0028588144953225346 and XOR 0.0020859594831811887. The frozen curve plateaus above the TRAIN XOR gate 0.0018827237797535974. That plateau is why no b in the grid qualifies.

The corrected curve converges to the exact TRAIN forecasts as b grows. At b=24 the maximum TRAIN |Δq| is 4.633e-8. Under the frozen selection rule, **b_sel = 4 and confirmation is CONFIRMED**. TEST also first meets A-FIT at b=4 (TEST E_total 0.0016523181037595013, TEST E_XOR 0.000882518843751816). The TEST plateau near 6.70e-4 comes from real TEST out-of-range clipping. It is below the gate and is reported descriptively.

**(iv) Alternative fix for comparison only (not proposed).** Keep the frozen ordering and build the ranges from post-transition TRAIN charts. The draft reports that this also converges and rejects it because it charges a predicted pre-observation chart, not the post-observation state. This adoption does not implement that alternative. The adopted ordering matches the learner arms: the stored state has already absorbed reading k, and the next transition consumes that stored state.

## 3. The fix

The attached diff has sha256 `bddf949f0cc166d40cecf111e90d023f3e1c54ea61ba5f8940875208cf5da06d`, which is the draft's `bddf949f…` hash in full. It was not applied to `twostream_acquisition_metrics.py`. The same four-line reordering is the body of `quantized_exact_forecasts_v2`:

```python
if stage > 0:
    mx, my, c = _transit_f(mx, my, c)
mx, my, c = _observe_f(mx, my, c, variable, bit)
reconstructed, outside, _constant = quantize_coordinates(
    np.array([mx, my, c]), ranges[stage][0], ranges[stage][1], bits
)
```

The corrected order per step is: transition the previous repaired chart, observe, quantize against post-observation ranges, then repair. The retained state between steps is still the three indices. The transition is part of the next step's deterministic update, so the protocol §5.2 "charged state = three quantization indices only" still holds. Nothing else changes: not the grid, the ranges rule, float32 endpoints, rounding, repair, the selection rule or the confirmation rule.

No more correct ordering was found. The diff's ordering is the one that phase-matches `exact_ranges` and the learner update.

## 4. Effect on E1, E2, E3 and the study verdict: none

- E1 and E2 score learner forecasts with `component_excess(preds, world)` against `world.q`. That is the frozen K-EXACT forecast loaded from `twostream_results_v1/results.json` (`twostream_acquisition_oracle.World`), not the quantized oracle.
- The A-FIT thresholds come from `world.e_cur` and `world.e_prod`. They do not depend on quantization.
- `twostream_acquisition_verdicts.py` does not reference precision. `summary.json` takes only `reference_afit_test` from the reference arms, which is the unquantized K-EXACT and is True.
- Learner b_sel values are unaffected, because their phases match (§1).
- **Superseded frozen outputs (two items):**
  - `RESULTS.md` L2339: "K-EXACT b_sel: no qualifying precision in the declared grid. Confirmation: NOT CONFIRMED."
  - The `K-EXACT.precision` block of `acquisition_results_v1/reference_arms.json`.

  Both stay in place and are marked superseded by this erratum. The replacement curve is `acquisition_results_v1_errata/reference_arms_kexact_v2.json`.

## 5. Rerun that was actually committed

Analytic only. No neural training and no CAND or rival seed was rerun.

Adopted files, corresponding to the draft's §5 list:
1. `twostream_acquisition_precision_v2.py` defines `quantized_exact_forecasts_v2` and `kexact_precision_v2`.
2. `test_twostream_precision_v2.py` contains T1–T5. T2 is the exact unquantized post-observation TRAIN overshoot, which is the quantity in §2(i). See the adoption note for the iterative quantizer.
3. `acquisition_results_v1_errata/reference_arms_kexact_v2.json` holds the full curve, per-stage maximum clip overshoot for all histories and for TRAIN and TEST separately, exact-chart overshoot, b_sel, confirmation, and stage-wise charged bits.
4. `acquisition_results_v1_errata/NOTE_kexact_precision_v2.md` states the smallest passing precision and the 24-bit error.
5. This file.

Preregistered decision rule, applied unchanged: b_sel is the smallest b in the grid where TRAIN meets A-FIT, with confirmation on TEST. Result: **b_sel = 4, CONFIRMED**. Charged state is 3 × 4 = 12 bits nominal. Stage-wise, m_y and c are constant at stage 1 and c is constant at stage 2, so the charge is 4, 8, 12, 12, 12, 12, 12, 12 bits. Metadata is 64 × 3 × 8 = 1536 bits. The smallest b at which TEST meets A-FIT is also 4.

T1–T5 passed before these values were written into the JSON. T1 max |Δq| at 52 bits with ±10 ranges is 1.89e-14. T3 TRAIN E_total is strictly decreasing on {8, 12, 16, 20, 24} and E_total(24) = 9.43e-16. T4 reproduces `reference_arms.json` exactly from the untouched frozen function. T5 matches the metrics sha256 above.

**Interpretation limits:**
- The corrected K-EXACT b_sel is a descriptive resource reference: a 12-bit indexed exact chart reaches A-FIT on TRAIN and is confirmed on TEST.
- It is not a learner result, not a claim that GRU-8 uses a chart, and not an input to any verdict.
- Learner state bits are not compared here. No resource claim is made.

## Adoption note: what disagrees with the draft

1. **Iterative TRAIN overshoot is not "≤ 3e-8" at every bit width.** Section 2(i), and T2, describe exact unquantized post-observation charts. Those TRAIN overshoots are ≤ 2.80e-8, as the draft says. Once repaired indices are fed into the next transition, later TRAIN charts leave the exact TRAIN box by more than that. The maximum TRAIN overshoot of the value actually quantized is 0.009196768797005483 at b=4 (stage 8) and falls to 3.42e-8 only at b=24. Clip counts at coarse b therefore mix endpoint rounding with propagated quantization error. This does not move b_sel or the excesses in §2(iii). The draft sentence that most TRAIN clips under the corrected ordering are endpoint events of ≤ 3e-8 is true at b=24 and false below that.
2. **Names.** The draft's `quantized_exact_forecasts_v1_1`, `twostream_acquisition_precision_fix_v1.py`, `test_twostream_precision_fix_v1.py`, and `reference_precision_v1_1.json` are the v2 names in this commit. The selection rule is unchanged.
3. **Scratch paths.** `/workspace/scratch/pr5/` is absent here, so the patched-file sha256 `152b1563…` was not recomputed. The diff sha256 was recomputed from the attached diff and matches the draft prefix.
4. **Grid display.** The draft table skipped b=10 and b=20. Both are in the frozen grid and in `reference_arms_kexact_v2.json`. Both pass A-FIT on TRAIN and TEST. They sit on the same decreasing TRAIN curve.
5. Line numbers L947–967, L936–944, and L699–731 were rechecked against `b25a30a` and are right. RESULTS.md L2339 is right.

## 6. Open points left open

- **B-1.** Should a later protocol add a maximum clip-overshoot column for learner arms? Not done here. Learner b_sel values are untouched.
- **B-2.** Rounding the float32 endpoints outward is not proposed. It would change the frozen quantizer.
