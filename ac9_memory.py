"""Paid, expiring allocated entries. Integration with the organism is pending.

Each slot is three bits (valid,key,value), seven physical replicas per bit.
Lifetime zero means absent matter, not a hidden stored bit. No external index.
"""
from dataclasses import dataclass
import hashlib
import numpy as np


@dataclass(slots=True)
class Memory:
    bits: np.ndarray
    life: np.ndarray

    @classmethod
    def empty(cls):
        return cls(np.zeros((2,2,3,7),dtype=np.uint8),np.zeros((2,2,3,7),dtype=np.uint8))

    def digest(self):
        return hashlib.sha256(self.bits.tobytes()+self.life.tobytes()).hexdigest()

    def occupied(self):
        return self.life>0

    def demand(self):
        return self.occupied().sum(axis=(1,2,3)).astype(int)

    def decoded_slot(self,region,slot):
        present=self.life[region,slot]>0
        counts=present.sum(axis=1)
        if np.any(counts<4): return None
        ones=(self.bits[region,slot]*present).sum(axis=1)
        if np.any(2*ones==counts): return None
        decoded=(2*ones>counts).astype(np.uint8)
        return tuple(map(int,decoded)) if decoded[0] else None

    def read(self,key):
        values=[]
        for region in range(2):
            for slot in range(2):
                entry=self.decoded_slot(region,slot)
                if entry is not None and entry[1]==key: values.append(entry[2])
        return values[0] if values and len(set(values))==1 else None


def age(memory,flips):
    memory.bits^=(flips & memory.occupied())
    expired=memory.life==1
    memory.life[memory.life>0]-=1
    memory.bits[expired]=0
    return int(expired.sum())


def deposit(memory,body,key,value,activation,interior_W):
    """Contact outcome supplies key/value; local sensory activity supplies placement.

    Returns material bound, physical writes, and destination. No history label.
    Caller must pay the enclosing action's living cost. No partial transaction.
    """
    if key not in (0,1) or value not in (0,1): raise ValueError('Invalid entry')
    if memory.read(key) is not None: return dict(writes=0,bound=0,region=None)
    for region in range(2):
        if not activation[region] or min(32,8*interior_W[region],body.energy,body.material)<21: continue
        for slot in range(2):
            if memory.occupied()[region,slot].any(): continue
            body.energy-=21; body.material-=21
            memory.bits[region,slot]=np.array([1,key,value],dtype=np.uint8)[:,None]
            memory.life[region,slot]=64
            return dict(writes=21,bound=21,region=region)
    return dict(writes=0,bound=0,region=None)


def renew(memory,body,region,interior_W):
    """Reconstruct only from currently surviving majority, including key/validity."""
    cap=min(32,8*interior_W,body.energy,body.material)
    writes=bound=waste=0
    for slot in range(2):
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
