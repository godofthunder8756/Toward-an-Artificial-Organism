# Baseline v3 — reconciled two-track state at HEAD `57ca900`

2026-09-24. B0 bookkeeping deliverable (card `t_707f270f`). Not a scientific claim —
nothing is re-run, re-frozen, re-hashed, or edited; this document only names what the
record already establishes so that the board and downstream planning stop inheriting (a)
claims demonstrated in an earlier architecture, (b) supplied scaffolding attributed to the
organism, and (c) two specific claims that require correction. Frozen artifacts (runners,
protocols, results dirs, hashes) are untouched. Supersedes `BASELINE_v2.md` (two-track state
at `db0ef2f`); the autonomy material is carried forward unchanged. This document is derived
and is not hashed into any study's `pre_run_snapshot.json`.

## Reference

- **Commit:** `57ca900` (P7/A0/W0/S0: feasibility + autopoiesis successor spec + manuscript
  + terminal synthesis).
- **Architecture = two tracks on one organism.** (i) AUTONOMY: the AC105 body (gray streak +
  persistent reconstruction trigger + allowance-42), over the AC86–89 internal-state substrate
  (130-bit stored description, maintained coordination state, generic order-preserving decode).
  (ii) COGNITION: the maintained cause-estimate in its one-bit (AC107/108) and counter
  (AC112/113) forms, terminating in the AC113 F1 frozen result. Neither track stands in for
  the other.

---

## 1. Bounded findings (established — closed with evidence)

These are the reconciled claims the record actually licenses. Each is already satisfied and is
closed here with its evidence and its exact ceiling; do not re-open them.

- **Level (a) production closure — SUPPORTED, bounded** (K3 / `CLOSURE_VERDICT_v1.md`).
  Components {W, C, B, description, derived program} meet C1–C5; maintained state {pointer,
  coordination, route memory, decision state} meets S1–S4; a single strongly-connected
  production-dependency network with no external root; substrate convention J1 = substrate,
  resolved. Clause (ii) spatial unity is met only at constituent-retention level (A2) — see §5.

- **Level (b) adaptive autonomy — ESTABLISHED** (AC99–AC105, 6/6 gates). The Gray-coded
  relinquishment streak (AC99/100), persistent reconstruction trigger (AC103), and allowance-42
  spending rule (AC104/105) coordinate the paid reconstruction write with the paid decision
  write; the organism acquires then relinquishes route content on its own viability conditions
  under corruption across a predeclared grid.

- **Level (c) representational coupling — with the survival caveat attached** (AC107/108).
  A maintained one-bit cause-estimate discriminates two causes at ceiling accuracy (0/32
  mistakes, AC107) and is causally coupled to its maintenance in both directions by the paid
  acquisition/update write (AC108). **Caveat:** the coupling is behavioural, not
  viability-advantageous — adaptation reversal 16/16, survival reversal 12/16; no survival
  advantage anywhere (AC107 Q4, AC108, AC113). Claimable only as "meets candidate indicator
  HOT-2 at degree Y"; never "metacognitive", never "conscious".

- **First-order uncertainty — bounded twice.** The graded posterior is an integer counter
  (P2, exact); heterogeneous (two-dimensional non-integer) weighting is NOT load-bearing at
  organism scale (AC113 F1). A maintained integer counter suffices. The load-bearing objects
  are decisive-observation handling plus a counter threshold, not a graded register. This
  bounds the *representation*; it does not touch the mechanism's content/coupling.

## 2. Claims requiring correction (flagged — NOT yet corrected; unblocks R1, R2)

Two claims now on record are wrong as stated and require correction before any downstream
document (manuscript, evidence index, synthesis) may carry them. Neither correction is done;
both are open `todo` cards.

