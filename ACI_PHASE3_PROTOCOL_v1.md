# ACI Phase-III protocol v1 — the frozen protocol for T3 (N2: recurrent cross-module availability of a maintained representation)

2026-09-27. Deliverable for the G10 card (t_ae28135a): *does the frozen protocol (v1)
incorporate G1–G9, with primary gates H1–H5 and a claim ceiling?* This is the **synthesis
and freeze** of the nine G-series design documents; it does **not** run, train, or execute
anything, and it edits no frozen artifact (runner, protocol, results dir, hash, or ledger).
It is not hashed into any study's `pre_run_snapshot.json`. It is the document G11 reads to
implement the candidate and rivals; nothing here is to be read as a result.

This is a **runnable protocol** — unlike `ACI_BRIDGE_PROTOCOL_v4.md`, it is not a STOP.
G9's reduction audit returned **no unidentifiability**: the central concept is identifiable,
every reduction rival R1–R5 removes exactly one organizational property, and a simple rival
winning is an admissible (even likely) Phase-III result. The binding obligations G9 handed
this card are frozen in §12 and load-bearing inside H1–H5.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): nothing here is, or is meant as, a consciousness claim.
(2) Seeds are the replication unit; every comparison is a planned-denominator readout
reported per seed family, never a per-family guarantee (AC39/AC68). (3) No gate may be
added or moved after finals begin (the card's own bar; AC16/17 discipline). (4) Each rival
is the candidate's own mechanism with exactly one property removed, and its parameter
family is swept alongside the candidate's own (P6, AC11/AC116). (5) The G0 demotions bind
everywhere: V is absent from all six arms, A is a fixed/reactive rule (verdict D), and
S_reg is a readout that does **not** gate π.

---

## 0. Verdict (read this first)

**FROZEN — runnable.** This protocol freezes the Phase-III experiment: the Shared Latent
Workspace candidate (SLW) plus five reduction rivals (R1–R5) on the G2 hidden-state
inference task, three objective-distinct specialists (G3), five causal interventions
(I1–I5, G5) plus the persistence cut (G2 §3.2) and the four leakage ablations (G8), the
coordination condition (G6), the novel-consumer test (G7), and the leakage audit (G8) —
with five primary gates H1–H5 and a claim ceiling, all fixed before any engineering seed
is scored.

The central claim under test is the five-predicate conjunction **H_share** (G1 §3): one
maintained representation W is **SHARED** (one storage location, one write point, one
refresh target read by all consumers), **CAUSAL** (intervening on W changes each consumer),
**FUNCTIONALLY DISTINCT** (three non-collapsing invariance classes), **AVAILABLE** (W is a
sufficient summary; consumers do not re-read the history), and **MAINTAINED** (persistence
is paid through π, not free recurrence). Phase III's claim is the existential: there is a
maintained W such that H_share(W; S_pol, S_plan, S_reg) holds — N2 at the stated degree.

---

## 1. The central question and the five primary gates

**Central question (N2, from `ACI_MASTER_RESEARCH_TREE_v2.md` §5).** Does one maintained
representation's content get shared — read by at least two objective-distinct downstream
modules that need different information and drive different behaviour — such that changing
the content changes them *differently*, and such that the organizational properties of
sharing (one burden of persistence, one point of update, structural coordination, reuse by
a new consumer) are each causally load-bearing against a rival that removes exactly one?

The five primary gates are the falsification structure. A gate is **passed** only if the
stated contrast resolves in the candidate's favour under the frozen gate shape; a gate is
**failed** (falsification) if the rival wins on the predicate it removes; a gate that is a
scope/consistency check is labelled as such and does **not** by itself carry a claim.

| Gate | Claim | Primary contrasts (load-bearing sub-tests) | Owned by |
| --- | --- | --- | --- |
| **H1** | Maintained hidden-state content: W predicts the latent cause above rivals exactly where the current observation is insufficient | probe accuracy vs the memoryless bound; Bayes-ceiling equivalence; π-cut decay; F1 free-recurrence | G2, G8 |
| **H2** | Multiple causal consumers: W interventions causally alter ≥2 specialist outputs in prespecified *different* directions | I1 differential-scramble signature; I2 per-consumer W-cut; G3 invariance classes | G3, G5 |
| **H3** | Same-content dependence: effects are attributable to the same W content, not private copies or hidden pathways | I3 consumer-cut byte-identity; I4 private-copy divergence; I5 coherent-error; G8 no-L audit | G5, G8 |
| **H4** | Organizational value of sharing (CRITICAL): the shared architecture gives a prespecified advantage in coordination/reuse/efficiency/transfer over the strongest non-shared rivals | COORD incoherence rate; G7 sample efficiency; single-write identity; maintenance economy | G6, G7 |
| **H5** | Novel-consumer reuse: frozen W is reusable content for a new consumer without retraining the inference | G7 frozen-core completeness; zero-retraining; R4 ceiling equivalence; interference | G7 |

Full gate definitions with endpoints and gate shapes are §9. **H5 is treated separately**
(§9.5): it is frozen here and run, but its power/sample demands are separable from H1–H4,
and a failure of H5 does not falsify H1–H4 (they are independent conjuncts; H5 is the
*reuse* face of the claim, not its foundation).

---

## 2. The freeze (the fourteen frozen elements, stated once)

This is the operative freeze. Where a G-document derived the value, the derivation is cited
and not re-run; where G10 was deferred a decision (training objectives, seeds, the
statistical plan), the decision is made here and is frozen.

1. **Environment.** `.venv-bridge` in the repo root (Python 3.12.3, torch 2.14.0, numpy
   2.5.3 — the bridge harness environment, G11's instruction). All RNGs seeded (torch
   `manual_seed`, numpy `default_rng`, the episode/decoder streams) with the model seed
   (§11); no GPU nondeterminism (CUDA determinism flags on, or CPU-only). A run is
   deterministic given its model seed.

2. **Latent-state process.** z ∈ {A, B}, one draw per episode, uniform (π_A = π_B = ½),
   fixed for the episode, never emitted as an observation (G2 §1.1). z is a training-only
   scaffold; at evaluation the only signal is the token stream and the decision reward.

3. **Observation model.** Token stream x_1..x_H from a 5-symbol alphabet Ω = {t1..t5},
   conditionally i.i.d. given z, with mirror distributions and log-likelihood ratios
   λ = {+2.00, +0.35, 0, −0.35, −2.00} (G2 §1.2 table). Steps 1..(H−K) are the
   accumulation phase (informative); steps (H−K+1)..H are the **probe window**, where every
   token is the neutral t3 (P(x|A) = P(x|B) exactly). Defaults H = 32, K = 8 (24
   informative steps). The probe is the load-bearing regime for H1/H3 (x_t is z-blind there,
   so W is the only carrier of z).

4. **W representation.** W is the scalar log-likelihood ratio S_H = Σ λ(x_i) quantized to
   **b = 5 bits** (range [−6, +6], resolution ≈ 0.39 < λ_lo = 0.35), swept as a level
   family; the rivals R4/R5 hold the same scalar at the same b bits (G2 §4.2). W is the
   minimal sufficient statistic (G2 §2.1); enriching it beyond b bits is prohibited (D2/P5).
   The Bayes-optimal decision is ẑ = A iff S_H > 0; Bayes ceiling at 24 informative steps is
   **0.812**; the memoryless bound is **0.606** clean / **0.500** probe (G2 §2.3).

5. **Persistence mechanism.** W's content is set by the encoder's acquisition/update write
   each step (correctness rides this write, D3); W's persistence between writes is **paid**
   through π (the N1 substrate), which re-energizes W against decay at rate δ for cost c per
   step, drawn from the shared budget (G0 §3.6, G1 §2.5). The maintenance rule A is
   **fixed/reactive** on the raw bookkeeping (s, E, d) — a threshold rule, never a learned
   allocator (verdict D). The F1 discipline binds: the no-maintenance control runs the
   recurrence **with W zeroed**, not a no-recurrence policy (N12 F1, G0 §3.7). Candidate and
   R1 carry π; R2/R3/R4/R5 have no π (their defining property, G4 §8 rule 5).

6. **Specialist objectives.** Three specialists, each learned against its own objective
   kind, with its analytic optimum kept as a co-equal fixed rival (G3 §6 gate 3):
   - **S_pol** (W, x_t) → ẑ ∈ {A, B}: external accuracy r = +1 iff ẑ = z; function of W is
     the sign (odd). Analytic optimum: the sign rule at 0.
   - **S_plan** (W, cost) → {commit-A, commit-B, postpone}: speed-accuracy-cost
     (R_correct, R_wrong, c_obs); function of W is a two-sided threshold (SPRT, commit iff
     |W| crosses a/b). Analytic optimum: the Wald SPRT, boundaries derived from the cost
     model before training, swept.
   - **S_reg** (W, E, d, s) → {preserve, release}: continued-operation/resource economy;
     function of W is the even value-of-information gate (preserve iff |W| ≥ θ(E,d,s)).
     Analytic optimum: the even threshold, θ swept in [θ_lo, a]. S_reg is a **readout**, not
     a maintenance controller; its output does not gate π (G3 §8, verdict D).
   The **encoder** f_enc (recurrent GRU, per G0 §3.7) is learned to map (W_{t-1}, x_t) → W_t,
   trained toward the quantized S_H with z as the training-only label (supervised /
   cross-entropy; G2 §1.1). The analytic scalar accumulator (G2 §2.1) is kept as R4.

7. **Architectures.** The six arms of G4: **CANDIDATE (SLW)** and rivals **R1** (private
   state, removes SHARING), **R4** (sufficient-statistic broadcast, removes learned content +
   paid persistence), **R5** (separate copies, removes the sharing mechanism), **R2**
   (monolithic RNN, removes modularity), **R3** (history access, removes the compressed
   maintained W). Full topologies and the five-rule comparability contract are G4 §2–§8 and
   are incorporated here by reference, not re-derived.

8. **Parameter budgets.** Frozen defaults, swept as level families (G2 §6, G3 §7, G4 §11,
   G6 §8, G7 §8): n = 3 specialists (minimal pair n = 2 as a variant); b = 5 bits (swept);
   H = 32, K = 8 (swept); λ = {+2.00, +0.35, 0, −0.35, −2.00} with the strong:weak ratio
   swept; total trainable parameter budget **P ∈ {small, mid, large}**, equal across arms,
   with R1/R5 splitting P per copy (robustness variant: R1/R5 at n·P); R2 hidden dim d_h
   swept ≥ b bits; R3 window M swept ≥ H; S_plan thresholds a = b (symmetric) swept with the
   cost model; S_reg θ swept in [θ_lo, a], **never above a** (the binding ordering θ ≤ a,
   G6 §2.3); refresh cost c and decay δ computed at implementation (G0 §3.6); contradiction
   penalty C_contradiction = 0 (endpoint measured, not scored, G6 §4); S_conf scoring
   {log loss, Brier}, S_bias cost ratio c_AB : c_BA = 3 : 1 swept; new-head capacity
   logistic/threshold (or one hidden layer ≤ 64, recorded).

9. **Rivals.** R1–R5 as in G4, each swept alongside the candidate's own hyperparameters,
   never fixed while selecting another's best member (AC11's fatal error). R4 and R3 are
   **advantaged** on information (optimal content / full history), R2 is advantaged on
   capacity and cost; no arm is ever given less than the candidate (G4 §8 rule 4). Each
   specialist's analytic optimum is itself a co-equal rival (G3 §6 gate 3).

