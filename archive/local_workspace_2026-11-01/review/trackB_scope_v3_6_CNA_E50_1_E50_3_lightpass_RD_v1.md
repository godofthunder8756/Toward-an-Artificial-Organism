# Track B v3.6: RD light pass of CNA E50-1 / E50-3 (CE50) and its Addendum 1 (CE50a1)

- **Author:** Research Delegate (RD). **Written:** 2026-11-01, about 12:17–12:25 PM EST (America/New_York, from `date`).
- **Status:** REVIEW RECORD. DRAFT, NOT FROZEN. Additive; edits no other file. Errors found after locking go in a separate `_corr` file, never a rewrite.
- **Split:** RD closely reviews code paths, RNG, counters, root rule and stop/exit. RD lightly reviews scope and citations, which CNA owns.
- **Computation:** exact rational arithmetic (Python `fractions`, integer `comb`) and SHA-256. There was also a deterministic float64 evaluation of the closed-form root rule F(x) = x − tanh(g·x + s) under the box's system libm. It used no RNG and was not a simulation, Monte Carlo, calibration or timing run. Scripts: /workspace/scratch/rd_e50_13_lp/chk2.py and bis.py. System libm is not the pinned libm (P6), so float values are UNVERIFIED for freeze.
- X1–X5 and the claim ceiling are unchanged. No consciousness claim. Astra was not contacted.
- **Abbreviations:** CE50 = CNA main file; CE50a1 = its addendum 1; A50 Ln = astra_consult50_response.txt (cat -n); M = merged v3.6 (`ab80afa5…`); V25 = v2.5 consolidated; RD26 = my v2.6 E50-2/E50-4 file (+ corr1).

## 0. Hash verification (recomputed 12:17–12:20 PM EST)

Footer convention in both CNA files: the footer line gives the sha256 of all bytes above it, i.e. through the newline that ends the `---` line. I checked that convention; the alternative that excludes the `---` line does not match, as expected.

| File | Whole-file sha256 | Claimed | Footer recomputed | Claimed | Lines | Result |
|---|---|---|---|---|---|---|
| CE50 trackB_scope_v3_6_CNA_E50_1_E50_3_v1.md | b5a880ea35a77ae2de47dfd8d9bb2516d9e9b331f96c52ded8e123c780939f97 | b5a880ea… | 1ebe8c5d4aec7027f97be89a01049fc7b9441d5dddeeea50aafa8b7fc4ba5a2f | 1ebe8c5d… | 207 | **MATCH** |
| CE50a1 …_v1_addendum1.md | fdba7c639e9e0deb0d20829ac6e8829d7a0429292d94aa68d6a3540014c6fc7c | fdba7c63… | 36a2ad78a43cd553a5b843fd9a94f990d1c7f9bed0773532f3b9288cfc2f9bc7 | 36a2ad78… | 72 | **MATCH** |

Reference inputs (whole-file sha256, all MATCH):
- A50 59e93cff… (review/ and /workspace copies are identical)
- C3 2f813ba4…
- V25 d101438d…
- ER1 10860e98…
- E2 81bdfcf2…
- #50 v4 manifest 57c0915d…
- P4v body ef92dff3…
- M ab80afa5…
- RD26 8a369208…
- RD26 corr1 ebe3a08c…

Lead E50-5 ledger trackB_freezeprep_v2_6_E50_5_workload_ledger_Lead.md: whole-file 83247be974ce3da79735c0eb28cbb8eb80d476d1d00a07ea43b270bb7e33e5fe and footer 39371967c33a3c709e562490fe97cca7f4b3a9a71af3244393a3f8c3a2b1f269 both **MATCH**. Its L11 and L86 use **7,068,312,000** at n = 67. Not otherwise reviewed.

## 1. Verdict summary (EDIT/FAIL first)

