# Track B freeze prep v2.6: RD light pass of the v2.6 consolidated file (Lead) and the #51 packet — v2

**STATUS: REVIEW ONLY. DESIGN ONLY. NOTHING RUNS.** A new, additive file; it edits no existing file. Nothing was sent or posted. The only computation was SHA-256, exact integer/rational arithmetic (Fractions, math.comb) and float64 evaluation of closed forms in the box's system `python3`. Nothing was run, timed, benchmarked or installed.
- **Written:** 2026-11-01 12:46 EST (from `date` at the moment of writing), by the Research Delegate (RD).
- **Supersedes** `review/trackB_freezeprep_v2_6_consolidated_lightpass_RD_v1.md` (sha256 235c4a77…, locked 12:46 PM ET, never posted). v1 miscounted V26 §10 as 20 rows; it has 21. That is the only change, and no verdict changes.
- **Scope:** code paths, RNG, counters, stop/exit and numerics. Light pass only. The WL ledger was not redone; cost was spot-checked line by line against WL §1.3.
- **Inputs:** V26 = `review/trackB_freezeprep_v2_6_consolidated_Lead.md`; #51 = `astra_serve51/` (`send_manifest.txt`, `send/c51_1..6.txt`, `c51_body.md`, `governing_sha256.txt`); every file in V26 §10. Other abbreviations as in V26 §10.

## 0. Verdict summary (FAIL/EDIT first)
**No FAIL.** Four EDITs, none of which changes a rule, a number or the scheduled 7,068,312,000 trials at 67 seeds. None blocks #51, which has already gone out as built. All four can be fixed in v2.7 or the freeze text (PD-10).

| # | Item | Verdict |
|---|---|---|
| L-1 | Cost attribution: the room statement that v2.6 CPU-h is lower than WL "because ΔLL is held-out only, with no CV" | **EDIT** |
| L-2 | V26 header time "about 12:36–12:50 PM ET" vs file mtime 12:39:15 PM ET | **EDIT** (disclosure only) |
| L-3 | V26 §1 "supersedes … C2 and C3 §1": "C2"/"C3" are not §10 abbreviations (§10 uses E2C2/E2C3) | **EDIT** (cosmetic) |
| L-4 | V26 §3 paraphrase of A50 L153 as "not guaranteed for every g"; Astra wrote "for every negative g" | **EDIT** (paraphrase, not a quote) |
| 1 | Hashes: V26, #51 manifest, parts, body, governing list, all 21 V26 §10 cites | OK |
| 2 | Amendment list AM-1..AM-11; CNA items (a)–(c); never PASS / never FAIL | OK |
| 3 | Fidelity of the adopted rulings (14 sub-items) | OK (one sub-item L-4) |
| 4 | Cost labelling and direction | OK on labelling and arithmetic; L-1 on attribution |
| 5 | Stop/exit and safety | OK |
| 6 | Astra quotes | OK |

## 1. Hash checks — OK
- **V26:** whole-file sha256 `ff03eb81c158e1306df0aaf2127d6191c81f80e11838231345749dd88e0de4c6` (MATCH ff03eb81…). Footer `85cc351656baddd047bc52597251d84fdd81d3a74114a1273f438526a1321dd6` recomputed over the bytes above it: MATCH (85cc3516…). 171 lines, mode r--r--r--, mtime 2026-11-01 12:39:15 EST.
- **#51 manifest** `astra_serve51/send_manifest.txt`: whole-file sha256 `e94313323b329b95744023de4b06d3d682f7267af03e191d5dd1b786383a9ac7` (MATCH e9431332…). Its own footer `46babeed…` recomputes: MATCH. It lists 6 parts; each part's sha256 and byte count (2059, 2464, 2486, 1659, 2420, 2406) MATCH on disk.
- **#51 body** `c51_body.md`: footer `06b362b1…` recomputes: MATCH. The 6 parts, with their `[c51 part n/6]` and end-marker wrappers stripped, equal the body above its footer (whitespace-normalised comparison: equal). So the body text quoted below is what was sent.
- **#51 governing list** `governing_sha256.txt`: footer `ebc76544…` recomputes: MATCH. It lists **24** files; all 24 whole-file hashes MATCH on disk. The 24 are the 21 V26 §10 files, V26 itself, plus A41 (`astra_consult41_response.txt`, 3f3b1b87…) and A42 (`astra_consult42_response.txt`, e438e329…), which back the N4 claim-ceiling and #42 quotes.
- **V26 §10 cites (21 rows):** every whole-file sha256 MATCHES the file on disk; every footer recomputes and MATCHES the cited value. A50 and MP carry no footer, as cited. Verified: A50 59e93cff, V25 d101438d, ER1 10860e98, E2 81bdfcf2, E2C1 c2c83921, E2C2 5100f4de, E2C3 2f813ba4, WL 83247be9, RD26 8a369208, RD26c1 ebe3a08c, RD26c2 e8bba1b2, RDLP 2b403bcb, CE50 b5a880ea, CE50a1 fdba7c63, CE50e1 42bf6c6d, PP a1dc190a, RDPP 12371a76, M ab80afa5, MP 1d5458e3, CNA2 17832b01, AMD 2f29a07a.
- The #51 parts carry no footers, by the #43–#50 precedent stated on manifest line 1; the manifest covers them. OK.

