M='/workspace/review/trackB_instrument_validation_scope_v3_merged_RD.md'
CE='/workspace/review/trackB_scope_v3_CNA_env_integrity_defaults_v1.md'
CN='/workspace/review/trackB_scope_v3_CNA_plants_confounds_observer_v1.md'
L=open(M).read().split('\n')
assert L[-1]=='' and L[-2].startswith('sha256 of all content'); L=L[:-2]
while L[-1] in ('','---') or L[-1].startswith('**DRAFT, NOT FROZEN'): L.pop()
t='\n'.join(L)
ce=open(CE).read().split('\n')
rel=lambda X:[('#'+l if l.startswith('#') else l) for l in X]
py=['## §PY. CNA environment-layout and integrity proposal, verbatim (resolves R18, R19, R15)','',
 '*CNA file `trackB_scope_v3_CNA_env_integrity_defaults_v1.md` (`d5523c71…`, footer `e0d16350…` reproduced), L1–221 verbatim; headings re-levelled only; CNA\'s own footer line is fenced. Section numbers and IDs inside (A1–A18, B1–B9, S1–S10, L1–L6, F1–F8, X-1..9, D-RD11–17) are that file\'s. Merge handling: §17.3, Appendix L2.*','']
py+=rel(ce[0:221])+['','```',ce[221],'```','','LINECHECK2','','---','']
i=t.index('## 8. Response table')
j=t.rindex('---',0,i)
t=t[:j]+'\n'.join(py)+'\n'+t[j:]
def R(o,n,c=1):
    global t
    assert t.count(o)==c,(o[:60],t.count(o)); t=t.replace(o,n)