| # | Item | Verdict |
|---|---|---|
| V-1 | R3: quota-shortfall INCOMPLETE classed with row 0 (outside S_cons) | **EDIT** (bounded hedging leak; conflicts with the M L3422 "every denominator" wording unless superseded) |
| V-2 | §2.3 assertions: completeness (s-range saturation, null-input special case, integer step count) | **EDIT** |
| V-3 | Symbol k overloaded (Fisher–Yates index, EM step count, quantile rank) | **EDIT** (minor, at merge) |
| V-4 | CE50 L40 quote of A50 L56 altered with "[s]" | **EDIT** (minor, citation) |
| V-5 | R4: rank, tails 5.66e-6 / 1.81e-5, and which event they are | **OK** (event is coverage < 0.97, *not* the 0.99-quantile reading) |
| V-6 | R4 guard: n_q < 99 → construction failure | **OK** (+ note: T = sample maximum for 99 ≤ n_q ≤ 198) |
| V-7 | LIM recost 4,005,072,000 + 45,720,000·n | **OK** |
| V-8 | S_cons definition, 95% CP level, min-n table, ordering claim, denominator 0 | **OK** |
| V-9 | Bisection bracket and 100-iteration bound | **OK** |
| V-10 | σ_ref = 0.05·2x*(g_P1) well defined | **OK** |
| V-11 | Validated object = EM recursion; §2.4 algebra; §2.6 example values | **OK** |
| V-12 | RNG roles and counters vs RD26 E50-4 and the Fisher–Yates counter | **OK** |
| V-13 | Stop/exit conformance, X1–X5 | **OK** |
| V-14 | §1.4 outcome rule; R1 (C3 superseded) | **OK** |
| V-15 | A50 L56–L58 "no narrowing" claim | **OK** (with wording nuance) |
| V-16 | L-2…L-8 vs RD26 | **OK** (one dependency left PENDING) |

## 2. Close checks (RD half)

### V-12 RNG roles and counters: OK
- CE50 adds **no** RNG role. Its EM recursion (CE50 L166) draws ξ from the existing `ign-trial` role: one normal per step, Box–Muller, counter t = trial step 1…N_steps (V25 L123, L191). CE50 does not change this.
- No overlap with RD26's `ign-null-centre` / `ign-null-quantile` (RD26 §2.3). Those are network-only. Scalar plants use the analytic reset x_0 = x_lo (CE50 L166), so they have no centre or quantile runs.
- The Fisher–Yates partition (role `ign-partition`, counter (508 − k, 0, 0, 0), idx = w0 mod (k + 1), k = 507…1; V25 L81) is untouched. CE50a1 R3's quota shortfall is a final-partition count. It triggers no top-up or redraw, so the 507 fixed draws and the "no outcome-dependent reassignment" condition (A50 L172–L173) stay intact.
- Counter range: for h = 1/300 and t_r = 5τ, N_steps = 1,500. That fits the u64 step word.

### V-3 Symbol collision: EDIT (minor)
"k" means three things:
- the Fisher–Yates loop index (V25 L81);
- the EM step count in V_k (CE50 L162);
- the quantile rank (CE50a1 R4).

PROPOSED at merge: rename them k_FY, n_step and k_q. Text only; no value changes.

### V-9 Bisection bracket and iteration bound: OK
- **Invariant.** The rule (CE50 L138) keeps F(a) < 0 ≤ F(b). This holds because F is evaluated deterministically and the bracket starts with a strict sign change (assertion (ii)).
  - Once a and b are adjacent floats, m = (a + b)/2 rounds to a or b.
  - The update then leaves the bracket unchanged, so the remaining iterations are idempotent: no cycling and no loss of the root.
  - (a + b)/2 cannot overflow on [−1, 1].
- **Graded bracket [−1, 1].** F(−1) = −1 + tanh(g − s) < 0 and F(1) = 1 − tanh(g + s) > 0 hold in exact arithmetic for finite s. See V-2 for the float64 caveat.
  - F′ ≥ 1 − g ≥ 0.2, so the root is unique (CE50 L142). Correct.
