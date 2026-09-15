# AC22: the scaled world's declarative layer

2026-09-15. `ac22_world.py`, `test_ac22.py`. Feasibility/infrastructure. **No body, no organism
simulation, no protocol, no final seeds, nothing claimed.** This builds what the scaled world
*shows* and *demands*; it does not build the organism that would live in it.

## Where this sits

`AC20_BUDGET_v1.md` measured the requirement for a broader developmental function — both format
axes must be at least C + B — and `ac21_format.py` supplies the format, proven to reduce to the
frozen one. What was missing is the world those apply to. This is that world's declarative layer:
observation layout, demonstration, acquired target, and the declared format parameters.

## The declared scale

| quantity | value |
| --- | --- |
| constituent needs (C) | 6 |
| banks (B) | 6 |
| observation word | 12 bits |
| rules | 12 (= C + B, the measured requirement) |
| mask bits | 12 (= the word width, the measured requirement) |
| program size | 204 of the bank's 1024 bit-columns — fits, with room |

Acquired structure, which is the substance of "broader":

    frozen design   B = 4  ->  log2(4!) = 4.58 bits
    scaled design   B = 6  ->  log2(6!) = 9.49 bits

and the rule budget is no longer a knife-edge: 12 rules against a domain needing 12, versus 9
against a domain needing 9.

Measured: the scaled target reproduces its demonstration on **4096/4096** observations (the whole
2^12 space).

## Reducibility, and the two errors it caught

The discipline used throughout this project is that an extension must reproduce its parent before
anything rests on it. At the frozen scale **and with the frozen layout** the same construction
reproduces `ac5_program` exactly:

| check | result |
| --- | --- |
| installed bits vs `ac5_program.install_at_acquisition`, 24 permutations | identical |
| interpreted actions, 24 permutations x 512 observations | **0 mismatches** |

Reaching that took two failed attempts, and both were my errors of the same kind — treating a
supplied convention as something derivable:

1. **The observation layout is not "C constituents then B banks".** The frozen word is
   `[fuel, material, bank0, bank1, bank2, bank3, W, particles, boundary]`: the constituent need
   bits are `0,1,6,7,8` and the bank disagreement bits are `2,3,4,5`, interleaved. Assuming a
   contiguous layout produced **2890 mismatches**. The layout is now a parameter, with the frozen
   layout as a special case.
2. **The constituent actions are not `range(C)`.** The frozen mapping is fuel → 0, material → 1,
   W → 6, particles → 7, boundary → 8. Assuming sequential actions produced **2712 mismatches**.
   The action mapping is now a parameter too.

Both errors were caught by the reducibility check rather than by reasoning, which is the argument
for running the check: re-deriving a convention instead of reading it is a repeatable failure mode
here, and it produced two rounds of false mismatches that looked like physics problems.

A third, smaller lesson is encoded in the code: when the mask field is narrower than the
observation word, a rule *cannot* test the high bits, so the limit surfaces as an encoding error
unless masks are clamped to the field — in which case it surfaces as the coverage shortfall the
mask-axis measurement predicts. `target_rules` clamps, and a test asserts both halves
(`test_narrow_mask_cannot_address_the_high_banks`).

## What is not here, stated plainly

- **No body**: `ac4.Body` still has four banks; `ac9.step` still has the frozen constituents; no
  organism is simulated in this world. The scaled world cannot yet be run.
- **No protocol and no final seeds.** The parameters above are declared in this document; a
  protocol must declare them again before any final seed, per the project's discipline.
- **The two endpoints the open item names are untouched**, and are the reason the world is now
  built rather than merely specified: the next study must report *random-fallback survival* and
  *retention of the acquired function* separately, and at B = 6 the acquired structure is
  9.49 bits against 4.58, so a retention claim has more content than before.

## The next step

Integrate the scaled world into a body and step — more banks (with their parent sites in `life`),
more constituents, a 12-bit observation function, and repair actions for the new banks — with the
format parameters from this module, a protocol declaring C = 6, B = 6, rules = 12, mask_bits = 12
before any final seed, and the two endpoints reported separately. The frozen files stay untouched:
the scaled world is a new module, as this one is.

## Artifacts

`ac22_world.py`, `test_ac22.py`. Related: `ac21_format.py`, `AC21_FORMAT_v1.md`,
`ac20_budget.py`, `ac20_mask.py`, `AC20_BUDGET_v1.md`, `AC20_FEASIBILITY_v1.md`.
