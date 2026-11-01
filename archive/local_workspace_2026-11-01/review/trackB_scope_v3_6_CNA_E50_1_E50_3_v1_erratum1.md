# Track B v3.6 freeze prep: CNA E50-1 / E50-3 file, ERRATUM 1: response to RD's light pass (root rule, symbols, quote, narrowing, R3 worst-case screen) (CNA v1)

- **Author:** CNA (scope-conformance owner). **Date/time:** 2026-11-01, about 12:35 PM EST (America/New_York, from `date`).
- **Status:** PLANNING ONLY. This file is additive. It **does not rewrite** CE50 (`b5a880ea35a77ae2…`) or CE50a1 (`fdba7c639e9e0deb…`); both stay read-only and in force except where this erratum amends them. X1–X5 are unchanged. Astra was not contacted. No consciousness claims.
- **Computation:** exact rationals (Python `fractions`, integer `comb`), SHA-256, and deterministic float64 evaluation of tanh and the frozen 100-step bisection under the box's system libm. No RNG, simulation or timing was used. System libm is not the pinned libm (P6), so every float value below is **UNVERIFIED for freeze**.
- **Answers:** RD light pass `/workspace/review/trackB_scope_v3_6_CNA_E50_1_E50_3_lightpass_RD_v1.md`, sha256 **2b403bcb162b0c1f9da7776ee47e44b692f83bd4f228000aaaeb73c02a1f5aad** (recomputed 12:24 PM EST, MATCH; 236 lines; read in full).
- **Other inputs (recomputed, MATCH):** A50 59e93cff…; M ab80afa5…; CE50 b5a880ea…; CE50a1 fdba7c63…; RD26 8a369208…

| RD item | Verdict there | Disposition here |
|---|---|---|
| V-2 root-rule completeness | EDIT | **E1-1**: S_max, null keying, integer n_EM. Owned by CNA, PROPOSED |
| V-3 symbol k overloaded | EDIT | **E1-2**: k_FY, n_EM, r_q. RULED |
| V-4 quote at CE50 L40 | EDIT | **E1-3**: verbatim fix |
| V-15 narrowing nuance | OK (nuance) | **E1-4**: conditional wording. RULED |
| V-1 R3 hedging leak / M L3422 | EDIT | **E1-5**: option (b) S_wc binding. RULED, plus a named amendment |
| V-6 n_q guard | OK + note | **E1-6**: n_q ≥ 199 is a construction requirement. RULED |

## E1-1. Root rule: three additions to CE50 §2.3 (CNA-owned; PROPOSED for Lead adoption)
**(a) Effective-input bound S_max.**
- **Effective input** u := s − θ. Here θ = 0 except for NC1 subunit offsets (CE50 L131). The LIM offset acts on the grid itself, so it is already inside s.
- **Freeze S_max = 8: every frozen u (every grid value of every scalar row and dose, combined with every θ) must satisfy |u| ≤ 8.**
- **New assertion (i′), replacing CE50 assertion (i)'s s clause:** u non-finite **or |u| > S_max → construction failure** (M L3421). There is no clipping and no fallback, and the row is not built.
- Justification:
  - On the box libm, float64 tanh(y) returns exactly 1.0 for y ≥ 19.061547465398498 (bisected on the box; UNVERIFIED for P6).
  - The graded bracket evaluates tanh at ±g + u, with |g| ≤ 0.8 (CE50 L129). So the largest argument is 8.8, below half the saturation point.
  - At 8.8, 1 − tanh = 4.544 × 10⁻⁸ ≈ 2.0 × 10⁸ × 2⁻⁵². F(1) and −F(−1) therefore keep a strict sign change by about eight orders of magnitude more than any few-ulp libm discrepancy. Assertion (ii) cannot fire inside the domain.
  - Box check at g = 0.8, u = ±8: F(∓1) = ∓1.999999, F(±1) = ±4.544e−8, root ±0.9999999545590779, |F(root)| = 0. At g = 0, 0.5 and u = 8 the result is the same in kind.
  - Margin: the largest frozen |u| under the proposed grids is 1.99815 (LIM/1, pending-params §4). That is a 4× margin to S_max and about 9.5× to saturation.
  - Bistable rows solve roots only at u = 0 (CE50 L144), so the bound only constrains their probe inputs.
  - At freeze, the pinned libm must reproduce tanh(8.8) < 1 − 2⁻³⁰. That check is to be added to the P6 KAT list. Settled by P6.
