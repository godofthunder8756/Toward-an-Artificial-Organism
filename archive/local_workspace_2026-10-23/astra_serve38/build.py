import re,hashlib
SRC='/workspace/review/ckappa_classfit_synthetic_scope_record_v1_1.md'
NOTE='/workspace/review/ckappa_classfit_synthetic_scope_record_v1_1_NOTE_1.md'
L=open(SRC).read().split('\n')
def R(a,b): return '\n'.join(L[a-1:b])+'\n'
M={'μ':'mu','×':'x','ε':'eps','κ':'kappa','‖':'||','·':'*','Φ':'Phi','−':'-','→':'->','§':'S','∈':'in','≈':'~','…':'...','δ':'delta','≥':'>=','≤':'<=','–':'-','—':'-','Σ':'sum','σ':'sigma','∂':'d','θ':'theta','√':'sqrt','≠':'!=','ᵀ':'^T','β':'beta','Δ':'Delta','ψ':'psi','τ':'tau','χ':'chi','λ':'lambda','ρ':'rho','±':'+-','′':"'",'ψ̄':'psi_bar','μ̄':'mu_bar','“':'"','”':'"','’':"'",'‘':"'",'≡':'==','∩':' intersect ','✓':'ok','⁻¹':'^-1'}
SUP={'⁻':'-','⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9'}
SUB={'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','ₖ':'k'}
def asc(t):
    t=t.replace('ψ̄','psi_bar').replace('μ̄','mu_bar').replace('⁻¹','^-1')
    t=re.sub('10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)',lambda m:'10^'+''.join(SUP[c] for c in m.group(1)),t)
    t=re.sub('[⁰¹²³⁴⁵⁶⁷⁸⁹]+',lambda m:'^'+''.join(SUP[c] for c in m.group(0)),t)
    t=re.sub('[₀₁₂₃₄ₖ]+',lambda m:''.join(SUB[c] for c in m.group(0)),t)
    for k,v in M.items(): t=t.replace(k,v)
    t=t.replace('**','').replace('`','')
    t=re.sub(r' \(([^()]*\.(py|json|npz)[^()]*|v1_4_N L[^()]*|closure note[^()]*)\)','',t)
    t=re.sub(r'(?m)^ +- ','- ',t)
    bad=sorted({c for c in t if ord(c)>127})
    if bad: raise SystemExit('nonascii %r'%bad)
    return t
exec(open('pieces.py').read())
body=asc(HEAD+REC+'\n=== ADDITIVE NOTE_1 (full, sha 00ec1902) ===\n'+open(NOTE).read()+TAIL)
open('c38_body.md','w').write(body)
lines=body.split('\n');parts=[];cur=''
LIM=2900
for l in lines:
    while len(l)>LIM:
        cut=l.rfind(' ',0,LIM)
        if cur: parts.append(cur);cur=''
        parts.append(l[:cut]);l=l[cut+1:]
    if len(cur)+len(l)+1>LIM and cur: parts.append(cur);cur=''
    cur+=l+'\n'
if cur: parts.append(cur)
n=len(parts)
for i,p in enumerate(parts,1):
    if i<n: t='[c38 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[end of c38 part %d/%d - more coming, do not answer yet]'%(i,n)
    else: t='[c38 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[END OF CONSULT #38 PACKET - all %d parts sent. Please answer now.]'%n
    open('send/c38_%d.txt'%i,'w').write(t)
print(n,len(body),[len(open('send/c38_%d.txt'%i).read()) for i in range(1,n+1)])