10. **Interventions.** The five canonical causal interventions of G5 (I1 W-scramble, I2
    W-cut, I3 consumer-cut, I4 private-copy substitution, I5 stale/incorrect W), plus the
    **π-cut** (the persistence intervention of G2 §3.2, inherited unchanged — the label
    "I1" for cut-π from Q4/G0–G4 is superseded; see §5's reconciliation), and the four
    leakage ablations of G8 §4 (sever, W-cut-as-leak-detector, decode-ablation,
    free-recurrence). Every intervention cuts exactly one link and is paired with its
    uninterrupted control on the same seed (byte-identity license, P7).

11. **Metrics.** Planned-denominator readouts, per seed, per consumer, never pooled:
    probe/clean accuracy (H1); the w★ ↦ triple differential signature and its match error
    (H2); the byte-identity flags and the i-vs-j divergence (H3); the incoherence rate
    R_inc and the coherent-correct-plan rate (H4); the learning-curve cost, frozen-core
    score, information required, and interference flag (H5); plus the G8 decode rates with
    the three anchors (chance 0.500 / memoryless 0.606 / W ceiling 0.812) and the I/D/L
    leak grades. Chronological scalars (first divergence tick, first incoherence tick,
    first leak tick) recorded where they carry the mechanism.

12. **Statistical plan.** §10: the replication unit is the model seed; N = 12 final model
    seeds; the exact sign-flip on paired per-seed differences (floor 2/2^N, never p = 0);
    effect sizes with exact binomial (Clopper–Pearson) CIs; per-gate α = 0.01, family-wise
    α = 0.05 over H1–H4; categorical claims gate on per-individual dominance, equivalence
    claims on byte-identity.

13. **Engineering / final seeds.** §11: engineering model seeds 0–7 (8 seeds), final model
    seeds 100–111 (12 seeds), disjoint; decoder train on engineering 0–7, evaluate on finals
    100–111 (never reverse). Engineering seeds are excluded from every final sample and may
    inform which endpoints discriminate, disclosed in the results doc.

14. **Claim ceiling.** §13: a full pass earns, at most, "one maintained representation's
    content is available to two-or-more objective-distinct modules that need different
    information and drive different behaviour — N2 at the stated degree." Nothing stronger:
    no global broadcast, no workspace seat (O3/GWT), no metacognition (N4), no autopoiesis,
    no consciousness, no level-(d)/(e) claim.

---

## 3. The six arms (G4, incorporated)

| Arm | Topology (one line) | Removes | The claim it isolates |
| --- | --- | --- | --- |
| **CANDIDATE (SLW)** | encoder → maintained W (paid π) → 3 specialists read W | — | SHARED ∧ CAUSAL ∧ DISTINCT ∧ AVAILABLE ∧ MAINTAINED, learned content |
| **R1** private-state | 3 encoders → 3 private W_i (paid π_i) → specialist i reads W_i | SHARING | does sharing beat solving the same inference three times? |
| **R4** suff-stat broadcast | fixed scalar S_t (free register) → 3 specialists read S_t | learned content + paid persistence | shared *sufficient content*, not learned/paid inference? |
| **R5** separate copies | fixed scalar S_t, 3 free copies → specialist i reads copy i | the sharing mechanism | does the sharing *mechanism* matter, or only equivalent content? |
| **R2** monolithic RNN | one RNN h_t → 3 heads read h_t jointly | modularity (+ W, + π) | is modularity necessary, or just interpretable? |
| **R3** history-access | full history x_1..x_t → 3 specialists read it directly | the compressed maintained W | does W provide a compression advantage? |

The five-rule comparability contract (G4 §8) is frozen verbatim: same task/token
stream/seeds for every arm; no z to any specialist in any arm; capacity matched by total
parameter budget P swept as a level family (R1/R5 split P per copy, with the n·P robustness
variant); information asymmetries always in the rival's favour and disclosed (R4/R5 get λ,
R3/R2 get the history, the candidate gets neither); no V and no pristine copy in any arm.

