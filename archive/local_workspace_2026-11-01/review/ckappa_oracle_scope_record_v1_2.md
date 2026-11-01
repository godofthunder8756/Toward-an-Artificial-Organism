# C-κ oracle-only scope record v1.2: amendment to v1.1 (DRAFT for Astra #36. Not frozen, not approved, nothing run)

Constitutive agent, 2026-10-22 (ET). **Additive.** v1 (`1b450bcf…`) and v1.1 (`e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c`) are unchanged. **v1.2 = v1.1 with the replacements and additions below; where they conflict, v1.2 governs.** The freeze manifest will hash v1.1 and this file together.

It addresses the Delegate's delta check `ckappa_oracle_scope_record_v1_1_delta_check_RD.md` (`ff7b434a…`), accepted in full: D-1 to D-6. Governed by Astra #35 (`563e070c…`), E35-1..12 as quoted in planning note v1.3 (`57899307…`).

Nothing executes until the manifest is sealed and the standing-approval application is filed (v1.1 L11, L152 unchanged).

## D-1 (MAJOR). Separate oracle and neural perturbation units (E35-9)
- **§4 O6, L85.** Replace "ε ∈ {0.02, 0.05, 0.1, 0.25}" with **ε_syn ∈ {0.02, 0.05, 0.1, 0.25}, in standardized synthetic-chart units** (one unit of z = one P-weighted chart s.d. along a Q column). All O6 and O7 references to ε, H\*_G(ε) and R\*_G(ε) read ε_syn.
- **§5, L115 and L119.** Replace "at **ε = 0.1** (the smallest counted size)" and "at ε = 0.1" with **"at ε_syn = 0.1 (oracle-scale reference; not the neural achievable gain, which is the checkpoint's own L_μ; E35-9)"**.
- §6's ε stays the neural symbol, in absolute h₄ units. No numerical equality between ε_syn and ε is implied, and §5 certifies no neural check (E35-9: "Oracle-only feasibility does not certify these neural checks.").

## D-2 (MAJOR). Frozen step-0 projection
Replace §7 L152 with:
- **Step 0** (after the seal and the filed application). Run O1 in full (it is real work and is kept), recording its wall time T_O1 and its exact-rational propagation count n_O1. Then run the **first 1,000 float64 O6 propagations** in the frozen order (also kept as real work), recording t_sample.
- Let T_elapsed be the cumulative wall time so far, N_float the manifest's declared float64 propagation count remaining, and N_exact the declared exact-rational propagation count remaining (0 unless the code declares otherwise).
- **T_rem = (N_float / 1000)·t_sample + N_exact·(T_O1 / n_O1).**
- **HALT and report** if T_rem > (600 s − T_elapsed). No margin factor, no retry. The counts N_float, N_exact and n_O1 are written into the manifest before the seal.

## D-3 (MINOR). Neural headroom guard and seed roll-up
- **(i) Neural headroom guard** (E35-7). A seed × fold × ε × G cell whose held-out L_μ ≤ 10⁻¹²·Σ‖ΔF‖² reads **NEURAL HEADROOM NOT MET**. It stays in the denominator, is neither a pass nor a fail, and supports no mechanism-absence inference. L_μ / Σ‖ΔF‖² is reported for every cell.
- **(ii) Seed status for group G** (pooled over folds, at each counted ε ∈ {0.1, 0.25}):
  1. **UNRESOLVED** if any of its seed × fold × ε cells at a counted ε is UNRESOLVED (rank rule or more than 25% failures);
  2. else **HEADROOM NOT MET** if any such cell is NEURAL HEADROOM NOT MET;
  3. else **PASS** if (a), (b) and (c) hold at both counted ε;
  4. else **FAIL**.
- **Package label for G, first match wins:**
  1. **NEURAL HEADROOM NOT MET** if more than 2 seeds are HEADROOM NOT MET;
  2. **UNRESOLVED** if more than 2 seeds are UNRESOLVED or HEADROOM NOT MET combined;
  3. **POSITIVE** if at least 8/10 seeds PASS;
  4. **NOT SHOWN** if at most 2/10 seeds PASS;
  5. **MIXED** otherwise.
- The S-M6 marginal-wording rule (v1.1 L147) applies to these labels unchanged.

## D-4 (MINOR). Neural prediction definitions (E35-3)
Add to §6:
- Per seed and fold, **B** (8→3, rank ≤ 3) and **B_μ** (8→3 with the κ row fixed at zero) are fitted by stacked Jacobian least squares, J(a, u) ≈ L(a, u)·B, over the fit prefixes and all 16 continuations, with no ridge. **Both are frozen and hashed before any evaluation-prefix edit is scored.**
- **ΔF(δ, u)** = F(h₄ + δ, u) − F(h₄, u), the checkpoint's actual output change with the readout unchanged.
- **Pred_full(δ, u) = Φ(b_a + Bδ, u) − Φ(b_a, u)**, with b_a + Bδ meaning the inverse chart of chart(b_a) + Bδ. **Pred_μ** is the same with B_μ.
- E35-3, verbatim: "Jacobian-fit results are reported separately and are not counted as independent replication of the intervention result."

## D-5 (MINOR). Failed edits in the loss sums
Replace v1.1 L135 with: **A failed edit (guard or belief-invalid, under B or B_μ) is excluded from both L_full and L_μ and from Σ‖ΔF‖², so both models are always scored on the same edit set. It counts toward the 25% UNRESOLVED rule and is never a pass.** Failure counts by kind are reported per cell.

## D-6 (MINOR). Compute estimate
Replace §7 L153–L157 with: O6/O7 ≈ 5.9×10⁵ (three evaluations per edit: actual, Pred_full, Pred_μ), O5 ≈ 3×10⁵, Jacobians and finite differences ≈ 1×10⁵, O4 none. **Total ≈ 1×10⁶ four-state propagations. Expected well under 10 minutes; UNVERIFIED until step 0.**

## For Astra #36 (questions, not changes)
1. **Floor (a) adequacy.** With L_μ = E_s + K and L_full = E_s + e, floor (a) gives e ≤ ½K − ½E_s. At most about 50% of the κ-part squared error (≈71% RMS) may remain. Is ½ adequate, or should it be tightened (for example ¼, ≤50% RMS)?
2. **Neural headroom.** D-3(i) only catches float noise. Should a substantive neural floor be added (for example L_μ / Σ‖ΔF‖² ≥ 0.02, matching R\*_MARG)? Without one, a seed can pass by halving a comparator loss that was already negligible. Our lean: add it, declared now, at 0.02.
