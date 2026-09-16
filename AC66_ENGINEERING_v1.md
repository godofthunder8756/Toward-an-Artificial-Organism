# AC66 engineering: the permutation's domain is real but narrow and marginal

2026-09-15. Engineering prerequisite. **No protocol, no final seeds, no claim.** Completes AC65's
investigation of where (if anywhere) the learned permutation order is the right decision rule.

## The question

AC65 found a value-blind earliest-deadline-first rule dominates the learned permutation in the schedulable
regime (it hits the ceiling at every stress level). AC66 asks the converse: is there a regime where the
permutation *beats* the deadline rule — where the developmental-function line's "order" is actually the
right object?

## The answer, measured

Two changes are needed for the permutation to win: (1) remove the stress-rescue quirk (stress sets a site
to `min(life, 16)`, pure damage, so a near-expiry site is not extended), making the world non-schedulable;
(2) make the critical region **rare-urgent** (low-stress), so its survival depends on priority rather than
on being frequently urgent. At stress multiplier 26 the permutation `OPT5 = (5, 1, 2, 4, 3, 0)` beats the
deadline rule:

| family | OPT5 (permutation) | deadline-first | median diff | p | impaired |
| --- | --- | --- | --- | --- | --- |
| ENG1 | 63,571 | 60,428 | 3,635 | 0.059 | 3/12 |
| ENG2 | 63,475 | 58,177 | 5,642 | 0.102 | 5/12 |

0 dead in all arms. The permutation wins on average (~5–9%) by keeping the rare-urgent critical region
alive while sacrificing the low-value tail — but the advantage is **not resolvable** (p above 0.01) and is
**inconsistent** (the deadline rule beats the permutation on 3–5 of 12 seeds).

## What this closes

The developmental-function line's object — the learned permutation order — has a **narrow and marginal
domain**:

- In schedulable worlds it is *dominated*: earliest-deadline-first reaches the ceiling, the best
  permutation does not (AC65).
- In non-schedulable worlds with a rare-urgent critical region it is *marginally better* (~5–9%, not
  resolvable), by choosing which scarce sites to sacrifice.

So the "order" is the right decision rule only in a corner — a scarce world where the thing worth
protecting is the thing a reactive rule is most likely to miss — and even there its advantage is a weak,
inconsistent one. The developmental-function claims (AC55/AC57/AC60) stand as claims about *permutation
orders in that corner*, and the line's broader framing — that a learned order is a significant acquired
object — is correspondingly bounded.

## Bounds

No claim. Engineering prerequisite. Not autopoiesis, closure, or life.

## Artifacts

This document (measurements inline). Related: `AC65_ENGINEERING_v1.md`, `AC55_RESULTS_v1.md`,
`AC57_RESULTS_v1.md`.
