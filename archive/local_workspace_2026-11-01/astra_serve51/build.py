# Builds the #51 ASCII send parts. Does NOT start any server and sends nothing.
import re, hashlib, os, subprocess, sys
os.chdir('/workspace/astra_serve51')
sys.path.insert(0,'/workspace/scratch/lead_v26')
def sha(b): return hashlib.sha256(b).hexdigest()
def foot(b): return b + ('sha256 of all content above this line: ' + sha(b) + '\n').encode()
def ok_footer(p):
    L=open(p,'rb').read().splitlines(True); return sha(b''.join(L[:-1]))==L[-1].decode().split(': ')[1].strip()
def ok_proj_footer(p):
    b=open(p,'rb').read(); i=b.rfind(b'sha256 of all content above this line:')
    return i>0 and sha(b[:i])==b[i:].split(b':',1)[1].strip()[:64].decode()
R='review/'
F=dict(V26=R+'trackB_freezeprep_v2_6_consolidated_Lead.md',WL=R+'trackB_freezeprep_v2_6_E50_5_workload_ledger_Lead.md',
 CE50=R+'trackB_scope_v3_6_CNA_E50_1_E50_3_v1.md',CE50A1=R+'trackB_scope_v3_6_CNA_E50_1_E50_3_v1_addendum1.md',CE50E1=R+'trackB_scope_v3_6_CNA_E50_1_E50_3_v1_erratum1.md',
 PP=R+'trackB_scope_v3_6_CNA_E50_pending_params_v1.md',RD26=R+'trackB_freezeprep_v2_6_E50_2_E50_4_RD.md',RD26C1=R+'trackB_freezeprep_v2_6_E50_2_E50_4_RD_corr1.md',
 RD26C2=R+'trackB_freezeprep_v2_6_E50_2_E50_4_RD_corr2.md',RDLP=R+'trackB_scope_v3_6_CNA_E50_1_E50_3_lightpass_RD_v1.md',RDPP=R+'trackB_scope_v3_6_CNA_E50_params_and_erratum1_lightpass_RD_v1.md',
 A50='astra_consult50_response.txt',V25=R+'trackB_freezeprep_v2_5_consolidated_Lead.md',ER1=R+'trackB_freezeprep_v2_5_erratum1_Lead.md',E2=R+'trackB_freezeprep_v2_5_erratum2_Lead.md',
 E2C1=R+'trackB_freezeprep_v2_5_erratum2_corr1_Lead.md',E2C2=R+'trackB_freezeprep_v2_5_erratum2_corr2_Lead.md',E2C3=R+'trackB_freezeprep_v2_5_erratum2_corr3_Lead.md',
 M=R+'trackB_instrument_validation_scope_v3_6_merged_RD.md',MP=R+'trackB_measurement_plan_v1_RD.md',CNA2=R+'trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md',
 AMD=R+'constitution_amendment_A-2026-10-24_record.md',R41='astra_consult41_response.txt',R42='astra_consult42_response.txt')
PRE=dict(V26='ff03eb81',WL='83247be9',CE50='b5a880ea',CE50A1='fdba7c63',CE50E1='42bf6c6d',PP='a1dc190a',RD26='8a369208',RD26C1='ebe3a08c',RD26C2='e8bba1b2',
 RDLP='2b403bcb',RDPP='12371a76',A50='59e93cff',V25='d101438d',ER1='10860e98',E2='81bdfcf2',E2C1='c2c83921',E2C2='5100f4de',E2C3='2f813ba4',M='ab80afa5',MP='1d5458e3',
 CNA2='17832b01',AMD='2f29a07a',R41='3f3b1b87',R42='e438e329')
if not os.path.exists('governing_sha256.txt'):
    r=subprocess.run(['sha256sum']+list(F.values()),cwd='/workspace',capture_output=True,text=True,check=True)
    open('governing_sha256.txt','wb').write(foot(r.stdout.encode()))
