"""Integrated spatial boundary, engineering v1."""
from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import numpy as np
import ac4_transport as tr
from ac1 import decode

ARMS = ('self', 'no_B', 'no_B_rescue', 'no_B_retention', 'no_policy_write', 'protected')
ENDPOINTS = np.array([[2,y] for y in range(-2,3)] + [[-2,y] for y in range(-2,3)]
                      + [[x,2] for x in range(-2,3)] + [[x,-2] for x in range(-2,3)])


@dataclass(slots=True)
class Body:
    traces: np.ndarray
    life: np.ndarray
    pos: np.ndarray
    boundary: np.ndarray
    energy: int = 64
    material: int = 128
    fuel: int = 32
    dead: bool = False

    def digest(self):
        raw = b''.join(x.tobytes() for x in (self.traces,self.life,self.pos,self.boundary))
        return hashlib.sha256(raw+json.dumps([self.energy,self.material,self.fuel,self.dead]).encode()).hexdigest()


def demonstration(o, priority):
    for bit, action in ((1,0),(2,1),(64,6),(128,7),(256,8)):
        if o & bit: return action
    for bank in priority:
        if o & (4 << bank): return 2+bank
    return 9


def policy(b):
    return (decode(b.traces[:2]).reshape(512,4)*np.array([1,2,4,8])).sum(axis=1)


def acquire(seed):
    rng = np.random.default_rng([seed,1004])
    priority = list(map(int,rng.permutation(4)))
    target = np.array([demonstration(o,priority) for o in range(512)])
    bits = rng.integers(0,2,(4,1024),dtype=np.uint8)
    bits[:2] = ((target[:,None] >> np.arange(4)) & 1).reshape(2,1024)
    b = Body(np.repeat(bits[:,:,None],7,axis=2),
             np.array([32,48,64,0]*4+[64,96,128,0],dtype=np.int16),
             rng.integers(-2,3,(20,2),dtype=np.int16),np.arange(128,248,6,dtype=np.int16))
    return b,bits,target,priority


def available(b):
    return (b.life>0) & tr.inside(b.pos)


def observe(b):
    a = available(b); ones = b.traces.sum(axis=-1)
    o = int(b.fuel<=8)+2*int(b.material<=64)
    for bank in range(4):
        o |= int(np.minimum(ones[bank],7-ones[bank]).sum()>=4) << (bank+2)
    o |= int(min(a[:16].reshape(4,4).sum(axis=1))<2)<<6
    o |= int(a[16:].sum()<2)<<7
    o |= int(b.boundary.min()<=64)<<8
    return o


def empty_event():
    return dict(active=0,in_m=0,in_f=0,overflow_m=0,overflow_f=0,converted=0,
                spent_e=0,spent_m=0,writes=0,W_birth=0,C_birth=0,B_birth=0,
                particle_expiry=0,particle_export=0,B_expiry=0,B_discard=0,external_B=0)


def pay(b,e,m,energy):
    if b.material<m or b.energy<energy: return False
    b.material-=m; b.energy-=energy; e['spent_m']+=m; e['spent_e']+=energy
    return True


def react(b,action,arm,e):
    b.energy-=1; e['spent_e']+=1; e['active']=1
    a = available(b)
    if action==0:
        e['in_f']=32; e['overflow_f']=max(0,b.fuel+32-64); b.fuel=min(64,b.fuel+32)
    elif action==1:
        e['in_m']=64; e['overflow_m']=max(0,b.material+64-256); b.material=min(256,b.material+64)
    elif 2<=action<=5:
        bank=action-2; majority=decode(b.traces[bank])
        sites=np.argwhere(b.traces[bank]!=majority[:,None])
        cap=0 if arm=='no_policy_write' and bank<2 else int(a[4*bank:4*bank+4].sum())*8
        n=min(cap,32,len(sites),b.energy,b.material)
        if n:
            sites=sites[:n]; b.traces[bank,sites[:,0],sites[:,1]]=majority[sites[:,0]]
            pay(b,e,n,n); e['writes']=n
    elif action in (6,7):
        groups=range(4) if action==6 else [4]
        for group in groups:
            parents=np.flatnonzero(a[group*4:group*4+4] if group<4 else a[:4])
            empty=np.flatnonzero(b.life[group*4:group*4+4]==0)
            if len(parents) and len(empty) and pay(b,e,4,2 if group<4 else 4):
                parent=int(parents[0])+(group*4 if group<4 else 0)
                child=group*4+int(empty[0]); b.pos[child]=b.pos[parent]
                b.life[child]=64 if group<4 else 128
                e['W_birth' if group<4 else 'C_birth']+=1
    elif action==8 and arm not in ('no_B','no_B_rescue','no_B_retention'):
        wp=b.pos[:16][a[:16]]
        if len(wp):
            near=(np.abs(ENDPOINTS[:,None,:]-wp[None,:,:]).sum(axis=2)<=1).any(axis=1)
            candidates=np.flatnonzero(near & (b.boundary<=64))
            if len(candidates) and pay(b,e,2,2):
                j=int(candidates[np.argmin(b.boundary[candidates])])
                e['B_discard']+=int(b.boundary[j]>0)
                b.boundary[j]=256; e['B_birth']+=1


