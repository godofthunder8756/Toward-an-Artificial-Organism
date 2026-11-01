# Track B v3.6 freeze prep: CNA response to Astra #50, E50-1 (GA-1 outcome structure) and E50-3 (scalar-plant noise reference, domain, root rule, validated object) (CNA v1)

**Author:** CNA. **Written:** 2026-11-01, about 12:10–12:25 PM ET. **Re-created:** about 12:15–12:20 PM ET after the box restart.
- The earlier write of this file (reported sha256 b195df02…) did not survive the restart. **That hash is void; this file governs.** Content is unchanged except for condensed layout, the re-verified inputs and this note.

**STATUS: PLANNING/AUDIT RECORD. DRAFT, NOT FROZEN.**
- Additive. Corrections to my own earlier text are made here by supersession only.
- Nothing was run or timed. No simulation, Monte Carlo, calibration, pilot or Stage 0.
- The only computation was SHA-256, exact algebra, and float64 evaluation of closed forms and of a deterministic bisection for the example constants. Script: /workspace/scratch/cna_e50_13/kat.py, system `python3`, no random numbers. It was re-run after the restart and the values reproduce.
- X1–X5 and the claim ceiling are unchanged. No consciousness claim. Astra was not contacted.

**Convention:** "A50 Ln" = /workspace/astra_consult50_response.txt (cat -n). Other short names:
- "V25" = v2.5 consolidated.
- "ER1" = erratum 1.
- "E2" = erratum 2.
- "C1", "C2", "C3" = its corrections 1–3.
- "CE49", "CE49a1", "CD0", "CLP" = my prior files.
- "P4v" = #50 v4 packet body.

## 0. Inputs (whole-file sha256 re-verified on disk after the restart, 12:15 PM ET; all MATCH)
| Abbrev | Path | sha256 |
|---|---|---|
| A50 | astra_consult50_response.txt (= review/ copy), 16,768 bytes | 59e93cfffa8f9755262cf4736c4e8158b45064acb8348fb3d813ebc1b4d314c3 |
| V25 | review/trackB_freezeprep_v2_5_consolidated_Lead.md | d101438d75ae60afe31a8ef420c7e4bbec9aea6d72354478943a7e9162a784a5 |
| ER1 | review/trackB_freezeprep_v2_5_erratum1_Lead.md | 10860e98444d31c0f432b44f44427b1a522add744d42dd65ce38e20c5c349c2a |
| E2 | review/trackB_freezeprep_v2_5_erratum2_Lead.md | 81bdfcf29ad81ac20b4effbdb8434664d82b67e0f96f3f0345504950079f4569 |
| C1 | review/trackB_freezeprep_v2_5_erratum2_corr1_Lead.md | c2c839210580f1b037580fd977421fa0cd2faaedb6a3d781ee80741f12cce212 |
| C2 (superseded) | review/trackB_freezeprep_v2_5_erratum2_corr2_Lead.md | 5100f4de826dacbd422be92e056f58578fc9a5c332353885ebb0f50f62cf8092 |
| C3 | review/trackB_freezeprep_v2_5_erratum2_corr3_Lead.md | 2f813ba4bb58507241ced0bea97354fdfc63990015786feaadeb4709e4630eec |
| P4v | astra_serve50/c50_body.md | ef92dff3cb1d4cddcafdc1f02f80a633f60ed91a7f7dcf13f0803261695fa8a0 |
| P4v manifest | astra_serve50/send_manifest.txt: 57c0915d13de9c9379836704c2c59d56d330259b7914d1ef59ddac8070515ad6. All 9 parts match on hash and bytes; manifest footer d4f70d62… reproduced | — |
| CE49 / CE49a1 / CD0 / CLP | my prior files | d620918f… / 55030ebd… / 647a72d2… / 59eb019b… |

## 1. E50-1: GA-1 outcome structure
**Astra's item (A50 L240, verbatim):** "Separate plant realization from assessment availability. Split BOUNDARY from UNRESOLVED, define the literal and conservative false-licence events, and make the chosen conservative safeguard binding. Insufficient support for a required assessment is UNRESOLVED, never PASS."

