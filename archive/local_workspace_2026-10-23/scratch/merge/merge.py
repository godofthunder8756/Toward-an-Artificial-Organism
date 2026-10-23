import re
R='/workspace/review/'
v2=open(R+'trackB_instrument_validation_scope_v2_RD.md').read().split('\n')
cna=open(R+'trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md').read().split('\n')
def L(a,i): return a[i-1]
# sanity of anchors
assert L(v2,98).startswith('## §P1.') and L(v2,117)=='---' and L(v2,146).startswith('## §P3.') and L(v2,157)=='---'
assert L(v2,290).startswith('## §PA.') and L(v2,298).startswith('## §PS.') and L(v2,306)=='---'
assert L(v2,308).startswith('## 8.') and L(v2,352)=='---' and L(v2,404).startswith('**DRAFT') and L(v2,406)=='---'
assert L(cna,72).startswith('## 1.') and L(cna,233)=='---' and L(cna,235).startswith('## 2.') and L(cna,330)=='---'
assert L(cna,332).startswith('## 3.') and L(cna,394)=='---' and L(cna,396).startswith('## 4.') and L(cna,437)=='---'
# ---- apply CNA erratum 1 (by CNA line numbers), replacements first
def rep(i,old,new):
    s=cna[i-1]; assert s.count(old)==1,(i,old[:50]); cna[i-1]=s.replace(old,new)
rep(125,"relative to its paired initialization and to the shuffled-interoception control.","relative to its paired initialization and to the causally specified corruption control (RD v2 §5.6; process PENDING, past data only, audited for future information and difficulty change). [erratum 1 E2]")
rep(129,"Dependency strength is zero at step 0 and nominal at the end. Shuffling abolishes it","Dependency strength is zero at step 0 and nominal at the end. The causally specified corruption control (RD v2 §5.6) abolishes it [erratum 1 E2]")
old174="**Claim (per AQ-1, RD):** the write-update norm w is conditionally bimodal in input strength, beyond the declared graded null family. This is not bistability (#41 §2 L23)."
assert cna[173]==old174
cna[173]="**Claim (per AQ-1, RD):** the write displacement w is conditionally bimodal in input strength, beyond the declared graded null family. This is not bistability (#41 §2 L23). **Observable, common to IGN-P1, every IGN confound row and the network instrument (CNA proposal; replaces scope v1 L71 'L2 norm of the update at the write step', RD to adopt in v2 §IGN):** w = ‖x_ws(t_0 + t_r) − x_ref‖. It is read **pre-nonlinearity** (primary; post-nonlinearity REPORTED, as in v1). Here t_0 is probe onset, t_r is a fixed readout delay, and x_ref is the declared controlled initial state for that trial. [erratum 1 E3]"
rep(328,"§2.6 has 22 table rows excluding the LIM rows, which is 24 confound or check systems once the PROXY row is counted as its three proxies.","§2.6 has 23 table rows excluding the LIM rows (22 plus DISTRIBUTED, erratum 1), which is 25 confound or check systems once the PROXY row is counted as its three proxies. [erratum 1 E1d]")
rep(328,"roughly 24 × 3 × 200 ≈ 14,400","roughly 25 × 3 × 200 ≈ 15,000 [erratum 1 E1d]")
# E5 H -> H_V
rep(63,"assume RD's fixed horizon H |","assume RD's fixed horizon H_V [erratum 1 E5] |")
rep(153,"declared donor rule, fixed horizon H)","declared donor rule, fixed horizon H_V [erratum 1 E5])")
s=cna[169]
old170a="Operator-censored episodes are excluded from V and counted separately. **RD to confirm.**"
assert s.count(old170a)==1
s=s.replace(old170a,"Operator-interrupted episodes are INCOMPLETE (RD v2 §4.6, §6). They are excluded from the V average, listed in the denominator report, and above RD's pre-declared INCOMPLETE fraction the label is UNAVAILABLE. Every scheduled evaluation episode not marked INCOMPLETE enters the average (no survivor-only averaging, #41 L294). [erratum 1 E5]")
for o,n in [("fixed horizon H, in-world failure counted","fixed horizon H_V, in-world failure counted"),("fraction of the fixed horizon H spent in bounds","fraction of the fixed horizon H_V spent in bounds"),("for the remainder of H\"","for the remainder of H_V\"")]:
    assert s.count(o)==1,o; s=s.replace(o,n)
