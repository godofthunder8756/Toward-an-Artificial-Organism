"""AC12 primitive: per-slot renewal of allocated memory entries.

The frozen `ac9_memory.renew` renews every slot of a region, which is coarser
than the usefulness boundary AC11 needed (one key can go stale while the other
stays valid). This module supplies the same law restricted to the slots an
allocation mask allows, with every price and capacity rule kept frozen:

- the capacity `min(32, 8*interior_W, energy, material)` is **per action**, shared
  across the slots renewed in that action, exactly as the frozen law shares it
  across a region's slots;
- one material and one energy per replica actually written;
- a replica is skipped when it is younger than 17 ticks and already equal to the
  decoded majority;
- reconstruction uses only the currently surviving majority, so an error can be
  reinforced rather than corrected;
- slots are visited in the frozen order (slot 0 then slot 1).

`renew_region(memory,body,region,interior_W)` is exactly `renew_alloc(...,[1,1])`
and is checked against the frozen function by equivalence test, so introducing the
per-slot interface does not change what a whole-region renewal does.
"""
import numpy as np


def renew_alloc(memory,body,region,interior_W,allowed):
    """Renew the allowed slots of a region under one shared action capacity."""
    allowed=[bool(x) for x in allowed]
    assert len(allowed)==2,'per-slot allowance must cover both slots'
    cap=min(32,8*interior_W,body.energy,body.material)
    writes=bound=waste=0
    for slot in range(2):
        if not allowed[slot]: continue
        entry=memory.decoded_slot(region,slot)
        if entry is None: continue
        for bit,value in enumerate(entry):
            for replica in range(7):
                if writes==cap: return dict(writes=writes,bound=bound,waste=waste)
                life=int(memory.life[region,slot,bit,replica])
                if life>16 and memory.bits[region,slot,bit,replica]==value: continue
                body.energy-=1; body.material-=1; writes+=1
                waste+=int(life>0); bound+=int(life==0)
                memory.bits[region,slot,bit,replica]=value
                memory.life[region,slot,bit,replica]=64
    return dict(writes=writes,bound=bound,waste=waste)


def renew_region(memory,body,region,interior_W):
    """The frozen region-wide behaviour expressed through the allocation mask."""
    return renew_alloc(memory,body,region,interior_W,[1,1])


def decoded_key(memory,region,slot):
    """The key stored in a slot, or None. Used to attribute a slot to a route."""
    entry=memory.decoded_slot(region,slot)
    return None if entry is None else int(entry[1])


def slot_of_key(memory,key):
    """(region,slot) holding the given key, or None."""
    for region in range(2):
        for slot in range(2):
            if decoded_key(memory,region,slot)==key: return (region,slot)
    return None


def occupied_slots(memory):
    return [(r,s) for r in range(2) for s in range(2) if bool(memory.occupied()[r,s].any())]
