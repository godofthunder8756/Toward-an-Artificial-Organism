# Exact-enumeration demonstration (Fractions). Theory-only; no learning, no training.
# Trial: X~Bern(1/2). n=3 world bits b_i = X^W_i, W_i~Bern(w). Default read y_i = b_i^N_i, N_i~Bern(e) (agent's own front-end).
# RECHECK: re-read the SAME b with fresh internal noise -> y'. RESAMPLE: fresh world bits b'' read once -> y''.
from fractions import Fraction as F
from itertools import product
import json, sys
n=3
def bern(p,x): return p if x else 1-p
def joint(w,e,action):
    """dict (X, obs tuple) -> prob. obs = y (+ y' or y'')"""
    out={}
    for X in (0,1):
        for W in product((0,1),repeat=n):
            pW=1
            for v in W: pW*=bern(w,v)
            b=tuple(X^v for v in W)
            for N in product((0,1),repeat=n):
                pN=1
                for v in N: pN*=bern(e,v)
                y=tuple(bi^v for bi,v in zip(b,N))
                if action=='none':
                    k=(X,y); out[k]=out.get(k,0)+F(1,2)*pW*pN
                elif action=='recheck':
                    for N2 in product((0,1),repeat=n):
                        p2=1
                        for v in N2: p2*=bern(e,v)
                        y2=tuple(bi^v for bi,v in zip(b,N2))
                        k=(X,y+y2); out[k]=out.get(k,0)+F(1,2)*pW*pN*p2
                elif action=='resample':
                    for W3 in product((0,1),repeat=n):
                        p3=1
                        for v in W3: p3*=bern(w,v)
                        for N3 in product((0,1),repeat=n):
                            p4=1
                            for v in N3: p4*=bern(e,v)
                            y3=tuple(X^a^c for a,c in zip(W3,N3))
                            k=(X,y+y3); out[k]=out.get(k,0)+F(1,2)*pW*pN*p3*p4
    return out
def marg_obs(J):
    m={}
    for (X,o),p in J.items(): m[o]=m.get(o,0)+p
    return m
def acc_given_y(J):
    """E[max_x P(x|obs) | y]*... returns dict y-> (P(y), expected correctness given y) with Bayes decision using TRUE regime."""
    po=marg_obs(J); best={}
    for o,p in po.items():
        p1=J.get((1,o),0); best[o]=max(p1,p-p1)   # prob mass of correct decision at obs o
    res={}
    for o,v in best.items():
        y=o[:n]; a=res.setdefault(y,[0,0]); a[1]+=v
    for (X,o),p in J.items():
        pass
    py={}
    for o,p in po.items(): py[o[:n]]=py.get(o[:n],0)+p
    return {y:(py[y],res[y][1]/py[y]) for y in py}
def tv(A,B):
    keys=set(A)|set(B); return sum(abs(A.get(k,0)-B.get(k,0)) for k in keys)/2
def decide_with(J_true,J_assumed):
    """accuracy when obs come from J_true but decision rule is Bayes under J_assumed"""
    po=marg_obs(J_assumed); dec={o:(1 if J_assumed.get((1,o),0)>=po[o]-J_assumed.get((1,o),0) else 0) for o in po}
    return sum(p for (X,o),p in J_true.items() if dec[o]==X)
def cls(y): return 'unanimous' if len(set(y))==1 else 'split'
def summarize(w,e):
    eps=w+e-2*w*e
    J={a:joint(w,e,a) for a in ('none','recheck','resample')}
    A={a:acc_given_y(J[a]) for a in J}
    byc={}
    for y,(py,acc) in A['none'].items():
        c=cls(y); d=byc.setdefault(c,{'P':0,'none':0,'recheck':0,'resample':0})
        d['P']+=py
        for a in ('none','recheck','resample'): d[a]+=py*A[a][y][1]
    for c,d in byc.items():
        for a in ('none','recheck','resample'): d[a]=d[a]/d['P']
    return eps,J,byc
REP={}
# --- primary illustrative pair: S (system fault) w=1/20,e=1/5 ; E (evidence noise) w=1/5,e=1/20 ---
wS,eS=F(1,20),F(1,5); wE,eE=F(1,5),F(1,20)
epsS,JS,cS=summarize(wS,eS); epsE,JE,cE=summarize(wE,eE)
print('eps S',epsS,'eps E',epsE)
print('D1 TV(X,y) S vs E, no check:',tv(JS['none'],JE['none']))
print('D1 TV(X,y,y\'\') S vs E, resample:',tv(JS['resample'],JE['resample']))
print('D4 TV(X,y,y\') S vs E, recheck:',tv(JS['recheck'],JE['recheck']), '~',float(tv(JS['recheck'],JE['recheck'])))
# per-bit read agreement under recheck
agS=(1-eS)**2+eS**2; agE=(1-eE)**2+eE**2; print('per-bit recheck agreement S',agS,'E',agE)
for name,c in (('S',cS),('E',cE)):
    for k,d in c.items(): print(name,k,'P=',d['P'],'acc none',d['none'],float(d['none']),'recheck',d['recheck'],float(d['recheck']),'resample',d['resample'],float(d['resample']))
