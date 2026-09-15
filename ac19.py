"""AC19: closure with persistent corruption -- is the decision state a *maintained* constraint?

Why this is the next step
-------------------------
AC14 asked whether the organism's own decision state is a maintained constraint in the loop:

    the allocation register lives inside traces[0,:126]
    -> the program bank is repaired only by the paid bank-0 repair action
    -> whose capacity is core interior W, which the program itself produces

It could not answer, and measured why: the frozen damage stream is `b.traces[0,:126] ^=
core_flips`, an XOR, so a flip **self-reverses** on the next hit. At 1e-4 per replica per tick
over 4096 ticks the bank accumulated 3 differing replicas of 882, and the register (read by
majority of seven) never changed. AC14's recorded requirement was therefore: **persistent
corruption** -- "a flip that stays flipped until repaired" -- or a much higher rate.

AC19 supplies exactly that, with one asserted surgery on the frozen step:

    b.traces[0,:126] ^= core_flips     ->     b.traces[0,:126] |= core_flips

Damage can then only *set* a register bit, never clear it, and the only thing that clears it
is the paid bank-0 repair (`ac4.react` sets every replica to the majority). Register bits are
zero when healthy, so a set bit means "relinquish this slot". The decision state is therefore
genuinely at risk for the first time, and repair is load-bearing **by construction** rather
than by luck of rate and horizon. This is the model AC14 named as the more interesting option.

The question, and its falsifier
-------------------------------
Does removing the organism's own funded repair degrade its decision state and thereby change
what it maintains? Falsifier, from AC14 and unchanged: if cutting the repair changes neither
the register's state nor the organism's maintenance behaviour, the loop is not load-bearing.

The protected-register arms are the control and are predicted to be **immune**: their decisions
read a shadow copy that the damage stream never touches, so if they behave exactly like the
live arms under the cut, corruption does not matter and the loop is not load-bearing.
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
import ac15
import ac16
from ac1 import decode

TICKS=4096
MOVE=1024
DEV=512
DAMAGE_RATE=1e-4          # the frozen rate; the mode, not the rate, is what changes
# Targeted corruption of the DECISION state alone. The global sticky mode left the program
# intact enough to matter but never flipped a register bit (screen: 6 of 28 register replicas
# set, no bit reaching 4 of 7), and cutting the repair killed the organism through its *other*
# program bits -- so the protected control was indistinguishable from the live arm and the
# decision state was never the cause. Concentrating the corruption on the register bits keeps
# the rest of the program pristine, so any behavioural change is attributable to the decision
# state and there is no death confound. Rate is per register replica per tick; with T=4096 a
# rate of 2.5e-4 gives each replica ~1 expected hit, i.e. P(a bit reaches 4 of 7) ~ 0.7.
REG_RATE=2.5e-4
# The corruption model the closure test needs, established by measurement: a 4-of-7 flip on
# ONE register bit flips the decision while leaving the observation untouched (the rule row's
# disagreement sum is 3, below the 4 that `ac9.observe` needs). Spread corruption was wrong --
# setting 2 replicas on each of the 4 register bits made bank 0's disagreement bit fire, so the
# organism *saw* a corruption it could never repair and died in a repair/W loop, identically in
# the live and protected arms. Measured: pristine obs 0 / disagreement 0; spread 2x4 -> obs 4 /
# disagreement 1; single bit 4-of-7 -> obs 0 / disagreement 0 and the bit reads relinquished.
FLIP_REPLICAS=4          # replicas to set on one bit: 4 of 7 flips it (majority), 3 does not
FLIP_PERIOD=128          # flip one decision bit this often after the move, round-robin

# the frozen damage line, and the sticky replacement
XOR_LINE="    b.traces[0,:126]^=core_flips"
OR_LINE="    b.traces[0,:126]|=core_flips"

ARMS=('two_way','two_way_protected','two_way_no_repair','two_way_protected_no_repair')
NEEDS=('two_way','two_way_protected')


class AllocTwoWayProtected(ac12.Alloc):
    """The two-way rule with the decision read from the protected shadow.

    ac12's `allowance` already reads the shadow for `arm=='protected'`, so this class only has
    to supply the two-way update (restore on a productive contact, drop on an unproductive
    streak) instead of ac12's one-way drop. The shadow is never touched by the damage stream,
    which is what makes these arms the control: their *decisions* cannot be corrupted, only
    their bodies can.
    """

    def outcome(self,o,key,e):
        if self.arm!='protected': return
        key=int(key)
        if e['productive']>0:
            self._restore(o,e,key)
            self.streak[key]=0
            return
        self.streak[key]=self.streak.get(key,0)+1
        if self.streak[key]>=ac12.STREAK_N: self._drop(o,e,key)

    def _restore(self,o,e,key):
        place=ac12.m12.slot_of_key(o.memory,key)
        if place is None: return
        off=self.offs[2*place[0]+place[1]]
        sites=self.shadow[off]
        n=int((sites!=0).sum())
        if n==0: return
        cap=min(32,8*int(ac4.available(o.body)[:4].sum()),o.body.energy,o.body.material)
        if n>cap: return
        o.body.energy-=n; o.body.material-=n
        e['spent_e']+=n; e['spent_m']+=n; e['writes']+=n
        sites[:]=0
        self.log.setdefault('restored',[]).append(list(place))


def arm_parts(arm):
    """(base arm, protected register?, repair cut?)"""
    protected='protected' in arm
    cut=arm.endswith('_no_repair')
    return ('protected' if protected else 'allocate'),protected,cut


def build(arm,alloc,sticky=True,cut_mode='bank0'):
    """cut_mode: 'bank0' cuts the whole program-bank repair (the frozen `no_policy_write`
    guard); 'register_only' lets the bank be repaired but reverts the repair *on the register
    offsets*, so the decision state is the only thing left unrepaired.

    'bank0' is confounded: the screen showed both the live and the protected arm dying under
    it, so its effect is not attributable to the decision state. 'register_only' isolates the
    question the closure claim actually asks.
    """
    base,protected,cut=arm_parts(arm)
    src=ac12.STEP_SRC; ns=dict(vars(ac9))
    assert src.count(ac12.RENEW_BLOCK)==1,'renewal block not found once'
    src=src.replace(ac12.RENEW_BLOCK,ac12.RENEW_BLOCK_NEW)
    src=src.replace(ac15.GATE_BLOCK,ac15.GATED_BLOCK)
    src=src.replace(ac15.PRODUCTIVE_LINE,ac15.CONTACTS_LINE+"\n            alloc.outcome(o,action,e)")
    ns['alloc']=alloc
    if sticky:
        assert src.count(XOR_LINE)==1,'frozen damage line not found once'
        src=src.replace(XOR_LINE,OR_LINE)
    else:
        assert src.count(XOR_LINE)==1,'frozen damage line not found once'
    ns['ac12_memory']=ac12.m12; ns['allowance']=alloc.allowance
    shim={k:getattr(ac4,k) for k in dir(ac4) if not k.startswith('_')}
    react=ac12.react_world()
    if cut and cut_mode=='bank0':
        react=(lambda b,action,a,e,_f=react: _f(b,action,'no_policy_write',e))
    elif cut and cut_mode=='register_only':
        def react(b,action,arm_arg,e,_f=react,_offs=alloc.offs):
            saved=None
            if action==2 and _offs:                     # bank-0 repair: keep it off the register
                saved=[b.traces[0,o].copy() for o in _offs]
            out=_f(b,action,arm_arg,e)
            if saved is not None:
                for o,keep in zip(_offs,saved): b.traces[0,o]=keep
            return out
    shim['react']=react
    ns['ac4']=SimpleNamespace(**shim)
    ns['grade']=SimpleNamespace(contact=ac15.make_contact(shim['react']))
    fns={}
    exec(compile(src,'ac19_step','exec'),ns,fns)
    return fns['step']


def run(seed,history,arm,ticks=TICKS,move=MOVE,sticky=True,rate=DAMAGE_RATE,
        reg_rate=REG_RATE,targeted=True,cut_mode='register_only',
        corruption='bit4of7',flip_period=FLIP_PERIOD,move_actions=ac15.MOVE_ACTIONS):
    ac15.set_world()
    ac12.DEV=DEV
    for k,v in ac15.DEFAULTS.items(): setattr(ac12,k,v)
    base,protected,cut=arm_parts(arm)
    ac15._misses[0]=0; ac15._chan[0]=[0,0]; ac15._chan[1]=[0,0]
    base_map=(seed%2,(seed//2)%2)
    true_after=tuple(1-c if a in ac15.MOVE_ACTIONS else c for a,c in enumerate(base_map))
    if protected:
        alloc=AllocTwoWayProtected('protected',seed,history)
    else:
        ac16.RESTORE=True
        alloc=ac16.AllocRestore('allocate',seed,history)
    o,offs=ac12.acquire(seed)
    alloc.offs=offs; alloc.shadow=o.body.traces[0].copy()
    step=build(arm,alloc,sticky=sticky,cut_mode=cut_mode)
    rng=np.random.default_rng([seed,1509])
    total=ac9.event()
    reg_history=[]
    for t in range(ticks):
        alloc.now=t
        mapping=base_map if t<move else true_after
        core=(rng.random((126,7))<rate).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<rate).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8)
        coin=bool(rng.random()<.5)
        e=step(o,core,noise,directions,coin,mapping,[True,True],True)
        for k in total: total[k]+=e.get(k,0)
        if targeted and not o.body.dead:
            if corruption=='bit4of7':
                # flip ONE decision bit: 4 of its 7 replicas set flips it, and the rule row's
                # disagreement sum stays at 3, below the 4 that ac9.observe needs -- so the
                # organism's *observation* is untouched and only its decision changes
                if t>=move and (t-move)%flip_period==0:
                    off=offs[((t-move)//flip_period)%len(offs)]
                    o.body.traces[0,off][:FLIP_REPLICAS]=1
            else:
                # the spread model: several bits with a few replicas each. Kept because it is
                # what the first screens used, and it is confounded -- it fires the bank-0
                # disagreement bit in ac9.observe and the organism dies in a repair/W loop.
                mask=(rng.random(7)<reg_rate).astype(o.body.traces.dtype)
                for off in offs: o.body.traces[0,off]|=mask
        if t%256==0:
            reg_history.append([int(o.body.traces[0,off].sum()) for off in offs])
        if o.body.dead: break
    dec=decode(o.body.traces[0,:126])
    pristine=ac12.acquire(seed)[0].body.traces[0,:126]     # the program the organism actually
    # carries. Comparing against ac9.acquire(seed) here was a bug: that is a *different*
    # program variant (priority v2 vs v1), so the metric reported ~140 "differences" that were
    # just the variant gap, in every arm including the uncut ones.
    return dict(seed=seed,history=history,arm=arm,ticks=ticks,move=move,sticky=sticky,
                damage_rate=rate,reg_rate=reg_rate,targeted=targeted,
                protected=protected,repair_cut=cut,cut_mode=cut_mode,corruption=corruption,
                completed=total['active']==ticks,activity=total['active']/ticks,
                register_replicas_set_total=sum(int(o.body.traces[0,off].sum()) for off in offs),
                register_bits_relinquished=[ac12.bit_value(o,off) for off in offs],
                register_bits_relinquished_count=sum(int(ac12.bit_value(o,off)) for off in offs),
                program_replicas_differing=int((o.body.traces[0,:126]!=pristine).sum()),
                register_history=reg_history,
                chan_late={a:list(ac15._chan[a]) for a in (0,1)},
                productivity_moved=(ac15._chan[1][1]/ac15._chan[1][0] if ac15._chan[1][0] else None),
                productivity_kept=(ac15._chan[0][1]/ac15._chan[0][0] if ac15._chan[0][0] else None),
                relinquishments=len(alloc.log['dropped']),
                restorations=len(alloc.log.get('restored',[])),
                demand=o.memory.demand().tolist(),ledger=total,state_hash=o.digest())


if __name__=='__main__':
    if '--screen' in sys.argv:
        for arm in ARMS:
            for sticky in (True,False):
                r=run(0,0,arm,sticky=sticky)
                print(json.dumps(dict(arm=arm,sticky=sticky,alive=r['completed'],
                    reg_set=r['register_replicas_set_total'],
                    reg_relinq=r['register_bits_relinquished_count'],
                    prog_diff=r['program_replicas_differing'],
                    moved=(round(r['productivity_moved'],3) if r['productivity_moved'] is not None else None),
                    kept=(round(r['productivity_kept'],3) if r['productivity_kept'] is not None else None),
                    relinq=r['relinquishments'],restore=r['restorations'])),flush=True)
