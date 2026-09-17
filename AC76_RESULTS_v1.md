# AC76 results v1: the controller is regenerated from its internal description — turnover, frozen

2026-09-17. Final seeds 3000–3003 (4 seeds × 2 histories = 8 individuals per condition), hashed protocol
`AC76_PROTOCOL_v1.md`, 16,384 ticks. Engineering seeds (0–2) excluded. **All five predeclared gates pass.**

## Gate outcomes

| gate | statement | result |
| --- | --- | --- |
| G1 | `regen` recovers the corrupted bits | **PASS** (8/8, `flipped_still_wrong=0`) |
| G2 | `baseline` cements the corruption | **PASS** (8/8, `flipped_still_wrong=8`) |
| G3 | regeneration load-bearing (`no_repair` dies) | **PASS** (8/8, deaths 393–758) |
| G4 | control clean (no corruption) | **PASS** (8/8 both arms) |
| G5 | completeness and determinism | **PASS** (48 rows, re-run exact) |

## The measured arms

| arm (with corruption at t=8192) | survive | corrupted bits | program correct |
| --- | --- | --- | --- |
| `regen` (re-instantiation) | **8/8** | **0/8 wrong** | 125–126/126 |
| `baseline` (repair only) | **0/8** (deaths 8400–8422) | **8/8 wrong** | 94–98/126 |
| `no_repair` | 0/8 (deaths 393–758) | 8/8 wrong | 94–98/126 |

Flipping the majority of the first 8 program bits (rule 0's enabled bit + mask — the fuel-acquisition rule)
is **regenerated to correct** by the re-instantiation arm, where the single-bank majority-restore arm
**cements** it and starves to death (rule 0 disabled → no fuel response → energy drain). This is the
AC61 boundary crossed: the controller's content is re-derived from an internal description rather than
frozen at a corrupted majority.

**A secondary result worth stating:** in the control (no corruption), the baseline's program silently
drifts to 102–106/126 over 16,384 ticks (sticky-SET damage accumulating, majority-restore cementing the
drift), while the re-instantiation arm holds at 125–126. So regeneration does not only recover explicit
corruption — it *prevents* the gradual drift that self-referential repair is blind to.

## What is established, and what is not

**Established:** the controller-bearing component turns over. Its content is re-derived from a
16×-smaller internal description (the 4-bank priority) through the organism's own vulnerable, paid
machinery, recovering corruption past the self-repair threshold that majority-restore cements — and
preventing the drift that majority-restore accumulates. This is the §3 "endogenous component replacement"
property, now frozen rather than a feasibility probe.

**Not established, plainly:** (1) **content self-production** — the priority is still externally supplied,
so the organism re-derives its rules from an inherited description rather than producing the description
itself (AC73/AC30–33, untouched); (2) **recovery from catastrophic corruption** — the engineering found
flipping ≥16 bits at once is economically unrecoverable (the corruption idles the program and starves the
paid regeneration), consistent with the goal's "not recovery from complete destruction" scope; (3) the
description's own maintenance (the priority was pristine in this run) is unscoped.

## A bug caught and fixed before finalizing

The first final run used `dead_idx = 5 + priority.index(3)` for the register exclusion; the dead rule
actually sits at position `4 + …` after `ac9_priority_v2`'s rule reorder `[[0,1,2,3,5,6,7,8,4]]`, so the
first run excluded the wrong bits and re-instantiated the register (harmlessly — the register is all-0
in this no-move world, but incorrectly). The offset was corrected, the finals re-run, and the gates are
unchanged. Recorded here, not hidden.

## Verification

`audit_ac76.py` passes (48 rows, 12 source hashes no drift, gates recomputed without simulating);
`replay_ac76.py` **6/6 exact**; `test_ac76.py` 4 tests green (including a unit test that the register is
excluded from re-instantiation); full AC core suite **310 tests pass**.

## Artifacts

`ac76.py`, `AC76_PROTOCOL_v1.md`, `ac76_results_v1/`, `test_ac76.py`, `audit_ac76.py`, `replay_ac76.py`.
Related: `AC76_ENGINEERING_v1.md` (feasibility + economic limit), `AC76_DESIGN_v1.md` (the redesign),
`DEPENDENCY_AUDIT_v1.md` (the gap this closes, partially), `AC61` (the property this overturns).
