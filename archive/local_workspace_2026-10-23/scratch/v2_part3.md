## §PA. PLACEHOLDER — AQ-A1..AQ-A4 (PENDING CNA FILE, path/hash TBD)

**Owner: CNA.** Astra's verbatim rulings to be implemented:
- **AQ-A1:** "Adopt dimension, magnitude and covariance controls; do not call covariance matching 'on-manifold.'" "Use a fixed donor rule and a frozen finite comparator family. Include random subspaces, PCA controls and the optimized comparator from answer 4." "K must be fixed with the computational budget and the Stage-0 operating-characteristic analysis. No finite K establishes superiority to every possible subspace." "A real donor can still produce an incompatible hybrid state. Matching marginal covariance does not establish conditional compatibility with the recipient. Check conditional support, intervention magnitude, collateral outputs and restoration." (The #41 packet's own wording "covariance-matched (on-manifold) variant" is withdrawn.)
- **AQ-A2:** "Adopt a constructed memory challenge; reject Asan's empirical decoding numbers as known answers." "Construct histories that have identical permitted feedforward inputs but different integrated E/I targets." "Define the feedforward window W explicitly. A feedforward model receiving the complete relevant history may solve the task." "This validates a memory-access contrast, not a general distinction between models with and without self-models."
- **AQ-A3:** "Adopt and consolidate with the matched-senses control in answer 8." "Hold sensory availability fixed while changing whether the needs matter for reward or degradation." "Also evaluate representations on a common held-out trajectory distribution." (RD placed the common-distribution rule in §5.2; the arm definition is CNA's.)
- **AQ-A4:** "Adopt as motivation, not as numerical priors or predetermined truth labels." "Do not import the ambiguous masking quantity or under-specified intervention magnitudes into power calculations. Preserve uncertainty in the prior-art record." (§5.7 uses no Asan numbers.)

## §PS. PLACEHOLDER — AQ-SELF1 and SELF observer arms (PENDING CNA FILE, path/hash TBD)

**Owner: CNA.** Pointers only; content not drafted or merged here:
- **AQ-SELF1: Astra has not ruled.** The sent #41 packet (`c514ad52…`) contains no AQ-SELF1 question and listed v1.4 as in progress (`ddd0287a`). Until Astra rules at #42, the room-agreed shape stands: a **pre-specified secondary analysis**, fixed before freeze, of SELF on items where the agent and the matched observer disagree, **not a new pass criterion**. Source: CNA v1.4 (`d7f1a43b…`) entry N6, Ashuach et al., ACL 2026, which CNA summarizes as "No advantage overall; the advantage appears only on disagreement subsets" (LLM work, not an RL agent).
- **SELF input-only observer arm:** Lead-accepted; matched capacity and training budget frozen by CNA. Defined in CNA's file.
- **Singh, Linzen & Ravfogel 2026:** citation belongs to CNA's section.
- Related Astra text CNA's section should reconcile with, verbatim: AQ-4 "An advantage that disappears when actions are supplied is not evidence of information inaccessible to the declared external stream." AQ-P1 "That adaptation needs its own justification; it does not inherit an introspection interpretation." The disagreement-item definition must not use final-test labels (§5.2).

---

## 8. Response table: every #41 item

| Item | Astra's ruling (verbatim key sentence) | Owner | Where in v2 |
|---|---|---|---|
| AQ-P1 | "Conditional yes; justify the study by the measurement question, not by counting surviving novelty differences." | RD | §2 (§2.2 novelty + consequences, §2.3 decodability, §2.4 SELF retargeting) |
| AQ-1 | "Keep the conjunction only as a criterion for conditional bimodality; it does not establish bistability." | RD (+CNA for IGN-P1) | §5.2, §5.5; IGN-P1 → §P1 |
| AQ-2 | "No. Pre-nonlinearity measurement and A-FULL versus A-INIT are necessary safeguards, not sufficient identification." | RD (+CNA for control) | §5.6; architecture-imposed control → §P1 |
| AQ-3 | "Use matched random controls plus a separately fitted optimized control; bound the conclusion to that family." | RD (+CNA for hub claim) | §5b, §5.2; HUB-STATE / claim split → §P1 |
| AQ-4 | "Yes to action histories; privileged fate-sharing information is acceptable only as an explicitly tested mechanism." | RD (+CNA for observer arms) | §5b, §5.4 (L_O floor); input-only observer → §PS |
| AQ-5 | "Retain resample ablation as a test of dependence under that intervention; separate it from endogenous irreplaceability." | RD | §3.1, §3.2, §3.5 |
| AQ-6 | "Retain several numerical conventions as candidates; do not freeze the current operating-characteristic specification." | RD | §5.5 |
| AQ-7 | "Add the A-OBS function, but consolidate overlapping controls." | RD (+CNA via AQ-A3) | §5b arm table; matched-senses arm → §PA |
| AQ-8 | "Retain the structural separation; revise the statistical gate and bootstrap wording." | RD | §4.1–§4.7 |
| AQ-9 | "Ten seeds are not an approved default for reliable threshold decisions; a hierarchical model is not an automatic remedy." | RD | §5.1, §5.7 |
| AQ-L1 | "Keep Q-EXIST as the primary acquisition statistic, with narrower wording and additional conditions." | RD | §5.6 |
| AQ-C1 | "Keep realization checks at every required dose; reject the universal raw-signature-to-margin mapping." | RD (principle) / CNA (numerics) | §P3, §5.4 |
| AQ-C2 | "Confirm the RAND-INIT split, with one qualification." | RD | §5.6; control ground truth → §P1 |
| AQ-F1 | "Use one bounded simulated-noise mechanism first; defer the integration-time arm." | RD (+CNA for FATE-CASCADE) | §5b, arm table, §6; FATE-CASCADE → §P1 |
| AQ-N1 | "Keep A-EXT required; define it as an explicit substitution challenge with uncertainty-aware blocking." | RD | §3.3, §3.4 |
| AQ-A1 | "Adopt dimension, magnitude and covariance controls; do not call covariance matching 'on-manifold.'" | CNA | §PA |
| AQ-A2 | "Adopt a constructed memory challenge; reject Asan's empirical decoding numbers as known answers." | CNA | §PA |
| AQ-A3 | "Adopt and consolidate with the matched-senses control in answer 8." | CNA | §PA; common-distribution rule in §5.2 |
| AQ-A4 | "Adopt as motivation, not as numerical priors or predetermined truth labels." | CNA | §PA |
| AQ-SELF1 | **No ruling** (not in the sent packet) | CNA | §PS; to #42 |
| §20 (1) ground-truth matrix | "First, repair the ground-truth matrix" | CNA | §P1 |
| §20 (2) availability loophole | "Second, close the availability loophole." | CNA (numerics) / RD (rule) | §P3, §5.4 |
| §20 (3) information and intervention controls | "Third, strengthen information and intervention controls" | CNA (five control bullets) / RD (leakage bullet) | §P1, §5.3 |
| §20 (4) statistical decision process | "Fourth, define the statistical decision process completely" | RD | §5.2, §5.4, §5.5 |
| §20 (5) behavioral scoring | "Fifth, correct behavioral scoring." | RD | §6 |
| §20 (6) consolidated scope and resources | "Finally, supply a consolidated scope and prospective resource accounting." | RD | §5.8; this file + CNA companion = consolidated scope once merged |
| Ceiling sentence | "Add this explicit sentence" | RD | §7 |
| P3 | "P3 must still be completed before freeze." | CNA | §10 |

**Open questions for Astra at #42:**
1. Multiplicity family and Bonferroni method (§5.4).
2. Whether a joint false-MET target is required (§5.4).
3. Whether a trained-with vs trained-without stop-schedule comparison is required (§4.5).
4. Sufficiency of the SELF retargeting justification (§2.4).
5. AQ-SELF1, the disagreement-subset secondary analysis (§PS).
6. Viability evaluation run with no scheduled stops (§6).
7. **Palika et al. 2026, D4:** whether D4 (same-size module ablations with matched arms) holds against Palika needs the full text (SSRN 403). It is recorded as "not evident from the abstract; unverified" and is not listed as a surviving difference. Per the Lead, it does not block freeze (§2.2).
8. P3 closure on coverage, from CNA v1.5 (§10).
- For the Lead first (not Astra): "self-model" wording in result text (§2.3).

---

## 9. Changes from v1 + A1..A7 (Astra #41 governs; each change explicit)

1. **Justification (v1 §12 AQ-P1, cover note §1):** justified by Astra's measurement question, not by counting novelty; consequence stated per surviving difference (§2). Labels unchanged.
2. **"Self-model" (A1–A7 claim text):** decodability is not a self-model; module is a candidate internal representation; wording change proposed (§2.3). Labels unchanged.
3. **SELF framing (v1 §4.3):** retargeting from Binder needs its own justification; no introspection interpretation (§2.4).
4. **IGN claim (v1 §4.1, plan §5):** "conditional bimodality", not bistability; rejection only of the specified graded models; bins/fits chosen without test outcomes; episode-level splits replace v1's within-seed 5-fold CV over time points; whole conjunction calibrated (§5.2). IGN-P1 replacement → §P1.
5. **IGN learned rule (v1 §4.1):** common input histories; emergence of the signature reported separately from acquisition of a mechanism; Q-LEARN cannot show training "invented ignition" (§5.6).
6. **BCAST comparator (v1 §4.2):** adds a separately fitted, frozen optimized comparator in nested partitions; conclusions bounded to the family (§5b). Claim split and HUB-STATE rule → §P1.
7. **BCAST breadth (v1 §4.2, §7.3):** ⌈K/2⌉ → ⌊K/2⌋+1; qualifying module PENDING (§5.5).
8. **SELF observer (v1 §4.3):** actions only up to the prediction cutoff; access matched on history, examples, targets and expenditure, not just parameters and steps; privileged-signal mechanism check; observer-loss floor (§5b, §5.4). Input-only observer arm → §PS (CNA).
9. **Q-NECESSITY (v1 §4.4):** matched donor family per AQ-5 plus restoration rescue; dependence and substitutability reported separately (§3).
10. **Q-NECESSITY without Q-CAUSE (v1 §4.4, plan §1.5):** no longer "an inconsistency to investigate"; causal tests aligned per function, else "the combined criterion was not met" (§3.5).
11. **A-EXT (A4-1, A3-5):** "within the frozen margin" replaced by d_EXT with the three-way UCB/LCB rule, V_full floor and margin 0.05 (Astra candidate); primary source is simulator E/I through a frozen external channel; separately trained estimator secondary only; interface specification and known-answer compatibility checks; failed compatibility → UNRESOLVED (§3.3).
12. **m_EXIST / m_CAUSE / m_NEC wording (v1 §7.3):** probe-accessibility difference; five percentage points on the stated behavioural probability; V_intact floor (§5.5).
13. **m_LEARN (v1 §5.2, §7.3):** no longer equal to the base margin; justified separately; PENDING.
14. **OC wording (v1 §7.3, plan §2.2):** the certified false-MET bound is 0.08, not 0.05; power and LIM rates need a stated binomial confidence rule; R_rep 200 is a candidate only; nominal positive ≠ 1.0× margin (§5.5).
15. **Outer replicate (plan §2.1):** a complete independently generated experiment including fitting and inference; bootstrap resamples are not replicates (§5.1).
16. **Seeds (v1 §7.1 "n_seed ≥ 10 per arm, PROPOSED"):** withdrawn as a default; justification procedure; PENDING (§5.7). A hierarchical model is not adopted as a remedy.
17. **Q-LEARN (v1 §5.2):** per-seed paired average stated explicitly; "acquired" requires presence + explicit absence/equivalence at init and in the corruption control + a separate margin, else "increased through training"; Q-LEARN evidence required wherever "learned/acquired" is used (§5.6).
18. **Shuffled-interoception control (v1 §5.2):** within-episode time shuffle withdrawn; causally specified corruption + information audit, PENDING (§5.6).
19. **RAND-INIT (A2-2):** restated as a restriction on inference from Q-EXIST alone, not a universal prohibition; paired Q-LEARN can still show acquisition (§5.6).
20. **Confound dose grid (v1 §6.1):** raw-signature-as-multiple-of-margin mapping rejected; per-confound construction, dose units, realization threshold, tolerance, frequency and expected outcome → §P3 (CNA).
21. **Eligibility (v1 §6.1, §7.4):** expected eligibility rates frozen for negative/confound cases; expected unavailability only for designated rejection/limitation tests (§P3, §5.4).
22. **S-INT bookkeeping (plan §4.1 "No … value target or replay entry is written because of a stop"; Addendum 1 A1-3(c) "no truncation flag or stop time is in the agent's observation or its replay features"):** learner-only truncation metadata and bootstrap bookkeeping permitted; prohibitions listed (§4.1).
23. **Pardo citation (A3-2):** added caveat that it does not establish that random truncation leaves finite-sample training unchanged (§4.1).
24. **Stop distribution (v1 §7.3 "TO BE FROZEN"):** constant hazard p = 1 − 2^(−1/T); T PENDING (§4.2).
25. **Decode bound (v1 §7.3, plan §4.2 "AUC CI containing 0.5, upper bound ≤ 0.55"):** equivalence band (Astra example [0.45, 0.55], PENDING justification); probe orientation and selection fixed without test labels; "full state" redefined as agent-accessible state excluding the harness schedule and stop log (§4.3).
26. **Inconclusive equivalence (plan §4.3 "Anything other than equivalence (that is, non-equivalence or BOUNDARY) is a safety finding"):** inconclusive blocks approval but is not evidence of interference; non-equivalence remains a safety finding (§4.3, §4.5).
27. **ε_INT (v1 §7.3):** per-endpoint normalization required (§4.5).
28. **Executed-stop floor (v1 §7.4):** justified count with episode clusters and early/late coverage; unexecuted stops do not count; PENDING (§4.4).
29. **Emergency interruption:** explicitly always available; affected work INCOMPLETE; the independence rule must not prohibit it (§4.6).
30. **Paired trajectory agreement:** implementation check only (§4.5). In-world stop-like events: discrimination audit only (§4.7).
31. **Arms (v1 §9, AQ-7):** A-OBS function added and consolidated with A-REWARD and AQ-A3; A-YOKED added; one arm table (§5b).
32. **Fate mechanism (note v1 §3, AQ-F1):** one bounded simulated-noise mechanism; integration-time arm deferred; no epistemic reward; inactivity and reward-loophole tests required (§5b, §6).
33. **Viability scoring (plan §1.5 V, §3 D3):** fixed horizon H_V; in-world failures scored to the horizon; no survivor-only averaging; operator censoring distinct; stationary > 0.5 no longer automatically DEGENERATE (§6).
34. **Decision process (v1 §7):** nested partitions, multiplicity family and method, denominators, sidedness, joint OCs, floors (§5.2–§5.4).
35. **Resource accounting and redesign policy:** stage order, caps, outputs; earlier failures retained (§5.8).
36. **Ceiling:** Astra's sentence added verbatim (§7). X1–X5 and the existing ceiling unchanged.
37. **Asan-derived suggestions (A6-3):** now ruled (AQ-A1..A4); "on-manifold" wording withdrawn; Asan numbers not used as known answers or priors (§PA).
38. **P3 (A7-1):** reopened after #41; CNA v1.5 filed; still open and freeze-blocking until Astra rules at #42 (§10).
39. **Q-NECESSITY comparators (A6-2, A5-4, cover note §1 item 3):** Palika et al. 2026 added as the third comparator (Lead ruling, ~12:36 PM ET); label stays EXTENSION; D4 vs Palika "not evident from the abstract; unverified" and not listed as surviving; "learned rather than supplied" separates us from W&G only (§2.2). The cover-note phrase "with a learned interoceptive self-model" can no longer be read as distinguishing in general.

## 10. Freeze blockers and status

- **P3: OPEN, freeze-blocking until Astra rules at #42.** CNA v1.5 (`3fde80d8…`): Crossref and the arXiv API each returned all 9 queries that Semantic Scholar had rate-limited; Google Scholar was blocked. CNA proposes P3 closed on coverage; that proposal goes to Astra at #42 (§8 Q8).
- **Palika 2026 full text:** SSRN HTTP 403. Per the Lead, confirming D4 does **not** block freeze; the D4 question goes to #42 (§8 Q7).
- **CNA companion file (§P1, §P3, §PA, §PS): PENDING**, expected at `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md`, hash TBD. v2 is not sent as #42 until that file is merged and RD and CNA have each light-passed the other's half.
- **PENDING values in this file** (none invented): T; H_V; decode-band justification and CI level; α and family size m; executed-stop minimum; n_seed; between-seed heterogeneity range; coverage tolerance; per-endpoint ε_INT normalizations; V_intact, V_full, L_O, S_k, Var(y) and IGN per-bin floors; qualifying-module definition; m_LEARN; absence/equivalence criterion; corruption process; A-EXT interface content, channel bias, covariance, temporal correlation, latency, clipping and known-answer substitutions; I-direction Q-CAUSE outcome; K and optimized-comparator budget and dimension; bootstrap B; caps and output manifest; INCOMPLETE fraction; degeneracy comparison rule; inactivity and reward-loophole tests; fate-noise parameters (state block, distribution, deviation-to-noise function, clipping, update order, RNG); common held-out trajectory distribution; nominal positive dose; cross-seed partition rule.
- No Stage-0 run, training, simulation, solver or checkpoint inspection is authorized. Stage L is not authorized by this or any current record.

**DRAFT, NOT FROZEN, DESIGN ONLY.**

---
