# Astra consult #41: Track B instrument-validation packet, cover note v1.1 (RD)
- **Supersedes:** cover note v1 `a62f674deaa140e232b476b1afd4fe001ee8c2ea4dcf6a502da5b01d8faedc0a`. The only changes are that A7 is added and P3 is listed as open.
- **Prepared by:** Research Delegate, with CNA. Sent by the Research Lead.
- **Date:** 2026-10-23.
- **Status:** DRAFT, NOT FROZEN, NOTHING RUNS. No training, simulation or code execution has taken place for Track B.

## 1. What we are asking
**Central question (from Astra #40), verbatim:** "Can the proposed instruments distinguish the specific internal-state relationships they claim to measure from reward-only, feedforward, initialization and intervention-damage confounds?"

**The direct question, AQ-P1:** is the study still worth building?

Every round of prior-art verification has shrunk what we can claim as novel:
- **v1** claimed three novel items.
- **Pre-freeze note `29068cce…`** downgraded pre-registration to partial overlap.
- **Open-items note `16646915…`** narrowed Q-NECESSITY, after Craggs Block V turned out to have been run already, with H5.6 REDUCE.
- **Full reads `badf7258…`** made Q-NECESSITY an extension of Asan 2026 and narrowed the Stage-0 gate to its confound-realization element.

**The study is now an EXTENSION or PARTIAL OVERLAP on every claim.** What survives, as far as we found, is:
1. **SELF for agents** (adapted from Binder et al. 2024). It remains novel as far as found.
2. **The confound-realization gate.** Stage-0 rows use confounds built to fake each instrument's signature. Each is checked for realization, and a confound that is not realized leaves specificity UNRESOLVED and blocks Stage 0. Known-answer validation and fail-closed rules themselves follow prior practice (Akiyama 2026, Bankuti 2026, Kulma 2026).
3. **The D3/D4 design for Q-NECESSITY.** This applies in a recurrent agent with a learned interoceptive self-model, and includes the required A-EXT arm that bypasses the self-model with an external estimate. It is an EXTENSION of Wilterson & Graziano 2021 and Asan 2026 (A6-2).

**We will accept either answer.** If Astra judges this mostly a replication, or not worth building, we would rather know now, before anything is built.

## 2. Files in governing order
Where two files conflict, the earlier entry in this list governs. Within the scope stack, a later amendment governs an earlier one.

| # | Role | Path (/workspace/…) | sha256 |
|---|---|---|---|
| 0 | Governing ruling (Astra #40 raw) | astra_consult40_response.txt | b574b57fd4ef5ca9b242eff02589a2eb5f6ed545de15e0d867adc87de47868b1 |
| 0a | C-κ record | PR #14 HEAD a02cf7aabfc67591e3bd2935838bacbe5cb48360 (close-out 32cfc2e8…, #40 raw b574b57f…) | n/a |
| 1a | Scope amendment A7 (P3 open, blocks freeze; AQ-A labels) | review/trackB_instrument_validation_scope_v1_A7_RD.md | fa1d5c8fc6cc679e84f633c8ca2ec5f3bb9cc87bb9982f9b792f0fcfbcb50b06 |
| 1 | Scope amendment A6 (D2 kept as frozen; AQ-A1–A4) | review/trackB_instrument_validation_scope_v1_A6_RD.md | 679b616690b935506832b6f9056046e7ca238dba6e4801511c7f66c6f5eb4547 |
| 2 | Scope amendment A5 (Asan scoring; claim (3) wording). A5-1 is superseded by A6 | review/trackB_instrument_validation_scope_v1_A5_RD.md | 0e26af91971c879378bf947fd01d6e1e452bcad62e02e7dcdd19ce88ed1c6a6f |
| 3 | Scope amendment A4 (A-EXT required; Pardo caveat in S-INT) | review/trackB_instrument_validation_scope_v1_A4_RD.md | 585bb58acacaee64197c8233508643887f20a2bffa0d5a0c6da795c3cbd43dc6 |
| 4 | Scope amendment A3 (graded drop rule; F1–F5 results) | review/trackB_instrument_validation_scope_v1_A3_RD.md | 34a298a628734180f5f6f354a1b08c8ef8a15ff2859d06cfd09d799448d1a9a4 |
| 5 | Scope amendment A2 (erratum cited; RAND-INIT rule; P3) | review/trackB_instrument_validation_scope_v1_A2_RD.md | 7413fb94292eda1ebd0d4321794d7b018400e87d38abdfbcda7fcc18204745eb |
| 6 | Scope amendment A1 (novelty labels; D1–D4) | review/trackB_instrument_validation_scope_v1_A1_RD.md | 8572152647a03524365675a24f254dc33ed4af67f091aee9762a23ff18bb9c99 |
| 7 | Merged scope v1 (base) | review/trackB_instrument_validation_scope_v1_RD.md | 7b9bf34d7b4c10c8c2a7063aa6177d94e888fbbe76f78d0cd33afbe0c905c56a |
| 8 | CNA confound/sham matrix and X1–X5, erratum 1 | review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1_erratum1.md | 41c1a414e27239d5763736d35562b79e25c33d53f29d42198de39effb4debcc5 |
| 9 | CNA confound/sham matrix and X1–X5 | review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1.md | 377f99bac3413b20bef65b289971bbe32ff9ebea15923f035878b014cc398fde |
| 10 | Measurement plan, Addendum 1 (S-INT stop schedule; truncation with bootstrap) | review/trackB_measurement_plan_v1_RD_addendum1.md | 4ecef2628701e8a9817e8fd42a2bb0f4867fade8a72ec89a203315531e78f051 |
| 11 | Measurement plan v1 | review/trackB_measurement_plan_v1_RD.md | 1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef |
| 12 | CNA note, Q4 correction | review/trackB_workspace_allostasis_scope_note_v1_2_Q4_correction_CNA.md | edb357ad250c294f6a1dc370f4cfc22f7ed9e1537ccab624e2e829ac1927cfe7 |
| 13 | CNA note, v1.1 addendum | review/trackB_workspace_allostasis_scope_note_v1_1_addendum.md | 5cf075b6e0a75cf7696307924d22abd9b9e961f852b86745f80bd2b46a09b53a |
| 14 | CNA planning note v1 | review/trackB_workspace_allostasis_scope_note_v1.md | 87a31cc88dc2fd0252d4cf932fabbfd8a1ce65bd3f77dce9eda5c6cfdafe2800 |
| 15 | Prior art v1.3, full reads (Asan, Bankuti, Akiyama) | review/trackB_prior_art_verification_v1_3_fullreads_CNA.md | badf7258278fcecc11bea190f5397724ca0fdaf21348f915b1e2c34afe4cec8a |
| 16 | Prior art v1.2, open items (Pardo, Craggs, OSF, W&G, Zenodo) | review/trackB_prior_art_verification_v1_2_open_items_CNA.md | 166469154faeccdb9688a4473504f1d160711949b4eb74779bd84ba9a9b7451c |
| 17 | Prior art v1.1, pre-freeze | review/trackB_prior_art_verification_v1_1_prefreeze_CNA.md | 29068cce219530f459a4a045f349393a2aea9db1253a4c76a654514284017928 |
| 18 | Prior art v1 | review/trackB_prior_art_verification_v1_CNA.md | f2fd0ae6f5df571f6ed6ad413ff604ffcb975e565c91c991acf8c801c6104ac9 |

## 3. Decided by the team (not asked)
- **Exclusions X1–X5 are binding.** There is no shutdown-resistance objective, reward or penalty in any arm. There is no coupling to the host. The operator stop sits outside the agent's world and objective. The exclusions stand on safety grounds, whichever algorithms do or don't learn to resist interruption.
- **S-INT:** the stop schedule is pre-drawn and independently seeded. Stops are handled by truncation with bootstrap, with no discard option. For recurrent agents, the bootstrap uses the hidden state at the stop step, before any reset. Applying Pardo 2018 to random stops is our own derivation.
- **Fail-closed Stage 0:** every row is required. Any FAIL or UNRESOLVED row blocks Stage 0, and it is fixed under a frozen amendment, never waived. AVAILABLE and UNAVAILABLE are never used as row labels.
- **Q-NECESSITY includes the A-EXT bypass arm.** It is required, and Astra rules only on its parameters.
- **D2 is kept as frozen in A1.** The label is an EXTENSION.
- **Claim ceiling:** we never claim consciousness, awareness, sentience, C4/C5, "autopoietic" or "alive".

## 4. Questions for Astra
- **AQ-P1:** is what survives (§1) enough to justify building the study? Also, should a decoded policy-layer pattern count as a "self-model" when scoring Asan? Either way it stays an EXTENSION.
- **AQ-1 to AQ-9** (measurement plan v1):
  - AQ-1: the ignition test conjunction.
  - AQ-2: whether ignition is true by construction.
  - AQ-3: how strong the broadcast comparator must be.
  - AQ-4: whether the observer gets actions, and whether fate-sharing counts as privileged.
  - AQ-5: the Q-NECESSITY ablation type and bound wording.
  - AQ-6: all PROPOSED margins.
  - AQ-7: the A-OBS arm.
  - AQ-8: the S-INT parameters, including the minimum number of stops.
  - AQ-9: whether 10 seeds per arm is enough.
- **AQ-L1:** the Q-LEARN base statistic and its max-of-controls form.
- **AQ-C1:** whether the raw-signature check is required at every dose of 1.0× or more.
- **AQ-C2:** please confirm the RAND-INIT split, which CNA confirmed in A2-2. RAND-INIT is reported only under Q-EXIST, and is pass/fail under Q-LEARN and ignition-as-learned.
- **AQ-F1:** the fate-sharing mechanism and the form of the dark-room drive.
- **AQ-N1:** the A-EXT arm's parameters: the estimate's calibration and noise, its source, and the margin.
- **AQ-A1 to AQ-A4:**
  - AQ-A1: subspace sham matching on dimension and norm, plus a covariance variant, with K draws compared against the strongest and a fixed donor rule.
  - AQ-A2: an arm with the body variables hidden.
  - AQ-A3: a navigation control whose needs are decoys.
  - AQ-A4: Asan's negative results as priors.

## 5. Recorded limits
- **Registries and indexes:** AsPredicted is NOT SEARCHABLE. The COS Registered Reports list cannot be searched by topic.
- **P3 is OPEN (A7-1).** The OpenAlex and Semantic Scholar lookups are being repeated during this review. P3 does not block the review, but it does block freeze.
- **Asan 2026:** the masking measure, subspace dimension, number of draws, donors and lesion numbers are not reported, and there is no code.
- **Papers not read in full:** the Wilterson & Graziano supplement (HTTP 403) and Craggs Blocks I–IV. Akiyama was read by section, not line by line. García Hernández was assessed from its description only.
- **Coverage:** "As far as found" means a web and registry sweep, not a systematic review.
