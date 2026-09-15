# AC11 protocol: acquired allocation of preservation spending under a post-development change

2026-09-15. Design and protocol. **No final seeds have been run.** Implementation
and engineering seeds follow review of this document, in that order, per the
project's Phase E. This does not amend or reinterpret AC10, the frozen AC9
lineage, or the stopped E3 v0.11 experiment, and makes no autopoiesis, new-need
or novelty claim.

## The claim

Falsifiable sentence:

> A single bounded organism whose decision to keep paying for an acquired access
> capability is stored in the same vulnerable, repairable trace bank as that
> capability, and is revised by its own realized contact outcomes, preserves the
> capability while its route is valid and relinquishes it after an unannounced
> post-development port move — remaining viable across both phases — whereas
> allocation decided by decay urgency, by a spending-matched fixed schedule, or
> at random fails at least one phase.

Tested level: functional motivation plus partial organismal autonomy (the
maintenance decision is made from, and stored in, the vulnerable organization).
Not subjectivity.

## Strongest simpler explanations, accepted in advance

1. **No learning is needed.** Any policy that simply spends less, or that stops
   renewing after contacts fail for a fixed number of ticks, may match the
   adaptive arm. The rivals below include exactly that family, and the adaptive
   arm must beat them on the declared endpoints, not merely equal them.
2. **The world was chosen to favour the adaptive arm.** True in the sense that
   the world constants were fixed by engineering feasibility before this
   protocol; disclosed in the engineering record below. Calibration cannot
   favour the learner *over its rivals* because every arm runs in the same world
   with the same seeds, observation stream and draws.
3. **Survival is not organization.** An organism can keep acting by blind
   sampling after losing its capability. Every arm therefore reports retained
   entries and per-phase contact productivity alongside viability, and activity
   alone is never the claim.

## Why a new world is required (measured, not assumed)

The frozen AC9 economy makes "relinquish" nearly free and therefore vacuous:

- From the frozen AC9 controls v3 keep rows, memory renewal is **1,723.6 writes,
  ≈ 54% of all material spending** (3,186.5) and ≈ 1,723 energy of 4,858.5 spent
  — while the preserved route buys only ~68 contact attempts in 2,048 ticks.
  Maintenance cost exceeds its payoff by roughly 25×.
- Measured in the frozen world (`ac11_feasibility_v1/`): with a valid route,
  preserving and relinquishing both complete the horizon (1.000 activity); after
  an unannounced port move, preserving is fatal (deaths at 756 and 761) but
  relinquishing survives. Since relinquishing also removes that 54% cost, a
  static "never preserve" policy is not reliably worse — so no allocation
  decision is being forced, and a study run here would report a vacuous pass.

The candidate regime therefore changes supplied world constants only (no frozen
`ac9.step`, `ac4.react`, `ac5_program` or `ac9_memory` law is edited):

| Constant | Frozen | AC11 | Rationale |
| --- | --- | --- | --- |
| Blind port space | 2 | **4** | A blind attempt is drawn uniformly from four access channels, of which one is live per resource. An acquired entry stores one bit (the frozen `deposit` law accepts only 0/1 values) and identifies the live channel exactly. Blind search therefore succeeds 1/4 of the time, so a correct entry is worth 4× a blind attempt — this is what makes preserving it worth its measured cost. |
| Material yield per productive contact | 64 | **16** | With the frozen yield the organism is material-saturated and its resource demand is maintenance-driven. At 16, meeting maintenance from a 1/4-success search is not viable (measured), so the maintained route is required while it is valid. |
| Fuel yield per productive contact | 32 | **16** | Same, for the fuel side. Energy is not the binding resource; this keeps both sides comparable. |
| Ceilings, prices, lifetimes, damage rates | — | unchanged | All frozen. |

Measured in this regime (6 engineering seeds, `ac11_feasibility_v2/`):

| policy | phase 2 | alive/6 | mean activity | deaths | productivity phase 1 / 2 |
| --- | --- | ---: | ---: | --- | ---: |
| preserve | route valid | 6/6 | 1.000 | – | 0.981 / 1.000 |
| preserve | route stale | 2/6 | 0.577 | 735–757 | 0.450 / 0.105 |
| relinquish | route valid | 2/6 | 0.559 | 512–890 | 0.445 / 0.316 |
| relinquish | route stale | 3/6 | 0.655 | 512–760 | 0.417 / 0.236 |

Each static policy therefore fails one phase, and the two failures are
structural (blind search cannot fund maintenance; a stale deterministic route
yields nothing). Only a policy that preserves while valid and relinquishes when
stale can be viable throughout.

## Causal and information inventory

- Acquired during life: the two route entries (key, value, validity; seven
  replicas per bit), deposited only by paid deposition after a productive
  contact, in the region selected by developmental sensory input.
- What sustains them: regional interior W gates every replacement write
  (`min(32, 8*interior_W, energy, material)`); energy comes only from
  C-catalysed conversion; material is collected and spent on writes, particles
  and boundary.
- What the new decision is: whether to keep paying those writes. Its state is the
  enabled bit of the rule that produces the region's renewal action, i.e. bits
  inside `traces[0,:126]` — the same bank whose contents the organism's other
  decisions are read from, subject to the same flips and the same paid repair.
  There is no protected copy in the adaptive arm.
- Learning signal: the organism's own realized contact outcomes (productive or
  unproductive) on the affected key, counted in a declared streak register whose
  replicas live in the same vulnerable trace bank and are paid for like any other
  write. No experimenter target, no reward, no correct-action signal, and the
  environment's mapping is never readable as state.
