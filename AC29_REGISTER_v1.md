# AC29: storing a six-position order — the register, and how its integrity scales

2026-09-15. `ac29_register.py`, `test_ac29.py` (14 tests), `ac29_register_v1.json`. **No acquisition,
no external reference, no error-correcting code, no re-acquisition, no protocol, no final seeds,
nothing claimed about the organism.**

## The question

AC14 asked whether the frozen organism's own decision state is a maintained constraint, and found it
"structurally present but arithmetically inert": 7-fold replication, self-reversing XOR damage, and a
4-of-7 read meant a single flip could never change what the organism read. Integrity was never at
risk.

AC28's world stores a *six-position order* — 720 values, 9.49 bits. That is a different object from a
one-bit route, so: does per-bit replication of 7 preserve a multi-bit object the way it preserved a
one-bit one? Four answers, each quantified.

## 1. The coding weakness

10 bits hold 1024 values; **only 720 are orders (70.3%)**. Damage therefore does not merely reorder
the rule positions — it can leave the space of orders entirely:

| tick (damage 1e-4/replica) | P(order intact) | P(code is any valid order) | behavioural agreement |
| --- | ---: | ---: | ---: |
| 100 | 1.0000 | 1.0000 | **1.0000** |
| 1000 | 0.9984 | 1.0000 | 0.9997 |
| 5000 | 0.7260 | 0.9990 | 0.9532 |
| 20000 | **0.0125** | **0.8574** | **0.6110** |

At 20,000 ticks the register holds its original order 1.25% of the time, holds *some* order 85.7% of
the time, and answers 61.1% of demand words as the target would. Three different numbers for what
"retained" might mean — which is the point of the next finding.

## 2. The weakest link is blunted, not absent

Exact, from the closed form (a replica overwritten at rate `r` still holds its original value at tick
`t` with probability `(1+(1-r)^t)/2`; a bit's majority is wrong iff ≥4 of 7 replicas differ, a
binomial tail):

| object | 1% chance of an error by tick | ratio |
| --- | ---: | ---: |
| 1 bit (the frozen route) | 3349 | — |
| 10 bits (the order) | 1667 | **2.01×** |

The naive weakest-link expectation is 10×. It is 2.01×, because a majority-of-7 failure is a
**fourth-power process in time** — the time to break scales as `k^{-1/4}`, i.e. 1.78× for 10 bits,
which brackets the measured 2.01. So widening the stored object is much cheaper than "k chances to
break" suggests, and the reason is the redundancy's own arithmetic rather than anything about the
world.

A methodological note worth keeping: a "half-chance of error" metric would have reported 55×, because
a 1-bit object's error probability **saturates at 0.5** (a fully randomised replica set is right half
the time by symmetry). 0.5 is that object's *maximum*, not a comparable point on the curve. The
threshold must be fixed in probability space, not at 0.5.

## 3. Behaviour decays far more slowly than bits

The AC14 lesson, now quantified: at 20,000 ticks the bit pattern is intact 1.25% of the time while
**behavioural agreement is still 61.1%**. A corrupted order frequently answers a given demand word
exactly as the target would, because only the relative order of the *urgent pair in that word*
matters. Any retention claim must therefore be behavioural; bit-level intactness is a poor proxy and
this table is the measurement that shows it.

## 4. Majority-write repair is error-preserving, not error-correcting

Repair writes the majority back for disagreeing bits — the frozen `write`. That restores light damage
(verified) but **freezes a flipped majority wrong**: after heavy damage, every bit is unanimous and
the store still does not hold the original order (verified as a test, `test_repair_cannot_correct_a_
flipped_majority`). Holding a multi-bit object against sustained damage needs an **external
reference** or an **error-correcting code** — not more replication.

This is also the mechanism behind a design choice made long before it: the frozen world's `protected`
arm had to keep its own copy of the correct value. Protection was never a convenience; majority
repair cannot recover a lost majority, so a reference is *required*.

Repair does scale usefully in the regime that matters: **one repair per tick holds both intactness
and behavioural agreement at 1.000 even at damage 1e-3**, because the broken-*bit* rate is far below
the replica-flip rate — four flips are needed to break one bit.

## My own errors in this module, recorded

Three harness bugs, all caught by cheap checks rather than by reasoning:

1. `unlehmer` did not invert `lehmer`, so an intact register scored 0.318 agreement instead of 1.0.
   Caught by a round-trip check over all 720 permutations.
2. The fix conflated *digit extraction* order (least-significant first) with *application* order (left
   to right) and popped chosen items too early. Caught by the same round-trip check.
3. The "half-chance" weakest-link metric compared a saturation point with a threshold — see §2.

This is the fourth consecutive step in this sequence where the unreliable component was my own
verification code rather than the science, and the pattern of the fix is always the same: an
exhaustive or closed-form check, not more care in writing.

## Not built, plainly

- **No acquisition.** The register can *hold* an order that is written into it; nothing here finds
  one. No scoring against demand, no search, no learning, no write process driven by the organism.
- **No reference, no error-correcting code, no re-acquisition.**
- **No protocol and no final seeds**, and no claims. The numbers are properties of a damage model.
- **Nothing about experience, understanding or life**, and nothing offered as evidence toward them.
- **The two open endpoints:** *retention* now has a measured behavioural endpoint (§3) but only against
  a written-in order, not an acquired one; *random-fallback survival* remains untouched.

## The next step

Acquisition: score orders against the AC27 demand schedule (which defines "correct" from the world,
not from us), and build a process that finds and writes one — with the reference question from §4
answered explicitly, since majority repair cannot hold a multi-bit object by itself. Then the two
endpoints, stated separately, in a protocol hashed before any final seed.

## Artifacts

`ac29_register.py`, `test_ac29.py`, `ac29_register_v1.json`. Related: `AC28_REGIONS_v1.md`,
`ac27_schedule.py`, `AC14_CLOSURE_v1.md`, `ac19.py`, `AC24_FUNCTIONAL_v1.md`.
