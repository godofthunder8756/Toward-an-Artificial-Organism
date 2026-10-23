"""Document checks for triage v1.2, claim synthesis v1 and the W-REL attainability note. Read-only (git cat-file only)."""
import hashlib, re, subprocess, json
from fractions import Fraction as F
R='/workspace/review/'; REPO='/workspace/repo'
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
fails=[]; info=[]
def ok(c,m):
    if not c: fails.append(m)
V12=open(R+'track_a_lineage_triage_v1_2.md',encoding='utf-8').read()
SYN=open(R+'track_a_claim_synthesis_v1.md',encoding='utf-8').read()
ATT=open(R+'wrel_attainability_from_existing_outputs_v1.md',encoding='utf-8').read()
C25=open('/workspace/astra_consult25_response.txt',encoding='utf-8').read()
C26=open('/workspace/astra_consult26_response.txt',encoding='utf-8').read()
AUD=open(R+'u1_substrate_audit_v1.md',encoding='utf-8').read()
# 1 fixed hashes
H={'track_a_lineage_triage_v1.md':'b4e1a772ee361128f1d88573673c6467d06d2029860bf8c79e9c33b668da7f0b',
 'track_a_lineage_triage_v1_1.md':'d2cc9152d58a81c8054e1ddc8c59d4d83cc32f9ea6428b8e331ffe9a64a5d3ef',
 'track_a_lineage_triage_v1_1_astra_digest.md':'d4034423b7dadddd40ed4a65ed76f3dd7f79e8bc4b3b288181cc3354e428bfa3',
 'u1_substrate_audit_v1.md':'48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a',
 'wrel_results_review_v1.md':'60c3f5a9a333e092ad625955696a0533e23ab667b3e332c3e0f6a7fa9cae8ace',
 'c4_reliability_exact_check_spec_FINAL.md':'ae626b65cae383121e6a902fe79c119b90ff46ffb8fe7cc39fafe27fc502adef',
 'c4_reliability_APPROVAL_RECORD.md':'be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687'}
for f,h in H.items(): ok(sha(R+f)==h,f'hash changed: {f}')
ok(sha('/workspace/astra_consult25_response.txt')=='31740a1e7129baf9ff9d3c047492fdbe1952970ad836d271742b5a6f14ff8791','consult25 sha')
ok(sha('/workspace/astra_consult26_response.txt')=='e7b64e40fe430455be97435a349cc0f8428f9da86ba68af8577e767ab999ab12','consult26 sha')
ADV={'/workspace/scratch/wrel_review/analytic_reference.py':'0e634895bf8c881519b8ff5360f67b94eb2251f46236a2d3da43222624e6bccf',
     '/workspace/scratch/wrel_review/analytic_reference_out.json':'1f99c5ed2fb518d28c368178a18b9a71ee15dabcadcc87732142ad828f113f1f'}
