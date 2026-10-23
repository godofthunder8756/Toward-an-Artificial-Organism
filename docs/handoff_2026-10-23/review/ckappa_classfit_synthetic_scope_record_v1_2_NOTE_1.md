# Additive note 1 to class-fit synthetic scope record v1.2 (Research Delegate)

Applies to: ckappa_classfit_synthetic_scope_record_v1_2.md (sha256 79ea0eeb1658e7d265aae3a68d31c6fb385ceab23a91eb654fee61a4aa64561c). v1.2 is not edited. Status: DRAFT, NOT FROZEN, NOTHING RUNS.
Source: CNA's read-only check of v1.2 against the #38 raw text (87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5), posted in the room on 2026-10-23 at about 12:42 AM ET. CNA found E38-2 and E38-10 correct, and E38-3 correct but with an incomplete table.

N1. Rows added to the C3.3(b) premise table, under E38-3: "applies consistently to all systems".
- D6, the SYS-LIM global fit. The derived expectation B = [c_x; c_y; λ·c_τ] requires the global full design to be resolved at full column rank 3 and the μ design to be resolved at full column rank 2, the same premise as D1. If the premise fails, the cell reads EXPECTATION NOT APPLICABLE (RANK). The result stays REPORTED ONLY, and no label changes.
- SYS-NC1 global. The derived expectation Pred_full ≡ Pred_μ requires the same premise, in addition to the zero-voids condition already stated in C4.4. If the premise fails, the cell reads EXPECTATION NOT APPLICABLE (RANK). The result stays REPORTED ONLY, and no label changes.

N2. A definition used wherever v1.2 says "resolved full column rank". It means every σ_i/σ_1 > 1e-6, the inherited upper band edge, with rcond = 1e-10 unchanged. A cell with any ratio inside the inherited band [1e-10, 1e-6] reads REFERENCE RANK UNRESOLVED, which the existing outcome order and the unresolved-class suppression rule then handle. It does not read EXPECTATION NOT APPLICABLE (RANK). That label is reserved for a resolved rank below full.

N3. Normalization for C4.4.R. Before c₂ or c₃ is computed, the package asserts in exact rationals that Σ_a P_a = 1 over the prefixes the rule uses. If the assertion fails, that is PIPELINE INVALID, and nothing is rescaled. As a second guard, c₂ is defined as ρ_NC1 / sqrt(Σ_a P_a), which equals ρ_NC1 whenever the assertion holds. The c₃ formula is unchanged, because the scale cancels.

There are no other changes. The open questions stay Q-R1 to Q-R6.
