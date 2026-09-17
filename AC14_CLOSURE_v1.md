# AC14 closure v1: the loop is structurally present but arithmetically inert

> **CORRECTION (2026-09-16, supersedes the "inert" conclusion below).** AC67 found a bug in this
> study's `arm_parts`: it matched `'_no_repair' in arm`, but the arm is named `'no_repair'` (no
> leading underscore), so the substring test never matched and the `no_repair` arm ran with repair
> **enabled** — identical to `closed` by construction. The "no observable consequence" identity this
> document reports was therefore an artifact of running the same arm twice, not a property of the
> loop. With the bug fixed and the declared non-self-reversing damage model, the repair loop is
> **load-bearing**: 8/8 survive with repair, 8/8 die with it cut (`AC67_RESULTS_v1.md`). The
> arithmetic below (7-replica majority never flips at 1e-4) remains correct, but it describes the
> *program*, not the *decision state* — the single-replica register read is what the loop maintains.
> The original text follows unchanged.

2026-09-15. Engineering results. **Closure is NOT established**, and the reason is
measured. No final seeds were run. One anomaly is flagged as unexplained rather
than reported as a result.

## The loop, and the link cut

The allocation register (four bits) lives inside `traces[0,:126]`; the program bank
is repaired only by the paid bank-0 repair action; that action's capacity is
`8 * available core interior W`; core W is produced by the action-6 reaction chosen
by the program that contains the register. So maintenance of the decision depends on
the machinery whose maintenance the decision allocates.

AC14 cut the **repair** link, leaving the economy and the observations intact, using
a *frozen* mechanism: `ac4.react`'s existing `arm='no_policy_write'` guard, which
zeroes repair capacity for banks 0 and 1. In this organism bank 1 holds only zeroed
payload, so the guard bites exactly the program bank carrying the register.
Two engineering designs were discarded first, and why is part of the record:

- Blocking core-W *births* is not a clean cut: observation bit 6 never clears, so the
  W rule fires every tick and the organism does nothing else. It dies at 251 with
  activity 0.123 — numerically identical to the AC10 `no_W` arm. That measures
  attention hijack, not the loop.
- Blocking the repair through the removed core-W link is therefore abandoned in
  favour of the frozen guard above.

## Result (6 engineering individuals per arm, 4096 ticks — twice the standard horizon)

| arm | alive | mean activity | program bits whose decoded value differs from installed | rules touched | register flips |
| --- | ---: | ---: | ---: | ---: | ---: |
| `closed` | 6/6 | 1.000 | 0.00 | 0.00 | 0/6 |
| `no_repair` | 6/6 | 1.000 | 0.00 | 0.00 | 0/6 |
| `protected_closed` | 6/6 | 1.000 | 0.00 | 0.00 | 0/6 |
| `protected_no_repair` | 0/6 | 0.211 | 0.00 | 0.00 | 0/6 |

Cutting the repair link has **no observable consequence** in the live-register
organism: identical completion, identical activity, and *identical per-seed action
histograms* (`closed` and `no_repair` choose the same action 4096 times per seed).

## Why — the arithmetic, measured

With the repair blocked for the whole run, the program bank accumulates
**3 differing replicas out of 882** (126 bits x 7 replicas) after 4096 ticks. That
is consistent with the damage rate: 882 x 4096 x 1e-4 ≈ 361 flip *events*, but flips
are XOR, so net differing replicas is small.

The allocation register is read by **majority of seven replicas**, so its decoded
value changes only when **4 of its 7 replicas** differ simultaneously. With ≈0.4
expected flips per replica over the run, that probability is negligible, and no
register bit flipped in any of the 24 register-bits examined (6 individuals x 4
bits) across either regime.

**So the decision state is nominally vulnerable but arithmetically protected by its
own replication.** The loop exists structurally and cannot be exercised by
corruption at this world's damage rate inside any practical horizon. The closure
claim therefore fails as posed — not because the loop is absent, but because the
constraint is never actually at risk.

## What would make the closure test meaningful (quantified)

One of these, each a declared world or format constant, to be fixed before any
closure protocol:

1. **Raise the program-bank damage rate** from 1e-4 to order 1e-3–1e-2 per replica
   per tick (10-100x), so that majority flips occur within a run. The required rate
   is set by the run length and the replication factor, and must be measured, not
   guessed.
2. **Store the decision with less redundancy**: a single unreplicated bit, or three
   replicas (a flip then needs 2 of 3), makes the decision state genuinely at risk
   while leaving the rest of the program at seven replicas. This is a format change
   to the register only, and it is the more faithful option — a constraint that
   cannot be perturbed cannot be shown to be maintained.
3. **A much longer horizon**, which is the same requirement spread over time and
   costs proportionally more runtime for the same result.

## Anomaly, flagged not explained

`protected_no_repair` dies (0/6, deaths 554-1381) with a pathological action
histogram — action 6 (produce W) chosen 3403-3826 times out of 4096 — while
`no_repair` is entirely unaffected. No drops are recorded in any arm, so this is not
a spurious relinquishment; the entries are lost without the decision machinery
asking for it (final occupancy 0 in all six). The only structural difference between
the two arms is that the protected arm's `choose` reads the shadow bank instead of
the body's, which should be equivalent while the body's decoded program is pristine
(0 bits differ). **I have not found the cause, and I am not reporting this as a
result.** The next diagnostic is a first-divergence trace between `no_repair` and
`protected_no_repair` from identical initial states, comparing the observation
vector, the chosen action and the register read at the first differing tick.

## v2: the redundancy fix, and the answer

