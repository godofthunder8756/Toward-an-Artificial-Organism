# Astra digest: Track A lineage triage v1.1

| | |
| --- | --- |
| Source | `/workspace/review/track_a_lineage_triage_v1_1.md` |
| Source sha256 | `d2cc9152d58a81c8054e1ddc8c59d4d83cc32f9ea6428b8e331ffe9a64a5d3ef` |
| Digest of | v1.1 only. v1 (`b4e1a772…7f0b`) and v1.1 are unchanged |
| Built by | `/workspace/scratch/track_a_triage/digest/build_digest.py` (verifies the source sha first) |
| Kind | Planning and assessment only. No runs, no training, no repo changes |

**What the digest contains.**
- **U1–U11** are copied **byte-exactly** from v1.1 §5.
- **F, S and R** entries are one-line condensations. Each cites its v1.1 entry id. Read the full file for evidence and citations.
- **Counts:** FOUNDATIONAL 5, SUPPORTING 15, REDUNDANT 11, UNRESOLVED 11; 42 in total.

---

## 1. FOUNDATIONAL (one line each: claim | simplest rival | excluded?)

- **F1** — Production closure (clause (i)) over {W, C, B, description, program} plus S1–S4 maintained state, one strongly connected component, no external root; bounded, under the substrate convention. | Rival: external coordination over an ALife production network. | **Partially excluded.** Excluded for components and for all coordinator writes (W-gated). **Gap:** not excluded for the transition logic and interpreter (`advance()`, `prog.choose`), which are retained by convention (U1).
- **F2** — Within-model ablation dependence: W, C and B production are needed; AC92 shows functional interruption while alive and a machinery-only rescue. | Rival: common resource starvation, or a t=0 kill. | **Largely excluded** within the model: AC2 clamp and rescue ("bounded"), AC92 failure while alive with content intact. **Gap:** generality outside the model; W=0 is an absorbing cascade.
- **F3** — Coordination writes are enacted by produced W machinery, and succession is coherent and resumable (AC93/AC94). | Rival: external coordination with a cosmetic gate. | **Excluded for writes:** the gate refuses at W=0, and the ungated comparator gives 32/32 byte-identity. **Gap:** the sequencing logic is still supplied; the gate is inert at the healthy fixed point W=3.
- **F4** — State sufficiency: no host-side operational memory steers the trajectory (AC95 16/16, AC96 8/8 observer-discard). | Rival: hidden host-side memory. | **Excluded at the endpoint.** **Gap:** per-tick trajectory not compared; host functions outside the audited architecture.
- **F5** — The working program is reconstructed from the maintained description by a generic decode (AC79→AC80, bit-for-bit). | Rival: an external recipe, or template copying of inherited content. | **External recipe excluded. Template copying not excluded** (and not claimed): the decode format is supplied, and content invention is blocked (R10).

## 2. SUPPORTING (one line each: claim | simplest rival | excluded?)

