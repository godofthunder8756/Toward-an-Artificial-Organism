# ERRATA v1

Additive reporting note for graded recurrent reversion against both first-order-matched and isotropic controls. Attributed to Astra consult #18.

- No existing file is edited or deleted.
- The primary label is unchanged: GRADED JOINT REVERSION EXCEEDS BOTH FIRST-ORDER-MATCHED AND ISOTROPIC CONTROLS (PREFIX FUNCTION): REPLICATED, at exactly 8/10.
- No dose curve was rerun and no network was trained.
- The original report remains `../PHASE_B_RESULTS.md`. The corrected copy is `../PHASE_B_RESULTS_v2.md`.

## E-C1. Phase A autograd ranges

The phase A sentence that marks the autograd spans `inside=False` against the printed Appendix B ranges is a rounding artifact. Astra accepted this wording:

> Per-seed comparison against the draft finite-difference values (`/workspace/scratch/fo_control/feasibility.json`, Research Delegate review) agrees within |Δcos| ≤ 3.7e-10 and relative |Δ⟨G,delta⟩| ≤ 1.7e-8 in all 20 seeds; ⟨G,delta⟩ < 0 in 15/20. The 'inside=False' flags reflect rounding of the printed ranges. This confirms the derivative calculations by autograd, as consult #17 required.

`/workspace/scratch/fo_control/feasibility.json` is not in this checkout. The versioned recomputation from the committed checkpoints is `feasibility_autograd_comparison_v1.json`.

- sha256: `43cd03492342e57bca25800959ebfb3e58eed4aecd70a75882efe07456effc7a`
- Maximum absolute cosine gap versus the committed autograd values: 3.805788600930171e-10, seed 102.
- Maximum relative inner-product gap: 1.7038662252133627e-08.
- Autograd ⟨G, delta⟩ is negative in 15 of the 20 phase A seeds.

The committed autograd spans are cosine (−0.33992948552390484, 0.07540785411202333) and inner product (−0.0023088689385560536, 0.0004244290335291259) for seeds 100–109, and cosine (−0.3965000573141834, 0.12934365440039314) and inner product (−0.0022006679762187707, 0.0006825993167205182) for seeds 200–209. The printed ranges are rounded. No tolerance was changed.

## E-C2. Per-seed margins and secondary condition counts

Verified from `phase_b_results.json` before this note was written. The counts agree.

| target | D_FO | D_ISO | both | M |
| --- | --- | --- | --- | --- |
| r | 6 | 6 | 5 | 0 |
| z | 9 | 9 | 8 | 0 |
| n | 8 | 8 | 6 | 8 |

The per-seed margin table for weight_hh, r, z, and n is in `PHASE_B_RESULTS_v2.md`. These counts complete reporting. They change no result. All three secondary labels remain CRITERION NOT MET.

## E-C3. Failed isotropic comparisons

Verified from `phase_b_results.json`: for seed 300, exactly one of 32 ISO paths has AUC greater than REV (0.007476265083572757 against 0.005588382653952067). For seed 301, exactly one of 32 ISO paths has AUC greater than REV (0.006349304542170263 against 0.00566617390773577). In both seeds the comparison is strict and the gap exceeds eps0. No FO path has greater AUC than REV in either seed.

> Seed 300: D_ISO failed; exactly one of 32 ISO paths had greater AUC than REV. Seed 301: D_ISO failed; exactly one of 32 ISO paths had greater AUC than REV.

## E-C4. Phase A pass counts

`PHASE_B_RESULTS.md` does not contain a combined 13/20 count or group-level 6/10 and 7/10 phase A pass counts. Where such summaries are read, including the independent review, Astra's note applies. It is copied into the development-history section of `PHASE_B_RESULTS_v2.md`.

> The combined and group-level Phase A pass counts are retrospective descriptive summaries that depart from the prescribed per-seed-only reporting format. They are not confirmatory evidence and do not enter any Phase B verdict. The authoritative Phase A presentation is the separate per-seed record for each exploratory group.

## E-C5. Boundary, FO wording, and ledger

Copied verbatim into `PHASE_B_RESULTS_v2.md`.

Boundary qualifier:

> This result meets the prespecified threshold exactly: 8/10 seeds. Two passing seeds have a margin below 10% against at least one control family. Each failing seed is exceeded by exactly one sampled ISO path. Robustness to additional draws, alternative control families or a new seed cohort is untested.

FO wording:

> The FO directional criterion was met more often in this cohort: 10/10 versus 8/10 for ISO. Adding FO to the joint gate excluded no additional seeds. This does not establish that FO controls are generally less demanding.

Astra's next sentence says FO had a larger sampled maximum than ISO in four seeds. In `phase_b_results.json` that maximum is larger for FO in five seeds: 305, 306, 307, 308, and 309. The sentence is quoted in `PHASE_B_RESULTS_v2.md` with that JSON count beside it. It is not corrected in place. The negative-derivative count in the following sentence agrees: ⟨G, delta⟩ is negative in 9 of 10 phase B seeds.

Ledger, verbatim:

> Q-CAUSE, organization level: SUPPORTED, BOUNDED. In W2, continuation-stage joint recurrent reversion met the prespecified joint FO-and-ISO AUC criterion in 8/10 fresh GRU-8 seeds. In each passing seed, excess prefix-function loss exceeded every one of 32 first-order-matched paths and every one of 32 isotropic paths and met the materiality threshold. This supports a causal contribution of the trained hidden-to-hidden parameters under the specified intervention and fixed surrounding computation.
>
> The result meets the replication threshold exactly. Two passing seeds have thin margins against at least one family; each failing seed loses to one sampled ISO path. FO passed in 10/10 seeds and excluded no additional seeds beyond ISO. The claim concerns sampled controls and dose-averaged AUC, not arbitrary perturbations, every dose or the endpoint.
>
> Secondary blocks: criterion not met, r 0/10, z 0/10, n 5/10. The primary effect was not reproduced by any single block at the declared criterion; no localization or interaction mechanism is identified.
>
> Q-LEARN: E1 and transfer replicated 10/10. Q-NECESSITY: NOT_ESTABLISHED, not tested. Q-EXIST: not addressed; the supplied exact solution remains available. No C4, consciousness or organism conclusion.

## Deviation 3. Exactly zero gradient (Astra section 4)

Ratified. With nonzero displacement and exactly zero gradient:

```text
r_k = norm(d_k)
rho_k = 1
```

The block has full randomized spread and belongs in `R_eff`. Skip the undefined unit-gradient orthogonality check, but retain norm and first-order identity checks. This is distinct from the diagnostic near-zero threshold.

## Deviation 4. Zero displacement (Astra section 5)

Keep it an ordinary eligibility non-pass, as frozen. There is no learned displacement in that target to test. Do not count it as an invalid or collapsed-comparison seed. If the entire displacement is zero, avoid forming undefined radius ratios. This ruling affects no observed result.
