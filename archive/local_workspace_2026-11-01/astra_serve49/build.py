# Builds the #49 ASCII send parts. Does NOT start any server and sends nothing.
import re, hashlib, os, subprocess
os.chdir('/workspace/astra_serve49')
def sha(b): return hashlib.sha256(b).hexdigest()
def foot(b): return b + ('sha256 of all content above this line: ' + sha(b) + '\n').encode()
def ok_footer(p):
    L=open(p,'rb').read().splitlines(True); return sha(b''.join(L[:-1]))==L[-1].decode().split(': ')[1].strip()
F=dict(V23='review/trackB_freezeprep_v2_3_addendum_RD.md',CE='review/trackB_scope_v3_6_CNA_E48_response_v1.md',
 ER='review/trackB_scope_v3_6_CNA_E48_response_v1_erratum1.md',RL4='review/trackB_freezeprep_v2_2_E48_4_lightpass_RD_v1.md',
 R48='astra_consult48_response.txt',V22='review/trackB_freezeprep_v2_2_addendum_RD.md',V21='review/trackB_freezeprep_v2_1_addendum_RD.md',
 V2='review/trackB_freezeprep_v2_consolidated_RD.md',M='review/trackB_instrument_validation_scope_v3_6_merged_RD.md',
 CON='repo/ACI_RESEARCH_CONSTITUTION_v3.md',KAT='scratch/fp2/kat/kat_vectors',R42='astra_consult42_response.txt',R41='astra_consult41_response.txt')
PRE=dict(V23='48f75cfb',CE='90fcb1fb',ER='65accc3c',RL4='3ae68704',R48='75f3438b',V22='9c10cbe0',V21='7b1a17d7',V2='b41f0e10',M='ab80afa5',CON='50bdfb54',KAT='aab5ebab',R42='e438e329',R41='3f3b1b87')
if not os.path.exists('governing_sha256.txt'):
    r=subprocess.run(['sha256sum']+list(F.values()),cwd='/workspace',capture_output=True,text=True,check=True)
    open('governing_sha256.txt','wb').write(foot(r.stdout.encode()))
r=subprocess.run(['sha256sum','-c','/workspace/astra_serve49/governing_sha256.txt'],cwd='/workspace',capture_output=True,text=True)
if 'FAILED' in r.stdout or not all(f+': OK' in r.stdout for f in F.values()): raise SystemExit('SHA MISMATCH - not building')
assert ok_footer('governing_sha256.txt')
tab={l.split()[1]:l.split()[0] for l in open('governing_sha256.txt') if l.strip() and not l.startswith('sha256 of')}
for k,f in F.items(): assert tab[f].startswith(PRE[k]),('PREFIX',k)
for k in ('V23','CE','ER','RL4','V22','V21','V2'): assert ok_footer('/workspace/'+F[k]),'footer '+k
print('governing hashes OK (%d files); footers OK'%len(F))
exec(open('pieces.py').read())
def rl(p): return [l.replace('\ufffd','') for l in open('/workspace/'+p,encoding='utf-8',errors='replace').read().splitlines()]
assert '"'+CEILING+'"' in rl(F['R41'])[303]
for n,q in Q42: assert q in rl(F['R42'])[n-1]
for n,q in Q48: assert q in rl(F['R48'])[n-1]
V23=open('/workspace/'+F['V23'],encoding='utf-8').read()
assert '"'+AMD_U+'"' in V23,'amendment not verbatim in v2.3'
for k in ('PENDING AIDAN\'S EXPLICIT APPROVAL','2:49 PM ET','**76,581**','**15,316,200**','**66,751,200**','**61,264,800**','**267,004,800**','No IGN code exists','**VERIFIED**','0.970519','0.934901','Not adopted','D53'): assert k in V23,k
CE=open('/workspace/'+F['CE'],encoding='utf-8').read().split('\n')
kat=open('/workspace/'+F['KAT']).read().split('\n')
for i in range(3): assert ' '.join(kat[40+i].split()[-4:]) in CE[151+i],('KAT line',i)
CON=open('/workspace/'+F['CON']).read().split('\n'); assert 'gate relaxation' in CON[154]
AMD=AMD_U.replace('\u2013','-')
sub=dict(CEILING=CEILING,AMD=AMD,**{k:tab[F[k]][:8] for k in F})
body=BODY
for k,v in sub.items(): body=body.replace('{'+k+'}',v)
assert not re.search(r'\{[A-Z0-9]+\}',body),'unfilled placeholder'
bad=sorted({c for c in body if ord(c)>127})
if bad: raise SystemExit('nonascii %r'%bad)
body=re.sub(r'\n{3,}','\n\n',body)
assert len(body)<=19000,('body too long',len(body))
for w in ('conscious','sentien','autopoie',r'\balive\b',r'\bC[45]\b'):
    for m in re.finditer(w,body,re.I):
        ctx=body[max(0,m.start()-60):m.end()+40].lower(); assert 'no consciousness' in ctx,(w,ctx)
