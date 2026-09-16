# AC58 protocol v1 — repair retains the acquired order, preventing corruption-induced collapse

Written before any final seed. Engineering (`ac58_engineering.py`) on seeds 4612–4635 (two disjoint
families), scoring on 9012–9023 — all disjoint from the final seeds 4848–4859 declared below.

## The claim

In the scaled body, the acquired six-position order held in a replica-encoded register is corrupted over
the run; paying to repair the register retains the order, sustaining production and survival — while an
unrepaired register corrupts and the organism collapses. This is AC14's integrity channel, which AC43
left off (`reg_rate = 0`); it is turned on here and joined to the developmental line (AC57's acquired
order).

AC58 engineering established the claim's honest shape: corruption is **abrupt**, not gradual — below a
damage rate of ~0.001 nothing happens, above ~0.003 the register corrupts catastrophically and the
organism dies. So this is a survival/integrity claim: repair prevents corruption-induced collapse, not a
gradual loss.

## The world (reused, verified)

AC57's scaled body: regime B (`VALUES_B = (0.5, 2, 3, 4, 5, 100)`, `RATES_B` = reversed `stress_rates()` × 7),
AC50's `World` mechanics, the acquired order `OPT_B = (5, 1, 2, 4, 3, 0)` written to a 10-bit × 7-replica
majority-4 register (`ac29_register`). Each tick the register is damaged (each replica flipped with
probability `DAMAGE_RATE = 0.005`); the repaired arm then restores majority bits at a cost of 1 energy
(`REPAIR_BUDGET = 10`), the unrepaired arm does not. The order read back from the register decides which
region is repaired that tick. Endpoint: cumulative value-weighted production over 600 ticks.

## Arms

| arm | register |
| --- | --- |
| `protected` | never damaged (ceiling) |
| `repaired` | damaged + repaired each tick (1 energy) |
| `unrepaired` | damaged only |

## Seeds

- Engineering: 4612–4623 (family 1), 4624–4635 (family 2). Scoring: 9012–9023.
- **Final: 4848–4859** (12 individuals, disjoint from all of the above).

## Gates (declared before seeds)

| gate | bar |
| --- | --- |
| G1 resolvable | sign-flip p ≤ 0.01 on (repaired − unrepaired), n ≥ 8 |
| G2 effect | median(repaired − unrepaired) ≥ 8000 value-units |
| G3 retention | repaired == protected for every individual |
| G4 repaired stability | 0 dead in the repaired arm |
| G5 protected stability | 0 dead in the protected arm |
| G6 corruption consequential | unrepaired arm has ≥ 1 dead individual |
| G7 horizon-robust | repaired production@1500 / @600 in [2.4, 2.6] |
| G8 completeness + determinism | all 12 × 3 arms; re-run of first 2 reproduces |

The unrepaired arm's death count is the honest consequence of corruption and is reported descriptively
(G6 pins it as non-zero rather than hiding it).

## Four-check (engineering, two families)

| | family 1 | family 2 |
| --- | --- | --- |
| repaired − unrepaired p | 0.0005 | 0.0005 |
| repaired − unrepaired median | 18,295 | 21,312 |
| impaired | 0/12 | 0/12 |
| repaired == protected | yes (median diff 0) | yes |
| dead (repaired / protected / unrepaired) | 0 / 0 / 5 | 0 / 0 / 5 |
| horizon @1500/@600 | 2.487 | — |

SOURCES (declared): ac58_order.py ac58_engineering.py ac50_heterogeneous.py ac30_acquire.py ac29_register.py ac38_variance.py AC58_PROTOCOL_v1.md

## Bounds

Nothing here claims autopoiesis, closure, or life. The order is supplied; the register and repair are
supplied mechanisms. This establishes that repair retains the acquired order and prevents
corruption-induced collapse — the integrity channel, on.
