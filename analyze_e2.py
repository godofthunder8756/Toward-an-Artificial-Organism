"""Seed-level descriptive inference for frozen E2; no per-trial pseudoreplication."""
import argparse,csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from e2.experiment import VARIANTS

def analyze(root):
    root=Path(root);rows=list(csv.DictReader(open(root/'evaluation.csv')))
    seeds=sorted({int(r['seed']) for r in rows});n=len(seeds)
    from collections import defaultdict
    grouped=defaultdict(list)
    for r in rows:grouped[(int(r['seed']),r['variant'],r['stage'])].append(r)
    rng=np.random.default_rng(91823);indices=rng.integers(0,n,(10000,n))
    def stat(x):
        x=np.array(x,float);b=x[indices].mean(1)
        return dict(mean=float(x.mean()),lo=float(np.quantile(b,.025)),hi=float(np.quantile(b,.975)),seeds=x.tolist())
    def vec(v,st,k,h=None):
        return np.array([np.mean([float(r[k]) for r in grouped[(s,v,st)] if (h is None or int(r['history'])==h)]) for s in seeds])
    stages=['initial','developed','normal','rescue','sham','lost','acute_swap','swap','frozen_weights','lesion_all']
    summary={v:{st:{k:stat(vec(v,st,k)) for k in ['recall','active_fraction','a_rate','b_rate','completion','mass_a','mass_b','energy']} for st in stages} for v in VARIANTS}
    contrasts={}
    for v in VARIANTS:
        rate=lambda st:vec(v,st,'a_rate')+vec(v,st,'b_rate')
        d=((vec(v,'developed','a_rate',0)-vec(v,'developed','b_rate',0))-(vec(v,'developed','a_rate',1)-vec(v,'developed','b_rate',1)))/2
        l=((vec(v,'lesion_1','recall',0)-vec(v,'lesion_0','recall',0))-(vec(v,'lesion_1','recall',1)-vec(v,'lesion_0','recall',1)))/2
        contrasts[v]={
            'development':stat(vec(v,'developed','recall')-vec(v,'initial','recall')),
            'history_priority':stat(d),'history_dependence':stat(l),
            'swap_recovery':stat(vec(v,'swap','recall')-vec(v,'acute_swap','recall')),
            'normal_minus_lost_collection':stat(rate('normal')-rate('lost')),
            'lost_collection':stat(rate('lost')),
            'normal_minus_rescue_collection':stat(rate('normal')-rate('rescue')),
            'normal_minus_frozen_recall':stat(vec(v,'normal','recall')-vec(v,'frozen_weights','recall'))}
    for rival in ['static','shuffled']:
        contrasts['plastic_minus_'+rival]=stat(vec('plastic','developed','recall')-vec(rival,'developed','recall'))
    c=contrasts['plastic'];s=summary['plastic'];adv=[contrasts['plastic_minus_'+r] for r in ['static','shuffled']]
    gates={
        'functional_development':s['developed']['recall']['mean']>=.85 and s['developed']['active_fraction']['mean']>=.90 and c['development']['lo']>0,
        'selective_value_of_growth':all(x['mean']>=.05 and x['lo']>0 for x in adv),
        'history_specific_priority':c['history_priority']['mean']>=.02 and c['history_priority']['lo']>0,
        'history_specific_dependence':c['history_dependence']['mean']>=.05 and c['history_dependence']['lo']>0,
        'viable_relinquishment':s['lost']['active_fraction']['mean']>=.90 and c['lost_collection']['mean']<=.05 and c['normal_minus_lost_collection']['lo']>0,
        'chemistry_swap_recovery':c['swap_recovery']['mean']>=.10 and c['swap_recovery']['lo']>0}
    result=dict(seeds=seeds,replication_unit='initial seed; histories and worlds paired within seed',summary=summary,contrasts=contrasts,gates={k:bool(v) for k,v in gates.items()})
    (root/'summary.json').write_text(json.dumps(result,indent=2))
    fmt=lambda x:f"{100*x['mean']:.1f} [{100*x['lo']:.1f}, {100*x['hi']:.1f}]"
    lines=['# E2 results','',f'{n} independent initial seeds; two paired histories per seed. Values below are means and descriptive 95% seed-bootstrap intervals, in percentage points. No multiplicity correction.','',
        '| Variant | Developed recall / planned | Active fraction | Completion |','| --- | ---: | ---: | ---: |']
    for v in VARIANTS:lines.append(f"| {v} | {fmt(summary[v]['developed']['recall'])} | {fmt(summary[v]['developed']['active_fraction'])} | {fmt(summary[v]['developed']['completion'])} |")
    lines+=['','## Frozen gates','', '| Gate | Outcome |','| --- | --- |']+[f"| {k} | {'PASS' if v else 'FAIL'} |" for k,v in gates.items()]
    lines+=['','## Primary contrasts','', '| Contrast | Mean [95% interval], points |','| --- | ---: |']
    for name in ['plastic_minus_static','plastic_minus_shuffled']:lines.append(f'| {name} | {fmt(contrasts[name])} |')
    for name,x in c.items():lines.append(f'| plastic: {name} | {fmt(x)} |')
    lines+=['','## All evaluated conditions','', '| Variant | Condition | Recall / planned | Active % | A collection / planned | B collection / planned |','| --- | --- | ---: | ---: | ---: | ---: |']
    for v in VARIANTS:
        for st in stages:
            ss=summary[v][st];lines.append(f"| {v} | {st} | {100*ss['recall']['mean']:.1f} | {100*ss['active_fraction']['mean']:.1f} | {100*ss['a_rate']['mean']:.1f} | {100*ss['b_rate']['mean']:.1f} |")
    lines+=['','Interpretation must follow E2_PROTOCOL.md. Bootstrap intervals condition on six common worlds. These controllers use explicit energy and recall objectives. E2 tests partial developmental coupling, not life or consciousness.']
    (root/'RESULTS.md').write_text('\n'.join(lines)+'\n')
    # Exportable scientific figure. All uncertainty is across independent seeds.
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(2,2,figsize=(12,8.4),constrained_layout=True)
    colors=['#008678','#6075b4','#c1772f']
    for j,v in enumerate(VARIANTS):
        x=summary[v]['developed']['recall'];y=np.array(x['seeds'])*100
        jitter=np.linspace(-.13,.13,len(y))
        ax[0,0].scatter(j+jitter,y,color=colors[j],s=18,alpha=.7)
        ax[0,0].errorbar(j,100*x['mean'],yerr=[[100*(x['mean']-x['lo'])],[100*(x['hi']-x['mean'])]],color='black',fmt='D',capsize=5)
    ax[0,0].set(xticks=range(3),xticklabels=['Local growth','Fixed target','Shuffled growth'],ylim=(-3,104),ylabel='Correct recall / planned trials (%)',title='A  Does local growth improve function?')
    stlist=['normal','rescue','sham','lost','swap']
    yy=[]
    for j,st in enumerate(stlist):
        rr=vec('plastic',st,'a_rate')+vec('plastic',st,'b_rate');xx=stat(rr);yy.append(xx['mean']*100)
        ax[0,1].errorbar(j,100*xx['mean'],yerr=[[100*(xx['mean']-xx['lo'])],[100*(xx['hi']-xx['mean'])]],fmt='o',color=colors[0],capsize=4)
    ax[0,1].set(xticks=range(5),xticklabels=['Normal','Repair','Sham','Task lost','Swapped'],ylabel='Material choices / planned trials (%)',title='B  Acquired resource priorities: local growth',ylim=(0,max(yy)*1.6+5))
    for j,st in enumerate(stlist):ax[0,1].text(j,0.5,f"{100*s[st]['active_fraction']['mean']:.0f}% active",ha='center',fontsize=8,rotation=90,va='bottom',alpha=.6)
    # Developmental edge density trajectories, one curve per seed after averaging
    # histories; downsample at 100-trial blocks to keep readable.
    for j,v in enumerate(VARIANTS):
        trajectories=[]
        for seed in seeds:
            hs=[]
            for h in [0,1]:
                d=list(csv.DictReader(open(root/f'seed_{seed}_{v}_h{h}'/'development.csv')))
                z=np.load(root/f'seed_{seed}_{v}_h{h}'/'developed.npz',allow_pickle=False)
                mass=np.array([float(r['mass_a'])+float(r['mass_b']) for r in d])/z['mask'].sum()
                hs.append(mass.reshape(-1,100).mean(1))
            trajectories.append(np.mean(hs,axis=0))
        arr=np.array(trajectories);t=np.arange(arr.shape[1])*100+50
        ax[1,0].plot(t,arr.mean(0),label=['Local growth','Fixed target','Shuffled growth'][j],color=colors[j])
        ax[1,0].fill_between(t,np.quantile(arr,.25,axis=0),np.quantile(arr,.75,axis=0),alpha=.12,color=colors[j])
    ax[1,0].axvline(2000,ls=':',color='#777');ax[1,0].set(xlabel='Developmental trials',ylabel='Mean edge biomass',title='C  Developing structure (bands: seed IQR)');ax[1,0].legend(frameon=False,fontsize=9)
    for j,v in enumerate(VARIANTS):
        for k,key in enumerate(['history_priority','history_dependence']):
            x=contrasts[v][key];pos=k+(j-1)*.17
            ax[1,1].errorbar(pos,100*x['mean'],yerr=[[100*(x['mean']-x['lo'])],[100*(x['hi']-x['mean'])]],fmt='o',color=colors[j],capsize=3)
    ax[1,1].axhline(0,color='#888',lw=1);ax[1,1].set(xticks=[0,1],xticklabels=['Resource preference D','Lesion dependence L'],ylabel='Paired history effect (percentage points)',title='D  Did different histories create different needs?')
    fig.suptitle('E2: One maintained network, developing connections, explicit learning objectives',fontsize=14)
    import io
    buffer=io.BytesIO();fig.savefig(buffer,format='png',dpi=180,facecolor='white')
    (root/'E2_RESULTS.png').write_bytes(buffer.getvalue());plt.close(fig)
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('results');a=p.parse_args();r=analyze(a.results)
    print(json.dumps({'gates':r['gates'],'primary_contrasts':{k:v for k,v in r['contrasts'].items() if k.startswith('plastic_minus')}},indent=2))
