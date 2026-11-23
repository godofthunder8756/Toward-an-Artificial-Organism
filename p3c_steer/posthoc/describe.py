"""P3c post-hoc descriptive checks (disclosed; not confirmatory; written after the scored result was known).
Reads p3c_steer/raw.json and p3c_steer_stage0/stage0_scores.json only; runs no network.

    python p3c_steer/posthoc/describe.py > p3c_steer/posthoc/describe.log
"""
import json
import os
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import run_p3b_diff as R3B
import run_p3c_steer as R
from trackc_swap.steerdiff import DIRS
from run_trackc_probe import fmt


def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    for k, i in enumerate(o):
        r[i] = float(k)
    return r


def spearman(x, y):
    keep = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    x, y = [a for a, _ in keep], [b for _, b in keep]
    rx, ry = rank(x), rank(y)
    mx, my = st.mean(rx), st.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else None


def med(v):
    v = [x for x in v if x is not None]
    return st.median(v) if v else None


d = json.load(open(os.path.join(HERE, "..", "raw.json")))["seeds"]
use = [s for s in d if R3B.phase1_usable(s)]
ARMS = ("PFATE", "PYOKED", "PNOFATE")
print(f"usable {len(use)} of {len(d)}")

for I, at in ((1, 3600), (0, 1800)):
    print(f"\n######## point {at}")
    sp = lambda s, a: s["points"][I]["steer"][a]

    print("\n== (1) one-sided effects (steered minus unsteered clear abstention), median over seeds")
    keys = ["+u_A", "-u_A", "+u_C", "-u_C", "+v_C", "-v_C", "+rand_u_A", "-rand_u_A", "+rand_u_C", "-rand_u_C"]
    for a in ARMS:
        print(f"  {a}")
        for t in "AC":
            row = "   ".join(f"{k} {fmt(med([sp(s, a)['steer'][k][t]['effect'] for s in use]), 3)}" for k in keys)
            print(f"    on {t}: {row}")

    print("\n== (2) correct-given-report on steered clear trials (held content), PFATE: median / min over seeds")
    for t in "AC":
        row = []
        for k in keys:
            v = [sp(s, "PFATE")["steer"][k][t]["correct_on"] for s in use]
            v = [x for x in v if x is not None]
            row.append(f"{k} {fmt(med(v), 3)}/{fmt(min(v) if v else None, 3)}")
        print(f"  on {t}: " + "   ".join(row))

    print("\n== (3) baseline clear abstention (no steering) and unsteered abstention inside steering runs, median")
    for a in ARMS:
        pl = {t: med([sp(s, a)["plain_clear_abstain"][t] for s in use]) for t in "AC"}
        off = {t: med([sp(s, a)["steer"]["+u_C"][t]["abstain_off"] for s in use]) for t in "AC"}
        print(f"  {a}: plain A {fmt(pl['A'], 3)} C {fmt(pl['C'], 3)}; unsteered in +u_C run A {fmt(off['A'], 3)} C {fmt(off['C'], 3)}")

    print("\n== (3b) leak: unsteered clear abstention inside each steering run minus plain, median / max over seeds")
    for a in ARMS:
        for t in "AC":
            row = []
            for k in keys:
                v = [sp(s, a)["steer"][k][t]["abstain_off"] - sp(s, a)["plain_clear_abstain"][t] for s in use]
                row.append(f"{k} {fmt(med(v), 3)}/{fmt(max(v), 3)}")
            print(f"  {a} {t}: " + "   ".join(row))

    print("\n== (4) geometry, median over seeds: norms, cosines, split-half reliability")
    for a in ARMS:
        nm = {k: med([sp(s, a)["norm"][k] for s in use]) for k in DIRS if k in sp(use[0], a)["norm"]}
        cs = {k: med([sp(s, a)["cos"][k] for s in use]) for k in sp(use[0], a)["cos"]}
        rl = {k: min(x for x in (sp(s, a)["split_half_cos"][k] for s in use) if x is not None) for k in DIRS}
        print(f"  {a}: norm " + ", ".join(f"{k} {fmt(v, 2)}" for k, v in nm.items())
              + "; cos " + ", ".join(f"{k} {fmt(v, 3)}" for k, v in cs.items())
              + "; min split-half " + ", ".join(f"{k} {fmt(v, 4)}" for k, v in rl.items()))

    print("\n== (5) per-seed association, PFATE (Spearman over usable seeds)")
    m = {s["seed"]: R.steer_measures(sp(s, "PFATE")) for s in use}
    A_low = [R3B.look_effect(s["points"][I], "PFATE", "A", "low") for s in use]
    C_rel = [R.neg(R3B.look_effect(s["points"][I], "PFATE", "C", "low")) for s in use]
    col = lambda k: [m[s["seed"]][k] for s in use]
    print(f"  behavioural A_low vs S_A: {fmt(spearman(A_low, col('S_A')), 2)}")
    print(f"  behavioural C release vs S_C: {fmt(spearman(C_rel, col('S_C')), 2)}")
    print(f"  S_C vs X_AC (u_C vs u_A on C): {fmt(spearman(col('S_C'), col('X_AC')), 2)}")
    print(f"  S_A vs X_CA (u_A vs u_C on A): {fmt(spearman(col('S_A'), col('X_CA')), 2)}")
    print(f"  S_A vs S_C: {fmt(spearman(col('S_A'), col('S_C')), 2)}")
    print(f"  S_A vs P_A (directional vs symmetric on A): {fmt(spearman(col('S_A'), col('P_A')), 2)}")
    print(f"  seeds with S_C < 0: {sum(1 for x in col('S_C') if x is not None and x < 0)}; "
          f"S_C quartiles {[fmt(x, 3) for x in st.quantiles([x for x in col('S_C') if x is not None], n=4)]}")
    print(f"  seeds with S_A < 0: {sum(1 for x in col('S_A') if x is not None and x < 0)}; "
          f"S_A quartiles {[fmt(x, 3) for x in st.quantiles([x for x in col('S_A') if x is not None], n=4)]}")

