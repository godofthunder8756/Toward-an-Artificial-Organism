"""Independent analytic check of the W-REL reference (R-HAC-MB) at the K_SEP settings.
Written from spec FINAL §0, §3.1, §4.2, §4.4 text only; imports nothing from the PR's wrel package.
Exact rationals. Small: belief nodes = multisets of RECHECK LR classes, T <= 4."""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import json
N=3
W={'S':(F(1,20),F(1,5)),'E':(F(1,5),F(1,20))}   # (w,e)
def eps(z): w,e=W[z]; return w+e-2*w*e
EPS=eps('S'); assert EPS==eps('E')==F(23,100)
# per-bit recheck pattern probabilities given X-bit target t: world bit wb = t xor Bern(w); reads y=wb xor Bern(e), y'=wb xor Bern(e)
def bitp(z,yb,ypb,tb):
    w,e=W[z]; tot=F(0)
    for wb in (0,1):
        pw = (1-w) if wb==tb else w
        py = (1-e) if yb==wb else e
        pyp= (1-e) if ypb==wb else e
        tot+=pw*py*pyp
    return tot
def bits(v): return [(v>>i)&1 for i in range(N)]
Y=range(8)
def split(y): return y not in (0,7)
def Ldef(y,x):  # P(y|X=x), same for both z
    d=sum(b!=x for b in bits(y)); return EPS**d*(1-EPS)**(N-d)
def Lre(z,y,yp,x):
    out=F(1)
    for yb,pb in zip(bits(y),bits(yp)): out*=bitp(z,yb,pb,x)
    return out
def cls(y,yp,x):
    nac=naw=nd=0
    for yb,pb in zip(bits(y),bits(yp)):
        if yb!=pb: nd+=1
        elif yb==x: nac+=1
        else: naw+=1
    return (nac,naw,nd)
CLASSES=sorted({cls(y,yp,x) for y in Y for yp in Y for x in (0,1)})
assert len(CLASSES)==10
# M: fresh world bits read once -> per-bit flip EPS, independent of y given X, same in both z
def LM(y,ypp,x): return Ldef(y,x)*Ldef(ypp,x)
def pred(p): return 1 if p>F(1,2) else 0
# F0 decisions and regime-specific decisions; check A11
def post_x1(lik):  # lik(x) -> joint with prior 1/2
    a=lik(1); b=lik(0); return a/(a+b)
a11=True
for y in Y:
    for yp in Y:
        dz=[pred(post_x1(lambda x,z=z:Lre(z,y,yp,x))) for z in 'SE']
        d0=pred(post_x1(lambda x:Lre('S',y,yp,x)+Lre('E',y,yp,x)))
        a11&= dz[0]==dz[1]==d0
print('A11 (S, E, F0 decisions coincide on 64 recheck patterns):',a11)
dP={y:pred(post_x1(lambda x:Ldef(y,x))) for y in Y}
# gross correctness kappa_a(z,y) = P(d = X | y, z, a)
def kP(y): return F(1,2)*Ldef(y,dP[y])/(F(1,2)*(Ldef(y,0)+Ldef(y,1)))
def kR(z,y):
    num=F(0); den=F(0)
    for x in (0,1):
        for yp in Y:
            p=F(1,2)*Lre(z,y,yp,x); den+=p
            d=pred(post_x1(lambda xx:Lre('S',y,yp,xx)+Lre('E',y,yp,xx)))
            if d==x: num+=p
    return num/den
def kM(y):
    num=den=F(0)
    for x in (0,1):
        for ypp in Y:
            p=F(1,2)*LM(y,ypp,x); den+=p
            d=pred(post_x1(lambda xx:LM(y,ypp,xx)))
            if d==x: num+=p
    return num/den
ysp=3  # a representative split read; check all split reads equal
gP={y:kP(y) for y in Y}; gM={y:kM(y) for y in Y}; gRS={y:kR('S',y) for y in Y}; gRE={y:kR('E',y) for y in Y}
assert len({gP[y] for y in Y if split(y)})==1 and len({gM[y] for y in Y if split(y)})==1
assert len({gRS[y] for y in Y if split(y)})==1 and len({gRE[y] for y in Y if split(y)})==1
print('split read: gP=%s gM=%s kR(S)=%s kR(E)=%s'%(gP[ysp],gM[ysp],gRS[ysp],gRE[ysp]))
print('   decimals: gP=%.6f gM=%.6f kR(S)=%.6f kR(E)=%.6f'%tuple(map(float,(gP[ysp],gM[ysp],gRS[ysp],gRE[ysp]))))
print('unanimous read: gP=%.6f gM=%.6f kR(S)=%.6f kR(E)=%.6f'%tuple(map(float,(gP[0],gM[0],gRS[0],gRE[0]))))
# LR class likelihood per z (constant within class)
Lc={z:{} for z in 'SE'}
for z in 'SE':
    for y in Y:
        for yp in Y:
            for x in (0,1):
                c=cls(y,yp,x); v=Lre(z,y,yp,x)
                assert Lc[z].setdefault(c,v)==v
def belief(node):  # node: tuple of class counts in CLASSES order; b = P(S|history)
    ls=F(1); le=F(1)
    for c,n in zip(CLASSES,node): ls*=Lc['S'][c]**n; le*=Lc['E'][c]**n
    return ls/(ls+le)