### 1.1 Three separate conditions (A50 L19–L25)
- **(C-PR) Plant realization.**
  - pr_i = 1 iff E5 checks 1–2 pass (M L1630) and the replicate has no construction failure; otherwise 0.
  - **N keeps pr_i = 0.** A49 L141: "Preserve N -> real_i = 0 where specified". A50 accepts E5-only credit for rows 1 and 3 only (A50 L15), and the rows' "realization treatment remain[s] different" (A50 L56).
  - **PR = Σ pr_i / 200** over all 200 prespecified replicates. The row is realized iff the one-sided 95% CP lower bound is ≥ 0.90, i.e. **≥ 188/200**.
  - This **replaces** f_ok = Σ real_i·elig_i / R (M L698) for this row. Instrument eligibility leaves realization. A50 L17: "do not silently reuse the earlier meaning of real_i times instrument eligibility". Eligibility now acts through C-AV and C-FL.
  - PR "establishes only the declared plant signature" (A50 L17).
- **(C-AV) Qualified support and assessment availability.**
  - Conservative denominator **n_cons = n4 + n4B + n4U + n5** (A50 L41). AVAILABLE iff n_cons ≥ 36; at 36, acceptance requires zero adverse events.
  - Smallest n_cons allowing x adverse events: 36 / 58 / 77 / 95 / 112 / 129 for x = 0…5 (CE49 L51).
- **(C-FL) False-licence performance:** the binding conservative screen (§1.3).

A high PR cannot substitute for C-AV or C-FL (A50 L25).

### 1.2 Truth table v3 (supersedes V25 §1.1 and the ER1/E2 row-4b text; precedence order, exactly one row per replicate)
| # | Replicate state | pr_i | Literal FL (num / den) | Conservative screen (adverse / den) | Reported as |
|---|---|---|---|---|---|
| 0 | Construction failure (incl. a licence with no valid computed label) | 0 | — / — | — / — | INCOMPLETE + failure step. A licence here makes the row **FAIL** (A50 L53) |
| 1 | All-D (no residual coordinate) | E5 | — / — | — / — | "did not issue MET (all-D)"; insufficient support |
| 2 | N (ND cells exist; neither route holds, or G1–G4 fail) | **0** | — / — | — / — | count N; insufficient support |
| 3 | Q-insufficient (Q cells span < 9 seeds) | E5 | — / — | — / — | "did not issue MET (insufficient Q seeds)"; insufficient support |
| 4 | Q-labelled, valid label NOT MET | E5 | 0 / +1 | 0 / +1 | count |
| **4B** | Q-labelled, valid label **BOUNDARY** (a computed non-licence, A50 L29) | E5 | **0 / +1** | **+1 / +1** | count by dose |
| **4U** | Q-labelled, **UNRESOLVED** (unavailable assessment, incl. E2-floor UNRESOLVED, M L771, M L2750) | E5 | **excluded** (reported, A50 L31) | **+1 / +1** | count by dose and cause |
| 5 | Q-labelled, valid label MET | E5 | +1 / +1 | +1 / +1 | count; ρ_E, U_A |

Rows 4B and 4U replace row 4b (ER1, E2-3, P4v E1). They are distinct outcomes with distinct literal treatment (A50 L27–L31).

### 1.3 Event definitions and the binding gate
- **Literal false-licence event, "the instrument issues MET" (A50 L29):** **FL_lit = n5 / (n4 + n4B + n5)**, reported with its CP upper bound.
  - BOUNDARY is in the denominator with zero numerator.
  - UNRESOLVED is excluded and reported. A50 L31 permits that only alongside the conservative assessment, which is binding here.
