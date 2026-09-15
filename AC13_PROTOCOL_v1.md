# AC13 protocol: acquired allocation of maintenance spending under an unreliable port

> **STATUS: UNFROZEN AND FALSIFIED BY REPLICATION — DO NOT RUN AS WRITTEN.**
> The calibration's 41% saving (6 individuals) did not replicate on 12 fresh
> engineering individuals: mean saving −9.3%, range −311% to +99.8%, and
> `preserve` matches the learner on phase-1 productivity and on phase-2 renewal
> writes in 10 of 12. See `AC13_REPLICATION_v1.md`. Retained as the design record
> and as the third measurement of the structural limit: with a single-bit port
> whose blind fallback is uniform over the same candidates, the value of a stored
> route is either fatal or negligible, so the decision has no consequence in
> between. `ac13.py` and `test_ac13.py` remain valid machinery.

2026-09-15. Protocol written before the first final seed. This study is the first
in the AC11→AC13 line whose learner is not beaten by a state-blind rival in
engineering; the world constants and gate magnitudes below come from the
calibration recorded in `AC13_CALIBRATION_v1.md` and the engineering seeds are
excluded from the final sample.

## The claim

> After an unannounced post-development change that makes one acquired route's
> information worthless but not harmful (the affected port answers on a channel
> drawn per contact, so a stored value earns exactly what blind search earns),
> an organism whose per-slot maintenance decision is stored in its own vulnerable,
> repairable program bank and revised by its own realized contact outcomes stops
> paying for that route while remaining viable, whereas a policy that never
> maintains it loses the route's fourfold advantage while the route is still valid,
> and a spending-matched fixed schedule keeps paying without adapting.

Level: functional motivation and partial organismal autonomy. Not subjectivity,
not full autopoiesis, not a new maintenance need.

## Strongest simpler explanations, accepted in advance

1. **Nothing is acquired; the register merely tracks failures.** Conversely: any
   rule built only on the *decay* state of the entry (the frozen urgency rule)
   behaves like `preserve`, because worthlessness is invisible to decay. A rule
   built on *realized outcomes* is what is being tested, and the rivals include a
   spending-matched schedule, a random allocator, a sham-write control with
   identical machinery, and the frozen behaviour itself.
2. **The saving is just spending less.** The sham-write arm spends the same
   attempted cost without writing, so any difference between it and the learner is
   attributable to the write landing in the vulnerable register.
3. **Survival, not organization.** Phase-1 and phase-2 contact productivity are
   reported separately, and the retained entries are reported at the endpoint.
   Activity alone is never the claim.

## Why this world (measured, not assumed)

AC11 (region-granular renewal) and AC12 (per-slot renewal) both failed because the
intervention *zeroed the organism's income*: a readable stale entry makes the
stored port unmatchable, so income is exactly zero and starvation lapses the entry
whether or not the policy chose to. AC13 makes the port **unreliable** instead:
post-intervention the affected channel is drawn per contact, so a stored value
earns 1/PORTS — identical to blind search. Income stays non-zero, the information
becomes worthless without being harmful, and the decision stops being downstream of
starvation.

Calibration (6 engineering individuals per arm, `ac13_calibration_v1/`) fixed the
remaining constants by measurement: the yield before the intervention must be high
enough that the route is needed while valid (at 64 the never-maintain arm completes
0-2/6 with phase-1 productivity 0.277 against 1.000; at 48/32 it survives 2-4/6 and
the question dissolves), and the post-intervention yield must not put the drop's own
payment on a knife edge (at 8 the learner falls to 3/6 while a scripted switch is
6/6, so that regime measures payment timing rather than the value of information).

| Constant | Value | Source |
| --- | --- | --- |
| blind port space | 4 | AC11/AC12 declared world |
| yield, material and fuel, before intervention | 64 | calibration |
| yield, material and fuel, after intervention | 12 | calibration |
| intervention tick | 1024 (development 0-512, phase 1 512-1024, phase 2 1024-2048) | this protocol |
| intervention content | key 1's port answers on a channel drawn per contact | this protocol |
| horizon | 2048 ticks | lineage standard |
| streak threshold | 6 consecutive unproductive contacts for one key | inherited from AC12 |
| fixed-schedule duty | renew both slots every 2nd opportunity | spending-matched rival |
| random allocator probability | 0.5 per slot per opportunity | matched-rate rival |

