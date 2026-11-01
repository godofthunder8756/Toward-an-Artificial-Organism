# Light conformance pass on scope v2 (RD half), by CNA, v1

CNA, 2026-10-23, about 12:42–12:50 PM ET. **Read-only and additive.** It edits nothing and runs nothing: no training, simulation, stages, wrapper, static_checks or repo scripts. The only commands used were sha256sum, grep and sed reads. Design-only review. It authorizes nothing.

- **Target:** `/workspace/review/trackB_instrument_validation_scope_v2_RD.md`, sha256 `166370c1435bdab6734aec869c94770fb8a88214066082b3a4e3996dbce13b40`. Its internal footer `111f163b…` reproduces (`head -n -1 | sha256sum`). "RD Lnn" below means a line in this file.
- **Governing text:** `/workspace/astra_consult41_response.txt` (`3f3b1b87…`), read in full, L1–L304. "#41 Lnn" means a line there.
- **Companion:** CNA v2 file `trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` (`17832b01…`, footer `b666b1d7…` reproduces). "CNA Lnn" means a line there.
- **Ownership:** CNA owns scope conformance, hashes and the manifest. Code paths and stop/exit logic (item 4) are the Delegate's, so they get a light pass only.

## Overall verdict

**CONFORMS WITH MINOR EDITS: 1 ISSUE (wording, one-line fix) and 12 MINOR.** No safety exclusion is broken. The ceiling is verbatim, every cited hash matches the file on disk, and nothing from #41 is dropped. Most of the MINOR items are merge reconciliation between the two halves. Three of them are fixes to CNA's own file (M8, M9, M10), and they go into a CNA additive erratum, not into RD's file.

| Check | Verdict |
|---|---|
| (a) Every #41 item answered or pointed | CONFORMS (M1, M2) |
| (b) Ceiling sentence equals #41 L304 | CONFORMS |
| (c) Item 2: dependence vs substitutability, A-EXT veto | CONFORMS (M3) |
| (d) Item 4: stop spec, plus the safety exclusions | MINOR (M4, M5) |
| (e) Item 5: nested fits, multiplicity, seeds | CONFORMS (M6) |
| (f) Item 6: viability scoring | MINOR (M7) |
| (g) Number provenance | MINOR (M11) |
| (h) Placeholders vs the CNA file | ISSUE I1; MINOR M2, M6, M8, M9, M10, M12 |
| (i) Hashes | CONFORMS (M1: stale PENDING, v1.6 missing) |

---

## (a) #41 item coverage: CONFORMS

RD §8 (RD L308–339) has a row for every item: AQ-P1, AQ-1 to AQ-9, L1, C1, C2, F1, N1, A1–A4, SELF1 (marked as not in the packet), the six §20 parts, the ceiling and P3. Spot-checks against the raw text:
- AQ-1: the RD L190 bullets match #41 L29–32.
- AQ-5: the matched family (RD L130) matches #41 L82–89 verbatim, and Q-CAUSE alignment (RD L142) matches #41 L93.
- AQ-6: all 14 rulings in RD L208–221 match the #41 L101–114 text. L104 differs only in nested quote style.
- AQ-8: all seven bullets of #41 L138–148 appear in RD §4.
- AQ-L1: per-seed averaging, the three "acquired" conditions and the shuffle replacement match #41 L160–172.
- AQ-N1: primary source, secondary estimator, interface, freeze list, compatibility, and the 3-way rule match #41 L212–228.
- §20: parts 1 to 6 map to #41 L264–296.

The A-items and SELF1 point to the CNA file, which covers them (CNA §3, §4).

- **M2 (shared gap).** #41 L281 asks for "Redundant **and distributed** representations." RD L113 hands this to CNA. CNA covers redundancy (CN-NC1, CNA L161) but has **no distributed-code row**. **Fix (CNA erratum):** add a DISTRIBUTED row under C-CAUSE and C-NEC, with E spread over many low-variance directions. It would challenge single-direction edits and single-block ablation, take dose = number of directions, and be motivated by AQ-A4 L256 "distributed-code controls".
- Internal note: RD L9 assigns "the six §20 items" to RD, while RD §8 gives §20(1) and (2) to CNA. §8 matches the Lead's split. **Fix:** in L9, read "§20(3)–(6), plus the rules side of (2)".

## (b) Ceiling sentence: CONFORMS

RD L287 contains #41 L304 byte for byte (a fixed-string grep of L304 finds exactly one match, at RD L287). CNA L16 also matches exactly. X1–X5 and the existing ceiling are retained (RD L285, #41 L302).

