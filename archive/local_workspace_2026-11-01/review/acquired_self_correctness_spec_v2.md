# Acquired assessment of the learner's own correctness: study specification v2 (DRAFT, PAPER ONLY)

Status: **DRAFT FOR REVIEW. NOT FROZEN. NOT APPROVED. NO LEARNER HAS BEEN RUN.**
Prepared 2026-10-21 (ET) by the research delegate for Aidan Ahern, ACI Track A.
No consciousness claim. NOT CLAIMED: C4 status, C5 status, consciousness, or any claim of autopoiesis or of being alive.

This document supersedes nothing on disk. It is a new file. v1 (`acquired_self_correctness_spec_v1.md`, sha256 `54bc8ea3b050551095bcc4d2b93fbc62476e52eb1678b08bdd37b6c1cfc0c8ac`) stays as written.

v2 is based on three inputs:
- v1;
- the CNA adversarial review (`acquired_self_correctness_spec_v1_review.md`, sha256 `997b2594d54a3d13327fc6be3e8bedcdddb50fdfea89aba77b0695fae00f47fa`);
- the v1 reference-only checks (`acq_reference_checks/N1_N2_results_v1.md`, sha256 `472185bbc7ca57d4599cf75b6d13737173202e08b6ee12112cf808db101d1463`).

The change log is in §23.

## 0. Status, approvals, sources and constraints

### 0.1 Approval placeholders (all required before any freeze or learner run)

| Gate | Required sign-off | Status |
| --- | --- | --- |
| A-REVIEW | Astra review of this draft, with rulings on §20 | `[PENDING — Astra review]` |
| A-PRE | Reference-only pre-freeze checks N1/N2 on v2. These are recorded under the PI standing approval as applied by the Research Lead; see `acq_reference_checks/v2/N1_N2_results_v2.md` | recorded separately; not a freeze |
| A-FREEZE | Aidan approval of the frozen spec (FINAL, with sha256) | `[PENDING — Aidan approval]` |
| A-RUN | Aidan approval of the run, scoped to the frozen spec, its seeds and its §15 caps | `[PENDING — Aidan approval]` |

Astra #30 L216: "The standing approval should be recorded against the next study's concrete scope once its specification has been reviewed and frozen." This draft records no freeze or run approval.

### 0.2 Sources

- Astra consult #30 response: `/workspace/astra_consult30_response.txt`, sha256 `4cc628034185fe456fa1f39be5f9dbf52d1d5b3556d34d18d7996d1b9511d04c`, §E (L113–L184). Quotes are cited as `Astra #30 Lnnn` and checked verbatim.
- GRU lineage, read-only from `origin/pr/5`, `origin/pr/7`–`origin/pr/10`. W-REL lineage from `origin/pr/11`. Citations take the form `path`@commit Lnnn.
- The frozen W-REL specification on the box: `/workspace/review/c4_reliability_exact_check_spec_FINAL.md`, sha256 prefix `ae626b65`.

### 0.3 Standing constraints

- PAPER ONLY with respect to the learner. Every number is labelled by source.
- Items needing computation are marked **NEEDS-APPROVED-RUN** (§21). PROPOSED values are open for Astra.
- No repository change. The costs stay at (1/100, 3/50), as in v1, and are not tuned.
- Execution order once approved:
  1. Stage 0: reference and support audit, including the learner-free CF1a (§1.1, §12).
  2. Stage 1: training.
  3. CF1b and CF2 (§1).
  4. Full evaluation.

## 1. Cheap falsifiers, run first and each with a declared stop rule

Astra #30 L158: "Before expensive intervention analysis, check whether actual learner correctness differs meaningfully from oracle correctness and whether the candidate state predicts that difference beyond current confidence."

### 1.1 CF1, decomposed (CNA m1)

The three quantities are defined on received states R (§6):
- m_a(R): the frozen learner's own correctness;
- o^R_a(R): the fault-aware Bayes decision on R;
- o_a(R): the clean world-model oracle, averaged over world samples given R.

Then

  m − o = (m − o^R) + (o^R − o) = λ (learner-specific term) + Δ^F (fault-exposure term).

- **CF1a (fault exposure, learner-free, Stage 0).**
  - D^F = sqrt( (1/3) Σ_a Σ w·(Δ^F_a)² / Σ w );
  - M^F = Σ w·1[max_a |Δ^F_a| ≥ δ_div] / Σ w;
  - computed on S_E with the §6.3 weights.
  - CF1a holds iff D^F ≥ δ_div and M^F ≥ ν_div. PROPOSED δ_div = ν_div = 1/20, carried from v1. **The threshold and the fault strength are OPEN for Astra (Q-A13).**
  - Because Δ^F does not depend on the learner, CF1a is decided before any training. **If CF1a fails, the label is `DESIGN NOT ADMITTED (CF1a: fault exposure below threshold)`, nothing is trained, and the response is a redesign by Astra.** The threshold is not lowered to fit.
- **CF1b (learner-specific term predicted beyond first order, per seed, final checkpoint).**
  - Target: λ_a(R).
  - The §10.1 decoder must beat **both** the confidence baseline (§9.1a) and the first-order-input baseline (§9.1b) by μ1_abs and μ1_rel.
  - If a baseline error is 0, the label is `NOT EVALUABLE [NO BASELINE ERROR TO IMPROVE]`, which counts as a CF1b failure.
- **CF1b stop rule.** Precedence applies in this order:
  1. More than two invalid or unresolved seeds gives `UNRESOLVED (insufficient evaluable seeds)`.
  2. Otherwise, at least three CF1b failures gives `STOPPED AT CF1b: LEARNER-SPECIFIC CORRECTNESS NOT PREDICTED BEYOND FIRST ORDER`.
- **Reported on a stop:**
  - per seed: λ statistics, both baselines' errors, the decoder error, both evaluators' values and the flags;
  - the Stage 0 CF1a values;
  - the manifest hashes.

  No intervention statistic is computed. Astra #30 L160: "Do not search for convenient faults or checkpoints afterward."

### 1.2 CF2: checking effects always break the first-order battery

Astra #30 L162: "A second cheap falsifier is that every intervention producing a checking effect also damages the first-order probe battery beyond tolerance."

