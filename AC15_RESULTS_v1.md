# AC15 graded access law: engineering results

2026-09-15. Engineering only. **No final seeds were run.** This is the primitive the
AC11 -> AC13 allocation line was missing, and the first measurement in that line
since AC10 where the intended mechanism is visible in the numbers.

## The primitive

The frozen contact is a hard gate: `if port==mapping[action]` earns the full yield,
otherwise nothing. Every failure in the allocation line had that shape — an entry
whose target has moved earns **exactly zero**, starvation stops the renewal spending,
and the decision is downstream of an economics that already fixed the outcome.

The graded law keeps the gate for a match and, on a miss, takes a declared fraction
of the yield: a quarter. Material channel full 64 / miss 16; fuel channel full 32 /
miss 8. **No conservation law is touched**: `ac4.balance` already carries intake as a
variable (`b.material == M + e['in_m'] - e['overflow_m'] - e['spent_m']`), so a
smaller `in_m` with the overflow term computed the same way satisfies the identity by
construction.

One design decision inside the primitive, and it matters: **productivity is owned by
the contact and defined by the match, not by intake.** In the frozen world the two are
equivalent; in a graded world, deriving productivity from intake would make every
stale route count as productive on every tick, so the relinquishment rule could never
fire. The decision signal has to stay "the target was right".

## Verification: GRADE=0 is byte-for-byte the frozen world

The surgery replaces the frozen gate block and the productivity line. At `GRADE=0` a
miss is exactly the frozen branch (`b.energy-=1; e['active']=1; e['spent_e']+=1`).
Measured against the unmodified AC12 harness, `arm='preserve'`, 512 ticks, seeds 0-2
x both histories:

    GRADE=0 EQUIVALENCE 6/6    final state_hash identical in all six
                               (e.g. 70baa91c7da7 both; inventory 125/109/9 both)

This test earned its keep: the first version failed 0/6 with a 31-unit material
divergence, because the contact primitive had been written to call the `ac4` module
directly instead of the world's shimmed react, silently reinstating the frozen
yields. It is now a closure over the shimmed react. A second bug of the same family —
`build_forced` hardcoding `GRADE=1` — made the first economics table show the graded
column twice; the table below is with the grade actually varied.

## The access law's economics (measured, action forced, 48 ticks)

Yield per contact attempt, seed 0, world pinned to full yields 64/32, inside the
entry's 64-tick life so the stored condition is real:

| stored port | frozen law (GRADE=0) | graded law (GRADE=1) |
| --- | ---: | ---: |
| correct (material) | 64 | 64 |
| stale, kept (material) | **0** | **16** |
| blind, dropped (material) | 26.7 | 36.0 |
| correct (fuel) | 32 | 32 |
| stale, kept (fuel) | **0** | **8** |
| blind, dropped (fuel) | 13.3 | 18.0 |

The blind fallback is a **single coin** (`port=int(coin)`), matching with probability
~1/2, not a uniform draw over a port space — the arithmetic in the first draft of
`ac15.py` assumed four ports and was wrong.

**Result: dropping a stale route improves per-contact yield from 16 to 36 (2.25x) and
keeping it is survivable (16, not 0).** Under the frozen law the same choice is 0
versus 26.7: the organism dies if it keeps the entry, so the decision is forced and
carries no information. Both properties the allocation line needed are now present.

## Full-organism engineering grid (2048 ticks, port move at t=1024, seeds 0-2 x 2)

| arm | frozen law: alive | frozen in_m late | graded: alive | graded in_m late | graded productivity late |
| --- | ---: | ---: | ---: | ---: | ---: |
| `allocate` | 0/6 | 0.0 | 6/6 | 725.3 | 0.294 |
| `preserve` | 0/6 | 0.0 | 6/6 | 1632.0 | 0.000 |
| `relinquish` | **6/6** | 469.3 | 6/6 | 480.0 | 0.560 |
| `random` | 3/6 | 341.3 | 6/6 | 1578.7 | 0.000 |
| `fixed_schedule` | 2/6 | 213.3 | 6/6 | 1584.0 | 0.000 |
| `no_learning` | 0/6 | 0.0 | 6/6 | 1802.7 | 0.000 |

What this shows: **the frozen wall reproduces** — with the hard gate, every arm that
keeps or delays dropping dies with late income exactly zero, and only immediate
relinquishment survives 6/6. **The graded law removes the wall**: every arm survives,
income is no longer zero on a miss, and the arms now differ in productivity and in
retained entries (`preserve` and `random` keep demand [42,0] and have productivity
exactly 0.000; `allocate` ends at [0,0] with 0.294).

What this does **not** show, and I am not claiming: that the dropping arm earns more.
Measured total income is *higher* for the keeping arms (`preserve` 1632 vs `allocate`
725). That comparison is confounded — a stored entry changes the observation, which
changes which actions the program chooses, so the arms differ in how often they
attempt contacts at all, not only in yield per contact. The confound is why the
economics above were measured with the action forced; **the per-contact table is the
valid economic evidence, and the aggregate income column must not be read as one.**

## What this establishes, and what is next

Establishes: a faithful graded-access primitive (GRADE=0 byte-identical to the frozen
world, 6/6); the economics that give the maintenance decision a consequence in which
neither option is fatal (16 vs 36 per contact); and that in the full organism the
three-way pattern of the frozen law (keep -> death, drop -> survival) becomes a
non-fatal difference in retained entries and productivity.

Does not establish: that an acquired allocation policy beats its rivals. That is the
next step and it needs the AC15 protocol written and hashed **before** the first final
seed, with the rivals swept first (AC11's lesson): fixed duty cycles at spending-matched
levels, random, and the sham-write control, plus the two consistency checks that must
reproduce (duty 1/1 and a threshold that can never trigger must both equal `preserve`).

Also open, from the same measurements: `preserve` and the other keeping arms show
productivity exactly 0.000 after the move, i.e. they never re-learn. Whether a policy
can *re-acquire* a correct port rather than merely dropping the stale one is the
stronger version of the claim and is not yet tested.

## Artifacts

`ac15.py` (primitive), the equivalence and economics measurements recorded in this
document, `ac15_engineering_v1/` when the full grid is collected, frozen machinery
`ac12.py`, `ac12_memory.py`, `ac9.py`, `ac4.py`.
