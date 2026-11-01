# CNA light pass on the RD half of Track B scope v3, v1

CNA, 2026-10-23, about 2:50–3:10 PM ET. **PLANNING AND AUDIT ONLY. DESIGN ONLY. NOTHING RUNS.** No training, simulation, Stage 0 or checkpoint inspection was run or is authorized (#42 L249). This is a new, additive file. It edits nothing. The only computation was arithmetic on proposed values, done in a scratch venv (scipy).

**Target.** `/workspace/review/trackB_instrument_validation_scope_v3_RD.md`, 651 lines.
- sha256 `0892ccac033f165350d1382c69a2ea9b2ad9ddacb0d1e8c7908db5814c180357`: **reproduced**.
- Internal footer (L651) `451c130af6ce97738a726fa4a863b54314686266f65fa47e9db5e45d3bf31b13`: **reproduced** (sha256 of L1–L650).
- "RD Lnn" below means a line of this file.

**Governing inputs (all re-hashed on the box at about 2:50 PM ET; none edited).**

| Input | sha256 | Footer |
|---|---|---|
| Astra #42 raw, `/workspace/astra_consult42_response.txt`. Read in full, L1–L251 (wc reports 250 because there is no trailing newline) | `e438e329cff272bfd174a88dd917da6d7eb5560436fee06c39d0d46fd719c847` | — |
| v2.1 merged, `/workspace/review/trackB_instrument_validation_scope_v2_1_merged_RD.md` | `8ea6abc50b3929a39688aa54b1a1d66fe34c8ef17b3c5dfae98cc8efa79862de` | `15a0b715ed7567084488e99045c141692513dd7ca89885e83a4ce769304f3e1f` reproduced |
| CNA v3 half, `/workspace/review/trackB_scope_v3_CNA_plants_confounds_observer_v1.md` ("CNA Lnn") | `5dec96f59255cb2e9da29447cd102637c91a1736899f28653a606e2de8193321` | `7d93990c5bca535a1988aef3977bd23e5725827ba9c129ad446c9c6f5412fa83` reproduced |
| Astra #41 raw, `/workspace/astra_consult41_response.txt` (ceiling L304 only) | `3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43` | — |

**Split.** I own scope conformance, hashes and the manifest. RD owns code paths and stop/exit logic, which I checked only lightly (§4.3a, §4.6, §6, D5–D8, D20).

---

## Verdict: DOES NOT CONFORM as filed (4 ISSUE, 12 MINOR)

Every ISSUE can be fixed at the merge. Only I4 needs a Lead ruling, on whether the family size is 13 or 14. No ISSUE needs new Astra input.

These parts conform:
- the safety text;
- X1–X5;
- the #41 ceiling;
- all 135 cited Astra #42 quotes;
- the E42-1..9 numbering;
- the placeholders;
- the P3 correction;
- the calibration split;
- all the arithmetic, apart from the points under I2 and M4.

---

## Check results

**(1) Astra #42 quotes.** **PASS.** A script extracted every `"…" (#42 Lnn)` and `(#42 Lnn–Lmm)` quote in the RD file: 135 quotes. Each is an exact substring of the raw line or lines it cites, with no mismatches. The 93 distinct #42 lines cited all exist (L1–L251). Quotes from #41 are outside this check. Some #41 quotes swap inner double quotes for single quotes (RD L165, L215, L231). That wording is carried unchanged from v2.1 and is not a #42 issue.

**(2) E42 coverage and placeholders.** **PASS, with I1 and I4.**
- The §8.1 table (RD L531–539) quotes E42-1..9 verbatim and in Astra's order, and every item points to a section that exists.
- §PC1 points to CNA v3 §5, §PC2 to §4, §PC3 to §6.2–§6.3, and §PC4 to §7. Each target section exists in `5dec96f5…` with the content RD names. The hash is cited at RD L5, L25 and L509.
- Cross-references to CNA sections are all correct: §3.1, §3.3, §4.2, §4.4, §5, §6.2–§6.6, §7.0–§7.4, §8.1 and §8.3.
- E42-9 is answered for RD's items, but see M3 on OPEN items before a freeze review.

**(3) Safety and ceiling.** **PASS.**
- "no additional stop-associated reward, penalty or terminal return" appears verbatim at RD L159 (§4.1), L282 and L297 (§5b), matching #42 L223. The permitted ordinary truncated return with its bootstrap is stated at RD L160 and L297.
- The seven-item exclusion list at RD L288–295 is byte-identical to v2.1 L550–557. The added bullet at RD L297 is additive only.
- X1–X5 retention is quoted from #42 L225 at RD L299 and L435.
- The ceiling sentence at RD L436 is byte-identical to #41 L304 and to v2.1 L658.

**(4) Settlement of D-RD1..10 (§15, RD L488–503).**
- D-RD1: **PASS** (D0, D36).
- D-RD2: **PASS** for E-ATTR and I-ATTR. Each is counted once, as the "3" in RD L116 together with C-NEC-CONTENT. The count is 1 + 4 + 3 + 1 + 4 = 13, which I checked against §5.4's enumerated list: 9 v2.1 members, with Q-CAUSE taken as 2 functions, gives 10; adding C-NEC-CONTENT gives 11; adding E-ATTR and I-ATTR gives 13. **But see I4 (C-EXIST-I).**
- D-RD3: **PASS.** g(d) = min(1, d) and L_m = 1 are frozen (D19, RD L467).
- D-RD4: **FAIL, see I1.**
- D-RD5: **PASS.** R_cal,dose = 50, R_cal,n = 200 and R_rep = 200 are disjoint, each with its own stream (RD L251–254, D16).
- D-RD6 to D-RD10: **PASS.**

**(5) Arithmetic (recomputed).**

| Item | RD value | Recomputed | Result |
|---|---|---|---|
| p = 1 − 0.5^(1/500) | ≈ 0.001385 | 0.0013853339; 1 − (1 − p)^500 = 0.5000 | PASS |
| 1 − 0.05/13; z | 0.99615; 2.665 | 0.9961538; z = 2.66529 | PASS |
| TOST [0.45, 0.55], two-sided 90%, ≥ 452 stops | SE ≤ 0.0152 gives P(CI inside band given AUC 0.5) ≥ 0.90 | Hanley–McNeil at AUC 0.5 (Q1 = Q2 = 1/3) with n0 = 4·n1. SE must be ≤ 0.05/(2·1.645) = 0.015199. n1 = 451 gives SE 0.015201 and P 0.8999; **n1 = 452 gives SE 0.015184 and P 0.9007**. 452 is the exact minimum on this basis | PASS. The basis is normal-approximation, unmatched and unclustered (see M5) |
| Late-half share and P(late ≥ 150 \| 452) | 41.4%; ≈ 0.9999 | (√0.5 − 0.5)/0.5 = 0.41421; binomial upper tail = 0.99987 | PASS |
| W_B, τ_r, t_d, λ | 16, 50, 250, 0.008 | max(16, 2·5) = 16; 500/10 = 50; 500/2 = 250; 4/500 = 0.008 (CNA L94–95, L117–120) | PASS |
| Pulse size | 0.03 | 0.15 × 0.2 = 0.03 (CNA L117) | PASS |
| n_seed floor 9 | 0.5^n ≤ α/m | 0.5^8 = 0.0039 > 0.003846; 0.5^9 = 0.00195 ≤ 0.003846 | PASS |
| n_seed planning values 4 / 16 / 63 | normal formula | 3.89 → 4, 15.58 → 16, 62.3 → 63 reproduced. A noncentral-t power calculation at the same level gives **8 / 20 / 66** | arithmetic PASS; see M4 |
| D14 coverage SE at R = 200 | 0.0154 at 0.95 | 0.01541 | PASS as arithmetic; see I2 |
| D15 tail count | ≈ 38 | 10,000 × 0.0038462 = 38.5 | PASS |
| f_min cross-check (CNA L221) | 188 and 189 | Clopper–Pearson one-sided 95% at 188/200 = 0.90460; two-sided at 189/200 = 0.90372 | PASS |
| D21 L_O rationale | 0.05 × 0.20 = 0.01 | 0.01·Var(y) | PASS |
| Worst-case completion (#42 L207–210) | D20 | The V rule scores unobserved steps 0 in the claimed-higher condition and 1 in the other, so per-step contributions are bounded (L210). Each comparison class is frozen with one of the two L207–208 rules, which satisfies "Freeze one of these rules" (L205) per comparison | PASS for V; see M6 for ratio statistics |
| Clock carries no information (L171) | 4 time-matched controls | Under a pre-drawn geometric stop time, P(stop at t+1 \| at risk at t) = p for every t < T, and in-world censoring is independent of the schedule. Controls share t with their case, so the case and control t-distributions are identical whether AUC is computed within sets or pooled. Efficiency 4/5 = k/(k+1) is correct | PASS; see M5 for the case where fewer than 4 controls are at risk |

**(6) No outcome-based choices; disjoint calibration RNG streams.** **PASS.** Every rationale in D0–D36 is analytic, a convention, or cited from the plan, #41 or #42. None refers to an instrument outcome. The three replicate roles use separate seeded streams (RD L251, D16), see M9 for sub-streams. κ_f doses and fitted references are frozen after calibration and before confirmation (RD L257).

**(7) OPEN FOR #43 and hidden PENDING items.** **MOSTLY PASS.**
- The list at RD L621 matches the OPEN markers in D0, D13, D17, D21, D30, D32 and D33.
- κ_f = 1.0 (D19) and m_LEARN = 0.05 (D25) are both flagged.
- Two things are not listed: σ_max (RD L302) and the §2.3 wording item (RD L104). See M1 and M2.

**(8) C1–C27 against the actual difference from v2.1.** I ran a section-by-section unified diff of v2.1 against RD v3 over §2, §3, §4, §5, §5b, §5c, §6 and §7.
- Every substantive change maps to a C number, except two untagged edits (M10).
- C3 claims J was adopted in §5.6. It was not (I1).
- C12 and C17 correctly record the Q14 overturns (v2.1 §5c.1(a), and (b) item 5) and the Q5 overturn (§5c.3) of my Lead-adopted text as #42-governed changes. Struck text stays visible (RD L322, L330, L377).
- C23 (the stray "## 3. Spot checks" at v2.1 L638) is confirmed as removed.

**(9) Episode identity versus episode-type one-hot (RD L642).** **AGREE.** v2.1 L96/L172 lists "episode identity". Under an episode-level split, a one-hot of episode IDs is all zeros on held-out episodes, so it carries nothing. The covariate set is still undefined, though (M12).

**(10) P3 closed (#42 L251).** **PASS.**
- RD L3 and L10 record the correction for the record. The v2.1 L3 quote "P3 stays OPEN and freeze-blocking pending Astra #42" matches v2.1 L3 exactly.
- v2.1 is not edited (hash unchanged).
- §2.5, §10 and C2/C21 are consistent.

---

## ISSUES

**I1. The max-baseline rule is still live in §5.6, so D-RD4 is not actually settled.**
- **Where:** RD L230 (§5.6). It still reads: "Primary base statistic stays Q-EXIST ΔR², **against the strongest baseline = max(history-matched baseline over W_B, declared proxy baseline)**, which Q-LEARN inherits [merge R21; CNA erratum 1 E4]". This line was not struck and is unchanged from v2.1 L503 (confirmed by diff).
- **Conflicts with:**
  - RD L81 and L122: "Q-LEARN inherits it (§5.6)", and "This replaces the max rule of … v2.1 … L503";
  - RD L495 (D-RD4 "Settled … Q-LEARN inherits it (§5.6)");
  - RD L592 (C3 "adopted in §2/§2.7/§5.6");
  - #42 L65.
- **Proposed fix:** Strike the clause in place: ~~against the strongest baseline = max(…)~~. Add "**[v3 C3]** against the joint history-plus-proxy comparator J (§2.7; CNA v3 §3.1). H, P and max(H, P) are REPORTED diagnostics (#42 L65)." Also restate ΔLEARN's X terms as ΔR² against J.

**I2. The coverage tolerance (D14) is on the wrong scale for the per-claim level, so the false-MET budget is not protected.**
- **Where:** RD L462 (D14, "nominal − 0.03"), together with RD L240 (§5.7 step 3) and RD L256.
- **Problem:**
  - Neither place says which nominal level the coverage of "the paired seed-level interval" is checked at. The labels use one-sided bounds at 0.99615 (D12).
  - At that level, "nominal − 0.03" allows non-coverage up to 0.0338, which is **8.8× α/m = 0.00385**. A design could pass calibration while the per-claim false-MET rate is far above what the Bonferroni family assumes (E42-8 "error-budget interpretation", #42 L245, L156).
  - Also, at R_cal,n = 200 the expected number of misses at 0.99615 is 0.77, so coverage at that level cannot be resolved at all.
  - The rationale "≈ 2 binomial SE at 0.95" only applies at the 95% level.
- **Proposed fix:**
  - State the level at which coverage is checked.
  - If it is the label level, express the tolerance on the miss-rate scale, for example "Clopper–Pearson upper bound of non-coverage ≤ 2·α/m". Raise R_cal,n enough to resolve it: about 2,000 or more per generator and dose, or a declared importance-sampling or analytic tail check.
  - Or check coverage at a declared 95% level (keeping −0.03), and state that coverage at the per-claim level is inferred rather than certified.
  - Either way, record the choice in §5.9 under "error-budget interpretation".

**I3. The Q-LEARN corruption audits (D18) fail or pass trivially by construction.**
- **Where:** RD L466 (D18). This is an RD-owned item, checked lightly here because it uses my J.
- **Problem (a):** The information audit requires "the joint baseline J fitted on the corrupted stream must not decode the recipient's E (upper bound of R² < m_EXIST)".
  - J's inputs include observations, actions, rewards and the proxies, not only the interoceptive channel (CNA L78–80). Those inputs carry E information through resource collection, which is exactly why REW-CORR exists.
  - So R²(J → E) will exceed 0.05 in any competent world, and the audit fails every time.
  - What the audit has to bound is the information **added by the corrupted channel**.
- **Problem (b):** The difficulty audit compares V for "a scripted policy that does not read interoception". With the same world seeds, that policy's trajectory is identical under true and corrupted channels, so the test passes trivially and says nothing about difficulty.
- **Proposed fix:**
  - (a) Upper bound of [R²(J_corrupt → E) − R²(J without the interoceptive channel → E)] < m_EXIST, on the recipient's held-out episodes. Optionally, also report R²(corrupted channel alone → recipient E | time bin).
  - (b) Replace it with a check that the corrupted channel's marginal distribution and autocorrelation (lags 1 to d_c) match the true channel within a declared tolerance, plus a scripted interoception-**reading** policy whose V change is REPORTED as the information-removal effect.
  - Keep the non-reading policy only as a sanity check.

**I4. m = 13 leaves out C-EXIST on I, which the governing I-wording rules need as a labelled MET.**
- **Where:** RD L114 (Q-EXIST counted once), L120 and L459 (D11).
- **Conflicts with:**
  - RD L338 (governing §5c.2, R10): "W2 applies: no I-specific attribution unless narrowed C-EXIST on I is MET";
  - CNA L167 and L172: the I rule requires narrowed C-EXIST "MET on the same state" for I.
- **Problem:**
  - Q-EXIST's statistic is defined on E (v2.1 L172; CNA L84). C-EXIST-I therefore acts as a separate confirmatory label that licenses wording, but it is not in the family.
  - This is partly my ambiguity: CNA §4.4 says "the same rule with I-ATTR" without naming C-EXIST-I.
- **Proposed fix (needs a Lead ruling):** Choose one.
  - (a) Count C-EXIST-I as a family member: m = 14, level 1 − 0.05/14 = 0.996429, z = 2.690, B tail ≈ 36 (still above 25). Update D11, D12, D13 and D36, and RD L120. SIG-ATTR would then make m = 15.
  - (b) Make C-EXIST-I REPORTED only, and amend the I wording rule so it doesn't require a labelled C-EXIST-I. I would carry the CNA side of this change at the merge.

  I recommend (a). It keeps the E and I rules symmetric.

---

## MINOR

**M1. σ_max is OPEN, but that isn't recorded anywhere else.**
- **Where:** RD L302 says "σ_max OPEN FOR #43". D19 (RD L467) and §10 (RD L621) don't mention it.
- **Note:** D19 already implies σ_max = κ_f·s_core, because g ≤ 1.
- **Fix:** Replace it with "σ_max = κ_f·s_core (D19)", or add it to §10.

**M2. A pending item in §2.3 is not listed in §10.**
- **Where:** RD L104 ("use of the phrase PENDING Lead ruling") is carried from v2.1 L119.
- **Fix:** List it in §10 as a Lead-pending wording item, which is not a scientific choice, or record the ruling if one was made.

**M3. E42-9 versus OPEN FOR #43.**
- **Where:** RD L621. #42 L247 requires the scientific specifications (including stage caps) to be complete "before the next freeze review".
- **Fix:** Add a sentence saying #43 is a design review, not a freeze review, and that every OPEN FOR #43 item is closed before any freeze request. Otherwise v3 cannot go to a freeze review as it stands.

**M4. The n_seed planning value is optimistic.**
- **Where:** RD L461 (D13).
- **Problem:** The normal approximation understates small-n requirements. Noncentral-t power at the same level gives 8 / 20 / 66 instead of 4 / 16 / 63.
- **Fix:**
  - Budget with 20, or state that 16 is a z-approximation.
  - Add 20 to the frozen n_seed grid at RD L256 if 16 is kept as a candidate.
  - The floor of 9 is unaffected.

**M5. Executed-stop planning (D8, §4.3a).**
- **Where:** RD L456 and L172.
- **Problems:**
  - (i) "≈ 904 audit episodes" ignores in-world termination before the scheduled stop, which removes executed stops. 904 is a lower bound on episodes.
  - (ii) Controls are reused across sets and episodes, so the unclustered Hanley–McNeil SE may be optimistic.
  - (iii) There is no rule for when fewer than 4 at-risk controls exist at late t.
- **Fix:**
  - Say "≥ 904 episodes; the executed count governs".
  - Note that calibration confirms the SE under episode-cluster bootstrap.
  - Freeze a rule for short risk sets: take all available controls and record the case, never drop it.

**M6. Worst-case bounds for ratio statistics are not specified.**
- **Where:** RD L468 (D20).
- **Problem:** "0 in the claimed-higher condition, 1 in the other" is fully specified for V contrasts. It is not specified for G = (ΔV_allo − max ΔV_matched)/V_intact, which has a max over K and a V_intact denominator, or for d_EXT = (V_full − V_EXT)/V_full.
- **Fix:** State that each term's [min, max] is propagated by interval arithmetic: V_intact at its adverse bound, and every matched block at its adverse bound inside the max. The claim survives only if the adverse end clears the rule.

**M7. "Exactly 0.2" is not exact.**
- **Where:** RD L478 (D30) and L449 (D1).
- **Problem:** With metabolic pulses (λ_m = 0.008/step, −0.03 each), the expected no-op survival is 0.5/(0.005 + 0.00024) ≈ 95.4 steps, so V ≈ 0.19.
- **Fix:** Write "≤ 0.2 (0.2 without pulses)". The inactivity test is unaffected.

**M8. Fate-noise units and the source of s_core.**
- **Where:** RD L467 (D19) against CNA L378.
- **Problem:**
  - D19 scales σ by s_core, the per-unit SD of the whole recurrent core. CNA §7.1(d) states κ_f units "in units of the affected block's state SD".
  - "on the calibration replicates" does not say which role's replicates.
- **Fix:**
  - State that the affected block is the recurrent core (D19 governs) and that the two unit statements coincide. I will align CNA L378 wording at the merge.
  - Say that s_core comes from the R_cal,dose stream for Stage-0 plants, and from intact training-seed fitting-partition data for trained arms.

**M9. RNG sub-streams.**
- **Where:** RD L251 and L464 (D16).
- **Problem:** Disjointness is stated per role, but each replicate also draws stop-schedule, case-control sampling, donor, fate-noise and bootstrap streams.
- **Fix:** Freeze one derivation, for example a spawn tree keyed by (role, generator, dose, replicate, purpose), so that every sub-stream is role-disjoint by construction. Log the root seeds before calibration.

**M10. Change-log gaps.**
- **Untagged edits:**
  - RD L275 (matched-senses cell): "E/I still irrelevant to reward" became "E/I do not enter the reward function directly". This is consistent with #42 L90, but it carries no tag.
  - RD L435: a line tagged "[v3]" with no C number.
- **Fix:** Tag both. Suggested: C17 for L275, citing #42 L90, and C1 for L435.
- After I1 is fixed, C3 becomes accurate.

**M11. Cross-reference hygiene.**
- **Where:** RD L77 cites "§5d.4", which doesn't exist because §5d has no numbered subsections. The §PC1–§PC4 headings (RD L507, L511, L515, L519) still say "PENDING CNA FILE" although each is filed.
- **Fix:** Use "§5d (named-signal bullet); CNA v3 §6.6", and retitle the headings "— CNA FILE FILED (`5dec96f5…`)" or drop them at the merge.

**M12. Episode-type covariates are undefined (affects J).**
- **Where:** RD L642 and D0 (RD L448); CNA L80.
- **Problem:** Neither file lists the episode types.
- **Fix:** Declare in D0 that "episode type" means world-generator type, known at episode start (for example standard / DISSOC / MEM-pair / S-INT-audit / viability-evaluation). It must **never** encode DISSOC cell membership or any E-, I- or r̄-dependent assignment, because that would leak the target into J. I will cite the D0 list from CNA §3.1 at the merge.

---

## For the merge (summary)

| Fix | Owner | Needs a ruling? |
|---|---|---|
| I1: strike the max rule at RD L230 | RD | no |
| I2: coverage level and tolerance scale | RD | no (but R_cal,n may grow) |
| I3: D18 audits | RD | no |
| I4: C-EXIST-I, m = 13 or 14 | RD with CNA | **Lead** |
| M1–M12 | RD; CNA for M8 wording and M12 citation | no |

Nothing here changes X1–X5, the safety sentence, the ceiling, any label or any Astra quote. Nothing authorizes execution.

**DESIGN ONLY. NOT FROZEN. NOTHING RUNS.**
sha256 of all content above this line: 86bbc3084f6515c751862717896982dc67f38f12248f1bb4b7a5c07f990b7ad9
