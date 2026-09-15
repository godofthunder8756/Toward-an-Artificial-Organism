# AC30: acquisition in the six-region world

2026-09-15. `ac30_acquire.py`, `test_ac30.py` (12 tests), `ac30_acquire_v1.json`. **No
re-acquisition, no protocol, no final seeds, no survival claims, nothing claimed about the
organism.**

## The prerequisite, checked first

AC13 was falsified because its headline saving did not replicate, and the underlying reason was that
the world barely distinguished its arms. So this step asks first whether the world *ranks* orders at
all, before building anything that learns.

The world: six regions of four sites, every site's life ticking down, the environment stressing
regions at different rates plus occasional bursts, one action per tick, and the action is one
region's renewal (the frozen `renew` semantics) at 3 material + 1 energy against a declared income of
1 + 1 per tick.

Measured over all 720 orders (2 seeds × 800 ticks):

| | value |
| --- | ---: |
| best order | `(3,4,1,5,0,2)` = **14.00** sites retained |
| worst order | `(1,0,3,2,5,4)` = **9.00** |
| median | 11.50 |
| **spread** | **5.00 sites of 24 (21% of the population)** |

That is a real ranking with a material margin — the precondition for any acquisition claim.

## Two design errors, both mine, both found by measuring

1. **The first world was degenerate.** Its only action filled *empty* slots, so an urgent site could
   never be saved and every region collapsed: all 720 orders scored exactly **0.00 sites retained**.
   A world that ranks everything identically teaches nothing. Fix: the action renews a *live* site,
   which is the frozen world's actual urgency action (`renew`, actions 3/4 there). Recorded in the
   `tick` docstring.
2. **The second world barely ranked.** Spread was 1.5 sites and the stress-ordered order placed 457th
   — because income exceeded renewal cost, so the organism could renew every tick, and an unaddressed
   urgent site has 16 ticks of life. Two simultaneous urgencies were both comfortably handled and
   priority almost never mattered. Contention is what makes a priority order consequential, so the
   world has to supply it: renewal was raised above income and stress made bursty (a 5% chance per
   tick of hitting three regions at once). Spread went 1.5 → **5.00**.

## A falsified hypothesis

I predicted the best order would prioritise the most-stressed region. **It does not** — that order
scores 11.50 and ranks **318th of 720**. The mechanism is visible in the parameters: `URGENT` is the
same for every region, so the deadline is region-independent and the urgency signal does not encode
*how close to loss* a site is. A fixed order cannot tell a site with 16 ticks left from one with 1,
and the best fixed order is a heuristic over correlated stress phases. Consequence: **the world's
ranking has to be found by evaluation, not derived by reasoning** — which makes it a fair test of a
learner and a poor one for anything that expects an analytical answer.

## Acquisition: real, noisy, and short of the ceiling

Six mutate-and-keep learners, each starting from a random order over 60 single-seed evaluations:

| learner | 2-seed score | gap to best (14.00) | percentile among 720 |
| ---: | ---: | ---: | ---: |
| 0 | 13.50 | 0.50 | **0.3%** |
| 1 | 12.50 | 1.50 | 7.4% |
| 2 | 12.50 | 1.50 | 7.4% |
| 3 | 12.00 | 2.00 | 21.2% |
| 4 | 11.00 | 3.00 | 72.6% |
| 5 | 11.50 | 2.50 | 44.0% |

**Mean gap 1.83 sites against a 5.00 spread — about 63% of the achievable margin captured.** One
learner lands within 0.50 of the best. Every learner beats the stress order on average.

So acquisition works here, but not reliably, and the cause is diagnosable rather than mysterious:
scoring a candidate on a **single seed** is noisy, so the hill-climb stops early on a lucky draw. The
fix is more seeds per evaluation or a population, not more iterations — the current loop is 6
distinct local optima out of 6 starts, which is what premature convergence looks like.

## Retention, and a correction to AC29 §4

The learned order was written into AC29's register and held under damage:

| regime (damage 1e-3/tick, 600 ticks) | intact | behavioural agreement |
| --- | ---: | ---: |
| no damage | 1.000 | 1.000 |
| damage, no repair | 0.833 | 0.833 |
| damage + **one bit repaired per tick** | **1.000** | **1.000** |
| damage + every disagreeing bit repaired | 1.000 | 1.000 |
| damage + an external reference copy (PROTECTED, non-autonomous) | 1.000 | 1.000 |

**AC29 §4 said "holding a multi-bit object against sustained damage needs an external reference or an
error-correcting code, not more replication." That was too strong.** One bit repaired per tick holds
the store *perfectly* at 1e-3 damage, and adding an external reference buys exactly nothing. The
correct statement is a **budget condition**: majority repair suffices whenever the repair rate keeps
pace with the broken-bit rate — and since breaking one bit needs four replica flips, that rate is
much lower than the raw damage rate. A reference (or an ECC) matters only when the budget cannot keep
pace. Ordered outcomes at heavy damage — `no repair ≤ tight repair ≤ full repair ≤ protection` — are
asserted as a test, so the corrected claim cannot silently drift back.

## Not built, plainly

- **No re-acquisition.** The AC16/AC18 question — can the organism re-acquire when the world changes
  so that a *different* order is best — is not asked here at all.
- **No protocol, no final seeds, no claims.** The learner's 60 evaluations per start and the seeds
  used are engineering choices, not a frozen design; nothing here has a pre-registered gate.
- **Not survival-level.** The declared metabolic income keeps the budget from being the binding
  constraint precisely so that the score measures *ordering*; this is not an autopoiesis or viability
  claim and is not offered as one.
- **Nothing about experience, understanding or life.**
- **The two open endpoints:** retention now has a behavioural endpoint on an *acquired* order (an
  advance on AC29, which stored only a written-in one); random-fallback survival remains untouched.

## The next step

Re-acquisition: change the demand regime so the best order changes, and measure whether the organism
re-acquires it — with the gate derived from the claim's own shape, per this line's standing lesson
("cannot hold" → separation of minima; "worse on average" → a justified margin; "better everywhere" →
dominance exempting the ceiling), and a protocol hashed before any final seed.

## Artifacts

`ac30_acquire.py`, `test_ac30.py`, `ac30_acquire_v1.json`. Related: `ac29_register.py`,
`AC29_REGISTER_v1.md`, `AC28_REGIONS_v1.md`, `AC27_SCHEDULE_v1.md`, `AC16_RESULTS_v1.md`.
