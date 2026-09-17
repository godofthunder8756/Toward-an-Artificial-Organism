# AC81 results v1: components replaced across generations — frozen, all 8 gates pass

2026-09-17. Final seeds 4012-4015 (4 seeds x 2 histories = 8 individuals per condition), hashed
protocol `AC81_PROTOCOL_v1.md`, 16,384 ticks, sticky 1e-4 damage on the program bank and (for the
internalized and unmaintained arms) on the 78-bit description from an independent stream.
Engineering seeds (0-7) excluded. **All eight predeclared gates pass.**

## Gate outcomes

| gate | statement | result |
| --- | --- | --- |
| G1 | turnover (constructed + replaced): each component class born many times | **PASS** (survivors) |
| G2 | use (W repairs, C converts, B retains) | **PASS** (survivors) |
| G3 | partial-loss recovery (killed C + B rebuilt) | **PASS** (survivors) |
| G4 | recipe maintained (internalized 78/78, unmaintained <78) | **PASS** |
| G5 | maintenance load-bearing (unmaintained dies, internalized survives) | **PASS** |
| G6 | loop cut dies (`no_repair`) | **PASS** (8/8) |
| G7 | control clean (no loss, mechanism inert) | **PASS** |
| G8 | completeness and determinism | **PASS** (64 rows, re-run exact) |

## The measured arms (partial loss: kill 1 C + 5 B at t=8192)

| arm | survive | deaths |
| --- | --- | --- |
| `internalized` | **2/8** | 6782, 9083, 15229 (collapse) |
| `pristine` | 4/8 | 367, 400 (collapse) |
| `unmaintained` | **0/8** | 1243-2069 |
| `no_repair` | 0/8 | 408-1680 |

## What the two internalized survivors show (seed 4015, both histories)

| endpoint | value |
| --- | --- |
| W_birth / C_birth / B_birth | 1511 / 256 / 1683 (vs 3-16 / 3-4 / 20 initial) |
| C_birth_post / B_birth_post | 127 / 845 (the killed C + 5 B rebuilt, many times over) |
| repair writes / energy converted | 14,295 / 4,769 |
| routes | [1, 1] (both held) |
| W / C / B at end | 6 / 2 / 20 |
| description_correct | 78/78 (recipe intact) |

Every component class is born far more often than its complement — W ~95x its 16 slots, C ~64x its
4 slots, B ~84x its 20 sites — genuine multiple turnover cycles, and the components are used (W
repairs, C converts fuel, B retains both routes). The killed converter and boundary sites are
rebuilt, and the recipe is intact.

## The causal contrast

- `internalized` (recipe maintained) survives 2/8 with the recipe intact (78/78) and the components
  turning over.
- `unmaintained` (recipe degraded to 22-25/78) dies 0/8: without the production recipe, the
  organism cannot rebuild the lost components and dies.
- `no_repair` (loop cut) dies 0/8: the re-instantiation loop itself is load-bearing.

The production recipe is the description's words 3-5 (the W/C/B birth rules), read from the
vulnerable state by the generic decode — verified by the unit test (`rebuild` copies bits 28-69
verbatim) and the audit, so the replacement is driven by internally retained information.

## The honest caveat: this final family is collapse-dominated

The claim is gated on **survivors** (the paid description maintenance stops at death), and survival
is a bimodality-aware lower bound, not gated — exactly AC79/AC80. For this family the AC68 W/C
collapse dominates in the **unfavourable** direction (AC39's lesson): engineering seeds 0-7 gave
12/16 internalized survival, finals 4012-4015 give 2/8. The six internalized deaths are the W/C
collapse, which also kills `pristine` (4/8, two at t=367/400), not a recipe-maintenance failure —
and the description-repair spend shifts the cliff seed-dependently (seed 4012 collapses in
`internalized` at 6782 but survives in `pristine`).

So the replacement mechanism is established **in the survivors**, and the causal contrast is
categorical (unmaintained and no_repair die 0/8); the survival level of the maintained arm is the
known AC68 bimodality, reported as a lower bound. This does not establish content self-production
(AC78, untouched) and does not test recovery from destruction of every usable copy (catastrophic
analog, out of scope).

## Verification

`audit_ac81.py` passes (64 rows, 15 source hashes no drift, arm invariants, the production-recipe
link, gates recomputed without simulating); `replay_ac81.py` **6/6 exact**; `test_ac81.py` green
(production words == birth rules, rebuild copies them, rebuild == prog.program, partial-loss
semantics, gate shape, recorded freeze); AC core suite (56 tests) and the AC67-80 line tests (44)
all pass.

## Artifacts

`ac81.py`, `AC81_PROTOCOL_v1.md`, `AC81_ENGINEERING_v1.md`, `ac81_engineering.py`,
`ac81_results_v1/`, `test_ac81.py`, `audit_ac81.py`, `replay_ac81.py`. Related: `AC80_RESULTS_v1.md`
(the internalized recipe this builds on), `AC76_RESULTS_v1.md` (the turnover whose external recipe
AC80 internalized).