- **S1** — AC1–AC4 building blocks confirmed on fresh seeds (AC3 at 2/3 rates). | Rival: common resource starvation in a dissipative chemistry. | **Partially excluded** (AC2 contrast, "bounded"). **Gap:** AC3's third rate (7/8).
- **S2** — Description succession holds 130/130. | Rival: in-place repair by redundancy and majority restore. | **Not excluded:** in-place repair alone also survives, so succession is a capability, not the load-bearer.
- **S3** — Boundary-mediated exchange at the material layer (AC114, D1–D3 16/16). | Rival: an aggregate count gate, or a supplied exchange law. | **Count gate excluded** (D1). **Gap:** the exchange law is still supplied.
- **S4** — Exchange composes with the five-mechanism closure at mechanism level (AC115). | Rival: externally coordinated, non-interacting modules. | **Excluded at mechanism level** (G1 byte-identity, G2/G3). **Gap:** whole-organism unity is not established (O4), and survival gates G4–G7 failed.
- **S5** — Internalized decision state (Gray streak + allowance-42). | Rival: a host-side counter, or a fixed failure-count threshold with a budget. | **Host counter excluded** as the steering memory (AC96 observer-discard). **Fixed-threshold rival not excluded** (R4). The host control is economically better (8/8 vs 2/8).
- **S6** — Route memory acquired from the organism's own outcomes, with reacquisition and erase-on-relinquish (AC7/AC8/AC75). | Rival: blind random-port search, or tabular associative (bandit) learning. | **Blind search excluded for use** (erasure 6/6, reacquire 8/8 vs 0/8, no-erase dies 8/8). **Gap:** not excluded for viability ("random ports also viable"); associative learning is not excluded and not claimed.
- **S7** — Content↔maintenance coupling of the one-bit estimate (AC107/AC108, 7/7 gates). | Rival: a same-information direct diagnostic, or a streak counter. | **Partially excluded.** Maintenance→content is excluded (paid write cut gives inaccuracy 16/16). **Gap:** storage is not excluded (direct diagnostic 48/48), and content use does not separate maintained content from a direct read.
- **S8** — AC106 errata K1 corrects scope: an engineering negative only. | Rival: an implementation defect rather than structural absence. | **Adopted, not excluded:** the errata endorses the defect reading (P1, P2).
- **S9** — Estimate–autonomy composition: direct channels are clean, but G3/G5 are 12/16 (AC111). | Rival: independent superposition. | **Excluded for direct channels; refuted as the full account** (interference on 6306 and 6307).
- **S10** — PR #3 restores the 78 deleted frozen files. | Rival: altered or regenerated files. | **Excluded:** 78/78 blobs identical to `d0ee2bb^`.
- **S11** — PR #4 world-admission certificate ADMIT. | Rival: an ordinary Bayesian joint filter. | **Not excluded, by design:** the chart is the joint posterior. The mean-field arm was not run.
- **S12** — PR #5 acquisition: E1 SHOWN, E2 RECURRENT ADAPTATION SUPPORTED, E3 NOT LOCALIZED. | Rival: a mean-field filter, or readout-only learning on a fixed core. | **UNVERIFIED in this triage:** I did not re-read which comparison E2 uses to exclude the readout-only rival. Localization is not established.
- **S13** — PR #7 TRANSFER SHOWN 10/10 (Q-LEARN). Matrix-specific effects not demonstrated. | Rival: reservoir computing (readout and gain tuning on a fixed core). | **Excluded within the declared grid** (advantage over tuned frozen GRU-8 10/10; F-INIT A-FIT 0/10). **Gap:** outside the grid; selection hit the grid edge.
- **S14** — PR #8 Q-CAUSE bounded, 9/10 against isotropic paths. | Rival: generic loss-aligned (first-order) displacement. | **Not excluded by PR #8.** It is addressed by PR #9 (S15).
- **S15** — PR #9 Q-CAUSE bounded, exactly 8/10 against both FO-matched and ISO controls. | Rival: first-order-matched and isotropic displacement. | **Excluded at 8/10 for the sampled families.** **Gap:** unsampled families, single extreme draws, and readout-compatibility disruption.

## 3. REDUNDANT (one line each: finding | simpler mechanism)

- **R1** — AC67/AC71 self-monitoring and repair loop | watchdog fault detection with a fixed corrective action (control theory).
- **R2** — AC11 adaptive maintenance allocation | a state-blind fixed-level duty cycle (control theory).
- **R3** — AC6 experience-dependent exploration | constant-rate (fixed-ε) exploration (RL).
- **R4** — Adaptivity of the internalized decision rule | a failure-count threshold with a fixed budget (control theory). This is a triage judgment.
- **R5** — AC106 maintained cause-belief | the frozen first-order streak counter (counting / change detection).
- **R6** — AC109 stored estimate | a reactive policy on the decisive current observation (RL / control).
- **R7** — AC110 "continuous repair sustains correctness" | re-estimation from fresh evidence (filtering / reacquisition).
- **R8** — AC117 reliability monitor as a predictor | directional-repair control plus a transient damage count (control / counting).
- **R9** — Graded/weighted posterior (P2/R2, AC113) | an integer counting statistic with a threshold (sequential ratio rule).
- **R10** — Self-directed content production (AC72–AC78) | a path-dependent, seed-specific fixed point (dynamical systems).
- **R11** — Explicit maintained self-state V (neural bridge) | a same-information reactive rule, or a 3-line sufficient-statistic threshold (control / RL).

