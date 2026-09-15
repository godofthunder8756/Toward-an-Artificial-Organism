"""Instantiate AC8 with explicit disjoint repair-exclusion masks."""
from pathlib import Path
from types import FunctionType
import hashlib
import json
import numpy as np
import ac8

MASKS={'keep':[], 'selectors':[12,13,26,27], 'action_types':[10,11,24,25], 'all_routes':[10,11,12,13,24,25,26,27]}


def run(seed,condition,ticks=8192):
    if condition=='keep': r=ac8.run(seed,'keep',ticks)
    else:
        # Separate function globals; never mutate frozen module or live shared state.
        reaction_globals=dict(vars(ac8),ROUTE_BITS=np.array(MASKS[condition]))
        reaction=FunctionType(ac8.selective_react.__code__,reaction_globals)
        step_globals=dict(ac8.step.__globals__,selective_react=reaction)
        step=FunctionType(ac8.step.__code__,step_globals,argdefs=ac8.step.__defaults__)
        run_globals=dict(vars(ac8),step=step)
        runner=FunctionType(ac8.run.__code__,run_globals,argdefs=ac8.run.__defaults__)
        r=runner(seed,'block_routes',ticks)
    r['condition']=condition
    return r


def main():
    assert run(1,'all_routes',80)==dict(ac8.run(1,'block_routes',80),condition='all_routes')
    root=Path('ac8_partition_results_v1'); root.mkdir(exist_ok=False)
    names=['ac8_partition.py','ac8.py','ac7.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py','AC8_PARTITION_PROTOCOL_v1.md']
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2)); rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in range(900,908):
            for condition in MASKS:
                r=run(seed,condition); rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,activity={r['condition']:r['activity'] for r in rows[-4:]})),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))


if __name__=='__main__': main()
