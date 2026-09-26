# N1 rival-selection correction v1 — replace the "genuinely beatable" engineering gate with an identifiability test

2026-09-25. Deliverable for the N1 card (t_2ecf3d42), consumed by N8, which issues
`ACI_BRIDGE_PROTOCOL_v3.md`. This document identifies the rival-selection flaw in
`ACI_BRIDGE_PROTOCOL_v2.md` and writes the correction. It edits nothing frozen: no
runner, protocol, results dir, hash, or ledger is touched. It is a derived successor
document and is not hashed into any study's `pre_run_snapshot.json`.

---

## 0. The one-paragraph answer

Yes. The pre-protocol engineering gate that requires the sufficient-statistic rival
(arm 9) — and, with it, the fixed-level family — to be "genuinely beatable" by a
state-dependent allocation is the wrong test, and it must be replaced by an
**identifiability test**. The flaw is not a matter of degree: "the candidate beats the
sufficient-statistic rival" tests *whether the candidate empirically wins*, which (a)
is either unsatisfiable by construction — a rival that conditions on the observable
sufficient statistic reaches the ceiling, so strict dominance cannot hold (AC17) — or
(b) measures how often a rival gets lucky (AC16) — and (c) is, in any case, not what
engineering exists to establish. Engineering's legitimate job is to establish that
the *inferred* integrity component of V is **identifiable from the permitted
information** — that two situations matched on every observable but differing in
actual representation integrity are distinguishable in the organism's own
observation/history. If they are not, the candidate cannot honestly claim an
internally-estimated integrity component, and the design is revised **before** any
final seed runs. If they are, engineering proceeds **without** requiring the candidate
to beat any rival empirically. The strongest rivals stay in the arm set, stay swept,
stay unhandicapped, and stay capable of defeating the hypothesis at the final run;
only the engineering superiority precondition is removed.

---

## 1. The flaw, identified with exact passages

The correction is scoped to the **engineering gate** (`ACI_BRIDGE_PROTOCOL_v2.md` §9),
not to the final run. The flawed passage is §9.5:

> 5. **Level sweep and sufficient-statistic sweep.** Confirm the fixed-level family
>    **and** the sufficient-statistic rival (arm 9) are genuinely beatable by a
>    state-dependent allocation — the condition making G3b/G3a non-vacuous.

This sentence does two things that the correction forbids. First, it makes
**candidate superiority** over the sufficient-statistic rival and the fixed-level
family a precondition for proceeding to finals. Second, it makes that superiority the
condition on which **a final gate** (G3b) is declared "non-vacuous" — i.e. it
requires, at engineering time, the *passing of* a final scientific gate, rather than
the *cleanability/identifiability* of that gate.

The same "beatable" requirement leaks into the final-run prose in two places, which
must be reconciled when v3 is written (they are not engineering gates, but they
encode the same confusion about what the sufficient-statistic rival is *for*):

- §7.2 predicted outcomes: "Arm 9: tracks the energy gauge but cannot reproduce the
  candidate's integrity-driven conservation — **beaten** if V's integrity component
  is real." (Reading "the mechanism's existence implies arm 9 loses on a score" into
  the mechanism.)
- §4.2 G3a note: "the sufficient-statistic rival (§5, arm 8) is what makes the
  integrity component load-bearing." — note also the **arm-numbering error**: the
  sufficient-statistic rival is **arm 9**; arm 8 is the multi-objective RL rival.
  The mis-numbering is symptomatic: the doc treats arm 9's role as a second-order
  "make the candidate win" device rather than a first-order "make the *integrity
  component* the load-bearing term" device.

**Re-verification against N0's baseline (2026-09-25).** This correction was
re-verified against `PHASE2_BASELINE_v1.md` (N0's reconciled baseline, the parent
handoff) before N8 consumes it. The baseline is consistent with every claim above:
its §6 arm table lists arm 8 as the multi-objective RL rival and arm 9 as the
sufficient-statistic rival (confirming the arm-numbering fix independently), and its
§7(b)(1) records the flaw in identical terms — "v2 §9.5 requires the
sufficient-statistic/fixed/reactive rivals to be 'genuinely beatable' as a
pre-protocol engineering condition, which is the wrong test (strict dominance over an
observable-sufficient-statistic rival is unsatisfiable, AC17; a mean margin over a
partially-succeeding rival is a luck statistic, AC16)". The falsifying-rival set
(arms 2, 3, 5, 7, 8, 9) and the EXTERNAL bounds (arms 4, 6) match §3.4 exactly. No
change to this correction is required by the baseline.

---

## 2. Why "genuinely beatable" is the wrong gate

Three independent reasons, each sufficient on its own.

**2.1 The sufficient-statistic rival reaches the ceiling, so "beat it" is
unsatisfiable (AC17).** Arm 9 is defined (`§5`) as "a reactive level whose duty cycle
is a function of the observable (energy, regime), no maintained integrity estimate, no
content attribution." By construction it conditions on exactly the observable
sufficient statistic of the task. If the optimal maintenance allocation is a function
of the observable alone — i.e. if latent integrity carries no additional information
about what to do — then arm 9's family *contains* the optimal policy, and
"genuinely beatable" cannot hold however good the candidate is. And even when
integrity *is* informative, arm 9 remains near-optimal and reaches the ceiling on
some seeds, so strict dominance is unsatisfiable (AC17's lesson: a strict-inequality
gate over a rival that can hit the ceiling is unsatisfiable by construction). The
engineering gate is therefore asking for a result that the task's own structure may
forbid.

