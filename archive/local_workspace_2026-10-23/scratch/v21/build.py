import re
R='/workspace/review/'
src=open(R+'trackB_instrument_validation_scope_v2_merged_RD.md').read().split('\n')
assert src[-1]=='' or True
lp=open(R+'trackB_scope_v2_merged_lightpass_CNA_v1.md').read().split('\n')
# drop old footer
assert src[-2].startswith('sha256 of all content above this line') or src[-1].startswith('sha256')
while src and not src[-1].startswith('sha256 of all'): src.pop()
src.pop()
L=src  # 0-indexed list; merged line n = L[n-1]
assert L[19]=='' and L[29]=='---' and L[30]=='---'
assert L[870].startswith('- **Safety exclusions') and L[879].startswith('  No positive control')
safety=L[870:880]
# line-based edits bottom-up first (indices fixed)
V1ptr='  *[v2.1 V1] This safety text (merged v2 L871–880) now also stands, word for word, as governing text in §5b under the X1–X5 restatement. This appendix copy stays non-governing; where the two differ, the stricter wording governs.*'
L.insert(880,V1ptr)
assert L[593].endswith('*(Merge note R28: per CNA the correct line is v1.6 L167; no second erratum filed.)*')
L[593]=L[593].replace(' *(Merge note R28: per CNA the correct line is v1.6 L167; no second erratum filed.)*','')
L.insert(594,'')
L.insert(595,'*[v2.1 V5] Merge note R28 (outside the verbatim E6 quote): per CNA the correct line is v1.6 L167 (the Q-NECESSITY: EXTENSION line); no second erratum filed.*')
r24=[i for i,s in enumerate(L) if s.startswith('**[merge R24, light-pass M5]**')]; assert len(r24)==1
blk=['','**[v2.1 V1, CNA merged light pass I1] Operator-safety exclusions, governing.** Quoted word for word from CNA §0 (Appendix A). Here "this file" reads as this whole v2.1 file. These exclusions are cumulative with §4 (S-INT) and this §5b; where they are stricter than other text in this file, the stricter text governs.','']+safety
L[r24[0]+1:r24[0]+1]=blk
del L[30]   # doubled ---
del L[19]   # blank inside M1 table
txt='\n'.join(L)
def RP(o,n,c=1):
    global txt; k=txt.count(o); assert k==c,(k,o[:80]); txt=txt.replace(o,n)
def ROW(tag,new):
    global txt; m=re.findall(r'^\| '+tag+r' \|.*$',txt,flags=re.M); assert len(m)==1,tag; txt=txt.replace(m[0],new)
