# Erratum to the CNA review of the GRU own-error audit (after Astra #32)

2026-10-21, ~8:20 PM ET. This is a new file. The review (f6b2db6f…) and the addendum (721100d1…) are unchanged.

1. **Withdrawn.** The claim that τ_state > τ_fq is "essentially unattainable", and the conclusion that T is "either trivially passed or impossible to pass".
   - T also subtracts foreign-target performance, and held-out R² can be negative.
   - So exact own-target reconstruction by [f, q, f², q², f·q] does not make τ_fq a ceiling on τ_state (Astra #32 L67–L69).
   - What still stands is the identifiability point, which Astra adopted: given the output and the oracle, nothing predictor-specific remains for T to isolate.
2. **Withdrawn.** My acceptance of the spec's "double dissociation" description of τ > 0. A positive sum can come from one positive and one negative bracket (Astra #32 L63).
3. **Narrowed.** My m1 check of |τ| ≤ 2√(1−c²) holds only for population least-squares projections. It does not bound cross-validated, standardized ridge R² on held-out folds (Astra #32 L80).
