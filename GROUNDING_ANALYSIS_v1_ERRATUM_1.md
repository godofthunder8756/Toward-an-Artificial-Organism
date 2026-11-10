# Grounding analysis G1: erratum 1 (terminology; no number changes)

Additive, 2026-11-10. The frozen protocol and the results are unchanged.

## E1. "A-EXT" was the wrong name

[GROUNDING_PROTOCOL_v1.md](GROUNDING_PROTOCOL_v1.md) (§1, §3, U6, R7) and
[GROUNDING_ANALYSIS_v1.md](GROUNDING_ANALYSIS_v1.md) (§7 item 1) call the
evaluator-paid homeostat "the A-EXT agent" and describe the analysis as
"Track C's ablation C (the A-EXT arm)".

In the program, A-EXT is something else: an external channel that replaces a
module's output, used for substitutability only (merged scope v3.1 §5b; Astra
#41 AQ-N1). It is not an external-reward arm.

Read every "A-EXT" in the two G1 files as **"paid regulator"**: an agent on
host-guaranteed machinery whose reward reads the body variable. The nearest
program arm is A-NOFATE without termination.

## E2. Corrected statement of the Track C consequence

Withdrawn: "A-EXT compared under one objective will reproduce the intrinsic
arm" (analysis §7 item 1).

Correct: every arm now defined pays for regulation, through the drive reward,
the matched-senses reward of +1 per food and repair use, or the λ viability
term. So none can show derived regulation. The cell G1 identifies as decisive
is the degradation-only cell that Astra specified in #42 Q5 and the Lead ruled
out as not then required, with a task reward in place of the matched-senses
reward. The design is in
[docs/trackC/trackC_amendment_A1_objective_swap_v1.md](docs/trackC/trackC_amendment_A1_objective_swap_v1.md).

A-EXT's own question (can an external estimate substitute for the internal
one) is not addressed by G1.

## E3. What is unaffected

All claims U1–U7 and R1–R7 as computed, the effect sizes, and findings F1–F6.
Only the label and the sentence in E2 change.