---

## 4. The three specialists (G3, incorporated)

The three consumers and their invariance classes (G3 §2, §4), which guarantee non-collapse
by construction:

| Specialist | Function of W | Invariance class | Output space |
| --- | --- | --- | --- |
| S_pol | ẑ = A iff W > 0 | **odd** (sign-equivariant) | {A, B} |
| S_plan | commit-A iff W ≥ +a; commit-B iff W ≤ −b; else postpone | **sign-and-magnitude** | {commit-A, commit-B, postpone} |
| S_reg | preserve iff \|W\| ≥ θ(E,d,s) | **even** (sign-invariant) | {preserve, release} |

The two canonical perturbations (sign flip W → −W, magnitude shrink W → W/2) must change
the three specialists in three pairwise-distinct ways (G3 §3.2): S_pol flips on sign only,
S_plan responds to both, S_reg responds to magnitude only. The two-linear-heads rival
(single-objective collapse) fails the differential-scramble test outright. S_conf and S_bias
(G7) add a fourth invariance class and a shifted-threshold decision respectively; both are
attached in every arm.

---

## 5. The interventions (label reconciliation, then the freeze)

G5 §1 renumbered the intervention space and is binding. The mapping, to prevent the
AC14-class arm-name error:

| Canonical (G5) | What it is | Predicate served |
| --- | --- | --- |
| **I1** W-scramble | overwrite W with w★, hold all else fixed | CAUSAL + FUNCTIONALLY_DISTINCT |
| **I2** W-cut | remove W from one consumer at a time | CAUSAL per consumer |
| **I3** consumer-cut | disable one consumer, leave W + others | SHARED (W independent of any consumer) |
| **I4** private-copy substitution | swap W for one consumer with a frozen private copy | SHARED (identity vs value) |
| **I5** stale/incorrect W | inject a controlled error into W | CAUSAL as a content-vehicle |

