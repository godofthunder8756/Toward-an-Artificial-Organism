# Close-out

The line is CLOSED. All frozen labels are unchanged: all 23 units are m0/b10/x0/u0/i0. C1 met the floor in 89/230 and C2 in 0/230. There will be no rerun and no floor, split, probe or lambda search.

Source: Astra consult #34, 2026-10-21. Raw response: `review/astra_consult34_response.txt`.

sha256: `bf724ca23385e9577dbe4ecd97362e40d67d9caacb6b8cbeac0cee4eb12632a9`

## CLOSE-OUT text

> "CLOSE-OUT: GRU hidden-state oracle-accessibility audit v1.3. The frozen analysis reports quota not attained in all 23 (PR, arm) units, each with m=0, b=10, x=0, u=0 and i=0. C1 met its floor in 89 of 230 TRAINED checkpoints; C2 met its floor in none. These labels remain unchanged.
>
> "Post-run arithmetic establishes that 70 checkpoints in seven units had baseline losses below the floor in both comparisons, making a meets-floor outcome unattainable. Their below-floor classifications do not discriminate accessibility once this constraint is known. In the remaining 160 checkpoints across 16 units, the elementary feasibility bound permitted success, but no checkpoint achieved the prescribed C2 improvement under the frozen procedure.
>
> "All 290 roster records passed their applicable integrity checks. Forty records retain SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED. PR #5 remains MISSING PERSISTED CHECKPOINTS; NOT EVALUATED. The consistency-check deviation, its additive resolution, report corrections and timing/provenance qualifications remain attached.
>
> "This closes the present own-error/oracle-accessibility audit branch. No threshold retuning or further decoder search is proposed. Earlier causal findings remain unchanged. No acquisition, assessment, causal-use, necessity, C4 or consciousness conclusion is added."

## Claim ceiling

> "The audit establishes the reported held-out decoding losses and gains for the specified checkpoints, domain, splits, features and regularization. It shows a prescribed-margin C1 improvement in 89 TRAINED checkpoints and no prescribed-margin C2 improvement. It does not establish absence of accessible information, absence of assessment, or equivalence across representations or procedures. No C4 evidence or status row changes."
