from __future__ import annotations
import json, math, hashlib, argparse
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Regenerate the preregistered B2 confirmatory analysis from raw run directories.')
parser.add_argument('--raw-root', default='results_b2_confirmatory/raw', help='Root containing experiment raw-run folders. Both exp/1.0.0/run and exp/run layouts are supported.')
parser.add_argument('--output-root', default='analysis_confirmatory', help='Directory for regenerated analysis artefacts.')
args = parser.parse_args()
RAW = Path(args.raw_root)
OUT = Path(args.output_root)
OUT.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(20261002)
NBOOT=10000

EXPS = [
'B2_MAINT_LOW_CONFIRM_001','B2_MAINT_MEDIUM_CONFIRM_001','B2_MAINT_HIGH_CONFIRM_001',
'B2_SUPPORT_WITHDRAW_CONFIRM_001','B2_ABLATE_C1_CONFIRM_001',
'B2_RESCUE_SPECIFIC_CONFIRM_001','B2_RESCUE_IRRELEVANT_CONFIRM_001']

def valid_run_dir(exp):
    base=RAW/exp/'1.0.0'
    if not base.exists():
        base=RAW/exp
    if not base.exists():
        raise RuntimeError(f'{exp}: raw directory not found under {RAW}')
    valid=[]
    partial=[]
    for d in sorted(base.iterdir()):
        if not d.is_dir(): continue
        v=d/'provenance_validation.json'
        s=d/'run_summary.json'
        if v.exists() and s.exists():
            rec=json.loads(v.read_text())
            if rec.get('status')=='PASS': valid.append(d)
            else: partial.append(d)
        else: partial.append(d)
    if len(valid)!=1:
        raise RuntimeError(f'{exp}: expected exactly 1 valid run, got {len(valid)}: {valid}')
    return valid[0], partial

def load_terminal(exp):
    d,partial=valid_run_dir(exp)
    path=d/'trajectories.jsonl'
    terminal={}
    # key arch, seed -> last record
    with path.open() as f:
        for line in f:
            r=json.loads(line)
            key=(r['architecture_id'], int(r['seed']))
            terminal[key]=r
    rows=[]
    for (arch,seed),r in sorted(terminal.items()):
        st=r['state_after']
        # failure time: derive by re-scan separately later if needed
        rows.append({
            'experiment_id':exp,'architecture_id':arch,'seed':seed,
            'terminal_q1':st['q'][0],'terminal_q2':st['q'][1],'terminal_q3':st['q'][2],
            'terminal_min_q':st['min_q'],'terminal_mean_q':st['mean_q'],
            'terminal_viable':bool(st['viable']),'path_viable':not bool(st['ever_failed']),
            'maintenance_total_terminal':st['maintenance_total'],
            'run_id':r['run_id'],
        })
    return pd.DataFrame(rows),d,partial

def failure_times(exp):
    d,_=valid_run_dir(exp)
    first={}
    horizon={}
    with (d/'trajectories.jsonl').open() as f:
        for line in f:
            r=json.loads(line); key=(r['architecture_id'],int(r['seed']))
            step=int(r['state_after']['step']); horizon[key]=max(horizon.get(key,0),step)
            if not r['state_after']['viable'] and key not in first: first[key]=step
    rows=[]
    for key,h in horizon.items():
        rows.append({'architecture_id':key[0],'seed':key[1],'failure_step':first.get(key, h+1),'censored':key not in first,'horizon':h})
    return pd.DataFrame(rows)

def wilson(k,n,z=1.959963984540054):
    if n==0:return [None,None]
    p=k/n; den=1+z*z/n
    cen=(p+z*z/(2*n))/den
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [cen-half,cen+half]

def boot_ci(vals):
    a=np.asarray(vals,float)
    idx=RNG.integers(0,len(a),size=(NBOOT,len(a)))
    means=a[idx].mean(axis=1)
    return [float(np.quantile(means,.025)),float(np.quantile(means,.975))]

def stats_count(df,arch,col='path_viable'):
    x=df[df.architecture_id==arch][col].astype(bool)
    return {'count':int(x.sum()),'n':int(len(x)),'proportion':float(x.mean()),'wilson95':wilson(int(x.sum()),len(x))}

frames={}; runs={}; partials={}
for exp in EXPS:
    frames[exp],runs[exp],partials[exp]=load_terminal(exp)

# Save all terminal per-seed metrics
all_df=pd.concat(frames.values(),ignore_index=True)
all_df.to_csv(OUT/'b2_per_seed_terminal_metrics.csv',index=False)

