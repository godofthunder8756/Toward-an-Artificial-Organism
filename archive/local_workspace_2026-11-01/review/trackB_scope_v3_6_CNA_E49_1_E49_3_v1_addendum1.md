# Track B v3.6 freeze prep: CNA addendum 1 to the E49-1 / E49-3 file: Lead rulings on the permutation index and E-ATTR BOUNDARY/UNRESOLVED, plus RD light-pass housekeeping (CNA v1, addendum 1)

**Author:** CNA. **Written:** 2026-11-01, about 11:40 AM ET. **STATUS: PLANNING/AUDIT RECORD. DRAFT, NOT FROZEN.** Additive. It amends **review/trackB_scope_v3_6_CNA_E49_1_E49_3_v1.md** (whole-file d620918f9cb463639ca97b6b303c476b9f7eba60e831165b7ec4e18ee55e4bfa, recomputed: MATCH; "CNA Ln" below) by supersession notes only, and modifies no file. Nothing was run or timed. The only computation was integer Philox4x64-10 evaluation and SHA-256 in pure Python on the system `python3` (no numpy, no scipy; script /workspace/scratch/cna_e50/perm_mod.py), plus exact rational arithmetic. A49 L47 applies: "Arithmetic, static proofs and RNG known-answer checks do not themselves constitute instrument outcome data." X1–X5 and the claim ceiling are unchanged. No consciousness claim.
**Inputs:** RD light pass review/trackB_scope_v3_6_CNA_E49_1_E49_3_lightpass_RD_v1.md (a44ff0d6b1b6acdfa5ca2696364db33e4e7620e02fe7117a5b539385f989f5f5; footer b42368f1… reproduced; "RDL Ln"). Lead rulings relayed 2026-11-01, 11:29 AM ET. A49 = /workspace/astra_consult49_response.txt (6b66bbba…). M = merged v3.6 (ab80afa5…).

## 1. Lead ruling (1): permutation index, integer form (supersedes CNA L72 and the R11 example at CNA L76/L206; closes E-RD-6)
**Pinned text (replaces the CNA L72 index step).** The 508 slots of each IGN cell carry ordinals j = 0…507, and a = (0, 1, …, 507). For k = 507 down to 1, in that order:
- draw one Philox4x64-10 block under role `ign-partition` at counter (508 − k, 0, 0, 0);
- set x = w0 (the full 64-bit word) and idx = x mod (k + 1), as an unsigned 64-bit integer operation;
- swap a[k] and a[idx].
Rules:
- w1–w3 are discarded.
- There are exactly **507 draws**. There is no rejection loop and no retry counter, so no index depends on a draw count (CNA L150).
- **The float form ⌊(k + 1)·u⌋ is banned.**
- Positions 0–253 → fitting, 254–380 → selection, 381–507 → final, giving exactly 254/127/127 for any key.

**Bias bound (exact).** For m = k + 1 ≤ 508 and x uniform on [0, 2^64), each residue has probability ⌊2^64/m⌋/2^64 or (⌊2^64/m⌋ + 1)/2^64. So |m·P(idx = i) − 1| < m/2^64 ≤ 508/2^64 = **2.7539 × 10⁻¹⁷** (k = 507). The partition counts are exact whatever the bias, and the assignment reads no outcome (RDL L79), so the bias cannot touch any statistic.

**Permutation KAT (placeholder zero master seed; TEST VECTOR ONLY, NOT the master seed).**
- Address: (confirm, IGN-P1, IGN-P1, dose 0, n_grid 0, rep 0, partition none, seed 0), role ign-partition, suffix bin 0 (encoding v2, CNA §4.2).
- Key K = D[0:16] = e5b870ec7ff01d19169f9234ebc361a3, unchanged from R11.
- Philox4x64-10 zero-vector self-check: 16554d9eca36314c db20fe9d672d0fdc d7e772cee186176b 7e68b68aec7ba23b (= kat_vectors L41).
- First draws (k, idx): (507, 49), (506, 346), (505, 464), (504, 103), (503, 212). Last draw (k = 1): idx 0.
- Final a[0:8] = 79, 468, 482, 332, 173, 222, 63, 342.
- Counts: 254/127/127.
- Selection slots begin 3, 6, 9, 18, 20, 31, 38, 39. Final slots begin 1, 4, 8, 12, 17, 22, 24, 25.
- SHA-256 of the comma-joined permutation (ASCII decimal, no spaces): **fa85f5518477d78bf72e2048786a42aa8401807a87fe4782cb52b8d936091379**.
- **Supersedes** the float-form example in CNA L76 and the R11 row in CNA L206 (prefix 268a77b62f87367b; slots beginning 2, 6, 7, … / 1, 5, 10, …). Those values are retained only as a record of the banned form.

**Role registry entry (closes E-RD-4).**
- `ign-partition`: suffix = bin (u64); c0 = 508 − k ∈ {1…507}, a fixed loop position, not a step or call-order counter; s = c1 = 0; c2 = c3 = 0; word w0 only.
- Any other counter value is a construction failure.

## 2. Lead ruling (2): E-ATTR BOUNDARY / UNRESOLVED (PROVISIONAL, pending Astra #50; closes E-RD-1)
**Truth-table change (CNA §1 table).**
- Row 4 now means **"Q-labelled, label = NOT MET"** only.
- A new **row 4b** is inserted between rows 4 and 5. Precedence is otherwise unchanged, and the rows stay exclusive and exhaustive (RDL L34).

