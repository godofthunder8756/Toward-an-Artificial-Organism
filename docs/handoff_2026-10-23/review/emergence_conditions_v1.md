# Emergence conditions v1: what pressures should make C3 and C4 structure emerge under ordinary learning

**Draft, theory and design only.**

- Written 2026-10-20 (EDT) by Research Delegate for the ACI Research Specialist, for Aidan
  Ahern.
- **Nothing was run.** That means no solver, replay, enumeration, certificate search,
  training or arithmetic script.
- **Repo untouched.** `/workspace/repo` was read only: master at `32cfbe6`, plus
  `git show` of branch `origin/elminster/loving-ptolemy-ityj4l` at `33fa803` with no
  checkout.
- **Untouched:** v1 of the theory queue, N4 and the indicator matrix.
- **No consciousness claim.** "Consciousness-relevant structure" here means only C3/C4 as
  defined in the ledger. Nothing below says or implies that any system meets C7.
- **Four questions, kept apart.** Every claim is tagged **Q-EXIST** (can the class
  realize it), **Q-LEARN** (does ordinary development acquire it), **Q-CAUSE** (is it
  used, by intervention) or **Q-NECESSITY** (what does it add against the strongest
  simpler rival). This document is about Q-LEARN. Wherever Q-LEARN depends on a Q-EXIST
  precondition, that dependence is stated.
- **Goal, as stated by the Research Specialist.** Show and reverse-engineer how the
  structure *emerges*. Do not build it in, and do not win on efficiency. Value margins
  are therefore reported context, never the gate. This follows constitution v3, "Keep
  causal role, property-relative necessity, and engineering advantage separate", and
  `SCARCITY_GAP_v1.md` §4.

---

## 0. One-paragraph answer

**The organizing fact is the sufficiency regime.** On the branch,
`SCARCITY_GAP_v1.md` §2 shows that when the agent can hold a sufficient statistic of
everything its consumers will be asked (`ρ = log K / H(S) ≥ 1`), every workspace,
monitor or self-state is a relabelling of the world posterior. A learner in that regime
has **no pressure** to grow a C3 or C4 structure. If one appears anyway, the conventional
rival explains it by construction. So **every pressure below is a candidate only insofar
as it pushes the agent below sufficiency, or breaks the ideal-observer premise.**
`C1_RELIABILITY_DISPOSITION_v1.md` already showed that breaking that premise is the
only place a reliability referent becomes identifiable.

Of the four pressures:

- **Paid maintenance under scarcity (P1)** and **hidden damage to the agent's own
  machinery (P3)** are the two that do this *intrinsically*. P1 is chosen garbling; P3 is
  involuntary garbling.
- **Non-stationary channel reliability (P2)** does it only when combined with P1 or P3.
  Alone it reduces to joint filtering. This is the same reduction that made M1
  REDUCED in `c_axis_theory_queue_v2.md` §3.2.
- **Multiple specialist consumers (P4)** is a C3 pressure only below sufficiency.
  Phase III/III-B show that broadcast or a free code wins otherwise. It is a C4
  pressure only if the content can carry a tag the consumer cannot recompute itself.

**C4-specific point.** No single pressure yields a *distinct* evaluator. A distinct
evaluator additionally needs a **temporal or spatial separation** between what the
evaluator holds and what the first-order state holds (Fleming & Daw 2017, as used in
C1). Hidden decay or damage provides that separation naturally: the agent's record of
its own state can go stale. This gives the leading candidate **P1×P3**: a maintenance
budget below demand, plus hidden decay of the maintained machinery.

**Cheapest falsifiers.** All are analytic Q-EXIST certificates, which must pass before
any Q-LEARN run. In rank order:

1. P1 (C3/access part)
2. P1×P3 (C4 part)
3. P4 (C3 at ρ<1)
4. P2 (already decided standalone)

Everything touching C4 needs Aidan's approval (§5).

---

## 1. What "emerges" must mean here (operational criteria)

A structure **emerged under Q-LEARN** only if **all** of the following hold. Each is
pre-declared, and each can be falsified.

