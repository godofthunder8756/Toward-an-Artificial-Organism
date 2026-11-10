# RWM design card v1: review and errata 1

Additive. [RWM_DESIGN_v1.md](RWM_DESIGN_v1.md), its code and its outputs are
unchanged. Written 2026-11-10 after re-reading the card against the rest of
the program. One finding is retracted, the verdict's interpretation is
narrowed, and the card is repositioned.

## E1. Retracted: "In use, the workspace is inert" (§8, finding 3)

The card inferred this from zero closed-loop conditional mutual information on
six edges. That measure is zero whenever the source node is determined by the
rest of the state, whatever causal work the edge does. Intervening directly on
the stationary states of the same closed loop gives:

| Edge | Stationary mass where flipping the source changes the target's next value | Mass where the source varies at all given the rest of the state |
| --- | --- | --- |
| I → G | 0.657 | 0.000 |
| X → K | 0.341 | 0.059 |
| I → K | 0.326 | 0.000 |
| K → I | 0.245 | 0.048 |
| G → K | 0.117 | 0.441 |
| K → X | 0.045 | 0.048 |

The workspace edges are causally active in use. The zero CMI reflects a
deterministic controller with no residual variability, which is the known
weakness of conditional transfer entropy. The "closed-loop causal density"
column in §8 should not be read as a measure of use. The interventional column
stands.

## E2. Narrowed: what the NO_GO verdict means

T6 and T7 clamp the world as background. The action node A acts mainly through
the world (A → location → observation). Inside the controller its only
consumer is X, which ignores A whenever its gated term is 0. With the world
clamped, the minimum partition falls at A on 78% of the mass. The instrument
therefore drew the system boundary across the perception-action loop the
design is built around. Whether Φ_s would be positive with the body and world
inside the boundary was not computed.

The computed numbers stand. The reading "the architecture is not integrated"
does not follow from them. The verdict means only: under this Φ_s definition,
with the environment clamped, the controller alone is severable.

## E3. Φ_s is not an instrument for Layer 3 as the program defines it

Layer 3 asks whether information is recurrently sustained and flexibly
available across specialized processes. That is a functional property, and the
card's own unfolding control shows Φ_s is blind to function. Track C's H1
(hysteresis, critical slowing) and H2 (content swap with ignition held) test
Layer 3 directly. Of the three options in the card's §10, the third is the
one to take: Φ_s is retired as a gate and kept, if at all, as a labelled
structural diagnostic.

## E4. Repositioning

The card was written without reference to Track C, which is the architecture
of record for the layered design. RWM-8 is a coarse logic-gate restatement of
it and is not a parallel architecture family. What remains useful:

- the exact objective certificate (prediction error alone selects the dark
  room; the setpoint prior must be supplied and not learnable);
- the instrument controls, in particular the unfolding equivalence;
- the structural predicates T1–T5 as a wiring checklist.

## E5. Smaller points

- "The monitor forms its own complex" is true of any pair of parity gates in a
  loop. It says nothing about metacognition.
- The gate criteria were fixed after exploratory runs, as the card disclosed.
  [GROUNDING_PROTOCOL_v1.md](GROUNDING_PROTOCOL_v1.md) froze its claims in a
  commit before its run.
- `rwm/gate.py` evaluates a rational string with `eval`. The code is left
  as it is because its hashes are recorded in the outputs.
