# Track B instrument-validation scope v1: Amendment A5 (additive; RD)
- **Amends:** v1 `7b9bf34d…`, A1 `85721526…`, A2 `7413fb94…`, A3 `34a298a6…` and A4 `585bb58acacaee64197c8233508643887f20a2bffa0d5a0c6da795c3cbd43dc6`. All are unchanged, and A5 governs wherever they conflict.
- **Inputs:** CNA's full-reads note `/workspace/review/trackB_prior_art_verification_v1_3_fullreads_CNA.md` (sha256 `badf7258278fcecc11bea190f5397724ca0fdaf21348f915b1e2c34afe4cec8a`), and the Lead's D2 ruling in the room, 2026-10-23, about 11:00 ET.
- **Status:** DRAFT, NOT FROZEN, NOTHING RUNS.

## A5-1. D2 defined (closes G3; supersedes the A1-2 wording)
D2 is "the self-model is learned by the agent, not supplied or hand-coded". This follows the Lead's ruling, on the ground that the claim adopted from `f2fd0ae6…` before any full read already said "a learned interoceptive self-model". The A1-2 wording, "the agent is a learned RL agent", is recorded as drift.

**The stricter reading is reported alongside, as the Lead directed.** Under the A1-2 wording, D2 fails against Wilterson & Graziano 2021 (DQN) and Asan 2026 (PPO), which makes Q-NECESSITY an EXTENSION.

## A5-2. Asan 2026 scored on D1–D4 (badf7258 Part 1)
- D1 (interoceptive content): DOES NOT HOLD.
- D2 (the self-model is learned by the agent): DOES NOT HOLD. Asan's affect variables are decoded from a learned policy layer.
- D3 (viability outcome): HOLDS with a caveat, because the measure behind 82%→10% under input masking is not named. If that measure is survival, D3 fails.
- D4 (same-size ablations of other modules and matched arms): HOLDS.

**Consequence:** D1 and D2 fail against Asan under both readings of D2. Q-NECESSITY is therefore an **EXTENSION whichever reading of D2 is adopted.** The D2 reading changes the score against Wilterson & Graziano only, not the label.

The differences that survive, to be named in the text:
- Against Asan: D3 (a viability outcome, with the caveat above), and D4 (same-size ablations of other modules plus a sham, and the required A-EXT bypass arm from A4-1).
- In addition: our agent is recurrent, while Asan's is feedforward. This is stated as a difference, not added as a criterion.
- Against Wilterson & Graziano: D1, D4, and, under the Lead's reading of D2, a self-model that is learned rather than supplied.

Q-EXIST and Q-CAUSE are EXTENSIONS of Asan 2026.

## A5-3. Claim (3), final wording (adopts badf7258 §2.8)
"a Stage-0 gate for this instrument battery in learned RL agents whose rows include confounds built to fake each instrument's signature, each checked for realization, with an unrealized confound leaving specificity UNRESOLVED; known-answer validation and fail-closed decision rules follow prior practice (Akiyama 2026; Bankuti 2026; Kulma 2026)."

Label: PARTIAL OVERLAP. The confound-realization element survives as far as found, with Akiyama §2.5 as the nearest precedent.

## A5-4. Novelty summary for the cover note (AQ-P1)
| Item | v1 label | Current label |
|---|---|---|
| Q-NECESSITY | NOVEL | EXTENSION (Asan 2026, Wilterson & Graziano 2021, Craggs 2026 Block V, Phua 2025) |
| SELF for agents | NOVEL | NOVEL AS FAR AS FOUND |
| Stage-0 gate | NOVEL | PARTIAL OVERLAP. Only the confound-realization gate survives (A5-3) |
| Pre-registration | (part of item 3) | PARTIAL OVERLAP (Craggs, Faeth) |

What survives, as far as found:
- SELF;
- the confound-realization gate;
- Q-NECESSITY's D3/D4 design in a recurrent agent with a learned interoceptive self-model and the A-EXT bypass.

AQ-P1 asks Astra whether that is enough to justify the study.

## A5-5. CNA design suggestions, for Astra to rule on (not adopted)
- **AQ-S1:** random-subspace sham controls matched on dimension and norm, plus a covariance-matched variant. K draws, compared against the strongest, with a fixed donor rule.
- **AQ-S2:** an input-hidden body-variable arm, using Asan's no-memory decoding result (R² 0.06–0.08) as a Stage-0 known-answer case.
- **AQ-S3:** a navigation control agent with the same senses but needs that don't affect its reward.
- **AQ-S4:** Asan's negative results cited as priors for the confound rows.

## A5-6. Freeze status
**Closed:**
- G1 (full reads of Bankuti and Akiyama);
- G2 (full read of Asan);
- G3 (the D2 definition, A5-1).

**Still open:** P3, repeating the OpenAlex and Semantic Scholar lookups (owner: CNA). The Lead decides whether P3 blocks freeze.

**Recorded limits:**
- Asan does not report its masking measure, subspace dimension, number of draws, donors or lesion numbers, and its code isn't available.
- Akiyama was read by section, not line by line.
- The Wilterson & Graziano supplement and Craggs Blocks I–IV were not read.
- AsPredicted is NOT SEARCHABLE.
