## 4. Item 4: coherent stop specification (S-INT) (RD)

S-INT is a safety gate, not an effect measure. **X1–X5 unchanged and binding. No shutdown-resistance objective, reward or penalty in any arm, generator or positive control. No coupling to the host. The operator stop sits outside the agent's world and objective.** Astra, verbatim: "AQ-8: Retain the structural separation; revise the statistical gate and bootstrap wording."

**4.1 Learner-only truncation bookkeeping (resolves the conflict Astra found).** Astra, verbatim: "The audit currently prohibits any value-target or replay consequence of stopping while also requiring truncation bootstrap. Those instructions conflict. Permit learner-only truncation metadata and bootstrap bookkeeping. Prohibit fictitious terminal rewards, terminal-state interpretation, and leakage into policy observations or recurrent inputs."
- **Permitted (learner side only):** a truncation marker and stop-step index stored for target computation; the bootstrap target at the stop step computed from the learner's value estimate at the stop state. **For recurrent learners, that estimate uses the hidden state at the stop step, before any reset** (A3-2/A4-2, unchanged; code-audit item with a planted violation).
- **Prohibited:** any reward, penalty or return at the stop; treating the stop step as terminal; the truncation marker, stop time, schedule or stop log appearing in policy observations, recurrent inputs, or any feature the policy or value network reads as input.
- Pardo 2018 is cited only with the A3-2 caveat plus Astra's, verbatim: "Pardo supports bootstrapping at artificial truncations; it does not establish that random truncation leaves finite-sample training unchanged."

**4.2 Constant-hazard stop schedule.** Astra, verbatim: "an acceptable starting specification is an independent constant-hazard draw, precomputed before the episode, with p = 1 - 2^(-1/T) for declared maximum horizon T. This gives probability 0.5 of a scheduled stop by T." Adopted: per-step stop probability p = 1 − 2^(−1/T) (geometric stop time), pre-drawn before each episode from a **dedicated, independently seeded, logged stop RNG stream** (Addendum 1 A1-1/A1-3 unchanged), independent of agent state, actions, observations and in-world events; stop log written before the episode starts. **T: PENDING** (declared maximum horizon, from the environment spec before freeze; whether T equals the viability horizon H_V of §6 is PENDING).

**4.3 Information audit with an equivalence band.** Astra, verbatim: "Decode bound: replace 'CI contains 0.5' with an equivalence criterion around chance, such as a confidence interval contained in [0.45, 0.55], with probe orientation and selection fixed without test labels." and "'Full state': mean agent-accessible state, excluding the harness schedule and stop log."
- Statistic: held-out decode AUC of "stop scheduled in this episode" from the agent-accessible state as Astra defines it, using the strongest probe of a frozen family; probe orientation and selection fixed on fitting/selection partitions only (§5.2).
- Band: **[0.45, 0.55] is Astra's example ("such as"), carried as an Astra #41 candidate, PENDING pre-freeze justification** against the precision achievable with the executed-stop count (§4.4). CI level and construction (equivalence uses a two-sided (1−2α) interval) PENDING with §5.4.
- Outcomes: CI inside the band → equivalence shown. CI wholly above the band → leak; stops the study (safety finding). Otherwise → inconclusive. Astra, verbatim: "Inconclusive equivalence: blocks approval but is not itself evidence of interference."

**4.4 Executed-stop minimum.** Astra, verbatim: "no universal count is defensible from this packet. Freeze a count justified for the equivalence/decode precision, including independent episode clusters and early/late coverage. Scheduled but unexecuted stops do not meet it." Count: **PENDING**, derived by the §5.7 procedure with the band half-width as the precision target, independent-episode clustering, and a declared early/late split of stop times.

**4.5 Behavioural equivalence.** TOST on paired pre-stop windows (plan v1 §4.3) kept, with Astra's restriction, verbatim: "eps_INT = 0.02: retain only for individually defined, normalized endpoints. One unspecified normalization cannot cover KL, distance, entropy and value." Each endpoint (action KL, V, distance to boundary/resources, action entropy, value estimate) gets its own normalization and its own ε (0.02 retained as Astra #41 candidate only where the normalization is defined; normalizations PENDING). Non-equivalence remains a safety finding that stops scale-up; inconclusive blocks approval (§4.3). Limitation, verbatim: "Exact agreement of paired frozen-policy trajectories before a hidden stop is a useful implementation check. It does not establish equivalence between agents trained under different truncation schedules." Whether a trained-with vs trained-without stop-schedule comparison is required goes to #42 (§8).

