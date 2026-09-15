"""AC13: acquired allocation of maintenance spending under an unreliable port.

Thin study wrapper around the AC12 harness. It declares the calibrated world from
`AC13_PROTOCOL_v1.md` (blind port space 4; yields 64 before and 12 after the
intervention; at tick 1024 the affected port begins answering on a channel drawn
per contact, so a stored value earns exactly what blind search earns) and runs the
seven declared arms. `preserve` with the register all-maintained is behaviourally
the frozen AC9 v2 organism.
"""
from pathlib import Path
import hashlib
import json
import sys
import ac12

ARMS=ac12.ARMS
PORTS=4
YIELD_M=64
YIELD_F=64
POST_YIELD_M=12
POST_YIELD_F=12
MOVE=1024
MOVE_KEYS=(1,)
MOVE_MODE='random'
TICKS=2048
DEV=512
STREAK_N=6
FIXED_PERIOD=2
RANDOM_P=0.5

NAMES=['ac13.py','ac12.py','ac12_memory.py','ac9.py','ac9_priority_v2.py','ac9_memory.py',
       'ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py',
       'test_ac13.py','AC13_PROTOCOL_v1.md']


def apply_world():
    ac12.PORTS=PORTS
    ac12.YIELD_M=YIELD_M; ac12.YIELD_F=YIELD_F
    ac12.POST_YIELD_M=POST_YIELD_M; ac12.POST_YIELD_F=POST_YIELD_F
    ac12.MOVE=MOVE; ac12.MOVE_KEYS=MOVE_KEYS; ac12.MOVE_MODE=MOVE_MODE
    ac12.DEV=DEV
    ac12.STREAK_N=STREAK_N; ac12.FIXED_PERIOD=FIXED_PERIOD; ac12.RANDOM_P=RANDOM_P


def run(seed,history,arm,ticks=TICKS):
    apply_world()
    return ac12.run(seed,history,arm,ticks=ticks)


def collect(root,seeds):
    apply_world()
    root=Path(root); root.mkdir(exist_ok=False)
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in NAMES if Path(n).exists()}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0,1):
                for arm in ARMS:
                    r=run(seed,history,arm); rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,outcomes=[
                (r['history'],r['arm'],round(r['activity'],3),r['completed'],
                 r['alloc']['dropped'],r['alloc']['relinquish_tick'])
                for r in rows[-2*len(ARMS):]])),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac13_engineering_v1',[3,4]); return
    collect('ac13_results_v1',[1600,1601,1602,1603])


if __name__=='__main__': main()
