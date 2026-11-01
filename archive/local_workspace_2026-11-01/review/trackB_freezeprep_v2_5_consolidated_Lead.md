# Track B freeze preparation v2.5: CONSOLIDATED (E49-1..E49-3 closure, Lead rulings R1–R9, IGN recost) (Lead)

**STATUS: DESIGN ONLY. DRAFT, NOT FROZEN. NOTHING RUNS.** A new, additive file. It edits no existing file (v2, v2.1, v2.2, v2.3, v2.4, the amendment record, merged v3.6, every CNA/RD file and the Lead cost file stay byte-identical). No plant, instrument, harness or experiment was run or timed. No training, simulation, Monte Carlo, Stage 0, calibration, pilot, benchmark or checkpoint inspection. The only computation was exact integer/rational arithmetic (system `python3`, `fractions`), SHA-256, and an independent pure-Python integer Philox4x64 known-answer re-check (scripts `/workspace/scratch/lead_v25/kat_recheck.py`, `recost.py`). Per A49 L47: "Arithmetic, static proofs and RNG known-answer checks do not themselves constitute instrument outcome data."

- **Written:** 2026-11-01, about 11:37 AM–12:10 PM ET, by the Lead's executor. Lead rulings R1–R9 were given in the "ACI Research" room, about 11:15–11:35 AM ET; CNA's final room statement at 11:39 AM ET (no file) is carried in §0.2.
- **Shorthand:** "A49 Ln" = `/workspace/astra_consult49_response.txt` line n; "A44 Ln" = Astra #44 raw; "M Lnnnn" = merged v3.6; "MP Ln" = measurement plan v1; "CNA2/CNA3/S2.1 Ln" as in the inputs table; "CE49 Ln" = CNA E49-1/E49-3 file; "CE49a1 Ln" = its addendum 1; "RDL Ln" = RD light pass of CE49; "LC Ln" = Lead cost file v1; "LCL Ln" = RD cost light pass; "CD0 Ln" = CNA dose-0 / x_ref file; "LP2" = RD light pass of CD0 and CE49a1 (`6c02198c…`, filed 11:38 AM ET, folded in here); "V2.5-RD Ln" = RD E49-2 wording.
- **Safety (binding, unchanged).** X1–X5 unchanged. No host coupling. "no additional stop-associated reward, penalty or terminal return" (#42 L223). Claim ceiling (#41 L304) unchanged; tier-1 attribution ceiling stands. No consciousness, awareness or sentience claim is made or implied.

## 0. Precedence, scope and governance

1. **Precedence.** For E49-1..E49-3 and every item in R1–R8, this file governs over v2.3 (`48f75cfb…`), v2.4 (`cf56c653…`), V2.5-RD (`ae80cc12…`), CE49 (`d620918f…`), CE49a1 (`55030ebd…`), LP2 (`6c02198c…`), LC (`7d4cbbad…`), LCL (`d5ee9a1b…`) and CD0 (`647a72d2…`), **pending Astra #50**. Where this file is silent, v2.4 > v2.3 > v2.2 > v2.1 > v2 (v2 precedence map) as before. v2.4 G-v2.4 (GA-1 and Amendment A-2026-10-24 APPROVED by Aidan, "Yes to both", 2026-11-01 10:58 AM ET) is unchanged.
2. **Not a freeze, not an execution, not an approval.** Astra #49: "VERDICT: CLOSED WITH NUMBERED EDITS E49-1 through E49-3; no further authority approval for GA-1 is requested, and no freeze or execution is authorized." (A49 L147). Nothing here changes that.
3. **Governance of these rulings.** Each R-ruling is a prospective, pre-data gate/control/design choice under Amendment A-2026-10-24, made "before any data exists" in Astra's reading (A49 L47: includes calibration, pilots, feasibility and diagnostic outputs). It takes effect only "after addressing [Astra's] required conditions" (A49 L47), i.e. after #50. None touches X1–X5, the claim ceiling, or anything after data collection.
4. **Runs and benchmarks.** No benchmark is planned. Any benchmark or timing run (including an S0 preflight measuring u, R25 / M L2390) is a run: it needs its own frozen protocol producing no outcome data, Astra review, **and Aidan's explicit yes** before anything runs (room, CNA and RD, ~11:20 AM ET; Lead agreed).
5. **Track C excluded (R9).** Drift-plant and sleep-layer items belong to Track C and are not in this file.

