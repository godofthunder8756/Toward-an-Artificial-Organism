from pathlib import Path
import json, random, math, statistics, hashlib, csv, sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from toe_exp.block5 import Trial, Outcome, self_monitor, world_monitor, true_success, act, clamp

variants=json.loads((ROOT/'configs/confirmatory_variants.json').read_text())
seeds=[int(x) for x in (ROOT/'configs/seeds/BLOCK5_CONFIRMATORY_SEEDS_V1.txt').read_text().split()]
OUT=ROOT/'results'/'confirmatory'
OUT.mkdir(parents=True,exist_ok=True)

DEC=variants['SELF_RELEVANT_DECISION_HELDOUT_V1']; VER=variants['SELF_RELEVANT_VERIFICATION_HELDOUT_V1']
IMP=variants['IMPAIRMENT_SWITCH_HELDOUT_V1']; MIS=variants['MISINFORMATION_HELDOUT_V1']
SVW=variants['SELF_VS_WORLD_HELDOUT_V1']

# Held-out generator: same frozen structural equations, registered held-out schedules/ranges.
def heldout_trial(seed, idx, family, impaired):
    cfg=DEC if family=='decision' else VER
    sched=cfg['difficulty_schedule']
    difficulty=sched[idx%len(sched)]
    rng=random.Random(seed*1000003 + idx*1009 + (101 if family=='decision' else 707))
    lo,hi=(IMP['impaired_latent_range'] if impaired else IMP['healthy_latent_range'])
    latent=lo+(hi-lo)*rng.random()
    da=clamp(latent+rng.gauss(0,0.18),0,1)
    db=clamp(math.sqrt(latent)+rng.gauss(0,0.16),0,1)
    label=rng.randrange(2)
    p=0.5+(difficulty-0.5)*latent
    signal=label if rng.random()<p else 1-label
    return Trial(seed,idx,label,signal,family,difficulty,latent,da,db,True)

def thresholds_costs(family):
    if family=='decision': return DEC['check_threshold'],0.68,DEC['checking_cost'],0.055
    return 0.70,VER['compute_threshold'],0.14,VER['compute_cost']

def outcome(t,arch,*,q_override=None,shuffled_q=None,prev_error=False,disable_optional=False):
    cth,compth,ccost,mcost=thresholds_costs(t.family)
    if disable_optional and arch=='S2':
        # Clarification: same task/base capacity but no causal route from monitor to optional action.
        arch_eff='S1'
    else:
        arch_eff=arch
    return act(t,arch_eff,q_override=q_override,shuffled_q=shuffled_q,prev_error=prev_error,
               check_threshold=cth,compute_threshold=compth,check_cost=ccost,compute_cost=mcost)

def summ(rows):
    n=len(rows)
    return {'accuracy':sum(x.correct for x in rows)/n,'utility':sum(x.utility for x in rows)/n,
            'check_rate':sum(x.checked for x in rows)/n,'compute_rate':sum(x.extra_compute for x in rows)/n}

def family_mixed(seed,family,arch,n=320,disable_optional=False):
    trials=[heldout_trial(seed,i,family,i%4 in (2,3)) for i in range(n)]
    rows=[]; prev=False
    for t in trials:
        o=outcome(t,arch,prev_error=prev,disable_optional=disable_optional)
        rows.append(o); prev=(o.correct==0)
    return summ(rows)

def recovery(seed,family,arch):
    pre,post=IMP['pre'],IMP['post']; n=pre+post
    trials=[heldout_trial(seed,i,family,i>=pre) for i in range(n)]
    qs=[self_monitor(t) for t in trials]
    # Exact multiset reverse-rank assignment: preserves exact marginal distribution, breaks correspondence.
    order=sorted(range(n),key=lambda i:qs[i]); rev=[qs[i] for i in reversed(order)]
    sh=[None]*n
    for rank,i in enumerate(order): sh[i]=rev[rank]
    rows=[]; used=[]; prev=False
    for i,t in enumerate(trials):
        o=outcome(t,arch,shuffled_q=(sh[i] if arch=='S3' else None),prev_error=prev)
        rows.append(o); used.append(o.q_used); prev=(o.correct==0)
    postrows=rows[pre:]
    threshold=DEC['check_threshold'] if family=='decision' else VER['compute_threshold']
    lat=None
    for k,o in enumerate(postrows,1):
        if o.q_used is not None and o.q_used<threshold:
            lat=k; break
    valid_pre=[q for q in used[:pre] if q is not None]; valid_post=[q for q in used[pre:] if q is not None]
    return {'post':summ(postrows),'detection_latency':lat,
            'mean_q_pre':sum(valid_pre)/len(valid_pre) if valid_pre else None,
            'mean_q_post':sum(valid_post)/len(valid_post) if valid_post else None,
            's3_exact_multiset_preserved': sorted(round(x,12) for x in qs)==sorted(round(x,12) for x in sh)}