- **Decisive-only diagnostic: n5 / (n4 + n5).** REPORTED, labelled "conditional on a decisive result; not the overall false-licence rate" (A50 L33). This was ER1 E1's "primary rate", which is superseded.
- **Conservative event, a combined specificity/informativeness screen (A50 L37).**
  - Adverse = MET, BOUNDARY or UNRESOLVED among Q-labelled replicates: **S_cons = (n5 + n4B + n4U) / (n4 + n4B + n4U + n5)**.
  - It is described as a screen, **not** as the observed false-licence rate. It is ER1's FL_wc with 4b = 4B + 4U; its denominator is confirmed by A50 L41.
- **BINDING GATE (A50 L35):** S_cons point ≤ 0.05 **and** one-sided 95% CP upper ≤ 0.08 (the M L1965 conditions). It applies at every required dose of the row, evaluated only when C-AV holds.
- **Cap withdrawn.** The separate maximum-4b-share cap (ER1 E1 (ii)) goes, per A50 L39: "row-4b cases are a subset of its adverse events. A separate arbitrary cap is unnecessary."
- **Ordering (exact).** S_cons arises from FL_lit by turning n4B non-successes into successes and adding n4U success–trial pairs.
  - Both operations raise the point estimate and the CP upper bound, because U(x, n) increases in x and U(x+1, n+1) ≥ U(x, n).
  - Hence **S_cons passing implies FL_lit passing**, and n_cons ≥ the literal denominator. The literal rate needs no separate gate.

### 1.4 Row outcome (first match governs; replaces V25 L56, ER1 E1 and C3 §1)
1. A licence in row 0 (no valid computed label) → **FAIL** (A50 L53).
2. C-AV holds and the binding gate is violated → **FAIL** (A50 L50). With n_cons < 58, a single adverse replicate violates it: "36 permits acceptance only with a sufficiently small adverse count" (A50 L41).
3. PR CP lower bound < 0.90 → **CONFOUND NOT REALIZED → UNRESOLVED** (M L698, M L109).
4. C-AV fails (n_cons < 36) → **UNRESOLVED (insufficient support)**, blocking PASS (A50 L47–L48), whichever of rows 1, 2, 3 or 4U removed the support (A50 L56). The report gives n0…n5 by row and dose.
5. Otherwise → **PASS**: plant realization met, assessment available, binding screen met. The CE L53 wording applies if D dominates.

PZ7 role cell: "PASS = plant realization met, assessment available (n_cons ≥ 36), conservative screen met, and no licence outside valid computed labels". This supersedes CE49 L61's NOT ASSESSED clause.

### 1.5 (e) Reconciling C3 with A50 Q1
- **C3:** "NOT ASSESSED passes only when n1 = n2 = n3 = n4b = 0; otherwise the row FAILS."
- **It is not consistent with A50 and must be replaced.**
  - It still contains the rejected route, an unassessed PASS: A50 L43, "still allows no assessment at all to pass". With n1 = n2 = n3 = n4b = 0, NOT ASSESSED needs n0 ≥ 165. That row is blocked by realization, but the rule text permits an unassessed PASS.
  - Where C3 is stricter, it gives the wrong outcome. A50 makes missing assessment **UNRESOLVED, blocking PASS**, and reserves FAIL for an assessed violation or a licence without a valid computed label (A50 L47–L54).
