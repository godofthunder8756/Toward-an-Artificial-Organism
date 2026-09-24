# S0 synthesis v2 — what the corrections, the boundary successor, and the cognition feasibility probe established, and the single strongest next question

2026-09-24. Terminal synthesis for the S0 card (`t_9e539956`): *what did the R1/R2
corrections, the A1–A4 boundary successor, and the C0 feasibility probe establish, and
what is the strongest justified next question?* Predecessors: A4 (`A4_EXCHANGE_VERDICT_v1.md`,
`t_83513108`), C0 (`C0_FEASIBILITY_v1.md`, `t_8dd15ab9`), W0 (`P1_MANUSCRIPT_DRAFT_v1.md`,
`EVIDENCE_INDEX_v3.md`, `AUTONOMY_RESEARCH_STATUS.md`, `CONSCIOUSNESS_ROADMAP_v1.md`,
`t_67d410e1`). It runs nothing, re-hashes nothing, freezes nothing, and edits no frozen
artifact (no runner, protocol, results dir, hash, or ledger). It reports the seven required
items and chooses one next research question with its cost and its falsification risk.

It **supersedes** `S0_SYNTHESIS_v1.md` (the planning-phase S0, card `t_4ab7a944`), which
chose SR-1 (boundary-mediated exchange) as the single successor requirement. That choice has
now been executed: SR-2 (`ac114.py`) was built, frozen, and confirmed (A1–A4), establishing
boundary-mediated exchange at the material layer. The earlier file is preserved unchanged as
the record. This file is derived and is not hashed into any study's `pre_run_snapshot.json`.

---

## Verdict (one paragraph)

Two tracks, one reconciled account, now carried through its corrections and its two open
probes. The **corrections** (R1, R2) sharpen without overturning anything: the graded/
weighted generalization's frozen "equivalence" label is withdrawn for **no demonstrated
advantage** (R1), and the P2 sufficient-statistic proof's central result is **strengthened** to
an exact statement (R2). The **boundary successor** (AC114, SR-2) established **boundary-
mediated exchange at the material layer** — the produced perimeter retains constituents *and*
mediates the intake that funds production (`B → retention + exchange → production → B`,
established by ablation, not assertion) — resolving the A2 "supplied exchange" limitation and
leaving the full two-clause criterion limited by **two** modeling declarations (supplied space,
non-spatial controller), not three. The **cognition feasibility probe** (C0) closed the
reliability tier: "monitoring the reliability of one's own estimate" is not identifiable as a
separable second-order mechanism; it collapses to first-order inference. Three paper-ready
claims stand. The single strongest next question is in the **cognition track** — whether the
organism's *maintained* (stored) cause-estimate earns its keep in the C2 occluded-gate world,
the designed world where the current observation is ambiguous and only accumulated history
separates the two causes — because it is the one remaining gap that completes-or-falsifies the
level-(c) "maintained representation" claim, at bounded cost and with a prespecifiable gate.
Neither a breakthrough nor exhaustion is claimed; a completed board is not autopoiesis and is
not consciousness.

---

## 1. The corrections, and their effect on previous conclusions

**R1 (`R1_AC113_REANALYSIS_v1.md`) — AC113's F1 label corrected.** AC113 froze "F1:
equivalence" for the heterogeneous-weighting generalization. R1 showed the two histories
within a seed are **byte-identical duplicates**, so the replication unit is the seed, not the
individual: the seed-level sign-flip p is **≈ 0.71 / 0.63, n = 8**, not the frozen n = 16.
"Nonsignificance ⇒ equivalence" is the fallacy R1 corrects. The label is withdrawn for
**no demonstrated advantage** — the maintained two-counter is statistically indistinguishable
from the single counter on post-cause income at the fixed engineering-selected parameters, and
is *worse* on survival, expenditure, and cut false-relinquish. **Effect:** the weighted/
graded generalization is *not* "falsified as equivalence" and *not* a capability falsification;
it is "no demonstrated advantage." The load-bearing object remains decisive-observation
handling plus a counter threshold, not a graded register.

