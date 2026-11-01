# Track B v3.6 freeze prep: CNA response to Astra #51, E51-1 (row-0 accounting) and E51-3 plant half (scalar reset, root rule, NC2 dose quantiles) (CNA v1)

- **Author:** CNA (scope-conformance owner). **Written:** 2026-11-01 13:02:36 EST (America/New_York, from `date` at write time).
- **Status:** PLANNING/ASSESSMENT ONLY. This is an additive file; no read-only file is rewritten. Nothing was run as an experiment, simulation or timing run.
  - The only computation was SHA-256, exact rationals, and a deterministic **noise-free** (σ = 0) float64 evaluation of the frozen recursion and the bisection. Script: `/workspace/scratch/cna_e51/nc2.py`, system `python3`, no RNG.
  - Floats come from the box libm and are **UNVERIFIED for the pinned libm (P6)**.
- X1–X5 unchanged. Astra not contacted. No consciousness claims. RD owns E51-2 and the fitter half of E51-3; this file fixes only labels and plant rules.
- **Abbreviations:** A51 Ln = astra_consult51_response.txt (cat -n); A50 = #50 reply; V26 = v2.6 consolidated; RDLP2 = RD light pass v2 of V26; RDPP = RD light pass of the params file and erratum1; CE50 / CE50a1 / CE50e1 = my E50 file, addendum1 and erratum1; PP = my params file; RD26 = RD's E50-2/E50-4 file; M = merged v3.6; MP = measurement plan v1.

## 0. Inputs (sha256 recomputed 12:58 PM EST, all MATCH)
| Tag | File | sha256 prefix |
|---|---|---|
| A51 | review/astra_consult51_response.txt (13,893 B; identical copy in /workspace) | f7f35ec21d37… |
| V26 | review/trackB_freezeprep_v2_6_consolidated_Lead.md | ff03eb81c158… |
| RDLP2 | review/trackB_freezeprep_v2_6_consolidated_lightpass_RD_v2.md | 77a889b36cde… |
| RDPP | review/trackB_scope_v3_6_CNA_E50_params_and_erratum1_lightpass_RD_v1.md | 12371a769217… |
| CE50 / CE50a1 / CE50e1 | review/trackB_scope_v3_6_CNA_E50_1_E50_3_v1{,_addendum1,_erratum1}.md | b5a880ea35a7… / fdba7c639e9e… / 42bf6c6d7538… |
| PP | review/trackB_scope_v3_6_CNA_E50_pending_params_v1.md | a1dc190a0583… |
| M / MP | review/trackB_instrument_validation_scope_v3_6_merged_RD.md / trackB_measurement_plan_v1_RD.md | ab80afa56ac1… / 1d5458e3319b… |

**Astra's items, verbatim.**
- E51-1 (A51 L183): "Close row-0 accounting for all missing-assessment causes. Construction/integrity failures must block; ordinary permitted incompleteness must not evade the conservative screen merely because it is not a quota shortfall. Scope the quota terminology to the relevant instrument."
- E51-3 (A51 L187): "Complete scalar reset and root rules, restricting the zero-root exception to graded plants. Pin NC2 dose quantiles and the fitter's bounds, restarts, termination and failure handling."

# Part I. E51-1: row-0 accounting

## 1. The two classes (A51 L28–L33)
- **BLOCKING (B-\*)**, from A51 L30: "A construction or integrity failure that invalidates the assessment: blocking, never absorbed as an acceptable missing fraction."
  - Any occurrence prevents PASS for the affected scope (replicate → row, or stage → study).
  - It is never absorbed into a denominator as an acceptable missing fraction.
- **PERMITTED INCOMPLETENESS (PI-\*)**, from A51 L31: "An ordinary incomplete assessment allowed by the protocol: retained adversely in the conservative screen, whatever its reason."
  - The replicate is counted **adverse in both the numerator and the denominator of S_wc**, whatever its reason code (A51 L33: "should not depend on the missing-result reason being spelled QUOTA-SHORTFALL").
