# Track B v3.6 freeze prep: RD light pass of CNA's dose-0 / IGN-P1 x_ref file and CNA's E49-1/E49-3 addendum 1 (RD v1)

**Author:** Research Delegate (RD). **Written:** 2026-11-01, 11:37 AM ET (box `date`: 2026-11-01 11:37 EST). **STATUS: DESIGN/TEXT ONLY. DRAFT, NOT FROZEN.** Additive; no other file is modified. Nothing was run, simulated or timed. Computation: integer Philox4x64-10 and SHA-256 in pure Python (system `python3`, no numpy/scipy, script on stdin, nothing saved); exact rational arithmetic; and closed-form evaluation of standard distribution functions (normal via `math.erf`, chi-square survival in closed form, quantiles by deterministic bisection) in float64. Per A49 L47, "Arithmetic, static proofs and RNG known-answer checks do not themselves constitute instrument outcome data." X1–X5 and the claim ceiling unchanged. No consciousness claim.
**Lane:** RD checks (a) permutation, (b) rewcorr-eta words, (c) stop/exit closely; (d)–(h) light pass.
**Convention:** "X Ln" = review/trackB_scope_v3_6_CNA_dose0_and_ignp1_xref_v1.md. "AD Ln" = review/trackB_scope_v3_6_CNA_E49_1_E49_3_v1_addendum1.md. "RDL Ln" = RD's previous light pass (a44ff0d6…). "RD2 Ln" = review/trackB_ign_cost_v1_lightpass_items2to4_RD.md. "CNA2", "CNA3", "S2.1", "M", "MP", "LC" as in X L4. Verdicts: CONFORMS / CONFORMS WITH EDITS / DOES NOT CONFORM.
**Footer convention (this file):** the footer is the SHA-256 of every byte above the line beginning `sha256 of all content above this line:`, including the `---` line and its newline; the footer line itself is excluded.

## 0. Hashes (recomputed)
- X: whole-file `647a72d249b96729764c2d19f0ce938973ee38afea0c5f5cdb9a981f4c58a122` (expected 647a72d2…) **MATCH**; footer `550617f12839a198cb6ad09728aff92f9cb93aa6f9fe06f9ae6be8f65ce4f627` (expected 550617f1…) reproduced under the project convention **MATCH**.
- AD: whole-file `55030ebd7bb71e14b33c51606af704d16c0f81d955aa076e0b0a84b8d82801fb` (expected 55030ebd…) **MATCH**; footer `8223da2e5b055b69c42934d3ab314d1ad2614ab9381c62bf946942977a518f9c` (expected 8223da2e…) **MATCH**.
- Inputs cited by X/AD: RD2 d5ee9a1b… ✓; CNA2 17832b01… ✓; CNA3 5dec96f5… ✓; M ab80afa5… ✓; S2.1 merged 8ea6abc5… (no prefix stated in X); RDL a44ff0d6… ✓ (AD L4).
- **Header timestamps (minor error).** AD L3 says "Written: … about 11:40 AM ET", but the file's mtime is 11:32:52 ET. X L3 says "about 11:35 AM ET", mtime 11:31:48 ET. Both header times are later than the files were written; they should be corrected in any reissue.

