# Scalar root-count sanity check for z = sigma(beta(a + kappa z - theta)). No agent, no training, no simulation.
# Solved in u = beta(a + kappa z - theta): F(u) = u/beta - (a - theta) - kappa*sigma(u) = 0, u in [beta(a-theta), beta(a-theta+kappa)].
import numpy as np
sig=lambda x: 0.5*(1+np.tanh(0.5*x)); logit=lambda p: np.log(p/(1-p))
def window(b,k,th):
    if b*k<=4: return None
    s=np.sqrt(1-4/(b*k)); zp,zm=(1+s)/2,(1-s)/2
    return th-k*zp+logit(zp)/b, th-k*zm+logit(zm)/b, zm, zp   # (a_lo, a_hi, z-, z+)
def nroots(a,b,k,th,N=400001):
    lo,hi=b*(a-th),b*(a-th+k); pad=1e-9*max(1,abs(lo),abs(hi))
    u=np.linspace(lo-pad,hi+pad,N); F=u/b-(a-th)-k*sig(u)
    sg=np.sign(F); sg=sg[sg!=0]
    return int(np.sum(sg[:-1]!=sg[1:]))
grid=[(1,2,0),(1,3.9,0),(1,4.0,0),(1,4.1,0),(1,5,0),(1,8,0),(4,2,0.5),(4,4,0.5),(10,1,0.3),(10,4,0.3),(2,10,1.0)]
tot=bad=0
for b,k,th in grid:
    w=window(b,k,th)
    avals=np.linspace(w[0]-1,w[1]+1,401) if w else np.linspace(th-k-2,th+2,401)
    mism=[];n3=0
    for a in avals:
        if w and min(abs(a-w[0]),abs(a-w[1]))<1e-6: continue
        n=nroots(a,b,k,th); exp=3 if (w and w[0]<a<w[1]) else 1
        tot+=1; n3+=(n==3)
        if n!=exp: mism.append((round(a,6),n,exp))
    bad+=len(mism)
    ws='none' if not w else f'a_lo={w[0]:.6f} a_hi={w[1]:.6f} width={w[1]-w[0]:.6f} centre={(w[0]+w[1])/2:.6f} theta-kappa/2={th-k/2:.6f} z-={w[2]:.6f} z+={w[3]:.6f}'
    print(f"beta={b} kappa={k} theta={th} beta*kappa={b*k:.2f} {ws} a-points-with-3-roots={n3} mismatches={len(mism)} {mism[:3]}")
print("total a-points",tot,"total mismatches",bad)