# ---- header
RP('# Track B instrument-validation scope v2 — MERGED (RD v2 + CNA items 1, 3, AQ-A1..A4, AQ-SELF1)',
'# Track B instrument-validation scope v2.1 — MERGED (RD v2 + CNA items 1, 3, AQ-A1..A4, AQ-SELF1; supersedes merged v2 `5824d5e5…`)')
RP('- **What this file is.** A new, additive merge record.',
'- **v2.1 (2026-10-23, about 1:05 PM ET, RD).** A new, full, self-contained file that **supersedes** the merged v2 (`/workspace/review/trackB_instrument_validation_scope_v2_merged_RD.md`, `5824d5e5…`, posted and frozen, not edited). It applies CNA\'s light pass on the merge (`2d52f7d3…`), CNA erratum 2 Part A (`5ddde854…`; inserts tagged "[erratum 2]") and the Lead\'s rulings of 1:01–1:02 PM ET. Every v2.1 change is tagged "[v2.1 Vn]" and listed in §14. Section numbers are unchanged from merged v2, except the new §5c and §14.\n- **What this file is.** A new, additive merge record.')
RP('| CNA erratum 1 to its v2 half (E1–E6) | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum1.md` | `c2cd0732c4bd319497306b1dc47d440b50011843a9078ad5a59f46c720003543` | `9b3417d21ded80189125b2227dbe8817b02f4016074e717bd1c7fe047b2d5cd9` reproduced |',
'| CNA erratum 1 to its v2 half (E1–E6) | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum1.md` | `c2cd0732c4bd319497306b1dc47d440b50011843a9078ad5a59f46c720003543` | `9b3417d21ded80189125b2227dbe8817b02f4016074e717bd1c7fe047b2d5cd9` reproduced |\n| **[v2.1]** Merged scope v2 (superseded by this file; frozen, not edited) | `/workspace/review/trackB_instrument_validation_scope_v2_merged_RD.md` | `5824d5e5651aa5ba08bf91e1a2df614be8a85122c49de2fbeafcf070fea0dcf3` | `bb06b43e23e72231cfc4d02998394421b0d7cb551e93f06c182e6eddbedab7ae` reproduced |\n| **[v2.1]** CNA light pass on merged v2 | `/workspace/review/trackB_scope_v2_merged_lightpass_CNA_v1.md` | `2d52f7d372f02896e895f8350ed5b66867cb925fe4c572ae338998593424f868` | `34331e6940736e24858be38406fe0180eaaf8216f085a97c65b50af3f8a167d7` reproduced |\n| **[v2.1]** CNA erratum 2 (Part A m6 + A3 applied in place; Part B = CNA light-pass counts, noted in §14) | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum2.md` | `5ddde854099020adf113d9c1fd81a1f511d272e5d294abcd3493a1283a1878bc` | `725411374e8fc7355a4f4dc897b4be4e5ed0ca508c6a4202f184dd8a697bf866` reproduced |')
RP('(c) a CNA **PROPOSED DEFAULT** with its stated rationale (CNA sections, erratum 1); or (d) PENDING. Nothing is from data.',
'(c) a CNA **PROPOSED DEFAULT** with its stated rationale (CNA sections, erratum 1, erratum 2); or (d) PENDING. Nothing is from data. **[v2.1 V2, m1]** No PROPOSED DEFAULT may be chosen or revised by reference to any instrument outcome (#41 L186, verbatim: "Do not tune doses on final instrument outcomes.").')
# ---- erratum 2 Part A
RP('corr within tol of ρ, **and** raw R²(state → E) ≥ ρ²·(1 − tol) |',
'corr(E, r̄) ≥ ρ·(1 − tol), **and** raw R²(state → E) ≥ ρ²·(1 − tol) (both one-sided, per §2.2). **Dose-fidelity check (REPORTED only, not a realization criterion):** |corr(E, r̄) − ρ| ≤ tol·ρ, two-sided, reported per replicate and per dose so dose levels stay distinguishable; failing it never changes real_i and never makes a row PASS [erratum 2 A1] |')
RP('| corr(E, p); raw R²(state → E) | As REW-CORR | As REW-CORR |',
'| corr(E, p); raw R²(state → E) | corr(E, p) ≥ ρ_p·(1 − tol), **and** raw R²(state → E) ≥ ρ_p²·(1 − tol) (both one-sided, per §2.2). **Dose-fidelity check (REPORTED only):** |corr(E, p) − ρ_p| ≤ tol·ρ_p, two-sided, as for REW-CORR [erratum 2 A2] | As REW-CORR |')
RP('(With R = 200 the bound requires roughly ≥ 189/200 observed. That is arithmetic on the proposed values, not data.)',
'(The sidedness and level of this bound, and of the e_min floor in §2.3, follow the α and sidedness frozen under merged §5.4 (cross-reference; RD-owned). As written here, the rule is one-sided 95%: with R = 200, the smallest count meeting it is 188/200, which gives a lower bound of 0.9046 (187/200 gives 0.8986). If §5.4 freezes a two-sided 95% interval instead, the smallest count is 189/200, which gives 0.9037 (188/200 gives 0.8975). These are exact binomial computations on the proposed values, not data.) [erratum 2 A3]')
# ---- §5c governing CNA proposals
i0=lp.index('### 2.1 R5: qualifying module (PROPOSAL)'); i1=lp.index('### 3.1 arXiv 2605.26242: VERIFIED')
body=lp[i0:i1]
while body and body[-1] in ('','---'): body.pop()
hmap={'### 2.1 R5: qualifying module (PROPOSAL)':'### 5c.1 R5: qualifying module and comparator block (CNA merged light pass §2.1; Lead adopted as written)',
'### 2.2 R10: I-direction Q-CAUSE rows (PROPOSAL)':'### 5c.2 R10: I-direction Q-CAUSE rows, C-CAUSE-I (CNA merged light pass §2.2; Lead adopted as written)',
'### 2.3 R18: matched-senses termination and A-REWARD (PROPOSAL)':'### 5c.3 R18: matched-senses termination and A-REWARD (CNA merged light pass §2.3; Lead adopted as written)'}
body=[hmap.get(s,s) for s in body]
assert all(not s.startswith('###') or s.startswith('### 5c') for s in body)
S5c=['## 5c. Lead-adopted CNA definitions: R5, R10, R18 (governing) [v2.1 V7–V9]','',
'**Status: GOVERNING.** Lead ruling, 2026-10-23, 1:02 PM ET: CNA\'s recommendations for R5 (including the m8 qualifying-block definition, #41 L83), R10 and R18 are adopted **as written**. The text below is quoted word for word from CNA\'s merged light pass (`2d52f7d3…` L147–214); only the three headings are renumbered. Inside it, "Mg Lnn" means line nn of the merged v2 (`5824d5e5…`), "CNA Lnn" a line of CNA\'s half (`17832b01…`) and "#41 Lnn" a line of the raw reply. Numeric tolerances, ratios and floors it names stay PENDING / PROPOSED DEFAULT. The "Optional, for #42" bullet in §5c.3 (degradation-only cell, #41 L248) goes to #42 per the Lead (§8). No label, ceiling or safety rule is weakened by this section; the §5c.2 safety constraint is binding.','']+body+['','---','']
k=txt.index('\n## 6. Item 6:'); txt=txt[:k]+'\n'+'\n'.join(S5c)+txt[k:]
# pointers into governing text
RP('I-direction edit → an integrity-related behavioural outcome, definition PENDING)','I-direction edit → an integrity-related behavioural outcome, definition PENDING; claim C-CAUSE-I and its rows per §5c.2, Lead adopted, R10 [v2.1 V8])')
RP('| changed to ⌊K/2⌋+1; qualifying-module definition PENDING |','| changed to ⌊K/2⌋+1; qualifying module defined in §5c.1(a) (Lead adopted, R5 [v2.1 V7]); its floors PENDING |')
RP('| PENDING CNA (§PA); whether A-REWARD stays a separate arm is decided there |','| Per §5c.3 (Lead adopted, R18 [v2.1 V9]): E/I never cause in-world termination; takes A-REWARD\'s external resource-collection reward (E/I still irrelevant to reward); A-REWARD absorbed and its separate row retired; V REPORTED only. Degradation-only cell → #42 (#41 L248) |')
RP('qualifying-module definition (§12 R5, OPEN);','qualifying-module and comparator-block tolerances and ratios (definitions §5c.1; R5 RESOLVED);')
RP('I-direction Q-CAUSE outcome;','I-direction Q-CAUSE in-world integrity behaviour (claim and rows §5c.2);')
RP('7. **BCAST breadth (v1 §4.2, §7.3):** ⌈K/2⌉ → ⌊K/2⌋+1; qualifying module PENDING (§5.5).','7. **BCAST breadth (v1 §4.2, §7.3):** ⌈K/2⌉ → ⌊K/2⌋+1; qualifying module defined in §5c.1 (v2.1).')
RP('A-OBS function added and consolidated with A-REWARD and AQ-A3; A-YOKED added; one arm table (§5b).','A-OBS function added and consolidated with A-REWARD and AQ-A3; A-YOKED added; one arm table (§5b); A-REWARD absorbed into the matched-senses arm (§5c.3, v2.1).')
# O-in guard in §PS
guard='**[v2.1 V11] O-in starving guard (PROPOSED DEFAULT; Lead adopted 1:02 PM ET; also to #42 under §12 R9).** SELF counts as MET only if it is MET against **both** O-in and O-in-large, **or** a pre-specified capacity and data sweep shows O-in\'s held-out loss has plateaued below its cap. If neither holds, the SELF label is UNRESOLVED. Basis: CNA merged light pass §3.4 (the cap at the self-probe\'s parameter count can leave O-in under-capacity) and #41 L71, verbatim: "Equal parameter counts and optimizer steps alone do not address the agent\'s previous representation learning." Sweep grid: PENDING.'
k=txt.index('\n## 8. Response table'); pre=txt[:k].rstrip('\n'); assert pre.endswith('---')
txt=pre[:-3].rstrip('\n')+'\n\n'+guard+'\n\n---\n'+txt[k:]
# ---- §12 rows
m=re.findall(r'^\| R4 \|.*$',txt,flags=re.M)[0]; assert m.endswith(' |')
txt=txt.replace(m,m[:-2]+'; **Lead ratified 1:01 PM ET** (m4 [v2.1 V6]): the designated-limitation-test rule replaces the old remap for LIM rows only |')
ROW('R5','| R5 | Qualifying module (BCAST breadth) and computationally comparable block (D4/C-NEC, #41 L83; m8) | §5.5: definition PENDING | CNA merged light pass §2.1(a) qualifying module (K never shrunk; below-floor modules non-transferring, in the denominator) and §2.1(b) comparator block | **RESOLVED (Lead adopted):** CNA §2.1(a) and (b) adopted as written; governing text §5c.1 [v2.1 V7] | Lead ruling 1:02 PM ET; Astra L104, L83–89, L232–234 |')
ROW('R10','| R10 | Q-CAUSE alignment per function | §3.5: E-direction → resource approach; I-direction → integrity-related outcome (PENDING) | C-CAUSE narrowed, resource-approach outcome only (CNA §1.3); CNA merged light pass §2.2: claim C-CAUSE-I and I-direction rows | **RESOLVED (Lead adopted):** W2 governs wording; C-CAUSE-I, its rows, doses, multiplicity and its binding safety constraint adopted as written; governing text §5c.2; the in-world integrity behaviour stays PENDING (environment spec, before freeze) [v2.1 V8] | Lead ruling 1:02 PM ET; Astra L93 |')
ROW('R18','| R18 | Matched-senses arm (AQ-7/AQ-A3) | §5b arm table: E/I affect termination "no"; whether A-REWARD stays separate "decided there" | CNA merged light pass §2.3: (a) termination NO; (b) A-REWARD absorbed into the matched-senses arm | **RESOLVED (Lead adopted):** (a) and (b) adopted as written; governing text §5c.3 and the §5b arm-table row. The degradation-only cell (#41 L248) is **OPEN FOR #42** [v2.1 V9] | Lead ruling 1:02 PM ET; Astra L124–126, L248 |')
RP('CNA recommended labelled secondary outside the family','CNA recommended a labelled secondary claim outside the combined label [v2.1 V4, m3]')
m=re.findall(r'^\| R9 \|.*$',txt,flags=re.M)[0]
RP('Carried as REPORTED pending #42. No interaction with the E3 IGN observable','**[v2.1 V11]** Lead adopted (1:02 PM ET) a PROPOSED DEFAULT guard: SELF counts as MET only against both O-in and O-in-large, or with a demonstrated capacity plateau (§PS, end); the role of O-in-large still goes to #42. No interaction with the E3 IGN observable')
m=re.findall(r'^\| R12 \|.*$',txt,flags=re.M)[0]
RP('Arithmetic note: with R = 200, the one-sided 95% Clopper–Pearson lower bound first reaches 0.90 at **188/200** (0.9046), not "roughly ≥ 189/200" (CNA L265); illustrative only',
'**[v2.1 V10, m7]** Sidedness tied to §5.4: §5.4 fixes one-sided bounds for threshold decisions ("MET uses the lower one-sided bound > margin"), so the e_min/f_min floors are one-sided (CNA erratum 2 A3); the level (95%) is the v1 candidate, PENDING with α. At R = 200: one-sided 95% → smallest k = **188/200**, lower bound 0.9046 (187 → 0.8986); two-sided 95% → **189/200**, 0.9037 (188 → 0.8975). Verified by RD with scipy.stats.beta.ppf and an exact binomial-tail bisection; illustrative only')
# ---- §8
RP('## 8. Response table: every #41 item (MERGED; supersedes RD v2 §8 table)','## 8. Response table: every #41 item (v2.1; supersedes the merged v2 §8 table)')
RP('| §5.5; qualifying module → §12 R5 (OPEN) |','| §5.5; qualifying module and comparator block → §5c.1 (§12 R5, RESOLVED) |')
RP('| §5b arm table; §PA CNA §3.3; §P1 CNA §1.1; **R18 OPEN** |','| §5b arm table; §5c.3; §PA CNA §3.3; §P1 CNA §1.1; R18 RESOLVED (degradation-only cell → #42) |')
RP('| §PA CNA §3.3; §5.2 (common distribution); R18 |','| §PA CNA §3.3; §5c.3; §5.2 (common distribution); R18 |')
RP('input-only observer → §PS CNA §4.2; R8, R9 |','input-only observer → §PS CNA §4.2 and the O-in starving guard (§PS, end); R8, R9 |')
RP('| §3; §P1 CNA §1.4 (DONOR-MISMATCH, DISTRIBUTED, C-NEC-DEP / C-NEC-CONTENT); §PA CNA §3.1 checks; §12 R6, R7 |','| §3; §P1 CNA §1.4 (DONOR-MISMATCH, DISTRIBUTED, C-NEC-DEP / C-NEC-CONTENT); comparator block §5c.1(b); §PA CNA §3.1 checks; §12 R6, R7 |')
RP('| §3.3, §3.4; §P1 CNA §1.4 (A-EXT row); R6 |','| §3.3, §3.4, §3.5 (C-CAUSE-I → §5c.2); §P1 CNA §1.4 (A-EXT row); R6, R10 |')
RP('| §5.2, §5.4, §5.5; R7, R8, R12 |','| §5.2, §5.4, §5.5; R7, R8, R12 (sidedness, v2.1 V10) |')
RP('| §P3 CNA §2.2–§2.5; §5.4 denominators |','| §P3 CNA §2.2–§2.6 (REW-CORR/PROXY one-sided realization, erratum 2); §5.4 denominators; no PROPOSED DEFAULT tuned on outcomes (header, V2) |')
RP('| §20 (6) consolidated scope and resources | "Finally, supply a consolidated scope and prospective resource accounting." | RD (+CNA counts) | §5.8; §P3 CNA §2.8; this merged file |','| §20 (6) consolidated scope and resources | "Finally, supply a consolidated scope and prospective resource accounting." | RD (+CNA counts) | §5.8; §P3 CNA §2.8; this v2.1 file |')
RP('| §7 (raw L304, verbatim; CNA §0 in Appendix A carries the same text) |','| §7 (raw L304, verbatim; CNA §0 in Appendix A carries the same text); operator-safety exclusions governing in §5b (v2.1 V1) |')
a=txt.index('**Open questions for Astra at #42 (merged list; packet contents in §11):**')
b=txt.index('every item marked OPEN FOR CNA/LEAD in §12.')+len('every item marked OPEN FOR CNA/LEAD in §12.')
new42='''**Open questions for Astra at #42 (v2.1; the Lead's #42 open list, 1:02 PM ET; packet contents in §11) [v2.1 V12]:**
1. **§12 R8:** counting the two-observer SELF conjunction as one family member (with the §5.4 multiplicity family and Bonferroni method; C-NEC-CONTENT is in the family by Lead ruling, §12 R7).
2. **§12 R9:** role of O-in-large, and the O-in starving guard adopted as a PROPOSED DEFAULT (§PS, end): SELF MET only against both O-in and O-in-large, or with a demonstrated capacity plateau. #41 L71 does not settle it.
3. **§12 R20:** reward-only specificity for Q-CAUSE and Q-NECESSITY after REW-CORR is reclassified as mechanism-present for those claims (CNA D-d).
4. **§12 R26:** AQ-2 architecture-imposed control: whether it needs a trained-arm counterpart or the Stage-0 plant suffices (#41 L42 does not settle it).
5. **#41 L248, degradation-only cell:** the arms span reward-and-degradation (A-FULL), reward only (A-NOFATE) and neither (matched-senses); whether a degradation-only cell is needed (§5c.3). Not proposed as a new arm.
6. **AQ-SELF1** (new question; not in the #41 packet): the pre-specified secondary disagreement-item analysis (§PS CNA §4.1), with the input-only observer matching spec (§PS CNA §4.2).
7. **Palika et al. 2026, D4** (new question): "not evident from the abstract; unverified"; not claimed as surviving; does not block freeze (Lead) (§2.2).
8. **Files:** final prior-art v1.4 (`d7f1a43b…`), v1.5 (`3fde80d8…`) and v1.6 (`9704f21d…`), which Astra has not seen (§11); P3 stays OPEN pending #42.

**Carried from the merged v2 #42 list but not on the Lead's 1:02 PM list (OPEN FOR LEAD: include at #42 or not; not dropped):** whether a joint false-MET target is required (§5.4); whether a trained-with vs trained-without stop-schedule comparison is required (§4.5); sufficiency of the SELF retargeting justification (§2.4); P3 closure on coverage from CNA v1.5/v1.6 (§10; may ride with item 8); viability evaluation run with no scheduled stops (§6).
- For the Lead first: "self-model" wording in result text (§2.3, R11). No §12 item remains OPEN FOR CNA/LEAD after the 1:01–1:02 PM ET rulings.'''
txt=txt[:a]+new42+txt[b:]
RP('the D4 question goes to #42 (§8 Q7).','the D4 question goes to #42 (§8 item 7).')
RP('that proposal goes to Astra at #42 (§8 Q8).','that proposal goes to Astra at #42 (§8 items 8 and the carried list).')
RP('Light passes: CNA on RD (`9f7a6ebc…`) applied in §12; RD on CNA in Appendix B. Items marked OPEN in §12 remain open.','Light passes: CNA on RD (`9f7a6ebc…`) applied in §12; RD on CNA in Appendix B; CNA on the merge (`2d52f7d3…`) and CNA erratum 2 (`5ddde854…`) applied in v2.1 (§14). Items marked OPEN FOR #42 in §12 remain open.')
# ---- §11
RP('- **P3** stays OPEN and freeze-blocking until Astra rules at #42',
'''- **[v2.1 V13] Singh citation confirmed.** arXiv 2605.26242 resolves to "Can LLMs Introspect? A Reality Check" by Shashwat Singh, Tal Linzen and Shauli Ravfogel, v2, first published May 25, 2026 (2:07 PM ET), per CNA's arXiv-API check at 12:56 PM ET (CNA merged light pass §3.1). RD did not re-query; Appendix B11's "UNVERIFIED by RD" is superseded by this CNA verification.
- **[v2.1 V11] Design note, O-in starving (tied to §12 R9, which goes to #42).** The O-in cap at the self-probe's parameter count can leave O-in under-capacity, so SELF could pass from a starved observer rather than privileged access. Adopted as a PROPOSED DEFAULT (Lead, 1:02 PM ET): require SELF MET against both O-in and O-in-large, or show a capacity plateau (§PS, end). Astra is asked at #42 to rule on it (§8 item 2).
- **P3** stays OPEN and freeze-blocking until Astra rules at #42''')
# §11 heading time stays; Appendix B11
RP('Its arXiv id `2605.26242` was not checked by RD (UNVERIFIED by RD).','Its arXiv id `2605.26242` was not checked by RD (UNVERIFIED by RD). *[v2.1: verified by CNA, arXiv API, 12:56 PM ET; §11 V13.]*')
# ---- §14
V='''## 14. v2.1 changes

Sources: "Lp2" = CNA light pass on the merged v2 (`2d52f7d3…`); "E2" = CNA erratum 2 (`5ddde854…`); "Lead" = Lead rulings in the room, 2026-10-23, 1:01–1:02 PM ET (relayed). Merged v2 (`5824d5e5…`) is not edited.

| # | Change | Where in v2.1 | Source |
|---|---|---|---|
| V1 | Operator-safety exclusions from CNA §0 (merged v2 L871–880: "nothing rewards resisting or evading operators", the shutdown-resistance / operator-evasion / real-world self-continuity term ban, "S-INT-P1 … is never a trained objective") copied word for word into governing text under the X1–X5 restatement; stricter wording governs; Appendix A stays non-governing with a pointer | §5b (after the R24 line); Appendix A CNA §0 | Lp2 I1; Lead (I1, as briefed) |
| V2 | Number-provenance line: no PROPOSED DEFAULT may be chosen or revised by reference to any instrument outcome, with #41 L186 quoted verbatim | Header, provenance line | Lp2 m1 |
| V3 | Blank line removed from inside the M1 inputs table; doubled `---` reduced to one | Header | Lp2 m2 |
| V4 | R7 now reads that CNA recommended C-NEC-CONTENT "outside the combined label"; family membership unchanged (Lead ruling M6) | §12 R7 | Lp2 m3 |
| V5 | R28 merge note moved out of the verbatim E6 blockquote into a separate merge note | §PA (after E6) | Lp2 m5 |
| V6 | R4: "Lead ratified 1:01 PM ET"; designated-limitation-test rule (#41 L113/L274) replaces the old `41c1a414…` remap for LIM rows only | §12 R4 | Lp2 m4; Lead |
| V7 | R5 RESOLVED: CNA's qualifying-module definition and the m8 computationally comparable block (#41 L83) adopted as written, as governing text | §5c.1; §5.5 table; §10; §12 R5 | Lp2 §2.1, m8; Lead |
| V8 | R10 RESOLVED: C-CAUSE-I with rows, doses, multiplicity and binding safety constraint adopted as written | §5c.2; §3.5; §12 R10 | Lp2 §2.2; Lead |
| V9 | R18 RESOLVED: matched-senses arm never terminates on E/I; A-REWARD absorbed; degradation-only cell (#41 L248) → #42 | §5c.3; §5b arm table; §12 R18; §8 item 5 | Lp2 §2.3; Lead |
| V10 | Clopper–Pearson sidedness tied to §5.4 (one-sided for threshold decisions; level PENDING); both values stated: one-sided 188/200 → 0.9046 (187 → 0.8986); two-sided 189/200 → 0.9037 (188 → 0.8975); verified by RD (scipy.stats.beta.ppf in a scratch venv, plus exact binomial bisection) | §12 R12; §P3 CNA §2.4 (E2 A3) | Lp2 m7; E2 A3 |
| V11 | O-in starving guard adopted as PROPOSED DEFAULT: SELF MET only against both O-in and O-in-large, or with a demonstrated capacity plateau; else UNRESOLVED; also to #42 under R9 | §PS (end); §11; §12 R9; §8 item 2 | Lp2 §3.4; Lead |
| V12 | #42 open list replaced by the Lead's list: R8, R9, R20, R26, L248, AQ-SELF1, Palika D4, files v1.4/v1.5/v1.6; other merged-v2 questions carried as OPEN FOR LEAD, not dropped | §8 | Lead |
| V13 | Singh citation confirmed (arXiv 2605.26242, v2, May 25, 2026, per CNA 12:56 PM ET) | §11; Appendix B11 | Lp2 §3.1 |
| V14 | REW-CORR and PROXY realization criteria made one-sided; two-sided dose fidelity REPORTED only (tagged [erratum 2 A1/A2]) | §P3 CNA §2.6 | Lp2 m6; E2 Part A |
| V15 | Inputs table: merged v2, Lp2 and E2 added with full hashes and footers; response table repointed to v2.1 sections; header supersession note | Header; §8; §10 | Brief |

**Note, CNA erratum 2 Part B (not applied as text).** Part B corrects only the counts in CNA's own light pass §1a: "323 of 368 non-blank lines match byte for byte (45 not exact)" in place of "431 of 476", and "re-levelled headings (31 lines)" in place of 29. The 45 lines are 31 headings + 9 erratum-1 replacements + 1 footer + 4 preamble. No verdict changes; no text in this file depends on those counts. (RD's own check in the merge found the same nine erratum-1 lines as the only non-heading body differences.)

'''
k=txt.index('## Appendix A.'); txt=txt[:k]+V+txt[k:]
open('/workspace/scratch/v21/v21.md','w').write(txt.rstrip('\n')+'\n')
print(len(txt.split('\n')))
