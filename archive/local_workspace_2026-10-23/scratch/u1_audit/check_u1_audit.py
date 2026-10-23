"""Consistency check for /workspace/review/u1_substrate_audit_v1.md. Read-only: git show / rev-parse only."""
import re, subprocess, hashlib, sys
DOC='/workspace/review/u1_substrate_audit_v1.md'; REPO='/workspace/repo'
CONSULT='/workspace/astra_consult25_response.txt'
doc=open(DOC,encoding='utf-8').read(); con=open(CONSULT,encoding='utf-8').read()
fails=[]
def ok(c,msg):
    if not c: fails.append(msg)
# 1 verbatim quotes
RULE='"A supplied substrate operation may implement generic state transformation, transport, execution or numerical integration. Organization-specific instructions, maintenance sequences, switching conditions and repair policies must be represented in declared system state rather than hidden in the supplied operation. The substrate must execute alternative admissible instruction contents, including unsuccessful ones, without substituting the intended organization."'
APPL='Under that rule, a hard-coded copy->verify->switch->remove routine is supplied organizational coordination unless that sequence is represented in maintained state. A generic interpreter can qualify as substrate; calling a function an interpreter is insufficient.'
NC2='"Track A\'s substrate rule is fixed before further runs. Organization-specific maintenance sequencing must be represented in declared system state; a supplied resource gate alone does not internalize the sequence it enables."'
for name,q in (('rule',RULE),('application',APPL),('named change 2',NC2)):
    ok(q in con, f'{name}: not in consult file'); ok(('> '+q) in doc, f'{name}: not quoted verbatim in audit')