low=frames['B2_MAINT_LOW_CONFIRM_001']; med=frames['B2_MAINT_MEDIUM_CONFIRM_001']; high=frames['B2_MAINT_HIGH_CONFIRM_001']
withdraw=frames['B2_SUPPORT_WITHDRAW_CONFIRM_001']; abl=frames['B2_ABLATE_C1_CONFIRM_001']; spec=frames['B2_RESCUE_SPECIFIC_CONFIRM_001']; irr=frames['B2_RESCUE_IRRELEVANT_CONFIRM_001']
active=['B2_EXTERNAL','B2_FEEDFORWARD','B2_RECIPROCAL','B2_BRUTE_FORCE']

# H1.1
pv_low=stats_count(low,'B2_PASSIVE')
pv_med=stats_count(med,'B2_PASSIVE')
pv_high=stats_count(high,'B2_PASSIVE')
active_high={a:stats_count(high,a) for a in active}
active_adv=np.mean([active_high[a]['proportion'] for a in active])-pv_high['proportion']
h11_retain=(pv_low['count']>=16 and pv_med['proportion']<pv_low['proportion'] and pv_med['proportion']>pv_high['proportion'] and pv_high['count']<=4 and sum(active_high[a]['count']>=16 for a in active)>=3 and active_adv>=.60)
if pv_low['count']<16: h11='SUSPEND'
elif h11_retain: h11='RETAIN'
elif pv_high['proportion']>=min(active_high[a]['proportion'] for a in active): h11='REJECT'
else: h11='RESTRICT'

# H1.2
wstats={a:stats_count(withdraw,a,'terminal_viable') for a in ['B2_EXTERNAL','B2_FEEDFORWARD','B2_RECIPROCAL','B2_BRUTE_FORCE']}
wmean={a:float(withdraw[withdraw.architecture_id==a].terminal_min_q.mean()) for a in wstats}
ext=wmean['B2_EXTERNAL']
internal=['B2_FEEDFORWARD','B2_RECIPROCAL','B2_BRUTE_FORCE']
int_diffs={a:wmean[a]-ext for a in internal}
h12_retain=(wstats['B2_EXTERNAL']['count']<=4 and all(wstats[a]['count']>=16 for a in internal) and sum(v>=.25 for v in int_diffs.values())>=2)
if h12_retain: h12='RETAIN'
elif wstats['B2_EXTERNAL']['proportion']>=min(wstats[a]['proportion'] for a in internal): h12='REDUCE/REJECT'
else:h12='RESTRICT'

# Helpers to paired data by seed
def paired(base, other, arch, base_col, other_col=None):
    other_col=other_col or base_col
    a=base[base.architecture_id==arch][['seed',base_col]].rename(columns={base_col:'base'})
    b=other[other.architecture_id==arch][['seed',other_col]].rename(columns={other_col:'other'})
    m=a.merge(b,on='seed',validate='one_to_one')
    m['diff']=m['base']-m['other']
    return m

# H1.3 deficits intact medium - ablated
rec_c2=paired(med,abl,'B2_RECIPROCAL','terminal_q2')
rec_c3=paired(med,abl,'B2_RECIPROCAL','terminal_q3')
rec=rec_c2[['seed','diff']].rename(columns={'diff':'c2_def'}).merge(rec_c3[['seed','diff']].rename(columns={'diff':'c3_def'}),on='seed')
rec['selectivity']=rec.c2_def-rec.c3_def
ff_c2=paired(med,abl,'B2_FEEDFORWARD','terminal_q2')
ff_c3=paired(med,abl,'B2_FEEDFORWARD','terminal_q3')
ff=ff_c2[['seed','diff']].rename(columns={'diff':'c2_def'}).merge(ff_c3[['seed','diff']].rename(columns={'diff':'c3_def'}),on='seed')
ff['abs_diff']=(ff.c2_def-ff.c3_def).abs()
# brute signature diagnostic
bf_c2=paired(med,abl,'B2_BRUTE_FORCE','terminal_q2')
bf_c3=paired(med,abl,'B2_BRUTE_FORCE','terminal_q3')
bf=bf_c2[['seed','diff']].rename(columns={'diff':'c2_def'}).merge(bf_c3[['seed','diff']].rename(columns={'diff':'c3_def'}),on='seed')
bf['selectivity']=bf.c2_def-bf.c3_def
h13_retain=(rec.c2_def.mean()>.25 and int((rec.c2_def>=.30).sum())>=16 and int((rec.selectivity>=.20).sum())>=16 and int((ff.abs_diff<=.15).sum())>=16)
# reduction check if feedforward/brute reproduces reciprocal propagation: operationally check primary signature thresholds in alt
alt_same=((ff.c2_def.mean()>.25 and (ff.c2_def>=.30).sum()>=16 and ((ff.c2_def-ff.c3_def)>=.20).sum()>=16) or (bf.c2_def.mean()>.25 and (bf.c2_def>=.30).sum()>=16 and (bf.selectivity>=.20).sum()>=16))
if h13_retain and not alt_same:h13='RETAIN'
elif alt_same:h13='REDUCE'
elif rec.c2_def.mean()>.25:h13='RESTRICT'
else:h13='REJECT'