r=subprocess.run(['sha256sum','-c','/workspace/astra_serve51/governing_sha256.txt'],cwd='/workspace',capture_output=True,text=True)
if 'FAILED' in r.stdout or not all(f+': OK' in r.stdout for f in F.values()): raise SystemExit('SHA MISMATCH - not building')
assert ok_footer('governing_sha256.txt')
tab={l.split()[1]:l.split()[0] for l in open('governing_sha256.txt') if l.strip() and not l.startswith('sha256 of')}
for k,f in F.items(): assert tab[f].startswith(PRE[k]),('PREFIX',k)
for k in F:
    if k not in ('A50','MP','CNA2','AMD','R41','R42'): assert ok_proj_footer('/workspace/'+F[k]),'footer '+k
print('governing hashes OK (%d files); footers OK'%len(F))
exec(open('pieces.py').read())
def rl(p): return [l.replace('\ufffd','') for l in open('/workspace/'+p,encoding='utf-8',errors='replace').read().splitlines()]
assert '"'+CEILING+'"' in rl(F['R41'])[303]
assert 'no additional stop-associated reward, penalty or terminal return' in rl(F['R42'])[222]
for n,q in Q50: assert q in rl(F['A50'])[n-1],('A50',n)
for n,q in QM: assert q in rl(F['M'])[n-1],('M',n)
for n,q in QMP: assert q in rl(F['MP'])[n-1],('MP',n)
# v2.6 consolidated content checks
V=open('/workspace/'+F['V26'],encoding='utf-8').read()
for x in ('AM-1','AM-2','AM-3','AM-4','AM-5','AM-6','AM-7','AM-8','AM-9','AM-10','AM-11','**ROW0-FL**','**ΔLL-HO**','**NC2 ceiling redefinition**','**Scalar-plant t_s = 0**','**RAND-INIT dose-0 drop**',
          '**NC2r demoted to descriptive**','**LIM in calibration**','**S_cons and S_wc thresholds**','**100-iteration float64 bisection**','**n_q ≥ 199 construction requirement**','**r_q = 991**',
          '7,068,312,000','4,416,552,000','72,009,000','5.6601e-06','Early stopping: NOT ADOPTED','Cross-validation is NOT run at all','PROVISIONAL','3.6673 × 10⁻⁴','5.28–9.05×','n_c = 101','n_q = 1,000','n_dc = 9',
          'Network Var(w) floor','K_dc','Network width d_h'): assert x in V,('v26',x)
for k in ('CE50','CE50A1','CE50E1','PP','RD26','RD26C1','RD26C2','RDLP','RDPP','WL','A50','V25','ER1','E2','E2C1','E2C2','E2C3'): assert tab[F[k]] in V,('v26 cites',k)
# ledger numbers
from ledger3 import R as LR
from ledger import trials,L15
r={k:v[0] for k,v in LR.items()}; c={k:v[1] for k,v in LR.items()}; T=lambda k:'{:,.0f}'.format(sum(r[k].values()))
s67,n67=trials(L15,67); s9,n9=trials(L15,9); f=lambda x:'{:,}'.format(int(x))
assert (s67+n67,s9+n9)==(7068312000,4416552000)
for k in ('low','high','max','low9','high9','v25pt'): assert '≈ '+T(k) in V,('cpu',k)
sub=dict(CEILING=CEILING,T67=f(s67+n67),T9=f(s9+n9),NC=f(c['low']['null_c']),NQ=f(c['low']['null_q']),HY=f(c['low']['hys_te']),FL=f(c['low']['fits']),FH=f(c['high']['fits']),
 DP=f(c['low']['dips']),CL=T('low'),CH=T('high'),CV=T('v25pt'),CL9=T('low9'),CH9=T('high9'),CM=T('max'),**{k:tab[F[k]][:8] for k in F})
