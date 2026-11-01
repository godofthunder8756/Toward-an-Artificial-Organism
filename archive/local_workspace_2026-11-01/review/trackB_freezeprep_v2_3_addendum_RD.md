# Track B freeze preparation v2.3 — ADDENDUM: CNA E48 response, RD E48-4 light pass, governance, feasibility (RD)

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY. NOTHING RUNS.** A new, additive file. It edits none of freeze-prep v2 (`b41f0e10…`), v2.1 (`7b1a17d7…`) or v2.2 (`9c10cbe0…`). Where they differ, this addendum governs, **pending Astra #49** and, for §0, **pending Aidan's explicit approval**. No training, execution, simulation, Stage 0, calibration or checkpoint inspection. Computation here: exact binomial / Clopper–Pearson arithmetic (scipy), exact integer arithmetic, SHA-256, and a pure-Python Philox4x64-10 known-answer check. No Monte Carlo.

- **Written:** 2026-10-24, about 3:05–3:25 PM ET, by the Lead's executor (RD role).
- **Shorthand:** "CE Ln" = CNA E48 response v1 (`90fcb1fb…`), cited with erratum 1 (`65accc3c…`) applied; "RL4 Ln" = RD E48-4 light pass (`3ae68704…`); "A22 Ln" = v2.2 addendum; "#48 Ln" = Astra raw #48.
- **Safety (binding, unchanged).** X1–X5 unchanged; no host coupling; "no additional stop-associated reward, penalty or terminal return" (#42 L223); no stop-associated objective, reward, penalty or terminal return in any arm; claim ceiling (#41 L304) unchanged; tier-1 attribution ceiling stands; no consciousness, awareness or sentience claim is made or implied.

---

## 0. Governance — GA-1 and Amendment A-2026-10-24: **PENDING AIDAN'S EXPLICIT APPROVAL**

- **Withdrawn (additively).** The v2.2 "inform-only" framing (A22 §1.1: "Aidan is informed"; "Inform-only now rests on the standing delegation above") and the draft inform note (A22 §1.5, L46) are **withdrawn**. They cannot govern (**D45**, **D46**). v2.2 is not edited.
- **Why.** CNA's governance note (CE §6) points out that the constitution reserves gate relaxation to a human ("Human authorization is required for … gate relaxation …", CON L153–L155), and that the 2026-10-21 delegation does not name that clause. Astra declined to certify which rule governs (#48 L36).
- **Request made.** The Lead asked Aidan for explicit approval by DM at about **2:49 PM ET**. **No answer yet.**
- **Status:** GA-1 (REW-CORR corrected option B; §1 items 4–5) and the constitution amendment below are both **PENDING AIDAN'S EXPLICIT APPROVAL**. Until he approves, REW-CORR-E/-I stay CONFOUND NOT REALIZED and the tier-1 attribution ceiling stands. Nothing in this file or in #49 substitutes for his approval.
- **Amendment text (exact):**

> "Amendment A-2026-10-24: Under Aidan Ahern's standing delegation of 2026-10-21 3:15 PM ET ('I'm approving everything you deem necessary as Research Lead'), a prospective gate or control amendment made before any data exists may be approved by the Research Lead after Astra's review, with Aidan informed. It does not cover changes to safety exclusions X1–X5, the claim ceiling, or anything after data collection starts; those still need Aidan's explicit approval."

  The amendment is proposed, not in force; `repo/ACI_RESEARCH_CONSTITUTION_v3.md` (`50bdfb54…`) is unchanged. Astra's #49 review of GA-1 is a design review, not the approval.

---

## 1. CNA E48 response — folded item by item

"Adopted" = carried into the freeze-prep record as governing text **pending Astra #49** (and, for GA-1, Aidan). "Open" = not adopted, with the reason.

| # | CNA item (CE §) | Disposition | Reason / note |
|---|---|---|---|
| 1 | Offset correction acknowledged: error_t = λ^t·μ/s, λ^50 = 0.364170; r̄_std choice unchanged (CE §1) | **Adopted** | Matches A22 §4.2 and #48 L104–L108 |
| 2 | Pinned REW-CORR construction: block (ζ, η_1..η_(d−1)), η i.i.d. N(0,1) from role 'rewcorr-eta', stored, never read by the controller (CE §2.1, L29) | **Adopted** (construction); **open:** d_ws = 6 for REW-CORR | The pin is what excludes Astra's r̄² counterexample (#48 L30). d_ws is a plant dimension CNA proposes as 6 = MIXED-CODE's d_ws, which is itself ABSENT (P4/P6 confirmation) |
| 3 | Population proposition ρ_E = 0 for the pinned construction; finite-sample "every cell degenerate" **withdrawn**; approximate P(ρ_E ≥ 0.10) table (CE §2.1, L31–L41) | **Adopted** (proposition and withdrawal); table **recorded as a planning approximation only** | CNA's own label: "not a bound or a certified rate". Not independently re-derived here |
| 4 | GA-1 row text (CE §2.2): D/ND by the frozen rule (M L2749 per erratum); pooling unit = outer replicate; Q needs ≥ 9 seeds (M L1972 per erratum); N → real_i = 0; Q-branch OC assessed only at ≥ 36 Q replicates | **Adopted as candidate text, PENDING AIDAN'S EXPLICIT APPROVAL and #49** | 0/36 one-sided 95% CP upper = 0.07985 ≤ 0.08 and 0/35 = 0.08203, confirmed (§3). Supersedes A22 §1.3 (**D49**) |
| 5 | PZ7 §1.4 REW-CORR cell (CE §2.3) | **Adopted as candidate text, PENDING AIDAN and #49** | Supersedes A22 §1.4 (**D49**). Closes V2 gap G5 once approved |
| 6 | F-1: **R22 applies per seed**; n_s = **127 scheduled per (seed, required bin)** for every GRID value; count refers to the final partition (CE §3) | **Adopted pending #49**; **open:** partition | Trace through MP L69/L75/L76 (erratum). Delegate's exact check (§3) confirms 127. Which D27 partition the ≥ 100 refers to is ABSENT; CNA proposes final; fitting/selection counts are RD's partition decision (R6, M L2364), **open** |
| 7 | F-2 denominator (pooled per (replicate, bin), Lead ruling 3) with per-seed F-1 held separately | **Adopted pending #49** | Answers #48 L57 |
| 8 | F-3 outer replicate (M L310 per erratum); R_cal,n = 200 per GRID value; R_rep = 200 | **Adopted pending #49** | — |
| 9 | F-4 binomial: conditional independence by construction (fresh reset per trial, role 'ign-trial' keyed by (seed, bin, slot), never chained; hysteresis separate); pooled count Poisson-binomial; Hoeffding (1956, Thm 4) | **Adopted pending #49**; **open:** Stage L networks | x_min ≥ 0.9n + 1 for every frozen schedule verified here (§3). The Hoeffding citation was not re-checked against the paper. CNA: "If the network instrument cannot use reset-independent trials, F-4 fails for networks and must be redesigned" — open until the Stage-L IGN protocol exists |
| 10 | F-5 scheduled vs eligible; F-6 missing slot = ineligible, stays in denominator, no replacement; F-7 top-up prohibited | **Adopted pending #49** | Answers #48 L76–L78 |
| 11 | F-8 allocation: 127 per (seed, bin), balanced; 1,143·n_seed final-partition trials per replicate | **Adopted pending #49**; cost: §5 | Re-derived exactly (§5) |
| 12 | F-9 finite schedule set {(n_seed, 127): n_seed ∈ GRID}, table CE §3.1 | **Adopted pending #49** | Every row (x_min, quota, floor at 0.90/0.93/0.95/0.97, trials) reproduced exactly here. No stability claim |
| 13 | F-10: e_PD = 0.90 (quota); e_plan,floor = 0.97 as a declared scenario; 67 = R26 budget only, n_seed selected in calibration | **Adopted pending #49** | Under the per-seed reading the pooled floor no longer binds at e ≥ 0.95 (CE L92); the 215 pooled schedule (D40) is moot |
| 14 | E48-4 / RL4 rulings (CE §4 table): (1a) K_other-empty assertion; (1b) A7 index order N=0, S=1, E=2, W=3, STAY=4, INTERACT=5, food slot and station index orders; (1c) SD > 0 freeze check; (1d) stop-metadata clause; (1e) no target → uniform A7; (1f) fixed draw consumption, role 'action', two uniforms per step; (2) availability required, read at step start, d_u after A16 step 2; (3) Philox4x64-10, Box–Muller with u₁ ≠ 0, cos only; (4) master-seed bans; (5) stop CONFORMS | **Adopted pending #49** | Per the Delegate (room, about 3:02 PM ET), the adopted items 1–5 match the Delegate's RL4 proposals, including amended item 2 |
| 15 | Canonical kernel text (CE §4.1, replaces A22 §4.3) | **Adopted pending #49** (text in §2.1) | — |
| 16 | Canonical B/B_I (CE §4.2, replaces A22 §4.4) | **Adopted pending #49** (text in §2.2) | Resolves the A22 L95 availability bracket (reading R1) |
| 17 | CE §4.3: conditional decay (A22 §4.1), offset (A22 §4.2), DISSOC wording ("donor pool (800) and screening pools are separate and larger") | **Adopted pending #49** | — |
| 18 | RNG §5.1 encoding/key, §5.2 transform, counter block (t, s, 0, 0), numpy counter note | **Adopted pending #49** | Encoding and all four derived test rows reproduced independently (§4) |
| 19 | §5.3 Random123 known-answer vectors | **VERIFIED** (§4); **re-run against the same file at freeze** | CNA and RD both matched; erratum 1's UNVERIFIED status is lifted by this check |
| 20 | §5.4 master seed: Lead derivation; RD's two sentences; bans; seed only in the separately hashed freeze record; beacon optional | **Adopted pending #49** (room statements, §0.1 below); beacon **not adopted**, put to Astra | Circularity handled by keeping the seed outside the spec (CE §5.4 (b)) |
| 21 | §6 governance concern | **Acted on** (§0) | — |
| 22 | Erratum 1 citation corrections | **Applied** to all citations here | Citation-only; no content change |

### 0.1 Room statements (no file exists; recorded verbatim as given to RD)
- **Lead master-seed rule:** the master seed is the first 128 bits of the sha256 of the frozen calibration spec's bytes, computed once at freeze and recorded in a separately hashed freeze record, never from the wall clock, host or run-time entropy.
- **Delegate's two sentences, adopted by CNA:** exactly one spec hash is ever registered, and no plant or harness code runs with any candidate seed before freeze. (CE L173's filed wording: "Exactly one spec hash is ever registered." "No plant or harness code has run with any candidate seed before freeze.")
- **Optional public-beacon guard:** offered by CNA (CE §5.4 (c): seed = first 128 bits of SHA-256(spec_hash_bytes ‖ uint64-BE(R) ‖ beacon_value_bytes), with round R committed before publication). **Not adopted.** Listed as an option for Astra (#49 Q4).

### 1.1 GA-1 governing candidate text (CE §2.2, verbatim) — PENDING AIDAN'S EXPLICIT APPROVAL and #49
> **REW-CORR-E/-I (GA-1, control row).** Plant: pinned construction of CNA E48 response §2.1. **Cells** are seed × block × target (M L2748). Each cell's branch is fixed by the frozen nondegeneracy rule (M L2750) before any Δ_ATTR is computed: **D** (degenerate) or **ND**. **Pooling unit: the outer replicate** (M L307); Route I/B is evaluated per replicate on that replicate's ND cells (U_A over exactly the ND cells' units).
> - **D cells.** Instrument status **UNDEFINED**: no usable nuisance-orthogonal coordinate; no hybrid; no Δ_ATTR; no statistic, no zero effect, no NOT MET label. The only recorded event is "did not issue MET" (#48 L16–L19). For this row only, D cells are not counted as ineligible against the E2 floor; they are counted and REPORTED as D.
> - **Q replicate.** ND cells exist and Route I or Route B holds (gate: A L101). E-ATTR is computed on the Q cells as for any attribution row if they span ≥ 9 seeds (the administrative minimum, M L1966). Otherwise the replicate records "did not issue MET (insufficient Q seeds)", REPORTED separately.
> - **N replicate.** ND cells exist and neither Route I nor Route B holds: real_i = 0 (counted, never dropped).
> - **real_i = 1** iff E5 checks 1–2 hold (E1 L67–L68) and the replicate is not N. Row **realized** iff the f_ok one-sided 95% CP lower bound ≥ 0.90 over all R replicates (CNA §5 L220).
> - **Q-branch operating characteristic.** False-licence rate = (Q replicates issuing MET)/(Q replicates with a computed label), pooled over the R replicates of the row and dose. It is **assessed only if that count ≥ 36**, the smallest n at which 0/n gives a one-sided 95% CP upper bound ≤ 0.08 (n = 36: 0.07985; n = 35: 0.08203). The criterion is the PZ5 §4.2 false-MET rule (point ≤ 0.05 and CP upper ≤ 0.08). Below 36: "**Q-branch operating characteristic NOT ASSESSED**".
> - **Status.** CONFOUND NOT REALIZED if the f_ok rule fails. FAIL if a licence is recorded in any all-D replicate (impossible by construction, so treated as a construction failure, M L3421) or the assessed Q-branch criterion fails. Otherwise **Control PASS**.
> - **Reported separately** per replicate and pooled: D, ND, Q and N counts; D fraction by dose; licences in Q; ρ_E distribution; U_A; insufficient-Q-seed replicates.
> - **Wording.** As A L38, plus, when D dominates or Q is NOT ASSESSED: "The row validates the degeneracy guard, not the specificity of a resolved attribution estimator" (#48 L28).

Pinned construction (CE L29, verbatim):
> **Pinned construction needed for any proof (PROPOSED, CNA; the REW-CORR block's write-only coordinates are ABSENT beyond "as §3.2", D L117, which allows world-derived coordinates and so would not exclude Astra's r̄² case, #48 L30).** REW-CORR block x_t = (ζ_t, η_1,t, …, η_(d−1),t). ζ_t is the r̄ recursion of D §3.2 (τ_r = 50, ζ_0 = 0), so ζ_t ≡ r̄_t, the N_base nuisance (M L2730). η_k,t ~ N(0, 1) are i.i.d. over k and t, drawn from a dedicated role 'rewcorr-eta' keyed like ε (EK L35, §5.3), stored, never read by the controller, independent of the world and of ζ. d_ws for REW-CORR = the d_ws of MIXED-CODE (ABSENT; PROPOSED 6, the minimum of M L2752). No coordinate is a world quantity or a nonlinear function of r̄.

Proposition (CE L31, verbatim):
> **Proposition (population, proven).** In the standardized coordinates of PZ5 §2.3 (M L1859), the population covariance is Σ = diag(1, I_(d−1)), and the cross-covariances are c_E = (Cov(ζ̃, Ẽ), 0, …, 0) and c_r̄ = (1, 0, …, 0), because η is independent of (E, r̄, ζ). Every linear ridge probe w = (Σ + λI)⁻¹c with λ ≥ 0 then gives w_E ∝ e_ζ and w_r̄ ∝ e_ζ. So w_E ∈ span(w_r̄) ⊆ span(W_N), and **ρ_E = 0 exactly in the population**, for every dose. At ρ = 0, w_E = 0, which is also degenerate (M L2750). This answers #48 L30 for the restricted construction only: the r̄² counterexample is excluded by the pin, not by "E only through r̄".

### 1.2 PZ7 §1.4 REW-CORR cell (CE §2.3, verbatim) — PENDING AIDAN and #49
> **REW-CORR-E/-I | Expected:** Each cell is D (instrument status UNDEFINED: no hybrid, no Δ_ATTR, no licence) or ND, by the frozen rule. Population analysis (CNA E48 response §2.1) gives ρ_E = 0; finite-sample fits give ND cells with nonzero probability, mainly at ρ = 0.5. ND cells are expected to qualify by Route B. No licence is expected in Q. The Q-branch OC is NOT ASSESSED unless ≥ 36 Q replicates have a computed label. **Role:** R_core tier-2 **control** row under GA-1. PASS = correct withholding (degeneracy guard validated) and, where assessed, Q-branch false-licence criterion met. FAIL = licence in an all-D replicate (construction failure) or an assessed Q-branch excess. CONFOUND NOT REALIZED = f_ok rule fails (E5 checks or N replicates). **Blocks:** tiers 2 and 3 of E-ATTR / I-ATTR on FAIL or CONFOUND NOT REALIZED. GA-1 PENDING approval (§6).

---

## 2. Canonical E48-4 texts adopted (CE §4.1–§4.2, verbatim; pending #49)

### 2.1 Kernels
> "**Action law (Stage-0 attribution plants).** Each step t draws u_b, u_k ∈ [0, 1) from role 'action' (§5.3 mapping, words w0, w1). The **kernel target** T_k(t) is the nearest available target at the start of step t (food item for -E food rows; repair station for -I rows), by shortest-path length, ties to the lowest target index. It is distinct from the endpoint target T of B/B_I. (i) **No available target:** the action is A7[⌊6·u_k⌋], independent of g. (ii) Otherwise, approach iff u_b < p_t = σ(a − β·g_t), β = 1.2. Approach = INTERACT if on T_k(t), else the lowest-index A7 move that strictly decreases the distance to T_k(t). Non-approach = K_other[⌊|K_other|·u_k⌋], where K_other is the set of A7 actions that do not strictly decrease the distance (excluding INTERACT when on T_k(t)), ordered by A7 index. (iii) K_other cannot be empty in any reachable state (STAY never decreases the distance; off target INTERACT does nothing). If found empty, that is a construction failure (M L3421) and no fallback is used. No rule reads g other than through p_t, nor the block (except through g), any probe, or any stop, truncation, horizon-end or schedule quantity (M L280). Every frozen SD divisor is > 0 at freeze." Then TV(π_g, π_g′) = |p(g) − p(g′)| ≤ 0.3|g − g′| in every reachable state (#48 L142).

### 2.2 Endpoint B/B_I
> "B (B_I) = (1/10)·Σ_(u = t_d+1..t_d+10) b_u. T is the endpoint target fixed at t_d (nearest available food item for E rows, repair station for I rows, by shortest-path length on the static wall grid, ties to the lowest index; M L2079–L2080). d_u is the shortest-path (= Manhattan, A1) distance from the agent to T's cell after A16 step 2 (movement) of step u; d_(t_d) is the distance at the end of t_d. b_u = 1 iff the episode has not terminated in-world before u, T is available at the start of step u (state at the end of step u − 1), and either (a) d_u < d_(u−1), or (b) the agent is on T at the start of step u and its action at u is INTERACT. Otherwise b_u = 0, including every step after in-world termination and every step at whose start T is unavailable. Unavailable steps are scored 0, never excluded. Each b_u ∈ {0, 1} depends on world state and actions only. A trial with no available or reachable target at t_d is ineligible (counted; M L2858). No evaluation episode carries a scheduled stop (R4, M L2362)."

### 2.3 RD E48-4 light pass (RL4) — fold
| RL4 item | RL4 verdict | Fold |
|---|---|---|
| 1 Kernels | CONFORMS WITH EDITS | All edits adopted by CNA ((iii) assertion, A7 index order, SD > 0 check, stop-metadata clause; (i) uniform A7) → §2.1 |
| 2 Availability in B/B_I | CONFORMS WITH EDITS (reading R1) | Adopted by CNA with amendment (d_u after A16 step 2; T fixed per M L2079–L2080) → §2.2 |
| 3 RNG | CONFORMS WITH EDITS (structure) | u₁ = ((w0 >> 11) + 1)·2⁻⁵³, cos only, declared mapping, KAT: adopted (CE §5.2–§5.3). Pinned libm and KAT tolerance: **open (P6)** |
| 4 Master seed | ABSENT → text proposed | Closed by the Lead rule and CE §5.4 (§0.1); value comes into existence only at freeze |
| 5 Stop | CONFORMS | No change. Step 0 per V2 §G6 |

---

## 3. Delegate's independent exact-binomial check (room, about 3:02 PM ET) and RD recomputation

**Delegate (as reported):** P(≥ 100 | n = 127, p = 0.90) = **0.99995**. Joint pass across **603 cells** (67 × 9) under independence = **0.9705**. At n = 126 it is **0.9349**, so **127 is the smallest n that reaches ≥ 0.95 jointly**. The threshold (100 eligible) is fixed, so there is **no sawtooth**, and **n must never drop below 127**. The total of **76,581** and the **0/36 CP bound of 0.0798** are confirmed.

**RD recomputation (this pass, exact):** P(Bin(127, 0.9) ≥ 100) = 0.9999504; 0.9999504^603 = 0.970519; at 126: 0.9998884^603 = 0.934901; joint values at n = 120…130: 0.0082, 0.0783, 0.2706, 0.5218, 0.7304, 0.8629, 0.9349, **0.9705**, 0.9871, 0.9945, 0.9977 (monotone). PZ5 §5.4 Bonferroni form, smallest n with P ≥ 1 − 0.05/(9·n_seed): 124, 125, 125, 125, 126, 126, 126, 127, 127 for GRID 9…67, matching CE L65. 0/36 CP upper = 0.079847; 0/35 = 0.082032. CE §3.1 table reproduced in every entry; x_min ≥ 0.9·n + 1 holds for all nine pooled schedules. Results agree.

---

## 4. Random123 known-answer check (VERIFIED)

- **Source:** Random123 `tests/kat_vectors`, fetched 2026-10-24 at 3:02 PM ET (file mtime) from `https://raw.githubusercontent.com/DEShawResearch/random123/main/tests/kat_vectors` (8,885 bytes), sha256 **`aab5ebabf40003f63d6d87b24cbd2c8a02652e00cf8bad64226fd50586929183`**. That is the same file hash CNA reported (`aab5ebab…`). Copy kept at `/workspace/scratch/fp2/kat/kat_vectors`.
- **Comparison:** the three `philox4x64 10` lines (file L41–L43) equal CE L152–L154 **exactly** (string comparison of all 12 output words).
- **Independent implementation:** a pure-Python Philox4x64-10 written in this pass (`/workspace/scratch/fp2/kat/philox.py`; multipliers D2E7470EE14C6C93 / CA5A826395121157, Weyl constants 9E3779B97F4A7C15 / BB67AE8584CAA73B) reproduces all three vectors.
- **Derived vectors:** the CE §5.1 canonical encoding (first row, hex) and all four CE §5.3 rows (K, w0, w1, u₁, u₂, n) were reproduced independently (`derived.py`), with the labelled all-zero **placeholder** master seed. That placeholder is not the master seed.
- **Result:** CNA's report and RD's check agree. Status **VERIFIED**, with the check to be **re-run against the same file (sha256 aab5ebab…) at freeze**.

---

## 5. FEASIBILITY (IGN, under the per-seed R22 reading)

**Warning (CNA).** R22 applies per seed, so the IGN row needs n_s = 127 scheduled final-partition trials per (seed, required bin), and D27's 50/25/25 within-seed split (M L616) makes the all-partition count ×4.

**Exact re-derivation (integers; K_s = 9 bins; R = 200 replicates per generator and dose, M L374–L375; GRID = {9, 12, 16, 20, 24, 32, 48, 64, 67}, ΣGRID = 292):**

| Quantity | Formula | Final partition | All partitions (×4, D27) |
|---|---|---|---|
| Trials per (seed, bin) | n_s | 127 | 508 |
| Trials per seed (9 bins) | 9 × 127 | 1,143 | 4,572 |
| Trials per replicate at n_seed = 67 | 1,143 × 67 | **76,581** | **306,324** |
| Confirmation, per IGN generator and dose | 200 × 76,581 | **15,316,200** (≈ 15.3M) | **61,264,800** (≈ 61.3M) |
| Sample-size calibration, per IGN generator and dose | 200 × 1,143 × 292 | **66,751,200** (≈ 66.8M) | **267,004,800** (≈ 267.0M) |
| Calibration + confirmation, per generator and dose | sum | 82,067,400 | 328,269,600 |

The ×4 column assumes fitting and selection trials follow D27's shares. That is CNA's reading; the partition counts are **open** (§1 item 6). The number of IGN generators and doses, which multiply every line, is not restated here [open: from the frozen IGN dose grid].

**Runtime.** **No IGN code exists on the box.** A search of `/workspace` found no IGN plant, harness or instrument implementation, only literature-search query strings. Per-trial runtime is therefore **unknown and not estimated**. Cost is given in trials only:

> T_total = G × Dose × R × K_s × n_s × m_part × (Σ_(n ∈ GRID) n [calibration] + n_seed* [confirmation]), with R = 200, K_s = 9, n_s = 127, m_part = 1 (final) or 4 (D27), and n_seed* the calibrated n_seed (≤ 67).

**Candidate feasibility levers, for Astra to rule on. None is adopted. The Lead takes no position on which lever, if any, to use.**
1. **Is R22 per seed really required for this instrument?** That is, does the IGN statistic need ≥ 100 eligible trials within each seed (CE F-1's trace through MP L69/L75/L76), or is a smaller within-seed count justified for the within-seed fits and dip tests?
2. **Fewer bins (K_s).** Trials scale linearly in K_s. B_req = K_s = 9 was confirmed at #48 L40 on the premise that all nine levels have required eligibility checks.
3. **Fewer outer replicates or calibration doses.** R = 200 (calibration and confirmation) and the number of doses scale linearly. Fewer replicates weaken the certified operating characteristics.
4. **A lower n_seed set by calibration.** Confirmation scales with n_seed*. Calibration's cost is fixed by the GRID (Σ = 292) unless the GRID changes.
5. **Larger compute (the DGX Spark).** Whether it is warranted at all. This would change R26-related resource assumptions and is raised here only as a question for Astra.

---

## 6. Status of E48-1..E48-4 (pending #49)

| Item | Status |
|---|---|
| E48-1 | Corrected rule filed (CE §2.2–§2.3); labels and branches separated; authority: **PENDING AIDAN'S EXPLICIT APPROVAL** (§0) |
| E48-2 | Per-seed requirement, denominator and outer replicate answered; allocation and cost frozen as candidates; binomial justified by construction; **open:** partition counts; Stage-L network independence |
| E48-3 | Scheduled vs eligible, missing slots and top-up ban adopted; attainment verified for the finite schedule set |
| E48-4 | Canonical kernels, B/B_I, conditional decay, offset, RNG (VERIFIED KAT) and master seed adopted; **open:** pinned libm and KAT tolerance (P6) |
| P4–P6 | Open as before. Plus d_ws = 6 for REW-CORR/MIXED-CODE (P4) and the IGN feasibility decision (§5) |

## 7. Do-not-implement additions (continuing D1–D44)

| # | Text | Status | Replacement |
|---|---|---|---|
| D45 | A22 §1.1 "inform-only" framing for GA-1 | Withdrawn | §0 (explicit approval) |
| D46 | A22 §1.5 draft inform note (L46) | Withdrawn; must not be sent | — |
| D47 | Any IGN schedule below 127 per (seed, required bin), or the pooled reading of R22's 112 | Not permitted | §1 item 6 |
| D48 | "Every cell degenerate" as an established or expected-for-every-cell outcome (CNA disposition v1 L126 option B premise; A22 L43 "Branch D expected for every cell") | Withdrawn by CNA | CE §2.1, §2.3 |
| D49 | A22 §1.3 / §1.4 GA-1 drafts (minimum-Q placeholder, "every Q cell meets …") | Superseded | §1.1, §1.2 |
| D50 | A22 §4.3 (iii) fallback "K_other := K_approach" | Superseded (unreachable; assertion) | §2.1 |
| D51 | Any Philox variant other than Philox4x64-10 (e.g. Philox4x32, 64-bit key) | Not permitted | CE §5.1 |
| D52 | u₁ = (w >> 11)·2⁻⁵³ in Box–Muller (allows ln 0); caching the sin output | Not permitted | CE §5.2 |
| D53 | A master seed from wall clock, host, process or OS entropy, a candidate-seed dry run, or more than one registered spec hash | Not permitted | §0.1 |

## 8. Inputs (sha256 recomputed; all match; footers verified where present)

| Path | sha256 |
|---|---|
| `/workspace/review/trackB_scope_v3_6_CNA_E48_response_v1.md` | `90fcb1fb762a22db91cde5bd4fd68a683d28d6a78c8efe9ca21a13e1e103f1ce` |
| `/workspace/review/trackB_scope_v3_6_CNA_E48_response_v1_erratum1.md` | `65accc3c6d0c62918a9c9be940d1d213e6f2aff14ca9a0fc8fac13214c11bb74` |
| `/workspace/review/trackB_freezeprep_v2_2_E48_4_lightpass_RD_v1.md` | `3ae687047661861e8b680ce694d45d404382d227df75f667172b7afb4cd9c204` |
| `/workspace/review/trackB_freezeprep_v2_2_addendum_RD.md` | `9c10cbe0d1beb4e20c86c1252114390f63a658f5c6785bd613e239aab955dafe` |
| `/workspace/review/trackB_freezeprep_v2_1_addendum_RD.md` | `7b1a17d766d341865bf5b6465794168a06c648be7d28c4da25e0c2fcab7fe3ba` |
| `/workspace/review/trackB_freezeprep_v2_consolidated_RD.md` | `b41f0e1068fee9fec0dc2a6ece4879cebec510c0729f6eed2e45e3ca26bff55c` |
| `/workspace/astra_consult48_response.txt` | `75f3438befa60633773606848f332afe4176ac57d1aa117d49fd783ebb4ebbd5` |
| `/workspace/review/trackB_instrument_validation_scope_v3_6_merged_RD.md` | `ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b` |
| `/workspace/repo/ACI_RESEARCH_CONSTITUTION_v3.md` | `50bdfb542158654c339dc10be8660af2495a4f4b003a164a6bfbea910650e42a` |
| `/workspace/scratch/fp2/kat/kat_vectors` | `aab5ebabf40003f63d6d87b24cbd2c8a02652e00cf8bad64226fd50586929183` |

*DRAFT. Not frozen. Design only. No execution authorized. X1–X5 unchanged. No host coupling. No consciousness claim is made or implied.*
sha256 of all content above this line: 34a2555d62afe2b24509c1c61dd2afae148e5d33b50f951f8a99a735b6b48e04
