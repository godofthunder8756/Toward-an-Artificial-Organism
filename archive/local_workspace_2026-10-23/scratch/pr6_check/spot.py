"""Independent spot checks for PR #6 (scarcity_v2 certificate). Written from SCARCITY_V2 FINAL definitions;
PR code not read or imported. Exact Fractions throughout."""
from fractions import Fraction as F
from itertools import product, combinations
from math import lcm
import numpy as np, json
ACT=['0','1','-']; CODES=[''.join(w) for w in product(ACT,repeat=3)]
XS=list(product((0,1),repeat=3)); NS=list(product((0,1,2),repeat=3))
def pq(q,c,v): return v if q==c else (1-v)/2
# ---------- evidence models: list of (e, P(e), post[i]=P(x_i=1|e)) ----------
def clean(): return [(x,F(1,8),[F(b) for b in x]) for x in XS]
def graded(a):
    a=F(a); pn={0:(a*a+(1-a)**2)/2,1:2*a*(1-a),2:(a*a+(1-a)**2)/2}
    # n_i = number of looks reporting 1
    post={2:a*a/(a*a+(1-a)**2),1:F(1,2),0:(1-a)**2/(a*a+(1-a)**2)}
    return [(n,pn[n[0]]*pn[n[1]]*pn[n[2]],[post[k] for k in n]) for n in NS]
def u(act,p1,r): return r if act=='-' else (p1 if act=='1' else 1-p1)
# ---------- unpaid S-DIRECT facility location ----------
def tables(ev,v,r):
    full=[[pe*F(1,3)*sum(pq(q,c,v)*u(w[q],po[q],r) for q in range(3)) for (e,pe,po) in ev for c in range(3)] for w in CODES]
    blind=[[pe*sum(F(1,3)*pq(q,c,v)*u(w[q],po[q],r) for c in range(3) for q in range(3)) for (e,pe,po) in ev] for w in CODES]
    return full,blind
def best(table,rows,K):
    D=lcm(*{t.denominator for row in table for t in row})
    M=np.array([[int(t*D) for t in table[i]] for i in rows],dtype=np.int64)
    k=min(K,len(rows)); bv=-1
    cs=list(combinations(range(len(rows)),k))
    for s in range(0,len(cs),200000):
        idx=np.array(cs[s:s+200000],dtype=np.int64)
        bv=max(bv,int(M[idx].max(axis=1).sum(axis=1).max()))
    return F(bv,D)
def patt(w): return tuple(i for i in range(3) if w[i]=='-')
def unpaid(ev,v,r,K):
    full,blind=tables(ev,v,r); ALL=list(range(27))
    f=best(full,ALL,K); cb=best(blind,ALL,K)
    st=max(best(full,[i for i in ALL if patt(CODES[i])==p],K) for p in {patt(w) for w in CODES})
    return f,cb,st
# ---------- ROUTE (S-MSG), one consumer, query law pq(.,c,v) ----------
def route(ev,v,r,L):
    best_full=best_static=F(-1); nf=ns=0
    for dec in product(ACT,repeat=3*L):  # dec[m*3+q]
        vf=vs=F(0)
        for (e,pe,po) in ev:
            vals=[[sum(pq(q,c,v)*u(dec[m*3+q],po[q],r) for q in range(3)) for m in range(L)] for c in range(3)]
            vf+=pe*F(1,3)*sum(max(row) for row in vals)
            vs+=pe*F(1,3)*max(sum(vals[c][m] for c in range(3)) for m in range(L))
        if vf>best_full: best_full,nf=vf,1
        elif vf==best_full: nf+=1
        if vs>best_static: best_static,ns=vs,1
        elif vs==best_static: ns+=1
    return best_full,best_static,nf,ns
# ---------- UPK stage A, ample K (field values, D-set) ----------
def fieldval(p,isD,r,d):
    conf=max(p,1-p); return max(conf,r) if isD else max((1-d)*conf+d*r,r)
def upk(ev,v,r,d,B):
    Ds=list(combinations(range(3),B))
    def val(Dsel):  # Dsel(e,c)->D
        return sum(pe*F(1,3)*sum(pq(q,c,v)*fieldval(po[q],q in Dsel(e,c),r,d) for q in range(3)) for (e,pe,po) in ev for c in range(3))
    vf=sum(pe*F(1,3)*max(sum(pq(q,c,v)*fieldval(po[q],q in D,r,d) for q in range(3)) for D in Ds) for (e,pe,po) in ev for c in range(3))
    vfix=max(val(lambda e,c,D=D:D) for D in Ds)
    vcb=sum(pe*max(sum(F(1,3)*pq(q,c,v)*fieldval(po[q],q in D,r,d) for c in range(3) for q in range(3)) for D in Ds) for (e,pe,po) in ev)
    return vf,vfix,vcb
out={}
def rec(k,val): out[k]=str(val); print(k,val,flush=True)
# unpaid clean, full grid K in {1,2,3,4,6,8}
for v in (F(1,3),F(3,4)):
  for r in (F(5,8),F(3,4)):
    for K in (1,2,3,4,6,8):
      f,cb,st=unpaid(clean(),v,r,K); rec(f"unpaid/clean/r={r}/v={v}/K={K}",(f,cb,st,f-cb,f-st))
# unpaid graded a=3/4 small K
for v in (F(1,3),F(3,4)):
  for r in (F(5,8),F(3,4)):
    for K in (1,2,3,4):
      f,cb,st=unpaid(graded(F(3,4)),v,r,K); rec(f"unpaid/graded/a=3/4/r={r}/v={v}/K={K}",(f,cb,st,f-cb,f-st))
# ROUTE clean L=2,3 and graded a=3/4 L=2
for r in (F(5,8),F(3,4)):
  for v in (F(1,3),F(3,4)):
    for L in (1,2,3):
      f,s,nf,ns=route(clean(),v,r,L); rec(f"route/clean/r={r}/v={v}/L={L}",(f,s,f-s,nf,ns))
for r in (F(5,8),F(3,4)):
  f,s,nf,ns=route(graded(F(3,4)),F(3,4),r,2); rec(f"route/graded/a=3/4/r={r}/v=3/4/L=2",(f,s,f-s,nf,ns))
# UPK ample
for B in (0,1,2,3):
  for v in (F(1,3),F(3,4)):
    for r in (F(5,8),F(3,4)):
      for d in (F(1,2),F(1,4)):
        vf,vfix,vcb=upk(clean(),v,r,d,B); rec(f"upk/clean/B={B}/d={d}/v={v}/r={r}",(vf,vfix,vcb,vf-vfix,vf-vcb))
for d in (F(1,2),F(1,4)):
  vf,vfix,vcb=upk(graded(F(3,4)),F(1,3),F(3,4),d,1); rec(f"upk/graded/a=3/4/B=1/d={d}/v=1/3/r=3/4",(vf,vfix,vcb,vf-vfix,vf-vcb))
# ADAPT zero values (B=1, v=r=3/4, d=1/2): regime-known vs iid regime (q=c or c+1 law, each w.p. 1/2)
d=F(1,2); r=F(3,4); fv=lambda P: max(sum(P[q]*(1 if q==j else 1-d*(1-r)) for q in range(3)) for j in range(3))
rec("adapt/known",fv([F(3,4),F(1,8),F(1,8)]))
rec("adapt/iid",fv([(F(3,4)+F(1,8))/2,(F(1,8)+F(3,4))/2,F(1,8)]))
json.dump(out,open('spot_results.json','w'),indent=1)
