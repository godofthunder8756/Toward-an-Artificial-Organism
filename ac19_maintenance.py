"""AC19-M: diagnosing the maintenance half -- why do the register-cut arms die?

The open item
-------------
AC19 (exploratory) demonstrated the PROPAGATION half: with persistent corruption of a decision bit,
a live two-way arm kept 0.68 of its sites against 0.97 for a protected arm, so corruption propagates
through the register. The MAINTENANCE half was left unshown: both register-cut arms died (0/4) and the
route was never identified. The record says the next measurement is

    register-cut vs register-cut with flip events suppressed

which is what this script does, plus the same cut under a protected arm, so the cause is either named
or excluded rather than guessed.

Diagnostic only. No protocol, no final seeds, no claim -- and nothing here is frozen.
"""
import json
import numpy as np
import ac19

ARMS=ac19.ARMS
SEEDS=(0,1,2,3)


def survey(**kwargs):
    out={}
    for arm in ARMS:
        alive=0; finals=[]
        for seed in SEEDS:
            r=ac19.run(seed,0,arm,**kwargs)
            alive+=int(bool(r.get('completed',False)))
            for key in ('sites','final_sites','particles'):
                if key in r: finals.append(r[key]); break
        out[arm]=dict(alive=alive,n=len(SEEDS),
                      mean_final=(float(np.mean(finals)) if finals else None))
    return out


if __name__=='__main__':
    print(__doc__)
    probe=ac19.run(0,0,ARMS[0])
    print('run() returns keys:',sorted(probe.keys()))
    print('\n--- 1. the study configuration (corruption on) ---')
    full=survey()
    for arm,v in full.items():
        print(f'  {arm:28s} alive {v["alive"]}/{v["n"]}  mean final '
              f'{v["mean_final"] if v["mean_final"] is None else round(v["mean_final"],2)}')

    print('\n--- 2. flip events suppressed (register damage rate 0) ---')
    quiet=survey(reg_rate=0.0)
    for arm,v in quiet.items():
        print(f'  {arm:28s} alive {v["alive"]}/{v["n"]}  mean final '
              f'{v["mean_final"] if v["mean_final"] is None else round(v["mean_final"],2)}')

    print('\n--- 3. the verdict ---')
    cut=[a for a in ARMS if 'no_repair' in a]
    rescued=[a for a in cut if quiet[a]['alive']>full[a]['alive']]
    print(f'  cut arms: {cut}')
    print(f'  cut arms rescued by suppressing the corruption: {rescued}')
    print(f'  -> the dying route is {"the corruption itself" if rescued else "NOT the corruption"}')
    json.dump(dict(full=full,quiet=quiet,rescued=rescued),
              open('/tmp/ac19_maintenance.json','w'),indent=2)