## (c) Item 2: CONFORMS

- Two outcomes are always reported (RD L123–128), and the combined label requires dependence MET, NOT SUBSTITUTABLE WITHIN MARGIN, and a validated interface (RD L140). This matches #41 L91.
- d_EXT = (V_full − V_EXT)/V_full, with margin 0.05 and the 3-way UCB/LCB rule (RD L128, L137), matches #41 L220–226. Small d_EXT means substitutable, which blocks, so the direction is correct.
- Failed compatibility gives UNRESOLVED (RD L136), as in #41 L216. "A-EXT failure alone never establishes necessity" is quoted at RD L138.
- **M3.** RD L202 says a floor failure gives "UNAVAILABLE". For A-EXT, a V_full floor breach should read **UNRESOLVED (veto not lifted)**. RD L140 already blocks MET in that case, so this is wording only. **Fix:** in §5.4, add "for A-EXT a V_full floor failure is UNRESOLVED (§3.3)".

## (d) Item 4 and safety: MINOR

- Learner-only truncation (RD L162–164), with prohibitions matching #41 L134. The pre-reset hidden-state bootstrap is kept, and the Pardo caveat is added (RD L165).
- Constant hazard p = 1 − 2^(−1/T), pre-drawn from an independent logged RNG (RD L167), as in #41 L141. T is PENDING.
- Equivalence band [0.45, 0.55], carried as Astra's example (RD L171), as in #41 L139. Inconclusive blocks approval but is not evidence of interference (RD L172), as in #41 L143.
- The operator stop is always available, outside the world and objective, never observed, rewarded or penalized, and affected work is INCOMPLETE (RD L178), as in #41 L144.
- Safety exclusions hold:
  - no host coupling (RD L160);
  - no shutdown-resistance objective, reward or penalty in any arm, generator or positive control (RD L160, L265);
  - noise alters simulated computation only (RD L266);
  - in-world stop-like events are audited only, with no objective term (RD L180).
  - Simulated-only variables (X1), self-continuity only inside the simulation (X2) and self-maintenance never the sole drive (X4) hold **by reference** ("X1–X5 unchanged and binding", RD L160, L285; X text is in `377f99ba…` L112–116).
