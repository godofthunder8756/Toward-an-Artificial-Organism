# Builds the #48 ASCII send parts. Does NOT start any server and sends nothing.
import re, hashlib, os, subprocess
os.chdir('/workspace/astra_serve48')
def sha(b): return hashlib.sha256(b).hexdigest()
def foot(b): return b + ('sha256 of all content above this line: ' + sha(b) + '\n').encode()
V2F='review/trackB_freezeprep_v2_consolidated_RD.md'; DF='review/trackB_scope_v3_6_CNA_disposition_v1.md'
RDLF='review/trackB_scope_v3_6_CNA_disposition_lightpass_RD_v1.md'; RSF='review/trackB_scope_v3_6_CNA_response_to_RD_lightpass_v1.md'
EXP={V2F:'',DF:'e84c1b1e6f88f1b99275924bf53f8fbbfe29494b527979f8026a21309f3c3a31',RDLF:'055014cc28a9cf01ee38a9c3fbc65df5dfce1370b7be8f0b0207d0de90e08f71',
     RSF:'0e4bf4e83fdb9d5aad6253f32ac43a374439d8c69f71c7e17f44dd001505e9f8',
     'review/trackB_freezeprep_v1_consolidated_RD.md':'a043df3d','review/trackB_freezeprep_v1_prerequisites_RD.md':'69f884d5',
     'review/trackB_instrument_validation_scope_v3_6_merged_RD.md':'ab80afa5','review/trackB_scope_v3_6_addendum_RD.md':'9bbde57e',
     'astra_consult47_response.txt':'51d9f30d','astra_consult42_response.txt':'e438e329','astra_consult41_response.txt':'3f3b1b87'}
if not os.path.exists('governing_sha256.txt'):
    r=subprocess.run(['sha256sum']+list(EXP),cwd='/workspace',capture_output=True,text=True,check=True)
    open('governing_sha256.txt','wb').write(foot(r.stdout.encode()))
r=subprocess.run(['sha256sum','-c','/workspace/astra_serve48/governing_sha256.txt'],cwd='/workspace',capture_output=True,text=True)
print(r.stdout.strip())
if 'FAILED' in r.stdout or not all(f+': OK' in r.stdout for f in EXP): raise SystemExit('SHA MISMATCH - not building')
G=open('governing_sha256.txt','rb').read().splitlines(True)
assert sha(b''.join(G[:-1]))==G[-1].decode().split(': ')[1].strip(),'governing footer mismatch'
tab={l.split()[1]:l.split()[0] for l in open('governing_sha256.txt') if l.strip() and not l.startswith('sha256 of')}
assert set(tab)==set(EXP)
for f,p in EXP.items():
    if not tab[f].startswith(p): raise SystemExit('PREFIX MISMATCH %s'%f)
for f in (V2F,DF,RDLF,RSF):
    L=open('/workspace/'+f,'rb').read().splitlines(True)
    assert sha(b''.join(L[:-1]))==L[-1].decode().split(': ')[1].strip(),'footer mismatch '+f
