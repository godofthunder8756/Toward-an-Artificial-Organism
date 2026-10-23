import re,hashlib,os,subprocess,sys
os.chdir('/workspace/astra_serve42')
# 1. re-verify governing sha256 table; abort on mismatch
r=subprocess.run(['sha256sum','-c','/workspace/astra_serve42/governing_sha256.txt'],cwd='/workspace',capture_output=True,text=True)
print(r.stdout.strip())
if r.returncode!=0: raise SystemExit('SHA MISMATCH - not building')
# 2. check against the prefixes named in /workspace/pending/astra_consult42_brief.md (and #41 record)
EXP={'astra_consult41_response.txt':'3f3b1b87','astra_serve41/c41_body.md':'c514ad52',
 'review/trackB_instrument_validation_scope_v2_1_merged_RD.md':'8ea6abc5','review/trackB_instrument_validation_scope_v2_RD.md':'166370c1',
 'review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md':'17832b01','review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum1.md':'c2cd0732',
 'review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum2.md':'5ddde854','review/trackB_scope_v2_RD_lightpass_CNA_v1.md':'9f7a6ebc',
 'review/trackB_scope_v2_merged_lightpass_CNA_v1.md':'2d52f7d3','review/trackB_instrument_validation_scope_v2_merged_RD.md':'5824d5e5',
 'review/trackB_prior_art_verification_v1_3_fullreads_CNA.md':'badf7258','review/trackB_prior_art_verification_v1_4_P3_scholarly_CNA.md':'d7f1a43b',
 'review/trackB_prior_art_verification_v1_5_P3_altroutes_CNA.md':'3fde80d8','review/trackB_prior_art_verification_v1_6_palika_route_CNA.md':'9704f21d',
 'review/trackB_astra41_cover_note_v1_1_RD.md':'b7d1e4ab'}
tab={l.split()[1]:l.split()[0] for l in open('governing_sha256.txt') if l.strip()}
for f,p in EXP.items():
    if not tab.get(f,'').startswith(p): raise SystemExit('PREFIX MISMATCH %s'%f)
assert set(tab)==set(EXP)
# v2.1 internal footer
v21=open('/workspace/review/trackB_instrument_validation_scope_v2_1_merged_RD.md','rb').read()
if hashlib.sha256(b''.join(v21.splitlines(True)[:-1])).hexdigest()[:8]!='15a0b715': raise SystemExit('v2.1 footer mismatch')
print('prefix check OK (%d files); v2.1 footer 15a0b715 OK'%len(EXP))
# 3. ceiling sentence must be verbatim in raw #41
exec(open('pieces.py').read())
raw=open('/workspace/astra_consult41_response.txt').read()
assert '"'+CEILING+'"' in raw.splitlines()[303], 'ceiling not verbatim at L304'
M={'μ':'mu','×':'x','ε':'eps','κ':'kappa','‖':'||','·':'*','Φ':'Phi','−':'-','→':'->','§':'S','∈':'in','≈':'~','…':'...','≥':'>=','≤':'<=','–':'-','—':'-','√':'sqrt','≠':'!=','“':'"','”':'"','’':"'",'‘':"'",'²':'^2','é':'e','ç':'c'}
def asc(t):
    for k,v in M.items(): t=t.replace(k,v)
    t=t.replace('**','').replace('`','')
    bad=sorted({c for c in t if ord(c)>127})
    if bad: raise SystemExit('nonascii %r'%bad)
    return t
body=asc(HEAD_FULL)
body=re.sub(r'\n{3,}','\n\n',body)
open('c42_body.md','w').write(body)
# cover note (new file; never overwrite an existing different file)
cov='# Track B Astra consult #42 cover note v1 (RD) - DRAFT, NOT FROZEN, NOTHING RUNS\n\nPacket: /workspace/astra_serve42/c42_body.md (this note is its cover section, verbatim). Primary: scope v2.1 8ea6abc5.\n\n'+asc(COVER).strip()+'\n'
cp='/workspace/review/trackB_astra42_cover_note_v1_RD.md'
if os.path.exists(cp):
    if open(cp).read()!=cov: raise SystemExit('cover note exists and differs - not overwriting')
else: open(cp,'w').write(cov)
lines=body.split('\n');parts=[];cur=''
LIM=2780  # leaves room for headers so each part file <= 2900 chars
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
    if i<n: t='[c42 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[end of c42 part %d/%d - more coming, do not answer yet]'%(i,n)
    else: t='[c42 part %d/%d]\n'%(i,n)+p.rstrip('\n')+'\n[END OF CONSULT #42 PACKET - all %d parts sent. Please answer now.]'%n
    assert all(ord(c)<128 for c in t) and len(t)<=2900, (i,len(t))
    open('send/c42_%d.txt'%i,'w').write(t)
# reassembly check: concatenated part bodies == body (modulo split newlines)
re_body=''.join(open('send/c42_%d.txt'%i).read().split('\n',1)[1].rsplit('\n',1)[0]+'\n' for i in range(1,n+1))
assert re.sub(r'\s+',' ',re_body).strip()==re.sub(r'\s+',' ',body).strip(), 'reassembly mismatch'
print(n,len(body),hashlib.sha256(open('c42_body.md','rb').read()).hexdigest(),[len(open('send/c42_%d.txt'%i).read()) for i in range(1,n+1)])
print('cover',hashlib.sha256(open(cp,'rb').read()).hexdigest(),len(cov))