- **R1 (`t_91e88df2`) — the AC113 F1 "equivalence" decision rule.** The frozen G-COMPARE rule
  (`AC113_PROTOCOL_v1.md` §8) maps `mean(d_i) < 0 AND p > 0.05` to **F1 (equivalence)**. That
  is "nonsignificance ⇒ equivalence", which does **not** establish statistical equivalence
  (absence of evidence ≠ evidence of absence). The measured mean is *negative* (−2336 / −2344),
  i.e. the two-counter is marginally worse, not tied. And "matches every decision-relevant
  endpoint" is contradicted by the recorded collapse tail: the two-counter dies on 2/16 finals
  under cut at θ*=0.5 where the single-counter survives 16/16. The audit that "passes"
  reproduces the flawed rule; it does not validate its interpretation. R1 must re-analyze the
  saved rows (no rerun) with seed-level dependence (seeds are the units, not histories),
  separate the engineering-selected comparison from the finals-selected optima, report effect
  sizes and the observed survival failures, and adopt the corrected headline — without
  retrofitting an equivalence margin as confirmatory.

- **R2 (`t_ba8011c3`) — the P2 "no rational threshold coincides" claim is FALSE.**
  `C4_P2_EQUIVALENCE_v1.md` §3 reasons that because `LR = log(4/3)` is irrational and every
  grid `θ` is rational, `logit(θ)/LR` is never an integer. That is false: `logit(4/7) =
  log((4/7)/(3/7)) = log(4/3) = LR` exactly, so the ratio is the integer 1. The general
  solution `logit(θ)/LR = k` ⟺ `θ = (4/3)^k / (1+(4/3)^k)` is rational for every integer k
  (θ = 1/2, 4/7, 16/25, 3/7, …). The fact that actually carries the proof is *numerical and
  grid-specific*, not a rationality argument: over the used grid {0.5,…,0.95} only θ=0.5 sits
  exactly on a boundary (k=0, handled by the `>=` convention), and the nearest non-zero
  distance is 0.0296 at θ=0.85 — verified by the boundary check, not by irrationality. **The
  central result survives** (graded posterior ≡ integer counter under matched decisive
  handling); only the stated reasoning must be repaired, with explicit equality handling and
  exact-boundary checks. R2 must also disclose the AC112/113 operational scaffolding (§3) as
  limitations and draw the four distinctions in its body (behaviourally-causal vs informative;
  sufficient integer representation vs absence of uncertainty; one failed immediate rival vs
  all-memoryless-proof; acquisition/update dependence vs ongoing-repair dependence).

## 3. Supplied scaffolds (disclosed limitations — not organism demonstrations)

- **Timing — `self.now < CUT_TICK`** (`ac112.py:312, 383, 426`). The estimator's update/decide
  path only operates on/after the supplied intervention tick; the timing of the two causes is
  host-supplied, not acquired.
- **Location — channel-1 specialization** (`key != 1` branches, same sites). Only channel 1
  moves/cuts/occludes; channel 0 is structurally inert. Which channel fails is supplied.
- **Interpretation — `prog.choose`** (`ac9.py:84` `action=prog.choose(b.traces,observe(o))`).
  The 126-bit-rule interpreter is supplied format-level machinery; J1 resolves it as acceptable
  substrate, not an undeclared coordinator.
- **Coordination — `advance()`** (`ac89.py:378`, `ac91.py:361`, `ac92.py:371`). The succession
  transition logic is supplied format-level machinery; J1 substrate, resolved.
- **Supplied likelihoods and cause assumptions** — the weights `w_u = log((4/3)(1−ε))`,
  `w_p = log(4ε)`, the residual yield ε, and the occlusion q are world constants / supplied
  values, not quantities the organism estimates (R2 must disclose these alongside the four above).

## 4. Evidence demonstrated only in earlier architectures (AC10–95)

The load-bearing-maintenance and production-machinery results are established in the AC10–95
autonomy body, not re-demonstrated in the current cognition architecture. Do not inherit them
into the AC107–113 estimate as if measured there:

- Constituent ablations — no W / no C / no B (AC10); the boundary's role is retention, not mass.
- Repair loop load-bearing under non-self-reversing damage (AC67); the single-replica→majority
  read/repair-threshold alignment (AC69/71).
