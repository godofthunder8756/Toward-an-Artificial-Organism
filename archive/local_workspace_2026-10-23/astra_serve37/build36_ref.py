import re
M={'μ':'mu','×':'x','ε':'eps','κ':'kappa','‖':'||','·':'*','Φ':'Phi','−':'-','→':'->','§':'S','∈':'in','≈':'~','…':'...','δ':'delta','≥':'>=','≤':'<=','–':'-','Σ':'Sum','½':'1/2','⊕':'(+)','₄':'4','σ':'sigma','∂':'d','₂':'2','θ':'theta','√':'sqrt','≠':'!=','ᵀ':'^T','β':'beta','¼':'1/4','Δ':'Delta','²':'^2','̄':'_bar'}
SUP={'⁻':'-','⁰':'0','¹':'1','³':'3','⁴':'4','⁵':'5','⁶':'6','⁸':'8','⁹':'9','²':'2'}
def asc(t):
    t=re.sub('10([⁻⁰¹²³⁴⁵⁶⁸⁹]+)',lambda m:'10^'+''.join(SUP[c] for c in m.group(1)),t)
    t=t.replace('D⁻¹','D^-1').replace('1)⁸','1)^8');t=t.replace('R⁸','R^8').replace('R³','R^3')
    for k,v in M.items(): t=t.replace(k,v)
    t=t.replace('**','').replace('\\*','*')
    for c in t:
        if ord(c)>127: raise SystemExit('nonascii %r'%c)
    return t
