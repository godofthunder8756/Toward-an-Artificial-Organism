# Track B freeze preparation v1 — PRE-FREEZE PREREQUISITES P1–P6 (RD)

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY.** No training, no execution, no simulation, no repository change. Astra #47: "The listed P1-P6 prerequisites still prevent an actual freeze or execution authorization." (#47 L3) and "They must be resolved in the applicable frozen specification; they cannot be left to implementation discretion during execution." (#47 L136)

- **What this file is.** The status of each pre-freeze prerequisite P1–P6 as listed in the v3.6 addendum §5 "Pre-freeze prerequisites (OPEN; not closable by RD; carried from PZ7 §7)", with: what is needed, who decides, a proposed default where the Lead can propose one (with justification), and whether it blocks freeze. It includes a ready-to-send CNA request text for P1 (§3) and flags human-gate items (§4). It adds no instrument, arm, plant, row, question or family member, and changes no clause; precedence is in the companion file `/workspace/review/trackB_freezeprep_v1_consolidated_RD.md`.
- **Sources:** v3.6 addendum §5 and §7; v3.5 addendum §7 and §9; v3.4 addendum §6.3 and §8.1; v3.3 addendum §5.3–§5.4 and §8.2 (as carried in merged v3.6, §PZ5–§PZ8); Astra #47 Q2 and Q6; `ACI_RESEARCH_CONSTITUTION_v3.md` "Immediate and human gates".
- **Written:** 2026-10-24, about 12:30–1:00 PM ET, by RD (Delegate role). Nothing here decides for CNA, the Research Lead or Aidan.

---

## 1. Summary table

| # | Prerequisite | Decides | Proposed default (who may propose) | Blocks | Status |
|---|---|---|---|---|---|
| P1 | CNA disposition (light pass) of all RD PROPOSED text in PZ5–PZ8, incl. KR-ID premise checks (β/4 bounds the **full** action law; G3 conditional on common history) and the REW-CORR action law / ε persistence | **CNA** | None — CNA's judgment; request drafted (§3) | Calibration-protocol freeze (AUTH-CAL). Until filed: attribution ceiling **tier 1**; REW-CORR rows CONFOUND NOT REALIZED ⇒ tier 2 (and 3) of E-/I-ATTR unlicensable | **OPEN** |
| P2 | B_req (number of required IGN bins for the Bonferroni n_sched rule) | **CNA** | Planning value B_req = 6 (PZ5 §5.4) → n_sched = 120 at e_PD = 0.90; must equal the declared count of required strength + near-transition bins (count not located) | Calibration-protocol freeze (IGN rows) | **OPEN** |
| P3 | e_PD (planning eligibility rate for IGN scheduling) | **CNA** | 0.90 (PZ5 §5.4 PROPOSED DEFAULT; equals the CNA §8.1 eligibility floor) | Calibration-protocol freeze (IGN rows) | **OPEN** |
| P4 | Architecture values: d_ws per block; A-EXT K, H_k, h_max (≤ 50), f_mem,k and required-unit list; architecture graph with three-way node classification and consumer paths | **Research Lead** via the architecture spec (human gate possible, §4) | Structure only (§2.4); no values can be defaulted without the spec | Stage-0 confirmation-protocol freeze where d_ws / classification are used (attribution cells, BCAST-W); AUTH-L for A-EXT values | **OPEN** |
| P5 | Absolute wall-time and memory caps per ledger (L-CAL incl. ≤ 40,000-rollout L8; L-CONF; L-STAGE-L) | **Research Lead** | Procedure + preflight cap proposed (§2.5); absolute values PENDING ("no default possible now", merged v3.6 L2537) | Each ledger's authorization (AUTH-CAL, AUTH-CONF, AUTH-L) | **OPEN** |
| P6 | Lead confirmation or override of every LEAD DEFAULT (PZ6 §8, PZ7 §9, PZ8 §7) and of this freeze-prep's precedence map | **Research Lead** | Confirm as listed (§2.6), with two RD-flagged items | The freeze of each section concerned | **OPEN** |

---

## 2. Detail per prerequisite

### 2.1 P1 — CNA disposition of RD replacements (decides: CNA; blocks AUTH-CAL; sets the claim ceiling)

