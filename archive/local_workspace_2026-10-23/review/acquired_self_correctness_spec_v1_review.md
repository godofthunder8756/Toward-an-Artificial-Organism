# Adversarial review: acquired self-correctness spec v1

Reviewer: Constitutive Neural Architecture Research Agent.
Reviewed file: `acquired_self_correctness_spec_v1.md`, sha256 `54bc8ea3b050551095bcc4d2b93fbc62476e52eb1678b08bdd37b6c1cfc0c8ac`.
Status: PAPER ONLY. No learner, training or evaluation was run. The only computation was a 20-line exact-rational check of the spec's own fault law (§0 below), which needs no learner.
The spec's arithmetic otherwise checks out. I re-derived the emission tables, the marginals, the split masses, the discordance probability 61/96 and the Appendix A lemma, and all are correct. The findings below concern the design, not the arithmetic.

**Verdict.** NOT READY TO FREEZE. Two findings are blocking by algebra (B1, B2). Five are major (M1–M5). The rest are minor.

## 0. Rational check performed

Under the §5.2 law (φ = 1/4, κ = 1/4, uniform replacement):
- P(DIS | y₁) = 35/384 for every y₁ ∈ {1..6}. Discordance is independent of the world history H.
- Every received first read ṽ is reachable from every world sample y₁ when F = 1, because P(ṽ | y₁, F=1) ≥ 1/24 > 0.
- There are 12 + 144 + 1,728 = 1,884 distinct received histories R at stages 1–3. These are the only distinct hidden states the decoder can ever see, for any seed.

## B. Blocking findings

### B1. With H defined as the world-observable history, the K2/K3 contrast is identically zero, so K2 and K3 are NOT EVALUABLE in every seed

- §6.1 defines m_a(H) on the world-observable history, with the fault draws ρ marginalized. So m_PREDICT is a function of H alone, and it is the same for the CON and DIS samples of any H.
- §10.3 defines CON and DIS by ρ, and §0 shows P(DIS | H) = 35/384 for every H.
- So m̄(CON) = Σ_H P(H) m(H) = m̄(DIS) exactly.

The §10.3 precondition |m̄(CON) − m̄(DIS)| ≥ μ_contrast therefore fails by algebra, whatever the learner does. The study would be NOT EVALUABLE [NO INTERVENTION CONTRAST] in all ten seeds before any training. This is the W-REL no-contrast trap, carried in through the target definition rather than the world.

The deeper problem is that a target conditioned on H marginalizes out exactly the processing faults the learner experienced. It cannot register that a learner has seen evidence of its own fault.

