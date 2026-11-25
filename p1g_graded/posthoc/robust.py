"""P1g, post-hoc robustness of the second-order result (disclosed; written after seeing REPORT.md).

The declared label is MONITOR_SECOND_ORDER (P1G_2: M2_nn_own of PFATE > 0 in 25/27 seeds), but the effect is
small (median 0.005 against M 0.578), and the balance inside the caliper is not 0 (conflict trials sit
slightly lower in own margin than their matched same trials, -0.003). Stage 0 (P1f) showed that a coarse
match can turn first-order confounding into an apparent second-order effect. This script asks whether the
P1g estimate survives the same kind of tightening.

Re-collects the per-trial graded-probe data at 3600 (same weights, same evaluation streams: the copies are
built and evaluated exactly as in gradmon.evaluate_point_g, tag 160) and computes, per seed, arm and probe
time, on clear undrained trials:
  - M2_nn at calipers 0.05 (declared; must reproduce raw.json), 0.025 and 0.01 pooled SD (at least 20 pairs);
  - bias_lin: the M2 that first-order confidence alone would give from the residual imbalance, from a local
    linear fit of abstention on own margin among same trials within 0.25 SD of each conflict trial
    (interpolation only: the window is centred on a kept conflict trial whose matched same trial is within
    the caliper); M2_corr = M2_nn - bias_lin;
  - M2_2d: nearest same trial in (own margin, LDA margin), each standardized, kept if within 0.05 SD on both
    (also at 0.1 and 0.2 SD, added after the first pass showed M2_2d small with lower coverage: to separate
    a real shrinkage from lost power); M2_lda: the same on LDA margin alone at 0.05;
  - M2_k: nearest same trial in own margin among same trials with the same K (damage size held equal);
  - abst_same_matched: abstention of the matched same trials (the base rate the effect is measured against);
  - M2 by own-margin tercile of the kept conflict trials.
Run from the repository root: python3 p1g_graded/posthoc/robust.py [seed ...]
"""
import copy
import json
import os
import sys
from multiprocessing import Pool

import numpy as np
import torch

sys.path.insert(0, os.getcwd())
import run_p1g_graded as G  # noqa: E402
from run_trackc_paid import PAY, WEAR  # noqa: E402
from trackc_swap.env import WorldConfig  # noqa: E402
from trackc_swap.gradmon import EVAL_TAG_G, KS_G, GradRunner, matched_nn  # noqa: E402
from trackc_swap.secondorder import lda_margin, own_margin  # noqa: E402
from trackc_swap.selfmon import (ARMS_M, EARLY, KIND_CONFLICT, KIND_SAME, LATE, LEADS_M, P_MAX_M,  # noqa: E402
                                 RATE_M, SPLIT_P)
from trackc_swap.train import TrainConfig  # noqa: E402

OUT = "p1g_graded/posthoc"
POINT = 3600


def nn_pairs(xs_list, c, s, cal, extra_eq=None):
    """Indices (conflict i, matched same j) of nearest same trial in standardized multi-d distance, kept if
    within `cal` SD in every dimension; optional exact match on extra_eq."""
    pool = c | s
    Z = np.stack([x / x[pool].std() for x in xs_list], 1)
    ci, si = np.flatnonzero(c), np.flatnonzero(s)
    pairs = []
    groups = [None] if extra_eq is None else np.unique(extra_eq[c])
    for g in groups:
        cg = ci if g is None else ci[extra_eq[ci] == g]
        sg = si if g is None else si[extra_eq[si] == g]
        if len(sg) == 0 or len(cg) == 0:
            continue
        if Z.shape[1] == 1:
            zs = Z[sg, 0]
            o = np.argsort(zs, kind="stable")
            zs, sg = zs[o], sg[o]
            zc = Z[cg, 0]
            j = np.clip(np.searchsorted(zs, zc), 1, max(len(zs) - 1, 1))
            if len(zs) == 1:
                nn = np.zeros(len(zc), int)
            else:
                nn = np.where(np.abs(zs[j - 1] - zc) <= np.abs(zs[j] - zc), j - 1, j)
            ok = np.abs(zs[nn] - zc) <= cal
            pairs += list(zip(cg[ok], sg[nn[ok]]))
        else:
            for i in cg:
                d = np.abs(Z[sg] - Z[i])
                j = np.argmin((d ** 2).sum(1))
                if (d[j] <= cal).all():
                    pairs.append((i, sg[j]))
    return np.array(pairs, int).reshape(-1, 2), len(ci)


def m2(ab, pairs, n_min=20):
    return float((ab[pairs[:, 0]] - ab[pairs[:, 1]]).mean()) if len(pairs) >= n_min else None