## Verdicts
| # | Item | Verdict |
|---|---|---|
| a | Permutation (mod form), KAT, registry, bias bound | CONFORMS |
| b | rewcorr-eta word allocation | CONFORMS |
| c | Stop / exit / truncation | CONFORMS |
| d | Dose 0 | CONFORMS |
| e | NC2r / LIM | CONFORMS WITH EDITS |
| f | IGN-P1 x_ref, half-normal, chi, M L1127/L1129 edits | CONFORMS WITH EDITS |
| g | Δt, t_r grid, steps, cost fraction, noise placement | CONFORMS WITH EDITS (and RD's own 2/8 corrected) |
| h | #50 questions | CONFORMS WITH EDITS |

## (a) Permutation: CONFORMS
**Against the Lead's ruling.** AD L7–L15: for k = 507 down to 1, one block at counter (508 − k, 0, 0, 0), x = w0 (full 64-bit word), idx = x mod (k + 1) as an unsigned 64-bit operation, swap a[k], a[idx]; w1–w3 discarded; exactly 507 draws; no rejection, no retry counter; float form banned. Matches the ruling (j = x mod (k+1), one 64-bit word per swap, no rejection, float banned).
**Counters and key.** Recomputed: counters c0 = 1…507, each used exactly once (507 distinct), c1 = c2 = c3 = 0. Registry entry (AD L31–L32): suffix = bin; c0 = 508 − k ∈ {1…507}; s = 0; c2 = c3 = 0; w0 only; any other counter is a construction failure. Closes E-RD-4. **No counter reuse with any other role:** the key is SHA-256 of the v2 encoding with role tag `ign-partition` (CNA §4.2), so its stream is disjoint from every other role's by key (role tags differ and the encoding is injective, RDL §3); within the key each counter is used once. Partition field "none" and suffix bin make it per (replicate set, generator, row, dose, n_grid, replicate, seed, bin).
**KAT, independently reproduced (RD's own pure-Python Philox; the zero-vector self-check 16554d9eca36314c db20fe9d672d0fdc d7e772cee186176b 7e68b68aec7ba23b = KV L41).**
- Key K = e5b870ec7ff01d19169f9234ebc361a3 ✓ (AD L21).
- First draws (507, 49), (506, 346), (505, 464), (504, 103), (503, 212); last (1, 0) ✓ (AD L23).
- a[0:8] = 79, 468, 482, 332, 173, 222, 63, 342 ✓ (AD L24).
- Counts 254/127/127 ✓. Selection slots begin 3, 6, 9, 18, 20, 31, 38, 39 ✓; final slots begin 1, 4, 8, 12, 17, 22, 24, 25 ✓ (AD L26). (Fitting slots begin 0, 2, 5, 7, 10, 11, 13, 14; not stated by CNA.)
- SHA-256 of the comma-joined permutation = fa85f5518477d78bf72e2048786a42aa8401807a87fe4782cb52b8d936091379 ✓ (AD L27).
**Slot → partition mapping.** After the shuffle, the slot ordinal stored at **position** p is assigned by position: p = 0–253 → fitting, 254–380 → selection, 381–507 → final (AD L15). So slot j is in partition P iff j ∈ {a[p] : p in P's position range}; the "slots begin" lists above are the sorted values a[254:381] and a[381:508]. Counts are exact for any key. Suggest one sentence making "position p, value a[p] = slot ordinal j" explicit in the consolidated text, since "positions" and "slots" are both 0…507.
**Bias bound.** For m = k + 1 and x uniform on [0, 2^64), each residue has probability ⌊2^64/m⌋/2^64 or (⌊2^64/m⌋ + 1)/2^64 (AD L17) ✓. 508/2^64 = 2.7538735 × 10⁻¹⁷ → **2.7539 × 10⁻¹⁷ ✓**. It is a valid bound on the relative deviation |m·P(idx = i) − 1|. Exact values at m = 508 (2^64 mod 508 = 256): max |m·P − 1| = 256/2^64 = 1.3878 × 10⁻¹⁷ (the bound is conservative by 2×), and the absolute deviation max |P − 1/m| = 2.73 × 10⁻²⁰. The bound should be labelled "relative" in the frozen text, since (k+1)/2^64 read as an absolute probability error would overstate it ~500×. Not an error; a wording precision.

## (b) rewcorr-eta word allocation: CONFORMS
AD L54: per (t, s = k) block, w0 → u1 = ((w0 >> 11) + 1)·2⁻⁵³, w1 → u2 = (w1 >> 11)·2⁻⁵³, Box–Muller cosine only, one η_k; w2, w3 discarded; no cached sine (A49 L116). Closes E-RD-3.
- **No overlap.** Each η_k uses its own block (t, k, 0, 0), k = 1…d_ws − 1 (s = 0 unused for eta, CNA L148), so no two variables share a block or a word; discarded words are never reused. rewcorr-eps (s = 0) and action (s = 0) have different role tags, hence different keys, so equal counters across roles cannot overlap. Consistent with the R7 value RD recomputed (RDL L74). s-range PENDING with d_ws (P4).

## (c) Stop / exit / truncation: CONFORMS
- Neither file adds a stop, truncation, horizon-end, cap or stop-log quantity to any key, counter, policy input or statistic. The permutation reads only schedule fields and k. The X file's "settling" t_s and the settling-exclusion tolerance (X §B) are trial-eligibility rules on null-input runs, not stop quantities, and are chosen "without the observable w" (M L1129).
- The B/B_I "in-world termination" clause is unchanged (RDL §8). M L280's prohibition still governs.

## (d) Dose 0: CONFORMS
- **Quotes verified.** CNA2 L242: "Each specificity row has at least two **required doses** (PROPOSED DEFAULT, …), plus a dose-0 sanity level that is REPORTED only. All required doses are listed in §2.6. Only required doses enter the label." X L7 elides the parenthesis with "…" ✓. CNA2 L328: "about 2–3 required doses each plus dose 0, each at R prespecified replicates" ✓. M L1951: "> for each seed-structured Stage-0 generator g and required dose k:      # every labelled row: positives, negatives, confound rows" (X quotes "each … generator g and required dose k") ✓. M L375: "R_rep = 200 fresh replicates per generator and dose" ✓.
- **Five rows** (X L9–L20): NC1 (CNA2 L185 "Confound, specificity") ✓, NC2 (L186) ✓, BOTTLENECK-ONLY (L188 "specificity for joint IGN∧BCAST") ✓, RAND-INIT (L189 "specificity for C-LEARN-on-IGN") ✓, Architecture-imposed (L134 "Confound, specificity") ✓; P1/N1, NC2r ("**Mechanism-present**", L187) and LIM (L190) excluded ✓. d0 = 5 agrees with RD2 L100's bound {0…5}.
- **Never calibration** (required doses only, M L1951) ✓; **confirmation only** at R_rep = 200 and frozen n_seed: 200 × 4,572 × n_seed = **914,400·n_seed\*** per cell ✓ (exact; = RD2 L100). REPORTED only, never changes n_seed, never blocks or passes a row ✓.
- **RAND-INIT dose 0** (g_0 → 0 or drop, d0 = 5 or 4): Lead question (X D1) ✓.

## (e) NC2r / LIM: CONFORMS WITH EDITS
- **Quotes.** M L1536: "The target is the one-sided 95% Clopper–Pearson lower bound of the MET rate ≥ 0.90, for C-NEC-DEP and for C-CAUSE at each required ρ" ✓ (and that row is called "a required mechanism-present positive check"). MP L79: "the transition s* lies outside the probed grid;" ✓. MP L199 "Correct UNAVAILABLE on LIM | ≥ 0.90" ✓; M L345 CP one-sided 95% ✓; CNA2 L308 "Construction check only (out of range by design)" ✓. grep confirms neither "NC2r" nor "IGN-LIM" occurs in M ✓.
- **Reasoning sound.** NC2r: a required MET-rate gate is n_seed-dependent, so required ⇒ IN the selection set (M L2785 lists "positives"; M L1536 treats the MIXED-CODE mechanism-present check as a required positive, which is the precedent that cuts toward IN if the Lead makes NC2r required). REPORTED ⇒ OUT. LIM: OUT only if the frozen MP L79 decision is n_seed-independent; the s* fit is ABSENT, so the Lead must fix it first (X D3) ✓.
- **Edit X-1 (citation).** X L36 and X L56 cite **CNA2 L259** for "P rows and mechanism-present (reclassified) rows: e_exp = 1.0 by construction". That text is at **CNA2 L258**. CNA2 L259 reads "- No row may be declared "expected UNAVAILABLE" after the fact." The same wrong citation is inside the proposed M L1127 replacement wording (X L63), so it must be fixed **before** that wording is merged.

## (f) IGN-P1 x_ref: CONFORMS WITH EDITS
**Texts verified.** S2.1 L240: "Each trial starts from a **reset to the low attractor x_lo**" ✓. S2.1 L242: "In IGN-P1, x_ref = x_lo, so plant and instrument share one definition. [erratum 1 E3]" ✓. M L314: "x_ref is the declared controlled initial state (x_lo in IGN-P1; …)" ✓. M L1127 = CNA3 L437 ("t_s = 5τ in plants (residual e^−5 < 1%)") ✓; M L1128 = CNA3 L438 ("t_r = 3τ in plants") ✓; M L1129 = CNA3 L439 ("2 × the median absolute deviation of ‖x_ref − median x_ref‖ in null-input runs on the fitting partition, with no probe input") ✓. Text A and Text B conflict as X describes.
**Half-normal arithmetic (1-D, d = |Z|σ), reproduced.**
- median |Z| = Φ⁻¹(0.75) = 0.674490.
- **Reading I** = "2 × (median of ‖x_ref − median x_ref‖)", i.e. 2 × the ordinary MAD of the scalar x_ref: tolerance 1.3490σ, P(exclude) = 2(1 − Φ(1.3490)) = **0.1773 (17.7%)** ✓.
- **Reading II** = "2 × MAD of the values d = ‖x_ref − median x_ref‖", i.e. 2 × median |d − median d|: MAD(d) = 0.399092σ, tolerance 0.7982σ, P(exclude) = **0.4248 (42.5%)** ✓.
- Both are scale-free (independent of σ, g, τ) ✓. This holds also if the 5τ settled state is not yet stationary (it is still Gaussian to first order), so Reason 1 does not depend on stationarity. Per-trial eligibility 0.823 / 0.575 < 0.90, so the M L1130 coverage floor fails by construction ✓.
**Contradiction with CNA2 "e_exp = 1.0 by construction"** is real; the quote is at CNA2 L258 (Edit X-1).
**Proposed M L1127/L1129 edits (X L63–L64).** Consistent with S2.1 L240/L242 and M L314: scalar plants have t_s = 0, x_ref = x_lo, no settling exclusion; the M L1129 tolerance becomes "Network instruments only." RD has conceded this in the room and agrees. Fix the CNA2 L259 → L258 citation inside the replacement text. M L314 unchanged ✓.
**Network dimension dependence (chi distribution, ‖X‖ = σ·χ_d), reproduced.** X L70–L75 use **Reading I** (tolerance = 2 × median of χ_d):
| d | median χ_d | Reading I P(exclude) | Reading II P(exclude) |
|---|---|---|---|
| 1 | 0.67449 | 0.1773 | 0.4248 |
| 2 | 1.17741 | **0.0625** (exact: P(χ²₂ > 8 ln 2) = 2⁻⁴) | 0.6688 |
| 3 | 1.53817 | 0.0237 | 0.8381 |
| 4 | 1.83213 | 0.0094 | 0.9294 |
| 8 | 2.71000 | 0.0003 | 0.9989 |
- CNA's figures (0.1773, 0.0625, 0.0237, 0.0094, 0.0003) match Reading I ✓.
- **Edit X-2 (addition).** Under Reading II the dependence runs the **other way** and is much worse: exclusion rises with d toward 1 (0.67 at d = 2, 0.93 at d = 4), so a high-dimensional workspace would fail coverage. X L76 ("Anisotropy behaves like a lower d. A low-dimensional workspace could fail …") is Reading-I-specific. Either way the rule is unusable unpinned; CNA's quantile proposal (0.99 quantile of ‖x_ref − median x_ref‖ on fitting-partition null runs, X L77) removes the dimension dependence under both readings. That strengthens D5; Lead/#50.

## (g) Steps and cost: CONFORMS WITH EDITS
- **Δt.** ABSENT in S2.1, M, MP, CNA3 ✓ (RD2 L128 agrees). Rule Δt ≤ τ/20 (≤ 5% decay per step), PROPOSED τ/100 ✓. **Edit X-3:** the rationale "the linearized drift rate is at most 1/τ" (X L82) holds near a stable point, where the rate is (1 − g·sech²(g·x + s))/τ ∈ (0, 1/τ]. In the unstable region crossed during ignition, the linearized growth rate is (g·sech² − 1)/τ ≤ (g − 1)/τ, which exceeds 1/τ if g > 2 (IGN-P1's g is PENDING CNA, RD2 L110). State the bound as Δt ≤ τ/(20·max(1, g − 1)), or confirm g ≤ 2.
- **t_r grid** {2τ, 3τ, 5τ} plants, {3, 5, 8} steps networks: PROPOSED; contains M L1128's 3τ and 5 steps ✓; every value is an integer multiple of τ/100 and τ/20 ✓. M L377 freezes "the IGN t_r grid" without values ✓ (quote verified). All candidates read from one trajectory (M L376) ✓.
- **Steps (exact):** Text A plants: 5τ/(τ/100) = **500** ✓; 5τ/(τ/20) = 100 ✓; 3τ → 300 / 60 ✓. Text B: (5τ + 5τ) → 1000 / 200 ✓; (5τ + 3τ) = 8τ → 800 / 160 ✓ (= RD2 L56, LC L86). Networks 20 + 8 = 28, or 25 at t_r = 5 ✓.
- **Cost fraction: RD's room figure corrected.** Under Text A a plant trial runs t_r,max, so the fraction of LC's 8τ basis is t_r,max/8τ. At the proposed grid (max 5τ) it is **5/8**. A grid whose maximum is 3τ gives **3/8**. A 2/8 fraction would need t_r,max = 2τ, i.e. a grid that excludes M L1128's t_r = 3τ; since the grid must contain 3τ, **3/8 is the floor. CNA's 3/8–5/8 (X L68) is correct; RD's 2/8–5/8 was wrong** (RD took the lower end from t_r,min, but cost is set by t_r,max). RD withdraws 2/8.
- **Noise placement, quoted.** MP L84: "**IGN-P1:** a bistable unit, τ·dx/dt = −x + tanh(g·x + s + ξ) with g > 1 and ξ white noise." M L1126: "| IGN plants | Process noise ξ | N(0, (0.05·‖x_hi − x_lo‖)²) per unit time | Keeps the bimodal modes separated by about 20 noise SD at readout |". MP puts ξ inside tanh; M states it as process noise with a variance per unit time. X's PROPOSED additive Wiener increment with variance (0.05·‖x_hi − x_lo‖)²·Δt per step (X L86) follows M L1126. **Edit X-4:** say whether the increment is added to τ·dx (so x gets it divided by τ) or to dx directly; the two differ by a factor τ in noise SD, and the Euler–Maruyama step is not determined until this is pinned. PENDING (X D6).

## (h) #50 questions: CONFORMS WITH EDITS
- **Q1 (AD L63)** is byte-identical to RD's draft (RDL L47) ✓. It covers A49 L43 (rows 1 and 3, real_i via E5 only).
- **Q2 (AD L64)** covers RD's realization point for the new row 4b: BOUNDARY/UNRESOLVED excluded from the FL denominator and from the count of 36, and credited toward realization (≥ 188/200) only through the label-independent E5 plant checks, never as correct withholds. That matches the Lead's ruling. Truth table with row 4b (AD L36–L41): rows 4 (NOT MET), 4b (BOUNDARY/UNRESOLVED), 5 (MET) now exhaust the E-ATTR label set of M L1884 ("E-ATTR UNRESOLVED, BOUNDARY or NOT MET"), so exclusivity and exhaustiveness hold ✓.
- **Together Q1 and Q2 cover both RD questions** (A49 L43, and no realization credit for withholding in any row). Q3 (A44 L108 computed results) carried ✓.
- **Edit AD-1 (wording error).** AD L45 and Q2 say hedging to BOUNDARY "cannot lower the false-licence rate" / "cannot improve … the false-licence rate". That is not true in general: if a replicate that would have been MET (a false licence) is labelled BOUNDARY instead, the numerator falls and the rate falls (e.g. 5/100 → 0/95). What is true: (i) relative to counting BOUNDARY as a non-licence, excluding it can only **raise or keep** the rate (x/n ≥ x/(n + b)); (ii) it shrinks the denominator, making ≥ 36 harder; (iii) an instrument that hedges at nulls also loses power at positives (MET-rate CP lower bound ≥ 0.90, M L1965), which is the real guard. Replace the sentence in AD L45 and in Q2 before the packet goes.
- **Optional Q4.** X D5 ("Reading I vs II", network tolerance) is marked "possibly #50" but no question is drafted. If the Lead keeps the 2×MAD rule, add one; if the quantile rule is adopted, it is a prospective gate change and still needs Astra's review under A-2026-10-24.

## Errors and edits (summary)
1. **X-1** CNA2 L259 → **CNA2 L258** (X L36, L56, and inside the proposed M L1127 text at X L63).
2. **X-2** Reading II dimension dependence runs the opposite way (rises to 0.93 at d = 4); X L76 is Reading-I-specific.
3. **X-3** Δt rationale: growth rate can reach (g − 1)/τ in the ignition region; bound needs g ≤ 2 or Δt ≤ τ/(20·max(1, g − 1)).
4. **X-4** Pin whether the Wiener increment is applied to τ·dx or dx.
5. **AD-1** "Hedging cannot lower the false-licence rate" (AD L45, Q2) is false as stated; reword.
6. **Header times** AD L3 (11:40) and X L3 (11:35) are later than the files' mtimes (11:32:52, 11:31:48 ET).
7. **RD self-correction** The plant cost fraction is 3/8–5/8 (CNA correct), not RD's 2/8–5/8.
8. **Wording precision (no error)** label the 2.7539e-17 bias bound as relative (|m·P − 1|); exact max is 1.3878e-17, absolute 2.73e-20.
No DOES NOT CONFORM item. No hash mismatch. The new permutation KAT reproduces exactly.

*DRAFT. Design/text only. No freeze or execution is authorized (A49 L147). X1–X5 and the claim ceiling unchanged. No consciousness claim.*
---
sha256 of all content above this line: f7d751d23e39e6ce949e0ff18fef06a41e30ac2606590d85fbebfa93cfd268c6