**R2 (`R2_P2_PROOF_CORRECTION_v1.md`) — the P2 proof's reasoning corrected, its result
strengthened.** The original P2 argument used a false "LR irrational and θ rational" premise.
R2 corrects the *reasoning* and makes the *result stronger*: the graded log-odds posterior is
computationally equivalent to an integer ambiguous-failure counter with
`N = ceil(logit θ / LR)`, **exact for every θ** under the matching `>=` convention. The
AC112/113 scaffolding (supplied timing, location, likelihoods, cause structure) is disclosed
as a supplied limitation, not something the organism acquired. **Effect:** the "graded
posterior is an integer counter in float clothing" conclusion stands, now with an exact
construction and without the flawed premise; the two corrections together pin the cognition
track's uncertainty result to a *wall* (a counter suffices), twice over (P2 exact, AC113
organism-scale no-advantage).

**Net effect on previous conclusions.** Nothing was overturned. The three paper-ready claims
(P1 §0) survive. What changed is wording precision: the generalization is "no demonstrated
advantage" (not equivalence, not falsified), the P2 result is exact (not approximately argued),
and the scaffolding is disclosed. The reliability tier's disposition was also re-opened by
this round and then closed by C0 (item 4).

---

## 2. The boundary successor's implementation and measured causal result

**Implementation (SR-2, `ac114.py`, frozen finals 6500–6507, 176 rows, 6/6 gates).** The
entire diff, read from the frozen source, is two source surgeries on `ac4.react` actions 0/1:
(i) intake is wrapped in `if ADMIT(b,c)` — a contact's intake is credited **iff a declared
gate link of channel c is live** (site gate, `GATE_LINKS = {0:(0,), 1:(1,)}, B_MIN=10,
ONSET=512`), taking the frozen failure branch (1 energy, no intake) if the gate link is a
hole; and (ii) the puncture arms add `& ~PUNCTURE` to the action-8 candidate set. The
`reference` arm calls the frozen `ac9.step` object itself, and `ac4.balance` carries
`in_m`/`in_f` as variables, so gating intake to 0 satisfies every conservation identity by
construction. G1 (keep == rival == reference byte-identical, `state_hash`/`ledger`/
`final_inventory`, 16/16) proves the diff is confined to the admission decision.

**Measured causal result.** Three prespecified discriminating predictions pass 16/16 on
untouched seeds 6500–6507:

| Prediction | Meaning | Frozen result |
| --- | --- | --- |
| **D1 — site vs count (decisive)** | puncture the gate link, leave 19 live: a site gate zeroes channel-0 admission; a count gate keeps it | `puncture` `in_f == 0` vs `rival_puncture` 320–480, paired 16/16 |
| **D2 — admission is local** | puncture a non-gate link: admission unchanged | `puncture_non_gate` both channels admit, 16/16 |
| **D3 — semipermeability** | the *same* links retain and admit | `keep`: export 0 AND in_f > 0 AND in_m > 0, 16/16 |

D1 is decisive because the aggregate count rival cannot express "this link is the interface."
Composition (item 5) is established by ablation: `no_B_retention` (site gate) and
`no_B_retention_ref` (no gate) are identical except the gate, and the site gate zeroes
post-onset admission while the twin keeps admitting and survives 16/16 — retention rescued
does **not** restore exchange, so the two roles are separable functions coupled through one
produced structure. `permeant` (exchange present, retention broken) dies by export 16/16.
Renewal (D5): `keep` B_birth 204–207 (~10× turnover), so the interface is *renewed*, not a
one-shot endowment. `B_rescue` (external B matter) is labelled EXTERNAL and never counted as
autonomous production.

**What it established, precisely.** The exchange interface's *presence* is produced (the
finite-lived gate links); the *admission reaction form* and the `GATE_LINKS`/yield constants
remain supplied. This is boundary-mediated exchange **at the material layer** — the stronger
result A2 withheld — not "boundary-dependent intake" and not whole-organization clause (ii).

---

## 3. Which claims strengthened, failed, or remain unresolved

**Strengthened.**
- The P2 sufficient-statistic equivalence is now **exact** (R2), not approximately argued.
- Production closure (clause i) is **extended**: the exchange interface is now a produced
  causal function of B (retention + exchange), not a supplied interface — the A4 verdict's
  "SUPPORTED, unchanged, and now extended."
