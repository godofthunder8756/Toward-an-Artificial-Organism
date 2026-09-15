# AC13 calibration v1: first design in this line where the learner is not beaten

2026-09-15. Engineering calibration only. **No final seeds, no protocol, no
claim.** The world constants and gates below are what a protocol would have to
declare; they are measured, not assumed. Results in `ac13_calibration_v1/`.

## Why this design and not the previous two

AC11 (region-granular renewal) and AC12 (per-slot renewal) both failed for one
reason: the intervention **zeroed the organism's income**. With a readable stale
entry the stored port can never match the moved port, so material income is
exactly zero, renewal stops by starvation, and the entry lapses whether or not the
policy chose to relinquish it. The decision was downstream of an economics that
had already decided (`allocate` indistinguishable from `preserve`).

AC13 removes that: at the unannounced intervention (tick 1024) the affected port
becomes **unreliable** — the channel is drawn per contact — so a stored value earns
exactly what blind search earns (1/PORTS each). The information becomes worthless
but not harmful, income stays non-zero, and lifetime is not decided by the choice.
The material yield also drops at the same intervention, so paying to maintain
worthless information competes with the metabolism.

## Calibration grid (6 engineering individuals per cell)

Completions, seeds 0-2 and both developmental histories, `switch` = maintain the
affected slot before the intervention and drop it after (engineering-only
calibration arm, not a rival):

| Y1 \ Y2 | 24 | 16 | 12 | 8 |
| --- | --- | --- | --- | --- |
| **64** | switch 6/6, preserve 5/6, relinquish 1/6 | 6/6, 5/6, 1/6 | 5/6, 5/6, **0/6** | 6/6, 4/6, 2/6 |
| 48 | 5/6, 6/6, 4/6 | 6/6, 6/6, 3/6 | 6/6, 6/6, 2/6 | 6/6, 5/6, 4/6 |
| 32 | 6/6, 6/6, 4/6 | 5/6, 6/6, 4/6 | 6/6, 3/6, 4/6 | 4/6, 5/6, 3/6 |

Two readings fix the world:

- **Y1 must be high enough that the route is needed while it is valid.** At Y1=64
  the never-maintain arm completes 0-2/6 with phase-1 productivity 0.277 against
  1.000 for every maintaining arm; at Y1=48/32 it survives 2-4/6, i.e. the route
  matters less and the world stops posing the question. **Y1=64.**
- **Y2 must make worthless maintenance compete with the metabolism without putting
  the decision itself on a knife edge.** At Y2=8 the payment for the drop (7
  replicas = 7 material + 7 energy) can tip a marginal organism: `allocate` falls
  to 3/6 while the scripted `switch` is 6/6, so that regime measures the timing of
  a 7-unit payment rather than the value of information. **Y2=12.**

## Study arms at Y1=64, Y2=12

| arm | alive | phase-1 productivity | phase-2 productivity | renewal writes phase 2 | drop tick |
| --- | ---: | ---: | ---: | ---: | ---: |
| **`allocate` (learner)** | **6/6** | **1.000** | 0.274 | **393** | 1070 |
| `protected` (scaffold) | 6/6 | 1.000 | 0.274 | 393 | 1070 |
| `no_learning` (paid sham write) | 6/6 | 1.000 | 0.272 | 463 | 1070 |
| `fixed_schedule` (blind duty 1/2) | 6/6 | 1.000 | 0.284 | 491 | – |
| `preserve` (maintain always) | 5/6 | 1.000 | 0.270 | 662 | – |
| `random` (matched rate) | 4/6 | 1.000 | 0.278 | 324 | – |
| `relinquish` (maintain never) | 0/6 | **0.277** | 0.137 | 0 | – |
| `switch` (scripted, calibration) | 5/6 | 1.000 | 0.284 | 272 | – |

Three contrasts, and why each matters:

1. **The route is maintained while it is worth 4× blind search.** Every
   maintaining arm reaches phase-1 productivity 1.000; `relinquish` reaches 0.277
   and dies 0/6. The organism must be maintaining the entry before the
   intervention, and it is.
2. **It stops paying once the information is worthless.** Phase-2 renewal writes
   fall to 393 (41% below `preserve`'s 662 and below `fixed_schedule`'s 491) with
   *equal* phase-2 productivity (0.274 vs 0.270). The drop fires 46 ticks after
   the intervention in 6/6 individuals, driven only by the organism's own
   unproductive contacts.
3. **The write is what matters, not the policy shape.** `no_learning` carries
   identical machinery and pays the same attempted costs but its writes are sham:
   it spends 463 replicas in phase 2 and behaves as a maintainer, so the 393
   figure is attributable to the write landing in the vulnerable register.

## Limitations, stated now rather than in a distant disclaimer

- **`preserve` survives (5/6), so this is not a survival-level need.** The claim
  this world can support is behavioural and economic: the organism's maintenance
  spending tracks the usefulness of the retained information while its viability is
  preserved, and the static policy that ignores usefulness (`relinquish`) dies. It
  cannot support "the organism must relinquish or die".
- Six engineering individuals per cell, one world, one intervention time. No
  protocol, no mechanism tests, no audit, no replay, no frozen sample yet.
- Y2=8 shows the drop's own payment can be decisive, which is why it is excluded
  from the declared world rather than reported as a result.
- The allocation register, the streak machinery and the interpreter are supplied
  as declared; the *decision* is in vulnerable paid state (proved inert by the
  AC12 frozen-row equivalence, 4/4).

## Next step

Write `AC13_PROTOCOL_v1.md` declaring this world (ports 4, Y1=64, Y2=12,
unreliable port plus yield drop at tick 1024), the seven arms including the
protected and sham-write controls, the gates above as measured contrasts, a sample
of eight individuals on new seeds (1600-1603), and the falsification conditions —
then `test_ac13.py`, the frozen run, `audit_ac13.py` and `replay_ac13.py`.

## Artifacts

`ac13_calibration.py`, `ac13_calibration_v1/` (calibration grid + study arms, all
rows), `ac12.py` (harness: per-slot allocation, register, world modes),
`ac12_memory.py` (the primitive), `AC12_DESIGN_CONTROLS_v1.md` (the failure this
answers), `AC11_DESIGN_CONTROLS_v2.md` (the granularity failure before that).
