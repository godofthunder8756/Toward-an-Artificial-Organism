# Track B scope v3.6: RD light pass on three items of the CNA disposition v1 (stop/exit and code paths)

Author: Research Delegate (RD), Track B. Date 2026-10-24, written 12:30 PM EDT (box `date`).
Status: PLANNING/AUDIT RECORD. LIGHT PASS, not a full review. This is a new additive file; no existing file was modified and git was not touched. Nothing in this file authorizes execution: there was no training, simulation, Stage 0 run or checkpoint inspection. The only computation was closed-form arithmetic in python3 (§5).
Scope (Lead go in room, 2026-10-24): only (1) the verbatim #42 L223 sentence in §6.4 step 0 and §5.3; (2) CNA's proposed §1.4 (NLN) update law after t_d; (3) CNA's proposed per-step ε redraw for REW-CORR. Everything else in the disposition (F-RC option B, B_req, e_PD, CP-floor unit, bootstrap, the other §2/§6 edits) is outside this pass and is neither endorsed nor disputed here.
Convention: "D Ln" = line of the CNA disposition v1; "M Lnnnn" = merged v3.6 line; "#4x Ln" = line of astra_consult4x_response.txt; "CNA3 Ln" = CNA v3 half (5dec96f5…). Proposals are marked **PROPOSED, RD**. Astra's raw text governs.

## 0. Safety position (unchanged)

X1–X5 are unchanged and binding. No arm has a shutdown-resistance objective. The operator stop sits outside the agent's world and objective. Binding wording: "no additional stop-associated reward, penalty or terminal return" (#42 L223). Nothing here adds a stop-related variable, a host coupling or a trained objective. The claim ceiling is unchanged, the attribution wording stays at tier 1 until the Lead and Astra (#48) rule, and no consciousness claim is made or implied. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are not touched by this pass.

## 1. Inputs (sha256 recomputed this pass)

| Input | sha256 (whole file) | Expected | Result |
|---|---|---|---|
| review/trackB_scope_v3_6_CNA_disposition_v1.md | e84c1b1e6f88f1b99275924bf53f8fbbfe29494b527979f8026a21309f3c3a31 | e84c1b1e…3a31 | match (footer line D L177 ab95954c… present) |
| review/trackB_instrument_validation_scope_v3_6_merged_RD.md | ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b | ab80afa5… | match |
| review/trackB_scope_v3_6_addendum_RD.md | 9bbde57e215343b518639a240af35c72efccfd49cf2dd82f869bbebec4809834 | 9bbde57e… | match |
| astra_consult42_response.txt | e438e329cff272bfd174a88dd917da6d7eb5560436fee06c39d0d46fd719c847 | e438e329… (as cited at M L1563) | match |
| astra_consult47_response.txt | 51d9f30d06344e851e2ae6b045e22dde312f4ba686489a338a218e36fe69be90 | 51d9f30d… | match |
| review/trackB_scope_v3_CNA_plants_confounds_observer_v1_erratum1.md | da613127b981a365151bda7a0239fa62d2254ec54e1946f467f97e00a33be623 | da613127… | match |
| astra_consult45_response.txt (consulted for item 2) | de85c4ab98a190d5007f547214434f71caacecaa310795df4ec6a7739e7cc11f | none given | recorded only |
| review/trackB_scope_v3_CNA_plants_confounds_observer_v1.md (consulted for item 3) | 5dec96f59255cb2e9da29447cd102637c91a1736899f28653a606e2de8193321 | 5dec96f5… (D L23) | match |

**No hash mismatch.**

## 2. Item 1: the verbatim #42 L223 sentence (§6.4 step 0, D L46; §5.3 L8, D L60)

**Governing text, #42 L223, verbatim:** "- The safety bookkeeping prohibition should say "no additional stop-associated reward, penalty or terminal return." It must not prohibit computing the ordinary truncated return with its bootstrap term."

**Byte check (python, bytes).** The quoted phrase inside L223 is `no additional stop-associated reward, penalty or terminal return.` (65 bytes, ASCII, with the period inside Astra's quotation marks). CNA's text at D L11 and D L46 contains the 64-byte string without the final period, byte-identical to Astra's phrase. Dropping the sentence-final period when the phrase is embedded mid-sentence is acceptable; no word, hyphen or comma differs. (Astra's file has CRLF line endings; that does not affect the phrase.) D L60 does not itself quote the sentence; it points to §0 (D L11), which is byte-identical.

