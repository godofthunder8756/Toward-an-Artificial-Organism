# AC86 results v1: replacement of the information-bearing components (recipe succession)

Frozen 2026-09-17, seeds 4016-4019 (4 seeds x 2 histories = 8 individuals per condition), 16,384
ticks. Protocol `AC86_PROTOCOL_v1.md` (rev 1.1), engineering `AC86_ENGINEERING_v1.md`. All 7 gates
pass. Audit passed (48 rows, no hash drift); replay 6/6 exact.

## Result

The recipe-bearing storage is a replaceable component. Every `succession` individual (8/8 survive)
performs 7 complete replacement cycles across the 16,384-tick horizon — the 78-bit description is
copied to a fresh slot, the copy verified valid and bit-correct, the generation pointer switched to
it, and only then is the old copy cleared. All four slots are cycled (final pointer = 3), and the
recipe ends correct (78/78) in every survivor. The `repair` arm (in-place majority-repair, no
succession machinery) also keeps 78/78 with zero successions; the `unmaintained` arm (no repair, no
succession) loses the recipe (23-46/78) and dies 8/8. The no-damage control is byte-identical
across arms (0 successions, 78/78, state_hash equality): the mechanism is inert.

## Frozen rows (per-individual summary)

| arm | survive | successions | description | pointer | first_dead |
| --- | --- | --- | --- | --- | --- |
| `succession` | 8/8 | 7 each | 78/78 | 3 (4 slots cycled) | — |
| `repair` | 8/8 | 0 | 78/78 | 0 | — |
| `unmaintained` | 0/8 | 0 | 23-46/78 | 3 (drifted) | 1754-2273 |

With `damage=False`, all three arms: 8/8 survive, 0 successions, 78/78, pointer 0, and `succession`
is byte-identical to `repair` (per-individual `state_hash` equality).

Succession provenance (every survivor, every completed cycle): `verified_valid == 1` and
`target_correct == 1`; `remove_tick >= switch_tick >= copy_done >= start` in every cycle. The
succession writes are paid and W-catalyzed: `succ_writes` 2104-2109 per individual over the horizon,
alongside `reg_writes` 1657-1805 and total writes ~18,150-18,280. `program_correct` = 122/122 static
bits (the 4 register bits are dynamic decision state and excluded; the 2 pointer bits live in bank
1, not the program bank).

## Gates

- **G1 (succession occurs)** PASS — 7 >= 2 in every completing `succession` individual.
- **G2 (successor functional)** PASS — every cycle verified valid and correct; ends 78/78, valid.
- **G3 (remove after verify)** PASS — ordering invariant holds in every cycle.
- **G4 (recipe maintained)** PASS — `succession`/`repair` 78/78; `unmaintained` 23-46 < 78.
- **G5 (succession is the replacer)** PASS — `repair`/`unmaintained` 0 successions; `succession` 7.
- **G6 (control clean)** PASS — no-damage control inert, byte-identical `succession`==`repair`.
- **G7 (completeness, determinism)** PASS — 48 rows; first individual reproduces exactly.

## The pointer-drift correction (disclosed, pre-freeze)

The first final-seed run exposed a real bug: the generation pointer was originally stored in the
program bank's dead rule (mask bits 6-7). There it is damaged by the *program* stream — which runs
even in the `damage=False` control — but repaired only by action 2's whole-bank majority-restore
(obs bit 2, `>=4` minority across 126 bits), far too slow for a 2-bit pointer. The no-damage control
seed 4019 drifted to pointer=2 (a 4/7 flip cemented), reading slot 2 instead of slot 0, giving
desc=57 and failing G6. The fix: the pointer lives in **bank 1** (recipe storage, offset 312-313),
damaged by the recipe stream (which `damage` actually controls) and maintained by its own
minority-count trigger (`pointer_minority >= POINTER_TRIGGER`), folded into the same paid
majority-restore machinery as the description. This is a faithful description of a bug-corrected
design, not a gate change; the protocol records it as revision v1.1 and the run was re-frozen.

## Boundary (unchanged from protocol)

The succession does not claim recovery from catastrophic recipe-content corruption — a successor is
a copy of the active slot's majority, so a majority-flipped description bit would be copied
faithfully (AC61 one level down). The generic decode still derives the four bank rules from the
permutation by the architectural convention (supplied machinery, not stored state — AC80's residual
4). The succession machinery (copy/verify/switch/remove) is supplied format-level machinery; what is
demonstrated is that the recipe-bearing storage is replaceable and the replacement is paid,
W-catalyzed, and performed on vulnerable state. No content self-production claim (AC78 still
blocked); this is turnover of the recipe substrate, not discovery of a better recipe.

## Files

- `ac86.py` — runner (frozen, hash 6dffa1d2...)
- `AC86_PROTOCOL_v1.md` — protocol rev 1.1 (hash edec18f3...)
- `AC86_ENGINEERING_v1.md` — engineering write-up
- `test_ac86.py` — 14 tests (layout, order-preserving decode, succession, pointer maintenance, gates)
- `audit_ac86.py` — split audit (re-derives coverage/invariants/hashes/gates without simulating)
- `replay_ac86.py` — sampled exact reruns (6/6 exact)
- `ac86_results_v1/` — frozen rows, pre-run snapshot, results