- **Bistable bracket [10⁻³, 1] at s = 0, g ∈ [1.25, 4].**
  - F(10⁻³) < 0: −2.4999935e-4 at g = 1.25, and it falls further as g grows.
  - F(1) = 1 − tanh(g) > 0, since tanh(4) < 1.
  - The positive root is unique: tanh(gx)/x is strictly decreasing on (0, ∞).
  - The outer roots are exactly ±x\*, x_lo = −x\* by exact float negation, and the middle root is 0. So there are exactly three fixed points at s = 0 for g > 1. Correct.
- **Is 100 iterations enough?** The deterministic evaluation (g step 0.01 over each domain; s ∈ [−10, 10] step 0.05 for graded rows) shows:
  - the bracket stops shrinking by iteration 58 (graded) and 53 (bistable);
  - the final width is ≤ 1.11e-16 and max |F(root)| = 1.11e-16 (CE50 L185 states ≤ 1.2e-16; consistent).
  - 100 is therefore sufficient, with margin.
  - Caveat: the resolution is absolute (2⁻⁹⁹ ≈ 1.6e-30), not 1 ulp, for roots with |x| below about 1e-14. This is harmless for a reset value, and CE50 L143 special-cases x0 = 0.
- The bistable domain minimum is x\* = 0.7104117834878703 at g = 1.25 (consistent with "x\* ≥ 0.71", CE50 L130). Assertion (v) (x\* < 0.6) therefore cannot fire inside the domain. It is a guard only, which is fine.
- min λ over the bistable domain = 0.38085612764802 (> 0). Assertion (iv) holds there.

### V-2 Assertion completeness: EDIT
The assertions CE50 L147–L153 lists are correct as far as they go. Three gaps:
1. **s range is unbounded ("Row's frozen grid, finite", CE50 L131).**
   - Float64 tanh returns exactly 1.0 for arguments ≳ 19.06 under this libm.
   - For example, g = 0.8, s = 18.5 gives F(1) = 0.0 in float64, and g = 0.8, s = −19 gives F(−1) = 0.0. Assertion (ii) then fires and the row is not built.
   - This is safe (fail-closed) but a planned-in failure. PROPOSED: CNA freezes a bound on the effective input, |s − θ| ≤ S_max, with S_max PENDING CNA, chosen so that g + S_max stays well below saturation under the pinned libm.
   - The saturation point above comes from system libm and is UNVERIFIED for P6.
2. **Null-input special case (CE50 L143) must key on the effective input.**
   - NC1 offsets enter as s → s − θ (CE50 L131), and x_lo is frozen "per row and dose" (CE50 L154).
   - State that "x0 := 0 exactly" applies only when the effective argument s − θ = 0. Otherwise x0 comes from bisection.
3. **Integer step counts.**
   - "Integer t_r/Δt" (CE50 L133) must be computed in integers: N = t_r·100·G with G = ⌈max(1, g − 1)⌉ and t_r in units of τ. Do not compute it by float division.
   - In float64, 3/(1/300) = 899.9999999999999; truncation would give 899 steps.
   - PROPOSED: add assertion (vii), "N_steps computed in integer arithmetic equals the frozen table value".
   - Optional: assert 0 < h·λ < 2 for the map. It holds automatically, since h ≤ 0.01 and λ ≤ 1, but it states the stability condition (CE50 L160) for the validated object.

### V-10 σ_ref well defined: OK
- g_P1 ∈ [1.25, 4] ⇒ the unique x\* > 0 exists ⇒ Δ_ref = 2x\* > 0 ⇒ σ_ref = 0.1·x\* > 0, finite and frozen once.
- Over the domain (system libm, UNVERIFIED for P6), σ_ref ranges from 0.07104117834878702 (g = 1.25) to 0.09993256730151082 (g = 4).
- This matches M L1126's σ = 0.05·‖x_hi − x_lo‖ at the reference, and A50 L142 ("Pin a positive reference separation from a declared bistable reference condition"). It is never recomputed per probe (CE50 L118).
- The g_P1 value itself is still PENDING CNA, so σ_ref has no frozen value yet.

