# Deviations and ambiguities

The protocol file is unchanged. Each item is a literal reading of a point the
protocol does not fully specify, or a float64 implementation choice required
to run it. None of these was chosen after seeing the study's TEST results.

1. **Gaussian draws.** `N(0, 1/5)` is the mathematical convention: mean 0 and
   variance 1/5. `a` and `C` use standard deviation `1/√5`.
2. **Grid edge.** A selected `(g, b)` is a grid edge when it is not the
   interior point `(1, 0)`.
3. **Tie band.** Configurations within ε₀ of the smallest VAL criterion are
   tied. The protocol order, ending in the smaller `g`, selects one of them.
4. **Probability-weighted PD/CD.** Weights are `P(h)`. The continuation mean
   is `Σ_p P(p|u) f(p,u)`, and the prefix mean is `Σ_u P(u|p) f(p,u)`.
5. **TEST-restricted PD/CD.** Uniform mean over the 64 TEST histories. Means
   are uniform over the TEST members of each continuation or prefix.
6. **PD/CD ratios.** A denominator ≤ 10⁻¹² is UNDEFINED, including when the
   numerator is large. UNDEFINED never passes. This is the §5 exception to
   E3-v2, which would have returned +∞.
7. **Transfer inequality.** The §3 gate is the direct comparison
   `E(F-TRAINED) ≤ ½ E(F-INIT)`. The E3-v2 ratio rule is used for the reported
   robustness ratio against F-TUNED32 and for ratio843, not as a replacement
   of that inequality.
8. **8/10 counting.** An invalid seed is not a pass. More than 2 invalid
   seeds makes that label UNRESOLVED. Otherwise 8 or more passes is the
   positive label, and every smaller count is the named negative label.
9. **E1.** Fewer than 8/10 fresh seeds with A-FIT, A-LEARN, and CAND integrity
   is `UNRESOLVED (E1 not replicated)`. The protocol gives no NOT SHOWN band
   for this prerequisite. The positive label used here is `E1 REPLICATED`.
   Sections 4–6 stay descriptive in that case.
10. **Seed validity.** §3 validity requires finite training, finite outputs in
    `(0, 1)`, whole-state identity and restoration ≤ `IDENTITY_TOL`, and a
    reproducible checkpoint hash, for CAND, F-TRAINED, and F-INIT. §4 also
    requires those for R-TUNED843 and CAND. §5 adds sham (≤ ε₀), restore
    (≤ `IDENTITY_TOL`), and finite reversion and perturbation forecasts. A
    sham or restore failure on any matrix invalidates the seed for all of §5.
    A failure confined to F-TUNED32 does not invalidate §3.
11. **Identity checks.** Identity and restoration are the PR #5 whole-state
    transplant and stage-5–8 restoration checks.
12. **SPECIFIC non-passes.** A seed that misses transfer, has `B ≤ 10⁻¹²`, or
    has `‖δ_k‖_F ≤ ε₀` does not pass SPECIFIC. It is not thereby invalid.
13. **Variation seeds.** A seed passes the variation conditions when it is
    §5-valid and the three primary uniform ratio conditions hold. The positive
    label is issued only when `REPLICATED SPECIFIC(k)` also holds. Otherwise
    the result is `selective variation reduction not demonstrated`, including
    when SPECIFIC(k) is UNRESOLVED.
14. **Fresh readout initialization.** Torch is seeded, a GRU-8 plus the stated
    readout is constructed (GRU first, then `Linear`, then `Linear`), and the
    recurrent weights are then overwritten with the frozen core. Every
    training run reseeds its episode generator at `1000+s`. The nine selection
    runs share that stream and the same `6000+s` readout initialization.
15. **Selection does not read TEST.** VAL risk is computed from the 48 VAL
    histories only. TEST for R-TUNED843 and F-TUNED32 is the refit evaluation.
16. **Checkpoint bytes.** The sha256 is of a canonical JSON dump: sorted
    keys, dtype, shape, and base64 little-endian payload. A checkpoint is
    reproducible when reloading it and hashing again returns the same digest
    and the same tensors.
17. **P1 RMSE.** Root mean squared error of each chart coordinate on the 8
    held-out prefixes. Held-out R² uses the held-out mean as the baseline. A
    total sum of squares ≤ ε₀ makes that R² undefined and the threshold fails.
    The protocol names only the positive decoder label; otherwise the result
    is `not met`.
18. **P2 LOCALIZED.** One draw is LOCALIZED when the six E3-v2 gates pass:
    partial and wrong ≤ 1/2, complement ≥ 3/4, vector and XOR. Coverage and
    rank are reported and are not extra gates. The frozen PR #5 ratio is
    stored beside each ratio as a historical diagnostic. `+∞` passes only an
    at-least gate. The protocol names only `PIPELINE VALID (E3-v2)`; the
    negative used here is `PIPELINE NOT VALID (E3-v2)`.
19. **Harness state.** The suite sees `z ∈ R^8`. For P2+ with `s = 0`, ν is
    stored beside z and is not written into z. A transplanted batch that does
    not continue the harness's previous tensor starts that side state at
    `ξ = 0`. P2+ forecasts do not depend on ν. One-hot `e_k` is the unit
    vector in position `k−1`. QR is NumPy's reduced QR with diagonal signs
    mapped so `diag(T) > 0`; a zero sign is mapped to `+1`.
20. **P2− cube-root roundoff.** Decoding `ψ = Rᵀ z` lets an unused Q-component
    leak into ψ at about 10⁻¹⁶, and the cube root amplifies that leak above
    ε₀. The harness therefore keeps the exact ψ written at encode time and
    reuses it when `Rᵀ z` matches that record within 10⁻⁸. A move that changes
    ψ by more than that is decoded from z. This is what makes the required
    zero-effect check meaningful in float64. A failed zero-effect check
    invalidates P2− only. It does not by itself change the P2+ pipeline label.
21. **P2 descriptive suite.** LOCALIZED for the pipeline is the cross-fitted
    partial, complement, and wrong block, or that same block with the basis
    replaced by Q. Donor tracking, random probes, nearest posterior, PCA, and
    the all-16 fit from the frozen PR #5 suite are not gates and are not
    re-run on the harness.
22. **Approval text.** The hashed protocol header still says the training
    approval is pending. That sentence was not edited. This run was authorized
    by the repository owner's explicit approval, dated 2026-10-20, recorded in
    the freeze manifest.
23. **Smoke test.** The freeze test suite trains two Adam steps at batch 8 to
    prove the wiring. Those losses are not study results and are not saved.
24. **Negative rival label.** The protocol says a failed §4 (ii) count is
    reported and does not give a second slogan. The results use `not met`
    together with the count. A failed §4 (i) result is the protocol's
    `not observed`.
25. **Matrix names in the claim.** The successful paragraph is quoted
    verbatim. The matrix is then named in a following sentence, `The specified
    matrix is W_hk.`, so the quoted wording stays exact.
