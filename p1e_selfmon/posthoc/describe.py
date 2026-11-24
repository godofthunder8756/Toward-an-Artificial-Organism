"""P1e post-hoc descriptives (disclosed; written after the final run was scored; not decisive).

1. Exposure per seed (the validity criterion that failed): PFATE and PYOKED share of clear trials with a
   conflict event, at 1800 and 3600; calibration median for comparison.
2. Whether conflict states settle: share of conflict-probed trials whose decoder margin reaches the
   confident threshold, and how many trials M_conf rests on.
3. Abstention levels per cell (none / same / conflict), early and late.
4. Exposure against monitoring across seeds (Spearman), PFATE and PYOKED.
5. The body referent: drain effect per arm.
Run: python3 p1e_selfmon/posthoc/describe.py > p1e_selfmon/posthoc/describe.log
"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
import run_p1e_selfmon as R  # noqa: E402


def spearmanr(x, y):
    """Spearman rho (average ranks) and a two-sided permutation p (10000 shuffles, fixed seed)."""
    def rank(v):
        v = np.asarray(v, dtype=float)
        o = np.argsort(v, kind="mergesort")
        r = np.empty(len(v))
        r[o] = np.arange(len(v))
        for u in np.unique(v):
            r[v == u] = r[v == u].mean()
        return r
    rx, ry = rank(x), rank(y)
    rho = float(np.corrcoef(rx, ry)[0, 1])
    g = np.random.default_rng(0)
    perm = np.array([np.corrcoef(rx, g.permutation(ry))[0, 1] for _ in range(10000)])
    return rho, float((np.abs(perm) >= abs(rho) - 1e-12).mean())

raw = json.load(open(os.path.join(ROOT, "p1e_selfmon", "raw.json")))
seeds = raw["seeds"]
ARMS = ("PFATE", "PYOKED", "PNOFATE")


def pt_at(s, it):
    return [p for p in s["points"] if p["iters"] == it][0]


def q(x):
    x = np.asarray([v for v in x if v is not None], dtype=float)
    if not len(x):
        return "n/a"
    return f"median {np.median(x):.3f} (IQR {np.percentile(x, 25):.3f}-{np.percentile(x, 75):.3f}; min {x.min():.3f}, max {x.max():.3f}; n {len(x)})"


print("## 1. Exposure per seed (natural share of clear trials with a conflict event)")
for it in (1800, 3600):
    for a in ("PFATE", "PYOKED"):
        v = [pt_at(s, it)["natural"][a]["probes"]["share_conflict"] for s in seeds]
        print(f"{it} {a}: {q(v)}; seeds >= 0.02: {sum(x >= 0.02 for x in v)}/{len(v)}")
for it in (1800, 3600):
    v = [pt_at(s, it)["natural"]["PFATE"]["mean_gain"] for s in seeds]
    b = [pt_at(s, it)["natural"]["PFATE"]["in_band"] for s in seeds]
    print(f"{it} PFATE mean gain {q(v)}; in band {q(b)}")
print("calibration round 1 (seeds 10200-10203, 3600): PFATE share_conflict median 0.032 (0.006-0.039)")

print("\n## 2. Do conflict states settle? Decoder at the report step, 3600")
for at in ("early", "late"):
    for a in ARMS:
        d = [pt_at(s, 3600)[f"decoder_{at}"][a] for s in seeds]
        d = [x for x in d if x.get("fitted")]
        cs = [x["conflict"]["confident_share"] for x in d]
        nc = [x["conflict"]["n_confident"] for x in d]
        ss = [x["same"]["confident_share"] for x in d]
        da = [x["conflict"]["decode_acc"] for x in d]
        print(f"{at} {a}: conflict confident share {q(cs)}; n confident conflict trials {q(nc)}; "
              f"same confident share {q(ss)}; conflict decode acc {q(da)}")

print("\n## 3. Abstention per cell, 3600 (undrained clear trials)")
for at in ("early", "late"):
    for a in ARMS:
        cells = {}
        for c in ("none_plain", "same_plain", "conflict_plain"):
            cells[c] = q([pt_at(s, 3600)[f"split_{at}"][a]["probes"][c]["abstain"] for s in seeds])
        print(f"{at} {a}: " + "; ".join(f"{k} {v}" for k, v in cells.items()))

print("\n## 4. Exposure against monitoring across seeds (Spearman)")
for it in (1800, 3600):
    for a in ("PFATE", "PYOKED"):
        ex = [pt_at(s, it)["natural"][a]["probes"]["share_conflict"] for s in seeds]
        m = [R.measures(pt_at(s, it), a)["M"] for s in seeds]
        ok = [(x, y) for x, y in zip(ex, m) if x is not None and y is not None]
        rho, p = spearmanr(*zip(*ok))
        print(f"{it} {a}: share_conflict vs M rho {rho:.2f} (p {p:.3f}, n {len(ok)})")
ex = [pt_at(s, 3600)["natural"]["PFATE"]["probes"]["share_conflict"] for s in seeds]
m = [R.measures(pt_at(s, 3600), "PFATE")["M"] for s in seeds]
lo = [y for x, y in zip(ex, m) if x < 0.02 and y is not None]
hi = [y for x, y in zip(ex, m) if x >= 0.02 and y is not None]
print(f"3600 PFATE M on seeds with exposure < 0.02: {q(lo)}; >= 0.02: {q(hi)}")

print("\n## 5. Body referent: drain effect per arm")
for it in (1800, 3600):
    for a in ARMS:
        print(f"{it} {a}: {q([R.measures(pt_at(s, it), a)['drain_effect'] for s in seeds])}")