**2.2 It measures the wrong quantity (AC16).** If the gate were instead weakened to a
mean margin — "candidate out-scores arm 9 on average" — it would measure how often a
rival that partially succeeds (re-binding repeatedly, or tracking the observable
gauge) gets lucky, not whether the candidate's mechanism is load-bearing. AC16's
falsification-by-0.006 is the cautionary case: a mean margin over a partially
succeeding rival is a luck statistic, not a mechanism statistic.

**2.3 Identifiability and dominance are different claims, and only identifiability
belongs to engineering.** The candidate's claim is "the allocation is computed from
an *inferred* integrity component of its own maintained resource state." The
sufficient-statistic rival exists to force that claim to mean something: it is a
rival the candidate is **not required to outscore**, but a rival whose *existence*
makes G3a (content-sensitivity of E_π to the integrity component) a test of self-state
rather than of observation. The engineering precondition should therefore be
"can the integrity state be distinguished from the permitted observation," not "does
the candidate beat the rival." The former is a property of the task + the permitted
information; the latter is a property of a *trained policy* that engineering seeds
(disjoint families, small N) cannot decide. Requiring the trained-policy outcome as a
precondition inverts the order of evidence.

---

## 3. The correction

### 3.1 What engineering must NOT require

- Engineering must **not** require the candidate to beat the sufficient-statistic,
  fixed-schedule, or reactive rival — not in aggregate, not per individual, not by a
  margin.
- Engineering must **not** require any final scientific gate to pass. G3b
  (level-sweep dominance), G3a (content-sensitivity), G3c (reward-invariance), G3d
  (decoupling) are **final-run** gates. Engineering may only establish that they are
  *well-defined, cleanable, and answerable* — never that they will pass.

### 3.2 What engineering MAY establish

Engineering may establish exactly the following five facts, and nothing stronger:

1. **Task non-vacuous.** The probe is reachable in the stable regime and the
   maintenance actually costs in the volatile regime (v2 §9.1, F5).
2. **A real resource trade-off exists.** Per-action economics run in the modelled
   direction (v2 §9.2, F6/AC113).
3. **Different latent integrity states can require different maintenance actions.**
   Holding a correct cue vs a degraded cue vs an already-dropped cue prescribe
   different (E_π, refresh) actions *somewhere* in the state space — the precondition
   for "allocation as a function of integrity" to be a non-trivial claim.
4. **The relevant states are identifiable from the permitted information** — the
   identifiability test (§3.3), which replaces §9.5.
5. **Candidate and rivals can physically express their mechanisms.** The decoupling
   and severance interventions can actually be built and run (v2 §9.4); no arm is
   silently unable to express its own mechanism.

### 3.3 The identifiability test (replaces §9.5)

Construct **matched situations**: resource level matched, regime matched, reward
matched, clock/probe-distance matched — but **actual integrity of the maintained
representation differs** (e.g. cue-slot content correct vs partially decayed vs
erased, at identical energy, regime, reward, and time-to-probe). Then ask, without
supplying the integrity label to any arm:

> Does the permitted observation/history — the same raw stream every arm receives
> (cue once at t=0, distractor stream, announced regime, energy reading, the
> organism's own maintenance/bookkeeping reads) — contain information that
> distinguishes those integrity states?

- **If NO** — the candidate cannot honestly claim an internally-estimated integrity
  component, because there is nothing for the estimate to be an estimate *of*. The
  design is revised **before** final execution (re-opened observation interface,
  faster decay, a richer maintained slot, or a scope narrowing to what is
  identifiable). This is the mirror of F5/F6: a pre-protocol stop, not a run-time
  falsification.
- **If YES** — engineering proceeds **without** checking whether the candidate
  empirically beats the sufficient-statistic rival, the fixed levels, or any other
  arm. The empirical "who wins" question is deferred to the final run, where the
  candidate is *allowed to lose* and the loss is recorded (the rivals must remain
  capable of defeating the hypothesis).

The test is run on engineering seeds only, excluded from the final sample (AC39).
Its output is a **binary go/no-go on identifiability**, not a superiority score. A
candidate that passes the identifiability test and then loses to a rival at finals is
a *recorded falsification* (F1/F4), not an engineering-screening failure.

### 3.4 The strongest rivals remain capable of defeating the hypothesis

The correction removes only the engineering superiority *precondition*. It does not
weaken the comparison set. Arms 2, 3, 5, 7, 8, 9 remain falsifying rivals; arms 4 and
6 remain labelled EXTERNAL bounds; every rival's parameter family remains swept
alongside the learner's; no rival is denied information, history, compute, or tuning
opportunities (AC109; and N2 strengthens exactly this). The final gates G3a/G3b/G3c/G3d
and the failure table F1–F7 remain the *falsification* instrument. What changes is
only that "the candidate beats the rival" is no longer smuggled in as an engineering
admission requirement before the experiment is allowed to run.

---

## 4. Replacement text for v3 (drop-in for §9.5)

> 5. **Integrity-state identifiability (replaces the v2 "beatable" sweep).** On
>    engineering seeds only, construct matched situations — resource level matched,
>    regime matched, reward matched, clock/probe-distance matched — that differ only
>    in the **actual integrity** of the maintained cue slot. Confirm that the
>    permitted observation/history (the raw stream every arm receives) distinguishes
>    those integrity states. If it does not, the candidate cannot honestly claim an
>    internally-estimated integrity component: redesign the observation interface,
>    the decay, the slot, or the scope before final execution (a pre-protocol stop,
>    mirroring F5/F6). If it does, proceed to finals **without** requiring the
>    candidate to beat the sufficient-statistic rival (arm 9), the fixed-level
>    family, or any other arm. Superiority over rivals is a *final-run* question,
>    not an engineering admission requirement; the rivals must remain capable of
>    defeating the hypothesis.

The v2 clause "the condition making G3b/G3a non-vacuous" is struck. Non-vacuity of
G3b/G3a is established by §9.1–§9.4 (trade-off exists, economy runs in the right
direction, gates are cleanable) plus §3.3 (the integrity state is identifiable), not
by a superiority precheck.

---

## 5. What this hands downstream

- **N8 (v3).** Drop the replacement above in place of v2 §9.5; fix the arm-numbering
  error in §4.2 G3a ("arm 8" → "arm 9"); reword §7.2's "Arm 9 … beaten if V's
  integrity component is real" to state arm 9's *role* (it makes G3a a test of the
  integrity component) rather than a predicted score; and keep §9.1–§9.4 as the
  non-vacuity/expressibility checks the correction preserves. No superiority
  requirement of any form may appear in the engineering section.
- **N2 (same-information rival discipline).** N2's raw-bookkeeping direct policy is
  the natural *implementation* of the identifiability test's "matched situations"
  construction: a policy mapping the raw maintenance/bookkeeping history directly
  into allocation, with no explicit V. N2 should confirm its raw-bookkeeping rival
  receives the same raw information as the candidate's V — that sameness is what
  makes the identifiability test non-vacuous. N1 hands N2 the principle; N2 hands
  back the concrete rival.
- **N6 (analytic identifiability).** N6's question — "are there two histories with
  the same observable tuple but different optimal actions due to different latent
  integrity?" — is the analytic form of §3.3. N1 establishes *what* must be shown
  (identifiability, not superiority) and *when* (before final execution, on
  engineering seeds); N6 proves or refutes it for T_bridge specifically, including
  whether the compact sufficient statistic (time-since-acquisition, time-since-
  refresh, energy, regime, probe-distance) collapses the architecture.

---

## 6. Implication for the constitution (a note, not an amendment)

`ACI_RESEARCH_CONSTITUTION_v1.md` §4.2 and Q4 state the *final-gate* rival discipline
("the claim is credited only if the strongest simpler mechanism that omits the
contested piece provably fails"). That discipline is correct and is **not** changed by
this correction. The correction draws the line that §4 does not: "provably fails" is
established at the **final run** by the falsification gates, never demanded as an
**engineering** precondition, and for the sufficient-statistic rival in particular
"fails" means "is structurally unable to express the integrity-dependent allocation"
(G3a), not "is outscored on a margin" (AC16/AC17). No constitution amendment is
required; v3 must simply not read "rival provably fails" as "engineering must confirm
the candidate wins."

---

## 7. Claim discipline

- This document makes no empirical claim about T_bridge, no claim that the candidate
  will or will not beat any rival, and no claim crossing the level-(d)/(e) boundary.
- "Identifiable" means "the permitted observation/history separates the integrity
  states" — not "the candidate succeeds" and not "the mechanism is load-bearing."
- No frozen artifact is edited, re-run, or re-hashed. This correction is a design
  note consumed by N8, and it does not itself amend any protocol: v2 remains the
  frozen design until N8 issues v3 as a new file.

## Sources

Read, not edited: `ACI_BRIDGE_PROTOCOL_v2.md` (§4.2, §5, §7.2, §9),
`ACI_BRIDGE_PROTOCOL_v1.md` (§9, F1), `ACI_BRIDGE_REVIEW_v1.md` (R3, R5),
`ACI_RESEARCH_CONSTITUTION_v1.md` (§3 Q4, §4), `TASK_IDENTIFIABILITY_v1.md` (K4),
`N1_CORRECTIONS_v1.md` (the prior N-series N1, for the correction-note form),
`PHASE2_BASELINE_v1.md` (N0; §6 arm table, §7(b)(1), re-verified against).
Study references from the skill: `ac11` (level-not-switch), `ac15` (asymmetric
intervention / vacuous pass), `ac16` (mean margin over a partially-succeeding rival),
`ac17` (strict dominance unsatisfiable at the ceiling), `ac109` (non-ignorance),
`ac113` (trade-off direction), `ac116` (economically invisible).
