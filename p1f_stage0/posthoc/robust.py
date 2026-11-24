"""P1f stage 0, post-hoc robustness (disclosed; written after seeing STAGE0_REPORT.md).

Concern: conflict trials have far lower own margin than same trials (medians about 2.7 vs 10.4), so within a
kept quantile bin the conflict trials may still sit lower; residual confounding by margin could give M2 > 0.
Re-collects the same per-trial data (same weights, same evaluation streams, tag 140) and computes per seed,
arm and probe time, on own margin:
  - M2 with 10 (as declared), 20 and 40 quantile bins;
  - imbalance: conflict-weighted mean of (mean margin conflict - mean margin same) inside kept bins (10 bins);
  - M2_nn: each conflict trial against its nearest same trial in margin (with replacement), caliper 0.05
    pooled SD; coverage the share of conflict trials matched;
  - bias_10: the 10-bin M2 when every conflict trial's abstention is replaced by the abstention rate of its
    20 nearest same trials in margin (a first-order-only world built from the agent's own same trials).
    M2_10 - bias_10 is a bias-corrected estimate.
Run from the repository root: python3 p1f_stage0/posthoc/robust.py
"""
import json
import os
import sys
from dataclasses import asdict
from multiprocessing import Pool

import numpy as np
import torch

sys.path.insert(0, os.getcwd())
import run_p1e_selfmon as R  # noqa: E402
from run_trackc_paid import PAY, WEAR  # noqa: E402
from trackc_swap.env import WorldConfig  # noqa: E402
from trackc_swap.secondorder import EVAL_TAG_F, KIND_CONFLICT, KIND_SAME, matched_diff, own_margin  # noqa: E402
from trackc_swap.selfmon import EARLY, LATE, SPLIT_P, MonRunner  # noqa: E402
from trackc_swap.train import TrainConfig  # noqa: E402

ARMS = ("PFATE", "PYOKED", "PNOFATE")
OUT = "p1f_stage0/posthoc"


def analyse(ab, c, s, x):
    r = {}
    for b, n in ((10, 5), (20, 5), (40, 3)):
        r[f"M2_{b}"] = matched_diff(ab, c, s, x, bins=b, n_min=n)["M2"]
    pool = c | s
    edges = np.unique(np.quantile(x[pool], np.linspace(0, 1, 11)))
    bi = np.clip(np.searchsorted(edges, x, side="right") - 1, 0, len(edges) - 2)
    num = w = 0.0
    for k in range(len(edges) - 1):
        mc, ms = c & (bi == k), s & (bi == k)
        if mc.sum() >= 5 and ms.sum() >= 5:
            num += mc.sum() * (x[mc].mean() - x[ms].mean())
            w += mc.sum()
    r["imbalance_10"] = num / w if w else None
    xs, as_ = x[s], ab[s]
    order = np.argsort(xs)
    xs, as_ = xs[order], as_[order]
    cal = 0.05 * x[pool].std()
    xc, ac = x[c], ab[c]
    if len(xs) >= 20 and len(xc):
        j = np.clip(np.searchsorted(xs, xc), 1, len(xs) - 1)
        nn = np.where(np.abs(xs[j - 1] - xc) <= np.abs(xs[j] - xc), j - 1, j)
        ok = np.abs(xs[nn] - xc) <= cal
        r["M2_nn"] = float((ac[ok] - as_[nn[ok]]).mean()) if ok.any() else None
        r["coverage_nn"] = float(ok.mean())
        # first-order-only null from the 20 nearest same trials
        p = np.empty(len(xc))
        for i, v in enumerate(xc):
            k = np.argsort(np.abs(xs - v))[:20]
            p[i] = as_[k].mean()
        ab0 = ab.copy()
        ab0[c] = p
        r["bias_10"] = matched_diff(ab0, c, s, x)["M2"]
    else:
        r["M2_nn"] = r["coverage_nn"] = r["bias_10"] = None
    return r


def one(seed):
    torch.set_num_threads(1)
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    out = {"seed": seed}
    for a in ARMS:
        sd = torch.load(f"p1e_selfmon/weights/seed{seed}_{a}_3600.pt", weights_only=False)
        mr = MonRunner(a, seed, wc, tc, PAY[1], tag_offset=EVAL_TAG_F)
        mr.agent.load_state_dict(sd)
        mr.agent.eval()
        for tag, at in (("early", EARLY), ("late", LATE)):
            _, _, _, col = mr.evaluate_m("zero", drain_p=0.0, split_p=SPLIT_P, split_at=at, collect=True)
            clear, und = ~col["unclear"].astype(bool), ~col["drained"].astype(bool)
            dm = col["damaged"].astype(bool)
            c = clear & und & (col["kind"] == KIND_CONFLICT) & dm
            s = clear & und & (col["kind"] == KIND_SAME) & dm
            ab = 1.0 - col["rep"].astype(np.float64)
            out[f"{a}_{tag}"] = analyse(ab, c, s, own_margin(mr.agent, col["h"]))
    return out


def med(v):
    v = [x for x in v if x is not None]
    return (float(np.median(v)), len(v)) if v else (None, 0)


if __name__ == "__main__":
    with Pool(4) as p:
        recs = sorted(p.map(one, R.FINAL_SEEDS), key=lambda r: r["seed"])
    with open(os.path.join(OUT, "robust.json"), "w") as fh:
        json.dump(recs, fh)
    keys = ("M2_10", "M2_20", "M2_40", "imbalance_10", "M2_nn", "coverage_nn", "bias_10")
    for a in ARMS:
        for t in ("early", "late"):
            row = []
            for k in keys:
                m, n = med([r[f"{a}_{t}"][k] for r in recs])
                row.append(f"{k} {m:.3f} (n {n})" if m is not None else f"{k} None")
            corr = [r[f"{a}_{t}"]["M2_10"] - r[f"{a}_{t}"]["bias_10"] for r in recs
                    if r[f"{a}_{t}"]["M2_10"] is not None and r[f"{a}_{t}"]["bias_10"] is not None]
            pos = sum(v > 0 for v in corr)
            row.append(f"corrected median {np.median(corr):.3f}, {pos}/{len(corr)} > 0" if corr else "corrected None")
            print(f"{a} {t}: " + "; ".join(row))