This is unchanged from v1 except that recipients are distinct received states (§10.3). Per seed and direction d:
- CE^d: σ_d·D_q^d ≥ μ_q.
- FP^d: the pre-check battery holds (B^d ≤ τ_FO, Dec^d = 0).
- A seed is **CF2-fired** iff some direction has CE^d and every such direction fails FP^d.
- A seed is **CF2-null** iff some direction lacks CE^d.
- **Stop rule:** after the >2 invalid precedence, if (#CF2-fired) + (#CF2-null) + (#CF1b failures) ≥ 3, the label is `STOPPED AT CF2`, with sublabel `NO FIRST-ORDER-PRESERVING CHECKING EFFECT` or `NO CHECKING EFFECT`.
- **Reported on a stop:** D_q, D_e (as a manipulation check), B, Dec and the flags, per seed and direction.

## 2. Scientific claim and claim ceiling [F1]

### 2.1 The exact claim (only if every gate in §11 passes)

For the declared GRU-16 learner trained for 10,000 updates on the declared task, in at least eight of ten prespecified seeds, with the denominator ten:

- **K1.** Held-out received-state content predicts the learner's own post-action correctness m_a(R) beyond both a confidence baseline and a first-order-input baseline. This is labelled a necessary condition, not by itself evidence of assessment (CNA M1).
- **K2.** Installing class-specific content changes **checking** in the predicted directions. The pre-check battery is preserved, and the effect exceeds FO, ISO and subspace-matched families. The assessment-error legs are reported as manipulation checks (CNA M3).
- **K3.** Repair on a shared received history reverses the checking change. The error reduction is reported as mechanical.
- **K4.** The conjunction is not met at initialization, and it is not met by the same seed's frozen-random-core arm K-FR (CNA M2).

The tags are Q-LEARN (K4) and Q-CAUSE (K2, K3), within the declared interventions and domain.

**Disclosure (CNA M5).** The content intervened on may be an acquired encoding of an input contrast, such as discordance between a read and its re-read. Under v2's κ₀ > 0 (§5.2), discordance is probabilistic evidence about the fault mode, not an indicator. The claim does not say that the learner computes anything beyond such an encoding.

### 2.2 Claim ceiling

**The card status is `C4-candidate` at most.** That is a card status, not a C-level determination. Astra #30 L166: "Neither the proposed study nor a positive result automatically establishes C4 status or consciousness." NOT CLAIMED: C4 status, C5, consciousness, autopoiesis, being alive, necessity, or behaviour outside the declared audit domain.

### 2.3 Restrictions attached automatically

1. **Compiled control equivalent (§13):** "An ordinary compiled implementation reproduces the tested predictions, actions and mapped interventions on the declared audit domain."
2. **Post-check battery (CNA M4).** Any wording of the form "assessment distinct from first-order prediction" requires the **post-check battery to pass as a gate** (§11.1). If it fails, the claim is narrowed to: "Checking is caused by state content orthogonal to the current first-order output." This follows Astra #30 L156: "Passing a pre-check battery is not preservation of the full first-order computation."
3. **R-VOI:** if R-VOI meets the conjunction in at least 8/10 seeds (§17.4), the label gains `[NOT DISTINGUISHED FROM FIRST-ORDER VALUE OF INFORMATION]`.
4. **Systems:** the result does not transfer to the GRU-8 two-stream studies (PRs #5 and #7–#10) or to the W-REL analytic agents.

## 3. Question separation (Q-tags)

| Tag | Content | Not covered |
| --- | --- | --- |
| Q-EXIST | Stage 0: CF1a (fault exposure), the support audit (§12) and reference attainability (§12.4) | Other tasks |
| Q-LEARN | K4: not at init, not by K-FR, present after training (8/10) | Learning dynamics |
| Q-CAUSE | K2 and K3, on the checking legs | Effects outside the declared interventions |
| Q-NECESSITY | **Not tested.** The compiled control is an equivalence control. R-FO, R-VOI and K-FR are comparisons | Everything |

The tags are reported separately and never pooled.

## 4. Network, inputs, readouts and learning rules [F2]

Astra #30 L121: "One small GRU, provisionally 16 hidden units, with ordinary prediction and checking-action readouts. No supplied assessment register, fault labels or oracle-correctness training target."

This section is unchanged from v1 §4. In summary:
- **Cell:** `nn.GRU(14, 16)`, h₀ = 0.
- **Inputs:** cue ±1, received ỹ one-hot (6), read type (3), stage (4). The stage code is an external timing scaffold, as in PR #5 (`TWOSTREAM_ACQUISITION_PROTOCOL_v1.md`@0b98460 L101).
- **Readouts:**
  - prediction head 16→32→1, decision 1[p̂ > 1/2] (`/workspace/review/c4_reliability_exact_check_spec_FINAL.md` L78);
  - action head 16→32→3.
- **Parameter count:** 1536 + 577 + 643 = 2756. The formula matches PR #5's GRU-16 record (`acquisition_results_v1/runs/cand_gru16_s0.json`@b25a30a L9–L10).

Astra #30 L123: "Train first-order prediction from revealed outcomes and action selection from correctness minus checking cost."

- **Loss:** BCE of p̂ against Y at every decision point, plus REINFORCE with an EMA baseline (β = 0.99) and an entropy bonus of 0.01.
- **Optimizer:** the PR #7 recipe (`RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md`@d118ae1 L36–L37).
- **Batch and determinism:** B = 64, single thread, deterministic (`RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md`@d118ae1 L40).
- No auxiliary target, fault label, m, o, o^R or correctness label. The decoder is fitted only after the Stage 1 seal.

## 5. World law, internal perturbations, costs and event order [F3]

Astra #30 L125: "A short finite episodic binary-evidence task with PREDICT, RECHECK and RESAMPLE. Retain the useful same-evidence versus fresh-evidence distinction."

### 5.1 World (unchanged from v1; PROPOSED)

- Y uniform; cue N ∈ {lo, hi} observable, 1/2 each.
- Evidence y ∈ {1..6}:
  - P(y | Y=1, lo) = (1,1,2,3,5,12)/24;
  - P(y | Y=1, hi) = (2,3,4,4,5,6)/24;
  - P(y | Y=0, N) = P(7−y | Y=1, N).
- Marginals: lo (13,6,5,5,6,13)/48; hi uniform.

### 5.2 Internal read-processing perturbation (v2: baseline noise κ₀ added, CNA M5)

Astra #30 L127: "Introduce prespecified stochastic perturbations in the learner's read-processing computation, alongside evidence-noise conditions. The intervention location, persistence and action-specific effects must be explicit."

- **Location:** the evidence-encoding step, as in v1. Q-A2 (hidden-state locus) stays OPEN. CNA m7 notes that an encoding-step perturbation reaches the learner only through its inputs.
- **Persistence:** episode fault mode F ~ Bernoulli(φ), φ = 1/4 (v1; fault strength OPEN, Q-A13).
- **Per-read effect, v2:** each read is replaced, independently, by a uniform draw from {1..6} with probability κ_F. That is κ₁ = κ = 1/4 under F = 1 (v1) and **κ₀ under F = 0 (new)**. So P(ỹ = y | F) = 1 − 5κ_F/6, and P(ỹ = v | F) = κ_F/6 for each v ≠ y.
- **Action-specific effects** are unchanged:
  - RECHECK re-reads the current world sample with a fresh processing draw;
  - RESAMPLE draws a fresh world sample with a fresh processing draw;
  - PREDICT reads nothing.
- The same law applies in training and evaluation.

**C-K0 criterion (verbatim; recorded with timestamp 2026-10-21 17:08:35 EDT in `acq_reference_checks/v2/PRE_RUN_FREEZE_v2.txt` before any v2 computation):**

> "kappa_0 is the per-read uniform-replacement probability under F = 0. It must satisfy: (1) kappa_0 > 0, so a RECHECK discordance is possible under F = 0 (CNA M5). (2) The single-discordance likelihood ratio LR = P(DIS | F=1) / P(DIS | F=0) lies in Jeffreys' 'substantial' evidence band [10^(1/2), 10], so a discordance is evidence of F = 1 but not an indicator, with kappa = 1/4 held at its v1 value. (3) kappa_0 = kappa / 2^j for the smallest integer j >= 1 satisfying (2), i.e. the weakest evidence inside the band, the least indicator-like admissible choice. The criterion uses only the per-read fault algebra P(DIS | r) = (5r/6)(2 - r). It does not use N1/N2, the reference controller, the oracle, CF1a or any learner quantity. Fault strength (phi, kappa) is not re-chosen; it stays OPEN for Astra. The resulting kappa_0 is not revised in light of N1/N2 v2."

**Hand algebra.** P(ỹ₁ = ỹ₂ | r) = (1 − 5r/6)² + 5(r/6)² = 1 − 5r/3 + 5r²/6. So P(DIS | r) = (5r/6)(2 − r).
- r = 1/4: 35/96.
- j = 1, κ₀ = 1/8: P(DIS | F=0) = 75/384, LR = 28/15 ≈ 1.87, which is outside the band.
- j = 2, κ₀ = 1/16: P(DIS | F=0) = 155/1536, LR = 112/31 ≈ 3.61, which is inside the band.
- **PROPOSED κ₀ = 1/16.**

Why not the room's example criterion of clearing the CF1a threshold by a margin: that would tie κ₀ to δ_div, which is itself OPEN (Q-A13), and it would choose the world by the statistic it is meant to test.

**Trade-offs for Astra (Q-A14):**
- A smaller κ₀ (larger j) makes discordance closer to an indicator, so the M5 fix is weaker, but it increases fault-exposure contrast.
- A larger κ₀ makes discordance weaker evidence and adds F = 0 errors.
- The Jeffreys band is a convention.

**Derived masses (exact hand algebra), with φ = 1/4, κ₀ = 1/16, κ = 1/4:**
- P(DIS) = (3/4)(155/1536) + (1/4)(560/1536) = 1025/6144, and P(CON) = 5119/6144.
- P(F=1 | DIS) = 560/1025 = 112/205.
- P(F=1 | CON) = 976/5119.

### 5.3 Costs and episode structure (unchanged)

- **Costs:** c_R = 1/100, c_S = 3/50 (`c4_reliability_exact_check_v1/RESULTS_A2.md`@dddd63c). They are not tuned.
- **Episode:** K_max = 3, with stage k the decision point after k reads.
- **Event order:** as in v1 §5.3.
- Astra #30 L129: "Do not assume that the old W-REL symmetry survives this change."

## 6. The assessed prediction stage and the learner-specific target [F4]

### 6.1 Target m_a(R), on the learner's received history (CNA B1; decides Q-A1)

Astra #30 L134–L135, verbatim:

```
m_a(H) = P(the frozen learner's own post-action decision is correct
           | observable history H, do(action=a))
```

**v2 reading.** "Observable history" is read as the **learner-observable** history: its received history R, meaning the cue, the received reads and the read types.

Under v1's world-observable reading, P(DIS | H) is constant, so m̄(CON) = m̄(DIS) for any learner. That is CNA B1, confirmed exactly by N2 v1, where both class means were 1105/1536.

v2 defines

  m_a(R) = Σ_{Y, world samples, F, next read} P(· | R, do(a)) · 1[the learner's post-action decision equals Y],

where:
- the posterior given R is computed under the declared world-plus-fault law;
- the post-action decision is ŷ = 1[p̂(R) > 1/2] for PREDICT, and the learner's immediate prediction after the new received read for RECHECK and RESAMPLE.

Astra #30 L138: "The target must include that learner's errors, not substitute the oracle's optimal decisions." Astra is asked to confirm this reading (Q-A1c).

### 6.2 Comparators on R

- **o^R_a(R):** correctness of the fault-aware Bayes decision on R (R-HIST's prediction readout), with the same post-action rule.
- **o_a(R):** expected correctness of the clean world-model oracle, whose decision uses the uncorrupted world samples. It is averaged over the world samples, Y and F given R, and the oracle's re-read under RECHECK is clean.
- The **decomposition** m − o = λ + Δ^F is defined in §1.1.

Astra #30 L127: "The purpose is to create cases in which the learner's actual conditional correctness differs from the world-model oracle's."

### 6.3 Domain and weights (corrected weight, from N1 v1)

- **Units:** distinct received states R at stages 1–3. There are 12 + 144 + 1,728 = 1,884 of them. Each R carries law mass P(R | do(prefix)).
- **Weight:** w(R) = P(R | do(prefix)) × **2^{−(k−1)}**, so the 2^{k−1} action prefixes are weighted uniformly.
  - v1's 4^{−(k−1)} did not normalize: N1 v1 found it sums to 1/2 at stage 2 and 1/4 at stage 3.
- **Positivity:** every R has positive mass under κ₀ > 0, under either fault mode.
- **Compiled domain:** stages 1–4, 12 + 144 + 1,728 + 20,736 = 22,620 states.

## 7. Training, identification and evaluation splits (on R; CNA B2) [F5]

- **Training** samples the task law unrestricted. Training never uses the decoder domain or any target.
- **Split rule:** **R ∈ S_E iff (ỹ₁ + 1[N=hi]) mod 2 = 1**, where ỹ₁ is the first received read. Otherwise R ∈ S_I.
- **Every state lies in exactly one split.** The held-out unit is the distinct learner state (CNA B2).
- **Mass check (hand algebra).** Under either fault mode, P(ỹ₁ = v | N) = (1 − r)P(y = v | N) + r/6. The odd set {1,3,5} carries (1 − r)·(1/2) + r·(1/2) = 1/2 under lo (13+5+6 = 24 of 48). The even set {2,4,6} carries 1/2 under hi. So each split carries exactly 1/2 of the law mass in every stage, cue and prefix.
- **State counts per split:** stage 1: 6; stage 2: 72; stage 3: 864.
- The split hash covers the sorted received-history indices. §17.3(b) checks disjointness **over received states**.
- **Doesn't fit from PR #7:** the TRAIN/TEST rule (`RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md`@d118ae1 L31) belongs to the W2 world and is not reused.

## 8. Seeds, training budget, checkpoints and stopping rules [F6]

- **Seeds:** s ∈ {500..509}. They must be disjoint from 200–209 (`GRADED_REVERSION_PROTOCOL_FINAL.md`@018f2a7 L283), 300–309 and 400–409.
  - Stream generator 1000+s (`RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md`@d118ae1 L39).
  - Action generator 3000+s.
  - Families: FO 1,000,000+100·s, ISO 40,000+100·s, random-donor 70,000+100·s and SUB 80,000+100·s, by analogy with `first_order_control_protocol_FINAL.md`@335e505 L197, L244.
- **Arms (v2), 40 runs:**
  - CAND (§4);
  - R-FO (§17.1);
  - **K-FR** (§9.3): core frozen at the seed's init, heads trained;
  - **R-VOI** (§17.4).
  - Each has 10 seeds, one run per seed, 10,000 updates at B = 64.
- **Checkpoints:** CAND init and final. Final only for R-FO, K-FR and R-VOI. K-FR's init equals CAND's init.
- **Stopping:** no early stopping, restarts or seed replacement. "There is no re-training" (`frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L394).

## 9. Baselines, information access and resource accounting [F7]

Astra #30 L142: "Current-output confidence and a cost-general history-dependent controller, with disclosed information and resources."

### 9.1 K1 and CF1b baselines

- **(a) Confidence baseline (v1).** Per action, weighted least squares on [1, c, c², c³], with c = p̂. Fitted on S_I.
- **(b) First-order-input baseline (new, CNA M1).**
  - The same affine ridge (λ = 1e-3·Σw) on the input-history features [p̂, N, stage one-hot (4), read-type one-hots for reads 2–4 (3×2), ỹ one-hots for reads 1–4 (4×6)].
  - That is 36 features plus the intercept, fitted on S_I.
  - It uses no internal state beyond the inputs and the current output.
  - Note: m_a(R) is a function of R, so a sufficiently rich input lookup could fit it exactly. K1 is therefore labelled a necessary condition (§2.1).

### 9.2 R-HIST (reference)

R-HIST is the exact Bayes controller over received history, given the law. It is used for Stage 0 attainability (§12.4) and the CF1a comparator o^R. It is not a gate for the learner (Q-A7 OPEN).

### 9.3 Initialization and frozen-core controls (CNA M2)

Astra #30 L143: "The same network at initialization, to distinguish acquired performance from supplied structure."
- **(a) Init checkpoint.** CAND untrained, full pipeline. This is K4's init leg.
- **(b) K-FR arm (new).**
  - The recurrent core is frozen at the seed's init. Both heads are trained with the identical recipe, stream and seed.
  - It reuses the PR #5 idea `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md`@0b98460 L133, with both heads trained instead of the readout only.
  - Freezing checks follow `frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L218–L225.
  - Full K1–K3 pipeline.

### 9.4 Information-access ledger

| Agent | Inputs | Knows the law? | Trained on | Trainable parameters |
| --- | --- | --- | --- | --- |
| CAND | N, ỹ, read type, stage | no | Y, payoff | 2756 |
| init | same | no | none | 0 (2756 at init) |
| K-FR | same | no | Y, payoff (heads only) | 577 + 643 = 1220 (core 1536 frozen) |
| R-FO | same; action head sees [p̂ (detached), N, read type, stage] | no | Y, payoff | 1536 + 577 + 419 = 2532 |
| R-VOI | same; action head sees [p̂ and its own 12 post-read p̂ (detached), N, read type, stage] | no | Y, payoff | 1536 + 577 + (21·32+32+32·3+3 = 803) = 2916 |
| confidence baseline | c | no | S_I targets | 4 per action |
| input baseline | input history + p̂ | no | S_I targets | 37 per action |
| decoder | h (16) | no | S_I targets | 17 per action |
| R-HIST, o^R | R | yes | none | table |
| oracle o | clean world samples | yes | none | — |

## 10. Decoder selection and intervention construction [F8]

### 10.1 Decoder (no selection)

- Per action, affine ridge on [1, h] (λ = 1e-3·Σw), fitted on S_I received states with weights w(R). Target m_a(R) for K1 and λ_a(R) for CF1b.
- Also fitted, as reported comparators: the same decoder on R-FO's and K-FR's hidden states (CNA M1).

### 10.2 Assessment subspace

A is the span of the three decoder weight vectors. g = ∇_h p̂. P projects onto A ∩ g^⊥. If dim(A ∩ g^⊥) = 0, the label is `NOT EVALUABLE [NO ASSESSMENT DIRECTION ORTHOGONAL TO FIRST ORDER]`.

### 10.3 Recipients and classes (distinct states)

- **Recipients:** S_E received states at stage 2 with read types (FIRST, RECHECK).
  - CON: ỹ₁ = ỹ₂. 6 states per split.
  - DIS: ỹ₁ ≠ ỹ₂. 30 states per split.
  - Class statistics are law-mass-weighted means over states.
- **Donor content:** h̄_D is the mass-weighted mean of S_I donor-class states. Single-donor draws are Q-A6.
- **Installation:** h_int = h_R + P(h̄_D − h_R).
  - Down: DIS content into CON recipients.
  - Up: CON content into DIS recipients.
- **Statistics:**
  - D_q = mean[q_int − q_intact], where q = π_R + π_S.
  - D_e = mean[e_int − e_intact], where e = m̂_P − m_P(R).
- **Contrast precondition:** |m̄_P(CON) − m̄_P(DIS)| ≥ μ_contrast = 1/100, with m on R. Otherwise `NOT EVALUABLE [NO INTERVENTION CONTRAST]`.

### 10.4 Control families (CNA M3: subspace-matched family added)

| Family | Construction | Count |
| --- | --- | --- |
| FO-matched | z ~ N(0, I₁₆), projected onto g^⊥, norm ‖P(h̄_D − h_R)‖ | 32 |
| ISO | z ~ N(0, I₁₆), same norm | 32 |
| **SUB (new)** | z ~ N(0, I₁₆), projected onto **A ∩ g^⊥**, same norm: random within the installation subspace | 32 |
| random-donor | donor h drawn by mass from all S_I stage-2 recipient states, then P(h_donor − h_R) | 32 |
| same-content | the recipient's own class mean | 1 |

Astra #30 L144: "Random-donor, same-content and first-order-matched intervention controls."

## 11. First-order controls, margins and the acquisition criterion [F9]

### 11.1 Battery

- **Pre-check battery (gating):** |Δp̂| ≤ τ_FO = 1/1000, and the decision is unchanged.
- **Post-check battery** (12 next reads):
  - weighted mean |Δp̂| ≤ τ_post = 1/100;
  - **gating for any "distinct from first-order prediction" wording** (CNA M4, §2.3);
  - otherwise reported, and the claim is narrowed.
- Astra #30 L156: "Post-check probability effects remain separately reported and constrain the dissociation claim."
- **Family collapse:** fewer than 16 of 32 battery-passing paths means the family is collapsed, and the seed counts toward the >2 rule (`first_order_control_protocol_FINAL.md`@335e505 L356).

### 11.2 K1: decoding beyond first order (Astra #30 L151)

Astra #30 L151: "Held-out state content predicts actual learner-specific correctness beyond the frozen confidence baseline, with both an absolute improvement floor and a relative criterion."

K1 passes iff, for **each** baseline b ∈ {confidence, input}, E_b − E_dec ≥ μ1_abs and (E_b − E_dec)/E_b ≥ μ1_rel, with errors on S_E against m_a(R). E_b = 0 gives NOT EVALUABLE. PROPOSED μ1_abs = 1/400, μ1_rel = 1/2 (Q-A4).

### 11.3 K2: checking legs gate, assessment legs mechanical (CNA M3; Astra #30 L152)

Astra #30 L152: "Content intervention changes assessment error and checking in the predicted directions while the declared first-order battery is preserved."

For each direction:
1. **Battery** (pre-check) passes.
2. **Direction:** σ_q·D_q ≥ μ_q = 1/100.
3. **D_FO, D_ISO and D_SUB:** σ_q·D_q − max_j σ_q·D_q^{fam,j} ≥ μ_q for each family. This takes the PR #9 form `first_order_control_protocol_FINAL.md`@335e505 L303, applied jointly as in L57.
4. **Random-donor:** σ_q·D_q − median_j σ_q·D_q^{RD,j} ≥ μ_q/2.
5. **Same-content:** |D_q^{same}| ≤ μ_q/2.
6. **Manipulation check (reported, not gating):** σ_e·D_e and its family comparisons. The installation lies inside the decoder span, so the e legs are mechanical (CNA M3).

### 11.4 K3: repair reverses checking (Astra #30 L153)

Astra #30 L153: "Repair reduces the assessment error and reverses the checking consequence on a shared received history."

- **Construction:** as in v1. Force RECHECK at stage 2 with a shared ỹ₃ and repair along P₃ toward the intact shadow.
- **Gating:** σ_q·(q_B − q_A) ≥ μ_res,q = 1/100 in both directions, with the stage-3 battery passing.
- **Reported as mechanical:** L_A − L_B and σ_e·(e_A − e_B).

### 11.5 K4: acquisition, with a paired frozen-core control (Astra #30 L154)

Astra #30 L154: "The conjunction is not met at initialization and is met after the declared training budget under the frozen seed rule."

- J(arm, s, ckpt) = valid ∧ K1 ∧ K2 ∧ K3.
- Seed s acquires iff all three hold:
  - J(CAND, s, final) is VERIFIED PASS;
  - J(CAND, s, init) is not met (as v1 §11.5);
  - J(K-FR, s, final) is not met.
- K-FR is paired by seed (same init core). A K-FR pass in seed s removes that seed from the success count.
- **Precedence:**
  1. Stage 0 support or CF1a failure means the design is not admitted.
  2. The CF1b and CF2 stop rules.
  3. More than two invalid, unresolved or collapsed seeds gives UNRESOLVED.
  4. Count: at least 8 of 10 gives `ACQUIRED ROLE CRITERION MET (card status C4-candidate)`. Otherwise NOT MET.
  5. Additional labels: §2.3. If K-FR meets J in at least 3 seeds, the report adds "role substantially supplied by random recurrent structure plus trained readouts in n/10 seeds".
- **Sources:** the 8/10 rule (`GRADED_REVERSION_PROTOCOL_FINAL.md`@018f2a7 L287) and the >2 invalid rule (L285).

### 11.6 Margins (PROPOSED unless noted; all OPEN for Astra, Q-A4 and Q-A13)

| Symbol | Value | Used in |
| --- | --- | --- |
| δ_div, ν_div | 1/20, 1/20 (v1; **OPEN**, Q-A13) | CF1a |
| μ1_abs, μ1_rel | 1/400, 1/2 | K1, CF1b |
| μ_contrast | 1/100 | §10.3 |
| τ_FO, τ_post | 1/1000, 1/100 | battery |
| μ_q, μ_res,q | 1/100 | K2, K3, CF2 |
| μ_e, μ_res,a, μ_res,L | 1/100 (reported only) | manipulation checks |
| family-collapse floor | 16 of 32 | §11.1 |
| t, agreement | 1e-9; 1e-12 + 1e-9·max(abs(x), abs(y)) | §15.2 (PR #10) |

## 12. Rescue conditioning events and support requirements: the pre-execution SUPPORT AUDIT [F10]

Astra #30 L184: "The new spec must contain a support audit before execution. It must not inherit PM-ACT's undefined-rescue problem or use failure of a compiled control as a necessary success condition."

### 12.1 Design rule (unchanged)

The PM-ACT rescue was `NOT EVALUABLE [zero-probability event]` (`c4_reliability_exact_check_v1/RESULTS_A3_D2.md`@1f2a6c9 L47). Its provenance was "(ii) a repaired PM state with zero occupancy under the intact distribution that defines its decoder" (`c4_reliability_exact_check_v1/WREL_CLOSEOUT_E30_v1.md`@37414d0 L17).

v2 keeps the v1 rule:
- conditioning events are law-defined received-state sets;
- the decoder is total (affine in h);
- supports are computed in Stage 0 from the law alone.

### 12.2 Minimums over distinct learner states (CNA B2/m5; N1 v1)

For every gating event E and every split:
- **(i)** law mass P(E) ≥ s_min = 1/100 within its do-space;
- **(ii)** at least n_state = 4 distinct received states, with at least one in each cue;
- **(iii)** for decoder and baseline fits, at least 38 distinct S_I states pooled over stages 1–3, which is the input baseline's 37 parameters plus 1.

| Event, per split (S_E and S_I alike) | Mass (hand algebra) | Distinct states | Per cue | Meets? |
| --- | --- | --- | --- | --- |
| stage 2 (FIRST, RECHECK), DIS | (1/2)(1025/6144) = 1025/12288 ≈ 0.0834 | 30 | 15 / 15 | yes, analytic |
| stage 2 (FIRST, RECHECK), CON | 5119/12288 ≈ 0.4166 | 6 | 3 / 3 | yes, analytic |
| K3: DIS × forced RECHECK × ỹ₃ (stage-3 states) | 1025/12288 | 180 | 90 / 90 | yes, analytic |
| K3: CON × forced RECHECK × ỹ₃ | 5119/12288 | 36 | 18 / 18 | yes, analytic |
| decoder S_I, stages 1–3 | 1/2 per stage | 6 + 72 + 864 = 942 | 471 / 471 | yes (≥ 38) |

How the table entries are derived:
- **Masses:** the split carries exactly 1/2 of each class, because P(ỹ₁ = v, CON | F) = P(y=v)[(1−r)² + (1−r)r/3] + r²/36, and both the odd and even sets carry P(y) mass 1/2 and contain 3 values. With κ₀ > 0, every received state has positive mass under F = 0 as well.
- **Recipient-state counts:** the CON and DIS state counts (12 and 60 in total) were measured by N1 v1 and are halved by the R-split.
- **Exact confirmation:** NEEDS-APPROVED-RUN (N1 v2, reference-only).

### 12.3 Learner-dependent quantities are outcomes, not supports (unchanged)

### 12.4 Reference attainability and contrast (Stage 0)

A reference-only exact enumeration (R-HIST, o^R and o; no learner) must report:
- **(a)** a positive optimal checking rate for RECHECK and for RESAMPLE. **Reading OPEN for Astra (Q-A12):**
  - "on some stage-1 received state", the v1 wording;
  - or "at some decision stage".
  - N2 v1 found the stage-1 reading fails for RECHECK at the v1 world while the some-stage reading holds. N2 v2 reports both readings.
- **(b)** a CON/DIS contrast ≥ μ_contrast for the reference's m_P on R (with R-HIST as the learner, m_P = o^R_P).
- **(c)** the directional signs for R-HIST's self-assessment and checking.
- **(d)** CF1a (fault exposure) at the PROPOSED thresholds.

Astra #30 L164 notes that the analytic reference needs "seconds".

### 12.5 On failure

`DESIGN NOT ADMITTED (support audit)` or `(CF1a)`. The response is a redesign, re-review and re-approval, never a rescue.

## 13. Compiled-control domain and intervention/readout correspondence [F11]

Astra #30 L145: "A compiled implementation of the frozen learner over the declared finite audit domain." Astra #30 L147: "It is an equivalence control, not a presumed negative example of assessment. If it reproduces the role, record an ordinary alternative implementation."

- **Domain:** the 22,620 received states, plus the mapped intervention keys:
  - 72 stage-2 recipient states × (2 content + 4·32 family + 1 same-content = 131);
  - their 12 post-check continuations;
  - the 6 K3 continuations per branch.
  - The table is built for every arm.
- **Equivalence margin:** the PR #10 agreement form (`frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L178–L206) on all tabulated outputs and behavioural statistics, with identical decisions.
- **Decoder statistics:** `NOT EVALUABLE [READOUT UNAVAILABLE IN COMPILED REPRESENTATION]`. Astra #30 L147: "If an assessment readout is unavailable in one representation, report that limitation without treating it as role absence."
- **Interpretation:** equivalence attaches the §2.3 restriction. Non-equivalence is `INVALID [COMPILATION]` and gives UNRESOLVED-COMPUTE. Neither enters K1–K4. Astra #30 E30-7 (L214): "It does not require a faithful compiled implementation to lack or fail the proposed functional role."

## 14. Outcome labels [F12]

The v1 label set is kept (`c4_reliability_exact_check_v1/RESULTS_v3.md`@0e17a05 L40 for UNRESOLVED-DESIGN), with these additions:
- `DESIGN NOT ADMITTED (CF1a: fault exposure below threshold)`;
- `STOPPED AT CF1b: …`;
- `[NOT DISTINGUISHED FROM FIRST-ORDER VALUE OF INFORMATION]`;
- the K-FR "role substantially supplied" sentence;
- `NOT EVALUABLE [NO ASSESSMENT DIRECTION ORTHOGONAL TO FIRST ORDER]`.

NOT EVALUABLE is never a pass. The denominator is always ten.

## 15. Verification coverage, smoke tests, retries and hard caps [F13]

### 15.1 Staged runner

The structure follows `frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L374–L394. Consult #18, as quoted there (L376): "For future studies, use a two-stage runner: write and seal the transformed-path manifest, then evaluate curves from that manifest."

- **Stage 0 (sealed, immutable, corrections only as dated addenda per `results_v1_errata/ERRATA_v1.md`@0329818 L9):**
  - the support audit, CF1a and §12.4;
  - split hashes over received states and the ledger;
  - init hashes, stream digests and family draws;
  - code, spec and fixture hashes.
- **Stage 1:** the 40 training runs, with timing and RSS, then sealed. There is no target evaluation.
- **Stage 2a:** CF1b. **Stage 2b:** CF2. **Stage 2c:** the full evaluation for all arms and the compiled control.
- **Stage 3:** independent replay, then labels.

### 15.2 Dual evaluator (as v1)

- **E1:** torch float64. **E2:** independent NumPy float64 (`frozen_recurrent_compensation_numpy_eval.py`@0fed34e L1–L3).
- PASS, FAIL and BOUNDARY use t = 1e-9. Disagreement is an integrity failure.
- Law masses are computed in exact rationals by E2.

### 15.3 Verification coverage (v1 table, plus these)

- **K-FR freezing:** the core is absent from the optimizer and has requires_grad=False, and its sha256 is unchanged after training (`frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L218–L225).
- **R-VOI:** a fixture check that its 12 post-read p̂ are detached and are computed by the arm's own prediction head.
- **Split disjointness:** checked over received states.
- **R-FO pipeline check:** uses the computed bound of §17.1, not zero.

### 15.4 Smoke tests, retries and hard caps (re-derived for 40 runs; CNA m6)

- **Smoke:** synthetic fixtures only, ≤ 120 s, no fresh seed (`frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L225).
- **Retries:** none.
- **Hard caps:**
  - one CPU process, `torch.set_num_threads(1)`, no GPU;
  - peak RSS ≤ 4 GB;
  - per run ≤ 270 s for CAND, R-FO and K-FR, and ≤ 360 s for R-VOI;
  - Stage 0 ≤ 10 min;
  - **Stage 1 ≤ 190 min**;
  - Stage 2 ≤ 75 min;
  - compiled control ≤ 15 min;
  - Stage 3 ≤ 75 min;
  - **cumulative ≤ 360 CPU-min**.
  - These are about 2.5× the §16 bounds.

## 16. Throughput and evaluation-cost estimates (bounds, with sources) [F13]

Astra #30 L164: "This is an estimate, not an execution budget; bounded throughput and evaluation-cost estimates must appear in the spec."

| # | Quantity | Value | Source label |
| --- | --- | --- | --- |
| T1 | GRU-8 run, 4000 updates at B = 256 | min 13.46 s, max 14.02 s, sum 409.36 s over 30 runs | **MEASURED-RECORD** `frozen_recurrent_compensation_results_v1/stage1/manifest_stage1.json`@22654aa (L29 first); runtime `frozen_recurrent_compensation_results_v1/stage0/manifest_stage0.json`@fd720ee L329–L330 |
| T2 | GRU-8 per update | ≤ 3.505 ms | ANALYTIC from T1 |
| T4 | Effective rate | ≥ 1.87 GFLOP/s | ANALYTIC (derived) |
| T5 | GRU-16 update, B = 64 | ≤ 3 × 3.505 = 10.5 ms (CAND, R-FO, K-FR); ≤ 4 × 3.505 = 14.0 ms (R-VOI, with 12 hypothetical reads batched per decision) | ANALYTIC BOUND (Appendix B) |
| T6 | Per run | ≤ 105 s; R-VOI ≤ 140 s | ANALYTIC BOUND |
| T7 | Stage 1, 40 runs | ≤ 30·105 + 10·140 = 4,550 s ≈ 76 min | ANALYTIC BOUND |
| T8 | Evaluation FLOP per checkpoint per evaluator | ≤ 2.1 GFLOP (R-VOI ≤ 8.4) | ANALYTIC |
| T9 | Evaluation, 50 checkpoints × 2 evaluators | ≤ 80 × 11.2 s + 20 × 45 s ≈ 30 min, assuming ≤ 10× float64 slowdown | ANALYTIC BOUND, slowdown ASSUMED |
| T10 | Target sums on R (CNA m6) | ≤ 1,884 states × 3 actions × 6 next reads × 24 latent ≈ 0.81 M multiply-adds per checkpoint-evaluator, so ≤ 1 s each and ≤ 100 s in total at ≥ 1e6 ops/s (ASSUMED). The learner-free o and o^R are computed once in Stage 0 | ANALYTIC BOUND. Anchor: the exact-rational N2 v1 reference run took 28.1 s wall (**MEASURED-RECORD on the box**, `acq_reference_checks/N2_primary.resources.json`) |
| T11 | Total | ≈ 76 + 30 + 2 + 3 + 30 + 2 ≈ 143 min | ANALYTIC BOUND |
| T12 | Memory | < 1 GB analytic; reference runs peaked at 94 MB (N2 v1, MEASURED-RECORD on the box); no GRU RSS record exists | ANALYTIC + box record |
| T13 | PR #10 evaluation claim | "taking seconds" | PROTOCOL CLAIM (`frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L429) |

## 17. Rivals and the tests that rule each out

### 17.1 R-FO, first-order-only action head (CNA m2 fix; M5)

R-FO is trained as in v1. **v2 pipeline check (m2):**
- Under the battery, R-FO's checking effect is bounded by B_FO = L̂_π·τ_FO, where L̂_π = (1/2)·‖W₂‖₂·‖W₁[:, p̂]‖₂ is computed from the trained action head. That uses tanh′ ≤ 1 and ‖∇_z(π_R + π_S)‖₂ ≤ √2/4 < 1/2.
- `UNRESOLVED-DESIGN [K2 PIPELINE]` is raised only if |D_q^{R-FO}| > B_FO plus the agreement form.
- v1's "zero to the agreement form" would have false-flagged.

R-FO cannot see discordance (M5). v2 therefore relies on R-VOI (§17.4) and K-FR (§9.3) as the strong rivals, and keeps R-FO as a pipeline check and a weak named rival.

### 17.2 Supplied assessment channel

The static input and loss audits, the post-seal decoder fit, the init leg and the K-FR arm (§9.3), and the ledger (§9.4).

### 17.3 Oracle leakage

- (a) m_a is computed from the learner's own decision table on R.
- (b) S_I ∩ S_E = ∅ over received states, checked by hash.
- (c) Decoder features are h only.
- (d) **Permuted-target control (m3):** m_a is permuted across received states **within strata** (stage, cue, read-type pattern) in S_I, using generator 9000+s. If it meets K1, the label is `UNRESOLVED-DESIGN [DECODER LEAKAGE OR DEGENERACY]`.
- (e) **Oracle-target decoders (m4):** decoders fitted to o_a and to **o^R_a** are scored against m_a. If either is within μ1_abs of the m-decoder, K1 is a non-pass ("NOT DISTINGUISHED FROM ORACLE / FAULT-AWARE-BAYES CORRECTNESS").
- (f) Training never reads m, o or o^R.

### 17.4 R-VOI, a first-order value-of-information rival (CNA M4: ADOPTED, with one sub-part REBUTTED)

- **Architecture:** R-VOI's action head reads [p̂, the arm's own predicted post-read p̂ for each of the 12 possible next reads (6 RECHECK, 6 RESAMPLE), N, read type, stage], all detached. It is trained with the identical recipe and seeds, and the full K1–K3 pipeline is run on it.
- **Rebutted sub-part:** CNA suggested weighting the 12 values "by the law". v2 gives them unweighted. Law weights would hand R-VOI world-law knowledge that CAND does not have (ledger §9.4). That would make the rival stronger than any learner without the law, so it would no longer be an information-matched rival. The action head can learn its own weighting.
- **Outcome rule:** if R-VOI meets J in at least 8 of 10 seeds, the §2.3 label is attached.
- **Open question for Astra (Q-A15):** are self-correctness content and anticipated first-order change meant to be separable here?

## 18. Reuse of the GRU-8 lineage

This is the v1 table, which still applies, with these v2 changes:

| Element | Source (file@commit) | v2 use | Where it does not fit |
| --- | --- | --- | --- |
| Harness | `RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md`@d118ae1 L36–L40; `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md`@0b98460 L100–L106 | §4, §8 | GRU-16 with I = 14 and two heads; B = 64; 10,000 updates; BCE + REINFORCE; the W2 world is not reused |
| FO+ISO conjunctive controls | `first_order_control_protocol_FINAL.md`@335e505 L57, L91–L92, L303, L356–L359 | §10.4, §11.3, plus the new SUB family | State-space installation, not a weight path; gated on q only |
| Freezing checks | `frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L218–L225 | evaluation freezing; **K-FR core freezing** | The whole core is frozen in K-FR, not weight_hh only |
| Frozen-at-init idea | `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md`@0b98460 L133 | K-FR arm | Both heads are trained, not one readout |
| 8/10 and >2 invalid | `GRADED_REVERSION_PROTOCOL_FINAL.md`@018f2a7 L285, L287; `frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L302 | §11.5 | Applied to a paired CAND/K-FR seed rule |
| Sealed runner | `frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L374–L394 | §15.1 | CF1a moves to Stage 0 |
| Dual evaluator | `frozen_recurrent_compensation_protocol_FINAL.md`@0fed34e L178–L206; `frozen_recurrent_compensation_eval.py`@0fed34e; `frozen_recurrent_compensation_numpy_eval.py`@0fed34e | §15.2 | New E2 code is needed |

The systems are separate. The PR #9 count (`first_order_control_results_v1/PHASE_B_RESULTS_v2.md`@4f6fc4c L26–L30) is not evidence about this learner.

## 19. W-REL lessons and v1 reference-check lessons applied

1. **No-contrast settings** (`c4_reliability_exact_check_v1/RESULTS_v3.md`@0e17a05 L43; `c4_reliability_exact_check_v1/WREL_CLOSEOUT_E30_v1.md`@37414d0 L67).
   - v1 reintroduced the trap through its target definition (B1). v2's target is on R, and the contrast is checked in Stage 0.
2. **Attainability before freeze** (`c4_reliability_exact_check_v1/WREL_CLOSEOUT_E27_v1.md`@7b89c66 L77).
   - §12.4 and CF1a are Stage 0 gates.
3. **UNRESOLVED-DESIGN** keeps its W-REL meaning (`c4_reliability_exact_check_v1/RESULTS_v3.md`@0e17a05 L40).
4. **Zero support.** Supports are law-defined and the decoder is total. Astra #30 L52: "We should have checked the decoder and repair-state support under compilation before freezing this comparison."
5. **Compiled control.** Astra #30 L50: "That does not establish that the compiled implementation lacks the functional role."
6. **Check the target definition algebraically before computing contrasts.** This is new from N1/N2 v1 and CNA B1.

## 20. Questions for Astra (decided items marked; open items stay open)

- **Q-A1: DECIDED by CNA B1.** m is on the received history R. **Q-A1c (open):** please confirm that "observable history H" means the learner-observable history.
- **Q-A2 (open):** the perturbation locus. CNA m7 adds that an encoding-step perturbation reaches the learner only through its inputs, which reinforces M5. Should it be a hidden-state locus?
- **Q-A3 (open):** the alphabet, emission table and K_max. The costs stay at (1/100, 3/50).
- **Q-A4 (open):** margins (§11.6).
- **Q-A5 (open):** the decoder class.
- **Q-A6 (open):** class-mean or single donors; median or maximum for random-donor.
- **Q-A7 (open):** should R-HIST gate anything?
- **Q-A8 (open):** the learning rule.
- **Q-A9 (open):** the decision-table computation of targets.
- **Q-A10 (open):** the CF2 definition.
- **Q-A11 (open):** init failure inside the 8/10 rule, now paired with K-FR.
- **Q-A12 (open, from N2 v1):** does §12.4(a) mean "stage 1" or "some decision stage"?
- **Q-A13 (open, from N2 v1):** the CF1a threshold δ_div and ν_div, and the fault strength (φ, κ). Neither is changed in v2. The room asked that CF1a first be recomputed on R with the m − o decomposition (N2 v2) before either is changed.
- **Q-A14 (open):** is the C-K0 criterion acceptable (Jeffreys band; the smallest-j rule giving κ₀ = 1/16)? Trade-offs are in §5.2.
- **Q-A15 (open, from CNA M4):** are self-correctness content and anticipated first-order change separable here?
- **Q-A16 (open):** should K-FR pairing be per seed (as drafted) or a count rule?

## 21. Not grounded in the record, and NEEDS-APPROVED-RUN items

**Not grounded** (PROPOSED or ANALYTIC):
- all numeric design values;
- κ₀ = 1/16, chosen by criterion and not from data;
- T4–T11;
- the float64 slowdown and the Python operations rate;
- GRU memory;
- the CPU model of the timed host.

**NEEDS-APPROVED-RUN, reference-only (A-PRE):**
- **N1 v2:** exact supports and split masses on R.
- **N2 v2:** CF1a on R with the decomposition, §12.4(a) under both readings, and the contrast and signs, under the PROPOSED v2 law. A κ₀ = 0 diagnostic was declared in `PRE_RUN_FREEZE_v2.txt` before running, to separate the effect of the target definition from κ₀.
- **N3 (smoke timing):** still deferred.

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

## 23. Change log (v1 → v2)

| ID | Finding | Credited to | Disposition | v2 section(s) |
| --- | --- | --- | --- | --- |
| B1 | Target on H gives zero CON/DIS contrast | CNA review; confirmed exactly by N2 v1 | ADOPTED: m on R | §6, §10.3 |
| B2 | Split on world samples does not separate states | CNA review | ADOPTED: split on R | §7, §12 |
| M1 | K1 passable by history encoding | CNA review | ADOPTED: input baseline; R-FO and K-FR decoder comparators; K1 labelled necessary | §9, §11 |
| M2 | Init control trivial | CNA review | ADOPTED: K-FR arm, paired per seed | §9, §11 |
| M3 | e legs tautological | CNA review | ADOPTED: q legs gate; e legs mechanical; SUB family | §10, §11 |
| M4 | First-order VOI loophole | CNA review | ADOPTED: R-VOI rival and gating post-check battery for strong wording. REBUTTED sub-part: law-weighted inputs (information matching) | §17, §11, §2 |
| M5 | Perfect fault detector; weak R-FO | CNA review | ADOPTED: κ₀ = 1/16 by C-K0; disclosure; R-VOI and K-FR as strong rivals | §5, §2, §12, §17 |
| m1 | CF1a passes via suboptimality | CNA review | ADOPTED: decomposition; CF1a on Δ^F in Stage 0; CF1b on λ | §1 |
| m2 | R-FO "exactly zero" false flag | CNA review | ADOPTED: computed Lipschitz bound | §17 |
| m3 | Permutation strata | CNA review | ADOPTED | §17 |
| m4 | o^R-target decoder | CNA review | ADOPTED | §17 |
| m5 | Supports in states | CNA review and N1 v1 (12/60 distinct recipient states) | ADOPTED | §12 |
| m6 | Caps for 40 runs; T10 bound | CNA review | ADOPTED | §15, §16 |
| m7 | Q-A2 still open | CNA review | Kept OPEN | §20 |
| E1 | §6.3 weight 4^−(k−1) does not normalize | **N1 v1** (not identified in the CNA review) | ADOPTED: 2^−(k−1) | §6 |
| E2 | Appendix A "never checks" is false under an adaptive policy | **N2 v1** (the CNA review checked the Appendix A numbers only) | ADOPTED: corrected | Appendix A |
| E3 | §12.4(a) fails at stage 1 for RECHECK, holds at later stages | N2 v1 | Kept OPEN (Q-A12) | §12, §20 |
| E4 | CF1a ≈ 0.015 under v1 | N2 v1 | Recomputed on R with decomposition in N2 v2; threshold and fault strength OPEN (Q-A13) | §1, §20 |

## Appendix A. Binary-read world (corrected per N2 v1)

**Setting and arithmetic** (as v1; all confirmed exactly by N2 v1):
- p_lo = 17/20, p_hi = 27/40.
- **Lemma:** for two exchangeable binary received reads with a symmetric posterior on disagreement, accuracy after two reads = p. So a single extra read adds zero accuracy, for both RECHECK and RESAMPLE.
- Two RECHECKs (majority of three copies): 139/160 = 0.86875 (lo) and 219/320 = 0.684375 (hi). Non-adaptive gains of 3/160 and 3/320 are both below 2c_R = 0.02.

**Correction.** v1 said the reference never checks. **That is false.** Under an adaptive policy (re-read again only after a disagreement), the exact stage-1 value of RECHECK at the low-noise cue is Q_R = 549/640 > 17/20 = Q_P. So RECHECK is optimal there (N2 v1: optimal at 18 binary decision-stage histories).

The binary world remains rejected on a narrower ground: the single-read lemma removes all myopic value of one extra read. The graded world does not have this symmetry.

## Appendix B. FLOP and op-count arithmetic (ANALYTIC)

- **CAND, R-FO, K-FR:** as v1. Training ≈ 66,888 FLOP per episode (×64 = 4.28 MFLOP per update), and the op-group ratio is 2.4, so r ≤ 3.
- **R-VOI:** at each of ≤ 3 decisions, 12 hypothetical next reads are run as one batched GRU step plus a prediction head, forward only and detached.
  - Extra FLOP: 36 × (3,200 + 1,122) ≈ 155.6 k per episode, so ≈ 222.5 k per episode in total, and ×64 = 14.2 MFLOP per update (FLOP ratio 2.17).
  - Extra op groups: 3 × (1 cell + 2 linear) = 9, so 33 in total (ratio 3.3).
  - r ≤ 4.
- **Evaluation:** tabulation ≤ 0.51 GFLOP. Interventions: 72 × 131 × ≤ 30 one-step forwards × 5,574 ≈ 1.58 GFLOP. So ≤ 2.1 GFLOP per checkpoint-evaluator, and R-VOI ≤ 4×.

End of draft v2.
