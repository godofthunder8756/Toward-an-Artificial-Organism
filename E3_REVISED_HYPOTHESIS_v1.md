---
title: E3 revised discriminating question after the H2 financial refutation
description: Free-energy-weighted local consolidation vs matched conventional rivals, proposed and unfrozen
ms.date: 2026-09-14
---

Status: **proposed, not frozen, not implemented as a confirmatory experiment.**
Nothing here authorizes touching `e3/` (frozen under
`E3_DESIGN_FREEZE_v0_11.json`) or launching final individuals. This document
does Phase A and Phase B of `NEW_AGENT_GUIDE.md` section 7 for the next
falsifiable question, as `E3_INTEGRATION_DECISION_v0_11.md`'s "Next permitted
execution stages" step 1 requires before any further engineering.

## Corrections (added later on 2026-09-14)

The text below keeps what was written. These corrections take precedence over
it. For lineage and audit evidence, see `E3_BRANCH_RECORD_2026-09-14.md`.

1. **"The guide was edited after that snapshot" is wrong.** The mismatch is a
   line-ending conversion. The content matches the frozen hash once line
   endings are normalized. See the erratum in the branch record.
2. **"Refuted at this scale" is withdrawn.** The claim compared overlapping
   confidence intervals around separate means. That neither establishes
   equivalence nor tests a paired difference. No minimum useful advantage was
   defined beforehand. Independently, the audit found that the v1 "paired"
   runs were not paired: policy draws desynchronized the shared random stream
   within ten ticks. The correct statement is that runs 3 and 4 give no
   evidence of an advantage and no evidence of equivalence.
3. **The "structural substrate defect" diagnosis is withdrawn.** Collapse under
   scarcity can have several causes: insufficient budget, ineffective repair,
   implementation error, poor scheduling, or loss before maintenance. It
   diagnosed nothing by itself. Exhaustive isolation testing shows majority
   repair behaves as a majority code should: below-threshold damage is
   restored, and damage beyond threshold is locked in. That is compatible with
   "partial damage recoverable, complete loss unrecoverable". A graded
   dose–response curve was never required. The one deviation is the tie rule
   at even widths, which always decodes 1.
4. **"Replace the substrate with continuous traces" is withdrawn as the next
   step.** Continuous amplification can reinforce a wrong sign just as
   majority repair does. A correct-answer attractor or external signal would
   reintroduce a protected template or turn maintenance into relearning. No
   substrate change is made until budget feasibility separates world failure,
   controller failure and interpretation.
5. **The Phase A claim is restated.** The narrower, theory-neutral wording is
   "An individual can allocate scarce maintenance resources according to
   predicted future recoverability and functional consequence, rather than
   only recent activity." FEP and autopoiesis motivate the design only. The
   precision allocator uses a hand-set staleness bonus, not a learned or
   self-modeled quantity.
6. **"Pre-fix run preserved in `scratch_fep_seed_run.json`" is false.** Later
   runs overwrote that file. The printed summaries of all four v1 runs and the
   JSON rows of runs 3 and 4 are now in `e3_fep_seed_results/v1/`.

## Why H2 needed replacing

`E3_INTEGRATION_DECISION_v0_11.md` found that fixed/frozen repetition coding
covers full conditioning plus maximal correction for at most 28+5=33 material
per source, under a budget of 36. A conventional error-correcting code already
affords perfect retention at this scale. Material scarcity alone therefore
cannot force abandonment of acquired information, so no observation about
*whether* something gets abandoned under this budget can discriminate the
candidate mechanism from ordinary engineering. The question has to change, not
the budget.

## Theoretical grounding, used as mechanism design, not as evidence

The four frameworks the user named point at the same gap in the refuted
design, not at four separate features:

- **Free Energy Principle / active inference.** A maintenance allocator that
  minimizes *expected* free energy — accuracy of recall traded against the
  complexity of what it commits to keeping, weighted by its own confidence
  (precision) in that trace's future relevance — has a reason to keep a
  cheap, nonzero exploratory investment in traces whose relevance is
  *uncertain* rather than confidently low. A recency-only heuristic has no
  such term: once a trace stops being queried, its priority strictly
  decays to zero.
- **Autopoietic enactivism.** What counts as worth maintaining should come
  from the same process that later uses the information to act, not from an
  externally flagged "useless" bit. Precision computed locally from the
  system's own usage statistics is a weak, defensible operationalization of
  that closure requirement — it is not full organizational closure, and this
  document does not call it that.
- **Neural self-organization.** The precision/complexity estimate should be
  computed from local per-trace statistics (a small recency/uncertainty
  filter), not from a global critic or backprop signal, matching E3's
  existing constraint that no privileged second controller may quietly do
  the interesting work.

None of this is evidence for phenomenal consciousness, autopoiesis proper, or
Fristonian active inference in its full variational-generative-model form.
What is implemented below is a **local proxy**: an upper-confidence-bound-style
exploration bonus standing in for epistemic value. Say that explicitly in any
future write-up; do not let the citation upgrade the claim.

## Phase A — the actual claim

Good:

