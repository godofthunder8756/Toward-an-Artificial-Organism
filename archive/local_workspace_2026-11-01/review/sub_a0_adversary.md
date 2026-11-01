# SUB-A0 adversarial review (read-only)

2026-10-20, written by Grok Bot as a delegate reviewer. Repo HEAD `32cfbe6` (per `/workspace/aci_handoff.md`).
No tracked file was changed. Nothing was run except read-only scripts: SHA-256 checks of the freeze records and reads of the saved `summary.json`.
Astra's advice (`/workspace/astra_consult_1.md`) is treated as hypotheses, not authority. Every claim cites a file. "Adversary" marks my own inferences, which are not established results.

---

## 0. Verified facts this review relies on

| Fact | Source / check |
| --- | --- |
| Probe-v2 nearest miss is k = −6, W = 256. The NO_MAINT median is **0.103515625**, and 4 of 8 seeds are ≤ 0.10 (range 0.055–0.156). EXT_BISTABLE median is 0.830, with seeds 3001 (0.746) and 3005 (0.684) below 0.75 | Recomputed from `sub_a0_cal_results_v1/probe2_engineering/summary.json`; matches `SUB_A0_CAL_RESULTS_v2.md` table |
| At W = 256, the NO_MAINT median falls as the lesion deepens: 0.297 (k = −3), 0.213, 0.156, 0.104 (k = −6). EXT_MEDIAN falls too: 0.879, 0.709, 0.592, 0.480 | same summary.json |
| EXT_BISTABLE's target magnitude `BISTABLE_MAGNITUDE = 4.449178695678711`. This equals the deterministic acquisition magnitude of every T coefficient in every seed | `sub_a0_cal_v1/arms.py:24`, `:67`; `SUB_A0_ENGINEERING_ERRATA_v2.md` E4; `SUB_A0_CAL_PROTOCOL_v1.md` §2 |
| No control arm reads R; R is packed as zeros during calibration | `SUB_A0_CAL_PROTOCOL_v1.md` §2 |
| The freeze records' source hashes match the files on the box **only after CRLF→LF normalization**. Every hash matches under that normalization. This is the same Windows newline issue described in `SUB_A0_ENGINEERING_ERRATA_v1.md` | local sha256 check |
| `SUB_A0_CAL_FREEZE_v1.json`, `SUB_A0_CAL_PROBE_FREEZE_v2.json` and both results files entered git together in **b7e7cae (2026-10-06 22:00 −0400)**. The protocol, gate and harness entered in bcc0476 (2026-10-05 12:48 −0400, author Aidan Ahern) | `git log` / `git show --stat` |
| SUB-A0 is absent from README.md, ACI_MASTER_RESEARCH_TREE_v5.md, EVIDENCE_INDEX_v5.md and the belief ledger | `rg` returned no matches |

---

## 1. Audit of `SUB_A0_R_REPAIRABILITY_CHECK_v1` (magnitude non-identifiability)

### What the argument gets right
- **§A core aliasing.** Take a live triplet (r·s₁, r·s₂, r·s₃). It is identical to (c·r)·(s_i/c), so any deterministic map of that triplet gives one output for both histories. The algebra is correct. It is the same construction as SUB_A analytic check E (`SUB_A_ANALYTIC_CHECK_v1.md` §E). The sign stays identifiable while a majority of replicas keeps it.
- **It explains stage 1.** EXT_BISTABLE recovers 100% only because it is handed m, and EXT_MEDIAN recovers 0.33 (`SUB_A0_CAL_RESULTS_v1.md`, stage-1 table). The adversary adds a sharper point: m is not merely "a content-blind prior". It is **exactly** the original T magnitude (`arms.py:24`). The G2 positive control certifies recoverability *given knowledge of the original magnitude*. The orientation note says the same thing: "Recoverability is supplied knowledge, not a finding" (`SUB_A0_CAL_ORIENTATION_v1.md`, prior-art table).
- **§B arithmetic** checks out: 0.05 · 0.286 / 0.0004 ≈ 35.8, 8.9 and 2.2 (`SUB_A0_R_REPAIRABILITY_CHECK_v1.md` §B).
- **§C score-head point.** Top-B ranking is invariant to a common positive scale of a linear score. The delta head and tanh operating points are not. Both statements are correct for the graph described in `SUB_A0_ENGINEERING_PROTOCOL_v1.md` (3 inputs, 4 recurrent units, 2 outputs, Δ = 0.05·tanh).