# H1.4 rescue terminal C2 relative no rescue reciprocal
no=abl[abl.architecture_id=='B2_RECIPROCAL'][['seed','terminal_q2']].rename(columns={'terminal_q2':'no'})
sp=spec[spec.architecture_id=='B2_RECIPROCAL'][['seed','terminal_q2']].rename(columns={'terminal_q2':'specific'})
ir=irr[irr.architecture_id=='B2_RECIPROCAL'][['seed','terminal_q2']].rename(columns={'terminal_q2':'irrelevant'})
r=no.merge(sp,on='seed').merge(ir,on='seed')
r['specific_gain']=r.specific-r.no
r['specific_vs_irrelevant']=r.specific-r.irrelevant
r['irrelevant_gain']=r.irrelevant-r.no
h14_retain=(r.specific_gain.mean()>=.30 and (r.specific_gain>=.30).sum()>=16 and r.specific_vs_irrelevant.mean()>=.30 and (r.specific_vs_irrelevant>=.30).sum()>=16 and r.irrelevant_gain.mean()<.10)
if h14_retain:h14='RETAIN'
elif r.specific_gain.mean()>0 and r.specific_vs_irrelevant.mean()>0:h14='RESTRICT'
else:h14='REJECT'

# H1.6 bypass
hi_rec=high[high.architecture_id=='B2_RECIPROCAL']; hi_bf=high[high.architecture_id=='B2_BRUTE_FORCE']
path_diff=abs(hi_bf.path_viable.mean()-hi_rec.path_viable.mean())
minq_diff=abs(hi_bf.terminal_min_q.mean()-hi_rec.terminal_min_q.mean())
ab_rec=abl[abl.architecture_id=='B2_RECIPROCAL'].copy(); ab_bf=abl[abl.architecture_id=='B2_BRUTE_FORCE'].copy()
ab_rec['nonablated_mean']=(ab_rec.terminal_q2+ab_rec.terminal_q3)/2
ab_bf['nonablated_mean']=(ab_bf.terminal_q2+ab_bf.terminal_q3)/2
ab_pair=ab_bf[['seed','nonablated_mean']].rename(columns={'nonablated_mean':'bf'}).merge(ab_rec[['seed','nonablated_mean']].rename(columns={'nonablated_mean':'rec'}),on='seed')
ab_pair['bf_minus_rec']=ab_pair.bf-ab_pair.rec
ab_condition=float(ab_pair.bf.mean()) >= float(ab_pair.rec.mean())-.05
h16_reduce=(path_diff<=.10 and minq_diff<=.10 and ab_condition)
if h16_reduce:h16='REDUCE_RECIPROCAL_NECESSITY'
elif h13=='RETAIN' and h14=='RETAIN' and (path_diff>.10 or minq_diff>.10 or not ab_condition):h16='RETAIN_EXPLANATORY_GAIN'
else:h16='RESTRICT'

# uncertainty summaries
cis={
'reciprocal_C1_to_C2_effect_bootstrap95':boot_ci(rec.c2_def),
'reciprocal_selectivity_bootstrap95':boot_ci(rec.selectivity),
'specific_rescue_gain_C2_bootstrap95':boot_ci(r.specific_gain),
'specific_vs_irrelevant_C2_bootstrap95':boot_ci(r.specific_vs_irrelevant),
'irrelevant_rescue_gain_C2_bootstrap95':boot_ci(r.irrelevant_gain),
'high_terminal_min_q_bf_minus_reciprocal_bootstrap95':boot_ci(hi_bf[['seed','terminal_min_q']].merge(hi_rec[['seed','terminal_min_q']],on='seed',suffixes=('_bf','_rec')).eval('terminal_min_q_bf-terminal_min_q_rec')),
'ablation_nonablated_bf_minus_reciprocal_bootstrap95':boot_ci(ab_pair.bf_minus_rec),
}