- **Both classes.**
  - Realization gives pr_i = 0, and the replicate stays in the 200. This is M L3422's "stays in every denominator as a non-success", preserved for realization.
  - A licence issued inside either class → row **FAIL** (A50 L41: "Row-0 licences remain immediate failures").

## 2. Cause list (exhaustive over the frozen text I could find; first matching class governs)
| Code | Cause | Frozen source | Class |
|---|---|---|---|
| B-BUILD | Freeze-time construction failure: a root-rule assertion (i′)–(viii) (V26 L49–L55), a KAT/hex mismatch at freeze (V26 PD-5), n_q < 199 (AM-10), the NC2 bitwise pre-nonlinearity fixture (V26 L61), FIXTURE-FAIL (RD26 L107–L108), SD(z_R) = 0 or a zero declared scale (M L3407, L3411) | CE50 L147 "the row is not built"; M L3421 | **BLOCKING** (the row is not built, so the row is UNRESOLVED) |
| B-RUN | Runtime construction failure in a replicate: NaN/±∞ in any declared computation (M L3421); nonzero/0 in a ratio rule (M L3541) | M L3421–L3422 | **BLOCKING** (see §3: stricter than M L3422) |
| B-INTEG | Integrity failure: RNG stream reuse across roles (M L372 "never reused across roles"); fitting or selection touching final data (M L312–L313); partition overlap; a thread-pool assertion failing (RDPP §4); mismatched input hash or manifest; any undisclosed rerun or reassignment | as cited; the list is a CNA proposal | **BLOCKING** at the stage scope: every row computed in that stage has no label |
| PI-IGN-QUOTA | IGN final-partition bin quota shortfall: fewer than 100 eligible of 127 per (seed, required bin). This is V26's former code QUOTA-SHORTFALL, renamed and scoped (§4) | M L2009; CE50a1 R3 | PI |
| PI-SSTAR-NL | **Non-locatable selection fit** (RD request): the selection H1 fit fails, θ₁ ≤ 0, or ŝ\* lies outside [s_1, s_9]. **Cross-reference:** this is the existing frozen-text code **IGN-UA-SSTAR** (RD26 L52, L73; causes FIT-FAIL / NONINCREASING / OUTSIDE-LOW/HIGH). A51 L141: such cases "are non-locatable; they are not finite outside-grid estimates". **RD's E51-2 owns the exact definition; this file fixes only the label and its accounting** | RD26 L52; A51 L141, L185 | PI (adverse in S_wc; pr_i = 0). **Exception:** at IGN-LIM this outcome is the known answer (MP L88 "Must be UNAVAILABLE"), so it scores as a correct outcome there and never as adverse (§5, L-E3) |
| PI-ATTR-ACCRUAL | GA-1 / E-ATTR: a seed's usable-allocation quota (50 recipients with donors per seed) not met at the cap. That gives "any incomplete required pair → no confirmatory label" | M L2819–L2820 (D20 no-label, M L609) | PI |
| PI-CAP | Cap-limited work: "cap-limited work is INCOMPLETE, never passed" | M L368, L2499; A51 L177 | PI |
| PI-OPINT | Emergency operator interruption: "makes affected work incomplete" | M L294, L302; M L1337 | PI |
| (not row 0) | Undefined cells / all-D | CE50 §1.2 rows 1 and 3 | rows 1/3: insufficient support |
| (not row 0) | N, or Q cells spanning < 9 seeds | CE50 §1.2 rows 2 and 3 | rows 2/3: insufficient support |
| (not row 0) | Computed but unavailable assessment (E2 floor etc.) | CE50 §1.2 row 4U; M L771, L2750 | row 4U: already adverse in S_cons |
| (not row 0) | Zero-invocation required unit, D = 0 | M L3410 (g), L3424 | an assessed failure, UNRESOLVED |

- A cause not listed here is **BLOCKING by default** until the Lead names it as PI. No missing result is silently absorbed.
- This answers A51 L26: a non-quota construction failure cannot launder an adverse replicate, because it blocks, and a non-quota INCOMPLETE stays adverse in S_wc.

