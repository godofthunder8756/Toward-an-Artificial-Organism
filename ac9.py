from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import numpy as np
import ac4
import ac5
import ac5_program as prog
import ac9_memory as mem
import ac4_transport as tr
from ac1 import decode

ARMS=('keep','block0','block1','no_growth')


@dataclass(slots=True)
class Organism:
    body: ac4.Body
    memory: mem.Memory
    def digest(self): return hashlib.sha256((self.body.digest()+self.memory.digest()).encode()).hexdigest()


def acquire(seed):
    b,_,_=ac5.acquire(seed); b.traces[0,126:]=0; b.traces[1:]=0
    b.life[4:16]=0
    return Organism(b,mem.Memory.empty())


def event():
    e=ac4.empty_event()
    e.update(memory_writes=0,memory_bound=0,memory_waste=0,memory_expiry=0,
             region0_births=0,region1_births=0,contacts=0,productive=0,deposits=0)
    return e


def memory_charge(e,result):
    n=result['writes']; e['memory_writes']+=n; e['writes']+=n
    e['spent_m']+=n; e['spent_e']+=n
    e['memory_bound']+=result['bound']; e['memory_waste']+=result.get('waste',0)


def birth(b,bank,parent,e):
    empty=np.flatnonzero(b.life[bank*4:bank*4+4]==0)
    if len(empty) and ac4.pay(b,e,4,2):
        j=bank*4+int(empty[0]); b.life[j]=64; b.pos[j]=b.pos[parent]
        e['W_birth']+=1
        if bank in (1,2): e[f'region{bank-1}_births']+=1
        return True
    return False


def observe(o):
    b=o.body; a=ac4.available(b); demand=o.memory.demand()
    obs=int(b.fuel<=8)+2*int(b.material<=64)
    ones=b.traces[0,:126].sum(axis=1)
    obs|=int(np.minimum(ones,7-ones).sum()>=4)<<2
    for region in range(2):
        life=o.memory.life[region]; bits=o.memory.bits[region]
        urgent=bool(np.any((life>0)&(life<=16)))
        for slot in range(2):
            v=o.memory.decoded_slot(region,slot)
            if v is not None: urgent|=bool(np.any((life[slot]>0)&(bits[slot]!=np.array(v)[:,None])))
        obs|=int(urgent)<<(region+3)
    low=int(a[:4].sum())<2
    for region in range(2): low|=bool(demand[region]>0 and a[4*(region+1):4*(region+2)].sum()<3)
    obs|=int(low)<<6; obs|=int(a[16:].sum()<2)<<7; obs|=int(b.boundary.min()<=64)<<8
    return obs


def step(o,core_flips,memory_flips,directions,coin,mapping,activation,grow=True,blocked=None):
    b=o.body; e=event()
    if b.dead: return e
    before=ac4.inventory(b); old_sites=int(o.memory.occupied().sum())
    b.traces[0,:126]^=core_flips; e['memory_expiry']=mem.age(o.memory,memory_flips)
    e['particle_expiry']=int((b.life==1).sum()); b.life[b.life>0]-=1
    e['B_expiry']=int((b.boundary==1).sum()); b.boundary[b.boundary>0]-=1
    inactive=b.life==0; old=inactive.copy()
    tr.move(b.pos,inactive,b.boundary,directions,np.ones(20,dtype=bool))
    lost=inactive&~old; e['particle_export']=int(lost.sum()); b.life[lost]=0
    a=ac4.available(b); units=min(int(a[16:].sum()),b.fuel,(128-b.energy)//8)
    b.fuel-=units; b.energy+=units*8; e['converted']=units
    if b.energy<1: b.dead=True
    else:
        action=prog.choose(b.traces,observe(o))
        if action in (0,1):
            selected=o.memory.read(action); port=int(coin) if selected is None else selected
            if port==mapping[action]: ac4.react(b,action,'self',e)
            else: b.energy-=1; e['active']=1; e['spent_e']+=1
            e['contacts']=1; e['productive']=int(e['in_m']+e['in_f']>0)
            if grow and selected is None and e['productive']:
                parents=np.flatnonzero(a[:4])
                if len(parents):
                    for r in range(2):
                        if not activation[r]: continue
                        while ac4.available(b)[4*(r+1):4*(r+2)].sum()<3:
                            if not birth(b,r+1,int(parents[0]),e): break
                        break
                w=[int(ac4.available(b)[4*(r+1):4*(r+2)].sum()) for r in range(2)]
                result=mem.deposit(o.memory,b,action,port,activation,w)
                memory_charge(e,result); e['deposits']=int(result['bound']>0)
        elif action in (3,4):
            b.energy-=1; e['active']=1; e['spent_e']+=1; r=action-3
            if r!=blocked:
                result=mem.renew(o.memory,b,r,int(a[4*(r+1):4*(r+2)].sum()))
                memory_charge(e,result)
        elif action==6:
            b.energy-=1; e['active']=1; e['spent_e']+=1
            banks=[0]+[r+1 for r,n in enumerate(o.memory.demand()) if n>0]
            for bank in banks:
                parents=np.flatnonzero(a[bank*4:bank*4+4])
                if len(parents): birth(b,bank,bank*4+int(parents[0]),e)
        else: ac4.react(b,action,'self',e)
    ac4.balance(before,b,e)
    assert o.memory.occupied().sum()==old_sites+e['memory_bound']-e['memory_expiry']
    return e


def run(seed,history,arm,ticks=2048):
    o=acquire(seed); mapping=(seed%2,(seed//2)%2); rng=np.random.default_rng([seed,1509])
    total=event(); checkpoint=None
    for t in range(ticks):
        if t==512: checkpoint=dict(demand=o.memory.demand().tolist(),routes=[o.memory.read(k) for k in (0,1)])
        core=(rng.random((126,7))<.0001).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8); coin=bool(rng.random()<.5)
        activation=[history==r for r in range(2)] if t<512 else [True,True]
        blocked=int(arm[-1]) if t>=512 and arm.startswith('block') else None
        e=step(o,core,noise,directions,coin,mapping,activation,t<512 and arm!='no_growth',blocked)
        for k in total: total[k]+=e[k]
    return dict(seed=seed,history=history,arm=arm,ticks=ticks,mapping=mapping,checkpoint=checkpoint,
                activity=total['active']/ticks,completed=total['active']==ticks,
                routes=[o.memory.read(k) for k in (0,1)],demand=o.memory.demand().tolist(),
                ledger=total,final_inventory=ac4.inventory(o.body),state_hash=o.digest())


def main():
    root=Path('ac9_results_v1'); root.mkdir(exist_ok=False)
    names=['ac9.py','ac9_memory.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py','test_ac9.py','AC9_PROTOCOL_v1.md']
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2)); rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in range(1000,1004):
            for history in (0,1):
                for arm in ARMS:
                    r=run(seed,history,arm); rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,outcomes=[(r['history'],r['arm'],r['activity'],r['routes']) for r in rows[-8:]])),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))


if __name__=='__main__': main()