## 2. Amendment list and CNA's three items — OK
**V26 §7 contains exactly AM-1..AM-11:** AM-1 ROW0-FL; AM-2 ΔLL-HO; AM-3 NC2 ceiling; AM-4 scalar t_s = 0; AM-5 RAND-INIT dose-0 drop; AM-6 NC2r descriptive; AM-7 LIM in calibration; AM-8 S_cons/S_wc thresholds; AM-9 100-iteration bisection replacing E2-2; AM-10 n_q ≥ 199; AM-11 r_q = 991. All eleven expected items are present, each with a superseded source and a pre-data rule. #51 §A repeats all eleven and Q2 asks for ACCEPT/REJECT on each. V26 L113's routing (AM-8 in Q1, AM-9 in Q4, AM-10/AM-11 in Q3) matches the #51 Q headers.

**CNA's three items are not separate AMs, but each is put to Astra in the #51 body.** Lead's steering claims checked against the sent text, quoted verbatim:
- **(a) E50-1 supersedes corr3; NOT ASSESSED → UNRESOLVED.** #51 R1: "Row outcome, first match: (1) licence in row 0 -> FAIL; (2) available and S_cons or S_wc violated -> FAIL; (3) PR CP lower < 0.90 -> UNRESOLVED (confound not realized); (4) n_cons < 36 -> UNRESOLVED (insufficient support), whatever row removed the support; (5) else PASS. NOT ASSESSED is never PASS." Q1(c): "Is the five-step row outcome correct?" **Accurate:** the only FAIL paths are steps (1) and (2), so FAIL comes only from a row-0 licence or a screen violation. The body does not use the word "only", and it does not name corr3 (2f813ba4) or say that corr3/C3 §1's "otherwise the row FAILS" is withdrawn. corr3 is in the 24-file governing list, and V26 L30 records the supersession ("supersedes V25 L56, ER1 E1, E2-3, E2-4, C2 and C3 §1, per CE50a1 R1").
- **(b) A single frozen σ_ref from IGN-P1.** #51 R3: "One sigma_ref = 0.05*Delta_ref per tau for every scalar row, Delta_ref = 2x* from the bistable IGN-P1 reference at s = 0 (…; float64 hex frozen at freeze; never recomputed from a row's own attractors)." Q4: "Are the gains (2.0 / 0.5), sigma_ref, domains, …". **Accurate.**
- **(c) The EM recursion as the validated object, with S_max = 8.** #51 R3: "Validated object: the discrete Euler-Maruyama recursion; the SDE is interpretation only." and "effective input u = s - theta non-finite or |u| > S_max = 8 (swept over the whole frozen input table)". Q4: "Is the 100-iteration float64 bisection with its assertions (S_max = 8, x0 key, integer n_EM, readout counter) a complete root rule and failure rule?" **Accurate.** Q4 names S_max explicitly. The validated-object choice is put through R3 and Q0's E50-3 closure question rather than by name in Q4.
- **Optional, non-blocking:** v2.7 could list (a)–(c) as AM-12..AM-14, each with its superseded source: corr3/C3 §1 for (a), any per-row σ for (b), the SDE reading for (c).

**never PASS / never FAIL.** In V26 and #51, every NOT ASSESSED/UNRESOLVED statement reads "never PASS": V26 L12 "NOT ASSESSED → UNRESOLVED, never PASS", and #51 R1 "NOT ASSESSED is never PASS". Neither V26 nor any #51 file contains "never FAIL" (rg, case-insensitive). The only "never FAIL" in the input set is CE50 L93 (hashed, untouched): "NOT ASSESSED → UNRESOLVED: never PASS, and never FAIL on that ground alone." That sentence also says never PASS. Its "never FAIL on that ground alone" agrees with V26's row outcome, where FAIL comes only from steps 1–2. **No edit needed.**

