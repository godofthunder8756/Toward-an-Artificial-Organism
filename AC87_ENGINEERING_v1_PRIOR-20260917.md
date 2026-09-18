# AC87 engineering v1: integrated successor — all eight gates pass on engineering seeds

2026-09-17. Engineering only — no protocol freeze, no final seeds, no claim. `ac87.py` (seeds 0-7,
16,384 ticks, no corruption intervention).

## What was measured

The AC85/AC86 review named three residuals, all addressed in one architecture:

1. The succession controller's state (phase/source/target/active/timing) was Python fields outside
   the maintained substrate.
2. AC86 copied the 78-bit description (bank rules still synthesized externally), not AC85's full
   description; and AC85's decoder rejected masks/actions that did not match the convention.
3. Only the active slot was damaged; `verified_valid` was logged but did not gate switching.

AC87: 122-bit description (5 words + 4 masks + 4 actions, no permutation), generic decode that never
rejects, succession phase/source/target internalized in bank 1 (6 bits, damaged + majority-restored),
all four slots + pointer + succession state in the damage stream, and the copy→switch transition
gated on verification (faithful copy + distinct masks).

## Findings

1. **`build_program == acquired` bit-for-bit for 12/12 priorities** (unit test), and the decode never
   rejects: changing a stored mask to another syntactically valid value is followed faithfully (the
   rebuilt program carries the new mask, not the convention).
2. **Succession works with the internalized state machine.** Every succession individual (16/16
   survive) completes 7 cycles (pointer 0→1→2→3→0→1→2→3), each cycle verified faithful (copy ==
   source) and well-formed (4 distinct masks), with `remove_tick >= switch_tick >= copy_done >=
   start`. The internalized state ends idle (phase 0) with succ_minority 0-1 — the 6 state bits were
   damaged (~69 flips over the horizon) and repaired, never cementing a wrong majority.
3. **The succession state is genuinely vulnerable.** In the `repair` arm (no succession machinery,
   so its state is unmaintained) the 6 bits cement to phase=3 (all-ones) with succ_minority 4-12 —
   the state is in the damage stream and only the succession arm's maintenance keeps it clean.
4. **The recipe is maintained and the contrast is categorical.** succession 122/122 and repair
   122/122; unmaintained dies 16/16 (857-3179) with the description degraded to 28-35/122. The
   no-damage control is byte-identical across arms (0 successions, 122/122, state_hash equality).

## Recovery table (engineering, seeds 0-7, 16,384 ticks)

| arm | survive | successions | description | pointer | succ_phase | first_dead |
| --- | --- | --- | --- | --- | --- | --- |
| succession | 16/16 | 7 each | 122/122 | 3 | 0 (idle) | — |
| repair | 16/16 | 0 | 122/122 | 0 | 3 (cemented, unmaintained) | — |
| unmaintained | 0/16 | 0 | 28-35/122 | 3 (cemented) | 3 (cemented) | 857-3179 |

`writes` ~20,900-21,068 per succession individual (vs ~18,150-18,280 in AC86) — the extra cost is the
122-bit copy, all-slots damage, and the succession-state maintenance. `succ_writes` 4,373-4,495.

## Conclusion carried into the protocol

The replacement machinery's persistent coordination state is now stored, damaged, and maintained, the
complete description (including bank-rule content) is replaced through it, the decoder is generic
over syntax, and the verify step is a real gate. All eight gates pass on engineering seeds.
