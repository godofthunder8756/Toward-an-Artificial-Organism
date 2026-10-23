# Acquired assessment of the learner's own correctness: study specification v1 (DRAFT, PAPER ONLY)

Status: **DRAFT FOR REVIEW. NOT FROZEN. NOT APPROVED. NOTHING HAS BEEN RUN.**
Prepared 2026-10-21 (ET) by the research delegate for Aidan Ahern, ACI Track A.
No consciousness claim. NOT CLAIMED: C4 status, C5 status, consciousness, or any claim of autopoiesis or of being alive.

## 0. Status, approvals, sources and constraints

### 0.1 Approval placeholders (all required before any freeze or run)

| Gate | Required sign-off | Status |
| --- | --- | --- |
| A-REVIEW | Astra review of this draft, with rulings on §20 | `[PENDING — Astra review]` |
| A-PRE | Aidan approval of the pre-freeze, reference-only NEEDS-APPROVED-RUN items in §21 (no learner, no training) | `[PENDING — Aidan approval]` |
| A-FREEZE | Aidan approval of the frozen spec (FINAL, with sha256) | `[PENDING — Aidan approval]` |
| A-RUN | Aidan approval of the run, scoped to the frozen spec, its seeds and its §15 caps | `[PENDING — Aidan approval]` |

Astra #30 L216 is relevant to the form of A-RUN: "The standing approval should be recorded against the next study's concrete scope once its specification has been reviewed and frozen." The same paragraph says "this design sketch is not yet an executable protocol." This draft does not record any approval. It only provides the placeholders.

### 0.2 Sources

- Astra consult #30 response: `/workspace/astra_consult30_response.txt`, sha256 `4cc628034185fe456fa1f39be5f9dbf52d1d5b3556d34d18d7996d1b9511d04c`, §E (L113–L184). Quotes below are cited as `Astra #30 Lnnn` and checked verbatim by the check script.
- GRU lineage, read-only from the fetched PR refs `origin/pr/5`, `origin/pr/7`, `origin/pr/8`, `origin/pr/9`, `origin/pr/10`. W-REL lineage from `origin/pr/11`. Citations take the form `path`@commit Lnnn.
- The frozen W-REL specification on the box: `/workspace/review/c4_reliability_exact_check_spec_FINAL.md`, sha256 prefix `ae626b65`.

### 0.3 Standing constraints on this document

- PAPER ONLY. No code, training, benchmark, solver or timing run was executed to write it. Its numbers come from existing records or from hand or analytic arithmetic, and each is labelled with its source.
- Items that need computation are marked **NEEDS-APPROVED-RUN** and collected in §21.
- No repository changes were made.
- Every **PROPOSED** value is open for Astra's review (§20).
- Order of execution, once approved: Stage 0 support audit (§12), then Stage 1 training, then the two cheap falsifiers (§1), then the full evaluation. The falsifiers are stated first here because they decide whether the rest is ever computed.

## 1. Cheap falsifiers, run first and each with a declared stop rule

Both falsifiers run on the sealed Stage 1 checkpoints (§15.1) before any FO, ISO, random-donor, rescue, initialization-conjunction or compiled-control computation. Only the statistics named here are computed at this point.

### 1.1 CF1: learner-specific correctness distinction

Astra #30 L158: "Before expensive intervention analysis, check whether actual learner correctness differs meaningfully from oracle correctness and whether the candidate state predicts that difference beyond current confidence."

Per seed, at the final checkpoint, compute on the evaluation split S_E (§7), with the world-plus-fault-law weights w (§6.3):

- **CF1a (distinction present).** Let Δ_a(H) = m_a(H) − o_a(H), where m_a is defined in §6.1 and o_a in §6.2.
  - RMS divergence: D_div = sqrt( (1/3) Σ_a Σ w·Δ_a² / Σ w ).
  - Divergent mass: M_div = Σ w·1[max_a |Δ_a| ≥ δ_div] / Σ w.
  - CF1a holds iff D_div ≥ δ_div and M_div ≥ ν_div. PROPOSED values: δ_div = 1/20, ν_div = 1/20.
- **CF1b (the state predicts the difference beyond confidence).** Fit on S_I and evaluate on S_E:
  - the §10.1 decoder, with target Δ_a in place of m_a (same features, same ridge, no selection);
  - the §9.1 confidence baseline, with the same target.
  - Let E_base^Δ and E_dec^Δ be their weighted mean squared errors, averaged over actions. CF1b holds iff E_base^Δ − E_dec^Δ ≥ μ1_abs and (E_base^Δ − E_dec^Δ)/E_base^Δ ≥ μ1_rel, using the same margins as K1 (§11.2).
  - If E_base^Δ = 0, the label is `NOT EVALUABLE [NO BASELINE ERROR TO IMPROVE]`, which counts as a CF1 failure for that seed.
- A seed passes CF1 iff it is valid and CF1a ∧ CF1b holds under both evaluators (§15.2). A boundary result counts as numerically unresolved.

**CF1 stop rule (declared now).** Precedence applies in this order:
1. If more than two seeds are invalid or numerically unresolved at CF1, the label is `UNRESOLVED (insufficient evaluable seeds)` and the study stops.
2. Otherwise, if at least three of the ten seeds fail CF1, the label is `STOPPED AT CF1: LEARNER-SPECIFIC CORRECTNESS DISTINCTION NOT EXERCISED`, with the sublabel counts CF1a-fail and CF1b-fail. The study stops.

Rationale for the threshold of three: K4 requires 8/10 with the denominator fixed at ten, so three failures make the bar unreachable.

**What is reported on a CF1 stop:**
- per seed: validity, D_div, M_div, E_base^Δ, E_dec^Δ, both evaluators' values and the CF1a/CF1b flags;
- the Stage 0 and Stage 1 manifest hashes;
- the sentence "The study did not exercise its motivating question under the declared design".

No intervention statistic is computed. Astra #30 L160: "Do not search for convenient faults or checkpoints afterward." No new perturbation law, checkpoint, seed or margin may be tried under this spec. A redesign needs a new spec version, review and approval.

### 1.2 CF2: checking effects always break the first-order battery

Astra #30 L162: "A second cheap falsifier is that every intervention producing a checking effect also damages the first-order probe battery beyond tolerance."

This runs only if CF1 does not stop the study. Per seed, at the final checkpoint, compute only the two content interventions (down and up, §10.3) on the S_E recipients. No family paths, rescue or initialization statistics are computed. For direction d:

- D_q^d is the class-mean change in checking probability (§10.3).
- B^d is the maximum, over recipient samples, of the absolute pre-check battery change (§11.1), and Dec^d is the number of changed binary decisions.

The predicates are:
- **CE^d (checking effect):** σ_d·D_q^d ≥ μ_q.
- **FP^d (first order preserved):** B^d ≤ τ_FO and Dec^d = 0.

The seed is **CF2-fired** iff at least one direction has CE^d, and every direction with CE^d fails FP^d. The seed is **CF2-null** iff some direction lacks CE^d. That is an ordinary K2 non-pass, not a CF2 firing.