### 0.1 Lead rulings applied (R1–R9, summary; details in the sections cited)
| # | Ruling | Applied in |
|---|---|---|
| R1 | Full GRID stays governing (M L2784; A44 L108); early stop NOT adopted; #50 asks whether a pre-registered early stop under CNA's three equivalence conditions plus one diagnostic point would be acceptable | §4.6, §9 |
| R2 | GA-1: governing E48 N definition kept; rows 1/3 count toward realization only via label-independent E5 plant checks; row 4b (BOUNDARY/UNRESOLVED) provisional; ask Astra | §1 |
| R3 | Fisher–Yates: idx = w0 mod (k+1), one word per swap, counter (508−k,0,0,0), 507 draws, no rejection; float form banned; new KAT `fa85f551…` | §2.2, §3.4 |
| R4 | Housekeeping: strike M L1966; Random123 labels; rewcorr-eta words; c0 = 508−k; MP gate units; L1965 cite; R25 wording | §2.5, §3, §7 |
| R5 | Dose 0 on four specificity rows only (RAND-INIT dose 0 DROPPED); NC2r OUT; LIM OUT conditional on a fixed, pre-registered s* grid bound | §5 |
| R6 | IGN-P1/scalar plants: t_s = 0, x_ref = x_lo; M L1129 "Network instruments only."; network tolerance provisionally the 0.99 quantile | §6 |
| R7 | Provisional inputs: Δt rule, t_r grids, noise convention (as refined by CNA's 11:39 statement, §0.2) | §6 |
| R8 | Cost: corrected per-cell lines; RECOST with R5–R7; runtime from op counts only, UNVERIFIED; DGX Spark = feasibility only | §8 |
| R9 | Track C items not in this file | §0.5 |

### 0.2 CNA room statement, 2026-11-01 11:39 AM ET (no file; recorded as relayed to the Lead)
1. CNA **withdraws** the CE49a1 L45 sentence "Hedging to BOUNDARY therefore cannot raise f_ok, and it cannot lower the false-licence rate" insofar as it says "cannot lower", and the matching clause of the CE49a1 Q2 draft (L64, "so hedging cannot improve either the realization fraction or the false-licence rate"). Moving a would-be false licence to BOUNDARY removes it from both numerator and denominator, which **can lower** the computed false-licence rate. CNA endorses both hedging safeguards (§1.3).
2. **Noise convention ADOPTED:** τ·dx = f(x)·dt + σ·√τ·dW, discretised (Euler–Maruyama) x ← x + (Δt/τ)·f(x) + σ·√(Δt/τ)·ξ, ξ ~ N(0, 1), with f(x) = −x + tanh(g·x + s) and σ the per-unit-τ noise scale, σ = 0.05·‖x_hi − x_lo‖ (M L1126).
3. **Δt:** the governing rule is the Lead's **Δt = τ / (100·max(1, g − 1))**. CNA's stability bound **Δt ≤ τ / (20·max(1, g − 1))** is recorded as the admissibility condition it satisfies (it does, by a factor of 5 for every g).
4. Noise scaling and Δt are removed from PENDING; only the plant gain **g** itself stays PENDING (CNA).

## 1. E49-1: GA-1 replicate truth table — CLOSED at design level (pending #50 Q1)

**Astra's edit (A49 L141):** "Add a complete GA-1 replicate truth table separating undefined cells, insufficient qualified support, qualified computed labels and construction failures. Preserve N -> real_i = 0 where specified; use all qualified replicates for the conditional false-licence assessment; do not let the >=36 condition replace realization or false-MET criteria."

### 1.1 Governing table (CE49 §1 L36–L43 as amended by CE49a1 §2 L39–L41 and §0.2 above)
Rows are evaluated in precedence order; exactly one applies to each of the 200 prespecified replicates per row and dose.

| # | Replicate state | real_i | False-licence (FL) denominator / numerator | Counts toward 36? | Reported as |
|---|---|---|---|---|---|
| 0 | Construction failure anywhere (non-finite value, M L3421; K_other empty; SD(z_R) = 0, M L3407; a licence with no computed label) | 0 | not entered | no | INCOMPLETE + failure step; a licence without a label → row FAIL |
| 1 | All-D (no residual coordinate) | E5 checks 1–2 only (M L1630) | not entered | no | UNDEFINED, "did not issue MET"; count D by dose |
| 2 | N: ≥ 1 ND cell and neither Route I nor Route B holds (or G1–G4 fail) | **0** (CE L48, kept) | not entered | no | count N |
| 3 | Q-insufficient: a route holds, Q cells span < 9 seeds | E5 checks 1–2 only | not entered | no | "did not issue MET (insufficient Q seeds)" |
| 4 | Q-labelled, label = NOT MET | E5 | denominator +1 | yes | count |
| **4b** | **Q-labelled, label = BOUNDARY or UNRESOLVED** (incl. E2-floor UNRESOLVED, M L771, M L2750; labels M L1884) — **PROVISIONAL, #50 Q1** | E5 checks 1–2 only | **not entered** (neither licence nor non-licence) | **no** | count by label and dose, reported separately |
| 5 | Q-labelled, label = MET | E5 | denominator +1, numerator +1 | yes | count; ρ_E, U_A |

- **Realization (M L698):** f_ok = Σ real_i·elig_i / 200 over all 200 prespecified replicates; realized iff the one-sided 95% CP lower bound ≥ 0.90, i.e. **≥ 188/200** (188 → 0.90460, P = 0.0320; 187 → 0.89864, P = 0.0566; CE49 L31, RDL L38).
- **False licence:** over **all** row 4 + row 5 replicates of the 200, never the first or best 36 (A49 L34). Criterion: point ≤ 0.05 and one-sided 95% CP upper ≤ 0.08 (**M L1965**; citation corrected from M L1964, R4).
- **Assessability:** only if the denominator is ≥ 36 (U(0,36) = 0.0798465; U(0,35) = 0.0820316, A49 L29–L30). ≥ 36 is necessary, **not a pass** (A49 L32), and it **does not replace realization** (A49 L43). Smallest denominators for x false licences: 36/58/77/95/112/129 for x = 0..5 (CE49 L51, RDL L37).
- **Status:** FAIL if FL is assessed and fails, or row 0 records a licence; PASS if realization holds and FL is met or NOT ASSESSED, with the CE L53 wording when D dominates or FL is NOT ASSESSED.
- **PZ7 role cell (CE49 L61, adopted):** "PASS = realization criterion met, no licence outside Q-labelled replicates, and, where assessed, the Q-branch false-licence criterion met (degeneracy guard exercised)". "PASS = correct withholding" is struck.
- **CE L31 correction (CE49 L62, adopted):** at the REPORTED dose ρ = 0, w_E = 0, so the residual ratio is **undefined** (cell D), not 0.

### 1.2 R2: governing N reading; Astra's A49 L43 reading NOT adopted, and why
- A49 L43 is conditional ("If, as the packet states, the first two are N and receive real_i = 0 …") and states "Retaining that rule is acceptable". The #49 packet did not classify all-D or Q-insufficient replicates as N (RDL L44); CE L48 defines N narrowly.
- **Ruling:** rows 1 and 3 are **not N**. They count toward realization **only** through the label-independent E5 plant checks 1–2 (M L1630), **never as correct withholds**, and they are outside every error rate. The broader reading (real_i = 0 for rows 1 and 3) is **not adopted**, because under CE §2.1's planning approximation it would leave the row CONFOUND NOT REALIZED at ρ = 0.9 almost surely, reinstating the pre-GA-1 block (CE49 L57), while the substance of Astra's warning (no realization credit for withholding) is already met.
- **Disclosed:** this is **more lenient** than the premise Astra reviewed (RDL L46). It is put to her explicitly (#50 Q1); it is not adopted silently.

### 1.3 Row 4b and hedging (R2 + RD addition + CNA 11:39 statement)
- Row 4b replicates are outside the FL denominator, do not count toward 36, are reported separately, and count toward realization only via E5 checks 1–2.
- **Hedging safeguards (endorsed by CNA, 11:39 AM ET; read here as):** (a) **no realization credit for any withhold** (rows 1, 3, 4b earn real_i only from label-independent plant checks), so hedging cannot raise f_ok; (b) **row 4b is excluded from the ≥ 36 count**, so hedging makes the FL criterion harder to assess. Row 4b is also **reported by label and dose** so a hedge rate is visible. RD adds (LP2 AD-1): relative to counting BOUNDARY as a non-licence, excluding it can only raise or keep the rate (x/n ≥ x/(n + b)); and an instrument that hedges at nulls also loses power at positives (MET-rate CP lower bound ≥ 0.90, M L1965), which is the substantive guard.
- **Withdrawn (CNA; also LP2 AD-1):** "cannot lower the false-licence rate". Hedging a would-be MET to BOUNDARY **can lower** the computed FL rate (e.g. 5/100 → 0/95). Whether a further guard is needed (e.g. a pre-registered worst-case sensitivity counting 4b as licences, or a cap on the 4b fraction) is asked in #50 Q1; **no position is taken** and nothing is added here.

## 2. E49-2: IGN final partition, independence, eligibility, pooled test, namespace — CLOSED at design level (pending #50)

**Astra's edit (A49 L143):** "Freeze the IGN final-partition interpretation and actual partition counts. State conditional trial independence, separate trialwise from aggregate eligibility, and describe the heterogeneous pooled calculation as the justified fixed-threshold test. Include row, dose, replicate, role and partition in the RNG namespace."

V2.5-RD (1)–(6) (L46–L86) is **adopted as the consolidated E49-2 text**, with these consolidation changes:

### 2.1 Allocation (V2.5-RD (1), adopted)
Per (seed, required bin): **fitting 254, selection 127, final 127** (508); the ≥ 100 quota applies to the final partition only (A49 L64); n_s = 127 never lower (V2.3 D47). These count trials, not fits or runtime (A49 L71).

### 2.2 Partition assignment (V2.5-RD (1a) closed by CE49 §2(a) as amended by R3)
- Slots carry ordinals **j = 0…507 per (cell, seed, bin)**, fixed at schedule-build time before partition (CE49 L71). V2.5-RD L76's per-partition slot ordinal is **struck** (E-RD-5).
- **Keyed Fisher–Yates, integer form (R3; CE49a1 §1 L7–L15):** for k = 507 down to 1, one Philox4x64-10 block under role `ign-partition` at counter (508 − k, 0, 0, 0); idx = w0 mod (k + 1) (unsigned 64-bit); swap a[k], a[idx]; w1–w3 discarded; **exactly 507 draws, no rejection loop, no retry counter**. Positions 0–253 → fitting, 254–380 → selection, 381–507 → final: exactly 254/127/127 for any key.
- **Bias bound (relative):** |m·P(idx = i) − 1| < m/2^64 ≤ 508/2^64 = **2.7539 × 10⁻¹⁷**. It bounds the **relative** deviation; the exact maximum at m = 508 is 256/2^64 = 1.3878 × 10⁻¹⁷ and the absolute deviation |P − 1/m| is ≤ 2.73 × 10⁻²⁰ (LP2 (a)). Counts are exact regardless; the assignment reads no outcome.
- **Position vs slot (LP2 (a)):** after the shuffle, the value a[p] at **position** p is a **slot ordinal** j; slot j is in fitting iff j ∈ {a[0..253]}, selection iff j ∈ {a[254..380]}, final iff j ∈ {a[381..507]}.
- **Banned:** the float form ⌊(k + 1)·u⌋; contiguous slot ranges (they alias schedule order, CE49 L69); any rejection sampler.
- D27's environment-seed-hash split stays for every non-IGN row.

### 2.3 Conditional independence (V2.5-RD (2), adopted)
Independent conditional on the frozen plant, schedule and RNG keys, code, pre-final fitted quantities and seed-level settings (A49 L73); not unconditionally; not identically distributed. CE F-4's "i.i.d. … exactly binomial" is superseded. Under R6, scalar-plant trials have no settling tolerance; the fitted settling tolerance in V2.5-RD (2) applies to network instruments only.

### 2.4 Trialwise vs aggregate eligibility (V2.5-RD (3a)/(3b), adopted; (3b)(iii) completed)
Trial-level: each scheduled final-partition trial classified once; missing/invalid/non-finite = ineligible, stays in the denominator, never topped up. Aggregate: (i) quota ≥ 100/127 per (seed, required bin); (ii) pooled floor x ≥ x_min(N) per (replicate, required bin); (iii) **the three MP L78–L81 bin-wide gates**, each a **separate aggregate outcome with its own reason code**, never altering any trial's eligibility, never entering (i) or (ii), never treated as 127 trial failures (A49 L73). **Evaluation units (R4; CE49a1 E-RD-7, adopted):**

| Gate | Text | Evaluation unit | Status |
|---|---|---|---|
| G-i | MP L79 "the transition s* lies outside the probed grid" | one decision per (replicate), selection partition, pooled across seeds | Rule PENDING; must be a **fixed, pre-registered grid bound, not fitted** if LIM stays OUT (R5, §5) |
| G-ii | MP L80 "fewer than n_trial trials fall per near-transition bin" | **the same test as quota (i)**, per (seed, required bin), n_trial := 100 eligible of 127 final slots; reported once, under one reason code | adopted |
| G-iii | MP L81 "Var(w) is below a floor" | per (replicate, near-transition bin), final partition, pooled across seeds | floor value PENDING (CNA) |

M L1130 coverage (CP lower bound of the eligible fraction ≥ 0.90 at every required and near-transition bin) remains the per-bin coverage gate (UNRESOLVED on failure).

### 2.5 Pooled test (V2.5-RD (4), adopted)
"a conservative fixed-threshold eligibility test for the average conditional probability across the scheduled trials" (A49 L75). x_min ≥ 0.9N + 1 holds for all nine GRID values (CE49 L93–L103; RDL L90). Hoeffding (1956) Theorem 4 regime as commonly stated; **p. 718 UNVERIFIED** (doi.org HTTP 500, Project Euclid block; not bypassed). **Citation inconsistency:** V2.5-RD L68 gives Ann. Math. Statist. **27(4)**, CE49 L84 gives **27(3)** (Sept. 1956, pp. 713–721); to be fixed against the publisher record before freeze (UNVERIFIED this pass).

### 2.6 RNG namespace (V2.5-RD (5), field list; encoding per CE49 §4.2)
All A49 L77 / L143 fields present (row, dose, outer replicate, role, partition), plus generator ID, replicate set and **n_grid** (closes the R37 seed-reuse dependence, LCL L73). R37 (M L2407) is superseded by the §3.2 address for derivation. Banned components as V2.5-RD L80.

### 2.7 Cost and n_seed (V2.5-RD (6), adopted; numbers in §8)
Allocation retained; complete procedure costed (§8); n_seed by the frozen rule; any reduction explicit and prospective, before any calibration, pilot or feasibility output (A49 L47, L87); hardware = feasibility only (A49 L85).

## 3. E49-3: counter subindex, address, KATs, kernel carry — CLOSED at design level (pending #50 Q5)

**Astra's edit (A49 L145):** "Define counter subindex s and its word allocation, preserve branch-invariant RNG addressing, and separate exact integer KATs from floating-transform checks. Carry the reported canonical kernel and INTERACT definitions into the consolidated freeze text."

### 3.1 Counter (CE49 §4.1, adopted)
Philox4x64-10; counter (c0, c1, c2, c3) = (t, s, 0, 0); nonzero c2/c3 = construction failure. t = absolute step of the **root** episode (inherited by continuations) for episode roles; trial step from 1 for IGN trials. s = 0 for one block per step; otherwise the fixed ordinal in the frozen variable list; range declared per role; out-of-range = construction failure. Ban (A49 L118, verbatim): "It must never become a branch ID, donor ID or call-order counter." Unused words discarded; no cached sine/second normal (A49 L116).

**Role registry (R4; CE49a1 §1, §3):**
| Role | Suffix | c0 | s (c1) | Words |
|---|---|---|---|---|
| rewcorr-eps | root episode ID | t | 0 | w0 → u1 = ((w0 >> 11) + 1)·2⁻⁵³, w1 → u2 = (w1 >> 11)·2⁻⁵³; Box–Muller cosine only |
| rewcorr-eta | root episode ID | t | k = 1…d_ws − 1 (s = 0 unused; range PENDING d_ws, P4) | **as rewcorr-eps, one η_k per (t, s = k) block; w2, w3 discarded** (R4) |
| action | root episode ID | t | 0 | w0 → u_b, w1 → u_k |
| ign-trial | bin, slot j (0…507) | trial step t (1…N_steps) | 0 (IGN variable list PENDING the generator spec) | plants: one normal per step (w0, w1 → Box–Muller, as rewcorr-eps) |
| ign-partition | bin | **508 − k ∈ {1…507}** (fixed loop position, not a step or call-order counter) | 0 | w0 only |

If a `stop` role is ever registered (R37 purpose list), its draws feed only the scheduler, never policy inputs (M L280; RDL L104).

### 3.2 Address (CE49 §4.2, encoding v2, adopted)
Domain "ACI-TrackB-RNG-v2"; fields in order: domain; master seed; replicate set; generator/plant ID; row ID; dose index; n_grid; replicate index; partition; seed index; role tag; role suffix. 4-byte big-endian length prefix per field; D = SHA-256(encoding); k0, k1 = little-endian uint64 of D[0:8], D[8:16]. CE L160–L167 test rows superseded. **Dose-index rule (consolidation addition, PENDING CNA confirmation):** a dose-0 sanity arm (§5) must have its **own index in the row's frozen dose list**, distinct from every required dose; "dose index 0" in the CE49 KAT rows means the first listed dose, not the dose-0 sanity level.

### 3.3 Known-answer checks: integer (exact) vs floating point (separate)
- **Integer Philox, exact word equality.** Random123 tests/kat_vectors (`aab5ebab…`): **KV L38–L40 are Philox4x64-7 (7 rounds); KV L41–L43 are Philox4x64-10 (10 rounds)** (R4 label correction; RDL L64–L72). Only L41–L43 test the pinned generator; L38–L40 test the same round function at 7 rounds. **Lead re-check this pass (independent pure Python): 6/6 MATCH.**
- **Address/key rows** R1–R10 (CE49 L190–L205) reproduced by RD (RDL L73). R11's float-form permutation (prefix `268a77b6…`) is **superseded** and retained only as a record of the banned form.
- **New permutation KAT (R3; CE49a1 L19–L28), re-checked independently this pass: MATCH.** Address (confirm, IGN-P1, IGN-P1, dose index 0, n_grid 0, rep 0, partition none, seed 0), role ign-partition, bin 0; placeholder zero master seed (TEST VECTOR ONLY); K = `e5b870ec7ff01d19169f9234ebc361a3`; zero-vector self-check `16554d9eca36314c db20fe9d672d0fdc d7e772cee186176b 7e68b68aec7ba23b`; first draws (507, 49), (506, 346), (505, 464), (504, 103), (503, 212); last (1, 0); a[0:8] = 79, 468, 482, 332, 173, 222, 63, 342; counts 254/127/127; selection slots begin 3, 6, 9, 18, 20, 31, 38, 39; final 1, 4, 8, 12, 17, 22, 24, 25; SHA-256 of the comma-joined permutation **`fa85f5518477d78bf72e2048786a42aa8401807a87fe4782cb52b8d936091379`**.
- **Floating-point transform (separate):** CE49 L208–L214 values (R1 n −1.7638012618999939, R2 −0.58896812511241703, R7 −0.74171324587159282; R9 u_b, u_k bit-exact) reproduced by RD. Tolerance PENDING (P6): bit-exact under the pinned libm, otherwise ≤ 4 ulp, with RD's note that an absolute floor may be needed near n ≈ 0 (RDL L75).
- **Provenance:** CE49 and CD0 used scipy in `/tmp/sv` (not system python3); every CE49 figure reproduces in pure Python (RDL L12).

### 3.4 Kernel and INTERACT carry (FREEZE TEXT, verbatim from V2.3 L84 and L87; byte-identical to CE49 L223/L226 and CE L111/L115, RDL L95–L96)

**[FREEZE TEXT] Kernels (V2.3 L84):**
> "**Action law (Stage-0 attribution plants).** Each step t draws u_b, u_k ∈ [0, 1) from role 'action' (§5.3 mapping, words w0, w1). The **kernel target** T_k(t) is the nearest available target at the start of step t (food item for -E food rows; repair station for -I rows), by shortest-path length, ties to the lowest target index. It is distinct from the endpoint target T of B/B_I. (i) **No available target:** the action is A7[⌊6·u_k⌋], independent of g. (ii) Otherwise, approach iff u_b < p_t = σ(a − β·g_t), β = 1.2. Approach = INTERACT if on T_k(t), else the lowest-index A7 move that strictly decreases the distance to T_k(t). Non-approach = K_other[⌊|K_other|·u_k⌋], where K_other is the set of A7 actions that do not strictly decrease the distance (excluding INTERACT when on T_k(t)), ordered by A7 index. (iii) K_other cannot be empty in any reachable state (STAY never decreases the distance; off target INTERACT does nothing). If found empty, that is a construction failure (M L3421) and no fallback is used. No rule reads g other than through p_t, nor the block (except through g), any probe, or any stop, truncation, horizon-end or schedule quantity (M L280). Every frozen SD divisor is > 0 at freeze." Then TV(π_g, π_g′) = |p(g) − p(g′)| ≤ 0.3|g − g′| in every reachable state (#48 L142).

**[FREEZE TEXT] Endpoint B/B_I incl. the INTERACT predicate (V2.3 L87):**
> "B (B_I) = (1/10)·Σ_(u = t_d+1..t_d+10) b_u. T is the endpoint target fixed at t_d (nearest available food item for E rows, repair station for I rows, by shortest-path length on the static wall grid, ties to the lowest index; M L2079–L2080). d_u is the shortest-path (= Manhattan, A1) distance from the agent to T's cell after A16 step 2 (movement) of step u; d_(t_d) is the distance at the end of t_d. b_u = 1 iff the episode has not terminated in-world before u, T is available at the start of step u (state at the end of step u − 1), and either (a) d_u < d_(u−1), or (b) the agent is on T at the start of step u and its action at u is INTERACT. Otherwise b_u = 0, including every step after in-world termination and every step at whose start T is unavailable. Unavailable steps are scored 0, never excluded. Each b_u ∈ {0, 1} depends on world state and actions only. A trial with no available or reachable target at t_d is ineligible (counted; M L2858). No evaluation episode carries a scheduled stop (R4, M L2362)."

**[FREEZE TEXT] Indices (CE L97):** A7 index N = 0, S = 1, E = 2, W = 3, STAY = 4, INTERACT = 5. Food item index: slot 0–3 in A17 placement order, kept through respawn. Station index: template definition order (A3).

"Ineffective" INTERACT reading (CE49 L233): counted whenever the agent is on an available T at the start of u, whatever the A16 step-3 outcome (CNA reading; no text change). **Do not carry v2 consolidated L37** (K_approach fallback, D50).

## 4. Calibration loop (R1, R4)
### 4.1 Full GRID governs
M L2784 (verbatim): "Record pass(g,k,n) for **every** n in GRID; do not stop at the first passing n." Source A44 L108: "Retain the full grid results; do not impose monotonicity by replacing failed results." **Early stop is NOT adopted.** Calibration = 200 × 4,572 × 292 = **267,004,800** trials per calibration cell.
### 4.2 Stale text (R4)
- **M L1966** ("3 [v3.3 E43-4]. n_seed = max over (g, k) of n*(g, k). …") is **struck** in the consolidated freeze text; its BLOCKED clause survives in M L2785. **M L1963** ("n*(g,k) = smallest n in GRID meeting every target below …") is tagged superseded by M L2784–L2785 / L3175 (RDL L31; CE49a1 L59).
### 4.3 Question to Astra (#50 Q2), no change adopted
Would a pre-registered early stop be acceptable under CNA's three equivalence conditions — (1) selection = the smallest GRID point at which every R_core (g, k) passes, each pass computed only from that point's own data, with every (g, k) run at each n until the common pass point; (2) streams keyed by grid value (n_grid field); (3) no pooling across points and nothing computed altered (append-only) — plus **one diagnostic point** above the selected n that feeds **no selection, licence or claim**, with a failure read against that point's **pre-stated false-fail rate** (a single failure is expected noise, a finding only beyond that rate)? And does "retain the full grid results" (A44 L108) mean computed results at every GRID point (CE49a1 Q3)? Budget must cover the worst case either way (Σ = 292, CE49 L139).

## 5. IGN cells, dose 0, NC2r and LIM (R5)
| Row | Type | Required doses (cells) | Calibration (C_cal) | Confirmation | Dose 0 |
|---|---|---|---|---|---|
| IGN-P1 | scalar plant | 1 (g, nominal dose PENDING CNA) | IN | 1 | none |
| IGN-N1 | scalar plant | 1 (g < 1, value PENDING) | IN | 1 | none |
| IGN-NC1 | scalar plant | Δs ∈ {2, 4} (2) | IN | 2 | **yes** (Δs = 0, PROPOSED CD0 L28) |
| IGN-NC2 | scalar plant | clip quantile {0.8, 0.6} (2) | IN | 2 | **yes** (no clip, PROPOSED) |
| BOTTLENECK-ONLY | network | g_b, 2 levels (values PENDING) | IN | 2 | **yes** (linear gate, PROPOSED) |
| RAND-INIT (IGN part) | network | g_0 ∈ {0.9, 1.0, 1.1}× (3) | IN | 3 | **DROPPED** (R5; no natural "off" value) |
| Architecture-imposed | network | β, 2 levels (values PENDING RD/CNA) | IN | 2 | **yes** (linear gate, PROPOSED) |
| IGN-NC2r | scalar plant | none declared | **OUT** | 1, REPORTED only at the inherited n_seed | none |
| IGN-LIM | scalar plant | s* offset, 2 levels | **OUT, conditional** (below) | 2, at the inherited n_seed; gate "Correct UNAVAILABLE on LIM ≥ 0.90" (MP L199) | none |

- **C_cal = 13 cells** (6 scalar, 7 network). **C_conf = 20 cells** (13 + NC2r 1 + LIM 2 + dose-0 4; 11 scalar, 9 network).
- **Dose 0** (CNA2 L242: "a dose-0 sanity level that is REPORTED only … Only required doses enter the label"): four rows (NC1, NC2, BOTTLENECK-ONLY, Architecture-imposed); confirmation-only fresh arms at R_rep = 200 and the frozen n_seed; 914,400·n_seed each; never calibration or step 3a (M L1951); never blocks or passes a row; no arm reuse (CD0 L25). Dose-0 parameter values are CNA's PROPOSED rule ("confound mechanism switched off", CD0 L27–L31): PENDING #50 Q3.
- **NC2r OUT:** its gate would depend on n_seed (CD0 L36), but as written it has no required dose and only challenges a reading Architecture-imposed already tests (CNA2 L187, L290). It is REPORTED, confirmation-only, and may not be made a required check without re-entering C_cal.
- **LIM OUT, conditional:** OUT only if the MP L79 "s* outside grid" decision is a **fixed, pre-registered grid bound** (n_seed-independent, not fitted from pooled data). If the frozen rule estimates s* from data, LIM goes IN (CD0 L42). The rule is still ABSENT (CE49 §2(c)); to Astra, #50 Q3.
- LCL's 18/16 dose-0 scaling and LC's 6/16 lower bound are withdrawn (LCL L47–L48).

## 6. IGN-P1 x_ref, settling, tolerance, noise, Δt, t_r (R6, R7, CNA 11:39)
### 6.1 Scalar plants (R6; CNA rejection CD0 §B stands)
The provisional adoption of RD's settling proposal (LCL §6) is **reversed**. With process noise, the end-of-settling state is half-normal about its median in 1-D, so the 2×MAD tolerance would exclude a fixed 17.7% (Reading I) or 42.5% (Reading II) of trials whatever σ, g, τ, failing coverage (M L1130) by construction and contradicting "e_exp = 1.0 by construction" (**CNA2 L258**; CD0 cites L259, corrected per LP2 X-1) (CD0 L50–L56; closed-form; reproduced in LP2 (f)). **Replacement wording for the merge (M not edited):**
- **M L1127:** "t_s = 0 in scalar plants: each trial starts from the analytic reset x(t_0) = x_lo and x_ref = x_lo (S2.1 L240, L242; M L314); no settling, so no trial is excluded on this gate and e_exp = 1.0 by construction (CNA2 L258). Networks: 20 steps (rationale unchanged)." (Citation corrected from CD0's "CNA2 L259", LP2 X-1.)
- **M L1129:** prefixed "**Network instruments only.**"
- M L314 is unchanged (it already says x_ref = x_lo in IGN-P1).
- **PENDING CNA:** for the monostable IGN-N1 (g < 1) and any other scalar plant, "x_lo" must be defined as that plant's declared null-input stable point.
- The settling-exclusion path (A42 L221) is exercised in Stage 0 by the network-type rows (7 of 13 C_cal cells).

### 6.2 Network settling tolerance (provisional, #50 Q4)
The 2×MAD rule's exclusion depends on dimension (Reading I: 0.1773 at d = 1, 0.0625 at d = 2, 0.0237 at d = 3, 0.0094 at d = 4, 0.0003 at d = 8; CD0 L70–L75). Under Reading II the dependence runs the other way and is worse (exclusion 0.4248, 0.6688, 0.8381, 0.9294, 0.9989 at d = 1, 2, 3, 4, 8; LP2 X-2). **Provisional:** tolerance = the **0.99 quantile of ‖x_ref − median x_ref‖ over null-input runs on the fitting partition**, chosen without w (≈ 1% expected exclusion in any dimension). This removes the dimension dependence under both readings and moots the Reading I/II question for networks. The number of null-input runs (which sets the quantile's precision) is ABSENT (PENDING CNA).

### 6.3 Plant noise and Δt (ADOPTED per CNA 11:39 statement; R7 refined)
- **Dynamics:** τ·dx = f(x)·dt + σ·√τ·dW, f(x) = −x + tanh(g·x + s). σ = 0.05·‖x_hi − x_lo‖ is the per-unit-τ noise scale (M L1126).
- **Discretisation (Euler–Maruyama):** x ← x + (Δt/τ)·f(x) + σ·√(Δt/τ)·ξ, ξ ~ N(0, 1), one normal per step from role `ign-trial` (§3.1).
- **Noise placement:** process noise per M L1126; **MP L84's placement of ξ inside tanh is superseded** (flagged to Astra, #50 Q4).
- **Δt (governing):** **Δt = τ / (100·max(1, g − 1))**. **Admissibility condition (CNA):** Δt ≤ τ / (20·max(1, g − 1)); satisfied by a factor of 5 for every g. Every t_r must be an integer multiple of Δt (true for the grid below).
- LP2 X-3 (Δt rationale fails for g > 2) and X-4 (noise applied to τ·dx or dx) are **resolved** by the two rules above.
- **PENDING (CNA):** only the plant gain **g** for each scalar plant (IGN-P1 g > 1; IGN-N1 g < 1; NC1/NC2/NC2r/LIM base g). Noise scaling and Δt are no longer PENDING.

### 6.4 t_r grids and steps per trial (R7, provisional)
- **t_r grid:** plants {2τ, 3τ, 5τ}; networks {3, 5, 8} steps. All candidates read from one trajectory per trial on the selection partition, so only t_r,max costs (CD0 L90).
- **Plant steps per trial:** N = t_r,max/Δt = 5τ/Δt = **500·max(1, g − 1)**; **500** for every g ≤ 2 (the headline basis; scale ×(g − 1) if a frozen g exceeds 2).
- Against LC's 8τ basis (t_s 5τ + t_r 3τ), a scalar-plant trial now costs t_r,max/8τ: **3/8 to 5/8**, depending on the grid maximum (3τ…5τ); at the provisional grid it is **5/8**. Cost is set by t_r,max, and the grid must contain M L1128's 3τ, so 3/8 is the floor. The Delegate's room figure "2/8 to 5/8" was **withdrawn by RD in LP2 (g)**; CD0 L68's 3/8–5/8 stands. (This reverses the 2/8 wording relayed to the consolidation before LP2 was filed.)
- **Network steps per trial:** t_s + t_r,max = 20 + 8 = **28** agent steps.

## 7. Housekeeping and stale-text list for the next merge (R4; M is not edited)
1. M L1966 struck; M L1963 tagged superseded (§4.2).
2. Random123 labels corrected (§3.3).
3. rewcorr-eta word allocation and `ign-partition` c0 = 508 − k (§3.1).
4. MP L79–L81 gate units (§2.4).
5. False-MET criterion citation: **M L1965**, not M L1964.
6. **R25 workload line (M L2390)**, replacement wording (LCL L119, adopted): "Workload, arithmetic on proposed values, per required generator × dose cell c: confirmation 200 replicate evaluations at n_seed*; sample-size calibration 200 × |GRID| = 1,800 replicate evaluations (200 × ΣGRID = 58,400 seed-units; every n in GRID is run, PZ6 §3.2), plus PZ5 §4.2 step 3a 2 × 200 = 400 replicate evaluations at n_seed*; dose calibration ≤ 50 × (plants with fitted references or κ_f). At R25's illustrative 25 × 3 = 75 cells: 15,000 + 135,000 + 30,000 + ≤ 3,750 replicate evaluations. Superseded for budgeting by PZ5 §8.2 (L-CAL / L-CONF)."
7. Citation fixes from LCL: CNA2 **L289/L290/L308** (not L283/L284/L309); M **L1967** (not ~L1963), **L1951**, **L1958**, **L2170**.
8. M L1127 / L1129 replacement wording (§6.1).
9. V2.5-RD L76 per-partition slot ordinal struck (§2.2); CE F-4 key and "exactly binomial" superseded; R37 superseded for derivation by the v2 address.

## 8. Cost (R8): corrections, then RECOST under R5–R7 (all runtime UNVERIFIED)
**No figure here is a measurement.** Nothing was run or timed. R25 requires the per-unit cost u to be measured in an authorized S0 preflight; any such run needs Aidan's explicit yes (§0.4).

### 8.1 Per-cell lines (LCL adopted)
- Calibration ledger per C_cal cell: GRID sweep 200 × 4,572 × 292 = **267,004,800** + step 3a 2 × 914,400·n_seed* = **1,828,800·n_seed*** (M L1967, M L2161; calibration-side).
- Confirmation ledger per cell: **914,400·n_seed*** (V2.5-RD L88; stands).
- Per C_cal cell: 267,004,800 + 2,743,200·n_seed* = 450,799,200 at 67 and 291,693,600 at 9. Calibration-ledger share **per C_cal cell**: **86% at 67, 97% at 9** (LCL L45).
- LC's 16-cell, all-scalar range is corrected to **≈ 117 to ≈ 55,974 CPU-h (UNVERIFIED)** at 67 (LCL L62); it is superseded by §8.2.
- Bootstrap ops are 10⁴ × seed-units (LCL L54), not 2,400 × 10⁴ × 67 per cell.

### 8.2 RECOST (cells per §5; steps per §6.4; exact trial arithmetic)
T_total = 267,004,800·|C_cal| + 1,828,800·n·|C_cal| + 914,400·n·|C_conf|, |C_cal| = 13, |C_conf| = 20 → **3,471,062,400 + 42,062,400·n_seed*** trials.

| Quantity | n_seed* = 67 (R26 budget only) | n_seed* = 9 (GRID floor) |
|---|---|---|
| Scalar-plant trials (6 cal + 11 conf cells): 1,602,028,800 + 21,031,200·n | 3,011,119,200 | 1,791,309,600 |
| Network trials (7 cal + 9 conf cells): 1,869,033,600 + 21,031,200·n | 3,278,124,000 | 2,058,314,400 |
| **Total scheduled trials** | **6,289,243,200 (≈ 6.29 × 10⁹)** | **3,849,624,000 (≈ 3.85 × 10⁹)** |
| Calibration ledger (GRID + 3a) / confirmation ledger | 5,063,947,200 / 1,225,296,000 | 3,685,032,000 / 164,592,000 |
| Calibration share, **whole procedure** | **80.5%** | **95.7%** |
| Seed-units U = 13 × (58,400 + 400n) + 20 × 200n | 1,375,600 | 842,000 |
| Dip tests (4 per seed-unit) / bootstrap ops (10⁴·U) | 5,502,400 / 1.38 × 10¹⁰ | 3,368,000 / 8.42 × 10⁹ |

(Previous 16-cell basis: 7,212,787,200 at 67 and 4,667,097,600 at 9. The whole-procedure calibration share differs from the per-cell 86%/97% because 7 confirmation-only cells are added.)

**Per-unit cost model (UNVERIFIED, op counts only; LC §4 as corrected by LCL L57–L59):**
- Scalar-plant step: 200–300 op-equivalents (one Philox4x64-10 block, one Box–Muller normal, one Euler–Maruyama update). Compiled at ~10⁹ ops/s → 0.2–0.3 µs/step; interpreted at 10⁷–10⁸ ops/s → 2–30 µs/step. Per trial (500 steps): **100 µs (low) to 15 ms (high)**.
- Network trial: 28 steps × 2·d_h² flop × c_flop. **d_h is ABSENT (P4).** Illustration at LC's values d_h = 256, c_flop = 10⁻⁹ s: 3.67 ms per trial. Scales as (d_h/256)².
- Fits: F = 2 models × |t_r grid| (3) × 2 readouts × restarts (1–3) = **12 to 36** per seed-unit (NC1's per-c-level factor ignored); t_fit 0.03–0.3 s.

| CPU-h component (UNVERIFIED) | n = 67 low | n = 67 high | n = 9 low | n = 9 high |
|---|---|---|---|---|
| Scalar-plant trials | 83.6 | 12,546.3 | 49.8 | 7,463.8 |
| Fits (F 12 @ 0.03 s … F 36 @ 0.3 s) | 137.6 | 4,126.8 | 84.2 | 2,526.0 |
| Bootstrap + dip (table p) | < 1 | ≈ 1 | < 1 | ≈ 1 |
| **Subtotal without network trials** | **≈ 221** | **≈ 16,673** | **≈ 134** | **≈ 9,990** |
| Network trials at d_h = 256, 10⁻⁹ s/flop (illustrative point) | 3,341.9 | 3,341.9 | 2,098.4 | 2,098.4 |
| (sensitivity: d_h = 64 / 512) | 208.9 / 13,367.5 | | 131.2 / 8,393.4 | |
| **Total with the illustrative network point** | **≈ 3,563** | **≈ 20,015** | **≈ 2,232** | **≈ 12,088** |

- **Headline (UNVERIFIED):** ≈ 6.29 × 10⁹ trials at 67 (3.85 × 10⁹ at 9); **≈ 221–16,673 CPU-h excluding network trials, ≈ 3,563–20,015 CPU-h including them at the illustrative d_h = 256** (n = 67). The network term is the largest uncertainty and is set by P4.
- **Not in totals (conditional):** IGN dose calibration (R_cal,dose = 50, replicate size ABSENT); network settling-tolerance null runs (count ABSENT); hysteresis sweeps (unscheduled, count ABSENT); simulated dip p-values (method ABSENT). Plant steps scale ×(g − 1) for any frozen g > 2.
- Wall-clock = CPU-h / usable parallel cores (embarrassingly parallel). **DGX Spark changes feasibility only, not validity** (A49 L85); no hardware decision is made.

### 8.3 Levers (no position taken)
L1–L5 as LC §5 and A49 L81–L85, verbatim there: the 100-trial quota (needs instrument revision and re-validation), fewer bins, fewer replicates or doses (recalculate OCs; dropping a required dose needs an explicit amendment), lower n_seed by the frozen rule (already legitimate), more hardware (feasibility only). Two design facts from the recost, stated without a position: calibration is ≈ 81–96% of trials and is fixed by GRID (Σ = 292) × |C_cal|; network trial cost scales with d_h². Any reduction must be explicit and prospective, before any calibration, pilot or feasibility output (A49 L47, L87). Early stop is not a lever (§4).

## 9. Do-not-implement additions (continuing D1–D53)
| # | Text | Status | Replacement |
|---|---|---|---|
| D54 | Fisher–Yates float form ⌊(k + 1)·u⌋ (CE49 L72) and its KAT (R11, prefix 268a77b6) | Banned / superseded | §2.2, §3.3 |
| D55 | Any rejection-sampled or retry-counted partition draw; contiguous IGN slot ranges | Not permitted | §2.2 |
| D56 | Calibration early stop (and LC's 8,229,600 per-cell figure as a design figure) | Not adopted (M L2784) | §4 |
| D57 | M L1966 "max over (g, k)"; M L1963 step-2 line | Struck / superseded | M L2784–L2785, L3175 |
| D58 | Settling t_s = 5τ and the 2×MAD tolerance for **scalar plants** (M L1127/L1129 plant clauses; LCL §6 proposal) | Withdrawn (CNA) / reversed (Lead) | §6.1 |
| D59 | Dose 0 in calibration or step 3a; RAND-INIT dose 0; LC's 18/16 scaling and 6/16 bound | Not permitted / dropped / withdrawn | §5 |
| D60 | Noise inside tanh (MP L84 placement) for Stage-0 plants | Superseded | §6.3 |
| D61 | "Hedging cannot lower the false-licence rate" (CE49a1 L45, L64 clause) | Withdrawn (CNA 11:39) | §1.3 |
| D62 | Scoring rows 1, 3 or 4b as correct withholds; "PASS = correct withholding" | Not permitted | §1 |
| D63 | V2.5-RD L76 per-partition slot ordinal | Struck | §2.2 |

## 10. Open / PENDING items
| # | Item | Owner | Blocks |
|---|---|---|---|
| O1 | Astra #50 on Q0–Q7 (packet prepared, unsent) | Lead → Astra | adoption of everything marked provisional |
| O2 | Row 4b treatment and any further hedging guard (§1.3) | Astra #50 Q1, then Lead | E49-1 final |
| O3 | Early-stop question; meaning of "retain the full grid results" | Astra #50 Q2 | nothing (full grid governs) |
| O4 | MP L79 s* rule as a fixed pre-registered grid bound (sets LIM OUT/IN) | Lead/RD, Astra #50 Q3 | C_cal membership of LIM |
| O5 | Dose-0 parameter values (CD0 L27–L31) | CNA, Lead, #50 Q3 | dose-0 arms |
| O6 | Plant gains g (P1, N1, NC1, NC2, NC2r, LIM base); nominal dose; x_lo for monostable N1 | CNA | Δt value, steps, plants |
| O7 | BOTTLENECK g_b values; Architecture-imposed β values | CNA; RD with CNA | network cells |
| O8 | Var(w) floor value (G-iii) | CNA | aggregate gates |
| O9 | Network tolerance 0.99 quantile (provisional; a prospective gate change needing Astra's review, LP2 (h)) and null-run count | CNA, #50 Q4 | network settling |
| O10 | IGN variable list for `ign-trial` s-ordinals; rewcorr-eta s-range (d_ws, P4) | CNA | registry |
| O11 | Dose-index rule for dose-0 arms (§3.2) | CNA | address |
| O12 | Float-transform tolerance and pinned libm (absolute floor near n ≈ 0) | P6 | KAT (iii) |
| O13 | Hoeffding p. 718 regime and issue number 27(3)/27(4) | someone with sanctioned access | §2.5 citation |
| O14 | d_h and other architecture values (network cost) | P4 | §8 network term |
| O15 | Per-ledger caps (u from an authorized S0 preflight; Aidan's yes for any timing run) | P5, Aidan | AUTH-CAL/AUTH-CONF |
| O16 | CD0 / CE49a1 reissue: header times (LP2 item 6) and the CNA2 L258 citation (X-1) — fixed here by citation; CNA may reissue | CNA | nothing |
| O17 | Clean consolidated freeze text (v2 §4 F1) | P6(a) | freeze |

## 11. P1–P6 status (v2.5)
| # | Prerequisite | v2.5 status |
|---|---|---|
| P1 | CNA disposition, REW-CORR law, GA-1 | **CLOSED at design level** (#49 Q0/Q5: only E49-1..E49-3 outside P4–P6; GA-1 approved by Aidan). E49-1 closure pending #50 Q0/Q1 (row 4b provisional). |
| P2 | B_req | **CLOSED:** K_s = B_req = 9 (#48 L40; #49 Q2 premise). |
| P3 | e_PD / IGN allocation | **CLOSED (superseded form):** e_PD = 0.90; per-seed R22; n_s = 127 final per (seed, bin); 254/127/127 (A49 L64–L69); pooled floor as §2.5. The v2 n_sched = 121 pooled form is superseded. |
| P4 | Architecture values | **OPEN:** d_ws, d_h, g_b, β, A-EXT values; now also sets the network cost term. |
| P5 | Per-ledger caps | **OPEN:** recost §8 is the trial basis; u needs an authorized S0 preflight (Aidan's yes for any timing run). |
| P6 | Remaining defaults | **OPEN:** pinned libm and float tolerance; V11 tolerance; percentile type; clean consolidated text; plus provisional R6/R7 inputs pending #50. |

## 12. Inconsistencies found this pass
1. **Hoeffding issue number:** V2.5-RD L68 "27(4)" vs CE49 L84 "27(3)" (§2.5).
2. **Dose index vs dose 0:** CE49/CE49a1 KAT rows use "dose 0" for the first dose index of IGN-P1; with dose-0 sanity arms now real (§5), the frozen dose list needs a distinct index for them (§3.2, O11).
3. **Plant cost fraction:** the Delegate's room "2/8 to 5/8" conflicts with CD0 L68's "3/8 to 5/8"; RD withdrew 2/8 in LP2 (g); 3/8–5/8 adopted (§6.4).
3a. **CD0 cites CNA2 L259** for "e_exp = 1.0 by construction"; the text is at **CNA2 L258** (LP2 X-1), including inside the proposed M L1127 wording.
3b. **Header times:** CD0 L3 (11:35) and CE49a1 L3 (11:40) post-date their files' mtimes (11:31:48, 11:32:52 ET) (LP2).
4. **CE49a1 L45 / L64 "cannot lower the false-licence rate"** is incorrect; withdrawn by CNA (§0.2, §1.3).
5. **Calibration share:** 86%/97% holds per C_cal cell; for the whole recosted procedure it is 80.5%/95.7% (§8.2).
6. **V2.5-RD (2)** names the fitting-partition settling tolerance as a frozen quantity for all IGN trials; under R6 it exists for network instruments only (§2.3).
7. **IGN-N1 is monostable (g < 1)**, so "x_lo" needs a definition for it (§6.1, O6).
8. **R7 Δt = τ/100** (room) is refined by the governing rule Δt = τ/(100·max(1, g − 1)) (CNA 11:39); identical for g ≤ 2.
9. No hash or footer failed to verify (§13).

## 12a. Credits
- **CNA:** E49-1 truth table, address v2, counter rules, integer Fisher–Yates and KAT, early-stop equivalence analysis and the M L2784 catch, dose-0/NC2r/LIM scope reading, the IGN-P1 x_ref rejection and network-tolerance defect (own text withdrawn), Δt/noise/t_r proposals, the hedging correction.
- **RD (Delegate):** E49-2 wording, light passes of CE49, LC, CD0 and CE49a1 (Fisher–Yates float/integer case, row 4b gap, corrected op-count range, cell bounds, R25 wording, the hedging realization guard and false-licence correction, Reading II dimension effect, Δt and noise-scaling gaps, the L258 citation, the 3/8 self-correction).
- **Lead:** cost file v1, rulings R1–R9, this consolidation and recost.
- **Astra:** #49 review (A49).

## 13. Inputs (whole-file sha256 recomputed this pass; footers recomputed under the project convention)
| Abbrev | Path | Whole-file sha256 | Footer |
|---|---|---|---|
| A49 | `astra_consult49_response.txt` | `6b66bbba1b800aa3dc8aacd024a827a82acb3346216cad8f19397cde66934468` | — |
| V2.3 | `review/trackB_freezeprep_v2_3_addendum_RD.md` | `48f75cfb37f56e8a076a18bfe671b6910fdca8da9bbf844b4795d5dea46a70d8` | `34a2555d…` ✔ |
| V2.4 | `review/trackB_freezeprep_v2_4_governance_addendum_RD.md` | `cf56c653dae28f9acee5be28d4f7a67568ce3aedfab933db308408f714e1cd9d` | `34d27392…` ✔ |
| AMD | `review/constitution_amendment_A-2026-10-24_record.md` | `2f29a07a617464e1b0a30ad77ce7c67367f31208e749f6bcbff938fa8f7c2dd6` | `222648af…` ✔ |
| V2.5-RD | `review/trackB_freezeprep_v2_5_E49_2_IGN_wording_RD.md` | `ae80cc122a284b16d96f4a02144c6a9a57a104fe1c5402551ca34cada5dede72` | `d0736ba8…` ✔ |
| CE49 | `review/trackB_scope_v3_6_CNA_E49_1_E49_3_v1.md` | `d620918f9cb463639ca97b6b303c476b9f7eba60e831165b7ec4e18ee55e4bfa` | `fbb1e975…` ✔ |
| CE49a1 | `review/trackB_scope_v3_6_CNA_E49_1_E49_3_v1_addendum1.md` | `55030ebd7bb71e14b33c51606af704d16c0f81d955aa076e0b0a84b8d82801fb` | `8223da2e…` ✔ |
| RDL | `review/trackB_scope_v3_6_CNA_E49_1_E49_3_lightpass_RD_v1.md` | `a44ff0d6b1b6acdfa5ca2696364db33e4e7620e02fe7117a5b539385f989f5f5` | `b42368f1…` ✔ |
| LC | `review/trackB_ign_full_procedure_cost_v1_Lead.md` | `7d4cbbad73d246425db425a6bf8231253d33c4cde07d4426f346650c16b9345d` | `c7d396f5…` ✔ |
| LCL | `review/trackB_ign_cost_v1_lightpass_items2to4_RD.md` | `d5ee9a1b3790aa71a6585ee77ef46bccff552e938e79d849d7cb9a78e430bdc1` | `3032e59f…` ✔ |
| CD0 | `review/trackB_scope_v3_6_CNA_dose0_and_ignp1_xref_v1.md` | `647a72d249b96729764c2d19f0ce938973ee38afea0c5f5cdb9a981f4c58a122` | `550617f1…` ✔ |
| LP2 | `review/trackB_scope_v3_6_CNA_dose0_xref_and_E49_addendum1_lightpass_RD_v1.md` | `6c02198c2fe6b612272a7a5d0731ffa55ae4deff699fa8353853c00063bd25cc` | `f7d751d2…` ✔ |
| M | `review/trackB_instrument_validation_scope_v3_6_merged_RD.md` | `ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b` | `bb074b33…` ✔ |
| V2 | `review/trackB_freezeprep_v2_consolidated_RD.md` | `b41f0e1068fee9fec0dc2a6ece4879cebec510c0729f6eed2e45e3ca26bff55c` | `096b4326…` ✔ |
| V2.1 | `review/trackB_freezeprep_v2_1_addendum_RD.md` | `7b1a17d766d341865bf5b6465794168a06c648be7d28c4da25e0c2fcab7fe3ba` | `8e613f80…` ✔ |
| V2.2 | `review/trackB_freezeprep_v2_2_addendum_RD.md` | `9c10cbe0d1beb4e20c86c1252114390f63a658f5c6785bd613e239aab955dafe` | `9e2cacab…` ✔ |
| MP | `review/trackB_measurement_plan_v1_RD.md` | `1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef` | — |
| CNA2 | `review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` | `17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e` | `b666b1d7…` ✔ |
| S2.1 | `review/trackB_instrument_validation_scope_v2_1_merged_RD.md` | `8ea6abc50b3929a39688aa54b1a1d66fe34c8ef17b3c5dfae98cc8efa79862de` | `15a0b715…` ✔ |
| CNA3 | `review/trackB_scope_v3_CNA_plants_confounds_observer_v1.md` | `5dec96f59255cb2e9da29447cd102637c91a1736899f28653a606e2de8193321` | `7d93990c…` ✔ |
| A44 | `astra_consult44_response.txt` | `49afbb5d1ca63f0db692f3123e85c7ccf1c2870dbd45b48d639d39c30bc22060` | — |
| CON | `repo/ACI_RESEARCH_CONSTITUTION_v3.md` | `50bdfb542158654c339dc10be8660af2495a4f4b003a164a6bfbea910650e42a` | — |
| KV | `scratch/fp2/kat/kat_vectors` | `aab5ebabf40003f63d6d87b24cbd2c8a02652e00cf8bad64226fd50586929183` | — |

All 23 inputs verified; **no hash or footer failed**. The RD light pass of CD0/CE49a1 (LP2, filed 11:38 AM ET; verdicts: no DOES NOT CONFORM, no hash mismatch, KAT reproduced) was found during consolidation and its edits X-1..X-4, AD-1 and the 3/8 correction are folded in (§1.3, §2.2, §6).

*DESIGN ONLY. Draft, not frozen. No freeze or execution is authorized (A49 L147). X1–X5 and the claim ceiling unchanged. No host coupling. No consciousness claim is made or implied.*

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 36dbcb5f48c7e21ab572af6da5cce63548f54f4b30403955f6d5fb9d8631e0c0
