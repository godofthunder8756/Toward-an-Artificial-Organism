# CNA erratum to the adversarial read of the GRU audit v1.3 results (`3f30ccda…`)

2026-10-21, ~11:05 PM ET. This is a new file; the original is not edited. It accepts the corrections in the Delegate's review `398e9220…`.

1. **R1 range.** For the 7 floor-infeasible units, R_exc runs from 6.8·10⁻⁴ to 2.9·10⁻³, not "about 7·10⁻⁴ to 2·10⁻³". The infeasibility conclusion is unchanged.
2. **R2 C1 counts.** Two sel_* arms have 0 C1 passes, not "5 to 9 each".
3. **Withdrawn wording that goes beyond §13a:**
   - "the state holds input information that the output has thrown away";
   - "not a hidden signal".

   The Delegate's in-bounds rewrites replace them.
4. **The "cuts both ways" argument is a conditional conjecture, not a result.** It holds only if the state encodes the collinear readings approximately linearly. It is withdrawn as support for any reading. The bounded statement stands without it: in the 16 floor-feasible units, no prespecified-margin gain was found beyond the declared input baselines under this split at λ = 1e-3, and nothing is claimed about the information content of the state.
