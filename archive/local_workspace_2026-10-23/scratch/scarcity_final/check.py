# Exact checks for Consult #10 edits 1 and 4 (clean, v=r=3/4, delta=1/2, uniform cue, S-DIRECT).
from fractions import Fraction as F
from itertools import product, combinations
v,r,d=F(3,4),F(3,4),F(1,2)
XS=list(product((0,1),repeat=3)); C=range(3)
pq=lambda q,c: v if q==c else (1-v)/2
PAIRS=[frozenset(p) for p in combinations(range(3),2)]
# Edit 1: per x, choose a pair containing c for every c; min distinct pairs per x
best=min(len({pc for pc in choice}) for choice in product(*[[p for p in PAIRS if c in p] for c in C]))
print('min distinct durable pairs per x:',best,'-> I-phase lower bound',8*best)
pol={0:frozenset({0,1}),1:frozenset({0,1}),2:frozenset({0,2})}
I={(x,pol[c]) for x in XS for c in C}
Q=set()
for x in XS:
  for c in C:
    D=pol[c]; frag=[i for i in range(3) if i not in D]
    for er in product((0,1),repeat=len(frag)):
      f=list(x)
      for i,e in zip(frag,er):
        if e: f[i]='-'
      Q.add(tuple(f))
print('two-fixed-pair policy: I =',len(I),' Q =',len(Q))
def value(Dfun):
  V=F(0)
  for x in XS:
    for c in C:
      D=Dfun(x,c)
      for q in range(3):
        val=F(1) if q in D else (1-d)*1+d*r
        V+=F(1,8)*F(1,3)*pq(q,c)*val
  return V
V2=value(lambda x,c:pol[c]); print('V(two-pair, B=2) =',V2,' expected 63/64:',V2==F(63,64))
# Edit 4: B=1, full D={c}
V1=value(lambda x,c:{c})
Vcued=value(lambda x,c:set())               # downgrade cued field c every episode
Vfixed=value(lambda x,c:set() if c==0 else {c})  # downgrade fixed field j=0 whenever durable
print('V_full(B=1)=',V1,' dV cued-every-episode =',Vcued-V1,' dV fixed-field-j=0 =',Vfixed-V1)