- Erase-on-relinquishment world-accommodation (AC75).
- Description maintenance / recipe succession / stored bank-rule convention (AC79–AC89).
- W-catalyst machinery load-bearing for reconstruction + coordination (AC91); functional
  interruption-and-rescue (AC92); turnover accounting (AC84).

Consequence for the cognition track: AC113 ran `corrupt=False` (no reconstruction fired), and
repair-dependence of the decision state was explicitly AC110's question, out of AC113's scope.
So the estimate's maintenance-dependence is established (AC108/110) in the AC110 architecture;
nothing in AC113 re-tests it. The counter bits under a *live* reconstruction remain a
unit-level assertion (P7), not a study.

## 5. Proposed mechanisms NOT yet implemented

- **SR-1 — boundary-mediated exchange** (`A0_SUCCESSOR_SPEC_v1.md`). Re-specify `react` actions
  0/1 so intake `in_m`/`in_f` is conditioned on produced boundary state (an aggregate integrity
  gate), with T1–T4 causal tests. Spec written; **not built, no runner, no seeds.** This is a
  re-architecture (a change to a supplied reaction's dependence), the only open question that
  moves the clause-(ii) verdict. A1 (`t_395079ed`) must first replace the claim/test spec —
  the aggregate B-count gate's ceiling is "B-dependent intake", NOT transport through a
  produced interface.
- **Reliability tier (second-order uncertainty — estimated ε / `P_YIELD`).** Distinct and
  identifiable (C4 §11 / K8 reopening condition 2 / P4 §9), but deferred on the AC113
  per-action-economics wall (a decision-theoretic weighting advantage does not transfer when a
  false relinquish refreshes the entry and holding carries entry-expiry cost). Gated on a
  harness-level probe (corrected economics, varying ε, estimated-vs-frozen weight) — **not**
  authorized as an organism-scale study (P7). Not implemented.

Explicitly NOT successors: supplied space (permanent substrate, infinite regress) and the
non-spatial controller (a separate full re-architecture, out of scope).

---

## 6. Board reconciliation

- **Already satisfied (closed with evidence above, §1–§2's positive half):** the three bounded
  findings, the P2 integer-counter equivalence, and the AC113 F1 result (as a *recorded
  falsification*, not as a support claim). The P/A/W arc is closed (S0/P7/P6/P5/W0 all `done`).
- **Open `todo` cards (genuinely open, none pre-satisfied):** R1 (`t_91e88df2`), R2
  (`t_ba8011c3`), A1 (`t_395079ed`), and their descendants A2 (`t_e7781faf`), C0
  (`t_8dd15ab9`), A3 (`t_d753dfba`), A4 (`t_83513108`). Completing B0 unblocks R1, R2, A1
  (parent edges); A2/C0/A3/A4 remain gated on their own parents.
- **Stale directives:** `RESUME_RESEARCH.md` (AC10-era), `DEPENDENCY_AUDIT_v1.md` (pre-AC79),
  `CLOSURE_BOUNDARY_v1.md` (superseded by v2) — carried forward from v1/v2, unchanged.

## Sources

`S0_SYNTHESIS_v1.md`, `P7_FEASIBILITY_v1.md`, `AC113_RESULTS_v1.md`, `AC113_PROTOCOL_v1.md`,
`A0_SUCCESSOR_SPEC_v1.md`, `C4_P2_EQUIVALENCE_v1.md`, `P1_MANUSCRIPT_DRAFT_v1.md`,
`EVIDENCE_INDEX_v3.md`, `AUTONOMY_RESEARCH_STATUS.md`, `BASELINE_v2.md`, `CLOSURE_VERDICT_v1.md`
(K3), `A2_BOUNDARY_VERDICT_v1.md`; code `ac112.py`, `ac113.py`, `ac9.py`, `ac89.py`,
`ac91.py`, `ac92.py`. Verification: `logit(4/7) = log(4/3)` and the general rational solution
`θ = (4/3)^k/(1+(4/3)^k)` were checked numerically against this repo's `.venv` interpreter.
