# AC36 PROTOCOL v1 — graded maintenance under an insufficient income

STATUS: **frozen before the first final seed.** Written 2026-09-15 after the prerequisite and arm
engineering. Final seeds are declared below and are disjoint from every seed used in AC29–AC35.

SOURCES (declared): ac36_survival.py ac33_search.py ac32_reacquire.py ac30_acquire.py ac29_register.py AC36_PROTOCOL_v1.md

## Claim

After the environment's stress regime changes so that **a different order is best**, an organism that can
both **release** its stored order and **search again** retains more population than one structurally
unable to overwrite its stored order.

Gate shape: **separation of minima** — the "cannot hold" form, as in AC18/AC32/AC33.

This is a **maintenance** claim, not AC33's ordering claim. AC33's world declared an income generous
enough that the budget never bound, so its endpoint measured pure ordering quality. Here the income is
deliberately **insufficient**: energy arrives at a fixed rate independent of the organism's state
(1/tick) and one renewal costs five ticks of it, so the organism can never maintain everything and must
spend what it has on ONE region per renewal. The endpoint is **population retained at the end of the
run** — graded, and paid for out of a budget that cannot cover the demand.

## Why not the two alternatives, recorded so the choice is auditable

| world | measured outcome |
| --- | --- |
| AC30: generous declared income | spread across orders 5.00 sites of 24, but the endpoint measures ordering, not maintenance |
| AC35: production-funded (organism's own sites produce energy) | **spread 1.00 site against 0.30 of noise → prerequisite FAILED**; production scales with the living population and that negative feedback equalizes every order toward carrying capacity |
| **AC36: insufficient fixed income** | **spread 2.17 sites, noise sd 0.11 → margin/noise 16.6** |

## Prerequisite, measured before this protocol

Declared criterion: margin/noise ≥ 10, where margin is the difference between the regime's optimum and
the previous regime's optimum rated under it.

| quantity | value |
| --- | ---: |
| regime B optimum (full 720-order sweep, paired seeds) | `(1,0,2,3,4,5)` = **6.83** |
| regime A optimum rated under B | **5.00** |
| **margin** | **1.83** |
| per-order noise, 8 disjoint seed sets | **sd 0.11** (6.22–6.58) |
| **margin / noise** | **16.6** → criterion met |
| spread across all 720 orders under B | 2.17 (median 5.75, worst 4.67) |
| refusals (wanted to renew, could not afford it) per 600-tick run | ≈ **119** |

The refusals are the point: insufficiency bites on roughly one tick in five.

Optima were taken from a **full 720-order sweep on the paired scoring seeds**, not a sample: a smaller
seed set selects a different order (the learner's engineering value, 6.67, exceeded the 3-seed
"optimum" of 6.50), which is selection noise, and the protocol must not inherit it.

## Regimes, arms, endpoint

Regimes differ only in the stress-rate vector: A = `acq.stress_rates()` × 3, B = its reverse. Bursts
hit three regions at once with probability 0.03/tick. Ticks 600. Paired scoring on the fixed seed set
**9000–9011**.

| arm | what it does |
| --- | --- |
| `learner_both` | steepest-ascent search under A, stores; under B **releases** (overwrites) and searches again |
| `no_release` | searches under A, stores; under B it **cannot overwrite**, so it stays |
| `no_search` | never searches; acts on its initial order |
| `preserve` | state-blind control: keeps its initial order |
| `oracle_a` | SCAFFOLD, non-autonomous: holds the *old* regime's optimum |
| `oracle_b` | SCAFFOLD, non-autonomous: holds the *new* regime's optimum |

The register is the store of record (written and read back). **No damage** is applied.

## Pre-declared gate

BAR = **6.45 sites**, derived from engineering as a point inside the observed gap: the structurally
incapable arms top out at 5.67 (`no_release`), 5.17 (`oracle_a`), and the state-blind arms at 6.25
(`no_search`/`preserve` max, mean 5.98), while the capable arm bottoms at 6.67.

| id | gate |
| --- | --- |
| G1 | `oracle_b` ≥ BAR |
| G2 | `learner_both` **worst** ≥ BAR |
| G3 | `no_release` **best** < BAR |
| G4 | `oracle_a` best < BAR |
| G5 | `no_search` and `preserve` **means** < BAR |
| G6 | all arms complete |
| G7 | determinism: re-running the declared seeds reproduces the rows exactly |
| G8 | the register is in the loop, every held order reads back |

As in AC32/AC33, G5 is on the **mean**: a single random order can be good in this world (state-blind
individuals reached 6.25 in engineering, against a bar of 6.45), so no separation-of-minima claim is
made for the state-blind arms.

## Anti-drift rules

- Final seeds **3500–3511** (12 individuals), disjoint from every earlier study and from all
  engineering seeds.
- The runner creates `ac36_results_v1/` with `mkdir(exist_ok=False)`.
- **Pre-flight enforced in code:** the runner parses the `SOURCES (declared):` line above and asserts it
  equals the set it hashes, before the first final seed.
- `test_ac36.py`, `audit_ac36.py`, `replay_ac36.py` are **not** hashed.
- If a gate fails, it fails. No threshold moves; this study is not re-run with a better bar.

## Source hashes (computed before the first final seed)

    a583abc9c7db6cdf73f2bacada35873c7c18da33ee0e8fa42038e9fdb8dd7c72  ac36_survival.py
    83dd235a0ba83afcf099e715f67921294491d0d8d54d8c7c429f49cca3bdade5  ac33_search.py
    08a58141df3d0c525c43025b98993e0e28c42096484f1f457747b93910e1ffdd  ac32_reacquire.py
    5a68e0b1cda5bf87002d2ec029f7a6bdf6a122b431f404ba538f8a6379bd041d  ac30_acquire.py
    f01d4ed784835eb4c5791116344d8cd1f87ebda7ffb5a09fd6cd53d4752e850c  ac29_register.py
