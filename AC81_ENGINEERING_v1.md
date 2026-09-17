# AC81 engineering v1: component replacement across generations — the design is measured

2026-09-17. Engineering only — no protocol, no final seeds, no claim. `ac81_engineering.py`
(final design), `ac81_probe.py` + `ac81_measure2.py` (exploratory).

## What the milestone requires

Milestone 2 (replacement across generations) follows AC80 (recipe internalized). The claim to
establish: the organism's **physical components** — W catalysts, C converters, B boundary — are
constructed, used, and replaced across multiple turnover cycles, driven by the internally retained
production recipe (the 78-bit description), with **partial losses** rebuilt and **multiple turnover
cycles** demonstrated, and **without** requiring resurrection after destruction of every usable
copy (the catastrophic-destruction analog already out of scope).

## Measured first: what the turnover actually is

In the AC80 internalized world (no intervention), over 16,384 ticks, per surviving individual:

| component | initial live | births over horizon | turnover multiple |
| --- | --- | --- | --- |
| W (16 slots, 3 live) | 3 | ~1506–1524 | ~94× its 16 slots, ~500× its 3 live |
| C (4 slots, 3 live) | 3 | ~255 | ~64× its 4 slots |
| B (20 sites) | 20 | ~1679–1686 | ~84× |

Uses are substantial in the same individuals: repair writes ~14,000–14,900, energy converted
~4,770–4,840, and both routes held (non-None). Every component class is therefore born many times
over the horizon — genuine multiple turnover cycles, not a held steady state. The turnover is the
observable "constructed, used, replaced."

## Measured second: which "partial loss" is clean

The natural damage stream already degrades the program and the description (sticky 1e-4), and the
organism rebuilds the program from the description and repairs the description (DESC_TRIGGER=2).
For an explicit partial loss, several interventions were screened:

- **Corrupt the 3 production rule words (42 bits) at t=8192**: too harsh. It pushes survivors into
  the AC68 W/C collapse branch (internalized 4/16 survive, pristine 8/16), and the residual
  "4 bits wrong" appears only in dying individuals — post-mortem degradation, not failed recovery.
  Dropped as the intervention; reported here so the choice is on the record.
- **Kill 2 W + 1 C + 5 B**: too harsh (kills half the W, 4/8 survive).
- **Kill 1 W**: adds a post-loss death (2/8 survive vs 4/8 baseline) — W powers repair, so it is the
  fragile component.
- **Kill 1 C, or 5 B, or 1 C + 5 B**: clean — survival is identical to the no-loss baseline (no
  additional deaths), and the killed converter/boundary are re-birthed as part of the continuing
  turnover.

The chosen intervention is therefore **kill 1 C converter + 5 B boundary sites at t=8192** — a
partial, non-catastrophic loss of the two replaceable components (C and B), leaving W (the repair
catalyst) intact so the loss is survivable and the rebuild is observable. The catastrophic analog
(destroying every usable copy) is deliberately not tested.

## Measured third: the arms separate on description integrity

With the loss at t=8192 (engineering seeds 0–7, 16 individuals/arm):

| arm | survive | descCorrect (survivors) | routes (survivors) |
| --- | --- | --- | --- |
| internalized | 12/16 | 78/78 | all held |
| pristine | 14/16 | 78/78 | 10/14 held (4 lose routes) |
| unmaintained | 0/16 | 22–25/78 | none held |
| no_repair | 0/16 | — | — |

The internalized survivors rebuild the killed C (C_birth_post ~128) and B (B_birth_post ~843) and
hold both routes with the description intact (78/78). The unmaintained arm's description degrades
to 22–25/78 (the production recipe is lost) and it dies 0/16. The no_repair arm dies 0/16 (loop
cut load-bearing, as in AC80). The baseline W/C collapse (seeds 2, 3 die pre-8192) is the AC68
bimodality, so recovery/description endpoints must be gated on **survivors** (exactly AC79/AC80).

## Design carried into the protocol

Arms = AC80's four (internalized, pristine, unmaintained, no_repair); intervention = partial
component loss (1 C + 5 B) at t=8192; endpoints = turnover (births), use (writes/converted/routes),
partial-loss recovery (post-loss births + restored populations), description integrity, survival.
Gates are categorical and gated on survivors where the paid maintenance stops at death:
turnover floors, use, partial-loss rebuild, recipe maintained (internalized 78/78 vs unmaintained
<78), maintenance load-bearing (unmaintained dies, internalized survives), loop cut dies, control
clean, completeness/determinism.