for p,h in ADV.items(): ok(sha(p)==h,f'ADVISORY artifact altered: {p}'); ok(h in ATT,f'advisory hash not in attainability doc {p}')
# 2 verbatim quotes
Q25=["F1 is foundational only to a conditional closure claim. A strongly connected dependency graph does not by itself demonstrate production closure: the edges must distinguish production, enabling conditions, resource dependence and supplied sequencing.",
"F2 supports within-model ablation dependence. The digest does not justify treating common-resource explanations as generally excluded.",
"F3 does not exclude an externally specified coordinator with a consequential resource gate. Refusal at W=0 establishes that the gate matters. It does not establish that the sequence of operations is internally constituted.",
'F4 should say "endpoint agreement under the audited observer-discard procedure." That is narrower than trajectory-level state sufficiency or absence of every host-side influence.',
'I would rename REDUNDANT to "REDUCED OR NO LONGER PRIORITY," with separate fields for retained evidence and future effort. A mechanism can instantiate a real role while being conventional.',
"PATTERN REPRODUCED BY NAMED CONTROL does not automatically create a REDUNDANT entry.",
"Triage priority, retained functional evidence and mechanism novelty are separate fields. Reproduction by a conventional mechanism does not automatically erase a functional role or classify a result as redundant.",
"Rival reproduction may end development of a claimed novelty without negating retained causal or functional evidence. The claim being retired is named explicitly.",
"No additional lineage experiment is proposed unless its possible outcomes change a named scientific claim or program decision. Completing an experiment queue is not itself a research objective.",
"Track A's substrate rule is fixed before further runs. Organization-specific maintenance sequencing must be represented in declared system state; a supplied resource gate alone does not internalize the sequence it enables.",
"A supplied substrate operation may implement generic state transformation, transport, execution or numerical integration. Organization-specific instructions, maintenance sequences, switching conditions and repair policies must be represented in declared system state rather than hidden in the supplied operation. The substrate must execute alternative admissible instruction contents, including unsuccessful ones, without substituting the intended organization.",
"Resolve now by specification and code audit. Stop after classifying each disputed operation and revising the claim. Do not automatically build a successor.",
"Retain as a question, not a standing experimental queue. Require one explicit acquired organizational change and one discriminating prediction before proposing a run.",
"Highest-value possible Track A experiment after U1","Propose that experiment only if the answer is yes",
"First establish that the machinery intervention isolates the proposed pathway without simply disabling computation or changing available resources.",
"For U3, use pathway interruption plus machinery-specific restoration, with resource and immediate-function controls. A single blocking arm is not a complete mediation argument.",
"Persistence of an effect under the U3 machinery clamp defeats the proposed mediation account; it does not prove reduction to ordinary estimation.",
"Failure of one adaptive implementation does not retire adaptation of organization as a construct.",
"Defer. Another failed R-FIX search is unlikely to affect program strategy. Reopen only for a decision that a compensation witness would change.",
'Defer unless "minimal" remains in a publication claim. Remove that adjective otherwise. Graph connectivity and leave-one-out ablations do not establish minimality over compensating alternatives.',
"Separate ALife successor project requiring an explicit PI decision. Not a prerequisite for Track B.",
"Keep as a documented operating-range limitation. Do an affordability analysis only if the intended claim requires the missing range.",
"Drop from the active queue.","Keep the sampled-control qualifier. No new draw-count study without a downstream decision requiring it.",
"Finish the already approved bounded analysis and review it separately.","Drop from the active queue; preserve the suspended result.",
"Do not automatically build a successor."]
Q26=["Under the stated overall gate, the formal A-SEP outcome remains UNRESOLVED-COMPUTE until the missing coverage is completed. This is an incomplete-computation outcome, not a cap-exceeded outcome.",
"conditional on completion of required validation","UNRESOLVED-DESIGN; no donor contrast; C-REF and C-T2 also fail","UNRESOLVED-DESIGN; same reasons",
"REFERENCE CRITERIA NOT MET; C-REF and C-SEL fail","REFERENCE CRITERIA NOT MET; C-REF fails","Retain the frozen precedence.",
"follows the chosen protocol precedence, not a general rule of logic","The coverage qualifier alone is insufficient.",
"Identity swaps do not supply the missing intervention comparison.","remain provisional comparison results, subject to the validation shortfall",
"Not immediately.","The checking ceiling remains FAIL.","These comparisons do not establish absence of an assessment role",
"that finite reference/grid/horizon combination as a successful separation design","The chosen A-SEP settings were not checked prospectively for joint criterion attainability."]
Q26A=["First inspect the already produced ITEM-2/3 outputs across the six costs and authorized horizons. Extract existing recheck counts, first-recheck distributions and relevant policy information. Reading existing results does not require recomputing a planner.",
"At approximately 10:59 AM ET, the reviewer executed a seven-second independent reference-planner calculation outside the frozen analysis specification. It preceded the subsequent scope-tightening message. Its artifacts are preserved as ADVISORY and do not satisfy mandatory replay coverage or support confirmatory labels. The scope deviation has been reported to Aidan.",
"that finite reference/grid/horizon combination as a successful separation design","do not add costs or horizons after seeing failures".capitalize()[0:0]+"Do not add costs or horizons after seeing failures",
"The attainability scan should be a separate decision after extracting what the existing outputs already establish.","a new operational criterion, not a correction to these results","justified independently of making the reference pass"]
for q in Q25: ok(q in C25,f'C25 source missing: {q[:60]}'); ok(q in V12,f'v1.2 missing C25 quote: {q[:60]}')
for q in Q26: ok(q in C26,f'C26 source missing: {q[:60]}'); ok(q in V12,f'v1.2 missing C26 quote: {q[:60]}')
for q in Q26A: ok(q in C26 or q.lower() in C26.lower(),f'C26 source missing (att): {q[:60]}'); ok(q in ATT or q.lower() in ATT.lower(),f'attainability missing quote: {q[:60]}')
# 3 audit sentence byte-identical
m=re.search(r'\*\*Revised sentence \(under the consult #25 rule\):\*\*\n\n> (.+)\n',AUD); SENT=m.group(1)
ok(('> '+SENT) in V12,'v1.2 F1 sentence differs from audit'); ok(('> '+SENT) in SYN,'synthesis sentence differs from audit')
ok('48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a' in V12,'audit sha not cited in v1.2')
# 4 path @ commit citations
pairs=sorted(set(re.findall(r'`([^`\s]+)` @ `([0-9a-f]{7})`',V12)))
for p,c in pairs:
    r=subprocess.run(['git','-C',REPO,'cat-file','-e',f'{c}:{p}'],capture_output=True)
    ok(r.returncode==0,f'citation missing {p}@{c}')
