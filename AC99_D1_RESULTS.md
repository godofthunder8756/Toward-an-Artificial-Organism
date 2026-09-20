# AC99-D1 — reserve-release atomicity: release and disarm succeed or fail together

## The defect (reproduced on the frozen `ac98.py`, then fixed in `ac99.py`)

`release_reserve()` in `ac98.py` credited `RESERVE_LEVEL` material to the spendable pool, then
called `write_reserve(o, e, 0)` and **ignored its return** (`ac98.py:147`). When the disarm write
is refused — W=0 ⇒ `ac95._cap` = 0, or energy/material < the ≤7 differing replicas — the material
is credited but the bit stays armed, so a second release credits again.

Reproduction (single-step, W=0, pool collapsed to 3 material, one prior arm = 21 withheld):

```
release 1 returns 21, release 2 returns 21
material after two releases: 45        (3 -> 24 -> 45: 42 credited)
reserve_released_m: 42                 (against 21 withheld)
bit still armed: 1
G4 released<=withheld: False
```

21 → 42 with only 21 withheld — the G4 endogenous invariant (released ≤ withheld, no injection) is
violated by construction in the refusal path.

## The fix

`ac99.py` (a copy of `ac98.py`; the freeze is untouched — `ac98.py` sha256
`1ae3d37…` is unchanged and `audit_ac98.py` still passes with no drift). `release_reserve` now
rolls the release back if the disarm write is refused, mirroring `arm_reserve`:

```
b.material += rel;  e['in_m'] += rel;  e['reserve_released_m'] += rel
if not write_reserve(o, e, 0):
    b.material -= rel;  e['in_m'] -= rel;  e['reserve_released_m'] -= rel
    return 0
return rel
```

## Funding-of-disarm decision: option (a) — fund the disarm from the released material

The three options were (a) fund the disarm from the released material before crediting the
remainder, (b) refuse the release if the disarm cannot be paid from the pre-release pool, (c)
something else. **Chosen: (a).**

Justification: the release exists precisely to fund the drop when the spendable pool has
*already collapsed*. Under (b) the disarm write would be refused on exactly that state (material
< 7), so the reserve could never be released when it is needed — a self-deadlock that defeats the
reserve's purpose. Under (a) the credit lands first, the disarm pays its ≤7 replicas out of that
credit (net pool gain = `RESERVE_LEVEL − replicas`), and the rollback fires only when the write is
refused for a reason the credit cannot fix (W=0 ⇒ cap 0, or energy short). The implementation is
credit-then-write-then-rollback, which is literally (a): the disarm's write cost is funded from the
just-released material, with the remainder (rel − n) left in the pool.

## Inertness on the successful path (byte-for-byte)

The fix changes behavior only in the refusal case. Verified that the refusal case never fires in
the AC98 finals: running the reserve arm on all 8 final individuals (4436–4439 × 2 histories),
`ac99` reproduces `ac98` **byte-for-byte** (8/8 `state_hash` equality, `reserve_released_m` 21/21
on every individual). The single-step successful release also matches `ac98` field-for-field
(material, energy, `reserve_released_m`, `spent_m`, bit read).

## Tests (`test_ac99.py`, 6 tests, 0.004 s — all green)

- `test_refused_disarm_credits_nothing_and_stays_armed` — W=0 ⇒ `_cap`=0: release returns 0,
  material unchanged, `in_m` and `reserve_released_m` unchanged, bit still armed. (The reviewer's
  reproduction now fails on `ac98` and passes on `ac99`.)
- `test_no_double_release_21_to_42` — two refused releases credit 0 in total (ac98 credited 42
  against 21 withheld).
- `test_conservation_released_never_exceeds_withheld` — G4: released (0) ≤ withheld (21) after a
  refused release.
- `test_successful_release_unchanged_from_ac98` — release 21, disarm paid from the credit (7), net
  material 3+21−7=17, bit disarmed.
- `test_successful_release_matches_ac98_field_for_field` — independent ac98 vs ac99 single-step
  releases agree exactly (proves inertness where the disarm succeeds).
- `test_arm_refuses_when_no_W_and_rolls_back` — `arm_reserve`'s existing rollback is unchanged.

## Conservation / G4 under the fix

`reserve_released_m` is incremented only on a successful release and fully restored on rollback, so
the released ≤ withheld invariant holds in the refusal path by construction (the reproduction above
now yields released 0 ≤ withheld 21). `arm_reserve`'s withholding-rollback is untouched. The G4 gate
("no external rescue, release never exceeds withhold") is therefore preserved under the fix.

## Scope notes (unchanged from AC98, not part of D1)

The partial-release edge in `release_reserve` — `rel = min(RESERVE_LEVEL, 256 − material)` can be <
21 when material is near the 256 cap, releasing less than the full withheld amount while still
disarming — is pre-existing, released ≤ withheld still holds, and it is out of D1's scope. The
reserve arm, no-reserve control, and all release triggers are otherwise byte-identical to AC98-D2.
