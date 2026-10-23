import re
RD='/workspace/review/trackB_instrument_validation_scope_v3_RD.md'
CN='/workspace/review/trackB_scope_v3_CNA_plants_confounds_observer_v1.md'
rd=open(RD).read().split('\n')
cn=open(CN).read().split('\n')
assert rd[-1]=='' and rd[-2].startswith('sha256 of all content'); rd=rd[:-2]
while rd[-1] in ('','---') or rd[-1].startswith('**DRAFT, NOT FROZEN'): rd.pop()
C=lambda a,b: cn[a-1:b]
rel=lambda L:[('#'+l if l.startswith('#') else l) for l in L]
def idx(pfx):
    r=[i for i,l in enumerate(rd) if l.startswith(pfx)]; assert len(r)==1,pfx; return r[0]
pc={1:(5,178,231),2:(4,110,175),3:(6,234,328),4:(7,331,421)}
titles={1:'MIXED-CODE plant (E42-2)',2:'Labelled dissociation contrast (E42-1)',3:'SELF observer family, pathway matching, budgets, AQ-SELF1, SIG-ATTR (E42-3, E42-4)',4:'Donor and intervention laws; comparator family; R5/R18 corrections (E42-5, E42-9)'}
starts=[idx('## §PC%d.'%k) for k in (1,2,3,4)]
end4=idx('## 8. Response table')-1
while rd[end4] in ('','---'): end4-=1
end4+=1
new=rd[:starts[0]]
for k in (1,2,3,4):
    s=starts[k-1]; 
    sec,a,b=pc[k]
    new+=['## §PC%d. %s — CNA v3 §%d, verbatim'%(k,titles[k],sec),'',
      '*Merged from CNA v3 half (`5dec96f5…`) L%d–%d; headings re-levelled only. Bare section numbers inside are CNA v3 numbering; "RD §n" is the RD body. Reconciliation: §17.*'%(a,b),'']
    new+=rel(C(a,b))
    new+=['','---','']
px=['## §PX. CNA v3 half: remaining sections, verbatim','',
 '*CNA v3 L1–107 (preamble, §1–§3) and L422–518 (§8–§12, input-hash footer); headings re-levelled only; CNA\'s own footer line is fenced. Section numbers inside are CNA v3 numbering.*','']
