"""AC11 feasibility confirmation (ENGINEERING ONLY).

The first feasibility grid (`ac11_feasibility_v1/`) showed that in the frozen
world a stale route is fatal while relinquishing survives, but that relinquishing
costs contact productivity when the route is still valid — so a static
"never maintain" policy is not clearly worse. This confirmation widens the seed
sample on the candidate regime (blind port space 4, material yield 16, fuel
yield 16) to check whether both static policies fail one phase reliably.

Seeds here are engineering seeds and are excluded from any later confirmatory
sample.
"""
from pathlib import Path
import hashlib
import json
import statistics
import numpy as np
import ac11_feasibility as F

CONDITIONS=[dict(maintain=m,phase2=p) for m in (True,False) for p in ('open','moved')]
SEEDS=(0,1,2,3,4,5)
WORLD=dict(ports=4,yield_m=16,yield_f=16)


def main():
    root=Path('ac11_feasibility_v2'); root.mkdir(exist_ok=False)
    names=[n for n in ('ac11_feasibility.py','ac11_feasibility_confirm.py','ac9.py',
                       'ac9_priority_v2.py','ac9_memory.py','ac5.py','ac5_program.py',
                       'ac4.py','ac4_transport.py','ac1.py') if Path(n).exists()]
    (root/'pre_run_snapshot.json').write_text(json.dumps(
        {n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names},indent=2))
    rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for cond in CONDITIONS:
            for seed in SEEDS:
                r=F.run(seed=seed,history=0,**cond,**WORLD)
                rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
    (root/'results.json').write_text(json.dumps(dict(kind='engineering_feasibility_confirm',
                                                    world=dict(WORLD),rows=rows),indent=2))
    print(f"world {WORLD}, history 0, seeds {SEEDS}, 2048 ticks (onset 512)")
    print(f"{'maintain':>8} {'phase2':>6} | {'alive/6':>7} {'mean act':>8} {'dead@':>14} "
          f"{'prod1st':>8} {'prod2nd':>8} {'in_m':>6} {'occ':>4} {'renWr':>6}")
    for cond in CONDITIONS:
        s=[r for r in rows if r['maintain']==cond['maintain'] and r['phase2']==cond['phase2']]
        alive=sum(r['completed'] for r in s)
        deaths=[r['first_dead'] for r in s if r['first_dead'] is not None]
        dd=(f"{min(deaths)}..{max(deaths)}" if deaths else '-')
        print(f"{str(cond['maintain']):>8} {cond['phase2']:>6} | {alive}/{len(s):<5} "
              f"{statistics.mean(r['activity'] for r in s):8.3f} {dd:>14} "
              f"{statistics.mean(r['total_productivity'] for r in s):8.3f} "
              f"{statistics.mean(r['late_productivity'] for r in s):8.3f} "
              f"{statistics.mean(r['ledger']['in_m'] for r in s):6.0f} "
              f"{statistics.mean(r['occupied_sites'] for r in s):4.1f} "
              f"{statistics.mean(r['ledger']['memory_writes'] for r in s):6.0f}")


if __name__=='__main__': main()
