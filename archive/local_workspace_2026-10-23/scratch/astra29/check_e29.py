"""Document checks for the Astra #29 revisions. Read-only: git show / cat-file / log, sha256, text and JSON parsing."""
import re, subprocess, hashlib, sys, json, os
sys.path.insert(0,'/workspace/scratch/u1_audit/v1_1'); sys.path.insert(0,'/workspace/scratch/astra29')
import common as c28m; import common29 as c29m
from common29 import *
NEW=c28m.NEW
exec(open('/workspace/scratch/u1_audit/v1_1/anch_v1.py').read())
REPO='/workspace/repo'; R='/workspace/review/'
AUD=R+'u1_substrate_audit_v1_2.md'; TRI=R+'track_a_lineage_triage_v1_4.md'; SYN=R+'track_a_claim_synthesis_v1_2.md'
C29='/workspace/astra_consult29_response.txt'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
docs={p:open(p,encoding='utf-8').read() for p in (AUD,TRI,SYN)}
c29=open(C29,encoding='utf-8').read(); c28=open('/workspace/astra_consult28_response.txt',encoding='utf-8').read()
c26=open('/workspace/astra_consult26_response.txt',encoding='utf-8').read(); c25=open('/workspace/astra_consult25_response.txt',encoding='utf-8').read()
fails=[]; info=[]
def ok(c,m):
    if not c: fails.append(m)
def git(*a): return subprocess.run(['git','-C',REPO,*a],capture_output=True,text=True)
ok(sha(C29)=='38056d5597fa3f8b077b7ed5b89c4cd64ea58ec1d6632b7d3d10c8936b352ce8','consult29 sha')
# 1 verbatim Astra #29 quotes
Q29={'E296':E296,'E291':E291,'LEDGER':LEDGER,'VERD':VERD,'STALE':STALE,'PROV':PROV,'SEPQ':SEPQ,'ORALT':ORALT,'NOEXT':NOEXT}
for k,q in Q29.items(): ok(q.strip('"') in c29, f'{k} not verbatim in consult29')
ok(E296.strip('"') in c29.split('E29-6.',1)[1][:500],'E29-6 not under its heading')
ok(E291.strip('"') in c29.split('E29-1.',1)[1][:500],'E29-1 not under its heading')
for p,d in docs.items(): ok(E296 in d, f'{p}: E29-6 missing')
for k in ('PROV',): ok(Q29[k] in docs[AUD] and Q29[k] in docs[TRI], f'{k} missing in audit/triage')
for k in ('LEDGER','E291','STALE','ORALT','NOEXT'): ok(Q29[k] in docs[TRI], f'triage missing {k}')
ok(SEPQ in docs[AUD] and SEPQ in docs[TRI],'SEPQ missing')
ok(VERD in docs[AUD],'verdict missing in audit')
# inline quotes in new text: short ones
INL=['Do not describe #28 alone as an unconditional code certification.','the declared donor interventions and first-order probe battery','The coverage qualifier alone is insufficient.','Not immediately.']
for q in INL: ok(q in c29 or q in c26, f'inline quote not verbatim: {q}')
# all earlier-consult constants still verbatim
for k in ('E1','E2','T1Q','STOP'): ok(getattr(c28m,k).strip('"') in c28, f'{k} c28')
# 2 closure sentence byte-identical, E28 edits retained
for p,d in docs.items():
    ok(any(l=='> '+NEW for l in d.splitlines()), f'{p}: closure blockquote missing')
    for m in re.finditer(r'The audited system exhibits[^\n]*', d): ok(m.group(0).startswith(NEW), f'{p}: variant closure')
    ok(c28m.E1 in d and c28m.E2 in d and c28m.T1Q in d, f'{p}: E28 edits not retained')