px+=rel(C(1,107))+['']+rel(C(422,517))+['','```']+C(518,518)+['```','','LINECHECK_PLACEHOLDER','']
new+=px+rd[end4:]
t='\n'.join(new)
PRE=[("(σ_max OPEN FOR #43)","(σ_max = κ_f·s_core [merge R32])"),
("**against the strongest baseline = max(history-matched baseline over W_B, declared proxy baseline)**","~~against the strongest baseline = max(history-matched baseline over W_B, declared proxy baseline)~~ **[merge R27] against the joint history-plus-proxy comparator J (§2.7; CNA v3 §3.1); H, P and max(H, P) are REPORTED diagnostics (#42 L65); ΔLEARN's X terms are ΔR² against J**"),
("(§5d.4)","(§5d, named-signal bullet; CNA v3 §6.6) [merge R41]"),

("| D13 | n_seed | ","| D13 | n_seed | **[merge R20, R30: range [0.25, 1.0]; noncentral-t planning 8 / 20 / 67 at m = 14; planning value 20 (Lead)]** "),
("| D14 | Coverage tolerance | nominal − 0.03 |","| D14 | Coverage tolerance | nominal − 0.03 **[merge R28: checked at a declared 95% level; per-claim coverage inferred, not certified]** |"),
("| D18 | Q-LEARN corruption process | ","| D18 | Q-LEARN corruption process | **[merge R29: audits (a) and (b) replaced, §17.2]** "),
("never a battery-wide figure (#42 L152).","never a battery-wide figure (#42 L152). **[merge R28]** Interval coverage in calibration is checked at a declared 95% level; coverage at the per-claim level 1 − α/m is inferred, not certified."),
("Planning arithmetic (power 0.90 at 1.5× margin, one-sided level 0.99615): n = ⌈((2.665 + 1.282)·σ_s/(0.5·margin))²⌉ = 4, 16, 63 at σ_s/margin = 0.25, 0.5, 1.0. **Proposed planning value for budgeting: 16** (σ_s = 0.5·margin).",
 "~~Planning arithmetic (power 0.90 at 1.5× margin, one-sided level 0.99@@615): n = ⌈((2.665 + 1.282)·σ_s/(0.5·margin))²⌉ = 4, 16, 63 at σ_s/margin = 0.25, 0.5, 1.0. Proposed planning value for budgeting: 16 (σ_s = 0.5·margin).~~ **[merge R30, R31] Planning arithmetic at m = 14 (one-sided level 0.996429, power 0.90 at 1.5× margin, noncentral t): n = 8, 20, 67 at σ_s/margin = 0.25, 0.5, 1.0 (z-approximation 4, 16, 64). Planning value: 20 (Lead ruling, M4).**"),
("**one-sided 1 − α/m = 0.99615** (Bonferroni; z = 2.665)","~~one-sided 1 − α/m = 0.99@@615 (Bonferroni; z = 2.6@@65)~~ **one-sided 1 − α/m = 0.996429 (Bonferroni; z = 2.690) [merge R31]**"),
("E-ATTR and I-ATTR join the family (CNA dependency D-RD2; §15).","E-ATTR and I-ATTR join the family (CNA dependency D-RD2; §15). **[merge R31] C-EXIST on I joins the family (Lead ruling, FINAL); the full list of 14 is in R31.**"),
("the 16 is a budgeting figure, never a certified value","~~the 16~~ **the 20 [merge R30]** is a budgeting figure, never a certified value"),
("| no by default; +1 (m = 14) if a signal is declared |","| no by default; +1 (~~m = 14~~ **m = 15 [merge R31]**) if a signal is declared |"),
("m = 14 if a named signal is declared for SIG-ATTR","~~m = 14~~ **m = 15 [merge R31]** if a named signal is declared for SIG-ATTR"),
("| MET iff lower bound of ΔR² > m_EXIST = 0.05; NOT MET iff upper bound < 0.05; else BOUNDARY | yes (1) |","| MET iff lower bound of ΔR² > m_EXIST = 0.05; NOT MET iff upper bound < 0.05; else BOUNDARY | ~~yes (1)~~ **yes (2: C-EXIST on E, C-EXIST on I) [merge R31]** |"),
("Total m = 1 + 4 + 3 + 1 + 4 = **13** (§14 D11).","Total ~~m = 1 + 4 + 3 + 1 + 4 = 13~~ **m = 2 + 4 + 3 + 1 + 4 = 14 [merge R31; Lead ruling FINAL]** (§14 D11)."),
("At level 0.99615 this leaves ≈ 38 resamples in the tail,","At level ~~0.99@@615~~ **0.996429 [merge R31]** this leaves ~~≈ 38~~ **≈ 36 (10,000 × 0.05/14 = 35.7)** resamples in the tail,"),
("{9, 12, 16, 24, 32, 48, 63}","~~{9, 12, 16, 24, 32, 48, 63}~~ **{9, 12, 16, 20, 24, 32, 48, 64, 67} [merge R30, R31]**"),
("Normal-approximation planning arithmetic; confirmed in calibration |","Normal-approximation planning arithmetic; confirmed in calibration. **[merge R31] Independent of m:** derived from the decode TOST (two-sided 90%, band ±0.05); S-INT is a safety gate outside the family, so 452 is unchanged at m = 14 |"),
]
for o,n in PRE:
    assert t.count(o)==1,o[:40]; t=t.replace(o,n)