for p,c in set(re.findall(r'`([^`\s]+)` @ `([0-9a-f]{7})`',SYN)):
    ok(subprocess.run(['git','-C',REPO,'cat-file','-e',f'{c}:{p}'],capture_output=True).returncode==0,f'syn citation {p}@{c}')
r=subprocess.run(['git','-C',REPO,'show','4b85851:DEPENDENCY_AUDIT_v2_CORRECTION.md'],capture_output=True,text=True); ok('A fixed sequence machine' in r.stdout,'dep audit quote')
# 5 counts
cnt={'F':len(re.findall(r'^### F\d\. ',V12,re.M)),'S':len(set(re.findall(r'^\| (S\d+) \|',V12,re.M))),
     'R':len(set(re.findall(r'^\| (R\d+) \|',V12,re.M))),'U':len(re.findall(r'^### U\d+[ .]',V12,re.M))}
ok(cnt=={'F':5,'S':15,'R':11,'U':11},f'counts {cnt}')
for rid in range(1,12): ok(len(re.findall(rf'^\| R{rid} \|',V12,re.M))==2,f'R{rid} lacks NC1/NC7 row')
tbl=re.search(r'\| FOUNDATIONAL \| (\d+) \|.*?\| SUPPORTING \| (\d+) \|.*?\| REDUCED OR NO LONGER PRIORITY \| (\d+) \|.*?\| UNRESOLVED \| (\d+) \|',V12,re.S)
ok(tbl and tuple(map(int,tbl.groups()))==(5,15,11,11),'§1 table counts')
secs=re.split(r'^(?=### U\d+[ .])',V12.split('## 5. UNRESOLVED')[1].split('## 6. Verification')[0],flags=re.M)[1:]
alloc={}
for sec in secs:
    uid=re.match(r'### (U\d+)',sec).group(1)
    a=('ADDRESSED' if 'ADDRESSED by the U1 audit' in sec.split('\n')[0] else 'DROPPED' if 'DROPPED FROM THE ACTIVE QUEUE' in sec.split('\n')[0]
       else 'EXECUTED' if 'EXECUTED AND REVIEWED' in sec.split('\n')[0] else 'RETAINED' if 'RETAINED AS A QUESTION' in sec
       else 'HELD' if 'HELD, NOT PROPOSED' in sec else 'DEFERRED' if 'DEFERRED.**' in sec else None)
    alloc[uid]=a
    if a!='DROPPED': ok('Named claim or decision its outcomes would change (NC8)' in sec,f'{uid} lacks NC8 field')
    else: ok('Dropped with reason' in sec,f'{uid} lacks dropped reason')
