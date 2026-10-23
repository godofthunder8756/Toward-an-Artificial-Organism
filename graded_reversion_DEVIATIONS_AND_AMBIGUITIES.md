# Deviations and ambiguities

Study: graded joint recurrent reversion with oracle-referenced prefix-function loss.

The protocol file `GRADED_REVERSION_PROTOCOL_FINAL.md` is unchanged. Each item is a literal reading of a point the protocol does not fully specify, or an implementation choice required to run it. None of these was chosen after seeing a phase A or phase B curve.

The repository already has `DEVIATIONS_AND_AMBIGUITIES.md` from the recurrent-core transfer freeze. That file is a hashed PR #7 artifact. It is left byte-identical. This study's log is this file.

## Adopted from the protocol

1. **A1.** "Exactly zero displacement" means Frobenius norm ≤ ε₀.
2. **A2.** C_prefix is a seed-level eligibility condition for the primary target and for every secondary block.
3. **A3.** Appendix A text is fixed in this hash. It is not edited after phase B, and it is not run: Appendix A is not approved.
4. **A4.** An engineering fix would be a new hashed version before phase B. Phase A outputs would be kept and labelled with their code version. No such fix is applied inside this version.

## Readings used to implement the frozen text

5. **Deviations filename.** See the note above. The protocol's log name collides with the frozen PR #7 file.
6. **Transfer inequality.** E is the TEST total excess. The comparison is the direct inequality E(F-TRAINED) ≤ ½ E(F-INIT), the frozen `transfer_pass` rule. Its validity argument is passed as true so that this study's §4 validity stays a separate eligibility item rather than being folded into the transfer flag twice.
7. **E1, phase B only.** Recurrent-core FINAL §3: CAND meets A-FIT on TEST, A-LEARN holds (the initialization does not meet A-FIT on TEST), and CAND integrity holds (finite training, outputs in (0, 1), whole-state identity and restoration ≤ IDENTITY_TOL, checkpoint hashes). Phase A does not recompute the ten-seed E1 replication.
8. **Draw digest.** The sha256 is of the raw float64 `torch.randn` arrays, shape (32, 24, 8), in path order, before rescaling. Rescaling depends on the displacement and is checked separately. Little-endian C-contiguous bytes are hashed.
9. **Phase B draw digests.** Seeds 200–209 are included in the freeze manifest. Recording the digests does not train those seeds and does not run phase B.
10. **Zero gaussian draw.** If a nonzero block has a random matrix of Frobenius norm 0, rescaling is undefined and the seed is invalid. This is not expected.
11. **Relative block norms.** The tolerance is 1e-12 relative: |‖ε‖ − ‖δ‖| / ‖δ‖ for each nonzero block and for the full matrix. A zero block's perturbation is exactly 0.
12. **Primary hook.** The primary target uses PR #7 `MatrixOverride` with rows (0, 24) and a 24×8 block. The frozen hook is not modified. `weight_ih`, both biases, updates 1–4, and the fresh readout stay at their trained values.
13. **Which tensors are W_T and W_0.** W_T is F-TRAINED `weight_hh_l0`, promoted from the stored float32 values to float64. W_0 is CAND-init `weight_hh_l0`, promoted the same way. F-INIT `weight_hh_l0` must match CAND-init; a mismatch invalidates the seed. L_prefix(F-INIT) is a rollout of the F-INIT checkpoint, including that checkpoint's own readout.
14. **Intact, α = 0, and SHAM.** Intact is the float64 F-TRAINED model with no override. α = 0 writes W_T. SHAM writes a copy of the trained block through the hook. Both must match intact within ε₀. RESTORE, after α = 1, reruns with no override and must match within IDENTITY_TOL.
15. **Components.** L_prefix^X, ^Y, and ^XOR use the same 1/256 factor on one output. They sum to L_prefix. There is no division by three.
16. **L_cont.** The prefix formula with the roles of prefix and continuation exchanged: means over u for each p.
17. **Weighted versions.** Probability-weighted L_prefix uses conditional means Σ_p P(h) f / Σ_p P(h) and an outer sum weighted by P(h). TEST-restricted L_prefix uses uniform means over the TEST members of each continuation and a uniform mean over the 64 TEST histories. PD and CD are the PR #7 `variation_stats` definitions (uniform, probability-weighted, and TEST-restricted).
18. **Rank.** The per-dose rank of REV is 1 plus the number of random paths with a strictly larger dose excess. A tie keeps the better rank. The rank is among the 33 paths.
19. **Monotonicity count.** A step is non-decreasing when Δ(α_{i+1}) ≥ Δ(α_i), with no extra tolerance. There are 5 steps. The count does not gate a label.
20. **Median.** The median of the 32 random AUCs is the arithmetic mean of the 16th and 17th sorted values.
21. **Counts in the phase B sentence.** Eligibility failures are valid seeds that miss an eligibility condition for the target being labelled. Invalid seeds are not included in that number. D and M counts are the mathematical flags out of ten; a missing curve is not a pass. A joint pass requires validity, eligibility, D, and M. The denominator remains ten.
22. **Seed-level integrity.** A sham, restore, endpoint, checkpoint, output, or block-norm failure on any target invalidates the whole seed. Curves that were computed are still reported. An invalid seed is not an eligibility failure and is not a pass.
23. **Resume files.** Each finished seed is written before the next seed starts. A finished seed is not retrained. Initialization uses `torch.manual_seed(s)` through the PR #7 constructor, and every training arm reseeds its own episode generator at 1000+s, so a resumed seed does not change the recipe.
24. **Appendix A, unimplemented run.** The selection tie uses the inherited ε₀ band and then smaller |log₂ g|, smaller |b|, smaller b, smaller g. The grid union has 47 configurations. The unrun refits are R-TUNED843 (8→70→3, torch seed 6000+s) and F-TUNED32 (8→32→3, torch seed 5000+s), because the appendix adopts recurrent-core FINAL §4 (i)/(ii). `APPENDIX_A_APPROVED` is false.
25. **Phase B guard.** The approval note records the 2026-10-20 10:38 PM ET approval. The runner still refuses to train until `graded_reversion_phaseA_exploratory/ENGINEERING_STATUS.json` exists, names code version `graded-reversion-v1`, and has `blocking_engineering_issue` false. A blocking issue is an implementation failure (draw digest mismatch, W(0) not exactly W_T, or an exception), not a scientific non-pass.
26. **Runtime.** Draw hashes and any phase B initialization are those of the torch build named in the freeze manifest, CPU `torch.Generator`, one thread. They are not retuned.
27. **Analytic oracle check.** The freeze tests recompute L_prefix(q_star) = 0, the prefix-blind identity, and the Appendix B rounded PD/CD scale from the oracle alone. No network dose curve is used to choose a parameter.
