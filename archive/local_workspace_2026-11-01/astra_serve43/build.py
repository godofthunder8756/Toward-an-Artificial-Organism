# Builds the #43 ASCII send parts. Does NOT start any server and sends nothing.
import re,hashlib,os,subprocess
os.chdir('/workspace/astra_serve43')
r=subprocess.run(['sha256sum','-c','/workspace/astra_serve43/governing_sha256.txt'],cwd='/workspace',capture_output=True,text=True)
print(r.stdout.strip())
if r.returncode!=0: raise SystemExit('SHA MISMATCH - not building')
EXP={'astra_consult42_response.txt':'e438e329','astra_consult41_response.txt':'3f3b1b87','astra_serve42/c42_body.md':'7968c191',
 'review/trackB_instrument_validation_scope_v3_2_merged_RD.md':'98e11d2c','review/trackB_instrument_validation_scope_v3_1_merged_RD.md':'9817c33b',
 'review/trackB_scope_v3_2_addendum_RD.md':'d724e453','review/trackB_scope_v3_CNA_plants_confounds_observer_v1_erratum1.md':'da613127',
 'review/trackB_scope_v3_1_merged_seams_lightpass_CNA_v1.md':'9c55aae1','handoff/LEAD_addendum1_rulings_2026-10-23.md':'e90d4929',
 'review/trackB_instrument_validation_scope_v3_RD.md':'0892ccac','review/trackB_scope_v3_CNA_plants_confounds_observer_v1.md':'5dec96f5',
 'review/trackB_scope_v3_RD_lightpass_CNA_v1.md':'c47d8d47','review/trackB_scope_v3_CNA_env_integrity_defaults_v1.md':'d5523c71'}
tab={l.split()[1]:l.split()[0] for l in open('governing_sha256.txt') if l.strip()}
for f,p in EXP.items():
    if not tab.get(f,'').startswith(p): raise SystemExit('PREFIX MISMATCH %s'%f)
assert set(tab)==set(EXP)
v32=open('/workspace/review/trackB_instrument_validation_scope_v3_2_merged_RD.md','rb').read()
L=v32.splitlines(True); assert hashlib.sha256(b''.join(L[:-1])).hexdigest()==L[-1].decode().split(': ')[1].strip(), 'v3.2 footer mismatch'
print('prefix check OK (%d files); v3.2 footer OK'%len(EXP))
exec(open('pieces.py').read())
r42=open('/workspace/astra_consult42_response.txt').read().splitlines(); r41=open('/workspace/astra_consult41_response.txt').read().splitlines()
assert '"'+CEILING+'"' in r41[303], 'ceiling not verbatim at #41 L304'
for n,q in Q42: assert q in r42[n-1],('#42',n,q)
for n,q in Q41: assert q in r41[n-1],('#41',n,q)
HF=HEAD_FULL.replace('{V32}',tab['review/trackB_instrument_validation_scope_v3_2_merged_RD.md'][:8]+' (internal footer '+L[-1].decode().split(': ')[1].strip()[:8]+' reproduced)')
M={'μ':'mu','×':'x','ε':'eps','κ':'kappa','‖':'||','·':'*','Φ':'Phi','−':'-','→':'->','§':'S','∈':'in','≈':'~','…':'...','≥':'>=','≤':'<=','–':'-','—':'-','√':'sqrt','≠':'!=','“':'"','”':'"','’':"'",'‘':"'",'²':'^2','é':'e','ç':'c','ρ':'rho','β':'beta','σ':'sigma','γ':'gamma','Δ':'Delta','χ':'chi','r̄':'rbar'}
def asc(t):
    for k,v in M.items(): t=t.replace(k,v)
    t=t.replace('**','').replace('`','')
    bad=sorted({c for c in t if ord(c)>127})
    if bad: raise SystemExit('nonascii %r'%bad)
    return t
body=re.sub(r'\n{3,}','\n\n',asc(HF))
for w in ('conscious','sentien','autopoietic','alive'):
    # allowed only inside the explicit no-claims disclaimers
    for m in re.finditer(w,body,re.I):
        ctx=body[max(0,m.start()-120):m.end()+40].lower()
        assert ('no consciousness' in ctx or 'no awareness' in ctx), (w,ctx)
open('c43_body.md','w').write(body)
cov='# Track B Astra consult #43 cover note v1 (RD) - DRAFT, NOT FROZEN, DESIGN REVIEW ONLY, NOTHING RUNS\n\nPacket: /workspace/astra_serve43/c43_body.md (this note is its cover section, verbatim). Primary: merged scope v3.2 '+tab['review/trackB_instrument_validation_scope_v3_2_merged_RD.md'][:8]+'.\n\n'+asc(COVER.replace('{V32}',tab['review/trackB_instrument_validation_scope_v3_2_merged_RD.md'][:8])).strip()+'\n'
cp='/workspace/review/trackB_astra43_cover_note_v1_RD.md'
if os.path.exists(cp):
    if open(cp).read()!=cov: raise SystemExit('cover note exists and differs - not overwriting')
else: open(cp,'w').write(cov)
lines=body.split('\n');parts=[];cur=''
LIM=2780
for l in lines:
    while len(l)>LIM:
        cut=l.rfind(' ',0,LIM)
        if cur: parts.append(cur);cur=''
        parts.append(l[:cut]);l=l[cut+1:]
    while len(cur)+len(l)+1>LIM and cur:
        room=LIM-len(cur)-1
        cut=l.rfind('. ',0,room) if len(l)>600 else -1
        if cut>200:
            cur+=l[:cut+1]+'\n'; l=l[cut+2:]
        parts.append(cur);cur=''
    cur+=l+'\n'
if cur.strip(): parts.append(cur)
n=len(parts)
for f in os.listdir('send'): os.remove('send/'+f)
for i,p in enumerate(parts,1):
    if i<n: t='[c43 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[end of c43 part %d/%d - more coming, do not answer yet]'%(i,n)
    else: t='[c43 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[END OF CONSULT #43 PACKET - all %d parts sent. Please answer now.]'%n
    assert all(ord(c)<128 for c in t) and len(t)<=2900, (i,len(t))
    open('send/c43_%d.txt'%i,'w').write(t)
re_body=''.join(open('send/c43_%d.txt'%i).read().split('\n',1)[1].rsplit('\n',1)[0]+'\n' for i in range(1,n+1))
assert re.sub(r'\s+',' ',re_body).strip()==re.sub(r'\s+',' ',body).strip(), 'reassembly mismatch'
print(n,len(body),hashlib.sha256(open('c43_body.md','rb').read()).hexdigest(),[len(open('send/c43_%d.txt'%i).read()) for i in range(1,n+1)])
print('cover',hashlib.sha256(open(cp,'rb').read()).hexdigest(),len(cov))
