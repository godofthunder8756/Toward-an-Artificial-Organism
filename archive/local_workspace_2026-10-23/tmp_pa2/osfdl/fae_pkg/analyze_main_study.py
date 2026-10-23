"""Frozen-design completeness audit and seed-paired primary analysis."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t

def encode(x): return json.dumps(x,sort_keys=True,allow_nan=False,separators=(',',':'))
def digest(x): return hashlib.sha256(x).hexdigest()
def primary(rows,metric='regulation_loss'):
    pivot=rows.pivot(index=['seed','layout','arm'],columns='condition',values=metric)
    changes=(pivot['bias']-pivot['clean']).unstack('arm')
    values=(changes['coupled']-changes['preference']).groupby('seed').mean()
    n=len(values);mean=float(values.mean())
    half=float(t.ppf(.975,n-1)*values.std(ddof=1)/np.sqrt(n)) if n>1 else None
    return values,dict(seed_count=n,mean=mean,ci95=None if half is None else [mean-half,mean+half],
        positive_direction='greater bias-induced loss for coupled than preference')

def analyze(folder):
    design=json.loads((folder/'design.json').read_text())
    design_id=digest(encode(design).encode())
    expected={f"{layout['layout_id']}__{arm}__{seed}__{condition}"
        for layout in design['layouts'] for arm in design['arms']
        for seed in design['seeds'] for condition in design['conditions']}
    files={f.name.removesuffix('.json.gz'):f for f in (folder/'episodes').glob('*.json.gz')}
    if set(files)!=expected:
        raise ValueError(f'Incomplete or unexpected trial set: {len(expected-set(files))} missing, {len(set(files)-expected)} extra. No complete-study inference generated.')
    rows=[];step_count=0
    for ident in sorted(expected):
        with gzip.open(files[ident],'rt',encoding='utf-8') as f: record=json.load(f)
        assert record['id']==ident and record['design_id']==design_id
        payload=record['payload'];assert digest(encode(payload).encode())==record['payload_sha256']
        s=payload['summary'];records=payload['records']
        assert ident==f"{s['layout']}__{s['arm']}__{s['seed']}__{s['condition']}"
        assert len(records)==s['steps'] and 1<=len(records)<=40
        for i,r in enumerate(records):
            step_count+=1
            assert r['t']==r['sample_t']==i
            raw=np.asarray(r['raw_sensor']);sensed=np.asarray(r['received_sensor'])
            eligible=5<=i<15 and 1<=raw[1]<=4
            assert r['eligible']==eligible
            assert np.array_equal(raw[[0,2,3]],sensed[[0,2,3]])
            delta=int(sensed[1]-raw[1])
            assert r['intended_delta']==r['realized_delta']==delta
            assert abs(delta)==int(eligible and s['condition']!='clean')
            if s['condition']=='bias': assert delta>=0
            assert np.all((0<=sensed)&(sensed<=5))
            actual_loss=float(np.mean(1-np.asarray(r['truth_after'][:2])/15))
            assert np.isclose(actual_loss,r['regulation_loss'])
            if i+1<len(records): assert r['truth_after']==records[i+1]['truth']
        observed=sum(r['regulation_loss'] for r in records)
        assert np.isclose(s['regulation_loss'],(observed+40-len(records))/40)
        assert np.isclose(s['terminal_hold_loss'],(observed+(40-len(records))*records[-1]['regulation_loss'])/40)
        assert s['eligible_steps']==sum(r['eligible'] for r in records)
        assert s['survived']==int(not records[-1]['terminated'])
        rows.append(s)
    df=pd.DataFrame(rows)
    values,result=primary(df)
    _,sensitivity=primary(df,'terminal_hold_loss')
    result.update(mode=design['mode'],episodes=len(rows),recorded_steps=step_count,
        terminal_hold_sensitivity=sensitivity,
        interpretation='Development preflight only; no confirmatory conclusion.' if design['mode']=='preflight' else 'Primary estimate over simulation seeds on the fixed 12-layout bank.')
    df.to_csv(folder/'audited-episodes.csv',index=False)
    values.to_csv(folder/'primary-seed-contrasts.csv',header=['contrast'])
    df.groupby(['layout','arm','condition']).agg(episodes=('survived','size'),survivors=('survived','sum'),
        mean_loss=('regulation_loss','mean'),mean_steps=('steps','mean'),mean_exposure=('eligible_steps','mean')).to_csv(folder/'layout-summaries.csv')
    (folder/'analysis.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (folder/'audit.json').write_text(json.dumps(dict(status='passed',episodes=len(rows),recorded_steps=step_count),indent=2))
    return result

def self_test():
    rows=[]
    for seed in range(8):
        for layout in ['a','b']:
            for arm in ['uniform','coupled','preference']:
                for condition in ['clean','bias','noise']:
                    effect={'uniform':0.,'coupled':.15,'preference':.10}[arm] if condition=='bias' else 0.
                    rows.append(dict(seed=seed,layout=layout,arm=arm,condition=condition,regulation_loss=.2+effect))
    values,result=primary(pd.DataFrame(rows))
    assert np.allclose(values,.05) and np.isclose(result['mean'],.05)
    print('Synthetic primary-estimator test passed: known contrast 0.05 recovered.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path,nargs='?');parser.add_argument('--self-test',action='store_true');opt=parser.parse_args()
    if opt.self_test: self_test()
    elif opt.folder is not None: print(json.dumps(analyze(opt.folder),indent=2))
    else: parser.error('Supply a run folder or --self-test.')
