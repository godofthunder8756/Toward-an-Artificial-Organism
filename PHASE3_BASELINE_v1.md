# Phase-III baseline v1 — the architecture reconciled from the Phase-II verdict (B + D)

2026-09-26. Deliverable for the G0 card (t_e408b2f6): *what is the Phase-III
baseline, with the architecture revised per the Phase-II verdict (B+D: explicit V
unnecessary, fixed maintenance suffices, N1 paid persistence survives)?* Category B/F —
**baseline reconciliation; do not execute.**

This is a **derived document**. It runs nothing, trains nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It states, in one place, the revised
architecture that the downstream G-series cards (G1 shared-content definition, G2/G3)
read their vocabulary from, instead of re-deriving it from the Phase-II verdict and the
old minimal architecture.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): nothing here is a consciousness claim. (2) Seeds are
the replication unit; survival/viability is a bimodality-aware lower bound, never a
per-seed-family guarantee (AC39/AC68). (3) The bridge verdict transfers as a *revision to
the architecture*, not as neural evidence for any organism claim: the organism program is
closed, and no frozen organism number is re-read as a neural result.

---

## 0. The one-paragraph answer

Phase III is **N2 — recurrent cross-module availability of a maintained
representation** — and its baseline is the bridge architecture *after* the B + D verdict
has stripped exactly what failed. Three components survive unchanged as the N1 substrate:
**W** (the maintained representation), **π** (the paid refresh that holds it), and
**GRU** (the recurrence substrate) — paid persistence REMAINS. One component is removed:
**V** (the explicit discrete integrity/self-resource state), because verdict B showed the
strongest same-information rival — a recurrent policy with no V slot — matches the
candidate, and V's integrity bit is a learned re-encoding of the readable age. One
component is simplified: **A** (the maintenance controller) demotes from a learned
homeostatic allocator to a fixed/reactive maintenance rule, because verdict D showed a
3-line `(s, E, d)` threshold rule attains the oracle *above* the candidate — fixed/simple
maintenance is ALLOWED. Two components are retained for a *new* reason — the second
specialist role N2 needs: **S_pol** and **S_reg**, the two objective-distinct consumers of
W. One component is deferred: **Θ_slow** (temporal continuity) belongs to Phase V (O1).
No component is retained merely because the old minimal architecture had it; each
retained component below earns its place against a named rival that omits it.

---

## 1. The verdict, restated as two architecture deltas

The Phase-II verdict (`BRIDGE_PHASE2_VERDICT_v1.md`) is **B (primary) + D
(allocation-specific), jointly**, and it forces two demotions, already recorded as D9
and D10 in `ACI_MASTER_RESEARCH_TREE_v2.md` §4.3. Stated here as the deltas this baseline
applies:

- **B — explicit maintained V is unnecessary → REMOVE V.** The strongest same-information
  rival, the recurrent no-V-slot direct policy P_rb (arm 10), **matches** the candidate
  (op 0.823 vs 0.895, exact sign-flip p = 0.64, 5/12 seeds positive). V's integrity bit is
  a learned re-encoding of the readable age `d_t`; its discrete, paid, maintained
  self-state carries no information the raw bookkeeping `(E_t, d_t)` lacks. The
  architectural claim that explicit maintained V is causally load-bearing for allocation
  is **not supported**. Consequence: V is not a load-bearing component of the Phase-III
  baseline.

- **D — fixed/reactive allocation suffices → SIMPLIFY A.** A 3-line sufficient-statistic
  threshold rule (`refresh iff s=stable and E>=E_crit and d>=L-1`, arm 9_d) attains the
  oracle (op 1.000) in every seed, **above** the candidate (0.895). The learned adaptive
  allocation is reproduced by a hand-coded reactive rule on the raw observable `(s, E, d)`.
  Consequence: the learned adaptive allocator is not a load-bearing component; a fixed or
  reactive maintenance rule is the baseline, and it is *allowed* (not merely tolerated).

