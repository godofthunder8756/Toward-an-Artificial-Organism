"""Document checks for the Astra #28 revisions. Read-only: git show / cat-file / rev-parse, sha256, text parsing."""
import re, subprocess, hashlib, sys
sys.path.insert(0,'/workspace/scratch/u1_audit/v1_1'); from common import *
exec(open('/workspace/scratch/u1_audit/v1_1/anch_v1.py').read())
REPO='/workspace/repo'; R='/workspace/review/'
AUD=R+'u1_substrate_audit_v1_1.md'; TRI=R+'track_a_lineage_triage_v1_3.md'; SYN=R+'track_a_claim_synthesis_v1_1.md'
C28='/workspace/astra_consult28_response.txt'; C25='/workspace/astra_consult25_response.txt'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
docs={p:open(p,encoding='utf-8').read() for p in (AUD,TRI,SYN)}
c28=open(C28,encoding='utf-8').read(); c25=open(C25,encoding='utf-8').read()
fails=[]; info=[]
def ok(c,m):
    if not c: fails.append(m)
ok(sha(C28)=='1df2fba3189a8217067dd4e13e0c3f5d4b22a25dc7aedabec85d7ee8bd8b96ed','consult28 sha')
# 1 verbatim Astra quotes
req_all=[E1,E2,T1Q,STOP]
named={'E1':E1,'E2':E2,'T1Q':T1Q,'STOP':STOP,'NORUN':NORUN,'U3HOLD':U3HOLD,'SKETCH1':SKETCH1,'SKETCH2':SKETCH2,'APPR':APPR,'NOAUTH':NOAUTH,'NORECERT':NORECERT}
for k,q in named.items(): ok(q.strip('"') in c28, f'{k} not verbatim in consult28')
for line in SUCC_REQ.splitlines(): ok(line[3:].strip('"') in c28, f'succ req not verbatim: {line[:40]}')
ok('E28-1' in c28 and E1.strip('"') in c28.split('E28-1',1)[1][:600],'E1 not under E28-1 heading')
ok(E2.strip('"') in c28.split('E28-2',1)[1][:600],'E2 not under E28-2 heading')
ok(NEW in c28,'closure sentence not in consult28')
for p,d in docs.items():
    for q in req_all: ok(q.strip('"') in d, f'{p}: missing required quote {q[:40]}')
for k in ('NORUN','NORECERT','SKETCH1','SKETCH2','APPR','NOAUTH','U3HOLD'):
    ok(named[k] in docs[AUD], f'audit missing {k}')
for k in ('NORUN','NORECERT','SKETCH1','SKETCH2','APPR','NOAUTH','U3HOLD'):
    ok(named[k] in docs[TRI], f'triage missing {k}')
EXTRA=['The primitive/policy distinction is right, but "the four steps are substrate, and only their order violates the rule" is too narrow.',
'Always selecting the next description slot is a targeting policy.','Making a successful comparison authorize this particular pointer/MODE transaction is organizational coordination unless represented in declared content.',
'Automatically erasing the previous active slot is a policy.','For `ac9.py:108`, "every bank with demand" is not necessarily a priority ordering. It is a supplied production-targeting rule. On the description provided, I would not clear it as generic chemistry yet.',
'A host operation identifying the program bank and every semantically designated memory bank, then distributing births to them, supplies organizational targeting.',
'A generic reaction acting on declared local substrates, receptors or demand markers can be substrate.',
'Show what "demand" reads, where it is represented, how targeting changes when that content changes, and how resource competition is resolved.',
'However, forced enablement of designated bank rules must be disclosed as an expressivity restriction. It cannot be classified as harmless syntax solely because other fields remain mutable. The question is whether it hard-wires an organization-specific action that declared content cannot suppress or redirect.',
'Fixed rule width, first-match interpretation and a fixed instruction vocabulary can be admissible syntax. A system need not have a universal programming language.',
'The revised closure sentence is directionally correct but still overstates the W/C/B clause while birth targeting remains contested. It also risks preserving the headline through "closure holds conditional on external coordination."',
'This would be a material architectural change. Whether the project calls it a new "family" depends on its architecture taxonomy; that terminology should not determine authorization.',
'Track A: ACCEPT THE MAIN AUDIT CONCLUSION, WITH NAMED CORRECTIONS. Under the adopted substrate rule, full production closure is not established. Further runs on the unchanged architecture will not resolve that structural limitation.',
'that terminology should not determine authorization']
nq=0
for q in EXTRA:
    ok(q in c28, f'extra quote not verbatim: {q[:50]}')
    ok(any(q in d for d in docs.values()), f'extra quote unused: {q[:50]}'); nq+=1