| # | Criterion | Why |
| --- | --- | --- |
| E1 **Not supplied** | The architecture family has no module, loss term, target, auxiliary head or routing rule dedicated to the structure. Example: no confidence target, no separate "evaluator" head, no supplied broadcast slot. | Astra #3: "Detachable head makes lesionability trivial." A supplied head passes C4's lesion limb for free. |
| E2 **Pressure-dependent** | Same architecture, same learner, same compute. The signature is present with the pressure **on** and absent with it **off**. | Within-system contrast (`SCARCITY_GAP_v1.md` §4, Baars' contrastive method). Separates "the pressure made it" from "the architecture always does this". |
| E3 **Dose-response and collapse** | Across a declared ρ family, the signature is zero at ρ ≥ 1 and non-zero only below. | `SCARCITY_GAP_v1.md` §7 S1. A non-zero signature at sufficiency is a bug or an artefact, not emergence. |
| E4 **Ceiling-separated** | The learned system is compared with the analytic optimum at matched capacity (an R10-style ceiling). | The III-B lesson (`PHASE3B_VERDICT_v1.md`, `PHASE3B_R10_CERTIFICATION_v1.md`). It keeps "the optimum lacks it" (a Q-EXIST failure) separate from "the learner did not find it" (a Q-LEARN failure). |
| E5 **Intervention-identified, decoder-free** | The structure is identified by causal interventions on inputs, on organizational variables (budget, damage, maintenance) or on pre-declared structural partitions. It is never identified by a trained probe or decoder. | Constitution v3 Q-CAUSE: "A probe is not enough." Li et al. 2023 show why: probe-defined variables need a separate interventional validation. |
| E6 **Conjunction-shaped (C4 only)** | The signature instantiates all three limbs of Astra's conjunction (`c_axis_theory_queue_v2.md` §1). | This is the C4 criterion now in force. |

**Ordering of the four questions.** Q-EXIST (the optimum at matched capacity contains the
structure) is a *precondition* for an emergence claim, not part of one. If the optimum
does not contain it, Q-LEARN finding it would be a suboptimal artefact, so an emergence
claim needs a different justification. Q-CAUSE is what E5 and E6 test. **Q-NECESSITY is
not claimed anywhere in this document.** Emergence does not imply the structure is
needed.

### 1.1 A decoder-free template for Astra's conjunction

This template is reused for every pressure below.

- **Limb 1 (referent).** Make two interventions that leave the *instantaneous evidence
  statistics* identical:
  - a **system change**: covert damage, decay or budget cut on the agent's own machinery;
  - an **evidence change**: matched stimulus degradation.

  The candidate's evaluation-type behaviour must track its *own* correctness under both,
  and must respond **differently** to the two. Evaluation-type behaviour means opt-out,
  wagering, information seeking, repair spend or re-routing. The ideal-observer rival
  treats the two identically wherever they induce the same likelihoods.
- **Limb 2 (selective causal content).** Corrupt or swap the evaluator content while
  holding the full first-order state. The decoder-free form is a **history transplant**:
  clamp the first-order state, and replay to the remaining substrate the
  self-relevant history (feedback, maintenance or damage history) of a *different*
  trial. Prediction: directional evaluation errors, with one pre-declared downstream
  consequence. Examples are confident errors, unnecessary opt-out, or misdirected repair
  spend. **Matched rescue:** restore the original history, and the errors reverse.
  - **Open problem (O1).** In a monolithic learned network, "hold the full first-order
    state" needs a partition, and finding that partition without a decoder is not
    solved here. It is clean only where the organizational variable is explicit, as in
    the organism harness's maintenance and allocation registers. Those registers are
    *supplied*, which bears on E1. See §6, C2.
- **Limb 3 (reduction).** Give the strongest adaptive rival the same information,
  resources and interventions, and compare the **whole** intervention-response pattern.
  Ruling R-A1 (v2 §3.2) puts **unlabeled self-consistency adaptation** inside
  "conventional".

---

## 2. C3 (shared availability): pressures, signatures, rivals

**Ledger status.** C3 is PARTIAL (`ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json`). The ceiling
is "broadcast can realize bounded coordination; no workspace necessity". The rival is
"joint filter, monolithic recurrence and scalar broadcast". Evidence:
`PHASE3_VERDICT_v1.md`. Counterevidence: `PHASE3B_VERDICT_v1.md`, where R9's free
eight-symbol code beat the structured candidate in 15/16 seeds.

**Target for emergence.** A single internal state whose content is (a) selected under a
limit, and (b) jointly causally available to several consumers. The contrast is private
per-consumer copies.

### C3-P1. Resource scarcity with paid self-maintenance

- **Why it should emerge (Q-LEARN hypothesis).**
  - `SCARCITY_GAP_v1.md` §6: with a maintenance budget below the cost of keeping all
    acquired content alive, *maintenance allocation is selection*. The capacity at any
    moment is whatever the agent chose to keep alive.
  - If several consumers draw on the same maintained content, keeping one shared copy
    alive is cheaper than keeping k private copies. Paid upkeep therefore pressures
    toward sharing.
  - The program's only robust positive, N1 (paid persistence is causally necessary
    under decay; `BRIDGE_PHASE2_VERDICT_v1.md`, `PHASE3_VERDICT_v1.md`), is what powers
    this.
- **Q-EXIST precondition.** `scarcity_v1` on the branch gives an exact certificate:
  - goal-dependent selection is strictly optimal in 24/63 scarcity cells;
  - collapse holds at K = 8 in 9/9 cells.

  Magnitudes are small (max 1/8). This is fixed capacity, not paid maintenance; the
  paid-maintenance version is §7.2 of that file and is **not done**.
