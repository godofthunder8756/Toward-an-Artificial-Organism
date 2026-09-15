"""Compact mutable controller primitive; not yet an adaptive organism.

Nine ordered rules, each an enabled bit, 9-bit positive condition mask and
4-bit action. Interpreter fallthrough supplies rest. Stored in existing
damageable trace sites. Interpreter and format are supplied laws.
"""
import numpy as np
from ac1 import decode

RULES=9
WIDTH=14
PROGRAM_BITS=RULES*WIDTH


def encode_rule(enabled,mask,action):
    if enabled not in (0,1) or not 0<=mask<512 or not 0<=action<16:
        raise ValueError('Invalid rule')
    word=int(enabled)|(int(mask)<<1)|(int(action)<<10)
    return np.array([(word>>k)&1 for k in range(WIDTH)],dtype=np.uint8)


def program(priority):
    if sorted(priority)!=list(range(4)):
        raise ValueError('Invalid acquired permutation')
    # Five resource/constituent rules followed by four bank rules.
    rules=[(1,1,0),(1,2,1),(1,64,6),(1,128,7),(1,256,8)]
    # Four bank rules make ten total with rest: rest is interpreter fallthrough,
    # independent of acquired action information, as in AC4 unused actions.
    rules += [(1,4<<bank,2+bank) for bank in priority]
    return np.concatenate([encode_rule(*r) for r in rules])


def choose(traces,observation):
    if not 0<=observation<512: raise ValueError('Invalid observation')
    bits=decode(traces[0,:PROGRAM_BITS]).reshape(RULES,WIDTH)
    words=(bits*(1<<np.arange(WIDTH))).sum(axis=1)
    for word in words:
        enabled=int(word)&1; mask=(int(word)>>1)&511
        if enabled and observation&mask==mask:
            return (int(word)>>10)&15
    return 9


def install_at_acquisition(traces,priority):
    """Initial demonstration installation only; forbidden as live repair target."""
    traces[0,:PROGRAM_BITS]=program(priority)[:,None]


def paid_replace(body,offset,bits,interior_W):
    """Atomic logical update; charge every changed replica, no free redundancy.

    Available W count must be calculated from physical body by the caller.
    This primitive does not claim a completed integration or enforce that caller.
    Whole update is rejected if 32-write/action capacity or resources insufficient.
    Returns explicit E/M/write charges; no protected expected value is retained.
    """
    bits=np.asarray(bits,dtype=np.uint8)
    if offset<0 or offset+len(bits)>PROGRAM_BITS or np.any(bits>1):
        raise ValueError('Invalid program write')
    sites=body.traces[0,offset:offset+len(bits)]
    changed=sites!=bits[:,None]
    n=int(changed.sum())
    if n>min(32,8*interior_W,body.energy,body.material):
        return dict(applied=False,writes=0,energy=0,material=0)
    sites[:]=bits[:,None]
    body.energy-=n; body.material-=n
    return dict(applied=True,writes=n,energy=n,material=n)