## 3. Generalised ROW0-FL (AM-1 v2; PROPOSED as an extension of the named override)
- Let **n0P** = the number of PI-\* replicates in the (row, dose), counted over every PI code, and **n0B** = the number of B-RUN replicates.
- **S_wc = (n5 + n4B + n4U + n0P) / (n4 + n4B + n4U + n5 + n0P).** This replaces V26 L27's n0Q (n0Q ⊂ n0P). The thresholds are unchanged: point ≤ 0.05 and one-sided 95% CP upper ≤ 0.08 (AM-8; A51 L15–L18).
- S_cons is unchanged: it keeps A50 L41's literal denominator n4 + n4B + n4U + n5.
- **Realization:** every row-0 replicate (B or PI) has pr_i = 0 and stays in the 200 (M L3422, preserved).
- **Stricter than M L3422 for B-RUN.**
  - M L3422 keeps a runtime construction-failure replicate as an INCOMPLETE non-success and makes the row UNRESOLVED only "if the row cannot meet its rule as a result".
  - A51 L30 requires it to block. So **n0B > 0 → the row cannot PASS** (UNRESOLVED-BLOCKED, §5 step 4).
  - This is a named A-2026-10-24 amendment, "ROW0-FL v2"; the blocking rule is consistent with M L2170 "never dropped, never reclassified".
- **Scope:** GA-1 rows and any Stage-0 row that uses S_cons/S_wc. All other Stage-0 rows keep M L3422 and M L2170 unchanged; they already count INCOMPLETE as a non-success. The Lead may extend B-RUN blocking battery-wide (L-E1).

## 4. Quota terminology, scoped per instrument (A51 L35)
| Instrument | Frozen "quota" | Unit | Shortfall consequence |
|---|---|---|---|
| **IGN** only | ≥ 100 eligible of 127 final-partition slots | (seed, required bin) | replicate INCOMPLETE (M L2009) → PI-IGN-QUOTA |
| **GA-1 / E-ATTR** (REW-CORR-E, M L1627) | usable allocations: 50 recipients plus donors, satisfying matching, caliper, support, donor-reuse and partition separation | seed (M L2819) | D20 no-label (M L2820) → PI-ATTR-ACCRUAL. Cells and seeds that exist but give too few Q seeds are row 3, not a shortfall |
| DISSOC | the same usable-allocation accrual | seed | INCOMPLETE (M L2818) |
| S-INT | executed-stop accrual under the cap | agent | INCOMPLETE/INCONCLUSIVE (M L2818); its own rules, not S_wc |
| others | none; M L3422 non-success | — | — |
- The IGN "per-(seed, bin)" quota is **not** imported into GA-1 (A51 L35). The GA-1 mapping to M L2819–L2820 is my reading. The Lead and RD (who own the E-ATTR pipeline) should confirm that GA-1 replicates use that accrual (L-E2).

## 5. Row decision table (first match governs; A51 L37, L179)
| Step | Condition | Outcome |
|---|---|---|
| 1 | B-INTEG in the stage | **BLOCKED (integrity)**: no label for any row in the stage, so no PASS and no FAIL |
| 2 | B-BUILD for the row | **UNRESOLVED (NOT BUILT)**: blocking (M L2170) |
| 3 | Any licence in a row-0 replicate (B-RUN or PI) | **FAIL** |
| 4a | S_cons available (n_cons ≥ 36) and violated | **FAIL** |
| 4b | S_wc available (n_wc = n_cons + n0P ≥ 36, so the denominator is nonzero) and violated | **FAIL** (an assessable failure takes precedence, A51 L37) |
| 5 | n0B > 0 | **UNRESOLVED (BLOCKED: construction failure)** |
| 6 | PR one-sided 95% CP lower < 0.90 | **UNRESOLVED (confound not realized)** |
| 7 | n_cons < 36, from whatever rows (1, 2, 3, 4B, 4U or row 0) | **UNRESOLVED (insufficient support)**. A larger S_wc denominator never compensates (A51 L22) |
| 8 | Otherwise: both screens available and passed | **PASS** |
- **Availability per screen** (A51 L37): S_cons needs n_cons ≥ 36; S_wc needs n_wc ≥ 36. A rate whose denominator is 0 is never computed. PASS needs step 8, so no unassessed screen can produce PASS.
- **Narrowing (A51 L179; A50 L58).** A branch (row 1, 2, 3 or 4B) is exempt from step 7 only if an applicable construction-level proof, made before execution, is filed. "population degeneracy alone is insufficient" (A51 L179). None is filed, so there is no exemption and narrowing stays closed.
- **IGN-LIM (MP L88):** PI-SSTAR-NL is the expected outcome there. LIM is scored by RD26 §1.3 (B), not by this table (L-E3).
- **Cost:** none. Accounting only; no trials added.