**CF2 stop rule (declared now).**
1. The >2 invalid or unresolved precedence applies first, as in CF1.
2. Otherwise, if (#CF2-fired) + (#CF2-null) + (#CF1 fails carried forward) ≥ 3, the label is `STOPPED AT CF2`, with sublabel `NO FIRST-ORDER-PRESERVING CHECKING EFFECT` when #CF2-fired ≥ 1, and sublabel `NO CHECKING EFFECT` otherwise. The study stops.

**What is reported on a CF2 stop:** per seed and direction, D_q^d, D_e^d, B^d, Dec^d, the CE/FP flags, both evaluators' values, and the CF1 report. No family, rescue, initialization or compiled-control result is computed or reported. The same no-search rule as CF1 applies.

## 2. Scientific claim and claim ceiling [F1]

### 2.1 The exact claim (only if every gate in §11 passes)

For a declared GRU-16 learner (§4) trained for a fixed 10,000 updates on the declared task (§5), in at least eight of ten prespecified seeds, with the denominator fixed at ten, the trained learner shows all four of K1–K4 (§11):

- **K1.** Held-out hidden-state content at the declared decision point predicts the learner's own post-action correctness m_a(H) (§6) beyond a frozen current-confidence baseline. Both an absolute and a relative margin must be met.
- **K2.** Installing class-specific content changes assessment error and checking in the predicted directions. The declared pre-check first-order battery is preserved within tolerance, and the effect exceeds both FO-matched and ISO families.
- **K3.** Repair on a shared received history reduces assessment error and reverses the checking change.
- **K4.** The conjunction is not met at initialization.

The tags are Q-LEARN (K4) and Q-CAUSE (K2, K3), within the declared interventions and domain only. Q-EXIST is addressed by §12 and CF1. Q-NECESSITY is not tested (§3).

### 2.2 Claim ceiling

**The card status is `C4-candidate` at most.** That is a card status, not a C-level determination. Astra #30 L166: "Neither the proposed study nor a positive result automatically establishes C4 status or consciousness." NOT CLAIMED: C4 status, C5, consciousness, autopoiesis, being alive, necessity of the representation, or behaviour outside the declared finite audit domain.

### 2.3 Claim restrictions that the results attach automatically

- If the compiled control is equivalent (§13), the claim must add: "An ordinary compiled implementation reproduces the tested predictions, actions and mapped interventions on the declared audit domain. The result concerns acquisition and causal use of this information in the trained network's state, not its irreducibility."
- If post-check probability effects exceed τ_post (§11.1), the claim must add: "The first-order dissociation is restricted to the pre-check output." This follows Astra #30 L156: "Passing a pre-check battery is not preservation of the full first-order computation."
- The GRU-16 result does not transfer to the GRU-8 two-stream studies (PRs #5 and #7–#10) or to the W-REL analytic agents. They are separate systems.

## 3. Question separation (Q-tags)

| Tag | Content in this study | Not covered |
| --- | --- | --- |
| Q-EXIST | The task admits a learner-specific correctness distinction with positive support. Shown by the pre-freeze reference attainability check (§12.4, §19), the §12 support audit and CF1. | Existence in other tasks |
| Q-LEARN | K4: the conjunction is absent at initialization and present after 10,000 updates (8/10) | Learning dynamics; intermediate checkpoints are not saved |
| Q-CAUSE | K2 and K3: the effects of declared state interventions on assessment error and checking | Effects outside the declared interventions |
| Q-NECESSITY | **Not tested.** The compiled control is an equivalence control (§13). R-FO is a comparison (§17). Neither is a necessity test. | Everything |

The tags are reported in separate result sections and are never pooled into one verdict.

## 4. Network, inputs, readouts and learning rules [F2]

Astra #30 L121: "One small GRU, provisionally 16 hidden units, with ordinary prediction and checking-action readouts. No supplied assessment register, fault labels or oracle-correctness training target."

### 4.1 Network (PROPOSED)

- **Cell:** `nn.GRU(input_size=14, hidden_size=16)`, with a single layer, h₀ = 0, float32 training and float64 evaluation.
- **Input at read step k (I = 14):**
  - cue N as ±1 (1);
  - the received evidence value ỹ_k ∈ {1..6} as a one-hot (6);
  - the read type ∈ {FIRST, RECHECK, RESAMPLE} as a one-hot (3);
  - the stage k ∈ {1..4} as a one-hot (4). The stage code is a declared external timing scaffold, as in PR #5 (`TWOSTREAM_ACQUISITION_PROTOCOL_v1.md`@0b98460 L101).
  - Nothing else. There is no F, no replacement flag, no Y, no m and no o.
- **Prediction readout:** MLP 16→32 (tanh)→1, sigmoid, giving p̂_k. The decision is ŷ = 1 iff p̂ > 1/2, the W-REL frozen rule (`/workspace/review/c4_reliability_exact_check_spec_FINAL.md` L78).
- **Action readout:** MLP 16→32 (tanh)→3, softmax over {PREDICT, RECHECK, RESAMPLE}, giving π_k. At stage 4 the action is forced to PREDICT, and the action readout is not used there.
- **Parameter count (analytic):**
  - GRU: 3·16·(14+16) + 2·3·16 = 1536;
  - prediction head: 16·32+32+32+1 = 577;
  - action head: 16·32+32+32·3+3 = 643;
  - total 2756.
  - For comparison, the PR #5 GRU-16 record (input size 9) reports recurrent 1296 and readout 643 (`acquisition_results_v1/runs/cand_gru16_s0.json`@b25a30a L9–L10). That matches the same formula, 3·16·(9+16)+96 = 1296.

### 4.2 Learning rules (PROPOSED)

Astra #30 L123: "Train first-order prediction from revealed outcomes and action selection from correctness minus checking cost. The analyst's assessment decoder is fitted afterward on a separate identification split."

- **First-order loss:** Σ_k BCE(p̂_k, Y) over every decision point of the episode. Y is the episode outcome, revealed after the episode. This is an ordinary outcome label.
- **Action loss:** REINFORCE with baseline, −(G − b)·Σ_k log π_k(a_k), where:
  - G = 1[ŷ_final = Y] − Σ_k c(a_k);
  - b is an exponential moving average of G (β = 0.99, b₀ = 0), not differentiated;
  - an entropy bonus 0.01·Σ_k H(π_k) is added, with the coefficient fixed and not annealed.
- **Total loss:** first-order loss + action loss, as the batch mean. No other term is allowed. In particular there is no auxiliary target, no fault label, no m_a, no o_a and no correctness label for the checking decision.
- **Optimizer:** the PR #7 recipe (`RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md`@d118ae1 L36–L37):
  - Adam (0.9, 0.999, 1e-8), weight decay 0;
  - cosine LR 1e-3→1e-4 over 10,000 updates;
  - global gradient clip 1.0.
- **Batch:** B = 64 episodes per update, PROPOSED as Astra's "a small batch" (Astra #30 L164).
- **Determinism:** `torch.set_num_threads(1)`, deterministic algorithms, CPU only (`RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md`@d118ae1 L40).
- The analyst decoder (§10.1) is fitted only after Stage 1 is sealed. The training code must not import decoder or target code. A static audit checks this (§17.2).

## 5. World law, internal perturbations, costs and event order [F3]

Astra #30 L125: "A short finite episodic binary-evidence task with PREDICT, RECHECK and RESAMPLE. Retain the useful same-evidence versus fresh-evidence distinction."

### 5.1 World (PROPOSED)

- **Outcome:** Y ∈ {0,1}, uniform.
- **Cue:** N ∈ {lo, hi}, observable, P = 1/2 each.
- **Graded evidence:** each world sample is y ∈ {1..6}, with emission table:
  - P(y | Y=1, lo) = (1, 1, 2, 3, 5, 12)/24;
  - P(y | Y=1, hi) = (2, 3, 4, 4, 5, 6)/24;
  - P(y | Y=0, N) = P(7−y | Y=1, N).
  - The task is binary in the outcome. The evidence alphabet is graded.
  - The reason for grading is Appendix A: a binary-read version with symmetric flips gives zero value to any single extra read and makes checking unprofitable at the W-REL costs. That is a no-contrast trap of the kind recorded in W-REL (§19).
- **Marginal of y (hand arithmetic):**
  - lo: (13, 6, 5, 5, 6, 13)/48;
  - hi: uniform 8/48.

### 5.2 Internal read-processing perturbation (PROPOSED; explicit location, persistence and action-specificity)

Astra #30 L127: "Introduce prespecified stochastic perturbations in the learner's read-processing computation, alongside evidence-noise conditions. The intervention location, persistence and action-specific effects must be explicit."

- **Location:** the learner's evidence-encoding step, which maps the world sample y to the 6-way one-hot that enters the GRU. The perturbation is part of the learner's read processing, not of the world. The world-observable history H records the emitted y.
- **Persistence:** an episode-level fault mode F ~ Bernoulli(φ), with φ = 1/4. F persists for the whole episode and is never an input.
- **Per-read effect:**
  - if F = 1, each read is independently replaced with probability κ = 1/4 by a value drawn uniformly from {1..6}, which may equal y;
  - if F = 0, there is no replacement.
  - So P(ỹ = y | F=1) = 1 − 5κ/6 = 19/24, and P(ỹ = v | F=1) = κ/6 = 1/24 for each v ≠ y.
- **Action-specific effects:**
  - FIRST reads the first world sample, with a fresh processing draw.
  - RECHECK re-reads the most recently drawn world sample (same evidence), with a fresh processing draw.
  - RESAMPLE draws a new world sample from P(y | Y, N) (fresh evidence), with a fresh processing draw.
  - PREDICT reads nothing.
  - The same F and κ apply to all three read types. Only RECHECK can expose processing disagreement on identical evidence. That is the same-evidence versus fresh-evidence distinction.
- **Training and evaluation use the same perturbation law.** Training and evaluation streams are separate draws (§7, §8).
- **Discordance on RECHECK (hand arithmetic):**
  - P(ỹ₁ = ỹ₂ | F=1) = (19/24)² + 5·(1/24)² = 366/576 = 61/96;
  - P(discordant | F=1) = 35/96;
  - unconditionally, P(discordant) = φ·35/96 = 35/384.
  - F = 0 is always concordant.

### 5.3 Costs and episode structure (PROPOSED)

- **Costs:** c(PREDICT) = 0, c(RECHECK) = c_R = 1/100, c(RESAMPLE) = c_S = 3/50. These are borrowed from the W-REL A2-attaining setting (`c4_reliability_exact_check_v1/RESULTS_A2.md`@dddd63c). They must be re-checked for this task (§12.4). Nothing carries over from W-REL. Astra #30 L129: "Do not assume that the old W-REL symmetry survives this change."
- **Episode:** at most K_max = 3 checks. Stage k is the decision point after k reads.
- **Event order:**
  1. Draw Y, N, F, and the first world sample y₁.
  2. Draw the processing outcome ỹ₁ and run GRU step 1.
  3. At stage k ≤ 3: compute p̂_k and π_k, and sample a_k. If a_k = PREDICT, the episode ends with ŷ = 1[p̂_k > 1/2]. Otherwise apply the read rule of §5.2, run GRU step k+1, and continue.
  4. At stage 4, PREDICT is forced.
  5. The payoff is 1[ŷ = Y] − Σ costs. Y is then revealed for the first-order loss.

## 6. The assessed prediction stage and the learner-specific target [F4]

### 6.1 Target m_a(H), as Astra defines it

Astra #30 L134–L135, verbatim:

```
m_a(H) = P(the frozen learner's own post-action decision is correct
           | observable history H, do(action=a))
```

Astra #30 L138: "The target must include that learner's errors, not substitute the oracle's optimal decisions."

**Operational definition (PROPOSED).**
- **Observable history:** H is the world-observable history at stage k ∈ {1,2,3}. It contains the cue, the emitted world samples and the action types. The learner's fault draws are latent. The learner's state h is a deterministic function of its received history R (inputs only).
- **Post-action decision**, following the "assessed prediction stage":
  - a = PREDICT: the decision is ŷ = 1[p̂(R) > 1/2], now.
  - a ∈ {RECHECK, RESAMPLE}: the decision is the learner's immediate post-read prediction ŷ' = 1[p̂(R') > 1/2], where R' extends R by the new received read. It is one step and myopic. Later actions are not part of the target.
- **Formula:**

  m_a(H) = Σ_{Y, F, ρ, y'} P(Y, F, ρ, y' | H, do(a)) · 1[learner decision on the resulting received history equals Y]

  Here ρ is the latent replacement pattern of the reads so far, and y' is the new world sample (RESAMPLE) or the same sample (RECHECK) with its fresh processing draw. All probabilities come from the declared world-plus-fault law. Evaluation uses the frozen learner and its decision table (§15.3).
- **Assessed stage for K2 and K3:** the stage-2 decision point after a forced first action RECHECK (§10.3). The assessment statistic is e = m̂_PREDICT − m_PREDICT.

### 6.2 World-model oracle o_a(H)

o_a(H) is the probability that the world-model Bayes decision is correct after action a. Its posterior over Y uses the emitted world samples in H with no processing faults, and its post-action read is unperturbed.

The difference m − o is therefore both the learner's processing-fault exposure and its suboptimality. This is the distinction CF1 tests. Astra #30 L127: "The purpose is to create cases in which the learner's actual conditional correctness differs from the world-model oracle's."

### 6.3 Sample space and weights (fixed before any outcome)

- A decoder sample is (H, ρ), weighted by w(H, ρ) = P(observations, ρ | do(action prefix)) × 4^{−(k−1)}.
  - Action prefixes over {RECHECK, RESAMPLE}^{k−1} are weighted uniformly, as the declared counterfactual observation distribution.
  - The weights do not depend on the learner's policy. This is the support-audit design choice of §12.1.
- **Distinct world histories (analytic):**
  - stage 1: 2·6 = 12;
  - stage 2: 2·6·7 = 84;
  - stage 3: 2·6·7² = 588.
  - Each check is either RECHECK, which adds no new world sample, or RESAMPLE, which adds one of 6.
- **Latent patterns per world history:** 1 under F = 0 and 6^k under F = 1. So there are 84 + 3,108 + 127,596 = 130,788 samples at stages 1–3, all with positive weight.
- **Learner received histories** (the compiled-control domain, §13):
  - stage k has 2·6^k·2^{k−1};
  - 12 + 144 + 1,728 + 20,736 = 22,620 in total.

## 7. Training, identification and evaluation splits [F5]

- **Training** uses freshly sampled episodes (§8). Training never uses the enumerated decoder domain or any target.
- **Identification split S_I and evaluation split S_E** partition world histories by their first world sample:
  - H ∈ S_E iff (y₁ + 1[N=hi]) mod 2 = 1;
  - otherwise H ∈ S_I.
- **Mass check (hand arithmetic from §5.1):**
  - lo: y₁ odd {1,3,5} has mass (13+5+6)/48 = 1/2;
  - hi: y₁ even {2,4,6} has mass 24/48 = 1/2.
  - Each split therefore carries exactly 1/2 of the mass at every stage and within each cue.
- All samples of a world history fall in one split. The split rule is applied to H only, never to learner outputs.
- **Uses of each split:**
  - S_I: all decoder and baseline fits, the donor class means, and the family generator calibration (none is needed).
  - S_E: all gating statistics.
- The split hashes (sha256 of the sorted history index lists) are written to the Stage 0 manifest.
- **Doesn't fit from PR #7:** the PR #7 TRAIN/TEST rule ((h mod 16) + ⌊h/16⌋) mod 4 = 0 over 256 histories (`RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md`@d118ae1 L31) belongs to the W2 world. It is not reused. PR #7 also rejected TEST episodes from training. Here the split is over the analyst's decoder domain, and training samples the task law unrestricted, because the learner's training is not the held-out test. The held-out test concerns the analyst's decoder (§17.3).

## 8. Seeds, training budget, checkpoints and stopping rules [F6]

- **Seeds:** s ∈ {500, …, 509}, ten seeds, prespecified (PROPOSED). Disjointness from the earlier ranges must be confirmed at freeze: 200–209 (PR #8, `GRADED_REVERSION_PROTOCOL_FINAL.md`@018f2a7 L283), 300–309 (PR #9) and 400–409 (PR #10). The seeds are:
  - torch init: `torch.manual_seed(s)`;
  - episode and fault stream: a float64 generator seeded 1000+s (the PR #7 convention, `RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md`@d118ae1 L39);
  - action sampling: a generator seeded 3000+s;
  - FO, ISO and random-donor families: generators 1,000,000+100·s, 40,000+100·s and 70,000+100·s, by analogy with PR #9 §4.2/§4.4 (`first_order_control_protocol_FINAL.md`@335e505 L197, L244).
- **Arms trained:** CAND (§4) and R-FO (§17.1). Each has 10 seeds, one fixed run per seed, 10,000 updates at B = 64 (640,000 episodes per run). That makes 20 runs.
- **Checkpoints:** init (Stage 0) and final (update 10,000) only. No intermediate checkpoint is saved, so there is nothing to select from later (Astra #30 L160).
- **Stopping:** there is no early stopping, no restart and no seed replacement. A NaN, an exceeded cap (§15.4) or a determinism failure makes the run invalid. The denominator stays ten. This follows PR #10, "There is no re-training" (`frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L394).

## 9. Baselines, information access and resource accounting [F7]

Astra #30 L142: "Current-output confidence and a cost-general history-dependent controller, with disclosed information and resources."

### 9.1 Frozen current-confidence baseline (gating comparator for K1 and CF1b)

- Per action a, a weighted least-squares fit on S_I of m_a against φ(c) = [1, c, c², c³], with c = p̂ at the same state.
- The ridge is 1e-9·Σw, for numerical stability only. Outputs are clipped to [0,1].
- **Information:** the learner's current output only.

### 9.2 R-HIST: cost-general history-dependent controller (reference, disclosed)

- R-HIST is an exact Bayes controller that maximizes expected payoff over the remaining checks, for all costs.
- **Information:** the full received history plus the declared world law and fault law. That is more than the learner has.
- **Resources:** an exact enumeration over at most 22,620 received histories.
- **Role:**
  - the attainability and contrast reference (§12.4);
  - a descriptive behavioural comparator (reward, checking rates).
  - It does not gate the learner's conjunction. Whether it should is open question Q-A7 (§20).

### 9.3 Same network at initialization

Astra #30 L143: "The same network at initialization, to distinguish acquired performance from supplied structure." The init checkpoint of each CAND seed is evaluated with the identical pipeline. That is K4 (§11.5).

### 9.4 Information-access ledger (written to the Stage 0 manifest)

| Agent | Inputs | Knows the law? | Trained on | Parameters |
| --- | --- | --- | --- | --- |
| CAND | N, ỹ, read type, stage | no | Y, payoff | 2756 |
| R-FO | same, but the action head sees only [p̂ (detached), N, read type, stage] | no | Y, payoff | 1536 + 577 + (9·32+32+32·3+3 = 419) = 2532 |
| init | same as CAND | no | none | 2756 |
| confidence baseline | c = p̂ | no | S_I targets (analyst) | 4 per action |
| decoder | h (16) | no | S_I targets (analyst) | 17 per action |
| R-HIST | received history | yes | none (exact) | table |
| oracle o | emitted world samples | yes | none (exact) | — |

The training-compute ledger records updates, episodes, wall-clock and CPU seconds per run.

## 10. Decoder selection and intervention construction [F8]

### 10.1 Decoder (no selection)

- Per action a, a weighted ridge least-squares fit on S_I of m_a against [1, h] (17 features), with λ = 1e-3·Σw. Outputs are clipped to [0,1].
- There is one prespecified decoder with no hyperparameter search. Any alternative decoder is descriptive only and is reported under its own name.
- Decoder samples are drawn at stages 1–3 under the §6.3 weights.

### 10.2 Assessment subspace and first-order direction

At the stage-2 recipient state h_R:
- g = ∇_h p̂(h_R) (float64, exact autograd);
- A = span of the three decoder weight vectors (with the intercept dropped);
- P = the orthogonal projector onto A ∩ g^⊥ (A orthogonalized against g).
- If dim(A ∩ g^⊥) = 0 for a recipient, that recipient is `NOT EVALUABLE [NO ASSESSMENT DIRECTION ORTHOGONAL TO FIRST ORDER]`. The mass of such recipients is reported.

### 10.3 Content interventions (K2) and recipient classes

- **Recipient population:** S_E samples at stage 2 with a₁ = RECHECK forced.
  - Concordant class CON: ỹ₁ = ỹ₂.
  - Discordant class DIS: ỹ₁ ≠ ỹ₂.
  - The classes are defined by world-plus-fault-law events, not by learner occupancy.
- **Donor content:** h̄_D is the weight-averaged S_I state of the donor class, following the class-mean form. Whether single-donor draws should be used instead is open question Q-A6.
- **Installation:** h_int = h_R + P(h̄_D − h_R).
  - Down: DIS content into CON recipients, σ = −1 for e and +1 for q.
  - Up: CON content into DIS recipients, σ = +1 for e and −1 for q.
- **Statistics per direction** (class weight means over recipient samples):
  - D_e = mean[e_int − e_intact], where e = m̂_PREDICT − m_PREDICT. With the binary decision preserved, m_PREDICT is unchanged.
  - D_q = mean[q_int − q_intact], where q = π(RECHECK) + π(RESAMPLE).
- **Contrast precondition (per seed):** |m̄_PREDICT(CON) − m̄_PREDICT(DIS)| ≥ μ_contrast and ‖h̄_CON − h̄_DIS‖ > 0. Otherwise K2 and K3 are `NOT EVALUABLE [NO INTERVENTION CONTRAST]`, which is a seed non-pass. PROPOSED μ_contrast = 1/100.

### 10.4 Control families (K2), per recipient and per direction

All family paths are installed at the same recipient state and must pass the same battery (§11.1).

| Family | Construction | Count |
| --- | --- | --- |
| FO-matched | z_j ~ N(0, I₁₆), projected onto g^⊥ and rescaled to ‖P(h̄_D − h_R)‖ | 32 |
| ISO | z_j ~ N(0, I₁₆), rescaled to the same norm, no projection | 32 |
| random-donor | donor h drawn by weight from the whole S_I stage-2 recipient population, then P(h_donor − h_R) | 32 |
| same-content | donor = the recipient's own class mean | 1 |

Astra #30 L144: "Random-donor, same-content and first-order-matched intervention controls."

## 11. First-order controls, margins and the acquisition criterion [F9]

### 11.1 Declared first-order battery

- **Pre-check battery (gating):**
  - |p̂(h_int) − p̂(h_R)| ≤ τ_FO, PROPOSED τ_FO = 1/1000;
  - and the binary decision 1[p̂ > 1/2] is unchanged, for every recipient sample.
- **Post-check probes (reported, constraining):** p̂ after each of the 12 possible next reads (6 RECHECK outcomes and 6 RESAMPLE outcomes), compared intact versus intervened. If the weighted mean absolute change exceeds τ_post = 1/100 (PROPOSED), §2.3 applies.
  - Astra #30 L156: "Post-check probability effects remain separately reported and constrain the dissociation claim."
- **Family collapse:** a family path that fails the battery is excluded from the family maximum. If fewer than 16 of 32 paths of a family pass, that family is collapsed for the seed. That seed counts toward the >2 rule, following PR #9 (`first_order_control_protocol_FINAL.md`@335e505 L356).

### 11.2 K1: decoding beyond confidence (Astra #30 L151)

- E_base and E_dec are the weighted mean squared errors against m_a on S_E, averaged over the three actions.
- **PASS** iff E_base − E_dec ≥ μ1_abs and (E_base − E_dec)/E_base ≥ μ1_rel.
  - PROPOSED μ1_abs = 1/400.
  - PROPOSED μ1_rel = 1/2, the W-REL relative value.
- If E_base = 0, the label is `NOT EVALUABLE [NO BASELINE ERROR TO IMPROVE]`, which is not a pass. This is the W-REL boundary rule ("0/0 is never treated as a pass", `/workspace/review/c4_reliability_exact_check_spec_FINAL.md` L520).

Astra #30 L151: "Held-out state content predicts actual learner-specific correctness beyond the frozen confidence baseline, with both an absolute improvement floor and a relative criterion."

### 11.3 K2: content intervention with preserved first order (Astra #30 L152)

For each direction d ∈ {down, up}, with X ∈ {e, q}, μ_e = μ_q = 1/100 (PROPOSED, W-REL selection-margin values):

1. **Battery:** passes for the content intervention (§11.1).
2. **Direction:** σ_X·D_X^d ≥ μ_X for both X.
3. **D_FO:** σ_X·D_X^d − max_j σ_X·D_X^{FO,j} ≥ μ_X for both X. This is the PR #9 form "D_FO = (AUC_REV - max_j AUC_FO,j > eps0)" (`first_order_control_protocol_FINAL.md`@335e505 L303), with μ_X in place of eps0.
4. **D_ISO:** the same, against the ISO family.
5. **Random-donor:** σ_X·D_X^d − median_j σ_X·D_X^{RD,j} ≥ μ_X/2.
6. **Same-content null:** |D_X^{same}| ≤ μ_X/2.

K2 passes iff all six hold in both directions. D_FO ∧ D_ISO is jointly required, as in PR #9 (`first_order_control_protocol_FINAL.md`@335e505 L57).

Astra #30 L152: "Content intervention changes assessment error and checking in the predicted directions while the declared first-order battery is preserved."

### 11.4 K3: repair on a shared received history (Astra #30 L153)

- **Branches:** from each stage-2 recipient sample under each direction's content intervention, force a₂ = RECHECK. Both branches receive the same stage-3 read ỹ₃. All ≤ 6 received values are enumerated with their law weights.
  - Branch A continues from h_int.
  - Branch B is the repaired state at stage 3: h_B = h_A + P₃(h_shadow − h_A), where h_shadow is the intact recipient's stage-3 state on the same received history, and P₃ is the §10.2 projector at stage 3.
- **Statistics:** L_X = mean |e_X| and q_X at stage 3.
- **PASS** iff, in both directions:
  - L_A − L_B ≥ μ_res,L;
  - σ_e·(e_A − e_B) ≥ μ_res,a (the signed error is reduced);
  - σ_q·(q_B − q_A) ≥ μ_res,q (the checking change is reversed);
  - and the battery (§11.1) holds at stage 3 for the repair.
  - PROPOSED μ_res,L = μ_res,a = μ_res,q = 1/100.
- The conditioning event is fully specified by the law (§12). There is no occupancy-defined cell.

Astra #30 L153: "Repair reduces the assessment error and reverses the checking consequence on a shared received history."

### 11.5 K4: acquisition under the frozen seed rule (Astra #30 L154)

- J(s, ckpt) = valid ∧ K1 ∧ K2 ∧ K3, at that checkpoint.
- A seed acquires iff J(s, final) is VERIFIED PASS and J(s, init) is not met.
- "Not met" means at least one of K1–K3 is a VERIFIED FAIL or `NOT EVALUABLE [NO INTERVENTION CONTRAST]` / `[NO BASELINE ERROR TO IMPROVE]` at init. A boundary result at init makes the seed numerically unresolved.
- **Precedence** (PR #8 L282–L287, `GRADED_REVERSION_PROTOCOL_FINAL.md`@018f2a7):
  1. A support-audit failure means the design is not admitted (§12.5), and nothing runs.
  2. The CF1 and CF2 stop rules (§1).
  3. More than two invalid, numerically unresolved or family-collapsed seeds gives `UNRESOLVED (insufficient evaluable seeds)`.
  4. Count rule: at least 8 of the 10 seeds acquire, with the denominator 10, gives `ACQUIRED ROLE CRITERION MET (card status C4-candidate)`. Otherwise the label is `ACQUIRED ROLE CRITERION NOT MET`.
- The 8/10 bar is frozen here as a default carried from the lineage. It is not inherited automatically.

Astra #30 L154: "The conjunction is not met at initialization and is met after the declared training budget under the frozen seed rule."

### 11.6 All margins in one place (PROPOSED; to be frozen after §12.4)

| Symbol | Value | Used in | Source of value |
| --- | --- | --- | --- |
| δ_div, ν_div | 1/20, 1/20 | CF1a | new, PROPOSED |
| μ1_abs | 1/400 | K1, CF1b | new, PROPOSED |
| μ1_rel | 1/2 | K1, CF1b | W-REL relative value |
| μ_contrast | 1/100 | §10.3 | new, PROPOSED |
| τ_FO | 1/1000 | battery | new, PROPOSED |
| τ_post | 1/100 | post-check | new, PROPOSED |
| μ_e, μ_q | 1/100 | K2, CF2 | W-REL selection values |
| μ_res,· | 1/100 | K3 | W-REL rescue values |
| family-collapse floor | 16 of 32 | §11.1 | new, PROPOSED |
| numerical t | 1e-9 | §15.2 | PR #10 |
| agreement | 1e-12 + 1e-9·max(abs(x), abs(y)) | §15.2, §13 | PR #10 |

## 12. Rescue conditioning events and support requirements: the pre-execution SUPPORT AUDIT [F10]

Astra #30 L184: "The new spec must contain a support audit before execution. It must not inherit PM-ACT's undefined-rescue problem or use failure of a compiled control as a necessary success condition."

### 12.1 The design rule that prevents the PM-ACT failure

The PM-ACT rescue in W-REL was `NOT EVALUABLE [zero-probability event]` (`c4_reliability_exact_check_v1/RESULTS_A3_D2.md`@1f2a6c9 L47). Its provenance was classified as "(ii) a repaired PM state with zero occupancy under the intact distribution that defines its decoder" (`c4_reliability_exact_check_v1/WREL_CLOSEOUT_E30_v1.md`@37414d0 L17).

The cause was a decoder defined as an occupancy-weighted cell average, which is undefined off the intact policy's support. This spec makes three changes:

1. Every conditioning event is a world-plus-fault-law event under the declared do-distribution (§6.3), never an event defined by the learner's own occupancy.
2. The decoder is a total function of h (affine, §10.1), so it is defined at every intervened or repaired state.
3. Supports are computed from the law alone in Stage 0, before training. No learner output enters them.

### 12.2 Events audited and minimum support (PROPOSED thresholds)

For every event E used by a gating statistic, the requirements are:
- (i) law mass P(E) ≥ s_min = 1/100 within its stage's do-space;
- (ii) at least n_min = 32 distinct samples;
- (iii) at least n_H = 4 distinct world histories;
- (iv) for decoder fits, at least 4·(17+1) = 72 positive-weight S_I samples per action and stage pooled.

| Event (per split) | Mass (analytic) | Samples | World histories | Meets? |
| --- | --- | --- | --- | --- |
| stage-2 after RECHECK, DIS | (1/2)·(35/384) = 35/768 ≈ 0.0456 | 6·30 = 180 | 6 | yes, analytic |
| stage-2 after RECHECK, CON | 1/2 − 35/768 = 349/768 | 6·(1+6) = 42 | 6 | yes, analytic |
| K3 DIS × forced RECHECK × ỹ₃ | 35/768 | 180·6 = 1,080 | 6 | yes, analytic |
| K3 CON × forced RECHECK × ỹ₃ | 349/768 | 6·1 + 36·6 = 222 | 6 | yes, analytic |
| decoder S_I, stages 1–3 pooled | 1/2 of each stage | ≈ 130,788/2 (exact count NEEDS-APPROVED-RUN) | 342 | yes for (iv) |

How the table entries are computed:
- **Masses:** the split carries 1/2 exactly (§7), and discordance is independent of y (§5.2).
- **CON samples per world history:** 1 under F = 0, plus 6 concordant (ỹ₁ = ỹ₂ = v) patterns under F = 1.
- **DIS samples per world history:** the 30 ordered pairs with ỹ₁ ≠ ỹ₂.
- **K3 CON samples:** under F = 0 there is one continuation. Under F = 1 there are 6 continuations for each of the 6 concordant patterns.
- **World histories for the decoder split:** 6 + 42 + 294 = 342.
- **Status:** the analytic rows are hand counts. An exact enumerated confirmation (masses as rationals, sample counts) is a Stage 0, learner-free computation: NEEDS-APPROVED-RUN (pre-freeze, A-PRE).

### 12.3 Learner-dependent quantities are not support events

The recipient contrast (§10.3), the decoder's subspace dimension (§10.2) and the battery outcomes depend on the trained learner. They are outcomes, not supports. They are labelled NOT EVALUABLE or non-pass per seed, never rescued by redefining events.

### 12.4 Reference attainability and contrast, checked before freeze (W-REL lesson)

Before freeze, a reference-only exact enumeration (R-HIST and the oracle, no learner) must show, at the declared costs:
- (a) a positive optimal checking rate for RECHECK on some stage-1 world history and for RESAMPLE on some stage-1 world history;
- (b) a CON/DIS correctness contrast ≥ μ_contrast for R-HIST;
- (c) the K2 and K3 directional predictions hold in sign for R-HIST's own assessment quantity.

This is NEEDS-APPROVED-RUN (pre-freeze, reference-only, seconds by analogy with the W-REL analytic reference, which Astra #30 L164 describes as needing "seconds").

Hand-derivable necessary conditions:
- the payoff gain of any single check is bounded above by the probability that the post-check decision differs from the current one;
- Appendix A shows that the binary alternative fails (a).

### 12.5 On support-audit failure

If any audited event fails (i)–(iv), or §12.4 fails, the label is `DESIGN NOT ADMITTED (support audit)`. The response is a **redesign**: a new spec version with changed world law, perturbation, costs or event definitions, followed by re-review by Astra and re-approval by Aidan. It is **not a rescue**:
- no extension rule;
- no event merging after the fact;
- no reweighting;
- no partial evaluation under this version.

## 13. Compiled-control domain and intervention/readout correspondence [F11]

Astra #30 L145: "A compiled implementation of the frozen learner over the declared finite audit domain."

Astra #30 L147: "It is an equivalence control, not a presumed negative example of assessment. If it reproduces the role, record an ordinary alternative implementation."

### 13.1 Construction

- **Domain D** consists of:
  - all 22,620 received histories at stages 1–4 (§6.3);
  - all mapped intervention keys (recipient received history at stage 2, which is 2·36 = 72 histories, × intervention id, which is 2 content + 3·32 family + 1 same-content = 99);
  - their 12 post-check continuations and the 6 K3 continuations in each branch.
- **Compiled table C:** key → (p̂, π). It is filled by the frozen learner (E1) and independently by E2.
- An intervention in the network maps to the corresponding key in C. That is the intervention/readout correspondence.

### 13.2 Equivalence margin and test

- Every tabulated output and every deciding behavioural statistic (the CF and K statistics that do not use h) recomputed from C must agree with the network value within the PR #10 agreement form abs(x−y) ≤ 1e-12 + 1e-9·max(abs(x), abs(y)) (`frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L178–L206).
- Every binary decision must be identical.
- Decoder-based statistics (K1, e, the K3 error terms) need h, which C does not have. They are `NOT EVALUABLE [READOUT UNAVAILABLE IN COMPILED REPRESENTATION]`. Astra #30 L147: "If an assessment readout is unavailable in one representation, report that limitation without treating it as role absence."

### 13.3 What equivalence implies

- **Equivalent (the expected case):** record "an ordinary alternative implementation" reproduces the tested behaviour on D. The §2.3 restriction is attached. Equivalence is **not** a failure, and **non-equivalence is not a success condition**.
- **Not equivalent:** this is a compilation integrity failure. The label for that seed's compiled control is `INVALID [COMPILATION]`. The study's verification is incomplete (`UNRESOLVED-COMPUTE`, §14) until the cause is found under approval, because the table is by construction a copy of the network on D.
- No result of this control enters K1–K4. Astra #30 E30-7 (L214): "It does not require a faithful compiled implementation to lack or fail the proposed functional role."

## 14. Outcome labels for failure, undefined support and incomplete computation [F12]

| Label | Meaning |
| --- | --- |
| `ACQUIRED ROLE CRITERION MET (card status C4-candidate)` | §11.5 count rule met |
| `ACQUIRED ROLE CRITERION NOT MET` | count rule not met, with per-seed reasons |
| `STOPPED AT CF1: …` / `STOPPED AT CF2: …` | §1 stop rules |
| `UNRESOLVED (insufficient evaluable seeds)` | more than two invalid, unresolved or family-collapsed seeds |
| `DESIGN NOT ADMITTED (support audit)` | §12.5; nothing runs |
| `UNRESOLVED-DESIGN` | an output, intervention correspondence or criterion turns out to be undefined. This is the W-REL label, used here with the same meaning (`c4_reliability_exact_check_v1/RESULTS_v3.md`@0e17a05 L40) |
| `UNRESOLVED-COMPUTE` | a cap was exceeded, verification is incomplete, or the compiled control is invalid |
| `NOT EVALUABLE [reason]` | per statistic: NO INTERVENTION CONTRAST, NO BASELINE ERROR TO IMPROVE, NO ASSESSMENT DIRECTION ORTHOGONAL TO FIRST ORDER, or READOUT UNAVAILABLE IN COMPILED REPRESENTATION |
| `INVALID [reason]` | per run: NaN, determinism, manifest mismatch, freezing check, or cap |
| `BOUNDARY` | evaluators agree but the statistic is within t of a threshold; counts as numerically unresolved |

All counts are reported with the denominator ten. NOT EVALUABLE is never a pass.

## 15. Verification coverage, smoke tests, retries and hard caps [F13]

### 15.1 Sealed-manifest staged runner (reuse of PR #10 §9)

Consult #18, as quoted in PR #10: "For future studies, use a two-stage runner: write and seal the transformed-path manifest, then evaluate curves from that manifest." (`frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L376).

- **Stage 0 (no training).** Contains:
  - support audit (§12), split hashes, the information ledger and init checkpoint hashes;
  - episode-stream digests per seed (sha256 of all accepted draws, regenerated without training);
  - family generator draws;
  - code-tree sha, spec sha and fixture-test results.
  - It is sealed by commit or timestamped artifact. It is immutable. Corrections go in a dated addendum, following the PR #10 lesson E-D1 (`results_v1_errata/ERRATA_v1.md`@0329818 L9).
- **Stage 1 (training only).** Contains final checkpoint hashes, integrity flags, timing and peak RSS. There is no target evaluation. It is sealed by a separate commit before any Stage 2 code runs.
- **Stage 2a (CF1)**, then **Stage 2b (CF2)**, then **Stage 2c (full K1–K4 and compiled control)**. Each loads only checkpoints whose sha matches the sealed manifests and writes its own sealed output before the next sub-stage starts.
- **Stage 3:** independent replay of every deciding statistic from the stored tables, then mechanical labels.

### 15.2 Dual evaluator (reuse of PR #10 §3.1, rewritten)

- **E1:** torch float64 forward pass and metrics.
- **E2:** an independent NumPy float64 forward pass and metric implementation, with no torch and no import of E1. This follows the PR #10 pattern (`frozen_recurrent_compensation_numpy_eval.py`@0fed34e L1–L3).
- For every deciding statistic S with threshold μ:
  - VERIFIED PASS iff both S₁, S₂ ≥ μ + t;
  - VERIFIED FAIL iff both ≤ μ − t;
  - otherwise BOUNDARY;
  - with t = 1e-9 (`frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L178–L206).
- Disagreement beyond the agreement form is an integrity failure for the seed.
- The world-law masses used in targets and supports are computed in exact rationals by E2 and in float64 by E1, and compared.

### 15.3 Verification coverage (what is checked, by what)

| Item | Check |
| --- | --- |
| Inputs and loss | static audit: no F, ρ, Y-as-input, m or o in the training code paths; import graph has no decoder or target modules |
| Freezing during evaluation | all tensors requires_grad=False and absent from any optimizer; sha256 byte equality before and after evaluation. Pattern from PR #10 Edit 4 (`frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L218–L225) |
| R-FO restriction | static and fixture check that the action head's input is exactly [p̂.detach(), N, read type, stage] |
| Targets | E1 and E2 agreement. A fixture with a hand-computable learner (always predicts 1[ỹ>3]) checks m_a against hand values |
| Interventions | the battery is recomputed by both evaluators. Family norms are checked against ‖P(h̄_D − h_R)‖ to the agreement form |
| Support | Stage 0 rational masses equal the §12.2 analytic values |
| Compiled control | §13.2 |

### 15.4 Smoke tests, retries and hard caps (PROPOSED)

- **Smoke tests** run before Stage 1, on synthetic fixtures only. There is no fresh-seed training, following PR #10's rule "do not consume an additional fresh-seed training run" (`frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L225). The cap is 120 s total.
- **Retries:** none. Any cap breach or integrity failure marks the item INVALID or UNRESOLVED-COMPUTE. There is no rerun without a new approval.
- **Hard caps:**
  - one CPU process, `torch.set_num_threads(1)`, no GPU;
  - peak RSS ≤ 4 GB;
  - per training run ≤ 270 s wall-clock;
  - Stage 1 total ≤ 90 min;
  - Stage 0 ≤ 5 min;
  - Stage 2 (a+b+c) ≤ 45 min;
  - compiled control ≤ 15 min;
  - Stage 3 ≤ 30 min;
  - **cumulative ≤ 180 CPU-min**.
  - The caps are about 2.5× the §16 analytic bounds. A cap breach is not a reason to extend.

## 16. Throughput and evaluation-cost estimates (bounds, with sources) [F13]

Astra #30 L164: "This is an estimate, not an execution budget; bounded throughput and evaluation-cost estimates must appear in the spec."

| # | Quantity | Value | Source label |
| --- | --- | --- | --- |
| T1 | GRU-8 PR #7-recipe training run, 4000 updates at B = 256 | min 13.46 s, max 14.02 s, sum 409.36 s over 30 runs | **MEASURED-RECORD** `frozen_recurrent_compensation_results_v1/stage1/manifest_stage1.json`@22654aa (field "seconds", first at L29); runtime python 3.12.3, torch 2.14.1+cpu (`frozen_recurrent_compensation_results_v1/stage0/manifest_stage0.json`@fd720ee L329–L330). CPU model not recorded |
| T2 | GRU-8 per-update time | ≤ 14.02/4000 = 3.505 ms | ANALYTIC from T1 |
| T3 | GRU-8 training FLOP per update | ≈ 6.56 MFLOP | ANALYTIC (Appendix B) |
| T4 | Achieved effective rate | ≥ 26.26 GFLOP / 14.02 s ≈ 1.87 GFLOP/s | ANALYTIC from T1 and T3 (derived, not measured) |
| T5 | GRU-16 per-update time at B = 64 | ≤ 3 × 3.505 = 10.5 ms | ANALYTIC BOUND (Appendix B: FLOP ratio 0.65, op-group ratio 2.4, bound r ≤ 3) |
| T6 | Training per run, 10,000 updates | ≤ 105 s | ANALYTIC BOUND from T5 |
| T7 | Stage 1, 20 runs | ≤ 35 min | ANALYTIC BOUND |
| T8 | Evaluation network FLOP per checkpoint per evaluator | ≤ 1.7 GFLOP (tabulation ≤ 0.51 plus interventions ≤ 1.19) | ANALYTIC (Appendix B) |
| T9 | Evaluation time, 40 checkpoints × 2 evaluators | ≤ 12.1 min, assuming ≤ 10× slowdown from T4 for float64 small-batch work | ANALYTIC BOUND, slowdown factor ASSUMED |
| T10 | Target sums | ≈ 6.5e6 weighted terms per checkpoint | ANALYTIC; time not bounded from any record |
| T11 | Total | ≈ 35 + 15 + 2 + 15 ≈ 67 min | ANALYTIC BOUND, below Astra's "a few CPU-hours" planning figure |
| T12 | Peak memory | analytic < 1 GB (states 22,620×16×8 B ≈ 2.9 MB; sample table ≈ 130,788×10×8 B ≈ 10.5 MB; plus the torch runtime) | ANALYTIC; **no RSS figure exists in any GRU record** |
| T13 | Earlier evaluation-time statement | "60 checkpoints (init and final) × 256 histories × 2 evaluators, taking seconds" | PROTOCOL CLAIM, not a measurement (`frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L429) |

The analytic total is below Astra's ballpark because targets are computed from a decision table over 22,620 received histories rather than by per-sample rollouts. If Astra prefers rollouts, T8–T11 must be recomputed (Q-A9).

A fresh GRU-16 timing, an RSS measurement and a float64 evaluation timing all need execution: **NEEDS-APPROVED-RUN** (§21). They are not used to set caps beyond the bounds above.

## 17. Rivals and the tests that rule each out

### 17.1 First-order-only learner (R-FO; trained comparison arm)

**Rival claim:** checking is driven by first-order confidence alone, so there is no separate assessment content.

**Tests:**
- K1 requires prediction beyond confidence.
- K2 requires checking effects with the pre-check battery preserved and decisions identical. That excludes changes routed through p̂.
- **R-FO arm:** the action head reads only [p̂ (detached), N, read type, stage], trained with the identical recipe and seeds. Its K2 checking effects must be zero to the agreement form, by construction. If R-FO "passes" K2, the intervention pipeline is broken. The label is then `UNRESOLVED-DESIGN [K2 PIPELINE]` for the study, not a CAND pass. R-FO's reward and checking rates are reported descriptively.

### 17.2 Supplied assessment channel

**Rival claim:** the assessment was built in through the inputs, the loss, the architecture or the analyst.

**Tests:**
- static input and loss audit (§15.3);
- no dedicated register (§4.1 parameter count);
- the decoder is fitted only after the Stage 1 seal;
- the init control (K4), which must not meet the conjunction;
- the information-access ledger (§9.4).

### 17.3 Oracle leakage

**Rival claim:** the decoder recovers the world-model oracle's correctness, or target information leaked into training or features.

**Tests:**
- (a) m_a is computed from the learner's own decision table, not o_a. The fixture test of §15.3 covers this, and CF1a requires measurable divergence.
- (b) S_I ∩ S_E = ∅ over world histories, checked by hash.
- (c) The decoder features are h only.
- (d) **Permuted-target control:** the decoder is fitted on S_I with m_a permuted across world histories within stage, using a fixed generator seeded 9000+s. If it meets the K1 margins, K1 is `UNRESOLVED-DESIGN [DECODER LEAKAGE OR DEGENERACY]`.
- (e) **Oracle-target decoder:** the same decoder is fitted to o_a and its error is scored against m_a. If E_o→m ≤ E_dec + μ1_abs, K1 is a non-pass, recorded as "NOT DISTINGUISHED FROM ORACLE CORRECTNESS".
- (f) Training never reads m or o (static audit).

## 18. Reuse of the GRU-8 lineage

| Element | Source (file@commit) | Reused as | Where it does not fit |
| --- | --- | --- | --- |
| Harness: optimizer, schedule, clip, threads, float32 train / float64 eval, generator 1000+s | `RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md`@d118ae1 L36–L40; `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md`@0b98460 L100–L106 | §4.2, §8 | Studied GRU-8 (PR #7 L19); here GRU-16 with I = 14 and two heads. PR #5 ran GRU-16 only as a secondary configuration of a different world and input (9 inputs, `acquisition_results_v1/runs/cand_gru16_s0.json`@b25a30a L9–L11). The terminal squared-error loss is replaced by BCE + REINFORCE. B is 64 instead of 256, and there are 10,000 updates instead of 4000. The 256-history exhaustive enumeration is replaced by 22,620 received histories. The W2 world, split and A-FIT gates are not reused |
| FO+ISO conjunctive controls | `first_order_control_protocol_FINAL.md`@335e505 L57, L91–L92, L303, L356–L359 | §10.4, §11.3: 32+32 paths, joint D_FO ∧ D_ISO, family-collapse rule | PR #9 perturbs the weight_hh parameter path with dose AUC and matches the initial loss derivative. Here the interventions are single state-space installations at h. FO matching is orthogonality to ∇p̂ plus a norm match. There is no dose path, and the eps0 margin becomes μ_X |
| R-FIX freezing checks | `frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L218–L225 | §15.3, for frozen-learner evaluation and the init control | There is no R-FIX arm (no frozen weight_hh training). R-FO restricts the action-head input instead of freezing a matrix |
| 8/10 bar, denominator 10 | `GRADED_REVERSION_PROTOCOL_FINAL.md`@018f2a7 L287; `frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L302 | §11.5, frozen here as a default | The bar is applied to a four-part conjunction including an init-failure requirement, not to one statistic |
| UNRESOLVED for >2 invalid seeds | `GRADED_REVERSION_PROTOCOL_FINAL.md`@018f2a7 L285; `first_order_control_protocol_FINAL.md`@335e505 L356 | §1, §11.5 | Extended to cover CF stops and family collapse |
| Two-stage sealed-manifest runner | `frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L374–L394; manifest `frozen_recurrent_compensation_results_v1/stage1/manifest_stage1.json`@22654aa | §15.1 | Extended with Stage 0 support audit and sub-stages 2a/2b/2c for falsifier gating. Stage 0 is immutable with an addendum (E-D1) |
| Dual evaluator | `frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L178–L206; `frozen_recurrent_compensation_eval.py`@0fed34e; `frozen_recurrent_compensation_numpy_eval.py`@0fed34e | §15.2 | PR #10 decided one target T per checkpoint. Here many statistics are decided. E2 code must be new: the forward pass, two heads and policy differ |
| Same-network-at-init idea | `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md`@0b98460 L133 (K-FR, frozen at init with readout trained) | §9.3, simplified | Here the init network is evaluated untrained. No readout is retrained |

The systems are separate. GRU-8 two-stream results (for example the PR #9 8/10 joint count, `first_order_control_results_v1/PHASE_B_RESULTS_v2.md`@4f6fc4c L26–L30) are not evidence about this GRU-16 learner.

## 19. W-REL lessons applied

1. **No-contrast settings.** W-REL recorded settings with no donor contrast: "At (1/50, 3/50) the reference has no donor contrast" (`c4_reliability_exact_check_v1/RESULTS_v3.md`@0e17a05 L43). The rows were kept `NOT EVALUABLE [NO INTERVENTION CONTRAST]` (`c4_reliability_exact_check_v1/WREL_CLOSEOUT_E30_v1.md`@37414d0 L67). Applied here:
   - the §10.3 contrast precondition;
   - the §12.4 reference contrast check before freeze;
   - the rejection of the binary-flip world (Appendix A).
2. **Cost-ceiling attainability checked before freeze.** W-REL learned after the fact that full reference-conjunction attainment was excluded in ten of twelve H0 settings (`c4_reliability_exact_check_v1/WREL_CLOSEOUT_E27_v1.md`@7b89c66 L77). Here, the §12.4 attainability check at the declared costs is a pre-freeze gate. The analytic part is Appendix A and the §12.4 necessary bound. The exact part is NEEDS-APPROVED-RUN (reference-only).
3. **UNRESOLVED-DESIGN labels.** The W-REL definition is reused verbatim in meaning (`c4_reliability_exact_check_v1/RESULTS_v3.md`@0e17a05 L40). It is kept distinct from failure and from compute incompleteness (§14).
4. **Zero-support rescue.** The decoder support and conditioning events are law-defined (§12.1), following Astra #30 L52: "We should have checked the decoder and repair-state support under compilation before freezing this comparison."
5. **Compiled control is not a negative control.** Astra #30 L50: "That does not establish that the compiled implementation lacks the functional role." See §13.

## 20. Open questions for Astra

- **Q-A1.** Should H be the world-observable history, as here with faults latent, or the learner's received history? The choice changes m_a, the decoder's achievable error and CF1a.
- **Q-A2.** Is perturbing the evidence-encoding step a faithful reading of "the learner's read-processing computation", or should the perturbation act on the hidden state or the GRU update?
- **Q-A3.** Are the graded alphabet, the emission table, φ = 1/4, κ = 1/4, K_max = 3 and the costs (1/100, 3/50) acceptable, subject to the §12.4 check?
- **Q-A4.** What margin values should be used (§11.6)? In particular: is μ1_rel = 1/2 reasonable for a learned affine decoder, is τ_FO = 1/1000 too tight given that the battery is first-order-orthogonal only, and what is δ_div?
- **Q-A5.** Is a decoder class of affine ridge regression with no selection acceptable, or should it be logistic?
- **Q-A6.** Class-mean donors or single-donor draws (E29-3)? The random-donor criterion uses the median rather than the maximum. Is that acceptable?
- **Q-A7.** Should R-HIST gate anything for the learner, or stay a reference only?
- **Q-A8.** Learning rule: REINFORCE with an EMA baseline and an entropy bonus of 0.01 at B = 64. Is this an acceptable reading of "action selection from correctness minus checking cost"?
- **Q-A9.** Is the decision-table computation of targets acceptable in place of rollouts? It drives the cost bounds in §16.
- **Q-A10.** Is the CF2 definition (with CF2-null counted toward the stop) faithful to L162?
- **Q-A11.** Should the 8/10 bar apply to the full conjunction including the init requirement, or should init failure be a separate gate?

## 21. Not grounded in the record, and NEEDS-APPROVED-RUN items

Not grounded in any record (stated as PROPOSED or ANALYTIC):
- every numeric design value in §5 and §11.6;
- GRU-16 throughput (T5–T7) and the effective FLOP rate (T4, derived);
- the float64 evaluation slowdown factor (T9, assumed);
- memory (T12): no GRU record contains RSS;
- evaluation wall-clock: only the PR #10 protocol's "taking seconds" claim exists;
- the CPU model of the timed host: not recorded;
- the exact pooled decoder sample counts (§12.2 last row).

NEEDS-APPROVED-RUN, requiring A-PRE before freeze, all learner-free:
- (N1) exact rational enumeration of the §12.2 supports and the §7 split masses;
- (N2) the §12.4 reference attainability and contrast check (R-HIST and the oracle at the declared costs);
- (N3) a bounded smoke timing of the GRU-16 update and float64 evaluation on synthetic fixtures, with no fresh seed, to replace T5 and T9 with measurements and to record RSS (T12).

N3 is optional, because the caps are set from the bounds.

## 22. Freeze-list coverage table (Astra #30 L170–L182)

| # | Astra freeze item (verbatim) | Spec section(s) |
| --- | --- | --- |
| F1 | The exact scientific claim and claim ceiling. | §2 |
| F2 | Network, inputs, readouts and learning rules. | §4 |
| F3 | World law, internal perturbations, costs and event order. | §5 |
| F4 | The assessed prediction stage and learner-specific target. | §6 |
| F5 | Training, identification and evaluation splits. | §7 |
| F6 | Seeds, training budget, checkpoints and stopping rules. | §8 |
| F7 | Baselines, information access and resource accounting. | §9 |
| F8 | Decoder selection and intervention construction. | §10 |
| F9 | First-order controls, all margins and acquisition criterion. | §11 |
| F10 | Rescue conditioning events and support requirements. | §12 |
| F11 | Compiled-control domain and intervention/readout correspondence. | §13 |
| F12 | Outcome labels for failure, undefined support and incomplete computation. | §14 |
| F13 | Verification coverage, smoke tests, retries and hard caps. | §15, §16 |

## Appendix A. Why a binary-read world was rejected (hand arithmetic)

**Setting:**
- binary reads x ∈ {0,1} with P(x = Y) = 1 − ε_N, where ε_lo = 1/10 and ε_hi = 3/10;
- the same F (φ = 1/4) and a per-read flip with probability κ = 1/4 under F = 1.

**Received-read accuracy:** p_N = (1−ε)(1−φκ) + ε·φκ.
- lo: 0.9·15/16 + 0.1/16 = 0.85.
- hi: 0.7·15/16 + 0.3/16 = 0.675.

**Lemma.** For two exchangeable binary received reads with a symmetric posterior on disagreement, PREDICT-after-two-reads accuracy = P(both correct) + ½·P(disagree) = ½ + ½·(P(r₁ correct) − P(r₂ wrong)) = ½ + ½·(2p − 1) = p.

- RECHECK pairs (same sample, F shared) and RESAMPLE pairs (fresh sample, F shared) are both exchangeable. Cue-level symmetry makes the disagreement posterior ½.
- So a single extra read has zero gain at either cue, and costs make it strictly unprofitable.

**Two RECHECKs (majority of three copies):**
- P(majority = world value) = 3/4 + 1/4·(27/64 + 27/64) = 246/256.
- lo accuracy: 0.9·246/256 + 0.1·10/256 = 0.86875, a gain of 0.01875 < 2c_R = 0.02.
- hi accuracy: 0.684375, a gain of 0.009375 < 0.02.

The reference therefore never checks at the W-REL costs, and K2/K3 have no contrast. This is a no-contrast trap. The graded world of §5.1 breaks the lemma's symmetry, because a value's reliability depends on its grade. Whether it restores profitable checking is exactly the §12.4 check (NEEDS-APPROVED-RUN).

## Appendix B. FLOP and op-count arithmetic (ANALYTIC)

**FLOP model.** Dense multiply-add counts as 2 FLOP. GRU step ≈ 2·3H·(I+H) + 20H (elementwise, bound). MLP H→32→o ≈ 2·(32H + 32o) + 33 + o. Training ≈ 3× forward.

**GRU-8 harness** (I = 9, H = 8, terminal readout 8→32→3, 8 steps):
- step 976, ×8 = 7,808;
- readout 740;
- forward 8,548 per episode;
- training 25,644 per episode;
- ×256 = 6.56 MFLOP per update;
- ×4000 = 26.26 GFLOP in ≤ 14.02 s (T1).

**GRU-16 study learner** (I = 14, H = 16, two heads at each of ≤ 4 steps):
- step 3,200 + heads (1,122 + 1,252) = 5,574, ×4 = 22,296 forward per episode;
- training 66,888 per episode;
- ×64 = 4.28 MFLOP per update;
- FLOP ratio to GRU-8 = 0.65.

**Op-group ratio** (launch-overhead proxy):
- GRU-8: 8 cell calls + 2 linear = 10 per forward.
- GRU-16: 4 cells + 4×(2 heads × 2 linear) + 4 sampling = 24.
- Ratio 2.4.

**Bound.** r ≤ 3 covers max(0.65, 2.4) with margin. This assumes per-update time scales at most linearly with the larger of FLOP and op-group count on the same host class. That assumption is not verified.

**Evaluation:**
- tabulation of 22,620 received histories by prefix sharing: 22,620 one-step forwards × 5,574 ≈ 0.126 GFLOP, bounded at ≤ 0.51 without sharing;
- interventions: 72 recipient states × 99 interventions × ≤ 30 one-step forwards × 5,574 ≈ 1.19 GFLOP.

End of draft v1.
