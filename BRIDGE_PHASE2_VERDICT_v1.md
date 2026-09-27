# N13 — Phase-II verdict (neural bridge)

2026-09-26. Deliverable of the N13 card (t_82c88b19): *what is the bounded
Phase-II verdict (OUTCOME A–F)?* Reads the frozen N11 finals
(`BRIDGE_FINALS_RESULTS_v1.md`) and the independent N12 audit
(`BRIDGE_FINALS_AUDIT_v1.md`); issues the verdict only — no re-run, no
re-freeze, no re-litigation of the N6/N6b STOP.

---

## 0. Verdict

**B (primary) + D (allocation-specific), jointly and not independently.**

The frozen finals and the independent audit converge on the same empirical fact
— the N6/N7 identifiability collapse, confirmed by measurement rather than
assumed — and that fact triggers **two** of the outcome clauses, which here are
two facets of one result, not competing alternatives:

- **B — internal information useful, explicit V unnecessary (same-information
  policy matches).** The strongest same-information rival — the recurrent
  no-V-slot direct policy P_rb (arm 10) — **matches** the candidate (op 0.823
  vs 0.895, exact sign-flip p = 0.64, 5/12 seeds positive). V's integrity bit
  is a learned re-encoding of the readable age `d_t`; its discrete, paid,
  maintained self-state carries no information the raw bookkeeping lacks. The
  architectural claim — that explicit maintained V is causally load-bearing for
  the allocation — is **not supported**. Consequence: simplify the architecture
  and weaken the explicit-maintained-self-state claim.

- **D — fixed/reactive allocation suffices; N3 not supported by this task.** A
  3-line sufficient-statistic threshold rule on the raw observable
  (`refresh iff s=stable and E>=E_crit and d>=L-1`, arm 9_d) attains the oracle
  (op 1.000) in every seed, **above** the candidate (0.895). The learned
  adaptive allocation is reproduced by a hand-coded reactive rule on (s, E, d).
  N3 (internal-state-driven nontrivial allocation) is **not supported**.
  Consequence: do not optimize T_bridge indefinitely.

**Not A** — the allocation is not distinctive (it is reproduced and exceeded by
same-information rivals), and the integrity is *observed* (`I_t = f(d_t)`), not
internally estimated. The precondition for A (adaptive allocation whose utility
depends on internally-estimated integrity, not reproduced by the strongest
same-information rivals) fails on both clauses.

**Not C** — free recurrence does **not** defeat paid persistence. Free-permanence
holds: with W's read-in disabled (free_memory) or π cut (no_maintenance) the cue
is unrecoverable at the probe in every seed (0.000). No auxiliary recurrent
state carries the cue; the paid W slot is necessary.

**Not E** — the homeostatic objective does real work (it is what keeps the
candidate alive where the reward-only arm 7 chases the probe reward to death),
but it does not explain *everything*: N1 paid persistence is a substrate-level
necessary-condition fact, not a reduction of the objective.

**Not F** — no optimization/feasibility failure. The experiment ran, froze, and
survived a 14/14 independent audit (source hashes, coverage, seeds, checkpoint
provenance, statistics, leakage, resource accounting).

---

## 1. What survives (the bounded positive)

Exactly one load-bearing claim, and it is narrow:

**N1 — active paid persistence (necessary condition).** Future-task information
depends on a representation whose retention is paid per tick out of a limited
budget, and is unrecoverable without it. Candidate stable slot survival 0.978
vs no_maintenance / free_memory 0.000; exact sign-flip p = 2/2^12 = 0.00049
(floor); 12/12 seeds. The W-intervention reads it causally (force-hold → probe
1.0; force-drop → chance).

This is a **substrate + architecture** fact, not a learned-behaviour fact. It is
**not unique to the candidate**: state-blind fixed schedules (fixed_p8/p16) and
the reward-only arm 7 also hold the cue through paid refresh (N12 finding F2).
It must not later be cited as evidence that the *learned allocator* is
load-bearing.

---

## 2. Exact scope

- **World:** the δ-decay scaffold's observed-integrity world, where
  `I_t = 1[age < lifetime]` is a readable age counter, not an inferred latent.
  The verdict is bounded to *this design*.
- **Unsettled, out of scope:** whether an *inferred* integrity estimate can do
  causal work. That question is a documented STOP (N6/N6b; v3 §10 / v4 §11) and
  is unidentifiable in this scaffold — nothing here is evidence against it, and
  nothing here licenses resurrecting it.
- **What "explicit V unnecessary" does and does not say:** it says the discrete
  paid-maintained integrity state adds no demonstrated value over a same-
  information recurrent rival *in this task*. It does not say internal state is
  useless in general, and it does not settle the inferred-integrity ambition
  (a separate, still-open experiment — T1/T7 per the v2 statistical-plan STOP).
- **Claim ceiling:** no autopoiesis, subjectivity, or consciousness claim is
  made, implied, or supported. This is a level-(b)/(c) representational result.
- **Two audit findings carried forward** (not part of the verdict, noted for
  N14): (F1) free_memory is measurement-redundant with no_maintenance — the
  free-permanence claim rests on the S4 architecture (structural), and any
  future "hidden recurrent memory" control must run the recurrence with W
  zeroed, not a no-GRU policy; (F2) paid persistence is shared by state-blind
  fixed schedules.

---

## 3. What this hands N14

Phase II's neural question is answered, negatively on the architectural/allocation
half and positively only as a necessary-condition substrate fact. Next work should
not optimize T_bridge, and any continuation of the "maintained self-state" ambition
must move off the δ-decay observed-integrity scaffold (see the v2 statistical-plan
STOP's T1/T7 successors). N14 is unblocked.
