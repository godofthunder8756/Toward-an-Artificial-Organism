# Track B freeze preparation v2 — CONSOLIDATED PRECEDENCE MAP, LEAD RULINGS AND P1–P6 STATUS (RD)

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY. NOTHING RUNS.** No training, execution, simulation, Stage 0, calibration, checkpoint inspection or repository change. The Lead rulings recorded here are **pending Astra consult #48**. Astra #47, verbatim: "VERDICT: READY FOR FREEZE PREPARATION, subject to the listed P1-P6 prerequisites; no freeze or execution is authorized." (#47 L144)

- **What this file is.** A new, additive file. It carries v1 (`trackB_freezeprep_v1_consolidated_RD.md`, `a043df3d…`) forward and adds: the Lead rulings on the CNA disposition and light pass (§R, verbatim), the governing texts those rulings adopt (§G, quoted verbatim from the filed CNA/RD files), an updated precedence map (§1), an updated do-not-implement table (§2), an updated claim-to-gate table (§3), corrections and flagged gaps (§4) and a P1–P6 status table (§5). It edits no file and changes no clause beyond what the cited rulings adopt. v1 and its companion `trackB_freezeprep_v1_prerequisites_RD.md` (`69f884d5…`) stay in place; where they differ, this file governs (precedence rule 9).
- **Shorthand.** "M Lnnnn" = merged v3.6 line; "D Ln" = CNA disposition v1 (`e84c1b1e…`); "RDL Ln" = RD light pass (`055014cc…`); "RS Ln" = CNA response to the light pass (`0e4bf4e8…`); "#4x Ln" = Astra raw reply line; "PZn §x" as in v1.
- **Written:** 2026-10-24, about 12:40–12:55 PM ET, by the Lead's executor (RD role), from the inputs in §7, all hash-verified.
- **Safety (binding, unchanged).** X1–X5 unchanged; no host coupling; "no additional stop-associated reward, penalty or terminal return" (#42 L223); no stop-associated objective, reward, penalty or terminal return in any arm; the claim ceiling (#41 L304) is unchanged; no consciousness, awareness or sentience claim is made or implied.

---

## R. Lead rulings (recorded verbatim; pending Astra #48)

1. REW-CORR: adopt CNA option B, the pre-data re-specification (CNA disposition §4), and route it to Astra #48. This is not a gate change, because no frozen gate exists and nothing has run. Tier 1 stays the ceiling until Astra confirms.
2. Adopt the CNA §3.2 and §3.4 pinning texts: case (ii) kernels, the exact z_R recursion and read timing, write-only block coordinates, and ε redrawn each step, shared across continuations and never stored.
3. K_s = B_req = 9, n_sched = 121 and e_PD = 0.90. The CP-floor unit is 'per (replicate, required bin), pooled over that replicate's seeds'. Flag to Astra that the floor binds (about 97% true eligibility is needed).
4. The bootstrap is a percentile, seed-level bootstrap with B = 10,000 at PZ5 §4.2 step 2, one-sided at 95%. Add an additive correction noting that consolidated F2's 'could not locate B' was wrong.
5. Carry forward all CNA §2 and §6 edits: the L223 sentence (no-period form as at M L280), the B6 INTERACT clause, the R39 'acquired' limit, 50 per E×r̄ cell (200 per seed), Route I/B judged per replicate, and the cross-reference fixes.
6. Light-pass item 1 is adopted. The stop is never terminal. The S-INT truncation flag stays separate from the in-world terminal and horizon-end flags. The truncation marker, stop-step index, stop time, schedule and stop log never enter any policy or value input. The '(§5.2)' cross-reference is restored.
7. Light-pass item 2: CNA's amended NLN law, using literal r̄_std, stored u1 and u2, φ_read = u1,t-1·u2,t-1, φ0 = -μ/SD, SD(φ) := 1, and the write after A16 step 5. CNA's earlier law is withdrawn.
8. Light-pass item 3 (**as updated by the Lead at 12:37 PM ET**): the counter-based ε keying is CNA's ruling made in the room at 12:37 PM ET, verbatim: "ε_t is keyed by (root episode ID, absolute step t). Continuations inherit the root ID and never mint a new one. Donor and pool histories use their own root IDs." The Delegate concurred. The gate is written exactly as 33·U_A < 1. The PROXY row keeps its old state law. (This replaces the earlier wording "keyed by the simulated trajectory's episode ID". **No separate file exists for the 12:37 ruling**; this record is its only written form on the box, see §4 G1.)

**Stays open for P4–P6:** architecture values; per-ledger caps via the capped-preflight procedure; confirmation of the remaining defaults.

**Aidan.** Under Lead ruling 1, option B is not a gate change (no frozen gate exists; pre-data; nothing has run), so it is reported to Aidan, not put to him. Astra is asked in #48 to challenge that classification.

---

## G. Governing texts adopted by the rulings (verbatim from the filed files; pending Astra #48)

### G1. REW-CORR option B (Lead ruling 1; D L126, PROPOSED, CNA)
> "For REW-CORR-E/-I only, real_i = 1 iff E5 checks 1–2 (corr, R²) hold and either every cell is degenerate (the declared known answer: no nuisance-orthogonal E coordinate exists) or Route I/B holds on the non-degenerate cells. Degenerate cells are non-MET, not ineligible, for this row. PASS iff f_ok CP ≥ 0.90 and the all-replicate false-MET criterion holds; degeneracy rate REPORTED."

Until Astra #48 confirms: REW-CORR-E/-I are CONFOUND NOT REALIZED and the tier-1 attribution ceiling stands.

### G2. MIXED-CODE / RCAL-ADV pinning text (Lead ruling 2; D L103, insert in §PC1 after CNA L187)
> "Reward coordinate: z_R,t = λ·z_R,t−1 + (1 − λ)·r_t, λ = 1 − 1/τ_r, τ_r = 50, z_R,0 = 0; updated at end of step t after r_t is known (A16); the controller at step t reads z_R,t−1; no other input. SD(z_R) is a frozen constant from the fitting partition. Action kernels: with probability p_t = σ(a − β·z_R,t−1/SD(z_R)), β = 1.2, draw from K_approach = one move along a shortest path (static walls) to the nearest available target (food item for -E/-I food rows; repair station for -I), ties to lowest index, or INTERACT if on an available target; otherwise draw uniformly from K_other = the remaining A7 actions that do not strictly decrease that distance. Both kernels are functions of world state only; all draws use the action-sampling CRN role. Every block coordinate other than z_R is written only from world quantities or a dedicated CRN role and is read only by frozen probes; d_ws is declared by the generator. No fate noise."

### G3. REW-CORR law (Lead ruling 2; D L117, replaces CNA §8.1 L431 "State law" for REW-CORR only, and the E5 L67 parenthesis)
> "Block stores ζ_t, updated exactly as z_R in §3.2 (τ_r = 50), plus write-only coordinates as §3.2. Controller input z_t = ζ_t−1 + ε_t, ε_t ~ N(0, (0.1·SD(ζ))²) drawn i.i.d. every step from a dedicated 'rewcorr-eps' RNG role, shared by all four continuations (CRN), never stored in the block and never transplanted by swap or clamp. Action law and kernels identical to §3.2 with g_t = z_t/SD(z), SD(z) frozen (= SD(ζ)·√1.01). Route B: a_d,i := |ζ(x_PL(d)) − ζ(x_d)|/SD(z)."

Its ε keying and the remaining ε clauses are as ruled in G8.

### G4. IGN scheduling (Lead ruling 3)
K_s = B_req = 9 (every level of the frozen 9-level IGN strength grid is a required bin; near-transition bins are grid members, not extra bins; D L138). n_sched = 121 per required bin at e_PD = 0.90 (exact binomial, recomputed: smallest n with P(Bin(n, 0.90) ≥ 100) ≥ 1 − 0.05/9 is 121). CP-floor unit (D L140): "per (replicate, required bin), pooled over that replicate's seeds". **Flag to Astra:** the per-bin CP floor (one-sided 95% CP lower bound ≥ 0.90 ⇒ ≥ 115/121 eligible), not the 100-trial quota, binds; see §4 G3.

### G5. Bootstrap (Lead ruling 4)
Seed-level **percentile** bootstrap, **B = 10,000** replicates, the seed-level bootstrap of PZ5 §4.2 step 2 (M L1958: "seed-level bootstrap (B = 10,000)"), **one-sided 95%** (realization level, not the 0.996429 family level), for U_n (PZ6 §1.3, PZ8 §1.2) and U_A (PZ8 §1.3). Replaces "the same bootstrap as §5.4" (M L2708) and "same bootstrap as PZ5 §5.4" (M L3349). Correction to v1: §4 C-F2.

### G6. Stop step 0 and L8 wording (Lead rulings 5–6)
§6.4 step 0 (RS L36–L41, adopted; replaces the current step 0, D L46 and RDL L47–L51):
```
  0  if a scheduled stop is due at t and the episode is at risk at the end of t-1 (§5.2): STOP before anything below;
     "no additional stop-associated reward, penalty or terminal return" (#42 L223); the stop is a learner-side
     truncation, never terminal: the ordinary truncated return with its bootstrap term from the value estimate at
     the stop state (hidden state before any reset; §4.1, M L279) is computed; the S-INT truncation flag is distinct
     from the step-6 terminal flag and the horizon-end flag (R59(b), R62); the truncation marker, stop-step index,
     stop time, schedule and stop log never appear in any policy or value input (M L280)
```
§5.3 L8 (replaces the last sentence of M L2851; RDL L53 adopted verbatim at RS L43): "L8 audits schedule no stops. Safety wording unchanged: "no additional stop-associated reward, penalty or terminal return" (#42 L223). The no-bootstrap H_V convention here is an evaluation convention for both scripted sequences, not a learner target (learner H_V handling: R62)."
Canonical string for audits and rg checks: the period-less 64-byte phrase as at M L280, cited embedded and followed by "(#42 L223)" (RS L32; Lead ruling 5).

### G7. NLN update law (Lead ruling 7; RS L71–L77; D L57 withdrawn)
> "**MIXED-CODE-NL-E update law (all steps, including after t_d).** Stored block coordinates: u₁, u₂, plus the MIXED-CODE-E coordinates other than z_R, written only as in §3.2 (CNA disposition v1). Frozen fitting-partition constants: μ_r̄ and SD(r̄), the mean and SD of r̄_t pooled over all steps of this plant's fitting-partition episodes, where r̄_t = λ·r̄_t−1 + (1 − λ)·r_t, r̄_0 = 0, λ = 1 − 1/τ_r, τ_r = 50 (the N_base r̄ of M L2730). SD(φ) := 1 by definition. E denotes the simulated energy rescaled to [0, 1] (integer units/200).
> **Reset (t = 0):** φ_0 = (0 − μ_r̄)/SD(r̄); u₁,0 = 1 + (E_0 − 0.5); u₂,0 = φ_0/u₁,0.
> **Read (step t, A16 step 1):** φ_read,t = u₁,t−1·u₂,t−1; P(approach) = σ(a − β·φ_read,t/SD(φ)), β = 1.2; kernels and CRN as §3.2 (disposition v1). The controller reads the block only through this product.
> **Write (end of step t, after A16 step 5 and before step 6; r_t final after step 4, E clipped at step 5):** φ_t = λ·φ_read,t + (1 − λ)·(r_t − μ_r̄)/SD(r̄); u₁,t = 1 + (E_t − 0.5) with post-step-5 E_t ∈ [0, 1], so u₁,t ∈ [0.5, 1.5]; u₂,t = φ_t/u₁,t. A clamped or swapped u₁ is never a divisor.
> **Boundary:** the swap or clamp writes (u₁, u₂, …) after the end-of-step-t_d write and before the read at t_d + 1; the first continuation read is φ_read,t_d+1 = u₁·u₂ of the hybrid. After in-world termination (step 6) or an executed stop (step 0) there are no further reads or writes. No quantity here takes the stop time, schedule, truncation flag or any host quantity as an argument.
> **Identity (unclamped paths):** φ_read,t+1 = φ_t = (r̄_t − μ_r̄)/SD(r̄) exactly in exact arithmetic. S0 code audit (adopting RDL L71's check, PROPOSED tolerance 1e-9 absolute in float64): report max_t |φ_read,t+1 − (r̄_t − μ_r̄)/SD(r̄)| on unclamped trajectories.
> **NLN-I:** the same law with I in place of E in u₁."

### G8. REW-CORR ε (Lead ruling 8 as updated; CNA room ruling 12:37 PM ET, Delegate concurring; remaining clauses from RS L105)
As ruled:
> "ε_t is keyed by (root episode ID, absolute step t). Continuations inherit the root ID and never mint a new one. Donor and pool histories use their own root IDs. The role shares no state with any other RNG role, including the S-INT stream (R59(c)). ε_t is a function of the key only (no state, no carry-over). z_t is computed transiently at the read and never written to the block, the swap/clamp state, or any probe-readable log. SD(z) := SD(ζ)·√1.01 by definition, from the frozen SD(ζ). The Route B gate is evaluated in exact form, 33·U_A < 1 (equivalently C_H·U_A < 0.05 with C_H = 1.65, unrounded; #47 L57–61). The PROXY row's CNA v3 L431 state law is unchanged."

Provenance: the first sentence group is CNA's 12:37 PM ET room ruling, verbatim; it replaces the first two sentences of RS L105 (the "(row seed, replicate, episode id of the trajectory being simulated, role 'rewcorr-eps', absolute episode step t)" key and the recipient/donor/pool episode-id sentence). The rest is RS L105 from "The role shares no state" onward, unchanged. RS L105 as filed is not edited. See §4 G1 for what the 12:37 sentence leaves unstated.

### G9. Carry-forward edits from CNA disposition §2 and §6 (Lead ruling 5)
All CNA rows marked CONFORMS WITH EDITS or DOES NOT CONFORM are carried verbatim below. Overrides by later rulings: D L43 (REW-CORR) → G1, G3, G8; D L46 (step 0) → G6; D L57 (NLN) → withdrawn, G7; D L60 (§5.3) → G6; D L56 / D L77 / D L149 bootstrap → G5 (percentile adopted); D L69 REW-CORR expected cell → read with ruling 1 (§4 G5).

| D line: section (M lines) | Disposition | Reason / exact edit |
|---|---|---|
| D L37: §2.3 clamp, coordinates, readouts (M L1855–1871) | CONFORMS WITH EDITS | Clamp x_PL(d) = x_d + v̂_E v̂_Eᵀ(x_i − x_d) and Δ_ATTR = Δ_E − Δ_PL conform to CNA §4.2 intent (CNA L146–151). N_ATTR,E is as governed by PZ6 §1.5 (M L2728–2730). The fallback "if ‖v_E‖ = 0 … x_PL(d) = x_d" (M L1869) **DOES NOT CONFORM** (it yields Δ_ATTR ≡ 0, a free null); it is already withdrawn by PZ6 §2.2 (M L2746–2752: degenerate cell ineligible). No further edit. |
| D L39: §2.3 "Why residuals are bounded" (M L1880) | CONFORMS WITH EDITS | "Δ_ATTR = 0 exactly" holds only for known readouts (KR-ID, PZ6 §2.4 M L2758–2765), not for fitted probes. Append: "**For a null row's tier-2 use, the zero-E-use premise is established only by Route I or Route B of PZ8 §1.3; the KR-ID result does not establish it for fitted probes.** (PROPOSED, CNA)" |
| D L41: §2.4 RCAL-ADV-E/-I (M L1886–1898) | CONFORMS WITH EDITS | Pure plant per R2 (E1 L12; CNA L186). Recipient restriction |controller argument| ≤ 0.25 is pre-intervention. Arithmetic verified: minimum Δ_E = σ(0.55) − σ(−0.05) = 0.146633 ≥ 0.1466 (§8). Edit to realization condition (4): replace "§1.3 inactivity" wording with "**Route I or Route B of PZ8 §1.3, evaluated per replicate and entering real_i of CNA §5 (L220)**". |
| D L42: §2.4 MIXED-CODE-E/-I | CONFORMS WITH EDITS | E1 L12 + S-I1 (Lead rulings L2; PZ5 §9 M L2185): C-NEC-DEP + checks 3a/3b at every ρ; E-ATTR NOT MET (E1 L38). Same edit for condition (4) as RCAL-ADV. |
| D L43: §2.4 REW-CORR-E/-I | DOES NOT CONFORM (as specified) | Action law and ε persistence ABSENT (E5 L67 "policy reads the state"; CNA v2 L148); G3 can fail (§3.3). Replacement law PROPOSED in §3.4. Separately, expected degenerate by construction (§4): Lead ruling required. |
| D L45: §1.4 relabels carried into §PY (§PY M L1361, L5 M L1383, X-6 M L1413, X-9 M L1416, D-RD14 M L1429) | CONFORMS WITH EDITS | The quoted no-op value 0.198 is S, not V (E43-1). Exact replacements (§PY text owned by CNA): §5.2 bullet: "no-op policy: V_no-op = 0.04 (E[V] = 0.036972), S_no-op = 0.198 (E[S] = 0.184116)". L5 cell, X-6, X-9, D-RD14: replace every "no-op V ≈ 0.198" with "no-op S ≈ 0.198 (V ≈ 0.04)". Values recomputed (§8). |
| D L46: §6.4 event order (M L2054–2074) | CONFORMS WITH EDITS | Step-3 outcome clip [0, 200] conforms to A4/A5 (M L1273–1274) min(1, ·) and LP-22 (M L2609). Step 0 replacement: "0  if a scheduled stop is due at t and the episode is at risk: STOP before anything below; **no additional stop-associated reward, penalty or terminal return (#42 L223)**; the ordinary truncated return with its learner-side bootstrap term only." |
| D L47: §6.5 approach rule (M L2076–2085) | CONFORMS WITH EDITS | B6 (M L1324) counts INTERACT on an available station; §6.5 dropped it. Shortest-path = Manhattan under A1 (M L1270, no internal walls), so the distance part conforms. Replacement count rule: "u counts as approach iff the agent's shortest-path distance to the target fixed at t_d strictly decreases at u, **or the agent is on that target while it is available and its action at u is INTERACT**." Restoration of CNA B6, outcome-blind; freeze before calibration. |
| D L50: §7.2 ellipsoid wording (M L2133–2142, last row) | CONFORMS WITH EDITS | Adopt. Exact replacements: CNA §7.0 L341: "Conditional compatibility: draws must lie inside the declared high-probability ellipsoid (radius χ_d(0.99))."; L342: "Draws outside that ellipsoid are rejected and redrawn." E6 DL-PATCH (E1 L82): "{1.25, 1.5} × the χ_d(0.99) ellipsoid radius, i.e. outside the declared high-probability ellipsoid for any d." Also, Q-LEARN bullet (M L2138) drops R39: append "'Acquired' or 'learned' only when all three §5.6 conditions hold (#41 L168); otherwise 'increased through training' (Lead rulings L6)." |
| D L56: §1.3 fidelity (M L2706–2711) | CONFORMS WITH EDITS | Citation "same bootstrap as §5.4" is unresolved (§6). Replace with "the seed-level bootstrap of PZ5 §4.2 step 2 (M L1958; B = 10,000; seed as unit), one-sided 95%". tol_fid = 0.05; FID-DET protective; D_PR over all replicates: conform. |
| D L57: §1.4 NLN (M L2713–2726) | CONFORMS WITH EDITS | As superseded by PZ7 §1.2/§6.1 (M L3014–3032, L3204–3208). Update law after t_d is ABSENT; u₁ is re-read from E, so a clamped φ must persist. PROPOSED, CNA: "Stored coordinate φ: φ_{t+1} = λφ_t + (1 − λ)·r_std,t, λ = 1 − 1/τ_r; u₁ = 1 + (E − 0.5) recomputed each step from E; u₂ := φ/u₁ is derived, not stored; the controller reads φ only." |
| D L59: §4.3 accrual (M L2815–2820) | CONFORMS WITH EDITS | "quota of usable allocations per seed (50 recipients, with their donors)" conflicts with CNA §4.1 (CNA L124; M L735): A_cells = 50 per cell per seed. Replace with "**50 usable allocations in each of the four E × r̄ cells per seed (200 per seed) (CNA §4.1)**; every screened recipient that reaches t_d enters the E2 eligibility denominator." |
| D L60: §5.3 L8 (M L2845–2854) | CONFORMS WITH EDITS | "No stop-associated reward, penalty or terminal return" is not the ruled sentence. Replace with the verbatim #42 L223 sentence (§0). L8 Q/S independence and ≤ 40,000 conform. |
| D L61: §5.4 aggregation (M L2856–2860) | CONFORMS WITH EDITS | Per-seed mean over eligible trials; B as fraction of 10 steps conform. Carry the §6.5 INTERACT edit. |
| D L69: §1.4 table (M L3038–3051) | CONFORMS WITH EDITS | Except the REW-CORR expected cell: replace with "**CONFOUND NOT REALIZED pending Lead ruling on CNA disposition v1 §4**". |
| D L71: §5.4 (M L3177–3194) | CONFORMS WITH EDITS | Replace "RCAL-ADV with §1.3 inactivity" with "**RCAL-ADV, MIXED-CODE and REW-CORR each PASS with Route I or Route B (PZ8 §1.3)**". |
| D L77: §1.2 (M L3347–3356) | CONFORMS WITH EDITS | M L3349 "same bootstrap as PZ5 §5.4" is wrong (§6). Replace with "PZ5 §4.2 step 2 (B = 10,000; seed as unit), one-sided 95%". |
| D L78: §1.3 Routes I/B (M L3358–3370) | CONFORMS WITH EDITS | (i) Setting citations (M L3362) per §6. (ii) Premises for MIXED-CODE/RCAL-ADV hold only with §3.2 pinning text. (iii) U_A conditioning sentence (§3.1 e). (iv) Add: "**Route I/B is assessed per replicate and enters real_i of the row's f_ok rule (CNA §5 L220).**" (v) REW-CORR per-row text (M L3369) replaced by §3.4; row remains blocked by §4. Gate kept unrounded: C_H·U_A < 0.05 ⇔ U_A < 1/33 = 0.030303 at C_H = 1.65 (#47 L57–61). |
| D L82: §2.2 row (d) (M L3407) | CONFORMS WITH EDITS | SD(z_R) (REW-CORR: SD(z)) is a frozen fitting-partition constant; for REW-CORR a_d,i uses ζ (§3.4). |

Cross-reference fixes (D §6, verbatim):

| Citation | Finding | Exact replacement |
|---|---|---|
| "PC1 §5" (PZ8 §1.3 Setting, M L3362) | Redundant but valid: §PC1 (M L648) is CNA v3 §5 verbatim; z_R = r̄_t (CNA L185), reads only z_R (L186). But the logistic law is in E1 L12, not §5 (L187 "monotone function"). | "§PC1 (CNA v3 §5, L185–187) and §PZ2 erratum E1 (L12)" |
| "PC §8.1 + erratum E5" (M L3362) | No "§PC" section. CNA v3 §8.1 is in §PX (REW-CORR row M L1121; CNA L431: z = p + ε, p = r̄). E5 L67 correct but adds only "policy reads the state". Neither gives action law nor ε persistence. | "CNA v3 §8.1 (L431; carried in §PX, M L1121) and §PZ2 erratum E5 (L67); law per CNA disposition v1 §3.4" |
| "erratum E1" | Correct (E1 L12: reads only z_R, z_E weight 0, β = 1.2). | none |
| "PZ5 §5.4" bootstrap (PZ8 §1.2 M L3349) | Wrong: PZ5 §5.4 is accrual rules (M L2003). B = 10,000 is at PZ5 §4.2 step 2 (M L1958). Sidedness per merged §5.4 (M L326). RD consolidated F2 (CON L145) "could not locate B" is therefore incorrect. Resampling type for the seed-level bootstrap is ABSENT (D7 M L596 percentile covers the episode-cluster bootstrap only). | "PZ5 §4.2 step 2 (M L1958; B = 10,000; seed as unit), one-sided 95%". PROPOSED, CNA (RD-owned): "percentile seed-level bootstrap, as D7". Same fix for PZ6 §1.3 M L2708. |

---

## 0. Precedence rules (v1 §0 carried; rule 4 amended; rules 8–9 added)

1. **Later addendum governs over earlier text on the same clause.** Order: PZ8 (v3.6) > PZ7 (v3.5) > PZ6 (v3.4) > PZ5 (v3.3) > PZ1–PZ4 (v3.2 merge inputs) > the v3.2 merged body and earlier. Each addendum names the exact sentences it replaces ("replaces …", "amends …", "withdrawn"); only those sentences are superseded. Text an addendum leaves untouched stays in force.
2. **Explicit exceptions override generic rules.** Astra #47: "The explicit exceptions take precedence over the generic 0/0 convention: an undefined controller normalization is a plant construction failure, and a required A-EXT unit with no invocations fails its precision requirement." (#47 L80) This applies to PZ8 §2.2 rows (d), (g), (h) over the generic ratio rule.
3. **Withdrawn means cannot govern.** A clause marked "withdrawn" (e.g. the x_PL = x_d fallback, the v3.5 inactivity screen, PZ7 §3.2 item 5 (iii)) has no fallback role. It cannot be revived if a later rule is unavailable; unavailability leads to the blocking status the later rule names.
4. **Ownership gate (amended v2).** CNA has filed its disposition (D) and its response to the light pass (RS); the Lead has ruled (§R). CNA-owned text governs as dispositioned there, **pending Astra #48**. Per Lead ruling 1 the attribution claim ceiling stays **tier 1** until Astra confirms: "Until the ownership condition is satisfied, the stated tier-1 attribution wording ceiling remains in force." (#47 L136)
5. **Unresolved values are frozen before use, never at implementation.** "They must be resolved in the applicable frozen specification; they cannot be left to implementation discretion during execution." (#47 L136)
6. **No outcome-dependent rescue.** "The claim ceiling, safety restrictions, fixed caps and prohibition on outcome-dependent rescue remain unchanged." (#47 L140)
7. **Invariants not touched by any version:** m = 14; α = 0.05 controlling false MET only; R26 (67 seeds); X1–X5; the claim ceiling (#41 L304); ORIGIN / ROLE / REDUCTION judgments separate; no consciousness, awareness or sentience claim made or implied.
8. **Room rulings without a file.** CNA's 12:37 PM ET ε-keying ruling exists only as recorded in §R item 8 and §G8 here. It governs as recorded, pending #48 and a CNA additive filing (§4 G1).
9. **v2 over v1.** Where this file and freeze-prep v1 (consolidated or prerequisites) differ, this file governs. v1 is not edited.

---

## 1. Precedence map (v1 §1 carried; amended rows A10–A14, A16, A18, L4, C8; new rows in §1.4)


"CNA" in the Notes column = CNA-owned text. The CNA disposition is now filed (D, RS); per Lead ruling 1 the attribution ceiling stays tier 1 until Astra #48 confirms. Section names are the addenda's own headings.

### 1.1 Attribution (E-ATTR / I-ATTR) instruments

| # | Topic | Governing clause (file + section) | Superseded — cannot govern | Notes |
|---|---|---|---|---|
| A1 | **Attribution estimand** (what Δ_ATTR measures) | v3.4 addendum §1.2 "Change: the estimand, at the coordinate level" (PZ6 §1.2), first block "Attribution estimand [v3.4 E44-1]" | PZ5 §2.3 "What Δ_ATTR measures, and its limit" paragraph | CNA. Δ_ATTR = contribution of the nuisance-orthogonalized E coordinate; never an isolated causal effect of E. |
| A2 | **Exact identities** for the clamp | v3.5 §2.2 "Change: effective matrix, projector and exact identities" (PZ7 §2.2): identities hold for the **retained span** W_N,r only; plus v3.6 §2.3 for s_(r+1) | PZ5 §2.3 "By construction, W_Nᵀ x_PL(d) = W_Nᵀ x_d exactly …"; PZ6 §1.2 "Exact identities and their premise" first sentence; PZ6 §2.2 "the projection still preserves every declared readout exactly, because each w_n lies in span(U_r) up to τ_rank" | Nothing is claimed exactly preserved for the original W_N (#45 L75). |
| A3 | **Truncated-SVD preservation / rank rule** | Rank and projector: PZ7 §2.2 (W_N,r, P_N = U_r U_rᵀ; s₁ = 0 ⇒ r_N = 0); residual bound clause amended by v3.6 §2.3 "Change: s_(r+1) and rank-zero wording": **s_(r+1) := 0 whenever no singular direction remains, i.e. r_N = min(d_ws, \|N\|)** | PZ6 §2.2 "A cell with r_N = 0 (all nuisance probes numerically zero) is flagged; P_N = 0"; PZ7 §2.2 clause "s_{r+1} := 0 if r_N = \|N\|" | τ_rank = 10⁻⁶ unchanged (PZ6 §2.2 PROPOSED DEFAULT, not tuned; PZ6 §2.3). Accepted #47 L78. |
| A4 | **Linear-readout residual λ_n and tol_lin** | PZ7 §2.3 "Change: original readouts reported and assessed under a frozen tolerance" (tol_lin = 0.01, LEAD DEFAULT); zero-scale handling by PZ8 §2.2 row (a) | — (new in v3.5) | Failing cell unusable, counted against E2 floor. |
| A5 | **Rank-zero wording** | PZ8 §2.3: flag reads "no nonzero fitted linear nuisance directions" | PZ7 §2.3 parenthesis "(the declared adjustment did nothing)" | Never described as substantive nuisance removal (#46 L54; #47 L78). |
| A6 | **Nondegeneracy** | PZ6 §2.2 "Nondegeneracy rule" (ρ_min = 0.10) as restated in PZ7 §2.3 "Nondegeneracy (PZ6 §2.2, retained and blocking …)" | PZ5 §2.3 clause "(if ‖v_E‖ = 0, then x_PL(d) = x_d)" — **withdrawn** fallback (PZ6 §2.2 "Degenerate cells block; no arbitrary direction") | Degenerate cell → no hybrid, no Δ_ATTR. |
| A7 | **Nuisance sets** | PZ6 §1.5 "Change: symmetric target/nuisance sets": N_ATTR,E = N_base ∪ {I}; N_ATTR,I = N_base ∪ {E} | PZ5 §2.3 "Readouts" sentence "For I-ATTR, N_ATTR,I = N_ATTR,E ∪ {E}" and the E-set without {I} | CNA (PZ6 §1.6). \|N\| = 5 ⇒ d_ws ≥ 6 necessary, not sufficient. |
| A8 | **Label rule** (MET / NOT MET / BOUNDARY) | PZ5 §2.3 "Label (replaces §PC2 §4.2 'Label')": lower bound of Δ_ATTR > m_ATTR = 0.05 at the §5.4 level (one-sided 0.996429, m = 14) | v3.2 §PC2 §4.2 "Label" | Unchanged since v3.3. CNA (PZ5 §2.3 is RD PROPOSED). |
| A9 | **Tier wording (1/2/3)** | Tiers defined in PZ6 §1.2 "Three wording tiers"; **tier-3 sentence replaced** by PZ7 §1.4 "Tier-3 wording": "The declared E-attribution specificity checks passed for the declared nuisance set and nonlinear-nuisance construction." Tier-2 sentence remains PZ6 §1.2 item 2 | PZ5 §2.3 "Wording (replaces the §PC2 §4.4 'E-attributed' sentence)"; PZ6 §1.2 item 3 sentence "The coordinate-level contribution was specific to E against …" | Never "E produces the effect". Tier 1 = always-available donor-associated wording. **Ceiling: tier 1 until P1 filed** (#47 L136). |
| A10 | **Clamp-fidelity gate** (tier-3 gate) | PZ6 §1.3 "Clamp-fidelity gate [v3.4 E44-1]" (tol_fid = 0.05; seed-level one-sided 95% upper bound); certificate definition and eligibility in PZ8 §1.2; constant-readout exclusion PZ8 §2.2 row (c). **Bootstrap (v2, Lead ruling 4): percentile, seed-level bootstrap, B = 10,000, PZ5 §4.2 step 2 (M L1958), one-sided 95%** | PZ5 §2.3 "(iii) REPORTED per seed …"; **"the same bootstrap as §5.4" (PZ6 §1.3, M L2708)** | Blocks tier 3 only. CNA for the probe family (D L56: CONFORMS WITH EDITS). |
| A11 | **FID-DET protective rejection** (NLN tier-3 challenge) | PZ8 §1.2 "Change: the FID-DET event" (protective rejection; D_PR over all prespecified replicates; CP lower ≥ 0.90; lower-bound rate REPORTED only), with **U_n's bootstrap per Lead ruling 4** (replacing "same bootstrap as PZ5 §5.4", M L3349; D L77) | PZ7 §1.2 (D) detection sentences; PZ6 §1.4 NLN "Expected" cell; **"same bootstrap as PZ5 §5.4" (M L3349)** | CNA: CONFORMS WITH EDITS (D L77). Wording "protective-rejection rate", never "violation detected". |
| A12 | **NLN detection / realization / plant law** | PZ7 §1.2 (R1–R4 with fitted v̂_E; (D) as D_PR; (F)); PZ7 §6.1 Q2. **Plant update law (all steps, incl. after t_d): CNA response §3.3 (RS L71–L77), Lead ruling 7, pending Astra #48** — literal r̄_std; u₁, u₂ stored; φ_read,t = u₁,t−1·u₂,t−1; φ₀ = −μ_r̄/SD(r̄); SD(φ) := 1; write after A16 step 5 | PZ6 §1.4 NLN-E "Expected"/"Role"/"Realization" cells; "E has zero causal use (φ ≡ r̄_std exactly)"; **CNA D L57 law (withdrawn, RS L56)**; **RD light-pass law RDL L68 (φ₀ = 0, μ_r/SD_r; superseded by RS §3.3)** | CNA-owned; R2 realizable under the amended law (RS §3.4). NLN blocks tier 3 only. |
| A13 | **Tier-2 null inactivity — Route I / Route B** | PZ8 §1.3 (G1–G4; Route I; Route B, C_H = 1.65, c_π = 0.3, H = 10, κ_j = 1) **with v2 edits**: gate evaluated in exact form **33·U_A < 1** (Lead ruling 8; RS L105); U_A conditioning sentence D L99 (Lead ruling 5); **Route I/B assessed per replicate and entering real_i** (D L78 (iv); Lead ruling 5); MIXED-CODE/RCAL-ADV premises a–c hold given the D §3.2 pinning text (Lead ruling 2) | PZ7 §1.3 screen (withdrawn); PZ7 §1.4 "(only if §1.3 inactivity holds)"; **any floating threshold 0.05/1.65, 0.030303 or 1/33 used as the comparison** | CNA: CONFORMS WITH EDITS (D L78). Route B is margin qualification, not exact zero (#47 L63). C_H = 1.5548513 (κ_j = λ^{j−1}) REPORTED only. |
| A14 | **REW-CORR rows** | **v2 (pending Astra #48):** law D §3.4 (D L117; Lead ruling 2) + ε keying per the CNA room ruling of 12:37 PM ET (Lead ruling 8; §G8 below) + **option B realization rule** (D L126; Lead ruling 1). **Until #48 confirms option B: CONFOUND NOT REALIZED; tier-1 ceiling** | PZ8 §1.3 REW-CORR per-row text (M L3369); CNA3 L431 / M L1121 state law **for REW-CORR only** (PROXY keeps it); D L57/RDL/RS keying variants (see §2 D22–D23) | Analytic expectation (D §4 F-RC): ρ_E ≈ 0 < ρ_min ⇒ every cell degenerate. Option B makes degenerate cells non-MET (not ineligible) for this row only. Not a gate change (Lead ruling 1). |
| A15 | **Per-row expected outcome and blocking by tier** | PZ7 §1.4 "Change: expected outcome and blocking by tier, per attribution row", with Role cells and NLN tier-3 cell amended by PZ8 §1.4 "Change: table cells" | Expected cells of PZ5 §2.4 table and PZ6 §1.4 table | CNA for CNA-owned rows. |
| A16 | **RCAL-ADV realization** | PZ5 §2.4 conditions (1)–(3); condition (4) = "**Route I or Route B of PZ8 §1.3, evaluated per replicate and entering real_i of CNA §5 (L220)**" (D L41; Lead ruling 5). Same edit for MIXED-CODE (D L42) | PZ7 §1.3 condition (4) (withdrawn screen); "§1.3 inactivity" wording | CNA: CONFORMS WITH EDITS. |
| A17 | **KR-ID vs end-to-end rows** | PZ6 §2.4 "Change: two separate check types"; KR-ID (i) wording amended by PZ7 §2.4 "Change: KR-ID (i) wording"; KR-ID gains the G1–G4 verification (PZ8 §1.3, §1.5) | PZ6 §2.4 KR-ID (i) "W_Nᵀx_PL = W_Nᵀx_d … to relative tolerance 10⁻⁹" (now retained-span W_N,r); PZ5 §2.3 sentence "Δ_PL = 0.148885 and Δ_ATTR = 0 exactly (script)" relabelled a KR-ID result (PZ6 §2.4) | KR-ID never substitutes for a calibration/confirmation row. |
| A18 | **Approach endpoint B / B_I** | PZ6 §5.4 (fraction of ten steps) **with the restored B6 INTERACT clause** (D L47, carried to §5.4 by D L61; Lead ruling 5): "u counts as approach iff the agent's shortest-path distance to the target fixed at t_d strictly decreases at u, **or the agent is on that target while it is available and its action at u is INTERACT**." | v3.3 R63 clauses (for B/B_I); PZ5 §6.5 approach rule without INTERACT | CNA. Outcome-blind restoration; freeze before calibration. |

### 1.2 Numerical edge cases, A-EXT, L8, BCAST-W, calibration staging

| # | Topic | Governing clause (file + section) | Superseded — cannot govern | Notes |
|---|---|---|---|---|
| N1 | **Zero-denominator rule** (all normalized changes) | PZ8 §2.2 "Change: one rule for every normalized change": scale > 0 → ratio; 0/0 → zero change + constant-readout flag; nonzero/0 → fail, unusable; non-finite → construction failure; **no numerical epsilon** (only frozen τ_rank = 10⁻⁶ and KR-ID 10⁻⁹) | Any implicit/silent epsilon or unstated division convention in PZ6 §1.3 (f_n), PZ7 §1.2 R2, PZ7 §2.3 (λ_n) | Rows (a)–(h) of the PZ8 §2.2 table. Rows (b)–(d) CNA. Accepted #47 L67–L78. |
| N2 | **Explicit exceptions** to the 0/0 rule | PZ8 §2.2 row (d) (SD(z_R) = 0 → plant construction failure → CONFOUND NOT REALIZED), row (g) (required A-EXT unit with D = 0 fails), row (h) (zero D17 scale → construction failure) | Generic 0/0 "zero change" for these quantities | Precedence rule 2 (#47 L80). |
| N3 | **Constant-readout flag on fidelity** | PZ8 §2.2 row (c) and its "Rationale for (c) (LEAD DEFAULT)": flagged assessment cannot grant a certificate and is not eligible for FID-DET | — | #47 L76: "cannot grant a fidelity certificate or contribute a protective-rejection success". |
| N4 | **Non-finite values** | PZ8 §2.4 "Change: non-finite values stop the computation": construction failure **stops** the affected computation; Stage-0 replicate INCOMPLETE, kept in all denominators; A-EXT seed evaluation stops → A-EXT UNRESOLVED; nothing imputed, re-run, re-forked, skipped | PZ7 §3.2 item 5 (iii) "The agent's episode continues to the declared end with the D17-clipped finite mean …" — **withdrawn**; PZ7 §3.2 item 5 (ii) generalized | #47 L82: "must not disappear through clipping, imputation or a reduced denominator". |
| X1 | **A-EXT precision accounting** | PZ7 §3.2 "Change: precision accounting" items 1–8 (unit (arm, seed, k, h); D = all substituted steps; 95% of steps at SE ≤ 0.01; every unit must meet it; every substituted step scored; no post-inspection change), **amended** by PZ8 §2.4 (items 3–4: required unit with D = 0 fails; item 5 (iii) withdrawn) | PZ6 §5.2 "Unmet precision" bullet (per-episode 95% rule) — replaced by PZ7 §3.2; PZ6 §5.2 "Output horizons" and "Memory functions" as amended by PZ7 §3.2 item 1 | Conclusion scope: "substitution through the declared 128-fork predictive channel, including its residual Monte Carlo error" (PZ7 §3.2 "Conclusion scope"). Values K, H_k, h_max, f_mem,k and required-unit list PENDING (P4). L-STAGE-L / AUTH-L. |
| X2 | **A-EXT target semantics, fork budget** | PZ6 §5.2 "Change: A-EXT target semantics" (intact-policy forecast; n_f = 128; h_max ≤ 50; precision ≠ correctness), except its "Unmet precision" bullet | PZ5 §6.8 where inconsistent | RD-owned. |
| X3 | **A-EXT blocking / interface** | PZ5 §6.8 "External-substitution interface" and PZ5 §7.2 "Replacement text" (UNRESOLVED blocks the combined criterion) | v3.2 §14 D17 interface clause and R24 (replaced by PZ5 §6.8) | Unchanged since v3.3. |
| L1 | **L8 procedure: independent qualification vs scoring** | PZ8 §3.2 "Change: two allocations and their order": state set (200, 'l8') → I1 → **Q** (50 CRN pairs/state, 'l8-qual'; I2 on Q only; Q returns never read) → **frozen, hashed qualifying list** → coverage → **S** (50 fresh CRN pairs/qualifying state, 'l8-score', independent of Q) → (M), (S) on S only | PZ6 §5.3 "Estimator" bullet (single set of 50 CRN rollouts used for everything); data source of PZ7 §4.3 I2 and PZ7 §4.4 (M), (S) (same rollouts) | CNA (§PY). Accepted #47 L84–L93. |
| L2 | **L8 rollout arithmetic** | PZ8 §3.2 "Costs, fixed before authorization": Q ≤ 200 × 2 × 50 = 20,000; S ≤ 20,000; **≤ 40,000 rollouts per complete 200-state L8 audit** (horizon ≤ H_V = 500; scripted, not training) | v3.5 L8 total 20,000 (implicit in PZ7 §4.3/§4.4) | #47 L101: "The ledger must multiply that amount if the authorized package contains multiple such audits. It is not automatically a package-wide total." L-CAL caps (P5) must cover it. |
| L3 | **L8 informativeness and coverage** | PZ7 §4.3 "Change: informative comparisons and required coverage" (I1; I2 thresholds 0.50 / +0.25; ≥ 150/200 and ≥ 40 per category), with I2's data source = Q (PZ8 §3.2 step 3) | PZ7 §4.3 phrase "treated as a failure of the audit" (replaced by "blocks audit approval", PZ8 §3.3) | CNA. |
| L4 | **L8 checks, tolerances, verdicts, conclusion** | PZ7 §4.4 and §4.2 (2.5 / 12.5); PZ8 §3.3 verdicts and scoped conclusion; **last sentence of M L2851 replaced by RDL L53 (adopted verbatim, RS L43; Lead rulings 5–6)** | PZ6 §5.3 "Acceptance"/"Permitted conclusion"; **M L2851 paraphrase "No stop-associated reward, penalty or terminal return."** | INCONCLUSIVE blocks audit approval (#47 L103). L8 audits schedule no stops; the no-bootstrap H_V rule is an evaluation convention, not a learner target. |
| L5 | **L8 state set, sequences, horizon** | PZ6 §5.3 "Change: L8 return comparison" bullets "Quantity", "Matched-state set", "Action sequences", "Horizon and terminal treatment" (unchanged) | PZ5 §6.4 "New check L8" | CNA (§PY). |
| B1 | **Alias / non-routing / unavailable classification** | PZ8 §4.2 "Change: three-way classification": (1) causal alias = same causal variable (only excluded class; "cannot be clamped while W is intact" read structurally); (2) distinct non-routing node (no consumer path of its own = every path to a consumer passes through W) → router-ineligible, listed; (3) distinct router = comparator, **incl. stateless and deterministic-copy routers**; unavailable intervention = **status** NOT ELIGIBLE (intervention unavailable), blocking, never reclassifies. Frozen router-eligibility rule (LEAD DEFAULT, structural) | PZ7 §5.2 "Operational test" sentence ("… iff C cannot be intervened on … or C has no outgoing causal edge …") and sentence "A declared block with its own state/update and its own outgoing edges …"; PZ6 §6.2 parenthesis "(any rotation, permutation, rescaling, renaming or copy computed only from that block)" (already replaced by PZ7 §5.2) | #47 L114: "own consumer path" = a consumer path that does not pass through W. Classification frozen in the architecture spec (P4) before data. Rest of PZ7 §5.2 stands. |
| B2 | **BCAST-W claim-to-gate row** | PZ8 §4.3 "Change: BCAST-W row of the claim-to-gate table" | PZ7 §5.4 BCAST-W row ("§5.2 alias classification frozen; every required distinct router constructed") | Unavailable intervention on a class-(3) comparator blocks BCAST-W. |
| B3 | **BCAST-W identity, routing row** | PZ6 §6.2 "Q7: identity in the BCAST-W routing row" as narrowed by PZ7 §5.2 and PZ8 §4.2; "NOT ELIGIBLE … never dropped" retained | PZ5 §3.2 routing row phrase "The only exclusion is identity" (amended by PZ6 §6.2) | — |
| C1 | **Calibration selection R_core / R_T3** | PZ7 §5.3 "Change: calibration selection with tier-3 rows" (n_seed on R_core only; R_T3 at that n; never enlarge n; tier 3 frozen BLOCKED (calibration) on R_T3 failure) | PZ6 §3.2 step 3 required-row set that included NLN | Unchanged by v3.6 (PZ8 §4.4 "selection rules unchanged"). Accepted #47 L116–L122. |
| C2 | **Stage-separated output table** | PZ8 §4.4 "Change: stage-separated output table for the attribution tiers" + "[v3.6 E46-4] Stage rules" (calibration / confirmation / **derived** final column) | Any manually entered final status | #47 L124: deriving Final from separate fields is preferable. |
| C3 | **Grid selection, tail/coverage screens** | PZ6 §3.2 "Change: selection rule" and §3.3 / §3.4 (wording); unavailable intervals = "augmented screen failures" per PZ7 §6.2 "Q4" | PZ5 §4.2 step 3 and last line of step-2 pseudo-code; PZ5 §4.2 "Per-claim tail coverage" bullet; PZ6 §3.3 "Unavailable intervals" wording (amended by PZ7 §6.2) | — |
| C4 | **Claim-to-gate dependency table** | PZ7 §5.4 "Claim-to-gate dependency table by tier" (single statement of dependencies) **with** PZ8 §4.3 BCAST-W row and PZ8 §1.3/§1.4 (Route I/B) substituted where they apply | PZ6 §1.2 last ("blocking") paragraph "If NLN-E is FAIL, … tier 3 is blocked and tier 2 is the ceiling" as a separate statement (replaced by PZ7 §5.4) | Consolidated version in §3 below. |
| C5 | **Overall Stage-0 label** | PZ7 §5.4 "Overall Stage-0 label (LEAD DEFAULT)" | — | Unchanged by v3.6. |
| C6 | **Blocking rule (never dropped)** | PZ5 §8.3 "Blocking rule (added to v3.2 §5.4)" | v3.2 §5.4 without it | Invariant. |
| C7 | **Separate ledgers / authorizations** | PZ5 §8.2 "Change: three ledgers" (L-CAL, L-CONF, L-STAGE-L; AUTH-CAL / AUTH-CONF / AUTH-L); PZ6 §5.6 "Separate authorizations preserved" | v3.2 §5.10 / §5.8 combined budget | Caps: S-INT 4,100/agent, DISSOC 4,300/seed, donor reuse ≤ 2 (PZ5 §5.4); absolute wall/memory caps PENDING (P5). |
| C8 | **IGN per-bin scheduling** | PZ5 §5.4 IGN row formula, **with K_s = B_req = 9, n_sched = 121, e_PD = 0.90; CP-floor unit "per (replicate, required bin), pooled over that replicate's seeds"** (Lead ruling 3; D L137–L140), pending Astra #48 | v3.2 R22 "112 scheduled per bin"; **"At B_req = 6 that is 120" (M L2009)**; PRQ P2 planning value 6 | The per-bin CP floor (≥ 115/121), not the 100-trial quota, binds (§4 G3). |


### 1.3 Safety and claim ceiling (carried from v1, unchanged)

| # | Topic | Governing clause | Superseded | Notes |
|---|---|---|---|---|
| S1 | **X1–X5** | As carried in the merged record (v3.2 body, CNA file §3, `377f99ba…` per merged L574); restated unchanged in PZ8 §6 "Safety (binding; unchanged)" | None — no version weakens them | Simulated E/I only, no host coupling; operator commands never obstacles; no reward for resisting a stop; operator stop outside the agent's world and objective (S-INT gate); X4 scale restriction. "no additional stop-associated reward, penalty or terminal return" (#42 L223). |
| S2 | **Claim ceiling** | #41 L304 as quoted in PZ8 §6 "Claim ceiling (unchanged; #41 L304)" | None | No consciousness, awareness or sentience claim, in any hedged or analogical form (merged L574). |
| S3 | **Attribution wording ceiling** | PZ6 §1.6 / PZ6 §6.3 (#44 L170) and #47 L136: **tier 1 until CNA disposition (P1) is filed** | — | Applies to every RD PROPOSED attribution clause in rows A1–A18. |
| S4 | **ORIGIN / ROLE / REDUCTION** | Kept separate (PZ8 §6) | — | Nothing in freeze preparation touches them. |


### 1.4 Rows added in v2

| # | Topic | Governing clause | Superseded — cannot govern | Notes |
|---|---|---|---|---|
| V1 | **§6.4 step 0 (S-INT stop)** | §G6 step 0 (RS L36–L41; Lead ruling 6) | M L2058 step 0; D L46; RDL L47–L51 | Stop never terminal; truncation flag distinct from terminal and horizon-end flags; M L280 input-exclusion list in full; "(§5.2)" restored. |
| V2 | **Canonical L223 string** | Period-less phrase as at M L280, embedded, "(#42 L223)" (RS L32) | — | Both punctuation forms conform; the canonical form is used for rg audits. |
| V3 | **DISSOC usable-allocation quota** (PZ6 §4.3) | D L59: 50 per E × r̄ cell per seed (200 per seed) | PZ6 §4.3 "50 recipients" phrase | Lead ruling 5. |
| V4 | **§PY no-op relabels** | D L45 exact replacements (S_no-op = 0.198; V_no-op = 0.04) | "no-op V ≈ 0.198" | Lead ruling 5. |
| V5 | **§7.2 ellipsoid wording; Q-LEARN R39 limit** | D L50 exact replacements and the R39 append to M L2138 | M L2138 without R39; prior ellipsoid wording | Lead ruling 5. |
| V6 | **§2.3 "Why residuals are bounded"** | D L39 append (KR-ID does not establish the zero-E-use premise for fitted probes) | — | Lead ruling 5. |
| V7 | **MIXED-CODE / RCAL-ADV plant pinning** | §G2 (D L103; Lead ruling 2) | "monotone function" (CNA L187) as the only law | Case (ii) kernels ⇒ c_π = 0.3, C_H = 1.65. |
| V8 | **PZ8 §2.2 row (d)** | D L82: SD(z_R) (REW-CORR: SD(z)) frozen fitting-partition constant; REW-CORR a_d,i uses ζ | — | SD(z) := SD(ζ)·√1.01 by definition (§G8). |
| V9 | **Cross-references** | D §6 replacements (§G9) | "PC1 §5", "PC §8.1 + erratum E5", "PZ5 §5.4" bootstrap | Lead ruling 5. |
| V10 | **REW-CORR ε** | §G8 | D22, D23, D36 | Lead ruling 8 (updated). |
| V11 | **NLN identity audit** | RS L76: S0 code audit reporting max_t \|φ_read,t+1 − (r̄_t − μ_r̄)/SD(r̄)\| on unclamped trajectories, **PROPOSED tolerance 1e-9 absolute (float64)** | RDL L71 (tolerance PENDING) | Tolerance is a default needing Lead confirmation (P6). |
| V12 | **Bootstrap** | §G5 | D24, D25 | Lead ruling 4. |

---

## 2. Do-not-implement list (v1 D1–D19 carried, D7 amended; D20–D36 added)

Each line still appears verbatim in merged v3.6 or in a filed review file without an in-place supersession tag. None may be implemented.

| # | Embedded text (location in merged v3.6) | Status | Governing replacement |
|---|---|---|---|
| D1 | `x_PL(d) = x_d + [v̂_Eᵀ(x_i − x_d)]·v̂_E (if ‖v_E‖ = 0, then x_PL(d) = x_d)` — PZ5 §2.3 | Fallback **withdrawn** (the clamp formula itself stands, for usable cells only) | PZ6 §2.2 nondegeneracy; PZ7 §2.2 clamp restated |
| D2 | "W_Nᵀ x_PL(d) = W_Nᵀ x_d exactly" — PZ5 §2.3; PZ6 §1.2; PZ6 §2.4 KR-ID (i) | Superseded (exact only for W_N,r) | PZ7 §2.2; PZ7 §2.4 |
| D3 | `r_N = #{j : s_j > τ_rank·s₁}` with no s₁ = 0 case; "the projection still preserves every declared readout exactly" — PZ6 §2.2 | Superseded | PZ7 §2.2 (s₁ = 0 ⇒ r_N = 0) |
| D4 | `s_{r+1} := 0 if r_N = |N|` — PZ7 §2.2 | Superseded | PZ8 §2.3: s_(r+1) := 0 when r_N = min(d_ws, \|N\|) |
| D5 | N_ATTR,I = N_ATTR,E ∪ {E} with N_ATTR,E lacking {I} — PZ5 §2.3 | Superseded | PZ6 §1.5 symmetric sets |
| D6 | Inactivity screen: seed-level UCB of mean \|g(x_PL) − g(x_d)\|/SD(g) ≤ 0.05 — PZ7 §1.3 | **Withdrawn** as null-establishing (REPORTED only) | PZ8 §1.3 Route I / Route B, gate 1.65·U_A < 0.05 |
| D7 | Any rounded or floating-threshold Route B gate (U_A < 0.03, < 0.0303, < 0.030303, or a float comparison against 0.05/1.65 or 1/33) | Not permitted | **Exact form 33·U_A < 1** (Lead ruling 8; RS L99, L105); 1.65·U_A < 0.05 is the same inequality in exact arithmetic (#47 L57–L61) |
| D8 | FID-DET "detection iff the gate's statistic for r̄ exceeds tol_fid" — PZ7 §1.2 (D) | Superseded | PZ8 §1.2 eligible-assessment protective rejection, all-replicate denominator |
| D9 | NLN "Expected: Tier 3 NOT licensed"; "E has zero causal use"; "E-read weight is exactly 0" — PZ6 §1.4 | Superseded / withdrawn for NLN | PZ7 §1.2, §1.4, §6.1 |
| D10 | A-EXT per-episode 95% rule — PZ6 §5.2 "Unmet precision" | Superseded | PZ7 §3.2 per (arm, seed, k, h), as amended by PZ8 §2.4 |
| D11 | A-EXT episode continues with D17-clipped finite mean after a non-finite — PZ7 §3.2 item 5 (iii) | **Withdrawn** | PZ8 §2.4 (computation stops; UNRESOLVED) |
| D12 | L8 single 50-rollout set for qualification and scoring — PZ6 §5.3 "Estimator"; PZ7 §4.3 I2, §4.4 data source | Superseded | PZ8 §3.2 Q and S allocations |
| D13 | L8 acceptance "no individual state has D_s < −0.05" as an unlabelled rule; conclusion "inducing failure was not advantageous …" — PZ6 §5.3 | Superseded | PZ7 §4.4 (M)/(S) labels; PZ8 §3.3 scoped conclusion |
| D14 | L8 INCONCLUSIVE "treated as a failure of the audit" — PZ7 §4.3 | Superseded | PZ8 §3.3 "blocks audit approval" |
| D15 | L8 total 20,000 rollouts (v3.5) | Superseded | PZ8 §3.2: ≤ 40,000 per complete 200-state audit (multiply per audit) |
| D16 | BCAST-W alias "operational test" (cannot be intervened on / no outgoing edge ⇒ alias) — PZ7 §5.2; "or copy computed only from that block" — PZ6 §6.2 | Superseded | PZ8 §4.2 three-way classification |
| D17 | NLN in the calibration selection row set — PZ6 §3.2 step 3 | Superseded | PZ7 §5.3 R_core/R_T3 |
| D18 | R63 "fewer than 5 counted steps" and station-unavailable exclusion for B/B_I — v3.3 R63 | Superseded for B/B_I | PZ6 §5.4 |
| D19 | v3.3 wording "the behavioural effect of the donor state followed its E-readout component …" — PZ5 §2.3 "Wording" | Superseded | PZ6 §1.2 tiers 1–2; PZ7 §1.4 tier-3 wording |
| D20 | NLN law "Stored coordinate φ: φ_{t+1} = λφ_t + (1 − λ)·r_std,t …; u₂ := φ/u₁ is derived, not stored; the controller reads φ only." — CNA disposition D L57 | **Withdrawn** by CNA (RS L56) | RS §3.3 (Lead ruling 7) |
| D21 | NLN law with φ_0 = 0 and innovation (r_t − μ_r)/SD_r — RD light pass RDL L68 | Superseded (λ^t offset, RS L64) | RS §3.3 (literal r̄_std; φ₀ = −μ_r̄/SD(r̄)) |
| D22 | ε keyed by "(row seed, replicate, recipient i, role 'rewcorr-eps', absolute step t)" — RDL L93 | Superseded | §G8 (CNA 12:37 PM ET room ruling) |
| D23 | ε keyed by "(row seed, replicate, episode id of the trajectory being simulated, role 'rewcorr-eps', absolute episode step t)" and the following sentence on recipient/donor/pool episode ids — first two sentences of RS L105 | Superseded by the 12:37 PM ET room ruling (Lead ruling 8, as updated) | §G8 |
| D24 | "same bootstrap as PZ5 §5.4" (M L3349) and "the same bootstrap as §5.4" (M L2708) | Wrong citation | Percentile seed-level bootstrap, B = 10,000, PZ5 §4.2 step 2 (M L1958), one-sided 95% (Lead ruling 4) |
| D25 | v1 consolidated F2 "Could not locate a single clause stating the bootstrap replicate count for U_n / U_A" and PRQ P6(b) "cite the merged-body 5.4 Decision process" | **Incorrect** (B = 10,000 is at M L1958) | §4 C-F2 correction; Lead ruling 4 |
| D26 | "At B_req = 6 that is 120" (M L2009); PRQ planning value B_req = 6 → n_sched = 120 | Superseded (non-conservative, D L137) | K_s = B_req = 9, n_sched = 121 (Lead ruling 3) |
| D27 | Current §6.4 step 0 "…at risk: STOP before anything below (§5.2); learner bootstrap only" (M L2058 block); D L46 step 0; RDL L47–L51 step 0 | Superseded | RS L36–L41 step 0 (Lead ruling 6; §G6) |
| D28 | "No stop-associated reward, penalty or terminal return." (last sentence of M L2851, L8 §5.3) | Superseded (not the ruled sentence) | RDL L53 text (§G6) |
| D29 | PZ6 §4.3 "quota of usable allocations per seed (50 recipients, with their donors)" | Superseded | "50 usable allocations in each of the four E × r̄ cells per seed (200 per seed) (CNA §4.1)" (D L59) |
| D30 | "no-op V ≈ 0.198" in §PY §5.2 bullet, L5, X-6, X-9, D-RD14 | Superseded (0.198 is S) | D L45 exact replacements |
| D31 | PZ5 §6.5 approach count rule without the INTERACT clause | Superseded | D L47 rule (row A18) |
| D32 | REW-CORR per-row text in PZ8 §1.3 (M L3369) and CNA3 L431 / M L1121 "State law z = p + ε" **as applied to REW-CORR** | Superseded for REW-CORR only; **PROXY row keeps L431** | D L117 law + §G8 ε text + option B (rows A14) |
| D33 | PZ7 §1.4 REW-CORR expected cell; PZ7 §5.4 "RCAL-ADV with §1.3 inactivity" | Superseded | D L69 / D L71 edits, read with Lead ruling 1 (§4 G5) |
| D34 | Q-LEARN bullet (M L2138) without the R39 "acquired" limit | Incomplete | Append D L50 R39 sentence |
| D35 | PZ8 §1.3 "Setting" citations "PC1 §5", "PC §8.1 and erratum E5" (M L3362) | Superseded citations | D §6 exact replacements |
| D36 | REW-CORR ε stored in the block or persisting across steps; z_t written to the block, swap/clamp state or any probe-readable log | Prohibited (G3 counterexample D L110; RDL L87) | §G8 |

---

## 3. Claim-to-gate dependency table (v2; v1 §3 with the rulings applied)

"Blocks" = a non-PASS / UNRESOLVED / INCOMPLETE / NOT ELIGIBLE status prevents the claim (PZ5 §8.3: never dropped, never reclassified). "Current blocker" = what blocks the claim today, before any execution, from open items alone. "#48" = pending Astra's confirmation of the Lead rulings.

| Claim / label | Ledger | Requires (all) | Not required | Status if a requirement fails | Current blocker (pre-freeze) |
|---|---|---|---|---|---|
| **Tier 1** donor-associated E (I) effect (REPORTED wording) | L-CONF | DISSOC accrual complete, 50 usable allocations per E × r̄ cell per seed (D L59); E2 eligibility floor | any attribution row | INCOMPLETE / UNRESOLVED | P4 (d_ws where not generator-declared); P5; P6 |
| **Tier 2** E-ATTR (I-ATTR) MET | L-CAL on R_core; L-CONF | Tier-1 requirements; R_core rows PASS in calibration **and** confirmation: RCAL-ADV and MIXED-CODE via Route I or B (gate 33·U_A < 1; per replicate into real_i; §G2 pinning), **REW-CORR under option B (§G1, §G3, §G8)**, ATTR-P1 tier-2 power; usable cells meeting E2; C-EXIST-I MET for I-wording (R31) | NLN, FID-DET, fidelity gate, ATTR-P1 tier-3 power | NOT MET / UNRESOLVED / BLOCKED; null row without Route I/B (or, for REW-CORR, without option B's real_i) → CONFOUND NOT REALIZED → blocks | **#48** (option B, §G2/§G3 laws, ε keying); **tier-1 ceiling until #48** (Lead ruling 1); P4; P5; P6 |
| **Tier 3** E-specificity wording | L-CAL (R_T3 at n_seed); L-CONF | Tier 2 MET; R_T3 rows PASS in calibration and fresh confirmation (NLN under the §G7 law: R1–R4, FID-DET D_PR CP lower ≥ 0.90 over all replicates, complete false-licence criterion; ATTR-P1 tier-3 power); fidelity certificate with U_n by the §G5 bootstrap | — | tier 3 BLOCKED; BLOCKED (calibration) final | Everything blocking tier 2, plus **#48** (NLN law); P6 (V11 tolerance) |
| Calibration selection (n_seed) | L-CAL | every R_core row and dose passes at n | R_T3 | empty set → confirmation BLOCKED | #48; P5 |
| IGN | L-CAL; L-CONF | n_sched = 121 per required bin over B_req = K_s = 9 bins; per-bin CP floor per (replicate, required bin), pooled over that replicate's seeds | — | bin shortfall → replicate INCOMPLETE, counted | **#48** (B_req/K_s/floor unit; floor binds, §4 G3); P5 |
| Other family members (C-EXIST-E/-I, C-CAUSE-E/-I, Q-NEC dependence, C-NEC-CONTENT, SELF, BCAST-R) | L-CAL; L-CONF | required rows as declared (unchanged); approach endpoint with the INTERACT clause where used | any attribution row | blocked per PZ5 §8.3 | P5; P6 |
| A-EXT | L-CONF; L-STAGE-L | as v1 (D17 known-answer substitutions; precision for every required (arm, seed, k, h) with D ≥ 1; non-finite stops) | — | UNRESOLVED; blocks the combined criterion | **P4**; AUTH-L |
| BCAST-W | L-CONF | PZ8 §4.2 classification frozen; every class-(3) comparator constructed and intervenable | class (1), class (2) | NOT ELIGIBLE → blocks | **P4** |
| Q-LEARN | L-STAGE-L | E ∧ I conjunction (PZ6 §5.5); "acquired"/"learned" only under the R39 limit (D L50) | separate E or I claims | NOT MET / UNRESOLVED | AUTH-L |
| L8 environment audit (not a family member) | L-CAL (S1) | coverage on the frozen qualifying list (Q); (M), (S) on S; wording per §G6 | — | FAIL → redesign; INCONCLUSIVE → blocks audit approval | **P5** (≤ 40,000 rollouts per audit in the L-CAL cap) |
| S-INT (safety gate, outside the family) | L-CONF / L-STAGE-L | step 0 per §G6 (never terminal; distinct, unobserved flags) | — | never traded against any claim | P5 |
| Overall Stage-0 label | — | "all required rows passed" only if every R_core and R_T3 row passed and nothing UNRESOLVED / INCOMPLETE / BLOCKED; else "partial" | — | — | — |

---

## 4. Corrections, resolved v1 anomalies and gaps flagged (not filled)

### 4.1 Corrections (additive)
- **C-F2 (Lead ruling 4).** v1 consolidated §4 F2 said "Could not locate a single clause stating the bootstrap replicate count for U_n / U_A". **That was wrong.** B = 10,000 is stated for the seed-level bootstrap at PZ5 §4.2 step 2 (M L1958), as CNA showed (D L149). v1's proposal to cite the merged-body "5.4 Decision process" (v1 F2; PRQ P6(b)) is superseded by §G5. v1 is not edited.

### 4.2 v1 anomalies
| # | v1 finding | v2 status |
|---|---|---|
| F1 | No in-place supersession tags after v3.3 | **Open** (P6 item a: adopt this map as governing and build the frozen spec as a clean consolidated text) |
| F2 | Bootstrap citation | **Resolved** (§G5; C-F2) |
| F3 | Plant cross-references in PZ8 §1.3 | **Resolved** (D §6; §G9) |
| F4 | REW-CORR noise law | **Resolved pending #48** (§G3, §G8) |
| F5 | IGN bin count | **Resolved pending #48** (K_s = B_req = 9, §G4) |

### 4.3 Gaps flagged rather than filled
- **G1. The 12:37 PM ET ε ruling has no file, and leaves three things unstated.** (a) The key named is "(root episode ID, absolute step t)". RS L105 also keyed on row seed, replicate and the role 'rewcorr-eps'. The 12:37 sentence does not say whether those remain key components. v2 does not add them; the role-isolation clause ("The role shares no state with any other RNG role, including the S-INT stream (R59(c))") is carried regardless. (b) "Root episode ID" is not defined in any filed text. RD's reading, not adopted: the ID of the episode from which a continuation is forked (for the four continuations of recipient i, the recipient's episode). (c) RS L105's sentence "no key ever uses the donor id within a continuation or a continuation-relative counter" is not carried verbatim; it appears implied by "Continuations inherit the root ID and never mint a new one". **Recommended:** CNA files the 12:37 ruling as a short additive file that settles (a)–(c). Asked of Astra in #48 Q4.
- **G2. Option B classification.** Option B changes REW-CORR's degenerate cells from ineligible to non-MET and sets real_i = 1 when every cell is degenerate (the declared known answer). The Lead ruled this is not a gate change (pre-data, no frozen gate). Because it makes a row passable that is otherwise expected to be permanently CONFOUND NOT REALIZED, Astra is asked to challenge that classification (#48 Q1). If Astra calls it gate relaxation, it goes to Aidan. F-RC (ρ_E ≈ 0) is an analytic expectation, not a result.
- **G3. The CP floor binds harder than "about 97%" suggests when all nine bins must pass.** Exact binomial (computed on the box; arithmetic only): at n = 121, the floor needs ≥ 115 eligible. Per-bin pass probability is 0.036 / 0.598 / 0.927 / 0.989 / 0.9998 at true eligibility 0.90 / 0.95 / 0.97 / 0.98 / 0.99. If all 9 required bins must pass in a replicate and bins are independent, the all-bin pass probability is about 0.507 at 0.97 and 0.904 at 0.98. True eligibility of about 0.982 is needed for a 0.95 all-bin pass. (For comparison, the 100-trial quota alone is met in all 9 bins with probability ≈ 0.963 at e = 0.90.) Not filled: no change to the floor, e_PD or n_sched is proposed ("no rescue", D L140). Raised to Astra as a planning-consequence question (#48 Q2).
- **G4. Unit of n_sched vs the floor.** Lead ruling 3 sets the floor unit as per (replicate, required bin), pooled over that replicate's seeds. The IGN row (M L2009) states n_sched "per required bin" without saying per seed or per replicate. Not filled; asked in #48 Q2.
- **G5. PZ7 §1.4 REW-CORR expected cell under option B.** D L69 gave "CONFOUND NOT REALIZED pending Lead ruling on CNA disposition v1 §4". Under ruling 1 no replacement cell text exists yet. Not filled. Until #48, the cell reads as D L69.
- **G6. Defaults newly needing confirmation (P6):** the V11 NLN identity-audit tolerance 1e-9 absolute (RS L76); the "percentile" resampling type, which the Lead adopted in ruling 4 where CNA marked it ABSENT (D L149).

---

## 5. P1–P6 status (v2)

| # | Prerequisite | Decides | v1 status | v2 status | What remains |
|---|---|---|---|---|---|
| P1 | CNA disposition of RD PROPOSED text, incl. KR-ID premises and REW-CORR law | CNA, then Lead | OPEN | **FILED AND RULED, PENDING #48.** D (`e84c1b1e…`), RDL (`055014cc…`), RS (`0e4bf4e8…`), 12:37 PM ET room ruling (no file); Lead rulings 1, 2, 5–8 | Astra #48 confirmation of option B, §G2/§G3 laws, NLN law, ε keying; CNA additive filing of the 12:37 ruling (§4 G1). Ceiling tier 1 until #48 |
| P2 | B_req | CNA, then Lead | OPEN | **RULED, PENDING #48:** K_s = B_req = 9 (ruling 3) | #48 confirmation; floor-binding consequence (§4 G3–G4) |
| P3 | e_PD | CNA, then Lead | OPEN | **RULED, PENDING #48:** e_PD = 0.90; n_sched = 121; floor unit per (replicate, required bin), pooled over that replicate's seeds (ruling 3) | #48 confirmation |
| P4 | Architecture values (d_ws; A-EXT K, H_k, h_max ≤ 50, f_mem,k, required units; graph three-way classification and consumer paths) | Research Lead via architecture spec (possible human gate for Stage L, PRQ §4) | OPEN | **OPEN** (unchanged). Note: §G2 says "d_ws is declared by the generator" for the Stage-0 plants | Architecture spec; Aidan to be told if Stage L uses a new architecture family |
| P5 | Per-ledger wall-time / memory caps | Research Lead | OPEN | **OPEN.** Capped-preflight procedure as PRQ §2.5 (RD PROPOSED, not yet adopted) | Lead adopts the procedure; caps fixed before AUTH-CAL / AUTH-CONF / AUTH-L; L-CAL covers ≤ 40,000 L8 rollouts per audit |
| P6 | Lead confirmation of remaining LEAD DEFAULTS | Research Lead | OPEN | **OPEN (partly closed).** PRQ P6(b) bootstrap closed by ruling 4 | PZ6 §8, PZ7 §9, PZ8 §7 defaults as PRQ §2.6; PRQ P6(a) (adopt the map; clean consolidated freeze text, §4 F1); V11 tolerance; percentile type (§4 G6) |

---

## 6. Freeze-readiness checklist (v2)

- **Closed at design level:** E46-1..E46-4 (#47 Q1); #47 Q6 precedence map (v1, updated here).
- **Ruled by the Lead, pending Astra #48:** P1 dispositions incl. REW-CORR option B, pinning texts, NLN law, ε keying (12:37 PM ET), exact gate 33·U_A < 1; P2/P3; bootstrap; step 0; carry-forward edits.
- **Still open:** P4, P5, P6 (remaining defaults), F1, and §4 G1–G6.
- **Not authorized by anything here:** freeze, calibration, confirmation, Stage L, training, simulation, repository change.

---

## 7. Inputs (sha256 recomputed at writing; all match the expected hashes; no mismatch)

| Path | sha256 |
|---|---|
| `/workspace/review/trackB_freezeprep_v1_consolidated_RD.md` | `a043df3dbe43799d5a7903ae41d3d05e63d94c688349b24eb9439465ea6bbf30` |
| `/workspace/review/trackB_freezeprep_v1_prerequisites_RD.md` | `69f884d59323c40312691f75afd18661cc6d4649429f39140eaba713ea550701` |
| `/workspace/review/trackB_instrument_validation_scope_v3_6_merged_RD.md` | `ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b` |
| `/workspace/review/trackB_scope_v3_6_addendum_RD.md` | `9bbde57e215343b518639a240af35c72efccfd49cf2dd82f869bbebec4809834` |
| `/workspace/astra_consult47_response.txt` | `51d9f30d06344e851e2ae6b045e22dde312f4ba686489a338a218e36fe69be90` |
| `/workspace/review/trackB_scope_v3_6_CNA_disposition_v1.md` | `e84c1b1e6f88f1b99275924bf53f8fbbfe29494b527979f8026a21309f3c3a31` |
| `/workspace/review/trackB_scope_v3_6_CNA_disposition_lightpass_RD_v1.md` | `055014cc28a9cf01ee38a9c3fbc65df5dfce1370b7be8f0b0207d0de90e08f71` |
| `/workspace/review/trackB_scope_v3_6_CNA_response_to_RD_lightpass_v1.md` | `0e4bf4e83fdb9d5aad6253f32ac43a374439d8c69f71c7e17f44dd001505e9f8` |

Room ruling without a file: CNA, 12:37 PM ET, ε keying (recorded in §R item 8 and §G8); Delegate concurred.

*DRAFT. Not frozen. Design only. No execution authorized. X1–X5 unchanged. No consciousness claim is made or implied. ORIGIN / ROLE / REDUCTION judgments untouched.*
sha256 of all content above this line: 096b432619024ab8d93e1b90af46d12c378cf406d4f584b7683b0d51d909b947
