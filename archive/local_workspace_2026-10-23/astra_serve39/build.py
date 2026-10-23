import re,hashlib,sys
sys.path.insert(0,'/workspace/astra_serve38')
SRC='/workspace/review/ckappa_classfit_synthetic_scope_record_v1_2.md'
NOTE='/workspace/review/ckappa_classfit_synthetic_scope_record_v1_2_NOTE_1.md'
L=open(SRC).read().split('\n')
def R(a,b): return '\n'.join(L[a-1:b])+'\n'
def noquote(a,b):
    out=[]
    for l in L[a-1:b]:
        if l.startswith('>'): continue
        if re.match(r'^\|[-| ]+\|$',l): continue
        if l.strip()=='| Requirement | Clause |': continue
        if l.strip()=='': continue
        out.append(l)
    return '\n'.join(out)+'\n'
src=open('/workspace/astra_serve38/build.py').read()
asc_code=src[src.index('M={'):src.index('exec(open')]
exec(asc_code)
exec(open('pieces.py').read())
body=asc(HEAD+REC+TAIL)
body=re.sub(r'(?m)^\|[-| ]+\|\n','',body)
body=re.sub(r'\n{3,}','\n\n',body)
open('c39_body.md','w').write(body)
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
import os
for f in os.listdir('send'): os.remove('send/'+f)
for i,p in enumerate(parts,1):
    if i<n: t='[c39 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[end of c39 part %d/%d - more coming, do not answer yet]'%(i,n)
    else: t='[c39 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[END OF CONSULT #39 PACKET - all %d parts sent. Please answer now.]'%n
    assert all(ord(c)<128 for c in t)
    open('send/c39_%d.txt'%i,'w').write(t)
print(n,len(body),[len(open('send/c39_%d.txt'%i).read()) for i in range(1,n+1)])
