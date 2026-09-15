"""Exact AC6 runner with one explicit exploration-probability parameter."""
from pathlib import Path
import hashlib
import inspect
import json
import numpy as np
import ac6
from ac1 import contrast

source=inspect.getsource(ac6.run)
assert source.count('def run(seed,arm,ticks=8192):')==1
assert source.count('rng.random()<1/512')==2
source=source.replace('def run(seed,arm,ticks=8192):','def run(seed,arm,ticks=8192,denominator=512):')
source=source.replace('probe=bool(rng.random()<1/512)','probe=bool(rng.random()<1/denominator)')
namespace=dict(vars(ac6)); exec(compile(source,'ac6_fixedrate_derived','exec'),namespace)
run=namespace['run']
DENOMINATORS=(512,1024,2048,4096,0)


def summarize(rows):
    baseline={r['seed']:r for r in rows if r['denominator']==0}
    result=[]
    for n in DENOMINATORS:
        g=[r for r in rows if r['denominator']==n]
        m=dict(completed=sum(r['completed'] for r in g),activity=float(np.mean([r['activity'] for r in g])),
               support_omission=float(np.mean([(r['windows'][0]['active']-r['windows'][0]['on'])/1024 for r in g])),
               support_active=float(np.mean([r['windows'][0]['active']/1024 for r in g])),
               return_on=float(np.mean([r['windows'][1]['on']/1024 for r in g])),
               support_B0=float(np.mean([r['phases'][1]['B0_birth'] for r in g])),
               material=float(np.mean([r['ledger']['spent_m'] for r in g])),
               energy=float(np.mean([r['ledger']['spent_e'] for r in g])),
               exports=float(np.mean([r['ledger']['particle_export'] for r in g])))
        c=contrast([r['ledger']['spent_m'] for r in g],[baseline[r['seed']]['ledger']['spent_m'] for r in g])
        criteria=dict(viability=m['completed']>=7 and m['activity']>=.9,
                      relinquishment=m['support_omission']>=.8 and m['support_active']>=.9,
                      reacquisition=m['return_on']>=.8,
                      local_saving=m['support_B0']<=.5*np.mean([r['phases'][1]['B0_birth'] for r in baseline.values()]),
                      structural=all(r['structural_accuracy']>=.99 for r in g if r['completed']),
                      net_material=c['mean']<0 and c['interval'][1]<0)
        result.append(dict(denominator=n,means=m,material_contrast=c,criteria=criteria))
    return result


def main():
    # Establish that parameterization preserves the frozen default runner.
    assert run(19,'local',80,512)==ac6.run(19,'local',80)
    root=Path('ac6_fixedrate_results_v1'); root.mkdir(exist_ok=False)
    names=['ac6_fixedrate.py','ac6.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py','AC6_FIXEDRATE_PROTOCOL_v1.md']
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in range(400,408):
            for n in DENOMINATORS:
                r=run(seed,'local' if n else 'frozen',8192,n or 512)
                r['denominator']=n; rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,activity={r['denominator']:r['activity'] for r in rows[-5:]})),flush=True)
    report=dict(hashes=hashes,rows=rows,summary=summarize(rows))
    (root/'results.json').write_text(json.dumps(report,indent=2)); print(json.dumps(report['summary']),flush=True)


if __name__=='__main__': main()
