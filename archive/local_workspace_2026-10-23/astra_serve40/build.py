import re,hashlib,os
M={'μ':'mu','×':'x','ε':'eps','κ':'kappa','‖':'||','·':'*','Φ':'Phi','−':'-','→':'->','§':'S','∈':'in','≈':'~','…':'...','≥':'>=','≤':'<=','–':'-','—':'-','√':'sqrt','≠':'!=','ᵀ':'^T','“':'"','”':'"','’':"'",'‘':"'",'✓':'ok','₂':'2'}
SUP={'⁻':'-','⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9'}
def asc(t):
    t=re.sub('10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)',lambda m:'10^'+''.join(SUP[c] for c in m.group(1)),t)
    for k,v in M.items(): t=t.replace(k,v)
    t=t.replace('**','').replace('`','')
    bad=sorted({c for c in t if ord(c)>127})
    if bad: raise SystemExit('nonascii %r'%bad)
    return t
exec(open('pieces.py').read())
body=asc(HEAD_FULL)
body=re.sub(r'\n{3,}','\n\n',body)
open('c40_body.md','w').write(body)
lines=body.split('\n');parts=[];cur=''
LIM=2900
for l in lines:
    while len(l)>LIM:
        cut=l.rfind(' ',0,LIM)
        if cur: parts.append(cur);cur=''
        parts.append(l[:cut]);l=l[cut+1:]
    if len(cur)+len(l)+1>LIM and cur: parts.append(cur);cur=''
    cur+=l+'\n'
if cur.strip(): parts.append(cur)
n=len(parts)
for f in os.listdir('send'): os.remove('send/'+f)
for i,p in enumerate(parts,1):
    if i<n: t='[c40 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[end of c40 part %d/%d - more coming, do not answer yet]'%(i,n)
    else: t='[c40 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[END OF CONSULT #40 PACKET - all %d parts sent. Please answer now.]'%n
    assert all(ord(c)<128 for c in t)
    open('send/c40_%d.txt'%i,'w').write(t)
print(n,len(body),hashlib.sha256(open('c40_body.md','rb').read()).hexdigest(),[len(open('send/c40_%d.txt'%i).read()) for i in range(1,n+1)])