# Part II. E51-3 plant half

## 6. (a) Scalar reset rule (A51 L94–L104; AM-4, A51 L48)
- **Inputs.** The effective input is u = s − θ. The **reset input** is u_null = 0 − θ, where θ ≠ 0 only for NC1 subunits. The **trial input** is s_i, the probe value applied from step 1 to step n_EM.
- **Graded plants (g = 0.5: N1, NC1 subunits, NC2, NC2r base).**
  - x_lo := the unique root of x = tanh(g·x + u_null).
  - If u_null = 0 exactly (N1, NC2, NC2r), x_lo := 0 exactly (zero-root exception).
  - For NC1 (u_null = −θ ≠ 0), x_lo is computed by the §7 bisection.
- **Bistable plants (g = 2: P1, LIM).** u_null = 0. Compute the positive stable root x\* by bisection on [10⁻³, 1] and set **x_lo := −x\*** (exact float negation; A51 L98–L100).
  - LIM uses the same null input: its offset shifts only the probe grid (CE50 L131). So LIM's x_lo equals P1's.
- **Fixed reset.**
  - x_lo is computed once at freeze per (row, dose, subunit) and frozen as hex.
  - It is **never re-solved at a probed input, t_r, seed or replicate** (A51 L104: "Solving a new equilibrium at every probed input would change the reset experiment").
  - Every trial starts at x_0 = x_lo, with **x_ref := x_lo** (M L314; AM-4).
- **t_s = 0 (AM-4).** There are no settling steps. Step 0 is the reset state, and the probe s_i acts on updates 1…n_EM. The readout is x after exactly n_EM updates (CE50e1 (vii-b)), and w = |x_{n_EM} − x_ref|, read pre-nonlinearity (M L314).
- This is **a reset experiment, not stationary sampling** (A51 L48). No text may call it stationary.
- **Example frozen candidates (UNVERIFIED for P6):**

| Row / subunit | u_null | x_lo | hex | λ at x_lo |
|---|---|---|---|---|
| P1, LIM (g = 2) | 0 | −0.9575040240772688 | bfeea3df7aa66894 | 0.8336279122483257 |
| N1, NC2, NC2r (g = 0.5) | 0 | 0 (exact) | 0000000000000000 | 0.5 |
| NC1, θ = fl(s_c·2)/4 | −0.266419987676776 | −0.4588387483231416 | bfdd5d9d328bdeb5 | 0.60527 |
| NC1, θ = fl(s_c·3)/4 | −0.399629981515164 | −0.6060504319446108 | bfe364c3e01db88b | 0.68365 |
| NC1, θ = fl(s_c·5)/4 | −0.6660499691919399 | −0.785133941856442 | bfe91fd137681872 | 0.80822 |
| NC1, θ = fl(s_c·6)/4 | −0.799259963030328 | −0.8393379483559269 | bfeadbdb41cf5fca | 0.85224 |

