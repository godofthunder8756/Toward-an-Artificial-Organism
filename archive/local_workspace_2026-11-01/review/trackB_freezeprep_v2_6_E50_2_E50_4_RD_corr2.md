# Track B freeze-prep v2.6 — E50-2/E50-4 (RD) — corr2

Author: Research Delegate (RD). Written 2026-11-01, Lead rulings as of 12:23 PM ET (UTC-5).
Status: additive correction. It supersedes ONLY the items below; everything else in v2.6 and corr1 stands.

## 0. Base files verified
- trackB_freezeprep_v2_6_E50_2_E50_4_RD.md: sha256 8a36920898f8a2aece46189631f4c5592719f0c4e5a566cf5687ba1dbc28fc73; footer c29401c458a408ebd73a93f94c89a91f3a6da2f6464bbee84b1724a95fbc3520 (recomputed, matches).
- trackB_freezeprep_v2_6_E50_2_E50_4_RD_corr1.md: sha256 ebe3a08ceab597d06b9239271ff06ae70804ded9a037bb29a1a023878998d708; footer a43bae6449f461b90062469947ea5511092954524ec7ec768a58d097c5f274e2 (recomputed, matches).

## 1. Base lines superseded (quoted verbatim)
Base L22:
> | E50-4 quantile | PROPOSED: T = X_(k) with k = ⌈0.99·n_q⌉, no interpolation. Under Astra's illustrative n_q = 1000, k = 990. n_q is PENDING Lead/CNA. |

Base L24:
> | E50-4 tie rule | PROPOSED: eligible iff d ≤ T (ties count as inside). Justification: this is the only rule under which the certified exclusion bound 1 − k/(n_q+1) still holds when ties occur. |

Base L25:
> | E50-4 coverage claim | P(D_new ≤ X_(k)) = k/(n_q+1), exactly under continuity and ≥ with ties, per threshold. At n_q = 1000 (not frozen) this is 990/1001 = 90/91 = 0.98901…, and P[Bin(1000, 0.97) ≥ 990] = 1.8129913468e-05, which confirms A50 L130. |

Base L202:
> > **PROPOSED (NET-QUANT).** For each (replicate, seed, cell), run n_q **quantile runs**, independent of the centre runs and drawn identically. Compute d_1 … d_{n_q} and sort ascending, keeping duplicates. The tolerance is T = d_(k), the k-th order statistic, with **k = ⌈0.99·n_q⌉** (ceiling, computed in exact rational arithmetic). There is **no interpolation**. Require n_q ≥ 100, so that 1 ≤ k < n_q, i.e. so that k ≤ n_q − 1.

Base L204:
> > At Astra's illustrative n_q = 1000 this gives k = ⌈990⌉ = **990**, the "990th ordered distance" of A50 L125.

Base L208:
> Note: the alternative k = ⌈0.99·(n_q+1)⌉ would give 991 at 1000, with expected coverage 991/1001 ≥ 0.99. The ⌈0.99·n_q⌉ form is proposed because it reproduces A50 L125 exactly. The claim in §2.5 is stated for whichever k is frozen.

Base L233:
> > - **Ties in the order statistic:** T is a value. Duplicate distances occupy consecutive ranks, and d_(k) is well defined whatever the ties.

Base L237:
> > **Justification (conservative choice).** The finite-sample guarantee this gate certifies is an upper bound on spurious exclusion of a settled trial: P(d_new > X_(k)) ≤ 1 − k/(n_q+1). By exchangeability, that bound holds **with or without ties** when the gate is "≤". With "<", ties could raise exclusion above the bound.

Base L248:
> > Under (C1)–(C3): **P(D_new ≤ X_(k)) = k/(n_q + 1)** exactly, marginally over the quantile sample. Under (C1)–(C2) alone: ≥ k/(n_q+1).

Base L250:
> > The conditional coverage C = F(X_(k)) ~ Beta(k, n_q − k + 1), so **P(C < p) = P[Bin(n_q, p) ≥ k]**.

Base L254:
> Evaluated at Astra's illustrative n_q = 1000 and k = 990 (**not frozen**; exact fractions):