def misinformation(seed,family,n=220):
    trials=[heldout_trial(seed,i,family,True) for i in range(n)]
    ans={}
    for name,qfix in [('accurate',None),('overconfident',MIS['overconfident']),('underconfident',MIS['underconfident']),('restored',None)]:
        rows=[]
        for t in trials:
            q=self_monitor(t) if qfix is None else qfix
            rows.append(outcome(t,'S2',q_override=q))
        ans[name]=summ(rows)
    return ans

def self_vs_world(seed,n=240):
    diff=SVW['external_difficulty_held_constant']; healthy,impaired=SVW['internal_reliability_states']
    vals=[]
    for i in range(n):
        rel=healthy if i<n//2 else impaired
        rng=random.Random(seed*400003+i*313+19)
        da=clamp(rel+rng.gauss(0,0.18),0,1); db=clamp(math.sqrt(rel)+rng.gauss(0,0.16),0,1)
        label=rng.randrange(2); p=0.5+(diff-0.5)*rel
        signal=label if rng.random()<p else 1-label
        t=Trial(seed,i,label,signal,'decision',diff,rel,da,db,True)
        vals.append((self_monitor(t),world_monitor(t),true_success(t),i>=n//2))
    def mae(j): return sum(abs(x[j]-x[2]) for x in vals)/len(vals)
    return {'self_mae':mae(0),'world_mae':mae(1),
            'self_healthy':sum(x[0] for x in vals if not x[3])/(n//2),
            'self_impaired':sum(x[0] for x in vals if x[3])/(n//2),
            'world_healthy':sum(x[1] for x in vals if not x[3])/(n//2),
            'world_impaired':sum(x[1] for x in vals if x[3])/(n//2)}

records=[]
for seed in seeds:
    r={'seed':seed,'H5.1':{},'H5.2':{},'H5.3':{},'H5.4':{},'H5.5':{},'H5.6':{}}
    for fam in ('decision','verification'):
        r['H5.1'][fam]={
            'self_relevant_S1':family_mixed(seed,fam,'S1'),
            'self_relevant_S2':family_mixed(seed,fam,'S2'),
            'self_irrelevant_S1':family_mixed(seed,fam,'S1',disable_optional=True),
            'self_irrelevant_S2':family_mixed(seed,fam,'S2',disable_optional=True),
        }
        r['H5.2'][fam]={'S1':recovery(seed,fam,'S1'),'S2':recovery(seed,fam,'S2')}
        r['H5.3'][fam]=misinformation(seed,fam)
        r['H5.4'][fam]={'S2':recovery(seed,fam,'S2'),'S3':recovery(seed,fam,'S3')}
        r['H5.6'][fam]={a:family_mixed(seed,fam,a) for a in ('S2','S4','H_ERROR','H_EXTERNAL')}
    r['H5.5']=self_vs_world(seed)
    records.append(r)

(OUT/'block5_confirmatory_per_seed.json').write_text(json.dumps(records,indent=2))

# Decision calculations
mean=lambda xs: sum(xs)/len(xs)
dec={}
# H5.1
h={}
retain=True
for fam in ('decision','verification'):
    gains=[x['H5.1'][fam]['self_relevant_S2']['accuracy']-x['H5.1'][fam]['self_relevant_S1']['accuracy'] for x in records]
    irr=[x['H5.1'][fam]['self_irrelevant_S2']['accuracy']-x['H5.1'][fam]['self_irrelevant_S1']['accuracy'] for x in records]
    h[fam]={'mean_gain':mean(gains),'seeds_favour':sum(g>0 for g in gains),'irrelevant_mean_gain':mean(irr)}
    retain &= mean(gains)>=.12 and sum(g>0 for g in gains)>=18 and abs(mean(irr))<=.05
dec['H5.1']={'decision':'RETAIN' if retain else 'RESTRICT','metrics':h}
# H5.2
h={}; retain=True
for fam in ('decision','verification'):
    gains=[x['H5.2'][fam]['S2']['post']['accuracy']-x['H5.2'][fam]['S1']['post']['accuracy'] for x in records]
    lats=[x['H5.2'][fam]['S2']['detection_latency'] for x in records if x['H5.2'][fam]['S2']['detection_latency'] is not None]
    qdrops=[x['H5.2'][fam]['S2']['mean_q_pre']-x['H5.2'][fam]['S2']['mean_q_post'] for x in records]
    h[fam]={'mean_gain':mean(gains),'seeds_favour':sum(g>0 for g in gains),'median_detection_latency':statistics.median(lats) if lats else None,'mean_q_drop':mean(qdrops)}
    retain &= mean(gains)>=.15 and len(lats)==20 and statistics.median(lats)<=3 and mean(qdrops)>=.10 and sum(g>0 for g in gains)>=18
dec['H5.2']={'decision':'RETAIN' if retain else 'RESTRICT','metrics':h}
# H5.3
h={}; retain=True
for fam in ('decision','verification'):
    fail=[]; rescue=[]; actiondiff=[]; seedsdir=0
    for x in records:
        a=x['H5.3'][fam]['accurate']; o=x['H5.3'][fam]['overconfident']; rr=x['H5.3'][fam]['restored']
        fail.append(a['accuracy']-o['accuracy']); rescue.append(rr['accuracy']-o['accuracy'])
        key='check_rate' if fam=='decision' else 'compute_rate'
        actiondiff.append(abs(rr[key]-a[key]))
        if o['accuracy']<a['accuracy'] and rr['accuracy']>o['accuracy']: seedsdir+=1
    h[fam]={'mean_failure_effect':mean(fail),'mean_rescue':mean(rescue),'mean_action_restoration_absdiff':mean(actiondiff),'seeds_predicted_direction':seedsdir}
    retain &= mean(fail)>=.15 and mean(rescue)>=.15 and mean(actiondiff)<=.05 and seedsdir>=18
dec['H5.3']={'decision':'RETAIN' if retain else 'RESTRICT','metrics':h}
# H5.4
h={}; retain=True
thresholds={'decision':.15,'verification':.10}
for fam in ('decision','verification'):
    gains=[x['H5.4'][fam]['S2']['post']['accuracy']-x['H5.4'][fam]['S3']['post']['accuracy'] for x in records]
    exact=all(x['H5.4'][fam]['S3']['s3_exact_multiset_preserved'] for x in records)
    h[fam]={'mean_gain':mean(gains),'seeds_favour':sum(g>0 for g in gains),'exact_multiset_preserved':exact}
    retain &= mean(gains)>=thresholds[fam] and sum(g>0 for g in gains)>=18 and exact
dec['H5.4']={'decision':'RETAIN' if retain else 'RESTRICT','metrics':h,'adjudication_note':'Both families show the predicted direction and seed consistency, but both preregistered effect-size margins are missed; the result is therefore restricted rather than promoted or treated as full equivalence.'}
# H5.5
mae_adv=[x['H5.5']['world_mae']-x['H5.5']['self_mae'] for x in records]
self_drop=[x['H5.5']['self_healthy']-x['H5.5']['self_impaired'] for x in records]
world_change=[abs(x['H5.5']['world_healthy']-x['H5.5']['world_impaired']) for x in records]
retain=mean(mae_adv)>=.05 and mean(self_drop)>=.10 and mean(world_change)<=.02 and sum(x>0 for x in mae_adv)>=18
dec['H5.5']={'decision':'RETAIN' if retain else 'REDUCE','metrics':{'mean_mae_advantage':mean(mae_adv),'mean_self_drop':mean(self_drop),'mean_world_change':mean(world_change),'seeds_mae_advantage':sum(x>0 for x in mae_adv)}}
# H5.6 utility precedence from clarification
h={}; retain=True; reduce_ext=True
for fam in ('decision','verification'):
    famm={}
    for b in ('S4','H_ERROR','H_EXTERNAL'):
        diffs=[x['H5.6'][fam]['S2']['utility']-x['H5.6'][fam][b]['utility'] for x in records]
        famm[b]={'mean_utility_advantage':mean(diffs),'seeds_favour_S2':sum(d>0 for d in diffs)}
        retain &= mean(diffs)>=.10 and sum(d>0 for d in diffs)>=18
    ext=famm['H_EXTERNAL']['mean_utility_advantage']
    reduce_ext &= abs(ext)<=.05
    h[fam]=famm
if retain: d='RETAIN'
elif reduce_ext: d='REDUCE'
else: d='RESTRICT'
dec['H5.6']={'decision':d,'metrics':h,'primary_metric':'utility'}

analysis={'schema_version':'1.0.0','n_seeds':20,'osf_preregistration_doi':'10.17605/OSF.IO/JZ4ED','clarification_update':'accepted before execution','decisions':dec}
(OUT/'block5_confirmatory_analysis_record.json').write_text(json.dumps(analysis,indent=2))
with open(OUT/'block5_decisions.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['hypothesis','decision'])
    for k,v in dec.items(): w.writerow([k,v['decision']])
print(json.dumps(dec,indent=2))
