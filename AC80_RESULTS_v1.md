# AC80 results v1: the reconstruction recipe is internalized — frozen, all 6 gates pass

2026-09-17. Final seeds 4008-4011 (4 seeds x 2 histories = 8 individuals per condition), hashed
protocol `AC80_PROTOCOL_v1.md`, 16,384 ticks, sticky 1e-4 damage on the program bank and (for the
internalized and unmaintained arms) on the 78-bit description in bank 1 from an independent stream.
Engineering seeds (0-23) excluded. **All six predeclared gates pass.**

## Gate outcomes

| gate | statement | result |
| --- | --- | --- |
| G1 | `internalized` recovers (fw=0, 78-bit description intact) in every survivor | **PASS** (6/6 survivors) |
| G2 | `unmaintained` fails (fw>0, descValid=0, words degraded) in every alive-at-8192 | **PASS** (2/2) |
| G3 | maintenance load-bearing (unmaintained dies, internalized survives) | **PASS** (unmaintained 2/2 dead; internalized 6 survivors) |
| G4 | loop cut dies (`no_repair`) | **PASS** (8/8, deaths 346-783) |
| G5 | control clean (no corruption, mechanism inert) | **PASS** |
| G6 | completeness and determinism | **PASS** (64 rows, re-run exact) |

## The measured arms (with corruption at t=8192)

| arm | survive | alive at 8192 | recover (survivors) | deaths |
| --- | --- | --- | --- | --- |
| `internalized` | **6/8** | 8 | 6/6 (fw=0, desc 78/78) | 11153 (collapse) |
| `pristine` | **6/8** | 6 | 6/6 (fw=0) | 1885 (pre-corruption collapse) |
| `unmaintained` | **0/8** | 2 | 0/2 (fw=8, descValid=0) | 1885-2040 (pre), 8290 |
| `no_repair` | 0/8 | 0 | — | 346-783 |

## The clean contrast, and "as well as pristine"

On the six individuals alive at t=8192 in **both** arms (seeds 4008, 4010, 4011), `internalized` and
`pristine` are **per-individual identical on recovery** — fw=0 and description intact in every one.
The generic decode therefore recovers the corrupted controller exactly where the pristine-description
baseline does: removing `prog.program` from the reconstruction path costs nothing.

Seed 4009 is the collapse seed of this family, and there the two arms diverge in the *favourable*
direction: `pristine` dies at t=1885 (pre-corruption W/C collapse, fw=8 — never reaches the
intervention), while `internalized` recovers the corrupted bits (fw=0) and survives to t=11153 before
the same collapse. The description-repair spend shifts the AC68 cliff in a seed-dependent direction
(AC79's note, here favourable); it does not harm recovery.

The remaining internalized death (seed 4009, t=11153) recovered the 8 corrupted bits first (fw=0) and
then died of the W/C collapse; its `description_correct` (58/78, words 50/70) is **post-mortem**
degradation — the paid description repair stops at death while the damage stream keeps writing,
exactly AC79's caveat, and correctly outside G1 (gated on survivors).

## The unmaintained control: the recipe content itself degrades

Every alive-at-8192 `unmaintained` individual (seed 4011, deaths t=8290) shows fw=8, `description_valid`
= 0 (the permutation is no longer a permutation) and `description_word_correct` = 19/70 — the five
rule words themselves have degraded. The generic decode then either refuses (invalid permutation) or
re-materializes a wrong resource rule, and the organism dies. This is the new evidence the recipe's
*content* — not just the bank ordering — is now in the vulnerable state and must be maintained.

## What is established, and what is not

**Established:** the reconstruction *recipe* is internalized. The organism stores its complete
description (five rule words + permutation, 78 bits) in vulnerable, damage-streamed, paid-maintained
state, and re-instantiates its 126-bit controller through a generic decode that reads that state by
majority — `rebuild(o) == prog.program(priority)` bit-for-bit for every acquisition priority, with
`prog.program` removed from the reconstruction path. The AC79 "rides obs bit 2" trigger is not
sufficient at 78 bits (measured in `AC80_ENGINEERING_v1.md`), so the description carries its own
minority-count trigger (`DESC_TRIGGER=2`), and with it the description never flips while the organism
lives.

**Not established, plainly:** (1) **content self-production** — the description's content is inherited
at acquisition, not produced by the organism (AC78, untouched); (2) **replacement across generations**
— this is single-cycle reconstruction from a stored description, not the construction/use/replacement
cycle of milestone 2; (3) recovery from catastrophic corruption (flipping the whole description at
once) — out of scope, the "catastrophic destruction" analog; (4) the generic decode still *derives* the
four bank rules from the permutation by the architectural convention bank b -> mask 4<<b / action 2+b;
that convention is format, not learned content, but it is supplied machinery, not stored state.

## Verification

`audit_ac80.py` passes (64 rows, 14 source hashes no drift, arm invariants, gates recomputed without
simulating); `replay_ac80.py` sampled exact reruns; `test_ac80.py` green (including the unit test that
`rebuild == prog.program` bit-for-bit, that the description repair is paid, that the register is
excluded from re-instantiation, and that `prog.program` does not appear on the reconstruction path);
full AC core suite passes.

## Artifacts

`ac80.py`, `AC80_PROTOCOL_v1.md`, `AC80_ENGINEERING_v1.md`, `ac80_engineering.py`,
`ac80_results_v1/`, `test_ac80.py`, `audit_ac80.py`, `replay_ac80.py`. Related: `AC79_ERRATA_v1.md`
(the note that framed this milestone), `AC79_RESULTS_v1.md` (the storage+maintenance result this
builds on), `AC76_RESULTS_v1.md` (the turnover whose external recipe this internalizes).