- **Emergence signature (decoder-free).**
  - **Covert maintenance withdrawal.** Withdraw maintenance from one content item
    covertly, with no observation change. Every consumer that uses the item degrades
    *together*, and consumers that do not use it are unaffected.
  - **Converse.** Covertly boosting upkeep of a non-selected item does not improve any
    consumer unless that item is the shared one.
  - **Coherence.** Under private copies, the same withdrawal hits only the consumer
    whose copy decayed. That consumer-specificity pattern is the discriminator.
  - **Dose-response.** Sharing should rise as the budget-to-demand ratio falls (E3).
- **Conventional rival.**
  - Static duty-cycle allocation plus a threshold on observables (age, cue). Phase II
    reduced exactly this way (`BRIDGE_PHASE2_VERDICT_v1.md`: integrity readable from
    age).
  - Same-budget random-allocation yoke.
  - Monolithic recurrent learner at the same budget.

  The rival explains "shared degradation" if the shared item is shared merely because it
  is the only one the static schedule maintains. The discriminator is therefore
  **goal/cue-dependence** of *which* item is shared.

### C3-P2. Non-stationary reliability of own channels

- **Why it might emerge.** If channel reliabilities drift covertly, every consumer needs
  current channel weights. One shared reliability-weighted estimate is cheaper than k
  separate filters.
- **Why it probably does not, standalone.** At ρ ≥ 1, each consumer can receive the
  joint posterior over (world, channel reliabilities). Phase III's "free scalar LLR
  broadcast beats paid workspace" is the template. The shared state is then just
  broadcast of a sufficient statistic, which the ledger already concedes to the rival.
- **Signature.** Covertly perturb one channel's noise. A shared estimate shifts all
  consumers' channel weighting **in lockstep, with one shared lag**. Independent filters
  show k independent lags.
- **Rival.** Scalar or joint-filter broadcast; adaptive conformal per consumer. The
  lag-coherence test still fails to separate a broadcast filter from a workspace, since
  both have one lag. It separates only shared from private.

### C3-P3. Damage to own machinery (O3 loop)

- **Why it should emerge.** When one specialist pathway is damaged, the remaining
  consumers must learn *what is still available*, and routing must change. That is
  shared availability about the agent's own machinery. It touches the unestablished O3
  arrows "content → future machinery" and "machinery → future content"
  (`ACI_RESEARCH_SYNTHESIS_v1.md`, O3 arrow audit).
- **Signature.** Covertly lesion pathway A. All consumers re-route away from A within
  one shared adaptation episode. Then *covertly repair* A: re-routing reverses only
  after evidence of repair arrives, and it reverses for all consumers together.
- **Rival.**
  - Redundancy plus majority vote. `SUB_A_ANALYTIC_CHECK_v1.md` showed live repair
    reduces to "repetition code + host median".
  - Per-consumer error-driven relearning.

  Sub A's warning is that "disagreement aliases correct/wrong".
- **Gate.** In the organism, this is **organism re-entry**, which constitution v3 says
  needs human authorization.

### C3-P4. Multiple specialist consumers

- **Why it should emerge.** Multi-task training of one recurrent network produces shared
  and compositional task representations without any supplied workspace (Yang et al.
  2019). That is the canonical case of shared structure emerging from consumer demand
  alone.
- **Why it did not help here.** Phase III-B: with enough channel, an unrestricted code
  (R9) holds everything, so there is no pressure toward *selection*, only toward
  *sharing*. `SCARCITY_GAP_v1.md` §1 reads III-B's capacity as binding only "shallow",
  with a certified penalty of about 0.0205, roughly the 0.02 gate margin.
- **Signature.**
  - **Exclusivity under load.** At ρ < 1 with consumers whose queries conflict,
    covertly favouring consumer i's cue changes which content *all* consumers can
    use. That is a capacity trade-off visible across consumers.
  - **Positive check.** Consumer j's performance drops exactly on the items displaced.
  - **Contrast.** Private copies predict no cross-consumer trade-off.
- **Rival.** Static partition of capacity among consumers ("cue_blind" in scarcity_v1);
  a free code at the same K.

---

## 3. C4 (evaluator-like structure): pressures, signatures, rivals

**Ledger status.** C4 is NOT_ESTABLISHED. The rival is "first-order statistic, count or
reflex". The criterion in force is Astra's conjunction (v2 §1).

**Prior art on emergence.** Confidence-like behaviour emerges readily under reward alone,
and this is the *problem*, not the solution:

- **Song, Yang & Wang (2017).** Reward-trained recurrent networks, with no confidence
  target, learned post-decision wagering. They chose the sure option more on hard
  trials, and were more accurate when they waived it.
- **Orhan & Ma (2017).** Generic networks trained with non-probabilistic feedback came
  to perform near-optimal probabilistic inference.