def add(node,c):
    l=list(node); l[CLASSES.index(c)]+=1; return tuple(l)
EMPTY=(0,)*10
def setting(T,cr,cs):
    @lru_cache(None)
    def V(t,node):  # value from trial t (1-based) to T, belief node at start of trial t
        if t>T: return F(0)
        b=belief(node); tot=F(0)
        for y in Y:
            py=Ldef(y,0)*F(1,2)+Ldef(y,1)*F(1,2)
            tot+=py*max(Q(t,node,y).values())
        return tot
    @lru_cache(None)
    def Q(t,node,y):
        b=belief(node)
        q={}
        q['P']=gP[y]+V(t+1,node)
        q['M']=gM[y]-cs+V(t+1,node)
        # R: immediate + continuation over class outcomes
        gr=b*gRS[y]+(1-b)*gRE[y]
        cont=F(0)
        # P(class c | y, b) = sum_z b_z sum_{yp,x: cls=c} P(yp,x|y,z)
        py=Ldef(y,0)*F(1,2)+Ldef(y,1)*F(1,2)
        pc={}
        for z,bz in (('S',b),('E',1-b)):
            for yp in Y:
                for x in (0,1):
                    c=cls(y,yp,x); pc[c]=pc.get(c,F(0))+bz*F(1,2)*Lre(z,y,yp,x)/py
        for c,p in pc.items(): cont+=p*V(t+1,add(node,c))
        q['R']=gr-cr+cont
        return q
    def act(t,node,y):
        q=Q(t,node,y); best=max(q.values())
        for a in 'PRM':
            if q[a]==best: return a
    # forward per Z: expected #R, #M on split-read trials; reachable nodes at layer tau
    res={}
    tau=T-2
    layer_nodes={}
    for z in 'SE':
        dist={EMPTY:F(1)}; nR=nM=F(0)
        for t in range(1,T+1):
            nd={}
            for node,p in dist.items():
                for y in Y:
                    py=Ldef(y,0)*F(1,2)+Ldef(y,1)*F(1,2)
                    a=act(t,node,y)
                    if split(y):
                        if a=='R': nR+=p*py
                        if a=='M': nM+=p*py
                    if a=='R':
                        for yp in Y:
                            for x in (0,1):
                                w=p*F(1,2)*Lre(z,y,yp,x)
                                nn=add(node,cls(y,yp,x)); nd[nn]=nd.get(nn,F(0))+w
                    else:
                        nd[node]=nd.get(node,F(0))+p*py
            dist=nd
            if t==tau: layer_nodes[z]=dict(dist)
        res[z]=(nR,nM)
    dR=res['S'][0]-res['E'][0]; dM=res['E'][1]-res['S'][1]
    # donors at layer tau: max / min P(S|history) among reachable nodes (either Z), ties by forward prob
    allnodes={}
    for z in 'SE':
        for n,p in layer_nodes.get(z,{}).items():
            if p>0: allnodes[n]=allnodes.get(n,F(0))+F(1,2)*p
    sd=max(allnodes,key=lambda n:(belief(n),allnodes[n]))
    ed=min(allnodes,key=lambda n:(belief(n),-allnodes[n]))
    # policy summary: does M ever get chosen at any reachable (t,node,split y)?
    actions=set()
    for t in range(1,T+1):
        pass
    return dict(T=T,cr=str(cr),cs=str(cs),ER_S=str(res['S'][0]),EM_S=str(res['S'][1]),ER_E=str(res['E'][0]),EM_E=str(res['E'][1]),
                delta_R=str(dR),delta_M=str(dM),donor_S=list(sd),donor_E=list(ed),act_t1_split=act(1,EMPTY,ysp),
                Q_t1_split={k:str(v) for k,v in Q(1,EMPTY,ysp).items()})
out=[]
for T in (3,4):
    for cr,cs in ((F(1,50),F(3,50)),(F(1,100),F(1,10))):
        r=setting(T,cr,cs); out.append(r)
        print(json.dumps({k:v for k,v in r.items() if k!='Q_t1_split'}))
        print('   Q at t=1, empty node, split read:',{k:round(float(F(v)),6) for k,v in r['Q_t1_split'].items()})
# Structural (any-horizon) dominance of M at (c_r, c_s): M and P leave belief unchanged (L1), R's continuation >= P's
# (information has nonnegative value for the Bayes planner), so M is never chosen at belief b on a split read if
# gM - cs <= max(gP, min_z kR(z) - cr) ... use worst case over b (gR linear in b).
for cr,cs in ((F(1,50),F(3,50)),(F(1,100),F(1,10))):
    worst_R=min(gRS[ysp],gRE[ysp])-cr
    print('c=(%s,%s): gM-cs=%.6f  gP=%.6f  min_b gR(b)-cr=%.6f  -> M myopically dominated at every b: %s'%(cr,cs,float(gM[ysp]-cs),float(gP[ysp]),float(worst_R), gM[ysp]-cs<=max(gP[ysp],worst_R)))
    print('      M dominated by P alone (gM - cs <= gP): %s ; gM-gP = %s (%.6f)'%(gM[ysp]-cs<=gP[ysp], gM[ysp]-gP[ysp], float(gM[ysp]-gP[ysp])))
json.dump(out,open('analytic_reference_out.json','w'),indent=1)
