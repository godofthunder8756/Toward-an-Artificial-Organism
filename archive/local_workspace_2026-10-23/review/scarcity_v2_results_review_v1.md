# Independent review: scarcity_v2 C3 certificate (draft PR #6), v1

- **PR:** godofthunder8756/Toward-an-Artificial-Organism #6 (draft), branch `cursor/scarcity-v2-c3-certificate-eb59`.
- **Commits reviewed:**
  - freeze `16e974a` (2026-10-20 7:49 PM ET);
  - implementation `ea20fef` and results `5fa6571`, both at 9:08 PM ET.
- **Method:**
  - I worked read-only on GitHub. The branch was fetched into the scratch clone `/workspace/scratch/pr6`, and the repo was not modified, committed to or pushed.
  - Independent checks are in `/workspace/scratch/pr6_check/` (`spot.py`, `compare.py`, `spot_results.json`, `compare.log`). They were written from the FINAL protocol definitions. The PR code was **not imported or reused** for any value; I read `verdicts.py`/`upkeep.py`/`unpaid.py` only to see how control cells and K < K_suff cells were labelled.
  - Nothing was frozen. No consciousness or C4 claim is made. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate: this certificate bears on C3 pressure and representability under W2′ only.
- **Reported outcomes reviewed:**
  - SEL ADMIT
  - ACC REJECT-NARROW
  - UPK ADMIT
  - UPK_cue ADMIT
  - ROUTE ADMIT
  - ADAPT VALUE-ONLY
  - 46/46 self-tests passing

## 0. Bottom line

1. **The protocol identity checks out.**
   - `SCARCITY_V2_PROTOCOL_FINAL.md` has sha256 `ea47d1375c9e3c2fc4abdc538d714f65c66ed44243ca6ddd5e319684bd0fd4a6` both at freeze commit 16e974a and at HEAD 5fa6571.
   - This is byte-identical to `/workspace/review/scarcity_v2_protocol_FINAL.md`. **PASS.**
2. **The values check out: 100/100 independent exact comparisons match, with 0 mismatches** (§2).
   - This includes the three required spot checks:
     - SEL 1/24 at K = 2;
     - UPK 5/192 at K ≥ 16;
     - ROUTE 1/24 at L = 2.
   - It also covers the full §7.3 ACC replay slice and graded small-K cells.