# 3 citations
ANCH.update({
 'ac9.py:L106-L111@6c6323b':"banks=[0]+[r+1 for r,n in enumerate(o.memory.demand()) if n>0]",
 'ac9.py:L42-L49@6c6323b':'def birth(b,bank,parent,e):',
 'ac9_memory.py:L26-L27@6c6323b':'return self.occupied().sum(axis=(1,2,3)).astype(int)',
 'ac95.py:L652@a1b9759':'target = (source + 1) % SLOTS',
 'ac95.py:L77@a1b9759':'SUCC_BUDGET = 6',
 'ac12.py:L64@5b06281':'STEP_SRC=inspect.getsource(ac9.step)',
 'ac95.py:L817-L840@a1b9759':'src = ac12.STEP_SRC',
 'ac4.py:L97-L98@6c6323b':'groups=range(4) if action==6 else [4]',
 'ac4.py:L89-L92@6c6323b':"int(a[4*bank:4*bank+4].sum())*8",
 'ac12.py:L67-L69@5b06281':'a[4*(r+1):4*(r+2)]',
 'ac12.py:L80@5b06281':'bits=decode(o.body.traces[0,:126]).reshape(9,14)',
 'ac105.py:L169@8f0218a':'o.body.traces[1, :ac95.DESC_BITS] = encoded[:, None]',
 'ac105.py:L161@8f0218a':'o, offs = ac12.acquire(seed)',
 'ac12.py:L94-L107@5b06281':'o=v2.acquire(seed)',
 'ac9_priority_v2.py:L11-L15@6c6323b':'o=ac9.acquire(seed)',
 'ac9.py:L23-L26@6c6323b':'return Organism(b,mem.Memory.empty())',
 'ac9.py:L9@6c6323b':'import ac9_memory as mem'})
pat=re.compile(r'([A-Za-z0-9_]+\.(?:py|md)):L(\d+)(?:-L(\d+))?@([0-9a-f]{7})')
cites=sorted(set(m.group(0) for m in pat.finditer(docs[AUD])))
blobs=set()
for c in cites:
    m=pat.fullmatch(c); f,a,b,commit=m.group(1),int(m.group(2)),int(m.group(3) or m.group(2)),m.group(4)
    r=git('show',f'{commit}:{f}')
    if r.returncode: fails.append(f'missing {c}'); continue
    L=r.stdout.split('\n'); ok(1<=a<=b<=len(L), f'range {c}')
    ok(c in ANCH, f'no anchor {c}')
    if c in ANCH: ok(ANCH[c] in '\n'.join(L[a-1:b]), f'anchor not in lines {c}')
    ok(git('log','-1','--format=%h','master','--',f).stdout.strip()==commit, f'not last-touch {c}')
    if f.endswith('.py'): blobs.add(f)
for f in sorted(blobs): ok(git('rev-parse',f'master:{f}').stdout==git('rev-parse',f'db0ef2f:{f}').stdout, f'{f} master!=db0ef2f')
ok(not (set(ANCH)-set(cites)), f'anchors uncited: {sorted(set(ANCH)-set(cites))}')
pat2=re.compile(r'`([A-Za-z0-9_./-]+\.(?:py|md|json|jsonl|txt))` @ `([0-9a-f]{7})`')
npairs=0
for p,d in docs.items():
    for f,c in sorted(set(pat2.findall(d))):
        npairs+=1; ok(git('cat-file','-e',f'{c}:{f}').returncode==0, f'{p}: missing {f}@{c}')
for p,d in docs.items():
    for lp in set(re.findall(r'`(/workspace/[^`\s]+)`',d)): ok(os.path.exists(lp), f'{p}: local path missing {lp}')