## 7. (b) Root rule, complete (A51 L96–L110; supersedes CE50e1 E1-1(b) and V26 L53's blanket key)
- **Function:** F(x) = x − tanh(g·x + u), in float64 under the pinned libm.
- **Stability margin**, pinned in this float form: t = tanh(g·x_root + u), **λ = 1 − g·(1 − t·t)**. This equals A51 L108's 1 − g·sech²(g·x_root + u) in exact arithmetic.
- **When a root is solved.** Only at reset inputs u_null, never at probe inputs. A bistable root call with u ≠ 0 is a construction failure (B-BUILD).
- **Zero-root exception: GRADED ONLY.** Graded and u = 0 exactly → x_root := 0 with no call.
- **Bistable at u = 0.** There are three roots, −x\*, 0 and +x\*. The middle root 0 has λ = 1 − g = −1 < 0 (unstable; A51 L102) and is never used. Bisect for +x\* on [10⁻³, 1]; x_hi = x\*, x_lo = −x\*. λ is the same at ±x\* by oddness, 0.83363 at g = 2.
- **Brackets.** Graded [a, b] = [−1, 1]. Bistable [10⁻³, 1].
- **Endpoint pre-check.** Require F(a) < 0 < F(b) strictly.
  - An endpoint zero, F(a) = 0 or F(b) = 0, is a construction failure.
  - It is unreachable in the domain: for |u| ≤ S_max = 8 and g ≤ 0.8, |F(±1)| ≥ 4.54 × 10⁻⁸ (CE50e1 E1-1). For bistable rows, F(10⁻³) < 0 and F(1) = 1 − tanh(g) > 0.
- **Iteration.** Exactly 100 passes. In each pass:
  - m = 0.5·(a + b);
  - if F(m) < 0 then a = m; else if F(m) > 0 then b = m; else (exact zero) a = b = m.
  - Return **x_root = 0.5·(a + b)**.
- **Stagnation.** Once a and b are adjacent floats, m rounds to a or b and later passes are idempotent.
  - 100 is a deterministic operation count, not 100 extra bits of precision (A51 L106).
  - Box check: brackets stop shrinking by pass 58 (graded) and 53 (bistable) (RDLP V-9).
- **Post-assertions → construction failure:**
  - (iii) |F(x_root)| ≤ 10⁻¹²;
  - (iv) λ > 0;
  - (v) bistable: x\* ≥ 0.6 and Δ_ref finite;
  - (vi) all values finite;
  - (viii) 0 < h·λ < 2. This last check is local to the stable fixed point and **not a global accuracy certificate for the noisy recursion** (A51 L110).
  - Plus (i′) S_max swept over the whole frozen input table and (vii-a/b) integer n_EM (V26 L50–L54).

## 8. (c) NC2 dose quantiles (AM-3, A51 L47, L125)
- **Doses:** p ∈ {**4/5**, **3/5**}, exact rationals (CNA2 L297 "{0.8, 0.6} quantile"; V25 L164). Dose 0 = no clip (DOSE0).
- **Plant:** graded g = 0.5, G = 1, h = 1/100, x_0 = x_lo = 0, σ = 0 for the ceiling only.
- **Inputs (exact rule, V26 L58):** s_i = fl(s_c·m)/4 with integer m = i − 1, i = 1…9 (o = 0). s_c = 0.532839975353552 (3fe10d066b84a372).

| i (m) | s_i | hex |
|---|---|---|
| 1 (0) | 0 | 0000000000000000 |
| 2 (1) | 0.133209993838388 | 3fc10d066b84a372 |
| 3 (2) | 0.266419987676776 | 3fd10d066b84a372 |
| 4 (3) | 0.399629981515164 | 3fd99389a146f52b |
| 5 (4) | 0.532839975353552 | 3fe10d066b84a372 |
| 6 (5) | 0.6660499691919399 | 3fe550480665cc4e |
| 7 (6) | 0.799259963030328 | 3fe99389a146f52b |
| 8 (7) | 0.932469956868716 | 3fedd6cb3c281e08 |
| 9 (8) | 1.065679950707104 | 3ff10d066b84a372 |

- **Readout:** x_nf(s_i, t_r) = x after exactly n_EM integer updates x ← x + h·(−x + tanh(g·x + s_i)). n_EM = t_r·100·G ∈ {200, 300, 500} for t_r ∈ {2, 3, 5} (literal integers). Since x_ref = 0 and x ≥ 0 here, w_nf = x_nf.
- **Type-1 quantile:** sort the 9 values ascending, with each weighted 1/9. Index **j = ⌈p·9⌉**: p = 4/5 → ⌈36/5⌉ = **8**; p = 3/5 → ⌈27/5⌉ = **6**. c_p(t_r) = the j-th order statistic.
  - Assert that the 9 readouts are strictly increasing in i, so c_p = x_nf(s_j). This holds on the box.