---

## 4. UNRESOLVED U1–U11 (byte-exact from v1.1 §5)

### U1 (rank 1). J1: supplied coordinator and interpreter — substrate, or externally coordinated computation?

**What is open.**
- K3 resolves J1 "substrate" **by convention**: "a modeling choice, not a measurement".
- A3 had issued UNRESOLVED on the same evidence and noted that the AC90 review "did not affirm" the substrate reading.
- K3 itself records `advance()` as "a **larger** substrate concession than `prog.choose`".
- The Track A directive explicitly requires separating closure from externally coordinated computation. That is exactly this locus.

**Evidence:**
- `CLOSURE_VERDICT_v1.md` @ `4b85851` §2;
- `AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §3 and §7;
- `DEFINITIONS_CHARTER_v2.md` @ `4b85851` §9;
- `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb` (the "transition LOGIC (`advance()`) and the interpreter (`prog.choose`)" paragraph).

**Exact missing clarification (formal, before any run).** A substrate-admissibility rule that is stated in advance and independent of this organism. For example:
- *Content-independence:* the supplied function must be the same for every organization the substrate can host, so that it encodes no organization-specific sequencing.
- *Replaceability:* the function's role can be realized by a generic local reaction-rule interpreter that is itself on the production cycle.

The rule is then applied to `advance()` (copy→verify→switch→remove with a built-in verify gate) and to `prog.choose`.

**The empirical half, if the rule demands it.** A within-model replacement of `advance()` by a sequence encoded in maintained or produced state and executed by a generic step rule. Then repeat the F3/F4 tests on that version: interruption, machinery-only rescue and observer-discard.

**Dependency flags:**
- This may require a protected controller or a new architecture family. Both are excluded by the standing rules without approval.
- A2 argues the fully general question is an infinite regress. Only a **declared, finite** admissibility rule is decidable.

**Simplest rival.** *External coordination*: a host-supplied sequencer (`advance()`) and interpreter (`prog.choose`) that carry the organization, while the produced machinery only funds their writes.

**Relevance: YES, high.**
- If `advance()` fails the rule, F1 drops from "SUPPORTED (bounded)" to charter-v2 re-assessment, with the coordinator failing C2.
- If it passes, F1 stands with a rule rather than a convention.
- Either way the flagship Track A sentence changes.

**Stopping criterion.** Stop once an admissibility rule is fixed and applied, or once Astra rules the question out of scope. Do not run an experiment before the rule exists.

### U2 (rank 2). Adaptation of the system's own functional organization

**What is open.**
- The status file row "New maintenance dependencies acquired autonomously" is **NOT ESTABLISHED**.
- AC11 was falsified by its own controls (R2).
- AC6 adaptivity is unnecessary (R3).
- Content self-production is blocked (R10).
- The decision rule reduces to a fixed threshold and budget (R4).
- Bridge allocation reduces to a reactive rule (R11).
- So the "adapt" leg of the Track A question has no positive result. "Maintain" (F1–F4) and "reconstruct" (F5) do.

**Evidence:**
- `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb` (row "New maintenance dependencies acquired autonomously");
- `AC11_DESIGN_CONTROLS_v2.md` @ `c348a67`;
- `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §2.5 items 5 and 6. In the frozen economy, maintenance was priced at about 25× its payoff, so a cost/benefit trade-off was absent.

**Exact missing causal test.**
- A world whose economy is checked analytically, *before* any run, to contain a genuine maintenance trade-off. The best *fixed level* must be strictly worse than the oracle state-dependent policy, by a declared margin.
- An organism-internal adaptation of its maintenance allocation that beats the **entire swept fixed-level family** and a same-information reactive rule. These are Appendix B6 rivals.
- An intervention that reverses the adaptation when the acquired state is scrambled, with matched expenditure (AC106 P5 lesson).

**Simplest rival.** *A fixed-level duty cycle, or a same-information reactive threshold rule* (control theory). These already reproduce every adaptive candidate on record (R2, R3, R11).

