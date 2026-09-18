# AC88 results v1: write_ctrl atomicity + resource-model defect fix — re-verification of AC87

2026-09-18. Final seeds 4028-4031 (4 seeds x 2 histories = 8 individuals per condition, 320 rows),
hashed protocol `AC88_PROTOCOL_v1.md`, 16,384 ticks, the same world and arms as AC87. This is NOT a
new experiment: it is the corrected implementation of the frozen AC87 design, fixing one
implementation defect found in review of dc3e428, and re-verifying that AC87's nine gates still
pass.

## The errata (old hash -> new hash)

`ac87.py` (frozen) sha256 `8b0a81ba8302479d2eab3eb17ec232df4b641ab2699a4bbc2e6b07200dc6c66d`
is replaced, for the succession-controller write only, by `ac88.py`
sha256 `8815834d22f2027887eef1244b8c364427da48dc52887cd6d37bf97989c57336`.
Every frozen dependency (`ac76.py`, `ac71.py`, `ac12.py`, `ac12_memory.py`, `ac9.py`,
`ac9_priority_v2.py`, `ac9_memory.py`, `ac5.py`, `ac5_program.py`, `ac4.py`, `ac4_transport.py`,
`ac1.py`) is unchanged; the protocol `AC88_PROTOCOL_v1.md` declares the fix and the source set.

## The defect (from review)

`ac87.py`'s `write_ctrl()` (the paid write of the 18-bit succession-controller word) was described
as atomic but was not: `n = min(len(sites), b.energy, b.material)` writes only the first `n`
replicas when energy or material cannot fund the whole transition, and the callers in `advance()`
ignore the return value. It also omitted the W-capacity limit every surrounding primitive applies
via `_cap(b) = min(32, 8*available_W, energy, material)`.

## The fix

The 18-bit controller word is split into MODE (active+phase, bits 0-3) and LAST (start timestamp,
bits 4-17). MODE is the load-bearing transition state, so `write_ctrl()` writes it all-or-nothing:
if energy or material cannot fund the full mode transition (at most 21 replicas), NOTHING is
written and the transition is refused and retried next tick — a partial mode is never observable.
LAST is rate-limit bookkeeping (read only by the SUCC_MIN_SPACING check while idle), so it is
written toward the target in energy/material-budgeted increments (the frozen behaviour). The resource model chosen (a modeling declaration; the review did not state this option): the controller register is the
coordinator's OWN working state, a distinct resource from the W-catalyzed CONTENT repair, bounded
by the register size (126 replicas), paid 1 energy + 1 material per replica, and not gated by 8*W —
the capacity the frozen AC87 protocol already declared ("written atomically, bounded by 18x7=126
replicas").

## Re-verification

| check | result |
| --- | --- |
| AC88 finals re-run (320 rows, seeds 4028-4031) | REPRODUCED |
| AC87's nine gates G1-G9 | 9/9 PASS |
| 320 rows byte-identical to frozen AC87 (state_hash) | 320/320 (0 diffs) |
| new atomicity/resource tests (`test_ac88.py`) | 9/9 PASS |
| audit (coverage, hashes, generic-decode, gates, AC87 re-verification) | passed |
| replay (sampled exact reruns) | 6/6 exact |

## Why the fix does not change the result

The MODE/last split is behaviour-preserving: the frozen write already ordered sites low-bit-first,
so a partial write only ever truncated the LAST field (mode was written first and fully funded in
every frozen call — measured, never a partial mode). Making MODE all-or-nothing therefore never
refuses in the frozen run, and LAST keeps its frozen budgeted-toward behaviour. The corrected
runner reproduces the frozen AC87 rows field-for-field, `state_hash` included.

A whole-word all-or-nothing version (an earlier engineering pass, preserved at
`ac88_results_v1_wholeword_atomic_prior/`) did NOT reproduce the result: it changed 22/320 rows and
G6 failed, because the frozen `ctrl_unmaintained` minority (>= 4) was in part the torn-LAST-field
left by the frozen partial writes — an artifact the whole-word fix removed. The MODE/last split
fixes the real defect (a partial MODE is now impossible) without removing that frozen behaviour.

## Boundary

No recovery from catastrophic recipe-content corruption, the four-bank-rule format, no content
self-production — all unchanged from AC87. The distinct-resource model is a declaration, not a new
empirical claim; the write is still paid in energy and material and the conservation identities
hold. The coordinator's metadata write is not W-catalyzed because it is the machine setting its own
register, not repairing content; the MODE field is the unit whose atomicity is enforced.

## Files

`ac88.py` (corrected runner), `AC88_PROTOCOL_v1.md` (hashed protocol), `test_ac88.py` (atomicity +
resource tests), `audit_ac88.py` (split audit incl. AC87 re-verification), `replay_ac88.py`
(sampled exact reruns), `ac88_results_v1/` (frozen rows, pre-run snapshot, results).
