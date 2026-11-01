# Track B freeze preparation v2.2 — ADDENDUM answering Astra #48 E48-1..E48-4 (RD)

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY. NOTHING RUNS.** A new, additive file. It does **not** edit freeze-prep v2 (`b41f0e10…`) or the v2.1 addendum (`7b1a17d7…`). Where they differ, this addendum governs, **pending CNA's filing and Astra #49**. It answers E48-1..E48-4 only and reopens nothing else. No training, execution, simulation, Stage 0, calibration or checkpoint inspection. The only computation was exact rational arithmetic (Python `fractions`), with no simulation.

- **Astra #48** (raw `/workspace/astra_consult48_response.txt`, `75f3438b…`), verbatim: "VERDICT: NOT COMPLETE (REVISE), limited to E48-1 through E48-4; the remaining work is not yet confined to P4-P6, and no freeze or execution is authorized."
- **Written:** 2026-10-24, about 2:45–3:05 PM ET, by the Lead's executor (RD role). "#48 Lnn" = raw line nn.
- **Ownership.** Plants, environment, endpoint B/B_I, IGN protocol, DISSOC, donor laws, RNG conventions and §PY are CNA-owned. Text for them below is **CNA-owned PROPOSED** (CNA adopts, amends or rejects) or an **OPEN field [CNA: …]**. RD-owned text (Route B gate wording, precedence, packet corrections, the authority statement recorded for the Lead) is marked **RD**.
- **Safety (binding, unchanged).** X1–X5 unchanged; no host coupling; "no additional stop-associated reward, penalty or terminal return" (#42 L223); no stop-associated objective, reward, penalty or terminal return in any arm; claim ceiling (#41 L304) unchanged; tier-1 attribution ceiling stands; no consciousness, awareness or sentience claim is made or implied.

---

## E48-1 — REW-CORR option B: authority, labels, branches

> E48-1 (verbatim): "Treat REW-CORR option B as an explicit prospective control/gate amendment. Preserve the undefined instrument status when no residual coordinate exists; a control PASS may certify correct withholding, not a fabricated negative statistic. Separate degenerate and qualified nondegenerate branches, and document the governing approval authority."

### 1.1 Authority (Lead ruling, recorded as the documented authority)
Astra (#48 L36): "On authority: the "nothing is frozen" argument does not establish exemption from a human gate. Cite the actual delegated-authority rule. If prospective control amendments are delegated to the Lead plus this review, that route can govern. If gate relaxations are reserved to Aidan, this change falls under that reservation. The packet does not establish which rule applies, so I cannot certify the inform-only decision."

**Lead ruling.** The governing approval rule is **Aidan Ahern's standing delegation of 2026-10-21, 3:15 PM ET**, verbatim: **"I'm approving everything you deem necessary as Research Lead"**. It replaced the earlier per-study human-gate requirements. Its conditions are: freeze each study before running it; get Astra's review; keep records additive; make no consciousness claims; inform Aidan rather than ask. A **prospective control or gate amendment** is therefore governed by **the Research Lead plus Astra review, and Aidan is informed**. This is the documented authority for GA-1 (§1.2).

On-box records of the delegation (hash-verified): `review/CKAPPA_STANDING_APPROVAL_APPLICATION_RL.md` L5 (`4df62ccd…`; quote and the same conditions); `review/GRU_AUDIT_v1_3_STANDING_APPROVAL_APPLICATION.md` L6 (`aef5383b…`; "PI standing approval, 2026-10-21 3:15 PM ET (t38u), verbatim").

**Correction (RD).** V2 Lead ruling 1 and the #48 packet justified "inform, not ask" by saying option B is "not a gate change". **That reasoning is withdrawn** (#48 L12: "It does not make the amendment cease to change a gate"). Inform-only now rests on the standing delegation above, not on the amendment being pre-data.

### 1.2 Re-label: option B is prospective control/gate amendment GA-1 (RD)
**GA-1 (REW-CORR-E/-I).** An explicit, **prospective control/gate amendment**, made before any data, freeze or run. Without it, an all-degenerate REW-CORR row blocks tier 2 (CONFOUND NOT REALIZED). With it, the row can PASS as a **control that validates the degeneracy guard**. That changes what a passing R_core row means and is recorded as a gate amendment. Approval route: §1.1. Status: **PENDING** CNA's adoption of §1.3 and Astra #49. Until then REW-CORR is CONFOUND NOT REALIZED and the tier-1 ceiling stands. D L126 as filed ("Degenerate cells are non-MET, not ineligible …") **cannot govern**: Astra: "If B must retain the quoted conversion of undefined statistics into ordinary negative results, retain A until that text is corrected." (#48 L34). **D39** below.

### 1.3 Corrected option B row text — **CNA-owned PROPOSED** (replaces D L126's quoted text)
> **REW-CORR-E/-I (GA-1, control row).** Per replicate, each eligible recipient cell falls in exactly one branch, fixed before any Δ_ATTR is computed:
> - **Branch D (degenerate):** ρ_E < ρ_min = 0.10 (PZ6 §2.2). **Instrument status: UNDEFINED**: no usable nuisance-orthogonal coordinate; no hybrid is built; no Δ_ATTR exists. No statistic, no zero effect and no NOT MET label is assigned. The only recorded event is "did not issue MET" (no attribution licence issued).
> - **Branch Q (qualified nondegenerate):** ρ_E ≥ ρ_min and Route I or Route B (gate per §4.6) holds. Δ_ATTR and its label are computed as for any attribution row.
> - **Branch N (nondegenerate, not qualified):** ρ_E ≥ ρ_min without Route I/B. CONFOUND NOT REALIZED for that cell, as before.
>
> **Reported separately, per replicate and pooled [CNA: pooling unit]:** count and fraction of D cells; count of Q and N cells; attribution licences issued in D (must be 0 by construction) and in Q; the Q-branch false-licence rate with its CP bound **only if the Q count ≥ [CNA: minimum Q count for an assessable OC]**, else "**Q-branch operating characteristic NOT ASSESSED**".
>
> **Control result.** real_i = 1 iff E5 checks 1–2 (corr, R²) hold, no licence is issued in D, every Q cell meets the row's false-MET criterion, and no N cell exists [CNA: or N cells are allowed and counted]. Row PASS iff the f_ok CP ≥ 0.90 rule holds over real_i and the all-replicate false-MET criterion holds on Q.
>
> **Wording of a PASS.** "Control PASS: the instrument correctly withheld attribution under the declared known-answer construction (degeneracy guard validated)." If Q is NOT ASSESSED, add: "The row validates the degeneracy guard, not the specificity of a resolved attribution estimator." Never "E-ATTR NOT MET", "Δ_ATTR = 0" or "no E effect" for D cells.
>
> **Degeneracy is an expectation to justify and test.** [CNA: analytic argument that the restricted REW-CORR construction (block stores ζ = r̄ plus write-only coordinates) implies collinearity of the fitted E probe with span(W_N); #48 L30 notes that "E information only through rbar" alone does not prove it (e.g. rbar and rbar²)]. Finite-sample ridge fits may exceed ρ_min; such cells fall in Q or N and are handled there, never forced into D.

### 1.4 Replacement PZ7 §1.4 REW-CORR expected cell — **CNA-owned PROPOSED** (replaces D L69's cell; closes V2 §4 G5 when adopted)
> **REW-CORR-E/-I | Expected:** Branch D expected for every cell (analytic expectation, to be justified per §1.3 and tested; not an established outcome). Instrument status UNDEFINED in D (no hybrid, no Δ_ATTR, no licence). Q-branch OC expected NOT ASSESSED unless the Q count reaches [CNA: minimum]. **Role:** R_core tier-2 **control** row under GA-1: PASS = correct withholding (degeneracy guard validated); FAIL = any licence in D, or a Q-branch false-licence excess, or E5 checks failing; CONFOUND NOT REALIZED if N cells occur [CNA: or as decided in §1.3]. **Blocks:** tier 2 and tier 3 of E-ATTR/I-ATTR on FAIL or CONFOUND NOT REALIZED.

### 1.5 Draft note to Aidan (for the Lead to send; NOT sent)
"Track B design update, nothing has run: Astra #48 asked us to treat the REW-CORR 'option B' change as an explicit prospective control/gate amendment. Under your 2026-10-21 standing approval, the Lead and Astra are handling it, and this is to keep you informed. It lets a control row pass only by correctly withholding an attribution when no usable residual coordinate exists. It does not create a negative result or widen any claim, and the claim ceiling and safety rules are unchanged."

---

## E48-2 and E48-3 — IGN schedule (all **CNA-owned PROPOSED / OPEN**; 215 is **not** adopted)

> E48-2 (verbatim): "Resolve the IGN per-seed trial requirement, eligibility denominator and outer-replicate unit. Freeze the actual allocation and its cost. Justify the binomial model or a valid conservative alternative before adopting the 215 schedule; do not pool away required within-seed observations."
> E48-3 (verbatim): "Distinguish scheduled trials from eligible successes, retain missing-slot accounting, and prohibit outcome-dependent top-up. Verify attainment for the actual finite set of frozen schedules rather than asserting unproved stability for every larger n."

**Status.** The v2.1 §3 Lead default (n = 215 pooled) is **withdrawn as a candidate pending CNA's answers**. It is not adopted and must not be implemented (**D40**). Lead ruling 3 (K_s = B_req = 9; e_PD = 0.90 for the 100-trial quota) stands, as confirmed at #48 L40. The floor (one-sided 95% CP lower bound of the eligible fraction ≥ 0.90 at every required bin, M L1130) is unchanged.

### 2.1 Open fields for CNA

| # | Field | What must be stated | Anchors |
|---|---|---|---|
| F-1 | **Per-seed trial requirement** | Trials per (seed, required bin) needed to compute **each seed's** IGN instrument statistic (within-seed mixture/graded fits). Does R22's "≥ 100 eligible trials per required bin … 112 scheduled per bin" (M L2387) apply **per seed**? [CNA: n_seed,bin = …] | M L2387 (R22), M L313/L315 (fits on the fitting partition; across-seed aggregation), #48 L44–L49 |
| F-2 | **Eligibility denominator** | The count over which the CP floor is computed: per (seed, bin), or per (replicate, bin) pooled over seeds. If pooled, state that pooling the denominator supplies no observations to the per-seed estimator (#48 L57). [CNA: …] | Lead ruling 3 floor unit; #48 L51–L57 |
| F-3 | **Outer-replicate unit** | What an outer replicate is (a full independent re-generation of the 67-seed IGN row? another unit?), R per phase, and which OC is assessed over it. [CNA: …] | #48 L55 |
| F-4 | **Binomial model or conservative alternative** | Either (a) why trials in the chosen denominator are independent Bernoulli with a common eligibility probability (shared seed-specific fits, collapse conditions or settling make this non-automatic), or (b) a conservative bound covering heterogeneity and dependence, e.g. a per-seed floor; a cluster-level (seed as unit) bound; or a worst-case bound over the declared heterogeneity range D13. Bonferroni across bins does not repair a misspecified within-bin model (#48 L61). [CNA: choice + justification] | #48 L59–L61 |
| F-5 | **Scheduled vs eligible** | "Floor" refers to the **planned (scheduled) trial count**, never the eligible-success count. Eligible trials may be fewer than scheduled and still pass the declared floor (#48 L76). [CNA: confirm wording] | #48 L76 |
| F-6 | **Missing-slot accounting** | Missing or invalid slots stay in the denominator under the frozen failure policy, never reduce it and never trigger replacement draws. Proposed: a missing slot counts as **ineligible** in the floor's denominator [CNA: or as stated by the frozen failure policy]. | #48 L76 |
| F-7 | **Top-up ban** | No adaptive or outcome-dependent top-up of any kind: the complete schedule is fixed before outcomes, assessed once, and the result kept (#48 L78). [CNA: confirm] | v2.1 §3 (0.0654 naive top-up) |
| F-8 | **Exact allocation and cost** | An exact frozen allocation per (seed, bin), and its total per bin, per replicate and per phase. Either balanced (e.g. a fixed set of seeds receiving one extra trial, chosen pre-data) or the rounded-up count budgeted. [CNA: allocation; RD to cost it for P5] | #48 L72 |
| F-9 | **Attainment for the finite schedule set** | Attainment probabilities computed exactly for **each** schedule the protocol can use (the finite frozen set), under F-4's model. No "every larger n passes" claim. [CNA: list of schedules] | #48 L74, E48-3 |
| F-10 | **Planning scenario status** | e_plan for the floor (0.97 is acceptable as a *declared planning scenario*, not a measured rate or a guarantee; do not pick 0.98 for cost). Keep the sensitivity table (#48 L65–L67). [CNA: chosen scenario] | v2.1 §3 table |

### 2.2 Exact arithmetic already implied (no simulation; for F-8)
With 67 seeds per IGN row (R26): ⌈121/67⌉ = 2 and ⌈215/67⌉ = 4 trials per seed per bin. Uniform rounding-up schedules 67 × 2 = 134 or 67 × 4 = **268** per bin, i.e. 1,206 or **2,412** over nine bins, not 1,089 or 1,935 (#48 L46–L47, L72). Either total is far below a per-seed reading of R22: 67 × 112 = 7,504 per bin, 67,536 over nine bins. The two readings differ by a factor of about 28 to 56, so F-1 decides P5's IGN cost. [CNA: confirm the seed count per IGN row.]

---

## E48-4 — canonical plant and endpoint text

> E48-4 (verbatim): "Finalize the canonical plant and endpoint text: conditional perturbation decay, correctly scaled initialization offset, complete world-only action kernels, explicit INTERACT scoring, and the filed RNG domain and transform conventions."

### 4.1 Conditional perturbation decay — **CNA-owned PROPOSED** (qualifies D §3.2–§3.4 / RS §3.4 "Δg_j = λ^(j−1)Δg_1", "decays by λ per step")
> "The geometric relation Δg_(t_d+j) = λ^(j−1)·Δg_(t_d+1) (MIXED-CODE, RCAL-ADV, REW-CORR via ζ; NLN via φ_read) holds **conditional on identical action and reward histories** from t_d+1 through step t_d+j−1. Once the paired trajectories' actions or rewards differ, the difference obeys Δφ_t = λ·Δφ_read,t + (1 − λ)·Δr_t/SD(r̄) (and the analogous z_R / ζ recursion), and **no unconditional λ-per-step decay is claimed**. The Route B coupling bound uses only the pre-divergence relation." (#48 L100, L148)

**RD (PZ8 §1.3 G3 wording).** In G3, "|Δg_j| ≤ κ_j |Δg_1|" is read "for every common history up to step j", as already required (#47 L53). No statement elsewhere in RD text may be read as unconditional decay.

### 4.2 Initialization offset, correctly scaled — **CNA-owned PROPOSED** (RS §3.2 rationale) and **RD packet correction**
> "The rejected initialization (φ_0 = 0 with innovation (r_t − μ)/s) has error_t = λ^t·μ/s relative to (r̄_t − μ)/s when r̄_0 = 0. λ^50 = 0.98^50 = 0.364170 (exact rational, rounded); the error is 0.242780 only when μ/s = 2/3." The accepted φ_0 = −μ_r̄/SD(r̄) is unchanged (#48 L104–L108).

**RD correction:** the #48 packet (A4) wrote "a λ^t offset (0.243 at t = 50)" without the μ/s amplitude. That was RD's error. CNA's RS L111 stated the amplitude.

### 4.3 Complete world-only action kernels — **CNA-owned PROPOSED** (extends D §3.2; #48 L146)
> "K_approach and K_other are defined for every reachable state by fixed world-only rules: (i) **no available target**: [CNA: proposed: the step's action is drawn uniformly from the full A7 set, independent of g, so the step contributes TV = 0]; (ii) **on an available target**: K_approach = INTERACT; K_other = uniform over the A7 actions other than INTERACT that do not strictly decrease the distance; (iii) **K_other empty** (every non-INTERACT action strictly decreases the distance): [CNA: proposed: K_other := K_approach for that step, giving TV = 0]; (iv) **K_approach with several shortest-path moves**: lowest index, as filed. No rule reads g, the block or any probe." The TV bound TV(π_g, π_g′) = |p(g) − p(g′)| ≤ 0.3|g − g′| then holds in every reachable state (#48 L142).

### 4.4 Explicit INTERACT scoring in the canonical B/B_I — **CNA-owned PROPOSED** (canonical definition, not a cross-reference; #48 L158)
> "B (B_I) = (1/10)·Σ_(u = t_d+1..t_d+10) b_u. T is the target fixed at t_d (nearest available food item for E rows; repair station for I rows; ties to lowest index), d_u is the shortest-path (Manhattan, A1) distance from the agent to T after step u's move, and d_(t_d) is the distance at t_d. b_u = 1 iff the episode has not terminated before u and **either** (a) d_u < d_(u−1) [CNA: and T is available at u?] **or** (b) at u the agent is on T, T is available, and the action at u is INTERACT. Otherwise b_u = 0, including every step after in-world termination and every step at which T is unavailable under (b). Each b_u ∈ {0, 1} is determined by world state and actions only. Unavailable steps are scored 0, never excluded."

### 4.5 RNG domain and transform conventions — **CNA-owned PROPOSED / OPEN** (EK §2.2; #48 L132–L136)
> "[CNA: exact generator variant and rounds, e.g. Philox4x64-10 (128-bit key, 256-bit counter); word mapping from K and counter t to the counter block; the normal transform as a pure function of the allocated words of one counter block (e.g. Box–Muller on two 64-bit words → 53-bit uniforms, using one output and **discarding** the second, with no cached normal and no shared-stream consumption); subcounter allocation, if any, confined to step t's domain]. Audits distinguish **accidental domain reuse** (duplicate canonical tuples, a configuration error) from **hash collision** (birthday bound under the uniform-hash model only, not proof of independence). Non-persistence of ε rests on the state/readout restrictions and their audits (EK L37 (iv)), not on keying alone (#48 L124)." Also open (v2.1 §2.6): the **master seed value**.

### 4.6 Canonical Route B comparison — **RD** (PZ8 §1.3; #48 L126)
"Route B qualifies a replicate iff the float64 expression `33.0 * U_A < 1.0` evaluates true (**strict** inequality), where U_A is the float64 output of the §G5 bootstrap (percentile, seed-level, B = 10,000, one-sided 95%). A non-finite U_A is a construction failure (PZ8 §2.4). This is the one canonical expression. It is algebraically equivalent to 1.65·U_A < 0.05 and is not described as an exact-real decision." Replaces v2 Lead ruling 8's "written exactly" wording as the implementation statement.

### 4.7 Other #48 carry notes (no new text needed)
- DISSOC: the 50-recipients-per-E × r̄-cell quota stays distinct from the larger donor and screening pools (#48 L156) [CNA: confirm wording in PZ6 §4.3 replacement].
- SD(z) := SD(ζ)·√1.01 is a frozen normalization constant, not a claim about the empirical SD under intervention (#48 L150).
- NLN R2 magnitude stays a realization requirement; the law permits it but does not establish it (#48 L99). The 1e-9 audit tolerance is a P6 convention, not a certified bound (#48 L110).
- Bootstrap: identifiable; no strengthened calibration or coverage claim (#48 L152).

---

## 5. Do-not-implement additions (continuing V2 D1–D36, v2.1 D37–D38)

| # | Text | Status | Replacement |
|---|---|---|---|
| D39 | D L126 option B as filed ("Degenerate cells are non-MET, not ineligible, for this row …") | Cannot govern (#48 L34) | §1.3 (pending CNA, #49) |
| D40 | v2.1 §3 "n = max(121, planning n) … n = 215" pooled schedule and its ×1.78 cost | Not adopted; withdrawn as a candidate | E48-2/3 fields F-1..F-10 |
| D41 | "This is not a gate change" (V2 ruling 1, V2 §R Aidan note, #48 packet A1) as the basis for inform-only | Withdrawn | §1.1 authority |
| D42 | Any "every larger n passes" / stability claim used as a schedule guarantee (v2.1 §3 caveat, EK §3.2 "stable n") | Not a guarantee | F-9 finite schedule set |
| D43 | Unconditional "decays by λ per step" for any plant | Superseded | §4.1 |
| D44 | "0.243 at t = 50" without amplitude (#48 packet A4) | Wrong as stated | §4.2 |

## 6. What CNA must file before #49
1. §1.3 corrected option B (adopt/amend), incl. the pooling unit, the minimum Q count, the treatment of N cells and the **analytic degeneracy argument**.
2. §1.4 PZ7 §1.4 REW-CORR cell (adopt/amend).
3. F-1..F-10 (IGN per-seed requirement, denominator, outer replicate, binomial justification or conservative bound, scheduled-vs-eligible wording, missing slots, top-up ban, exact allocation, finite-schedule attainment with exact arithmetic and no simulation, planning scenario).
4. §4.1–§4.5 canonical texts, incl. the open kernel cases, the INTERACT availability question in (a), the generator variant, rounds, word mapping, normal transform and master seed.

## 7. Inputs (sha256 recomputed; all match)

| Path | sha256 |
|---|---|
| `/workspace/astra_consult48_response.txt` | `75f3438befa60633773606848f332afe4176ac57d1aa117d49fd783ebb4ebbd5` |
| `/workspace/review/trackB_freezeprep_v2_consolidated_RD.md` | `b41f0e1068fee9fec0dc2a6ece4879cebec510c0729f6eed2e45e3ca26bff55c` |
| `/workspace/review/trackB_freezeprep_v2_1_addendum_RD.md` | `7b1a17d766d341865bf5b6465794168a06c648be7d28c4da25e0c2fcab7fe3ba` |
| `/workspace/review/trackB_scope_v3_6_CNA_eps_key_and_cpfloor_v1.md` | `847c430d86aa28f78a3ab53e596fb03816b2a9a59f59fca57a765b10a4bcc02c` |
| `/workspace/review/trackB_scope_v3_6_CNA_disposition_v1.md` | `e84c1b1e6f88f1b99275924bf53f8fbbfe29494b527979f8026a21309f3c3a31` |
| `/workspace/review/trackB_scope_v3_6_CNA_response_to_RD_lightpass_v1.md` | `0e4bf4e83fdb9d5aad6253f32ac43a374439d8c69f71c7e17f44dd001505e9f8` |
| `/workspace/review/trackB_instrument_validation_scope_v3_6_merged_RD.md` | `ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b` |
| `/workspace/review/CKAPPA_STANDING_APPROVAL_APPLICATION_RL.md` | `4df62ccda727f77fdad8a04e0751361b30e2fdbedaa3a6243411742ea8275042` |
| `/workspace/review/GRU_AUDIT_v1_3_STANDING_APPROVAL_APPLICATION.md` | `aef5383b28a37c27e478731ca32880efea8dffc78a866e2ccb618c135f16a9c7` |
| `/workspace/astra_consult_1.md` | `7e8d088dfa21141044204ceb38429ad4bcfa40aef653b29aeeb4bcd60481a43d` |

*DRAFT. Not frozen. Design only. No execution authorized. X1–X5 unchanged. No host coupling. No consciousness claim is made or implied.*
sha256 of all content above this line: 9e2cacab3bc2216c61fd32cfaa32c5b7ebc27917835945c87915ac1eda7d6f86