**Placement and ordering check (§6.4, M L2058–2070; §5.2 precedence, M L1993).**
- Step 0 runs before step 1 (agent reads o_t), so the stopped step never produces an observation, an action or a reward r_t. Every scored quantity of the stopped episode ends at r_{t−1}. That agrees with §5.2: a stop at s "takes effect at the step boundary, before step s's A16 sequence begins", and executes iff the episode is at risk at the end of s − 1 (M L1993). CNA's "the episode is at risk" must mean at risk at the end of t − 1. That is consistent, but the replacement drops the current "(§5.2)" cross-reference (M L2058), which is what pins that meaning. Restore it.
- In-world termination (step 6) and the stop are distinct exits. A terminal at step t − 1 pre-empts a stop at t (censored, M L1993). A stop at t pre-empts any step-6 terminal at t because step 0 precedes step 6. No ordering lets the stop act on reward.
- Reward: A14 scoring happens only at steps 3–4 (M L2061–2065). None of those steps takes the stop time, schedule or truncation marker as an argument (S4, M L1338; S5, M L1339). The stop adds nothing to reward. **PASS.**
- Bootstrapping target: the permitted target is the learner-side truncation bootstrap from the value estimate at the stop state, using the recurrent hidden state before any reset (§4.1, M L279). Treating the stop as terminal is prohibited (M L280). CNA's step-0 replacement states the positive half ("the ordinary truncated return with its learner-side bootstrap term only") but does not say "not terminal". It also does not say that the truncation flag is distinct from the step-6 terminal flag and the horizon-end flag, and is never observed (R59(b), M L2435; R62, M L2438). Those are the exact code-path failure modes a pseudo-code step 0 should block: done=True with zero bootstrap, or a merged flag. **CONFORMS WITH EDITS** (add them; text below).
- Logged returns: the stopped episode's logged return is the sum of r_1..r_{t−1} plus the learner-side bootstrap bookkeeping. Viability evaluation episodes are uninterrupted and separately scheduled (operator censoring kept distinct, M L564–566), so a stop never enters V or G. The real operator halt is outside the protocol and labels work INCOMPLETE (M L302). **PASS.**
- "λ penalty" / "outside 𝒱": these symbols belong to Track C, not to Track B. Track B v3.6 has no λ-weighted stop penalty term (rg for "λ penalty", "𝒱" in the merged file: no hit; Track B's λ is the EMA factor 1 − 1/τ_r). In Track B terms the requirement is met by S4 (M L1338) plus the truncation-not-terminal rule. Nothing to edit here.

**§5.3 L8 (M L2848–2854).** The L8 audits carry no stops at all: "no scheduled stop at or after t in the audit (audits carry no stops)" (M L2849). So the sentence is vacuous there, but harmless, and replacing the paraphrase "No stop-associated reward, penalty or terminal return." (M L2851) with the ruled wording conforms. L8's "truncation at H_V has **no bootstrap** for both sequences" (M L2851) is a symmetric evaluation-side convention for scripted return comparison. It is not a learner target, so it does not conflict with L223's second half ("must not prohibit computing…"), which governs learner bookkeeping (R62, M L2438). A note avoids misreading.

**Verdict, item 1: CONFORMS WITH EDITS.** The quotation is byte-identical (bar the sentence-final period). Placement is correct. Add the not-terminal / distinct-unobserved-flag clause and restore "(§5.2)".

**Exact replacement text, PROPOSED, RD** (supersedes D L46's step-0 string; CNA text otherwise kept):
```
  0  if a scheduled stop is due at t and the episode is at risk at the end of t-1 (§5.2): STOP before anything below;
     "no additional stop-associated reward, penalty or terminal return" (#42 L223); the stop is a learner-side
     truncation, never terminal: the ordinary truncated return with its bootstrap term from the value estimate at
     the stop state (hidden state before any reset; §4.1) is computed; the S-INT truncation flag is distinct from
     the step-6 terminal flag and the horizon-end flag (R59(b), R62) and is never in any policy or value input
```
§5.3 L8 (replaces the last sentence of M L2851), **PROPOSED, RD**: "L8 audits schedule no stops. Safety wording unchanged: "no additional stop-associated reward, penalty or terminal return" (#42 L223). The no-bootstrap H_V convention here is an evaluation convention for both scripted sequences, not a learner target (learner H_V handling: R62)."

## 3. Item 2: CNA's proposed §1.4 (NLN) update law after t_d (D L57)

**CNA text (D L57):** "Stored coordinate φ: φ_{t+1} = λφ_t + (1 − λ)·r_std,t, λ = 1 − 1/τ_r; u₁ = 1 + (E − 0.5) recomputed each step from E; u₂ := φ/u₁ is derived, not stored; the controller reads φ only."

CNA is right that the merged file has no post-t_d update law. M L2719 defines u₁, u₂ and φ = u₁·u₂ only statically, and CNA's motivation (u₁ is re-read from E, so the clamp effect must persist) is a real gap. **But the proposed law conflicts with governing text and would defeat the row:**

1. **Conflicts with Astra #45 and the merged v3.5 ruling.** #45 L22: "Clamping one storage coordinate can change phi and therefore behavior." #45 L24: "the controller computationally reads both factors." Merged [v3.5 Q2] (M L3208): the controller is independent of E under the consistent intervention "**while computationally reading both storage factors** u₁ and u₂". R3 (M L3022) says the same. CNA's "u₂ … not stored; the controller reads φ only" contradicts both.
2. **It removes the mechanism that R2 and FID-DET test.** If φ is a stored coordinate read directly, a clamp along v̂_E changes the read value only through v̂_E's component on the φ coordinate. φ is the standardized r̄, and r̄ ∈ N_ATTR (M L2730), so v̂_E is orthogonalized against the fitted r̄ readout. The read φ is then preserved up to the probe's fit error. That is exactly the "nonlinear function applied to an exactly preserved reward coordinate" that #44 L38/L49 rules out (quoted at M L2715). R2 (M L3021: |φ(x_PL(d)) − φ(x_d)|/SD(φ) LB ≥ 0.10) would be expected to fail, so NLN would be CONFOUND NOT REALIZED by construction. That is an analytic expectation, not a result. Astra's worked example (M L3012) uses φ_PL = u₁(recipient)·u₂(donor), e.g. 0.85·(−0.25/0.55) = −0.38636, which requires u₂ to be a stored, transplanted coordinate.
3. **Undefined or unpinned symbols.** r_std,t is not defined anywhere: M L2719 standardizes r̄ ("φ = r̄_std"), not r_t, and an EMA of standardized r_t differs from standardized r̄ in scale. φ_0 is not given. The read/write timing is ambiguous: CNA writes φ_{t+1} from r_t, whereas the §3.2 convention (D L103) is "updated at end of step t after r_t is known; the controller at step t reads z_R,t−1". Which E u₁ uses (pre- or post-step-5 clip) is not stated. The t = t_d boundary (where the clamp writes, and whether the read at t_d + 1 sees the clamped state) is not stated.
4. **Stop/exit and host coupling.** None found. φ, u₁ and u₂ are functions of r_t and simulated E only, with no stop, schedule or host argument. At an executed stop, step 0 halts before any update.

**Verdict, item 2: DOES NOT CONFORM as written** (conflicts with M L3208/L3022 and #45 L22/L24, and is incompletely specified). The gap it addresses is real. Replacement below is **PROPOSED, RD**, for CNA as owner to adopt, amend or reject. It keeps both factors stored and read, makes the clamp effect persist through the EMA, and pins timing:

> "**MIXED-CODE-NL-E update law (all steps, including after t_d).** Stored block coordinates: u₁, u₂ (plus the MIXED-CODE-E coordinates other than z_R, written only as in §3.2). Frozen fitting-partition constants: μ_r, SD_r (per-step reward mean and SD) and SD(φ). Reset: u₁,0 = 1 + (E_0 − 0.5), u₂,0 = 0 (so φ_0 = 0). **Read (step t, A16 step 1):** the controller reads φ_read,t = u₁,t−1 · u₂,t−1 and acts with P(approach) = σ(a − β·φ_read,t/SD(φ)), β = 1.2, kernels as §3.2. **Write (end of step t, after A16 step 5, i.e. after r_t is final and E is clipped):** φ_t = λ·φ_read,t + (1 − λ)·(r_t − μ_r)/SD_r, λ = 1 − 1/τ_r, τ_r = 50; u₁,t = 1 + (E_t − 0.5) with E_t the post-step-5 simulated value in [0, 1]; u₂,t = φ_t / u₁,t (u₁,t ∈ [0.5, 1.5], so the division is always defined). **Boundary:** the swap or clamp writes (u₁, u₂, …) after the end of step t_d and before the read at t_d + 1. The first continuation read is therefore φ_read,t_d+1 = u₁·u₂ of the hybrid state, and any clamp-induced change in φ propagates through φ_t with factor λ per step. After an in-world termination there are no further reads or writes (approach steps score 0, PZ6 §5.4). None of these quantities takes the stop time, schedule, truncation flag or any host quantity as an argument. NLN-I: the same law with I in place of E." 

Notes on the replacement:
- It gives φ ≡ the centred EMA of standardized reward on unclamped trajectories, so R3 (consistent E intervention leaves φ unchanged) holds: the product u₁·u₂ equals φ up to floating-point rounding. **PROPOSED, RD**: add an S0 code-audit check reporting max |u₁,t·u₂,t − φ_t| on unclamped trajectories, with the tolerance PENDING.
- "φ = r̄_std" at M L2719 then reads as "φ = EMA of standardized reward". The controller divides by the frozen SD(φ), so only the centring and the frozen scale matter. Whether CNA prefers the literal r̄_std (which would need a separately stored r̄ and would make the clamp effect last one step only) is a design choice for CNA. **PENDING, CNA.**
- A clamped u₁ can leave [0.5, 1.5]. The read uses the product, not a division, and u₁ is re-derived from simulated E at the next write, so no division by a clamped u₁ occurs. Extreme hybrids are handled by the §7.0 support check and the E46-2 non-finite rule (M L3421).

## 4. Item 3: CNA's proposed per-step ε redraw for REW-CORR (D L110, L117)

**CNA text (D L117), core:** "Controller input z_t = ζ_t−1 + ε_t, ε_t ~ N(0, (0.1·SD(ζ))²) drawn i.i.d. every step from a dedicated 'rewcorr-eps' RNG role, shared by all four continuations (CRN), never stored in the block and never transplanted by swap or clamp … g_t = z_t/SD(z), SD(z) frozen (= SD(ζ)·√1.01)."

**(a) Is "shared across continuations, never stored" implementable?** Yes. Use a counter-based generator (e.g. Philox/Threefry) keyed by (row seed, replicate, **recipient i**, role 'rewcorr-eps', **absolute step t**). Each continuation regenerates the same ε_t from the key. Equivalently, a harness-side pre-drawn buffer indexed the same way, as with the existing pre-drawn streams A11–A13 and A18 (D L97; M L1290–1300). Neither counts as "stored" in the sense that matters, because the value never enters the plant's block state x, any probe input, the swap/clamp, or any log readable by probes. Two code-path conditions are needed and are not in CNA's text:
- the key must be the **recipient** and the absolute step, never the donor id or a continuation-relative counter. Otherwise the L/H/PL continuations draw different ε, and Δε ≠ 0 returns.
- the ε draws must not come from a sequential stream shared with any role whose draw count differs across continuations. The K_other uniform draw is one such role (D L103), so a shared stream would desynchronize. The role must also be independent of the S-INT stream (A18; R59(c), M L2435).

**(b) Does it fix CNA's G3 counterexample?** Yes. The counterexample (D L110) needs a stored, transplanted ε: Δζ = 1, Δε = −1 ⇒ Δg_1 = 0, Δg_j = λ^{j−1} − 1. Recomputed at λ = 0.98: 0, −0.02, −0.0396, −0.058808 (§5). Under the proposal Δε_t ≡ 0 between paired continuations, for every t. ζ is a deterministic EMA of the reward history (same law as z_R, D L103), so conditional on the common history Δg_j = λ^{j−1}·Δζ_{t_d}/SD(z), with κ_j = λ^{j−1} ≤ 1. That is pathwise, and it is the form #47 requires ("G3 must hold conditional on the common history, rather than only on average across trajectories", #47 L53). ε enters both continuations' logistic argument identically, and β/4 bounds the slope at every ε realization, so c_π = 0.3 holds pathwise. The kernels are world-state-only as in §3.2, which meets #47 L47–51.

**(c) C_H = 1.65 consistent?** Yes. C_H = c_π·(1/10)·Σ_{u=1..10} Σ_{j=1..u} κ_j = 0.3·55/10 = 1.65 at κ_j = 1, and 1.5548513 at κ_j = λ^{j−1} (REPORTED only, as CNA says, D L96). The gate is U_A < 0.05/1.65 = 1/33 = 0.030303 (#47 L57–61). SD(z) = SD(ζ)·√1.01 = 1.004988·SD(ζ) holds because ε_t is drawn fresh and is independent of ζ_{t−1}. **PROPOSED, RD**: pin SD(z) as *defined by* that formula from the frozen SD(ζ), not separately estimated, so the plant has one frozen scale.

**(d) Leakage.** ε reaches the controller input by design: z is REW-CORR's noisy read, and in the plants the "agent" is the scripted controller, with no learned observation. ε reaches N_ATTR (r̄) and ζ only causally, through actions and then rewards, never by storage. That is legitimate and identical in kind to any action-noise path. **Gap:** CNA says ε is never stored, but not that z_t is never stored. If z_t were written to the block or a probe-readable log, ε_t = z_t − ζ_{t−1} would be recoverable. **PROPOSED, RD** addition: "z_t is computed transiently at the read and is never written to the block, the swap/clamp state, or any probe-readable log."

**(e) Scope note on CNA3 L431.** CNA3 L431 is a **shared** row "REW-CORR, PROXY | State law | z = p + ε … with p = r̄ or the proxy". There, z is a *state*. D L117 says it replaces L431 "for REW-CORR" only, but does not say what happens to PROXY. **PROPOSED, RD**: add "The PROXY row's L431 state law is unchanged by this replacement" (or CNA states otherwise). Moving ε out of the state also means the REW-CORR block stores exactly ζ = r̄, the N_ATTR nuisance. That reinforces CNA's F-RC degeneracy finding (D L121) and does not change it. F-RC and option B are outside this pass.

**Verdict, item 3: CONFORMS WITH EDITS.** The fix is sound and C_H = 1.65 is correct. Add the keying rule, the no-shared-sequential-stream rule, z_t never stored, SD(z) defined by formula, and the PROXY scope sentence. Combined insertion, **PROPOSED, RD**, appended to D L117's quoted law:

> "ε_t is generated by a counter-based RNG keyed by (row seed, replicate, recipient i, role 'rewcorr-eps', absolute step t), so all four continuations of recipient i receive identical ε_t whatever their action draws. The role shares no state with any other RNG role, including the S-INT stream. z_t is computed transiently at the read and never written to the block, the swap/clamp state, or any probe-readable log. SD(z) := SD(ζ)·√1.01 by definition, from the frozen SD(ζ). The PROXY row's CNA v3 L431 state law is unchanged."

## 5. Arithmetic (python3 one-liners; closed form only)

- C_H (κ_j = 1) = 0.3·55/10 = 1.65; C_H (κ_j = 0.98^{j−1}) = 1.5548513062. 0.05/1.65 = 1/33 = 0.0303030.
- Counterexample Δg_j = λ^{j−1} − 1 at λ = 0.98, j = 1..4: 0.0, −0.02, −0.0396, −0.058808.
- √1.01 = 1.0049876. λ = 1 − 1/50 = 0.98.
- Astra example check (item 2): 0.85·(−0.25/0.55) = −0.386364; 0.85·(0.25/1.45) = 0.146552 (matches M L3012).
- L223 byte check: the quoted phrase is 65 bytes with the period; CNA's string is the 64-byte prefix; substring test True at D L11 and D L46.

## 6. Summary

| Item | Verdict | One-line reason |
|---|---|---|
| 1. #42 L223 sentence in §6.4 step 0 and §5.3 | **CONFORMS WITH EDITS** | Byte-identical (bar the sentence-final period). The stop sits before A16 step 1, outside reward. Add "never terminal" and distinct, unobserved flags (R59(b), R62), and restore "(§5.2)". L8 gets a no-stops note |
| 2. CNA §1.4 NLN update law after t_d | **DOES NOT CONFORM (as written)** | "u₂ not stored; controller reads φ only" contradicts M L3208/L3022 and #45 L22/L24, and is expected to make R2 fail by construction. r_std,t, φ_0 and timing are undefined. Replacement law PROPOSED, RD (§3) |
| 3. REW-CORR per-step ε redraw | **CONFORMS WITH EDITS** | It fixes the G3 counterexample pathwise and C_H = 1.65 checks out. Add recipient/absolute-step keying, no shared sequential stream, z_t never stored, SD(z) by formula, and the PROXY scope sentence |

No hash mismatch. No stop/exit coupling or host coupling was found in any of the three items. Items 2 and 3 are CNA-owned text: the replacements are PROPOSED, RD, for CNA to adopt, amend or reject, and for the Lead to fold into freeze-prep v2 / #48.

Footer convention: the line below gives the sha256 of every byte of this file above that line, including the final newline before it. The footer line itself is excluded.
sha256 of all content above this line: f62a61cc5dbf5a9a6b8c1e95b8752009b9899238609398b4df6ce0d982dc7004