ok(con.splitlines()[26]=='> '+RULE, 'rule not at consult line 27')
ok(hashlib.sha256(open(CONSULT,'rb').read()).hexdigest()=='31740a1e7129baf9ff9d3c047492fdbe1952970ad836d271742b5a6f14ff8791','consult sha changed')
# 2 citations
ANCH={
 'ac5_program.py:L33-L41@6c6323b':'def choose(traces,observation):',
 'ac5_program.py:L1-L5@6c6323b':'Interpreter and format are supplied laws.',
 'ac5_program.py:L22-L30@6c6323b':'rules=[(1,1,0),(1,2,1),(1,64,6),(1,128,7),(1,256,8)]',
 'ac9.py:L84@6c6323b':'action=prog.choose(b.traces,observe(o))',
 'ac9.py:L85-L112@6c6323b':'elif action==6:',
 'ac9.py:L108@6c6323b':'banks=[0]+[r+1 for r,n in enumerate(o.memory.demand()) if n>0]',
 'ac9.py:L52@6c6323b':'def observe(o):',
 'ac9.py:L113@6c6323b':'ac4.balance(before,b,e)',
 'ac1.py:L67-L68@6c6323b':'def decode(traces):',
 'ac95.py:L261-L263@a1b9759':'def read_slot(o, g):',
 'ac95.py:L243-L253@a1b9759':'def build_program(desc):',
 'ac95.py:L607-L725@a1b9759':'def advance(o, e, succ, now, succ_trigger',
 'ac95.py:L659-L664@a1b9759':'write_toward_slot(o, e, target, src_maj, SUCC_BUDGET)',
 'ac95.py:L341-L352@a1b9759':'def write_toward_slot',
 'ac95.py:L665-L676@a1b9759':'valid = build_program(tgt_maj) is not None',
 'ac95.py:L677-L692@a1b9759':'commit_switch(o, e, target, last)',
 'ac95.py:L476-L532@a1b9759':'def commit_switch',
 'ac95.py:L510@a1b9759':'c = encode_ctrl(1, PHASE_REMOVE, last)',
 'ac95.py:L717-L725@a1b9759':'elif phase == PHASE_REMOVE:',
 'ac95.py:L89@a1b9759':'PHASE_IDLE, PHASE_COPY, PHASE_VERIFY, PHASE_SWITCH, PHASE_REMOVE = range(5)',
 'ac95.py:L642@a1b9759':'encode_ctrl(1, PHASE_COPY, now)',
 'ac95.py:L663@a1b9759':'encode_ctrl(1, PHASE_VERIFY, last)',
 'ac95.py:L673-L676@a1b9759':'if valid and correct:',
 'ac95.py:L680-L681@a1b9759':'if not (bool(np.array_equal(tgt_maj, src_maj))',
 'ac95.py:L720-L721@a1b9759':'encode_ctrl(0, PHASE_IDLE, last)',
 'ac95.py:L85-L88@a1b9759':'CTRL_BASE = PTR_BASE + 2',
 'ac95.py:L291-L296@a1b9759':'def ctrl_fields(o):',
 'ac95.py:L735@a1b9759':'succ_trigger = dm >= DESC_TRIGGER',
 'ac95.py:L76-L80@a1b9759':'DESC_TRIGGER = 2',
 'ac95.py:L635@a1b9759':'rate_ok = timer_value(o) >= TIMER_MAX',
 'ac95.py:L638-L650@a1b9759':'if succ_trigger and rate_ok:',
 'ac95.py:L611-L623@a1b9759':'if rip(o):',
 'ac95.py:L428-L473@a1b9759':'def reset_timer(o, e):',
 'ac95.py:L101-L103@a1b9759':'TIMER_K = 200',
 'ac95.py:L309-L327@a1b9759':'def write_rip(o, e, val):',
 'ac95.py:L729-L748@a1b9759':'def maintain(o, e, succ, reg_offs, cfg, now):',
 'ac95.py:L836-L837@a1b9759':'maintain(o,e,succ,reg_offs,cfg,now)',
 'ac95.py:L536-L577@a1b9759':'def reg_description_active(o, e):',
 'ac95.py:L580-L594@a1b9759':'def reg_from_active(o, e, reg_offs):',
 'ac95.py:L734@a1b9759':'reg_trigger = obs2 or',
 'ac95.py:L336-L338@a1b9759':'def _cap(b, budget=None):',
 'ac95.py:L369-L408@a1b9759':'def write_ctrl(o, e, c, gate=True):',
 'ac95.py:L645-L658@a1b9759':'succ._entry = dict(n=succ._n',
 'ac95.py:L71@a1b9759':'FIXED_WORDS = ((1, 1, 0)',
 'ac95.py:L168-L170@a1b9759':"'gated':   dict(ac_arm='regen'",
 'ac105.py:L171-L177@8f0218a':"cfg = dict(ac95.ARM_PARTS['gated'])",
 'ac105.py:L177-L178@8f0218a':"step.__globals__['maintain'] = maintain_fn",
 'ac105.py:L166-L167@8f0218a':'build_offs = reg_offs + streak_offs',
 'ac104.py:L144-L157@343ba17':'program_incomplete(o, reg_offs)',
 'ac104.py:L118-L123@343ba17':'def budget_rule(material, allowance):',
 'ac104.py:L87@343ba17':'DECISION_ALLOWANCE = STREAK_N * 7',
 'ac103.py:L98-L112@3c89857':'def program_incomplete(o, reg_offs):',
 'ac99.py:L267-L270@8e9ab4a':'ac95.maintain(o, e, succ, reg_offs, cfg, now)',
 'ac99_d2.py:L128-L159@8e9ab4a':'if cur + 1 >= STREAK_N:',
 'ac99_d2.py:L76-L116@8e9ab4a':'def gray_streak_read(o, key, streak_offs):',
 'ac12.py:L52@5b06281':'STREAK_N=6',
 'CLOSURE_VERDICT_v1.md:L59-L70@4b85851':'J1 (substrate/component boundary)',
 'CLOSURE_VERDICT_v1.md:L96-L99@4b85851':'The substrate is supplied, and the verdict says so.',
 'CLOSURE_VERDICT_v1.md:L35@4b85851':'succession copy→verify→switch→remove (turnover)',
 'CLOSURE_VERDICT_v1.md:L32@4b85851':'action 6 birth',
 'CLOSURE_VERDICT_v1.md:L38-L46@4b85851':'decision state (register + Gray streak)',
}
pat=re.compile(r'([A-Za-z0-9_]+\.(?:py|md)):L(\d+)(?:-L(\d+))?@([0-9a-f]{7})')
cites=sorted(set(m.group(0) for m in pat.finditer(doc)))
def git(*a): return subprocess.run(['git','-C',REPO,*a],capture_output=True,text=True)
blobs=set()
for c in cites:
    m=pat.fullmatch(c); f,a,b,commit=m.group(1),int(m.group(2)),int(m.group(3) or m.group(2)),m.group(4)
    r=git('show',f'{commit}:{f}')
    if r.returncode: fails.append(f'missing {c}'); continue
    lines=r.stdout.split('\n')
    ok(1<=a<=b<=len(lines), f'range out of bounds {c}')
    ok(c in ANCH, f'no anchor declared for {c}')
    if c in ANCH: ok(ANCH[c] in '\n'.join(lines[a-1:b]), f'anchor not in lines {c}')
    lt=git('log','-1','--format=%h','master','--',f).stdout.strip()
    ok(lt==commit, f'not last-touch on master {c} (last={lt})')
    if f.endswith('.py'): blobs.add(f)