- **Kepecs et al. (2008).** Confidence behaviour in rats.
- **Kadavath et al. (2022).** In large language models, calibration and P(IK) appear.

In all of these, the emergent "confidence" is explained by a **readout of the
first-order state**. That is the "same-information second readout" rival.

So "opt-out emerged" is **not** a C4 emergence signature. What has to emerge is evaluator
content that is selectively mistakable while the first-order content is right. By
Fleming & Daw (2017), as applied in `C1_RELIABILITY_DISPOSITION_v1.md`, that requires a
**separation between the evaluator's information and the first-order state over space
and/or time**. The question for each pressure is therefore whether it creates such a
separation.

### C4-P1. Scarcity with self-maintenance

- **What it creates.** A genuine *agent* referent. Below sufficiency, the agent's
  confidence departs from the world's by an amount set by its own encoding
  (`SCARCITY_GAP_v1.md` §2, "self-induced uncertainty", non-zero in 63/63 scarcity cells).
  An **access record**, "what this state lets me answer", is strictly optimal over
  static access in 14/63 cells, with max 1/24.
- **What it does not create.** A *distinct* evaluator. In the certificate, the access
  record is part of the same codeword (`0--`, `00-`). It is the memory code itself, not
  a second structure that could be wrong while content is right.
  - **Clean world.** Forced choice on opted-out trials is exactly 1/2 everywhere, so
    there is no partial-access dissociation.
  - **Reading.** P1 alone predicts C3/AST-type **access** emergence, not C4 distinctness.
- **Signature, if it went further.** S2 of `SCARCITY_GAP_v1.md` §7: opt-out with
  above-chance forced choice on trials where the *ideal observer was certain*. S3: the
  agent's meta-d′/d′ falls below the ideal observer's only at ρ < 1.
- **Rival.** `no_opt`, which wagers by ideal-observer confidence; static opt-out; a
  same-capacity monolithic learner whose opt-out is a readout of its own garbled state.
  That last rival is decisive: at matched K, P(correct | m) is a function of m.

### C4-P3, and the leading combination P1×P3: hidden machinery decay under a maintenance budget

- **What it creates.** Two things.
  1. *A referent that is unambiguously the agent's machinery.* Damage to inference
     machinery breaks the ideal-observer premise directly. The damaged posterior differs
     from the ideal one by an amount set by the damage. This is exactly C1's
     identifiability condition.
  2. *A temporal separation for free.* If decay is hidden and maintenance is budgeted,
     the agent's record of which machinery it kept intact was written at upkeep time
     and is read at query time. Between the two, hidden decay can make the record
     **stale while first-order processing reflects the actual machinery**. That is the
     selective-mistakability structure C4 needs, and here it arises from the world's
     dynamics rather than from a supplied evaluator.
- **Emergence signature (decoder-free; all three limbs).**
  - **Limb 1.** Covert decay of pathway A (system change) versus matched stimulus
    degradation (evidence change), with the same instantaneous likelihoods.
    - A learned upkeep or damage record predicts own wrongness under the system change.
    - Under the evidence change, it predicts wrongness only through the evidence.
    - The two response patterns differ, for example in opt-out, repair spend or
      re-routing.
  - **Limb 2.** History transplant. Clamp the first-order state and replay to the rest
    of the substrate the upkeep history of a trial in which A was maintained, then
    present a query that uses A after A has *actually* decayed.
    - **Predicted directional error.** A confident error on A-dependent queries (an
      evaluation error).
    - **Pre-declared downstream consequence.** No repair spend on A in the next upkeep
      cycle.
    - **Matched rescue.** Restore the true history, and both the opt-out and the repair
      spend return.
    - **Converse.** Transplant a "not maintained" history onto an intact A. The
      prediction is unnecessary opt-out and wasted repair spend.
  - **Limb 3.** Run the same interventions on the adaptive rival. If the whole response
    pattern matches, the case is REDUCED.
- **Conventional rivals at parity.** At least these three:
  1. **Per-pathway adaptive selective prediction.** This is Mondrian or adaptive
     conformal conditioned on which pathways a query uses, updated from outcome
     feedback *or* from unlabeled agreement (Ruling R-A1).
  2. **Redundancy plus vote**, with disagreement as the damage signal (Sub A).
  3. **Elapsed-time threshold on observables** (Phase II).

  Rival 1 is the hard one. It also lags behind hidden decay, so it also shows a limb-2
  stale-record error. The candidate separates only if its errors are **specific to the
  upkeep history** and not just to elapsed time or outcome history. That is why the
  limb-2 transplant must swap *upkeep* history while holding *outcome* history fixed.
  Whether the optimum distinguishes the two is open, and it is the first thing the
  certificate in §4 must decide.