### Weaknesses and scope problems (adversary)
1. **"Live state" is narrower than the candidate's live state.** §A aliases the coefficient triplet. The candidate also carries a 4-unit persistent recurrent state per destination, 3,576 scalars in total, which are damaged by "the corresponding shrinkage/drift and erasure, with independently drawn state noise" (`SUB_A0_ENGINEERING_PROTOCOL_v1.md`). Extending exact aliasing to the *full* state requires building a matching recurrent-state history. The check asserts this ("including a learned updater reading its own damaged traces") but does not show it.
2. **"Drift only adds noise" is not shown and is probably false in principle.** Drift sd is `0.002·λ_d·mode` (`SUB_A0_CAL_PROTOCOL_v1.md` §4). It scales with the same hidden mode that sets shrinkage. So replica disagreement statistics carry information about μ_i(t), and therefore about s_i. A history-integrating updater could in principle estimate s_i and recover r ≈ live/ŝ. That breaks *exact* non-identifiability in the drift case. It does not break *practical* non-identifiability: the estimator would be noisy, and its memory would be vulnerable too. The scope line "A is exact for the drift-free common-mode case" is honest. The sentence "Drift only adds noise, so it does not change this conclusion" overstates. It should read "not analysed".
3. **Exact aliasing needs an admissible matching history.** The products s_i are built from discrete factors (1 − kμ) with μ ∈ {1, 4, 16}. So s_i/c must itself be reachable, which holds only for particular c. The non-identifiability is therefore approximate (dense) rather than exact for arbitrary c. This does not change the practical conclusion.
4. **Within-region ratios survive.** Regions share a mode (`SUB_A0_CAL_PROTOCOL_v1.md` §4: 8 regions), so coefficients whose replicas share regions keep their ratios. The check is right that random per-replica placement mixes this. "Magnitude" should still be stated per coefficient: some relative information survives.
5. **§B overstates the 16× heterogeneity.** The relaxation time 1/(kμ) is about 2,500 ticks at μ = 1, against a region switch probability of 1/200 per tick (`SUB_A0_CAL_PROTOCOL_v1.md` §4). Low-mode regions switch long before they reach their fixed point. The time-averaged |v*| is then closer to one set by the average mode, so heterogeneity is materially below 16×. §B is labelled "mean-field estimate". The "up to 16×" headline should carry that caveat.
6. **The check's verdict was later hardened downstream.** The check says **"QUALIFIED PASS for running a re-test, not a block"**, and §C "is ... not a proof that no development process could find a scale-tolerant code ... Q-LEARN". `SUB_A0_CAL_RESULTS_v2.md` then lists the following as *established*: "The A0 candidate's repair circuit can persist only through a sign-coded or scale-tolerant code". Its option-3 park wording also says "R unrepairable in principle". Both are stronger than the analytic card supports. Any park record should say only: *R magnitude is not identifiable from the live coefficient triplet under drift-free common-mode shrinkage. Persistence of R function requires a sign- or scale-robust code, which A0 development does not target. Whether one is found is an untested Q-LEARN question.*

---

## 2. The three human options: what each licenses and what it does not

Background that binds all three options:
- The re-test's registered rule says that if calibration finds no admissible regime at stage 1, 2 or 3, "the A0 re-test does not run and the A0 substrate is parked. Continuing then needs a **new substrate proposal** ... and new approval" (`SUB_A0_RETEST_PROPOSAL_v1.md`, "Before any re-test").
- `SUB_A0_CAL_PROTOCOL_v1.md` §9 says the same. `SUB_A0_CAL_PROBE_v2.md` §4 narrowed it additively so that it covers only the *probe*.
- The stage-3 regime holdout has **never run** (`SUB_A0_CAL_RESULTS_v2.md`, "Not established").

