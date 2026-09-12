"""Frozen-source, complete-data, ledger, and saved-policy replay audit."""
import argparse,csv,json,hashlib,copy
from pathlib import Path
import numpy as np
from e2.model import Config,Network
from e2.experiment import rollout

def verify(root):
    root=Path(root);run=json.loads((root/'run.json').read_text());cfg=Config(**run['config']);base=Path(__file__).resolve().parent
    freeze=json.loads((base/'E2_FREEZE.json').read_text())['sources'];checks={}
    checks['frozen_sources']=all(hashlib.sha256((base/k).read_bytes()).hexdigest()==v for k,v in freeze.items())
    data=list(csv.DictReader(open(root/'evaluation.csv')));expected=cfg.seeds*len(run['variants'])*2*16*cfg.eval_worlds
    keys=[(r['seed'],r['variant'],r['history'],r['stage'],r['world']) for r in data]
    checks['evaluation_coverage']=len(data)==expected and len(set(keys))==expected
    checks['seed_coverage']=sorted({int(r['seed']) for r in data})==list(range(cfg.seed_start,cfg.seed_start+cfg.seeds))
    max_error=0.;training_rows=0;train_resets=0
    for p in root.glob('seed_*/*.csv'):
        if not (p.name.endswith('_adaptation.csv') or p.name=='development.csv'):continue
        with open(p) as f:
            rows=csv.DictReader(f);last=None
            for r in rows:
                training_rows+=1;max_error=max(max_error,float(r['balance_error']));last=r
            if last:train_resets+=int(last['resets'])
    expected_training=cfg.seeds*len(run['variants'])*2*(cfg.rounds+6*cfg.branch_rounds)
    checks['training_coverage']=training_rows==expected_training
    checks['material_ledger']=max_error<1e-12
    replays=[]
    for v in run['variants']:
        for h in [0,1]:
            d=root/f'seed_{cfg.seed_start}_{v}_h{h}'
            for stage in ['developed','normal','rescue','sham','lost','swap','frozen_weights']:
                net,b=Network.load(d/f'{stage}.npz',cfg);b.energy=cfg.energy_cap;b.store[:]=cfg.initial_store
                mode=stage if stage in ['rescue','sham','lost','swap'] else 'normal'
                rows=rollout(net,b,80000000,cfg.eval_rounds,mode,v)
                saved=list(csv.DictReader(open(d/f'{stage}_trace.csv')))
                exact=len(rows)==len(saved) and all(all(float(r[k])==float(s[k]) for k in r) for r,s in zip(rows,saved))
                replays.append(dict(variant=v,history=h,stage=stage,exact=exact))
    checks['saved_checkpoint_replays']=all(r['exact'] for r in replays)
    output=dict(checks=checks,evaluation_rows=len(data),expected_evaluation_rows=expected,
        training_rows=training_rows,expected_training_rows=expected_training,max_training_ledger_error=max_error,replays=replays)
    (root/'VALIDATION.json').write_text(json.dumps(output,indent=2));print(json.dumps({k:v for k,v in output.items() if k!='replays'},indent=2))
    if not all(checks.values()):raise SystemExit('Validation failed')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('results');a=p.parse_args();verify(a.results)
