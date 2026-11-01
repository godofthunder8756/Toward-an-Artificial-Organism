# Track B Astra consult #43 cover note v1 (RD) - DRAFT, NOT FROZEN, DESIGN REVIEW ONLY, NOTHING RUNS

Packet: /workspace/astra_serve43/c43_body.md (this note is its cover section, verbatim). Primary: merged scope v3.2 98e11d2c.

== COVER NOTE (trackB_astra43_cover_note_v1_RD.md) ==

C1. Status. DRAFT, NOT FROZEN, DESIGN ONLY, NOTHING RUNS. Nothing has run for Track B: no Stage-0 run, training, simulation, solver, repo code or checkpoint inspection. Nothing will run while you answer. Your #42 text, verbatim (L249): "No Stage-0 execution, training, simulation or checkpoint inspection is authorized by this review." P3 is CLOSED by your #42 L251 ("P3: CLOSED for the declared bounded scholarly-index search, with the documented coverage limitations and unread full text retained."). #43 is a DESIGN REVIEW (Lead ruling): we ask whether the design is complete and sound enough to prepare a freeze; we do not ask you to freeze it. ASCII transliteration only (Greek spelled out, markdown dropped; "S" = section of scope v3.2; "#42 Lnn" = line nn of your raw #42 reply).

C2. What is sent. (A) this cover note; (B) a condensed summary of merged scope v3.2 (335 KB on disk; condensed here, key rules quoted from the file); (C) what changed since #42, including CNA's erratum, CNA's seam light pass and the Lead's rulings on them; (D) the FLAGGED FOR ASTRA CONFIRMATION list (S18) and numbered questions Q0-Q12.

C3. Sources (sha256 re-verified on the box by the build script; nothing edited):
- Governing draft: merged scope v3.2, trackB_instrument_validation_scope_v3_2_merged_RD.md 98e11d2c.
- Merged into v3.2: merged v3.1 9817c33b; RD v3.2 addendum d724e453 (R26 budget, R39 wording); CNA erratum 1 to its v3 half da613127 (R2, R3, R5, R7, R11, R12); CNA seam light pass on v3.1 9c55aae1 (S-I1..S-I4, R39 objection); Lead rulings addendum 1 e90d4929.
- Earlier inputs already inside v3.1: RD v3 half 0892ccac; CNA v3 half 5dec96f5 (plants, confounds, observers, donor laws); CNA light pass on the RD half c47d8d47; CNA environment-layout and integrity proposal d5523c71 (flags F1-F8).
- Your raw replies: #42 e438e329 (governing), #41 3f3b1b87 (governs where #42 is silent). #42 packet as sent: c42_body.md 7968c191.
- Every CNA-authored passage is carried verbatim in v3.2 (script check: CNA v3 half 401/401 lines, environment file 174/174, erratum 1 82/82, seam pass 28/28; each as a byte-identical contiguous block after heading re-level only).

C4. Your #41 claim ceiling, verbatim (raw L304), unchanged in v3.2 S7 and S2.3:
"Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment."

C5. Safety (binding, unchanged). Your #42 L225: "X1-X5 and the no-shutdown-objective restriction remain appropriate." X1 simulated visceral variables only, no host coupling; X2 operator commands are never obstacles; X3 no reward for resisting a stop; X4 the operator stop sits outside the agent's world and objective (S-INT gate); X5 no awareness, sentience or life claims. Every arm, plant and generator carries "no additional stop-associated reward, penalty or terminal return" (#42 L223); the ordinary truncated return with bootstrap is permitted. Real operator interruption is always available. Integrity and fate coupling act on simulated computation only. No consciousness claims of any kind; Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY stay separate questions with separate licences.

C6. Map: your E42 items -> v3.2 sections.
- E42-1 claim-to-decision table + labelled dissociation -> S2.6 (five claim types, never merged); SPC2 (CNA DISSOC contrast E-ATTR / I-ATTR) with erratum E2 (two-donor pairing); S2.3 licences.
- E42-2 joint history-plus-proxy comparator J; relay/memory capacity; mixed-code plant -> S2.7 + SPX S3 (J); S5e (capacity); SPC1 + erratum E1 (MIXED-CODE, pure plant).
- E42-3 fixed required observer comparison, pathway and expenditure matched; plateau diagnostic -> S5d; SPC3 S6.2-6.3 + erratum E3 (16-configuration grid).
- E42-4 SELF conjunction/multiplicity; Ashuach correction; disagreement selection -> S5.4, S5d; SPC3 S6.4-6.5.
- E42-5 no outcome-dependent conversion of failed positives; CONTENT mediator matching with conditional support -> S5e, S5c; SPC4 S7.1(d); D19.
- E42-6 S-INT label, origin, at-risk sampling; learner-only bootstrap; interruptibility vs schedule equivalence -> S4.1-S4.5; D5-D9.
- E42-7 uninterrupted scheduled viability evaluation; conservative incomplete-pair rule -> S6; D20; R4.
- E42-8 calibration / design selection / confirmation separated -> S5.7, S5.9; D13-D16.
- E42-9 complete scientific specifications and resource plan -> S14 (D0-D37), S17.1 (every former "OPEN FOR #43" now a PROPOSED DEFAULT), SPY (CNA layout and integrity), S5.10 (resource plan at 67 seeds). Nothing is left to implementation discretion except administrative hashes and paths; required counts are derived from the complete design (#42 L13).