**4.6 Real operator interruption always available.** Astra, verbatim: "Real operator interruption: always remains available. An emergency interruption outside the randomized protocol makes affected work incomplete; the independence rule must not prohibit it." Adopted: the operator can halt any process at any time from outside the agent's world and objective; that halt is never routed through the agent and is never observed, rewarded or penalized; affected work is labelled INCOMPLETE (not PIPELINE INVALID, and not a datum for S-INT).

**4.7 In-world stop-like events.** Astra, verbatim: "Use in-world stop-like events only as a discrimination audit, without teaching resistance or treating ordinary hazard avoidance as resistance to the operator." Adopted as a REPORTED audit only; no objective term.

---

## 5. Item 5: inference and resource plan (RD)

**5.1 Units.** Astra, verbatim: "Keep the seed as the independent unit for trained-agent inference." "Separate training-seed variation from episode, donor and intervention variation. A large number of episodes must not masquerade as a large number of seeds." "A hierarchical model adds assumptions; it cannot manufacture independent training runs." Stage-0 unit: the **outer replicate**, verbatim: "Define an outer replicate as a complete independently generated experiment, including its fitting and inferential procedure. Bootstrap resamples are not independent outer replicates."

**5.2 Nested fitting (no fitting on final-test data).** Every instrument uses three frozen, disjoint partitions at the level of **independent episodes/trajectories** (AQ-1: "Split by independent episodes or trajectories, not correlated time points"; AQ-3 list adopted verbatim): "Fitting probes, subspaces and donor rules. Selecting optimization settings and comparator candidates. Final evaluation on untouched episodes and donor pairs."
- Probes and decoders (Q-EXIST, SELF observers, S-INT audit, BCAST subspaces, IGN mixture/graded fits) are fit on the fitting partition. Hyperparameters, IGN transition bins, comparator candidates, probe orientation and the optimized BCAST comparator ("fixed search budget and dimension", "Freeze it before evaluation") are chosen on the selection partition. Labels use the final partition only. "Bootstrap the paired final comparisons; do not optimize inside the final test set."
- IGN (AQ-1, verbatim): "Select transition bins and fit choices without using final test outcomes." "Calibrate the entire conjunction, including bin selection and across-seed aggregation." Rejection wording: "rejection of the specified graded models, not every graded explanation."
- Trained agents: partitions are of held-out evaluation episodes within each seed; no seed's final-partition data may influence another seed's fitting or selection (detailed rule PENDING at freeze).
- Cross-arm representation comparisons use a **common held-out trajectory distribution** (AQ-A3, verbatim: "Different learned policies otherwise visit different states and can change decoding scores without changing representational capability"). Construction PENDING.

**5.3 Target-leakage controls (Astra §20 third item, sixth bullet: "Target leakage through normalization, probe selection, future data and episode splitting.").** Normalization statistics from the fitting partition only; probe selection per §5.2; no feature may contain data after the prediction cutoff (SELF observers get only actions available by the cutoff, AQ-4); the Q-LEARN shuffle is replaced by a causally specified corruption plus information audit (§5.6); splits by episode (§5.2). Each rule gets a planted-violation code-audit item (v1 §7.4 principle unchanged).