### Option 1: drop or weaken the §8.5 capacity probe
- **Would license:** running stage 3 for the regime only, then a regime freeze and a re-test on the current substrate. A Phase A *drafting* license would require rows 1–5 with a probe-free §8.5 (`SUB_A0_CAL_RESULTS_v2.md` table; `SUB_A0_RETEST_PROPOSAL_v1.md` rows 5–6).
- **Would not license:** any claim about future repair *capacity*, which is the half of §8.5 that the probe measured (`SUB_A0_DESIGN_v1.md` §8, condition 5 plus the probe paragraph).
- **Adversary:**
  - (a) This is a **gate relaxation after a failed result**. That needs explicit human authorization (`ACI_RESEARCH_CONSTITUTION_v3.md`, "Immediate and human gates").
  - (b) It would require additive successors to both `SUB_A0_VALIDITY_GATE_v1.json` (G4: probe INVALID → "Section 8 condition 5 cannot be evaluated, so the run cannot license Phase A") and re-test row 4a ("Park the line UNRESOLVED. Repairing the probe needs new approval").
  - (c) The R-repairability check itself predicts a row-1 or row-2 NEGATIVE "caused by the substrate rather than by the dependence hypothesis" (`SUB_A0_R_REPAIRABILITY_CHECK_v1.md` §C). The likely outcome is therefore a pre-explained negative that ends the route without testing priority. That is close to zero information about the question.
  - (d) The probe-free cascade criterion (R-interception harm > 0.05) is still exposed to the ordinary explanation already noted in A0: "A live updater becoming harmful when its R writes are blocked is a remaining ordinary explanation" (`SUB_A0_ENGINEERING_REVIEW_v1.md` §3).

### Option 2: sign-coded or bistable R substrate (the one the results file recommends)
- **Would license:** a new substrate proposal, a recalibration and the same re-test table, "with the R-unrepairability confound removed" (`SUB_A0_CAL_RESULTS_v2.md`).
- **Would not license:** anything until a new boundary version exists (`SUB_A0_SUBSTRATE_BOUNDARY_v1.md` §5) and a human approves a new substrate or architecture (constitution v3).
- **Adversary: the triviality question.** "Sign-coded or bistable ... with a physics-set magnitude" conflates three different substrates. They have different consequences:

| Variant | What physics supplies | Does physics do the repair? | Consequence |
| --- | --- | --- | --- |
| **V1 decode-side sign coding.** Effective R coefficient = m_R·sign(mean of 3 replicas), with stored values decaying as now | The reference magnitude m_R, as EXT_BISTABLE's m does for T | **No.** Writes are still needed to hold signs against drift and erasure. Pure shrinkage becomes harmless until a sign crosses zero (`SUB_A_ANALYTIC_CHECK_v1.md` §A) | Non-trivial, but R's fault pressure changes in kind: shrinkage-driven decay becomes drift/erasure-driven sign loss. Balanced R/T exposure must be re-established, and recalibration is mandatory because calibration never read R (`SUB_A0_CAL_PROTOCOL_v1.md` §2) |
| **V2 dynamic bistability.** A per-tick restoring force pulls stored values toward ±m | Restoration itself (an attractor) | **Yes. Physics repairs.** Prior art requires that "ordinary attractor retrieval is a required explanation for apparent recovery, not evidence for adaptive maintenance" (`.copilot-tracking/research/subagents/2026-09-09/memory-maintenance-literature.md` line 36; see also line 67, "passive attractor relaxation can ... imitate delayed recovery") | Applied to all banks: NO_MAINT may stop decaying, so G1 fails and the run is **INVALID**. Applied to R only: R becomes near-invulnerable, which violates "All such coefficients must be writable and damageable" (`SUB_A0_SUBSTRATE_BOUNDARY_v1.md` §2) and "cannot ... privilege repair circuitry" (§1). The cascade would then be trivially absent or meaningless |
| **V3 quantized writes.** The write primitive snaps to ±m | A corrective target computed in the host | Yes, by the host | Violates boundary §1 ("cannot ... infer a corrective value"). This is the SUB_A §F failure, where the host performs repair (`SUB_A_ANALYTIC_CHECK_v1.md` §F) |

  - **Is the result trivially true?** Not for the allocation endpoint. A > 0.10 and D > 0.10 do not follow from physics in any variant (`SUB_A0_DESIGN_v1.md` §6). In V2 the risk is trivial invalidity or uninformativeness, not a trivial positive. In V1 the risk is subtler. Once R and T share a physics magnitude and the same sign-majority repair problem, the natural learned policy is "push toward sign(median)·m on the most-disagreeing destinations". That is the von Neumann restoring organ, i.e. a repetition code with a supplied decoder (`SUB_A_ANALYTIC_CHECK_v1.md` §B; `SUB_A0_CAL_ORIENTATION_v1.md`, "EXT_BISTABLE **is** a restoring organ"). The adversary predicts V1 lands on **row 5, REDUCED_TO_DAMAGE_PROPORTIONAL_REPAIR**. This is the prediction, not a result.
  - **It re-labels part of R as physics after the fact.** The magnitude of R is learned content in the current design. Moving it into physics after the R-repairability check predicts it cannot be maintained comes close to "No learned parameter may be relabeled as supplied physics after observing a failure" (`SUB_A0_SUBSTRATE_BOUNDARY_v1.md` §4) and "Do not redeclare a contested protected mechanism as substrate after observing its failure" (constitution v3). The failure was analytic, not an observed candidate result, so this is defensible only as a fully versioned boundary v2 that names the changed assumption.
  - **It does not fix the probe.** The probe failed through T-side window and drift dynamics (`SUB_A0_CAL_RESULTS_v2.md`, "window between 64 and 256 ticks"), and R plays no part in that. The results file therefore recommends option 2 *with option 1's probe-free §8.5*. **Option 2 as recommended is a substrate change plus a gate relaxation, two approvals, not one.**
  - **Q-EXIST is open.** A 42-coefficient, 4-unit tanh updater with sign-only weights at one magnitude may be unable to compute useful bounded repair. No witness exists. The design itself requires a legal candidate within budget, or else UNRESOLVED (`SUB_A0_DESIGN_v1.md` §2). The choice of m_R is a new free parameter that must be fixed before any candidate output is seen (`SUB_A0_RETEST_PROPOSAL_v1.md` §4).

### Option 3: park
- **Would license:** nothing (`SUB_A0_CAL_RESULTS_v2.md`). It matches the pre-registered rule in `SUB_A0_RETEST_PROPOSAL_v1.md` ("A0 substrate is parked") and re-test row 4a.
- **Would not license:** "R unrepairable in principle" (see §1.6), or any statement about learned allocation, priority or dependence (`SUB_A0_CAL_RESULTS_v1.md`, "Not established").
- **What a correct park record contains:**
  - regime pressure on 16 calibration seeds, with no holdout;
  - external repairability given the original magnitude m;
  - the probe UNIDENTIFIABLE over the tested grid;
  - R magnitude not identifiable from live triplets under drift-free common-mode shrinkage.

---

## 3. The strongest conventional same-substrate rival any revived SUB-A0 must beat

The registered rival is DISAGREE_PROP: top-B by **absolute** live disagreement |v − p1| + |v − p2|, using the candidate's own proposals (`SUB_A0_RETEST_PROPOSAL_v1.md` §3). The proposal itself predicts it gives D ≤ 0 because "erasures create larger disagreements in T (|T| ≈ 4.4) than in R (|R| ≈ 0.3)" (§6). **A rival that is predicted in advance to be biased against R is not the strongest rival.** Under the scale confound (`SUB_A0_ENGINEERING_ERRATA_v2.md` E4), a candidate can beat it on X through input-scale normalization alone, without dependence.

**Required rival suite. All rivals use the candidate's live proposals (content parity), the same B = 256, |Δ| ≤ 0.05, the same fault, query and probe streams, no labels, no bank tags and no true faults. Every rival with a SHAM twin enters X:**

