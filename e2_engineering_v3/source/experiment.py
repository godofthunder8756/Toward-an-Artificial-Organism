"""Reproducible E2 runner. All independent seeds are retained."""
import argparse,copy,csv,hashlib,json,platform,time
from pathlib import Path
from dataclasses import asdict
import numpy as np
from .model import Config,Network
VARIANTS=('plastic','static','shuffled')
MODES=('normal','rescue','sham','lost','swap')
def write_csv(path,rows):
    if rows:
        with open(path,'w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def rollout(net,body,seed,rounds,mode='normal',variant='plastic',training=False,history=None,freeze_weights=False,lesion=None):
    cfg=net.cfg;rng=np.random.default_rng(seed);lrng=np.random.default_rng(seed+700000);rows=[];resets=0
    bits=rng.integers(0,2,rounds);attempts=rng.integers(0,2,rounds)
    gu=rng.random(rounds);us=rng.random(rounds);ra=rng.integers(0,3,rounds)
    noises=rng.normal(0,cfg.neural_noise,(rounds,cfg.gap+3,cfg.hidden))
    perms=np.argsort(rng.random((rounds,cfg.hidden,cfg.hidden)),axis=1)
    for t in range(rounds):
        if training and (body.energy<=0 or t%128==0):
            # Training-only energy support; no material or biomass replenishment.
            body.energy=cfg.energy_cap;resets+=1
        active=body.energy>0
        if not active and not training:
            rows.append(dict(trial=t,active=0,action=-1,correct=0,net_energy=0.,energy=body.energy,
                mass_a=float(body.mass[:,net.types==0].sum()),mass_b=float(body.mass[:,net.types==1].sum()),
                store_a=float(body.store[net.types==0].mean()),store_b=float(body.store[net.types==1].mean()),
                resets=resets,mass_added=0.,mass_lost=0.,consumed=0.,external=0.,balance_error=0.,demand_a=0.,demand_b=0.));continue
        z=body.mass.copy();x=net.inputs(body.observe(mode),int(bits[t]),history)
        q,logits,cache=net.forward(x,z,noises[t][None],lesion=lesion)
        action=int(ra[t]) if (training and us[t]<cfg.exploration) or np.ptp(q)==0 else int(q.argmax())
        # Exploratory developmental gate probes are actual paid attempts. Only their
        # success/failure trains the auxiliary recall loss (no target label).
        preferred=int(logits.argmax())
        gate=int(attempts[t]) if training and gu[t]<.30 else preferred
        propensity=.15+.70*(gate==preferred)
        correct=int(gate==bits[t])
        states=np.array(cache[-1])[:,0]
        activity=np.einsum('ti,tj->ij',abs(states[:-1]),abs(states[1:]))/len(x)
        if variant=='shuffled':
            for j in range(cfg.hidden):
                ids=np.flatnonzero(net.mask[:,j]);rank=np.argsort(perms[t,ids,j])
                activity[ids,j]=activity[ids[rank],j]
        if variant=='static':
            target=cfg.initial_mass*net.mask
            desired=np.maximum(0,target-(1-cfg.decay)*body.mass)
            activity=np.divide(desired-cfg.decay*body.mass,cfg.growth*(1-body.mass),out=np.zeros_like(desired),where=(1-body.mass)>1e-12)
        accounting=body.update(action,activity,mode)
        food=.30 if mode=='lost' else cfg.basal_yield
        reward=(food if action==0 else 0.)+(0 if mode=='lost' else cfg.task_yield*correct)-cfg.cost-.008*float(np.mean(abs(states)))
        body.energy=float(np.clip(body.energy+reward,0,cfg.energy_cap))
        if training:
            net.add_learn((x,z,action,reward,net.inputs(body.observe(mode)),body.mass.copy(),body.energy<=0,gate,correct,propensity),lrng,enabled=not freeze_weights)
        rows.append(dict(trial=t,active=1,action=action,correct=correct,net_energy=reward,energy=body.energy,
            mass_a=float(body.mass[:,net.types==0].sum()),mass_b=float(body.mass[:,net.types==1].sum()),
            store_a=float(body.store[net.types==0].mean()),store_b=float(body.store[net.types==1].mean()),resets=resets,**accounting))
    return rows

def metrics(rows):
    n=len(rows);active=sum(r['active'] for r in rows);tail=rows[-min(80,n):]
    return dict(active_fraction=active/n,recall=sum(r['correct'] for r in rows)/n,
        a_rate=sum(r['action']==1 for r in rows)/n,b_rate=sum(r['action']==2 for r in rows)/n,
        a_active=sum(r['action']==1 for r in rows)/max(1,active),b_active=sum(r['action']==2 for r in rows)/max(1,active),
        energy=float(np.mean([r['energy'] for r in tail])),mass_a=float(np.mean([r['mass_a'] for r in tail])),
        mass_b=float(np.mean([r['mass_b'] for r in tail])),demand_a=float(np.mean([r['demand_a'] for r in tail])),
        demand_b=float(np.mean([r['demand_b'] for r in tail])),consumed=sum(r['consumed'] for r in rows),
        external=sum(r['external'] for r in rows),max_balance_error=max(r['balance_error'] for r in rows),completion=int(active==n))

def evaluate(net,body,seed,variant,stage,out,mode='normal',lesion=None):
    result=[]
    for world in range(net.cfg.eval_worlds):
        b=copy.deepcopy(body);b.energy=net.cfg.energy_cap;b.store[:]=net.cfg.initial_store
        rows=rollout(net,b,80000000+world,net.cfg.eval_rounds,mode,variant,lesion=lesion)
        result.append(dict(seed=seed,variant=variant,stage=stage,world=world,**metrics(rows)))
        if world==0:write_csv(out/f'{stage}_trace.csv',rows)
    return result

def run_one(cfg,seed,variant,history,out):
    out.mkdir(parents=True);net=Network(cfg,seed);body=net.initial_body()
    evaluation=evaluate(net,body,seed,variant,'initial',out);development=[]
    for phase,n,route in [('history',cfg.history_rounds,history),('common',cfg.rounds-cfg.history_rounds,None)]:
        rows=rollout(net,body,100000+seed*10+(phase=='common'),n,variant=variant,training=True,history=route)
        for row in rows:row['phase']=phase
        development+=rows
    write_csv(out/'development.csv',development);net.save(out/'developed.npz',body)
    evaluation+=evaluate(net,body,seed,variant,'developed',out)
    evaluation+=evaluate(net,body,seed,variant,'lesion_all',out,lesion=np.ones(cfg.hidden,dtype=bool))
    for chem in [0,1]:evaluation+=evaluate(net,body,seed,variant,f'lesion_{chem}',out,lesion=net.types==chem)
    for mode in MODES:
        child=copy.deepcopy(net);b=copy.deepcopy(body)
        evaluation+=evaluate(child,b,seed,variant,'acute_'+mode,out,mode)
        rows=rollout(child,b,300000+seed,cfg.branch_rounds,mode,variant,training=True)
        write_csv(out/f'{mode}_adaptation.csv',rows);child.save(out/f'{mode}.npz',b)
        evaluation+=evaluate(child,b,seed,variant,mode,out,mode)
    child=copy.deepcopy(net);b=copy.deepcopy(body)
    rows=rollout(child,b,300000+seed,cfg.branch_rounds,'normal',variant,training=True,freeze_weights=True)
    write_csv(out/'frozen_weights_adaptation.csv',rows);child.save(out/'frozen_weights.npz',b)
    evaluation+=evaluate(child,b,seed,variant,'frozen_weights',out)
    for row in evaluation:row['history']=history
    write_csv(out/'evaluation.csv',evaluation);return evaluation

def source_hashes():
    root=Path(__file__).resolve().parent.parent
    paths=sorted((root/'e2').glob('*.py'))+[root/'e1/circuits.py']
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--config')
    p.add_argument('--feasibility',action='store_true');p.add_argument('--variants',nargs='+',default=list(VARIANTS))
    a=p.parse_args();cfg=Config(**json.loads(Path(a.config).read_text())) if a.config else Config()
    if a.feasibility:cfg=Config(**{**asdict(cfg),'seeds':2,'seed_start':1,'eval_worlds':2})
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.time()
    meta=dict(config=asdict(cfg),variants=a.variants,sources=source_hashes(),python=platform.python_version(),numpy=np.__version__,exploratory=a.feasibility)
    (out/'run.json').write_text(json.dumps(meta,indent=2));allrows=[]
    for seed in range(cfg.seed_start,cfg.seed_start+cfg.seeds):
        for variant in a.variants:
            for history in (0,1):
                rows=run_one(cfg,seed,variant,history,out/f'seed_{seed}_{variant}_h{history}')
                allrows+=rows;write_csv(out/'evaluation.csv',allrows)
                r=[x for x in rows if x['stage']=='developed']
                print(seed,variant,history,'recall',round(np.mean([x['recall'] for x in r]),3),'A/B',
                    round(np.mean([x['a_rate'] for x in r]),3),round(np.mean([x['b_rate'] for x in r]),3),'sec',round(time.time()-start),flush=True)
    meta['seconds']=time.time()-start;(out/'run.json').write_text(json.dumps(meta,indent=2))
if __name__=='__main__':main()