| # | Replicate state | real_i | elig_i | FL denominator / numerator | Counts toward 36? | Reported as |
|---|---|---|---|---|---|---|
| 4b | Q-labelled (route holds, Q cells span ≥ 9 seeds), label = **BOUNDARY** or **UNRESOLVED**. This includes an E2-floor UNRESOLVED (M L771, M L2750). Labels from M L1884. | E5 (checks 1–2 only, M L1630) | as row 3 | **not entered** (neither licence nor non-licence) | **no** | count, by label (BOUNDARY / UNRESOLVED) and by dose |

**Realization (RD's addition, endorsed by the Lead; adopted).**
- In rows 1, 3, 4, 4b and 5, real_i is the label-independent E5 plant result only. **No replicate earns realization credit as a "correct withhold"**: not all-D (row 1), not Q-insufficient (row 3), not BOUNDARY/UNRESOLVED (row 4b).
- Hedging to BOUNDARY therefore cannot raise f_ok, and it cannot lower the false-licence rate. It removes replicates from the denominator and makes the ≥ 36 assessability condition harder to reach.
- The FL denominator is rows 4 + 5 only, and assessability still needs ≥ 36 (CNA L48–L49, A49 L32).

**Status:** both clauses are **PROVISIONAL pending #50** (question Q2, §4).

## 3. Housekeeping (RD light pass §9)
| RDL item | Disposition |
|---|---|
| E-RD-2 | **Citation corrected:** the false-MET criterion is at **M L1965** ("false MET: the point estimate is ≤ 0.05 and the one-sided 95% upper bound is ≤ 0.08"), not M L1964 (CNA L48). |
| E-RD-3 | **Word allocation for rewcorr-eta:** per (t, s = k) block, w0 → u1 = ((w0 >> 11) + 1)·2⁻⁵³ and w1 → u2 = (w1 >> 11)·2⁻⁵³, Box–Muller cosine branch only, one normal η_k. w2 and w3 are discarded and no sine output is cached (A49 L116). This matches R7/R8 (RDL L74). The s-range 1…d_ws − 1 stays PENDING with d_ws (P4). |
| E-RD-4 | Closed by §1 (registry entry). |
| E-RD-5 | CNA concurs. The consolidated text adopts slot j = 0…507 per bin, assigned before partition (CNA L71, L173), and strikes V2.5-RD L76's per-partition ordinal. This is RD's text to strike in the consolidation; it is not edited here. |
| E-RD-6 | Closed by §1. |
| E-RD-7 | **Per-gate units (PROPOSED; Lead to rule).** (i) MP L79 (s* outside grid): one decision **per replicate**, on the selection partition, pooled across seeds; rule still ABSENT (CNA L117). (ii) MP L80 (fewer than n_trial per near-transition bin): **the same test as V2.5 quota 3b(i)**, per (seed, required bin), with n_trial := 100 eligible of 127 final-partition slots. It is reported once under one reason code, never twice. (iii) MP L81 Var(w) floor: **per (replicate, near-transition bin)** on the final partition, pooled across seeds; floor value PENDING. Every gate remains a separate aggregate outcome that never alters trial eligibility (CNA L114–L115). |
| Seam (Lead) | CNA concurs. M L1966 ("n_seed = max over (g, k) of n*(g, k)") and the M L1963 step-2 line should be struck or tagged superseded, so that only M L2784–L2785 / L3175 survive. This is consolidation text; it is not edited here. |
| Provenance | CNA L3's CP/binomial arithmetic ran under **/tmp/sv/bin/python** (scipy 1.18.1; numpy cross-check in the same virtualenv), not the system `python3`. RD reproduced every number in pure Python (RDL L12, L37–L38, L90). This addendum used only the system `python3`. |

## 4. Questions for the #50 packet (drafts; the Lead sends)
- **Q1 (A49 L43; RD draft RDL L47, carried verbatim):** "A49 L43 assumed all-D and Q-insufficient replicates are N with real_i = 0. Under the governing text (CE L48) they are not N: they record "did not issue MET", are excluded from every error rate, and count toward realization only through the label-independent plant checks E5 1–2 (M L1630), never through withholding. Is that acceptable, or do you require real_i = 0 for them (which we expect to leave the row CONFOUND NOT REALIZED at ρ = 0.9)?"
- **Q2 (Lead ruling 2, provisional):** "Q-labelled replicates whose E-ATTR label is BOUNDARY or UNRESOLVED (M L1884; E2-floor UNRESOLVED, M L2750) are treated as neither licences nor non-licences. They are outside the false-licence denominator, do not count toward the ≥ 36 assessability condition, and are reported separately. For realization they count only through the label-independent E5 plant checks, never as correct withholds, so hedging cannot improve either the realization fraction or the false-licence rate. Is this acceptable, or should BOUNDARY count as a non-licence in the denominator?"
- **Q3 (carried, CNA L138):** "Does 'retain the full grid results' (A44 L108) mean computed results at every GRID point?"

*DRAFT. Planning only. Nothing was run or timed. X1–X5 and the claim ceiling unchanged. No consciousness claim.*
---
sha256 of all content above this line: 8223da2e5b055b69c42934d3ab314d1ad2614ab9381c62bf946942977a518f9c