> A local allocator that adds an uncertainty-driven exploration bonus to its
> maintenance priority recovers a dormant-then-reactivated association faster
> than a matched-material-budget recency-only allocator, because the
> recency-only allocator lets confidently-idle traces decay to chance while
> the uncertainty-aware allocator keeps spending a small, principled amount on
> them.

Bad:

> The system knows which memories still matter to it.

Level: functional motivation, bordering partial organismal autonomy through
the closure framing above. Not subjectivity. Do not describe a pass as
evidence of wanting, caring, or awareness.

## Phase B — causal dependency chain

1. **Capability acquired:** anticipating that a currently-idle association may
   become relevant again, without ever observing "relevance" directly — only
   inferable from the statistics of which cues get queried.
2. **Physical representation:** a per-trace scalar precision/uncertainty
   estimate, computed and stored locally alongside the same redundant
   material trace bits E3a already uses, not in a separate protected array.
3. **Sustaining resource:** the identical scarce material/scrub budget as the
   conventional rival. The candidate mechanism gets no unmatched budget.
4. **Decision made by the same vulnerable organization:** which cue receives
   this tick's scrub is chosen by the local precision score itself — an
   emergent, per-trace quantity, not a fixed external schedule.
5. **What stays protected outside it:** the corruption/decoding physics, the
   environment's query-generating process, and the definition of a
   "successful decode" remain experimenter-supplied, exactly as in E3a.
6. **Interventions that break the chain:**
   - freeze or shuffle the local precision signal so scrubs become pure
     round-robin — removes anticipation without touching the budget;
   - delete a trace's usage-history statistic while preserving its material
     bits — tests whether the "memory of relevance" is itself materially
     grounded rather than free, the exact leak that sank E2;
   - replace gradual relevance drift with an abrupt flip — removes the
     condition that makes anticipation distinguishable from reaction.
7. **Ordinary controller that could fake it — the sharp rival:** a
   recency-weighted heuristic (priority ∝ exponential moving average of
   recent queries, no exploration term) is the required rival, not plain
   uniform ECC. It must receive the same budget, the same trace substrate,
   and the same observations. If it matches the proposed allocator's
   recovery speed, the exploration term adds nothing and the claim fails.

## Controls (Phase D)

| Control | Question it answers |
| --- | --- |
| Random-needing-scrub reflex | Is the task trivially solvable at this budget? |
| Uniform round-robin (matched standard method) | Does ignoring relevance entirely already suffice at this budget? |
| Recency-only heuristic | Is a cheap non-Bayesian statistic sufficient? (the sharp rival) |
| Precision/UCB allocator frozen after burn-in | Did the exploration term matter, or just its initial value? |
| Shuffled precision assignment | Does the *local correspondence* between a trace and its own statistic matter, or would any signal do? |
| Abrupt instead of gradual relevance flip | Does the effect require gradual, uncertain drift specifically? |
| Complete trace-history deletion with material restored | Is apparent recovery leakage through a preserved statistic rather than the material substrate? |

Budget, corruption process, decode rule, and query generator must be identical
across all rows. If any row cannot be exactly budget-matched, report the
mismatch instead of the comparison.

## Failure criteria

- If the recency-only heuristic matches the precision/UCB allocator's
  post-return recall within its confidence interval, the mechanism is refuted
  at this scale — record it as a valid negative result, not a bug.
- If shuffling the precision assignment does not degrade post-return recall,
  the local correspondence was not doing the work.
- If deleting trace history while preserving material bits does not lower
  performance, there is no leak to worry about; if it does not lower it *and*
  performance stays high, that is itself suspicious and must be re-audited
  before being reported as a positive result.

## What a pass would and would not establish

Would establish, at best: "a materially-grounded, locally-computed uncertainty
estimate produces anticipatory maintenance reallocation beyond a cheap recency
heuristic, at equal budget." Would not establish active inference in its
formal sense, autopoietic closure, self-organization as a general principle,
or anything about subjective experience. Use the wording from
`NEW_AGENT_GUIDE.md` section 8 and no stronger.

## Immediate next bounded step

Phase C — the smallest discriminating world, as an **engineering seed only**,
outside the frozen `e3/` package: `e3_fep_engineering_seed.py`. Its results are
exploratory and excluded from any future confirmatory sample.

## Freeze-manifest note

`verify_e3_design.py` currently fails: `NEW_AGENT_GUIDE.md` no longer matches
the byte length/hash recorded in `E3_DESIGN_FREEZE_v0_11.json` (expected
20529 bytes, found 20960). The guide was edited after that snapshot. This is
recorded here rather than silently patched; whoever performs the next design
freeze should re-hash it as part of that cycle rather than force the old
snapshot to pass.

## Engineering seed results (2026-09-14)

Two paired-seed runs of `e3_fep_engineering_seed.py`, 16 seeds each, all four
policies on the identical environment stream per seed:

| Setting | random | uniform | recency | precision (post-return) |
| --- | --- | --- | --- | --- |
| `--budget 5 --trace-bits 8 --corrupt-p 0.03` (default) | 0.811 | 0.801 | 0.781 | 0.782 |
| `--budget 3 --trace-bits 6 --corrupt-p 0.04` (stress) | 0.537 | 0.538 | 0.539 | 0.524 |

All 95% CIs overlap heavily within each row. Two negative findings, not one:

1. **At the default budget, precision does not beat recency.** Per the
   pre-registered failure criterion, the exploration-bonus mechanism is
   refuted at this scale — a plain recency heuristic already captures
   whatever the toy world offers, most likely because even "cold" cues are
   queried occasionally (weight 0.05, not 0), so recency's own EMA gets a
   sporadic direct signal instead of decaying to a true zero. That undercuts
   the intended contrast: the rival wasn't starved of information the way
   Phase B assumed.
2. **At the stress budget, everyone collapses to chance, including
   currently-hot cues under every policy.** This is not scheduling failure;
   it is a structural property of the repetition-code substrate. Scrubbing
   always pushes a disagreeing bit toward the trace's *current* majority
   (correctly, per the no-privileged-copy design in `E3_DESIGN.md`), which
   makes majority self-reinforcing: once corruption drifts a trace across the
   50% line, further scrubbing locks in the new, wrong majority rather than
   correcting it. Binary majority vote has no gradual-damage middle ground —
   a cue is either well short of the tipping line (protected indefinitely by
   modest upkeep) or past it (permanently lost, chance-level, unrecoverable
   by any scheduling policy). Two parameter settings landed on opposite sides
   of that cliff and none in between; a scarce-vs-generous parameter sweep on
   this substrate is unlikely to find the graded middle regime the question
   needs, because the substrate itself doesn't have one.

This is useful negative engineering knowledge, not just a failed toy: it says
a binary-repetition-code implementation of E3's traces would inherit this
same absorbing-state cliff, which conflicts with the "partial damage
recoverable, complete loss unrecoverable" *gradient* `NEW_AGENT_GUIDE.md`
section 6 actually wants. A next iteration should replace binary majority
vote with continuous, decaying, real-valued traces (closer to the "several
spatially separated, metabolically maintained noisy traces" language in
`E3_DESIGN.md`) combined into a confidence-weighted estimate, so degradation
is graded and a precision-style allocator has room to matter before full
information loss. That substrate change, not further parameter tuning on the
binary version, is the right next engineering step — and it should happen
before any further claim about the precision/UCB mechanism specifically,
positive or negative.

## End-of-session fields

- Question tested: at a toy scale, does a local precision/UCB allocator beat
  a matched-budget recency-only allocator on post-return recall, across a
  normal and a scarce budget setting.
- Mechanism implemented: `e3_fep_engineering_seed.py` only — four maintenance
  policies over a binary repetition-code substrate. Nothing in the frozen
  `e3/` package was touched.
- Externally supplied objectives/rules: corruption process, decode rule, query
  generator, hot/cold Markov rates, and success criterion are experimenter-
  defined and identical across all four policies (paired seeds).
- Engineering changes made: two bugs found and fixed during this session —
  (1) the precision policy's exploration bonus was inverted (grew for
  recently-queried cues instead of stale ones); (2) seeds were keyed by
  `hash(policy)`, which CPython randomizes per process, so policies were
  compared on different, unpaired environment realizations. Both are fixed
  in the committed script; the pre-fix run is preserved in
  `scratch_fep_seed_run.json`'s git-untracked history for anyone who wants to
  see the artifact rather than take this description on faith.
- Frozen sample and gates: none; this document and the seed script remain
  unfrozen and excluded from any confirmatory sample.
- Primary results: at the default budget, precision does not separate from
  recency (post-return 0.782 vs 0.781, seeds paired, CIs overlapping) —
  refuted per the pre-registered criterion. At a scarce budget, all four
  policies including uniform round-robin collapse to chance (~0.53) even on
  currently-hot cues, showing an absorbing-state cliff in the majority-vote
  substrate rather than a graded scarcity regime.
- Simplest sufficient rival explanation: a recency-weighted heuristic at the
  same material budget — and at this toy scale it wins the comparison, not
  just ties it.
- Failures and negative results: precision/UCB refuted at default budget;
  no discriminating middle regime found between the default and stress
  budgets on this substrate; the two bugs above produced spurious results
  before being caught and are recorded rather than quietly discarded.
- What this establishes: a candidate falsifiable replacement for the refuted
  H2, with explicit failure criteria, now evaluated once at toy scale and
  refuted there; and a concrete substrate defect (binary-majority lock-in)
  worth fixing before the next attempt.
- What this does not establish: any E3 result, active inference, autopoiesis,
  self-organization as validated theory, organismal autonomy, or that the
  underlying idea is wrong in general — only that this binary-repetition
  toy implementation does not show it.
- Next falsifiable question: does the same precision/UCB-vs-recency contrast
  separate once the substrate uses continuous, decaying, confidence-weighted
  traces instead of binary majority vote, removing the all-or-nothing lock-in
  this run exposed? Build that substrate variant before revisiting the claim,
  and before any protocol freeze.