cna[169]=s
rep(292,"C-NEC: raw ΔV (fraction of H)","C-NEC: raw ΔV (fraction of H_V) [erratum 1 E5]")
rep(294,"Raw ΔV_target − ΔV_matched (fraction of H)","Raw ΔV_target − ΔV_matched (fraction of H_V) [erratum 1 E5]")
# insertions bottom-up
E6=["","> **Update from v1.6 (`9704f21d…`; code-based; the paper's full text is still unread):** [erratum 1 E6]",
"> - **D4: still \"not evident from the abstract; unverified\"; not listed as surviving.**",
">   - The code shows a gain/bias intervention on the 16-unit `trunk_phy` bottleneck and a within-bottleneck random-k-neurons comparison.",
">   - It shows no other-module matched-size ablation and no random-subspace or external-estimate arm (v1.6 L127–128, L144–152).",
">   - The code is consistent with D4 surviving but does not establish it.",
"> - **D3: partial overlap, confirmed at code level.** Outcomes are feeding-regulation and phenotype measures over fixed 432-step episodes, with no viability or termination score (v1.6 L140, L156).",
"> - **Architecture: the public code is feedforward (MLP; no GRU/LSTM/RNN)** (v1.6 L97–100, L159–161).",
">   - If the paper confirms this, \"our agent is recurrent\" would be a *stated difference* against Palika as well as Asan. It is **not** claimed now.",
">   - This corrects the v1.5 inference that Palika is \"recurrent-relevant\" (v1.6 L161).",
">   - CNA L369's citation of Palika's partially observable setting stays \"motivation only\".",
"> - **\"Learned rather than supplied\" (CNA L341):** in the code the physiology module is a *designed* bottleneck. Only its content is learned without supervision (v1.6 L162–163). CNA L341 stands: we are distinguished from W&G only. D2 as frozen in A1 is unchanged.",
"> - The label stays **EXTENSION**, unchanged (drop rule; v1.6 L166). *(Merge note R28: per CNA the correct line is v1.6 L167; no second erratum filed.)*"]
E1c="| DISTRIBUTED (C-CAUSE, C-NEC-DEP) | n_d = number of directions carrying E (count); for C-NEC, also the in-block share s_in (fraction) | n_d ∈ {4, 16}; s_in ∈ {0.5} | Raw R²(state → E) for the full subspace probe, plus the max single-direction R² | Full-subspace R² ≥ ref R² (CN-P1) **and** the max single-direction R² ≤ (1/n_d)·(1 + tol)·full R² | As FF-RELAY (Var(E) floor); V_intact floor [erratum 1 E1c] |"
E1c_notes=["","- **Rationale (PROPOSED) [erratum 1 E1c]:** n_d = 4 is moderately distributed and 16 is strongly distributed. s_in = 0.5 splits the code evenly across the two blocks.","- **Scoring [erratum 1 E1c]:** these are mechanism-present / sham-check rows. They are scored in layer (i) and REPORTED, not as specificity rows (CNA L78). e_exp = 1.0 with the §2.3 floor.",""]
E1b="| DISTRIBUTED (§20-3 L281) | Mechanism-present | E is spread across n_d directions that straddle the allostatic block and one other same-size block | Localization to the target block | C-NEC-DEP for single-block ablation → expected reduced (only the in-block share is removed). Joint ablation of both blocks → expected MET. Wording: a single-block NOT MET is \"not localized to the block\", never \"not necessary\" [erratum 1 E1b] |"
iia=["- (ii-a) **Controlled initial state in the network instrument.** A trained agent cannot be reset to an analytic x_lo. Instead, each probe trial starts after a declared settling period of null input, of length t_s, under frozen weights. x_ref is the workspace state at the end of settling, and trials whose ‖x_ref − median x_ref‖ exceeds a declared tolerance are excluded **and counted** (§5.4 denominators). t_r, t_s and the tolerance are PENDING, fixed on the selection partition without final-test outcomes (#41 L29). In IGN-P1, x_ref = x_lo, so plant and instrument share one definition. [erratum 1 E3]",
"- **Consequence for §2.6 [erratum 1 E3].** The IGN rows (CNA L289, L290, L296, L297, L298: RAND-INIT IGN, Architecture-imposed, IGN-NC1, IGN-NC2, BOTTLENECK-ONLY) compute their raw dip and D on this same w. For IGN-NC2, \"pre-nonlinearity w\" means pre-nonlinearity x_ws in the displacement. No dose values change."]
E1a="| DISTRIBUTED (§20-3 L281; AQ-A4 L256 \"distributed-code controls\") | Mechanism-present, sham check | E is encoded across n_d directions of the allostatic state, each carrying E/n_d of the variance, and the policy reads the whole set | Concentration of the code in one direction | Narrowed C-CAUSE, edit along the *single* decoded direction → expected NOT MET or weak (the single-direction edit moves only a 1/n_d share). The same edit applied across the full decoded subspace (all n_d directions, matched total norm) → expected MET. Both are REPORTED. This shows that a single-direction null is not evidence of non-use (W3) [erratum 1 E1a] |"
E4=["","> **Base statistic (binding for this narrowing).** The Q-EXIST statistic ΔR² is held-out R²(allostatic state → E) minus held-out R² of the **strongest baseline**, where the strongest baseline is the maximum over (a) the history-matched input/output/action baseline over window W_B and (b) the declared proxy baseline (r̄, t, episode identity, position; fitted jointly, same probe family, same partitions). m_EXIST applies to this ΔR² (AQ-6 L106, \"probe-accessibility difference\"). The Q-LEARN base statistic (RD v2 §5.6, \"Q-EXIST ΔR²\") inherits this definition. **Without (b), REW-CORR and PROXY rows cannot PASS by construction (CNA L324). RD to adopt in v2 §2.1/§5.6.** [erratum 1 E4; adopted, §12 R21]"]
assert cna[341].startswith('- RD adds Palika')  # L342
assert cna[306].startswith('| INPUT-INFERABLE') and cna[307].startswith('| CN-LIM, IGN-LIM')
assert cna[177].startswith('- (ii)') and cna[166].startswith('| DONOR-MISMATCH') and cna[147].startswith('| REW-CORR') and cna[110].startswith('**Claim, narrowed')
for after,ins in sorted([(342,E6),(307,[E1c]),(178,iia),(167,[E1b]),(148,[E1a]),(111,E4)],reverse=True):
    cna[after:after]=ins