body=BODY
for k,v in sub.items(): body=body.replace('{'+k+'}',v)
assert not re.search(r'\{[A-Z0-9_]+\}',body),'unfilled placeholder'
bad=sorted({ch for ch in body if ord(ch)>127})
if bad: raise SystemExit('nonascii %r'%bad)
body=re.sub(r'\n{3,}','\n\n',body)
assert len(body)<=22000,('body too long',len(body))
for w in ('conscious','sentien','autopoie',r'\balive\b'):
    for m in re.finditer(w,body,re.I):
        ctx=body[max(0,m.start()-60):m.end()+40].lower(); assert 'no consciousness' in ctx,(w,ctx)
for k in ('NOT a freeze, execution, timing or approval request','no freeze, execution or timing run is requested','Q0.','Q1.','Q2.','Q3.','Q4.','Q5.','Q6.','E51-n','VERDICT','UNVERIFIED','X1-X5','host coupling',
          'AM-1 ROW0-FL','AM-2 Delta-LL-HO','AM-3 NC2 ceiling','AM-4 Scalar-plant t_s = 0','AM-5 RAND-INIT dose-0 drop','AM-6 NC2r demoted','AM-7 LIM in calibration','AM-8 S_cons and S_wc thresholds',
          'AM-9 100-iteration float64 bisection','AM-10 n_q >= 199','AM-11 r_q = 991','AM-1, AM-8)','AM-10, AM-11)','AM-9)','5.6601e-06','1.8130e-05','one rank above your 990th',
          'ACCEPT or REJECT','Early stopping is NOT adopted','NOT RUN BY DESIGN','PROVISIONAL','cross-validation is NOT run','72,009,000','IGN-LIM is IN calibration','S_wc','S_cons','A50 L56-L58',
          'Aidan\'s explicit yes','v2.6 consolidated '+tab[F['V26']][:8]): assert k in body,k
bb=foot(body.encode()); open('c51_body.md','wb').write(bb)
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
    if i<n: t='[c51 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[end of c51 part %d/%d - more coming, do not answer yet]'%(i,n)
    else: t='[c51 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[END OF CONSULT #51 PACKET - all %d parts sent. Please answer now.]'%n
    assert all(ord(ch)<128 for ch in t) and len(t.encode())<2600,(i,len(t))
    open('send/c51_%d.txt'%i,'w').write(t)
assert 'END OF CONSULT #51 PACKET' in open('send/c51_%d.txt'%n).read()
assert all('END OF CONSULT' not in open('send/c51_%d.txt'%i).read() for i in range(1,n))
re_body=''.join(open('send/c51_%d.txt'%i).read().split('\n',1)[1].rsplit('\n',1)[0]+'\n' for i in range(1,n+1))
assert re.sub(r'\s+',' ',re_body).strip()==re.sub(r'\s+',' ',body).strip(),'reassembly mismatch'
man='# c51 send-part manifest (send parts carry no footer, per the #43-#50 packet precedent; this manifest covers them)\n'
man+=''.join('%s  send/c51_%d.txt  %d bytes\n'%(sha(open('send/c51_%d.txt'%i,'rb').read()),i,len(open('send/c51_%d.txt'%i,'rb').read())) for i in range(1,n+1))
open('send_manifest.txt','wb').write(foot(man.encode()))
for l in open('send_manifest.txt'):
    if l.startswith('#') or l.startswith('sha256 of'): continue
    hh,ff=l.split()[:2]; assert sha(open(ff,'rb').read())==hh,ff
assert ok_footer('send_manifest.txt')
assert sorted(os.listdir('send'))==sorted('c51_%d.txt'%i for i in range(1,n+1))
S=open('serve.py','rb').read(); assert ok_footer('serve.py') and b'astra_consult51_response.txt' in S and b'astra_serve51/send' in S and b'8840' in S and b'8841' in S and b'consult50' not in S and b'c50_' not in S
print('BUILD OK: %d parts, body %d chars, body sha256 %s, manifest sha256 %s, part sizes %s'%(n,len(body),sha(bb),sha(open('send_manifest.txt','rb').read()),[len(open('send/c51_%d.txt'%i,'rb').read()) for i in range(1,n+1)]))