- Boundary-mediated exchange at the material layer is **newly established** (AC114), resolving
  the A2 §4.2 item-2 limitation.

**Failed / withdrawn.**
- The graded/weighted (two-counter) generalization: **no demonstrated advantage** at organism
  scale (AC113 + R1) — the frozen "equivalence" label withdrawn.
- The C4 "graded strictly dominates the sharpest heuristic" claim: removed earlier (P2) as a
  rival defect; R2 confirms it.

**Closed (not failed).**
- The reliability tier: **not identifiable** as a separable second-order mechanism (C0) —
  supersedes the earlier "blocked with reopening conditions" framing (K8).

**Remain unresolved.**
- **Full two-clause autopoiesis (clause ii) for the whole organization** — met only at the
  material layer; limited by two modeling declarations: supplied space/geometry and the
  non-spatial controller (item 5).
- **Composition of the cognition mechanism with the full autonomy body** — AC111 showed the
  direct channels are clean but full composition retains two failed gates (G3/G5 12/16) as a
  named seed-dependent interference; three-cause integration (corruption as a third cause) is
  untested.
- **Ongoing-repair isolation (C3)** — repair is not load-bearing for correctness/use in the
  decision window, only for post-window storage (AC110 G4 8/16); an exercised, load-bearing
  ongoing-repair loop is unestablished (N1 point 3).
- **The re-acquisition boundary** (candidate move deaths 6100/6107, 6002) — an
  operating-range limit, untested as a mechanism.

---

## 4. The cognition feasibility result (C0)

**Verdict: the "reliability continuation" is NOT identifiable as a separable second-order
mechanism.** Under a label-free criterion, "monitoring the reliability of one's own estimate"
has no referent distinct from:

- **(a)** learning the channel's diagnostic value ε (a first-order world parameter) — ε enters
  the likelihood only *conditional on the latent cause*, so the observable rate
  `r = P(move)·ε + P(cut)·(1/4)` is a continuum of (ε, cause-belief) pairs all producing the
  identical stream (demonstrated: (0.02, 0.435), (0.08, 0.588), (0.125, 0.80) → r = 0.15); or
- **(b)** a function of the sufficient statistic (n_u, n_p) — confidence = tanh(|L|/2) is a
  re-encoding of the first-order counter, predicting nothing it does not already contain.

The third self-referential reading ("is my substrate intact") is AC110's already-answered
substrate question, not cognition. So (c) collapses to (a) or (b); the "second-order" language
describes the *level of a parameter in a hierarchy*, not a distinct cognitive mechanism.
**No probe was run (none authorized); no organism-scale study proposed.** The residue is a
first-order question — acquire and maintain a graded estimate of ε when it varies, and beat a
stale/supplied weight — framed as *parameter learning*, never as "reliability monitoring."
This narrows P4 §9's "reliability tier" from a second-order cognition target to a first-order
parameter-learning target, and it is the disposition now recorded in the roadmap §5/§12.

---

## 5. What the evidence now supports about production closure and spatial unity

**Production closure (M&V clause (i)) — SUPPORTED, bounded, and extended.** Components
{W, C, B, description, derived program} meet C1–C5 and maintained state {pointer, coordination,
route memory, decision state} meets S1–S4, forming one strongly-connected production-
dependency network with no external root, *within the declared model and operating range,
under the accepted substrate convention* (K3; J1 = substrate, resolved). The A4 successor
extends its content without disturbing the verdict: B is now both product and condition of the
production network — production makes B (action 8, W-anchored, program-selected, ~10×
turnover); B sustains the interior through two coupled roles (outward retention barrier,
inward admission gate); and the intake funds the W/C/B production that renews B. That is the
material-layer closure cycle **B → (retention + exchange) → production → B**, established by
ablation (G3, `permeant`, `no_B`), not asserted.

