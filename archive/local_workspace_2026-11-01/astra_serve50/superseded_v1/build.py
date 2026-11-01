# Builds the #50 ASCII send parts. Does NOT start any server and sends nothing.
import re, hashlib, os, subprocess
os.chdir('/workspace/astra_serve50')
def sha(b): return hashlib.sha256(b).hexdigest()
def foot(b): return b + ('sha256 of all content above this line: ' + sha(b) + '\n').encode()
def ok_footer(p):
    L=open(p,'rb').read().splitlines(True); return sha(b''.join(L[:-1]))==L[-1].decode().split(': ')[1].strip()
def ok_proj_footer(p):
    b=open(p,'rb').read(); i=b.rfind(b'sha256 of all content above this line:')
    return i>0 and sha(b[:i])==b[i:].split(b':')[1].strip()[:64].decode()
F=dict(V25='review/trackB_freezeprep_v2_5_consolidated_Lead.md',A49='astra_consult49_response.txt',
 CE49='review/trackB_scope_v3_6_CNA_E49_1_E49_3_v1.md',CE49A1='review/trackB_scope_v3_6_CNA_E49_1_E49_3_v1_addendum1.md',
 RDL='review/trackB_scope_v3_6_CNA_E49_1_E49_3_lightpass_RD_v1.md',LC='review/trackB_ign_full_procedure_cost_v1_Lead.md',
 LCL='review/trackB_ign_cost_v1_lightpass_items2to4_RD.md',CD0='review/trackB_scope_v3_6_CNA_dose0_and_ignp1_xref_v1.md',
 LP2='review/trackB_scope_v3_6_CNA_dose0_xref_and_E49_addendum1_lightpass_RD_v1.md',V25RD='review/trackB_freezeprep_v2_5_E49_2_IGN_wording_RD.md',
 V24='review/trackB_freezeprep_v2_4_governance_addendum_RD.md',AMD='review/constitution_amendment_A-2026-10-24_record.md',
 M='review/trackB_instrument_validation_scope_v3_6_merged_RD.md',MP='review/trackB_measurement_plan_v1_RD.md',
 A44='astra_consult44_response.txt',KV='scratch/fp2/kat/kat_vectors',CON='repo/ACI_RESEARCH_CONSTITUTION_v3.md',
 R42='astra_consult42_response.txt',R41='astra_consult41_response.txt',CNA2='review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md')
PRE=dict(V25='d101438d',A49='6b66bbba',CE49='d620918f',CE49A1='55030ebd',RDL='a44ff0d6',LC='7d4cbbad',LCL='d5ee9a1b',CD0='647a72d2',LP2='6c02198c',
 V25RD='ae80cc12',V24='cf56c653',AMD='2f29a07a',M='ab80afa5',MP='1d5458e3',A44='49afbb5d',KV='aab5ebab',CON='50bdfb54',R42='e438e329',R41='3f3b1b87',CNA2='17832b01')
if not os.path.exists('governing_sha256.txt'):
    r=subprocess.run(['sha256sum']+list(F.values()),cwd='/workspace',capture_output=True,text=True,check=True)
    open('governing_sha256.txt','wb').write(foot(r.stdout.encode()))