**What survives, and its exact status (N1 — active paid persistence).** Future-task
information depends on a representation whose retention is paid per tick out of a limited
budget, and is unrecoverable without it: candidate stable slot survival 0.978 vs
no_maintenance / free_memory 0.000, exact sign-flip p = 2/2^12 = 0.00049 (floor), 12/12
seeds; force-hold → probe 1.0, force-drop → chance. This is a **substrate + architecture
fact, not a learned-behaviour fact, and not unique to the candidate** (state-blind fixed
schedules and the reward-only arm also hold the cue through paid refresh — N12 finding
F2). It must never be cited as evidence that a *learned allocator* is load-bearing.

**Two audit findings that bind the baseline** (from `BRIDGE_PHASE2_VERDICT_v1.md` §2):
(F1) a "hidden recurrent memory" control must run the recurrence with W zeroed, not a
no-recurrence fixed policy (`free_memory` was measurement-redundant with `no_maintenance`);
(F2) paid persistence is shared by state-blind fixed schedules.

---

## 2. The four revision rules (the card's constraints, applied)

1. **Paid W persistence REMAINS.** π, the paid refresh, and the recurrent substrate that
   needs it are load-bearing. The Phase-III architecture keeps W maintained through a
   paid, budgeted write. No free permanence; no pristine backup.