nq+=len(named)+7
# 2 closure sentence byte-identical; old sentence absent
OLD_FR=['Within the declared model and operating range, and with interpretation','holds only conditional on that external coordination','executes declared, inherited content and meets C1–C5']
counts={}
for p,d in docs.items():
    blocks=[l for l in d.splitlines() if l=='> '+NEW]
    counts[p]=(d.count(NEW),len(blocks))
    ok(len(blocks)>=1, f'{p}: no standalone closure blockquote')
    for f in OLD_FR: ok(f not in d, f'{p}: old sentence fragment present: {f}')
    # any other sentence starting "The audited system exhibits" must be exactly NEW-prefixed
    for m in re.finditer(r'The audited system exhibits[^\n]*', d):
        ok(m.group(0).startswith(NEW), f'{p}: variant closure sentence: {m.group(0)[:80]}')
# 3 citations
def git(*a): return subprocess.run(['git','-C',REPO,*a],capture_output=True,text=True)
ANCH.update({
 'ac9.py:L106-L111@6c6323b':"banks=[0]+[r+1 for r,n in enumerate(o.memory.demand()) if n>0]",
 'ac9.py:L42-L49@6c6323b':'def birth(b,bank,parent,e):',
 'ac9_memory.py:L26-L27@6c6323b':'return self.occupied().sum(axis=(1,2,3)).astype(int)',
 'ac95.py:L652@a1b9759':'target = (source + 1) % SLOTS',
 'ac95.py:L77@a1b9759':'SUCC_BUDGET = 6'})
for k in ['ac5_program.py:L1-L5@6c6323b','ac95.py:L645-L658@a1b9759','ac95.py:L168-L170@a1b9759','ac105.py:L171-L177@8f0218a']: pass
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
# code block in §4.1 matches source lines
src=git('show','6c6323b:ac9.py').stdout.split('\n')[105:111]
blk=docs[AUD].split('```python\n',1)[1].split('```',1)[0].strip('\n').split('\n')
ok([l.strip() for l in blk]==[l.strip() for l in src], 'code block != ac9.py L106-L111')
ok('self.occupied().sum(axis=(1,2,3)).astype(int)' in docs[AUD],'demand quote')
# backtick path @ commit pairs in all three
pat2=re.compile(r'`([A-Za-z0-9_./-]+\.(?:py|md|json|txt))` @ `([0-9a-f]{7})`')
npairs=0
for p,d in docs.items():
    for f,c in sorted(set(pat2.findall(d))):
        npairs+=1; ok(git('cat-file','-e',f'{c}:{f}').returncode==0, f'{p}: missing {f}@{c}')
# local paths cited
for p,d in docs.items():
    for lp in set(re.findall(r'`(/workspace/[^`\s]+)`',d)):
        import os; ok(os.path.exists(lp), f'{p}: local path missing {lp}')
# 4 forbidden phrases
term=re.compile(r'\bC4\b|\bC5\b|\bconscious\w*|\bautopoie\w*|\balive\b|\bsentien\w*',re.I)
neg=re.compile(r'\b(no|not|nothing|neither|nor|excludes?|without|cannot)\b',re.I)
for p,d in docs.items():
    for i,l in enumerate(d.splitlines(),1):
        for m in term.finditer(l):
            ctx=l
            st,en=m.start(),m.end()
            if (st>0 and l[st-1] in '_`/') or (en<len(l) and l[en] in '_.'): continue  # identifier / file name
            if re.search(r'charter C4|C4 admission',l) and m.group(0)=='C4': info.append(f'{p.split("/")[-1]}:{i} criterion reference: C4'); continue
            if 'AC92\'s "while alive" is an operational not-yet-dead label' in l: info.append(f'{p.split("/")[-1]}:{i} quoted repo label: alive'); continue
            # allowed: term inside a file name/identifier, a C1-C5 range, or in a negated/disclaimer line
            if re.search(r'C1[–-]C5',l) and m.group(0).upper()=='C5': continue
            if neg.search(ctx): info.append(f'{p.split("/")[-1]}:{i} negated: {m.group(0)}'); continue
            fails.append(f'{p}:{i} forbidden term outside disclaimer: {l[:120]}')
    for ph in [r'\bis autopoietic\b',r'\bis alive\b',r'\bare alive\b',r'(?<!")\bwhile (the organism is )?alive\b(?!")',r'conscious(ness)? (is|was) (shown|demonstrated|established)',r'\bC[45] (is|was) (met|established|demonstrated)']:
        ok(not re.search(ph,d,re.I), f'{p}: forbidden phrase {ph}')