- **Prior art on self-models under damage.** Both of these *supply* the self-model
  machinery:
  - Bongard, Zykov & Lipson (2006): continuous self-modelling for damage recovery.
  - Kwiatkowski & Lipson (2019): task-agnostic learned self-models.

  They show the referent is usable, not that it emerges unbidden. Cleeremans (2011) and
  Cleeremans et al. (2020) argue, as a theoretical hypothesis, that metarepresentation is
  *learned*. They are cited only as the theoretical motivation for asking Q-LEARN, not as
  evidence.

### C4-P2. Non-stationary reliability of own channels

- **What it creates.** Temporal separation, because reliability is learned from history.
  The task needs an estimate of one's own channel reliability, and volatility tracking
  emerges in humans (Behrens et al. 2007) and in meta-RL networks without supplied
  machinery (Wang et al. 2018).
- **Why it reduces standalone.** At ρ ≥ 1, channel reliability is a latent variable of
  the generative model, and the joint filter over (world, reliability) is the
  sufficient statistic.
  - **Precedents:** this is the C0/C1 collapse, and it is the v2 §3.2 constructive
    mapping that made M1 REDUCED. By Ruling R-A1 the reduction holds even for
    unlabeled self-consistency adaptation.
  - **Q-NECESSITY:** at sufficiency there is nothing to find.
- **When it stops reducing.** When it is combined with P1 or P3 so that the joint filter
  cannot be held, or so that the channel *is* the agent's damaged machinery. Then it
  becomes a special case of P1×P3.
- **Signature, if combined.** The limb-1 system/evidence contrast, with the system
  change applied to channel gain inside the agent rather than at the input.
- **Rival.** Hierarchical or volatility filter (Behrens-style); adaptive conformal
  (Gibbs & Candès 2021).

### C4-P4. Multiple specialist consumers

- **What it creates.** A need for the producer to tell each consumer *whether the shared
  content is good enough for that consumer's query*. That is a tag accompanying content,
  as in PRM-style tags (Lau 2022) and theory-family background in v2 §2.
- **Why it reduces standalone.**
  - Phase III: a scalar LLR broadcast *is* such a tag, and it is a function of the
    content's sufficient statistic.
  - If consumers can see enough of the state, each consumer's own readout is the
    same-information second readout.
- **When it does not reduce.** The tag is non-redundant only if it carries information
  about the *producer's machinery* that the content message cannot carry within the
  channel limit. That requires P1 or P3 again.
- **Signature, if combined.** Swap the tags between two messages while holding content.
  - **Predicted errors:** consumers make directional errors (they trust bad content
    and discard good content).
  - **Pre-declared consequence:** consumer-side opt-out or re-query rates shift in the
    tag's direction.
  - **Matched rescue:** swap the tags back.

  Tag position in a message is a structural partition, so no decoder is needed. But the
  message format is a design choice and can amount to a supplied slot (E1 risk).
- **Rival.** Scalar LLR broadcast; per-consumer adaptive selective prediction on the
  received content.

### 3.1 Summary table

| Pressure | C3 emergence plausible? | C4 *distinct* evaluator plausible? | Separation source | Hardest rival |
| --- | --- | --- | --- | --- |
| P1 scarcity + paid upkeep | **Yes, below sufficiency** (selection and access certified small-positive at fixed K) | Access record yes; distinctness **no** alone (same codeword) | None alone | Same-K monolithic learner; static allocation |
| P2 non-stationary reliability | Weak (broadcast filter) | **No** standalone (M1/C0 reduction) | Temporal, but held by joint filter | Joint/volatility filter; adaptive conformal |
| P3 hidden machinery damage | Yes (re-routing availability) | **Candidate** (breaks ideal-observer premise) | Temporal (stale record) | Per-pathway adaptive SP; redundancy + vote |
| **P1×P3** | Yes | **Leading candidate** | Temporal: upkeep record vs actual decay | Per-pathway adaptive SP with upkeep-blind history |
| P4 multiple consumers | **Yes, only at ρ<1** (Yang 2019 shows sharing emerges; III-B shows the free code wins at ρ≈1) | Only with P1/P3 (tag about producer machinery) | Spatial (producer vs consumer) | Scalar LLR broadcast |

---

## 4. Ranking by cheapest analytic or small-engineering falsifier

**Rules.**

- No new architecture families.
- The falsifier is for the **Q-EXIST precondition** of each emergence claim: does the
  matched-capacity optimum contain the structure? If not, the Q-LEARN question for that
  pressure is closed with a reason.
- Q-LEARN runs come only afterwards. They need separate approval and an R10-style
  ceiling.
- Costs are qualitative. Nothing was run to estimate them.