print("\n== (6) stage 0 (P3b's nets, 27 usable) against the final run, PFATE medians at 3600")
s0 = json.load(open(os.path.join(HERE, "..", "..", "p3c_steer_stage0", "stage0_scores.json")))
arms0 = s0["scores"]["steer"]["arms"]["PFATE"]
finarms = json.load(open(os.path.join(HERE, "..", "scores.json")))["scores"]["points"]["3600"]["steer"]["arms"]["PFATE"]
for k in ("S_A", "S_C", "X_AC", "X_CA", "V_C", "P_A", "P_C"):
    print(f"  {k}: stage 0 {fmt(arms0[k] if arms0 else None, 3)}; final {fmt(finarms[k] if finarms else None, 3)}")

print("\n== (7) leak-robust check, PFATE: steered-versus-steered contrasts (the unsteered baselines, which the leak in")
print("   (3b) inflates in the +u runs on C, drop out). E.g. S_C' = abstain_on(-u_C, C) - abstain_on(+u_C, C).")
print("   The leak can also raise abstain_on in the +u runs, which biases S_C' and X_AC' DOWN (conservative).")
from run_p1_selfeval import one_sample
for I, at in ((1, 3600), (0, 1800)):
    on = lambda s, k, t: s["points"][I]["steer"]["PFATE"]["steer"][k][t]["abstain_on"]
    dd = lambda s, kp, km, t: (None if on(s, kp, t) is None or on(s, km, t) is None else on(s, kp, t) - on(s, km, t))
    tests = {"S_A'": [dd(s, "+u_A", "-u_A", "A") for s in use], "S_C'": [dd(s, "-u_C", "+u_C", "C") for s in use],
             "X_AC'": [dd(s, "-u_A", "+u_A", "C") for s in use], "X_CA'": [dd(s, "+u_C", "-u_C", "A") for s in use]}
    for k, v in tests.items():
        r = one_sample(v, "CAUSAL", "REVERSED_CAUSAL")
        print(f"  {at} {k}: {r['positive']}/{r['n']} (p {fmt(r['sign_p'], 4)}; median {fmt(r['median'], 3)}) {r['label']}")

print("\n== (8) the same leak in stage 0 (P3b's nets), PFATE C, +u_C run: unsteered minus plain, median / max")
s0 = json.load(open(os.path.join(HERE, "..", "..", "p3c_steer_stage0", "stage0_raw.json")))["records"]
v0 = []
for s in s0:
    if s["seed"] == 2401:          # excluded from stage 0 (P3b's phase-1 exclusion)
        continue
    pt = s.get("steer", s).get("PFATE") if isinstance(s.get("steer", s), dict) else None
    if pt and "plain_clear_abstain" in pt:
        v0.append(pt["steer"]["+u_C"]["C"]["abstain_off"] - pt["plain_clear_abstain"]["C"])
print(f"  n {len(v0)}: median {fmt(med(v0), 3)}, max {fmt(max(v0) if v0 else None, 3)}")
