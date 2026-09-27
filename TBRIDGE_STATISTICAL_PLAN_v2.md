# T_bridge statistical plan v2 — no plan to write: the re-designed latent-integrity task is unidentifiable (documented STOP)

2026-09-26. Deliverable for the N7b card (t_520416cc): *what is the frozen
statistical plan (primary contrast, sample size, resolution) for the re-designed
latent-integrity T_bridge?*

**Answer: there is none to write.** N7b's precondition is "conditional on
identifiable," and the predecessor N6b (`TBRIDGE_IDENTIFIABILITY_v2.md`) returned
**NO-GO with a documented STOP**. The re-designed integrity (Path B — unrevealed
corruption stream replacing δ-decay) is unidentifiable for two structural reasons,
both established there and not re-argued here:

1. **No signal (identifiability).** Under the bridge's isolation constraints (cue
   observable only at t=0; distractor i.i.d. independent of c; W the only record of c),
   W's correctness has no observable correlate during the delay. The corruption is
   unobservable in principle, the two-histories contrast has no pair with different
   optimal actions attributable to the latent, and the maintenance DP is degenerate
   (refresh has zero causal effect on probe success).
2. **No action (well-posedness).** The paid refresh π has no correct content to write:
   c is unobservable after t=0 and a pristine copy is forbidden by N3 §3.6.
   "Maintain-or-drop" is not executable by the substrate as specified.

With no well-posed contrast there is nothing to define a primary contrast over, no
smallest effect worth distinguishing, and no sample size to derive from engineering
variance + minimum meaningful effect + the sign-flip resolution floor. Writing a
statistical plan against this design would be fabricating a plan for an experiment
that does not exist. Per the predecessor's directive, this card's honest output is
this STOP recording, not a plan.

**What this card does not do:** it does not re-argue the identifiability verdict (that
is N6b's deliverable), does not propose a further re-design (the "do not loop" applies
upstream), does not pick Path A vs Path B (the operator picked B), and does not edit any
frozen artifact (`ACI_BRIDGE_PROTOCOL_v3.md` remains the last issued protocol, itself a
STOP).

**Honest successors (for the operator).** The program's "inferred integrity" ambition,
wherever it is honestly testable, is one of two different experiments — neither the
bridge:

- **T1** — maintained hidden-state inference over a cause. Sufficient statistic is a
  scalar counter; claim ceiling **N1+N2** (active persistence + content load-bearing),
  never endogenous allocation.
- **T7** — internalized repair of OBSERVED damage. The load-bearing question is *who
  enacts repair*, not whether integrity is inferred.

Each needs its own card; neither inherits the bridge's clause (c)(i).

**Operator decision required.** Cancel N7b or re-parent it to T1/T7. Downstream, N8b
(`ACI_BRIDGE_PROTOCOL_v4.md`) inherits this STOP through its own clause — *"if the
re-designed experiment is NOT identifiable, STOP (do not execute a structurally
incapable experiment)"* — and should record its own documented STOP rather than freeze a
v4 protocol for an unidentifiable task.

---

## Claim discipline

- This is a **level-(b)/(c) representational** finding: the re-designed integrity state
  is absent from the permitted observation and the maintenance action ill-defined.
  Nothing here is a consciousness claim, an empirical prediction about which arm would
  win, or a verdict that the mechanism is inert in general.
- "No plan to write" is a property of **this design** (task + permitted information),
  not a claim that statistical planning is unnecessary elsewhere. The v1 plan
  (`TBRIDGE_STATISTICAL_PLAN_v1.md`) remains the frozen plan for the δ-decay bridge as
  N6 left it; it is not superseded by this STOP, which applies only to the Path B
  re-design.
- No frozen artifact is edited, re-run, or re-hashed.

## Sources

Read, not edited: `TBRIDGE_IDENTIFIABILITY_v2.md` (N6b; §4 the refresh-content blocker,
§5 the degenerate DP, §6 the two-histories verdict, §8 the boundary, §9 the NO-GO
verdict), `TBRIDGE_STATISTICAL_PLAN_v1.md` (N7; the δ-decay plan this v2 does not
replace), `TBRIDGE_IDENTIFIABILITY_v1.md` (N6; the δ-decay collapse).