| Rank | Pressure / layer | Cheapest falsifier (design only) | Apparatus | Falsified / parked if | Needs Aidan's C4 approval? |
| --- | --- | --- | --- | --- | --- |
| **0 (decided)** | P2 standalone, C3 & C4 | None needed. Blackwell collapse (`SCARCITY_GAP_v1.md` §2) plus the v2 §3.2 constructive mapping already predict REDUCED at ρ ≥ 1 | Proof already in hand | — (already reduced; reopen only inside P1/P3) | No (no study) |
| **1** | P1, C3 + access (selection, access record) | Extend the branch's `scarcity_v1` exact certificate per its §7.1 (graded evidence) and §7.2 (refresh budget under hidden decay). Report selection value and access value over a declared ρ family. Rivals: `static`, `cue_blind`, `no_opt`, random-allocation yoke | Analytic exact enumeration; existing stdlib code on branch `elminster/loving-ptolemy-ityj4l` | Selection and access value are zero in every scarcity cell of the declared family, or non-zero at ρ ≥ 1 (bug) | **Partly.** The §7.1–7.2 selection/access quantities are C2/C3-boundary (the branch's own Q11), but `SCARCITY_GAP_v1.md` §7 already says "human gate required". The S3 meta-d′ signature is C4-adjacent: flag it and treat it as needing C4 approval. |
| **2** | **P1×P3, C4** (distinct evaluator via stale upkeep record) | Smallest finite POMDP: 2 pathways, hidden per-pathway decay, refresh budget below demand, queries using one pathway, opt-out. Exact matched-K optimum. Test whether the optimal state contains an upkeep-history component that is *not* a function of (outcome history, elapsed time), i.e. whether limb 2's upkeep-vs-outcome transplant has an effect in the optimum. Rivals: per-pathway adaptive SP (label-driven and unlabeled), redundancy + vote, elapsed-time threshold | Analytic; same enumeration style as `scarcity_v1`; no new family | The optimum's evaluation-relevant state is a function of (outcome history, elapsed time) at every declared cell, giving constructive equivalence to the adaptive rival (REDUCED, like M1) | **Yes.** First C4 research (constitution v3; Ruling R-A2 by analogy). Free parameters (decay rates, budget, costs) **unset** until approval. |
| **3** | P4, C3 at ρ < 1 | Re-certify the Phase III-B world's R10 ceiling with a declared capacity axis below ρ = 1: does certified headroom for *selection* (not just sharing) exceed the gate margin by a declared factor? Analytic re-certification only, no training | Analytic, extending `PHASE3B_R10_CERTIFICATION_v1.md`'s method; existing family | Certified selection headroom ≤ the gate margin across the declared ρ family, i.e. III-B's shallow binding persists | No for the certificate; a later Q-LEARN rerun needs separate approval as a scale/protocol change |
| **4** | P3 alone, C3 (re-routing) | Same POMDP as rank 2 without the budget, testing only whether re-routing state is shared across consumers in the optimum | Analytic | Re-routing in the optimum is per-consumer, or reduces to redundancy + vote | No for analytic C3; **organism-harness instantiation is organism re-entry and needs human authorization** |
| **5** | P4, C4 (tags) | Only after rank 2 passes: tag-swap analysis in a 2-consumer version of rank 2's world | Analytic | The tag is a function of the content sufficient statistic at matched channel | **Yes** |

**Why this order.**

- **Rank 1** reuses an existing, tested certificate. Its failure parks the whole
  scarcity line with an exact reason, as §8 Q7 of the branch file already says.
- **Rank 2** is the only design where a C4-*distinct* structure has a structural reason
  to exist. That reason is the temporal separation created by hidden decay. It is
  ranked after rank 1 because it is the same certificate family plus one hidden-state
  dimension, and because it is C4-gated.
- **Rank 3** is cheap but has already been tried once at ρ ≈ 1.
- **Ranks 4–5** depend on rank 2.

---

## 5. Approval flags (for Aidan)

| Item | Gate | Source |
| --- | --- | --- |
| Rank 2 (P1×P3 C4 certificate), rank 5 (P4 tags), and any S3 meta-d′ signature in rank 1 | **First C4 study: needs Aidan's approval.** Parameters stay unset until then. | Constitution v3 "Immediate and human gates"; Ruling R-A2 (v2 §4) |
| Rank 1 extension of `scarcity_v1` | `SCARCITY_GAP_v1.md` §7 says "design only; human gate required" | Branch file |
| Any organism instantiation of P3 (O3 loop) | Organism re-entry: human authorization | Constitution v3 |
| Any Q-LEARN run (any rank) | No neural training is authorized; needs a separately approved prospective protocol with an R10-style ceiling | Constitution v3; `PHASE3B_VERDICT_v1.md` lesson |
| Ranking itself | The rank-1-before-rank-2 order is a judgement. If Aidan prefers to test C4 distinctness first, rank 2 can go first, since it does not logically depend on rank 1. | — |

---

## 6. Caveats and open questions

- **C1. All Q-EXIST magnitudes cited are from the branch certificate.** Max access value
  is 1/24 and max selection value is 1/8. They come from a clean 3-item world at fixed K.
  I did not re-run them, and they were not merged to master.