# 5 prior versions unchanged
PRIOR={R+'u1_substrate_audit_v1.md':'48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a',
R+'track_a_lineage_triage_v1.md':'b4e1a772ee361128f1d88573673c6467d06d2029860bf8c79e9c33b668da7f0b',
R+'track_a_lineage_triage_v1_1.md':'d2cc9152d58a81c8054e1ddc8c59d4d83cc32f9ea6428b8e331ffe9a64a5d3ef',
R+'track_a_lineage_triage_v1_1_astra_digest.md':'d4034423b7dadddd40ed4a65ed76f3dd7f79e8bc4b3b288181cc3354e428bfa3',
R+'track_a_lineage_triage_v1_2.md':'84fa9614e022561b86cf2dddea0e3713d6f84585ee228d1016d95cea122fdb09',
R+'track_a_claim_synthesis_v1.md':'95888230db56906b7eb82b0936d04f6a897cbabd8062587c315f4a4aa3f26705',
R+'wrel_results_review_v1.md':'60c3f5a9a333e092ad625955696a0533e23ab667b3e332c3e0f6a7fa9cae8ace',
R+'wrel_attainability_from_existing_outputs_v1.md':'64ebd4a5d9b5954c30d2136b77fb1d13e42ce03c56ef519794d40b9cd76e82f4',
R+'c4_reliability_exact_check_spec_FINAL.md':'ae626b65cae383121e6a902fe79c119b90ff46ffb8fe7cc39fafe27fc502adef',
R+'c4_reliability_APPROVAL_RECORD.md':'be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687',
'/workspace/astra_consult25_response.txt':'31740a1e7129baf9ff9d3c047492fdbe1952970ad836d271742b5a6f14ff8791',
'/workspace/astra_consult26_response.txt':'e7b64e40fe430455be97435a349cc0f8428f9da86ba68af8577e767ab999ab12',
'/workspace/scratch/wrel_review/analytic_reference.py':'0e634895bf8c881519b8ff5360f67b94eb2251f46236a2d3da43222624e6bccf',
'/workspace/scratch/wrel_review/analytic_reference_out.json':'1f99c5ed2fb518d28c368178a18b9a71ee15dabcadcc87732142ad828f113f1f'}
for p,h in PRIOR.items(): ok(sha(p)==h, f'changed: {p}')
# 6 audit-specific structure
a=docs[AUD]
ok('| I12 | **Birth targeting**' in a and 'EXTERNAL COORDINATION (supplied targeting)' in a.split('| I12 | **Birth targeting**')[1].split('\n')[0],'I12 row not reclassified')
ok('contested at' not in a,'v1 contested label remains')
sec=a.split('### 4.1 Birth targeting',1)[1].split('## 5.',1)[0]
wc=len(sec.split()); ok(300<=wc<=520, f'4.1 word count {wc}')
ok('SKETCH ONLY' in a and 'SKETCH ONLY' in docs[TRI] and 'SKETCH ONLY' in docs[SYN],'SKETCH ONLY label missing')
r=git('status','--porcelain','--untracked-files=no')
print('quotes checked:',nq,'| closure sentence occurrences (total, standalone blockquotes):',{k.split('/')[-1]:v for k,v in counts.items()})
print('audit line citations:',len(cites),'| code blobs master==db0ef2f:',len(blobs),'| backtick path@commit pairs:',npairs,'| §4.1 words:',wc)
print('synthesis words:',len(docs[SYN].split()))
print('repo tracked changes (non-__pycache__):',len([l for l in r.stdout.splitlines() if '__pycache__' not in l]))
for x in info: print('  note',x)
print('RESULT:','PASS' if not fails else 'FAIL'); [print(' -',f) for f in fails]
sys.exit(1 if fails else 0)