The v1 requirement was to make the decision state genuinely at risk. Since every
bit in the program bank is stored as seven replicas, "less redundancy" is expressed
as a **declared read convention** rather than a storage change: the register bit
reads as relinquished when at least `REGISTER_THRESHOLD` of its replicas are set,
where 4 is the majority convention and 1 is a single designated replica. Both were
run, on the arms that are comparable without the anomaly (`closed` vs `no_repair`),
6 engineering individuals each, 4096 ticks.

| register read | arm | first damage | final register | occupancy | late contacts | alive |
| --- | --- | ---: | --- | --- | ---: | --- |
| 4 of 7 (majority) | `closed` | never | [0,0,0,0] | 0 / 42 / 21 | 106 / 124 / 120 | 6/6 |
| 4 of 7 (majority) | `no_repair` | never | [0,0,0,0] | 0 / 42 / 21 | 106 / 124 / 120 | 6/6 |
| 1 of 7 (single replica) | `closed` | 77, 798, 216 | [0,0,0,0] | 0 / 42 / 21 | 106 / 124 / 120 | 6/6 |
| 1 of 7 (single replica) | `no_repair` | 77, 798, 216 | [0,0,0,0] | 0 / 42 / 21 | 106 / 124 / 120 | 6/6 |

**The answer is negative, and it is not close.** Under the most damage-favourable
convention the register *does* read wrong — the first damaged read lands at the same
tick with and without the repair loop (77, 798, 216) — and cutting the repair loop
changes nothing: identical final register state, identical occupancy, identical
contact counts, identical survival. The decision state's integrity is not maintained
by the loop that repairs the bank it lives in. Its dominant dynamics are the
organism's own writes and the self-reversing damage stream, not the repair action.

At the majority convention the register never reads wrong at all, in any arm: over
4096 ticks the program bank accumulates 3 differing replicas out of 882, and a
majority-of-seven read needs 4 on one bit.

### Why the damage cannot propagate (measured, and the real obstacle)

*Correction, this supersedes the "empty slots" reading in the first write-up of this
section.* `demand()` counts live cells per region, and one live slot is three bits x
seven replicas = 21 cells. So demand [42,0] means **two live entries in region 0** and
none in region 1: the organism *is* carrying two maintained entries, and they are
governed by register bits `offs[0]` and `offs[1]` — exactly the bits that read wrong.
So there was no absent subject. The reason the wrong read has no consequence is
different and more specific:

**the register is sampled only when the organism chooses a renewal action (3 or 4),
and the damage is transient.** Flips are XOR, so a replica that reads damaged returns
to its original value on the next hit; the first damaged read lands at tick 77 (seeds
0), 798 (seed 1), 216 (seed 2) and does not persist. A wrong decision state therefore
has to coincide with a renewal opportunity to matter at all, and there are few such
coincidences in 4096 ticks — which is why the contact counts are *identical* to the
tick in both arms (106 / 124 / 120), not merely similar.

The requirement is therefore not "more occupied slots" but **persistent corruption of
the register**: a damage process that leaves the bit set, so the next renewal samples
a wrong state rather than a self-reversed one. Concretely, one of:

1. **A higher program-bank damage rate** (order 1e-3–1e-2 rather than 1e-4 per replica
   per tick), so several replicas of the same register bit are set simultaneously and
   the read survives until the next renewal. Note that a *majority* read then also
   becomes reachable, so the threshold convention and the rate have to be chosen
   together and declared before the run.
2. **A non-self-reversing damage model for the program bank** (a flip that stays
   flipped until repaired), which is the faithful way to model a constraint that is
   maintained rather than merely perturbed. This is a world change requiring its own
   protocol, and it is the more interesting option because it is what makes repair
   load-bearing by construction.

The read convention (single designated replica) remains necessary, and is now
implemented as `REGISTER_THRESHOLD` in `ac12.py`.

### Anomaly remains open, with the next diagnostic named

New data, still unexplained: instrumenting the first divergence between `no_repair`
and `protected_no_repair` from identical initial states shows a split at **tick 36**
with equal observations and equal chosen action (9), where the live arm records
`spent_m=4, writes=4` and the protected arm records neither. `_drop` as written
writes all seven replicas at once and requires capacity ≥ n, so a four-replica write
should not occur; the harness does not double-inject the outcome call (verified:
`STEP_SRC` contains zero occurrences of `alloc.outcome` and exactly one occurrence of
the outcome line), and no drops are logged in any arm. The next diagnostic is
mechanical rather than theoretical: instrument `_drop` to log every invocation with
its `place`, `n` and `cap`, which will say immediately whether that write came from
`_drop` at all. Until then the `protected` comparison is not used for any claim in
this document.



## What this does and does not establish

Establishes: the loop is present in the machinery; cutting its repair link is
without consequence at this damage rate; and the precise arithmetic reason — a
7-replica register never reaches a majority flip within a 4096-tick horizon at
1e-4 per replica per tick. Three candidate ways to make the test meaningful are
quantified.

Does not establish: closure of constraints, mutual maintenance, autopoiesis, or
anything about subjective experience. It also does not establish that the loop is
absent or unmaintainable — only that this world does not exercise it.

## Artifacts

`ac14.py`, `ac14_engineering_v1/` (all rows for the frozen-guard design), the frozen
machinery it builds on: `ac12.py`, `ac12_memory.py` (equivalence-verified per-slot
renewal and the dead-rule register). The discarded core-W-supply design's numbers
(activity 0.123, deaths 251-252) are recorded only in this document; that run was
superseded before it was retained.
