import numpy as np, itertools
H=np.array([[(h>>k)&1 for k in range(8)] for h in range(256)])
R=2*H-1
pairs=list(itertools.combinations(range(8),2))
X=np.hstack([R,np.stack([R[:,i]*R[:,j] for i,j in pairs],1)])
names=[f"r{i}" for i in range(8)]+[f"r{i}r{j}" for i,j in pairs]
p4=H[:,:4]@np.array([1,2,4,8])
G={'A':{0,5,10,15},'B':{1,4,11,14},'C':{2,7,8,13},'D':{3,6,9,12}}
grp=np.array([[k for k,v in G.items() if p in v][0] for p in p4])
for a,b in [('A','B'),('C','D'),('A','C'),('B','D'),('A','D'),('B','C')]:
    m=np.isin(grp,[a,b]); Z=X[m]; sd=Z.std(0); keep=sd>1e-12
    Zc=Z[:,keep]-Z[:,keep].mean(0)
    rk=np.linalg.matrix_rank(Zc)
    const=[names[i] for i in np.where(~keep)[0]]
    # does fit-set row space contain held-out centered rows? (extrapolation identifiability)
    Zh=X[~m][:,keep]-Z[:,keep].mean(0)
    P=np.linalg.pinv(Zc)@Zc
    resid=np.linalg.norm(Zh-Zh@P)/np.linalg.norm(Zh)
    print(a+b,'kept',keep.sum(),'rank',rk,'const',const,'heldout_rowspace_resid',round(resid,3))