2. **Explicit integrity-state V is NOT required** (unless a later task needs it — see §3,
   V's entry). The raw bookkeeping `(s, E, d)` carries what V carried. A self-state slot
   is not assumed; if a future task re-introduces one, it must be re-derived against a
   rival that omits it (D9), never by default.
3. **Fixed/simple maintenance is ALLOWED.** The maintenance decision may be a fixed
   schedule or a reactive threshold rule; a learned adaptive allocator is not assumed and
   is not a baseline requirement (D10).
4. **No component is retained merely because the old minimal architecture had it.** Every
   retained component is justified below by the Phase-III claim (N2) it serves and the
   rival that must fail if it is omitted.

---

## 3. Component classification (the core deliverable)

The classification vocabulary is the card's: RETAIN / SIMPLIFY / REMOVE / DEFER /
THEORY-SPECIFIC. The components are the union of the Q4 minimal architecture
(`ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md`) and the bridge skeleton (`PHASE2_BASELINE_v1.md`
§3): W, V, A, S_pol, S_reg, π, GRU, Θ_slow. (E, the self-evaluative pathway, is out of
scope here — it is N4, a Phase-IV target — and is not in this list.)

| Component | Symbol | Old role (Q4 / bridge) | Classification | Phase-III role |
| --- | --- | --- | --- | --- |
| Maintained representation | W | the cue slot / world-cause belief; decay δ unless refreshed | **RETAIN** | the shared content that N2's two specialists consume; N1's substrate |
| Self-resource / integrity state | V | discrete paid-maintained estimate {energy, integrity} | **REMOVE** | raw bookkeeping `(s, E, d)` carries it; no discrete self-state |
| Maintenance controller | A | learned homeostatic allocator, reads (V, s) | **SIMPLIFY** | a fixed/reactive maintenance rule (threshold on `(s, E, d)`) |
| Policy specialist | S_pol | (W, x) → task action, reward objective | **RETAIN** | consumer 1 of W (task behaviour) |
| Regulation specialist | S_reg | (W, V) → relinquish/maintain, continued-operation objective | **RETAIN** (input simplified) | consumer 2 of W (upkeep behaviour); reads W + raw bookkeeping, not W + V |
| Paid refresh | π | the separable write re-energizing W at cost c | **RETAIN** | N1's mechanism — the paid write that holds W |
| Recurrence | GRU | the recurrence law (Q4's workspace H) | **RETAIN** | the substrate N1/N2 run on |
| Temporal continuity | Θ_slow | consolidation store, cross-episode carry | **DEFER** | Phase V (O1), not Phase III |

**No component is THEORY-SPECIFIC.** The theory-specific candidates — attention as a
serial bottleneck (→ O3/GWT), predictive coding / self-supervised internal models (→
O2/PP), differentiable memory (→ O1) — live *outside* the core architecture and are Q5's
rows (`ACI_THEORY_INDICATOR_MATRIX_v1.md`), not components of this baseline. None of the
eight above adopts a theory-specific loading, and none is classified THEORY-SPECIFIC.

### 3.1 W — RETAIN

The one load-bearing survivor of Phase II. Its content is set by the acquisition write at
t=0 (correctness rides reacquisition, D3); its *persistence* is paid per tick through π
(P1). It is the representation whose retention is causally necessary for later task
performance — the N1 substrate fact, confirmed at the resolution floor.

Why it stays, and for what: Phase III (N2) is *about* W — one maintained representation
whose content is flexibly consumed by two objective-distinct modules. W earns its place
against the memoryless/direct-diagnostic rival (conditions on the current observation,
no maintained state) and the pristine-backup rival (a copy the decay stream never reaches
and π never touches); both must fail. It is not retained "because the old architecture
had a world model"; it is retained because the N2 claim is literally "a maintained W
causally contributes to ≥2 distinct specialist computations," which has no referent
without W.

Scope note for G1: W need not be high-dimensional. A scalar sufficient statistic may be
legitimate shared content (P5 — encoding is secondary to causal function and cost). What
is required is that W is *maintained* (paid persistence) and *shared* (the same W reaches
both consumers), not that it is rich.

### 3.2 V — REMOVE

Verdict B removes V: the same-information rival P_rb (no V slot) matches the candidate,
and V's integrity bit is a learned re-encoding of the readable age `d_t`. A discrete,
paid-maintained self-state carries no information the raw bookkeeping `(E_t, d_t)` lacks,
so it does no demonstrated causal work in this task and is dropped from the baseline.

What replaces it: the raw bookkeeping — energy `E_t`, the announced regime `s`, and the
age/countdown `d_t` — is supplied to the consumers that need it, exactly as the
sufficient-statistic arm (arm 9) reads it. No learned, maintained re-encoding of that
bookkeeping is assumed.

The "unless another task needs it" clause: a later task may re-introduce a maintained
self-state — T1 (maintained hidden-state inference) or T4 (endogenous allocation) could
require one — but only by re-deriving it against a rival that omits it and fails (D9), as
a named, swept experiment. It is not part of the Phase-III (N2) baseline, and it is not
smuggled back in by assumption.

### 3.3 A — SIMPLIFY

Verdict D simplifies A: the learned homeostatic allocator is reproduced and *exceeded* by
a 3-line reactive threshold rule on `(s, E, d)`. The learned adaptive allocation does no
demonstrated work beyond a fixed/reactive rule, so A demotes from a learned controller
(whose own state lives in the maintained loop, N5) to a **fixed/reactive maintenance
rule** — a supplied or hand-coded threshold, or at most a trivially-learned reactive
policy, with no claim of an acquired adaptive decision.

This is what "fixed/simple maintenance is ALLOWED" means operationally: the Phase-III
baseline may hold W on a fixed schedule or a reactive threshold, and that is a legitimate
— not a falsifying — choice. The rival discipline still applies in one direction: any
*later* claim that the allocation is learned and adaptive must sweep the fixed/reactive
family (and the learner's own parameters) and beat every member (AC11/AC116). The
baseline does not make that claim.

### 3.4 S_pol — RETAIN

The policy specialist: reads W (plus the current observation x_t), emits the task action,
trained on the external reward. It is consumer 1 of W. It is unchanged by the verdict —
task behaviour was never in question — and it is retained for the positive reason that N2
requires a first objective-distinct consumer. Its rival is the finite-state /
direct-control mapping (a hardwired channel choice with no maintained belief); that rival
must fail the differential-scramble test (I2: scramble W, the action must change).

### 3.5 S_reg — RETAIN (input simplified)

The regulation specialist: consumer 2 of W. In Q4 it read (W, V) and decided
relinquish-vs-maintain on a continued-operation objective. The verdict does **not** touch
its existence as the second consumer — it touches only *what it reads*. So S_reg is
retained for the positive reason that N2 requires a *second, objective-distinct* consumer
of the same W; its input is simplified: it reads W plus the raw bookkeeping `(s, E, d)`
instead of W plus the explicit maintained V (which §3.2 removes).

Why it is not SIMPLIFY'd out of existence: N2 is falsified by the single-objective
collapse — one reward-maximizing policy with two heads whose outputs co-vary with W
identically. S_reg is the load-bearing thing that keeps that collapse from being the
baseline: it must consume the same W and drive *different* behaviour (relinquish-vs-
maintain, not channel choice), with a different objective (continued operation, not
reward). If S_reg were removed, Phase III would have no second consumer and N2 would be
untestable. The simplification is its *input* (no V), not its *role*.

### 3.6 π — RETAIN

The paid refresh: the separable write that re-energizes W at cost c per slot per step,
drawn from the shared budget. This is N1's mechanism — the thing that makes persistence
an *achievement* rather than a default. It is retained unchanged, and it is the component
the N1 contrast (cut π → W decays on timescale 1/δ) and the free-permanence check (no
hidden recurrent carry) both act on. Its rival is the pristine backup, which must fail.

### 3.7 GRU — RETAIN

The recurrence substrate (Q4's workspace H): the gated recurrent state that integrates
observations and relaxes toward neutral at rate δ when not re-energized. It is the
substrate both N1 (the paid-persistent slot lives in it) and N2 (the shared content is
held and read from it) run on. Retained unchanged. The one binding correction it carries
is audit finding F1: the free-permanence control must run the recurrence *with W zeroed*,
not a no-recurrence policy — otherwise the "no hidden recurrent memory" claim is not
tested.

### 3.8 Θ_slow — DEFER

The consolidation store (cross-episode carry, O1) is out of scope for Phase III. O1 is a
graded/optional property (`ACI_TARGET_CONSTRUCT_v1.md` §4), its necessity is a
theory-specific question Q5 tests, and its decisive experiment (T8) is a Phase-V concern.
Θ_slow is deferred, not removed: it is retained as a named component of the full
architecture, but it is not part of the Phase-III (N2) baseline and earns no place here
against a rival, because Phase III does not test cross-episode carry.

---

## 4. The revised Phase-III architecture (for N2)

The baseline for the G-series, stated as the smallest wiring that tests N2 under the
revised principles:

```
        observations x_t ──▶ GRU (recurrence, decay δ)
                                  │
                                  ▼
                        W (maintained, 1–2 bits, paid-persistent via π)
                         ▲                      │
                         │ paid refresh        │ shared content (the SAME W)
                         │                      ├───────────────┬───────────────┐
                         │                      ▼               ▼               │
                    ┌────┴──────┐        ┌────────────┐  ┌────────────┐        │
                    │  π        │        │  S_pol     │  │  S_reg     │        │
                    │  (paid    │        │  (W,x)→a_t │  │  (W,s,E,d) │        │
                    │   write)  │        │  reward    │  │   →relinq/ │        │
                    └───────────┘        │  objective │  │  maintain  │        │
                                          └────────────┘  └────────────┘        │
                    maintenance rule (fixed/reactive on (s,E,d))  ◀─────────────┘
                    ── A, SIMPLIFIED: no learned allocator, no maintained V ──
```

- **Two consumers, one content.** The same W drives S_pol (task action, reward objective)
  and S_reg (relinquish-vs-maintain, continued-operation objective). Changing W must
  change them *differently* (I2). A rival that gives each specialist its own private state
  (two-independent-modules) or one reward policy with two heads (single-objective
  collapse) must fail.
- **Maintenance is fixed/simple.** W is held by π on a fixed schedule or a reactive
  threshold over `(s, E, d)`. The allocation is not a learned adaptive decision, and no
  discrete maintained self-state V sits between the bookkeeping and the maintenance rule.
- **What is supplied vs learned.** Supplied: the recurrence law and decay δ, the budget
  B_t, the paid-write primitive, the discrete code format, the regime announcement, the
  task constants, and the maintenance rule (fixed or reactive). Learned: S_pol's and
  S_reg's weights, and W's content (set by acquisition, held by paid persistence).
- **Intervention map for N2.** I2 (scramble/retain W only, holding sensors and both
  specialists' other inputs fixed) is the decisive test; I1 (cut π's refresh of W) pins
  that W is paid-maintained, not freely recurrent (F1).

**What this baseline does NOT contain (by design):** no explicit self-state V; no learned
adaptive allocator; no self-evaluative pathway E (N4, Phase IV); no consolidation store
Θ_slow (O1, Phase V); no theory-specific loading (attention, predictive coding,
differentiable memory are Q5's, not the core's).

---

## 5. Claim ceiling and what transfers

- **Claim ceiling.** A Phase-III pass earns, at most: **"one maintained representation's
  content is available to two objective-distinct modules that need different information
  and drive different behaviour — N2 at the stated degree."** Nothing stronger. No
  "global broadcast", no "workspace seat" (O3/GWT), no "unified conscious field", no
  metacognition (N4, Phase IV), no autopoiesis, no consciousness claim.
- **N1 is a substrate fact, not a learned-behaviour fact.** It is carried into Phase III
  as the *substrate* (W is paid-persistent), not as evidence that any allocator is
  load-bearing, and it is shared by state-blind schedules (F2). Phase III does not
  re-litigate it; it builds the second specialist on top of it.
- **What transfers from the bridge.** The demotions D9 (no explicit self-state by
  assumption) and D10 (no learned adaptive allocator by assumption) are the negative
  constraints this baseline applies. The methodology — mandatory rival set (P6), gate
  shape matched to claim shape (AC16/17), byte-identity as the composition license (P7),
  seeds as the replication unit with disjoint families (AC39/68), and the collapse record
  as the standing falsification set — binds every G-series card unchanged.
- **What does not transfer.** The organism's physics (rule bank, W/C/B particles,
  conservation economy, succession machine) maps to nothing here (function, not
  realization). No frozen organism number is re-read as a neural result.

---

## 6. Provenance

Reconciled from, and reading the vocabulary of: `BRIDGE_PHASE2_VERDICT_v1.md` (N13;
OUTCOME B + D, the one surviving claim N1, findings F1/F2),
`BRIDGE_FINALS_RESULTS_v1.md` (N11; the frozen measurements, arms 1–10, G-N1/G3b/N3c),
`ACI_MASTER_RESEARCH_TREE_v2.md` (N14; D9/D10, Phase III re-scoped onto N2),
`ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4; the eight components, §5 fields, §7
interventions), `PHASE2_BASELINE_v1.md` (N0; the bridge skeleton and its §3 table),
`ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (Q2; P1–P7, D1–D8), `ACI_PHASE2_BENCHMARKS_v1.md`
(Q6; T1/T3/T4/T5/T7/T8 and the rival set), `ACI_RESEARCH_CONSTITUTION_v1.md` (Q11; the
ten questions, claim ceiling, standing rules), and
`ARCHITECTURE_BY_CLAIM_MATRIX_v1.md` (I0 + extensions; §8 neural-bridge lineage). Organism
study references read from the skill's `references/` dir where named (`ac11`, `ac16`,
`ac17`, `ac39`, `ac68`, `ac109`, `ac110`, `ac116`).

No autopoiesis claim and no consciousness claim is made anywhere in this document. It is a
baseline, not a result.