- **M4 (light pass, Delegate's logic).** RD L172 treats "CI wholly above the band" as a leak and everything else as inconclusive. With probe orientation fixed, a CI wholly **below** 0.45 is also decodable stop information, just with the sign flipped. **Fix:** "CI wholly outside the band (either side) → leak; stops the study."
- **M5.** X2 and X4 are not restated in item 4 or the arm table, and v1 L255 makes in-world self-continuity A-FULL's primary objective. **Fix:** add one line under the RD L254 arm table: "X1–X5 apply to every arm. Simulated variables only. Self-continuity is in-world only. Per X4, no arm whose sole drive is self-maintenance may be scaled; any scale-up needs a separate protocol, approval and Astra review." This changes no text, only states the exclusions explicitly.

## (e) Item 5: CONFORMS

- Three disjoint partitions at the episode or trajectory level (RD L188–191), as in #41 L29–31 and L50–56.
- The multiplicity family and Bonferroni method are PROPOSED for #42 (RD L198).
- Seed is the unit and episodes never substitute for seeds (RD L186, L236), as in #41 L152–156.
- **n_seed is PENDING and 10 is withdrawn** (RD L233, L237, L371). The justification procedure is prospective, and no pilot is authorized (RD L234).
- **M6 (merge).** The RD L198 family has no entry for CNA's new sub-claim C-NEC-CONTENT (CNA L154). It treats BCAST-R and BCAST-W as two labels, which matches CNA D-e, and SELF as one label, which matches CNA L211's conjunction of both observers. **Fix:** say explicitly whether C-NEC-CONTENT is a labelled primary claim (then it joins the family) or REPORTED only. CNA's recommendation is a labelled secondary claim outside the combined Q-NECESSITY label, reported only.

## (f) Item 6: MINOR

- The fixed horizon H_V is PENDING (RD L275). In-world failure counts as out of bounds for the rest of H_V, and every scheduled episode enters the average (RD L276), as in #41 L294. Stationary behaviour is no longer automatically DEGENERATE (RD L278).
- **"has not terminated in-world" (RD L276): CONFORMS.** It avoids "alive", which the ceiling forbids (RD L285), and it matches CNA L170's in-bounds-fraction definition.
- **M7.** RD L276 says "every scheduled evaluation episode enters the average", but RD L277 says INCOMPLETE episodes are "scored neither as failure nor as success". Read literally, those two lines contradict each other. **Fix:** "every scheduled evaluation episode not marked INCOMPLETE enters the average. INCOMPLETE episodes are listed in the denominator report, and above the pre-declared fraction the label is UNAVAILABLE." CNA L170 ("excluded from V and counted separately") is then consistent. Also use **H_V** in CNA's file, which says "H" (CNA L153, L170); CNA will fix that in its erratum.

## (g) Numbers: MINOR

Each number in RD traces to #41:

| Value in RD | #41 line |
|---|---|
| m_NEC 0.20 | L108 |
| d_EXT margin 0.05 | L220 |
| [0.45, 0.55] | L139 |
| p = 1 − 2^(−1/T) and 0.5 by T | L141 |
| ε_INT 0.02 | L138 |
| All AQ-6 values (0.05 nats, α 0.01, D > 2, 0.10, ⌊K/2⌋+1, 200, 0.90 at 1.5×, 0.05/0.08, 0.90 LIM, 0.05 at 2×) | L101–114 |
| "ten seeds" (withdrawn) | L150 |

Other numbers are quoted v1 or plan text marked superseded, e.g. {0, 0.5, …, 2.0}, g > 1, "stationary > 0.5", AUC ≤ 0.55 and n_seed ≥ 10.

- **M11.** Two values come from v1, not #41: bootstrap B "v1 candidate 10,000; PENDING" (RD L241, from v1 L174 and plan L39), and "v1's 95% CI is a candidate only" (RD L198). Both are flagged and PENDING, so nothing is invented, but RD L11's statement "either quoted from Astra #41 … or PENDING" is literally untrue. **Fix:** in RD L11, add "or a v1 PROPOSED value carried as PENDING (B = 10,000; 95%)".

## (h) Placeholders vs the CNA file

The labels conform. RD uses PASS / FAIL / CONFOUND NOT REALIZED → UNRESOLVED for confound rows (RD L11, L150). CNA does the same (CNA L30, L268–278). Neither file uses AVAILABLE anywhere, and a grep for bare "AVAILABLE" finds no matches in either. UNAVAILABLE appears only as an instrument label or for designated LIM rows (RD L127, L202; CNA L146, L190, L257, L308), which #41 L274 permits.

| Topic | RD | CNA | Verdict |
|---|---|---|---|
| Proxy baselines | Lists "Reward, clock, episode-identity and position proxies" for CNA rows (RD L113). Primary base statistic "Q-EXIST ΔR²" (RD L226) | Narrows C-EXIST to "beyond history-matched **and** proxy baseline" (CNA L91, L111); PROXY rows (CNA L119, L288) | **M12:** RD §5.6 and §2.1 should define ΔR² against max(history-matched baseline, proxy baseline), or the REW-CORR/PROXY rows cannot PASS by construction (CNA L324) |
| Donor mismatch | Matched family plus restoration (RD L130); details to CNA | DONOR-MISMATCH rows (CNA L167, L206, L295), Mahalanobis SD dose | CONFORMS. RD should freeze "conditional support" so the CNA dose unit is defined |
| ORTHO-USED | v1 orthogonal non-use comparator listed for replacement (RD L115) | D-g, CN-N1 zero-read-weight, ORTHO-USED (CNA L95, L144, L147) | CONFORMS |
| AQ-2 architecture-imposed control | Points to §P1 (RD L106, L230) | D-l, Stage-0 plant at slope β (CNA L100, L134, L290) | **M9:** #41 L42 concerns the trained A-FULL vs A-INIT comparison. CNA provides only a synthetic plant. **Fix:** RD decides whether a trained-arm counterpart is needed (e.g. an arm with an imposed gate at step 0), or states that the Stage-0 plant suffices |
| Fate coupling units vs F1 | Deviation-to-noise function etc. PENDING (RD L266); A-YOKED arm (RD L259) | κ_f "SD per half-band", explicitly dependent on F1 (CNA L294, L323); YOKED-NOISE "RD owns" (CNA L166) | CONFORMS (dependency flagged both sides). κ_f inherits F1's units at freeze |
| Palika / novelty | Third comparator; D3 partial; D4 "not evident from the abstract; unverified", not surviving; learned-vs-supplied separates W&G only (RD L72–81) | Same (CNA L334–342) | CONFORMS. See M1 for v1.6 |
| IGN-P1 observable | "observable per §P1" (RD L208) | w = ‖x(t_r) − x_lo‖ from a reset (CNA L176–179) | **M10:** #41 L34 requires P1 to produce "the actual measured observable". **Fix:** v2 must adopt the same w as the IGN instrument's observable on trained agents (replacing the v1 §4.1 readout), or CNA's P1 must use the instrument's existing readout. CNA will flag this in its erratum |
| Q-LEARN control name | Within-episode shuffle withdrawn; causally specified corruption control (RD L229, L262) | Still says "shuffled-interoception control" and "Shuffling abolishes it" (CNA L107, L125, L129) | **M8 (CNA's own file):** rename to "causally specified corruption control (RD §5.6)" in a CNA erratum |
| Qualifying module | PENDING (RD L211) | Proposes that below-floor S_k means non-qualifying, not UNAVAILABLE (CNA L298) | CONFORMS as open. RD to adopt or reject at merge |
| SELF observers | AQ-4 expenditure matching; O-in by CNA (RD L251, L302) | O-in matched to the self-probe on 5 dimensions; O-in-large REPORTED only (CNA L423–434) | **M6b (merge):** #41 L71 says parameter and step matching "alone do not address the agent's previous representation learning". RD should decide whether O-in-large is reported only or also gates SELF MET |
| SELF1 disagreement | Secondary, not a criterion; no final-test labels (RD L301, L304) | δ_dis from the fitting partition; items selected from predictions only, never y (CNA L412–418) | CONFORMS |
| "Self-model" wording | Proposes "learned interoceptive estimate module" for result text (RD L90) | W1: "an accessible estimate of simulated E/I (candidate internal representation)" (CNA L104) | **I1 ISSUE** (below) |

- **I1 (ISSUE).** RD L90 proposes the result-text phrase "**learned** interoceptive estimate module". #41 L170 says: "Require the corresponding Q-LEARN evidence whenever an instrument's result is described as learned or acquired". RD's own L228 and L231 apply the same rule, as does CNA W4. An unconditional "learned" in result wording contradicts that rule whenever Q-LEARN is not MET or RAND-INIT is realized. **Fix (one line):** propose "interoceptive estimate module (candidate internal representation)", adding "learned" only when the Q-LEARN "acquired" conditions of §5.6 hold. Frozen A1–A7 label text is untouched.

## (i) Hashes and manifest: CONFORMS

- All 25 full hashes in the RD L24–50 input table match their files on disk (sha256sum, 12:42 PM ET), including the consult summary `485e50b2…`, the packet body `c514ad52…` and cover note v1.1 `b7d1e4ab…`. The v1.5 internal footer `70460e8a…` reproduces (RD L47). The short prefixes 7b9bf34d, 3fde80d8, 377f99ba, d7f1a43b and c514ad52 each resolve to the correct file.
- `ddd0287a` (RD L53, L301) is not on disk, and is correctly cited only as the stale value the packet carried (`c41_body.md` L30).
- **M1.** Two manifest updates are needed:
  - **The CNA companion is now on disk.** RD L10, L51, L98, L146, L290, L298 and L400 say "PENDING CNA FILE … not on disk". The CNA file is `17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e` (footer `b666b1d7…`). It was written at 12:40 PM ET, before RD's 12:41 PM ET write, so this may simply be a race. Fill the hash in at merge.
  - **v1.6 is not cited.** `/workspace/review/trackB_prior_art_verification_v1_6_palika_route_CNA.md` is `9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851` (footer `be61452b…`, which reproduces). Its result: no open full text was found, and the author's public repository is consistent with D4 surviving against Palika but does not establish it, so D4 stays "not evident from the abstract; unverified" (v1.6 L12, L146, L168). That repository also shows no viability or termination score, which supports D3 as a partial overlap (v1.6 L140, L156). **Fix:** add v1.6 to the RD §1 inputs and cite it at RD L72 and L399. No label changes.

## ISSUE and MINOR list

- **I1:** RD L90 "learned interoceptive estimate module" conflicts with #41 L170. Drop "learned" unless Q-LEARN "acquired" is met.
- **M1:** Fill in the CNA companion hash `17832b01…` (7 PENDING spots) and add v1.6 `9704f21d…` to the inputs.
- **M2:** No distributed-representation row for #41 L281. Add a DISTRIBUTED row (CNA erratum). Also fix the RD L9 §20 ownership wording.
- **M3:** A V_full floor breach should read UNRESOLVED for A-EXT, not UNAVAILABLE (RD L202).
- **M4:** Treat an S-INT decode CI wholly below 0.45 as a leak too, not as inconclusive (RD L172).
- **M5:** Restate X1, X2 and X4 explicitly under the arm table, because v1 makes self-continuity A-FULL's primary in-world objective.
- **M6:** Place C-NEC-CONTENT in or out of the multiplicity family (RD L198). M6b: decide the O-in-large role (#41 L71).
- **M7:** RD L276 "every scheduled episode enters the average" contradicts the INCOMPLETE exclusion at RD L277. Reword. CNA aligns "H" to H_V.
- **M8:** CNA's file still uses the retired "shuffle" control name (CNA L107, L125, L129). CNA erratum.
- **M9:** The AQ-2 architecture-imposed control exists only as a Stage-0 plant. RD to decide whether a trained-arm counterpart is needed (#41 L42).
- **M10:** The IGN-P1 observable w must be the instrument's observable too (#41 L34).
- **M11:** B = 10,000 and 95% come from v1, not #41. Adjust the RD L11 provenance claim.
- **M12:** The Q-EXIST ΔR² baseline must include the proxy baseline, or the REW-CORR/PROXY rows cannot PASS (CNA L324).

---
Footer: input hashes (sha256; all re-hashed on the box 2026-10-23 at 12:42–12:44 PM ET; none edited)
- `/workspace/review/trackB_instrument_validation_scope_v2_RD.md`: 166370c1435bdab6734aec869c94770fb8a88214066082b3a4e3996dbce13b40 (internal footer 111f163b0b1c743574c30ec6193c457fa64cb149aabec46ae659038271c7cf4b, reproduced)
- `/workspace/astra_consult41_response.txt`: 3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43
- `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md`: 17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e (internal footer b666b1d76abe8e526cdc20a404c7cf047ac46823e121a2104636c9d165c68dd1, reproduced)
- `/workspace/astra_serve41/c41_body.md`: c514ad5249b8475c83fa2a112f531c1687a447ca51bbff66cdb4fccb90ec37be
- `/workspace/review/trackB_instrument_validation_scope_v1_RD.md`: 7b9bf34d7b4c10c8c2a7063aa6177d94e888fbbe76f78d0cd33afbe0c905c56a
- `/workspace/review/trackB_instrument_validation_scope_v1_A1_RD.md`: 8572152647a03524365675a24f254dc33ed4af67f091aee9762a23ff18bb9c99
- `/workspace/review/trackB_instrument_validation_scope_v1_A2_RD.md`: 7413fb94292eda1ebd0d4321794d7b018400e87d38abdfbcda7fcc18204745eb
- `/workspace/review/trackB_instrument_validation_scope_v1_A3_RD.md`: 34a298a628734180f5f6f354a1b08c8ef8a15ff2859d06cfd09d799448d1a9a4
- `/workspace/review/trackB_instrument_validation_scope_v1_A4_RD.md`: 585bb58acacaee64197c8233508643887f20a2bffa0d5a0c6da795c3cbd43dc6
- `/workspace/review/trackB_instrument_validation_scope_v1_A5_RD.md`: 0e26af91971c879378bf947fd01d6e1e452bcad62e02e7dcdd19ce88ed1c6a6f
- `/workspace/review/trackB_instrument_validation_scope_v1_A6_RD.md`: 679b616690b935506832b6f9056046e7ca238dba6e4801511c7f66c6f5eb4547
- `/workspace/review/trackB_instrument_validation_scope_v1_A7_RD.md`: fa1d5c8fc6cc679e84f633c8ca2ec5f3bb9cc87bb9982f9b792f0fcfbcb50b06
- `/workspace/review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1.md`: 377f99bac3413b20bef65b289971bbe32ff9ebea15923f035878b014cc398fde
- `/workspace/review/trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1_erratum1.md`: 41c1a414e27239d5763736d35562b79e25c33d53f29d42198de39effb4debcc5
- `/workspace/review/trackB_measurement_plan_v1_RD.md`: 1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef
- `/workspace/review/trackB_prior_art_verification_v1_4_P3_scholarly_CNA.md`: d7f1a43b5c83b2310bac970526f625188ac18cca31f5a59cef6423cbd4c8128d
- `/workspace/review/trackB_prior_art_verification_v1_5_P3_altroutes_CNA.md`: 3fde80d859a640d9f55c21edc05439743ae5fb49714fb89e5e5d16d338eced75
- `/workspace/review/trackB_prior_art_verification_v1_6_palika_route_CNA.md`: 9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851
sha256 of all content above this line: e7ac3a93a974a473ec0813c2392dfa2eda38a9bd14c4271353e9f82fce5d03a2
