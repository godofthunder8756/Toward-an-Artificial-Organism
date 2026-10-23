# Read-only: parameter counts, init pairing, and T(theta) of EXISTING checkpoints (no training).
import sys, json, base64, numpy as np, torch
CL='/workspace/scratch/pr9/clone'; sys.path.insert(0, CL)
from recurrent_core_transfer_models import CoreGRU, build_initialized
from twostream_acquisition_oracle import World
from twostream_acquisition_metrics import component_excess
torch.set_num_threads(1)
print("== parameter counts ==")
for H in (32,48,70):
    m=CoreGRU(H); P={n:p.numel() for n,p in m.named_parameters()}
    rec=sum(v for k,v in P.items() if k.startswith('rnn')); ro=sum(v for k,v in P.items() if k.startswith('readout'))
    hh=P['rnn.weight_hh_l0']
    print(f"H={H}: per-tensor {P}; recurrent {rec}, readout {ro} (=12H+3={12*H+3}), total {rec+ro}; R-FIX trainable (total - weight_hh {hh}) = {rec+ro-hh}")
print("== init pairing: build_initialized(s,32) vs (s,48) ==")
for s in (400,409):
    a=dict(build_initialized(s,32).named_parameters()); b=dict(build_initialized(s,48).named_parameters())
    for k in a:
        A=a[k].detach(); B=b[k].detach()
        if A.shape==B.shape: print(s,k,'identical' if torch.equal(A,B) else 'DIFFERENT')
        else:
            sl=tuple(slice(0,n) for n in A.shape) if A.dim()==B.dim() else None
            eqsub = torch.equal(A, B[:A.shape[0]]) if k=='readout_fc1.weight' else None
            print(s,k,'shape',tuple(A.shape),'vs',tuple(B.shape), '| first-32-rows equal' if eqsub else ('| first rows differ' if eqsub is False else ''))
# readout init distribution parity: fc2 fan_in differs (32 vs 48) -> bound differs
print("fc2 init bound 1/sqrt(32)=%.4f vs 1/sqrt(48)=%.4f"%(32**-0.5,48**-0.5))
print("== T(theta) of existing checkpoints (tau=0.25) ==")
w=World(); q=np.asarray(w.q,float)
thrT=float(w.afit_threshold['TEST']['total']); thrX=float(w.afit_threshold['TEST']['XOR'])
print('A-FIT TEST thresholds total %.6g XOR %.6g'%(thrT,thrX))
bits=np.array([[(h>>s)&1 for s in range(8)] for h in range(256)],float)
def load(p):
    P=json.load(open(p)); return {k:np.frombuffer(base64.b64decode(v['data_b64']),dtype=np.dtype(v['dtype'])).reshape(v['shape']).astype(np.float64) for k,v in P.items()}
sig=lambda x:1/(1+np.exp(-x))
def fwd(st):
    Wih,Whh,bih,bhh=st['rnn.weight_ih_l0'],st['rnn.weight_hh_l0'],st['rnn.bias_ih_l0'],st['rnn.bias_hh_l0']; h=np.zeros((256,8))
    for s in range(8):
        x=np.zeros((256,9)); x[:,0]=bits[:,s]*2-1; x[:,1+s]=1; gi=x@Wih.T+bih; gh=h@Whh.T+bhh
        r=sig(gi[:,:8]+gh[:,:8]); z=sig(gi[:,8:16]+gh[:,8:16]); n=np.tanh(gi[:,16:]+r*gh[:,16:]); h=(1-z)*n+z*h
    return sig(np.tanh(h@st['readout_fc1.weight'].T+st['readout_fc1.bias'])@st['readout_fc2.weight'].T+st['readout_fc2.bias'])
grid=lambda a: np.transpose(a.reshape(16,16,3),(1,0,2)); Q=grid(q)
def Lp(f):
    F=grid(f); d=(F-F.mean(0,keepdims=True))-(Q-Q.mean(0,keepdims=True)); return float(np.mean(np.sum(d*d,-1)))
PD=Lp(np.tile(q.reshape(16,16,3).mean(1)[:,None,:],(1,16,1)).reshape(256,3))
print('PD',PD)
def T(st):
    f=fwd(st); e=component_excess(f,w)['TEST']; l=Lp(f)
    return max(l/(0.25*PD), e['total']/thrT, e['XOR']/thrX), l/PD, e['total']/thrT, e['XOR']/thrX
rows={}
for grp,ss,d in (('PR7',range(100,110),'recurrent_core_results_v1/checkpoints'),('PR8',range(200,210),'graded_reversion_results_v1/checkpoints'),('PR9',range(300,310),'first_order_control_results_v1/checkpoints')):
    for arm in ('cand_final','f_trained','f_init','cand_init'):
        vals=[T(load(f'{CL}/{d}/s{s}_{arm}.ckpt')) for s in ss]
        a=np.array(vals); rows[f'{grp}_{arm}']=a.tolist()
        print(f"{grp} {arm:10s} T range {a[:,0].min():.3f}-{a[:,0].max():.3f}  T<=1: {int((a[:,0]<=1).sum())}/10 | L/PD {a[:,1].min():.3f}-{a[:,1].max():.3f} | Etot/thr {a[:,2].min():.3f}-{a[:,2].max():.3f} | Exor/thr {a[:,3].min():.3f}-{a[:,3].max():.3f}")
json.dump(rows,open('T_existing.json','w'),indent=1)
