# Track B instrument-validation scope v1: Amendment A3 (additive; RD)
- **Amends:** v1 `7b9bf34d7b4c10c8c2a7063aa6177d94e888fbbe76f78d0cd33afbe0c905c56a`, A1 `8572152647a03524365675a24f254dc33ed4af67f091aee9762a23ff18bb9c99` and A2 `7413fb94292eda1ebd0d4321794d7b018400e87d38abdfbcda7fcc18204745eb`. All three are unchanged.
- **Inputs:** CNA's v1.2 open-items note `/workspace/review/trackB_prior_art_verification_v1_2_open_items_CNA.md` (sha256 `166469154faeccdb9688a4473504f1d160711949b4eb74779bd84ba9a9b7451c`), and the Lead's gap ruling in the room, 2026-10-23, about 10:53 ET.
- **Status:** DRAFT, NOT FROZEN, NOTHING RUNS.

The erratum citation (`41c1a414…`) and CNA's AQ-C2 sentence are already in A2-1 and A2-2.

## A3-1. Drop rule: gap closed (replaces the referral clause in A1-2)
Any result short of all four of D1–D4 failing is an EXTENSION, including results where D1 fails. The text must name which differences survive. A REPLICATION requires all four to fail. This needs no Astra ruling.

## A3-2. F1 Pardo 2018: SUPPORTS WITH CAVEATS
Eq. 6 bootstraps at terminations that the environment did not cause. Applying that to independently seeded random stops is our derivation; Pardo itself tests fixed time limits only. Pardo may be cited as support only with that statement attached.

**New S-INT requirement:** for recurrent agents, the bootstrap target at a stop is computed from the agent's hidden state at the stop step, before any reset. A code-audit item checks this.

The other caveats are already covered: stops independent of state (Addendum 1 A1-1) and stops not predictable (the probe-AUC audit). The safety basis remains Orseau & Armstrong 2016 and Leike et al. 2017.

## A3-3. Difference-by-difference results (CNA v1.2)
- **Craggs 2026 Blocks I–V.** The agents are fixed hand-written rules and the self-model is a competence estimate. D1, D2 and D3 HOLD, and D4 HOLDS narrowly (cite S4, the capacity-matched non-self monitor). **Correction to A1-1:** Block V has been run. Results were posted on 15–16 Oct 2026: H5.6 (necessity) was REDUCE, because an externally supplied calibrated estimate came within 0.006–0.007 utility of the agent's own monitor.
- **Wilterson & Graziano 2021.** A DQN agent with an experimenter-supplied attention schema. See A3-4.
- **Zenodo partial overlaps to cite:** Valerio Porras 2026, Asan 2026, García Hernández 2026, and Bankuti, Akiyama & Kulma 2026.

## A3-4. OPEN FOR THE LEAD: what D2 means
A1-2 defines D2 as "the agent is a learned RL agent". Wilterson & Graziano 2021 also uses a learned RL agent (DQN), and so does Asan 2026 (PPO). Under the A1-2 wording, D2 therefore does NOT HOLD against either one, and the A3-1 rule makes Q-NECESSITY an EXTENSION.

CNA's verdict of "still novel" (v1.2 L224, L238) holds only if D2 means "the self-model is learned by the agent", not supplied or hand-coded.
- If the Lead adopts that reading, D2 is redefined that way and both papers are re-scored against it.
- Otherwise, Q-NECESSITY is labelled EXTENSION, and the text names the surviving differences: D1 interoceptive content, and D4 against W&G.

Asan 2026 has not been read in full, only keyword-searched. It uses lesions matched to random subspaces and masks interoceptive input, so it may also bear on D1 and D4. A full read is therefore needed under either reading of D2.

## A3-5. Proposed for the Lead: AQ-N1
Proposed new Q-NECESSITY arm: replace the learned interoceptive model with an externally supplied, calibrated interoceptive estimate of the same dimension. This is the bypass that reduced Craggs H5.6. Q-NECESSITY could not read MET if the bypass agent comes within the frozen margin of the full agent. Whether this goes to Astra as AQ-N1 is the Lead's call.

## A3-6. Third novelty item: further narrowed (pending the Lead's adoption)
Known-answer instrument validation has precedent (Bankuti, Akiyama & Kulma 2026). The claim that survives is this Stage-0 gate for this battery of instruments, with confounds that can fake each signature and the fail-closed UNRESOLVED rule. Plain known-answer gating is PARTIAL OVERLAP.

## A3-7. Freeze-blocking items, updated
**CLOSED:**
- F1, with the caveats in A3-2;
- F2;
- F3;
- F4, except the supplement (HTTP 403);
- F5, for Zenodo. PCI RR returned nothing, and the COS Registered Reports list cannot be searched by topic.

**OPEN (owner: CNA unless noted):**
- G1: full reads of Bankuti 2026 and Akiyama 2026;
- G2: a full read of Asan 2026, needed for A3-4;
- G3: the Lead's ruling on what D2 means (A3-4);
- G4: the Lead's decision on AQ-N1 (A3-5);
- G5: the Lead's adoption of A3-6;
- P3: repeat the OpenAlex and Semantic Scholar lookups.

AsPredicted stays NOT SEARCHABLE. Craggs Blocks I-B1 to IV, the García Hernández full text, and the W&G supplement are recorded as not read.