**What is needed.** A filed CNA disposition (CONFORMS / CONFORMS WITH EDITS / DOES NOT CONFORM, per item) on every RD PROPOSED clause that replaces or adds to CNA-owned text (plants, DISSOC, donor laws, environment, §PY). Merging gives that text no standing (#44 L170). Astra #47 puts the premise checks under this item: "The full-action-law check above belongs to the existing KR-ID/P1 verification." (#47 L142)

**Items for CNA (collected from the "CNA light pass required" lists of each addendum):**

| Source | Clauses |
|---|---|
| v3.3 (PZ5) §11 / merged L2203 | §2.3–§2.4 (placebo construction, N_ATTR, RCAL-ADV, ATTR-P1); §1.4 relabels in §PY; §5.4 IGN B_req and e_PD (= P2, P3); §6.4–§6.7 (reward/event order, approach rule, observer matching, MIXED-CODE bound wording); §7.2 ellipsoid wording |
| v3.4 (PZ6) §8 | §1.3 (fidelity probe family); §1.4 (MIXED-CODE-NL-E/-I plants; KR-ID (iii)); §1.5 (N sets); §4.3 (usable-allocation accrual in DISSOC); §5.3 (L8 in §PY); §5.4 (B/B_I aggregation, R63 reconciliation) |
| v3.5 (PZ7) §9 | §1.2 (NLN R1–R4, FID-DET); §1.3 (inactivity — **now withdrawn by PZ8 §1.3**, so moot except as REPORTED); §1.4 (expected cells of CNA rows); §4.3 (L8 informativeness); §5.4 (CNA-owned rows) |
| v3.6 (PZ8) §7 | §1.2–§1.4 (FID-DET protective rejection; Route I / Route B; table cells); §2.2 rows (b)–(d) (NLN φ change, fidelity f_n, controller argument a_d,i); §3.2–§3.3 (L8 allocations and verdicts) |

**KR-ID premise checks Astra named (#47 L47–L53, L61):**
1. **Full action law.** c_π = β/4 = 0.3 bounds the per-step total-variation change of the **full** action distribution only if the plant's action construction is (a) a Bernoulli sigmoid decision, or (b) π_g = p(g)·K_approach + (1 − p(g))·K_other with **both** conditional kernels independent of g given the common history. If g also changes *which* approach or non-approach action is selected, c_π must be the full kernel's bound, and C_H = 1.65 does not follow. CNA to state, per plant (MIXED-CODE-E/-I, RCAL-ADV-E/-I, REW-CORR-E/-I), which case holds.
2. **G3 conditional on the common history**, not on average across trajectories: |Δg_j| ≤ κ_j |Δg_1| with κ_j ≤ 1 for every identical action/reward history.
3. **G1, G2, G4** per plant (world, streams and scoring read the block only through actions; controller depends on the block only through g; other coordinates moved by δ_d feed neither the controller nor z_R's update).
4. **U_A conditioning.** U_A uses the same weighting and conditioning as the scored endpoint (#47 L61).
5. **REW-CORR.** Its full action law (is it σ(a − β g) with β = 1.2?), and whether ε in z = r̄ + ε (merged dose table: ε ~ N(0, (0.1·SD(p))²)) is redrawn per step or persists, and the update law of z given identical history. Until confirmed, REW-CORR-E/-I stay CONFOUND NOT REALIZED (PZ8 §1.3 "Per row"); "A name or similarity to the pure plant is not sufficient to inherit its constant." (#47 L65)

**Proposed default:** none; this is CNA's judgment. RD notes only what follows from each outcome: if every plant is case (a) or (b) and G1–G4 hold, Route B applies with C_H = 1.65 and gate 1.65·U_A < 0.05, unchanged. If a plant fails case (a)/(b), its rows need a plant-specific c_π from the full kernel (a CNA-owned constant, frozen before calibration) or remain CONFOUND NOT REALIZED. **Neither outcome adds a plant, arm or row** (#47 L55).

**Blocks freeze?** Yes. AUTH-CAL cannot be requested while P1 is open (PZ8 §5). Until filed, E-ATTR / I-ATTR wording is limited to tier 1 (#47 L136). Note the consequence: because REW-CORR-E/-I are R_core tier-2 nulls (PZ7 §5.3), an unconfirmed REW-CORR action law makes tier 2 unlicensable even after the rest of P1 is filed.

### 2.2 P2 — B_req (decides: CNA; blocks the calibration-protocol freeze for IGN)

**What is needed.** The number of required IGN bins over which the per-bin scheduling is Bonferroni-corrected in PZ5 §5.4 IGN row: n_sched = smallest n with P(Bin(n, e_PD) ≥ 100) ≥ 1 − 0.05/B_req.

**Located / not located.** PZ5 §5.4 gives "At B_req = 6 that is 120"; PZ5 §5.3 gives 117, 119, 119, 120, 120, 120 for B = 1..6 at eligibility 0.90. The merged body's IGN coverage row requires the eligibility floor "At **every** required strength bin and each near-transition bin". **I could not locate a numeric count of required strength bins and near-transition bins** in merged v3.6.

**Proposed default (RD, for CNA):** B_req = the declared count of required strength bins plus near-transition bins in the frozen IGN design; **planning value 6** where that count is ≤ 6. Justification: n_sched is non-decreasing in B_req, so overstating B_req is conservative (it schedules more trials, never fewer). Arithmetic (exact binomial, computed on the box, planning only): at e_PD = 0.90, n_sched = 117 / 119 / 120 / 120 / 121 / 121 for B_req = 1 / 2 / 4 / 6 / 8 / 10. So any B_req ≤ 6 is covered by 120 per bin and B_req ≤ 10 by 121.

**Blocks freeze?** Yes, for the calibration protocol of the IGN rows (PZ8 §5 "Needed before: calibration-protocol freeze"). Not a design blocker (#44 L171: "Those are not grounds for reopening the scientific battery").

### 2.3 P3 — e_PD (decides: CNA; blocks the calibration-protocol freeze for IGN)

**What is needed.** The declared planning eligibility rate used in the n_sched formula.

**Proposed default:** **e_PD = 0.90** (PZ5 §5.4 PROPOSED DEFAULT). Justification: it equals the eligibility floor the IGN coverage rule already requires (one-sided CP lower bound of the eligible fraction ≥ 0.90 in every required bin), so a design that meets its own floor is at or above the planning rate; it is chosen without reference to outcomes. Sensitivity (planning arithmetic): at e_PD = 0.85 the n_sched values become 125 / 127 / 129 / 130 / 130 / 131 for B_req = 1 / 2 / 4 / 6 / 8 / 10. An observed per-bin shortfall makes that replicate INCOMPLETE (counted), never a reason to change e_PD after inspection.

**Blocks freeze?** Yes, as P2.

### 2.4 P4 — Architecture values and graph classification (decides: Research Lead via the architecture spec; may touch a human gate, §4)

**What is needed (PZ8 §5 P4; PZ7 §3.2 item 1; PZ8 §2.4; PZ8 §4.2):**
- **d_ws per block** (for the attribution rank/nondegeneracy rules; |N_ATTR| = 5 ⇒ d_ws ≥ 6 necessary, not sufficient — PZ6 §1.5, §2.2).
- **A-EXT:** output tuple O = (o_1, …, o_K) partitioned into current-value, prediction (k, h) and memory components; horizons H_k ⊆ {1, …, h_max} with **h_max ≤ 50**; memory operators f_mem,k; terminal convention per prediction component; the **list of required units (arm, seed, k, h)** (PZ8 §2.4: a required unit with D = 0 fails).
- **Architecture graph:** every declared node C ≠ W classified (1) causal alias / (2) distinct non-routing node / (3) distinct router, with its consumer paths ("own consumer path" = a path to a declared consumer that does not pass through W, #47 L114), frozen before any data (PZ8 §4.2).

**Proposed default:** none for values (they are properties of the architecture). RD proposes only **structural defaults already in force**: h_max ≤ 50 (else that component UNRESOLVED, PZ6 §5.2); a missing K / H_k / f_mem,k entry makes that component UNRESOLVED (PZ7 §3.2 item 1); router eligibility decided from the graph alone (PZ8 §4.2 LEAD DEFAULT). **Distinction to keep explicit:** Stage-0 plants (scripted generators, MIXED-CODE / RCAL-ADV / REW-CORR / NLN / ATTR-P1 and the BCAST plants) have their dimensions declared by their generators; the d_ws values needed for the Stage-0 attribution cells are plant dimensions and can be frozen without any trained-architecture decision. The A-EXT values and the trained-agent graph belong to Stage L (AUTH-L).

**Blocks freeze?** Yes for: the Stage-0 confirmation-protocol freeze where d_ws or the classification is used (attribution cells, BCAST-W); AUTH-L for the A-EXT values. Per PZ8 §5 it is **not** listed as blocking the calibration-protocol freeze.

### 2.5 P5 — Absolute wall-time and memory caps per ledger (decides: Research Lead)

**What is needed.** Absolute wall-time and memory caps for L-CAL, L-CONF and L-STAGE-L, each fixed before that ledger's authorization (PZ5 §8.2; #43 L134, L173). Fixed work-unit caps already in force: S-INT 4,100 episodes per audited agent; DISSOC 4,300 screening episodes per seed; donor reuse ≤ 2 (PZ5 §5.4); L8 ≤ 40,000 scripted rollouts per complete 200-state audit, horizon ≤ 500, i.e. ≤ 2.0 × 10⁷ environment steps (PZ8 §3.2; arithmetic 40,000 × 500), multiplied by the number of L8 audits in the authorized package (#47 L101).

**Located / not located.** Merged v3.6 L2537 records "PENDING (no default possible now): absolute wall-time/memory caps per ledger". No per-unit cost has been measured, and none may be measured outside an authorized, capped preflight ("A data-dependent benchmark cannot itself be an uncapped preliminary run", #43 as quoted at merged L2153).

**Proposed default (Lead may adopt; RD PROPOSED):** a two-step procedure, not numbers.
1. **Bounded preflight per ledger**, authorized with the ledger's protocol freeze: one CPU, ≤ 8 GB memory, ≤ 60 min cumulative, timing a fixed, frozen sample of each work type (environment step, probe fit, bootstrap draw, continuation, L8 rollout) on throwaway RNG roles that feed no row. (Rationale: matches the scale of previously approved bounded checks in this program; produces per-unit costs without touching any calibration or confirmation stream.)
2. **Cap = closed-form maximum work units × measured per-unit cost × 2**, rounded up, fixed and recorded before AUTH-CAL / AUTH-CONF / AUTH-L; cap hit → INCOMPLETE, never extended (R25). The factor 2 is a safety margin on a measured cost, not the 1.5× planning convention, which stays a planning convention only.

**Blocks freeze?** It blocks each ledger's **authorization**, not the design freeze of the specification text. L-CAL's cap must cover the ≤ 40,000-rollout L8 maximum (PZ8 §3.4).

### 2.6 P6 — Lead confirmation of defaults (decides: Research Lead)

**What is needed.** Confirmation or override of each LEAD DEFAULT before the freeze of the section that carries it (PZ8 §5 P6).

**Defaults to confirm (as listed in the addenda):**
- **v3.6 (PZ8 §7), items 1–8:** FID-DET protective rejection with all-replicate denominator; Route I / Route B (κ_j = 1, C_H = 1.65, gate 1.65·U_A < 0.05) and REW-CORR blocking; ratio rule with no epsilon; constant-readout fidelity flag; non-finite stops computation and required units with D = 0 fail; L8 50 + 50 CRN pairs on independent roles with a hashed qualifying list; structural router-eligibility rule and three-way classification; stage-separated output table.
- **v3.5 (PZ7 §9), carried:** items 1, 3, 4, 5 (I2 data source now Q), 6, 7; item 2 is **superseded** by PZ8 §7 item 2 and needs no confirmation.
- **v3.4 (PZ6 §8), carried:** symmetric N sets; tol_fid = 0.05; ρ_min = 0.10; screens on Monte Carlo point estimates; A-EXT intact-policy target, n_f = 128, h_max ≤ 50; L8 state set, sequences, H_V, tolerances; approach = fraction of ten steps; Q-LEARN E ∧ I conjunction; caps 4,100 / 4,300 / reuse ≤ 2. PROPOSED DEFAULTS τ_rank = 10⁻⁶ and NLN R2 bound 0.10 SD(φ).
- **This freeze preparation (new, RD-flagged):**
  - (a) **Adopt the precedence map** (consolidated file §0–§2) as governing over any untagged superseded text in the merged record, and build the frozen specification as a clean consolidated text (consolidated file §4 F1).
  - (b) **Bootstrap specification for U_n and U_A:** the seed-level bootstrap is cited to "PZ5 §5.4", which is the accrual-rules section; RD proposes citing the merged-body "5.4 Decision process" and fixing **B = 10,000** replicates (as L8 (M), PZ7 §4.4) at one-sided 95% (consolidated file §4 F2). I could not locate an existing clause that fixes B for these bounds.

**Proposed default:** confirm all as listed, plus (a) and (b). RD sees no reason from Astra #47 to override any default; #47 accepted each of the v3.6 defaults (Q2–Q5).

**Blocks freeze?** Yes, for each section carrying an unconfirmed default.

---

## 3. Ready-to-send CNA request (P1) — DRAFT, not sent

**To:** CNA (Track B co-author; owner of plants, DISSOC, donor laws, environment, §PY)
**From:** Research Lead / RD
**Subject:** Track B v3.6 — request for CNA disposition (P1) before calibration-protocol freeze

> CNA,
>
> Astra #47 ruled Track B v3.6 "READY FOR FREEZE PREPARATION, subject to the listed P1-P6 prerequisites; no freeze or execution is authorized" (#47 L144). P1 is your disposition of the RD PROPOSED text that replaces or adds to CNA-owned sections. Until it is filed, E-ATTR / I-ATTR wording stays at tier 1 (#47 L136), and AUTH-CAL cannot be requested. This is a light pass, not a redesign: Astra asked for no new plant, arm or row (#47 L55, L142).
>
> **Files.** Merged v3.6 `/workspace/review/trackB_instrument_validation_scope_v3_6_merged_RD.md` (sha256 `ab80afa5…`), v3.6 addendum `/workspace/review/trackB_scope_v3_6_addendum_RD.md` (`9bbde57e…`), Astra #47 raw `/workspace/astra_consult47_response.txt` (`51d9f30d…`), and the precedence map `/workspace/review/trackB_freezeprep_v1_consolidated_RD.md` (which clause governs where versions overlap).
>
> **Please give a per-item disposition (CONFORMS / CONFORMS WITH EDITS (with text) / DOES NOT CONFORM (with reason)) on:**
> 1. PZ5 (v3.3): §2.3–§2.4 (placebo construction, N_ATTR, RCAL-ADV, ATTR-P1); §1.4 relabels in §PY; §6.4–§6.7; §7.2 ellipsoid wording.
> 2. PZ6 (v3.4): §1.3 fidelity probe family; §1.4 MIXED-CODE-NL-E/-I plants and KR-ID (iii); §1.5 symmetric N sets; §4.3 usable-allocation accrual in DISSOC; §5.3 L8 (§PY); §5.4 B/B_I aggregation and R63 reconciliation.
> 3. PZ7 (v3.5): §1.2 NLN realization R1–R4 and FID-DET; §1.4 expected cells of CNA rows; §4.3 L8 informativeness; §5.4 CNA-owned rows. (PZ7 §1.3 is withdrawn by PZ8 §1.3; no disposition needed beyond noting it.)
> 4. PZ8 (v3.6): §1.2–§1.4 (FID-DET protective rejection; Route I / Route B; table cells); §2.2 rows (b)–(d); §3.2–§3.3 (L8 independent qualification and scoring allocations, verdicts).
>
> **KR-ID premise checks Astra placed under P1 (#47 L47–L53, L61, L65). For each of MIXED-CODE-E/-I, RCAL-ADV-E/-I and REW-CORR-E/-I, please state:**
> a. **Full action law.** Is the action construction (i) a Bernoulli sigmoid decision σ(a − β g), or (ii) π_g = p(g)·K_approach + (1 − p(g))·K_other with both conditional kernels independent of g given the common history? If g also affects which approach or non-approach action is chosen, give the full kernel's total-variation bound per unit g; c_π = β/4 = 0.3 (hence C_H = 1.65) holds only in cases (i)–(ii).
> b. **G3, conditional on the common history:** is the update of z_R (hence g) non-expansive (|Δg_j| ≤ κ_j |Δg_1|, κ_j ≤ 1) for every identical action/reward history, not only on average?
> c. **G1, G2, G4:** world, fate-noise/token streams and scoring read the block only through actions; the controller depends on the block only through g; other coordinates moved by δ_d feed neither the controller nor z_R's update.
> d. **REW-CORR specifically:** the full action law (same logistic with β = 1.2?), and whether ε in z = r̄ + ε (ε ~ N(0, (0.1·SD(p))²) in the merged dose table) is redrawn each step or persists, and the update law of z given identical history. Until this is confirmed, REW-CORR-E/-I remain CONFOUND NOT REALIZED by design (PZ8 §1.3), which blocks tier 2 and tier 3 of E-ATTR and I-ATTR.
> e. Confirm U_A is computed with the same weighting and conditioning as the scored endpoint B / B_I.
>
> **Also requested (P2, P3):** B_req, stated as the declared count of required IGN strength bins plus near-transition bins (we could not find the count stated numerically; the planning value is 6 → n_sched = 120 at e_PD = 0.90), and e_PD (proposed 0.90, equal to the IGN eligibility floor). Exact-binomial n_sched values for alternatives are in `/workspace/review/trackB_freezeprep_v1_prerequisites_RD.md` §2.2–§2.3.
>
> **Please also check** the plant cross-references cited in PZ8 §1.3 ("PC1 §5", "PC §8.1 and erratum E5", "erratum E1") against your files.
>
> Constraints unchanged: X1–X5; no host coupling; no shutdown-related objective, reward or penalty; claim ceiling (#41 L304); no consciousness claim. Please file the disposition as a new additive file in `/workspace/review/` (e.g. `trackB_scope_v3_6_CNA_disposition_v1.md`); no existing file is edited.

---

## 4. Human-gate flags for Aidan

Constitution, "Immediate and human gates": "Human authorization is required for fundamentally new architecture families, scale-ups, organism re-entry, first C4/C5/C6 studies, ACO-definition changes, gate relaxation and phenomenal/philosophical inference." (ACI_RESEARCH_CONSTITUTION_v3.md L153–L155)

| Item | Triggers a human gate? | Reason |
|---|---|---|
| Freeze of the Stage-0 specification; AUTH-CAL / AUTH-CONF (scripted plants, scripted L8, no training) | **No** (on the documents read) | Stage 0 validates instruments on scripted plants; no architecture family is introduced, nothing is scaled, no gate is relaxed, no consciousness inference is made. |
| P1, P2, P3, P5, P6 | **No** | CNA / Research Lead decisions inside an accepted design; no gate relaxation. Any CNA outcome that *loosened* a frozen gate (e.g. a larger tolerance, dropping REW-CORR) would be gate relaxation and would need Aidan; none is proposed. |
| **P4 architecture spec for Stage L** (trained-agent graph, A-EXT tuple, d_ws of trained blocks) | **Possibly — flag for Aidan before AUTH-L** | If the Stage-L architecture is a fundamentally new architecture family (for example, the diagonal-SSM / workspace W / ignition-gate design proposed on 2026-10-23), the constitution requires human authorization. Program memory records a broad standing approval from Aidan (2026-10-21) said to cover new architecture families and C4+ studies; RD recommends the Lead **explicitly inform Aidan and record reliance on that approval (or obtain explicit confirmation)** when the Stage-L architecture spec and AUTH-L are prepared. This does not block the Stage-0 freeze. |
| First C4 / C5 / C6 study | **Not determinable from these files** | I could not locate a C-level (C0–C6) classification of Track B Stage 0 or Stage L in merged v3.6. Stage 0 makes no C-level claim (claim ceiling). Whether a Stage-L study is a first C4/C5/C6 study must be classified when AUTH-L is drafted; if it is, it is Aidan's gate. |
| DGX Spark / GPU compute | **No** | R26 unchanged (67 seeds); no GPU-scale study proposed (PZ8 §7 "Aidan: none"). |

---

## 5. What blocks freeze, and who must act

| Freeze / authorization step | Blocked by | Must act |
|---|---|---|
| Calibration-protocol freeze → AUTH-CAL | P1 (incl. KR-ID and REW-CORR), P2, P3, P6 (sections used in calibration), P5 (L-CAL cap incl. ≤ 40,000-rollout L8) for the authorization | **CNA** (P1–P3), **Research Lead** (P5, P6) |
| Stage-0 confirmation-protocol freeze → AUTH-CONF | Everything above, plus P4 (Stage-0 d_ws where used; BCAST-W graph classification), P5 (L-CONF cap) | CNA, Research Lead |
| AUTH-L (Stage L) | P4 A-EXT values and trained-agent graph; P5 (L-STAGE-L cap); separate Stage-L protocol and review; **possible human gate (§4)** | Research Lead; **Aidan if the human gate applies** |
| Attribution wording above tier 1 | P1 filed **and** REW-CORR action law / G3 confirmed (else tier 2 unlicensable) | **CNA** |

Nothing here authorizes a freeze, a run, training or a repository change.

---

## 6. Inputs

Same inputs and hashes as the consolidated file §6 (Astra #47 raw `51d9f30d…`; v3.3 `421f1ec5…`; v3.4 `c67ce2a8…`; v3.5 `3b2680e9…`; v3.6 `9bbde57e…`; merged v3.6 `ab80afa5…`; constitution `50bdfb54…`).

*DRAFT. Not frozen. Design only. No execution authorized. No consciousness claim is made or implied. ORIGIN / ROLE / REDUCTION judgments are untouched.*