r=subprocess.run(['sha256sum','-c','/workspace/astra_serve50/governing_sha256.txt'],cwd='/workspace',capture_output=True,text=True)
if 'FAILED' in r.stdout or not all(f+': OK' in r.stdout for f in F.values()): raise SystemExit('SHA MISMATCH - not building')
assert ok_footer('governing_sha256.txt')
tab={l.split()[1]:l.split()[0] for l in open('governing_sha256.txt') if l.strip() and not l.startswith('sha256 of')}
for k,f in F.items(): assert tab[f].startswith(PRE[k]),('PREFIX',k)
for k in ('V25','CE49','CE49A1','RDL','LC','LCL','CD0','LP2','V25RD','V24','AMD','M','CNA2'): assert ok_proj_footer('/workspace/'+F[k]),'footer '+k
print('governing hashes OK (%d files); footers OK'%len(F))
exec(open('pieces.py').read())
def rl(p): return [l.replace('\ufffd','') for l in open('/workspace/'+p,encoding='utf-8',errors='replace').read().splitlines()]
assert '"'+CEILING+'"' in rl(F['R41'])[303]
for n,q in Q42: assert q in rl(F['R42'])[n-1]
for n,q in Q49: assert q in rl(F['A49'])[n-1],('A49',n)
for n,q in Q44: assert q in rl(F['A44'])[n-1],('A44',n)
for n,q in QM: assert q in rl(F['M'])[n-1],('M',n)
# KAT labels and permutation hash
kv=rl(F['KV'])
for i,R in zip(range(37,43),(7,7,7,10,10,10)): assert kv[i].split()[0]=='philox4x64' and int(kv[i].split()[1])==R,('KV',i+1)
PERM='fa85f5518477d78bf72e2048786a42aa8401807a87fe4782cb52b8d936091379'
for k in ('CE49A1','LP2','V25'): assert PERM in open('/workspace/'+F[k],encoding='utf-8').read(),('perm',k)
# Recost (exact integer arithmetic) and cross-check against v2.5
GRID=[9,12,16,20,24,32,48,64,67]; CAL=200*4572*sum(GRID); A3=2*200*4572; CONF=200*4572
cs,cn,fs,fn=6,7,11,9
def T(n): return cs*(CAL+A3*n)+fs*CONF*n, cn*(CAL+A3*n)+fn*CONF*n
TC=(cs+cn)*CAL; TS=(cs+cn)*A3+(fs+fn)*CONF
s67,n67=T(67); s9,n9=T(9); t67=s67+n67; t9=s9+n9
U=lambda n:(cs+cn)*(200*sum(GRID)+400*n)+(fs+fn)*200*n
sh=lambda n,t:(cs+cn)*(CAL+A3*n)/t
def h(x): return x/3600
lo=lambda s,n:h(s*500*0.2e-6)+h(U(n)*12*0.03); hi=lambda s,n:h(s*500*30e-6)+h(U(n)*36*0.3)
net=lambda w,d:h(w*28*2*d*d*1e-9)
f=lambda x:'{:,}'.format(x); r0=lambda x:'{:,}'.format(int(round(x)))
sub=dict(CEILING=CEILING,TCONST=f(TC),TSLOPE=f(TS),T67=f(t67),S67=f(s67),N67=f(n67),T9=f(t9),SH67='%.1f%%'%(100*sh(67,t67)),SH9='%.1f%%'%(100*sh(9,t9)),
 U67=f(U(67)),LO67=r0(lo(s67,67)),HI67=r0(hi(s67,67)),NET67=r0(net(n67,256)),NET67_64=r0(net(n67,64)),NET67_512=r0(net(n67,512)),
 TLO67=r0(lo(s67,67)+net(n67,256)),THI67=r0(hi(s67,67)+net(n67,256)),TLO9=r0(lo(s9,9)+net(n9,256)),THI9=r0(hi(s9,9)+net(n9,256)),
 **{k:tab[F[k]][:8] for k in F})