- Protected, generic machinery (supplied, unchanged): interpreter, majority
  decoding, addressing, reaction recipes and prices, geometry, transport,
  observation encoder, random streams.
- Interventions touch only: whether the preservation reaction/write happens, and
  the world constants above. Nothing else.

## Arms

Final sample individuals: 8 (four seeds × two developmental histories). All arms
run the same 2,048 ticks with the unannounced port move at onset 512, and rows
are paired within seed and history.

| Arm | Preservation decision |
| --- | --- |
| `adaptive` | Stored in the vulnerable program bank; revised by paid writes from the organism's own unproductive-contact streak; no teacher, no protected copy |
| `preserve` | Frozen AC9 v2 behaviour: renew whenever decay urgency fires (this *is* the reactive baseline — any rule built only on decay state is behaviourally equivalent to it, so it takes no separate arm) |
| `relinquish` | Never renew after the first onset: static relinquisher, spends least |
| `fixed_schedule` | Spending-matched fixed duty cycle: renews on a declared periodic schedule calibrated in engineering to the adaptive arm's mean renewal writes |
| `random` | Renewal target chosen at random each time it is taken, matched attempt count to the adaptive arm |
| `protected` | Adaptive machinery with the preservation bit held in a protected external copy (scaffold control; never counted as autonomous) |
| `no_learning` | Adaptive machinery present with its writes sham-blocked while their costs are paid (shows the effect is the write, not the policy shape) |

`B_rescue`-style external supply is **not** used here: AC10 established the
enclosure's substitution; AC11 asks only about allocation spending.

## Endpoints

Per individual and per phase (development t<512, phase 1 512–1024, phase 2
1024–2048): activity and completion; retained entries and occupied sites; contact
productivity; material and energy spent specifically on renewal, and total;
W/C/B production; deaths; and the tick at which preservation spending stops.
Also reported: the streak register's final state, and whether the organism's
relinquishment preceded or followed its first failure-dense window.

## Prespecified gates

G1 `adaptive`: at least 6/8 complete the full horizon; in phase 2 the arm's mean
contact productivity exceeds the `preserve` arm's; retained entries still present
in at least 4/8 at the endpoint; renewal spending in phase 2 below the `preserve`
arm's by at least 50%.
G2 `preserve`: 8/8 complete while the route is valid, and in the moved world at
most 4/8 complete with phase-2 productivity at or below 0.15.
G3 `relinquish`: in the valid-route world at most 4/8 complete (blind search
cannot fund maintenance), establishing that preservation is worth its cost.
G4 `fixed_schedule`: matched renewal spending to `adaptive` within 15% in phase
1, and at most 4/8 complete in the moved world — i.e. matching the spending is
not sufficient.
G5 `random`: at most 4/8 complete in the moved world.
G6 `protected`: completes, and is reported as a scaffold outcome only.
G7 `no_learning`: behaves as `preserve` under the move (at most 4/8 complete),
showing the adaptive arm's advantage requires the write to occur.

Falsification. If `adaptive` fails G1, or if any rival matches it on both phases
without the stored, paid, vulnerable state mattering, the claim fails as stated
and must be reported as a negative result. If `relinquish` completes in the
valid-route world, the world does not make preservation worth its cost and the
study is not diagnostic; that outcome is reported as a failed design, not
reinterpreted.

## Sample and discipline

Seeds 1400–1403, two histories, 8 individuals, all seven arms: 56 rows. Disjoint
from every earlier family (AC10 1300–1303, AC9 1200–1203 / 1100–1103 / 1000–1003,
AC8 800–808, AC7 700–708, AC6 400–431, AC5 200–207, AC4–AC2 0–15, AC1 0–31).
Engineering seeds (0–2 and any later fixes) are excluded from the final sample
and retained separately with their source snapshots. No constant, threshold or
arm definition changes after the first final seed; later analyses are labelled
prespecified or exploratory. Intervals, if computed, are descriptive.

## Verification plan (before the final run)

`test_ac11.py`, at minimum: the frozen-behaviour equivalence of the `preserve`
arm against the frozen AC9 v2 rows for the same seeds; single-step isolation of
the preservation write (only the targeted bits and their 1:1 costs differ);
preservation-spending accounting against the frozen ledger identity; the
streak register's decay and paid repair; complete-state erasure noninterference
for every arm; exact replay; and paired-observation equivalence across arms.
`audit_ac11.py` re-derives coverage, ledgers, arm invariants and source hashes
from the saved table without simulating. `replay_ac11.py` performs sampled exact
reruns. All three must pass before results are written up.

## What this does not establish

No full autopoiesis, intrinsic normativity, subjective experience or rich
developmental individuality. Relinquishment here is region-granular because the
frozen renewal primitive is; per-key relinquishment needs a new primitive and is
future work. The world's port space and yields are supplied constants, not
organism achievements. The organism does not discover a new metabolic need; it
reallocates spending on a capability it already acquired. Absence of a learning
advantage over the spending-matched and random rivals is a publishable negative
result and will be reported as one.

## Recording

Feasibility outputs are retained as `ac11_feasibility_v1/` (frozen economy, 32
rows) and `ac11_feasibility_v2/` (candidate regime, 24 rows), both labelled
engineering. Implementation will be a new `ac11.py` plus tests, audit and replay,
with frozen results in a new versioned directory; earlier freezes, results and
protocols remain untouched.
