# Read-only feasibility check: numpy GRU-8 forward, harness reproduction, gradient geometry only.
# No training. No control path is constructed or evaluated.
import sys, json, base64, numpy as np
CL='/workspace/scratch/pr8/clone'; sys.path.insert(0, CL)
from twostream_acquisition_oracle import World
q = np.asarray(World().q, float)
def load(path):
    p=json.load(open(path)); return {k: np.frombuffer(base64.b64decode(v['data_b64']),dtype=np.dtype(v['dtype'])).reshape(v['shape']).astype(np.float64) for k,v in p.items()}
bits = np.array([[(h>>s)&1 for s in range(8)] for h in range(256)], float)
sig = lambda x: 1/(1+np.exp(-x))
def forward(st, Whh_late=None):
    Wih, Whh, bih, bhh = st['rnn.weight_ih_l0'], st['rnn.weight_hh_l0'], st['rnn.bias_ih_l0'], st['rnn.bias_hh_l0']
    h = np.zeros((256,8))
    for s in range(8):
        x = np.zeros((256,9)); x[:,0]=bits[:,s]*2-1; x[:,1+s]=1
        W = Whh_late if (Whh_late is not None and s>=4) else Whh
        gi = x@Wih.T + bih; gh = h@W.T + bhh
        r = sig(gi[:,0:8]+gh[:,0:8]); z = sig(gi[:,8:16]+gh[:,8:16]); n = np.tanh(gi[:,16:24]+r*gh[:,16:24])
        h = (1-z)*n + z*h
    return sig(np.tanh(h@st['readout_fc1.weight'].T+st['readout_fc1.bias'])@st['readout_fc2.weight'].T+st['readout_fc2.bias'])
def grid(a): return np.transpose(a.reshape(16,16,3),(1,0,2))
Q = grid(q)
def Lp(f):
    F=grid(f); d=(F-F.mean(0,keepdims=True))-(Q-Q.mean(0,keepdims=True)); return float(np.mean(np.sum(d*d,-1)))
PD = Lp(np.repeat(q.reshape(16,16,3).mean(1,keepdims=True),16,1).reshape(256,3)*0 + np.tile(q.reshape(16,16,3).mean(1)[:,None,:],(1,16,1)).reshape(256,3))
def grad(st, W):
    g = np.zeros_like(W); h=1e-6
    for i in range(24):
        for j in range(8):
            E=np.zeros_like(W); E[i,j]=h
            g[i,j]=(Lp(forward(st,W+E))-Lp(forward(st,W-E)))/(2*h)
    return g
BL={'r':(0,8),'z':(8,16),'n':(16,24)}
out={}
pr8=json.load(open(CL+'/graded_reversion_results_v1/phase_b_results.json'))
pr8a=json.load(open(CL+'/graded_reversion_phaseA_exploratory/phase_a_results.json'))
recs={r['seed']:r['evaluation'] for r in pr8['seeds']}
for r in pr8a['seeds']: recs[r['seed']]=r['evaluation'] if 'evaluation' in r else r
for seed in list(range(100,110))+list(range(200,210)):
    d0 = CL+('/recurrent_core_results_v1/checkpoints' if seed<200 else '/graded_reversion_results_v1/checkpoints')
    ft=load(f'{d0}/s{seed}_f_trained.ckpt'); ci=load(f'{d0}/s{seed}_cand_init.ckpt')
    WT=ft['rnn.weight_hh_l0']; W0=ci['rnn.weight_hh_l0']; D=W0-WT
    f=forward(ft); L0=Lp(f); fs=forward(ft,WT.copy())
    ev=recs[seed]
    ref=ev['intact_outcomes']['L_prefix']
    tg=ev['targets']['weight_hh']
    rev18=Lp(forward(ft,WT+0.125*D))-L0; rev1=Lp(forward(ft,W0))-L0
    g=grad(ft,WT)
    # directional FD check along d-hat and along gradient
    dh=D/np.linalg.norm(D); hh=1e-6
    dd=(Lp(forward(ft,WT+hh*dh))-Lp(forward(ft,WT-hh*dh)))/(2*hh)
    row=dict(L_intact_np=L0, L_intact_committed=ref, L_gap=abs(L0-ref), sham_gap=float(np.max(abs(fs-f))),
             rev18_np=rev18, rev18_committed=tg['delta_rev'][1], rev1_np=rev1, rev1_committed=tg['delta_rev'][5],
             dirderiv_fd=dd, dirderiv_grad=float(np.sum(g*dh)))
    tot_r2=0
    for k,(a,b) in BL.items():
        gk=g[a:b].ravel(); dk=D[a:b].ravel()
        ak=gk@dk/(gk@gk); rk=np.linalg.norm(dk-ak*gk); tot_r2+=rk**2
        row[k]=dict(gnorm=float(np.linalg.norm(gk)), dnorm=float(np.linalg.norm(dk)), a=float(ak),
                    cos=float(gk@dk/np.linalg.norm(gk)/np.linalg.norm(dk)), rho=float(rk/np.linalg.norm(dk)),
                    gd=float(gk@dk), gd_scale=float(np.linalg.norm(gk)*np.linalg.norm(dk)),
                    rho_formula=float(np.sqrt(max(dk@dk-ak**2*(gk@gk),0))/np.linalg.norm(dk)))
    gf=g.ravel(); df=D.ravel()
    row['full']=dict(cos=float(gf@df/np.linalg.norm(gf)/np.linalg.norm(df)), R_over_d=float(np.sqrt(tot_r2)/np.linalg.norm(df)),
                     gd=float(gf@df), FO_auc=float(gf@df/2), auc_rev_committed=tg['auc_rev'],
                     gnorm=float(np.linalg.norm(gf)))
    out[seed]=row
    print(seed, f"Lgap={row['L_gap']:.1e} rev18 {rev18:.6e}/{tg['delta_rev'][1]:.6e} rev1 {rev1:.6e}/{tg['delta_rev'][5]:.6e} dd {dd:.6e}/{row['dirderiv_grad']:.6e}",
          ' '.join(f"{k}:cos={row[k]['cos']:+.3f},rho={row[k]['rho']:.3f},|g||d|={row[k]['gd_scale']:.2e}" for k in BL),
          f"full cos={row['full']['cos']:+.3f} R/d={row['full']['R_over_d']:.3f}", flush=True)
print('PD',PD)
json.dump(out,open('feasibility.json','w'),indent=1)