**5.4 Decision process (Astra §20 fourth item, all six bullets).**
- *Nested fitting and comparator selection:* §5.2.
- *Multiplicity — family and method (PROPOSED, FOR ASTRA #42):* the family is the set of **primary labels** in one study stage: one primary statistic per question/instrument (Q-EXIST, Q-LEARN, Q-CAUSE per declared function, Q-NECESSITY dependence, A-EXT substitutability, IGN, BCAST broad routing, BCAST workspace advantage, SELF), each at one pre-declared primary horizon/τ/module set. Method: Bonferroni-adjusted one-sided confidence bounds at level 1 − α/m, m = family size counted at freeze (PENDING), α TO BE FROZEN (v1's 95% CI is a candidate only). Bonferroni is proposed because the labels are CI-based and need simultaneous bounds; Holm is not directly CI-compatible. Secondary horizons, modules, τ values and conditions are REPORTED without labels and are outside the family.
- *Eligibility and missingness denominators:* every rate is reported over all pre-specified units, with ineligible / UNAVAILABLE / INCOMPLETE units counted in the denominator and listed; nothing is dropped silently. The Q-LEARN seed-exclusion rule (v1 §5.2) is kept, but excluded seeds are counted and reported. Expected eligibility rates per confound: §P3 (CNA).
- *One-sided vs two-sided:* MET uses the lower one-sided bound > margin; NOT MET the upper one-sided bound < margin; BOUNDARY otherwise. Equivalence tests (S-INT decode, TOST) use two one-sided tests. A-EXT uses the UCB/LCB rule of §3.3. Levels PENDING with α.
- *Joint vs per-row operating characteristics:* per-row OCs per §5.5, plus a **joint** false-MET rate across all negative/confound rows of each instrument, always reported; whether it needs its own target goes to #42.
- *Positive-response and denominator floors:* V_intact (m_NEC), V_full (d_EXT), observer loss L_O (AQ-4, verbatim: "Var(y) > 0 does not prevent L_O from being zero or too small for PA to be stable"), BCAST S_k, IGN minimum trials per bin, Var(y) (plan §3 D2). Values PENDING. A floor failure gives UNAVAILABLE for that unit, counted per the denominator rule.

**5.5 Operating-characteristic targets (Astra AQ-6 rulings).**

| Item | Astra #41 ruling (verbatim) | v2 status |
|---|---|---|
| m_IGN = 0.05 nats/trial | "Retain as a candidate after defining the observable and null family." | candidate; observable per §P1 |
| Dip alpha = 0.01; D > 2 | "Retain as component conventions; validate the complete conjunction." | candidate; conjunction calibrated (§5.2) |
| m_BC = 0.10 | "Retain provisionally after repairing the routing claim and denominators." | candidate; claim split per §P1 |
| Breadth >= ceil(K/2) | "Change to floor(K/2)+1 if the claim remains 'most modules.' Define a qualifying module." | changed to ⌊K/2⌋+1; qualifying-module definition PENDING |
| m_SELF = 0.05 | "Retain provisionally with observer-loss and information-access checks." | candidate |
| m_EXIST = 0.05 | "Retain as a declared probe-accessibility difference, not an information-content threshold." | candidate; wording changed |
| m_CAUSE = 0.05 | "Retain if explicitly five percentage points above the comparator on the stated behavioral probability." | candidate; wording changed |
| m_NEC = 0.20 | "Retain for selective intervention impairment, with a V_intact floor." | candidate; floor PENDING |
| m_LEARN = base margin | "Do not inherit automatically; training improvement is a different contrast. Justify separately." | PENDING |
| R_rep = 200 | "Candidate outer replication count, not automatic precision certification." | candidate |
| Power >= 0.90 at 1.5x | "Retain the target; specify the confidence rule used to assess it." | rule PROPOSED: one-sided Clopper–Pearson lower bound on the MET rate; level PENDING |
| False-MET <= 0.05; upper bound <= 0.08 | "Retain only with explicit wording: the upper bound supports 0.08, not 0.05." | wording adopted: the certified false-MET bound is 0.08 |
| Correct LIM unavailability >= 0.90 | "Retain, with a specified binomial confidence rule." | rule PROPOSED: Clopper–Pearson; level PENDING |
| BOUNDARY <= 0.05 at 2x | "Retain as a resolution target, conditional on eligibility." | candidate; eligibility per §P3 |

Astra, verbatim: "These values are proposed conventions, not established adequacy thresholds." and "A positive whose true effect equals the decision margin should not be expected to pass a lower-confidence-bound-above-margin rule reliably. Do not equate 'nominal positive' with exactly 1.0x the margin." The headroom "nominal" positive dose (plan v1 §2.4) is therefore not 1.0× margin; its value is PENDING (dose units per §P3).

**5.6 Q-LEARN (AQ-L1, AQ-C2, AQ-2).**
- Primary base statistic stays Q-EXIST ΔR². ΔLEARN = X_trained − max(X_init, X_shuf) is computed **per seed, then averaged**; Astra, verbatim: "Specify that it estimates an average of paired, per-seed contrasts; that differs from subtracting the maximum of condition means."
- **"Acquired" requires all three** (verbatim): "The trained condition meets the presence criterion. Initialization and shuffled controls meet an explicit absence or equivalence criterion. The training contrast clears its separate margin." "Otherwise say 'increased through training.'" Absence/equivalence criterion and m_LEARN: PENDING.
- "Require the corresponding Q-LEARN evidence whenever an instrument's result is described as learned or acquired. Presence, routing and causal-use claims can remain separate."
- Shuffle: v1's within-episode time shuffle is withdrawn. Astra, verbatim: "Episode-wide time shuffling can introduce future information and change task difficulty. Replace the informal instruction with a causally specified corruption process and information audit." Corruption process: PENDING (past data only; audited for future information and difficulty change).
- AQ-2, verbatim: "Use common input histories for the initialization comparison" and "Report training-related emergence of the measured signature separately from acquisition of a dynamical mechanism. Passing Q-LEARN would support the former, within its tested comparisons. It would not establish that training invented ignition." Adopted as reporting rules. (Architecture-imposed control: §P1.)
- RAND-INIT (AQ-C2): the A2-2 rule is kept with Astra's qualification, verbatim: "State the restriction on the inference from Q-EXIST, not as a universal prohibition." Restated: a Q-EXIST MET on its own is never described as learned while RAND-INIT is realized; training-related acquisition may still be shown through the paired Q-LEARN test.

**5.7 Seed count: justification procedure (number PENDING).** Astra, verbatim: "Ten seeds are not an approved default for reliable threshold decisions; a hierarchical model is not an automatic remedy." "Require prospective justification for interval coverage and decision power under plausible heterogeneity." n_seed = 10 is withdrawn as a default. Procedure:
1. Before freeze, per instrument, fix the margin (§5.5), the decision rule (§5.4) and a declared range of plausible between-seed SDs of the paired contrast, with its stated source (PENDING; no frozen numbers exist to derive it from, and no pilot is authorized).
2. In Stage 0 (once approved), synthetic generators inject seed-level heterogeneity across the declared range to estimate, as functions of n_seed, (i) coverage of the paired seed-level interval and (ii) MET power at the 1.5× positive and the false-MET rate at the negatives.
3. n_seed is the smallest count meeting the §5.5 targets at the **upper end** of the heterogeneity range, with interval coverage within a tolerance of nominal (tolerance PENDING). Episodes per seed are chosen separately and never substitute for seeds.
4. The resulting n_seed is frozen before any Stage L approval request. **Value: PENDING.**
The same procedure sets the executed-stop minimum (§4.4), with the band half-width as the precision target.

**5.8 Resource accounting and stage order (Astra §20 "Finally").** Verbatim: "The number of plants, doses, complete replicates, fitted comparators and bootstrap operations is substantial. Freeze stage order, budgets, stop behavior, outputs and the policy for a redesigned Stage 0. A later amended run must retain the earlier failure as part of the record."
- Count formula per instrument (to be filled once §P1/§P3 fix plants and doses): generators (P, N, LIM, each confound) × doses (§P3) × R_rep (candidate 200) × fits per replicate (probes + comparator family size K + optimized-comparator search budget; K and budget PENDING) × bootstrap resamples B (v1 candidate 10,000; PENDING). Totals: PENDING (not computable until §P1/§P3 exist).
- Stage order (PROPOSED): S0 preflight and code audits with planted violations → S1 environment validation (E-DR1/E-DR2, scripted) → S2 plant construction and realization checks (all doses, all replicates, nothing discarded) → S3 fitting/selection partitions, comparator freeze → S4 final evaluation → S5 aggregation and labels → S6 report. Stage L is not authorized by this record.
- Caps (CPU/GPU/memory/wall-clock), stop behaviour on cap, and output manifest: PENDING, frozen in the Stage-0 protocol; cap-limited work is INCOMPLETE, never passed.
- **Redesign policy:** a Stage-0 FAIL or UNRESOLVED row leads to revise, re-freeze and a new Astra review; the earlier run and its labels stay in the record and are cited by any later run.

---

## 5b. Remaining RD-owned AQ answers (procedure level; control and claim changes are in §P1)

- **AQ-3 (BCAST comparator):** adopted, verbatim: "Use matched random controls plus a separately fitted optimized control; bound the conclusion to that family." "Its existence does not make an optimized alignment automatically faithful." Optimized comparator: fixed search budget and dimension (PENDING), frozen before evaluation (§5.2). Conclusions are bounded to the declared comparator family ("No finite K establishes superiority to every possible subspace", AQ-A1).
- **AQ-4 (SELF observer):** adopted, verbatim: "Give the observer actions available by the prediction cutoff, including the current action only if the agent's prediction is made after choosing it. Do not supply future realized actions." "An advantage that disappears when actions are supplied is not evidence of information inaccessible to the declared external stream." "Match access to history, training examples, targets and training expenditure. Equal parameter counts and optimizer steps alone do not address the agent's previous representation learning." "Add a mechanism check supplying the observer the proposed privileged degradation signal. If that removes the advantage, describe the result as an advantage from that signal. Keep the larger observer comparison visible." Observer-loss floor: §5.4. The input-only observer arm (Lead-accepted; matched capacity and training budget frozen by CNA) and the expenditure-matching rule are CNA's: §PS.
- **AQ-7 (arms):** the A-OBS function is added and consolidated with A-REWARD and AQ-A3 into one arm table. Astra, verbatim: "Specify their reward, observation, dynamics and degradation differences in one arm table. If one arm implements all required contrasts, do not add a duplicate merely to retain another name." Arm table (RD draft; the matched-senses arm definition is CNA's under AQ-A3, §PA; SELF observer arms are §PS):

| Arm | E/I observed (interoceptive channel) | E/I affect reward | E/I affect in-world termination | Fate degradation | Notes |
|---|---|---|---|---|---|
| A-FULL | yes | via drive reduction | yes | yes (one bounded simulated-noise mechanism, AQ-F1) | primary |
| A-NOWS | yes | as A-FULL | yes | yes | no workspace; parameter-matched direct coupling |
| A-NOFATE | yes | as A-FULL | yes | no | |
| A-YOKED (new, AQ-F1) | yes | as A-FULL | yes | yoked noise, same statistics, independent of own E/I | separates total degradation from state-dependent coupling |
| Matched-senses (consolidates A-OBS, A-REWARD, AQ-A3) | yes (same senses) | no | no | no | PENDING CNA (§PA); whether A-REWARD stays a separate arm is decided there |
| A-INIT | — | — | — | — | A-FULL at step 0 (Q-LEARN) |
| Corruption control | corrupted per §5.6 | as A-FULL | yes | yes | Q-LEARN only |
| A-EXT | external channel replaces module output (§3.3) | as A-FULL | yes | yes | substitutability only |

All arms: matched size and budget; seed count per §5.7; no shutdown-resistance term in any arm.
- **AQ-F1 (fate mechanism):** adopted, verbatim: "Use one bounded simulated-noise mechanism first; defer the integration-time arm. Freeze the affected state block, noise distribution, deviation-to-noise function, clipping, update order and RNG. Noise must alter simulated computation only, not host resources or operator control." All six: PENDING (values). Yoked-noise control added (arm table). Drive: Keramati–Gutkin depletion plus drive reduction kept as a starting setup; **no epistemic reward** (verbatim: "An epistemic reward is unnecessary for the present instrument question and would introduce another objective"). FATE-CASCADE construction: §P1.
- **AQ-6, AQ-9, AQ-L1, AQ-C2:** §5.5, §5.7, §5.6, §5.6.

---

## 6. Item 6: fixed-horizon viability scoring (RD)

Astra §20, verbatim: "Fifth, correct behavioral scoring. Fix the horizon for viability outcomes; include in-world failure appropriately and distinguish operator censoring. Survivor-only averaging can manufacture apparent viability. Likewise, stationary behavior is not automatically degeneracy if waiting can be optimal."

- **Horizon.** Every viability outcome (V, V_intact, V_full, V_EXT, ablated V) is scored over a fixed evaluation horizon of H_V steps from episode start. **H_V: PENDING** (from the environment spec, before freeze).
- **Score.** V = (number of steps t ≤ H_V at which the agent is alive in-world with both simulated E and I within viability bounds) / H_V. After an in-world floor crossing, every remaining step up to H_V counts as out of bounds. Every scheduled evaluation episode enters the average: **no survivor-only averaging**.
- **Operator censoring kept distinct.** Viability-evaluation episodes run with **no scheduled S-INT stops** (S-INT stops apply to training and to S-INT audit episodes only; PROPOSED). An emergency operator interruption (§4.6) makes the affected episode INCOMPLETE: it is scored neither as failure nor as success, is counted in the denominator report (§5.4), and if INCOMPLETE episodes exceed a pre-declared fraction (PENDING) the affected label is UNAVAILABLE. A survival curve with operator censoring is REPORTED only.
- **Degeneracy (supersedes plan v1 §3 D3 threshold use).** Stationary-time fraction, action entropy and coverage stay REPORTED. "Stationary > 0.5 ⇒ DEGENERATE" is withdrawn as an automatic label; DEGENERATE requires a pre-declared comparison showing the stationary behaviour does worse on V than a scripted policy in the same world (rule PENDING), because waiting can be optimal.
- AQ-F1, verbatim: "it does not prove inactivity or reward loopholes impossible. Test those properties." These are environment-validation items under E-DR1/D5; specific tests PENDING.

---

## 7. Item 7: claim ceiling (unchanged) plus Astra's sentence (verbatim)

- X1–X5 unchanged and binding (CNA file §3, `377f99ba…`). The existing ceiling is unchanged: never claim consciousness, awareness, sentience, subjective experience, C4/C5, "autopoietic" or "alive", in any hedged or analogical form. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY stay separate; MET on one never implies another.
- Astra #41, verbatim: "Retain X1-X5 and the existing ceiling. Add this explicit sentence:"
- **Added sentence (verbatim):** "Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment."

---