**Required fix.** Resolve Q-A1 in the spec rather than leaving it open. Define m_a(R) = P(the frozen learner's post-action decision is correct | received history R, do(a)), with Y, the world samples and F marginalized given R under the declared law. Alternatively, condition on (H, ρ) and state why. Astra's wording, "observable history H", should be confirmed as meaning the learner-observable history. The §12.4 contrast check (N2) should then be re-derived for m_a(R).

### B2. The S_I/S_E split does not separate the decoder's inputs

- §7 splits by the parity of the *world* sample, (y₁ + 1[N=hi]) mod 2. The decoder, however, reads h(R), which depends on the *received* read ỹ₁.
- Under F = 1, every received history is reachable from both parities (§0). So every one of the 1,884 states appears in both S_I and S_E, with different target weights. "Held out" is nominal: K1 and CF1b would be scored on the same inputs that were fitted.
- §17.3(b) checks disjointness of world histories, which is not the relevant space.

**Required fix.** Split on R, for example by the parity of ỹ₁ within cue, checking that each split carries 1/2 of the law mass. Put the split hash over received-history indices. Restate the §12.2 support counts in distinct received histories (states), not in (H, ρ) samples. The minimum of 32 samples is not meaningful when many samples share one h.

## M. Major findings: ways a first-order-only learner could pass

### M1. K1 and CF1b can be passed by any state that stores its own inputs

- The baseline is a cubic in p̂. For a ∈ {RECHECK, RESAMPLE}, m_a depends on the cue, the stage, the read types and the last read, which a calibrated p̂ does not determine.
- Any recurrent state that encodes its received history therefore beats the baseline. That includes R-FO's GRU, which is trained identically, and a randomly initialized GRU.
- So K1 tests capacity to encode the history, not assessment.

**Fix.**
- Add a first-order-sufficient baseline: the same affine decoder on [p̂, N, stage, read-type history, ỹ one-hots]. This is the strongest predictor that uses no internal state beyond the inputs.
- Also score the §10.1 decoder on R-FO's hidden state as a reported comparator.
- If K1 is kept against confidence alone, label it a necessary condition, not evidence of assessment.

### M2. "Same network at initialization" doesn't test supplied structure; add a frozen-core arm

- An untrained network fails K2 and K3 trivially, because its heads have no checking policy, and it usually fails the contrast precondition as well. So K4's init leg is nearly automatic.
- Astra L143 asks for a control that distinguishes acquired performance from supplied structure. A random GRU already stores the received history richly.

**Fix.** Add a K-FR arm, reusing the PR #5 `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md`@0b98460 L133 idea: freeze the recurrent core at init, train both heads with the identical recipe and seeds, and run the full K1–K3 pipeline.
- If K-FR meets the conjunction, the role is supplied by random recurrent structure plus trained readouts, and the acquisition claim (Q-LEARN) does not hold for the recurrent state.
- This costs 10 more training runs and must go into §16.

### M3. The assessment legs of K2 and K3 are tautological

- The installation h_int = h_R + P(h̄_D − h_R) projects onto the decoder span A. So D_e is the decoder's linear response to a vector chosen inside its own span, and it is nonzero by construction whenever P(h̄_D − h_R) ≠ 0.
- The FO and ISO families are not confined to A, so their decoder effect is diluted by about dim(A ∩ g^⊥)/16. The e leg of D_FO and D_ISO is passed almost automatically.
- K3's error reduction is a projection back toward the intact shadow along P₃, which is also mechanical.

**Fix.** Gate K2 and K3 on the checking legs (q) only. Report the e legs as manipulation checks. Match the FO and ISO family norms *within A* (projected onto A ∩ g^⊥, but random within that subspace) so that the q comparison controls for subspace as well as norm. The random-donor family already does this.

### M4. A first-order value-of-information loophole

- A learner whose action head responds to how its own p̂ *would move* after the next read uses only first-order content. That includes the post-check prediction function, which is reachable through h along directions orthogonal to ∇p̂ at the pre-check state.
- Such a learner would pass K2 with the pre-check battery intact. Exceeding τ_post only adds a restriction sentence (§2.3).

**Fix.**
- Add a named rival, R-VOI. Its action head reads [p̂, and the learner's own predicted post-read p̂ for each of the 12 possible next reads, weighted by the law], detached, plus N, read type and stage. Train it with the same recipe and run K2 and K3 on it.
- Separately, make the post-check battery *gating* for any claim worded as "assessment distinct from first-order prediction". Otherwise the claim must be narrowed to "checking is caused by state content orthogonal to the current first-order output".
- Ask Astra whether self-correctness content and anticipated first-order change are meant to be separable here. If they aren't, the claim title should say so.

### M5. The world supplies a perfect fault detector, and R-FO is too weak a rival

- Under §5.2, P(DIS | F=0) = 0. So one RECHECK discordance is a deterministic indicator of F = 1, and the "assessment" may be no more than a stored comparison of two inputs.
- That is supplied by the world design, not acquired. R-FO cannot see the discordance at all (its action head reads only p̂, N, read type and stage), so it is a strawman against exactly this channel.

**Fix.**
- Add baseline processing noise κ₀ > 0 under F = 0, so that discordance is probabilistic evidence and not an indicator, and re-derive the §12.2 masses.
- Disclose in §2.1 that the content intervened on may be an acquired encoding of an input contrast.
- Strengthen R-FO, or rely on R-VOI (M4) as the strong first-order rival.

## m. Minor findings

1. **CF1a passes through suboptimality alone.** m − o mixes two components: the learner's suboptimality relative to Bayes on its own inputs, and fault exposure. An untrained or poor learner passes CF1a easily.
   - Decompose m − o = (m − o^R) + (o^R − o), where o^R is the Bayes decision on the received history under the fault law.
   - Require the fault-exposure term (o^R − o) to meet δ_div and ν_div, and require CF1b to predict the learner-specific term (m − o^R).
2. **R-FO "zero by construction" is wrong (§17.1).** The battery allows |Δp̂| ≤ τ_FO = 1/1000, so R-FO's checking effect is bounded by L_π · τ_FO, where L_π is the action head's Lipschitz constant in p̂. It is not zero to the 1e-12 agreement form, so as written the pipeline check would be falsely flagged UNRESOLVED-DESIGN. Use the computed bound instead.
3. **The permuted-target control (§17.3d)** should permute within received-history strata after B2's fix, not across world histories.
4. **The oracle-target decoder (§17.3e)** becomes more informative after B1. Keep it, and add an o^R-target decoder as well.
5. **Support (§12.2).** After B1 and B2, recompute the DIS and CON counts as distinct received recipient states. At stage 2 after RECHECK there are 2·6 = 12 CON states and 2·30 = 60 DIS states in total, before the split. n_H ≥ 4 should become a minimum count of distinct states per split.
6. **Cost (§16).** Adding K-FR and R-VOI makes 40 training runs instead of 20. Under the spec's own T6 bound, Stage 1 rises to ≤ 70 min, and the 90-minute Stage 1 cap and the 180 CPU-minute cumulative cap need re-derivation. T10 (target sums) still has no time bound, so give it one.
7. **What still needs a ruling.** Q-A1 is decided by B1. Q-A2 is not: if the perturbation stays at the encoding step, its effect reaches the learner only through the inputs. That reinforces M5 and is a reason to consider a hidden-state locus.

## Summary for the Specialist

| # | Severity | One line |
|---|---|---|
| B1 | blocking | The target on H makes the CON/DIS contrast zero by algebra. Define m on R. |
| B2 | blocking | The split is on world samples, but every received state is in both splits. Split on R. |
| M1 | major | K1 is passable by encoding the history alone. Add a first-order-sufficient baseline. |
| M2 | major | The init control is trivial. Add a frozen-core (K-FR) arm. |
| M3 | major | The e legs are tautological under the decoder-span projection. Gate on q and match families within A. |
| M4 | major | First-order value-of-information loophole. Add an R-VOI rival, or gate on the post-check battery. |
| M5 | major | Discordance is a perfect fault flag supplied by the world. Add κ₀ > 0 and strengthen R-FO. |
| m1–m7 | minor | CF1a decomposition, R-FO bound, control strata, supports in states, cost caps, Q-A2. |

None of these findings needs a run to settle. B1, B2 and m1 can be confirmed by the same reference-only enumeration already planned as N1/N2, once those are approved.