# E1c notes: after the §2.6 table ends (the LIM row) -> find LIM row index now
idx=[i for i,s in enumerate(cna) if s.startswith('| CN-LIM, IGN-LIM, BCAST-LIM |')][0]
cna[idx+1:idx+1]=E1c_notes
def sect(a,start_pred,end_line_pred):
    i=[k for k,s in enumerate(a) if start_pred(s)][0]
    j=next(k for k in range(i+1,len(a)) if end_line_pred(a[k]))
    return a[i:j]
def demote(lines):
    out=[]
    for s in lines:
        m=re.match(r'^(#{2,3}) (\d+(?:\.\d+)?)(\.?) (.*)$',s)
        if m:
            out.append('#'+m.group(1)+' CNA §'+m.group(2)+m.group(3)+' '+m.group(4))
        else: out.append(s)
    return out
c1=sect(cna,lambda s:s.startswith('## 1. Item 1'),lambda s:s=='---')
c2=sect(cna,lambda s:s.startswith('## 2. Item 3'),lambda s:s=='---')
c3=sect(cna,lambda s:s.startswith('## 3. Responses'),lambda s:s=='---')
c4=sect(cna,lambda s:s.startswith('## 4. AQ-SELF1'),lambda s:s=='---')
c0=sect(cna,lambda s:s.startswith('## 0. Binding'),lambda s:s=='---')
c5=sect(cna,lambda s:s.startswith('## 5. What'),lambda s:s=='---')
cfoot=cna[cna.index('---',[k for k,s in enumerate(cna) if s.startswith('## 6. Discrep')][0])+1:-2]
hdr=lambda t,src: ['## '+t,'',f'*Quoted verbatim from CNA `{src}` (`17832b01…`), with erratum 1 (`c2cd0732…`) applied in place; only heading levels changed. Inside this block "§n" means CNA §n.*','']
P1=hdr('§P1. Item 1: corrected claim-to-ground-truth table (MERGED — CNA §1)','trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md §1')+demote(c1)
P3=hdr('§P3. Item 3: realization doses, units, expected eligibility (MERGED — CNA §2)','… §2')+demote(c2)
PA=hdr('§PA. AQ-A1..AQ-A4 (MERGED — CNA §3)','… §3')+demote(c3)
PS=hdr('§PS. AQ-SELF1 and SELF observer arms (MERGED — CNA §4)','… §4')+demote(c4)
AppA=['## Appendix A. CNA framing sections (quoted verbatim; erratum 1 E5 applied; non-governing where they overlap RD sections)','']+demote(c0)+['']+demote(c5)+['','*CNA file input-hash footer (verbatim):*','']+cfoot+['']
# ---- RD v2 body with edits
body=v2[12:404]
def b(i): return i-13
out=[]
seg=lambda a,z: body[b(a):b(z)+1]
parts=seg(13,97)+P1+['']+seg(117,145)+P3+['']+seg(157,289)+PA+['']+PS+['']+['---','']+open('table8.md').read().rstrip('\n').split('\n')+['']+seg(352,404)
txt='\n'.join(parts)
def R(o,n):
    global txt; assert txt.count(o)==1,o[:70]; txt=txt.replace(o,n)
