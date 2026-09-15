from pathlib import Path
import hashlib
import json
import numpy as np
import ac4
from ac1 import contrast

ARMS=('self','no_policy_write','protected','no_B_retention')
ROOT=Path('ac4_followup_results_v1')


def summarize(rows):
    summaries=[]
    for p in (.00005,.0001):
        g={a:[r for r in rows if r['p']==p and r['arm']==a] for a in ARMS}
        means={a:dict(activity=float(np.mean([r['activity'] for r in v])),
                      completed=sum(r['completed'] for r in v),
                      policy_accuracy=float(np.mean([r['policy_accuracy'] for r in v])),
                      functional_policy=float(np.mean([r['policy_accuracy']*r['completed'] for r in v]))) for a,v in g.items()}
        delta=[x['activity']-y['activity'] for x,y in zip(g['self'],g['no_policy_write'])]
        c=contrast(delta,np.zeros(len(delta)))
        criteria=dict(self_viable=means['self']['activity']>=.9,
                      self_information=means['self']['policy_accuracy']>=.99,
                      protected_viable=means['protected']['activity']>=.9,
                      repair_dependence=c['mean']>=.2 and c['interval'][0]>0)
        summaries.append(dict(p=p,means=means,contrast=c,criteria=criteria))
    return summaries


def main():
    ROOT.mkdir(exist_ok=False)
    names=['ac4.py','ac4_transport.py','ac1.py','test_ac4.py','ac4_followup.py','AC4_FOLLOWUP_PROTOCOL_v1.md']
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}
    (ROOT/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (ROOT/'rows.jsonl').open('x') as f:
        for p in (.00005,.0001):
            for seed in range(100,108):
                for arm in ARMS:
                    row=ac4.run(seed,p,arm,8192); rows.append(row)
                    f.write(json.dumps(row)+'\n'); f.flush()
                print(json.dumps(dict(p=p,seed=seed,activity={r['arm']:r['activity'] for r in rows[-4:]})),flush=True)
    report=dict(hashes=hashes,rows=rows,summary=summarize(rows))
    (ROOT/'results.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report['summary']),flush=True)


if __name__=='__main__': main()
