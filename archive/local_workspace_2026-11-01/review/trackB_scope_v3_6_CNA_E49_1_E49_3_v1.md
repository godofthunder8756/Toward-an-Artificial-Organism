# Track B v3.6 freeze prep: CNA response to Astra #49, E49-1 (GA-1 replicate truth table) and E49-3 (RNG address, counter, KATs, kernel carry), with E49-2 items addressed to CNA and E49-x (early-stop equivalence) (CNA v1)

**Author:** CNA. **Written:** 2026-11-01, 11:18 AM ET. **STATUS: PLANNING/AUDIT RECORD. DRAFT, NOT FROZEN.** Additive; no existing file is modified, including the amendment record. Nothing here authorizes execution: no training, simulation, Monte Carlo, Stage 0, calibration, pilot, timing or checkpoint inspection. The only computation was exact arithmetic: Clopper–Pearson and binomial tails (scipy 1.18.1), exact Poisson-binomial recursions on a deterministic grid of probability vectors (no random numbers), SHA-256, and integer Philox4x64-10 evaluation in pure Python, cross-checked with numpy 2.5.4. Scripts: /workspace/scratch/cna_e49/{e49.py, e49_v2.py, hoeff.py}. Nothing was timed. X1–X5 unchanged. The claim ceiling (#41 L304) is unchanged. "no additional stop-associated reward, penalty or terminal return" (#42 L223) applies. No consciousness claim.
**Convention:** "A49 Ln" = /workspace/astra_consult49_response.txt (cat -n). "CE Ln" = CNA E48 response (citations as corrected by erratum 1). "EK" = CNA ε-key file. "M Lnnnn" = merged v3.6. "V2.3", "V2.5" = RD addenda. "LC" = Lead cost file.

## 0. Inputs (sha256 recomputed; every stated prefix matches)
| File | whole-file sha256 |
|---|---|
| /workspace/astra_consult49_response.txt | 6b66bbba1b800aa3dc8aacd024a827a82acb3346216cad8f19397cde66934468 |
| review/trackB_scope_v3_6_CNA_E48_response_v1.md | 90fcb1fb762a22db91cde5bd4fd68a683d28d6a78c8efe9ca21a13e1e103f1ce |
| review/trackB_scope_v3_6_CNA_E48_response_v1_erratum1.md | 65accc3c6d0c62918a9c9be940d1d213e6f2aff14ca9a0fc8fac13214c11bb74 |
| review/trackB_freezeprep_v2_3_addendum_RD.md | 48f75cfb37f56e8a076a18bfe671b6910fdca8da9bbf844b4795d5dea46a70d8 |
| review/trackB_freezeprep_v2_4_governance_addendum_RD.md | cf56c653dae28f9acee5be28d4f7a67568ce3aedfab933db308408f714e1cd9d |
| review/trackB_freezeprep_v2_5_E49_2_IGN_wording_RD.md | ae80cc122a284b16d96f4a02144c6a9a57a104fe1c5402551ca34cada5dede72 |
| review/trackB_ign_full_procedure_cost_v1_Lead.md | 7d4cbbad73d246425db425a6bf8231253d33c4cde07d4426f346650c16b9345d |
| review/trackB_freezeprep_v2_consolidated_RD.md | b41f0e1068fee9fec0dc2a6ece4879cebec510c0729f6eed2e45e3ca26bff55c |
| review/trackB_instrument_validation_scope_v3_6_merged_RD.md | ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b |
| review/trackB_scope_v3_6_CNA_eps_key_and_cpfloor_v1.md | 847c430d86aa28f78a3ab53e596fb03816b2a9a59f59fca57a765b10a4bcc02c |
| review/constitution_amendment_A-2026-10-24_record.md | 2f29a07a617464e1b0a30ad77ce7c67367f31208e749f6bcbff938fa8f7c2dd6 |
| review/trackB_measurement_plan_v1_RD.md | 1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef |
| /workspace/astra_serve49/c49_body.md (current; superseded_v1 body is dd1526be…) | 9aeaea1e05e0069254f821ec12c244c5f378931ab88080c158373b4505a9dab2 |
| /workspace/astra_consult44_response.txt | 49afbb5d1ca63f0db692f3123e85c7ccf1c2870dbd45b48d639d39c30bc22060 |
| /workspace/scratch/fp2/kat/kat_vectors (Random123) | aab5ebabf40003f63d6d87b24cbd2c8a02652e00cf8bad64226fd50586929183 |

## 1. E49-1: GA-1 replicate truth table (A49 L36–L43, L141)
**Definitions used, unchanged:**
- **Cells:** seed × block × target (M L2748).
- **D/ND:** decided by the frozen nondegeneracy rule (M L2749): usable iff ‖w_E‖ > 0, d_ws − r_N ≥ 1 and ρ_E ≥ 0.10. ‖w_E‖ = 0 means ρ_E is undefined, so the cell is D.
- **Route I / Route B:** replicate-level, over the replicate's ND cells (M L3364–L3368; canonical comparison `33.0 * U_A < 1.0`, v2.2 §4.6). Requires G1–G4.
- **Nine-seed minimum:** M L1972, "an administrative minimum only" (A49 L45 agrees).
- **Realization:** f_ok = Σ real_i·elig_i / R over all R = 200 prespecified replicates. The row is realized iff the one-sided 95% CP lower bound is ≥ 0.90, i.e. ≥ 188/200 (CP LB 0.90460; 187/200 gives 0.89864) (M L698; CE L49).
- **E5 checks 1–2** (M L1630): corr(E, r̄) ≥ ρ(1 − tol) and raw R²(state → E) ≥ ρ²(1 − tol). These are plant checks and do not depend on the attribution label.

**Evaluation:** rows are evaluated in order. Exactly one row applies to each replicate.

| # | Replicate state (exclusive, in precedence order) | real_i | elig_i | False-licence (FL) denominator / numerator | Error-rate treatment | Reported as |
|---|---|---|---|---|---|---|
| 0 | **Construction failure** anywhere in the replicate. This covers: a non-finite value (M L3421); K_other found empty (kernel (iii), §4.6); SD(z_R) = 0 (M L3407); a licence (MET) recorded in a replicate with no computed label. | 0 | 0 | not entered | none. It stays in R as a non-success (INCOMPLETE). A licence without a computed label also makes the row **FAIL** (CE L51). | INCOMPLETE + failure step |
| 1 | **All-D:** every cell is D, so no residual coordinate exists | E5 (1 iff checks 1–2 pass) | 1 by the explicit GA-1 carve-out (CE L46): D cells are not ineligible for this row | not entered | UNDEFINED. "Did not issue MET" is an output event (A49 L23). It is **not a correct withhold and not a negative**, so it adds nothing to any error rate. | count D; D fraction by dose |
| 2 | **N:** ≥ 1 ND cell, and Route I and Route B both fail (or G1–G4 fail) | **0** (CE L48; kept) | n/a | not entered | none; counted, never dropped | count N |
| 3 | **Q-insufficient:** a route holds, but the Q cells span < 9 seeds | E5 | E2 floor on the replicate's ND cells | not entered | UNDEFINED for the label. "Insufficient qualified support cannot certify the nondegenerate branch" (A49 L25). | "did not issue MET (insufficient Q seeds)" |
| 4 | **Q-labelled, NOT MET:** a route holds, Q cells span ≥ 9 seeds, label computed, no licence | E5 | as row 3 | denominator +1 | correct non-licence within the Q branch | count |
| 5 | **Q-labelled, MET:** as row 4, but the label is MET | E5 | as row 3 | denominator +1, **numerator +1** | false licence | count; ρ_E, U_A |

**Row-level outcome (applied to all 200 replicates per row and dose):**
- **(a) Realization.** CONFOUND NOT REALIZED if the CP lower bound of f_ok is < 0.90. Rows 0 and 2 always contribute 0.
- **(b) False licence.** The rate is computed over **all** row 4 + row 5 replicates among the prespecified 200, never the first or best 36 (A49 L34). Q status is fixed by D/ND, route and seed span, all computed before and independently of the label (A49 L34).
- **(c) Assessability.** The FL criterion (point ≤ 0.05 **and** one-sided 95% CP upper ≤ 0.08; M L1964) is **assessable only if denominator ≥ 36**. Below that it is "Q-branch OC NOT ASSESSED".
  - ≥ 36 is a necessary assessability condition only. It is **not an automatic pass** (A49 L32), and it **does not replace the realization criterion (a)** (A49 L43).
  - CP upper bound formula: U(x, n) = Beta⁻¹(0.95; x + 1, n − x), and U(0, n) = 1 − 0.05^(1/n). The floor example is U(0, 36) = 0.0798465 (U(0, 35) = 0.0820316), matching A49 L29–L30.
  - With nonzero counts, both criteria bind. The smallest denominator allowing x false licences is: x = 1 → 58; x = 2 → 77; x = 3 → 95; x = 4 → 112; x = 5 → 129. The maximum allowed x is 0 at n = 36 or 50, 3 at n = 100, and 9 at n = 200 (script e49.py).
- **(d) Status.** **FAIL** if (b) is assessed and fails, or row 0 records a licence. **PASS** if (a) holds and (b) is met or NOT ASSESSED. When D dominates or (b) is NOT ASSESSED, PASS carries the wording "The row validates the degeneracy guard, not the specificity of a resolved attribution estimator" (CE L53).

**Answer to A49 L43.** A49 L43 reads "If, as the packet states, the first two are N and receive real_i = 0". Under the governing text, all-D and Q-insufficient replicates are **not N**. CE L48 defines N only as "ND cells exist and neither Route I nor Route B holds". The #49 packet's one-line summary (c49 A1) compressed this.
- Rows 1 and 3 contribute to realization **only through the label-independent plant checks** (E5 checks 1–2), never through "correct withholding". They are excluded from every error rate. So no double counting arises.
- Correct withholding earns nothing. If the Lead prefers Astra's reading (rows 1 and 3 → real_i = 0), that is a prospective gate change: Lead ruling plus Astra under A-2026-10-24, before any data.
  - Consequence: under CE §2.1's planning approximation (P(ρ_E ≥ 0.10) ≈ 0 at ρ = 0.9), the row would be CONFOUND NOT REALIZED at ρ = 0.9 almost surely, which reinstates the pre-GA-1 block.
  - CNA recommends the governing reading.

**Proposed wording edits (CNA-owned text; replacement text proposed for the consolidated freeze):**
- **PZ7 Role cell (CE L59 / V2.3 L77):** replace "PASS = correct withholding (degeneracy guard validated)" with "PASS = realization criterion met, no licence outside Q-labelled replicates, and, where assessed, the Q-branch false-licence criterion met (degeneracy guard exercised)". This keeps it consistent with the approved wording that UNDEFINED is not scored as a correct withhold.
- **Correction to CE L31 (A49 L18).** At dose ρ = 0 (the REPORTED sanity level), c_E = 0 and w_E = 0. The residual ratio is **undefined**, not 0, and the cell is D by M L2749. CE's "ρ_E = 0 exactly in the population, for every dose" holds for every dose with Cov(ζ̃, Ẽ) ≠ 0.
- **Amendment record L20** ("assessed at >= 36 Q replicates (0/36 gives Clopper-Pearson upper bound 0.0798)") is read with A49 L32 and L43 as in (c). The record is not edited.

**Astra's reading of A-2026-10-24, recorded verbatim (A49 L47); the amendment record is not edited:** "The governance amendment is appropriately limited. Interpret "before any data exists" to include calibration, pilots, feasibility outputs and diagnostic study outputs. Starting a new ledger does not reset that boundary. Arithmetic, static proofs and RNG known-answer checks do not themselves constitute instrument outcome data. "After Astra's review" should mean after addressing its required conditions, rather than merely obtaining a review. No additional approval of GA-1 is needed."

## 2. E49-2 items addressed to CNA (V2.5)
**(a) IGN partition assignment (Lead ruling: deterministic slots for IGN; D27 seed-hash split stays for every other row).** CNA assesses this as sound: it is exact, outcome-free and fixed before data, and it satisfies A49 L64–L69.
- Contiguous slot ranges are rejected, because the partition would alias schedule order (for example strength order within a bin).
- **Specification:**
  - Within each IGN cell (replicate set, generator, row, dose, n_grid, replicate, seed, required bin), the 508 scheduled slots carry ordinals j = 0…507, fixed at schedule-build time.
  - A keyed Fisher–Yates permutation under role `ign-partition` (§4.2; partition field "none"; suffix = bin) permutes (0…507). For k = 507 down to 1: u = (w0 >> 11)·2⁻⁵³ from counter (508 − k, 0, 0, 0); idx = ⌊(k + 1)·u⌋; swap a[k] and a[idx].
  - Positions 0–253 → **fitting**, 254–380 → **selection**, 381–507 → **final**. That is exactly 254/127/127.
- The permutation reads no outcome, is computed before any trial runs, and is written to the frozen schedule.
- The trial-level RNG for slot j uses partition = its assigned label and slot = j (§4.2).
- Example (placeholder zero seed; NOT the master seed): selection slots begin 2, 6, 7, 11, 13, 17, 23, 25; final slots begin 1, 5, 10, 15, 16, 21, 29, 30. Counts are 254/127/127 (e49_v2.py).

**(b) CE F-4 superseded: CONFIRMED against the raw text.**
- A49 L73 limits independence to "conditional on the frozen plant, fitted quantities and seed-level settings" and excludes jointly computed gates. A49 L75 says the pooled count is not binomial. So CE F-4's "i.i.d. Bernoulli given the seed … exactly binomial" is superseded by V2.5 §3 and §5. CNA adopts both.
- A49 L77 says (seed, bin, slot) "is sufficient only inside that already-separated namespace". The §4.2 address therefore carries the full namespace.

**(c)** Handled in §1 (c) above.

**(d) Hoeffding 1956, Ann. Math. Statist. 27(3):713–721, doi:10.1214/aoms/1177728178 (Crossref-confirmed).**
- **p. 718 is UNVERIFIED by CNA.** doi.org returned HTTP 500, and Project Euclid returned an Incapsula block. I did not bypass it or use a mirror.
- **As commonly stated (Theorem 4):** let S be a sum of N independent Bernoulli(p_i) variables with p̄ = mean p_i. If c ≥ Np̄ + 1, then P(S ≥ c) ≤ P(Bin(N, p̄) ≥ c). Equivalently, for b ≤ Np̄ − 1, P(S ≤ b) ≤ P(Bin(N, p̄) ≤ b). Between these thresholds the inequality can reverse.
- **Exact numerical spot-check** (no randomness; 64 deterministic linear-spread p-vectors, N = 5…40): 1,278 checks in the regime c ≥ Np̄ + 1 gave 0 violations. 2,881 out-of-regime cases had the Poisson-binomial tail above the binomial tail, which confirms that the regime matters.
- **RD's argument holds under this statement:**
  - Pooled floor: for p̄ ≤ 0.90, x_min ≥ 0.9N + 1 ≥ Np̄ + 1 gives P(S ≥ x_min) ≤ P(Bin(N, p̄) ≥ x_min) ≤ P(Bin(N, 0.9) ≥ x_min) ≤ 0.05, because the binomial upper tail is nondecreasing in p.
  - Quota: c = 99 ≤ 127·p̄ − 1 for p̄ ≥ 0.90.
- **Recomputed x_min(N)** (N = 127·n_seed; smallest x with P(Bin(N, 0.9) ≥ x) ≤ 0.05):

| n_seed | N | x_min | 0.9N + 1 | P(Bin(N, 0.9) ≥ x_min) |
|---|---|---|---|---|
| 9 | 1,143 | 1046 | 1029.7 | 0.046346 |
| 12 | 1,524 | 1392 | 1372.6 | 0.042505 |
| 16 | 2,032 | 1852 | 1829.8 | 0.044784 |
| 20 | 2,540 | 2312 | 2287.0 | 0.044211 |
| 24 | 3,048 | 2771 | 2744.2 | 0.048172 |
| 32 | 4,064 | 3690 | 3658.6 | 0.046383 |
| 48 | 6,096 | 5526 | 5487.4 | 0.046494 |
| 64 | 8,128 | 7360 | 7316.2 | 0.049833 |
| 67 | 8,509 | 7704 | 7659.1 | 0.049576 |

  All nine satisfy x_min ≥ 0.9N + 1. **Before freeze, the regime must be confirmed against p. 718 by someone with sanctioned access.**
- **Note:** A49 L75's link points to a third-party host (paperzz.com) labelled "Hoeffding, Wassily; 1955". The primary publication is 1956 (Sept issue).

**(e) Joint (bin-wide) eligibility gates: YES, specified.**
- MP L78–L81 (IGN UNAVAILABLE) lists three:
  - (i) "the transition s* lies outside the probed grid";
  - (ii) "fewer than n_trial trials fall per near-transition bin";
  - (iii) "Var(w) is below a floor (workspace collapse, §3)", which is Astra's "bin-wide variance test" (A49 L73).
- M L1130 adds the per-bin **coverage** floor (CP lower bound of the eligible fraction ≥ 0.90; otherwise UNRESOLVED), which is the pooled floor itself.
- **Definition (CNA PROPOSED):** each of (i)–(iii) is a separate **aggregate instrument outcome**, computed once per (seed) or (replicate) on the final partition as its frozen rule states. On failure, the label is IGN UNAVAILABLE (or UNRESOLVED for coverage), recorded with its own reason code.
  - It **never changes any trial's eligible/ineligible classification**, never enters the quota count (V2.5 3b(i)) or the pooled floor count (3b(ii)), and is never treated as 127 trial failures.
  - Its operating characteristic is reported over replicates.
  - The Var(w) floor value and the s* fit procedure are **ABSENT/PENDING** and must be frozen before calibration.
  - The MP D1 occupancy-entropy and write-rate gates (MP L236) are network-study gates and are out of Stage-0 scope.

## 3. E49-x: early-stop equivalence (LC §6 item 4)
**Rule as written.** v3.4 E44-3 (M L2784, replacing PZ5 §4.2's last step-2 line): "`pass(g,k,n) = TRUE iff every target below is met at n`. Record pass(g,k,n) for **every** n in GRID; do not stop at the first passing n." M L2785 continues: "n_seed = the smallest n in GRID at which pass(g, k, n) is TRUE for every required (g, k) … The full grid table pass(g, k, n), with every OC, is retained and reported; failed results are never replaced to impose monotonicity." It is amended by v3.5 §5.3 (M L3175): R_core only, and R_T3 is evaluated at the selected n only. The source is Astra #44 L100–L108: "Select the smallest n in GRID at which every required row and dose passes … Retain the full grid results; do not impose monotonicity by replacing failed results."

**Checking the Lead's three conditions against the text:**
- **(1) Smallest common passing point, from its own data: HOLDS.**
  - pass(g, k, n) uses only point n's replicates.
  - No monotonicity, smoothing, "all larger n" requirement or cross-point pooling appears.
  - Precision: the stop point is the first n at which **every** R_core (g, k) passes **simultaneously**. Every (g, k) must keep running at each n until then, including rows that passed at a smaller n. Stopping a row at its own first pass would recreate the withdrawn max-of-n* rule (#44 L100).
- **(2) Streams identical whether or not later points run: HOLDS IN EFFECT, BUT NEEDS A SENTENCE.**
  - R37 (M L2407) keys the spawn tree by (role, generator, dose, replicate, purpose), with **no grid value**. Counter-based keyed streams make point n's data independent of whether later points run.
  - But replicate r at different n reuses the same stream, which is an implicit nested-seed design.
  - §4.2 adds the field n_grid, so each point's streams are a function of (n, r) alone.
- **(3) The stop alters nothing already computed: HOLDS** with an append-only ledger.

**Verdict.** Under (1)–(3), early stop gives exactly the same selected n_seed, the same pass/fail at every computed point, and the same OCs at the selected n (and therefore the same 3a envelope and R_T3 evaluation). What is lost is the pass table above n_seed, which is diagnostic only.
- **However, the frozen text explicitly forbids early stop** (M L2784, "do not stop at the first passing n"), and that text was written to satisfy Astra #44 L108 ("Retain the full grid results").
- So early stop is **not available as written**. Adopting it would need a prospective replacement sentence: a Lead ruling plus Astra review under A-2026-10-24, before any calibration output (A49 L47).
- **Proposed sentence, if wanted:** "Calibration runs GRID in ascending order and stops after the first n at which every R_core (g, k) passes; pass(g, k, n) for every computed n is retained and reported; points above the selected n are not run and are reported as NOT RUN; nothing computed is altered."
- Astra should confirm that "retain the full grid results" means computed results.
- **Budgeting:** calibration cost is 200 × 4,572 × Σ_{n ∈ GRID, n ≤ n_seed} n per cell, which is not known in advance. The worst case (n_seed = 67, or BLOCKED) is still Σ = 292, so the prospective budget must still cover 267,004,800 per cell.

## 4. E49-3: counter subindex, RNG address, KATs, kernel carry
### 4.1 Counter (A49 L118)
- **Generator and counter:** Philox4x64-10. The counter block is the four 64-bit words (c0, c1, c2, c3) = **(t, s, 0, 0)**, with c2 = c3 = 0 reserved, and a nonzero reserved word is a construction failure.
  - **t (c0):** the absolute step: for episode roles, A16 step numbering 1…H_V of the **root** episode, inherited by every continuation (EK L35, L41: "Continuations inherit the root ID and never mint a new one"); for IGN trials, the trial step from 1.
  - **s (c1):** the draw ordinal within step t for that role.
- **Rules for s:**
  - **s = 0** when a role makes one block-draw per step: rewcorr-eps (w0, w1 → Box–Muller, one normal) and action (w0 → u_b, w1 → u_k).
  - With several draws per step, **s = the draw's fixed ordinal in the frozen spec's variable list for that role**: rewcorr-eta uses s = k for η_k, k = 1…d_ws − 1, and s = 0 is unused. IGN roles take ordinals from their frozen variable list (PENDING the IGN generator spec).
  - The range of s is declared per role at freeze. An s outside the declared range is a construction failure.
  - **Ban, verbatim (A49 L118):** "It must never become a branch ID, donor ID or call-order counter." Also banned (EK §2.3/§2.4): continuation-relative counters, draw-count-dependent indices, wall clock, process/thread/worker or completion order.
- **Words and caching:** unused words in a block are discarded and never carried over. No sine output or second normal is cached (A49 L116).

### 4.2 Address (canonical encoding v2; extends CE §5.1 and keeps its field order, with new fields inserted)
**Encoding:**
- Every field is a 4-byte big-endian length followed by its bytes. Integers are uint64 big-endian. The master seed is 16 bytes, big-endian.
- D = SHA-256(encoding); k0 = little-endian uint64 of D[0:8]; k1 = little-endian uint64 of D[8:16].
- The domain string becomes **"ACI-TrackB-RNG-v2"**, so no v1 tuple can collide. The CE L160–L167 test rows are superseded.

**Fields, in order:**
1. "ACI-TrackB-RNG-v2";
2. master seed;
3. **replicate set** (UTF-8: "dose-cal" | "size-cal" | "confirm"; M L372 D16, disjoint streams);
4. **generator/plant ID** (UTF-8, from the frozen generator registry; needed because row ID does not identify the IGN generator, LC §2);
5. row ID (UTF-8);
6. **dose index** (u64, 0-based in the row's frozen dose list);
7. **n_grid** (u64: the GRID value for size-cal; the frozen n_seed for confirm; 0 for dose-cal);
8. replicate index (u64, within the set);
9. **partition** (UTF-8: "fitting" | "selection" | "final" | "none"; "none" only for roles that determine partition membership, i.e. `ign-partition` and environment/episode-generation roles evaluated before the D27 hash);
10. seed index (u64);
11. role tag (UTF-8);
12. **role suffix:**
    - for "rewcorr-eps", "rewcorr-eta" and "action": root episode ID (u64);
    - for "ign-trial": bin (u64), slot j (u64, 0…507);
    - for "ign-partition": bin (u64).

**Partition values:** for IGN, partition = the §2(a) slot label. For every other row, partition = the D27 environment-seed-hash label (Lead ruling).

**Role registry and its relation to R37:**
- Every role must be declared in the frozen role registry with its suffix and s-range. An undeclared role may not draw.
- This single derivation implements R37's "one frozen derivation". R37's "purpose" maps to the role tag.
- S-INT keeps its own tag (EK L35).
- The length-prefixed encoding is injective over field sequences, and audits distinguish domain reuse from hash collision (CE L169).

### 4.3 Known-answer checks: integer (exact) separated from floating point (A49 L120)
**(i) Philox core, exact word equality.** All six philox4x64 lines of Random123 tests/kat_vectors (L38–L43: 7 and 10 rounds) match.
- This supersedes erratum 1's "UNVERIFIED" note for CE L152–L154, which match file L41–L43.
- Re-check against the same file (aab5ebab…) at freeze.

**(ii) Key derivation and address, exact.** Placeholder master seed = 128 zero bits. **TEST VECTORS ONLY: this is NOT the master seed.** numpy Philox (counter = (t − 1, s, 0, 0)) agrees on every row.
- R1 canonical encoding (hex): 000000114143492d547261636b422d524e472d7632000000100000000000000000000000000000000000000007636f6e6669726d0000000d504c414e542d524557434f52520000000a5245572d434f52522d450000000800000000000000000000000800000000000000000000000800000000000000000000000566696e616c0000000800000000000000000000000b726577636f72722d657073000000080000000000000000
- SHA-256: 1bcc32c856b97452bfa7fc93fe57b28f032709c877b77fa9c803947b26eb62aa
- "PLANT-REWCORR" and "IGN-P1" are placeholder generator IDs.

| # | (set, generator, row, dose, n_grid, rep, partition, seed), role, suffix, (t, s) | K (D[0:16]) | w0 w1 w2 w3 |
|---|---|---|---|
| R1 | (confirm, PLANT-REWCORR, REW-CORR-E, 0, 0, 0, final, 0), rewcorr-eps, root 0, (1,0) | 1bcc32c856b97452bfa7fc93fe57b28f | 2d9ff92b420480da 7304dfec9b46f921 b19f8ae5c947f0e2 3f88e7943d6a7b97 |
| R2 | as R1, (2,0) | same | d7395e7e40c01d4c 80bb429efa06a877 6efd0674b7123029 fb4d33bfaebb4e70 |
| R3 | as R1, root 1 | 2884eb017739de9de0205752ac9950a2 | 13b1582d8d374a1a 7691f131850bf6db 0e35cf80b8c05f80 f19f1ec52b6a915a |
| R4 | as R1, dose 1 | ba45a900a0c8e66bff70cd5c1c1f123f | a2c9b5b4497b26ec 94364aab26dd92c9 9f507417b71b7bce 0ff69c92741c2267 |
| R5 | as R1, partition fitting | 1eb20c1947b7f492ad8dd5e1576372e9 | d57119b49216d576 2411ab4ee39c6f8e 0973b71be600c02a 52ea00ee6ccaceea |
| R6 | (size-cal, …, n_grid 9, …), rewcorr-eps, root 0, (1,0) | d2857941aebdd3f44dbf5f981ab56f2d | 533a82a93c848d1d 406c65827c413265 4a7166fd4d592374 579357321cdb8702 |
| R7 | as R1, rewcorr-eta, (1,1) | af968838897ed6e12941d983b61e3d09 | c1ed0d8250fa56ca 7c0706e492cde5a9 a58cbe19e33e6a36 978b66124079cbf8 |
| R8 | as R7, (1,2) | same | 3dc20c312dd9cf47 4bf53ed71881ba60 ac480b144c4c328e 99bc887f9e1ef705 |
| R9 | as R1, action, (1,0) | 3bc36775c9f5c512063231d0a2e4f07d | 41bd1a017bfe152c 6e9047ff0bb58663 c5c23d6e91fa027d f63f625a263adb00 |
| R10 | (confirm, IGN-P1, IGN-P1, 0, 0, 0, final, 0), ign-trial, bin 0, slot 3, (1,0) | c0c912ca9d3c6f618ed2263169a72934 | 704cbc4f65495b55 8757b2fcdbdb05fc c347a9ccec5d1bdd e0a00ef515f161f0 |
| R11 | (confirm, IGN-P1, IGN-P1, 0, 0, 0, none, 0), ign-partition, bin 0 | e5b870ec7ff01d19169f9234ebc361a3 | permutation (§2(a)); sha256 of the comma-joined permutation, first 16 hex = 268a77b62f87367b |

**(iii) Floating-point transform, separate check.** These values are derived, from CPython float64 with the box's libm.
- **Tolerance: PENDING (P6, pinned maths library still open).** Proposed: bit-exact under the pinned libm; otherwise |Δn| ≤ 4 ulp of n, with the integer words still exact.
- Values:
  - R1: u1 0.178222249089247, u2 0.44929313208129062, n −1.7638012618999939.
  - R2: n −0.58896812511241703.
  - R7: n −0.74171324587159282.
  - R9: u_b 0.25679171119917776, u_k 0.43188905693724244. Uniforms are exact dyadic rationals, so they are bit-exact.
- The maximum |n| is 8.571674 (CE §5.2).

**Master seed and beacon.** The master-seed rule is unchanged (A49 L124–L127). The beacon is **optional and not a freeze blocker** (A49 L131).

### 4.4 Carried for the consolidated freeze text: kernel and INTERACT definitions (A49 L89–L101), verbatim
Source: review/trackB_freezeprep_v2_3_addendum_RD.md (48f75cfb…). Identical to CE §4.1 L111 and §4.2 L115 (90fcb1fb…).

**[FREEZE TEXT] Kernels (V2.3 L84):**
> "**Action law (Stage-0 attribution plants).** Each step t draws u_b, u_k ∈ [0, 1) from role 'action' (§5.3 mapping, words w0, w1). The **kernel target** T_k(t) is the nearest available target at the start of step t (food item for -E food rows; repair station for -I rows), by shortest-path length, ties to the lowest target index. It is distinct from the endpoint target T of B/B_I. (i) **No available target:** the action is A7[⌊6·u_k⌋], independent of g. (ii) Otherwise, approach iff u_b < p_t = σ(a − β·g_t), β = 1.2. Approach = INTERACT if on T_k(t), else the lowest-index A7 move that strictly decreases the distance to T_k(t). Non-approach = K_other[⌊|K_other|·u_k⌋], where K_other is the set of A7 actions that do not strictly decrease the distance (excluding INTERACT when on T_k(t)), ordered by A7 index. (iii) K_other cannot be empty in any reachable state (STAY never decreases the distance; off target INTERACT does nothing). If found empty, that is a construction failure (M L3421) and no fallback is used. No rule reads g other than through p_t, nor the block (except through g), any probe, or any stop, truncation, horizon-end or schedule quantity (M L280). Every frozen SD divisor is > 0 at freeze." Then TV(π_g, π_g′) = |p(g) − p(g′)| ≤ 0.3|g − g′| in every reachable state (#48 L142).

**[FREEZE TEXT] Endpoint B/B_I, including the INTERACT predicate (V2.3 L87):**
> "B (B_I) = (1/10)·Σ_(u = t_d+1..t_d+10) b_u. T is the endpoint target fixed at t_d (nearest available food item for E rows, repair station for I rows, by shortest-path length on the static wall grid, ties to the lowest index; M L2079–L2080). d_u is the shortest-path (= Manhattan, A1) distance from the agent to T's cell after A16 step 2 (movement) of step u; d_(t_d) is the distance at the end of t_d. b_u = 1 iff the episode has not terminated in-world before u, T is available at the start of step u (state at the end of step u − 1), and either (a) d_u < d_(u−1), or (b) the agent is on T at the start of step u and its action at u is INTERACT. Otherwise b_u = 0, including every step after in-world termination and every step at whose start T is unavailable. Unavailable steps are scored 0, never excluded. Each b_u ∈ {0, 1} depends on world state and actions only. A trial with no available or reachable target at t_d is ineligible (counted; M L2858). No evaluation episode carries a scheduled stop (R4, M L2362)."

**[FREEZE TEXT] Indices (CE L97, adopted V2.3 item 14):** A7 index N = 0, S = 1, E = 2, W = 3, STAY = 4, INTERACT = 5. Food item index: slot 0–3 in A17 placement order, kept through respawn. Station index: template definition order (A3).

**Coverage of A49 L95–L99:**
- Target fixed at the window start: "fixed at t_d".
- Availability and movement timing: "start of step u", and "after A16 step 2".
- INTERACT on an unavailable target: 0. Off-target INTERACT: not counted (requires "on T"). "Ineffective" INTERACT: (b) counts INTERACT whenever the agent is on an available T at the start of u, whatever the outcome at A16 step 3 (CNA reading, no text change).
- No target: kernel (i), and the endpoint trial is ineligible.
- Target loss: scored 0 from the step whose start finds T unavailable.
- Termination: 0 thereafter.
- Empty kernel: construction failure.

**Do not carry v2 consolidated L37** (the older kernel text with the K_approach fallback, superseded per V2.3 D50). v2 L154 (A18 INTERACT clause) is subsumed by V2.3 L87.

## 5. Discrepancies found
1. **A49 L43 premise.** All-D and Q-insufficient replicates are not N under CE L48 (§1). The packet summary compressed this.
2. **CE L31.** At ρ = 0, ρ_E is undefined, not 0 (A49 L18). Corrected in §1.
3. **CE F-4.** "i.i.d. … exactly binomial" and the (seed, bin, slot) key are superseded (A49 L73–L77). Confirmed.
4. **M L2784 explicitly forbids early stop.** LC §6 item 4 says the loop "does not say whether larger n must still be run", but M L2784 does say it (§3).
5. **R37 (M L2407)** has no grid-value or partition field, so it is superseded by the §4.2 address. M L2390 (R25 workload, no ×|GRID|) conflicts with PZ5 §4.2, as LC notes.
6. **Hoeffding:** A49 L75 links a third-party copy dated 1955; the primary is 1956. The p. 718 check is UNVERIFIED (blocked).
7. **Erratum 1's KAT "UNVERIFIED"** is now resolved against kat_vectors (§4.3).
8. **MP L78–L81 joint gates** were not listed in CE F-1 to F-10 (V2.5 3b(iii) PENDING). Answered in §2(e).

*DRAFT. Design/audit only. No freeze or execution is authorized (A49 L147). X1–X5 and the claim ceiling unchanged. No host coupling. No consciousness claim.*
---
sha256 of all content above this line: fbb1e97536eb6230bbc86d27e1be7b4b351560349e44019c8da14ed0d50f0b66
