"""Per-seed sign counts and sign-test p for the tight-matching estimates in robust.json (post-hoc)."""
import json
from math import comb
recs = json.load(open("p1f_stage0/posthoc/robust.json"))
def p2(k, n):
    t = sum(comb(n, i) for i in range(0, min(k, n - k) + 1)) / 2 ** n
    return min(1.0, 2 * t)
for a in ("PFATE", "PYOKED"):
    for t in ("early", "late"):
        for k in ("M2_10", "M2_20", "M2_40", "M2_nn"):
            v = [r[f"{a}_{t}"][k] for r in recs if r[f"{a}_{t}"][k] is not None]
            pos, neg = sum(x > 0 for x in v), sum(x < 0 for x in v)
            print(f"{a} {t} {k}: {pos} > 0, {neg} < 0, {len(v) - pos - neg} = 0; sign p {p2(pos, pos + neg):.4f}")