**Relevance: YES, high.**
- A positive result would add the first established "adapt own organization" claim.
- A clean negative with the analytic trade-off certified would retire it.
- Today nothing is concluded.

**Stopping criterion.** If the analytic check shows that no fixed-vs-adaptive gap exists in any admissible world of the declared family, stop and record "not well posed". Do not run organism finals.

### U3 (rank 3). O3 constitutive loop: does a content intervention alter the enabling machinery and then future content?

**What is open.** Ledger O3 = PARTIAL: "maintenance affects content and content affects adaptation; full constitutive loop unestablished".
- AC108 shows content → adaptation/production (force_machinery) and maintenance → content.
- It does not show a closed loop in which content changes the machinery that later regenerates content.

**Evidence:**
- `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c` (layer O3);
- `AC108_RESULTS_v1.md` @ `5c0b2f1`;
- `ACI_PRIOR_ART_AND_REDUCTION_v1.md` @ `a72136c` ("Cross-route discriminator": "what is restored, and whether it restores the conditions enabling restoration").

**Exact missing causal test** (ledger `next_falsifier`, made operational).
1. Apply a matched-current-observation content intervention at t0.
2. Measure (a) a change in the *production or repair* of the enabling machinery during t0..t1 (for example W-gated repair writes or the description repair schedule).
3. Measure (b) a change in *content regenerated* after t1 that is mediated by (a). Mediation is shown by a second arm that clamps the machinery change while leaving the content intervention intact, so (b) must vanish.
4. Rivals:
   - a world-state-only controller;
   - the inactive-queue reduction "production-versus-state-regrowth dependency audit" (`ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c`, inactive_theory_queue).

**Simplest rival.** *Ordinary state estimation with intact, supplied machinery* (counting / filtering): a world-state-only controller whose content changes behaviour but never the machinery that regenerates content.

**Relevance: YES, high.** It decides whether closure extends from the material and production layer (O1/O2) to the informational and functional organization (O3), which is the "functional organization" in the Track A question.

**Stopping criterion.** If the clamp arm shows that (b) occurs without (a), the loop reduces to ordinary state estimation; record it REDUNDANT and stop.

### U4 (rank 4). Q-NECESSITY of recurrent-matrix learning (PR #10)

**What is open.**
- R-FIX-32 and R-FIX-48 both return **TARGET NOT REACHED WITHIN DECLARED SEARCH**, with 0/10 final verified passes, 0 init witnesses, 0 invalid and 0 boundary.
- CAND, the unrestricted comparator, reaches target 10/10.
- Q-NECESSITY = **NOT_ESTABLISHED**. "Failure means only 'not reached within declared search.' This is not a necessity certificate."

**Evidence:**
- `frozen_recurrent_compensation_results_v1/stage2/RESULTS.md` @ `0329818`;
- `frozen_recurrent_compensation_results_v1/results_v1_errata/RESULTS_v2.md` @ `0329818` (the ledger, per `results_v1_errata/ERRATA_v1.md` @ `0329818`);
- `frozen_recurrent_compensation_protocol_FINAL.md` @ `0329818`;
- PR #10.

**Exact missing test.**
- *Either* a pre-registered extended R-FIX search (protocol Appendix D) with a fixed grid of LR, steps and restarts, a held-out selection subset, a CAND comparator under the same search, and training-loss curve logging;
- *or* a finite-class bound: inf T > 1 over a declared parameter domain. The review judged a bound infeasible at 651–843 continuous parameters except for a narrow quantized subclass.

**Simplest rival.** *Reservoir computing*: train the input weights, biases and readout on a fixed random recurrent matrix. This is exactly the R-FIX arm, so it is a rival not yet excluded or confirmed beyond the declared search.

**Relevance: asymmetric.**
- **One verified R-FIX witness would change a conclusion.** It would refute, within GRU-8 at that W0 and head width, that weight_hh learning is needed for the target.
- Another failure would **not** change the conclusion: it stays NOT_ESTABLISHED.
- Necessity can only come from a bound.