def inventory(b):
    return (b.energy,b.material,b.fuel,int((b.life>0).sum()),int((b.boundary>0).sum()))


def balance(before,b,e):
    E,M,F,N,B=before
    assert b.energy==E+8*e['converted']-e['spent_e']
    assert b.material==M+e['in_m']-e['overflow_m']-e['spent_m']
    assert b.fuel==F+e['in_f']-e['overflow_f']-e['converted']
    assert (b.life>0).sum()==N+e['W_birth']+e['C_birth']-e['particle_expiry']-e['particle_export']
    assert (b.boundary>0).sum()==B+e['B_birth']+e['external_B']-e['B_expiry']-e['B_discard']
    assert e['spent_m']==e['writes']+4*(e['W_birth']+e['C_birth'])+2*e['B_birth']


def step(b,flips,directions,arm='self',protected=None):
    if arm not in ARMS or (protected is not None and arm!='protected'):
        raise ValueError('Invalid arm or hidden policy')
    if arm=='protected' and protected is None: raise ValueError('Missing protected control')
    e=empty_event()
    if b.dead: return e
    before=inventory(b); b.traces^=flips
    e['particle_expiry']=int((b.life==1).sum()); b.life[b.life>0]-=1
    e['B_expiry']=int((b.boundary==1).sum()); b.boundary[b.boundary>0]-=1
    if arm=='no_B_rescue':
        missing=b.boundary==0; e['external_B']=int(missing.sum()); b.boundary[missing]=256
    # Empty slots are excluded from movement using the kernel's inactive mask.
    inactive=b.life==0; old=inactive.copy()
    tr.move(b.pos,inactive,b.boundary,directions,np.ones(20,dtype=bool),arm=='no_B_retention')
    lost=inactive & ~old; e['particle_export']=int(lost.sum()); b.life[lost]=0
    a=available(b); units=min(int(a[16:].sum()),b.fuel,(128-b.energy)//8)
    b.fuel-=units; b.energy+=8*units; e['converted']=units
    if b.energy<1: b.dead=True
    else:
        o=observe(b); action=int((protected if arm=='protected' else policy(b))[o])
        react(b,action,arm,e)
    balance(before,b,e)
    return e


def run(seed,p,arm,ticks=2048):
    b,bits,target,priority=acquire(seed); rng=np.random.default_rng([seed,1104])
    total=empty_event()
    for _ in range(ticks):
        flips=(rng.random(b.traces.shape,dtype=np.float32)<p).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8)
        e=step(b,flips,directions,arm,target if arm=='protected' else None)
        for k in total: total[k]+=e[k]
    return dict(seed=seed,p=p,arm=arm,ticks=ticks,priority=priority,
                activity=total['active']/ticks,completed=total['active']==ticks,
                policy_accuracy=float(np.mean(policy(b)==target)),
                payload_accuracy=float(np.mean(decode(b.traces[2:])==bits[2:])),
                final_inventory=inventory(b),final_inside=int(available(b).sum()),
                ledger=total,state_hash=b.digest())


def main():
    root=Path('ac4_results_v1'); root.mkdir(exist_ok=False)
    names=['ac4.py','test_ac4.py','ac4_transport.py','ac1.py','AC4_PROTOCOL_v1.md']
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    for p in (.00005,.0001):
        for seed in range(4):
            for arm in ARMS: rows.append(run(seed,p,arm))
        print(json.dumps({'p':p,'activity':{a:float(np.mean([r['activity'] for r in rows if r['p']==p and r['arm']==a])) for a in ARMS}}),flush=True)
    (root/'results.json').write_text(json.dumps(dict(kind='engineering',hashes=hashes,rows=rows),indent=2))


if __name__=='__main__': main()
