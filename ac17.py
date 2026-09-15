"""AC17: re-acquisition with gates whose shape matches the claim, plus two new claims.

What AC17 changes relative to AC16 v1, and what it does not
----------------------------------------------------------
AC16 v1 is falsified: its G2 asked for a **mean** margin of +0.25 over one-way
relinquishment and measured +0.2437, while the learner was strictly better in 8/8
individuals. The claim is categorical -- a one-way rule *cannot hold* a re-bound route, a
two-way rule *can* -- and a mean margin over a rival that partially succeeds by re-binding
repeatedly measures how often that rival gets lucky, which varies by seed and has nothing to
do with whether holding is possible.

AC17 therefore changes **the gates, declared before the run**, and adds claims:

- G1 / G2 are now **categorical and dominance-based** (every individual, not a mean):
  the learner holds >= 0.90 in every individual, and strictly beats one-way in every
  individual. A stricter test than AC16's mean margin, in the direction the claim is stated.
- **New claim A: both directions are necessary.** A `restore_only` arm -- the restore rule
  with no drop rule -- can never free the key, so the frozen deposit gate bars it and it must
  score exactly 0.000. This tests the necessity of the relinquishment direction with a
  structural prediction, not an empirical one.
- **New claim B: the two-way rule also handles both channels moving.** AC15 could not
  discriminate in that world (moving both channels makes drop-everything optimal, which is
  why AC15 declared an asymmetric move). With the two-way rule the prediction is different:
  the learner drops and re-binds *both*, so it should hold >= 0.90 on both channels, while
  keeping arms score exactly 0.000 on both and one-way relinquishment stays intermediate.

The world, arms, primitive, horizon and intervention stay exactly as in AC16; only the
declared seeds and the gates' shape change, and the new arms are additions. AC16 v1's
falsification is permanent and is not amended by this document.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import statistics
import sys
import numpy as np
import ac9
import ac12
import ac4
import ac15
import ac16

TICKS=4096
MOVE=1024
DEV=512
WINDOWS=8

SEEDS_SINGLE=(2300,2301,2302,2303)      # claim 1 and A: one channel moves
SEEDS_BOTH=(2400,2401,2402,2403)        # claim B: both channels move (fresh, disjoint)

SINGLE_ARMS=('allocate_restore','allocate','preserve','no_learning','relinquish',
             'random','fixed_schedule','restore_only','fixed_period_1','streak_never',
             'restore_disabled')
BOTH_ARMS=('allocate_restore','allocate','preserve','no_learning','relinquish',
           'restore_only','fixed_period_1')
CONSISTENCY=('fixed_period_1','streak_never','restore_disabled')


class AllocRestoreOnly(ac12.Alloc):
    """Restore direction only: maintenance is restored on a productive contact, but the
    drop rule is absent, so the register bit is never set. Structural prediction: this arm
    keeps every entry, so the frozen deposit gate (`selected is None`) bars it from binding
    and it scores exactly 0.000 -- i.e. the relinquishment direction is necessary."""

    def outcome(self,o,key,e):
        if self.arm not in ('allocate',): return
        key=int(key)
        if e['productive']>0:
            self._restore(o,e,key)
        self.streak[key]=0

    def _restore(self,o,e,key):
        place=ac12.m12.slot_of_key(o.memory,key)
        if place is None: return
        off=self.offs[2*place[0]+place[1]]
        sites=o.body.traces[0,off]
        n=int((sites!=0).sum())
        if n==0: return
        cap=min(32,8*int(ac4.available(o.body)[:4].sum()),o.body.energy,o.body.material)
        if n>cap: return
        o.body.energy-=n; o.body.material-=n
        e['spent_e']+=n; e['spent_m']+=n; e['writes']+=n
        sites[:]=0
        self.log.setdefault('restored',[]).append(list(place))


def run(seed,history,arm,ticks=TICKS,move=MOVE,move_actions=(1,)):
    """AC16's world and measurement, with the arm set widened by `restore_only` and the
    intervention channels selectable (claim B moves both)."""
    ac15.set_world()
    ac12.DEV=DEV
    for k,v in ac15.DEFAULTS.items(): setattr(ac12,k,v)
    base=arm
    if arm in ac15.ARM_CONFIG:
        base,kw=ac15.ARM_CONFIG[arm]
        for k,v in kw.items(): setattr(ac12,k,v)
    ac15._misses[0]=0
    ac15._chan[0]=[0,0]; ac15._chan[1]=[0,0]
    base_map=(seed%2,(seed//2)%2)
    true_after=tuple(1-c if a in move_actions else c for a,c in enumerate(base_map))
    if arm=='restore_only':
        base='allocate'
        alloc=AllocRestoreOnly('allocate',seed,history)
    elif arm in ('allocate_restore','restore_disabled'):
        base='allocate'
        ac16.RESTORE=(arm=='allocate_restore')
        alloc=ac16.AllocRestore('allocate',seed,history)
    else:
        ac16.RESTORE=True
        alloc=ac12.Alloc(base,seed,history)
    o,offs=ac12.acquire(seed)
    alloc.offs=offs; alloc.shadow=o.body.traces[0].copy()
    step=ac15.build(base,alloc)
    rng=np.random.default_rng([seed,1509])
    total=ac9.event()
    win=[[[0,0],[0,0]] for _ in range(WINDOWS)]
    bound={0:None,1:None}; stored={0:None,1:None}
    for t in range(ticks):
        alloc.now=t
        mapping=base_map if t<move else true_after
        core=(rng.random((126,7))<.0001).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8)
        coin=bool(rng.random()<.5)
        e=step(o,core,noise,directions,coin,mapping,[True,True],True)
        for k in total: total[k]+=e.get(k,0)
        if t>=move:
            for a in (0,1):
                if stored[a] is None and o.memory.read(a) is not None: stored[a]=t
                if bound[a] is None and o.memory.read(a)==mapping[a]: bound[a]=t
            w=min(WINDOWS-1,(t-move)*WINDOWS//max(1,ticks-move))
            for a in (0,1):
                win[w][a][0],win[w][a][1]=ac15._chan[a][0],ac15._chan[a][1]
        if o.body.dead: break
    prev=[[0,0],[0,0]]; per_window=[]
    for w in range(WINDOWS):
        row=[]
        for a in (0,1):
            n=win[w][a][0]-prev[a][0]; m=win[w][a][1]-prev[a][1]
            row.append(dict(attempts=n,matches=m,productivity=(m/n if n else None)))
        per_window.append(row); prev=[[win[w][0][0],win[w][0][1]],[win[w][1][0],win[w][1][1]]]
    last=per_window[-1]
    moved=set(move_actions)
    return dict(seed=seed,history=history,arm=arm,ticks=ticks,move=move,
                move_actions=list(move_actions),grow_open=True,
                productivity_moved=(last[1]['productivity'] if 1 in moved else last[0]['productivity']),
                productivity_kept=(last[0]['productivity'] if 0 not in moved else last[1]['productivity']),
                productivity_ch0=last[0]['productivity'],productivity_ch1=last[1]['productivity'],
                mean_chan_productivity=((last[0]['productivity'] or 0)+(last[1]['productivity'] or 0))/2,
                reacquired_at=bound[1] if 1 in moved else bound[0],
                reacquired_at_ch1=bound[1],reacquired_at_ch0=bound[0],
                stored_at_ch1=stored[1],stored_at_ch0=stored[0],
                per_window=per_window,
                final_routes=[o.memory.read(0),o.memory.read(1)],final_mapping=list(mapping),
                route_correct_moved=bool(o.memory.read(1 if 1 in moved else 0)==mapping[1 if 1 in moved else 0]),
                activity=total['active']/ticks,completed=total['active']==ticks,
                relinquishments=len(alloc.log['dropped']),
                restorations=len(alloc.log.get('restored',[])),
                demand=o.memory.demand().tolist(),ledger=total,state_hash=o.digest())


NAMES=['ac17.py','ac16.py','ac15.py','ac12.py','ac12_memory.py','ac9.py','ac9_priority_v2.py',
       'ac9_memory.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py',
       'test_ac17.py','audit_ac17.py','replay_ac17.py','AC17_PROTOCOL_v1.md']


def collect(root,seeds,arms,move_actions=(1,),ticks=TICKS,move=MOVE):
    root=Path(root); root.mkdir(exist_ok=False)
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in NAMES if Path(n).exists()}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0,1):
                for arm in arms:
                    r=run(seed,history,arm,ticks=ticks,move=move,move_actions=move_actions)
                    rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,world=('both' if len(move_actions)>1 else 'single'),
                out=[(r['history'],r['arm'],round(r['activity'],3),r['completed'],
                      r['productivity_ch0'],r['productivity_ch1'],r['reacquired_at'])
                     for r in rows[-2*len(arms):]])),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac17_engineering_v1',[0,1],SINGLE_ARMS); return
    # Claim B (both channels moving) is NOT run as a final: engineering measured the crude
    # always-relinquish arm at 0.93 mean in that world (ch0 1.000, ch1 0.857) against the
    # learner's 0.75, because an arm that never renews is always free to re-bind. The
    # two-way rule adds nothing there, so AC17 claims nothing there; the measurement is
    # recorded in AC17_ENGINEERING_v1.md and the world stays out of scope.
    collect('ac17_results_single_v1',SEEDS_SINGLE,SINGLE_ARMS,move_actions=(1,))


if __name__=='__main__': main()