## Arms

Seven arms, eight individuals each (seeds 1600-1603, both developmental
histories), 56 rows. All arms run the identical world, seeds and observation
streams; only the maintenance decision differs.

| Arm | Decision |
| --- | --- |
| `allocate` | from the vulnerable register, revised by paid writes when a key's unproductive streak reaches 6 |
| `preserve` | frozen behaviour: renew every slot whenever decay urgency fires |
| `relinquish` | never renew (the usefulness-blind static) |
| `fixed_schedule` | renew both slots every 2nd opportunity, state-blind |
| `random` | renew each slot with probability 0.5, state-blind |
| `protected` | the learner's rule with the register held in a protected copy (scaffold) |
| `no_learning` | the learner's machinery with its writes sham-blocked while their costs are paid |

## Endpoints

Per individual and per phase: activity and completion; contact productivity;
renewal writes; retention entries and occupied sites; the register state; the tick
of the first drop; deaths; and the full resource ledger with the frozen material,
energy and fuel identities.

## Prespecified gates

G1 `allocate`: at least 6/8 complete; phase-1 contact productivity at least 0.90;
a drop occurs in at least 7/8, after the intervention; phase-2 renewal writes at
least 25% below `preserve`; phase-2 productivity no more than 0.05 below
`preserve`'s.
G2 `relinquish`: phase-1 contact productivity at most 0.40, and at most 4/8
complete — the route is required while it is valid.
G3 `preserve`: phase-2 renewal writes at least 1.25x `allocate`'s.
G4 `fixed_schedule`: phase-2 renewal writes at least `allocate`'s (a matched
schedule does not adapt and does not save).
G5 `random`: at most 5/8 complete, or phase-2 writes at least `allocate`'s.
G6 `no_learning`: register changed in at most 1/8 while phase-2 renewal writes are
at least 1.10x `allocate`'s — the saving requires the write to land.
G7 `protected`: completes, and is reported as a scaffold outcome only.

Falsification. If `allocate` fails G1, or if any static arm matches it on both
phase-1 productivity and phase-2 renewal writes, the claim fails as stated and
must be reported as a negative result, not reinterpreted. If `relinquish` completes
more than 4/8 the world does not make the route necessary and the study is not
diagnostic; that outcome is reported as a failed design.

## Sample and discipline

Seeds 1600-1603, two histories, eight individuals, seven arms: 56 rows. Disjoint
from every earlier family (AC12/AC11/AC13 calibration and engineering seeds 0-2,
AC10 1300-1303, AC9 1200-1203 / 1100-1103 / 1000-1003, AC8 800-808, AC7 700-708,
AC6 400-431, AC5 200-207, AC4-AC2 0-15, AC1 0-31). No constant, gate or arm
changes after the first final seed. Engineering outputs stay separate.

## What this does not establish

No autonomous need acquisition: the organism reallocates spending on a capability
it already acquired; it does not discover a new metabolic need. `preserve`
survives, so the requirement is **not** survival-level: the supported claim is
behavioural and economic (spending tracks the usefulness of retained information
while viability is preserved, and the usefulness-blind static dies). No full
autopoiesis, no closure of constraints, no intrinsic normativity, no subjectivity.
Per-slot renewal, the allocation register, the streak signal and the interpreter
are supplied machinery; only the decision state is the organism's, and its
vulnerability is inherited from the frozen program bank.

## Recording

`ac13.py` (runner), `test_ac13.py`, `ac13_results_v1/` (frozen),
`audit_ac13.py` (table re-derivation without simulating), `replay_ac13.py`
(sampled exact reruns), `AC13_RESULTS_v1.md`. Earlier freezes and results remain
untouched.
