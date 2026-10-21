# Deviations and ambiguities

This file is part of the freeze. It does not change a dose, a tolerance, a seed, a family size, or a label rule. Protocol §13 readings R1–R8 are followed as written there.

## Implementation specifications fixed before any dose curve

1. **Gradient-check draw shape.** The protocol names generator seed `2,000,000 + 100·s` and three random unit directions in V-space. It does not name the tensor shape. Each direction is one `torch.randn((24, 8), dtype=torch.float64)` call, in order, divided by its Frobenius norm. The manifest hashes those raw draws, before normalization. A zero-norm draw is an integrity failure. The reversion direction `d/‖d‖` is checkpoint-dependent and is not part of the base Gaussian manifest.

2. **Tied versus untied gradients.** The tied override and the sum of the four untied stage gradients are the same derivative. Float64 accumulation order can differ by a few units in the last place. The test requires the maximum absolute entrywise gap to be at most `1e-18`. Byte identity is required for the two tied recomputations, not for the tied-versus-untied comparison. This gap is not a scientific threshold and is not used on a dose curve or a label.

3. **Exactly-zero gradient and `R_eff`.** The protocol defines `r_k = ‖d_k − p_k‖` for a nonzero gradient, and a separate isotropic fallback when every entry of `g_k` is `0.0`. For that fallback this code sets `r_k = ‖d_k‖` and `ρ_k = 1` when `‖d_k‖ > eps0`, so the block is not collapsed and its full radius enters `R_eff`. `gh_k` is undefined, so the orthogonality check is not applied. The first-order match is exact because both inner products are zero.

4. **Primary collapse when `‖delta‖ ≤ eps0`.** `R_eff/‖delta‖` is not formed. The seed is ineligible because the displacement is below `eps0`. It is not marked as a collapsed control family.

5. **AUC rank ties.** Rank uses exact float equality. An equal AUC counts against REV. Endpoint ties stay on the separate `eps0` rule in §6.1.

6. **Appendix B files.** `/workspace/scratch/fo_control/` is not in this checkout. Phase A reports autograd `⟨G, delta⟩` and `cos(G, delta)` for every seed and compares the spans with the ranges printed in protocol Appendix B. No per-seed draft finite-difference value is filled in.

7. **Continuation rollout.** Dose curves continue from the stage-4 state with the same `MatrixOverride` and GRU step as a full rollout. A test requires bit-identical predictions on a real checkpoint. The intervention is unchanged.

8. **Test-only switches.** `prefix_loss` accepts `detach_h4` and `freeze_parameters` so a test can show that detaching h_4 blocks the early-weight gradient. Study calls use the defaults: detach h_4, and freeze every parameter other than V.

9. **Transfer helper.** As in the graded-reversion evaluator, `transfer_pass` is called with its validity argument true. Seed validity remains a separate eligibility item.

No consciousness claim is made. No rival grid is run.