## 3. Fidelity of the adopted rulings — OK (one sub-item EDIT)
| Sub-item | V26 text | Check | Verdict |
|---|---|---|---|
| Rank and coverage | §4: r_q = ⌈0.99·(n_q + 1)⌉ = 991; T = X_(r_q), no interpolation; eligible iff d ≤ T; n_q = 1,000; AM-10 n_q ≥ 199 asserted before any null draw; nominal 991/1001 | Exact: ⌈0.99·1001⌉ = 991. r_q = n_q exactly for 99 ≤ n_q ≤ 198 (r_q > n_q for n_q ≤ 98); r_q < n_q for every n_q in 199…10,000 | OK |
| Tail event | §4 and AM-11: "coverage < 0.97" = P[Bin(n_q, 0.97) ≥ r_q] = 5.6601e-06 at 991 (vs 1.8130e-05 at 990); per threshold, not simultaneous (A50 L132) | Exact rational sums: 5.6600699e-6 and 1.8129913e-5; V26's 5-significant-figure values are correct roundings | OK |
| Symbols | §4 L68: k_FY, n_EM, r_q | Matches CE50e1 E1-2 and RD26c2. V26 does not restate the Fisher–Yates counter. The governing text is CE50e1 L49 and RD26c2 L81: "counter (508−k_FY, 0, 0, 0), j = w0 mod (k_FY+1)". Slots 254–380 are RD26 L50, unchanged per RD26c2 L56. Nothing in V26 contradicts them. The per-seed 2,286/1,143 in §5 equals 0.5 and 0.25 of 4,572, consistent with 254/508 and 127/508 | OK (carry the counter line into the PD-10 freeze text) |
| ROW0-FL, S_cons, S_wc | §1 L23–L29, AM-1, AM-8: point ≤ 0.05 and one-sided 95% CP upper ≤ 0.08 for both; S_wc adds n0Q to numerator and denominator; any row-0 licence → FAIL | CP upper recomputed: 20/200 → 0.142; 8/188 → 0.0755; 9/200 → 0.0772; 10/200 → 0.0833. All match V26 and #51. **Zero denominator:** not stated in words. By construction, step 2 applies only when availability holds (n_cons ≥ 36 on S_cons's denominator, and S_wc's denominator ≥ S_cons's). A zero or short denominator therefore falls to step 4, UNRESOLVED, never PASS | OK |
| ΔLL-HO and anti-leak pins | §5: fit per seed on 2,286 fitting trials, score on 1,143 final; CV not run; pins (1) per-seed fits, (2) starts/scales only from the fitted partition, (3) Ashman D from the fitting-partition H1 fit; M L312–L313 govern | Matches RDPP V-3 and M L312 ("no fitting on final-test data") | OK |
| NC2 ceiling | §3 L61, AM-3: type-1 p-quantile of the 9 noise-free readouts, index ⌈p·9⌉ exact, hex per t_r ∈ {2, 3, 5} and p ∈ {0.8, 0.6}; clip post-readout; bitwise pre-nonlinearity w fixture → construction failure; post-nonlinearity D ≥ 2 binding | Matches RDPP V-1 | OK |
| Dose calibration | §5 L73: n_dc = 9, max 72,009,000 (7 × 50 × 4,572 × 9 × 5), K_dc = 5 placeholder, PENDING (PD-2) | Exact: 72,009,000; 15-cell 154,305,000; WL 1,148,715,000 at n_dc = 67. Attribution to n_dc is correct (RDPP V-2) | OK |
| G-iii floor | §3 L60: (0.01·Δ_ref)² = 3.6673 × 10⁻⁴; 5.28–9.05× over t_r ∈ {2, 3, 5}, V(n_EM) for both rows; network floor PENDING | Floor recomputed: 3.66726e-4 from x* = 0.9575040240772688. Range as RDPP V-4. PP's 5.45×/8.66× marked superseded (§9.3) | OK |
| Grid and inputs | §3 L58–L59: s = fl(s_c·m)/4, integer m, one rounding, hex; s_c(2) = 0.532839975353552 = hex 3fe10d066b84a372; LIM ∓7δ; max abs u 1.99815 | Recomputed: s_c(2) = 0.532839975353552, hex 3fe10d066b84a372; 15·s_c/4 = 1.99815 ≤ 8. Division by 4 is exact, so one rounding holds | OK |
| S_max sweep | §3 L50: construction-time sweep over the full frozen input table and at every root call (RDPP V-6) | As ruled. P6 KAT tanh(8.8) < 1 − 2⁻³⁰: box value 1 − tanh(8.8) = 4.544e-8 > 2⁻³⁰ = 9.31e-10 (box libm; pinned libm UNVERIFIED) | OK |
| n_EM | §3 L53: n_EM = t_r × 100 × G as literal integers in the freeze record, plus (vii-b) readout counter equals n_EM; never t_r/Δt in floating point | Matches RDPP V-7 (G = 1: 200/300/500) | OK |
| Root rule wording | §3 L49: "(which Astra found not guaranteed for every g, A50 L153)" | A50 L153: "not guaranteed to converge for every negative g". The rule itself is unaffected | **EDIT (L-4)** |
| Fitter pin | §5 L72 and PD-4: "Library pin PROVISIONAL: scipy 1.18.1 / numpy 2.5.4, UNVERIFIED for the run environment; confirmed at freeze" | Matches RDPP §4. Tolerances (ftol 1e-10, absolute gtol 1e-8 on mean NLL, maxiter 1,000, maxfun 15,000, maxcor 10, maxls 20, 3 restarts) as proposed | OK |
| RNG roles | §4 L64–L65: `ign-null-centre` (n_c = 101), `ign-null-quantile` (n_q = 1,000), separate, never reused | Matches RD26/corr2 and WL D1 KATs | OK |
| Scheduled totals | §6 L77: 4,005,072,000 + 45,720,000·n | Exact: 7,068,312,000 at 67; 4,416,552,000 at 9 | OK |