**Spatial unity (M&V clause (ii)) — NOT ESTABLISHED for the whole organization; met only at
the material (constituent) layer.** The produced spatial unity is a unity of the constituent
layer: W, C, B have lattice positions; B is a produced, finite-lived, decaying, semipermeable
perimeter that retains the constituents and admits the resources that fund production, and is
renewed by that production. This is now established in the strong sense A2 withheld. But the
whole organization is the material layer *plus* the informational core (program, description,
route memory, pointer, decision state), and that core lives in fixed arrays never passed to
`tr.move` — it is "inside" only by declaration, not by spatial realization. The two remaining
limits are each a property of the supplied substrate, not an empirical gap: **(1) the space is
supplied** (geometry, lattice, interior/exterior, reflection rule — the infinite-regress
point); **(2) the controller is non-spatial.** The former third limitation (supplied,
non-boundary-mediated exchange) is resolved at the material layer by AC114.

---

## 6. What remains before a stronger whole-organism claim

Three things, none achievable by an in-model run:

1. **A spatial realization of the informational core.** The non-spatial controller is the
   *fixable* limit: program/description/route memory/pointer/decision state would need to be
   positioned and passed to transport — a re-architecture, not a study. The supplied space is
   the *unfixable* limit (infinite regress) and remains permanent substrate. Moving clause
   (ii) for the whole organization is therefore a modeling/architecture decision, not a
   measurement gap (A4 §5–§6).
2. **Composition of the cognition mechanism with the full autonomy body.** The estimate
   discriminates and couples in the *clean two-cause* world; whether it survives the AC105
   combined-challenge body (corruption as a third cause) is untested (AC111 left it open).
   Until then the program's two halves are not shown to hold together.
3. **The level-(c) "maintained representation" half.** In the only world tested, the stored
   bit remembers nothing (C1: storage inert, content load-bearing) and repair is not
   load-bearing in the decision window (C3). The claim's word "maintained" is doing no
   empirical work until storage is shown to earn its keep in a world where history matters —
   the C2 occluded-gate world. This is the item that *can* be addressed by a study, and is
   the chosen next question (item 7).

---

## 7. The single strongest justified next question

**Chosen: in the C2 occluded-gate world — the designed world where the current observation
is ambiguous and only accumulated history separates the two causes — does the organism's
*maintained* (stored) cause-estimate outperform the transient direct-diagnostic rival? I.e.,
is maintained *storage* load-bearing, and not merely the estimate's content?**

The question is the natural synthesis of the C1/C2/C3 line. C1 (AC109) measured that in the
clean world a direct diagnostic reading the same `(bound, used_held, productive)` triple
transiently matches the stored estimate on 48/48 behavioural endpoints at lower cost — storage
inert, content load-bearing. C2 (`C2_TASK_DESIGN_v1.md`, `_c2_identifiability.py`) showed by
design, before any run, that occluding the `used_held` observation on a Bernoulli(q) fraction
of contacts makes the two causes produce an identical current observation while their
histories differ — so a maintained accumulator of the last open-gate conclusion is load-bearing
where the transient discriminator is wrong. C3 (AC110) showed repair is not load-bearing in
the window but is load-bearing for post-window storage. The one thing none of them established
is the claim the level-(c) wording already asserts: that the organism's **maintained storage**
is what carries the load in the world where history matters.

**Why this, against the named alternatives.**

- **The C0 residue (first-order ε-parameter acquisition/maintenance)** is a *third* attempt at
  the graded/weighted generalization. AC113 just showed no demonstrated advantage at fixed
  parameters, and the same per-action economics wall (the paid decision write is starved by the
  income collapse it exists to pre-empt) has killed every internalized decision so far (AC96/97/
  98/101/102/103). Highest falsification risk, narrowest payoff — a channel-parameter learner.
- **Three-cause integration (corruption as a third cause)** is the genuine composition question,
  and the right one for a *stronger whole-organism* claim (item 6.2) — but AC111 already showed
  the corruption-cause interaction is a seed-dependent, survival-neutral behavioural
  interference (G3/G5 12/16), so a three-cause run is likely to reproduce "named interference"
  rather than a clean verdict, at higher cost and with a murkier gate. It is the named runner-up.
- **The autonomy track** is stable within the current model: clause (ii) moves only by
  re-architecture (item 6.1), and the one finite boundary successor is already done (SR-2).
  There is no next in-model autonomy run.

