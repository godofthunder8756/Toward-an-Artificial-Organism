import json, collections, hashlib
from fractions import Fraction
R='/workspace/scratch/pr12/audit/gru_v1_3/results/'
d=json.load(open(R+'results.json')); s=json.load(open(R+'summary.json'))
ros=json.load(open('/workspace/review/gru_own_error_audit_roster_v1.json'))
R_or=0.5823877685694766; floor=0.01*R_or; g=1e-10
print('floor 0.01*R', floor, 'json', d['constants']['floor'], floor==d['constants']['floor'])
print('R+Var=', Fraction(d['constants']['R_oracle'])+Fraction(d['constants']['Var_w_q']), float(Fraction(d['constants']['R_oracle'])+Fraction(d['constants']['Var_w_q'])))
print('r2floor check', floor/d['constants']['Var_w_q'], d['constants']['r2_floor'])
def lab(x):
    return 'meets-floor' if x>floor+g else ('below-floor' if x<floor-g else 'BOUNDARY')
def comb(a,b):
    if a=='meets-floor' and b=='meets-floor': return 'meets-floor'
    if 'below-floor' in (a,b): return 'below-floor'
    return 'BOUNDARY'
mism=[];c1m=c2m=c1b=c2b=0;bnd=[];near=[]
units=collections.defaultdict(lambda: collections.Counter())
statuses=collections.Counter(); rl=collections.Counter()
lbase_c1_lt=lbase_c2_lt=0; mind1=[];mind2=[]
import math
for c in d['checkpoints']:
    statuses[c['status']]+=1; rl[(c['pr'],c['arm'] if c['pr'] in (8,9) else '', c['replay_label'])]+=1
    l1=lab(c['C1']['delta']); l2=lab(c['C2']['delta'])
    # check delta arithmetic and r2
    for k in ('C1','C2'):
        C=c[k]
        if C['delta']!=C['L_base']-C['L_full']: mism.append((c['id'],k,'delta'))
        if abs(C['r2']-C['delta']/d['constants']['Var_w_q'])>1e-15: mism.append((c['id'],k,'r2'))
        # pooled from foldwise? check foldwise sum consistency later
    if l1!=c['C1']['label']: mism.append((c['id'],'C1lab'))
    if l2!=c['C2']['label']: mism.append((c['id'],'C2lab'))
    dec=comb(l1,l2)
    if dec!=c['decision']: mism.append((c['id'],'dec'))
    c1m+= l1=='meets-floor'; c2m+= l2=='meets-floor'
    for k in ('C1','C2'):
        if abs(c[k]['delta']-floor)<=1e-6: near.append((c['id'],k,c[k]['delta']-floor))
    if c['C1']['L_base']<=floor: lbase_c1_lt+=1
    if c['C2']['L_base']<=floor: lbase_c2_lt+=1
    mind1.append(c['C1']['delta']-floor); mind2.append(c['C2']['delta']-floor)
    if not all(math.isfinite(v) for k in ('C1','C2') for v in (c[k]['L_base'],c[k]['L_full'],c[k]['delta'])) or not math.isfinite(c['R_exc']): mism.append((c['id'],'nonfinite'))
    st=c['status']
    key=(c['pr'],c['arm'])
    if st=='ok': units[key][{'meets-floor':'m','below-floor':'b','BOUNDARY':'x'}[dec]]+=1
    else: units[key][st]+=1
    units[key]['seeds_'+str(c['seed'])]+=0
print('statuses',statuses); print('replay labels',dict(rl))
print('C1 meets',c1m,'C2 meets',c2m,'of',len(d['checkpoints']))
print('closest C1 delta-floor', max(mind1), 'closest |C1-floor|', min(abs(x) for x in mind1))
print('max C2 delta-floor', max(mind2))
print('near floor within 1e-6', near)
print('C1 L_base<=floor', lbase_c1_lt, 'C2 L_base<=floor', lbase_c2_lt)
print('mismatches', mism[:10], len(mism))
# units
def quota(m,b,x,u,i):
    v=m+b+x
    if v<8: return 'UNRESOLVED (insufficient verified checkpoints)'
    if m>=8: return 'quota is attained'
    if m+u+i<8: return 'quota is not attained'
    return 'quota attainment is UNRESOLVED'
ok=True
for u in d['units']:
    k=(u['pr'],u['arm']); C=units[k]; mine={x:C.get(x,0) for x in 'mbxui'}
    if mine!=u['counts'] or sum(mine.values())!=10 or quota(**mine)!=u['quota']: ok=False; print('UNIT MISMATCH',k,mine,u)
print('units recomputed match:',ok, len(d['units']))
su={(u['pr'],u['arm']):(u['m'],u['b'],u['x'],u['u'],u['i'],u['quota']) for u in s['units']}
rj={(u['pr'],u['arm']):tuple(u['counts'][x] for x in 'mbxui')+(u['quota'],) for u in d['units']}
print('summary==results units', su==rj)
# roster mapping
print(type(ros), list(ros.keys())[:10] if isinstance(ros,dict) else len(ros))
json.dump({'c1m':c1m,'c2m':c2m},open('/dev/null','w'))
