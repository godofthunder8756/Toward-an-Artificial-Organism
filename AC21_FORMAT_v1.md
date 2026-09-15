# AC21: a parametric rule format, proven to reduce to the frozen one

2026-09-15. `ac21_format.py`, `test_ac21.py`. Feasibility/infrastructure only — no world, no
protocol, no final seeds, nothing claimed. This supplies the format width the previous two
measurements said a broader developmental function needs, and it proves the extension is a
generalization rather than a replacement.

## What the two prior measurements asked for

- `AC20_FEASIBILITY_v1.md`: at four banks the *format* is not the constraint — five fixed slots
  plus four free slots reproduces essentially every preference structure derivable on a
  four-element domain, so the narrow thing is the demonstration (4.58 bits), not the format.
- `AC20_BUDGET_v1.md`: the format nonetheless binds at the very first *growth* of the domain.
  Full routing needs `C + B <= 9` slots, and the present design sits exactly on that boundary
  (`C = 5`, `B = 4`, nine rules). A second, independent limit is the mask width: the word is
  `1 + 9 + 4 = 14` bits, so a rule conditions on at most nine observation bits.

So a broader world needs a format wider on **both axes**, and the required scale is now specified
rather than guessed: **slots >= C + B, mask bits >= the observation word width.**

## What this module does

Generalizes the frozen layout exactly — `word = enabled | mask << 1 | action << (1 + mask_bits)`,
`word_width = 1 + mask_bits + 4`, packed into the program bank and interpreted first-match-wins
with action 9 as the interpreter's fallthrough — with `rules` and `mask_bits` as parameters.
Nothing else about the frozen conventions changes.

## Reducibility, measured

At the frozen parameters (`rules = 9`, `mask_bits = 9`) the module must be the frozen format, and
that is checked rather than asserted:

| check | result |
| --- | --- |
| installed bit patterns vs `ac5_program.install_at_acquisition`, all 24 permutations | **identical** |
| interpreted actions vs `ac5_program.choose`, all 24 permutations x 512 observations = 12,288 pairs | **0 mismatches** |
| unit tests (`test_ac21.py`) | 8 pass |

## Capacity, and a correction to my own earlier claim

I previously wrote that a widened format "needs 140 of the 126 bits the bank provides, so the
broader function requires a declared storage extension." **That was wrong.** The bank has 1024
bit-columns; 126 is merely what the frozen nine-rule format *occupies*. Measured:

| mask bits | 9 rules | 13 rules | 17 rules | 21 rules |
| ---: | ---: | ---: | ---: | ---: |
| 9 | 126 | 182 | 238 | 294 |
| 11 | 144 | 208 | 272 | 336 |
| 13 | 162 | 234 | 306 | 378 |
| 16 | 189 | 273 | 357 | 441 |

Every one of those fits in 1024 bit-columns. So the extension costs **no storage change at all** —
it is a declared change of two parameters, `rules` and `mask_bits`, with the encoding and the
interpreter generalizing the frozen ones bit for bit. At the scales the budget analysis identified
(`C + B` in the teens, observation words up to 16 bits) the bank is not a limit.

## What is not here, stated plainly

No larger world: no additional constituents, no additional banks, no wider observation function,
no organism simulation. This is the format only. The world build is the next step and will be
parameterized on this module — with the two endpoints the open item names kept separate
throughout (random-fallback survival, and retention of the acquired function), and with a
protocol declaring `C`, `B`, `rules` and `mask_bits` before any final seed.

## Artifacts

`ac21_format.py`, `test_ac21.py`. Related: `ac20_feasibility.py`, `AC20_FEASIBILITY_v1.md`,
`ac20_budget.py`, `AC20_BUDGET_v1.md`.