# failure-time summaries for low/medium/high/support withdrawal
failure_summary={}
for exp in ['B2_MAINT_LOW_CONFIRM_001','B2_MAINT_MEDIUM_CONFIRM_001','B2_MAINT_HIGH_CONFIRM_001','B2_SUPPORT_WITHDRAW_CONFIRM_001']:
    ft=failure_times(exp)
    for arch,g in ft.groupby('architecture_id'):
        obs=g[~g.censored].failure_step
        failure_summary[f'{exp}:{arch}']={
            'failures':int((~g.censored).sum()),'n':int(len(g)),
            'median_failure_step_observed':None if obs.empty else float(obs.median()),
            'right_censored':int(g.censored.sum()),'horizon':int(g.horizon.max())}

# Condition summaries
condition_summary={}
for exp,df in frames.items():
    condition_summary[exp]={}
    for arch,g in df.groupby('architecture_id'):
        condition_summary[exp][arch]={
            'n':int(len(g)), 'path_viable_count':int(g.path_viable.sum()), 'terminal_viable_count':int(g.terminal_viable.sum()),
            'mean_terminal_min_q':float(g.terminal_min_q.mean()), 'mean_terminal_q':[float(g.terminal_q1.mean()),float(g.terminal_q2.mean()),float(g.terminal_q3.mean())]
        }

record={
  'study':'B2 Causal Maintenance Network','preregistration_doi':'10.17605/OSF.IO/GQANP',
  'analysis_rng_seed':20261002,'bootstrap_resamples':10000,
  'valid_run_ids':{k:runs[k].name for k in EXPS},
  'excluded_technical_attempts':{k:[p.name for p in partials[k]] for k in EXPS if partials[k]},
  'hypothesis_verdicts':{'H1.1':h11,'H1.2':h12,'H1.3':h13,'H1.4':h14,'H1.5':'DEFERRED','H1.6':h16},
  'H1.1':{'passive_low':pv_low,'passive_medium':pv_med,'passive_high':pv_high,'active_high':active_high,'mean_active_minus_passive_high_path_viability_advantage':float(active_adv)},
  'H1.2':{'terminal_viability':wstats,'mean_terminal_min_q':wmean,'internal_minus_external_mean_terminal_min_q':int_diffs},
  'H1.3':{'mean_reciprocal_C1_to_C2_effect':float(rec.c2_def.mean()),'reciprocal_C2_deficit_ge_0_30_count':int((rec.c2_def>=.30).sum()),'reciprocal_selectivity_ge_0_20_count':int((rec.selectivity>=.20).sum()),'feedforward_abs_C2_C3_deficit_le_0_15_count':int((ff.abs_diff<=.15).sum()),'bruteforce_mean_C2_deficit':float(bf.c2_def.mean()),'bruteforce_mean_selectivity':float(bf.selectivity.mean()),'alternative_reproduces_signature':bool(alt_same)},
  'H1.4':{'mean_specific_gain_C2':float(r.specific_gain.mean()),'specific_gain_ge_0_30_count':int((r.specific_gain>=.30).sum()),'mean_specific_vs_irrelevant_C2':float(r.specific_vs_irrelevant.mean()),'specific_vs_irrelevant_ge_0_30_count':int((r.specific_vs_irrelevant>=.30).sum()),'mean_irrelevant_gain_C2':float(r.irrelevant_gain.mean())},
  'H1.6':{'high_path_viability_abs_difference_bf_vs_reciprocal':float(path_diff),'high_mean_terminal_min_q_abs_difference_bf_vs_reciprocal':float(minq_diff),'ablation_nonablated_mean_bf':float(ab_pair.bf.mean()),'ablation_nonablated_mean_reciprocal':float(ab_pair.rec.mean()),'ablation_bf_minus_reciprocal':float(ab_pair.bf_minus_rec.mean()),'noninferiority_conditions_all_hold':bool(h16_reduce)},
  'bootstrap95':cis,'failure_time_summary':failure_summary,'condition_summary':condition_summary,
  'scope':'Artificial functional/causal maintenance within the preregistered three-component architecture family; H1.5 boundary/timescale robustness deferred; no claim of life or universal reciprocal closure necessity.'
}

