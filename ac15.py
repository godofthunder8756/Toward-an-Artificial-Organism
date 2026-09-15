"""AC15: graded access law -- a wrong port costs a fraction of the yield, not all of it.

The wall the whole AC11->AC13 allocation line hit
-------------------------------------------------
Every failure in that line had one shape: an entry whose target has moved yields
**exactly zero** income, because the frozen contact is a hard gate
(`if port==mapping[action]`). Starvation then stops the renewal spending whether or
not the policy chose to relinquish the entry, so the decision is downstream of an
economics that already fixed the outcome -- `allocate` came out indistinguishable
from `preserve`, and AC13's apparent 41% saving did not replicate.

The graded law
--------------
Keep the frozen gate for a *match*: a correct stored port earns the full yield.
On a *miss*, take a fraction of the yield instead of nothing. The fraction is
declared, not tuned: a quarter of the channel's full amount.

    material channel: full 64, graded miss 16
    fuel channel:     full 32, graded miss 8

This needs no change to any conservation law: the frozen `ac4.balance` already
carries intake as a variable (`b.material == M + e['in_m'] - e['overflow_m'] -
e['spent_m']`), so a smaller intake with the overflow term computed the same way
satisfies the identity by construction.

The incentive structure it creates (measured, action forced, entry inside its 64-tick life)
-----------------------------------------------------------------------------------------
The blind fallback is **not** a uniform draw over the port space: the frozen step guesses
with a single coin, `port=int(coin)`, so a blind attempt matches with probability ~1/2.
Measured yield per contact attempt:

    stored port     frozen law      graded law
    correct             64              64
    stale (kept)         0              16
    blind (dropped)   26.7              36.0

So dropping a stale route **improves** per-contact yield from 16 to 36 (2.25x) and is
**not required for survival** (16 leaves the organism able to fund its reduced
metabolism). Under the frozen law the same decision is between 0 and 26.7 — the organism
dies if it keeps the entry, so the decision is forced and carries no information. That
pair of properties is what the allocation line needed and never had.

Wrinkle for any protocol: an entry expires after 64 ticks, so a "stored port" condition
decays to blind search if it is not renewed. Measure inside the life window, or renew.

GRADE=0 must reproduce the frozen world byte for byte -- on a miss the frozen branch
is exactly `b.energy-=1; e['active']=1; e['spent_e']+=1`, which is what this module
does before any intake. That equivalence is the test that the surgery is a no-op at
GRADE=0.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import numpy as np
import ac9
import ac12
import ac4
from ac1 import decode

GRADE=1                  # 1 = graded access law; 0 = the frozen hard gate
FULL_M, FULL_F = 64, 32  # frozen full yields
GRADE_M, GRADE_F = 16, 8 # declared fractional yield on a miss (a quarter)
PORTS=4
DEV=512
TICKS=2048
MOVE=1024                # post-development intervention: the true channel moves
# Which channels move. Moving BOTH makes "drop everything" optimal and so cannot
# discriminate an outcome-driven learner from a state-blind one: with both routes stale,
# always-relinquish wins on productivity (0.560 vs the learner's 0.294 in the first
# grid). Moving ONE channel makes the two blind extremes wrong in opposite directions --
# keep-both is wrong about the stale route, drop-both is wrong about the valid one -- so
# only a decision driven by the organism's own outcomes can get both right.
MOVE_ACTIONS=(1,)        # action 0 = fuel channel, 1 = material channel
ARMS=('allocate','preserve','relinquish','random','fixed_schedule','no_learning',
      'fixed_period_1','streak_never')

# arm -> (base arm, module constants to set for that arm). The last two are the G3
# consistency checks from AC15_PROTOCOL_v1.md: duty 1/1 and an unreachable streak must
# each reproduce `preserve` exactly, including the final state hash.
ARM_CONFIG={
    'fixed_period_1':('fixed_schedule',{'FIXED_PERIOD':1}),
    'streak_never':('allocate',{'STREAK_N':10**6}),
}
DEFAULTS={'FIXED_PERIOD':2,'RANDOM_P':0.5,'STREAK_N':6}
FINALS=(1900,1901,1902,1903)

# the frozen contact gate (two lines: the gate and its else-clause), and the line that
# derives productivity from intake
GATE_BLOCK=("            if port==mapping[action]: ac4.react(b,action,'self',e)\n"
            "            else: b.energy-=1; e['active']=1; e['spent_e']+=1")
GATED_BLOCK="            grade.contact(b,action,port,mapping[action],e)"
PRODUCTIVE_LINE="            e['contacts']=1; e['productive']=int(e['in_m']+e['in_f']>0)"
CONTACTS_LINE="            e['contacts']=1"

_misses=[0]              # per-run miss counter, reset by run()
_chan={0:[0,0],1:[0,0]}  # per-channel [attempts, matches], reset by run(): the
                         # discriminator, since an asymmetric move makes one route stale
                         # and leaves the other valid


def make_contact(react):
    """Build the contact primitive over the *world's* react.

    It must close over the shimmed react rather than the `ac4` module: the world's
    react is where the frozen yield constants are expressed, and calling the module's
    unshimmed `ac4.react` silently reinstates the frozen yields. That mistake produced
    a 31-unit material divergence at GRADE=0 and was caught by this equivalence test.
    """
    def contact(b,action,port,true,e):
        """One contact. A match runs the world's reaction; a miss pays the action's cost
        and, under the graded law, takes the declared fraction of the yield.

        Productivity is owned here and is defined by the **match**, not by intake: in
        the frozen world the two are equivalent (a miss yields nothing), and keeping it
        as "the target was right" is what preserves the allocation signal in a graded
        world. Deriving it from intake instead would make every stale route count as
        productive on every tick, so the relinquishment rule could never fire.
        """
        if port==true:
            react(b,action,'self',e)
            e['productive']=int(e['in_m']+e['in_f']>0)
            if action in (0,1): _chan[action][0]+=1; _chan[action][1]+=1
            return
        b.energy-=1; e['spent_e']+=1; e['active']=1
        e['productive']=0
        if action in (0,1): _chan[action][0]+=1
        _misses[0]+=1
        if not GRADE: return                   # identical to the frozen world
        if action==0:
            amt=GRADE_F
            e['in_f']=amt; e['overflow_f']=max(0,b.fuel+amt-FULL_F*2); b.fuel=min(FULL_F*2,b.fuel+amt)
        elif action==1:
            amt=GRADE_M
            e['in_m']=amt; e['overflow_m']=max(0,b.material+amt-256); b.material=min(256,b.material+amt)
    return contact


def build(arm,alloc):
    base=arm
    src=ac12.STEP_SRC; ns=dict(vars(ac9))
    assert src.count(ac12.RENEW_BLOCK)==1,'renewal block not found once'
    src=src.replace(ac12.RENEW_BLOCK,ac12.RENEW_BLOCK_NEW)
    assert src.count(GATE_BLOCK)==1,'contact gate block not found once'
    src=src.replace(GATE_BLOCK,GATED_BLOCK)
    assert src.count(PRODUCTIVE_LINE)==1,'productivity line not found once'
    # the frozen productivity line is also the line ac12 injects the outcome call after,
    # so this replacement owns both and the outcome call is appended here
    contacts=CONTACTS_LINE
    if base in ('allocate','protected','no_learning'):
        contacts=CONTACTS_LINE+"\n            alloc.outcome(o,action,e)"
        ns['alloc']=alloc
    src=src.replace(PRODUCTIVE_LINE,contacts)
    ns['ac12_memory']=ac12.m12; ns['allowance']=alloc.allowance
    shim={k:getattr(ac4,k) for k in dir(ac4) if not k.startswith('_')}
    shim['react']=ac12.react_world()
    ns['ac4']=SimpleNamespace(**shim)
    ns['grade']=SimpleNamespace(contact=make_contact(shim['react']))
    fns={}
    exec(compile(src,'ac15_step','exec'),ns,fns)
    return fns['step']


def set_world():
    """Pin the world constants for both the AC12 harness and this one, so an
    equivalence comparison is on the same world and not on module defaults."""
    ac12.PORTS=PORTS
    ac12.YIELD_M=FULL_M; ac12.YIELD_F=FULL_F
    ac12.POST_YIELD_M=None
    ac12.MOVE_KEYS=(); ac12.MOVE=10**9
    ac12.DEV=DEV


def run(seed,history,arm,ticks=TICKS,move=MOVE):
    for k,v in DEFAULTS.items(): setattr(ac12,k,v)
    base=arm
    if arm in ARM_CONFIG:
        base,kw=ARM_CONFIG[arm]
        for k,v in kw.items(): setattr(ac12,k,v)
    _misses[0]=0
    _chan[0]=[0,0]; _chan[1]=[0,0]
    chan_at_move=None
    set_world()
    base_map=(seed%2,(seed//2)%2)
    alloc=ac12.Alloc(base,seed,history)
    o,offs=ac12.acquire(seed)
    alloc.offs=offs
    alloc.shadow=o.body.traces[0].copy()
    step=build(arm,alloc)
    rng=np.random.default_rng([seed,1509])
    total=ac9.event(); late=ac9.event()
    for t in range(ticks):
        alloc.now=t
        mapping=base_map
        if move is not None and t>=move:
            mapping=tuple(1-c if act in MOVE_ACTIONS else c for act,c in enumerate(base_map))
        core=(rng.random((126,7))<.0001).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8)
        coin=bool(rng.random()<.5)
        e=step(o,core,noise,directions,coin,mapping,[t<DEV]*2,t<DEV)
        for k in total: total[k]+=e.get(k,0)
        if move is not None and t==move: chan_at_move=[[*_chan[0]],[*_chan[1]]]
        if t>=move:
            for k in late: late[k]+=e.get(k,0)
        if o.body.dead: break
    late_ticks=max(1,ticks-move) if move is not None else ticks
    ch=chan_at_move or [[0,0],[0,0]]
    chan_late={a:[_chan[a][0]-ch[a][0],_chan[a][1]-ch[a][1]] for a in (0,1)}
    chan_prod={a:(chan_late[a][1]/chan_late[a][0] if chan_late[a][0] else None) for a in (0,1)}
    return dict(seed=seed,history=history,arm=arm,ticks=ticks,move=move,
                move_actions=list(MOVE_ACTIONS),
                move_ticks=late_ticks,
                chan_late=chan_late,chan_productivity=chan_prod,
                productivity_kept=chan_prod[0],productivity_moved=chan_prod[1],
                mean_chan_productivity=((chan_prod[0] or 0)+(chan_prod[1] or 0))/2,
                activity=total['active']/ticks,completed=total['active']==ticks,
                activity_late=late['active']/late_ticks,
                contacts_late=late['contacts'],productive_late=late['productive'],
                in_m=late['in_m'],in_f=late['in_f'],
                productivity_late=late['productive']/max(1,late['contacts']),
                misses=_misses[0],
                dropped=alloc.log['dropped'],demand=o.memory.demand().tolist(),
                ledger=total,state_hash=o.digest())


NAMES=['ac15.py','ac12.py','ac12_memory.py','ac9.py','ac9_priority_v2.py','ac9_memory.py',
       'ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py','AC15_PROTOCOL_v1.md']


def collect(root,seeds,ticks=TICKS,move=MOVE):
    root=Path(root); root.mkdir(exist_ok=False)
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in NAMES if Path(n).exists()}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0,1):
                for arm in ARMS:
                    r=run(seed,history,arm,ticks=ticks,move=move)
                    rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps([(r['history'],r['arm'],round(r['activity'],3),r['completed'],
                               round(r['productivity_late'],3),r['in_m'],r['in_f'])
                              for r in rows[-2*len(ARMS):]]),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))
    return rows


def main():
    if '--equiv' in sys.argv:
        # GRADE=0 must reproduce the frozen (ungraded) harness byte for byte
        globals()['GRADE']=0
        out=[]
        for seed in (0,1):
            for h in (0,1):
                r=run(seed,h,'preserve',ticks=512,move=None)
                out.append((seed,h,r['state_hash'][:16],round(r['activity'],4)))
        print(json.dumps(out,indent=2)); return
    if '--engineering' in sys.argv:
        collect('ac15_engineering_v1',[0,1,2]); return
    collect('ac15_results_v1',FINALS)


if __name__=='__main__': main()