### V-11 Validated object and algebra: OK
- EM: x ← x + h·f(x) + σ·√h·ξ with h = Δt/τ. This matches A50 L148–L149 and V25 L191.
- CE50 §2.4 algebra checked:
  - λ = 1 − g(1 − x0²);
  - V_c = σ²/(2λ) under τ·dx = f dt + σ√τ dW (τ cancels);
  - V_EM = σ²h/(1 − a²) = σ²/(λ(2 − hλ)), so V_EM/V_c = 1/(1 − hλ/2);
  - V_k = σ²h(1 − a^(2k))/(1 − a²).
  All are exact for the linearised recursion.
- The CE50 §2.6 example roots, hex bit patterns, λ, V_c, V_EM and V_k reproduce to every printed digit under system libm. These are EXAMPLE values, not frozen.
- Fixed-point and stability statements (a) and (b) (CE50 L169–L172): correct.

### V-13 Stop/exit conformance: OK
- CE50 and CE50a1 contain no stop, schedule, truncation, stop-step, stop-time, stop-log or sleep quantity. A case-insensitive grep for "stop|schedul|shutdown|truncat" returned no matches.
- No such quantity enters any policy, value, consolidation, dream or selection input.
- No shutdown-resistance objective is introduced. X1–X5 are restated (CE50 L10, CE50a1 L8).
- The CE50 §1.4 outcomes (FAIL / UNRESOLVED / PASS) are instrument-validation labels only.

## 3. Exact arithmetic

### V-5 R4 rank and tails: OK, event identified
- k = ⌈0.99·(n_q + 1)⌉; at n_q = 1000, 0.99·1001 = 99099/100 = 990.99 → **k = 991**. Correct.
- Exact rational sums at n_q = 1000:

| Event | k = 990 | k = 991 |
|---|---|---|
| P[Bin(1000, 0.97) ≥ k] = P(coverage F(X_(k)) < 0.97) | **1.8129913468e-05** | **5.6600699268e-06** |
| P[Bin(1000, 0.99) ≥ k] = P(X_(k) < true 0.99 quantile), continuous F | 0.58304080330 | 0.45730059217 |
| Expected coverage k/(n_q + 1) | 90/91 = 0.989010989… | 991/1001 = 0.990009990… |

- **The quoted 5.66e-6 (k = 991) and 1.81e-5 (k = 990) reproduce only as P[Bin(1000, 0.97) ≥ k]**: the probability that the threshold covers less than 97% of the null distribution (A50 L128–L130; RD26 §2.5). This is how CE50a1 L54 defines it, and it is correct there.
- Under the other reading, P[Bin(1000, 0.99) ≥ k], they do **not** reproduce: that event has probability ≈ 0.58 / 0.46.
- Any text that describes these figures as "the probability X_(k) falls below the 0.99 quantile" would be wrong. The frozen text should name the event as "coverage < 0.97".

### V-6 n_q guard: OK (with a note)
- k ≤ n_q ⇔ ⌈0.99(n_q + 1)⌉ ≤ n_q ⇔ 0.99(n_q + 1) ≤ n_q ⇔ n_q ≥ 99. Checked exactly: n_q = 98 → k = 99 > 98; n_q = 99 → k = 99.
- So "n_q < 99 → construction failure" is the correct threshold.
- **Note for the Lead.** For 99 ≤ n_q ≤ 198, k = n_q, so T is the sample **maximum**. k ≤ n_q − 1 needs n_q ≥ 199.
  - That is valid for the coverage claim (expected coverage k/(n_q + 1) ≥ 0.99) but sensitive to one extreme null run.
  - RD26 L202's "Require n_q ≥ 100, so that … k ≤ n_q − 1" was written for ⌈0.99·n_q⌉ and is superseded by the ruled k. RD will record that in an RD26 corr2 (pending; not done here).
  - Whether to require n_q ≥ 199 is a Lead choice: PROPOSED, not required.