exp={'U1':'ADDRESSED','U2':'RETAINED','U3':'HELD','U4':'DEFERRED','U5':'DEFERRED','U6':'DEFERRED','U7':'DEFERRED','U8':'DROPPED','U9':'DEFERRED','U10':'EXECUTED','U11':'DROPPED'}
ok(alloc==exp,f'allocations {alloc}')
from collections import Counter
ac=Counter(alloc.values()); ok(ac==Counter({'DEFERRED':5,'DROPPED':2,'ADDRESSED':1,'RETAINED':1,'HELD':1,'EXECUTED':1}),f'alloc counts {ac}')
# 6 rename: REDUNDANT only in changelogs or verified quotes
body=V12[:V12.index('## Changelog v1.2')]+V12[V12.index('---\n\n## 0. Scope'):]
for q in Q25: body=body.replace(q,'')
ok('REDUNDANT' not in body,'REDUNDANT outside quotes/changelog')
ok(not re.search(r'would add a REDUNDANT entry',V12),'old U10 wording present')
# 7 forbidden phrases (all three docs)
FORB=[r'\bis autopoietic\b',r'\bare autopoietic\b',r'\bis alive\b',r'\bare alive\b',r'\bsentien',r'\bconscious(ness)? (is|was) (shown|demonstrated|established|supported)',
      r'\bC4 (is|was) (met|established|demonstrated|supported)',r'\bC5 (is|was) (met|established|demonstrated|supported)',r'supports? (a )?C4 claim',r'establishes? (an )?assessment role']
for name,t in (('v1.2',V12),('synthesis',SYN),('attainability',ATT)):
    for p in FORB: ok(not re.search(p,t,re.I),f'{name}: forbidden {p}')
# 8 synthesis
wc=len(re.findall(r'\S+',SYN)); info.append(f'synthesis words {wc}'); ok(wc<=610,f'synthesis too long {wc}')
for k in ['Q-EXIST','Q-CAUSE','Q-LEARN','Q-NECESSITY','For the closure sentence: no','For a separate Q-CAUSE claim','What it cannot claim']: ok(k in SYN,f'synthesis lacks {k}')
# 9 attainability numbers against emitted outputs
O='/workspace/scratch/pr11/head/c4_reliability_exact_check_v1/outputs/'
for f,h in (('ITEM-2.json','4ac58ac8ab74b837ce97def6d1869be0f07b525a868680d30d32a9823b78e999'),('ITEM-3.json','9f65f641917d835162d1e9b592c7a98f1b1bea8f23a5633664e66eac1a19395d'),('deviation_1/ITEM-8.json','5c1e8200cc8063a8bcf01b2e11f362cb2bc43dd55df543f7f323d0229680c103')):
    ok(sha(O+f)==h,f'input hash {f}'); ok(h in ATT,f'input hash not cited {f}')
i2=json.load(open(O+'ITEM-2.json'))
def row(T,cr,cs): return next(r for r in i2['rows'] if r['T']==T and r['cr']==cr and r['cs']==cs)
def dR(r): return (F(r['n_R']['S'])-F(r['n_R_unanimous']['S']))-(F(r['n_R']['E'])-F(r['n_R_unanimous']['E']))
ok(str(dR(row(3,'1/100','3/50')))=='759297337109988831/2048000000000000000' and '759297337109988831/2048000000000000000' in ATT,'dR(3,1/100,3/50)')
for (T,cr,cs,txt) in [(3,'1/100','3/50','0.3708'),(4,'1/100','3/50','0.6508'),(3,'1/100','1/10','0.0239'),(4,'1/100','1/10','0.0903'),(3,'1/50','1/10','0.1376'),(4,'1/50','1/10','0.3161'),(3,'1/25','1/10','0.3750'),(4,'1/25','1/10','0.6544')]:
    ok(f'{float(dR(row(T,cr,cs))):.4f}'==txt,f'dR {T},{cr},{cs}')
for cr in ('1/100','1/50','1/25'):
    for T in range(1,11): ok(F(row(T,cr,'1/10')['n_M']['S'])==0==F(row(T,cr,'1/10')['n_M']['E']),'nM nonzero at cs=1/10')
for cr in ('1/50','1/25'):
    for T in (3,4): ok(F(row(T,cr,'3/50')['never_R']['S'])==1,'recheck at no-recheck setting')
q=F(23,100); ps=1-q**3-(1-q)**3; ok(ps==F(5313,10000) and F(432817,500000)-3*q*(1-q)**2/ps==F(47817,500000),'world constants')
print('\n'.join(info)); print('citations checked:',len(pairs)); print('RESULT:','PASS' if not fails else 'FAIL'); [print(' -',x) for x in fails]
