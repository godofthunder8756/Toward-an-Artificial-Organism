"""AC16: can the organism *re-acquire* a correct route after the move?

Why AC15 could not see this
---------------------------
AC15's learner relinquished the stale route but never bound a correct new one: its
moved-channel productivity stayed at blind-search level (0.398 against a blind rate
near 1/2). The reason is mechanical, not behavioural. In the frozen step the deposit
path -- the only way the organism binds a new key/port entry -- is gated on `grow`:

    if grow and selected is None and e['productive']:
        ...  mem.deposit(o.memory, b, action, port, activation, w)

and the frozen runner passes `grow = t<512`. Growth stops at development, and the AC15
intervention happens at t=1024, so re-binding was switched off before the move.

This is the frozen world with that single constant changed: **the growth window is left
open** (`grow=True`). No new machinery. The frozen runner's own post-development state
is `activation=[True,True]` and `grow=(t<512)`; AC16 declares `grow=True`, which is the
frozen deposit path with a longer window, nothing else.

Why that makes the study well posed
-----------------------------------
The deposit is gated on `selected is None` -- the organism may only bind a key it does
not already hold -- and it binds the port that *just proved productive*
(`mem.deposit(memory, body, action, port, ...)`, value = the port of the successful
contact). So:

- an organism that **relinquished** the stale route eventually loses the entry
  (`life` decays once renewal stops), `read(key)` returns None, and its next productive
  contact binds a *correct* port -> re-acquisition, driven entirely by its own outcome;
- an organism that **kept** the stale entry never has `selected is None` for that key, so
  it can never bind anything -> it is barred from re-acquiring by construction.

That makes `preserve` and the sham-write arm (`no_learning`, which pays for the
relinquishment without writing it) the causal controls, and no separate scaffold is
needed: the frozen gate supplies the control.
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
from ac1 import decode

TICKS=4096               # longer than the lineage standard: the entry must lapse and a
                         # productive contact must follow before re-binding is possible
MOVE=1024                # the asymmetric intervention (material channel moves)
DEV=512                  # development window for the *frozen* scheduling
WINDOWS=8                # report per-channel productivity per eighth of the post-move run

ARMS=('allocate','preserve','relinquish','random','fixed_schedule','no_learning',
      'fixed_period_1','streak_never','allocate_restore','restore_disabled')

RESTORE=True   # module switch so the two-way arm's own control can be run with the
               # restore rule disabled: that configuration must reproduce the one-way
               # `allocate` arm exactly


class AllocRestore(ac12.Alloc):
    """Two-way outcome-driven allocation.

    One-way relinquishment cannot *hold* a re-acquired route: once the register bit is
    set the slot is never renewed again, so an entry re-bound from a productive contact
    (measured: `allocate` binds a correct port at t=1146) lapses again within its 64-tick
    life, and productivity stays at the intermediate level of a route that is live only
    part of the time. The symmetric rule is to restore maintenance when the route proves
    right.

    The thresholds are deliberately asymmetric, and that is sound rather than a fudge: a
    productive contact on a stored port is *proof* the port is right (the frozen gate can
    only be passed by a match, and the deposit binds exactly the port that matched),
    whereas an unproductive contact is one noisy observation, which is why the drop rule
    requires a streak. Both writes are paid per replica and land in the same vulnerable
    program bank as the drop, so this is not free state.
    """

    def outcome(self,o,key,e):
        if self.arm not in ('allocate',): return
        key=int(key)
        if e['productive']>0:
            if RESTORE: self._restore(o,e,key)
            self.streak[key]=0
            return
        self.streak[key]=self.streak.get(key,0)+1
        if self.streak[key]>=ac12.STREAK_N: self._drop(o,e,key)

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


def run(seed,history,arm,ticks=TICKS,move=MOVE,grow_after_dev=True):
    """The AC15 world, driven with the growth window left open."""
    ac15.set_world()
    ac12.DEV=DEV
    for k,v in ac15.DEFAULTS.items(): setattr(ac12,k,v)
    base=arm
    if arm in ac15.ARM_CONFIG:
        base,kw=ac15.ARM_CONFIG[arm]
        # arm-specific constants must be applied AFTER the defaults, or a default reset
        # silently clobbers them (this ordering bug made `streak_never` run with the
        # learner's threshold and score as the learner instead of as `preserve`)
        for k,v in kw.items(): setattr(ac12,k,v)
    ac15._misses[0]=0
    ac15._chan[0]=[0,0]; ac15._chan[1]=[0,0]
    base_map=(seed%2,(seed//2)%2)
    true_after=tuple(1-c if a in ac15.MOVE_ACTIONS else c for a,c in enumerate(base_map))
    if arm in ('allocate_restore','restore_disabled'):
        base='allocate'
        globals()['RESTORE']=(arm=='allocate_restore')
        alloc=AllocRestore('allocate',seed,history)
    else:
        globals()['RESTORE']=True
        alloc=ac12.Alloc(base,seed,history)
    o,offs=ac12.acquire(seed)
    alloc.offs=offs; alloc.shadow=o.body.traces[0].copy()
    step=ac15.build(base,alloc)
    rng=np.random.default_rng([seed,1509])
    total=ac9.event()
    # per-window per-channel [attempts, matches] over the post-move run
    win=[[[0,0],[0,0]] for _ in range(WINDOWS)]
    bound_at=None            # first tick at/after the move with a *correct* stored entry
    stale_at=None            # first tick with a stored entry for the moved key (either value)
    for t in range(ticks):
        alloc.now=t
        mapping=base_map
        if t>=move: mapping=true_after
        core=(rng.random((126,7))<.0001).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8)
        coin=bool(rng.random()<.5)
        activation=[True,True]                     # the frozen runner's post-dev state
        grow=True if grow_after_dev else (t<DEV)   # AC16's single declared change
        e=step(o,core,noise,directions,coin,mapping,activation,grow)
        for k in total: total[k]+=e.get(k,0)
        if t>=move:
            if stale_at is None and o.memory.read(1) is not None: stale_at=t
            if bound_at is None and o.memory.read(1)==mapping[1]: bound_at=t
            w=min(WINDOWS-1,(t-move)*WINDOWS//max(1,ticks-move))
            for a in (0,1):
                win[w][a][0], win[w][a][1] = ac15._chan[a][0], ac15._chan[a][1]
        if o.body.dead: break
    # convert cumulative counters to per-window values
    prev=[[0,0],[0,0]]; per_window=[]
    for w in range(WINDOWS):
        row=[]
        for a in (0,1):
            n=win[w][a][0]-prev[a][0]; m=win[w][a][1]-prev[a][1]
            row.append(dict(attempts=n,matches=m,productivity=(m/n if n else None)))
        per_window.append(row); prev=[[win[w][0][0],win[w][0][1]],[win[w][1][0],win[w][1][1]]]
    last=per_window[-1]
    overall_last=[[0,0],[0,0]]
    for a in (0,1):
        overall_last[a][0]=win[-1][a][0]; overall_last[a][1]=win[-1][a][1]
    return dict(seed=seed,history=history,arm=arm,ticks=ticks,move=move,
                grow_after_dev=grow_after_dev,move_actions=list(ac15.MOVE_ACTIONS),
                reacquired_at=bound_at,stored_after_move_at=stale_at,
                per_window=per_window,
                productivity_kept=per_window[-1][0]['productivity'],
                productivity_moved=per_window[-1][1]['productivity'],
                mean_chan_productivity=((per_window[-1][0]['productivity'] or 0)
                                        +(per_window[-1][1]['productivity'] or 0))/2,
                final_routes=[o.memory.read(0),o.memory.read(1)],
                final_mapping=list(mapping),
                route_correct_moved=bool(o.memory.read(1)==mapping[1]),
                activity=total['active']/ticks,completed=total['active']==ticks,
                relinquishments=len(alloc.log['dropped']),
                restorations=len(alloc.log.get('restored',[])),
                demand=o.memory.demand().tolist(),
                ledger=total,state_hash=o.digest())


NAMES=['ac16.py','ac15.py','ac12.py','ac12_memory.py','ac9.py','ac9_priority_v2.py',
       'ac9_memory.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py',
       'test_ac16.py','AC16_PROTOCOL_v1.md']


def collect(root,seeds,ticks=TICKS,move=MOVE,grow_after_dev=True):
    root=Path(root); root.mkdir(exist_ok=False)
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in NAMES if Path(n).exists()}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0,1):
                for arm in ARMS:
                    r=run(seed,history,arm,ticks=ticks,move=move,grow_after_dev=grow_after_dev)
                    rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps([(r['history'],r['arm'],round(r['activity'],3),r['completed'],
                               (round(r['productivity_moved'],3) if r['productivity_moved'] is not None else None),
                               r['reacquired_at'],r['route_correct_moved'])
                              for r in rows[-2*len(ARMS):]]),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac16_engineering_v1',[0,1,2]); return
    collect('ac16_results_v1',[2100,2101,2102,2103])


if __name__=='__main__': main()
