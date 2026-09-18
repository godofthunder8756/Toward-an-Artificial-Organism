# AC88 protocol v1: defect-fix of AC87's write_ctrl (atomicity + resource model), re-verification

STATUS: **frozen before the first re-verification seed.** Written 2026-09-18. This is NOT a new
experiment and NOT another internalization step. It is the corrected implementation of the frozen
AC87 design, fixing one implementation defect found in review of dc3e428, and re-verifying that
AC87's nine gates still pass. The AC87 design, arms, seeds, and gates are unchanged.

SOURCES (declared): ac88.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC88_PROTOCOL_v1.md

## The defect (from review of dc3e428)

AC87's `write_ctrl()` (the paid write of the 18-bit succession-controller word, `ac87.py` lines
263-278) was described as atomic but was not:

```python
sites = np.argwhere(b.traces[1, CTRL_OFFS] != c[:, None])
n = min(len(sites), b.energy, b.material)   # NO W-capacity limit
if n:
    idx = sites[:n]                          # partial write if energy/material insufficient
    ...
```

If energy or material could not fund the whole transition it wrote only the first `n` replicas and
returned; the callers in `advance()` ignore the return value, so a partially-changed phase or
last-start timestamp could be left in the substrate. It also omitted the W-capacity limit every
surrounding primitive applies via `_cap(b) = min(32, 8*available_W, energy, material)`. Passing the
AC87 tests therefore did not establish atomicity or the resource model.

## The fix (declared before the re-run)

1. **Atomicity for the MODE field — all-or-nothing.** The 18-bit controller word is two fields:
   MODE (active+phase, bits 0-3) and LAST (start timestamp, bits 4-17). The MODE field is the
   load-bearing transition state (a partial mode -- phase read as a different valid phase
   mid-transition -- is what corrupted the first AC87 build), so `write_ctrl()` writes it
   all-or-nothing: if energy or material cannot fund the full mode transition (at most 21 replicas),
   NOTHING is written and the transition is refused (retried next tick). A partial mode is never
   observable. The LAST field is rate-limit bookkeeping (read only by the SUCC_MIN_SPACING check
   while idle, ~300 ticks after a start), and a partially-updated timestamp is still a valid 14-bit
   integer that cannot corrupt the state machine, so it is written toward the target in
   energy/material-budgeted increments -- the frozen behaviour, like `write_toward_slot`.

2. **Resource model — distinct resource, stated explicitly.** The controller register is the
   succession coordinator's OWN working state, its program counter. It is a distinct resource from
   the W-catalyzed CONTENT repair (`ac4.react` actions 2-5, where the 8*W term is the repair
   catalyst's per-action capacity). The controller write is bounded by the register size itself
   (18 bits x 7 = 126 replicas), pays the same physical price (1 energy + 1 material per replica, so
   the conservation identities hold), and is NOT rate-limited by 8*W because it is the machine
   setting its own register, not repairing content. This is the resolution the frozen AC87 protocol
   already declared ("the controller-state word is written atomically, bounded by 18x7=126
   replicas"); the defect was that the implementation silently wrote a partial word (including a
   partial MODE when energy/material fell below the mode transition) and never stated the resource
   model. The reviewer's three resolutions were (a) shrink the word, (b) split into atomic
   sub-steps, (c) declare a distinct resource; (c) is chosen for the capacity question because it is
   the frozen design and (a)/(b) would change the word size or the write timing and so alter the
   frozen result, while the MODE/last split is the (b)-style atomic sub-step that makes the
   load-bearing transition all-or-nothing without changing the frozen behaviour. The distinct-
   resource model is pinned by unit test (see below).

## Arms, world, seeds, gates

Unchanged from AC87: five arms (`succession`, `repair`, `ctrl_unmaintained`, `unmaintained`,
`no_repair`), damage/corrupt/transition conditions, world constants (PORTS=4, YIELD=64, TICKS=16384,
sticky 1e-4 damage on both banks from independent streams, DESC_TRIGGER=2, POINTER_TRIGGER=2,
CTRL_TRIGGER=2, SLOTS=4, SUCC_MIN_SPACING=2400, SUCC_BUDGET=6), and the same nine prespecified
gates G1-G9 (`ac88.gates`, copied verbatim from `ac87.gates`). Final seeds `4028, 4029, 4030, 4031`
(4 seeds x 2 histories = 8 individuals per condition, 320 rows), disjoint from every prior family.

New unit tests (`test_ac88.py`, not hashed — AC17's rule) that FAIL on the old `ac87.write_ctrl`:

- (i) energy too small for the MODE transition -> nothing written (no partial mode; energy/material
  unchanged).
- (ii) material too small for the MODE transition -> nothing written (no partial mode;
  energy/material unchanged).
- (iii) the distinct-resource model is pinned: with W = 0 and sufficient energy/material the write
  PROCEEDS (the coordinator's register write is not gated by 8*W); this is the frozen declaration,
  not a new claim.
- (iv) the machine is well-defined on ANY controller word: spurious active/phase values do not crash
  or corrupt the succession machinery.

## Anti-drift rules

- The runner creates `ac88_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the hashed set.
- `test_ac88.py` is not hashed. If a gate fails, it fails. This protocol may not be edited after the
  first re-verification seed.

## Errata record (computed at freeze time)

`ac87.py` (old) sha256 and `ac88.py` (new) sha256 are recorded in
`ac88_results_v1/pre_run_snapshot.json`, alongside the source hashes, and restated in
`AC88_RESULTS_v1.md`.

## Source hashes (computed before the first re-verification seed)

    (recorded in ac88_results_v1/pre_run_snapshot.json at freeze time)
