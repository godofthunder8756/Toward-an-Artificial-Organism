"""Joint neural controller and locally maintained recurrent tissue.

A deliberately scaffolded model, not autopoiesis. Signed synaptic weights use
ordinary global gradient learning. Edge biomass uses a local activity rule;
per-neuron material stores pay for every deposited unit. No text or drive labels.
"""
from dataclasses import dataclass, asdict
import copy
import numpy as np
from e1.circuits import Adam, softmax

@dataclass(frozen=True)
class Config:
    hidden: int = 12
    rounds: int = 4000
    branch_rounds: int = 1800
    eval_rounds: int = 240
    eval_worlds: int = 6
    history_rounds: int = 2000
    gap: int = 4
    growth: float = .10
    decay: float = .025
    deposit: float = .25
    store_cap: float = .50
    basal_growth: float = .04
    initial_store: float = .12
    initial_mass: float = .30
    neural_noise: float = .025
    lr: float = .003
    gamma: float = .90
    exploration: float = .20
    batch: int = 32
    train_every: int = 4
    energy_cap: float = 4.
    cost: float = .23
    basal_yield: float = .065
    task_yield: float = .24
    seed_start: int = 200
    seeds: int = 16

class Network:
    def __init__(self, cfg, seed):
        self.cfg=cfg
        rng=np.random.default_rng(seed)
        h=cfg.hidden
        self.types=np.arange(h)//(h//2)
        # Same-size two-bank sparse graph; no chemistry-specific objective.
        self.mask=(rng.random((h,h))<.45).astype(float)
        np.fill_diagonal(self.mask,1.)
        self.p={'u':rng.normal(0,.3,(8,h)),
                'w':rng.normal(0,.6,(h,h))*self.mask+np.eye(h)*1.5,
                'b':np.zeros(h),'v':rng.normal(0,.15,(h,5))}
        # Sensor channel 6 enters bank A; channel 7 enters bank B.
        self.umask=np.ones((8,h)); self.umask[6,self.types==1]=0
        self.umask[7,self.types==0]=0
        self.p['u']*=self.umask
        self.opt=Adam(self.p,cfg.lr);self.target=copy.deepcopy(self.p)
        self.buf=[];self.cursor=0;self.updates=0

    def initial_body(self):
        return Body(self.cfg,self.mask,self.types)

    def inputs(self,obs,bit=None,history=None):
        x=np.zeros((self.cfg.gap+3,8)); x[:2,:6]=obs
        # The maintenance decision occurs after step 1, before the cue exists.
        if bit is not None:
            sign=2*bit-1
            if history is None: x[2,6:]=sign
            else:x[2,6+history]=sign
        return x

    def forward(self,x,mass,noise=None,target=False,lesion=None):
        p=self.target if target else self.p
        x=np.asarray(x)
        if x.ndim==2:x=x[None]
        n=len(x); z=np.asarray(mass)
        if z.ndim==2:z=np.broadcast_to(z,(n,*z.shape))
        node=np.sqrt(np.maximum(0,z.sum(1)/self.mask.sum(0)))
        if lesion is not None:
            node=node.copy();node[:,lesion]=0
        w=p['w'][None]*z
        h=np.zeros((n,self.cfg.hidden));states=[h.copy()]
        if noise is None:noise=np.zeros((n,x.shape[1],self.cfg.hidden))
        for t in range(x.shape[1]):
            h=node*np.tanh(x[:,t]@p['u']+np.einsum('ni,nij->nj',h,w)+p['b']+noise[:,t])
            states.append(h.copy())
        q=states[2]@p['v'][:,:3]
        logits=h@p['v'][:,3:]
        return q,logits,(x,z,node,w,states)

    def grads(self,cache,dq,dlogits):
        x,z,node,w,states=cache
        g={k:np.zeros_like(v) for k,v in self.p.items()}
        g['v'][:,:3]=states[2].T@dq
        g['v'][:,3:]=states[-1].T@dlogits
        dh=dlogits@self.p['v'][:,3:].T
        for t in reversed(range(x.shape[1])):
            if t==1:dh+=dq@self.p['v'][:,:3].T
            normalized=np.divide(states[t+1],node,out=np.zeros_like(node),where=node>0)
            da=dh*node*(1-normalized**2)
            g['u']+=x[:,t].T@da
            g['b']+=da.sum(0)
            g['w']+=np.einsum('ni,nj,nij->ij',states[t],da,z)
            dh=np.einsum('nj,nij->ni',da,w)
        g['u']*=self.umask;g['w']*=self.mask
        return g

    def add_learn(self,item,rng,enabled=True):
        if not enabled:return
        if len(self.buf)<512:self.buf.append(item)
        else:self.buf[self.cursor]=item
        self.cursor=(self.cursor+1)%512
        if len(self.buf)<self.cfg.batch or self.cursor%self.cfg.train_every:return
        b=[self.buf[i] for i in rng.integers(0,len(self.buf),self.cfg.batch)]
        x,z,a,r,nx,nz,done,attempt,success,propensity=map(np.array,zip(*b))
        q,logits,cache=self.forward(x,z)
        nq,_,_=self.forward(nx,nz,target=True)
        targets=r+self.cfg.gamma*(1-done)*nq.max(-1)
        dq=np.zeros_like(q);dq[np.arange(len(b)),a]=np.clip(q[np.arange(len(b)),a]-targets,-1,1)/len(b)
        probs=softmax(logits);dl=probs.copy();dl[np.arange(len(b)),attempt]-=1
        # Exploratory gate attempts supply only success/failure; inverse propensity
        # estimates a success-conditioned loss. This explicit auxiliary learning
        # objective is disclosed and shared by all variants.
        dl*=(success/propensity)[:,None]/len(b)
        g=self.grads(cache,dq,dl)
        self.opt.step(self.p,g)
        self.p['w']=np.clip(self.p['w'],-3,3)*self.mask
        self.p['u']=np.clip(self.p['u'],-3,3)*self.umask
        self.p['v']=np.clip(self.p['v'],-3,3)
        self.p['b']=np.clip(self.p['b'],-1,1)
        self.updates+=1
        if self.updates%30==0:self.target=copy.deepcopy(self.p)

    def save(self,path,body):
        np.savez_compressed(path,**{'p_'+k:v for k,v in self.p.items()},
            mask=self.mask,umask=self.umask,types=self.types,mass=body.mass,
            store=body.store,energy=np.array(body.energy),updates=np.array(self.updates))

    @classmethod
    def load(cls,path,cfg):
        d=np.load(path,allow_pickle=False);net=cls(cfg,0)
        net.p={k:d['p_'+k].copy() for k in net.p}
        net.mask=d['mask'].copy();net.umask=d['umask'].copy();net.types=d['types'].copy()
        net.target=copy.deepcopy(net.p);net.opt=Adam(net.p,cfg.lr);net.updates=int(d['updates'])
        b=net.initial_body();b.mass=d['mass'].copy();b.store=d['store'].copy();b.energy=float(d['energy'])
        return net,b

