# AC80 engineering v1: internalized reconstruction recipe — the trigger must be widened

2026-09-17. Engineering only — no protocol, no final seeds, no claim. `ac80.py` + `ac80_engineering.py`.

## What was measured

Milestone 1 of the "internalize the recipe" goal: store the complete organism-specific description
(the five rule words, 5×14 = 70 bits, plus the 8-bit permutation = 78 bits) in vulnerable,
damage-streamed, paid-maintained state, and replace `prog.program(priority)` during life with a
generic decode that reads that state by majority and rebuilds the 126-bit program. The task's
"measure first" question: AC79 rode the program's corruption trigger (obs bit 2), conservative only
because the program (126 bits) is 16× the 8-bit description. At 78 bits the program is only ~1.6×
larger — does obs bit 2 still precede a description-majority flip?

## Finding 1: the generic decode is bit-identical to the scaffold

`rebuild` (ac80.py) reads the 78-bit description by majority and rebuilds the program: the five
rule words are copied verbatim from the stored bits, and the four bank rules are derived from the
permutation by the architectural convention bank b → (enabled=1, mask=4<<b, action=2+b). It knows
only the format (14-bit word, 5-word + 4-bank layout, majority read); no rule word value or
permutation. Measured: `rebuild(o) == prog.program(priority)` bit-for-bit for 12/12 acquisition
priorities with an intact description, and `rebuild` returns None on an invalid permutation.
`prog.program` is retained only in the observer (corruption setup + endpoint scoring), never on the
reconstruction path.

## Finding 2: obs bit 2 does NOT suffice at 78 bits — the description needs its own trigger

With the AC79 trigger (obs bit 2 only), the description's correct-0 bits flip to a wrong majority
in a subset of individuals. Measured over 32 internalized individuals (seeds 0–23 × 2 histories,
16,384 ticks): every individual that **survived** kept max 3 set replicas on any correct-0
description bit (never 4), but several **dying** individuals reached a majority flip (4–7 set
replicas) *before* their W collapsed, and died with the corruption cemented:

- **WORD flip** (seeds 10, 16, 22): a rule-word bit (e.g. bit 5 = fuel-rule mask bit, bit 47, bit
  66) flipped first; the permutation stayed valid, so `rebuild` produced a *well-formed but wrong*
  program and the organism re-instantiated itself into the wrong controller and died. Silent
  corruption of the recipe content.
- **PERM flip** (seeds 17, 19): a permutation bit (70, 76) flipped first; `rebuild` returned None,
  the re-instantiation silently refused, the program drifted, and the organism died.

The root cause is that obs bit 2 fires on the *program's* corruption, and for some seeds the
program's own bank-0 repair keeps it clean enough that obs bit 2 fires only a handful of times
(seed 16: 9 fires over 16,384 ticks), during which the 78-bit description accumulates damage
un-repaired.

## Finding 3: a description-minority trigger fixes it

The description was given its own trigger: the re-instantiation fires on (obs bit 2) OR (the
description's minority count `sum over bits of min(ones, 7-ones)` reaches `DESC_TRIGGER = 2`). This
is the same integrity statistic obs bit 2 computes for the program, applied to the description's 78
bits; it is format-level (7 replicas per bit, minority detectable), needs no new observation bit,
and knows no policy. Measured: max set-replicas on any correct-0 description bit at a repair
opportunity drops to **2, never 4**, in all 16 individuals, and the three seeds that previously died
of description corruption (13, 16, 19) now survive with the description intact.

## Recovery table (engineering, widened trigger, 16,384 ticks, corruption at t=8192)

| arm | survive | died<8192 | alive@8192 | recover (alive@8192) | desc intact |
| --- | --- | --- | --- | --- | --- |
| internalized | 12/16 | 4 | 12 | 12/12 (fw=0) | 12/16 (all survivors 78/78) |
| pristine | 12/16 | 2 | 14 | 12/14 (2 die 11275, W/C collapse) | 16/16 |
| unmaintained | 0/16 | 14 | 2 | 0/2 (fw=8, descValid=0) | 0/16 |
| no_repair | 0/16 | 16 | 0 | — | 0/16 |

Per-individual, `internalized` and `pristine` are identical on recovery (fw=0) among every
individual alive at t=8192 in both arms. The remaining internalized deaths are the AC68 W/C
collapse, and their low `description_correct` (24–46/78) is post-mortem degradation — the paid
description repair stops at death while the damage stream keeps writing, exactly AC79's caveat.

## Conclusion carried into the protocol

1. The recipe is internalized: `rebuild == prog.program` bit-for-bit, and `prog.program` is removed
   from the reconstruction path.
2. The AC79 "rides obs bit 2" trigger is **not** sufficient at 78 bits; the description needs (and
   gets) its own minority-count trigger at `DESC_TRIGGER = 2`.
3. With the widened trigger, the description never flips while the organism lives; recovery is
   gated on survivors (the AC68 W/C collapse kills internalized and pristine alike), and survival
   is reported as a bimodality-aware lower bound.