def analyse(ab, c, s, own, lda, kk):
    r = {}
    for cal in (0.05, 0.025, 0.01):
        p, n = nn_pairs([own], c, s, cal)
        r[f"M2_{cal}"] = m2(ab, p)
        r[f"cov_{cal}"] = len(p) / n if n else 0.0
    r["M2_decl"] = matched_nn(ab, c, s, own)["M2"]          # the declared function, for the reproduction check
    p, _ = nn_pairs([own], c, s, 0.05)
    sd = own[c | s].std()
    r["balance"] = float((own[p[:, 0]] - own[p[:, 1]]).mean()) if len(p) else None
    r["abst_same_matched"] = float(ab[p[:, 1]].mean()) if len(p) >= 20 else None
    r["abst_conf_matched"] = float(ab[p[:, 0]].mean()) if len(p) >= 20 else None
    # first-order bias from the residual imbalance (local linear fit among same trials)
    xs, as_ = own[s], ab[s]
    bias = []
    for i, j in p:
        w = np.abs(xs - own[i]) <= 0.25 * sd
        if w.sum() >= 10 and xs[w].std() > 0:
            slope = np.polyfit(xs[w], as_[w], 1)[0]
            bias.append(slope * (own[i] - own[j]))
        else:
            bias.append(0.0)
    r["bias_lin"] = float(np.mean(bias)) if len(p) >= 20 else None
    r["M2_corr"] = r["M2_0.05"] - r["bias_lin"] if r["M2_0.05"] is not None else None
    if lda is not None:
        p2, n = nn_pairs([own, lda], c, s, 0.05)
        r["M2_2d"], r["cov_2d"] = m2(ab, p2), (len(p2) / n if n else 0.0)
        for cal in (0.1, 0.2):
            p2, n = nn_pairs([own, lda], c, s, cal)
            r[f"M2_2d_{cal}"], r[f"cov_2d_{cal}"] = m2(ab, p2), (len(p2) / n if n else 0.0)
        p2, n = nn_pairs([lda], c, s, 0.05)
        r["M2_lda"], r["cov_lda"] = m2(ab, p2), (len(p2) / n if n else 0.0)
    else:
        r["M2_2d"] = r["cov_2d"] = r["M2_lda"] = r["cov_lda"] = None
        for cal in (0.1, 0.2):
            r[f"M2_2d_{cal}"] = r[f"cov_2d_{cal}"] = None
    pk, n = nn_pairs([own], c, s, 0.05, extra_eq=kk)
    r["M2_k"], r["cov_k"] = m2(ab, pk), (len(pk) / n if n else 0.0)
    # by own-margin tercile of the kept conflict trials
    if len(p) >= 60:
        q = np.quantile(own[p[:, 0]], [1 / 3, 2 / 3])
        t = np.digitize(own[p[:, 0]], q)
        r["M2_terciles"] = [float((ab[p[t == k, 0]] - ab[p[t == k, 1]]).mean()) for k in range(3)]
        r["abst_same_terciles"] = [float(ab[p[t == k, 1]].mean()) for k in range(3)]
    else:
        r["M2_terciles"] = r["abst_same_terciles"] = None
    return r


def one(seed):
    torch.set_num_threads(1)
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    copies = {}
    for a in ARMS_M:
        c = GradRunner(a, seed, wc, tc, PAY[1], tag_offset=EVAL_TAG_G, rate=RATE_M, p_max=P_MAX_M, base=G.BASE_F,
                       ks=KS_G)
        c.agent.load_state_dict(torch.load(f"p1g_graded/weights/seed{seed}_{a}_{POINT}.pt", weights_only=False))
        c.agent.eval()
        copies[a] = c
    lead = {}
    for a, c in copies.items():                       # natural running first, exactly as in evaluate_point_g
        if a not in LEADS_M:
            _, g, _, _ = c.evaluate_g("own" if a == "PFATE" else "zero")
            lead[a] = g
    for a, c in copies.items():
        if a in LEADS_M:
            c.evaluate_g("replay", lead[LEADS_M[a]])
    out = {"seed": seed}
    for a, c in copies.items():
        for tag, at in (("early", EARLY), ("late", LATE)):
            c.evaluate_g("zero", drain_p=0.5, split_p=SPLIT_P, split_at=at, collect=True, base_on=False)
            _, _, _, col = c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=at, collect=True,
                                        probe_ks=c.ks, base_on=False)
            clear, und = ~col["unclear"].astype(bool), ~col["drained"].astype(bool)
            dm = col["damaged"].astype(bool)
            cf = clear & und & (col["kind"] == KIND_CONFLICT) & dm
            sm = clear & und & (col["kind"] == KIND_SAME) & dm
            ab = 1.0 - col["rep"].astype(np.float64)
            out[f"{a}_{tag}"] = analyse(ab, cf, sm, own_margin(c.agent, col["h"]), lda_margin(col), col["k"])
    return out


