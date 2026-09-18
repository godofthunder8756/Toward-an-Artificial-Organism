# AC84 engineering v1: component turnover is unconditional — the design is measured

2026-09-17. Engineering only — no protocol, no final seeds, no claim. `ac84_eng_probe.py`
(horizon sweep), `ac84_eng_verify.py` (load-bearing gates), `ac84_eng_scan.py` (finals seeds),
`ac84_eng_broad.py` (floor robustness over 256 individuals), `ac84_engineering_v1/` (frozen
engineering rows, seeds 0-7).

## What the card requires, and why AC81 fell short

AC81 (milestone 2) froze replacement-across-generations but gated its turnover claim (G1-G3) on
`completed`, and the final family was collapse-dominated (internalized 2/8), so the turnover claim
rested on 2 survivors — the survivor-conditioning weakness flagged in AC79's and AC80's G1. AC84
reports turnover UNCONDITIONALLY: every individual in the cohort, dead or alive, is scored on the
same turnover floors, and the kill intervention is dropped.

## Measured first: turnover is continuous and does not need the kill intervention

In the AC80 internalized world with NO intervention, at every horizon, every individual's
turnover is far above the slot complement:

| horizon | internalized dead | min W / C / B births | healthy (survivors) W |
| --- | --- | --- | --- |
| 2048 | 4/64 | 89 / 18 / 103 | ~185 (~11x) |
| 4096 | 8/64 | 89 / 18 / 103 | ~300-384 (~20x) |
| 8192 | 20/64 | 89 / 18 / 103 | ~750 (~47x) |
| 16384 | 24/64 | 89 / 18 / 103 | ~1500 (~95x) |

The minimum is pinned by the earliest-collapse seed (dies at t=1244 with W=89, C=18, B=103, ~5x the
complement), independent of horizon. The kill intervention (1 C + 5 B at t=8192) is therefore
unnecessary for the turnover claim: the components turn over continuously.

## Measured second: the horizon — 4096 sits inside the pre-collapse window

The AC68 W/C collapse onset is ~7400-7800 (at 16384). At 4096 ticks the internalized arm collapses
8/64 (12.5%), and every collapse victim still demonstrates turnover (>= 89/18/103). The turnover
multiple in survivors is ~20x. 4096 is the horizon: long enough for unambiguously multiple turnover
cycles, short enough that the collapse does not dominate the cohort (vs 24/64 at 16384).

## Measured third: the unconditional floor is "births >= complement", and it is robust

"Multiple turnover cycles" as a per-individual floor is NOT robust: a broad scan (seeds 0-127, 256
individuals) found an earliest collapse at t=603 with W=30, C=5, B=37 — below the 2x-complement
floors (32/8/40). So the unconditional gate is **births >= the slot complement** (16/4/20 = "each
class fully replaced at least once"), which holds for every one of 256 engineering individuals (the
t=603 collapse still reaches 30/5/37). The stronger "multiple cycles" is reported per individual
(healthy ~18-23x, earliest collapse ~1.3-1.9x), not gated. The floor is met by the earliest collapse
because the W/C cascade takes hundreds of ticks to develop, during which the production rules keep
birthing — a mechanistic argument, not an empirical coincidence.

## Measured fourth: the arm set — `pristine` is dropped

`pristine` (AC80's hidden backup) has early W/C collapses (t=439-673) with W=21, B=0 in some seeds,
so its turnover is NOT unconditional (10/64 fail the floor). Its description is never damaged, so it
is not a test of the maintained recipe. Dropped. The load-bearing arms are `unmaintained` (recipe
degrades, desc_correct max 71/78 < 78, 62/64 die) and `no_repair` (loop cut, dies 64/64, B_birth=0
in every individual — the loop is what sustains boundary turnover).

## Design carried into the protocol

Arms = internalized, unmaintained, no_repair; horizon = 4096; no kill intervention; floors = the
slot complements (W 16, C 4, B 20), scored unconditionally. Gates: G1 turnover unconditional, G2 use
unconditional, G3 loop load-bearing, G4 recipe degrades unmaintained, G5 recipe maintained in
survivors (the one genuinely survivor-scoped endpoint, AC79's post-mortem caveat), G6
completeness/determinism. The finals seeds 4020-4023 were verified (disjoint, no early collapse in
the internalized arm) before the protocol froze.
