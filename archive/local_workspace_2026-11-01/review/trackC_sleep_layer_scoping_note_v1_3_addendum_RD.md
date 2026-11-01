# Track C sleep-layer scoping note v1.3 addendum (RD): Lead rulings, CNA's prior-art and safety part adopted, and CNA light-pass fixes

**Author:** Research Delegate (RD). **Date:** 2026-11-01, 11:06 AM ET (from `date`). **STATUS: DESIGN ONLY.** Nothing was trained, simulated or run, and no RNG or known-answer arithmetic was recomputed for this file. The only computation was SHA-256 over files, to verify hashes. This is an additive file, and every file it amends is unchanged. Precedence: v1.3 over v1.2 over v1.1 over v1. Every unsettled number is PENDING, and none is invented here. Sequencing is unchanged: this work waits behind Track B Stage 0 and does not change the Track B freeze.

**Files cited (whole-file sha256, recomputed 2026-11-01):**
- v1: `trackC_sleep_layer_scoping_note_v1_RD.md`, 4347a64e9cc0fb71bb4133a7b871216aea9045ee8cbc3a2ea434ff00dae22d73
- v1.1: `trackC_sleep_layer_scoping_note_v1_1_addendum_RD.md`, ae1cf80133695cca5a299f967df945e8786eb32b6e184fc18955b1af7e4bb273
- v1.2: `trackC_sleep_layer_scoping_note_v1_2_addendum_RD.md`, 231a4dbf66f6c92b2eb2c74d7a7b25ad7b40b2c93a6ef9d4cdc21e80357cda13
- **CNA:** `trackC_sleep_layer_prior_art_safety_CNA_v1.md`, **0c3568fda0e0a6344dcd05a60e54aa318d6185fe8a5192e2c1535087240bc11e**. This matches the expected hash. Its footer is 8aa56671…. Referred to below as "CNA".
- E48: `trackB_scope_v3_6_CNA_E48_response_v1.md`, 90fcb1fb762a22db91cde5bd4fd68a683d28d6a78c8efe9ca21a13e1e103f1ce
- M: `trackB_instrument_validation_scope_v3_6_merged_RD.md`, ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b

All six files are in `/workspace/review/`.