print('governing hashes OK (%d files); v2, D, RDL, RS footers OK'%len(EXP))
exec(open('pieces.py').read())
def rl(n): return [l.replace('\ufffd','') for l in open('/workspace/astra_consult%d_response.txt'%n,encoding='utf-8',errors='replace').read().splitlines()]
r47,r42,r41=rl(47),rl(42),rl(41)
assert '"'+CEILING+'"' in r41[303],'ceiling not verbatim at #41 L304'
for n,q in Q47: assert q in r47[n-1],('#47',n,q)
for n,q in Q42: assert q in r42[n-1],('#42',n,q)
v2=open('/workspace/'+V2F,encoding='utf-8').read()
S1237_U='ε_t is keyed by (root episode ID, absolute step t). Continuations inherit the root ID and never mint a new one. Donor and pool histories use their own root IDs.'
assert v2.count(S1237_U)>=2 and S1237_U.replace('ε_t','eps_t')==S1237_ASCII,'12:37 sentence'
D=open('/workspace/'+DF,encoding='utf-8').read()
assert 'Degenerate cells are non-MET, not ineligible, for this row.' in D and 'Degenerate cells are non-MET, not ineligible, for this row.' in v2
for k in ('33·U_A < 1','B = 10,000','n_sched = 121','pooled over that replicate\'s seeds'): assert k in v2,k
body=BODY.replace('{V2}',tab[V2F][:8]).replace('{D}',tab[DF][:8]).replace('{RDL}',tab[RDLF][:8]).replace('{RS}',tab[RSF][:8]).replace('{CEILING}',CEILING).replace('{S1237}',S1237_ASCII)
for q in [Q47[0][1],Q47[1][1],Q47[2][1],Q42[0][1],S1237_ASCII]: assert q in body,('quote missing',q)
bad=sorted({c for c in body if ord(c)>127})
if bad: raise SystemExit('nonascii %r'%bad)
body=re.sub(r'\n{3,}','\n\n',body)
assert len(body)<=15000,('body too long',len(body))
for w in ('conscious','sentien','autopoie',r'\balive\b',r'\bC[45]\b'):
    for m in re.finditer(w,body,re.I):
        ctx=body[max(0,m.start()-60):m.end()+40].lower(); assert 'no consciousness' in ctx,(w,ctx)
for k in ('REW-CORR','option B','B_req','CP-floor','NLN','root episode ID','33 U_A < 1','P4-P6','VERDICT','High effort','Q0.','Q6.','E48-n','X1-X5','host coupling'): assert k in body,k
bb=foot(body.encode()); open('c48_body.md','wb').write(bb)
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
    if i<n: t='[c48 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[end of c48 part %d/%d - more coming, do not answer yet]'%(i,n)
    else: t='[c48 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[END OF CONSULT #48 PACKET - all %d parts sent. Please answer now.]'%n
    assert all(ord(c)<128 for c in t) and len(t)<=2600,(i,len(t))
    open('send/c48_%d.txt'%i,'w').write(t)
re_body=''.join(open('send/c48_%d.txt'%i).read().split('\n',1)[1].rsplit('\n',1)[0]+'\n' for i in range(1,n+1))
assert re.sub(r'\s+',' ',re_body).strip()==re.sub(r'\s+',' ',body).strip(),'reassembly mismatch'
man='# c48 send-part manifest (send parts carry no footer, per the #43-#47 packet precedent; this manifest covers them)\n'
man+=''.join('%s  send/c48_%d.txt  %d chars\n'%(sha(open('send/c48_%d.txt'%i,'rb').read()),i,len(open('send/c48_%d.txt'%i).read())) for i in range(1,n+1))
open('send_manifest.txt','wb').write(foot(man.encode()))
for l in open('send_manifest.txt'):
    if l.startswith('#') or l.startswith('sha256 of'): continue
    h,f=l.split()[:2]; assert sha(open(f,'rb').read())==h,f
M=open('send_manifest.txt','rb').read().splitlines(True); assert sha(b''.join(M[:-1]))==M[-1].decode().split(': ')[1].strip()
assert sorted(os.listdir('send'))==sorted('c48_%d.txt'%i for i in range(1,n+1)),'stray files in send/'
S=open('serve.py','rb').read().splitlines(True); assert sha(b''.join(S[:-1]))==S[-1].decode().split(': ')[1].strip(),'serve.py footer'
assert b"astra_consult48_response.txt" in S[2] and b"astra_serve48/send" in S[2] and b"8840" in b''.join(S) and b"8841" in b''.join(S)
print('BUILD OK: %d parts, body %d chars, body sha256 %s, manifest sha256 %s, part sizes %s'%(n,len(body),sha(bb),sha(open('send_manifest.txt','rb').read()),[len(open('send/c48_%d.txt'%i).read()) for i in range(1,n+1)]))
