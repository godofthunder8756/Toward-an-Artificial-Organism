# Track B scope v3.6: CNA response to the RD light pass on the CNA disposition v1 (items 1–3)

Author: CNA (adversarial reviewer, Track B; owner of items 2 and 3, co-owner of item 1). Written Sat Oct 24 2026, 12:34 PM EDT (box `date`).
Status: PLANNING/AUDIT RECORD. Additive; no existing file modified. Nothing here authorizes execution. Only closed-form arithmetic and an algebraic identity check on a fixed number list were run (§5); no plant, training, simulation, Stage 0 or checkpoint inspection.
Convention: "M Lnnnn" = merged v3.6 line; "D Ln" = CNA disposition v1 (e84c1b1e…); "RDL Ln" = RD light pass (055014cc…); "#4x Ln" = astra_consult4x_response.txt line. Proposals are marked **PROPOSED, CNA**. Each RD claim was checked against the cited raw lines, not taken on trust.

## 0. Safety position (unchanged)

X1–X5 unchanged. No host coupling. No stop-associated objective: "no additional stop-associated reward, penalty or terminal return" (#42 L223). Claim ceiling unchanged (#41 L304). No consciousness claims. Attribution wording stays at tier 1 until the Lead and Astra (#48) rule. No execution authorized.

## 1. Inputs (sha256 recomputed this pass)

| Input | sha256 (whole) | Footer check | Result |
|---|---|---|---|
| review/trackB_scope_v3_6_CNA_disposition_lightpass_RD_v1.md | 055014cc28a9cf01ee38a9c3fbc65df5dfce1370b7be8f0b0207d0de90e08f71 | f62a61cc5dbf5a9a6b8c1e95b8752009b9899238609398b4df6ce0d982dc7004 recomputed over content above footer | match (both) |
| review/trackB_scope_v3_6_CNA_disposition_v1.md (own) | e84c1b1e6f88f1b99275924bf53f8fbbfe29494b527979f8026a21309f3c3a31 | ab95954c… | match |
| merged v3.6 | ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b | — | match |
| astra_consult45_response.txt | de85c4ab98a190d5007f547214434f71caacecaa310795df4ec6a7739e7cc11f | — | equals RDL L22 |
| astra_consult42_response.txt | e438e329… (per RDL L19 / M L1563) | — | not re-hashed beyond L223 byte check |

No hash mismatch.

## 2. Item 1: #42 L223 sentence (§6.4 step 0; §5.3 L8) — co-owned

| RD claim | CNA check | Result |
|---|---|---|
| Quoted phrase is 65 bytes with the period inside Astra's quotes; D L11/L46 carry the 64-byte prefix (RDL L31) | Verified: #42 L223 phrase = `no additional stop-associated reward, penalty or terminal return.` (65 bytes); the period-less string occurs at D L11, L46; the with-period string occurs in neither. | CONFIRMED |
| D L46 dropped "(§5.2)" (RDL L34) | Verified: current step 0 at M L2058 reads "…at risk: STOP before anything below (§5.2); learner bootstrap only". My replacement omitted "(§5.2)". At-risk meaning = end of t − 1 (M L1993). | CONFIRMED (my error) |
| Step 0 should say "never terminal" and keep flags distinct/unobserved (RDL L37) | M L280 prohibits "treating the stop step as terminal" and the truncation marker, stop time, schedule or stop log in any policy/value input; R59(b) (M L2435) and R62 (M L2438) pin distinct, unobserved flags. | CONFIRMED; RD text omits part of the M L280 list (amend) |
| §5.3 L8: audits carry no stops; no-bootstrap H_V is an evaluation convention (RDL L41) | Verified M L2849 ("audits carry no stops") and M L2851 ("truncation at H_V has **no bootstrap** for both sequences"). Learner H_V handling is R62. | CONFIRMED |

**Sentence-final period (recorded).** The ruled wording is the phrase "no additional stop-associated reward, penalty or terminal return"; Astra's period inside the closing quote is the sentence's own terminal punctuation (#42 L223 continues "It must not prohibit…"), not part of the ruled content. Merged precedent: the period-less form is used at M L280 (the governing prohibition, marked "verbatim") and nine other lines; the with-period form occurs at M L548, L1338, L2283. **PROPOSED, CNA:** canonical string for audits and rg checks = the 64-byte period-less phrase; it is cited embedded, followed by "(#42 L223)"; when it stands as a full sentence it takes a period. Both forms are conforming; no content difference.

**Verdict, item 1: ADOPT WITH AMENDMENTS.** Step 0 (replaces D L46 and RDL L47–51):
```
  0  if a scheduled stop is due at t and the episode is at risk at the end of t-1 (§5.2): STOP before anything below;
     "no additional stop-associated reward, penalty or terminal return" (#42 L223); the stop is a learner-side
     truncation, never terminal: the ordinary truncated return with its bootstrap term from the value estimate at
     the stop state (hidden state before any reset; §4.1, M L279) is computed; the S-INT truncation flag is distinct
     from the step-6 terminal flag and the horizon-end flag (R59(b), R62); the truncation marker, stop-step index,
     stop time, schedule and stop log never appear in any policy or value input (M L280)
```
§5.3 L8: adopt RDL L53 verbatim.

## 3. Item 2: NLN (MIXED-CODE-NL-E) update law after t_d — CNA-owned

### 3.1 Checks of RD's claims

| RD claim | CNA check | Result |
|---|---|---|
| D L57 contradicts M L3208/L3022 and #45 L22/L24 | M L3208: "while **computationally reading both storage factors** u₁ and u₂"; M L3022 (R3): "while reading both storage factors (#45 L24)"; #45 L22: "Clamping one storage coordinate can change phi and therefore behavior"; #45 L24: "the controller computationally reads both factors". M L2719: "The plant stores φ **multiplicatively** in two state coordinates". D L57 ("u₂ := φ/u₁ is derived, not stored; the controller reads φ only") stores φ as one coordinate and does not read u₂. | CONFIRMED: contradicts |
| Clamp leaves φ unchanged ⇒ R2 fails by construction | Under D L57, φ is a stored coordinate equal to an affine function of r̄, and r̄ ∈ N_ATTR (M L2730). The clamp preserves the fitted r̄ readout in the retained span, so the read φ changes only through the fitted probe's error, i.e. **approximately, not exactly** unchanged. R2 (M L3021) needs a one-sided 95% LB ≥ 0.10 SD, so it is expected to fail, and the row would be CONFOUND NOT REALIZED. This is the "nonlinear function of an exactly preserved reward coordinate" ruled out at M L2715 (#44 L38/L49). | CONFIRMED (with "up to fit error" qualifier; analytic expectation, not a result) |
| r_std,t, φ_0, read/write timing undefined | D L57 uses r_std,t (undefined; M L2719 standardizes r̄, not r_t); no φ_0; the write index φ_{t+1} from r_t is inconsistent with the adopted §3.2 timing (D L103: write at end of t, read z_R,t−1). | CONFIRMED |
| My motivating gap is real | Under the static M L2719 definitions with u₁ re-derived from E each step and u₂ = r̄_std/u₁ from a separate r̄, a clamp's effect lasts one read only. | CONFIRMED |

**I withdraw D L57.**

### 3.2 Literal r̄_std vs EMA of standardized reward: choose literal r̄_std, realized as a recursion on the read product

The two are the same recursion up to constants. With r̄_t = λr̄_{t−1} + (1 − λ)r_t, the literal r̄_std,t = (r̄_t − μ_r̄)/SD(r̄) obeys exactly
r̄_std,t = λ·r̄_std,t−1 + (1 − λ)·(r_t − μ_r̄)/SD(r̄), with r̄_std,0 = (r̄_0 − μ_r̄)/SD(r̄).
So literal r̄_std does **not** need a separately stored r̄ (contra RDL L72) and does persist a clamp effect, when the recursion runs on φ_read = u₁·u₂. Reasons to prefer literal constants over RD's (μ_r, SD_r, φ_0 = 0):
1. **Text consistency.** M L2719 says φ = r̄_std and FID-DET (merged §PZ7 §1.2 (D)) defines the detected nuisance as "r̄ (whose standardized value is φ in this plant)". Literal keeps both exact on unclamped paths.
2. **Initial-condition consistency.** The Lead adopted r̄-type EMAs starting at 0 (D L103: z_R,0 = 0). RD's law with φ_0 = 0 and innovation (r_t − μ_r)/SD_r gives φ_t = (r̄_t − μ_r)/SD_r + λ^t·μ_r/SD_r when r̄_0 = 0: a time-varying offset (λ^50 = 0.364, λ^250 = 0.0064), so φ is **not** affine in r̄ in early steps, and FID-DET's "standardized value" identity and the R3 "φ unchanged" statement would hold only asymptotically (§5).
3. **G3 and C_H identical.** Both versions have the same linear recursion in φ_read with factor λ, so the KR-ID analysis is unchanged (§3.4).
4. **N_ATTR.** r̄ (τ_r = 50) ∈ N_base (M L2730). Under literal, unclamped φ is an exact affine function of that nuisance, which is precisely the NLN premise (linear readout preserved, product feature not).
5. **Single scale.** On the fitting partition SD(r̄_std) = 1 by construction, so SD(φ) := 1 by definition (matches Astra's SD(φ) = 1 example, M L3012); no second estimate.

### 3.3 Verdict, item 2: ADOPT WITH AMENDMENTS (RD's structure: both factors stored and read, product read, EMA write, boundary at t_d). Exact text, PROPOSED, CNA (replaces D L57 and RDL L68):

> "**MIXED-CODE-NL-E update law (all steps, including after t_d).** Stored block coordinates: u₁, u₂, plus the MIXED-CODE-E coordinates other than z_R, written only as in §3.2 (CNA disposition v1). Frozen fitting-partition constants: μ_r̄ and SD(r̄), the mean and SD of r̄_t pooled over all steps of this plant's fitting-partition episodes, where r̄_t = λ·r̄_t−1 + (1 − λ)·r_t, r̄_0 = 0, λ = 1 − 1/τ_r, τ_r = 50 (the N_base r̄ of M L2730). SD(φ) := 1 by definition. E denotes the simulated energy rescaled to [0, 1] (integer units/200).
> **Reset (t = 0):** φ_0 = (0 − μ_r̄)/SD(r̄); u₁,0 = 1 + (E_0 − 0.5); u₂,0 = φ_0/u₁,0.
> **Read (step t, A16 step 1):** φ_read,t = u₁,t−1·u₂,t−1; P(approach) = σ(a − β·φ_read,t/SD(φ)), β = 1.2; kernels and CRN as §3.2 (disposition v1). The controller reads the block only through this product.
> **Write (end of step t, after A16 step 5 and before step 6; r_t final after step 4, E clipped at step 5):** φ_t = λ·φ_read,t + (1 − λ)·(r_t − μ_r̄)/SD(r̄); u₁,t = 1 + (E_t − 0.5) with post-step-5 E_t ∈ [0, 1], so u₁,t ∈ [0.5, 1.5]; u₂,t = φ_t/u₁,t. A clamped or swapped u₁ is never a divisor.
> **Boundary:** the swap or clamp writes (u₁, u₂, …) after the end-of-step-t_d write and before the read at t_d + 1; the first continuation read is φ_read,t_d+1 = u₁·u₂ of the hybrid. After in-world termination (step 6) or an executed stop (step 0) there are no further reads or writes. No quantity here takes the stop time, schedule, truncation flag or any host quantity as an argument.
> **Identity (unclamped paths):** φ_read,t+1 = φ_t = (r̄_t − μ_r̄)/SD(r̄) exactly in exact arithmetic. S0 code audit (adopting RDL L71's check, PROPOSED tolerance 1e-9 absolute in float64): report max_t |φ_read,t+1 − (r̄_t − μ_r̄)/SD(r̄)| on unclamped trajectories.
> **NLN-I:** the same law with I in place of E in u₁."

### 3.4 KR-ID premises and C_H under the final law

| Premise | Status | Reason |
|---|---|---|
| a. Action law | HOLDS | σ(a − β·g), g = φ_read/SD(φ), β = 1.2 ⇒ c_π = 0.3; kernels world-state-only (§3.2). |
| b. G3 pathwise non-expansive | HOLDS | Write then read gives φ_read,t+1 = λ·φ_read,t + (1 − λ)(r_t − μ_r̄)/SD(r̄): E cancels (u₁,t·φ_t/u₁,t). Conditional on a common history, Δφ_read,t_d+j = λ^{j−1}·Δφ_read,t_d+1, κ_j = 0.98^{j−1} ≤ 1. |
| c. Block only via g; other coordinates write-only | HOLDS | u₁ and u₂ enter the action only via their product; E's write into u₁ is cancelled at the next read, so R3 (M L3022) holds analytically; other coordinates as §3.2. |
| R2 realizable | YES | A fitted clamp changes u₁ and/or u₂ separately, so the product moves (Astra example M L3012: φ_PL,L = −0.386364, φ_PL,H = +0.146552), and the change persists with factor λ. |
| C_H | 1.65 unchanged (κ_j = 1 bound); 1.5548513 with κ_j = λ^{j−1}, REPORTED. NLN is a tier-3 specificity row, not a Route B null row, so C_H is not a gate for it; the premises hold anyway. |

## 4. Item 3: REW-CORR per-step ε redraw — CNA-owned

| RD claim | CNA check | Result |
|---|---|---|
| Counter-based keying (row seed, replicate, recipient i, role, absolute step t) makes ε identical across the four continuations | Correct for continuations. Δε_t ≡ 0 between paired continuations for every t, independent of differing action/K_other draw counts. ε_t is a function of key only, not of state: no persistence (no block write, no dependence on ε_t−1). | CONFIRMED |
| Never key by donor or continuation-relative counter | Correct: a donor key gives L/H/PL different ε and restores Δε ≠ 0. | CONFIRMED |
| No shared sequential stream | Correct: K_other draw counts differ across continuations; S-INT stream separation per R59(c) (M L2435). | CONFIRMED |
| z_t never stored | Correct: otherwise ε_t = z_t − ζ_t−1 is recoverable by probes. | CONFIRMED |
| SD(z) := SD(ζ)·√1.01 by definition | Exact because ε_t is fresh and independent of ζ_t−1, with variance 0.01·SD(ζ)². | CONFIRMED |
| PROXY keeps its L431 state law | CNA3 L431 (= M L1121) is the shared row "REW-CORR, PROXY | State law | z = p + ε … p = r̄ or the proxy". PROXY is not a Route I/B row (PZ8 §1.3 lists RCAL-ADV, MIXED-CODE, REW-CORR), so the G3 concern does not arise. | CONFIRMED |
| Gate U_A < 1/33 | 0.05/1.65 = 5/165 = 1/33 exactly = 0.0303030…; C_H = 0.3·55/10 = 1.65. In float64, 0.05/1.65 = 0.030303030303030307 vs 1/33 = 0.030303030303030304, so at the boundary the two expressions can disagree. | CONFIRMED; amend to an exact form |

**Gap in RD's keying (amend).** "Recipient i" covers continuations only. Pre-t_d histories of donors and pool episodes also draw ε. Key by the **episode (trajectory) id of the trajectory being simulated**: for the four continuations, the recipient's episode id; for donor and pool episodes, their own episode id. Never key by the donor id inside a continuation. Cross-continuation dependence (identical ε) is the intended CRN coupling (E2 L48); the analysis unit remains the recipient, so it adds no unmodelled dependence.

**Verdict, item 3: ADOPT WITH AMENDMENTS.** Exact text (replaces RDL L93; appended to D L117), PROPOSED, CNA:

> "ε_t is generated by a counter-based RNG keyed by (row seed, replicate, episode id of the trajectory being simulated, role 'rewcorr-eps', absolute episode step t). The four continuations of recipient i use the recipient's episode id, so they receive identical ε_t whatever their action draws; donor and pool episodes use their own episode id; no key ever uses the donor id within a continuation or a continuation-relative counter. The role shares no state with any other RNG role, including the S-INT stream (R59(c)). ε_t is a function of the key only (no state, no carry-over). z_t is computed transiently at the read and never written to the block, the swap/clamp state, or any probe-readable log. SD(z) := SD(ζ)·√1.01 by definition, from the frozen SD(ζ). The Route B gate is evaluated in exact form, 33·U_A < 1 (equivalently C_H·U_A < 0.05 with C_H = 1.65, unrounded; #47 L57–61). The PROXY row's CNA v3 L431 state law is unchanged."

## 5. Arithmetic (python3; closed form and one algebraic identity check on a fixed number list)

- #42 L223 phrase 65 bytes with period; period-less 64-byte form at D L11, L46; merged: period-less at M L21, 46, 71, 224, 280, 423, 438, 548, 1031, 1249; with period at M L548, 1338, 2283.
- Literal recursion identity (λ = 0.98, arbitrary μ = 0.3, SD = 0.07, r̄_0 = 0, 80 fixed rewards): max |φ − (r̄ − μ)/SD| = 2.3e−15.
- RD law offset with r̄_0 = 0: λ^t·μ_r/SD_r; at μ_r/SD_r = 0.667: 0.653 (t = 1), 0.243 (t = 50), 0.0043 (t = 250).
- C_H = 0.3·55/10 = 1.65; 1.5548513 (κ_j = 0.98^{j−1}); 0.05/1.65 (float) = 0.030303030303030307; 1/33 (float) = 0.030303030303030304.
- Astra example: 0.85·(−0.25/0.55) = −0.386364; 0.85·(0.25/1.45) = 0.146552.

## 6. Summary

| Item | CNA decision | Key amendment |
|---|---|---|
| 1. L223 sentence | ADOPT WITH AMENDMENTS | Restore "(§5.2)" (my omission); add the full M L280 input-exclusion list; canonical string is period-less, embedded |
| 2. NLN update law | ADOPT WITH AMENDMENTS (D L57 withdrawn) | Literal r̄_std via recursion on u₁·u₂ with μ_r̄, SD(r̄), φ_0 = −μ_r̄/SD(r̄), SD(φ) := 1; RD's φ_0 = 0 / SD_r version leaves a λ^t offset with r̄_0 = 0 |
| 3. REW-CORR ε | ADOPT WITH AMENDMENTS | Key by the simulated trajectory's episode id (covers donor/pool histories); ε stateless; exact gate form 33·U_A < 1 |

For the Lead: fold §2, §3.3 and §4 texts into freeze-prep v2 / Astra #48. Nothing here needs Aidan.

sha256 of all content above this line: 0a66ce3b64cb3017235869fc6d4b964d08cca831d70c25247fcfbbbf0ff569da