- **C2. The decoder-free limb 2 (open problem O1, §1.1).** A history transplant "holding
  the full first-order state" needs a partition. In a monolithic learned network I have
  no decoder-free way to define one. In the organism harness, partitions are explicit,
  but those registers are *supplied* structure, which strains E1. This is the main
  unsolved methodological issue for C4 emergence.
- **C3. Ruling R-A1 makes the rank-2 rival strong.** Upkeep history is self-generated
  and unlabeled. A reviewer could argue that conditioning on it is itself "unsupervised
  calibration", so it is conventional. If that holds, rank 2 can at best return
  constructive equivalence. The definitional boundary needs the same contestable note
  as M1.
- **C4. Song et al. (2017) and Orhan & Ma (2017)** are used only to show that
  confidence-*behaviour* emergence is cheap and first-order-explicable. I did not check
  whether either tested separability, and I make no claim that they did.
- **C5. Cleeremans (2011) and Cleeremans et al. (2020)** are theoretical proposals. They
  motivate Q-LEARN; they are not evidence for it.
- **C6. Not examined.** Other pressures (social or other-agent modelling, curriculum or
  developmental staging, intrinsic-motivation objectives). They are named for a later
  version.
- **C7. No consciousness inference.** Even a full P1×P3 pass would earn at most
  "an evaluator-like structure meeting Astra's conjunction emerged under declared
  pressure at capacity parity". That says nothing about C7.

---

## 7. Thirteen admission answers (for this design card as a whole)

| Q | Answer |
| --- | --- |
| Q1 | C-axis emergence question: under what developmental pressures do C3 and C4 structures arise under Q-LEARN rather than being supplied? O3 bridge via P3. |
| Q2 | One hypothesis: a C4-distinct evaluator can emerge only where a pressure creates both sub-sufficiency (ρ<1, or a broken ideal-observer premise) and a temporal/spatial separation. P1×P3 is the minimal such pressure. |
| Q3 | Defeated if the rank-2 matched-K optimum's evaluation-relevant state is a function of (outcome history, elapsed time) in every declared cell (constructive equivalence to the adaptive rival); or if rank 1 shows zero selection/access value across the declared ρ family. |
| Q4 | Blackwell sufficiency / joint filtering; adaptive selective prediction (label-driven or unlabeled, per R-A1); redundancy + vote (Sub A); static allocation plus observable thresholds (Phase II); scalar LLR broadcast (Phase III); same-K monolithic learner. |
| Q5 | `SCARCITY_GAP_v1.md` (branch) §1–2; `C1_RELIABILITY_DISPOSITION_v1.md`; `PHASE3_VERDICT_v1.md`; `PHASE3B_VERDICT_v1.md` / `PHASE3B_R10_CERTIFICATION_v1.md`; `SUB_A_ANALYTIC_CHECK_v1.md`; `AC117_RESULTS_v1.md`; `c_axis_theory_queue_v2.md` §3.2 (M1 REDUCED). |
| Q6 | Success at rank 2 would justify proposing a prospective Q-LEARN protocol at matched K or budget, with the rank-2 optimum as ceiling (still separately gated). Success at rank 1 would make P1 the default pressure for C3. |
| Q7 | Failure at rank 1 would park the scarcity line with an exact reason. Failure at rank 2 would log P1×P3 REDUCED (like M1) and move C4 emergence to pressures not examined here (C6). An unresolved result would close the effort and preserve the open question. |
| Q8 | Analytic certificates only (exact enumeration in the `scarcity_v1` style). No neural model, no organism. |
| Q9 | Organizational cognition (identifiability and emergence of a role), not engineering advantage. |
| Q10 | Ceiling: at most "the matched-capacity optimum contains an X-type structure under pressure P", which is Q-EXIST. Q-LEARN, Q-CAUSE in a learner, Q-NECESSITY and anything conscious are NOT established by any certificate here. |
| Q11 | C3 (ranks 1, 3, 4) and C4 (ranks 2, 5). The decoder-free limb 2 (O1) and Q-LEARN itself remain unsupported. |
| Q12 | O3 (P3) and O0/N1 paid maintenance (P1). Capacity, damage process and budget are supplied by the world design. |
| Q13 | Rank 1 pass or fail updates the C3 ledger "rival"/"ceiling" fields. Rank 2 pass or fail updates C4 "next_falsifier". A rank-2 REDUCED result adds a collapse-ledger entry. |

---

## 8. Citations

**Verification.** New references were checked on 2026-10-20 against Crossref and
publisher or arXiv pages. References carried from v1/v2 were verified there (v1 §7).

### New in this file