def med(v):
    v = [x for x in v if x is not None]
    return (float(np.median(v)), len(v)) if v else (None, 0)


def sign(v):
    from math import comb
    v = [x for x in v if x is not None and x != 0]
    n, k = len(v), sum(x > 0 for x in v)
    if n == 0:
        return "n/a"
    p = min(1.0, 2 * sum(comb(n, i) for i in range(min(k, n - k) + 1)) / 2 ** n)
    return f"{k}/{n} > 0, p {p:.4f}"


if __name__ == "__main__":
    seeds = [int(a) for a in sys.argv[1:]] or G.FINAL_SEEDS
    with Pool(4) as pool:
        recs = sorted(pool.map(one, seeds), key=lambda r: r["seed"])
    name = "robust.json" if len(seeds) == len(G.FINAL_SEEDS) else "robust_partial.json"
    with open(os.path.join(OUT, name), "w") as fh:
        json.dump(recs, fh)
    with open("p1g_graded/raw.json") as fh:
        raw = {s["seed"]: s for s in json.load(fh)["seeds"]}
    # reproduction check against raw.json
    bad = 0
    for r in recs:
        pt = [p for p in raw[r["seed"]]["points"] if p["iters"] == POINT][0]
        for a in ARMS_M:
            for t in ("early", "late"):
                want = pt[f"graded_{t}"][a]["own"]["nn"]["M2"]
                got = r[f"{a}_{t}"]["M2_decl"]
                if not ((want is None and got is None) or (want is not None and got is not None
                                                           and abs(want - got) < 1e-12)):
                    bad += 1
    print(f"reproduction of M2_nn_own against raw.json: {bad} mismatches over {len(recs) * 6} runs")
    keys = ("M2_0.05", "M2_0.025", "M2_0.01", "cov_0.01", "balance", "bias_lin", "M2_corr", "M2_2d", "cov_2d",
            "M2_2d_0.1", "cov_2d_0.1", "M2_2d_0.2", "cov_2d_0.2", "M2_lda", "cov_lda", "M2_k", "cov_k", "abst_same_matched", "abst_conf_matched")
    for a in ARMS_M:
        for t in ("early", "late"):
            print(f"\n{a} {t}:")
            for k in keys:
                vals = [r[f"{a}_{t}"][k] for r in recs]
                m, n = med(vals)
                tail = f"; {sign(vals)}" if k.startswith("M2") else ""
                print(f"  {k}: median {m:.4f} (n {n}){tail}" if m is not None else f"  {k}: None")
            ter = [r[f"{a}_{t}"]["M2_terciles"] for r in recs if r[f"{a}_{t}"]["M2_terciles"]]
            ab3 = [r[f"{a}_{t}"]["abst_same_terciles"] for r in recs if r[f"{a}_{t}"]["abst_same_terciles"]]
            if ter:
                print("  M2 by own-margin tercile (low, mid, high): "
                      + ", ".join(f"{np.median([x[i] for x in ter]):.4f}" for i in range(3))
                      + "; matched same abstention: "
                      + ", ".join(f"{np.median([x[i] for x in ab3]):.4f}" for i in range(3)))
    # PFATE against PNOFATE, paired (mean of EARLY and LATE as in the declared measure), tight caliper
    for k in ("M2_0.05", "M2_0.01", "M2_corr", "M2_2d", "M2_2d_0.1", "M2_2d_0.2", "M2_lda", "M2_k"):
        d = []
        for r in recs:
            v = {}
            for a in ("PFATE", "PNOFATE"):
                xs = [r[f"{a}_{t}"][k] for t in ("early", "late") if r[f"{a}_{t}"][k] is not None]
                v[a] = np.mean(xs) if xs else None
            if v["PFATE"] is not None and v["PNOFATE"] is not None:
                d.append(v["PFATE"] - v["PNOFATE"])
        print(f"\nPFATE - PNOFATE, {k} (mean of EARLY and LATE): {sign(d)}; median diff "
              f"{np.median(d) if d else float('nan'):.4f}")
    for k in ("M2_0.05", "M2_0.01", "M2_corr", "M2_2d", "M2_2d_0.1", "M2_2d_0.2", "M2_lda", "M2_k"):
        for a in ARMS_M:
            vals = []
            for r in recs:
                xs = [r[f"{a}_{t}"][k] for t in ("early", "late") if r[f"{a}_{t}"][k] is not None]
                vals.append(float(np.mean(xs)) if xs else None)
            m, n = med(vals)
            print(f"{k} {a} (mean of EARLY and LATE): median "
                  f"{m if m is not None else float('nan'):.4f} (n {n}); {sign(vals)}")
