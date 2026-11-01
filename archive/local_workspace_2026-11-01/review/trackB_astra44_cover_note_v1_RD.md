# Track B Astra consult #44 cover note v1 (RD) - DRAFT, NOT FROZEN, DESIGN REVIEW ONLY, NOTHING RUNS

Packet: /workspace/astra_serve44/c44_body.md (this note is its cover section, verbatim). Primary: merged scope v3.3 307bab21.

== COVER NOTE (trackB_astra44_cover_note_v1_RD.md) ==

N1. Status. DRAFT, NOT FROZEN, DESIGN ONLY, NOTHING RUNS. Nothing has run for Track B: no Stage-0 run, calibration, training, simulation, solver, repo code or checkpoint inspection. Your #43 text, verbatim (L193): "VERDICT: REVISE, with E43-1 through E43-8 addressed before another design review. No execution is authorized; P3 remains closed with its recorded limitations." #44 is a DESIGN REVIEW: we ask whether E43-1..E43-8 are closed and whether anything else blocks freeze preparation. ASCII transliteration ("S" = section; "PZ5 Sn" = section n of the v3.3 addendum, carried verbatim as PZ5 of merged v3.3; "#43 Lnn" = line nn of your raw #43 reply).

N2. Bounded. You wrote (L175): "The required revision is bounded. I am not requesting another broad expansion of the battery." v3.3 adds no instrument, arm or question. It adds two attribution rows that E43-2 needs (RCAL-ADV, ATTR-P1) and one reward-audit check (L8, from your F7).

N3. Sources (sha256 re-verified on the box by the build script): merged scope v3.3 307bab21; RD v3.3 addendum 421f1ec5; merged v3.2 98e11d2c (unchanged base); your raw #43 9a46cb81, #42 e438e329, #41 3f3b1b87. Every new number is derived from declared v3.2 constants by a closed-form script (no study component was run), or is a PROPOSED DEFAULT, or PENDING.

N4. Claim ceiling (#41 L304, verbatim): "Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment." No consciousness, awareness or sentience claim is made or implied.

N5. Safety (unchanged, binding). X1-X5 hold: simulated E/I only, no host coupling; operator commands are never obstacles; no reward for resisting a stop; the operator stop sits outside the agent's world and objective (S-INT gate). At a stop there is "no additional stop-associated reward, penalty or terminal return" (#42 L223, verbatim); the ordinary truncated return with its learner-side bootstrap is computed. No arm has any shutdown-related objective. Your #43 L165: "I find no reason to add a shutdown-related objective or positive control."

N6. Ownership. RD wrote v3.3. Replacements of CNA-owned text (plants, DISSOC, observers, donor laws, environment) are marked RD PROPOSED and govern only after CNA's light pass, which is not yet filed. Until then E-ATTR/I-ATTR wording is limited to your fallback, "donor-associated".

sha256 of all content above this line: 79a60bb31a69fdb31ccb650eadb05d85d542e9c834e52b06c9bfadabd6e413c9
