exec(open('new_sections.py').read())
r=lambda f: open(f).read().rstrip('\n')
parts=[r('hdr.md'), r('sec_2.md')+'\n'+S26.rstrip('\n'), r('sec_3.md'), r('sec_4.md'), r('sec_5.md')+'\n'+S59.rstrip('\n'), r('sec_5b.md'), r('sec_5c.md'), S5d.strip('\n'), S5e.strip('\n'), r('sec_6.md'), r('sec_7.md'), r('s14.md'), r('s15pc.md'), r('tail.md')]
txt='\n\n---\n\n'.join(p if not p.startswith('---') else p for p in parts)
txt=txt.replace('---\n\n\n\n---','---')
txt+='\n\n**DRAFT, NOT FROZEN, DESIGN ONLY.** P3 CLOSED (#42 L251). Merge with CNA v3 next.\n\n---\n'
open('v3.md','w').write(txt)
t=open('v3.md').read()
F=[
("definition PENDING; claim C-CAUSE-I","definition OPEN FOR #43 (§14 D32) [v3 C24]; claim C-CAUSE-I"),
("**T: PENDING** (declared maximum horizon, from the environment spec before freeze; whether T equals the viability horizon H_V of §6 is PENDING).","**T = H_V = 500 steps, PROPOSED DEFAULT (§14 D2) [v3 C24]**; p ≈ 0.001385 per step."),
("carried as an Astra #41 candidate, PENDING pre-freeze justification** against the precision achievable with the executed-stop count (§4.4).","carried as an Astra #41 candidate, justified against the precision at the executed-stop minimum (§4.4; §14 D8) [v3 C24]**."),
("normalizations PENDING","normalizations §14 D9 [v3 C24]"),
("t_r, t_s and the settling tolerance are PENDING, fixed on the selection partition.","t_r, t_s, the settling tolerance and per-bin coverage: CNA v3 §8.1 (§14 D22) [v3 C24]."),
("(detailed rule PENDING at freeze)","(rule: §14 D27) [v3 C24]"),
("Construction PENDING.","Construction: §14 D28 [v3 C24]."),
("m = family size counted at freeze (PENDING), α TO BE FROZEN (v1's 95% CI is a candidate only)","m = 13 and α = 0.05, PROPOSED DEFAULTS (§14 D10–D12) [v3 C24]"),
("Levels PENDING with α.","Levels: §14 D10–D12 [v3 C24]."),
("its floors PENDING |","S_k floor OPEN FOR #43 (§14 D21) |"),
("| candidate; floor PENDING |","| candidate; V_intact floor 0.40 (§14 D21) |"),
("Justify separately.\" | PENDING |","Justify separately.\" | 0.05 ΔR², separately justified, flagged for #43 (§14 D25) |"),
("one-sided Clopper–Pearson lower bound on the MET rate; level PENDING |","one-sided Clopper–Pearson lower bound on the MET rate; level one-sided 95% (v1 level; per-row OC claims sit outside the primary family) [v3 C24] |"),
("rule PROPOSED: Clopper–Pearson; level PENDING |","rule PROPOSED: Clopper–Pearson; level one-sided 95% (v1 level) [v3 C24] |"),
("with its stated source (PENDING; no frozen numbers exist","with its stated source (**OPEN FOR #43**, §14 D13; no frozen numbers exist"),
("(tolerance PENDING)","(tolerance nominal − 0.03, §14 D14)"),
("K and budget PENDING)","K per CNA v3 §7.2 and budget per §14 D23)"),
("B (v1 candidate 10,000 — carried from v1, not #41 [merge R25]; PENDING). Totals: PENDING.","B (10,000, carried from v1, not #41 [merge R25]; §14 D15). Totals: derived at the v3 merge (§14 D34)."),
("fixed search budget and dimension (PENDING)","fixed search budget and dimension (§14 D23)"),
("a pre-declared fraction (PENDING) the affected","a pre-declared fraction the affected"),
]
for o,n in F:
    assert t.count(o)==1,(o[:60],t.count(o)); t=t.replace(o,n)
open('v3.md','w').write(t)
