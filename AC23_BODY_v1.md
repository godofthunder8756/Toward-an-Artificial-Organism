# AC23: the scaled body layer, and a correction to how I had described the observation

2026-09-15. `ac23_body.py`, `test_ac23.py` (11 tests). Infrastructure. **No step, no simulation,
no protocol, no final seeds, nothing claimed.** This builds the body the scaled world needs and
proves it reduces to the frozen body. It does not build an organism that could run.

## The correction, first, because it matters more than the build

Throughout AC22 I described the frozen observation as "fuel, material, then a disagreement bit per
bank at 2-5, then W, particles, boundary". **That is `ac4.observe`. It is not `ac9.observe`,** which
is the function the whole AC9-onward line actually uses. Reading it properly:

| bit | `ac9.observe` |
| --- | --- |
| 0 | `fuel <= 8` |
| 1 | `material <= 64` |
| 2 | the **program bank's** disagreement: `min(ones, 7-ones).sum() >= 4` over `traces[0,:126]` |
| 3 | memory urgency, region 0 — a slot near expiry (`0 < life <= 16`) or disagreeing with its decode |
| 4 | memory urgency, region 1 |
| 5 | **never set** |
| 6 | W low — core group under 2 sites, or a region with demand under 3 |
| 7 | particles under 2 |
| 8 | `boundary.min() <= 64` |

Two consequences worth recording:

- **AC12's mask-32 rule is dead *by construction*, not by accident.** Bit 5 cannot be set, so the
  rule conditioned on mask 32 can never fire. That was an observed fact in AC12 (the "dead rule"
  in the frozen program); this is the mechanism.
- **The AC22 reducibility check passed while my stated semantics were wrong.** It compares
  installed program *bits*, and the frozen program uses masks `4<<bank` (bits 2-5) for its four
  bank rules — which is true of the mask layout regardless of what those observation bits mean. So
  the bits matched and the labels did not. A check can pass for a different reason than the one
  assumed, and this is a clean example: the correct conclusion from AC22's numbers ("the
  construction reproduces the frozen program") was right, the explanation attached to it was not.

The general lesson, now at the third instance in this sequence: **a supplied convention is data,
not something to re-derive.** The frozen layout, the frozen action numbering, and now the frozen
observation semantics were each reconstructed from memory and each was wrong; reading the source
settled each one immediately.

One piece of arithmetic surfaced while testing, and it connects to AC19:

    a single bit with minority replicas contributes min(ones, 7-ones) <= 3 to the disagreement
    sum, so bit 2 needs at least TWO disagreeing bits to reach the threshold of 4

which is why the corruption model in AC19 had to be a 4-of-7 flip and why corruption spread thinly
across many bits read differently from corruption concentrated in one.

## What the body layer now is

Frozen body, read rather than assumed: `life = [32,48,64,0]*4 + [64,96,128,0]` — **four parent
sites per bank** for four banks (0-15), then **four particle slots** (16-19). `available` slices
`a[4*bank:4*bank+4]` per bank and the step reads particles as `a[16:]`, so the frozen 16 is exactly
`4 * banks` and the layout scales without a shift: with B banks, bank sites are `0..4B-1` and
particles begin at `4B`.

`ac23_body.py` supplies:

- `Body` (traces, life, pos, boundary, energy, material, fuel, dead) with `digest` and `inventory`;
- `available`, unchanged — the frozen formula only ever used the body's own shapes;
- the scale inferred **from the body** (`banks_of`), so nothing carries a hard-coded 4;
- the observation word assembled from **named quantities placed at declared bits**, with the frozen
  five constituent positions and the program/urgency positions preserved;
- the added quantities — one constituent and two banks — declared as such, with the added
  constituent's formula explicitly flagged as a placeholder the world build may change;
- `acquire` that returns the true frozen body at the frozen counts and **raises** beyond them,
  because a silent fallback to four banks would make every scaled measurement meaningless.

## Reducibility

| check | result |
| --- | --- |
| observation word vs the real `ac9.observe`, 600 randomized states over 3 seeds | **0 mismatches** |
| frozen eight bits unchanged by the scaled extension | holds over 100 randomized states |
| bit 5 unset over 300 randomized states | holds |
| `available` vs `ac4.available` | identical |

"0 mismatches" is against the actual function, not against my description of it — which is the
whole point, given how the description went.

## Not built, plainly

- **No scaled acquisition** (`ac24`): no body with six banks, no parent sites for the added banks,
  no widened particle array. `acquire(banks=6)` raises.
- **No step**: no reactions, no conservation accounting, no `needs`/`spend`/`balance`. The scaled
  world cannot be run, and this module does not pretend otherwise.
- **No protocol, no final seeds, no claims.** The AC22 parameters (C = 6, B = 6, rules = 12,
  mask_bits = 12) are the target and must be declared again in a protocol before any final seed.
- **The two endpoints the open item names** — random-fallback survival and retention of the
  acquired function — remain untouched, and remain the reason for building the world at all.

## The next step

`ac24`: the scaled acquisition and the step. Build the six-bank body with parent sites for every
bank and bank-3..5 parent sites representing the added constituent's reserve; extend the
observation to its full 12 bits (bit 9 for the added constituent, bits 10-11 for banks 4-5); carry
the conservation laws unchanged and assert the balance identity as a test. Then a protocol
declaring the scale before any final seed, with the two endpoints reported separately.

## Artifacts

`ac23_body.py`, `test_ac23.py`. Related: `ac22_world.py`, `AC22_WORLD_v1.md`, `ac21_format.py`,
`AC21_FORMAT_v1.md`, `AC20_BUDGET_v1.md`.
