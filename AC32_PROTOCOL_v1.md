# AC32 PROTOCOL v1 — re-acquisition, re-engineered (paired scoring)

STATUS: **frozen before the first final seed.** Written 2026-09-15 after engineering on seeds 0–5.
Final seeds are declared below and are disjoint from every engineering seed used in this study.

## Claim

After the environment's stress regime changes so that a **different order** is best, an organism that
can both **release** its stored order and **search again** ends up performing at the level the new
regime permits; an organism that is structurally unable to release its stored order does not.

Gate shape: **separation of minima**. The claim is of the "cannot hold" form, and this line's standing
lesson (AC16 falsified by 0.006 on a margin gate; AC17's "better in every individual" unsatisfiable;
AC18 passing on separation of minima) is that the gate must be derived from the claim's own shape.

## Why this supersedes AC31

AC31's design was falsified in its own engineering (see `AC31_ENGINEERING_v1.md`): the capable arm
(mean 11.83) came out below `no_search` (12.00) and `oracle_b` (12.33) against a 2.67-site margin. The
diagnosis was a **measurement** failure, not a mechanism failure, and it was fixed here before any arm
was re-run:

| change | before (AC31) | after (AC32) |
| --- | --- | --- |
| arm comparison | unpaired: each arm scored on its own seeds | **paired**: one scoring set shared by all arms |
| scoring seeds | 3 per individual | **12 fixed seeds (9000–9011)** |
| search | 80 evals × 3 seeds, single run | **4 restarts × 40 evals × 5 seeds**, best kept |
| noise measured | not measured | **measured: sd 0.12 over 8 disjoint seed sets** |

The design fix is justified by AC30's diagnosis (single-seed scoring makes the hill-climb stop on a
lucky draw → premature convergence) and by AC31's diagnosis (unpaired comparison), **not** by whether
the arms separate.

## Validity criterion, declared and met before the arms were run

| quantity | value |
| --- | ---: |
| regime B optimum | `(2,0,1,3,5,4)` = 12.67 |
| old optimum rated under B | 10.67 |
| **margin** | **2.00 sites** |
| per-order scoring noise (8 disjoint seed sets) | **sd 0.12** |
| **margin / noise** | **16.15** |

The criterion is margin/noise ≥ 10. It is **16.15**. The world was **not retuned** to achieve this —
only the measurement was fixed.

## Regimes and arms

Regimes differ only in the stress-rate vector: A is `acq.stress_rates()` in descending order, B is its
reverse. Ticks per run: 800 (as in AC30/AC31).

| arm | what it does |
| --- | --- |
| `learner_both` | searches under A, stores; under B it **releases** (overwrites) and searches again |
| `no_release` | searches under A, stores; under B it **cannot overwrite**, so it stays |
| `no_search` | never searches; acts on its initial order |
| `preserve` | state-blind control: keeps its initial order |
| `oracle_a` | SCAFFOLD, non-autonomous: holds the *old* regime's optimum |
| `oracle_b` | SCAFFOLD, non-autonomous: holds the *new* regime's optimum — the ceiling |

The order of record lives in AC29's register (written and read back). **No damage is applied**: the
register's integrity question belongs to AC29/AC30, and mixing it in would confound re-acquisition
with retention.

## Endpoint

Sites retained under regime **B**, averaged over the shared scoring seeds 9000–9011. Per-individual
values are recorded, not only means.

## Pre-declared gate

BAR = **12.00 sites**, derived from engineering as a point in the middle of the observed gap (the
structurally incapable arms top out at 11.08; the capable arm bottoms at 12.33), not chosen from the
final results. The gate is evaluated on the declared final seeds only.

| id | gate |
| --- | --- |
| G1 | `oracle_b` (scaffold ceiling) ≥ BAR — the bar is reachable |
| G2 | `learner_both`'s **worst** individual ≥ BAR — the capable arm reliably re-acquires |
| G3 | `no_release`'s **best** individual < BAR — structural inability to release is decisive |
| G4 | `oracle_a`'s best individual < BAR — holding the old optimum is not enough |
| G5 | `no_search` and `preserve` **means** < BAR — not searching is not reliably good |
| G6 | all arms complete: every individual yields a score for every arm |
| G7 | determinism: re-running the declared seeds reproduces the rows exactly |
| G8 | the register is in the loop: every held order reads back non-None |

**Recorded in advance, not hidden:** in engineering, individual `no_search`/`preserve` runs (random
orders) reached up to 12.17, i.e. a single random order *can* exceed BAR. G5 is therefore stated on
the **mean**, and a separation-of-minima reading of those arms is **not** claimed. This is a fact about
the world (a random order achieves ≈88% of optimal, measured in AC30), not a defect of the study, and
it is why the "cannot hold" claim is made against `no_release` and `oracle_a`, which are structurally
incapable, rather than against a state-blind control.

## Anti-drift rules for this study

- Final seeds are **3300–3311** (12 individuals), disjoint from engineering seeds 0–5 and from every
  seed used in AC29–AC31.
- The runner creates `ac32_results_v1/` with `mkdir(exist_ok=False)`; it can never be overwritten.
- A pre-run snapshot of source hashes is written **before** the first row: `ac32_reacquire.py`,
  `ac30_acquire.py`, `ac29_register.py`, `ac27_schedule.py`, `AC32_PROTOCOL_v1.md`.
- `test_ac32.py`, `audit_ac32.py` and `replay_ac32.py` are **deliberately NOT hashed** — editing a
  verification tool must not create a self-inflicted drift (AC17's lesson).
- If a gate fails, it fails. **No threshold is moved**, and this study is not re-run with a
  better-chosen bar.

## Source hashes (computed before the first final seed)

    7a683a6ae3f17d05250680bbab63e908844d5c1799bf99c7ea61aeb763e2a266  ac32_reacquire.py
    5a68e0b1cda5bf87002d2ec029f7a6bdf6a122b431f404ba538f8a6379bd041d  ac30_acquire.py
    f01d4ed784835eb4c5791116344d8cd1f87ebda7ffb5a09fd6cd53d4752e850c  ac29_register.py
    402ae74b6c60943dbe982048b502e531d9ef111b350c97e44d977e68addc1896  ac27_schedule.py