- EM steps evaluate tanh(g·x + u) with no root solve, so saturation there is harmless and needs no assertion.

**(b) Null-input special case keys on the effective input.**
- CE50 L143's "At s = 0, x0 := 0 exactly" becomes **"x0 := 0 exactly iff u = s − θ = 0 exactly (float64 equality of the frozen constants); otherwise x0 comes from the 100-step bisection on [−1, 1]."**
- x_lo is frozen per row and dose (CE50 L154), so each NC1 subunit with θ ≠ 0 gets a bisected x0 = root at u = −θ.

**(c) EM step counts in integer arithmetic (symbol n_EM, E1-2).**
- **G = ⌈max(1, g − 1)⌉** is set by exact float64 comparisons: G = 1 if g ≤ 2; 2 if 2 < g ≤ 3; 3 if 3 < g ≤ 4. It is never derived from a float ceiling of a computed quotient.
- t_r is in integer units of τ (t_r ∈ {2, 3, 5}, τ = 1). **n_EM = t_r × 100 × G**, integer product, so n_EM ∈ {200·G, 300·G, 500·G}.
- The constant h = 1/(100·G) is used only inside the update and is never divided back. The time index is the integer step counter.
- **Never compute n_EM = t_r/Δt in floating point.** On the box, 3/(1/300) = 899.9999999999999, which truncates to 899.
- **New assertion (vii):** n_EM, computed in integers, equals the frozen table value for every (row, dose, t_r). Otherwise construction failure.
- **New assertion (viii)** (states CE50 L160's stability condition for the validated object): 0 < h·λ < 2 at every frozen x0. It holds automatically (h ≤ 0.01, λ ≤ 1); it is asserted, not assumed.
- **Cost:** none. The counts are the existing 500·G per trial (WL L17).

## E1-2. Symbols (RULED by the Lead; text only, no value changes; apply in the consolidated file)
| Old | Meaning | Source | New symbol |
|---|---|---|---|
| k | Fisher–Yates loop index, k = 507…1; counter (508 − k_FY, 0, 0, 0); j = w0 mod (k_FY + 1) | V25 L81 | **k_FY** |
| k | EM step count to readout, in V_k = σ²h(1 − a^(2k))/(1 − a²) | CE50 L162 | **n_EM**: V(n_EM) = σ²h(1 − a^(2·n_EM))/(1 − a²) |
| k | network quantile rank ⌈0.99(n_q + 1)⌉ | CE50a1 R4 | **r_q** |
- The bias bound becomes ≤ (k_FY + 1)/2⁶⁴, and the threshold T = X_(r_q).
- RD's proposal (n_step, k_q) is superseded by the Lead's symbols.

## E1-3. Quote correction at CE50 L40 (V-4)
- CE50 L40 has: the rows' "realization treatment remain[s] different" (A50 L56).
- **Replace with A50 L56 verbatim:** "Their causes and realization treatment remain different; their absence cannot demonstrate an unmeasured operating characteristic."
- The meaning is unchanged: N keeps pr_i = 0.

## E1-4. Narrowing of rows 1/2/3/4b (V-15; RULED: stays closed unless a construction-level proof is filed)
- CE50a1 L28's "closed by A50 L56–L58" becomes: **"Closed: no exemption from the insufficient-support rule for rows 1, 2, 3 or 4b unless an applicable construction-level proof, made before execution, is filed (A50 L56–L58)."**
- A50 L58, verbatim: "A branch can be designated analytically inapplicable before execution only with an applicable construction-level proof. Population rho_E = 0 is not a proof that every fitted finite-sample coordinate is degenerate."
- CE50 L100 and L-5 already carry this condition. No such proof exists in the governing text, so the question stays off the next consult until one is filed.

## E1-5. R3 quota shortfall: conflict conceded; binding worst-case screen S_wc (RULED: option (b))
- **Concession.** CE50a1 R3 classed quota-shortfall INCOMPLETE with row 0 and removed it from the FL_lit and S_cons denominators. That conflicts with M L3422 ("it stays in every denominator as a non-success") and leaves a bounded hedging gap.
  - RD V-1 gives an exact example: 20 adverse of 200 FAILs. If 12 of them become shortfall INCOMPLETE, the result is 8 of 188, which PASSes, while PR = 188/200 is still met.
  - Exact check here: 8/188 passes; 20/200 fails; the largest passing count at 200 is 9.
- **Ruled rule.** Let n0Q = number of quota-shortfall INCOMPLETE replicates (M L2009) in the (row, dose):
  - **S_wc = (n5 + n4B + n4U + n0Q) / (n4 + n4B + n4U + n5 + n0Q).** Each such replicate is adverse in **both numerator and denominator**.
  - **BINDING**, with the S_cons thresholds: point ≤ 0.05 **and** one-sided 95% CP upper ≤ 0.08 (M L1965; CE50 L73).
  - It is evaluated alongside the literal S_cons (A50 L41 denominator n4 + n4b + n5). **Both must pass.** Failing either → row FAIL (an assessed violation, CE50 §1.4 step 2).
  - C-AV (n_cons ≥ 36) is unchanged and is computed on S_cons's denominator.
- **Gap closed:** the example becomes (8 + 12)/(188 + 12) = 20/200 → FAIL. Converting adverse replicates into shortfalls can no longer raise either screen. S_wc ≥ S_cons whenever n0Q ≥ 0, because adding x to numerator and denominator raises the ratio when the ratio is ≤ 1.
- Kept from CE50a1 R3: a licence inside any INCOMPLETE replicate → row FAIL (CE50 §1.4 step 1; A50 L41 "Row-0 licences remain immediate failures"). pr_i = 0 for INCOMPLETE replicates, and PR keeps them in its 200, consistent with M L3422 as a non-success. Their count is reported under the reason code QUOTA-SHORTFALL.
- **Named amendment A-2026-10-24 "ROW0-FL" (RULED).** Ruled as the Lead's "row-0 realization overriding M L3422". This file reads it as follows:
  - For the GA-1 false-licence screens, M L3422's "stays in every denominator as a non-success" is overridden. INCOMPLETE replicates are **not** counted as non-events in FL_lit or S_cons, where that would lower the rate, which is anti-conservative (RD V-1).
  - They enter S_wc as **adverse**, and they enter realization as pr_i = 0.
  - **The Lead should confirm this reading of the amendment's scope (realization + FL denominators).**
- This deviates from A50 L41's conservative denominator and must be disclosed to Astra in #51.

## E1-6. Quantile guard (V-6; RULED)
- **n_q ≥ 199 is a construction requirement.** It is equivalent to r_q ≤ n_q − 1, so T is never the sample maximum. n_q < 199 → construction failure.
- This supersedes CE50a1 R4's n_q ≥ 99 guard. The event wording is frozen as **"coverage < 0.97": P[Bin(n_q, 0.97) ≥ r_q]** (5.6601 × 10⁻⁶ at n_q = 1,000, r_q = 991).
- The proposed n_q = 1,000 is in the pending-params file §2.2.

## E1-7. Ledger of status
| Item | Status |
|---|---|
| E1-1 S_max = 8; u-keyed null case; integer n_EM; assertions (i′), (vii), (viii) | PROPOSED (CNA); P6 check of tanh(8.8) pending |
| E1-2 k_FY / n_EM / r_q | RULED |
| E1-3 quote | Text fix |
| E1-4 narrowing wording | RULED |
| E1-5 S_wc binding; A-2026-10-24 "ROW0-FL" | RULED; scope reading to be confirmed by the Lead |
| E1-6 n_q ≥ 199 | RULED |
Cost: no change. The totals stay at 4,005,072,000 + 45,720,000·n_seed*.

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: fd5b764b5e2a728f6d86e10e1bf97a2640f8e918da827a0983410a1b2184e2e7
