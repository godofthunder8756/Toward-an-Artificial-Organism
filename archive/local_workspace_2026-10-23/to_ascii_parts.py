import unicodedata,re,sys,os,glob
src,outdir,prefix=sys.argv[1:4]
s=open(src,encoding='utf-8').read()
m={'δ':'delta','ρ':'rho','β':'beta','α':'alpha','ε':'eps','λ':'lambda','σ':'sigma','π':'pi','τ':'tau','θ':'theta','μ':'mu','η':'eta','Δ':'Delta','Σ':'Sum','⌊':'floor(','⌋':')','⌈':'ceil(','⌉':')','≥':'>=','≤':'<=','≠':'!=','×':'x','·':'*','→':'->','←':'<-','↔':'<->','⇔':'<=>','∝':' propto ','∈':' in ','∉':' not in ','∀':'for all ','∃':'exists ','−':'-','—':'--','–':'-','§':'Sec.','′':"'",'″':"''",'≈':'~=','∞':'inf','∑':'Sum','∏':'Prod','⊆':' subset of ','∪':' union ','∩':' intersect ','¬':'not ','∧':' and ','∨':' or ','⇒':'=>','↦':'|->','…':'...','“':'"','”':'"','‘':"'",'’':"'",'⊕':' XOR ','√':'sqrt','∅':'emptyset','≡':'==','±':'+/-','½':'1/2','¼':'1/4','⅓':'1/3','∣':'|','‖':'||','⟨':'<','⟩':'>','•':'*','✓':'[ok]','✗':'[x]','⊥':'_|_','∘':' o ','⋅':'*','²':'^2','∖':' \\ ','ℓ':'l','∂':'d','∇':'grad','⊗':' (x) ','κ':'kappa'}
for k,v in m.items(): s=s.replace(k,v)
s=unicodedata.normalize('NFKD',s)
for k,v in {'Π':'Prod','⁄':'/','−':'-'}.items(): s=s.replace(k,v)
left=sorted(set(c for c in s if ord(c)>127 and not unicodedata.combining(c)))
s=''.join(c for c in s if not unicodedata.combining(c)).encode('ascii','replace').decode()
print('unmapped',left)
heads=[mm.start() for mm in re.finditer(r'\n## ',s)]
parts=[];start=0;last=0
for h in heads+[len(s)]:
    if h-start>13000 and last>start: parts.append(s[start:last]); start=last
    last=h
parts.append(s[start:])
os.makedirs(outdir,exist_ok=True)
for i,p in enumerate(parts,1): open(f'{outdir}/{prefix}{i}.txt','w').write(p); print(i,len(p))