# 3b W-REL record supports the written statements (read-only git show + JSON parse)
D='c4_reliability_exact_check_v1/'
ok(git('merge-base','--is-ancestor','dddd63c','origin/pr/11').returncode==0,'dddd63c not on PR #11 ref')
for c in ('0e17a05','7b89c66','fb3e9b4','8a4b393','dddd63c'): ok(git('merge-base','--is-ancestor',c,'origin/pr/11').returncode==0, f'{c} not on PR #11')
v3=git('show','0e17a05:'+D+'RESULTS_v3.md').stdout.split('\n')
ok('is lifted' in v3[26] and 'ITEM-9 now agrees' in v3[26],'RESULTS_v3 L27 does not record the lifted status')
ok('Mismatches: 0' in v3[16] and 'COMPLETE' in v3[16],'RESULTS_v3 L17')
ok([l.split('|')[3].strip() for l in v3[32:36]]==['UNRESOLVED-DESIGN','UNRESOLVED-DESIGN','REFERENCE CRITERIA NOT MET','REFERENCE CRITERIA NOT MET'],'RESULTS_v3 label table')
e27=git('show','7b89c66:'+D+'WREL_CLOSEOUT_E27_v1.md').stdout.split('\n')
ok(e27[8].startswith('**(a) holds.**') and e27[10].startswith('**(b) is not established.**'),'E27 (a)/(b) lines')
a2=git('show','dddd63c:'+D+'RESULTS_A2.md').stdout.split('\n')
ok('empty control list' in a2[8] and 'were not evaluated' in a2[8],'RESULTS_A2 L9')
for ln in (33,95): ok('`ATTAINED`' in a2[ln],'RESULTS_A2 ATTAINED line %d'%(ln+1))
for ln in (29,91): ok('UNRESOLVED-DESIGN' in a2[ln],'RESULTS_A2 label line %d'%(ln+1))
summ=json.loads(git('show','dddd63c:'+D+'outputs/attainability_A2/SUMMARY.json').stdout)
st={x['T_SEP']:x for x in summ['settings']}
ok(set(st)=={3,4},'A2 settings')
for T,n in ((3,432),(4,1552)):
    x=st[T]; ok(x['reference_conjunction']=='ATTAINED' and x['reference_met'] and x['agreed'] and x['status']=='COMPLETE','A2 T%d'%T)
    ok(all(v=='PASS' for v in x['flags'].values()) and x['n_action_disagree']==0 and x['n_action_agree']==n, 'A2 flags T%d'%T)
    ok(x['formal_label']=='UNRESOLVED-DESIGN','A2 formal T%d'%T)
for f,c in (('c4_reliability_APPROVAL_ADDENDUM_A2.md','fb3e9b4'),('c4_reliability_exact_check_spec_ADDENDUM_A2.md','8a4b393')):
    ok(git('cat-file','-e',f'{c}:{D}{f}').returncode==0, f'missing {f}')
# 3c AC95 stored-row counts quoted in §4.2
tot=dict(W=0,b0=0,r0=0,r1=0); n=0
for l in git('show','a1b9759:ac95_results_v1/rows.jsonl').stdout.splitlines():
    d=json.loads(l); n+=1; tot['W']+=d['W_births']; tot['b0']+=d['W_births_bank0']; tot['r0']+=d['region0_births']; tot['r1']+=d['region1_births']
ok((n,tot['W'],tot['b0'],tot['r0'],tot['r1'])==(136,174978,87394,87584,0), f'AC95 counts {n} {tot}')
ok('136 rows) record 174978 W births: 87394 in bank 0, 87584 in bank 1 (region 0) and 0 in bank 2 (region 1)' in docs[AUD],'AC95 counts text')
r105=json.loads(git('show','8f0218a:ac105_results_v1/rows.jsonl').stdout.splitlines()[0])
ok('region0_births' not in r105 and 'W_births_bank0' not in r105,'AC105 rows do store per-bank births')
# 4 text scans outside quotes / changelogs
QSTR=[v for v in list(Q29.values())+[c28m.E1,c28m.E2,c28m.T1Q,c28m.STOP,c28m.NORUN,c28m.U3HOLD,c28m.SKETCH1,c28m.SKETCH2,c28m.APPR,c28m.NOAUTH,c28m.NORECERT,TESTQ]]
def body(p,d):
    if p==TRI:
        out=[];skip=False
        for l in d.split('\n'):
            if l.startswith('## '): skip=l.startswith('## Changelog')
            if not skip: out.append(l)
        d='\n'.join(out)
    if p==AUD: d=d[:d.index('## 10. Changes in v1.1')]
    for q in QSTR: d=d.replace(q,' ').replace(q.strip('"'),' ')
    d='\n'.join(l for l in d.split('\n') if not l.lstrip().startswith('>'))
    d=re.sub(r'"[^"\n]*"',' ',d); d=re.sub(r'`[^`\n]*`',' ',d)
    return d
