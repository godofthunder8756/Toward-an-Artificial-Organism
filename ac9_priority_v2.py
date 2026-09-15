from pathlib import Path
from types import FunctionType
import hashlib
import json
import numpy as np
import ac9

ARMS=('priority','original','block0','block1','no_growth')


def acquire(seed):
    o=ac9.acquire(seed)
    rules=o.body.traces[0,:126].reshape(9,14,7).copy()
    o.body.traces[0,:126]=rules[[0,1,2,3,5,6,7,8,4]].reshape(126,7)
    return o


runner=FunctionType(ac9.run.__code__,dict(vars(ac9),acquire=acquire),argdefs=ac9.run.__defaults__)


def run(seed,history,arm,ticks=2048):
    if arm=='original': r=ac9.run(seed,history,'keep',ticks)
    else: r=runner(seed,history,'keep' if arm=='priority' else arm,ticks)
    r['variant']=arm
    return r


def main():
    for seed in range(4):
        a=acquire(seed); b=ac9.acquire(seed)
        old=b.body.traces[0,:126].reshape(9,14,7)
        new=a.body.traces[0,:126].reshape(9,14,7)
        assert sorted(x.tobytes() for x in old)==sorted(x.tobytes() for x in new)
        np.testing.assert_array_equal(old[4],new[8])
    root=Path('ac9_priority_results_v2'); root.mkdir(exist_ok=False)
    names=['ac9_priority_v2.py','ac9.py','ac9_memory.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py','AC9_PRIORITY_PROTOCOL_v2.md']
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2)); rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in range(1100,1104):
            for history in (0,1):
                for arm in ARMS:
                    r=run(seed,history,arm); rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,outcomes=[(r['history'],r['variant'],r['activity'],r['routes']) for r in rows[-10:]])),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))


if __name__=='__main__': main()
