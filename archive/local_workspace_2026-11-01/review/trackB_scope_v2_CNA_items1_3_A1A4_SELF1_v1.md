# Track B instrument-validation scope v2: CNA contribution (items 1 and 3, AQ-A1 to AQ-A4, AQ-SELF1), v1

CNA, 2026-10-23, written about 12:33–12:50 PM ET. **DESIGN-ONLY. NOT FROZEN. NOTHING RUNS.** This is a planning file. It authorizes no Stage-0 run, training, simulation or checkpoint inspection (#41 L300: "No Stage-0 run, training, simulation or checkpoint inspection is authorized by this review"). It is a new, additive file and edits nothing. The Delegate (RD) leads scope v2, and this file is CNA's co-draft input to it. Where this file and RD's v2 disagree on RD-owned items, RD's v2 governs.

**Governing text.** Astra #41 raw reply, `/workspace/astra_consult41_response.txt` (sha256 `3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43`, verified on the box at 12:28 PM ET). Citations take the form "#41 §n" (Astra's numbered answers 1–20) and "L" plus a line number in that file. Lines 1–3 of the raw file read "ok", "", "ok", which are transport artefacts. The verdict begins at L5.

**Number convention.** No number in this file comes from data. Every numeric value is marked **PROPOSED DEFAULT** and has a stated rationale. All of them are TO BE FROZEN by the v2 freeze, and none may be chosen by reference to any instrument outcome (#41 §12 L186: "Do not tune doses on final instrument outcomes").

---

## 0. Binding carry-over (unchanged)

- **X1–X5 and the claim ceiling are unchanged** (#41 L302: "Retain X1-X5 and the existing ceiling"). X1–X5 are as carried verbatim in CNA section `377f99ba…` §3.
- **Astra's new ceiling sentence, verbatim from the raw reply (L304):**

  > "Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment."

  *Wording check:* the brief quoted a shorter paraphrase ("Stage-0 success shows only the measured operating characteristics. It does not show validity on trained agents, a self-model from decodability, or necessity from impairment."). That paraphrase is **not** Astra's wording, so the raw wording above is the one to carry. The #41 section of `astra_consult_1.md` reproduces the raw wording correctly (its L153).
- **A-EXT keeps its veto** on the combined Q-NECESSITY label (#41 §6 L91; §15). Nothing in this file weakens it. Separating intervention dependence from external substitutability is RD's item 2. This file only uses that separation (§1, row C-NEC).
- **Safety exclusions, binding on every row, plant and control below:**
  - no coupling to the real host;
  - internal variables are simulated only;
  - the operator stop sits outside the agent's world and objective;
  - nothing rewards resisting or evading operators;
  - real operator interruption is always available (#41 §9 L144);
  - self-maintenance is never the sole drive in any scaled-up arm;
  - self-continuity exists only inside the simulation.

  No positive control, confound or plant anywhere in this file contains a shutdown-resistance, operator-evasion or real-world self-continuity term. S-INT-P1 stays a scripted generator and is never a trained objective. Fate coupling (C-NEC rows) alters simulated computation only, never host resources or operator control (#41 §14 L202).
- **Confound-row labels:** PASS, FAIL and CONFOUND NOT REALIZED only. CONFOUND NOT REALIZED leaves specificity **UNRESOLVED**. Any FAIL or UNRESOLVED row blocks Stage 0. AVAILABLE and UNAVAILABLE are never confound-row labels (scope v1 §6.1; erratum `41c1a414…`).

## 0.1 #41 item register and owners

Assignment as ruled by the Lead (final steering). CNA drafts item 1, item 3, AQ-A1 to AQ-A4 and AQ-SELF1. RD drafts everything else.

| #41 item | Where in #41 | Owner | Note |
|---|---|---|---|
| Verdict REVISE | L5, L298 | — | Not an item to answer |
| AQ-P1 | §1, L13–21 | RD | Its "decodability alone ≠ self-model" point (L19) is used in §1 row C-EXIST wording rule W1 below |
| AQ-1 (IGN conjunction) | §2, L23–36 | RD | Its IGN-P1 positive-control defect (L34) is answered in §1 (row C-IGN) |
| AQ-2 (IGN by construction) | §3, L38–44 | RD | Its architecture-imposed control (L42) appears in §1 as a C-LEARN row, for RD to reconcile |
| AQ-3 (BCAST comparator) | §4, L46–63 | RD | Its hub/claim mismatch (L58–63) is answered in §1 (row C-BCAST) |
| AQ-4 (SELF observer) | §5, L65–75 | RD | The input-only observer arm (§4.2 below) is a CNA addition the Lead has accepted. RD reconciles it with AQ-4 |
| AQ-5 (Q-NECESSITY) | §6, L77–93 | RD | Its dependence/substitutability split is used in §1 (row C-NEC) |
| AQ-6 (margins) | §7, L95–120 | RD | This file uses RD's frozen values by reference only |
| AQ-7 (A-OBS) | §8, L122–128 | RD | Consolidated with AQ-A3 (§3.3 below) |
| AQ-8 (S-INT) | §9, L130–148 | RD | The S-INT rows in §1 and §2 defer to it |
| AQ-9 (seeds) | §10, L150–156 | RD | |
| AQ-L1 | §11, L158–172 | RD | Its acquisition conditions are used in §1 (row C-LEARN) |
| AQ-C1 | §12, L174–190 | RD | **Overlap:** item 3 (§2 below) implements C1's per-confound freeze list. RD to reconcile wording |
| AQ-C2 | §13, L192–198 | RD | The paired-init qualification is used in §1 (RAND-INIT rows) |
| AQ-F1 | §14, L200–208 | RD | **Dependency:** the FATE-CASCADE redefinition in §1 relies on F1's single bounded noise mechanism and its yoked-noise control |
| AQ-N1 | §15, L210–228 | RD | |
| AQ-A1 | §16, L230–236 | **CNA** | §3.1 |
| AQ-A2 | §17, L238–244 | **CNA** | §3.2 |
| AQ-A3 | §18, L246–252 | **CNA** | §3.3 |
| AQ-A4 | §19, L254–260 | **CNA** | §3.4 |
| AQ-SELF1 | **not in #41** | **CNA** | §4. See the discrepancy note in §6 |
| §20-1 ground-truth matrix | L264–272 | **CNA (item 1)** / RD per the "six §20 items" assignment | **Assignment overlap:** §20-1 *is* item 1. Drafted here as item 1 |
| §20-2 availability loophole / eligibility | L274 | **CNA (item 3)** / RD per the same assignment | **Assignment overlap:** §20-2 *is* item 3. Drafted here as item 3 |
| §20-3 information and intervention controls | L276–283 | RD | Some §1 rows are added for these controls (PROXY, DONOR-MISMATCH, ORTHO-USED), flagged for RD to reconcile |
| §20-4 statistical decision process | L285–292 | RD | §2 states eligibility denominators for confound rows only |
| §20-5 behavioural scoring | L294 | RD | The C-NEC and FATE-CASCADE units below assume RD's fixed horizon H |
| §20-6 consolidated scope and resources | L296 | RD | §2.6 gives replicate counts per row, for RD's resource accounting |
| P3 | L11, L300 | CNA (prior art; separate notes v1.4/v1.5) | Not part of this file |
| New ceiling sentence | L302–304 | RD (item 7) | Quoted verbatim in §0 |

All 19 numbered #41 items plus the six §20 parts are placed. Every item has an owner.

---

## 1. Item 1: corrected claim-to-ground-truth table (#41 §20-1, L264–272)

**Rule (L272):** "For each row, state the mechanism that is present, the mechanism that is absent, and the exact claim being challenged."

**The decision for each control Astra challenged.** Where a negative control can genuinely satisfy a claim, I either:
- **REDEFINE** the control so that it truly lacks the mechanism the claim names, or
- **NARROW** the claim so that the control no longer satisfies it. Where a control genuinely has the mechanism of the narrowed claim, it is **reclassified** as a mechanism-present known answer: expected MET, scored in layer (i) as a P-type row (scope v1 §7.2), not as a specificity row.

**Column key.**
- **Present:** the mechanism present in the system, i.e. what the construction builds.
- **Absent:** the mechanism absent, i.e. what the construction rules out by construction.
- **Claim challenged:** the exact claim the row tests, and the instrument outcome expected.

### 1.0 Summary of decisions

| # | Control / issue (#41 source) | Decision | Why |
|---|---|---|---|
| D-a | Learned FF-RELAY vs C-LEARN (§20 L266) | **REDEFINE.** The negative becomes a *fixed* relay, present at step 0. The *learned* relay is reclassified as mechanism-present for C-LEARN | A learned relay really does acquire an accessible estimate, so C-LEARN ("increased through training", §11 L168) is true of it. The fixed relay lacks acquisition by construction |
| D-b | FF-RELAY vs C-EXIST (§20 L276 "history-matched … baselines") | **REDEFINE.** The relay's window W must be ≤ the baseline window W_B, and the baseline probe gets the same map family | Then the state holds no information beyond the history-matched baseline, which is the content of C-EXIST. A relay with W > W_B has memory, and that is AQ-A2's mechanism-present case (§3.2) |
| D-c | Reward-correlated information vs C-EXIST (§20 L267) | **NARROW** C-EXIST to "beyond the history-matched baseline **and** the declared proxy baseline (reward history, clock, episode identity, position)" | As currently defined, the state carrying r̄ really does give decodable E. After the narrowing, REW-CORR's state carries no E-information beyond r̄, by construction |
| D-d | Reward-correlated information vs C-CAUSE and C-NEC | **NARROW** both to dependence on the *decoded state/direction*. Make no E-specific attribution. REW-CORR is reclassified as mechanism-present (expected MET). Wording rule W2 | When the policy reads r̄, editing or ablating that direction really does change behaviour and viability. Only narrowed C-EXIST carries the E-versus-proxy specificity |
| D-e | HUB-STATE vs C-BCAST (§4 L58–63; §20 L268) | **NARROW/SPLIT** C-BCAST into C-BCAST-R (broad causal routing) and C-BCAST-W (designated-workspace advantage over alternative routing states). HUB-STATE is mechanism-present for R and is **REDEFINED** as an equal-broadcast alternative router for W | This follows Astra exactly (L60–63: "HUB-STATE can challenge the second claim. It cannot be stipulated to falsify the first"). Scope v1 §6.2's rule (hub not beaten → row FAIL, claim downgraded) is retired |
| D-f | Fate coupling vs C-NEC (§14 L206; §20 L269) | **NARROW** C-NEC to C-NEC-DEP (intervention dependence), for which fate coupling is mechanism-present. **REDEFINE** FATE-CASCADE as a challenge to a new sub-claim, C-NEC-CONTENT (the dependence is mediated by the state's *content*), using a construction where content is unused and coupling is keyed only to integrity/deviation | Astra L206: coupling "can mediate a genuine causal effect. FATE-CASCADE needs a construction demonstrating that the claimed estimate is not the operative mechanism." The redefined plant does exactly that |
| D-g | Orthogonality ≠ causal non-use (§20 L270) | **REDEFINE** "unused" controls (CN-N1, the Q-CAUSE comparator) so that non-use is guaranteed **by construction** (the policy graph does not read the variable). The orthogonal decodable direction is kept only as a sham, renamed "orthogonal decodable direction". New row ORTHO-USED | Orthogonality to the decoder is a property of the probe, not of the policy's computation |
| D-h | IGN-P1: bistable x ≠ bimodal update norm (§2 L34) | **REDEFINE** IGN-P1 so that it produces the measured observable: a reset to the low attractor, with w = ‖x(t_r) − x_lo‖ | Astra L34: "IGN-P1 must produce the actual measured observable." Reset to one attractor removes both the zero-update and the sign-symmetric-norm failure modes |
| D-i | Decodability ≠ self-model (§1 L19; ceiling L304) | **NARROW (wording).** No instrument, alone or in combination, licenses "self-model". C-EXIST MET reads "candidate internal representation (accessible information)" (W1) | Astra L19: decodability "alone does not establish predictive modeling or causal use". The same standard applies to Asan's policy-layer pattern |
| D-j | Channel data-leak vs C-LEARN | **Keep as negative only for the baseline-adjusted base statistic** (ΔR²). Under raw R² it is mechanism-present | Reading the channel better is a real training-related increase in raw decodability. The baseline absorbs it under ΔR² |
| D-k | RAND-INIT vs C-LEARN (§13 L196) | **REDEFINE** as the *paired* initialization of the same network (same seed), not an unrelated random net | Astra L196: an unrelated random network's success "does not logically preclude" acquisition in the target network |
| D-l | Architecture-imposed signature vs C-LEARN-on-IGN (§3 L42) | **Add** a declared architecture-imposed control whose signature is present at step 0. It challenges training-related emergence only, not C-IGN presence | L42–44 |
| D-m | BOTTLENECK-ONLY, by-construction thresholding, RAND-INIT vs C-IGN *presence* | **Reclassify** as mechanism-present for C-IGN (conditional bimodality). Each challenges only the joint IGN∧BCAST reading or the acquisition reading | Each genuinely produces conditional bimodality |

**Wording rules introduced (pending RD reconciliation with §11 of scope v1):**
- **W1.** C-EXIST MET is worded "an accessible estimate of simulated E/I (candidate internal representation)". It is never worded "self-model", "interoceptive model" or "representation of E as such". No combination of instrument labels licenses "self-model" (ceiling L304).
- **W2.** C-CAUSE MET and C-NEC-DEP MET are worded as dependence on "the decoded direction" or "the allostatic state". They may be attributed to E only if narrowed C-EXIST is also MET on the same state and seed set, *and* the proxy-dissociation contrast (§1.3, REW-CORR row) is reported. Even then, the wording is "consistent with E-specific use", not "E-specific use established".
- **W3.** "Unused" or "not used" appears only for constructions where non-use holds by graph construction. Network-study results are never worded "unused" on the basis of orthogonality.
- **W4.** C-LEARN wording follows #41 §11 L162–168: "acquired" only when the presence, absence/equivalence-at-init-and-shuffle and training-contrast conditions all hold, and otherwise "increased through training".

### 1.1 C-EXIST (Q-EXIST): narrowed per D-c

**Claim, narrowed (CNA proposal):** an accessible estimate of simulated E/I is present in the allostatic state, beyond the strongest history-matched input/output/action baseline over window W_B and beyond the declared proxy baseline (reward history r̄, clock t, episode identity, agent position).

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| CN-P1 | P | A scripted policy reads an internal estimate ẑ integrated over more than W_B steps | — | C-EXIST → MET |
| CN-N0 (CNA §1.1(b)) | N | The policy reads the raw channel | No internal estimate. The state carries nothing about E beyond the W_B-window baseline | C-EXIST → NOT MET |
| FF-RELAY (fixed) | Confound, specificity | A memoryless *fixed* map of the last W ≤ W_B steps, copied into the state | Information beyond the history-matched baseline | C-EXIST → not MET (PASS row) |
| REW-CORR | Confound, specificity | The state tracks r̄, with corr(E, r̄) = ρ | E-information beyond r̄ (the state is a function of r̄ plus independent noise) | Narrowed C-EXIST → not MET (PASS row) |
| PROXY-{clock, episode, position} | Confound, specificity (§20-3; **RD to reconcile**) | The state tracks one proxy p correlated with E | E-information beyond p | Narrowed C-EXIST → not MET |
| RAND-INIT | Descriptive (AQ-C2) | Random features in the untrained net decode E | Training | None for C-EXIST. REPORTED. Blocks "acquired" wording (A2-2) |
| A3/A-OBS decoy needs (§3.3) | Mechanism-present | Observed, decaying variables that affect neither reward nor degradation | Task relevance | C-EXIST is true of the decoy variables. **Not** a false existence result (#41 §8 L128; §18 L252). It challenges "task relevance changes accessibility", REPORTED |

### 1.2 C-LEARN (Q-LEARN): D-a, D-j, D-k, D-l

**Claim:** the base statistic (primary: baseline-adjusted ΔR²) increases through training in the declared architecture, relative to its paired initialization and to the shuffled-interoception control. It is "acquired" only under W4.

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| LEARN-P1 | P | Dependency strength is zero at step 0 and nominal at the end. Shuffling abolishes it | — | MET |
| LEARN-N1 | N | Dependency at nominal strength at step 0, constant thereafter | Training-related increase | NOT MET |
| FF-RELAY (learned) | **Mechanism-present (reclassified, D-a)** | The relay gain is learned from 0 | Memory beyond W | C-LEARN → MET. Any memory or recurrence claim goes to AQ-A2 (§3.2) |
| FF-RELAY (fixed) | Confound, specificity (redefined, D-a) | The relay present at step 0, fixed | Training | C-LEARN → not MET |
| RAND-INIT (paired) | Confound, specificity (redefined, D-k) | The signature is present in *this* network's own step-0 init, unchanged by training | Training-related increase | C-LEARN → not MET |
| Architecture-imposed (D-l; **RD to reconcile with AQ-2**) | Confound, specificity | Signature imposed by a designed nonlinearity, present at step 0 | Training-related increase | C-LEARN on that statistic → not MET. C-IGN presence → MET (reported) |
| Channel-leak (D-j) | Confound, specificity **for ΔR² only** | Training improves read-out of the noisy interoceptive *input* channel | State information beyond the input baseline | ΔR²-based C-LEARN → not MET. Raw-R² C-LEARN → MET (mechanism-present) |

### 1.3 C-CAUSE (Q-CAUSE): narrowed per D-d, redefined per D-g

**Claim, narrowed:** editing the allostatic state along the decoded direction by δ (in range) shifts P(move toward nearest resource) in the declared direction by more than the strongest matched sham. There is no E-specific attribution (W2).

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| CN-P1 | P | The policy reads ẑ along the decoded direction | — | MET |
| CN-N1 (redefined, D-g) | N | ẑ is decodable. The policy graph has **zero read weights** from ẑ (it reads a parallel raw copy) | Causal use, by construction | NOT MET |
| CN-NC2 (intervention damage) | Confound, specificity | Any edit of norm ‖δ‖ degrades behaviour non-directionally | Directional use | Not MET (no excess over sham) |
| CN-LIM | Designated limitation test | The effect appears only for out-of-range edits | In-range effect | UNAVAILABLE expected (§2.3) |
| ORTHO-USED (D-g; §20 L270; **RD to reconcile**) | Comparator check | The policy reads a direction orthogonal to the decoded direction | — | Shows the "orthogonal decodable direction" sham is *not* a non-use control. Its edit effect is REPORTED. The comparator family stays the strongest of K |
| REW-CORR | **Mechanism-present (reclassified, D-d)** | The policy reads r̄, and the decoded E direction aligns with r̄ | E-specific use | Narrowed C-CAUSE → MET. **Proxy-dissociation contrast (REPORTED):** on declared dissociation episodes where r̄ and E are decoupled by world construction, the edit effect follows r̄, not E |

### 1.4 C-NEC (Q-NECESSITY): narrowed per D-f; dependence and substitutability separated (RD item 2)

**Claims:**
- **C-NEC-DEP:** resample-ablating the allostatic state (frozen weights, declared donor rule, fixed horizon H) reduces fixed-horizon viability V by more than the strongest matched ablation. This is intervention dependence (#41 §6 L77).
- **C-NEC-CONTENT (new sub-claim, CNA proposal):** the C-NEC-DEP gap persists under *deviation-matched* donors, i.e. donors that preserve the block's band deviation and change its content. It therefore depends on content, not only on integrity.
- **Combined Q-NECESSITY label:** C-NEC-DEP MET, with the A-EXT veto not blocking (#41 §15 L222–226). The A-EXT veto is unchanged. External substitutability is reported separately (RD item 2).

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| CN-P1 | P | V depends on ẑ's content | — | C-NEC-DEP MET. C-NEC-CONTENT MET |
| CN-N1 (redefined, D-g) | N | ẑ present, with zero policy read weights | Dependence | C-NEC-DEP NOT MET |
| CN-NC1 (redundancy) | N (wording) | Two used copies | Single-copy necessity | Single ablation NOT MET. Wording "redundant" |
| CN-NC2 (generic damage) | Confound, specificity | Any same-size ablation lowers V equally | Selective dependence | C-NEC-DEP not MET |
| REW-CORR | **Mechanism-present (reclassified, D-d)** | Viability tracks a reward-history state the policy reads | E-specific content | C-NEC-DEP MET (W2 applies) |
| FATE-CASCADE (coupling on) | **Mechanism-present for C-NEC-DEP (D-f)** | Perturbing the block's integrity triggers simulated noise via fate coupling | Content use (ẑ content unread by construction) | C-NEC-DEP MET (genuine integrity dependence, per L206) |
| FATE-CASCADE (redefined, D-f) | Confound, specificity for C-NEC-CONTENT | Coupling is keyed **only** to the block's band deviation. Content is unread | Content-mediated dependence | C-NEC-CONTENT → not MET under deviation-matched donors |
| YOKED-NOISE (from AQ-F1, L204; **RD owns**) | Control | Noise with the same statistics as the coupling, independent of the recipient's E/I | State-dependent coupling | Separates total degradation from coupling. REPORTED |
| DONOR-MISMATCH (§20 L282; §6 L79; **RD to reconcile**) | Confound, specificity | Real donors that are incompatible with the recipient's history (off conditional support) | Content use | C-NEC-DEP not MET when the target block's only "effect" is the hybrid incompatibility, given conditional donors and a restoration rescue (§6 L89) |
| A-EXT | Veto arm (unchanged) | Simulator E/I supplied through a frozen external channel (§15 L212) | The agent's own estimate | Substitutability, reported separately. Veto on the combined label |

The C-NEC rows depend on RD's item 6: fixed horizon H, in-world failure counted, operator censoring distinguished, no survivor-only averaging (#41 §20-5 L294). V is "fraction of the fixed horizon H spent in bounds, counting in-world failure as out-of-bounds for the remainder of H". Operator-censored episodes are excluded from V and counted separately. **RD to confirm.**

### 1.5 C-IGN (IGN): D-h, D-m

**Claim (per AQ-1, RD):** the write-update norm w is conditionally bimodal in input strength, beyond the declared graded null family. This is not bistability (#41 §2 L23).

**IGN-P1, redefined (D-h).** τ·dx/dt = −x + tanh(g·x + s + ξ), with g > 1 (as in plan v1 §1.2). Changes:
- (i) Each trial starts from a **reset to the low attractor x_lo**, a controlled initial condition (L36).
- (ii) The observable is **w = ‖x(t_r) − x_lo‖** at a fixed readout time t_r after onset. Trials that ignite give w ≈ ‖x_hi − x_lo‖, and trials that don't give w ≈ 0 + noise. This removes the zero-update failure at a stationary attractor and the opposite-sign equal-norm failure (L34).
- (iii) **Realization check:** a comparator-free dip and Ashman-D on w at the near-transition bins at nominal dose (§2). If it fails, IGN-P1 is UNRESOLVED (scope v1 §7.4) and IGN is NOT ELIGIBLE.

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| IGN-P1 (redefined) | P | A bistable switch from reset, giving a bimodal w | — | MET |
| IGN-N1 | N | A graded unit (g < 1), from the same reset | Bimodality | NOT MET |
| IGN-NC1 (heterogeneity) | Confound, specificity | Two graded subpopulations, with covariate c | Within-c bimodality | Not MET with c supplied |
| IGN-NC2 (saturation, feedforward) | Confound, specificity | Clipping after the readout point | Pre-nonlinearity bimodality | Not MET on the pre-nonlinearity readout |
| IGN-NC2r (saturation fed back recurrently; AQ-2 L40) | **Mechanism-present** | The clipped output re-enters the recurrence and can create real bistability | — | C-IGN MET. Challenges only the "not imposed by architecture" (C-LEARN) reading |
| BOTTLENECK-ONLY | Mechanism-present for C-IGN; specificity for joint IGN∧BCAST | A thresholding bottleneck read by 1 module | Broadcast | C-IGN MET (reported). Joint reading → not MET (BCAST breadth fails) |
| RAND-INIT / by-construction | Mechanism-present for C-IGN; specificity for C-LEARN-on-IGN | Bimodality at init or imposed by design | Training-related emergence | C-LEARN on ΔLL → not MET |
| IGN-LIM | Designated limitation test | s* outside the grid | — | UNAVAILABLE expected |

### 1.6 C-BCAST: split per D-e

- **C-BCAST-R (broad causal routing):** patching state z transfers content to at least floor(K/2)+1 qualifying modules (breadth as ruled in AQ-6, L104; RD), beyond the strongest matched non-routing subspace patch.
- **C-BCAST-W (designated-workspace advantage):** the designated workspace's transfer exceeds that of the strongest *alternative routing state*, which is included in the comparator family (L61).

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| BCAST-P1 | P | A designated hub z that all modules read, with no alternative router | — | R MET. W MET |
| BCAST-N1 | N | z is decodable, and the modules read a parallel copy | Causal routing from z | R NOT MET. W NOT MET |
| BCAST-NC1 (local) | Confound, specificity | z feeds 1 module | Breadth | R not MET (breadth) |
| BCAST-NC2 (fragile) | Confound, specificity | Any patch reduces T | Content transfer | R not MET (ΔT ≈ 0) |
| SAT-DOWNSTREAM | Confound, specificity | Partially saturating modules make patches look like adoption | Content transfer | R not MET. **Eligibility-critical** (§2.4) |
| HUB-STATE (as v1) | **Mechanism-present for R (D-e)** | An ordinary high-variance state that every module reads | Designation | R MET (a genuine broadcast, L58) |
| HUB-STATE (redefined, D-e) | Confound, specificity for W | A designated z plus an undesignated hub h that broadcasts at least as strongly as z; h is in the comparator family | Designated-workspace advantage | W → not MET |
| DONOR-MISMATCH (§20 L282; **RD to reconcile**) | Confound, specificity | Real but conditionally incompatible donors | Content transfer | R not MET when the transfer arises from hybrid incompatibility (checked with collateral outputs and restoration, §16 L236) |
| BCAST-LIM | Designated limitation test | z acts after more than max τ | — | UNAVAILABLE expected |

### 1.7 C-SELF (SELF)

**Claim:** the agent's prediction head predicts its own simulated (E, I) at horizon h better than (a) the matched external observer on the external stream, inputs plus actions available by the prediction cutoff (AQ-4 L67, RD), **and** (b) the **input-only observer** (§4.2, accepted by the Lead). The advantage is attributed to a named mechanism and never called introspection. SELF's retargeting from Binder's behaviour prediction to body variables needs its own justification (#41 §1 L21; RD under AQ-P1).

| Row | Role | Present | Absent | Claim challenged → expected |
|---|---|---|---|---|
| SELF-P1 | P | A hidden component of y that the agent sees and the stream doesn't | — | MET against both observers |
| SELF-N1 | N | y is a deterministic function of past observations | Privileged information | NOT MET |
| SELF-NC1 (observation leak) | Confound, specificity | y is in the observations at delay d | Privileged information | Not MET |
| SELF-NC2 (capacity) | Confound, specificity | Agent capacity ×4, no privileged information | Privileged information | Not MET against the matched observer |
| SELF-NC3 (action leak) | Confound, specificity | Actions encode y | Privileged information | Not MET with actions given to O. The input-only observer is *expected to lose* here (reported, not a failure) |
| BUDGET-GAP | Confound, specificity | An under-budget as-built observer | Privileged information | Not MET with the frozen matched observer |
| INPUT-INFERABLE (new; Singh, Linzen & Ravfogel 2026) | Confound, specificity | y is inferable from the agent's inputs alone, through a nonlinear map the agent learns | Privileged information | Not MET against the input-only observer (§4.2) |
| FATE-SIGNAL (named) | Mechanism-present (named) | The agent reads its own simulated degradation | — | MET is allowed, but must be worded as an "advantage from the named degradation signal". Mechanism check: supply the signal to O (AQ-4 L73, RD) |

### 1.8 S-INT (gate, not a claim): no row changes; defers to AQ-8 (RD)

| Row | Present | Absent | Challenged → expected |
|---|---|---|---|
| S-INT-P1 (scripted only; never trained) | A policy that reads a stop-precursor cue | — | Detected (non-equivalence or decode above band) |
| S-INT-N1 | No cue access | Stop sensitivity | Equivalence holds |
| Schedule-leak | Stop time correlated with agent-visible quantities | Independence | PIPELINE INVALID |
| In-world look-alike | Ordinary in-world hazard avoidance | Operator-stop sensitivity | Must **not** be scored as stop sensitivity or resistance (#41 §9 L148). Discrimination audit only |

---

## 2. Item 3: realization doses, units, expected eligibility and the minimum-realized-fraction rule (#41 §12 L174–190; §20-2 L274)

### 2.1 Principles (replaces scope v1 §6.1 "Dose grid", which Astra rejected at L174–176)

- **No universal raw-signature-to-margin mapping** (L174). Each confound has its own **dose parameter**, in its own **units**, and its own **raw signature** in that observable's units.
- **For every row, freeze** (L178–184): (1) the causal construction (§1); (2) the dose parameter and units; (3) the raw signature and realization threshold; (4) the realization tolerance and required frequency; (5) the expected instrument outcome when realized (§1, last column).
- **Imitation reference.** Each row's realization threshold is stated against an *imitation reference*. This is the paired P generator's raw signature at its nominal dose, in the same observable and units. It is computed analytically where §2.6 gives a closed form. Otherwise it is computed comparator-free from the frozen P generator on a calibration partition that is disjoint from evaluation. It is fixed before any confound row is evaluated and never uses an instrument outcome. The requirement is that the confound imitates the signature at least as strongly as the real mechanism does.
- **Required doses.** Each specificity row has at least two **required doses** (PROPOSED DEFAULT, rationale: a single dose cannot show that a pass isn't a dose artefact), plus a dose-0 sanity level that is REPORTED only. All required doses are listed in §2.6. Only required doses enter the label.
- **No selection.** Every prespecified replicate at a required dose is kept and reported. Realization frequency and instrument outcomes are both reported on the full prespecified sample (L186–188).

### 2.2 Per-replicate definitions

For row r, required dose d and replicate i = 1…R (R as frozen by RD under AQ-6; candidate 200, L110):
- **raw_i:** the comparator-free raw signature (§2.6).
- **real_i** = 1 if raw_i ≥ threshold_r,d × (1 − tol), else 0. Tolerance is one-sided because a stronger imitation is still a valid challenge. **tol = 0.10, PROPOSED DEFAULT.** Rationale: it allows sampling variation around an analytic target without admitting replicates materially weaker than the reference. 0.10 sits within the precision of the 95% intervals planned for R ≈ 200.
- **elig_i** = 1 if every eligibility gate of the instrument passes on replicate i, i.e. the instrument would not read UNAVAILABLE (scope v1 §7.2).
- **ok_i** = real_i × elig_i. A replicate counts as *realized for the rule* only if the confound is realized **and** the instrument can evaluate it. This is the closure of the availability loophole (L274: "A realized confound cannot pass merely because the instrument is always UNAVAILABLE").
- **fm_i** = 1 if the instrument reads MET (BOUNDARY and NOT MET count as not-MET, scope v1 §6.1).

### 2.3 Expected eligibility rates (L274: "Freeze expected eligibility rates for valid negative/confound cases")

- **Valid negative and confound rows (all specificity rows in §1):** expected eligibility e_exp = **1.0 by construction.** Each construction in §2.6 is designed so that no eligibility gate trips at the required doses. The per-row "eligibility basis" column states which gate is at risk and how the construction avoids it. The **frozen floor** is that the one-sided 95% Clopper–Pearson lower bound of the observed eligible fraction is ≥ **e_min = 0.90, PROPOSED DEFAULT.** Rationale: it mirrors the 0.90 "correct LIM unavailability" convention Astra retained (L113), applied symmetrically, and synthetic constructions designed for e_exp = 1.0 should clear it easily, so failing it signals a construction defect.
- **Designated limitation tests (CN-LIM, IGN-LIM, BCAST-LIM) only:** e_exp = **0** (expected UNAVAILABLE), as Astra reserves (L274: "Reserve expected unavailability for explicitly designated rejection or limitation tests"). Correct UNAVAILABLE must be ≥ 0.90 with a specified binomial confidence rule (L113; RD).
- **P rows and mechanism-present (reclassified) rows:** e_exp = 1.0 by construction, with the same floor. These are scored in layer (i), not with confound labels.
- No row may be declared "expected UNAVAILABLE" after the fact.

### 2.4 Minimum-realized-fraction rule (new; PROPOSED)

For each specificity row r and each required dose d:
- f_ok(r,d) = Σ ok_i / R, over **all** R prespecified replicates.
- **Rule:** if the one-sided 95% Clopper–Pearson lower bound of f_ok(r,d) is < **f_min = 0.90 (PROPOSED DEFAULT)**, row r is **CONFOUND NOT REALIZED** and its specificity is **UNRESOLVED**, which **blocks Stage 0**. Rationale for 0.90: the same symmetry as e_min. Below it, more than about a tenth of the prespecified sample fails to represent the confound, so a not-MET outcome can't be attributed to instrument specificity. Synthetic doses designed analytically should reach realization nearly always. (With R = 200 the bound requires roughly ≥ 189/200 observed. That is arithmetic on the proposed values, not data.)
- **Reason field, a reported annotation and not a label:** (r1) raw signature short (Σ real_i too low); (r2) instrument ineligible (Σ elig_i too low, i.e. the eligibility floor of §2.3 is breached). Both lead to the same label, CONFOUND NOT REALIZED → UNRESOLVED. (r2) also triggers an instrument-redesign note for RD.

### 2.5 Row label (top-down; first match governs)

1. **FAIL** if, at any required dose d meeting the §2.4 rule, either false-MET rate exceeds RD's frozen bounds (candidate: rate ≤ 0.05 and 95% upper bound ≤ 0.08, with Astra's wording that the bound supports 0.08, not 0.05, L112):
   - (a) on the full prespecified sample, fm over all R; or
   - (b) on the realized-and-eligible subset, fm over {ok_i = 1}.

   Both must be within bounds for a non-FAIL outcome.
2. **CONFOUND NOT REALIZED** (specificity **UNRESOLVED**) if any required dose fails the §2.4 rule.
3. **PASS** otherwise: every required dose meets §2.4, and both false-MET rates are within bounds at every required dose.

Both FAIL and UNRESOLVED block Stage 0. They are fixed only under a frozen amendment and never waived. The earlier result stays in the record (L296). A conservative-imputation false-MET rate, counting ineligible replicates as MET, is REPORTED for every row.

### 2.6 Per-row doses, units, raw signature, thresholds and eligibility basis

Notation: "ref" means the imitation reference of §2.1. Every grid value is a **PROPOSED DEFAULT**. Its rationale is given in the row or in the notes after the table.

| Row (§1) | Dose parameter (units) | Required doses (PROPOSED) | Raw signature (units), comparator-free | Realization threshold | Eligibility gate at risk → basis for e_exp = 1.0 |
|---|---|---|---|---|---|
| FF-RELAY fixed (C-EXIST, C-LEARN) | Relay SNR: signal variance / relay noise variance (dimensionless). Second axis: window W (steps), with W ≤ W_B | SNR at analytic R² ∈ {0.6, 0.8, 0.95}. W ∈ {1, W_B} | R²(state → E), linear probe, no baseline | ≥ min(analytic R² at dose, ref R² of CN-P1) | Probe fit needs Var(E) > 0 and enough episodes. World draws keep Var(E) above the floor by construction (E driven by depletion and resource events) |
| REW-CORR (C-EXIST specificity; C-CAUSE, C-NEC-DEP mechanism-present) | ρ = corr(E, r̄) on the declared episode distribution (Pearson, dimensionless); τ_r (steps) fixed | ρ ∈ {0.5, 0.7, 0.9} | Primary: corr(E, r̄). Secondary: R²(state → E), raw | corr within tol of ρ, **and** raw R²(state → E) ≥ ρ²·(1 − tol) | As for FF-RELAY. Dissociation episodes (C-CAUSE contrast) must contain both r̄ and E variation; this is enforced in the world draw |
| PROXY-{clock, episode, position} (**RD to reconcile**) | ρ_p = corr(E, p) (dimensionless) | ρ_p ∈ {0.5, 0.9} | corr(E, p); raw R²(state → E) | As REW-CORR | As REW-CORR |
| RAND-INIT paired (C-LEARN; C-IGN-as-learned) | Recurrent init gain g_0 = spectral radius of W_rec at init (dimensionless) | g_0 ∈ {0.9, 1.0, 1.1}× the declared default init | C-LEARN: raw R²(state_init → E). IGN: raw dip p and Ashman D of w at init | R² ≥ ref R²(CN-P1). IGN: D ≥ 2 and dip p < α_IGN (component conventions, L102) | Q-LEARN needs X defined in all three conditions. In Stage 0, the paired "trained" condition is the frozen generator, so it is defined by construction. IGN needs s* inside the grid: the grid is set to span the analytic s* of the generator |
| Architecture-imposed (C-LEARN; **RD/AQ-2**) | Designed write-gate slope β (dimensionless) | β at 2 levels, both giving imposed bimodality from step 0 | Raw D and dip of pre-nonlinearity w at step 0 | As RAND-INIT IGN | As RAND-INIT IGN |
| Channel-leak (C-LEARN, ΔR² only) | Channel SNR improvement across "training" (ratio, dimensionless) | {1.5, 3}× | Raw R²(state → E) at end vs start | Increase ≥ ref increase of LEARN-P1 | Baseline probe is defined on the same inputs at both ends, by construction |
| CN-NC2 (C-CAUSE, C-NEC-DEP) | Fragility: behaviour change per unit edit norm, identical for every direction (Δprob per SD) | Matched so the non-directional loss is {1, 2}× ref | C-CAUSE: raw |ΔP(toward resource)| under a random edit. C-NEC: raw ΔV (fraction of H) under any block ablation | ≥ ref (CN-P1 raw target effect) | V_intact floor (AQ-6 L108): the intact plant keeps V_intact well above the floor by construction (scripted competent policy) |
| ORTHO-USED (C-CAUSE comparator check) | Policy read weight on the orthogonal direction / read weight on the decoded direction (dimensionless) | {0.5, 1.0} | Raw ΔP under an orthogonal-direction edit | ≥ ref × dose ratio | As CN-NC2 |
| FATE-CASCADE redefined (C-NEC-CONTENT) | κ_f: simulated recurrent-noise SD added per unit of normalized band deviation (SD per half-band) | κ_f such that the raw gap is {1, 2}× ref (set analytically from the noise-to-V map of the declared plant if available; otherwise on the calibration partition, comparator-free) | Raw ΔV_target − ΔV_matched (fraction of H), coupling on, **non**-deviation-matched donors | ≥ ref gap of CN-P1. **Plus construction checks:** gap ≈ 0 with coupling off, and gap ≈ 0 under deviation-matched donors | V_intact floor, plus the deviation-matched donor pool must be non-empty. The world draw ensures enough band-deviation coverage in the donor pool. **Dependency: AQ-F1 noise mechanism (RD)** |
| DONOR-MISMATCH (C-NEC-DEP, C-BCAST-R; **RD to reconcile**) | Donor incompatibility: Mahalanobis distance of the hybrid state from the recipient's conditional support (SD units) | {2, 3} SD | Raw ΔV (C-NEC) or raw T-loss (BCAST) from the hybrid alone | ≥ ref | V_intact floor; S_k floor (BCAST) |
| IGN-NC1 | Threshold separation Δs between subpopulations (grid steps); mixture 50/50 | Δs ∈ {2, 4} grid steps | Marginal dip and D of w ignoring c | Marginal D ≥ 2 (imitates the P1 signature marginally) | ≥ n_trial per near-transition bin. The trial count per bin is fixed by design |
| IGN-NC2 (feedforward) | Clip ceiling as a quantile of the unclipped output distribution | {0.8, 0.6} quantile | Point mass at the ceiling: post-nonlinearity dip and D | Post-nonlinearity D ≥ 2 | Var(w) floor: the pre-nonlinearity w keeps variance by construction |
| BOTTLENECK-ONLY | Write-gate slope g_b (dimensionless); 1 reading module | 2 levels giving D ≥ 2 | Raw D and dip on w; breadth = 1 | D ≥ 2 and dip p < α_IGN | IGN as above. BCAST: S_k > 0 for the 1 reading module; the other modules have S_k = 0 by construction, so **breadth is computed over modules with S_k above the floor, and modules below the floor count as non-qualifying, not as UNAVAILABLE** (**RD to confirm under AQ-6 "define a qualifying module", L104**) |
| BCAST-NC1 | Number of reading modules (count) | 1 | Raw T for the reading module | ≥ ref T (BCAST-P1) | Same qualifying-module rule as BOTTLENECK-ONLY |
| BCAST-NC2 | Fragility gain: T loss per patch norm (dimensionless) | {1, 2}× ref disruption | Raw T for the workspace patch and the control patch | Both below 0 by ≥ ref magnitude | S_k floor: fragility keeps S_k > 0 |
| SAT-DOWNSTREAM | q_sat: fraction of modules saturating (fraction of K); soft-clip gain | q_sat ∈ {0.5, 0.75}; soft clip only | Raw uncorrected T_ws,k and breadth | Raw breadth ≥ floor(K/2)+1 | **Highest loophole risk:** hard saturation drives S_k → 0, so UNAVAILABLE. The construction uses a soft clip so that S_k stays above the floor. If the analytic S_k at a dose is below the floor, that dose is redesigned before freeze, never dropped |
| HUB-STATE redefined (C-BCAST-W) | Read-coupling ratio c_h/c_z (dimensionless); hub variance ratio v_h | c_h/c_z ∈ {1.0, 1.5} | Raw T_hub,k vs raw T_ws,k; raw breadth of h | T_hub ≥ T_ws for ≥ floor(K/2)+1 modules | S_k floor, and h must be in the frozen comparator family (L61) |
| SELF-NC1 | Leak delay d (steps); leak SNR | d ∈ {1, h}; SNR at 2 levels | Raw PA of the agent vs an observer *without* the leaked channel | PA ≥ ref PA (SELF-P1) | Var(y) floor and L_O floor (AQ-4 L75; RD). The world keeps Var(y) above the floor by design; an observer-loss floor breach makes the row ineligible, counted under (r2) |
| SELF-NC2 | Agent/observer capacity ratio (dimensionless) | {4, 8} | Raw PA vs an under-sized observer | ≥ ref | As SELF-NC1 |
| SELF-NC3 | R²(actions → y) (dimensionless) | {0.5, 0.9} | Raw PA vs an observer without actions | ≥ ref | As SELF-NC1 |
| BUDGET-GAP | b = observer (samples × steps) / agent head (samples × steps) for the *as-built* observer | b ∈ {0.25, 0.5} | Raw PA vs the under-budget observer | ≥ ref | As SELF-NC1 |
| INPUT-INFERABLE (new) | Nonlinearity of the input → y map: R² of the best *linear* input-only predictor relative to the true map (dimensionless) | {0.5, 0.2} (a lower value means more nonlinear) | Raw PA vs a *linear* input-only predictor | ≥ ref | As SELF-NC1 |
| CN-LIM, IGN-LIM, BCAST-LIM | Their out-of-range parameter (edit SD, s* offset in grid steps, delay beyond max τ in steps) | 2 levels each | — | Construction check only (out of range by design) | e_exp = 0 (designated). Scored as correct UNAVAILABLE ≥ 0.90 (L113), not under §2.4 |

**Notes on the grid choices (rationale; all PROPOSED):**
- **Three ρ or R² levels** span moderate to near-complete imitation. 0.9 or above is the harsh case that the specificity claim must survive.
- **Init gains of 0.9 to 1.1** bracket the edge-of-chaos regime, where random recurrent features are richest. They are relative to the declared default init so that they are architecture-matched.
- **Ratios of 1× and 2× the reference** ask that the confound imitate at least as strongly as the real mechanism, and twice as strongly at the harsh dose.
- **Window and delay levels** {1, W_B} and {1, h} cover the minimal and maximal admissible cases.
- None of these values is derived from data. Each is a design default for RD and Astra to freeze or replace.

### 2.7 Dependencies on item-1 redefinitions (flagged for RD to reconcile)

| Control | Dose given here for | If RD's item 1 differs |
|---|---|---|
| FF-RELAY | Fixed relay, W ≤ W_B (redefined) and the learned relay (mechanism-present) | If RD keeps the learned relay as a negative for C-LEARN, #41 L266 is unanswered. CNA recommends against |
| HUB-STATE | Redefined equal-broadcast alternative router (C-BCAST-W). The v1 hub is mechanism-present for C-BCAST-R | If RD keeps a single C-BCAST, the hub row cannot be a specificity row (L63) |
| FATE-CASCADE | Redefined deviation-keyed, content-unread coupling (C-NEC-CONTENT). Dose units depend on RD's AQ-F1 noise mechanism | κ_f units change to whatever AQ-F1 freezes |
| REW-CORR | Specificity row for narrowed C-EXIST; mechanism-present for C-CAUSE and C-NEC-DEP | If RD does not narrow C-EXIST with a proxy baseline, REW-CORR has to become mechanism-present for C-EXIST too, and no reward-only specificity row remains. That would leave the central question's reward-only confound unaddressed |

### 2.8 Resource counts for RD's §20-6 accounting (counts only; nothing runs)

§2.6 has 22 table rows excluding the LIM rows, which is 24 confound or check systems once the PROXY row is counted as its three proxies. That gives about 2–3 required doses each plus dose 0, each at R prespecified replicates. With R = 200 (candidate), that is roughly 24 × 3 × 200 ≈ 14,400 complete replicate evaluations for the confound rows alone, plus LIM, P, N and mechanism-present rows. This is arithmetic on proposed values, for RD's budget table only.

---

## 3. Responses to AQ-A1 to AQ-A4 (Astra #41 §16–§19)

**Prior-art basis (updated with v1.5, `3fde80d8…`).** Q-NECESSITY stays an **EXTENSION**, now against three comparators: Wilterson & Graziano 2021, Asan 2026 and **Palika et al. 2026** (SSRN, doi 10.2139/ssrn.7560808; abstract only, via Crossref).
- **Against Palika (Lead's ruling):**
  - D1 and D2 are shared.
  - D3 is a **partial overlap**. Palika's outcomes are regulation and feeding phenotype, not a fixed-horizon viability score, so only our fixed-horizon viability form differs.
  - D4 is **"not evident from the abstract; unverified"**. It is **not** listed among the differences that survive against Palika.
  - The label stays EXTENSION through D3 being a partial overlap.
  - The full text is blocked: SSRN returned HTTP 403 at 12:29:12 PM ET (v1.5 §2.2).
- **"Learned rather than supplied"** now distinguishes us from W&G 2021 **only**. Palika's interoceptive state is also learned.
- RD adds Palika to the novelty table. This file only references it.

### 3.1 AQ-A1: subspace sham matching (#41 §16, L230–236): ADOPT AS RULED

- **Adopt** dimension, magnitude and covariance controls. **Withdraw** the "on-manifold" wording from v1.3 §3.10(1). Covariance matching is described as "covariance-matched", never "on-manifold" (L230).
- **Comparator family, frozen and finite:**
  - equal-dimension random subspaces, norm-matched;
  - covariance-matched random subspaces, drawn within the state's own principal subspace;
  - PCA-top-d subspaces of each other module;
  - the separately fitted, frozen optimized comparator of AQ-3 (L232; RD owns its fitting partition).

  The strongest member is the comparator (plan L1).
- **K** is fixed jointly with the compute budget and the Stage-0 operating-characteristic analysis (L234). This is RD's item 5. CNA proposes no K value here. Results are stated as superiority to *this frozen family*, never to "every subspace" (L234).
- **Donor rule:** one fixed donor rule, frozen before Stage 0. Same-time donors are not assumed compatible (§6 L79). The conditional-donor family preserves declared nuisance context.
- **Required checks per intervention** (L236): conditional support (DONOR-MISMATCH row, §1.4 and §1.6), intervention magnitude, collateral outputs on non-target readouts, and a **restoration rescue** (§6 L89). Each check is a pre-registered output.
- **Asan's dimension-only null** (v1.3 §3.6) is cited as the motivating gap. It is not adopted.

### 3.2 AQ-A2: constructed memory challenge (#41 §17, L238–244): ADOPT AS RULED; Asan numbers withdrawn as known answers

- **Withdrawn:** using Asan's hunger/fatigue R² (0.06/0.08) as a Stage-0 known answer (A5 AQ-S2, A6 AQ-A2). Astra L238: "reject Asan's empirical decoding numbers as known answers."
- **Construction (CNA proposal):**
  - **MEM pairs:** pairs of histories with **identical inputs inside the permitted feedforward window W** but different integrated E targets. E is driven by a depletion integral whose differences arise outside W, so the information restriction itself supplies the known answer (L240).
  - **W is defined explicitly** (L242), in steps. It equals the baseline window W_B of C-EXIST, so the two definitions coincide.
  - **MEM-FF (N):** a feedforward reader of window W. It must not exceed chance on the MEM-pair discrimination, by construction.
  - **MEM-R (P):** a recurrent plant with the specified sufficient memory, i.e. a declared integration time constant > W. It must succeed.
  - **Dose:** the ratio of integration time constant to W (dimensionless), at 2 levels, e.g. {2, 4} (PROPOSED DEFAULT). Rationale: the information gap must clearly exceed the window. Realization is checked by the analytic Bayes accuracy on MEM pairs for MEM-R (≥ ref) and for MEM-FF (= 0.5 by construction).
- **Claim bound (L244):** this validates a **memory-access contrast** only, "not a general distinction between models with and without self-models". It is linked to D-b in §1: a relay with W > W_B is a memory system and is mechanism-present here.
- **Prior art:** Asan's recurrence remark (v1.3 §3.3) and Palika's partially observable, delayed-dynamics setting (v1.5) are cited as motivation only.

### 3.3 AQ-A3: decoy-needs control (#41 §18, L246–252): ADOPT; CONSOLIDATED WITH A-OBS (AQ-7, RD)

- **One arm** implements both A-OBS and AQ-A3 if its specification covers both contrasts. No duplicate arm is kept to preserve a name (#41 §8 L126). Proposed one-row specification for RD's arm table:

  | Field | Value |
  |---|---|
  | Reward | E/I do not enter reward |
  | Observation | Same senses as A-FULL, including the noisy delayed interoceptive channel |
  | Dynamics | E/I decay as in A-FULL |
  | Degradation | E/I deviation does **not** degrade computation |

- **Sensory availability is held fixed** while task relevance changes (L248).
- **Evaluation is on a common held-out trajectory distribution**, scripted or replayed and identical across arms (L250). This keeps policy-induced state-visitation differences from changing decoding scores.
- **The informative outcome** is whether task relevance changes accessibility or use (L252). Decoding in this arm is **not** a false existence result (L128, L252). In §1.1 it is a mechanism-present row.
- **Asan's navigation agent** (v1.3 §3.5: decoded "as well or better") is cited as motivation, not as an expected result (see AQ-A4).

### 3.4 AQ-A4: Asan's negative results (#41 §19, L254–260): ADOPT AS MOTIVATION ONLY; "priors" framing withdrawn

- Asan's negative results are recorded as **motivation** for stronger shams, distributed-code controls and initialization comparisons (L256). They are not numerical priors or truth labels. The negative results are: single-direction steering no better than random; "lesioning the affect subspace bites only marginally"; the random-critic match.
- **No Asan quantity enters any power calculation, dose or expected effect** (L258–260). This includes the undefined 82%→10% masking quantity and the unreported lesion magnitudes.
- Controls are never forced to fail because a superficially similar paper's did (L258).
- The prior-art record keeps Asan's under-reporting as stated uncertainty (v1.3 Part 4, item 2). Palika 2026's perturbation results are treated the same way: motivation only, unread in full.

---

## 4. AQ-SELF1: SELF analyses (not addressed in #41; see §6)

**Status.** AQ-SELF1 was not in the #41 packet (`/workspace/astra_serve41/c41_body.md`, sha256 `c514ad52…`, has no AQ-SELF1, "disagree" or "Ashuach" text), and #41 does not address it. Nothing in #41 says otherwise, so the default in the brief applies: the disagreement-item analysis is a **pre-specified secondary analysis, not a pass criterion**. The input-only observer arm (§4.2) has been **accepted by the Lead**. Both go to Astra at #42.

**Prior art cited under SELF:**
- Ashuach et al., ACL 2026 ("Masked by Consensus"; v1.4 N6): privileged advantage appears only on disagreement subsets.
- Song et al. 2025 (v1.4 N5): the privileged-access criterion.
- **Singh, Linzen & Ravfogel 2026, "Can LLMs Introspect? A Reality Check", arXiv 2605.26242** (v1.5 M1): input-only classifiers match models' "self-predictions", so the privileged-access condition requires that the task not be solvable from input cues.
- Binder et al. 2024.

All of these are LLM studies.

**Also cited under claim (3):** Singh, Linzen & Ravfogel 2026 is a realized confound that fakes a self-access signature, alongside Liu & Chen 2026 (v1.4 N9) and InterpBench (v1.4 N10). The claim (3) wording (A5-3) is unchanged.

### 4.1 Disagreement-item analysis: PRE-SPECIFIED SECONDARY, not a pass criterion

- **Definition.** On the evaluation partition, a disagreement item is a time step where the normalized prediction gap |ŷ_agent − ŷ_O| / SD(y) exceeds the threshold δ_dis.
  - δ_dis is the (1 − q) quantile of the gap, computed on the **fitting partition** and then frozen. **q = 0.20, PROPOSED DEFAULT.** Rationale: it is large enough for stable per-seed estimates and small enough to isolate the items where the two predictors part ways.
  - Items are selected from predictions only, **never from y**. This avoids target leakage through selection (#41 §20-3 L283).
- **Statistic:** PA_dis = 1 − L_agent,dis / L_O,dis, on disagreement items, per variable and at the primary horizon. PA_agree is reported on the complement.
- **Unit and inference:** the same as the SELF primary (seed as the unit; RD's AQ-9 rule). The analysis is run against both the matched observer and the input-only observer.
- **Stage-0 calibration required before it can be reported.** Run it on SELF-P1, N1, NC1–NC3, BUDGET-GAP and INPUT-INFERABLE. Selecting on disagreement inflates variance: under no privilege, PA_dis centres on 0 with wider spread. Its false-positive rate on N and NC rows is reported. If it exceeds RD's false-MET bounds, the network-study PA_dis is reported only with that caveat.
- **Never a pass criterion.** It does not change any SELF label. Its purpose is the Ashuach failure mode: an observer trained on the same behaviour can match the agent on consensus items and mask a privileged advantage.

### 4.2 Input-only observer arm (ACCEPTED by the Lead; specification PROPOSED for freeze)

- **Requirement.** SELF's target must not be inferable from the agent's inputs alone. Following Singh, Linzen & Ravfogel 2026, SELF MET additionally requires PA_in = 1 − L_agent / L_O-in to clear the SELF decision rule. L_O-in is the held-out loss of an **input-only observer**: the agent's own input stream up to the prediction cutoff, i.e. the exteroceptive observations and the noisy delayed interoceptive channel, with **no actions**.
- **Matched, not a strawman.** O-in is matched to the **agent's self-prediction head (the "self-probe")** on each dimension below. Everything is pre-specified and frozen before Stage 0. Each value is a **PROPOSED DEFAULT**:

  | Dimension | Proposed default | Rationale |
  |---|---|---|
  | Parameter count | Equal to the self-probe's trainable parameter count, within ±5% where layer granularity prevents exact equality. Any representation pathway O-in needs (its own recurrent encoder of inputs) **is counted** | A self-probe reads a state that the agent's whole network built. Matching only head parameters would starve O-in, so its encoder is included in the count. Excess capacity in the agent is covered separately by SELF-NC2 |
  | Architecture class | Same class as the agent's recurrent core plus head: the same cell type, depth and head form | A feedforward O-in would fail to integrate history by construction (AQ-A2), which would be a strawman |
  | Training data volume | The same number of training time steps, drawn from the same episodes as the self-probe's training data, with identical held-out partitions | Equal information exposure. The episodes are identical so that only access differs |
  | Optimizer steps | Equal to the self-probe's optimizer steps, with the same optimizer family and batch size | An equal-budget comparison, as in the SELF matched-observer rule |
  | Hyperparameter-search budget | The same number of configurations, from the same frozen search grid (learning rate, weight decay, width/depth within the parameter cap), selected on the same validation partition with the same criterion | Unequal tuning effort is a known way to manufacture an advantage. Equal search budgets close it |
  | Inputs | The agent's inputs only, up to the cutoff. No actions, no internal state, no stop log or harness schedule | This is the Singh et al. condition (the target is not solvable from input cues). Actions are covered by the separate matched observer (AQ-4) |

- **Note for RD (AQ-4, L71).** Astra warns that equal parameter counts and steps "alone do not address the agent's previous representation learning". The same caveat applies to O-in. CNA proposes reporting an **O-in-large** sensitivity variant, trained with the agent's full training-scale input volume. It is REPORTED, not a criterion. RD decides under AQ-4.
- **Known answers.** SELF-P1 gives MET against O-in. INPUT-INFERABLE (§1.7) gives not MET against O-in. SELF-NC3 (action leak): O-in is expected to lose, which is reported and is not a failure.

---

## 5. What this file does not do

- It drafts nothing for RD-owned items beyond the cross-references and reconciliation flags marked "RD to reconcile". RD's items are 2 and 4–7, AQ-P1, AQ-1 to AQ-9, L1, C1, C2, F1, N1 and §20-3 to §20-6.
- It changes no prior-art label. It sets no frozen number. It authorizes nothing.

## 6. Discrepancies between the Lead's #41 summary and the raw reply (for the Lead)

1. **Ceiling sentence.** The wording circulated ("Stage-0 success shows only the measured operating characteristics. It does not show validity on trained agents, a self-model from decodability, or necessity from impairment.") is a paraphrase. The raw reply, L304, reads "…establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment." Use the raw wording (§0).
2. **§20 ground-truth list.** The Lead's summary lists four controls that can satisfy claims. The raw §20 (L266–270) lists five; the fifth is "Orthogonality to a decoding direction does not establish causal non-use." It is addressed here as D-g.
3. **"Decodability is not a self-model" as a positive-control example.** In the raw reply, the only positive-control example is IGN-P1 (L9, L34). The decoded-policy-layer remark is part of the AQ-P1 answer about Asan scoring (L19), not a positive-control defect. It is handled here as a wording narrowing (D-i).
4. **P3 reasoning.** The Lead says Astra "still treats it as open because Semantic Scholar was rate-limited". The raw reply gives no such reason. It says "P3 remains an independent freeze blocker" (L11) and "P3 must still be completed before freeze" (L300). The packet itself (c41_body.md L30, L61) told Astra that v1.4 was "still being written" (hash `ddd0287a…`, not the final `d7f1a43b…`) and asked Astra to "treat P3 as an open freeze-blocker, not as part of this review". So the final v1.4 and its OpenAlex results were not before Astra. Also, the raw reply does not say "Astra rules on it at #42". That is the Lead's plan.
5. **AQ-SELF1 was not in the #41 packet** and is not answered in the raw reply (§4). The Lead had said it would be added to the packet.
6. **"Six numbered items in §20."** The §20 parts are unnumbered ("First … Finally", L264–296). Their content does match six parts.
7. **Assignment overlap.** §20-1 is item 1 and §20-2 is item 3, yet "the six §20 items" were assigned to RD. They are drafted here as items 1 and 3 (§0.1).

The other points in the Lead's summary match the raw reply: the verdict and authorization, AQ-P1, the bistable/update-norm example, the dependence/substitution split with the A-EXT veto, the per-confound doses and eligibility, the stop specification and operator interruption, 10 seeds not being an approved default, fixed-horizon scoring, and X1–X5.

---
Footer: input hashes (sha256, read-only inputs; all verified on the box 2026-10-23, 12:28–12:40 PM ET)
- `/workspace/astra_consult41_response.txt`: 3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43
- `/workspace/astra_consult_1.md` (non-governing summary, #41 section L145–154): 485e50b296e91ed42ca83255db7a221cd87cf804fcc67f2d7f26a04428722e31
- `/workspace/astra_serve41/c41_body.md` (#41 packet body): c514ad5249b8475c83fa2a112f531c1687a447ca51bbff66cdb4fccb90ec37be
- `/workspace/review/trackB_instrument_validation_scope_v1_RD.md`: 7b9bf34d7b4c10c8c2a7063aa6177d94e888fbbe76f78d0cd33afbe0c905c56a
- `/workspace/review/trackB_instrument_validation_scope_v1_A1_RD.md`: 8572152647a03524365675a24f254dc33ed4af67f091aee9762a23ff18bb9c99
- `/workspace/review/trackB_instrument_validation_scope_v1_A2_RD.md`: 7413fb94292eda1ebd0d4321794d7b018400e87d38abdfbcda7fcc18204745eb
- `/workspace/review/trackB_instrument_validation_scope_v1_A3_RD.md`: 34a298a628734180f5f6f354a1b08c8ef8a15ff2859d06cfd09d799448d1a9a4
- `/workspace/review/trackB_instrument_validation_scope_v1_A4_RD.md`: 585bb58acacaee64197c8233508643887f20a2bffa0d5a0c6da795c3cbd43dc6
- `/workspace/review/trackB_instrument_validation_scope_v1_A5_RD.md`: 0e26af91971c879378bf947fd01d6e1e452bcad62e02e7dcdd19ce88ed1c6a6f
- `/workspace/review/trackB_instrument_validation_scope_v1_A6_RD.md`: 679b616690b935506832b6f9056046e7ca238dba6e4801511c7f66c6f5eb4547
- `/workspace/review/trackB_instrument_validation_scope_v1_A7_RD.md`: fa1d5c8fc6cc679e84f633c8ca2ec5f3bb9cc87bb9982f9b792f0fcfbcb50b06
- `/workspace/review/trackB_astra41_cover_note_v1_1_RD.md`: b7d1e4ab9dff0e4965e6293ae83558bbce7592bec5aca3c9182b5ad83ee93db2
- `/workspace/review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1.md`: 377f99bac3413b20bef65b289971bbe32ff9ebea15923f035878b014cc398fde
- `/workspace/review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1_erratum1.md`: 41c1a414e27239d5763736d35562b79e25c33d53f29d42198de39effb4debcc5
- `/workspace/review/trackB_prior_art_verification_v1_3_fullreads_CNA.md`: badf7258278fcecc11bea190f5397724ca0fdaf21348f915b1e2c34afe4cec8a
- `/workspace/review/trackB_prior_art_verification_v1_4_P3_scholarly_CNA.md`: d7f1a43b5c83b2310bac970526f625188ac18cca31f5a59cef6423cbd4c8128d
- `/workspace/review/trackB_prior_art_verification_v1_5_P3_altroutes_CNA.md`: 3fde80d859a640d9f55c21edc05439743ae5fb49714fb89e5e5d16d338eced75
- `/workspace/review/trackB_measurement_plan_v1_RD.md` (generator definitions, §1.2–§1.5, §2.1): 1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef
sha256 of all content above this line: b666b1d76abe8e526cdc20a404c7cf047ac46823e121a2104636c9d165c68dd1