for p,d in docs.items():
    b=body(p,d)
    ok(not re.search(r'resolved by',b,re.I), f'{p}: "resolved by" outside quotes: '+str(re.findall(r'.{40}resolved by.{20}',b,re.I)[:3]))
    for pat_ in (r'UNRESOLVED-COMPUTE',r'\b(2|two)-setting',r'attainability check',r'reference-only check'):
        hits=re.findall(r'[^\n]*'+pat_+r'[^\n]*',b,re.I); ok(not hits, f'{p}: {pat_} outside changelog/quotes: {[h[:100] for h in hits]}')
    for l in b.split('\n'):
        if 'NEEDS-APPROVED-RUN' in l and re.search(r'W-REL|A-SEP|attainab|T_SEP|c_S',l): fails.append(f'{p}: W-REL NEEDS-APPROVED-RUN: {l[:100]}')
    # 8/10 contributions
    for i,l in enumerate(b.split('\n'),1):
        if '8/10' in l and not re.search(r'\bbar\b|default|Default',l):
            ok('PR #9' in l and 'D_FO' in l and 'D_ISO' in l, f'{p}:{i} 8/10 without PR #9 FO+ISO conjunction: {l[:110]}')
    ok('separate systems' in d and 'GRU-8' in d and 'one organism' in d, f'{p}: systems separation statement missing')
ok('PROVISIONAL' in docs[AUD].split('| I12 | **Birth targeting**')[1].split('\n')[0],'I12 row not PROVISIONAL')
ok('### 4.2 Status of the I12 judgment (v1.2): PROVISIONAL' in docs[AUD] and '**What the code does not show.**' in docs[AUD],'§4.2 missing')
ok('PROVISIONAL' in docs[SYN] and docs[TRI].count('PROVISIONAL')>=4,'PROVISIONAL not propagated')
# 5 forbidden phrases (same allowlist as check_v1_1)
term=re.compile(r'\bC4\b|\bC5\b|\bconscious\w*|\bautopoie\w*|\balive\b|\bsentien\w*',re.I)
neg=re.compile(r'\b(no|not|nothing|neither|nor|excludes?|without|cannot)\b',re.I)
for p,d in docs.items():
    for i,l in enumerate(d.splitlines(),1):
        for m in term.finditer(l):
            st_,en=m.start(),m.end()
            if (st_>0 and l[st_-1] in '_`/') or (en<len(l) and l[en] in '_.'): continue
            if re.search(r'C1[–-]C5',l) and m.group(0).upper()=='C5': continue
            if re.search(r'charter C4|C4 admission',l) and m.group(0)=='C4': continue
            if 'AC92\'s "while alive" is an operational not-yet-dead label' in l: continue
            if neg.search(l): continue
            fails.append(f'{p}:{i} forbidden term outside disclaimer: {l[:120]}')
    for ph in [r'\bis autopoietic\b',r'\bis alive\b',r'\bare alive\b',r'(?<!")\bwhile (the organism is )?alive\b(?!")',r'conscious(ness)? (is|was) (shown|demonstrated|established)',r'\bC[45] (is|was) (met|established|demonstrated)']:
        ok(not re.search(ph,d,re.I), f'{p}: forbidden phrase {ph}')