| Ref | Status |
| --- | --- |
| Song, H. F., Yang, G. R., & Wang, X.-J. (2017). Reward-based training of recurrent neural networks for cognitive and value-based tasks. *eLife* 6:e21492. doi:10.7554/eLife.21492 | Verified (PubMed/PMC, publisher). The post-decision wager result was read in the PMC text summary. |
| Orhan, A. E., & Ma, W. J. (2017). Efficient probabilistic inference in generic neural networks trained with non-probabilistic feedback. *Nature Communications* 8. doi:10.1038/s41467-017-00181-8 | Verified (Crossref) |
| Kepecs, A., Uchida, N., Zariwala, H. A., & Mainen, Z. F. (2008). Neural correlates, computation and behavioural impact of decision confidence. *Nature* 455:227–231. doi:10.1038/nature07200 | Verified (Crossref) |
| Wang, J. X., Kurth-Nelson, Z., Kumaran, D., Tirumala, D., Soyer, H., Leibo, J. Z., Hassabis, D., & Botvinick, M. (2018). Prefrontal cortex as a meta-reinforcement learning system. *Nature Neuroscience* 21:860–868. doi:10.1038/s41593-018-0147-8 | Verified (Nature page, DOI). The end page 868 is from memory; the page shows "21, 860". |
| Behrens, T. E. J., Woolrich, M. W., Walton, M. E., & Rushworth, M. F. S. (2007). Learning the value of information in an uncertain world. *Nature Neuroscience* 10:1214–1221. doi:10.1038/nn1954 | Verified (Crossref) |
| Yang, G. R., Joglekar, M. R., Song, H. F., Newsome, W. T., & Wang, X.-J. (2019). Task representations in neural networks trained to perform many cognitive tasks. *Nature Neuroscience* 22:297–306. doi:10.1038/s41593-018-0310-2 | Verified (Crossref). The "shared/compositional representations" characterization is from my knowledge of the paper; the full text was not re-read. |
| Li, K., Hopkins, A. K., Bau, D., Viégas, F., Pfister, H., & Wattenberg, M. (2023). Emergent world representations: Exploring a sequence model trained on a synthetic task. arXiv:2210.13382 | arXiv verified (full text read: nonlinear probes plus activation interventions). ICLR 2023 venue not checked. |
| VanRullen, R., & Kanai, R. (2021). Deep learning and the Global Workspace Theory. *Trends in Neurosciences* 44:692–704. doi:10.1016/j.tins.2021.04.005 | Verified (Crossref). Background only; cited as a *supplied*-workspace proposal. Not cited above in the body; kept for v2 cross-reference. |
| Cleeremans, A. (2011). The radical plasticity thesis: How the brain learns to be conscious. *Frontiers in Psychology* 2:86. doi:10.3389/fpsyg.2011.00086 | Verified (Crossref). The article number is inferred from the DOI. |
| Cleeremans, A., Achoui, D., Beauny, A., Keuninckx, L., Martin, J.-R., Muñoz-Moldes, S., Vuillaume, L., & de Heering, A. (2020). Learning to be conscious. *Trends in Cognitive Sciences* 24:112–123. doi:10.1016/j.tics.2019.11.011 | Verified (Crossref; first six authors on Crossref, the last two from memory) |

**Dropped:** Khalvati, Kiani & Rao, "Bayesian inference with incomplete knowledge
explains perceptual confidence and its deviations from accuracy". Only the bioRxiv
preprint (doi:10.1101/2020.09.18.304220) was verified; the journal version was not, so I
dropped it rather than cite it partially.

### Carried from v1/v2 (verified there)

- Fleming & Daw 2017
- Kiani & Shadlen 2009
- Kadavath et al. 2022
- Gibbs & Candès 2021 (venue unchecked)
- Lau 2022 (PRM description via reviews)
- Bongard, Zykov & Lipson 2006
- Kwiatkowski & Lipson 2019
- Butlin et al. 2023

### Repo sources

**Master `32cfbe6`:**

- `ACI_RESEARCH_CONSTITUTION_v3.md`
- `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json`
- `ACI_RESEARCH_SYNTHESIS_v1.md` (O3 arrow audit, cognitive frontier)
- `C1_RELIABILITY_DISPOSITION_v1.md`
- `PHASE3_VERDICT_v1.md`
- `PHASE3B_VERDICT_v1.md`
- `PHASE3B_R10_CERTIFICATION_v1.md`
- `BRIDGE_PHASE2_VERDICT_v1.md`
- `SUB_A_ANALYTIC_CHECK_v1.md`
- `AC117_RESULTS_v1.md`

**Branch `origin/elminster/loving-ptolemy-ityj4l` @ `33fa803`, via `git show`:**

- `SCARCITY_GAP_v1.md`
- `scarcity_v1/` (present only on the branch; not read beyond the .md's description)

**Workspace:**

- `/workspace/review/c_axis_theory_queue_v2.md` (§1 conjunction, §3.2 M1 REDUCED,
  Rulings R-A1 to R-A3)
- `/workspace/astra_consult_1.md` (consultation #3)
