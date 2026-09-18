# AC85 results v1: the bank-rule convention is internalized — frozen, all 6 gates pass

2026-09-17. Final seeds 4024-4027 (4 seeds x 2 histories = 8 individuals per condition, 64 rows),
hashed protocol `AC85_PROTOCOL_v1.md`, 16,384 ticks, sticky 1e-4 damage on the program bank and (for
the internalized and unmaintained arms) on the 130-bit description in bank 1 from an independent
stream. Engineering seeds (0-7) excluded. **All six predeclared gates pass.**

## Gate outcomes

| gate | statement | result |
| --- | --- | --- |
| G1 | `internalized` recovers (fw=0, 130-bit description intact) in every survivor | **PASS** (8/8 survivors) |
| G2 | `unmaintained` fails (fw>0, descValid=0, words degraded) in every alive-at-8192 | **PASS** (1/1) |
| G3 | maintenance load-bearing (unmaintained dies, internalized survives) | **PASS** (unmaintained 1/1 alive-at-8192 dead; internalized 8/8) |
| G4 | loop cut dies (`no_repair`) | **PASS** (8/8, deaths 391-810) |
| G5 | control clean (no corruption, mechanism inert) | **PASS** |
| G6 | completeness and determinism | **PASS** (64 rows, re-run exact) |

## The measured arms (with corruption at t=8192)

| arm | survive | alive at 8192 | recover (survivors) | deaths |
| --- | --- | --- | --- | --- |
| `internalized` | **8/8** | 8 | 8/8 (fw=0, desc 130/130) | — |
| `pristine` | **8/8** | 8 | 8/8 (fw=0) | — |
| `unmaintained` | **0/8** | 1 | 0/1 (fw=8, descValid=0) | 1215-8423 |
| `no_repair` | 0/8 | 0 | — | 391-810 |

## What changed from AC80

AC80 internalized the reconstruction recipe but left one residual: `rebuild` still derived the four
bank rules from the permutation by the convention bank b -> (enabled=1, mask=4<<b, action=2+b).
AC85 stores the bank rules' masks and actions as vulnerable, damage-streamed, paid-maintained state
alongside the words and permutation. The description is now 130 bits: the five rule words (70 bits),
the 8-bit permutation, the four bank-rule masks (9 bits each, in priority order), and the four
bank-rule actions (4 bits each, in priority order). `rebuild` READS the masks/actions and
cross-checks them against the permutation; no function on the reconstruction path computes a mask or
action from a bank index, and a degraded description decodes to None rather than a silently wrong
controller.

The decode is also ORDER-PRESERVING (AC86's correction carried forward): it reproduces the ACQUIRED
program (`ac9_priority_v2`'s reorder — resource words 0-3, bank rules, boundary word last), not
`prog.program` order, so re-instantiation does not move the dead rule or the register. `rebuild ==
acquired` bit-for-bit for every acquisition priority (unit test, 12/12), and `prog.program` survives
only in the observer (corruption setup and the consistency cross-check).

## The clean contrast

On the 8 individuals per arm, `internalized` and `pristine` are per-individual identical on recovery
(fw=0, description intact in every survivor): removing the bank-rule derivation from the
reconstruction path costs nothing. The `unmaintained` arm's description degrades across ALL its
content — words 17-20/70, permutation invalid, and bank-rule masks+actions 10-12/52 — so the
bank-rule convention itself, not just the words, is now in the vulnerable state and degrades without
maintenance. The one unmaintained individual alive at t=8192 (seed 4026) then dies with fw=8 and an
invalid description (the G2 contrast is non-vacuous); the other unmaintained individuals die before
the corruption tick, never re-instantiated because no corruption fires obs bit 2.

## What is established, and what is not

**Established:** the bank-rule convention is internalized. The masks and actions are stored in the
vulnerable, maintained description and read by the generic decode; no function on the reconstruction
path derives a mask or action from a bank index, and a degraded description is refused, not silently
re-materialized. This closes AC80's recorded residual (4).

**Not established, plainly:** (1) **content self-production** — the description's content (including
the masks/actions) is inherited at acquisition, not produced by the organism (AC78, untouched); (2)
recovery from catastrophic corruption of the description (AC61 one level down); (3) that the bank
rules are no longer four bank rules — what moved into the vulnerable state is their mask/action
content, not the fact that four bank rules exist (that is format).

## Verification

`audit_ac85.py` passes (64 rows, 14 source hashes no drift, arm invariants, decode==acquired for
12/12 priorities, gates recomputed without simulating); `replay_ac85.py` **6/6 exact**;
`test_ac85.py` green (12 tests, including `rebuild == acquired` bit-for-bit, the read-not-derive
source check, `rebuild -> None` on an invalid permutation and on a mask/permutation inconsistency,
description-repair-is-paid, and register exclusion); the AC core suite plus the AC71-86 line tests
pass.

## Artifacts

`ac85.py`, `AC85_PROTOCOL_v1.md`, `AC85_ENGINEERING_v1.md`, `ac85_engineering_v1/`,
`ac85_results_v1/`, `test_ac85.py`, `audit_ac85.py`, `replay_ac85.py`. Related: `AC80_RESULTS_v1.md`
(the residual this closes), `AC86_RESULTS_v1.md` (the order-preserving correction carried forward).