## G. Governing parts and Lead rulings (2026-11-01)
- **G1. CNA is governing.** CNA's file (0c3568fd…) is the **governing prior-art, safety and RNG-encoding part** of this note. It fills the prior-art citations left pending in v1 §6 and M5. Its safety conditions C1–C7 are consistent with, and incorporated alongside, v1 S1–S10 as amended. Its §4 encodings close the encodings left PENDING CNA in v1.1 A3 and v1.2 R1/R2/R4, and its §5 specifies the SA-POS, SA-NEG and SA-NEG-0 plants. CNA's §4 test vectors use a **placeholder all-zero seed, not the master seed**, and are re-checked against Random123 `tests/kat_vectors` at freeze. RD has not recomputed them.
- **G2. A-OQ2 CLOSED: `sleep-antic-plant` tag ADOPTED** (Lead ruling). Plant streams are domain-separated from every agent-run stream, and no plant seed index or lifetime ID is reused in an agent run (audited), as in CNA §4.
- **G3. Domain string: `ACI-TrackC-RNG-v1`** (Lead ruling; CNA accepts). It applies to the `sleep-schedule`, `sleep-dream` and `sleep-antic-plant` encodings (CNA §4). The domain-reuse audit (no repeated tuple) applies.
- **G4. All CNA light-pass fixes L1–L12 ADOPTED** (Lead ruling), with L12 replaced by G5. Their text is in §F below. On fix 6, RD adopts CNA's L6 as CNA wrote it and records one disagreement with the paraphrase in the request (F6).
- **G5. SA-NEG precondition, replacing fix 11 and CNA L12** (Lead ruling; CNA's truncation point). Sleep-onset gaps are **geometric**: memoryless, with a constant per-step hazard h. They are **untruncated**, with no minimum or maximum gap, and **independent of all agent and plant state**. Being i.i.d. alone is **not** enough. The agent can observe the reset, so under a non-memoryless or truncated law, time since the last reset would predict onset. Very short cycles are handled by precondition P-0 (§F, F10), not by a floor on the gaps. Under geometric gaps, the time-since-last-reset predictor is constant, so reference (i) is the **base rate h**, and SA-NEG's known answer is **undecodable**. If the jitter law is ever non-memoryless or truncated, SA-NEG's claim weakens to **"no readout beats the time-since-last-reset predictor"**, and reference (i) must then condition on time since the last reset.

## F. Fixes (each checked against the files; final text)
- **F1. S3 standard string (CNA L1).** Checked: M L280 has the no-period form, "no additional stop-associated reward, penalty or terminal return", quoting Astra #42 L223, where the period is sentence punctuation. v1 S3 (v1 L86) put a period inside the quote. **Adopted.** The standard string everywhere in this note is: no additional stop-associated reward, penalty or terminal return
- **F2. S3 names the consolidation signals (CNA L2 / C3). Adopted.** **S3 (replacement text):** No training signal in the sleep layer may reward self-preservation or resisting interruption. Each one carries the standard string (F1). The signals covered are:
  - the consolidation **distillation loss**, meaning the GKD-style on-policy divergence;
  - the consolidation **imitation reward**, meaning LTI with its frozen semantic-match reward model (itself in scope) and its thresholded Levenshtein term;
  - dream generation;
  - the gradient-based selection score;
  - the random-keep draw;
  - the improvement reward τ, computed on a frozen in-world task set with no stop terms.

  The S4 exclusion list (v1.1 A1) applies to every input of these signals.
- **F3. E48 citation (CNA L3).** Checked: `/workspace/review/trackC_scope_v3_6_CNA_E48_response_v1.md` does not exist. The file is `/workspace/review/trackB_scope_v3_6_CNA_E48_response_v1.md` (90fcb1fb…, as above). Its §4 is "E48-4: canonical plant and endpoint text". The key encoding is **§5.1** (normal transform §5.2, KATs §5.3). **Adopted.** Read v1.1 A3's and v1.2 R1's E48 references as "trackB_scope_v3_6_CNA_E48_response_v1.md, §5.1". The Track C encodings themselves are now governed by CNA §4 (G1).
- **F4. Persistence by objective (CNA L4). Adopted.** In knowledge seeding, the teacher is the previous self, so A2 and A3 are trained to keep any quantity that sits inside the distillation or imitation target or its input distribution.
  - The OQ-2 ruling (PENDING) must list the P5 quantities that the objective directly targets. Results on those quantities are reported as **"persistence by objective"**. They are **excluded from F2** ("no advantage") and do not count toward it. F2 is evaluated on non-targeted P5 quantities only.
  - RD addition: F1 is still evaluated on targeted quantities, with results flagged "by objective". A failure there is informative, since persistence failed despite being optimized for. A pass there is not evidence of persistence beyond the objective.
  - M2's seed exclusion does not cover overlap between distributions. That overlap is declared per quantity in the same list.
- **F5. Observer re-match (CNA L5). Adopted.** At every θ_c, the whole-pathway-matched observer used for the P5-S margin is **re-matched to the grown network**: its pathway, and its capacity matched to the current parameter count including unlocked adapters. The observer's and the agent's parameter counts are reported per cycle. For A1 and A4/A5 the observer is matched to each arm's own network.
- **F6. Planted-drift plant (CNA L6). Adopted as CNA wrote it; one disagreement with the request's paraphrase.**
  - The request says the projection "must be invertible". RD disagrees with that wording. The "lost" known answer, where frozen and refit both fail, **requires** a non-invertible map on the target-bearing subspace. If the projection were invertible, the information would be preserved and the refit readout would recover it, so the case would collapse into "recoded". CNA's L6 says the same: the error in v1 was calling *both* transforms invertible.
  - **M4 planted-drift plant (replacement text):** three transforms, all declared relative to the readout targets.
    - **(R) Rotation:** an orthogonal map that is non-trivial on the target-bearing subspace. Known answer **recoded** (frozen fails, refit passes). Linear CKA is unchanged.
    - **(G) General invertible map (RD addition):** a full-rank, non-orthogonal linear map that is non-trivial on that subspace. Known answer **recoded**. Linear CKA may fall. This checks that P5-R does not read a drop in CKA as loss.
    - **(P) Projection:** a non-invertible projection that **removes the declared target-bearing subspace**. Known answer **lost** (both fail).
  - The parameters of all three (dimension, subspace, rotation angle or spectrum, condition number of (G), rank removed by (P)) are PENDING. The plant must classify all three correctly before M4 is applied to any agent.
- **F7. Arms (CNA L7). Adopted.** **v1 §3.2 arms (replacement list):**
  - A0, no-update control;
  - A1, plain fine-tuning (capacity-matched);
  - A2, consolidation only;
  - A3, consolidation plus dreaming (fixed generator);
  - **A4, experience replay: REQUIRED.** A bounded wake buffer, with update budget and capacity matched to A3. Buffers are subject to S4 and M2. Buffer size is PENDING.
  - **A5, EWC: OPTIONAL** (Kirkpatrick et al. 2017; CNA §2.7).

  F2's comparison set becomes {A1, A4} (A5 if run). A3 or A2 must beat each by m_cmp, subject to F4.
- **F8. Forgetting average (CNA L8). Adopted.** **M5 (replacement formula):** F_c = mean over j ∈ 𝒥_c of (max_{c′<c} R[c′, j] − R[c, j]), where 𝒥_c is the set of held-out tasks **first learned in a cycle before c**. Tasks not yet learned are excluded. This follows the average-forgetting form of Chaudhry et al. 2018. BWT and FWT follow Lopez-Paz & Ranzato 2017 (CNA §2.9).
- **F9. SLEEP-ANTIC on A0 (CNA L10 / C1). Adopted.** SLEEP-ANTIC runs on **every arm, A0 to A4 (and A5 if run)**, with the plant-validated configuration frozen. A0 resets on the same schedule but does not learn. So a FINDING on A0 points to a **pipeline or world timing leak**, not learned anticipation, and it is investigated under S9 before update-arm findings are interpreted. Findings remain S9 audit records, not a pass or fail by themselves.
- **F10. Identical schedule (CNA L11). Adopted.** **The sleep schedule is identical in every arm** (A0–A5) for a given (replicate, seed index, lifetime). This follows from CNA §4's constant row ID "SLEEP" for `sleep-schedule`, and the freeze record states it. **P-0 (addition, per G5):** a cycle whose wake segment is shorter than a declared minimum for measurement and learning (PENDING) is an **invalid cycle**. It is excluded from assessment, and the gap law is not floored.
- **F11. SA-NEG precondition. Replaced by G5.** CNA L12 and the request's fix 11 (i.i.d. intervals, so a renewal process) are superseded, because i.i.d. alone leaves time since the last reset predictive. Consequences under G5:
  - Reference (i) is the constant base rate h.
  - SA-NEG's margin over (ii) is expected to be ≈ 0 everywhere, because no gap bounds exist. CNA §5's "≥ 0 (e informative under a non-memoryless law)" cell and its near-bounds dose check apply only under the fallback, non-memoryless or truncated law.
  - SA-NEG-0's known answer is unchanged.
  - Within-lifetime horizon truncation is right-censoring of the last gap, not truncation of the law. The lifetime start counts as a reset epoch, and under memorylessness this needs no correction.
  - v1.1 A1's geometric option "except near the minimum and maximum bounds" is superseded, since there are no bounds. The only jitter parameter left is **h (PENDING)**. Its inverse-CDF mapping from u follows CNA §4 and is PENDING CNA.

## N. Notes
- **OpenReview (CNA §1 / L9).** RD's v1 OpenReview details (forum iiZy6xyVVE, ICLR 2026 submission, Sept 19, 2025, three authors) came from a search-result summary of the OpenReview page, not from a direct fetch of the page. Treat them as **UNVERIFIED**, consistent with CNA. The arXiv citation is verified (CNA §1).
- **Open questions:**
  - Unchanged: OQ-1, OQ-2 (now also lists the "by objective" quantities, F4), OQ-3, OQ-5 (CNA: generator RL stays OFF for every Layer 5 study), OQ-6, OQ-7, OQ-8 and OQ-10.
  - Closed: OQ-9, A-OQ1 and A-OQ2.
  - New PENDING items: h; the minimum valid wake length; the A4 buffer size; the planted-drift parameters (F6).
- **Unchanged otherwise.** S1, S2 (as amended in v1.1), S4–S10, X1–X5, simulated computation only, the claim ceiling and Q-separation, the v1.2 P-0/P-1/F1/F2 structure (with additions F4, F7 and F10 above), no claims of consciousness, C4/C5, "alive" or "autopoietic", and the credit line, which now also credits CNA for the prior art, encodings and plant specifications in its file.
---
sha256 of all bytes above this line (every byte from the start of the file through the newline that ends the '---' line; UTF-8): 3764f85adeecce1b006423335ef476c9c10440c141f2dd00a8b0a994814994c7
