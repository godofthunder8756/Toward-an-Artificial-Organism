"""Evaluate a saved E2 checkpoint without training or network access."""
import argparse,json
from pathlib import Path
from e2.model import Config,Network
from e2.experiment import rollout,write_csv,metrics
p=argparse.ArgumentParser();p.add_argument('--results',default='e2_results');p.add_argument('--seed',type=int,default=200)
p.add_argument('--variant',choices=['plastic','static','shuffled'],default='plastic');p.add_argument('--history',type=int,choices=[0,1],default=0)
p.add_argument('--stage',choices=['developed','normal','rescue','sham','lost','swap','frozen_weights'],default='developed')
p.add_argument('--world',type=int,default=0);p.add_argument('--out',required=True);a=p.parse_args()
r=Path(a.results);cfg=Config(**json.loads((r/'run.json').read_text())['config'])
net,b=Network.load(r/f'seed_{a.seed}_{a.variant}_h{a.history}'/f'{a.stage}.npz',cfg)
b.energy=cfg.energy_cap;b.store[:]=cfg.initial_store
mode=a.stage if a.stage in ['rescue','sham','lost','swap'] else 'normal'
rows=rollout(net,b,80000000+a.world,cfg.eval_rounds,mode,a.variant);write_csv(a.out,rows);print(json.dumps(metrics(rows),indent=2))