## 4. Cost — OK on labelling and arithmetic; EDIT (L-1) on attribution
- **Labelling:** V26 L3 says "Every CPU-hour figure is arithmetic on stated per-unit costs and is UNVERIFIED (A50 L212)". L79 and the table total read "UNVERIFIED", and #51 R6 says "CPU-h (UNVERIFIED, op counts only)". OK.
- **Arithmetic (sums of V26's own table rows):** Low 67 = 815.1; d_h 256 = 4,499.4; High 67 = 85,860.4; Max = 103,038.2; Low 9 = 509.8; High 9 = 54,226.6. All match the headline figures. Spot-checks against WL §1.3 per-unit rates: B1 High 1,174.6 = 72,009,000 network trials × WL's network per-trial rate (53,470.1 h / 3,278,124,000 trials). B2a High 843.7 = 8,362.0 × 72,417,000/717,717,000. C1 Low 463.8 = 3 × 154.6 (restarts = 3).
- **L-1 (EDIT), direction of the change from WL:** the room statement attributes the drop from WL to removing CV ("lower than the ledger's because ΔLL is held-out only, with no CV"). WL never included CV in any total. WL L95 lists it as a "Conditional addition outside the envelope (5-fold CV)", and WL's C1 row is already priced at 1× (High/Max 5,901.6, the same in V26). So removing CV changes no total. It only removes the up-to-×6 contingency (WL L95: C1 Max ≈ 35,410 instead of ≈ 5,902). Line by line, the actual drivers are:
  - B1 11,296.6 → 1,174.6 (High) and 13,849.3 → 1,174.6 (Max): n_dc 67 → 9 plus network-only cells under AM-3;
  - B2a 8,362.0 → 843.7: n_c up to 1,001 → 101;
  - A-scalar Max 31,584.9 → 15,792.5: G = 2 dropped, since g ≤ 2 gives G = 1.
  
  Two lines rise:
  - C1 Low 154.6 → 463.8: 3 restarts;
  - B3 Low < 0.1 → 1.2: hysteresis now scheduled.
  
  The Low total therefore rises from 505 to 815, while High falls from 103,501 to 85,860 and Max from 139,086 to 103,038. V26 §9.5 already lists the right causes ("B1 at n_dc = 67 …, the CV option at ×6, hysteresis as optional and n_c up to 1,001"). The V26 text and #51 R6 do not misattribute; only the room summary does. **Edit:** in v2.7 §6 add one line, "Change from WL: High/Max fall from n_dc 67 → 9, n_c 1,001 → 101 and G = 1; Low rises from 3 restarts and scheduled hysteresis; CV was never in WL's totals (WL L95), so its removal only drops the ×6 contingency." The direction claim "fits 1× instead of up to 6×" is correct as a statement about the contingency.

## 5. Stop/exit and safety — OK
- No stop or schedule quantity enters any policy, value, consolidation, dream or selection input. V26 and #51 contain no such input. "Stop" occurs only as grid early stopping (V26 L96; #51 R6, Q5), which is NOT adopted ("the full grid governs", M L2784), and in the #42 safety line. The grep found no "policy", "dream", "consolidation" or "reward" outside the #42 line.
- X1–X5 are stated as unchanged at V26 L7 and L166 and #51 N4. No text modifies them.
- #42 wording at V26 L7 and #51 N4 reads verbatim "no additional stop-associated reward, penalty or terminal return", with no trailing period inside the quotes. (#42 L223's source sentence ends ".\"", and the period is correctly dropped.)
- There is no shutdown-resistance objective (grep for shutdown/resist: none).
- No claims of consciousness, "alive" or "autopoietic". The only hits are the disclaimers "no consciousness claim is made or implied" (V26 L7, L166; #51 N4).
- Personal files: rg over V26 and all of `astra_serve51/` (body, parts, manifest, governing list, build.py, pieces.py, serve.py) for aidan-resume, job-shortlist, applications/ and resume found **no hits**. None of them is among the 24 governing files.

## 6. Astra and source quotes — OK
Checked against the source lines:
- **A50 L41:** #51 R1 "(d) Yes: the conservative denominator is n4+n4b+n5." and V26 L28 "Row-0 licences remain immediate failures" are verbatim.
- **A50 L56:** V26 L20 "Their causes and realization treatment remain different; their absence cannot demonstrate an unmeasured operating characteristic." is verbatim, with **"remain"** (CE50 L40's "remain[s]" corrected; V26 §9.1).
- **A50 L58:** #51 Q6 is verbatim.
- **A50 L125:** #51 R4 "Use the 990th ordered distance as the threshold, with a fixed tie rule." is verbatim, with the list dash dropped. V26 AM-11 has the same quote, truncated.
- **A50 L130:** cited as 1.8130e-05; the source gives "approximately 0.00001813". Consistent.
- **A50 L250:** #51 N1 "no freeze, execution or timing run is authorized." is verbatim.
- **A50 L97, L107, L109, L132, L142, L151:** paraphrased faithfully.
- **A50 L153:** see L-4.
- **Other sources:**
  - #41 L304 (#51 N4) is verbatim.
  - M L3422 "stays in every denominator as a non-success" is verbatim.
  - M L2009 "bin shortfall → that replicate is INCOMPLETE" is verbatim.
  - M L368 "INCOMPLETE, never passed" is verbatim.
  - M L2784 "do not stop at the first passing n." is verbatim.
  - M L1965 matches the AM-8 thresholds.
  - MP L69 "from 5-fold cross-validation over trials within a seed" is verbatim.
  - CNA2 L297 "Clip ceiling as a quantile of the unclipped output distribution" is verbatim.
  - M L1127 "t_s = 5τ in plants" is verbatim; #51 transliterates it to ASCII "5 tau" per N1.

## 7. Other notes (non-blocking)
- **L-2 (EDIT, disclosure):** the V26 header says "about 12:36–12:50 PM ET", but the file's mtime is 12:39:15 PM ET, so the stated range runs past the lock time. There is no content effect. Disclose it in v2.7 as CNA did for PP/CE50e1; do not edit in place.
- **L-3 (EDIT, cosmetic):** V26 L30's "C2 and C3 §1" should read "E2C2 and E2C3 §1" to match §10.
- The V26 header says the only computation was SHA-256 and exact integer/rational arithmetic. #51 N1 also lists "deterministic float64 evaluation of closed forms and of the noise-free recursion". The float64 work was done in the RD and CNA files, not by the Lead, so there is no conflict. Noted only.
- V26 L166 ("Nothing was sent to Astra or anyone else") was true at lock time (12:39); #51 was built at 12:40:54 PM ET.

*REVIEW ONLY. Design only. Nothing was run, sent or posted, and no other file was edited. X1–X5 and the claim ceiling unchanged. No consciousness claim is made or implied.*

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 5165b5c4c460a13446e2a31d4728b42db70465d94c63a2cb260aed2a9a87015c