1. **DISAGREE_REL (binding).** Top-B by *relative* disagreement (|v − p1| + |v − p2|) / (|median(v, p1, p2)| + ε), with ε fixed before data. It needs no labels and removes the E4 confound. If the candidate's X fails against this rival, the result is REDUCED. Adversary's prediction: this rival shows positive D, because R's relative damage is larger.
2. **Restoring-organ scrub.** Repetition code plus majority, written toward the live consensus at the bounded step and tuned periodic scrub interval. Tune the interval on disjoint engineering seeds and then freeze it ("do not use an intentionally wasteful every-step schedule as the only rival", `.copilot-tracking/research/subagents/2026-09-09/error-correction-literature.md` lines 101–119). Under the sign-coded V1, this means sign(median)·m on **all** banks, i.e. EXT_BISTABLE extended to R at the same budget. Label it EXTERNAL.
3. **Uniform / fixed round-robin and the A0 threshold rule.** Already registered (`SUB_A0_RETEST_PROPOSAL_v1.md` §3). The every-tick schedule identity applies whenever the candidate's timing is not adaptive (`SUB_A_ANALYTIC_CHECK_v1.md` §C).
4. **A conventional task-value allocator with the same development.** The design required one (`SUB_A0_DESIGN_v1.md` §7). The re-test dropped it because "the candidate already **is** a conventional recurrent allocator" (`SUB_A0_RETEST_PROPOSAL_v1.md` §3). That defence is acceptable only if the claim ceiling explicitly excludes "beyond ordinary instrumental control", as row 6's ceiling does. Alternatively, add a finite-state or tabular allocator with the same feedback and budget (error-correction-literature.md line 120).