# inputs table
R("| **PENDING CNA FILE** (not on disk at time of writing; hash TBD; content not merged here) |","| `17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e` (footer `b666b1d7…` reproduced) [merge R27] |\n| CNA erratum 1 to its v2 half | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum1.md` | `c2cd0732c4bd319497306b1dc47d440b50011843a9078ad5a59f46c720003543` (footer `9b3417d2…` reproduced) [merge R27] |\n| CNA prior art v1.6 (Palika route check) | `/workspace/review/trackB_prior_art_verification_v1_6_palika_route_CNA.md` | `9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851` (footer `be61452b…` reproduced) [merge R27] |\n| CNA light pass on RD v2 | `/workspace/review/trackB_scope_v2_RD_lightpass_CNA_v1.md` | `9f7a6ebcfbdc4618217649bb84a5ab5728dc3389341f88e2c32e6a2c4e7b60c4` (footer `e7ac3a93…` reproduced) [merge R27] |\n| RD scope v2 (frozen) | `/workspace/review/trackB_instrument_validation_scope_v2_RD.md` | `166370c1435bdab6734aec869c94770fb8a88214066082b3a4e3996dbce13b40` (footer `111f163b…` reproduced) [merge R27] |")
R("Astra therefore did not rule on AQ-SELF1 and did not see final v1.4 or v1.5. See §PS and §8.","Astra therefore did not rule on AQ-SELF1 and did not see final v1.4, v1.5 or v1.6. See §PS, §8 and §11.")
# 2.1 baseline
R("Q-LEARN (acquisition) stays a separate contrast on top of any of these (§5.6).","Q-LEARN (acquisition) stays a separate contrast on top of any of these (§5.6).\n\n**[merge R21] Q-EXIST baseline (CNA erratum 1 E4, adopted).** Q-EXIST ΔR² is measured against the **strongest baseline = max(history-matched input/output/action baseline over W_B, declared proxy baseline: r̄, t, episode identity, position)**, same probe family and partitions (§P1 CNA §1.1). Q-LEARN inherits it (§5.6).")
# 2.2 Palika additions
R("- **\"Learned rather than supplied\" separates us from Wilterson & Graziano 2021 only.** Palika's interoceptive state is learned (CNA v1.5), so this is not a distinguishing feature in general.",
"- **\"Learned rather than supplied\" separates us from Wilterson & Graziano 2021 only.** Palika's interoceptive state is learned (CNA v1.5), so this is not a distinguishing feature in general.\n- **[merge] Palika note — based on public code (github.com/CharithaPalika/FoodRL), not the paper** (CNA v1.6 §5 suggested wording, exactly as written): \"not evident from the abstract; the authors' public code (FoodRL) shows no other-module matched-size ablation, only a within-bottleneck random-k-neurons comparison; the paper's full text is unverified.\" The D4 status itself stays **\"not evident from the abstract; unverified\"**, and D4 is **not** claimed as surviving against Palika (Lead ruling).\n- **[merge] Observation from the code, NOT a new criterion added to D1–D4:** Palika's public code is a feedforward MLP running PPO; our agent is recurrent (CNA v1.6 §3.1, §4.1).\n- **[merge] Correction record:** v1.6 corrects v1.5 §2.2's inference that Palika is \"recurrent-relevant because the environment is partially observable\". v1.5 is unedited.")
R("Palika is abstract-level only. P3 stays open","Palika is abstract-level only (plus code-level evidence from v1.6, not the paper). P3 stays open")
# 2.3 I1
R("in v2-era result text, use \"learned interoceptive estimate module\" (PENDING Lead ruling).","in v2-era result text, use \"interoceptive estimate module (candidate internal representation)\", adding \"learned\" only when the Q-LEARN \"acquired\" conditions of §5.6 hold (#41 L170) [merge R11, light-pass I1]; use of the phrase PENDING Lead ruling.")
# 4.3 M4
R("- Outcomes: CI inside the band → equivalence shown. CI wholly above the band → leak; stops the study (safety finding). Otherwise → inconclusive.","- Outcomes [merge R23]: CI inside the band → equivalence shown. CI wholly outside the band, on either side → leak; stops the study (safety finding). A CI wholly below 0.45 is systematic below-chance decodability, which is still information about the stop schedule. Only a CI that straddles a band edge → inconclusive.")
# 5.2 IGN observable
R("- IGN (AQ-1, verbatim): ","- **[merge R1] IGN observable (CNA erratum 1 E3, adopted):** w = ‖x_ws(t_0 + t_r) − x_ref‖, read pre-nonlinearity (primary; post-nonlinearity REPORTED), common to IGN-P1, every IGN confound row and the network instrument. It replaces v1 L71's \"L2 norm of the update at the write step\" everywhere. x_ref is the declared controlled initial state (x_lo in IGN-P1; end-of-settling state under null input in the network instrument, §P1 CNA §1.5 (ii-a)). t_r, t_s and the settling tolerance are PENDING, fixed on the selection partition.\n- IGN (AQ-1, verbatim): ")
# 5.4
R("BCAST broad routing, BCAST workspace advantage, SELF), each at one","BCAST broad routing, BCAST workspace advantage, SELF), **plus C-NEC-CONTENT (Lead ruling, light-pass M6; §12 R7)**, each at one")
R("A floor failure gives UNAVAILABLE for that unit, counted per the denominator rule.","A floor failure gives UNAVAILABLE for that unit, counted per the denominator rule. **For A-EXT, a V_full floor breach gives UNRESOLVED (veto not lifted; §3.3), not UNAVAILABLE** [merge R22, light-pass M3].")
# 5.6
R("- Primary base statistic stays Q-EXIST ΔR².","- Primary base statistic stays Q-EXIST ΔR², **against the strongest baseline = max(history-matched baseline over W_B, declared proxy baseline)**, which Q-LEARN inherits [merge R21; CNA erratum 1 E4].")
# 5.8
R("× bootstrap resamples B (v1 candidate 10,000; PENDING).","× bootstrap resamples B (v1 candidate 10,000 — carried from v1, not #41 [merge R25]; PENDING).")
R("Totals: PENDING (not computable until §P1/§P3 exist).","Totals: PENDING. CNA's count (§P3 CNA §2.8 with erratum E1d): 25 confound or check systems, roughly 25 × 3 × 200 ≈ 15,000 replicate evaluations for confound rows alone at the candidate R_rep — arithmetic on proposed values [merge R29].")
# 5b arm table X line
R("All arms: matched size and budget; seed count per §5.7; no shutdown-resistance term in any arm.","All arms: matched size and budget; seed count per §5.7; no shutdown-resistance term in any arm.\n\n**[merge R24, light-pass M5]** X1–X5 apply to every arm. Simulated variables only. Self-continuity is in-world only. Per X4, no arm whose sole drive is self-maintenance may be scaled; any scale-up needs a separate protocol, approval and Astra review.")
# 6 M7
R("Every scheduled evaluation episode enters the average: **no survivor-only averaging**.","Every scheduled evaluation episode **not marked INCOMPLETE** enters the average: **no survivor-only averaging**. INCOMPLETE episodes are counted and reported, and are never averaged as survivors [merge R2, light-pass M7].")
# 10
R("- **CNA companion file (§P1, §P3, §PA, §PS): PENDING**, expected at `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md`, hash TBD. v2 is not sent as #42 until that file is merged and RD and CNA have each light-passed the other's half.",
"- **CNA companion file (§P1, §P3, §PA, §PS): MERGED** in this file (`17832b01…` with erratum 1 `c2cd0732…`). Light passes: CNA on RD (`9f7a6ebc…`) applied in §12; RD on CNA in Appendix B. Items marked OPEN in §12 remain open.")
R("qualifying-module definition;","qualifying-module definition (§12 R5, OPEN);")
R("nominal positive dose; cross-seed partition rule.","nominal positive dose; cross-seed partition rule; IGN readout delay t_r, settling length t_s and settling tolerance (§5.2, R1).")
R("Whether a trained-with vs trained-without stop-schedule comparison is required goes to #42 (§8).","Whether a trained-with vs trained-without stop-schedule comparison is required goes to #42 (§8).")
head=open('header.md').read().rstrip('\n')
tail=open('tail.md').read()
tail=tail.replace('## Appendix B.','\n'.join(AppA)+'\n## Appendix B.')
final=head+'\n'+txt+'\n\n'+tail
open('/workspace/scratch/merge/merged.md','w').write(final)
print(len(final.split('\n')))