REP['primary']={'S':{'w':str(wS),'e':str(eS)},'E':{'w':str(wE),'e':str(eE)},'eps':str(epsS),
  'byclass':{nm:{k:{kk:str(vv) for kk,vv in d.items()} for k,d in c.items()} for nm,c in (('S',cS),('E',cE))}}
# posterior after recheck depends on regime: decision rule mismatch
accS_true=decide_with(JS['recheck'],JS['recheck']); accS_wrong=decide_with(JS['recheck'],JE['recheck'])
accE_true=decide_with(JE['recheck'],JE['recheck']); accE_wrong=decide_with(JE['recheck'],JS['recheck'])
print('D5 post-recheck accuracy, correct vs mismatched regime model: S',accS_true,accS_wrong,'E',accE_true,accE_wrong)
# --- D2/D3: costs and optimal actions; regime-blind vs regime-aware ---
c_r,c_s=F(1,50),F(3,50)   # illustrative costs (reward 1 per correct prediction)
def opt(c):
    vals={'none':c['none'],'recheck':c['recheck']-c_r,'resample':c['resample']-c_s}; return max(vals,key=vals.get),vals
pol={}
for name,c in (('S',cS),('E',cE)):
    for k in ('unanimous','split'):
        a,v=opt(c[k]); pol[(name,k)]=a; print('D2',name,k,'optimal',a,{kk:str(vv) for kk,vv in v.items()})
# regime mixture 1/2-1/2; regime-blind policy picks one action per y-class (any function of first-order posterior, which is identical)
def value(name,k,a):
    c={'S':cS,'E':cE}[name][k]; return {'none':c['none'],'recheck':c['recheck']-c_r,'resample':c['resample']-c_s}[a]
Pk={k:cS[k]['P'] for k in ('unanimous','split')}; assert all(cS[k]['P']==cE[k]['P'] for k in Pk)
aware=sum(Pk[k]*F(1,2)*(value('S',k,pol[('S',k)])+value('E',k,pol[('E',k)])) for k in Pk)
blind_best=sum(Pk[k]*max(F(1,2)*(value('S',k,a)+value('E',k,a)) for a in ('none','recheck','resample')) for k in Pk)
blind_choice={k:max(('none','recheck','resample'),key=lambda a:F(1,2)*(value('S',k,a)+value('E',k,a))) for k in Pk}
print('D3 regime-aware value',aware,float(aware),'best regime-blind',blind_best,float(blind_best),'gap',aware-blind_best,float(aware-blind_best),'blind choices',blind_choice)
REP['costs']={'c_r':str(c_r),'c_s':str(c_s)}; REP['optimal']={f'{a}|{b}':v for (a,b),v in pol.items()}
REP['D3']={'aware':str(aware),'blind':str(blind_best),'gap':str(aware-blind_best),'blind_choice':blind_choice}
# --- grid robustness of D1 (exact invariance) and recheck-value ordering under swap ---
vals=[F(1,20),F(1,10),F(3,20),F(1,5),F(3,10)]
grid=[]
for w in vals:
    for e in vals:
        if w>=e: continue
        a_eps,Ja,ca=summarize(w,e)   # evidence-dominant? here w<e -> system-dominant
        b_eps,Jb,cb=summarize(e,w)
        inv=tv(Ja['none'],Jb['none'])==0 and tv(Ja['resample'],Jb['resample'])==0
        gainA=sum(ca[k]['P']*(ca[k]['recheck']-ca[k]['none']) for k in ca); gainB=sum(cb[k]['P']*(cb[k]['recheck']-cb[k]['none']) for k in cb)
        grid.append((str(w),str(e),inv,float(gainA),float(gainB),gainA>gainB))
ok=all(g[2] and g[5] for g in grid)
print('GRID (w<e system-dominant vs swapped): FO+resample invariance and recheck gain(sys)>gain(evid) in all',len(grid),'pairs:',ok)
for g in grid: print('  w=%s e=%s invariant=%s recheck gain sys-dominant %.5f evid-dominant %.5f'%g[:5])
REP['grid']=grid; REP['grid_all_ok']=ok
json.dump(REP,open('demo_results.json','w'),indent=1,default=str)
