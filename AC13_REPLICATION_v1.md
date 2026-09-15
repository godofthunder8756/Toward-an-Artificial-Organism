# AC13 replication check: the calibration result was seed noise, design falsified

2026-09-15. Engineering replication check. **No final seeds were run.** The AC13
protocol is unfrozen and its claim is not established. This is the third negative
result in the AC11→AC13 allocation line, and the third is what makes the
structural explanation solid.

## What happened

`AC13_CALIBRATION_v1.md` reported a positive first signal on six engineering
individuals (seeds 0-2): `allocate` completed 6/6 with phase-2 renewal writes 393
against `preserve`'s 662 — a 41% saving with equal productivity. Before running
the frozen sample, the same measurement was repeated on twelve fresh engineering
individuals (seeds 3-8, both histories) through the study runner:

| seed / history | allocate writes ph2 | preserve writes ph2 | saving | allocate alive | preserve alive |
| --- | ---: | ---: | ---: | --- | --- |
| 3/0 | 441 | 442 | +0.2% | yes | yes |
| 3/1 | 441 | 441 | 0.0% | yes | yes |
| 4/0 | 0 | 0 | 0.0% | **no** | yes |
| 4/1 | 444 | 108 | **−311.1%** | yes | **no** |
| 5/0 | 21 | 21 | 0.0% | no | no |
| 5/1 | 1 | 442 | +99.8% | yes | yes |
| 6/0 | 423 | 441 | +4.1% | yes | yes |
| 6/1 | 422 | 441 | +4.3% | yes | yes |
| 7/0 | 465 | 446 | −4.3% | yes | yes |
| 7/1 | 18 | 18 | 0.0% | no | no |
| 8/0 | 21 | 441 | +95.2% | yes | yes |
| 8/1 | 443 | 443 | 0.0% | yes | yes |

Mean saving **−9.3%** (the learner spends slightly *more* on average), range
−311% to +99.8%, and only 2 of 12 individuals show a saving above 5%. AC13's
protocol falsification clause — "if any static arm matches it on both phase-1
productivity and phase-2 renewal writes, the claim fails as stated" — therefore
fires: `preserve` matches on phase-1 productivity (1.000) and on phase-2 writes in
10 of 12 individuals.

## Why the saving is not there (measured)

The phase-2 renewal count is dominated by the slot the policy keeps, not by the
slot it drops. Post-intervention the yield is 12 and a correct contact cannot be
distinguished from a blind one, so material income is thin; the material slot's
entry is frequently undecodable, and `renew` on an undecodable slot writes
**nothing** by the frozen law. When that happens the drop is indistinguishable from
starvation, which lapses the slot in both arms (seed 4/0, 5/0, 7/1: writes 0, 21,
18 in *both* arms). When the entry stays decodable, both arms keep renewing it and
the difference is a handful of replicas (seeds 3, 6, 8: 4% or less). The 41% in the
calibration came from the two individuals (0/0, 0/1) where the kernel happened to
line up; the calibration's six individuals were too few to show that.

## What replicates, and what is falsified

Replicates (12/12 or near): the drop is triggered by the organism's own realized
contact outcomes, fires shortly after the intervention (tick 1050–1098), is paid
per replica, lands in the vulnerable program bank, and leaves the other slot's
maintenance intact; the usefulness-blind static dies while the route is valid
(`relinquish` 0-1/4, phase-1 productivity 0.23–0.28 against 1.000). The *decision
machinery* works.

Falsified: that the decision has a distinct economic consequence. On a wider
sample it does not, because paying for worthless information is either
unaffordable — in which case starvation lapses the entry in every arm — or
affordable — in which case the waste is a handful of replicas that changes nothing.
There is no middle in this architecture, and that is now supported by three
independent measurements (AC11 region granularity, AC12 per-slot granularity,
AC13 unreliable port with a wider sample).

## The structural limit, stated plainly

With a single-bit resource port whose blind fallback is uniform over the same
candidate set, the value of a stored route is either **decisive because fatal**
(`flip` worlds: a wrong stored value zeroes income) or **negligible** (unreliable
worlds: a stored value earns exactly what blind search earns). The maintenance
decision therefore never has a consequence intermediate between "forced by
starvation" and "irrelevant". No learner can demonstrate a need under those
conditions, because there is no such need to have.

Two architectural changes would change that, and both are supplied-law additions
needing their own primitive and protocol, exactly as AC12's per-slot renewal was
needed before AC13 could be posed at all:

1. **A graded access law**: being wrong should cost a *fraction* of the yield
   rather than all of it, so that a correct entry is worth strictly more than a
   blind attempt by an amount comparable to its maintenance cost, without zeroing
   income when wrong.
2. **A wider access channel with a non-uniform fallback**: a stored value must be
   able to carry more than one bit of usable information relative to what a blind
   attempt can reach, so that the fallback is strictly worse without being useless.

## What this does not affect

AC10's constituent ablations stand (they removed whole constituents, not
maintenance levels). AC9's results stand. AC12's per-slot primitive and the
dead-rule register stand, are equivalence-verified, and reproduce the frozen rows
exactly — they remain the correct foundation for any future allocation or
closure study. Nothing frozen was touched.

## Artifacts

`ac13.py` (runner), `test_ac13.py` (12 methods, all passing), `ac13_engineering_v1/`
(seeds 3-4), `ac13_calibration_v1/` (seeds 0-2), `AC13_CALIBRATION_v1.md` (the
result that did not replicate), `AC13_PROTOCOL_v1.md` (unfrozen, do not run).