for f in sorted(blobs):
    ok(git('rev-parse',f'master:{f}').stdout==git('rev-parse',f'db0ef2f:{f}').stdout, f'{f} differs master vs db0ef2f')
unused=set(ANCH)-set(cites)
ok(not unused, f'anchors without citation: {sorted(unused)}')
# 3 forbidden claim phrases
for p in [r'\bis autopoietic\b',r'\bis alive\b',r'\bare alive\b',r'\bconscious(ness)? (is|was) (shown|demonstrated|established)',r'\bC4 (is|was) (met|established|demonstrated)',r'\bC5 (is|was) (met|established|demonstrated)',r'\bsentien']:
    ok(not re.search(p,doc,re.I), f'forbidden phrase {p}')
# 4 earlier files unchanged
OLD={'/workspace/review/track_a_lineage_triage_v1.md':'b4e1a772ee361128f1d88573673c6467d06d2029860bf8c79e9c33b668da7f0b',
 '/workspace/review/track_a_lineage_triage_v1_1.md':'d2cc9152d58a81c8054e1ddc8c59d4d83cc32f9ea6428b8e331ffe9a64a5d3ef',
 '/workspace/review/track_a_lineage_triage_v1_1_astra_digest.md':'d4034423b7dadddd40ed4a65ed76f3dd7f79e8bc4b3b288181cc3354e428bfa3',
 '/workspace/review/wrel_results_review_v1.md':'60c3f5a9a333e092ad625955696a0533e23ab667b3e332c3e0f6a7fa9cae8ace',
 '/workspace/review/c4_reliability_exact_check_spec_FINAL.md':'ae626b65cae383121e6a902fe79c119b90ff46ffb8fe7cc39fafe27fc502adef'}
for p,h in OLD.items(): ok(hashlib.sha256(open(p,'rb').read()).hexdigest()==h, f'changed: {p}')
# 5 F1 original quote present in v1.1
v11=open('/workspace/review/track_a_lineage_triage_v1_1.md',encoding='utf-8').read()
ok('Every necessary component {W, C, B, description, derived program} meets C1–C5.' in v11,'F1 quote not in v1.1')
ok('git status' not in doc,'')
r=git('status','--porcelain','--untracked-files=no'); 
print(f'citations checked: {len(cites)}; anchors: {len(ANCH)}; code blobs master==db0ef2f: {len(blobs)}')
print('repo tracked changes (expected only pre-existing __pycache__ deletions):', len([l for l in r.stdout.splitlines() if '__pycache__' not in l]))
print('RESULT:', 'PASS' if not fails else 'FAIL'); [print(' -',f) for f in fails]
sys.exit(1 if fails else 0)