The persistence intervention — **cut π's refresh of W** (G2 §3.2, G1 §2.5) — is **not** one
of the five; it is the **π-cut (I_π)**, inherited unchanged from G2, and it is the
MAINTAINED test. It is distinct from I1 (W-scramble): I1 leaves π running and overwrites
content; I_π cuts the paid refresh and measures decay. Nothing here re-specifies or weakens
I_π. The four leakage ablations (G8 §4) — sever, W-cut-as-leak-detector, decode-ablation,
free-recurrence (F1) — are the instrument G8 uses; they are listed here as frozen and
bound to the same surgical discipline (cut one link, byte-identity at the intact boundary).

The central quality bar over all five (G5 §9) is frozen: **the observed signature must equal
the signature W's content predicts** — an exact function of the injected value, not a
non-zero change. A correlated movement that does not trace the predicted function of W is a
falsification, not a pass.

---

## 6. Coordination (G6, incorporated)

**COORD — joint-realizability.** At every tick, the triple (S_pol, S_plan, S_reg) must lie on
the shared-content manifold M = { (S_pol(w), S_plan(w), S_reg(w)) : w scalar }, a 1-D curve
of six realizable triples inside the 12-triple product (symmetric default, θ < a). The six
off-curve triples decompose into four sign contradictions and two magnitude contradictions
(G6 §2.2). The binding design constraint is **θ ≤ a** for every feasible (E, d, s), so
"commit ⇒ preserve" is invariant (G6 §2.3); θ is swept in [θ_lo, a], never above a.

Per-arm expectation (G6 §5), frozen as a **prediction to verify, not a gate on R2/R3**:
candidate, R4, R5 = 0 incoherence by construction; R1 = measured > 0; R2/R3 = empirical
(training outcome, no structural guarantee). The clean load-bearing separation is
**candidate vs R1**. Per G9's binding handoff (§12), COORD must **not** be promoted to a
candidate-vs-R2 fact: it is candidate-vs-R1, and the modularity contrast with R2 lives in
the interventions and the π-cut, not in COORD.

---

## 7. The novel-consumer test (G7, incorporated)

Freeze the encoder, W's acquisition write, and the three original specialists after training;
leave π + A running (candidate/R1); attach two new read-only heads — **S_conf** (the
calibrated posterior P̂ = σ(W), the fourth invariance class, needing the full b-bit magnitude)
and **S_bias** (the asymmetric-cost decision ẑ = A iff W > θ_bias) — trained only on their own
objectives with no gradient into the frozen core. The four measures (G7 §4): sample
efficiency (retraining cost + readout cost), frozen-core performance (ceiling), information
required (b bits vs M tokens vs d_h), and interference (old consumers byte-identical). The
R1 wiring question is resolved by three disclosed sub-arms: R1-concat (3 W_i), R1-piggyback
(one W_i), R1-retrain (fourth encoder). Freezing is symmetric across arms (G7 §6).

