exec(open('h.py').read())
C=open('/workspace/review/trackB_scope_v3_CNA_plants_confounds_observer_v1.md').read().split('\n')
dep={}
for l in C[495:505]:
    m=re.match(r'^\| \*\*(D-RD\d+)\*\* \| (.*) \|$',l); assert m,l; dep[m.group(1)]=m.group(2)
assert len(dep)==10
settle={
'D-RD1':'**Settled.** Environment spec defaults §14 D0: pulses and tokens at λ = 4/H_V = 0.008/step in training and every evaluation world; d_c = 5, so W_B = 16 (D36). Layout items OPEN FOR #43 (D0).',
'D-RD2':'**Settled.** §2.6, §5.4: E-ATTR, I-ATTR and C-NEC-CONTENT are family members; SELF is one member; m = 13 (D11). **α controls false MET only** (D10; #42 L156).',
'D-RD3':'**Settled.** §14 D19: g(d) = min(1, d) with d in half-band units, memoryless, **L_m = 1**; κ_f units = noise SD per unit g, in units of s_core.',
'D-RD4':'**Settled.** §2 [v3 C3] and §2.7: max rule struck; Q-EXIST ΔR² vs J (CNA v3 §3.1); Q-LEARN inherits it (§5.6); H, P and max(H, P) REPORTED diagnostics.',
'D-RD5':'**Settled.** §5.9 and §14 D16: R_cal,dose = 50 sits outside confirmation (R_rep = 200) and outside the n_seed calibration set (R_cal,n = 200); disjoint RNG streams.',
'D-RD6':'**Settled.** Header [v3 C2] (P3 CLOSED; correction for the record); §5d (V11 plateau route withdrawn); §5c struck clauses with CNA v3 §7.3(a), §7.3(b) and §7.4 as replacement text (Lead accepted, 2:39 PM ET).',
'D-RD7':'**Settled.** §5d and §14: h = 1 (D3); L_O ≥ 0.20·Var(y) (D21); agent tuning budget 16 × 3 and full trajectory archiving (D31).',
'D-RD8':'**Settled.** A-EXT stays RD-owned: §3.3 and §14 D17.',
'D-RD9':'**Settled.** S-INT stays RD-owned: §4.3a and §14 D5–D8. The CNA "Schedule-leak" row uses the §4.3a next-step hazard label (fixed-origin label as its REPORTED secondary).',
'D-RD10':'**Settled.** §6 and §14 D20: uninterrupted scheduled evaluation and the incomplete-paired rule apply to DL-NEC, DL-CONTENT and E-ATTR/I-ATTR evaluations; CNA rows add no rule of their own.',
}
S15='## 15. Settlement of CNA\'s dependencies on RD (CNA v3 §12) [v3 C25]\n\n| ID | CNA dependency (verbatim, CNA v3 §12) | Settlement and section |\n|---|---|---|\n'
for k in sorted(dep,key=lambda x:int(x[4:])): S15+=f'| {k} | {dep[k]} | {settle[k]} |\n'
S15+='\nCNA values given as functions of RD quantities are concrete at the §14 defaults (D36).\n'
PC=f'''## §PC1. MIXED-CODE plant (E42-2) — PENDING CNA FILE

Astra, verbatim: {ql(63)} **Lead ruling (2:39 PM ET, CNA D1):** the raw wording governs — the plant must pass generic dependence and must fail E-use attribution. **Status: PENDING CNA FILE → filed** as CNA v3 §5 (`5dec96f5…`); content enters at the v3 merge. RD inputs: J (§2.7), family level (§14 D11–D12), floors (D21).

## §PC2. Labelled dissociation contrast (E42-1) — PENDING CNA FILE

Astra, verbatim: {ql(61)} **Status: PENDING CNA FILE → filed** as CNA v3 §4 (E-ATTR, I-ATTR, wording rule §4.4); content enters at the v3 merge. RD inputs: environment drivers (§14 D0), H_V (D1), family membership (§2.6), incomplete-pair rule (D20).

## §PC3. Observer pathway matching and budgets (E42-3) — PENDING CNA FILE

Astra, verbatim: {ql(235)} and {q(112,'Charging only its head parameters against an observer\'s encoder-plus-head creates an asymmetric comparison.')} {q(122,'There is no uniquely correct parameter-count equation, but the accounting must expose rather than hide the asymmetry.')} **Status: PENDING CNA FILE → filed** as CNA v3 §6.2–§6.3 (observer family, accounting table, plateau sweep diagnostic); content enters at the v3 merge. RD inputs: §5d, §14 D3, D21, D31.

## §PC4. Donor and intervention laws (E42-9) — PENDING CNA FILE

Astra, verbatim: {q(13,'conditional donor construction')} (#42 L13 list) and {q(218,'Match the declared coupling/noise law and relevant history. If matching removes all content variation or lacks support, CONTENT is unresolved.')} **Status: PENDING CNA FILE → filed** as CNA v3 §7 (DL-CAUSE, DL-NEC, DL-ATTR, DL-CONTENT, DL-COV, DL-PATCH; comparator family §7.2; R5/R18 corrections §7.3–§7.4); content enters at the v3 merge. RD inputs: g and L_m (§14 D19), H_V (D1), comparator budget (D23).
'''
open('s15pc.md','w').write(S15+'\n---\n\n'+PC)
print('ok')
