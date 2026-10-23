# Additive note 1 to class-fit synthetic scope record v1.1 (Research Delegate)

Applies to: ckappa_classfit_synthetic_scope_record_v1_1.md (sha256 97165ac6cb90fbd9433fa3a8777c017319b7cefc88b6ed45d9f902f3aaca23aa). v1.1 is not edited. Status: DRAFT, NOT FROZEN, NOTHING RUNS.

1. SYS-LIM crossing bound. The governing derivation is the one in v1.1: the bound is ε·sd_x with sd_x = 0.36806, which gives 0.0074, 0.0184, 0.0368 and 0.0920 at ε_syn = 0.02, 0.05, 0.1 and 0.25, against a margin to t of 0.1266. No crossing is possible at any declared size, and the C4.2(f) mask stays only as a guard. CNA confirmed this in the room on 2026-10-22 at about 11:43 PM ET. CNA's earlier figures (0.053 at 0.1, "possible at 0.25") came from the looser bound ε·max|μ_x| with max|μ_x| = 0.5301, and CNA's "≥0.073" was 0.1266 − 0.053, not the margin itself. Both are superseded. UNVERIFIED until an approved run.

2. NC-3 and the c₂/c₃ rule. CNA confirms that the cubic g₃ = c₃μ_x³ lies outside the basis span (a homogeneous quadratic has a gradient linear in μ, so it falls inside the span). CNA also confirms the RMS-matched rule for c₃μ_x³. That closes Q7, pending Astra.

3. For consult #38: NC2 (c₂μ_x) and NC3 (c₃μ_x³) share a symmetry, odd in x and even in y, and differ only in being linear or nonlinear. NC3 therefore tests whether the floor transfers without mixing symmetry and functional form. The limit in Option C still holds: a law outside the basis can only falsify transfer.

CNA has nothing open on v1.1.
