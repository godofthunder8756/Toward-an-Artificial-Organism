"""Independent replay of SCARCITY_GAP_v1 §5 (branch elminster/loving-ptolemy-ityj4l).
Written from the .md definitions only; the branch script was not read or imported.
World: 3 uniform binary items, observed cleanly. Uniform cue c in {0,1,2}; query q=c w.p. v,
else each other item w.p. (1-v)/2. Answer: reward 1 if correct, else 0; opt-out: sure reward r.
A memory state is identified with a codeword (an action per query): 27 codewords.
Value = E_{x,c} max_{w in codebook} sum_q P(q|c) u(w_q, x_q)   (facility location, exact).
Classes at equal K: full; static (all codewords share one opt-out pattern);
no_opt (no opt-out); cue_blind (encoder sees x only).
Exactness: Fractions -> common-denominator integers -> exhaustive integer max/sum -> Fraction."""
from fractions import Fraction as F
from itertools import product, combinations
from math import lcm
import numpy as np, json, sys

ACT = ['0', '1', '-']
CODES = [''.join(w) for w in product(ACT, repeat=3)]
XS = list(product((0, 1), repeat=3))
VS = [F(1, 3), F(1, 2), F(3, 4)]
RS = [F(1, 2), F(5, 8), F(3, 4)]

def pq(q, c, v): return v if q == c else (1 - v) / 2
def u(a, bit, r): return r if a == '-' else (F(1) if int(a) == bit else F(0))

def tables(v, r):
    # column per (x,c), weight P(x)P(c)=1/24 folded in; cue-blind column per x (cue averaged)
    full = [[F(1, 24) * sum(pq(q, c, v) * u(w[q], x[q], r) for q in range(3))
             for x in XS for c in range(3)] for w in CODES]
    blind = [[F(1, 8) * sum(F(1, 3) * pq(q, c, v) * u(w[q], x[q], r) for c in range(3) for q in range(3))
              for x in XS] for w in CODES]
    return full, blind

def best(table, rows, K):
    """Exact max over codebooks of size min(K,len(rows)) drawn from rows."""
    D = lcm(*{t.denominator for row in table for t in row})
    M = np.array([[int(t * D) for t in table[i]] for i in rows], dtype=np.int64)
    k = min(K, len(rows))
    bestv, bestc = -1, None
    combos = combinations(range(len(rows)), k)
    while True:
        chunk = np.fromiter((i for cmb in _take(combos, 200000) for i in cmb), dtype=np.int64)
        if chunk.size == 0: break
        idx = chunk.reshape(-1, k)
        vals = M[idx].max(axis=1).sum(axis=1)
        j = int(vals.argmax())
        if vals[j] > bestv: bestv, bestc = int(vals[j]), [CODES[rows[i]] for i in idx[j]]
    return F(bestv, D), bestc

def _take(it, n):
    for _ in range(n):
        try: yield next(it)
        except StopIteration: return

def patt(w): return tuple(i for i in range(3) if w[i] == '-')

out = []
ALL = list(range(27))
for v in VS:
    for r in RS:
        full, blind = tables(v, r)
        for K in range(1, 9):
            f, fc = best(full, ALL, K)
            st = max((best(full, [i for i in ALL if patt(CODES[i]) == p], K) for p in
                      {patt(w) for w in CODES}), key=lambda t: t[0])
            no, _ = best(full, [i for i in ALL if '-' not in CODES[i]], K)
            cb, _ = best(blind, ALL, K)
            out.append(dict(v=str(v), r=str(r), K=K, full=str(f), static=str(st[0]), no_opt=str(no),
                            cue_blind=str(cb), access=str(f - st[0]), selection=str(f - cb),
                            codebook=' '.join(sorted(fc))))
            print(out[-1], flush=True)
json.dump(out, open('replay_results.json', 'w'), indent=1)
sc = [o for o in out if o['K'] < 8]
acc = [F(o['access']) for o in sc]; sel = [F(o['selection']) for o in sc]
print('max access (K<8):', max(acc), ' cells>0:', sum(a > 0 for a in acc), '/', len(sc))
print('max selection (K<8):', max(sel), ' cells>0:', sum(s > 0 for s in sel), '/', len(sc))
print('both>0:', sum(a > 0 and s > 0 for a, s in zip(acc, sel)))
print('K=8 collapse (full==1, access==sel==0):', all(o['full'] == '1' and o['access'] == '0' and o['selection'] == '0' for o in out if o['K'] == 8))
print('access>0 at K in {1,2,4} or r=1/2:', [ (o['v'],o['r'],o['K']) for o,a in zip(sc,acc) if a>0 and (o['K'] in (1,2,4) or o['r']=='1/2')])
print('selection>0 at v=1/3:', [(o['r'],o['K']) for o,s in zip(sc,sel) if s>0 and o['v']=='1/3'])
