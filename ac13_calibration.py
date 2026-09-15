"""AC13 calibration: does an unreliable port pose the allocation question?

AC11 and AC12 failed because the intervention zeroed the organism's income, so
starvation lapsed the entry whether or not the policy chose to relinquish it.
This script tests the repaired design: at the intervention the affected port
becomes *unreliable* (a channel drawn per contact), so a stored value earns
exactly what blind search earns -- the information is worthless but not harmful
-- and the material yield drops, so paying for worthless information competes
with the metabolism.

Calibration arm `switch` (engineering only, not a rival) maintains the affected
slot before the intervention and drops it after, giving the outcome any
experience-driven policy would have to discover. Six engineering individuals per
condition, seeds 0-2 and both developmental histories.

ENGINEERING ONLY: no final seeds, no claim. Results retained in
`ac13_calibration_v1/`.
"""
from pathlib import Path
import hashlib
import json
import ac12

SEEDS=(0,1,2)
HIST=(0,1)
GRID_Y2=(24,16,12,8)
STUDY_ARMS=('switch','allocate','protected','no_learning','fixed_schedule','random',
            'preserve','relinquish')
NAMES=['ac13_calibration.py','ac12.py','ac12_memory.py','ac9.py','ac9_priority_v2.py',
       'ac9_memory.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py']


def run_arm(arm,y1,y2):
    ac12.YIELD_M=y1; ac12.YIELD_F=y1
    ac12.POST_YIELD_M=y2; ac12.POST_YIELD_F=y2
    ac12.MOVE_MODE='random'
    return [ac12.run(seed,h,arm) for seed in SEEDS for h in HIST]


def main():
    root=Path('ac13_calibration_v1'); root.mkdir(exist_ok=False)
    (root/'pre_run_snapshot.json').write_text(json.dumps(
        {n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in NAMES if Path(n).exists()},
        indent=2))
    grid=[]; study=[]
    with (root/'rows.jsonl').open('x') as f:
        for y1 in (64,48,32):
            for y2 in GRID_Y2:
                for arm in ('switch','preserve','relinquish'):
                    for r in run_arm(arm,y1,y2):
                        r=dict(r,y1=y1,y2=y2); grid.append(r); f.write(json.dumps(r)+'\n'); f.flush()
        for y1,y2 in ((64,12),(64,8)):
            for arm in STUDY_ARMS:
                for r in run_arm(arm,y1,y2):
                    r=dict(r,y1=y1,y2=y2); study.append(r); f.write(json.dumps(r)+'\n'); f.flush()
    (root/'results.json').write_text(json.dumps(dict(kind='engineering_calibration',
                                                    grid=grid,study=study),indent=2))

    def prod(r,p):
        l=r['phases'][p]; return l['productive']/max(1,l['contacts'])
    print("calibration: which world makes the switch necessary?")
    print(f"{'Y1':>3} {'Y2':>3} | {'switch':>7} {'preserve':>9} {'relinquish':>11}")
    for y1 in (64,48,32):
        for y2 in GRID_Y2:
            cells=[]
            for arm in ('switch','preserve','relinquish'):
                s=[r for r in grid if r['y1']==y1 and r['y2']==y2 and r['arm']==arm]
                cells.append(f"{sum(x['completed'] for x in s)}/{len(s)}")
            print(f"{y1:3} {y2:3} | {cells[0]:>7} {cells[1]:>9} {cells[2]:>11}")
    for y1,y2 in ((64,12),(64,8)):
        print(f"\nstudy arms at Y1={y1} Y2={y2}:")
        print(f"{'arm':15} {'alive':>5} {'prod1':>6} {'prod2':>6} {'renWr₁':>6} {'renWr2':>6} "
              f"{'drop@':>6} {'dead@':>12}")
        for arm in STUDY_ARMS:
            s=[r for r in study if r['y1']==y1 and r['y2']==y2 and r['arm']==arm]
            d=[r['first_dead'] for r in s if r['first_dead'] is not None]
            drops=[r['alloc']['relinquish_tick'] for r in s if r['alloc']['relinquish_tick'] is not None]
            print(f"{arm:15} {sum(r['completed'] for r in s)}/{len(s):<3} "
                  f"{sum(prod(r,1) for r in s)/len(s):6.3f} {sum(prod(r,2) for r in s)/len(s):6.3f} "
                  f"{sum(r['phases'][1]['memory_writes'] for r in s)/len(s):6.0f} "
                  f"{sum(r['phases'][2]['memory_writes'] for r in s)/len(s):6.0f} "
                  f"{(sum(drops)/len(drops) if drops else -1):6.0f} "
                  f"{(f'{min(d)}..{max(d)}' if d else '-'):>12}")


if __name__=='__main__': main()