- **Noise-free example values (UNVERIFIED for P6).** Readouts at t_r = 3: (0, 0.202447, 0.380256, 0.522427, 0.630487, 0.710969, 0.770643, 0.814991, 0.848098). These match RDPP L63.

| t_r (n_EM) | c_{4/5} (j = 8) | hex | c_{3/5} (j = 6) | hex |
|---|---|---|---|---|
| 2 (200) | 0.7236751313428893 | 3fe72858bfc17a96 | 0.6196396635762804 | 3fe3d4168f4baa88 |
| 3 (300) | 0.8149911622727751 | 3fea1468588fb2fb | 0.7109685643594419 | 3fe6c041258d0d4e |
| 5 (500) | 0.8683130490329827 | 3febc93872892cb0 | 0.7704177862870704 | 3fe8a743338b8289 |

- **Recorded ceilings (A51 L125).** These six ceilings are recorded per (dose, t_r), and the selected t_r picks one of them.
  - Discreteness: every p in (7/9, 8/9] gives j = 8, and every p in (5/9, 6/9] gives j = 6. So 0.8 and 0.85 would give the same ceiling. The frozen object is the recorded ceiling, not p.
  - The clip y = min(x, c) is applied **post-readout only**; the pre-nonlinearity w is unchanged (bitwise fixture, V26 L61).
  - **Noise-free ceilings do not establish realization under noise** (A51 L125). The post-nonlinearity D ≥ 2 check stays per replicate and binding.
- **KAT plan (P6):** freeze the hex of s_c, the 9 s_i, x\*, the x_lo table (§6), the 27 readouts and the 6 ceilings.
  - At construction, recompute them under the pinned libm and compare bitwise. Any mismatch is B-BUILD.
  - A second, independent implementation of the 27 readouts (same formula order) must agree bitwise.
  - No RNG. This is a fixed computation of 9 × (200 + 300 + 500) = 9,000 noise-free steps, off-total.
- **Cost:** none. The scheduled total stays at **4,005,072,000 + 45,720,000·n**.

## 9. Needs the Lead's ruling
| # | Decision | CNA proposal |
|---|---|---|
| L-E1 | ROW0-FL v2: S_wc uses n0P (all PI codes); B-RUN blocks the row (stricter than M L3422; A-2026-10-24); scope GA-1 plus S_cons/S_wc rows, or battery-wide | Adopt for GA-1; battery-wide is the Lead's call |
| L-E2 | GA-1 shortfall = M L2819–L2820 usable-allocation accrual → PI-ATTR-ACCRUAL; the IGN quota stays IGN-only | Adopt after RD/Lead confirm the E-ATTR pipeline |
| L-E3 | PI-SSTAR-NL = IGN-UA-SSTAR accounting; at IGN-LIM it is the known answer, not adverse | Adopt; RD's E51-2 owns the definition |
| L-E4 | B-INTEG list and "unlisted cause → BLOCKING by default" | Adopt |
| L-E5 | Decision table §5, including S_wc availability n_wc ≥ 36 and FAIL precedence (step 4b) | Adopt |
| L-E6 | Reset rule §6 (fixed x_lo per row/dose/subunit; bistable x_lo = −x\*) and root rule §7 (graded-only zero exception, endpoint-zero failure, exact-zero collapse, pinned λ) | Adopt; supersedes the V26 L53 blanket key |
| L-E7 | NC2 p ∈ {4/5, 3/5}, j ∈ {8, 6}, six recorded ceilings, KAT plan | Adopt |
No item changes the scheduled 4,005,072,000 + 45,720,000·n.

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 3444c7bfe9bbcfc4c5eeab25a9e9715102c15ee214ba76244ab11933d4f917dd
