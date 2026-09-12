"""Exploratory post-freeze diagnostics; never used to select or retune agents.

Separates fixed-snapshot computational capacity from closed-loop viability and
checks whether preserved weight information supplies restoration from outside
biomass. This is a diagnostic intervention, not a new learning architecture.
"""
import argparse,copy,csv,json
from pathlib import Path
import numpy as np
from e2.model import Config,Network
from e2.experiment import write_csv

def main(root):
    root=Path(root);cfg=Config(**json.loads((root/'run.json').read_text())['config']);rows=[]
    rng=np.random.default_rng(99000001);bits=np.tile([0,1],256)
    noise=rng.normal(0,cfg.neural_noise,(len(bits),cfg.gap+3,cfg.hidden))
    for d in sorted(root.glob('seed_*')):
        net,b=Network.load(d/'developed.npz',cfg)
        _,sid,variant,hstr=d.name.split('_');hist=int(hstr[1:]);seed=int(sid)
        b.energy=cfg.energy_cap;b.store[:]=cfg.initial_store
        x=np.array([net.inputs(b.observe(),int(bit)) for bit in bits])
        obs_mass=b.mass.copy()
        intact=net.forward(x,obs_mass,noise)[1].argmax(1)
        # Give a scalar conductance model every bit of its prior mass back.
        depleted=obs_mass*.03
        q,l,_=net.forward(x,depleted,noise);depleted_acc=float(np.mean(l.argmax(1)==bits))
        restored=net.forward(x,obs_mass,noise)[1].argmax(1)
        # Information-loss intervention: permute signed recurrent weights across
        # allowed edges; preserves their histogram and structural resource cost.
        eroded=copy.deepcopy(net);ids=np.flatnonzero(net.mask)
        rr=np.random.default_rng(65000000+seed)
        flat=eroded.p['w'].ravel();original=flat[ids].copy();flat[ids]=original[rr.permutation(len(ids))]
        eroded_logits=eroded.forward(x,obs_mass,noise)[1]
        donor=root/f'seed_{seed}_{variant}_h{1-hist}'/'developed.npz'
        donor_net,donor_body=Network.load(donor,cfg)
        # Same weights, input observations and random noise, different developed
        # biomass from its paired history. No retuning and no claim of autonomy.
        donor_logits=net.forward(x,donor_body.mass,noise)[1]
        rows.append(dict(seed=seed,variant=variant,history=hist,
            snapshot_recall=float(np.mean(intact==bits)),depleted_snapshot_recall=depleted_acc,
            restored_snapshot_recall=float(np.mean(restored==bits)),restored_exact=int(np.array_equal(intact,restored)),
            shuffled_weight_recall=float(np.mean(eroded_logits.argmax(1)==bits)),
            paired_history_biomass_recall=float(np.mean(donor_logits.argmax(1)==bits)),
            developed_mean_mass=float(obs_mass.sum()/net.mask.sum())))
    write_csv(root/'diagnostics.csv',rows)
    summary={v:{k:float(np.mean([r[k] for r in rows if r['variant']==v])) for k in rows[0] if k not in ['seed','variant','history']} for v in ['plastic','static','shuffled']}
    (root/'DIAGNOSTICS.json').write_text(json.dumps({'status':'Exploratory post-freeze diagnostics; not additional primary tests.','summary':summary},indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('results');a=p.parse_args();main(a.results)