v11=asc(open('/workspace/review/ckappa_oracle_scope_record_v1_1.md').read())
v12=asc(open('/workspace/review/ckappa_oracle_scope_record_v1_2.md').read())
head="""Consult #36 - PRE-FREEZE REVIEW of the C-kappa ORACLE-ONLY SCOPE RECORD (follows your #35 READY WITH NAMED EDITS, raw sha 563e070c). Please wait for all parts (see END marker), then answer in plain ASCII. Challenge, don't endorse. High effort.

What is sent. BASE TEXT = scope record v1.1 (ckappa_oracle_scope_record_v1_1.md, sha256 e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c), IN FULL. AMENDMENT = v1.2 (ckappa_oracle_scope_record_v1_2.md, sha256 7e15e812c9ddfa17369d99f97d6dee5658aedf0dbdb9e37c947300bfc1411d7d), IN FULL; v1.2 = v1.1 plus its replacements, and v1.2 governs on conflict. v1 (1b450bcf...) is cited for lineage only. Planning note v1.3 (57899307...) carries your E35-1..12 verbatim. Both texts are transliterated to ASCII only (Greek letters spelled out, ** bold markers dropped); no content changed. Nothing has run; no code exists; no checkpoint is opened.

=== BASE TEXT: v1.1 (full) ===
"""
mid="\n=== AMENDMENT: v1.2 (full) ===\n"
tail="""
=== REVIEW CONTEXT ===
Delegate adversarial review of v1 (sha 6dbf3deb), briefly. MAJOR: S-M1 filter-composition error (wrong number of transitions stage 4->8); S-M2 headroom H did not match your separately fitted fixed-kappa comparator (H* is the right quantity); S-M3 a dry run was scheduled before freeze + application; S-M4 the inference floors allowed "two poor predictions"; S-M5 the eps range was small enough to collapse into the Jacobian test; S-M6 an ALL-group positive could be driven by XOR alone. MINOR: S-m1 results.json stores terminal exact rationals, not stage-4 beliefs (cite commit 5d9d8a7); S-m2 threshold rationale; S-m3 R_G weighting unstated; S-m4 no numerical-rank rule (E35-7); S-m5 compute undercounted; S-m6 guard vs belief-invalid accounting differed; S-m7 PR #7 VAL holdout tabulation; S-m8 MARG label wording; S-m9 package order; S-m10 O7 details/disclaimer.

Delegate delta check of v1.1 (sha ff7b434a): PASS WITH NOTES. All S-M1..6 resolved (S-M2 and S-M3 via D-1, D-2); S-m1..10 resolved (S-m5 partial). New items D-1 (MAJOR: one eps symbol for oracle and neural units, against E35-9), D-2 (MAJOR: step-0 projection undefined; exact-rational O1 timing unrepresentative), D-3 (neural low-headroom guard; seed roll-up precedence), D-4 (neural Pred_full with B frozen; E35-3 sentence), D-5 (failed edits in loss sums), D-6 (compute counts ~1e6). All six are addressed in v1.2. H* reading: H* is oracle-only and computed before any checkpoint, but it is NOT the neural achievable gain: O6 eps acts on standardized synthetic coordinates (a unit v moves the chart ~0.61*eps s.d. RMS), while neural eps acts on absolute GRU hidden units through the checkpoint's fitted B. So H*(eps_syn=0.1) is an oracle-scale resolvability reference; the neural floors are relative, so the neural achievable gain is the checkpoint's own L_mu. Floor arithmetic: write S = Sum||dF||^2, L_mu = E_s + K, L_full = E_s + e (shared non-kappa error E_s, kappa-part errors K and e). Floor (a) gives e <= K/2 - E_s/2: the full model must remove at least half the kappa-part squared error, i.e. at most ~71% RMS kappa error may remain; shared error makes (a) harder. At R*=0.05, E_s~0: K~0.05*S, (b) binds the comparator weakly and (a) requires e <= 0.025*S. It closes the "two poor predictions" case at the declared level but does not guarantee good kappa accuracy.

Research Lead rulings (binding): Step 0 (the timing check) runs only after the manifest seal and the filed standing-approval application. Cap: 1 CPU, no GPU, 4 GB, 10 cumulative minutes, no auto-retries, no checkpoint loading.

=== QUESTIONS ===
(1) Does the scope record (v1.1 + v1.2) conform to E35-1..12, especially E35-9 unit separation after the eps_syn rename?
(2) Is H* the right headroom basis, as an oracle-scale resolvability reference? Are the S5 thresholds acceptable as declared conventions?
(3) Is floor (a) (L_full <= L_mu/2) plus normalized error <= 0.25 adequate? Is the 1/2 enough, or tighten (e.g. 1/4)? Also rule on: the 8/10 seed quota with dependent folds; the roll-up precedence (UNRESOLVED > HEADROOM NOT MET > PASS > FAIL per seed; package NEURAL HEADROOM NOT MET if >2 seeds HEADROOM NOT MET, then UNRESOLVED, POSITIVE, NOT SHOWN, MIXED); and whether eps in {0.1, 0.25} escapes the linear regime.
(4) CNA question: the noise guard (L_mu <= 1e-12 * Sum||dF||^2) does not stop a seed passing by halving an already-negligible comparator loss. Should a declared neural floor L_mu / Sum||dF||^2 >= 0.02 be added now? Yes or no, and what value and rationale?
(5) Verdict: FREEZE, FREEZE WITH NAMED EDITS (give the edits verbatim, numbered E36-1..), or REVISE. List what must be in the freeze manifest.
"""
body=head+v11+mid+v12+tail
open('c36_body.md','w').write(body)
lines=body.split('\n');parts=[];cur=''
for l in lines:
    while len(l)>2700:
        cut=l.rfind(' ',0,2700); 
        if cur: parts.append(cur);cur=''
        parts.append(l[:cut]);l=l[cut+1:]
    if len(cur)+len(l)+1>2700 and cur: parts.append(cur);cur=''
    cur+=l+'\n'
if cur: parts.append(cur)
n=len(parts)
for i,p in enumerate(parts,1):
    t='[c36 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[end of c36 part %d/%d - more coming, do not answer yet]'%(i,n) if i<n else '[c36 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[END OF CONSULT #36 PACKET - all %d parts sent. Please answer now.]'%n
    open('send/c36_%d.txt'%i,'w').write(t)
print(n,[len(open('send/c36_%d.txt'%i).read()) for i in range(1,n+1)], len(body))