assert (TC,TS,t67,t9)==(3471062400,42062400,6289243200,3849624000)
V25=open('/workspace/'+F['V25'],encoding='utf-8').read()
for x in ('3,471,062,400 + 42,062,400·n_seed*','6,289,243,200','3,849,624,000','3,011,119,200','3,278,124,000','1,375,600','80.5%','95.7%','≈ 221','≈ 16,673','≈ 3,563','≈ 20,015','≈ 2,232','≈ 12,088','Δt = τ / (100·max(1, g − 1))','2.7539 × 10⁻¹⁷'): assert x in V25,('v2.5 missing',x)
for k in ('LO67','HI67','TLO67','THI67','TLO9','THI9'): pass
assert sub['LO67']=='221' and sub['HI67']=='16,673' and sub['TLO67']=='3,563' and sub['THI67']=='20,015' and sub['TLO9']=='2,232' and sub['THI9']=='12,088',sub
body=BODY
for k,v in sub.items(): body=body.replace('{'+k+'}',v)
assert not re.search(r'\{[A-Z0-9_]+\}',body),'unfilled placeholder'
bad=sorted({c for c in body if ord(c)>127})
if bad: raise SystemExit('nonascii %r'%bad)
body=re.sub(r'\n{3,}','\n\n',body)
assert len(body)<=19500,('body too long',len(body))
for w in ('conscious','sentien','autopoie',r'\balive\b',r'\bC[45]\b'):
    for m in re.finditer(w,body,re.I):
        ctx=body[max(0,m.start()-60):m.end()+40].lower(); assert 'no consciousness' in ctx,(w,ctx)
for k in ('Consult #50 - TRACK B FREEZE PREPARATION v2.5 (design only): are E49-1..E49-3 closed, and rulings on the listed questions. NOT a freeze, execution or approval request. Challenge, don\'t endorse. High effort.',
          'Q0.','Q1.','Q2.','Q3.','Q4.','Q5.','Q6.','Q7.','E50-n','VERDICT','UNVERIFIED','X1-X5','host coupling','P4-P6','DGX Spark','fa85f5518477d78b','did NOT adopt','2.7539e-17','Aidan\'s explicit yes','no position'): assert k in body,k
bb=foot(body.encode()); open('c50_body.md','wb').write(bb)
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
for fn_ in os.listdir('send'): os.remove('send/'+fn_)
for i,p in enumerate(parts,1):
    if i<n: t='[c50 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[end of c50 part %d/%d - more coming, do not answer yet]'%(i,n)
    else: t='[c50 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[END OF CONSULT #50 PACKET - all %d parts sent. Please answer now.]'%n
    assert all(ord(c)<128 for c in t) and len(t.encode())<2600,(i,len(t))
    open('send/c50_%d.txt'%i,'w').write(t)
assert 'END OF CONSULT #50 PACKET' in open('send/c50_%d.txt'%n).read()
re_body=''.join(open('send/c50_%d.txt'%i).read().split('\n',1)[1].rsplit('\n',1)[0]+'\n' for i in range(1,n+1))
assert re.sub(r'\s+',' ',re_body).strip()==re.sub(r'\s+',' ',body).strip(),'reassembly mismatch'
man='# c50 send-part manifest (send parts carry no footer, per the #43-#49 packet precedent; this manifest covers them)\n'
man+=''.join('%s  send/c50_%d.txt  %d bytes\n'%(sha(open('send/c50_%d.txt'%i,'rb').read()),i,len(open('send/c50_%d.txt'%i,'rb').read())) for i in range(1,n+1))
open('send_manifest.txt','wb').write(foot(man.encode()))
for l in open('send_manifest.txt'):
    if l.startswith('#') or l.startswith('sha256 of'): continue
    hh,ff=l.split()[:2]; assert sha(open(ff,'rb').read())==hh,ff
assert ok_footer('send_manifest.txt')
assert sorted(os.listdir('send'))==sorted('c50_%d.txt'%i for i in range(1,n+1))
S=open('serve.py','rb').read(); assert ok_footer('serve.py') and b'astra_consult50_response.txt' in S and b'astra_serve50/send' in S and b'8840' in S and b'8841' in S and b'49' not in S
print('BUILD OK: %d parts, body %d chars, body sha256 %s, manifest sha256 %s, part sizes %s'%(n,len(body),sha(bb),sha(open('send_manifest.txt','rb').read()),[len(open('send/c50_%d.txt'%i,'rb').read()) for i in range(1,n+1)]))
