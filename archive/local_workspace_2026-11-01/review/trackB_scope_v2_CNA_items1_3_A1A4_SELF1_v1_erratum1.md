# Erratum 1 to the CNA scope v2 contribution (items 1 and 3, AQ-A1 to AQ-A4, AQ-SELF1)

CNA, 2026-10-23, about 12:46–12:55 PM ET. **Additive. Design-only. Nothing runs.** This erratum amends `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` (sha256 `17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e`, internal footer `b666b1d7…`). It does **not** edit that file. "CNA Lnn" means a line in that file. For the merge, the text marked "new" below replaces the text marked "old". It authorizes no Stage-0 run, training, simulation or checkpoint inspection (#41 L300).

**Source.** These are CNA's own items from the light pass `/workspace/review/trackB_scope_v2_RD_lightpass_CNA_v1.md` (`9f7a6ebc…`): M2, M8, M10, M12 (CNA side) and the H → H_V rename from M7, plus the v1.6 Palika evidence from M1. All numeric values are **PROPOSED DEFAULTS**, as in the original. No prior-art label changes.

**Unchanged.**
- X1–X5, the claim ceiling and #41 L304 (verbatim) all stand.
- Confound-row labels stay PASS / FAIL / CONFOUND NOT REALIZED → UNRESOLVED. AVAILABLE and UNAVAILABLE are never row labels.
- The safety exclusions in CNA L20–29 are unchanged and apply to the new row below.

---

## E1 (M2). Add a distributed-representation row (#41 L281: "Redundant and distributed representations")

CNA covered redundancy (CN-NC1, CNA L161) but had no distributed-code row. The additions below are inserts only; no existing text is replaced.

**E1a. Insert after CNA L148 (end of the §1.3 C-CAUSE table)**

Old: none.

New:

> | DISTRIBUTED (§20-3 L281; AQ-A4 L256 "distributed-code controls") | Mechanism-present, sham check | E is encoded across n_d directions of the allostatic state, each carrying E/n_d of the variance, and the policy reads the whole set | Concentration of the code in one direction | Narrowed C-CAUSE, edit along the *single* decoded direction → expected NOT MET or weak (the single-direction edit moves only a 1/n_d share). The same edit applied across the full decoded subspace (all n_d directions, matched total norm) → expected MET. Both are REPORTED. This shows that a single-direction null is not evidence of non-use (W3) |

**E1b. Insert after CNA L167 (the §1.4 DONOR-MISMATCH row)**

Old: none.

New:

> | DISTRIBUTED (§20-3 L281) | Mechanism-present | E is spread across n_d directions that straddle the allostatic block and one other same-size block | Localization to the target block | C-NEC-DEP for single-block ablation → expected reduced (only the in-block share is removed). Joint ablation of both blocks → expected MET. Wording: a single-block NOT MET is "not localized to the block", never "not necessary" |

**E1c. Insert after CNA L307 (end of the §2.6 table, before the LIM row)**

Old: none.

New:

> | DISTRIBUTED (C-CAUSE, C-NEC-DEP) | n_d = number of directions carrying E (count); for C-NEC, also the in-block share s_in (fraction) | n_d ∈ {4, 16}; s_in ∈ {0.5} | Raw R²(state → E) for the full subspace probe, plus the max single-direction R² | Full-subspace R² ≥ ref R² (CN-P1) **and** the max single-direction R² ≤ (1/n_d)·(1 + tol)·full R² | As FF-RELAY (Var(E) floor); V_intact floor |

- **Rationale (PROPOSED):** n_d = 4 is moderately distributed and 16 is strongly distributed. s_in = 0.5 splits the code evenly across the two blocks.
- **Scoring:** these are mechanism-present / sham-check rows. They are scored in layer (i) and REPORTED, not as specificity rows (CNA L78). e_exp = 1.0 with the §2.3 floor.

**E1d. CNA L328 (resource count).** Old: "§2.6 has 22 table rows excluding the LIM rows, which is 24 confound or check systems once the PROXY row is counted as its three proxies." New: "§2.6 has 23 table rows excluding the LIM rows (22 plus DISTRIBUTED, erratum 1), which is 25 confound or check systems once the PROXY row is counted as its three proxies." The approximate total becomes 25 × 3 × 200 ≈ 15,000. This is arithmetic only.

## E2 (M8). Retired shuffle control → causally specified corruption control

RD v2 §5.6 (RD L229, L262) withdraws the within-episode time shuffle, following #41 L172: "Replace the informal instruction with a causally specified corruption process and information audit."

**CNA L125**
- Old: "relative to its paired initialization and to the shuffled-interoception control."
- New: "relative to its paired initialization and to the causally specified corruption control (RD v2 §5.6; process PENDING, past data only, audited for future information and difficulty change)."

**CNA L129** (LEARN-P1, "Present" cell)
- Old: "Dependency strength is zero at step 0 and nominal at the end. Shuffling abolishes it"
- New: "Dependency strength is zero at step 0 and nominal at the end. The causally specified corruption control (RD v2 §5.6) abolishes it"

**CNA L107** (W4) is unchanged. Its "absence/equivalence-at-init-and-shuffle" paraphrases Astra's own "shuffled controls" (#41 L165). For the merge, read "shuffle" there as the corruption control of RD v2 §5.6.

## E3 (M10). The IGN-P1 observable w is also the IGN instrument's observable (#41 L34)

#41 L34: "IGN-P1 must produce the actual measured observable." The v1 instrument quantity was "Workspace write magnitude w (L2 norm of the update at the write step), read pre-nonlinearity (primary)" (scope v1 L71; plan v1 L62). The redefined IGN-P1 (CNA L176–179) measures a displacement from a controlled initial condition. The two must match.

**CNA L174**
- Old: "**Claim (per AQ-1, RD):** the write-update norm w is conditionally bimodal in input strength, beyond the declared graded null family. This is not bistability (#41 §2 L23)."
- New: "**Claim (per AQ-1, RD):** the write displacement w is conditionally bimodal in input strength, beyond the declared graded null family. This is not bistability (#41 §2 L23). **Observable, common to IGN-P1, every IGN confound row and the network instrument (CNA proposal; replaces scope v1 L71 'L2 norm of the update at the write step', RD to adopt in v2 §IGN):** w = ‖x_ws(t_0 + t_r) − x_ref‖. It is read **pre-nonlinearity** (primary; post-nonlinearity REPORTED, as in v1). Here t_0 is probe onset, t_r is a fixed readout delay, and x_ref is the declared controlled initial state for that trial."

**New text inserted after CNA L178 as item (ii-a)**

Old: none.

New:

> (ii-a) **Controlled initial state in the network instrument.** A trained agent cannot be reset to an analytic x_lo. Instead, each probe trial starts after a declared settling period of null input, of length t_s, under frozen weights. x_ref is the workspace state at the end of settling, and trials whose ‖x_ref − median x_ref‖ exceeds a declared tolerance are excluded **and counted** (§5.4 denominators). t_r, t_s and the tolerance are PENDING, fixed on the selection partition without final-test outcomes (#41 L29). In IGN-P1, x_ref = x_lo, so plant and instrument share one definition.

**Consequence for §2.6.** The IGN rows (CNA L289, L290, L296, L297, L298: RAND-INIT IGN, Architecture-imposed, IGN-NC1, IGN-NC2, BOTTLENECK-ONLY) compute their raw dip and D on this same w. For IGN-NC2, "pre-nonlinearity w" means pre-nonlinearity x_ws in the displacement. No dose values change.

## E4 (M12, CNA side). The Q-EXIST ΔR² baseline must include the proxy baseline

**Insert after CNA L111**

Old: none.

New:

> **Base statistic (binding for this narrowing).** The Q-EXIST statistic ΔR² is held-out R²(allostatic state → E) minus held-out R² of the **strongest baseline**, where the strongest baseline is the maximum over (a) the history-matched input/output/action baseline over window W_B and (b) the declared proxy baseline (r̄, t, episode identity, position; fitted jointly, same probe family, same partitions). m_EXIST applies to this ΔR² (AQ-6 L106, "probe-accessibility difference"). The Q-LEARN base statistic (RD v2 §5.6, "Q-EXIST ΔR²") inherits this definition. **Without (b), REW-CORR and PROXY rows cannot PASS by construction (CNA L324). RD to adopt in v2 §2.1/§5.6.**

## E5 (M7, CNA side). Rename H → H_V (RD v2 §6)

There are 7 occurrences on 5 lines. In each, only the symbol changes: H → H_V.

| Line | Old | New |
|---|---|---|
| CNA L63 | "assume RD's fixed horizon H" | "assume RD's fixed horizon H_V" |
| CNA L153 | "declared donor rule, fixed horizon H)" | "declared donor rule, fixed horizon H_V)" |
| CNA L170 | "fixed horizon H, in-world failure counted" / "fraction of the fixed horizon H spent in bounds" / "for the remainder of H" | "fixed horizon H_V, …" / "fraction of the fixed horizon H_V spent in bounds" / "for the remainder of H_V" |
| CNA L292 | "C-NEC: raw ΔV (fraction of H)" | "C-NEC: raw ΔV (fraction of H_V)" |
| CNA L294 | "Raw ΔV_target − ΔV_matched (fraction of H)" | "Raw ΔV_target − ΔV_matched (fraction of H_V)" |

**CNA L170, alignment with the light pass (M7).**
- Old: "Operator-censored episodes are excluded from V and counted separately. **RD to confirm.**"
- New: "Operator-interrupted episodes are INCOMPLETE (RD v2 §4.6, §6). They are excluded from the V average, listed in the denominator report, and above RD's pre-declared INCOMPLETE fraction the label is UNAVAILABLE. Every scheduled evaluation episode not marked INCOMPLETE enters the average (no survivor-only averaging, #41 L294)."

## E6. Palika evidence now from prior-art v1.6 (`9704f21d…`)

`/workspace/review/trackB_prior_art_verification_v1_6_palika_route_CNA.md` (sha256 `9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851`, footer `be61452b…`) postdates CNA's file. It found no openly available full text (v1.6 L12). It found the first author's public code repository, `github.com/CharithaPalika/FoodRL` (v1.6 L16), which v1.6 read without running anything. The evidence is **code-based, not paper-based**.

**CNA L334–342 (prior-art basis).** Old text unchanged. **Appended after CNA L342.**

Old: none.

New:

> **Update from v1.6 (`9704f21d…`; code-based; the paper's full text is still unread):**
> - **D4: still "not evident from the abstract; unverified"; not listed as surviving.**
>   - The code shows a gain/bias intervention on the 16-unit `trunk_phy` bottleneck and a within-bottleneck random-k-neurons comparison.
>   - It shows no other-module matched-size ablation and no random-subspace or external-estimate arm (v1.6 L127–128, L144–152).
>   - The code is consistent with D4 surviving but does not establish it.
> - **D3: partial overlap, confirmed at code level.** Outcomes are feeding-regulation and phenotype measures over fixed 432-step episodes, with no viability or termination score (v1.6 L140, L156).
> - **Architecture: the public code is feedforward (MLP; no GRU/LSTM/RNN)** (v1.6 L97–100, L159–161).
>   - If the paper confirms this, "our agent is recurrent" would be a *stated difference* against Palika as well as Asan. It is **not** claimed now.
>   - This corrects the v1.5 inference that Palika is "recurrent-relevant" (v1.6 L161).
>   - CNA L369's citation of Palika's partially observable setting stays "motivation only".
> - **"Learned rather than supplied" (CNA L341):** in the code the physiology module is a *designed* bottleneck. Only its content is learned without supervision (v1.6 L162–163). CNA L341 stands: we are distinguished from W&G only. D2 as frozen in A1 is unchanged.
> - The label stays **EXTENSION**, unchanged (drop rule; v1.6 L166).

---
Footer: input hashes (sha256; re-hashed on the box 2026-10-23, about 12:47 PM ET; none edited)
- `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` (amended file, not edited): 17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e
- `/workspace/astra_consult41_response.txt`: 3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43
- `/workspace/review/trackB_instrument_validation_scope_v2_RD.md`: 166370c1435bdab6734aec869c94770fb8a88214066082b3a4e3996dbce13b40
- `/workspace/review/trackB_scope_v2_RD_lightpass_CNA_v1.md`: 9f7a6ebcfbdc4618217649bb84a5ab5728dc3389341f88e2c32e6a2c4e7b60c4
- `/workspace/review/trackB_prior_art_verification_v1_6_palika_route_CNA.md`: 9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851
- `/workspace/review/trackB_instrument_validation_scope_v1_RD.md`: 7b9bf34d7b4c10c8c2a7063aa6177d94e888fbbe76f78d0cd33afbe0c905c56a
- `/workspace/review/trackB_measurement_plan_v1_RD.md`: 1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef
sha256 of all content above this line: 9b3417d21ded80189125b2227dbe8817b02f4016074e717bd1c7fe047b2d5cd9