for k in ('Q0.','Q1.','Q2.','Q3.','Q4.','Q5.','E49-n','VERDICT','Yes to both','beacon','76,581','15,316,200','66,751,200','0.99995','0.9705','0.9349','DGX Spark','No IGN code exists','VERIFIED','X1-X5','host coupling','P4-P6','High effort'): assert k in body,k
bb=foot(body.encode()); open('c49_body.md','wb').write(bb)
lines=body.split('\n'); parts=[]; cur=''; LIM=2450
for l in lines:
    while len(l)>LIM:
        cut=l.rfind('. ',0,LIM-len(cur)-1) if cur else l.rfind('. ',0,LIM)
        if cut<200:
            if cur: parts.append(cur); cur=''
            cut=l.rfind('. ',0,LIM)
        cur+=l[:cut+1]+'\n'; parts.append(cur); cur=''; l=l[cut+2:]
    if len(cur)+len(l)+1>LIM and cur: parts.append(cur); cur=''
    cur+=l+'\n'
if cur.strip(): parts.append(cur)
n=len(parts)
for f in os.listdir('send'): os.remove('send/'+f)
for i,p in enumerate(parts,1):
    if i<n: t='[c49 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[end of c49 part %d/%d - more coming, do not answer yet]'%(i,n)
    else: t='[c49 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[END OF CONSULT #49 PACKET - all %d parts sent. Please answer now.]'%n
    assert all(ord(c)<128 for c in t) and len(t)<=2600,(i,len(t))
    open('send/c49_%d.txt'%i,'w').write(t)
re_body=''.join(open('send/c49_%d.txt'%i).read().split('\n',1)[1].rsplit('\n',1)[0]+'\n' for i in range(1,n+1))
assert re.sub(r'\s+',' ',re_body).strip()==re.sub(r'\s+',' ',body).strip(),'reassembly mismatch'
man='# c49 send-part manifest (send parts carry no footer, per the #43-#48 packet precedent; this manifest covers them)\n'
man+=''.join('%s  send/c49_%d.txt  %d chars\n'%(sha(open('send/c49_%d.txt'%i,'rb').read()),i,len(open('send/c49_%d.txt'%i).read())) for i in range(1,n+1))
open('send_manifest.txt','wb').write(foot(man.encode()))
for l in open('send_manifest.txt'):
    if l.startswith('#') or l.startswith('sha256 of'): continue
    h,f=l.split()[:2]; assert sha(open(f,'rb').read())==h,f
assert ok_footer('send_manifest.txt')
assert sorted(os.listdir('send'))==sorted('c49_%d.txt'%i for i in range(1,n+1))
S=open('serve.py','rb').read(); assert ok_footer('serve.py') and b'astra_consult49_response.txt' in S and b'astra_serve49/send' in S and b'8840' in S and b'8841' in S and b'48' not in S
print('BUILD OK: %d parts, body %d chars, body sha256 %s, manifest sha256 %s, part sizes %s'%(n,len(body),sha(bb),sha(open('send_manifest.txt','rb').read()),[len(open('send/c49_%d.txt'%i).read()) for i in range(1,n+1)]))
