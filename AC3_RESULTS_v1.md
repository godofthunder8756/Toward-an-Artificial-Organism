# AC3: maintained energy conversion supports acquired organization

2026-09-14. Engineering evidence. The broader autonomy goal remains active.

## Finding

The vulnerable acquired controller now maintains both its repair catalysts W
and fuel-to-energy converters C. W enables controller repair and C production;
C supplies usable energy for decisions, repair and constituent production.
Fuel collection itself supplies no usable energy. All 24 self runs (eight seeds
in three repeated environments) completed 4,096 ticks with 100% final controller
and payload accuracy. Every individual produced 63 C and at least 508 W.
The initial constituents expired long before the endpoint.

This establishes a designed, model-relative maintenance dependency involving
decision information, repair machinery and energy conversion. It does not
establish autonomous acquisition of needs, self-produced enclosure or full
autopoiesis. Acquisition memorizes demonstrations from only 24 priority
permutations. The larger table is not additional independently acquired entropy.

## Full engineering grid

[Protocol](AC3_PROTOCOL_v1.md) and [source snapshot](ac3_results_v1/pre_run_snapshot.json)
precede the run. All 216 rows are retained in [data](ac3_results_v1/results.json).
These are same-author engineering comparisons, not independent confirmation.
The larger AC3 representation and different rates prevent a matched robustness
comparison with AC2.

Mean fraction of planned ticks active:

| Copy-flip probability | Self | No C production | C rescue | Energy rescue of no C | No W production | Self, energy clamp | No W, energy clamp | No policy writes | Protected policy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.0001 | 1.000 | 0.055 | 1.000 | 1.000 | 0.061 | 1.000 | 1.000 | 0.842 | 1.000 |
| 0.0002 | 1.000 | 0.055 | 1.000 | 1.000 | 0.061 | 1.000 | 1.000 | 0.507 | 1.000 |
| 0.0004 | 1.000 | 0.055 | 1.000 | 1.000 | 0.061 | 1.000 | 1.000 | 0.241 | 1.000 |

Every configuration passed the stated engineering criteria. Blocking C or W
production yielded zero completions. Blocking policy writes yielded 3/8, 0/8
and 0/8 completions. Self-minus-no-policy-write activity differences were
15.8, 49.3 and 75.9 percentage points, with descriptive paired 95% bootstrap
intervals [5.1,26.3], [39.1,58.7] and [70.9,79.9]. Seeds are the replication
unit; environments are repeated conditions, not 24 independent individuals.

## Activity rescue is not organizational rescue

Energy clamps refill usable energy each tick. They keep execution going even
when the controller is damaged. Final policy accuracy makes the distinction:

| Rate | Self with energy clamp | No W with energy clamp | No C with energy clamp |
| --- | ---: | ---: | ---: |
| 0.0001 | 100.0% | 65.9% | 67.1% |
| 0.0002 | 100.0% | 24.4% | 26.1% |
| 0.0004 | 100.0% | 8.7% | 8.8% |

The W-dependent accuracy differences are 34.1 [31.4,36.7], 75.6 [74.1,77.2]
and 91.3 [89.9,92.6] percentage points. Thus energy supply alone does not
preserve the acquired controller without its produced repair machinery.
The direct reaction tests separately verify that W gates actual writes.

C rescue restores both activity and final information in all tested runs.
It favorably maintains at least three external converters, whereas self runs
finish with two; this is a rescue intervention, not an efficiency comparison.
Energy rescue restores activity but fails to restore information. Inspection of
the specified policy offers a candidate explanation: persistent low C prioritizes
blocked synthesis over repair. This is not a demonstrated causal mediation
analysis. The controller does not learn to relinquish an unnecessary reaction
when external energy substitutes for it. That limitation stays explicit.

High raw accuracy in terminated no-C/no-W individuals is not continued
maintenance: their states freeze early. Functional endpoints score them zero.

## Physical accounting and verification

Each self run produces 63 C, experiences 64 C expirations and ends with two:
3+63−64=2. W production is 508 in all but one self run, which produces 512.
All four banks receive paid writes. Fuel conversion ranges from 1,394 to
3,615 units across the tested environments and individuals. Each converted
unit supplies eight energy units under the explicitly supplied reaction law.

The [audit](AC3_AUDIT_v1.json) verifies all 216 rows, source snapshot hashes,
rectangular coverage, paired environments, all means and descriptive intervals,
and 27 exact replays (seed zero, every arm and rate). Eight mechanism tests pass.
Material accounting includes free precursor, bound W/C, imported material,
external converter additions, replacement waste, expiry waste and overflow.
Fuel and usable energy balance separately. Blocked reactions do not produce
hidden constituents, and fuel collection does not directly create energy.

Complete-state erasure and protected-template rejection cover the expanded
state: traces, W/C lifetimes, fuel, energy, precursor and termination. These
tests concern the declared simulator boundary, not all possible architectures.

Generic execution, sensing, memory addressing, molecular recipes, product
inhibition, shared energy transport and enclosure remain supplied. There is no
spatial boundary, spontaneous chemistry or biological validation. Conventional
error correction remains part of this constructive witness; its conventional
status does not invalidate the measured dependence, nor imply new intelligence.

## Next experiment

The next structural target is a produced boundary B with explicit spatial
transport. Its absence must cause measured loss of constituents through actual
transport, rather than an arbitrary boundary-quality death threshold. Required
contrasts include boundary-production ablation, external boundary rescue and
matched retention rescue, while measuring controller accuracy and turnover.

Before claiming broad autonomy, the architecture must also demonstrate acquired
maintenance dependencies and viable policy adaptation. The energy-rescue
information failure supplies a concrete challenge for that later test. Adding
another demonstrated maintenance action alone cannot satisfy it.

## Reproduction

```powershell
py -3.12-arm64 -B -m unittest -v test_ac3
py -3.12-arm64 -B ac3.py --out new_ac3_engineering
```

The runner refuses an existing output directory. Recorded runtime was about
277 seconds on Python 3.12 ARM64 with NumPy 2.3.5. [Model](ac3.py),
[tests](test_ac3.py), [audit source](audit_ac3.py). Earlier freezes remain intact.