---

## 8. The leakage audit (G8, incorporated)

The seven pathways L1–L7 (GRU hidden state, specialist private state, maintenance variables,
trainer signals, timing, action history, cached observations) each get exactly one of three
grades per arm: INERT (chance in the probe), DISCLOSED (carries z, declared advantage),
LEAK (carries z, free, reaches a specialist or persists without π). The candidate's claim
fails iff any pathway P ≠ W is LEAK-grade on any seed. The three falsification conditions
(G8 §1.3): availability leak (sever changes an output), free-persistence leak (F1: h_t
retains z under π-cut), weight/trainer leak (I2-scramble leaves an output above chance). The
rival arms are audited to **quantify** their disclosed pathways (R3's history decodes ≥ the
W ceiling; R1's three W_i decode ≈ W; R2's h_t ≈ W; R4/R5's S_t at the ceiling), never to
condemn them. The decoder is a supplied instrument (capacity-capped, disjoint seed family,
never back-propagated through arm weights) — labelled, never counted as autonomous (G8 §2.1).

---

## 9. The five primary gates (frozen; none added or moved after finals begin)

Gate shape matches claim shape throughout (AC16/17): categorical claims gate on
per-individual dominance or a threshold met by every seed, never a mean margin; equivalence
claims gate on exact/byte equality, never "similar"; a rival that can reach the ceiling is
gated by equivalence-on-the-ceiling plus separation on the organizational endpoint, never a
strict `>` on the ceiling. Each gate states its endpoint, test, and the falsification it
would record.

### 9.1 H1 — maintained hidden-state content

**Claim.** The candidate's W is a paid-maintained sufficient statistic of z that predicts z
above the memoryless rival exactly where the current observation is insufficient (the probe).

**Endpoints (probe is load-bearing; accumulation is the companion).**
- H1.1 — **Probe discrimination above the memoryless bound.** The candidate's probe accuracy
  reaches the Bayes ceiling 0.812 (to the quantization floor), above the memoryless bound
  0.500, on **every** final seed. Falsified by a candidate that sits at the memoryless bound.
- H1.2 — **Ceiling equivalence with R4 (the rival that must not be beaten).** The candidate's
  accuracy equals R4's on every seed to the quantization floor — an equivalence gate, never
  `>` (R4's S_t *is* S_H). A candidate that exceeds R4 is a wiring bug (it read more than
  b-bit W); a shortfall is an incompleteness finding.
- H1.3 — **Paid persistence (the π-cut, I_π).** Cutting π (holding W's value and the sensors
  fixed) decays W on timescale 1/δ and decays probe accuracy toward the memoryless bound.
  This pins MAINTAINED (G2 §3.2, G1 §2.5).
- H1.4 — **Free-recurrence (F1).** With π cut and the recurrence run **with W zeroed** (not a
  no-recurrence policy), decode z from h_t at the probe ≤ 0.500 + ε on every seed. A h_t that
  retains z is a free hidden memory and falsifies MAINTAINED (G8 §4.4, N12 F1).

**Rival that must fail.** The memoryless / bounded-window rival at chance (0.500) in the
probe; the finite-state / direct-control rival identically. R4 is the *ceiling* rival
(matched, not beaten), not the thing to fail.

### 9.2 H2 — multiple causal consumers

**Claim.** Interventions on W causally alter ≥2 specialist outputs in prespecified,
*functionally different* directions.

**Endpoints.**
- H2.1 — **Differential-scramble signature (I1).** Sweep w★ ∈ [−6, +6]; the measured triple
  must equal (S_pol(w★), S_plan(w★), S_reg(w★)) up to the finite-sample resolution, on every
  seed — the sign-equivariance, two-sided threshold, and even magnitude-gate traced exactly.
  A flat (co-varying) response is the two-linear-heads rival and a falsification (G3 §1).
- H2.2 — **Per-consumer causal independence (I2).** For each of the three sub-arms, the cut
  consumer reaches its exact no-W baseline (chance / abstain / release) and the two survivors
  are byte-identical to the intact run, on every seed. Gated per consumer, not pooled.
- H2.3 — **Invariance classes (anti-collapse).** On the finals family, the sign-flip and
  magnitude-shrink response matrix of G3 §3.2 holds: S_pol sign-equivariant and
  magnitude-invariant; S_plan responds to both; S_reg sign-invariant and magnitude-sensitive.
  Any co-variance (e.g. S_reg co-varying with S_pol on sign flips) falsifies the design.

### 9.3 H3 — same-content dependence

**Claim.** The causal effects are attributable to the same W content — not private copies,
not hidden pathways, not W's mere presence.

**Endpoints.**
- H3.1 — **Consumer-independence of W (I3).** For each sub-arm, W's trajectory and the
  surviving outputs are byte-identical to the intact run. Any drift falsifies SHARED (W would
  be a consumer's private state).
- H3.2 — **Literal-shared-state (I4, load-bearing per G9).** For each sub-arm, the privatized
  consumer's output equals S_i(frozen copy) exactly, and the i-vs-j divergence equals the
  evidence accumulated since substitution (measured in the accumulation phase, where W keeps
  moving). This is the behavioral discriminator that separates the candidate from R5
  (same content, no shared identity).
- H3.3 — **Coherent-error propagation (I5, load-bearing per G9).** For each error model
  (wrong-sign, stale), the measured triple equals (S_pol(w), S_plan(w), S_reg(w)) for the
  injected w, on every seed — mutually consistent with one (wrong) belief. An inconsistent
  triple means the specialists read different content, and H_share fails. The
  shared-vs-unshared contrast (candidate/R4 global error vs R1/R5 local error) is a recorded
  prediction, reported not gated where gate 1 of G5 §10 already pins the single-write fact.
- H3.4 — **No hidden pathway (G8 no-L audit).** In the candidate, every pathway except L1 is
  INERT in the probe (decode ≤ 0.500 + ε per seed); L1 (the encoder hidden state) is
  DISCLOSED acquisition machinery held to the sever-byte-identity and F1 constraints. A
  single L-grade pathway falsifies. The single-write-reaches-all check (G5 §10 gate 1) is the
  source-level SHARED assertion: one write changes all three consumers in the candidate,
  three writes are required in R1/R5.

### 9.4 H4 — organizational value of sharing (CRITICAL)

**Claim.** The shared architecture provides a prespecified advantage in coordination,
reuse, efficiency, and transfer over the strongest non-shared rivals — the candidate is not
merely three correct modules that happen to agree; its shared structure does work the
non-shared rivals cannot.

**Endpoints.**
- H4.1 — **Coordination (COORD, G6).** On the finals family, the candidate's incoherence
  rate is **exactly 0** at every tick (no sign contradiction, no magnitude contradiction; the
  ordering θ ≤ a verified in the same pass). R1's incoherence rate is **> 0 on at least one
  seed** (per-seed distribution reported; a gate of "R1 = 0" would be a wiring bug, a gate of
  "R1 > 0 on every seed" an over-claim). This is the load-bearing candidate-vs-R1 contrast.
  R4/R5 are 0 by construction (asserted); R2/R3 report their empirical rate with no structural
  guarantee (a modularity fact, not a gated candidate win).
- H4.2 — **Reuse sample efficiency (G7).** The candidate serves S_conf/S_bias with **exactly 0**
  inference-retraining samples (encoder frozen, byte-identity of W's trajectory across the
  Phase-1/Phase-2 boundary); R1-retrain's full retraining cost is measured and reported. The
  contrast is categorical (0 vs measured > 0).
- H4.3 — **Single-write identity at n = 4.** One write to the candidate's W changes S_pol,
  S_plan, S_reg **and** S_conf (and S_bias); reaching the same consumers in R1-piggyback and
  R5 requires a write per copy. Categorical, on every seed.
- H4.4 — **Maintenance economy.** The candidate carries one refresh target (one π, one A);
  R1 carries three (three π_i). Reported as the economic form of the sharing advantage; the
  per-action economics are recorded, not gated as a hypothesis test.

**Rivals that must fail.** R1 (the strongest non-shared rival, on H4.1–H4.4) and R3 (the
information-ceiling rival, on the compression half: b bits vs M tokens at matched accuracy).
R4 and R5 are expected to tie on several of these (R4 coordinates for free, R5 ties on
content); their separations live on the maintained/learned endpoints (H1.3/H1.4) and the
identity endpoints (H3.2/H3.3), not on H4.1 — this is G9's Q4/Q5 correction, frozen.

### 9.5 H5 — novel-consumer reuse (treated separately)

**Claim.** The frozen maintained W is reusable content for a new consumer (S_conf, S_bias)
without retraining the inference — not merely ordinary representation transfer.

**Endpoints (G7 §7 gates, run and gated separately from H1–H4).**
- H5.1 — **Frozen-core completeness.** S_conf reaches the Bayes-calibrated ceiling (log loss
  = posterior entropy) to the quantization floor, and S_bias reaches the asymmetric-cost
  optimum, on **every** seed, reading W alone.
- H5.2 — **Ceiling equivalence with R4.** The candidate's S_conf/S_bias scores equal R4's on
  every seed to the quantization floor (equivalence, never `>`; R4 is the ceiling). R3 may
  exceed (full history) and is reported, not gated as a failure.
- H5.3 — **Information required (AVAILABLE extends).** S_conf/S_bias read b bits and nothing
  else; sever-history leaves them byte-unchanged.
- H5.4 — **Modular extension (interference).** After Phase 2, the three original specialists'
  outputs are byte-identical to the Phase-1 run, on every seed. R2's joint-retrain sub-arm
  reports its measured interference as its reduction, not a gated candidate claim.
- H5.5 — **Non-collapse with a fourth class.** S_conf responds as a strict monotone readout
  and S_bias as a shifted-threshold decision; neither co-varies identically with any existing
  specialist.

**Scope.** H5 is the *reuse* face of N2 and is frozen and run, but it is **separate**: its
sample/power demands do not draw on the H1–H4 family budget, and a negative H5 (e.g. R2's
probe reaching the ceiling) is an admissible reduction finding that does not falsify
H1–H4. The new consumers are experimenter-supplied (G7 §6.7): H5 establishes reusability of
the content, never that the organism *acquires* consumers.

### 9.6 Consistency checks (Tier-0/1 — must pass for the run to be valid, not claim-bearing)

These are mechanical assertions, not hypothesis gates; a failure is a setup/wiring defect
to fix, not a falsification to report (AC85). They are frozen and may not be dropped:
byte-identity at every intact boundary (P7, AC83's method); the θ ≤ a ordering across the
sweep; the manifold geometry (exactly six realizable triples, four sign + two magnitude
contradictions); the single-write test; the sever-history test per consumer; the decode-
ablation sanity (zeroing P drops the decoder to chance); the statelessness of the candidate's
specialists (no recurrent carry, no output-recurrence); A's z-blindness (A reads (s,E,d)
only, never W); z absent from every forward graph at eval.

---

## 10. Statistical plan (frozen)

1. **Replication unit.** The **model seed** — one independent draw of the training RNG
   (weight init, curriculum order) and the evaluation-episode stream. N = 12 final model
   seeds. This is the Phase-III resolution of the G5/G8 "episode seed" language: the episode
   is a *repeated measure* within a model seed (one draw of z and its token stream), and
   "N model seeds × balanced-A/B episodes = N units, not 2N or N×episodes" (the AC88 lesson,
   applied from the outset). Every arm runs on the **same** model seeds, so arm comparisons
   are paired.
2. **Test.** The exact sign-flip on paired per-seed differences (ties excluded), as
   implemented in this repo (`_ac116_signflip.py`, AC38/AC46):
   `p = |{σ ∈ {±1}^n : |Σ σ_i·diffs_i| ≥ |Σ diffs_i|}| / 2^n`. It is exact, assumption-free,
   and its p-support is a discrete subset of {2/2^n, 4/2^n, …} — **never 0**.
3. **Resolution floor.** 2/2^n: at n = 12, the floor is **0.00049**.
4. **α and error control.** Per-gate two-sided α = 0.01; family-wise α = 0.05 over the
   hypothesis-test gates of H1–H4 (H1.1, H1.3, H2.1, H4.1, H4.2). The equivalence and
   byte-identity checks (H1.2, H3.1–H3.4, H5.x) and the consistency checks (§9.6) are not
   hypothesis tests and draw no family budget.
5. **Effect sizes are primary.** Every gate reports the mean/median paired difference and
   the fraction of seeds with a positive difference, the latter with an exact binomial
   (Clopper–Pearson) 95% CI. A result at the floor but below α is an effect size, never a
   pass. Ties are excluded and N_eff = N − ties is stated.
6. **N re-derivation rule.** The sign-flip assumes nothing about effect magnitude, but the
   paired criterion does (AC38): report σ_difference (sd of paired differences across
   engineering seeds, measured on a range the finals do not score on) and require
   |mean paired difference| / σ_difference ≥ 3 on data the study does not then judge. If
   engineering σ_difference is larger than the minimum meaningful effect assumes, N is
   recomputed **before freezing finals**, and every engineering seed used to measure it is
   excluded from the final sample (AC39). The constants (α, the minimum-effect definition,
   the floor) are frozen; only N may be re-derived, and never after finals begin.
7. **Decoder seed discipline (G8 §2.4).** The leakage decoder trains on engineering
   0–7 and evaluates on finals 100–111, never the reverse; its label is z, which never
   enters any arm's forward graph.

---

## 11. Seeds (frozen)

| Family | Range | Count | Use |
| --- | --- | --- | --- |
| Engineering model seeds | 0–7 | 8 | screens, the §10 σ_difference measurement, decoder training; excluded from all finals |
| Final model seeds | 100–111 | 12 | the frozen final sample |
| Decoder train / eval | 0–7 / 100–111 | — | the G8 instrument only |

The runner must **assert** the actual seeds equal these declared families in the audit —
never trust a placeholder seed list (AC15 rule 5). A deviating run is preserved, corrected,
re-run; the protocol is never amended to match a result. Families are never mixed; every
engineering seed is excluded from every final sample (AC39). Within a model seed, evaluation
episodes are balanced across z ∈ {A, B}.

---

## 12. The reduction-audit obligations (G9's binding handoff, frozen)

G9 (`PHASE3_REDUCTION_AUDIT_v1.md`) concluded the concept is identifiable and handed this
card three obligations that are now frozen and load-bearing inside the gates:

1. **Keep I4 and I5 as the load-bearing SHARED tests.** SHARED's identity criterion has
   behavioral discriminators only in I4 (private-copy divergence, §9.3.2) and I5
   (global-vs-local error, §9.3.3). The single-write test (§9.3.4, G5 §10 gate 1) is a
   necessary *source* assertion, never a sufficient *behavioral* proof. Dropping I4/I5 would
   make SHARED unidentifiable by construction.
2. **Keep the π-cut (I_π) and F1 as the load-bearing MAINTAINED tests.** MAINTAINED's only
   behavioral roles are the π-cut decay signature (§9.1.3) and the free-recurrence test
   (§9.1.4). The sever tests are source checks; they cannot carry MAINTAINED alone. Dropping
   I_π or F1 would make MAINTAINED unidentifiable by construction.
3. **Do not promote COORD to a candidate-vs-R2 fact.** COORD is the load-bearing
   candidate-vs-R1 contrast (§9.4.1); the candidate-vs-R2 modularity contrast lives in the
   interventions (R2 has no W to scramble/cut/stale), the π-cut (R2 has no π), and in-policy
   consumer addition (G7). Stating COORD as a candidate-vs-R2 separation would be the
   AC14-class arm-name error at the level of the predicate.

These three are incorporated as the load-bearing sub-tests marked "load-bearing per G9" in
§9, and they may not be dropped, downgraded, or renamed.

---

## 13. Claim ceiling

A full pass on H1–H5 earns, **at most**: "one maintained representation's content is
available to two-or-more objective-distinct modules that need different information and
drive different behaviour, and the organizational properties of that sharing — single-write
identity, paid persistence, structural coordination, compression, and reuse by a new
consumer — are each causally load-bearing against a rival that removes exactly one — N2 at
the stated degree."

Nothing stronger, in particular not: "global broadcast"; "a workspace seat" (O3/GWT);
"a unified conscious field"; metacognition (N4, a Phase-IV target); endogenous allocation
(T4, verdict D — S_reg is a readout, not a maintenance controller); content self-production
(AC78 blocked, not required); autopoiesis; any claim crossing the level-(d)/(e) boundary.
This is a **level-(b)/(c) representational** claim. Paid persistence is carried as the N1
*substrate* (shared by state-blind schedules, N12 F2), never as evidence that any allocator
is load-bearing.

A rival winning is an admissible Phase-III result: R2 (Q5) is the most likely clean winner
(richer, cheaper, would match on inference and coordination), and R5 (Q3) is the most likely
near-winner (ties on coordination and performance, loses only on I4/I5). Both are recorded
as falsifications of the corresponding conjunct, never reclassified as scope notes after the
fact (G9's standing bar).

---

## 14. Provenance

This protocol is the synthesis of the nine G-series design documents, each incorporated by
reference, not re-derived: `PHASE3_BASELINE_v1.md` (G0 — W/π/S_pol/S_reg RETAIN, V REMOVE,
A SIMPLIFY, the supplied-vs-learned contract), `SHARED_CONTENT_DEFINITION_v1.md` (G1 — the
five-predicate conjunction H_share and the per-criterion falsifiers),
`PHASE3_INFERENCE_TASK_v1.md` (G2 — the scalar-LLR sufficient statistic, the b-bit
quantization, the probe, the Bayes/memoryless ceilings, the π-cut), `PHASE3_SPECIALISTS_v1.md`
(G3 — S_pol/S_plan/S_reg and the three invariance classes), `PHASE3_ARCHITECTURES_v1.md`
(G4 — candidate SLW + R1–R5, the comparability contract, the per-rival gate shapes),
`PHASE3_CAUSAL_PLAN_v1.md` (G5 — the canonical I1–I5 and the signature-match quality bar),
`PHASE3_COORDINATION_v1.md` (G6 — COORD, the θ ≤ a ordering, the per-arm table),
`PHASE3_NOVEL_CONSUMER_v1.md` (G7 — S_conf/S_bias, the four measures, the R1 sub-arms),
`PHASE3_LEAKAGE_AUDIT_v1.md` (G8 — the seven pathways, the I/D/L grades, the four ablations),
and `PHASE3_REDUCTION_AUDIT_v1.md` (G9 — the unidentifiability verdict and the three binding
obligations frozen in §12).

The phase and claim-level vocabulary is `ACI_MASTER_RESEARCH_TREE_v2.md` (N14 — Phase III
re-scoped onto N2, D9/D10), `DEFINITIONS_CHARTER_v1.md` (§2 levels (a)–(e)), and
`ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (P1–P7, D1–D8 — P5/P6 and D1/D2/D8 are the scope and
rival-discipline clauses). The statistical machinery is `TBRIDGE_STATISTICAL_PLAN_v1.md`
(N7 — the sign-flip, the 2/2^n floor, N = 12, the re-derivation rule) and
`ACI_BRIDGE_PROTOCOL_v4.md` (the STOP whose T1 successor this is). Organism study references
read from the skill's `references/` dir where named: `ac11`/`ac16`/`ac17` (gate shape matched
to claim shape, sweep the rival family, never move a threshold post-hoc), `ac14` (arm names
must match the wiring), `ac38`/`ac46` (the exact sign-flip), `ac39`/`ac68` (disjoint seed
families, engineering does not transfer), `ac47` (graded vs saturated endpoints), `ac83`/`ac85`
(byte-identity license and the silently-wrong-wiring failure mode), `ac109`/`ac110` (causal
claim where the content is the only carrier, correctness rides content), `ac116` (the integer
counter vs the tuned memoryless rival).

No autopoiesis claim and no consciousness claim is made anywhere in this document. It is a
frozen protocol, not a result.
