# Compact vulnerable program primitive

2026-09-15. Implemented prerequisite, not an adaptive-system result.

`ac5_program.py` replaces the conceptual 512-row truth table with nine ordered
rules: enabled bit, nine-bit condition mask, four-bit action. The representation
uses126 logical bits (882 replica sites), with protected generic fallthrough to
REST. Five rules cover fuel/material/W/C/B, four cover memory-bank repair.
The rule order encodes the same acquired permutation. No increase in acquired
history or autonomous need discovery is claimed.

Three tests verify:

- Exact action equivalence with AC4 across all24 permutations and512 observations
  (12288 comparisons).
- Disabling the boundary rule changes the selected action and costs seven replica
  replacements, seven energy and seven material units. Majority corruption of
  that enabled bit changes behavior again; no protected intended rule restores it.
- Updates fail without catalytic capacity or sufficient resources and preserve
  state exactly when rejected.

This is a storage/evaluation primitive only. It has not replaced the controller
inside an AC4 run and does not perform learning. The initial demonstration
installer must never serve as a live repair target. The write primitive accepts
a W count from its caller; the future integrated caller must derive that count
from interior physical constituents. No isolation guarantee follows from this API.

Integration must charge living/learning time as well as effective replica writes,
prevent learning plus repair from exceeding an action's capacity, and include
all learned timers/values/eligibility state in the erasure boundary. Non-atomic
multi-action updates need explicit semantics. Existing protected host arrays
cannot become hidden memory for an otherwise vulnerable learner.

The primitive preserves the existing memory-bank allocation for now; smaller
program length does not imply a matched reduction in total exposed state or a
measured robustness improvement. It must be tested in the actual maintenance
architecture before claiming any adaptive merit.

Reproduce: `py -3.12-arm64 -B -m unittest -v test_ac5_program`.
[Source](ac5_program.py), [tests](test_ac5_program.py),
[adaptation design](AC5_ADAPTATION_DESIGN_v0_1.md).