3. **Labels.** No deviation, listed or unlisted, flips a reported ADMIT into a non-ADMIT in substance. Three items need an erratum before the labels can be called literal-protocol clean:
   - **(E1) ACC label type (#7).** The §7.2 precedence rule makes the primary label **REJECT-SIG(ACC)**. The §7.3 REJECT-NARROW record is preserved alongside it, not substituted for it. Either way ACC is not admitted.
   - **(E2) UPK K = 1 cells are UNRESOLVED (new; related to #8).**
     - "K = 1 → DEGENERATE" is a row of the §5.5 proved-control table, and ADMIT requirement 4 says no control may be UNRESOLVED.
     - Read literally, 8 UNRESOLVED K = 1 UPK decision cells block ADMIT(UPK). For UPK_cue, the 4 v = 3/4 cells block ADMIT(UPK_cue); the v = 1/3 cells are already CERT-ZERO through UPK-C0.
     - A one-line proof certifies them zero (§1, E2). This is an erratum or relabel, not a substantive rerun.
   - **(E3) "UNRESOLVED" below K_suff means "not searched" (#9/#11, wording).**
     - Every paid UPK cell below K_suff was left unsearched by design (`upkeep.py` header). These cells were not budget-limited.
     - RESULTS.md's "every search returned before its limit" is true but can mislead.
     - This does not change any label, because ADMIT is existential and the loophole closures govern rejections only. It does narrow the claim: **UPK is certified only at ample K** (K ≥ 26 for B_up = 1, K ≥ 16 for B_up = 2), and those cells are exactly the §5.3 closed-form self-test values.
4. **ADAPT is VALUE-ONLY as designed.** The one experimental cell of interest (SWITCHING, B_up = 1) is UNRESOLVED, with interval [0, 105/3968] at K = 64 and K = 125 only. Most other experimental cells were not searched. No label is at stake, but the ADAPT result is essentially empty (§4).

## 1. Deviation table (DEVIATIONS.md items 1–19, plus unlisted items)

Verdict key:
- **F** = faithful literal reading;
- **F-scope** = faithful, but it narrows what the result can claim;
- **L?** = could change a label under a literal reading;
- **E** = erratum needed;
- **R** = rerun needed to resolve.

| # | Item | Verdict | Reasoning |
| --- | --- | --- | --- |
| 1 | Grid inferred from the parameter table; S1/S2 not run | **F (grid); E-minor (S1/S2)** | I checked the inferred grid against §2.1/§3.3/§12. It covers clean, graded a ∈ {3/4, 5/6}, the null (3/5, 3/4) at r = 3/4 only, r ∈ {5/8, 3/4}, v ∈ {1/3, 3/4} and all 17 frozen K values. That gives 238 unpaid cells (68 clean, 102 graded a = 3/4 plus null, 68 for a = 5/6) and 544 upkeep cells (4 B_up × 2 δ × 2 v × 2 r × 17 K). §2.1 declares S1/S2 "descriptive only", so the omission cannot change a label. It is still a pre-registered descriptive output (O-SEL-R and the derangement/resample kernels in §8), so RESULTS should state "S1/S2 not run" as an omission rather than leave it implicit. The ADAPT grid is not covered by #1; see U1. |
| 2 | a = 5/6 decision-bearing; δ = 1/4 and H = 3 report-only | **F** | §1/§12 list a = 5/6 as "secondary" with no report-only clause, while δ = 1/4 and H ∈ {1, 3} are explicitly report-only (§12, §4.3). Adding decision cells can only help an existential ADMIT. I checked that SEL does not depend on a = 5/6: excluding those cells, the three SEL bins still hold 10, 8 and 10 CERT-POS cells. |
| 3 | Paid small-K SEL/ACC not searched | **F-scope; E-minor** | §7.3 makes paid ACC descriptive. §2.6 says S-DIRECT covers "all SEL, ACC and UPK cells, unpaid and paid", so paid SEL cells are literally in scope. ADMIT(SEL) is existential and already met by unpaid cells, and SEL-Z covers unpaid cells only, so the omission **cannot** change ADMIT(SEL). The SEL claim should say "certified on unpaid cells; paid SEL not evaluated". |
| 4 | Order-8 bit-flip symmetry; K > 27 treated as K = 27 | **F** | K > 27: an unpaid S-DIRECT configuration is one of 27 field vectors, so the I- and Q-phase counts are ≤ 27, which is exact. The symmetry group only affects orbit counts. ROBUST/PERMITTED are evaluated over all optima, so labels are unaffected. Any joint item-and-cue permutation is not quotiented, which is conservative. |
| 5 | Word order | **F** | An exhaustive exact search is order-invariant. |
| 6 | Replay file absent; control checked against the §7.3 quoted gaps | **F, now independently closed** | I compared every clean unpaid cell at K ∈ {1,2,3,4,6,8} × v ∈ {1/3,3/4} × r ∈ {5/8,3/4}, which includes the §7.3 slice, against a replay that extends `/workspace/scratch/scarcity_replay` (same codeword semantics). All match. The PR's reading of the order (r = 5/8 → 1/48, r = 3/4 → 1/24) is confirmed: K = 3 and 6 at v = 1/3 give ACC 1/48 at r = 5/8 and 1/24 at r = 3/4. |
| 7 | ACC kept as REJECT-NARROW rather than REJECT-SIG | **L? (label type) → E1 + Astra ruling** | All REJECT-SIG(ACC) conditions hold on the storage-attributed scope (20 clean unpaid ACC cells): CERT-POS exists (5 cells); there are no UNRESOLVED cells; there is no truncation (the largest positive-cell optimum list is 4,512, under the cap); every CERT-POS cell is SIG-UNDEFINED; and controls pass. Value-breadth REJECT-NARROW also holds, because bin (0, 1/4] has 0 CERT-POS. §7.2 says "Where rejection categories overlap, use REJECT-ABSENT, then REJECT-SIG, then REJECT-NARROW. ACC's separately established, replay-based REJECT-NARROW record (§7.3) is preserved." The most literal reading is: the **reported label is REJECT-SIG(ACC)**, and the §7.3 REJECT-NARROW **record** stays on file and is not overwritten. The PR reads "preserved" as "overrides precedence". That is defensible but not the most literal reading, and the sentence was added in edit 5 next to the precedence rule, not as an exception to it. ACC is not admitted on either reading, so no ADMIT changes. The label type matters downstream (§12 Q7: NARROW → redesign the family; SIG → the signature fails as a discriminator; neither rejects C3). Recommended erratum text: "ACC: REJECT-SIG(ACC) by §7.2 precedence; the §7.3 replay-based REJECT-NARROW(ACC) record is preserved and is also satisfied (bin (0, 1/4] has no CERT-POS cell)." Get Astra's confirmation. |
| 8 | K = 1: certified zero → DEGENERATE; uncertified → UNRESOLVED | **L? → E2** | This is correct for unpaid cells, where all K = 1 cells are DEGENERATE. In the upkeep family it leaves **all 8 decision-bearing UPK cells at K = 1 (B_up ∈ {1,2} × v × r) UNRESOLVED**. "K = 1 → DEGENERATE" is a row of the §5.5 proved-zero table, and ADMIT requirement 4 is "no control is UNRESOLVED". Read literally, that blocks ADMIT(UPK). It also blocks ADMIT(UPK_cue) through the 4 v = 3/4 cells; the v = 1/3 cells are already CERT-ZERO via UPK-C0. `verdicts.py` checks only records tagged as controls, and these cells are not tagged, so the K = 1 control was never evaluated. **Proof that fixes it:** at K = 1 the I-phase configuration (field values plus D/F marks) is a single configuration, so full's policy is input-independent. A constant policy lies in fixed_upkeep and in cue_blind_upkeep, and both are sub-classes of full, so V_full = V_fixed = V_cue_blind_upkeep and UPK = UPK_cue = UPK_ev = 0, i.e. DEGENERATE. The erratum relabels the cells; no search rerun is needed. Substantively, UPK ADMIT stands. |
| 9 | O-UPK ROBUST on the ample family; cells below K_suff UNRESOLVED | **F (ADMIT); F-scope + E3 (wording)** | ADMIT requirements 2–3 are existential per bin, and the UPK bins are B_up ∈ {1, 2}, not K. Both bins are qualified by ample cells: B = 1 has 14 CERT-POS ROBUST cells at K ≥ 26 (v = 3/4); B = 2 has 20 at K ≥ 16, with B_up = 2 decision-bearing. The edit-5 loophole closures (all cells resolved, failing bin fully resolved) are conditions on **REJECT-SIG and signature REJECT-NARROW** only, and no UPK rejection is being issued. "If unresolved cells could supply a qualifying optimum, use UNRESOLVED" is likewise a rejection-side rule, so it is moot once a bin is qualified. **The UNRESOLVED cells therefore do not matter for UPK ADMIT, apart from K = 1 (E2).** Two caveats. (a) Below K_suff no search was run; `upkeep.py` says "the search of arbitrary I-configurations is not claimed complete", so these cells were never attempted and were not stopped by the budget. RESULTS should say so (E3). (b) The admitted UPK claim is therefore **ample-capacity UPK only**: upkeep-budget pressure (B_up) with no storage scarcity. The ROBUST argument is a proof (every value-achieving policy must keep j = c durable, so the cued withdrawal applies to all optima) rather than an enumeration. I accept it as exact. |
| 10 | r = 5/8 UPK uses 1 − δ(1 − r) | **F; verified** | I enumerated independently over D-sets with fragile-field value max((1−δ)·conf + δ·r, r). B = 1 gives 5/64 and B = 2 gives 5/128 at r = 5/8, matching the PR. |
| 11 | UPK-C0: UPK_cue CERT-ZERO at v = 1/3 for every K; UPK_ev UNRESOLVED | **F** | The §5.5 proof is K-independent. All 136 decision cells at v = 1/3 have UPK_cue CERT-ZERO, so the control is resolved. The self-test named "UPK-C0 below K_suff: PASS / UNRESOLVED" reports the status of the *UPK* gap there, not of the control. It is confusingly named but not an error (E-cosmetic). UPK_ev is not a decision quantity. |
| 12 | SWITCHING read as a flip chain; IID redrawn independently | **F** | An independent uniform redraw has the same law as a flip with probability 1/2, which is how the protocol defines IID-REGIME. |
| 13 | ADAPT subclass covers only true-bit encoders; wrong-bit/dash signalling not enumerated | **F-scope (no label); R only if an ADAPT magnitude is wanted** | ADAPT is VALUE-ONLY (§7.1), so no label can change. The regime-known upper bound is valid for every encoder, so the CERT-ZERO cells that rest on it are sound regardless of the subclass: B_up = 2/3 at K ≥ 16 and B_up = 0 at K ≥ 48. The experimental B_up = 1 SWITCHING cell is UNRESOLVED with [0, 105/3968]. The **lower end 0** means the enumerated subclass found **no** advantage for adaptive_select over the trackers. Whether signalling encoders could open a gap is unknown. To report an ADAPT value, a rerun with the full encoder set (or a proof that signalling cannot help) is needed. |
| 14 | ADAPT B_up = 2 and B_up = 0 pins | **F** | I checked the B_up = 2 argument by hand: the exposed field c+2 has probability (1−v)/2 under both regimes. The pins are correctly marked as not §5.5 controls. |
| 15 | Stage-B T2 counts (2, 48, 52) | **F (value-only)** | It is used as a lower bound only at K ≥ 52. This makes ADAPT cells at K < 52 one-sided, which is consistent with the UNRESOLVED labels. |
| 16 | ROUTE optima counted as decoder pairs; sender ties not expanded | **F; verified** | My brute force over all 3^(3L) decoders gives the same per-consumer optimal-decoder counts in every clean cell (e.g. 8/6 at r = v = 3/4, L = 2; 192/72 at r = 5/8, v = 3/4, L = 3) and in graded a = 3/4, L = 2 (24/12). The interval-over-ties argument for O-ROUTE separates across inputs and is exact. |
| 17 | Budget: no search hit its limit | **F, with E3 caveat** | This is true of the searches that ran. It should be paired with an explicit list of cells that were **not searched**: UPK below K_suff, and most ADAPT experimental cells, which show 0 ms with no interval. |
| 18 | B_up = 2 optimum count 2^24; Burnside orbit closed form | **F** | This affects counts only, not labels. |
| 19 | Codebook cap of 20,000 | **F; verified** | Every truncated record has gap 0: clean unpaid K = 16/18 (75,582 and 92,378 optima), and null graded a = 3/5 at K = 6–18. The largest optimum count in any SEL- or ACC-positive cell is 4,512, below the cap, and no positive cell is truncated. This cannot change a label. |
| U1 | **Unlisted:** the ADAPT K grid is {1, 16, 26, 48, 64, 125}, a subset of the frozen stage-B grid (stage-A grid × {1, H, 2H}, capped at 125·2H) | **E (disclose); no label** | §3.3 says grid points are included regardless of optima. The subset is undisclosed. ADAPT is value-only, so no label changes, but it should be listed as deviation #20. |
| U2 | **Unlisted:** DEVIATIONS.md was committed with the implementation, at the same timestamp as the results | **E (process note)** | The readings were not pre-declared before the outcomes were known, so I can't tell which were fixed before the run. Items 7, 8 and 9 are the ones whose direction favours the reported labels. |
| U3 | **Unlisted:** §7.3 says "No search is spent rediscovering this"; the PR computed the ACC cells anyway | **F (harmless)** | Computing ACC cells was a useful cross-check (the replay control) and produced the REJECT-SIG evidence. Note it only. |
| U4 | **Unlisted:** ROUTE values equal SEL values at L = K | **Interpretive (§3)** | This is not an error but affects interpretation. Every clean ROUTE gap equals the clean SEL gap at K = L (1/24, 7/192, 1/8, 3/32), and graded a = 3/4 L = 2 equals SEL at K = 2 (227/6144, 31/12288). With ample memory and one decoder per consumer, the L-symbol channel is the same facility-location problem as a K-codeword codebook. ROUTE ADMIT therefore does **not** independently corroborate SEL; it is the same mathematical fact under S-MSG. |

**Items needing an erratum or rerun:**
- **E1 (#7)** — ACC label type; needs an Astra ruling.
- **E2 (#8, K = 1 UPK)** — relabel to DEGENERATE by proof; a literal-rule blocker of ADMIT(UPK) and ADMIT(UPK_cue) until fixed.
- **E3 (#9/#11/#17)** — state that cells below K_suff were not searched, and scope the UPK claim to ample K.
- **U1** — disclose the ADAPT grid subset.
- **U2** — process note.
- **#1/#3 minor** — S1/S2 not run; paid SEL not evaluated.
- **Rerun (#13)** — only if an ADAPT magnitude is wanted.

No item calls for a rerun to protect any ADMIT.

## 2. Independent spot checks (exact rational arithmetic)

**Scripts.** `/workspace/scratch/pr6_check/spot.py` (independent; about 65 s) and `compare.py` (joins to the PR JSON). Log: `compare.log`.
- **Semantics.** S-DIRECT codeword or facility-location for unpaid cells; full / cue_blind / static_access (one dash pattern) classes.
- **ROUTE.** S-MSG with brute force over all decoders, the sender taking the argmax per input (full_route) or per evidence (static_route).
- **UPK.** Exhaustive over D-sets for full, constant D (fixed_upkeep), and evidence-only D (cue_blind_upkeep).
- **Graded evidence.** Two looks, each correct w.p. a, with statistic n_i.

| Check | Independent value | PR value | Result |
| --- | --- | --- | --- |
| **SEL clean, v = r = 3/4, K = 2** | V_full 7/8, V_cue_blind 5/6, **gap 1/24** | 7/8, 5/6, 1/24 | **MATCH** |
| **UPK clean, B_up = 2, δ = 1/2, v = r = 3/4, ample** | **5/192** (UPK_cue = 5/192) | 5/192 and 5/192 at all 10 grid K ≥ 16; UNRESOLVED below 16 | **MATCH** |
| **ROUTE clean, v = r = 3/4, L = 2** | full_route 7/8, static 5/6, **gap 1/24**; optimal decoders 8 / 6 | same; decoder pairs 64 | **MATCH** |
| UPK B_up = 1, v = r = 3/4 | 5/96 (UPK_cue 5/96) | 5/96 at K ≥ 26 | MATCH |
| UPK r = 5/8, v = 3/4 | B1 5/64, B2 5/128 | same | MATCH |
| UPK v = 1/3 (Z4/Z4′), B_up = 0 (Z1), B_up = 3 (Z2), δ = 1/4 rows | 0; δ = 1/4 values scale as stated | same where resolved | MATCH (32 UPK rows) |
| ACC replay slice §7.3 (clean, K ≤ 8, 4 (v, r) cells) | K = 1, 2 → 0; K = 3 → 1/48, 1/24 (v = 1/3), 1/192 (v = r = 3/4), 0 (v = 3/4, r = 5/8); K = 6 → 1/48, 1/24 (v = 1/3) | same | MATCH (24 cells, all five quantities) |
| Graded a = 3/4 unpaid, K = 1–4, 4 (v, r) cells | e.g. SEL 227/6144 at r = 5/8, K = 2; ACC 311/8192 at v = 1/3, r = 3/4, K = 4 | same | MATCH (16 cells) |
| ROUTE clean L = 1, 2, 3, all (v, r); graded a = 3/4 L = 2 | e.g. 7/192 (L = 3), 1/8, 3/32, 227/6144, 31/12288; ROUTE-Z1/Z2 zeros | same, including decoder counts | MATCH (14 cells × 2) |
| Graded UPK (§5.4), a = r = 3/4, v = 1/3, B = 1 | V_full 3361/4096, V_fixed 13/16, **UPK 33/4096**, UPK_cue 0; δ = 1/4: 33/8192 | 33/4096 in graded_upk.json | MATCH |
| Zero-ADAPT values (B_up = 1, v = r = 3/4, δ = 1/2) | known 31/32, IID 119/128 | self-test 31/32, 119/128 | MATCH |

**Totals.** 100 automated comparisons with 0 mismatches, plus the graded-UPK and ADAPT values checked by hand against the PR records. The K_suff counts (16 for B_up = 2, 26 for B_up = 1) and the −3/32 and −1/32 withdrawals were already independently enumerated in `/workspace/scratch/scarcity_final/check.py` and agree with the PR self-tests: I,Q = (16,16) and (24,26), and fixed Q = 18.

**Not independently checked:**
- graded K ≥ 6 and the a = 5/6 unpaid cells;
- ROUTE L = 3 graded;
- signature labels other than the ROUTE decoder counts;
- the ADAPT interval 105/3968;
- the B_up = 2 optimum count 2^24.

## 3. Interpretation draft and claim ceiling

**What the certificate supports**, conditional on errata E1–E3:

- **SEL (ADMIT).** In W2′ under S-DIRECT, on **unpaid** cells, a cue-using memory policy strictly beats the best cue-blind policy at equal per-phase configuration count in every capacity bin. Optima carrying the declared response property exist in each bin, and all positive cells are ROBUST. The gap vanishes when the query is cue-independent (v = 1/3, SEL-Z) and at ample K. *Example:* a gap of 1/24 at K = 2 when v = r = 3/4.
- **ROUTE (ADMIT).** With an L = 2 or 3 symbol channel per consumer, a cue-aware sender beats a static sender (gap 1/24 at L = 2, v = r = 3/4). This is **the same facility-location fact as SEL with K = L** (U4). It shows the pressure is not specific to the S-DIRECT field semantics, but it is not independent evidence.
- **UPK and UPK_cue (ADMIT).** With an upkeep budget of B_up durable fields (decay δ = 1/2), state-dependent allocation of durability beats any fixed allocation. In clean cells the advantage is entirely cue-attributed: 5/96 at B = 1 and 5/192 at B = 2 (v = r = 3/4). This is certified **only at ample storage** (K ≥ K_suff = 26 and 16); it is **upkeep scarcity, not storage scarcity**. The ADMIT cells reproduce the protocol's own §5.3 closed forms; behaviour at small K is unknown, because those cells were not searched.
- **ACC (not admitted).** Storage-attributed access pressure exists at K = 3 and 6 but is absent at K ≤ 2. Every positive cell is SIG-UNDEFINED: at these small codebooks, the O-ACC operator is not applicable at any optimum. The certificate shows only that, in this family, the declared access signature cannot discriminate ACC, and the value breadth also fails. It does **not** reject C3 or the ACC role.
- **ADAPT (value-only).** There is no positive result. See §4.

**Claim ceiling (the strongest sentence this supports):**

> "In the toy world W2′, under the declared semantics and exact search, the C3 task shows strict value pressure toward cue-dependent selection and routing at scarce capacity, and toward state-dependent durability allocation under a scarce upkeep budget (at ample storage). Certified optima carrying the declared response properties exist in each declared bin. These are **pressure and representability** results about optimal policies in a specified task. They are not evidence that any learned system acquires these roles (Q-LEARN), that the roles cause behaviour in any organism or model (Q-CAUSE), that they are necessary for any capacity (Q-NECESSITY), or that such roles exist in any system (Q-EXIST)."

**Explicitly outside the ceiling:**
- any C4 or higher claim;
- any claim about consciousness, experience or awareness;
- any claim about learning dynamics, neural networks or the organism;
- "typical" or "robust across optima" for UPK below K_suff;
- any ADAPT magnitude;
- SEL on paid cells;
- treating ROUTE as independent confirmation of SEL.

## 4. What "VALUE-ONLY ADAPT" means (plain language)

ADAPT asks whether a memory that can **learn across episodes**, by updating a small register η about which query regime it is in, does better than the best non-adaptive trackers (T_const, T_2, T_3).

"VALUE-ONLY" was fixed in the protocol before the run (§7.1). For ADAPT the certificate reports **only the value difference**. It never issues ADMIT or REJECT, and no signature or response property is tested. So whatever the numbers show, ADAPT cannot become a headline role claim from this study.

What the numbers show:
- Where the answer is provable, it is **zero**:
  - when the regime is known or redrawn every episode (the controls);
  - when B_up = 2 or 3 (protecting enough fields makes the regime irrelevant);
  - when B_up = 0 at K ≥ 48.
- In the one interesting case (switching regime, one durable field), the best the certificate can say is "between 0 and 105/3968". The adaptive policies it actually enumerated **did not beat** the trackers, and the stronger policies (ones that deliberately write a wrong bit or a dash to "signal" to themselves) were not searched.
- Many other experimental cells were not searched at all.

In short, ADAPT is **not shown, not ruled out, and by design not a label**.

## 5. Questions for Astra

1. **ACC label (E1).** When REJECT-SIG(ACC) and the value-breadth REJECT-NARROW(ACC) both hold, does the §7.2 precedence make the reported label **REJECT-SIG(ACC)**, with the §7.3 REJECT-NARROW record "preserved" alongside it? Or does "preserved" override precedence for ACC, as the PR reads it? Which downstream action from §12 Q7 applies: family redesign or signature redesign?
2. **K = 1 as a control (E2).** Is the "K = 1 → DEGENERATE" row of §5.5 a control under ADMIT requirement 4? If so, may the PR certify the K = 1 UPK cells DEGENERATE by the constant-policy argument (§1 #8) as an erratum without a rerun? Or must it rerun those cells?
3. **Unsearched cells (E3).** Is a decision cell that was **never searched** (UPK below K_suff) correctly labelled UNRESOLVED under §11? Or should it carry a distinct "NOT-RUN" status? Is ADMIT(UPK) acceptable when every qualifying cell is at K ≥ K_suff, i.e. when it carries no storage-scarcity content? Should the UPK claim be explicitly scoped "ample-storage, upkeep-scarce"?
4. **ROUTE ≡ SEL (U4).** Given the exact identity of the ROUTE(L) and SEL(K = L) gaps under these semantics, should ROUTE ADMIT be reported as a semantics-robustness check on SEL rather than as an independent role?
5. **Paid SEL (#3).** §2.6 puts paid SEL cells in scope. Is "SEL certified on unpaid cells only" acceptable, or must paid SEL be searched before the card is final?
6. **ADAPT (#13, U1).** Is the undisclosed ADAPT K grid subset {1, 16, 26, 48, 64, 125} acceptable for a value-only role? Should the signalling encoders (wrong-bit or intentional-dash) be enumerated, or ruled out by proof, before any ADAPT value is quoted?
7. **ACC signature design.** All positive ACC cells are SIG-UNDEFINED because O-ACC is inapplicable at every small-codebook optimum. Is that an expected property of O-ACC at K ≤ 6? Does it indicate that the declared ACC signature is non-identifiable by construction in this family, as opposed to an empirical negative?
8. **Process (U2).** DEVIATIONS.md was committed together with the results. Is a post-hoc readings file acceptable for this certificate? Or should items 7, 8 and 9, whose direction favours the reported labels, be re-ruled independently?

## 6. Provenance

- **Protocol (identical at freeze and HEAD):** `/workspace/review/scarcity_v2_protocol_FINAL.md`, sha256 `ea47d137…0fd4a6`.
- **PR artifacts extracted to** `/workspace/scratch/pr6/ex/`: RESULTS.md, DEVIATIONS.md, verdicts.json, cells_*.json, selftests.json and graded_upk.json.
- **Independent checks:** `/workspace/scratch/pr6_check/spot.py`, `compare.py`, `spot_results.json` and `compare.log`. They extend `/workspace/scratch/scarcity_replay/replay.py` (same codeword semantics) and complement `/workspace/scratch/scarcity_final/check.py`.
- **Earlier drafts and protocol versions** in `/workspace/review/` were not touched. The repo was not modified.
