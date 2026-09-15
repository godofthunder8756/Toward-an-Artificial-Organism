# AC17 engineering record: what the runs decided before the protocol

2026-09-15. Engineering only, seeds 0-1 x 2 histories (excluded from the final sample). The
frozen final sample and its verdict are in `AC17_RESULTS_v1.md`; the declaration is
`AC17_PROTOCOL_v1.md`.

## Claim B (both channels move) — killed here, not claimed

The first draft of AC17 carried a second claim: that the two-way rule also handles a move of
**both** channels, the world AC15 could not use because moving both makes drop-everything
optimal. Measured on engineering seed 0 (single individual, so a screen rather than a result):

| arm | ch0 (fuel, moved) | ch1 (material, moved) | mean |
| --- | ---: | ---: | ---: |
| `allocate_restore` (two-way) | 0.500 | 1.000 | 0.750 |
| `allocate` (one-way) | 0.333 | 0.714 | 0.524 |
| `relinquish` (always drop) | **1.000** | **0.857** | **0.929** |
| `preserve` | 0.000 | 0.000 | 0.000 |
| `restore_only` | 0.000 | 0.000 | 0.000 |

The crude always-relinquish arm — an arm with no decision at all, which simply never renews —
**beats the learner** in that world, because an organism that never renews is always free to
re-bind the current correct port. The two-way rule therefore adds nothing there.

Rather than reframe the claim to fit the measurement, the world was removed from the protocol
and the measurement is recorded here. This is the same discipline that should have caught the
G2 ceiling problem in the *gate* (see `AC17_RESULTS_v1.md`): run the screen before writing the
declaration.

The learner's own weakness in that world is also visible and worth recording: it holds
channel 1 (re-bound at t=1146) but only 0.500 on channel 0, because its restore rule needs a
**productive contact while the entry still exists** — if the re-bound entry lapses before the
next productive contact on that key, there is nothing to restore and the cycle repeats.

## Claim A — confirmed structurally before the protocol

`restore_only` (restore rule, no drop rule) on the single-channel world:

| seed | kept | moved | re-binding tick | relinquishments | restorations |
| --- | ---: | ---: | --- | ---: | ---: |
| 0 | 1.000 | 0.000 | none | 0 | 1 |
| 1 | 1.000 | 0.000 | none | 0 | 0.5 mean over 2 histories |

It restores maintenance when a route proves right, and it never relinquishes — so it never
frees the key, so the frozen deposit gate (`selected is None`) bars binding entirely. Predicted
from the code, then measured. It became G6 in the protocol.

## The single-channel engineering grid (8 individuals per arm)

| arm | alive | kept | moved | re-binding ticks |
| --- | --- | ---: | ---: | --- |
| `allocate_restore` | 4/4 | 1.000 | 1.000 | 1146, 1154 |
| `allocate` | 4/4 | 1.000 | 0.744 | 1146, 1154 |
| `restore_disabled` | 4/4 | 1.000 | 0.744 | 1146, 1154 (identical to `allocate`) |
| `preserve`, `no_learning`, `fixed_schedule`, `random`, `restore_only` | 4/4 | 1.000 | 0.000 | none |
| `fixed_period_1`, `streak_never` | 4/4 | 1.000 | 0.000 | none (identical to `preserve`) |

The rivard sweep (`sweep_ac17.py`, `ac17_engineering_sweep.json`) sweeps fixed duties 1/2/4/8,
random p 0.25/0.5/0.75 and the learner's own family (streaks 2/4/6/8); every blind
configuration scores 0.000 and the learner's whole family 1.000. The learner's final
configuration is the prespecified streak 6, not a member chosen from that sweep.

## Lesson recorded

Two consecutive versions were falsified by **gate shape** rather than by the mechanism: AC16's
mean margin over a partially-succeeding rival, and AC17's strict per-individual dominance,
which is unsatisfiable when both arms can reach the ceiling (measured: 2 of 8 individuals tie
at 1.000). Both misfits were avoidable at declaration time. The rule taken forward: derive the
gate from the claim's *logic* — "a one-way rule cannot hold" is a statement about the **worst
case**, so it is tested as a separation of minima, not as a mean and not per individual.