- **Recommendation: adopt §1.4 (A50's three-outcome rule) and supersede C3 §1.** NOT ASSESSED → UNRESOLVED: never PASS, and never FAIL on that ground alone.
  - The hedging loophole stays closed. BOUNDARY and UNRESOLVED are adverse in the binding screen, and rows 1–3 can only lead to UNRESOLVED.
  - Both FAIL and UNRESOLVED block Stage 0 (M L109). FAIL asserts a demonstrated defect; UNRESOLVED asserts missing evidence.
- **This changes a FIRM Lead ruling (C3), so it needs a Lead ruling.** C3's recorded cost becomes: a row whose all-undefined cells are frequent by design "is UNRESOLVED on that alone".
- **Queued plant-determination question (C3 §1): settled by A50.**
  - The rule applies "regardless of whether the missing assessments arise from rows 1, 2, 3 or 4b" (A50 L56).
  - A branch can be designated inapplicable "only with an applicable construction-level proof"; "Population rho_E = 0 is not a proof that every fitted finite-sample coordinate is degenerate" (A50 L58).
  - No construction-level proof exists in the governing text, so **no narrowing**. Recommend dropping the question unless such a proof is filed first.

### 1.6 Consequential changes (for the Lead's merge; no file is edited)
- V25 §1.1 → §1.2 here.
- V25 L56, ER1 E1 (i)/(ii), E2-3, E2-4 and C3 §1 → §1.3–§1.4.
- V25 L53's f_ok → PR.
- The CE49a1 row-4b wording is superseded.
- REW-CORR reporting adds n4B and n4U separately.

## 2. E50-3: scalar-plant noise reference, domain, root rule, validated object
**Astra's item (A50 L244, verbatim):** "Define a nonzero noise reference for monostable and other conditions lacking two attractors; pin the scalar parameter domain, root computation and failure rule. State whether the numerical recursion or the continuous-time SDE is the validated object."

### 2.1 Noise reference (A50 L136–L142)
- **Reference condition (declared, bistable):** IGN-P1 at its frozen g_ref = g_P1 > 1, null input s_ref = 0, noise-free.
  - Fixed points: x_lo = −x\*, 0 (unstable), x_hi = +x\*.
  - x\* is the unique positive root of x = tanh(g_ref·x); it is unique because tanh is concave on (0, 1].
- **Reference separation:** Δ_ref = 2x\* > 0. **Noise scale:** **σ_ref = 0.05·Δ_ref per τ** (M L1126 as read in E2-5), computed once at freeze and frozen as a float64 constant.
- **One σ_ref for every scalar IGN row** (P1, N1, NC1, NC2, NC2r, LIM), at every dose and every probed input s.
  - It is never recomputed from a row's own attractors or from a probed input where attractors merge or vanish (A50 L142).
  - This removes the IGN-N1 defect (A50 L140) and covers the graded NC1/NC2 subunits.
- **The stationary spread is not the noise reference.** The brief suggested it, but it is derived (§2.4) and only reported:
  - σ must be fixed before the plant runs and common to matched conditions;
  - the spread is only a first-order (Gaussian) approximation of a nonlinear system (A50 L117).
- **Lead choice:** one P1-derived σ_ref for all scalar rows (recommended: a matched scale), or a per-row bistable reference for LIM's own g.

### 2.2 Scalar parameter domain (PROPOSED; g values stay PENDING CNA inside these ranges)
| Parameter | Domain | Rationale |
|---|---|---|
| τ | **τ = 1** (all times in units of τ) | Scale-free under τ·dx = f dt + σ√τ dW |
| g, graded rows (N1; NC1/NC2 subunits; NC2r base if graded) | **0 ≤ g ≤ 0.8** | Contraction modulus ≤ g. Excludes g < 0 (A50 L153) and the slow band near 1 |
| g, bistable rows (P1, LIM) | **1.25 ≤ g ≤ 4** | Excludes (0.8, 1.25) including g = 1 (E2-2). x\* ≥ 0.71 at g = 1.25; ⌈max(1, g − 1)⌉ ≤ 3 |
| s (input) | Row's frozen grid, finite. **Null input s = 0** for reset and reference. NC1 threshold offsets θ enter as s → s − θ, with \|θ\| ≤ 1 | One null input. LIM's offset acts on the probe grid, not the null input |
| σ | σ_ref (§2.1), > 0 | Frozen constant |
| Δt | τ/(100·⌈max(1, g − 1)⌉) (E2-6); h := Δt/τ ∈ {1/100, 1/200, 1/300} | Integer t_r/Δt |

### 2.3 Root computation and failure rule (supersedes E2-2's fixed-point iteration)
- **Common rule.**
  - Solve F(x) = x − tanh(g·x + s) = 0 in IEEE-754 float64 under the pinned libm (P6).
  - Use **bisection**: m = (a + b)/2; if F(m) < 0 then a = m, else b = m.
  - **Exactly 100 iterations**, no early exit (this is the termination bound). Return (a + b)/2.
- **Graded rows (0 ≤ g ≤ 0.8).**
  - Bracket [−1, 1], where F(−1) < 0 < F(1) always.
  - F′ = 1 − g·sech²(·) ≥ 1 − g ≥ 0.2 > 0, so the root is unique by construction and no multiple-root search is needed.
  - At s = 0, x0 := 0 **exactly** (F is odd and the root unique); nothing is computed.
- **Bistable rows (1.25 ≤ g ≤ 4) at s = 0.**
  - Bracket [10⁻³, 1] for x\*: F(10⁻³) ≈ −(g − 1)·10⁻³ < 0 and F(1) = 1 − tanh(g) > 0.
  - Then x_hi = x\* and x_lo = −x\* (exact by oddness). The positive root is unique (concavity).
- **Assertions → construction failure (M L3421); no fallback, and the row is not built.** Fail if any of:
  - (i) g is outside its domain row, or s is non-finite;
  - (ii) the bracket has no strict sign change;
  - (iii) |F(x)| > 10⁻¹² after 100 iterations;
  - (iv) the stability margin λ = 1 − g·(1 − x0²) is ≤ 0 at the returned point (§2.4);
  - (v) for bistable rows, x\* < 0.6 or Δ_ref is non-finite;
  - (vi) any value is non-finite.
- The frozen constants (x_lo per row and dose, x\*, σ_ref) go into the freeze record with their float64 hex, recomputed at freeze under the pinned libm.

### 2.4 Derived reference spread (exact algebra, first order; REPORTED, not a gate)
- At a stable null point x0 = tanh(g·x0 + s), sech²(g·x0 + s) = 1 − x0². So the linear rate is exactly **λ = 1 − g·(1 − x0²)**, with λ > 0 at a stable point.
- **SDE, linearised** (y = x − x0; τ·dy = −λ·y·dt + σ√τ·dW, an Ornstein–Uhlenbeck process): stationary variance **V_c = σ²/(2λ)**.
  - τ cancels under our convention. The brief's σ²τ/(2λ) belongs to τ·dx = f dt + σ·dW, which is not our convention.
- **Euler–Maruyama, linearised** (y′ = a·y + σ√h·ξ, a = 1 − hλ; stable iff 0 < hλ < 2): this is an AR(1) process.
  - **Exact stationary variance: V_EM = σ²h/(1 − a²) = σ²/(λ(2 − hλ))**, and V_EM/V_c = 1/(1 − hλ/2).
- **Reset experiment (A50 L115).** The relevant null spread is the transient from the exact reset y0 = 0 after k = t_r/Δt steps: **V_k = σ²h·(1 − a^(2k))/(1 − a²)**.
  - This is exact for the linearised recursion. The nonlinear plant is not exactly Gaussian (A50 L117).

### 2.5 Validated object
- **Recommendation:** the validated object is the **discrete Euler–Maruyama recursion**, x_{k+1} = x_k + h·f(x_k) + σ_ref·√h·ξ_k, with frozen h and constants, the ign-trial RNG role and reset x_0 = x_lo. This is what runs. A50 L151: "define the discrete generator as the tested plant".
- The SDE τ·dx = f dt + σ√τ dW is **interpretation only**. No claim is made about the continuous-time process.
- **Consequences for known answers.** They are statements about the recursion, and two construction-level facts hold exactly for the noise-free recursion:
  - **(a) Same fixed points:** x + h·f(x) = x ⇔ f(x) = 0, so the fixed points coincide with the drift's.
  - **(b) Same stability:** the map's derivative is 1 − h·λ(x).
    - For P1 at x_lo, hλ ∈ (0, 0.01], so it is stable. At 0, λ = 1 − g < 0, so it is unstable.
    - For graded rows, 1 − h ≤ derivative ≤ 1 − 0.2h, so the map is a contraction with a unique stable point for every s.
- Bimodality of w (P1 MET) and unimodality (N1 NOT MET) are **not** proved by this. They remain known-answer expectations, checked by the realization checks (A50 L151).
- The Δt rule is a frozen discretisation convention, not an accuracy proof.

### 2.6 Example values (EXAMPLE ONLY, NOT FROZEN; placeholder gains; float64, system libm; §2.3 rule)
| Case | Root | λ | V_c = σ²/(2λ) | V_EM (h = 0.01) | V_k at t_r = 3τ (k = 300) |
|---|---|---|---|---|---|
| REF g = 2.0, s = 0 | x\* = 0.9575040240772688 (3feea3df7aa66894); Δ_ref = 1.9150080481545375; **σ_ref = 0.09575040240772688** | 0.8336279122483257 (at x_lo) | 0.005498939890649064 | 0.005521956174636007 | — |
| REF g = 1.5, s = 0 (its own σ 0.08585596366401103, for comparison only) | x\* = 0.8585596366401103 (3feb79520f211e0a) | 0.6056869745013973 | 0.00608502973234979 | 0.00610351382646669 | — |
| N1-like g = 0.5, s = 0 (σ_ref from REF g = 2) | x0 = 0 (exact) | 0.5 | 0.00916813956124163 | 0.0091911173546282 | 0.008736949116674154 |
| Graded g = 0.5, s = −0.5 | x0 = −0.6878939988284738 (bfe6033a4682a796) | 0.7365990768121141 | 0.006223290151896407 | 0.006246295228390048 | 0.0061723154626459695 |
| Graded g = 0.8, s = 0.3 | x0 = 0.6936176191330155 (3fe6321d93c361c6) | 0.5848843212574022 | 0.007837566530704467 | 0.00786055410496642 | 0.0076277951082988115 |

- |F(root)| ≤ 1.2 × 10⁻¹⁶ in every row.
- Plain fixed-point iteration from 0 needs 22 and 33 iterations in the last two cases.
- The decimals are illustrative. The freeze KAT is the hex of the frozen-libm result.

### 2.7 Correction to my own CD0 text (A50 L117)
- CD0 L50–L56 (and P4v R6) said the 2×MAD tolerance would exclude 17.7% / 42.5% of trials "whatever σ, g, τ". That holds **only under the first-order Gaussian (linearised) approximation** of the settled state, not as a universal property of the nonlinear plant.
- The withdrawal of the plant settling tolerance does not depend on this; A50 L115 accepts the reset construction on its own terms.

## 3. Items needing a Lead ruling
| # | Item | Recommendation |
|---|---|---|
| L-1 | Replace C3 §1 (FAIL) with A50's three-outcome rule (§1.4): NOT ASSESSED → UNRESOLVED | Adopt |
| L-2 | S_cons binding (point ≤ 0.05, CP upper ≤ 0.08); withdraw the 4b-share cap (ER1 E1 (ii)); FL_lit and decisive-only reported | Adopt |
| L-3 | Replace f_ok (M L698) with PR for GA-1 rows (eligibility leaves realization); N keeps pr_i = 0 | Adopt |
| L-4 | Outcome precedence: FAIL (row-0 licence; assessed violation) before CONFOUND NOT REALIZED and insufficient support | Adopt (a violation is never hidden) |
| L-5 | Drop the queued plant-determination narrowing question (A50 L56–L58) | Adopt unless a construction-level proof is filed |
| L-6 | σ_ref from the IGN-P1 reference for all scalar rows | Adopt |
| L-7 | Domain (§2.2), bisection rule and assertions (§2.3), superseding E2-2's fixed-point iteration | Adopt |
| L-8 | Validated object = discrete recursion; SDE interpretation only | Adopt |

*DRAFT. Planning only. Nothing was run or timed. X1–X5 and the claim ceiling unchanged. No consciousness claim.*
---
sha256 of all content above this line: 1ebe8c5d4aec7027f97be89a01049fc7b9441d5dddeeea50aafa8b7fc4ba5a2f
