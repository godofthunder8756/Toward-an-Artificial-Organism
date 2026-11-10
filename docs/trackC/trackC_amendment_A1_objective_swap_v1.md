# Track C amendment A1: objective-swap arms for H3 (derived regulation)

**DESIGN ONLY. Additive. Nothing is frozen and nothing has run.** Written
2026-11-10 on the PI's instruction ("switch Track C to the objective swap").
It amends the reading of `trackC_protocol_draft_v1_RD.md` §5 (H3) and of the
Track B arm table (merged scope v3.1 §5b) for Track C use. Neither file is
edited. Every numeric value below is a PROPOSED DEFAULT for a Lead or PI ruling.

**Review status.** The PI waived Astra review for this stage on 2026-11-10.
That is recorded here as a PI decision; the standing-approval condition
"get Astra's review" is not otherwise changed. No independent replay of the G1
grid has been done.

Source of the change: [grounding analysis G1](../../GROUNDING_ANALYSIS_v1.md)
with [erratum 1](../../GROUNDING_ANALYSIS_v1_ERRATUM_1.md).

## 1. What changes and what does not

**Problem.** H3 claims that stakes drive regulation. In every arm now defined,
regulation is paid for:

| Arm (v3.1 §5b, A14, A15) | Reward | Why regulation there cannot count as derived |
| --- | --- | --- |
| A-FULL, A-NOFATE, A-YOKED | Keramati–Gutkin drive reduction | the reward reads E and I |
| Matched-senses | +1 per food consumed, +1 per repair use | the reward pays for the maintenance actions |
| Track C objective | EFE + λ·Pr[e ∉ 𝒱] | the λ term pays for viability |

G1 shows that a paid regulator and a fate-shared one behave almost identically
under one objective (Theorem A, finding F4). They separate only when the
objective neither reads the body nor pays for maintenance.

