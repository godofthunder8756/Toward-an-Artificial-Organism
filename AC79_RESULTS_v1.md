# AC79 results v1: description maintenance through paid vulnerable machinery — frozen, no hidden pristine backup

2026-09-17. Final seeds 4004-4007 (4 seeds x 2 histories = 8 individuals per condition), hashed protocol
`AC79_PROTOCOL_v1.md`, 16,384 ticks, sticky 1e-4 damage on the program bank and (for the maintained and
unmaintained arms) on the 8-bit description in bank 1, from an independent stream. Engineering seeds
(0-7) excluded. **All six predeclared gates pass.**

## Gate outcomes

| gate | statement | result |
| --- | --- | --- |
| G1 | `maintained` recovers (fw=0, description intact) in every survivor | **PASS** (2/2 survivors) |
| G2 | `unmaintained` fails (fw>0, descValid=0) in every alive-at-8192 individual | **PASS** (4/4) |
| G3 | maintenance load-bearing (unmaintained dies, maintained survives) | **PASS** (unmaintained 4/4 dead; maintained 2 survivors) |
| G4 | loop cut dies (`no_repair`) | **PASS** (8/8, deaths 449-704) |
| G5 | control clean (no corruption, mechanism inert) | **PASS** |
| G6 | completeness and determinism | **PASS** (64 rows, re-run exact) |

## The measured arms (with corruption at t=8192)

| arm | survive | alive at 8192 | recover (survivors) | deaths |
| --- | --- | --- | --- | --- |
| `maintained` | **2/8** | 4 | 2/2 (fw=0, description intact) | 562, 1788 (pre); 8436 (collapse) |
| `pristine` | **2/8** | 4 | 2/2 (fw=0) | 563, 7165 (pre); 8321 (collapse) |
| `unmaintained` | **0/8** | 4 | 0/4 (fw=8, descValid=0) | 8287-8325 |
| `no_repair` | 0/8 | 0 | — | 449-704 |

The heavy pre-8192 mortality (4/8 die at 562-1788 in every arm, 563-7165 in pristine) is the AC68 W/C
bimodality on these seeds, not a mechanism effect — the corruption intervention is at t=8192, after
these deaths, and they are bucketed separately per the repo rule. This final family is collapse-heavy
(2/8 = 25% survival) where the engineering seeds were survival-heavy (12/16 = 75%): AC39's
engineering-to-finals transfer failure in the unfavourable direction, and exactly the reason survival
is reported as a bimodality-aware lower bound rather than gated to a count.

## The clean contrast, and "as well as pristine"

Among the 4 individuals alive at t=8192, maintained and pristine are **per-individual identical on
recovery**:

| seed | maintained fw | pristine fw |
| --- | --- | --- |
| 4005 | 2 | 2 |
| 4006 | 0 | 0 |

Both arms recover the corrupted bits where the organism survives (seed 4006, fw=0), and both fail to
complete recovery where the organism is in the terminal W/C collapse (seed 4005, fw=2 — the collapsed W
leaves zero `8*interior_W` repair capacity, so the paid re-instantiation cannot run). The description
maintenance therefore neither helps nor hurts recovery relative to the pristine baseline: it removes the
hidden-backup privilege without costing the recovery. Maintenance is **sufficient** (G1) and
**necessary** (G2/G3): the unmaintained control's description degrades to an invalid permutation,
re-instantiation silently refuses, the frozen majority-restore cements the t=8192 corruption, and every
alive-at-8192 unmaintained individual dies 8287-8325 — the AC76 baseline death signature.

## The boundary (restated from the protocol)

The description is the terminal, non-regenerable reference: majority-restore cements its own
past-majority corruption (AC61 one level down) — the "catastrophic destruction" analog already out of
scope — not a hidden backup. There is no more-internal description to re-derive it from. This is not
content self-production (AC78: still blocked — the priority is externally supplied); it establishes only
that the description's *storage and maintenance* is endogenous.

## Gate-shape corrections (disclosed, not hidden)

Two endpoint-population corrections were made during finalization, both population-filter changes only
(the simulation is unchanged) and recorded in the protocol rather than applied silently:

1. **G5** first gated description integrity on individuals *alive at t=8192*; a deviating run (seeds
   4000-4003, preserved at `ac79_deviation_seeds4000_v1/`) showed a maintained individual can be alive
   at t=8192 and then die of the W/C collapse, after which the paid repair stops and the description
   degrades post-mortem. Corrected to *survivors* (`completed`).
2. **G1** had the same flaw in the corruption arm: an alive-at-8192 organism already in the terminal
   collapse cannot fund the re-instantiation, and pristine fails *identically* on such individuals.
   Corrected to *survivors* (`completed`), with non-vacuity carried by G3.

The deviating run's G1-G4 pass; only the mis-specified population filter failed. Both corrections are
principled (paid maintenance stops at death), not data-driven, and are recorded with the structural
reasons in `AC79_PROTOCOL_v1.md`.

## Verification

`audit_ac79.py` passes (64 rows, 14 source hashes no drift, arm invariants, gates recomputed without
simulating); `replay_ac79.py` **6/6 exact** (state_hash and endpoint fields); `test_ac79.py` 6 tests
green (including a unit test that the description repair is paid, that the register is excluded from
re-instantiation, and that the pristine arm reproduces AC76's regen arm byte-for-byte); full AC core
suite **533 tests pass**.

## Artifacts

`ac79.py`, `AC79_PROTOCOL_v1.md`, `ac79_results_v1/`, `test_ac79.py`, `audit_ac79.py`,
`replay_ac79.py`, `ac79_deviation_seeds4000_v1/` (disclosed deviating run). Related:
`AC79_ENGINEERING_v1.md` + `ac79_engineering.py` (the engineering result), `AC76_RESULTS_v1.md` (the
turnover whose "pristine description" caveat this closes), `DEPENDENCY_AUDIT_v1.md`,
`AC78_ENGINEERING_v1.md` (the falsified self-production premise this re-scopes away).
