# AC37 engineering: a self-funded world that DOES resolve orders

2026-09-15. `ac37_selfsufficient.py`, engineering only so far. **No protocol, no final seeds, no claim
yet.** This records a positive design result and the economy it selects.

## The problem, and the fix

AC35 had the organism's own productive sites supply its energy, and the endpoint collapsed: spread 1.00
site against 0.30 of noise, because production scales with the living population, so a population near
carrying capacity maintains itself easily and **every order converges to 76–80% of maximum**.

The fix, stated before it was tested: add a **constant metabolic drain** that does not scale with the
population. The balance becomes

    E' = E + (productive sites)/PRODUCTION_PERIOD − DRAIN − RENEW_ENERGY × renewals

so self-sufficiency requires `productive sites > DRAIN × PRODUCTION_PERIOD` — a **population floor set by
the economy**, not by carrying capacity. An order that wastes renewals sits nearer that floor; a good
order sits above it, and the punishment is graded rather than a collapse.

## The scan, and the economy it selects

18 configurations (production period 4/6/8 × drain 1–6), 72 sampled orders, 300 ticks, 2 seeds:

| | mean sites | spread | noise sd | ratio |
| --- | ---: | ---: | ---: | ---: |
| period 4, drain 1 | 22.31 | 1.50 | 0.09 | 17.6 |
| period 4, drain 2 | 22.31 | 1.50 | 0.09 | 17.6 |
| **period 4, drain 3** | **16.22** | **11.00** | **0.50** | **22.1** |
| period 6, drain 1 | 21.71 | 6.00 | 0.17 | 36.2 |
| period 4/6/8, drain ≥ 4 mostly | 0.8–4.2 | 0.5–3.0 | 0.1–0.3 | 10–52 |

**Chosen economy: production period 4, drain 3.** Self-funded (the organism's own sites produce the
energy), a population floor makes falling behind costly, and the endpoint carries an **11.00-site
spread against 0.50 of noise — ratio 22.1**.

Two things the scan makes visible:

1. **The drain is what creates the graded region.** With drain 1–2 the population saturates at 22.31 and
   the spread is 1.50 — the AC35 failure, reproduced by a different route. At drain 3 the population
   settles at 16.22 and the spread jumps to 11.00. This is the predicted mechanism, measured.
2. **A high ratio alone is not a valid endpoint.** Seventeen of the eighteen configurations exceed the
   ratio-10 criterion, but most of them sit at a mean population of ~1 site — organisms on the edge of
   death, where the "spread" is a few dying individuals rather than a graded maintenance outcome. The
   validity criterion therefore required **both** ratio ≥ 10 **and** a mean in the graded range
   (3 < mean < 20), which excluded them. Requiring only the ratio would have selected a degenerate
   world and produced a confident-looking study about nothing.

## What this does and does not establish

- **Establishes**: a self-funded maintenance world exists in this line that resolves the rule ORDER by a
  factor of 22× the noise — i.e. AC35's obstacle is a design choice (a population-scaled budget with no
  floor), not a property of self-funding as such.
- **Does not establish** anything about an organism: this is an endpoint measurement. No arms were run,
  no protocol exists, no final seed has been spent, and no claim is made.
- **Not autopoiesis, not survival, not life.** The endpoint is sites retained by an organism that pays a
  constant cost to stay alive and produces energy from its own sites. Nothing here speaks to
  self-production in any stronger sense, and nothing about experience or understanding.

## The next step

Protocol for AC37 with the same discipline as AC33/AC36: arm engineering to size the bar (the optima from
a full 720-order sweep on the paired seeds, the arm ranges), a frozen protocol declaring seeds, bar, gate
shape (separation of minima) and the source list for the pre-flight check, then the finals. The claim is
the same one AC33 established for ordering and AC36 for an insufficient income, now with the organism
funding its own maintenance: **releasing and re-searching retains more population than being unable to
overwrite.**

## Artifacts

`ac37_selfsufficient.py`, `test_ac37.py`, `/tmp/ac37_scan.json`. Related: `AC35_ENGINEERING_v1.md` (the
failed self-funded attempt), `AC36_RESULTS_v1.md` (the passing insufficient-income study),
`AC34_ENGINEERING_v1.md` (the rejected binary endpoint).
