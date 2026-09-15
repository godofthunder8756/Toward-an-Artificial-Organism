"""AC18: confirmatory replication with the minima-separation gate (see AC18_PROTOCOL_v1.md).

The world, arms, horizon, intervention, primitive and simulation are the frozen AC17 ones:
`ac17.run` is imported and not modified. AC18 supplies a fresh seed family and its own
frozen table, so the declared gate is evaluated on data it has never seen.
"""
from pathlib import Path
import hashlib
import json
import sys
import ac17

ARMS=ac17.SINGLE_ARMS
SEEDS=(2500,2501,2502,2503)
BAR=0.90        # the claim's bar: the learner's WORST individual must clear it and one-way's
                # WORST must not (see AC18_PROTOCOL_v1.md for why the gate takes this shape)
NAMES=['ac18.py','ac17.py','ac16.py','ac15.py','ac12.py','ac12_memory.py','ac9.py',
       'ac9_priority_v2.py','ac9_memory.py','ac5.py','ac5_program.py','ac4.py',
       'ac4_transport.py','ac1.py','test_ac18.py','audit_ac18.py','replay_ac18.py',
       'AC18_PROTOCOL_v1.md']


def run(seed,history,arm,**kw):
    return ac17.run(seed,history,arm,move_actions=(1,),**kw)


def collect(root,seeds,arms=ARMS):
    root=Path(root); root.mkdir(exist_ok=False)
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in NAMES if Path(n).exists()}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0,1):
                for arm in arms:
                    r=run(seed,history,arm)
                    rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,out=[
                (r['history'],r['arm'],round(r['activity'],3),r['completed'],
                 r['productivity_ch0'],r['productivity_ch1'],r['reacquired_at'])
                for r in rows[-2*len(arms):]])),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac18_engineering_v1',[2500],ARMS); return
    collect('ac18_results_v1',SEEDS)


if __name__=='__main__': main()