The chosen question is the single most load-bearing open gap in the *paper-ready* level-(c)
claim (P1 §6.3), it has a pre-designed world and a pre-defined rival, and its answer — positive
or negative — is a correction that must travel with the claim either way.

**Cost.** One new runner (an `acN.py` extending the AC107/108 two-cause world with the C2
occlusion gate on `used_held` — a small source surgery on the shimmed retrieval, no frozen file
edited, no conservation law touched), arms = the maintained estimate vs the transient
direct-diagnostic rival (C1's rival) vs a history-free control (and the state-blind fixed-policy
rival where the comparison calls for it), engineering seeds first, then a hashed protocol, then
disjoint final seeds, with audit/replay/unit tests per the extension checklist. Compute is
negligible (the AC line runs ~0.17 s/condition). The real cost is the build + protocol +
prespecified gate + verification discipline — comparable to AC110/AC111 (one runner, one
protocol, three verification tools, a unit-test file; a few sessions). No frozen artifact is
touched, re-run, or re-hashed.

**Falsification risk (two kinds, named separately).**

1. **Hard falsification (real probability).** The maintained estimate does **not** beat the
   transient rival in the occluded world — either the accumulation rule is itself confused by
   occlusion (it latches the last *open* conclusion, which may be wrong under occlusion), or
   the paid maintenance write is starved by the same economics that bounded AC113. Recorded,
   not moved: the level-(c) wording is re-scoped from "maintained representation" to "content
   selector, storage contingent on the task," which is an honest and important correction to
   the paper-ready claim.
2. **Weak-positive (moderate).** The maintained estimate beats the rival only via a raw
   history counter (no cause *attribution*), so the result establishes "history is
   load-bearing" without establishing "the maintained cause-attribution is load-bearing."
   Reported at the weaker level; the attribution-specific rival is added to keep the gate
   discriminating.

**Gate discipline.** The gate is prespecified on **calibration + decision utility** (defer-vs-
act regret in the occluded regime), explicitly *not* survival — per the lineage's rule that a
death must never improve an average and survival is a bimodality-aware lower bound. The
consistency checks are promoted to gates (the transient rival and the maintained estimate must
agree in the q→0 clean limit; the maintained arm with storage cut must reproduce the transient
rival). This is a storage-load-bearing study, not a reflex repair study — the constraint
against auto-adding a repair study after a failed seed is respected: no repair mechanism is
added, and the ongoing-repair question (C3) is deliberately *not* the gate.

**Named, not authorized now.** (1) Three-cause integration (corruption as a third cause) and
the re-acquisition boundary — the composition question, subordinate to this one. (2) The C0
residue (first-order ε-learning) — deferred behind the same economics discipline that bounded
AC113. (3) Any clause-(ii) re-architecture — a modeling decision, not a study.

---

## Sources

`R1_AC113_REANALYSIS_v1.md`, `R2_P2_PROOF_CORRECTION_v1.md`, `AC113_RESULTS_v1.md` /
`AC113_PROTOCOL_v1.md` (P6), `A1_EXCHANGE_SPEC_v1.md` (SR-2), `A2_BOUNDARY_VERDICT_v1.md`,
`A4_EXCHANGE_VERDICT_v1.md`, `AC114_RESULTS_v1.md` / `AC114_PROTOCOL_v1.md` (A3),
`C0_FEASIBILITY_v1.md`, `P1_MANUSCRIPT_DRAFT_v1.md`, `EVIDENCE_INDEX_v3.md`,
`AUTONOMY_RESEARCH_STATUS.md`, `CONSCIOUSNESS_ROADMAP_v1.md`, `S1_SYNTHESIS_v2.md`,
`S0_SYNTHESIS_v1.md` (superseded), `AC109_ENGINEERING_v1.md` (C1), `C2_TASK_DESIGN_v1.md`,
`AC110_RESULTS_v1.md` (C3), `AC111_RESULTS_v1.md` (I1), `CLOSURE_VERDICT_v1.md` (K3),
`C4_P2_EQUIVALENCE_v1.md` (P2), `AC105_RESULTS_v1.md`, `AC107_RESULTS_v1.md`,
`AC108_RESULTS_v1.md`. This document is derived and is not hashed into any study's
`pre_run_snapshot.json`.
