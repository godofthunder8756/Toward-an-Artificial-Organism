# AC85 engineering v1: internalizing the bank-rule convention — all six gates pass on engineering seeds

2026-09-17. Engineering only — no protocol freeze, no final seeds, no claim. `ac85.py` (seeds 0-7,
16,384 ticks, corruption at t=8192).

## What was measured

AC80's residual: the generic decode still DERIVES the four bank rules from the permutation by the
architectural convention bank b -> (enabled=1, mask=4<<b, action=2+b). This study stores the bank
rules' masks and actions as vulnerable, damage-streamed, paid-maintained state alongside the words
and permutation, and `rebuild` READS them instead of deriving them.

## The description (130 bits)

Five rule words (70 bits) + the 8-bit permutation + four bank-rule masks (9 bits each, in priority
order) + four bank-rule actions (4 bits each, in priority order) = 130 bits, all in `traces[1,:130]`,
7 replicas/bit, sticky 1e-4 damage from an independent stream, paid majority-restore on
(obs bit 2) OR (minority count >= DESC_TRIGGER=2).

`rebuild` reads the masks/actions from state and cross-checks them against the stored permutation
(valid permutation, masks read back as 4<<b and actions 2+b for each b in order); a degraded
description decodes to None, never to a silently wrong controller. The decode is ORDER-PRESERVING
(AC86's correction carried forward): it reproduces the ACQUIRED program, not `prog.program` order.

## Findings

1. **`rebuild == acquired` bit-for-bit for 12/12 acquisition priorities** (unit test), and the
   masks/actions read back as the convention materialization. No function on the reconstruction path
   constructs a mask or action from a bank index; `prog.program` survives only in the observer
   (corruption setup + the consistency cross-check).

2. **The bank-rule content is now in the vulnerable state and degrades without maintenance.** The
   unmaintained arm ends with `description_bank_correct` 10-12/52 (masks+actions) alongside word
   degradation 17-20/70 — the convention itself, not just the words, is damaged and unrepaired.

3. **All six gates pass on engineering seeds** (16 individuals per arm = 8 seeds x 2 histories).
   internalized survives 16/16 and recovers every corrupt individual (fw=0, description 130/130);
   unmaintained dies (first_dead 1059-8423) with a degraded, invalid description; no_repair dies
   16/16 (first_dead 366-1050); the no-corruption control is clean (fw=0, description_same=1). The
   description-bank degradation is what the G2 contrast now measures — the bank-rule convention is
   inside the maintained state.

## Recovery table (engineering, seeds 0-7, 16,384 ticks)

| arm | survive | fw (corrupt survivors) | description (corrupt) | bank-rule bits | first_dead |
| --- | --- | --- | --- | --- | --- |
| internalized | 16/16 | 0 | 130/130 | 52/52 | — |
| pristine | 16/16 | 0 | 130/130 | 52/52 | — |
| unmaintained | 0/16 | 8 | 19-52/130 (word 17-20/70, bank 10-12/52) | 10-12/52 | 1059-8423 |
| no_repair | 0/16 | 8 | 19-52/130 | 10-12/52 | 366-1050 |

Note the unmaintained individuals die *before* the corruption tick in most seeds (the degraded
description is never re-instantiated because no corruption fires obs bit 2); the two that are alive
at t=8192 (seeds 1 and 6) then die with fw=8 and an invalid description — the G2 contrast is
non-vacuous.

## Conclusion carried into the protocol

The bank-rule convention is internalized: masks and actions are stored in the vulnerable,
maintained description and read by the generic decode, with no derivation on the reconstruction
path. The study is an internalization claim, not a content self-production claim (AC78) and not a
better-controller claim — the four bank rules are still the four bank rules; what moved into the
vulnerable state is their mask/action content.