**Stopping criterion.** Stop after one pre-registered extended search with no witness, unless a bound becomes feasible. Do not iterate searches (forking paths). Any training needs Aidan's approval.

### U5 (rank 5). Minimal organization

**What is open.**
- K3 §5 and A3 §5 classify components as necessary or optional by ablation (AC10/91/92).
- No document shows that the set is *minimal*, meaning that no proper subset meets C1–C5 and S1–S4 and forms a closed strongly connected component.
- Pointer, coordination and decision state are established as maintained state (S1–S4), but not each individually as ablation-necessary at the AC105 body.
- Coordination maintenance is a "state-cleanliness contrast" only (AC87 G6).

**Evidence:**
- `CLOSURE_VERDICT_v1.md` @ `4b85851` §1;
- `AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §5;
- `AC87_RESULTS_v1.md` @ `dc3e428`.

**Exact missing test** (mostly analytic, then a small causal table):
1. An exhaustive check over the declared production graph that no proper subset is a closed strongly connected component with no external root. This is graph work, no simulation.
2. A leave-one-out ablation per maintained-state item at the AC105 body, with a declared functional endpoint (reconstruction completion or income) rather than survival alone.

**Simplest rival.** *A smaller autocatalytic sub-network* (ALife: a minimal autocatalytic set). For example, the W/C/B production loop with the description treated as passive storage.

**Relevance: MEDIUM.** It delivers Track A's "minimal organization" item and could demote an item from necessary to optional. The closure verdict is unaffected unless a necessary component turns out to be removable.

**Stopping criterion.** Stop if step 1 shows the strongly connected component is already minimal and every S-item has an existing ablation. Then record "minimal within the declared component list".

### U6. Clause (ii): whole-organism unity (non-spatial informational core)

**What is open.**
- Clause (ii) is NOT ESTABLISHED: met only at the material layer.
- The "sole remaining genuine limitation" is the non-spatial informational core.
- The finite successor requirements R1–R4 and tests T1–T5 are specified. The S1 spec and its protocol are "AWAITING separate execution authorization".

**Evidence:**
- `A0_AUTONOMY_VERDICT_v1.md` @ `eb79ecb` §4–§6;
- `S1_SPATIAL_SUCCESSOR_SPEC_v1.md` @ `eb79ecb`;
- `I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md` @ `eb79ecb` (c);
- ledger O4 = NOT_ESTABLISHED.

**Exact missing test.** A0 T1–T5:
- T1: localized-read ablation and endogenous restoration;
- T2: retention vulnerability, with a transport-exempt contrast arm;
- T3: mid-function production block plus machinery-only rescue;
- T4: two directed cuts with separable effects;
- T5: observer-discard with exactly one copy.

The falsification clauses are A0 §6 (i)–(iii).

**Dependency flag.** It needs a new component class. The status file calls it "a re-architecture of the supplied physics", so it requires approval under the "no new architecture family" rule.

**Simplest rival.** *External coordination through a declared non-spatial host array*: the informational core is ordinary host memory that space and boundary never touch.

**Relevance.** YES for the full two-clause autopoiesis verdict, which would move from NOT ESTABLISHED for the informational core. NO for any neural or Track B architecture: the mission audit says "NO — defer to the ALife paper".

**Stopping criterion.** Do not start without explicit authorization. If started, stop at the first prespecified falsification clause.

### U7. Economic viability of the internalized decision state

**What is open.**
- AC96: the internalized streak is paid, and in the move world it is starved by the income collapse it exists to pre-empt. The maintained arm relinquishes 2/8 against the host's 8/8, and 6/8 die. The status file calls it "the new open item".
- AC104/AC105 show the allowance economics are seed-dependent: allowance 33 vs 42, the 5804 rescue and the 5603 harm.

**Evidence:**
- `AC96_RESULTS_v1.md` @ `d7925cf`;
- `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`;
- `CLOSURE_VERDICT_v1.md` @ `4b85851` §5.

**Exact missing test.** An analytic affordability bound: the expected cost of maintaining the decision state against the income it protects, across the declared challenge grid. Then one frozen run only if the bound is not decisive.

**Simplest rival.** *A host-side counter* (external coordination). It is economically better on record: the host relinquishes 8/8 against the maintained arm's 2/8 (`AC96_RESULTS_v1.md` @ `d7925cf`).

**Relevance: LOW for closure** (K3 §5: "Robustness limits are NOT redesign requirements"). Medium for the level-(b) robustness claim.

**Stopping criterion.** Stop at the analytic bound if it is decisive.

### U8. Survival-level composition (AC115 G4–G7; AC68 bimodality; AC39 transfer)

**What is open.** Survival-bundled gates fail on a minority of seeds through early W/C collapse, puncture W/C leaks, and one particle leak.

**Evidence:**
- `AC115_ERRATA_v1.md` @ `e2e2ac6`;
- `AC68_RESULTS_v1.md` @ `6df811b` (rows in PR #3);
- `AC39_ENGINEERING_v1.md` @ `685642f`.

**Exact missing test.** A bimodality-aware survival protocol with a pre-registered lower-bound gate on a disjoint seed family.

**Simplest rival.** *Seed-dependent bistability* (dynamical systems): W/C bimodality with two attractors, and a basin selected by the seed.

**Relevance: LOW.** It would not change F1 or S4; the mission audit calls it "a known wall".

**Stopping criterion.** Do not pursue. Reopen only if a closure claim comes to depend on survival.

### U9. Robustness of PR #9's Q-CAUSE label to additional control draws

**What is open.**
- The REPLICATED label is at exactly 8/10. Each failing seed lost to one isotropic draw.
- Protocol-mandated sentence: "robustness to additional draws is untested".

**Evidence:**
- `first_order_control_results_v1/PHASE_B_RESULTS_v2.md` @ `4f6fc4c`;
- `first_order_control_protocol_FINAL.md` @ `4f6fc4c` §6.1.

**Exact missing test.** A new pre-registered confirmatory study on fresh seeds with more draws per family (for example 128), the same joint rule, and the B5 default bar (8/10, with UNRESOLVED above two invalid seeds) frozen in its own protocol. Not a reanalysis.

**Simplest rival.** *Order-statistic variability* of the maximum over a finite set of random control draws (sampling). The label could move with more draws, without any change in mechanism.

**Relevance: MEDIUM.** It could weaken the bounded Q-CAUSE entry. It cannot touch Q-NECESSITY or closure.

**Stopping criterion.** Run only if a downstream claim relies on Q-CAUSE strength. Otherwise keep the qualifier.

### U10. W-REL exact check (approved and currently running; results pending)

**Status.**
- **Approved by Aidan at 8:58 AM ET, 2026-10-21**, with the verbatim answer "Yes, approve the theory-only study".
- Recorded in `/workspace/review/c4_reliability_APPROVAL_RECORD.md`. File verified present: 1423 bytes, sha256 `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`.
- **Currently running**: a cloud agent is implementing and running it, as relayed by the Specialist.
- **Results pending. This triage did not touch the check, its implementation or its outputs.** Progress and the implementation manifest are UNVERIFIED here.

**Evidence:**
- `/workspace/review/c4_reliability_APPROVAL_RECORD.md`;
- `/workspace/review/c4_reliability_exact_check_spec_FINAL.md` (sha256 `ae626b65…adef`);
- `/workspace/review/c4_reliability_assessment_admission_v3_2.md` (sha256 `f35b6f9d…4207`).

**What resolves it.** The six frozen outcome labels per setting (spec §4.5). None is a C4 or consciousness claim.

**Simplest rival.** *The battery's own named count-based and policy-only analytic agents* (counting / filtering): R-CONF-A, R-BLIND/R-CONF-S, R-CG counts, R-HAC-MF, and the policy-minimized PM-ACT.

**Relevance.** Track B (C4 admission) mainly. For Track A it is LOW: it bears on whether an assessment role separates from the named analytic rivals. A **PATTERN REPRODUCED BY NAMED CONTROL** outcome would add a REDUNDANT entry.

**Stopping criterion.** As frozen in the spec: the hard cap of 4 h total and 1 h per item, and no in-place horizon cuts.

### U11. AC116 storage question (suspended at the resolution floor)

**What is open.**
- Maintained counter vs a tuned memoryless rival: exact sign-flip p = 0.0625 with n = 8, which is the floor of the test.
- 0 seeds worse, 5 better, 3 tied.
- "Suspended — not closed, not demonstrated".

**Evidence:**
- `AC116_ERRATA_v1.md` @ `e2e2ac6`;
- `AC116_RESULTS_v1.md` @ `3ebccdf`.

**Exact missing test.** A larger independent seed family (n ≥ 10 gives a floor below 0.05), with a pre-registered clean readout-only intervention (AC116 errata §2).

**Simplest rival.** *A tuned memoryless reactive policy* (RL / control), which nearly ties on record.

**Relevance: LOW.** S0 records it as "not a license for further storage-comparison runs", and the mission audit says it "would not move the architecture".

**Stopping criterion.** Do not pursue.

---

## 5. Caveats (in full)

1. **UNVERIFIED items.**
   - **S12:** the comparison E2 uses to exclude the readout-only rival was not re-read.
   - **U10 / B4:** W-REL progress, implementation manifest and results are not inspected.
   - **Row level:** numbers quoted from repo documents (gate counts, seeds, p-values) were read from those documents, not re-derived from rows. They are UNVERIFIED at row level, except PR #8, #9 and #10, which earlier independent reviews recomputed from committed artifacts.
   - **Economy figure:** the mission audit's "≈25×" economy figure is quoted, not re-traced.
2. **PR #3 re-audit limit.**
   - Commit `d0ee2bb` (2026-10-02, 11:38 PM ET) deleted the frozen rows of 26 result directories from master, including AC67, AC68, AC71, AC75, AC76, AC79 and AC80.
   - PR #3 (head `efceef3`) restores them. All 78 paths are blob-identical to `d0ee2bb^`.
   - Until PR #3 merges, the AC75 and AC79/AC80 row-level evidence (F5, S6, R1) cannot be re-audited from master alone.
   - Separately, the `/workspace/repo` working tree shows 15 tracked `__pycache__` `.pyc` files deleted. This triage did not cause that and did not repair it.
3. **Q-separation lock.** None of the following upgrades another:
   - Q-EXIST: an exact or supplied solution exists.
   - Q-LEARN: acquisition or transfer.
   - Q-CAUSE: intervention-based causal contribution.
   - Q-NECESSITY: requires a bound or a complete search within a declared restricted class.

   Organism results shown by ablation are "within-model ablation dependence", never Q-NECESSITY.
4. **W-REL pending.**
   - Approved by Aidan at 8:58 AM ET on 2026-10-21. The record is `/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`.
   - It is currently running, as relayed by the Specialist.
   - Results are pending. The triage did not touch it.
5. **Claim ceiling.** No C4, C5 or consciousness claim is made or implied anywhere. W-REL outcome labels are not C4 claims. Production closure is bounded to the declared model, operating range and substrate convention; it is not "autopoietic" unqualified and not "alive".

## 6. Pointer: Track B test pack (full file, Appendix B1–B7)

The full v1.1 appendix gives the portable Track B falsification tests, with exact rules and file refs:
- **B1:** graded-reversion AUC directional rule (PR #8).
- **B2:** conjunctive FO + ISO matched controls, with the thin-margin sentence (PR #9).
- **B3:** the R-FIX freeze-and-compensate rules and the dual-evaluator rule, as seven byte-exact excerpts of `frozen_recurrent_compensation_protocol_FINAL.md` @ `0329818`. Track B ranks this test most important.
- **B4:** W-REL named-rival battery, labelled **METHOD ONLY, RESULTS PENDING**.
- **B5:** the 8/10 replication bar and "more than two invalid seeds = UNRESOLVED", stated as **defaults that each Track B study must freeze in its own protocol**, not universal rules. The PR #8, #9 and #10 wordings are frozen instances only.
- **B6:** organism-lineage tests: T-RIVAL, T-INTERRUPT, T-OBS, T-INERT, T-SCRAMBLE, T-DIRECT, T-REACQ, T-RESTORE.
- **B7:** the Q-separation lock.
