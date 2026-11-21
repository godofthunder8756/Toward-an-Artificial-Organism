"""P3 post-hoc descriptive checks (disclosed; not confirmatory). Reads p3_global/raw.json only; runs no network.

    python p3_global/posthoc/describe.py > p3_global/posthoc/describe.log
"""
import json
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import run_p3_global as R
from run_trackc_probe import fmt


def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    for k, i in enumerate(o):
        r[i] = float(k)
    return r


def spearman(x, y):
    rx, ry = rank(x), rank(y)
    mx, my = st.mean(rx), st.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else None


d = json.load(open(os.path.join(os.path.dirname(__file__), "..", "raw.json")))["seeds"]
use = [s for s in d if R.phase1_usable(s)]
print("== (1) excluded seeds: phase-1 clear correct / unclear-minus-clear abstention, per type")
for s in d:
    if not R.phase1_usable(s):
        p = s["phase1"]["PLAIN"]["probes"]
        print(s["seed"], "  ".join(f"{t} {fmt(R.clear_correct_t(p[t]))}/{fmt(p[t]['unclear_plain']['abstain'] - p[t]['clear_plain']['abstain'])}"
                                   for t in R.TYPES))
print("\n== (2) sensitivity: every test on all 28 seeds (no usability rule), 3600")
sp = R.score_point(d, 1, 2)
for k in ("P3_0_referent", "P3_1", "P3_2", "P3_3"):
    print(k, R._pt(sp[k]))
print("transfer ratio", fmt(sp["transfer_ratio_PFATE"]), "| C worse PFATE vs PYOKED", R._pt(sp["secondary"]["C_worse_PFATE_vs_PYOKED"]))
print("\n== (3) steering, usable seeds, 3600: medians of the steered-minus-unsteered effect, A direction and random")
for arm in ("PFATE", "PYOKED", "PNOFATE"):
    for t in R.TYPES:
        a = [s["points"][1]["steer"][arm]["steer"][t]["effect"] for s in use]
        b = [s["points"][1]["steer"][arm]["random"][t]["effect"] for s in use]
        print(f"{arm:8s} {t}  A-direction {fmt(R.med(a))}  random {fmt(R.med(b))}")
print("\n== (4) PFATE worse effects per usable seed, 3600 (A, B, C) and rank correlations")
rows = [(s["seed"], *(R.worse_effect(s["points"][1], "PFATE", t) for t in R.TYPES)) for s in use]
for r in rows:
    print(r[0], *(fmt(x) for x in r[1:]))
A, B, C = ([r[k] for r in rows] for k in (1, 2, 3))
print("spearman A-B", fmt(spearman(A, B)), " A-C", fmt(spearman(A, C)), " B-C", fmt(spearman(B, C)))
print("\n== (5) where in the trial: PFATE worse effect by cue-step reading bin (median over usable seeds, 3600)")
for t in R.TYPES:
    out = []
    for b in ("low", "in_low", "in_high", "high"):
        v = []
        for s in use:
            c = s["points"][1]["probe_worse"]["PFATE"]["probes"][t]["clear_by_xcue"]
            x, y = c[f"{b}_drained"], c[f"{b}_plain"]
            if x["abstain"] is not None and y["abstain"] is not None:
                v.append(x["abstain"] - y["abstain"])
        out.append(f"{b} {fmt(R.med(v))}")
    print(t, "  ".join(out))
print("\n== (6) plain clear abstention (baseline) per type, usable seeds, 3600")
for arm in ("PFATE", "PYOKED", "PNOFATE"):
    print(arm, "  ".join(f"{t} {fmt(R.med(R.cell(s['points'][1], 'probe_worse', arm, t, 'clear_plain') for s in use))}" for t in R.TYPES))
print("\n== (7) natural running, usable seeds, 3600: clear-trial abstention per type (all reliabilities pooled) and in-band time")
for arm in ("PFATE", "PYOKED", "PNOFATE"):
    print(arm, "  ".join(f"{t} {fmt(R.med(R.cell(s['points'][1], 'natural', arm, t, 'clear_plain') for s in use))}" for t in R.TYPES),
          " in band", fmt(R.med(s["points"][1]["natural"][arm]["in_band"] for s in use)))
print("\n== (8) natural running: clear-trial abstention by implied reliability (r = 1 | 0.6-1 | < 0.6), usable seeds, 3600")
for arm in ("PFATE", "PYOKED"):
    for t in R.TYPES:
        b = lambda s: s["points"][1]["natural"][arm]["probes"][t]["clear_by_rel"]
        cols = []
        for j in ((0,), (1,), (2, 3)):
            v = []
            for s in use:
                cs = [b(s)[k] for k in j if b(s)[k]["n"]]
                n = sum(c["n"] for c in cs)
                if n:
                    v.append(sum(c["abstain"] * c["n"] for c in cs) / n)
            cols.append(fmt(R.med(v)))
        print(f"{arm:8s} {t}  " + " | ".join(cols))