class Body:
    def __init__(self,cfg,mask,types):
        self.cfg=cfg;self.mask=mask;self.types=types
        self.mass=cfg.initial_mass*mask
        self.store=np.full(cfg.hidden,cfg.initial_store)
        self.energy=cfg.energy_cap

    def observe(self,mode='normal'):
        q=self.mass.sum(0)/self.mask.sum(0)
        return np.array([q[self.types==k].mean() for k in (0,1)]+
            [self.store[self.types==k].mean()/self.cfg.store_cap for k in (0,1)]+
            [self.energy/self.cfg.energy_cap,1. if mode=='lost' else 0.])

    def update(self,action,activity,mode='normal',structural='plastic'):
        cfg=self.cfg;before=self.mass.copy();stores=self.store.copy()
        # Local recurrent activity determines proposed new material, no reward
        # or error gradient enters the biomass rule. Row=source, column=target.
        demand=cfg.growth*(cfg.basal_growth+activity)*(1-self.mass)*self.mask
        if structural=='static':
            demand=np.maximum(0,cfg.initial_mass*self.mask-(1-cfg.decay)*self.mass)
        if structural=='frozen':return dict(mass_added=0.,mass_lost=0.,consumed=0.,external=0.,balance_error=0.,demand_a=0.,demand_b=0.)
        deposited=np.zeros_like(self.store)
        if action in (1,2) and mode!='sham':
            deposited[self.types==action-1]=cfg.deposit
        if mode=='swap':
            deposited[:]=0
            if action in (1,2):deposited[self.types==2-action]=cfg.deposit
        overflow=np.maximum(0,self.store+deposited-cfg.store_cap)
        self.store+=deposited-overflow
        # Equal accounting unit per potential incoming connection at each neuron.
        want=demand.sum(0)/self.mask.sum(0)
        supplied=np.minimum(self.store,want)
        if mode=='rescue':supplied=want.copy()
        ratio=np.divide(supplied,want,out=np.zeros_like(want),where=want>0)
        grown=demand*ratio[None]
        decay=cfg.decay*self.mass
        self.mass=np.clip(self.mass-decay+grown,0,1)*self.mask
        used=supplied if mode!='rescue' else np.zeros_like(supplied)
        self.store-=used
        # No hidden reserve cap/discard: exact store and biomass ledgers.
        err=float(np.max(np.abs(self.store-(stores+deposited-overflow-used))))
        err=max(err,float(np.max(np.abs(self.mass-(before-decay+grown)))))
        return dict(mass_added=float(grown.sum()),mass_lost=float(decay.sum()),
            consumed=float(used.sum()),overflow=float(overflow.sum()),external=float(supplied.sum()) if mode=='rescue' else 0.,
            balance_error=err,demand_a=float(want[self.types==0].sum()),
            demand_b=float(want[self.types==1].sum()))