### V-7 LIM recost: OK
- 15 × 267,004,800 = 4,005,072,000. 15 × 1,828,800 + 20 × 914,400 = 45,720,000.
- At n = 67: 7,068,312,000. At n = 9: 4,416,552,000.
- Identical to RD26 L175 and the E50-5 ledger (L11, L86).

### V-8 S_cons and the binding gate: OK
- **Definition.** S_cons = (n5 + n4B + n4U)/(n4 + n4B + n4U + n5) equals A50 L41's n4 + n4b + n5 with 4b = 4B + 4U. Both conditions are pinned at **one-sided 95%** CP (CE50 L73), matching M L1965.
- **Minimum-n table** (CE50 L46): exact check of U(x, n) ≤ 0.08 ⇔ P[Bin(n, 0.08) ≤ x] ≤ 0.05, plus x/n ≤ 0.05.
  - Minimum n for x = 0…5: **36, 58, 77, 95, 112, 129**. Reproduced.
  - The pass/fail boundary is monotone in n up to 400 for each x.
  - Max passing adverse count: 8 at n = 188, 9 at n = 200.
- **Ordering claim** (CE50 L75–L77): correct.
  - U(x, n) increases in x.
  - U(x + 1, n + 1) ≥ U(x, n), because P[Bin(n + 1, p) ≤ x + 1] ≥ P[Bin(n, p) ≤ x] for every p (couple Bin(n + 1) = Bin(n) + Bernoulli).
  - (x + 1)/(n + 1) ≥ x/n for x ≤ n.
  - So S_cons passing ⇒ FL_lit passing.
- **Small and zero denominators.** The gate is evaluated only when C-AV holds (n_cons ≥ 36; CE50 L73).
  - With n_cons = 0, S_cons is undefined and is never computed. §1.4 step 2 does not apply, and step 3 or step 4 gives **UNRESOLVED**. PASS is unreachable: step 5 needs C-AV.
  - At 36 ≤ n_cons < 58, one adverse replicate fails the gate.
  - FL_lit with a zero literal denominator (all Q-labelled replicates are 4U) is reported only, and S_cons = 1 → FAIL.
  - Correct throughout.

## 4. Light checks (CNA half)

### V-1 R3 quota shortfall → row 0: EDIT
- **Label: consistent.** M L2009: "bin shortfall → that replicate is INCOMPLETE and counted". This matches RD26 §1.2 G-ii.
- **Conflict with M L3422.** For Stage-0 rows, M says an INCOMPLETE replicate "stays in every denominator as a non-success". CE50 row 0 (and R3) removes it from the FL_lit and S_cons denominators. In PR it stays as pr_i = 0, which is consistent.
  - For a false-licence screen, M's "non-success/non-event" reading would *lower* S_cons, which is anti-conservative. Exclusion is better than that literal reading.
  - Even so, CE50/CE50a1 should state explicitly that §1.2 supersedes M L3422 for the FL_lit and S_cons denominators.
- **Hedging leak (bounded, exact).** Row-0 replicates leave the S_cons denominator. PR (≥ 188/200) caps them at 12 per (row, dose), counting all pr_i = 0 rows together.
  - Exact example: 20 adverse of 200 Q-labelled replicates is FAIL (max passing at 200 is 9). If 12 of the adverse replicates became quota-shortfall INCOMPLETE instead, the result is 8 adverse of 188, which PASSes, with PR = 188/200 still realized.
  - Eligibility is decided before labelling, so the label cannot *choose* a shortfall. But eligibility and adverse labels can be correlated through the plant or instrument state, and nothing in CE50 rules that out.
  - This is the hedging route the brief asked about, bounded at 12 replicates.
  - A50 L41 itself defines the conservative denominator without row 0, so closing the leak deviates from Astra's text.