# 6 earlier versions unchanged
PRIOR={R+'u1_substrate_audit_v1.md':'48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a',
R+'u1_substrate_audit_v1_1.md':'3d9bbde3644e15d81f2489c15cd6b68c07c93590097c95ef959b79758cd96373',
R+'track_a_lineage_triage_v1.md':'b4e1a772ee361128f1d88573673c6467d06d2029860bf8c79e9c33b668da7f0b',
R+'track_a_lineage_triage_v1_1.md':'d2cc9152d58a81c8054e1ddc8c59d4d83cc32f9ea6428b8e331ffe9a64a5d3ef',
R+'track_a_lineage_triage_v1_1_astra_digest.md':'d4034423b7dadddd40ed4a65ed76f3dd7f79e8bc4b3b288181cc3354e428bfa3',
R+'track_a_lineage_triage_v1_2.md':'84fa9614e022561b86cf2dddea0e3713d6f84585ee228d1016d95cea122fdb09',
R+'track_a_lineage_triage_v1_3.md':'167c7e67791bb24e2ec7667c4c669fd96fd5b9bf48f9e307fd7f5cb07e579b66',
R+'track_a_claim_synthesis_v1.md':'95888230db56906b7eb82b0936d04f6a897cbabd8062587c315f4a4aa3f26705',
R+'track_a_claim_synthesis_v1_1.md':'41da2819ae6e623041239e6aa6119eafb5099c017baf660effe44de7c428424c',
R+'wrel_results_review_v1.md':'60c3f5a9a333e092ad625955696a0533e23ab667b3e332c3e0f6a7fa9cae8ace',
R+'wrel_attainability_from_existing_outputs_v1.md':'64ebd4a5d9b5954c30d2136b77fb1d13e42ce03c56ef519794d40b9cd76e82f4',
R+'c4_reliability_exact_check_spec_FINAL.md':'ae626b65cae383121e6a902fe79c119b90ff46ffb8fe7cc39fafe27fc502adef',
R+'c4_reliability_APPROVAL_RECORD.md':'be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687',
'/workspace/astra_consult25_response.txt':'31740a1e7129baf9ff9d3c047492fdbe1952970ad836d271742b5a6f14ff8791',
'/workspace/astra_consult26_response.txt':'e7b64e40fe430455be97435a349cc0f8428f9da86ba68af8577e767ab999ab12',
'/workspace/astra_consult28_response.txt':'1df2fba3189a8217067dd4e13e0c3f5d4b22a25dc7aedabec85d7ee8bd8b96ed',
'/workspace/scratch/wrel_review/analytic_reference.py':'0e634895bf8c881519b8ff5360f67b94eb2251f46236a2d3da43222624e6bccf',
'/workspace/scratch/wrel_review/analytic_reference_out.json':'1f99c5ed2fb518d28c368178a18b9a71ee15dabcadcc87732142ad828f113f1f'}
for p,h in PRIOR.items(): ok(sha(p)==h, f'changed: {p}')
r=git('status','--porcelain','--untracked-files=no')
print('Astra #29 quotes checked:',len(Q29)+len(INL),'| audit line citations:',len(cites),'| code blobs master==db0ef2f:',len(blobs),'| path@commit pairs:',npairs)
print('W-REL record checks: RESULTS_v3@0e17a05, E27@7b89c66, RESULTS_A2 + SUMMARY.json@dddd63c, approval@fb3e9b4, spec@8a4b393 all on origin/pr/11')
print('word counts:',{k.split('/')[-1]:len(v.split()) for k,v in docs.items()})
print('repo tracked changes (non-__pycache__):',len([l for l in r.stdout.splitlines() if '__pycache__' not in l]))
print('RESULT:','PASS' if not fails else 'FAIL'); [print(' -',f) for f in fails]
sys.exit(1 if fails else 0)
