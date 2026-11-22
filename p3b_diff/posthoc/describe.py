"""P3b post-hoc descriptive checks (disclosed; not confirmatory). Reads p3b_diff/raw.json only; runs no network.

    python p3b_diff/posthoc/describe.py > p3b_diff/posthoc/describe.log
"""
import json
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import run_p3b_diff as R
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


def _pt(t):
    return f"{t['label']} ({t.get('n_pos', t.get('k', '?'))}/{t.get('n', '?')}, p {fmt(t.get('p'), 4)})" if t else "n/a"


d = json.load(open(os.path.join(os.path.dirname(__file__), "..", "raw.json")))["seeds"]
use = [s for s in d if R.phase1_usable(s)]
I = 1  # 3600, primary

print("== (1) excluded seeds: phase-1 clear correct / unclear-minus-clear abstention, per type")
for s in d:
    if not R.phase1_usable(s):
        p = s["phase1"]["PLAIN"]["probes"]
        print(s["seed"], "  ".join(f"{t} {fmt(R.clear_correct_t(p[t]))}/{fmt(p[t]['unclear_plain']['abstain'] - p[t]['clear_plain']['abstain'])}"
                                   for t in R.TYPES))

print("\n== (2) sensitivity: preconditions and primary tests on all 28 seeds (no usability rule), 3600")
sp = R.score_point(d, I, 2)
for k in ("P3B_0_referent_A", "P3B_0_referent_C", "P3B_1", "P3B_2", "P3B_A", "P3B_C"):
    print(k, sp[k]["label"], {kk: sp[k][kk] for kk in sp[k] if kk not in ("label",)})
print("C_low PFATE vs PYOKED", sp["secondary"]["C_low_PFATE_vs_PYOKED"]["label"], "| S median", fmt(sp["selectivity_PFATE"]))

print("\n== (3) per usable seed, PFATE, 3600: the four look cells, unprobed clear abstention (baseline) and exposure")
print("seed    A_low  A_high  C_low  C_high | base_A base_C (look_low eval) | PYOKED base_A base_C | exposure A C")
rows = []
for s in use:
    pt = s["points"][I]
    e = R.parts(pt, "PFATE")
    bA = R.cell(pt, "probe_look_low", "PFATE", "A", "clear_plain")
    bC = R.cell(pt, "probe_look_low", "PFATE", "C", "clear_plain")
    yA = R.cell(pt, "probe_look_low", "PYOKED", "A", "clear_plain")
    yC = R.cell(pt, "probe_look_low", "PYOKED", "C", "clear_plain")
    nat = pt["natural"]["PFATE"]
    rows.append((s["seed"], e["A_low"], e["A_high"], e["C_low"], e["C_high"], bA, bC))
    print(s["seed"], *(fmt(x) for x in (e["A_low"], e["A_high"], e["C_low"], e["C_high"])), "|", fmt(bA), fmt(bC), "|",
          fmt(yA), fmt(yC), "|", fmt(R.exposure_t(nat, "A")), fmt(R.exposure_t(nat, "C")))
col = lambda k: [r[k] for r in rows]
print("medians: A_low", fmt(st.median(col(1))), "A_high", fmt(st.median(col(2))), "C_low", fmt(st.median(col(3))),
      "C_high", fmt(st.median(col(4))), "| baseline A", fmt(st.median(col(5))), "C", fmt(st.median(col(6))))

print("\n== (4) what carries the C half (C_high - C_low) in PFATE, 3600")
ch, cl = col(4), col(3)
print("seeds with C_high > 0:", sum(x > 0 for x in ch), "| with C_low < 0:", sum(x < 0 for x in cl), "of", len(rows))
print("median C_high", fmt(st.median(ch)), "| median -C_low", fmt(st.median([-x for x in cl])))
print("share of the C half from -C_low (median over seeds with C half > 0):",
      fmt(st.median([-l / (h - l) for h, l in zip(ch, cl) if h - l > 0])))
print("C_low as a fraction of the baseline it can remove (C_low / base_C, median):",
      fmt(st.median([l / b for l, b in zip(cl, col(6)) if b and b > 0])))

print("\n== (5) the same on A: what carries the A half (A_low - A_high)")
al, ah = col(1), col(2)
print("seeds with A_low > 0:", sum(x > 0 for x in al), "| with A_high < 0:", sum(x < 0 for x in ah))
print("share of the A half from -A_high (median over seeds with A half > 0):",
      fmt(st.median([-h / (l - h) for l, h in zip(al, ah) if l - h > 0])))

print("\n== (6) rank correlations across usable seeds (PFATE, 3600)")
for name, x, y in (("A_low vs -C_low", al, [-v for v in cl]), ("A_low vs C_high", al, ch),
                   ("-A_high vs -C_low", [-v for v in ah], [-v for v in cl]), ("A_low vs -A_high", al, [-v for v in ah]),
                   ("C_high vs -C_low", ch, [-v for v in cl])):
    print(f"spearman {name}: {fmt(spearman(x, y))}")

print("\n== (7) same cells at 1800 (median over usable seeds, PFATE)")
for k in ("A_low", "A_high", "C_low", "C_high"):
    print(k, fmt(st.median([R.parts(s["points"][0], "PFATE")[k] for s in use])))