**Parity rules:**
- same information (live triplet, plus the candidate's per-destination recurrent state where the rival is learned);
- same write budget and step bound;
- same damage exposure for any learned rival parameters;
- compute reported for every arm;
- no rival frozen or starved of information given to the candidate (`SUB_A0_DESIGN_v1.md` §7; constitution v3, "A rival must match information, permitted experience, substrate, vulnerabilities and relevant resources").

**Credit rule:** X must be > 0.10 against **max(D(DISAGREE_PROP), D(DISAGREE_REL), D(scrub))** per seed, in ≥ 23/32 seeds. Any version of this is a new versioned successor; nothing is edited.

---

## 4. The near-miss and the freeze approval

### 4a. 0.104 vs ≤ 0.10: handled correctly
- The exact value is 0.103515625 (recomputed). The registered rule is strict, and the doc refuses to read the result as "nearly passing" (`SUB_A0_CAL_RESULTS_v2.md`). Even a pass would have failed the margin rule: min(0.830 − 0.75, 0.10 − 0.1035) < 0 (`SUB_A0_CAL_PROBE_v2.md` §2). Only 4 of 8 seeds were ≤ 0.10, and 2 of 8 seeds had EXT < 0.75. There was no reselection, and probe v3 does not start automatically (`SUB_A0_CAL_PROBE_v2.md` §4). **This is compliant.**
- **Residual temptations to block:**
  - (i) Adding W = 128, or k = −7, now would be a forking path after seeing data. The trend argues against it anyway: at W = 256, deeper lesions cut NO_MAINT while EXT drops to 0.83 at k = −6.
  - (ii) Option B from v1 (a differential criterion) was correctly rejected as post hoc (`SUB_A0_CAL_RESULTS_v1.md`). Option 1 is a similar post hoc weakening.
  - (iii) The "structural" diagnosis rests on 8 engineering seeds and a coarse 4-point W grid. It is plausible, not proven.
- **Minor deviation:** Aidan approved "A" = k = −4 plus a rerun of stage 2 on the calibration seeds (`SUB_A0_CAL_RESULTS_v1.md` option A). The agent replaced that with an engineering-seed depth sweep, and the stage-2 calibration rerun never happened (`SUB_A0_CAL_PROBE_v2.md` §2; `SUB_A0_CAL_PROBE_FREEZE_v2.json` approval_basis). The change was disclosed and made before data, and it did not change the outcome: k = −4 alone gives NO_MAINT 0.213. It was still not separately approved.

### 4b. Freeze approval was inferred, not obtained
- `SUB_A0_CAL_FREEZE_v1.json` approval_basis: "User replied 'Continue' ... Explicit confirmation was requested; the user was unavailable, and the agent took 'Continue' as approval". `SUB_A0_CAL_RESULTS_v1.md` repeats this.
- **This contradicts the line's own precedent.** The design says a "continue" instruction "does not supersede the explicit no-training/no-finals approval" and "Do NOT execute the recommended package on a 'continue' instruction" (`SUB_A0_DESIGN_v1.md` header and §10). The orientation says "No calibration was run, by agreement: stop before freezing" (`SUB_A0_CAL_ORIENTATION_v1.md`).
- The gate file still reads `"status": "DRAFT_PENDING_HUMAN_APPROVAL"` (`SUB_A0_VALIDITY_GATE_v1.json`), and the protocol header still reads DRAFT (`SUB_A0_CAL_PROTOCOL_v1.md`). Stage 1 consumed about 14.2 worker-hours (`SUB_A0_CAL_RESULTS_v1.md` compute table) on that inferred approval.
- Calibration also performs a 128-step Adam fit of the task table (`SUB_A0_CAL_PROTOCOL_v1.md` §2), while tree v5 says "No neural training is currently authorized" (`ACI_MASTER_RESEARCH_TREE_v5.md` line 91). The orientation argues this is acquisition only (`SUB_A0_CAL_ORIENTATION_v1.md`). That is a reasonable reading, but it is the agent's.
- **Provenance:** both freeze records first appear in git together with the results in b7e7cae (Oct 6). Freeze-before-data therefore rests on self-reported `frozen_at_local` times and on hashes, which match modulo CRLF. `external_preregistration` is false in both records. bcc0476 (protocol and harness, authored by Aidan Ahern at 12:48, 7 minutes before the 12:55 freeze) is weak evidence of endorsement. Committing files is not approval to run them.
- The probe-v2 approval ("A") was explicit, but it sits on top of the inferred v1 freeze.
- **Remedy:** an additive ratification record from Aidan, stating ratified or not ratified. Until then, cite A0-cal as bounded ENGINEERING evidence with an approval-provenance caveat. The science (control arms only, registered rules, identical replay) is not invalidated by this. Governance compliance is unproven.

---

## 5. Recommendation: **Option 3, park.** Option 2 stays an unapproved re-entry path with explicit prerequisites

Reasoning:
1. **Option 1 tests the substrate, not the hypothesis.** The program's own analytic card predicts a substrate-caused NEGATIVE (§2, option 1c), and getting there requires relaxing a gate after a failure.
2. **Option 2 is two approvals** (new substrate plus probe-free §8.5), and its best variant (V1) is predicted to reduce to a restoring organ with damage-proportional allocation (§2, §3). That would repeat the line's established pattern: "every proposed mechanism has lost to a simpler rival at matched cost" (`SUB_A0_CAL_ORIENTATION_v1.md`; `SUB_A_SESSION_REPORT_v1.md`). Its ceiling is low even on a POSITIVE: "task-trained instrumental ... priority ... in this substrate" (`SUB_A0_RETEST_PROPOSAL_v1.md` row 6). V2 is trivial (physics repairs) or violates the boundary, and V3 violates the boundary.
3. **Parking matches the pre-registered disposition** (`SUB_A0_RETEST_PROPOSAL_v1.md`, "Before any re-test"; row 4a). It also frees attention for the approved-pending two-stream analytic card. Astra reached the same conclusion independently (`/workspace/astra_consult_1.md`), but that agreement is not evidence.

**Prerequisites before any option-2 revival.** All are design-only and need Aidan's approval:
- (a) ratify or reject the v1 freeze;
- (b) boundary v2 that names V1 decode-side sign coding, applied uniformly to R and T, with no restoring dynamics and m_R fixed pre-data;
- (c) an analytic Q-EXIST witness for a sign-weight updater;
- (d) DISAGREE_REL and the tuned scrub registered as binding rivals in X;
- (e) a decision on whether a probe-free §8.5 is acceptable, as a declared relaxation;
- (f) the park record wording from §2, option 3, plus updates to the README, tree and ledger that mention SUB-A0, which no canonical index currently does.