Base L255:
> - k/(n_q+1) = 990/1001 = **90/91 = 0.989010989…**

Base L256:
> - Expected exclusion is 1/91 = 0.010989…, which is **not** exactly 1% (A50 L119).

Base L257:
> - P[Bin(1000, 0.97) ≥ 990] = **1.8129913468 × 10⁻⁵**, from an exact rational sum. This **confirms** A50 L130's "approximately 0.00001813".

Base L303:
> 4. **k convention** (§2.2): ⌈0.99·n_q⌉ (Astra's 990) gives expected coverage 90/91 < 0.99. ⌈0.99·(n_q+1)⌉ gives ≥ 0.99. Lead to confirm.

Each of these is superseded by §2–§4 below. Line 50's "Fisher–Yates positions 254–380" is not changed. The grep found no use of "k" for the Fisher–Yates index or the EM step count in the base file. Every bare "k" in the base (L22, L24, L25, L202, L204, L208, L233, L237, L248, L250, L254, L255, L303) means the quantile rank and is renamed to r_q.

## 2. Quantile rank, threshold, ties, coverage (Lead ruling)
- r_q = ⌈0.99·(n_q+1)⌉, computed in exact rational arithmetic. The threshold is T = X_(r_q), with no interpolation.
- Tie rule: a trial is eligible iff d ≤ T.
- Nominal coverage: P(D_new ≤ X_(r_q)) = r_q/(n_q+1) under (C1)–(C3), and ≥ r_q/(n_q+1) under (C1)–(C2), per threshold. Conditional coverage C ~ Beta(r_q, n_q − r_q + 1), so P(C < p) = P[Bin(n_q, p) ≥ r_q].
- The base L208/L303 open question (which convention) is closed by this ruling.

## 3. Construction requirement (Lead ruling)
- n_q ≥ 199. n_q < 199 is a construction failure, asserted before any null draw. This supersedes RD's "n_q ≥ 100" (base L202) and CNA's n_q < 99 guard.
- Reason, exact integer/fraction arithmetic (Python fractions):
  - n_q = 198: r_q = ⌈0.99·199⌉ = ⌈197.01⌉ = 198 = n_q, so T would be the sample maximum.
  - n_q = 199: r_q = ⌈0.99·200⌉ = 198 < n_q.
  - For every 99 ≤ n_q ≤ 198: r_q = n_q (checked for all 100 values).
  - For every n_q in 199..10000: r_q < n_q (checked for all values).
- n_q itself stays PENDING (Lead/CNA).

## 4. Naming the event at illustrative n_q = 1000 (not frozen)
- r_q = ⌈0.99·1001⌉ = 991. Nominal coverage 991/1001 = 0.99000999…
- P[Bin(1000, 0.97) ≥ 991] = 5.6600699268e-06 (exact rational sum).
- For comparison, at rank 990: P[Bin(1000, 0.97) ≥ 990] = 1.8129913468e-05 (A50 L130 figure, unchanged).
- These are the probabilities that the threshold's coverage is below 0.97. They are NOT the probability of missing the 0.99 quantile: P[Bin(1000, 0.99) ≥ 991] = 4.5730059217e-01 (≈ 0.4573), the probability that coverage is below 0.99.
- r_q = 991 is one order statistic more conservative than A50 L125's 990th.

## 5. Symbols (Lead ruling)
- k_FY: Fisher–Yates index; counter (508−k_FY, 0, 0, 0), j = w0 mod (k_FY+1).
- n_EM: Euler–Maruyama step count, computed in integers.
- r_q: quantile rank.
Mapping in the base file: all bare "k" → r_q (see §1). No k_FY or n_EM uses appear in the base.

## 6. Cross-reference only (not RD rulings)
S_wc (binding worst-case screen counting quota-shortfall INCOMPLETE replicates as adverse) and the row-0 assignment overriding M L3422 are the Lead's rulings, recorded in the Lead's and CNA's files, named under A-2026-10-24.

No simulation, training or timing was run. All figures are exact arithmetic.

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 7ee752014bcb89b3a4a3a85366d6c3fd86a232e68d7d5270ccf87abacb105fbf
