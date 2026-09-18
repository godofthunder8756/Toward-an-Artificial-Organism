# AC84 results v1: component turnover reported unconditionally — frozen, all 6 gates pass

2026-09-17. Final seeds 4020-4023 (4 seeds x 2 histories = 8 individuals per condition, 24 rows),
hashed protocol `AC84_PROTOCOL_v1.md`, 4096 ticks, sticky 1e-4 damage on the program bank and (for
the internalized and unmaintained arms) on the 78-bit description from an independent stream.
Engineering seeds (0-127) excluded. **All six predeclared gates pass.**

This is milestone 2 re-established without the survivor-conditioning weakness that AC81 carried:
AC81 gated its turnover claim (G1-G3) on `completed`, so the claim rested on 2/8 survivors. AC84
scores turnover and use on **every individual, dead or alive** — no `completed` filter — and drops
the t=8192 kill intervention entirely (the components turn over continuously with no intervention).

## Gate outcomes

| gate | statement | result |
| --- | --- | --- |
| G1 | turnover, unconditional: every internalized individual (dead or alive) fully replaces each class (births >= complement) | **PASS** (8/8, incl. the two collapse deaths) |
| G2 | use, unconditional: every internalized individual repairs, converts, binds both routes | **PASS** (8/8) |
| G3 | loop load-bearing (`no_repair` dies) | **PASS** (8/8) |
| G4 | recipe degrades when unmaintained (`description_correct < 78`) | **PASS** (8/8) |
| G5 | recipe maintained in survivors (`description_correct == 78`) | **PASS** (6/6 completers) |
| G6 | completeness and determinism | **PASS** (24 rows, re-run exact) |

## The measured arms (no intervention, 4096 ticks)

| arm | survive | deaths | turnover (births) | description |
| --- | --- | --- | --- | --- |
| `internalized` | **6/8** | 3464 (W/C collapse, both histories of seed 4021) | W 293-361, C 50-64, B 337-418 | 78/78 |
| `unmaintained` | 0/8 | 1400-3148 | W 87-266, C 18-46, B 118-299 | 65-72/78 |
| `no_repair` | 0/8 | 589-793 | W 71-90, C 25-34, **B 0** | 65-72/78 |

## The unconditional turnover claim

Every `internalized` individual — including seed 4021, which dies at t=3464 of the AC68 W/C
collapse with the recipe **intact** (78/78) — fully replaces each component class over the horizon:
W births 293-361 against 16 slots (~18-23x), C births 50-64 against 4 slots (~13-16x), B births
337-418 against 20 sites (~17-21x). Turnover is therefore demonstrated across the whole cohort, not
a survivor subset. Use is likewise unconditional: every individual repairs (writes 1611-3030),
converts energy (930-1125 units), and binds both routes during development (first_acquire 39-99).

The one internalized death (seed 4021, both histories, at t=3464) is the fragility finding the
protocol anticipated: its turnover (W 293, C 50, B 337) far exceeds the floors, so the collapse did
not prevent turnover from being observable — it is reported as a finding about the body's fragility,
not used to gate. The multiple-turnover-cycles claim is reported per individual (18-23x for the
healthy cohort), not gated.

## The causal contrast (recipe drives the turnover)

- `internalized` turns over unconditionally and holds the recipe (78/78 in survivors).
- `unmaintained` degrades the recipe (65-72/78) and dies 8/8: without maintenance, the production
  recipe is lost and turnover is not sustained.
- `no_repair` (loop cut) dies 8/8 with **B_birth = 0** in every individual — the reconstruction loop
  is load-bearing, and cutting it halts boundary turnover entirely.

The production recipe is the description's words 3-5 (the W/C/B birth rules), read from the
vulnerable state by the generic decode — verified by the unit test (`rebuild` copies bits 28-69
verbatim) and the audit — so the replacement is driven by internally retained information.

## Boundary (unchanged, restated)

Content self-production is not claimed (AC78, untouched). The description is the terminal
non-regenerable reference (AC61 one level down). The bank rules are still synthesized by the
architectural convention (AC80's residual). This is replacement of the physical components driven by
the inherited, maintained recipe — not discovery of a better recipe.

## Verification

`audit_ac84.py` passes (24 rows, 15 source hashes no drift, arm invariants, the production-recipe
link, the unconditional-turnover floor, gates recomputed without simulating); `replay_ac84.py`
**6/6 exact**; `test_ac84.py` green (8 tests, including a test that pins G1 to the full cohort — a
dead individual meeting the floors still passes, a below-floor dead individual still fails); the AC
core suite (56 tests) and the full 571-test suite both pass.

## Artifacts

`ac84.py`, `AC84_PROTOCOL_v1.md`, `AC84_ENGINEERING_v1.md`, `ac84_results_v1/`, `test_ac84.py`,
`audit_ac84.py`, `replay_ac84.py`. Engineering probes: `ac84_eng_probe.py`, `ac84_eng_verify.py`,
`ac84_eng_scan.py`, `ac84_eng_broad.py`, `ac84_engineering_v1/`. Related: `AC81_RESULTS_v1.md`
(the survivor-gated milestone-2 result this strengthens), `AC80_RESULTS_v1.md` (the internalized
recipe).