(OUT/'b2_confirmatory_analysis_record.json').write_text(json.dumps(record,indent=2,sort_keys=True),encoding='utf-8')
rec.assign(metric='reciprocal_ablation').to_csv(OUT/'h13_reciprocal_ablation_effects.csv',index=False)
ff.to_csv(OUT/'h13_feedforward_ablation_effects.csv',index=False)
r.to_csv(OUT/'h14_rescue_effects.csv',index=False)
ab_pair.to_csv(OUT/'h16_bypass_ablation_comparison.csv',index=False)

# Summary markdown
md=[]
md += ['# B2 Confirmatory Analysis Record','',f'Preregistration: 10.17605/OSF.IO/GQANP','', '## Preregistered verdicts','']
for k,v in record['hypothesis_verdicts'].items(): md.append(f'- **{k}: {v}**')
md += ['', '## Key registered estimands','', f"- H1.1 passive path viability low/medium/high: {pv_low['count']}/20, {pv_med['count']}/20, {pv_high['count']}/20.", f"- H1.1 high-disturbance mean active-minus-passive path-viability advantage: {active_adv:.3f}.", f"- H1.2 external terminal viability after support withdrawal: {wstats['B2_EXTERNAL']['count']}/20; feed-forward {wstats['B2_FEEDFORWARD']['count']}/20; reciprocal {wstats['B2_RECIPROCAL']['count']}/20; brute-force {wstats['B2_BRUTE_FORCE']['count']}/20.", f"- H1.3 mean paired reciprocal C1→C2 effect: {rec.c2_def.mean():.6f}; C2 deficit ≥0.30 in {(rec.c2_def>=.30).sum()}/20; topology selectivity ≥0.20 in {(rec.selectivity>=.20).sum()}/20.", f"- H1.4 mean specific rescue gain in C2: {r.specific_gain.mean():.6f}; mean specific-minus-irrelevant rescue effect: {r.specific_vs_irrelevant.mean():.6f}; irrelevant rescue mean C2 gain: {r.irrelevant_gain.mean():.6f}.", f"- H1.6 high-disturbance path-viability absolute difference (brute-force vs reciprocal): {path_diff:.6f}; terminal minimum-state absolute difference: {minq_diff:.6f}; post-ablation brute-force minus reciprocal mean non-ablated state: {ab_pair.bf_minus_rec.mean():.6f}.", '', '## Interpretation','', 'The confirmatory design permits a mixed outcome. A causal reciprocal edge and specific functional rescue can be retained while reciprocal topology is reduced as a necessity claim if the preregistered serious bypass satisfies its non-inferiority conditions.', '', 'H1.5 was preregistered as deferred and receives no verdict from this study.', '', 'The result does not establish biological life, universal organisational closure, the historical origin of life, intelligence, or consciousness.']
(OUT/'B2_CONFIRMATORY_ANALYSIS_RECORD.md').write_text('\n'.join(md)+'\n',encoding='utf-8')

# Figure: path viability across disturbances
fig,ax=plt.subplots(figsize=(8,5))
arches=['B2_PASSIVE','B2_EXTERNAL','B2_FEEDFORWARD','B2_RECIPROCAL','B2_BRUTE_FORCE']
labels=['Passive','External','Feed-forward','Reciprocal','Brute-force']
xs=np.arange(3)
for arch,label in zip(arches,labels):
    vals=[frames[e][frames[e].architecture_id==arch].path_viable.mean() for e in ['B2_MAINT_LOW_CONFIRM_001','B2_MAINT_MEDIUM_CONFIRM_001','B2_MAINT_HIGH_CONFIRM_001']]
    ax.plot(xs,vals,marker='o',label=label)
ax.set_xticks(xs,['Low','Medium','High']); ax.set_ylim(-.05,1.05); ax.set_ylabel('Path viability proportion'); ax.set_xlabel('Disturbance regime'); ax.set_title('B2 confirmatory path viability'); ax.legend(loc='best',fontsize=8); fig.tight_layout(); fig.savefig(OUT/'b2_path_viability_by_disturbance.png',dpi=180); plt.close(fig)

# Artifact checksums
files=[p for p in OUT.iterdir() if p.is_file() and p.name != 'artifact_checksums.json']
checks={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
(OUT/'artifact_checksums.json').write_text(json.dumps(checks,indent=2,sort_keys=True),encoding='utf-8')
print(json.dumps(record['hypothesis_verdicts'],indent=2))
print(json.dumps({'H1.1':record['H1.1'],'H1.2':record['H1.2'],'H1.3':record['H1.3'],'H1.4':record['H1.4'],'H1.6':record['H1.6'],'bootstrap95':cis},indent=2))
