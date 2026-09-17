# AC1–AC4 foundational-claims confirmation — results (confirmatory v1)

2026-09-17. Same-author confirmatory study. Re-runs the decisive contrasts of
AC1–AC4 on fresh seed families (5100–5507) with prespecified gates, reusing the
frozen physics **unmodified** (`ac1.py`, `ac1_followup.py`, `ac2.py`, `ac3.py`,
`ac4.py`, `ac4_transport.py`). Protocol hashed before the run
(`AC1_4_CONFIRMATION_PROTOCOL_v1.md`). This closes status item 28 for the
foundational constituent claims; it is not external preregistration or
independent scientific review, and it changes nothing about the broader
autopoiesis claim.

## Verdict

**AC1, AC2, AC4 (transport and long-horizon repair dependence) fully confirm:
every prespecified claim gate passes at every declared rate on fresh seeds.**
**AC3 confirms at two of three rates; at the highest corruption rate its
self-viability gate fails (7/8 complete rather than 8/8) while all causal gates
pass.** The one failure is recorded, not amended, and is reported as a
robustness caveat rather than a falsification of the C-dependence mechanism.

## AC1 confirm — vulnerable controller pays for its own repair (seeds 5100–5107, 3,000 ticks, no pulse)

| p | self | no_policy_write | free_policy_ablation | protected | paid contrast | free contrast |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.0005 | 1.000 (8/8) | 0.306 (0/8) | 0.373 (0/8) | 1.000 (8/8) | +0.694 [0.626, 0.769] | +0.627 [0.539, 0.723] |
| 0.001 | 1.000 (8/8) | 0.145 (0/8) | 0.150 (0/8) | 1.000 (8/8) | +0.855 [0.810, 0.899] | +0.850 [0.809, 0.893] |

All 8 paired differences positive at each rate. Every `self` individual writes
all four banks. Gates G1–G5 pass at both rates. The free-ablation contrast
confirms the dependence is not futile spending: refunding controller-write costs
does not rescue activity.

## AC2 confirm — produced W catalysts enable controller repair (seeds 5200–5215, 4,096 ticks)

| p | self | no_synthesis | no_synthesis_rescue | protected | synthesis contrast | clamp info contrast |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.00025 | 1.000 (16/16) | 0.620 (0/16) | 1.000 (16/16) | 1.000 (16/16) | +0.380 [0.267, 0.493] | +0.732 [0.713, 0.752] |
| 0.0005 | 1.000 (16/16) | 0.342 (0/16) | 1.000 (16/16) | 1.000 (16/16) | +0.658 [0.563, 0.734] | +0.856 [0.840, 0.871] |

All 16 paired differences positive at each rate. The clamp contrast
(`self_clamp − no_synthesis_clamp` policy accuracy) confirms information
maintenance, not mere survival: resource abundance preserves execution but not
the acquired controller without produced W. Every `self` individual produces
>120 W and writes every bank. Gates G1–G6 pass at both rates.

## AC3 confirm — produced C converters supply usable energy (seeds 5300–5307, 4,096 ticks)

| p | self | no_C | C dependence | W-clamp info | self completes |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.0001 | 1.000 | 0.055 (0/8) | +0.945 [0.944, 0.945] | +0.344 [0.323, 0.360] | 8/8 |
| 0.0002 | 1.000 | 0.055 (0/8) | +0.945 [0.945, 0.945] | +0.757 [0.739, 0.778] | 8/8 |
| 0.0004 | 0.969 | 0.055 (0/8) | +0.914 [0.851, 0.945] | +0.915 [0.904, 0.926] | **7/8** |

`no_C_rescue`, `no_C_energy`, `protected`, `self_energy` complete 8/8 at every
rate. The C-dependence and W-under-clamp contrasts are large and positive at
every rate, and every `self` individual produces >120 W and >30 C, converts
fuel, and writes every bank.

**G1 (self completes 8/8) FAILS at p = 0.0004:** one fresh-seed individual died
(activity 0.751, final policy accuracy 0.9844 — the lowest of the eight), the
policy-corruption-then-death pattern the AC2 highest-rate chronology named. The
engineering claim "all 24 self runs complete" does not fully transfer to fresh
seeds at the highest rate. This is recorded as a gate failure, not amended; the
claim's causal content (G2 C dependence, G4 W dependence under energy clamp, G6
turnover) passes at all three rates, so the produced-converter mechanism is
confirmed and only the self-viability-at-the-highest-rate edge is qualified.

## AC4 short (transport) — produced B boundary retains machinery (seeds 5400–5407, 2,048 ticks)

| p | self | no_B | no_B_rescue | no_B_retention | protected | B contrast |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.00005 | 1.000 (8/8) | 0.183 (0/8) | 1.000 (8/8) | 1.000 (8/8) | 1.000 (8/8) | +0.817 [0.789, 0.840] |
| 0.0001 | 1.000 (8/8) | 0.171 (0/8) | 1.000 (8/8) | 0.959 (7/8) | 1.000 (8/8) | +0.829 [0.817, 0.842] |

Every `no_B` individual exports W/C (transport loss), every `self` individual
produces >40 B, and the retention rescue restores activity. Gates GA1–GA4 pass
at both rates.

## AC4 long (repair dependence) — maintained decision information enables sustained activity (seeds 5500–5507, 8,192 ticks)

| p | self | no_policy_write | protected | no_B_retention | repair contrast |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.00005 | 1.000 (8/8) | 0.621 (0/8) | 1.000 (8/8) | 0.751 (1/8) | +0.379 [0.245, 0.540] |
| 0.0001 | 1.000 (8/8) | 0.437 (0/8) | 1.000 (8/8) | 0.479 (0/8) | +0.563 [0.442, 0.675] |

`no_policy_write` completes 0/8 at both rates; `self` completes 8/8 with 100%
policy accuracy. All 8 paired differences positive. Gates GB1–GB3 pass at both
rates, confirming controller repair is necessary for sustained activity at the
long horizon (the AC4 follow-up's claim, now on fresh seeds).

## Verification

`audit_ac1_4_confirm.py` passes: 568 rows, rectangular coverage across all five
studies, `rows.jsonl` agreement, source hashes (protocol + runner + six frozen
dependencies) un-drifted, and every mean, contrast and gate re-derived from the
saved table without simulating. `replay_ac1_4_confirm.py` reports 59/59 exact
sampled reruns (first seed of each study, all arms and rates).
`test_ac1_4_confirm.py` (10 tests) passes, including seed-family disjointness
against every prior AC-line family and a falsifiability test asserting GB2 can
fail. Wall time 150.8 s on Python 3.12 / NumPy 2.5.3. Verification tools are
hashed into the report only, never the frozen snapshot.

## Claim boundaries

This confirms, on fresh seeds, that (1) acquired controller information drives
and receives paid maintenance and disabling that repair breaks operation even
when free (AC1); (2) that repair requires produced, decaying W catalysts and the
dependence survives resource abundance (AC2); (3) that produced C converters
supply the energy for maintenance, with the C- and W-dependence robust to the
highest rate despite one self death there (AC3); and (4) that the produced B
boundary retains machinery via transport and controller repair enables
sustained activity at the long horizon (AC4). It does not establish autonomous
need acquisition, a self-produced controller, rich development, full
autopoiesis or subjectivity; those remain governed by the later frozen studies
and the structural gap in `DEPENDENCY_AUDIT_v1.md`.
