# AC33 PROTOCOL v1 — re-acquisition with a steepest-ascent search

STATUS: **frozen before the first final seed.** Written 2026-09-15 after the landscape engineering in
`ac33_search.py`. Final seeds are declared below and are disjoint from every seed used in AC29–AC32 and
from this study's engineering starts (0–23).

SOURCES (declared): ac33_reacquire.py ac33_search.py ac32_reacquire.py ac30_acquire.py ac29_register.py AC33_PROTOCOL_v1.md

## Claim (unchanged from AC32)

After the environment's stress regime changes so that **a different order is best**, an organism that
can both **release** its stored order and **search again** ends up performing at the level the new
regime permits; an organism structurally unable to release its stored order does not.

Gate shape: **separation of minima** — the claim's own form ("cannot hold"), as established by this
line's AC16/AC17/AC18 sequence.

## What changed, and why that is legitimate

AC32 is **falsified as written** and remains so. Its G2 failed because one individual's search settled
at 11.75 while its peers reached 12.33–12.42. The diagnosis was mechanistic: mutate-and-keep accepting
**random single swaps** with 40 evaluations per restart stops as soon as no random neighbour happens to
improve.

This study changes the **mechanism**, and nothing else:

| | AC32 | AC33 |
| --- | --- | --- |
| search | random single-swap moves, greedy accept, 40 evals/restart | **steepest ascent**: evaluate all 15 swaps, move to the best, repeat |
| cost | ~160 rating calls per acquisition | **~36** |
| mechanism justified by | — | the landscape measurement below |

**The bar is not moved** (12.00, unchanged), the claim is not weakened, the arms, regimes, endpoint,
scoring seeds and gate shape are identical, and the final seeds are fresh. Fixing an identified
mechanism and re-declaring is not the same thing as adjusting a threshold to fit a result; AC16's rule
("do not re-run with a better-chosen threshold") is respected, and **this protocol may not be edited
after the first final seed**.

## Mechanism engineering, measured before this protocol was written

`ac33_search.py`, 24 random starts, paired scoring (so the rating is a deterministic function of the
order and steepest ascent is well defined):

| neighbourhood | min local optimum | mean | max | within 0.34 of ceiling |
| --- | ---: | ---: | ---: | ---: |
| swaps only | **12.33** | 12.62 | 12.67 | 24/24 |
| swaps + insertions + reversals | **12.33** | 12.65 | 12.67 | 24/24 |

Two conclusions, both used here:

1. The landscape is not the obstacle — the weaker **mechanism** was. Steepest ascent reaches within
   0.34 of the 12.67 ceiling from every start, in ~2.4 steps, and is *cheaper* than AC32's search.
2. A richer neighbourhood buys almost nothing (mean 12.62 → 12.65), so swaps suffice and the
   mechanism is kept as simple as it can be.

Six distinct local optima exist under swaps and the **worst is 12.33** — above the bar, which is why
the "every individual" requirement is now achievable.

## Validity criterion (unchanged)

Margin/noise ≥ 10. Measured in AC32: margin 2.00, per-order scoring noise sd 0.12 → **16.15**. Reused
here because nothing about the world changed.

## Regimes and arms

Regimes differ only in the stress-rate vector (A = `acq.stress_rates()` descending, B = its reverse);
ticks 800; paired scoring on the fixed seed set **9000–9011**.

| arm | what it does |
| --- | --- |
| `learner_both` | steepest-ascent search under A, stores; under B **releases** (overwrites) and searches again |
| `no_release` | searches under A, stores; under B it **cannot overwrite**, so it stays |
| `no_search` | never searches; acts on its initial order |
| `preserve` | state-blind control: keeps its initial order |
| `oracle_a` | SCAFFOLD, non-autonomous: holds the *old* regime's optimum |
| `oracle_b` | SCAFFOLD, non-autonomous: holds the *new* regime's optimum — the ceiling |

The register is the store of record (written and read back). **No damage** is applied: the register's
integrity question belongs to AC29/AC30.

## Endpoint

Sites retained under regime **B**, averaged over the paired scoring seeds 9000–9011, per individual.

## Pre-declared gate

BAR = **12.00 sites** — unchanged from AC32, where it was derived from engineering as a point inside
the observed gap (structurally incapable arms top out at 11.08 over two independent engineering
rounds; the capable mechanism's worst local optimum is 12.33).

| id | gate |
| --- | --- |
| G1 | `oracle_b` ≥ BAR — the bar is reachable |
| G2 | `learner_both` **worst** ≥ BAR — the capable arm reliably re-acquires |
| G3 | `no_release` **best** < BAR |
| G4 | `oracle_a` best < BAR |
| G5 | `no_search` and `preserve` **means** < BAR |
| G6 | all arms complete |
| G7 | determinism: re-running the declared seeds reproduces the rows exactly |
| G8 | the register is in the loop, every held order reads back |

As in AC32, G5 is stated on the **mean**, because a single random order can be as good as a searched
one in this world (AC30: a random order achieves ≈88% of optimal; in AC32 finals one state-blind
individual reached 12.42). No separation-of-minima claim is made for the state-blind arms.

## Anti-drift rules

- Final seeds **3400–3411** (12 individuals), disjoint from AC29–AC32 and from AC33's engineering
  starts.
- The runner creates `ac33_results_v1/` with `mkdir(exist_ok=False)`.
- **Pre-flight (AC32's process lesson, enforced in code):** the runner parses the `SOURCES (declared):`
  line above and asserts it equals the set of files it hashes, **before** the first final seed. AC32
  declared five sources and hashed four; this check makes that failure impossible to repeat silently.
- `test_ac33.py`, `audit_ac33.py`, `replay_ac33.py` are **not** hashed (AC17's lesson).
- If a gate fails, it fails. No threshold moves; this study is not re-run with a better bar.

## Source hashes (computed before the first final seed)

    4ea41f8d2210a1b58ec48de4ea2f1a0298f59f25229294d612add11c58dd8dc0  ac33_reacquire.py
    83dd235a0ba83afcf099e715f67921294491d0d8d54d8c7c429f49cca3bdade5  ac33_search.py
    08a58141df3d0c525c43025b98993e0e28c42096484f1f457747b93910e1ffdd  ac32_reacquire.py
    5a68e0b1cda5bf87002d2ec029f7a6bdf6a122b431f404ba538f8a6379bd041d  ac30_acquire.py
    f01d4ed784835eb4c5791116344d8cd1f87ebda7ffb5a09fd6cd53d4752e850c  ac29_register.py