t=t.replace("m = 13","~~m = 13~~ **m = 14 [merge R31]**").replace("0.99615","~~0.99615~~ **0.996429 [merge R31]**").replace("z = 2.665","~~z = 2.665~~ **z = 2.690**").replace("@@","").replace("**~~m = 13~~ **m = 14 [merge R31]****","~~m = 13~~ **m = 14 [merge R31]**")
# header edits
t=t.replace(rd[0],'# Track B instrument-validation scope v3 — MERGED (RD half `0892ccac…` + CNA half `5dec96f5…`)',1)
old5=[l for l in rd if l.startswith('- **What this file is.**')][0]
t=t.replace(old5,'- **What this file is.** The **merged** scope v3: the RD half (`0892ccac…`, frozen, not edited) with §PC1–§PC4 replaced by CNA\'s v3 text verbatim and CNA\'s remaining text in §PX; reconciliation in §17, the consolidated FLAGGED FOR ASTRA CONFIRMATION list in §18, OPEN FOR CNA/LEAD in §19, RD\'s light pass on CNA\'s half in Appendix L, merge method in Appendix M. New, additive file; edits nothing. Merged by RD, 2026-10-23, about 2:48–3:10 PM ET.',1)
cnarow=[l for l in rd if l.startswith('| CNA v3 half (plants')][0]
t=t.replace(cnarow,cnarow+'\n| CNA light pass on RD v3 half (applied as R27–R42) | `/workspace/review/trackB_scope_v3_RD_lightpass_CNA_v1.md` | `c47d8d47e895914fce101e75b618304d58dde9266ef21cf492741e31e1c24c8f` | `86bbc3084f6515c751862717896982dc67f38f12248f1bb4b7a5c07f990b7ad9` reproduced |\n| RD v3 half (base of this merge; frozen, not edited) | `/workspace/review/trackB_instrument_validation_scope_v3_RD.md` | `0892ccac033f165350d1382c69a2ea9b2ad9ddacb0d1e8c7908db5814c180357` | `451c130af6ce97738a726fa4a863b54314686266f65fa47e9db5e45d3bf31b13` reproduced |',1)
for o,n in [('| CNA placeholder |','| CNA text (merged, verbatim) |'),('| PC1 = CNA |','| §PC1 = CNA v3 §5 |'),('| PC2 = CNA |','| §PC2 = CNA v3 §4 |'),('| PC3 = CNA |','| §PC3 = CNA v3 §6 |'),('| partly PC4 |','| partly §PC4 = CNA v3 §7 |'),('| PC3, PC4 = CNA |','| §PC3, §PC4 = CNA v3 §6, §7 |')]:
    assert t.count(o)==1,o; t=t.replace(o,n)
n43=t.count('OPEN FOR #43')
t=t.replace('**OPEN FOR #43**','OPEN FOR #43').replace('OPEN FOR #43','~~OPEN FOR #43~~ **→ PROPOSED DEFAULT at merge (§17.1)**')
b10=[l for l in t.split('\n') if l.startswith('- **P3: CLOSED** (#42 L251). No further search')][0]
t=t.replace(b10,b10+'\n- **[merge] FLAGGED FOR ASTRA CONFIRMATION replaces OPEN FOR #43 (Lead ruling, 2:47 PM ET):** §18. OPEN FOR CNA/LEAD: §19.',1)
t=t.rstrip('\n')+'\n\n---\n\n'+open('r1.md').read()+open('r2.md').read()+open('r4.md').read()+open('r3.md').read()+'\n---\n\n'+open('lp.md').read()
t+='\n---\n\n**DRAFT, NOT FROZEN, DESIGN ONLY.** P3 CLOSED (#42 L251). Merged v3 (RD + CNA). Not authorized for any run.\n\n---\n'
# line check
strip=lambda l:l.lstrip('#').strip()
have=set(strip(l) for l in t.split('\n'))
need=[strip(l) for l in cn if l.strip()]
miss=[l for l in need if l not in have]
t=t.replace('LINECHECK_PLACEHOLDER','*Line check (script, at merge): %d of %d non-blank CNA v3 lines present; %d missing.*'%(len(need)-len(miss),len(need),len(miss)))
t=t.replace('Result: see the line-check note in §PX.','Result: %d of %d present, %d missing.'%(len(need)-len(miss),len(need),len(miss)))
open('merged.md','w').write(t)
print('OPEN43 replaced',n43,'missing',len(miss),miss[:3])
