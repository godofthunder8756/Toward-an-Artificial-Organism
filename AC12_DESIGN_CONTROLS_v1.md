# AC12 design controls v1: the per-slot primitive works, the question still is not posed

2026-09-15. Engineering controls only. **No final seeds were run.** The AC12 claim
is not established and is not claimed. `ac12.py` is retained as an unfrozen
harness. The broader autonomy goal remains active.

## What was built

AC11 failed because the frozen `ac9_memory.renew` renews a whole region while the
usefulness boundary is per key. AC12 supplies the missing granularity and asks the
same question again.

1. **`ac12_memory.renew_alloc(memory, body, region, interior_W, allowed)`** — the
   frozen renewal law restricted to the allowed slots. Two properties were fixed
   by measurement, not assumption:
   - the frozen capacity `min(32, 8*interior_W, energy, material)` is **per
     action**, shared across the slots renewed in that action. A first version
     gave each slot its own budget (42 writes where the frozen law writes 32) and
     was discarded; sharing it is what makes the primitive a restriction of the
     frozen law rather than a cheaper replacement.
   - `renew_region` is `renew_alloc(..., [1, 1])`, and an equivalence test shows
     it reproduces the frozen `ac9_memory.renew` exactly — same writes, same
     bound/waste, same resulting replica state — in 6/6 stressed cases with real
     work performed.
2. **A vulnerable allocation register inside the frozen program.** The frozen
   program contains a permanently dead rule: the bank rule whose mask is 32, which
   `ac9.observe` can never match because it never sets observation bit 5
   (verified: 0 of 12 observed observation values over 1,500 ticks have bit 5
   set). Its mask bits 1-4 are free, and they sit inside `traces[0,:126]` — flipped
   by the same damage stream and repaired only by the same paid bank-0 repair as
   the rest of the program. Four (region, slot) allocation bits live there, zero
   meaning "maintain". Because the bits are zero in the frozen program and setting
   one cannot make the dead rule live, the acquired organism is **byte-identical
   to the frozen one**, and the register is genuinely vulnerable state.
3. **Verification of inertness.** With the register all-maintained and the frozen
   world constants restored (ports 2, yields 64/32, no port move), AC12's
   `preserve` arm reproduces the **frozen AC9 v2 rows exactly** — activity, routes,
   demand, ledger, final inventory and state digest — in 4/4 tested individuals.
   So the per-slot interface changes nothing when every slot is maintained.

## The measurement (6 engineering individuals per arm)

World: blind port space 4, material and fuel yields 16, unannounced relabelling of
key 1's port at tick 1024, 2048 ticks.

| arm | alive | mean activity | phase-1 productivity | phase-2 productivity |
| --- | ---: | ---: | ---: | ---: |
| `preserve` (maintain all) | 1/6 | 0.715 | 1.000 | 0.133 |
| `allocate` (learner) | 1/6 | 0.729 | 1.000 | 0.133 |
| `protected` (scaffold) | 1/6 | 0.729 | 1.000 | 0.133 |
| `no_learning` (paid sham write) | 2/6 | 0.767 | 1.000 | 0.147 |
| `random` (matched rate) | 2/6 | 0.747 | 1.000 | 0.119 |
| `relinquish` (maintain none) | 2/6 | 0.566 | 0.174 | 0.079 |
| **`fixed_schedule` (blind, duty 1/2)** | **4/6** | **0.912** | 1.000 | 0.195 |

The learner's drop is correctly targeted and does occur — the register ends with
exactly the failing key's slot relinquished at tick ≈1041, about 17 ticks after
the move, and the write is paid — yet **`allocate` is indistinguishable from
`preserve`** in aggregate (identical phase-1 and phase-2 productivity, same death
window), and a state-blind fixed duty cycle survives four times as often.

## Why allocation is not the deciding factor here (measured)

The per-individual phase-2 breakdown explains it. After the relabelling, an
organism whose stale entry is still readable has **material income exactly zero**,
because the stored port never matches the moved port. Material starvation then
does the policy's work for it:

| arm | individual | phase-2 contacts | productive | phase-2 renewal writes | phase-2 material spent | died |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `preserve` | seed1/0 | 38 | 2 | **3** | 15 | 1272 |
| `preserve` | seed2/0 | 60 | 2 | **0** | 4 | 1277 |
| `preserve` | seed0/0 | 301 | 89 | 443 | 1164 | – |
| `allocate` | seed1/1 | 106 | 18 | 1 | 210 | 1627 |
| `fixed_schedule` | seed2/0 | 230 | 42 | 0 | 490 | – |

With no material income the organism cannot pay for renewal at all: renewal writes
in phase 2 collapse to 0-3 replicas in most individuals and the entry lapses by
starvation whether or not the policy chose to relinquish it. `seed0/0` is the
exception that proves the rule — there the key-1 entry had never been deposited
(only 2 deposits occurred), so no stale route existed, blind access at 1/4 already
provided income, and both `preserve` and the learner survived on it.

So the obstacle is not the learner, and not (as I first suspected) that
maintenance is merely break-even: measured against the frozen economy the route is
worth several times its cost. The obstacle is that **this intervention drives
income to zero, which forces the entry to lapse regardless of policy**, leaving
the allocation decision downstream of an economics that has already decided the
outcome.

## What would make the question well posed

1. **An intervention that does not zero income.** The stale entry must keep
   costing the organism while some income continues, so that "keep paying" and
   "stop paying" are both affordable options whose consequences differ. Relabelling
   the port of a resource the organism can also obtain another way, or damaging a
   route rather than invalidating it (partial wrongness, so the stored value is
   sometimes right), are the natural candidates.
2. **A maintained-route cost large enough to matter while income continues**, and
   a world where the blind fallback's rate is high enough to fund the reduced
   metabolism but low enough that the route is still worth keeping. AC11 measured
   the two requirements pulling in opposite directions across regimes; AC12
   shows that even with per-slot granularity the chosen intervention collapses the
   trade-off before the decision can matter.
3. **Rivals at the same granularity** (a spending-matched per-slot schedule and a
   random per-slot allocator) — already implemented, and they remain the correct
   rivals once the world is fixed.
4. The AC11 requirements that are unaffected: no protected copy, no externally
   fixed correct state, and the decision in vulnerable paid state.

## What this establishes

- A working, equivalence-verified per-slot renewal primitive, with the frozen
  per-action capacity preserved (the first attempt was wrong by 10 writes per
  action and was caught by the equivalence test).
- A way to hold vulnerable allocation state inside the frozen program without
  changing the program, the economy, or the organism: the dead-rule register,
  whose inertness is proved by reproducing the frozen rows exactly.
- A measured negative result: with per-slot granularity alone, the allocation
  question is still not posed, because the intervention zeroes income and
  starvation decides the outcome. A state-blind fixed duty cycle survives 4/6
  where the learner survives 1/6.

Does not establish: any acquired allocation, any new maintenance need, any
autopoiesis, and nothing whatever about consciousness.

## Artifacts

`ac12_memory.py` (the primitive), `ac12.py` (harness, no final seeds),
`ac12_engineering_v2/` (the grid above; the earlier draft's outputs were discarded
as superseded when the program-format approach was abandoned), `ac11_*` (the prior
line's evidence), `AC11_DESIGN_CONTROLS_v2.md` (the granularity finding this
answers).