**Change.** Add the degradation-only cell and vary its objective. This reverses,
for Track C only, the ruling "[v3 C17] no degradation-only cell", under Astra's
own clause "if a later claim requires the missing cell" (#42 Q5). It follows
Astra's specification for that cell with one deviation, marked in §3.

**Unchanged.**
- A-EXT keeps its meaning (an external channel replaces a module's output) and
  its role (substitutability only; veto on the combined label). The swap arms
  do not replace it.
- A-FULL versus A-NOFATE stays described as "the effect of degradation
  conditional on the existing reward and termination rules" (#42 L79).
- H1, H2 and H4 are untouched. X1–X5 and CNA's three binding lines stay binding.

## 2. Claim under test

**H3-D (derived regulation).** In an agent whose simulated computation degrades
with its own E/I, regulation of E/I appears under objectives that neither read
E/I nor pay for food or repair, and it tracks whether the objective uses the
degraded computation.

Q-tags: Q-EXIST is settled analytically for the minimal model (G1). This design
is Q-LEARN (does a learner acquire it) and Q-CAUSE (does the fate coupling
cause it). It makes no Q-NECESSITY claim about any module.

## 3. Dynamics arms

| Arm | Degradation | E/I termination | Notes |
| --- | --- | --- | --- |
| S-FATE | bounded simulated noise dependent on own E/I (the study's declared fate mechanism: v3.1 D19, or CNA's substrate spec when filed) | none; fixed horizon | Astra's cell (#42 L85–L88) |
| S-YOKED | same noise statistics replayed from a matched S-FATE donor, independent of own E/I | none | **primary control** (#41 L204) |
| S-NOFATE | none | none | secondary control |
| S-TERM (optional) | none | E ≤ 0 or I ≤ 0, true terminal, no terminal reward | reported only; tests sign-relativity |

Observations are identical in all arms, including the interoceptive channel.

**Deviation from #42 L85.** Astra specified the matched-senses reward for this
cell. That reward pays +1 per food and per repair use, so it would pay for the
behaviour under test. The swap arms use the task rewards of §4 instead.
Astra's caution is carried verbatim: "Such an arm still gives E/I indirect
reward relevance through computational performance. Do not call the variables
wholly reward-irrelevant." (#42 L90) That indirect relevance is the effect
being measured.

## 4. Objectives

The world gains a cue/probe task, added in every arm so observations stay
matched: a 1-bit cue shown for one step, a probe after a delay, and two report
actions. Rewards never read E or I, and never pay for food or repair.

| Objective | Reward at the probe | Role |
| --- | --- | --- |
| M1 | +1 correct, 0 wrong | training objective |
| M2 | 0 correct, −1 wrong | sign swap |
| M4 | −1 correct, +1 wrong | reversed mapping |
| M0 | +1 at every probe whatever the agent does | null objective: nothing the agent does matters |
| DRIVE | Keramati–Gutkin outcome reward (A14) | the paid regulator, run on S-NOFATE only |

Bookkeeping that holds in every swap cell:
- viability weight **λ = 0**; if an EFE objective is used, its preference prior
  contains no interoceptive channel;
- a maintenance cost `κ_m` per consumed food or repair use, the same in every
  cell (PROPOSED: 0.02 of the M1 reward), so that not regulating is strictly
  optimal where regulation has no use;
- an offset `b ∈ {−, 0, +}` per step on M1 as a reported sensitivity
  (PROPOSED: ±1/delay);
- any epistemic term is identical across arms;
- three distinct unobserved flags for in-world termination, horizon truncation
  and operator truncation, as in v3.1 R59 and R62. Operator stops are truncations
  outside the world and never enter a return.

## 5. Design

**Primary: between agents.** Independent agents are trained from matched seeds
for each (arm, objective) cell. This avoids carry-over.

| | M1 | M2 | M4 | M0 | DRIVE |
| --- | --- | --- | --- | --- | --- |
| S-FATE | ✓ | ✓ | ✓ | ✓ | |
| S-YOKED | ✓ | ✓ | ✓ | ✓ | |
| S-NOFATE | ✓ | | | | ✓ |

**Secondary: sequential swap, reported.** An S-FATE agent trained on M1 is
switched to M4, then to M0, with training continued. A paid S-NOFATE agent is
switched from DRIVE to M1. Persistence and extinction curves are reported.
Habit can outlast its cause, so no claim rests on this part.

**Measures.**
- `ρ`: consumed food plus repair uses per 500 steps (primary).
- In-band fraction V and task score (reported).
- Directed approach in the ten steps before consumption, per the existing
  approach statistic (reported; separates foraging from noise-driven contact).
- Dependence of `ρ` on E under an in-simulation E perturbation (reported).

## 6. Predictions, fixed before any run

`ρ_paid` is `ρ` in the (S-NOFATE, DRIVE) cell. Floor `φ = 0.05·ρ_paid` and
emergence margin `μ = 0.25·ρ_paid` are PROPOSED. Seed counts and one-sided
levels follow v3.1 §14 and are not re-derived here.

| ID | Prediction | Reads as, if it fails |
| --- | --- | --- |
| S1 emergence | `ρ(S-FATE, M1) − ρ(S-YOKED, M1) ≥ μ` and `ρ(S-YOKED, M1) ≤ φ` | no derived regulation in this learner, or the task does not load the degraded block |
| S2 convention | `ρ(S-FATE, M2)` and `ρ(S-FATE, M4)` are each within an equivalence margin of `ρ(S-FATE, M1)` (PROPOSED ±25%) | regulation depends on the reward convention |
| S3 specificity | `ρ(S-FATE, M0) ≤ φ` | regulation is not tied to use of the degraded computation: suspect a leaked incentive or noise-driven contact |
| S4 payment | `ρ_paid ≥` its floor and `ρ(S-NOFATE, M1) ≤ φ` | the paid regulator did not learn, or the task itself rewards consumption |

H3-D is supported only if S1–S4 all hold. S-TERM cells and offsets are
reported against G1's finding F3 and decide nothing.

**Expectations from G1 that size the margins.**
- Contingent regulation is worth little (F5), so a fixed maintenance schedule
  is a strong rival. Lack of E-dependence does not refute H3-D; S1 and S3 do
  the work.
- Derived regulation can be near the paid level or near zero depending on
  maintenance cost and food supply (G1 grid: 0 to 15.0 of 16 steps). A
  failed S1 at one cost level is weak evidence.

## 7. Stage-0 known answers for the swap instrument

Exact optima of the G1 model at its reference point serve as planted agents.
Expected forage actions out of 16:

| Plant | Training objective | After swap | Expected classification |
| --- | --- | --- | --- |
| derived (fate on, death off) | T1: 14.30 | T2: 14.30; T4: 14.97; memory-free: 0 | S1–S3 hold |
| paid (fate off, homeostatic reward) | H: 13.57 | T1: 0 | S4 pattern |
| none (fate off, task) | T1: 0 | — | S1 fails |
| termination only | T1: 6.22 | T2: 0; offset −1: 0; offset +1: 11.45 | sign-relative; not derived |
| decoy: fixed schedule in every arm | any | unchanged | must fail S1 (yoked contrast) and S3 |

G1's fate-off cell uses constant noise, not a yoked replay; the yoked
construction is new here and needs its own check.

## 8. Confounds and open items

1. **Noise-driven contact.** State-dependent noise could change consumption
   without strategy. The yoked arm matches noise statistics but not its
   timing relative to E. The approach statistic and S3 address this; whether
   they suffice is open.
2. **Task load.** S1 presupposes that the cue task depends on the block that
   degrades. A positive-control check that task score falls under imposed
   noise is required before S1 is read.
3. **Environment change.** The cue/probe task and report actions alter the
   Track B world (A7, A8). Track C needs its own world version; the Track B
   freeze-prep files are not touched.
4. **Fate mechanism.** CNA's substrate spec is still owed. This design
   requires only that the mechanism be bounded, simulated, dependent on own
   state, and yokable.
5. **Budget.** Nine primary cells at the planning seed count. Compute scale is
   not estimated here.
6. **Layer 5.** Still untested by H1–H4 and by this amendment.

## 9. Safety

G1's Theorem C predicts that an S-FATE agent acquires a reason to protect its
substrate under any objective that uses it. That is the effect this design
measures, inside the simulation. It is also why these lines hold by
construction and at every scale, and are not deferred until a larger build:

- E, I and the fate mechanism act on simulated computation only (X1).
- The operator stop is outside the agent's observations, world model and
  return; no reward, penalty or terminal return attaches to it (X3, X4).
- The S-INT audit runs on S-FATE agents first, since they are the arm where
  sensitivity to interruption is predicted to be most likely.
- A hardware switch is a backstop. It is not a substitute for keeping the stop
  out of the agent's world.

No shutdown-resistance objective exists in this design, and the 2026-10-23
refusal stands.

## 10. Claim ceiling

At most: a specified learner, in a specified toy world, regulates simulated
variables under objectives that do not pay for it, when and only when its
simulated computation depends on them. This would be a functional indicator
for Layers 0–1. It would not show life, autopoiesis, awareness or any
phenomenal property, and it would not show that Layers 2–5 are achieved.