- **PROPOSED options (Lead ruling):**
  - (a) Count quota-shortfall INCOMPLETE replicates as adverse (+1/+1) in S_cons. This is conservative and an "informativeness" failure; disclose it as a deviation from A50 L41.
  - (b) Keep the exclusion and add a binding worst-case S_cons including INCOMPLETE as adverse.
  - (c) Keep the exclusion and report the INCOMPLETE count per (row, dose) next to S_cons. This is weakest; the leak stays.
  - RD prefers (a) or (b). CE50a1 L48 already flags the mapping as a CNA reading pending Lead confirmation.
- The licence-in-row-0 → FAIL part is consistent with A50 L41 and L53–L54. OK.

### V-4 Quote alteration: EDIT (minor)
- CE50 L40 renders A50 L56 as "realization treatment remain[s] different".
- The verbatim text (A50 L56) is: "Their causes and realization treatment remain different; their absence cannot demonstrate an unmeasured operating characteristic."
- Quote it verbatim in the merge.

### V-15 A50 L56–L58 and narrowing: OK (nuance)
- A50 L56: "Apply the insufficient-support rule regardless of whether the missing assessments arise from rows 1, 2, 3 or 4b. Their causes and realization treatment remain different; their absence cannot demonstrate an unmeasured operating characteristic."
- A50 L58: "A branch can be designated analytically inapplicable before execution only with an applicable construction-level proof. Population rho_E = 0 is not a proof that every fitted finite-sample coordinate is degenerate."
- Astra does not say a flat "no". It says no narrowing **unless** a construction-level proof is filed.
- CE50 L100 and L-5 ("Adopt unless a construction-level proof is filed") state this correctly. CE50a1 L28 ("closed by A50 L56–L58") should carry the same condition.
- Dropping the question from the next consult is reasonable only while no such proof exists.

### V-14 §1.4 outcome rule and R1: OK
- §1.4 matches A50 L45–L54: FAIL for an assessed violation or an unlabelled licence; UNRESOLVED for insufficient support; never an unassessed PASS.
- FAIL takes precedence over CONFOUND NOT REALIZED, so a violation is never hidden.
- Superseding C3 is consistent with RD26 §4.
- 4B and 4U are both adverse and neither is a licence, so the anti-loophole intent holds, subject to V-1.

### V-16 L-2…L-8 vs RD26: OK
- **L-2 and L-1:** match RD26 §4: delete the PASS branch, split BOUNDARY/UNRESOLVED, make the screen binding with no cap.
- **L-3:** matches RD26 §4's renaming to plant realization.
- **L-4:** consistent with RD26 §1.2's precedence. Every gate is computed, and the higher-precedence label governs.
- **L-5:** see V-15.
- **L-6, L-7, L-8:** these settle three RD26 §3 dependencies: the G-iii noise reference, the root rule, and recursion vs SDE. ŝ\* refers to the discrete generator (L-8).
- **Still PENDING CNA, not supplied by CE50:**
  - the analytic s\*_LIM and the LIM offsets (RD26 §1.3 (A));
  - the s grids;
  - the Var floor.
  RD does not supply any of these values here.
- R3 (INCOMPLETE) matches RD26 §1.2 G-ii.
- R4's k supersedes RD26 §2.2's ⌈0.99·n_q⌉; the RD26 corr2 is pending (V-6). The RD26 §2.4 tie rule (≤) is unaffected.

## 5. Items for the Lead (no file edited)
1. V-1: choose the R3 option (a), (b) or (c), and state that it supersedes M L3422 for the FL denominators.
2. V-2: S_max bound (PENDING CNA); the null-input keying on s − θ; integer N_steps assertion (vii).
3. V-5: freeze the event wording "coverage < 0.97" for the 5.66e-6 / 1.81e-5 figures.
4. V-6: optionally require n_q ≥ 199 (PROPOSED). Otherwise accept T = sample maximum for n_q ≤ 198.
5. V-3, V-4: merge-time text fixes.

*REVIEW RECORD. Nothing was run or timed. X1–X5 and the claim ceiling unchanged. No consciousness claim.*
---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 80314aa7ed42e55feac20067c5853d1d565e095b1d7bf5b6269e59b7e94d8365