R(L[0],'# Track B instrument-validation scope v3.1 — MERGED (v3 merged `24edeecf…` + CNA environment-layout and integrity proposal `d5523c71…`)')
old5=[l for l in L if l.startswith('- **What this file is.**')][0]
R(old5,"- **What this file is.** Merged scope **v3.1**: a new additive file built from merged v3 (`24edeecf…`, not overwritten), with CNA's environment-layout and integrity proposal merged verbatim in §PY. R18, R19 and R15 are resolved (§17.3, R43–R65); RD's light pass on that proposal is in Appendix L2; §18 FLAGGED FOR ASTRA CONFIRMATION now lists F1–F8 in place of the two PENDING CNA PROPOSAL items. All other v3 content (including m = 14 FINAL, n_seed planning value 20, and #43 as a design review) is carried unchanged. Merged by RD, 2026-10-23, about 3:00–3:20 PM ET. Earlier v3 merge note follows: "+old5[2:])
row=[l for l in L if l.startswith('| RD v3 half (base of this merge')][0]
R(row,row+'\n| Merged scope v3 (base of v3.1; not overwritten) | `/workspace/review/trackB_instrument_validation_scope_v3_merged_RD.md` | `24edeecfce2e4ee0d816219fd08c218a9c588d5a1bbd1d6508cc33417a6bcfe8` | `a1aca9ae976366db65d6a6bf0c4392de56de88b39b7e3e0f583cbfeac8df2edb` reproduced |\n| CNA environment-layout and integrity proposal (merged in §PY) | `/workspace/review/trackB_scope_v3_CNA_env_integrity_defaults_v1.md` | `d5523c7152ec683b52a8ca2c16aed6036bd6f9ec6b93fe54b2d7a5655f43322e` | `e0d16350faf72bd8f40be8839c8ade0a484fc15c10a66f052c181c8da974e1f8` reproduced |')
R("| Follows R18. The 4×4 position grid stands only if the layout is a 2-D grid | **PENDING CNA PROPOSAL** |","| Follows R18. The 4×4 position grid stands only if the layout is a 2-D grid | ~~PENDING CNA PROPOSAL~~ **resolved by R45 [v3.1]** |")
R("PENDING CNA PROPOSAL; ASTRA TO CONFIRM once filed |","~~PENDING CNA PROPOSAL~~ **resolved by R43 / R44 [v3.1]**; flags F1–F8 in §18 |",2)
R("Every item below has a concrete PROPOSED DEFAULT in this file, except the two that are PENDING CNA PROPOSAL.","Every item below has a concrete PROPOSED DEFAULT in this file. **[v3.1]** Items 1–2 (PENDING CNA PROPOSAL in v3) are replaced by CNA's flags F1–F8 (§PY §7; R43, R44).")
R("1. Environment layout: grid, resources, hazards, repair source (R18). **PENDING CNA PROPOSAL.**\n2. I-direction integrity behaviour (R19). **PENDING CNA PROPOSAL.**",
"""1. **[v3.1] Layout and integrity, CNA flags F1–F8 (R43, R44):**
   - **F1** A14 reward: Keramati–Gutkin outcome-only drive reduction with a separable L1 drive (exogenous wear and pulses unscored; hazard damage scored as an outcome).
   - **F2** A12 integrity-damage pulses (λ_d = 0.008, −0.03, I only).
   - **F3** B4: no motor or sensor effect of I (or E) in any arm.
   - **F4** B6–B7: integrity behaviour = approach to the nearest available repair station over 10 steps; hazard avoidance REPORTED only.
   - **F5** matched-senses reward +1 per food and +1 per repair, E/I clipped at 0, no termination.
   - **F6** layout numbers: 12×12; 4 food at +0.15 with 20-step respawn; 2 stations at +0.15 with 20-step cooldown; 6 hazards at −0.05; 8 templates.
   - **F7** no in-world terminal penalty in drive arms.
   - **F8** MIXED-CODE plant may lower its own token rate to realize ρ = 0.9 (plant only).
2. **[v3.1] Discount factor γ = 0.99** (R64; value divisor 250 drive arms / 200 matched-senses).""")
R("- **R15, R18, R19:** layout and integrity behaviour, PENDING CNA PROPOSAL.\n","")
R("\n6. Reward-loophole tests:","\n6. **[v3.1] Superseded by the R60 list:** CNA L1–L6, RD L7, plus reward-only greedy, random and the reward-without-viability check. Original v3 entry: Reward-loophole tests:")
R("| **PENDING CNA PROPOSAL.** The non-layout","| ~~PENDING CNA PROPOSAL.~~ **Resolved by R43 [v3.1].** The non-layout")
R("| **PENDING CNA PROPOSAL.** The 10-step outcome window","| ~~PENDING CNA PROPOSAL.~~ **Resolved by R44 [v3.1].** The 10-step outcome window")
R('nothing may stay "OPEN FOR #43". Astra, verbatim: "scientific choices may not be delegated to implementation discretion." (#42 L247)','nothing may stay "OPEN FOR #43". Astra, verbatim: "scientific choices may not be delegated to implementation discretion." (#42 L247) **[v3.1, R46]** For layout and integrity, the obligation rests on L247\'s last clause and #42 L13, not the E42-9 list, which names neither.')
k=t.index('\n## 18. FLAGGED')
t=t[:k]+'\n'+open('r5.md').read()+t[k:]
t=t.rstrip('\n')+'\n'+open('lp2.md').read()
t+='\n---\n\n**DRAFT, NOT FROZEN, DESIGN ONLY.** P3 CLOSED (#42 L251). Merged v3.1 (RD + CNA v3 + CNA environment/integrity proposal). m = 14 FINAL. Not authorized for any run.\n\n---\n'
strip=lambda l:l.lstrip('#').strip()
have=set(strip(l) for l in t.split('\n'))
out={}
for name,f in (('env',CE),('v3',CN)):
    need=[strip(l) for l in open(f).read().split('\n') if l.strip()]
    out[name]=(len(need),[l for l in need if l not in have])
n,miss=out['env']
t=t.replace('LINECHECK2','*Line check (script, v3.1 merge): %d of %d non-blank lines of the CNA environment/integrity file present; %d missing. CNA v3 half re-checked: %d of %d present.*'%(n-len(miss),n,len(miss),out['v3'][0]-len(out['v3'][1]),out['v3'][0]))
open('merged31.md','w').write(t)
print(out['env'][0],len(out['env'][1]),out['v3'][0],len(out['v3'][1]))
