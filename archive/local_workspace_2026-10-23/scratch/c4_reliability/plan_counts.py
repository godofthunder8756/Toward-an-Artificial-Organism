# Planning-only: count distinct recheck likelihood-ratio classes (for compute estimates). Not the admission check.
from fractions import Fraction as F
from itertools import product
from math import comb
import io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import demo as D
JS,JE=D.JS['recheck'],D.JE['recheck']
LR={}
for k,p in JS.items():
    q=JE[k]; LR.setdefault(p/q,[]).append(k)
print('recheck (X,y,y\') patterns:',len(JS),'distinct LR values:',len(LR))
for T in (5,8,10,12):
    L=len(LR)
    print('T=%d h=0 cumulative belief nodes <= C(T+L,L)=%d ; last layer <= %d ; h>0 worst sum (L+1)^t = %d'%(T,comb(T+L,L),comb(T+L-1,L-1),sum((L+1)**t for t in range(T+1))))
for T in (6,8,10):
    print('R-CG count states cumulative to T=%d: C(T+12,12)=%d'%(T,comb(T+12,12)))
