"""P1h stage 1, post-hoc (disclosed; written after seeing REPORT.md).

Finding to characterize: matched on the clean evidence decoder alone, a conflict raises the damage-trained
agent's abstention probability by about 0.10 (M2_E, 28/28; never-damaged net 0.000), while matched also on the
agent's own report gap nothing beyond the leak range remains. So the agent's own confidence is lower on conflicts
than the clean evidence says. Is that discount warranted, and where does it come from?

Re-collects stage 1's data exactly (same weights, streams, decoder seeds) and, per seed, arm and probe time, on
conflict trials and their evidence-matched same trials (caliper 0.05 SD, as M2_E):
  - M2_E per damage size K (dose);
  - reliability: share of trials the clean decoder gets right, conflict vs matched same (is the evidence less
    trustworthy on conflicts at the same strength?);
  - the agent's own report-head accuracy (sign of logit REP1 - REP0 against the stored value), conflict vs
    matched same; and the clean decoder's accuracy on all conflict trials against the agent's;
  - own margin, conflict vs matched same (how much of the discount sits in the report gap);
  - Spearman correlation, on conflict trials, of the integrity-trace score with own margin at matched evidence
    (does the trace that separates conflicts from same trials go with lower confidence?).
Run from the repository root: python3 p1h_evidence/stage1/posthoc/calib.py
"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np
import torch

sys.path.insert(0, os.getcwd())
import run_p1g_graded as G  # noqa: E402
import run_p1h_evidence as H  # noqa: E402
from run_trackc_paid import PAY, WEAR  # noqa: E402
from trackc_swap.env import A_REP0, A_REP1, WorldConfig  # noqa: E402
from trackc_swap.evidence import collect_graded, evidence_logit, p_abstain  # noqa: E402
from trackc_swap.gradmon import CALIPER, KS_G  # noqa: E402
from trackc_swap.secondorder import own_margin  # noqa: E402
from trackc_swap.selfmon import KIND_CONFLICT, KIND_NONE, KIND_SAME  # noqa: E402
from trackc_swap.train import TrainConfig  # noqa: E402

OUT = "p1h_evidence/stage1/posthoc"
ARMS = ("PFATE", "PYOKED", "PNOFATE")


def rank(x):
    r = np.empty(len(x))
    r[np.argsort(x, kind="stable")] = np.arange(len(x))
    return r


def analyse(agent, col, seed):
    clear, und = ~col["unclear"].astype(bool), ~col["drained"].astype(bool)
    K, DM = col["kind"], col["damaged"].astype(bool)
    cf = clear & und & (K == KIND_CONFLICT) & DM
    sm = clear & und & (K == KIND_SAME) & DM
    none = clear & und & (K == KIND_NONE) & ~DM
    Hs, y = col["h"], col["val"].astype(np.int64)
    fit = none | sm
    if min(int((fit & (y == 0)).sum()), int((fit & (y == 1)).sum())) < 50 or cf.sum() < 20:
        return None
    lg = evidence_logit(Hs, y, fit, cf, seed=seed)           # identical to evidence_summary's first decoder
    ev = np.abs(np.nan_to_num(lg))
    pab = p_abstain(agent, Hs)
    own = own_margin(agent, Hs)
    with torch.no_grad():
        pl = agent.pi(torch.as_tensor(Hs, dtype=torch.float32)).numpy()
    agent_ok = ((pl[:, A_REP1] - pl[:, A_REP0]) > 0) == (y == 1)
    dec_ok = (lg > 0) == (y == 1)
    # evidence-matched pairs (as matched_nn)
    pool = cf | sm
    sd = ev[pool].std()
    si = np.flatnonzero(sm)
    o = np.argsort(ev[si], kind="stable")
    si = si[o]
    xs = ev[si]
    ci = np.flatnonzero(cf)
    j = np.clip(np.searchsorted(xs, ev[ci]), 1, len(xs) - 1)
    nn = np.where(np.abs(xs[j - 1] - ev[ci]) <= np.abs(xs[j] - ev[ci]), j - 1, j)
    ok = np.abs(xs[nn] - ev[ci]) <= CALIPER * sd
    c, s = ci[ok], si[nn[ok]]
    if len(c) < 20:
        return None
    r = {"n_pairs": int(len(c)),
         "M2_E": float((pab[c] - pab[s]).mean()),
         "dec_ok_conflict": float(dec_ok[c].mean()), "dec_ok_same": float(dec_ok[s].mean()),
         "agent_ok_conflict": float(agent_ok[c].mean()), "agent_ok_same": float(agent_ok[s].mean()),
         "own_conflict": float(own[c].mean()), "own_same": float(own[s].mean()),
         "agent_ok_all_conflict": float(agent_ok[cf].mean()), "dec_ok_all_conflict": float(dec_ok[cf].mean())}
    kk = col["k"]
    r["M2_E_k"] = {str(k): (float((pab[c[kk[c] == k]] - pab[s[kk[c] == k]]).mean()) if (kk[c] == k).sum() >= 10
                            else None) for k in KS_G}
    r["dec_ok_conflict_k"] = {str(k): (float(dec_ok[c[kk[c] == k]].mean()) if (kk[c] == k).sum() >= 10 else None)
                              for k in KS_G}
    # integrity trace: cross-fitted logistic score (as trace_auc), correlated with own margin on matched conflicts
    m = cf | sm
    idx = np.flatnonzero(m)
    g = np.random.default_rng(seed + 1)
    g.shuffle(idx)
    mu, sdv = Hs[m].mean(0), Hs[m].std(0) + 1e-6
    X = torch.tensor((Hs - mu) / sdv, dtype=torch.float32)
    Y = torch.tensor(cf.astype(np.float32))
    sc = np.full(len(Hs), np.nan)
    for f, te in enumerate(np.array_split(idx, 5)):
        tr = torch.as_tensor(np.setdiff1d(idx, te))
        w = torch.zeros(Hs.shape[1], requires_grad=True)
        b = torch.zeros(1, requires_grad=True)
        opt = torch.optim.LBFGS([w, b], max_iter=200)

        def closure():
            opt.zero_grad()
            loss = torch.nn.functional.binary_cross_entropy_with_logits(X[tr] @ w + b, Y[tr]) + 1e-3 * (w * w).sum()
            loss.backward()
            return loss
        opt.step(closure)
        with torch.no_grad():
            sc[te] = (X[te] @ w + b).numpy()
    # partial out evidence: residual of own margin and of trace score on evidence (rank-linear), then correlate
    rc = lambda v: rank(v[c]) - np.polyval(np.polyfit(rank(ev[c]), rank(v[c]), 1), rank(ev[c]))
    a1, a2 = rc(sc), rc(own)
    r["rho_trace_own_given_ev"] = float(np.corrcoef(a1, a2)[0, 1]) if a1.std() > 0 and a2.std() > 0 else None
    return r


def one(seed):
    torch.set_num_threads(1)
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    weights = {a: torch.load(f"p1g_graded/weights/seed{seed}_{a}_3600.pt", weights_only=False) for a in ARMS}
    cols = collect_graded(seed, weights, wc, tc, PAY[1], G.BASE_F)
    return {"seed": seed, **{f"{a}_{t}": analyse(*cols[a][t], seed) for a in ARMS for t in ("early", "late")}}


def med(v):
    v = [x for x in v if x is not None]
    return float(np.median(v)) if v else None


def sign(v):
    from math import comb
    v = [x for x in v if x is not None and x != 0]
    n, k = len(v), sum(x > 0 for x in v)
    if not n:
        return "n/a"
    p = min(1.0, 2 * sum(comb(n, i) for i in range(min(k, n - k) + 1)) / 2 ** n)
    return f"{k}/{n} > 0, p {p:.4f}"


if __name__ == "__main__":
    with Pool(4) as pool:
        recs = sorted(pool.map(one, H.STAGE1_SEEDS), key=lambda r: r["seed"])
    with open(os.path.join(OUT, "calib.json"), "w") as fh:
        json.dump(recs, fh)
    # check: M2_E equals stage 1's per-run value
    with open("p1h_evidence/stage1/raw.json") as fh:
        raw = {s["seed"]: s for s in json.load(fh)["seeds"]}
    bad = sum(1 for r in recs for a in ARMS for t in ("early", "late")
              if r[f"{a}_{t}"] is not None and raw[r["seed"]]["arms"][a][t].get("fitted")
              and abs(r[f"{a}_{t}"]["M2_E"] - raw[r["seed"]]["arms"][a][t]["E"]["M2"]) > 1e-12)
    print(f"M2_E reproduction against stage 1: {bad} mismatches")
    for a in ARMS:
        for t in ("early", "late"):
            rs = [r[f"{a}_{t}"] for r in recs if r[f"{a}_{t}"] is not None]
            g = lambda k: med([x[k] for x in rs])
            print(f"\n{a} {t} (n {len(rs)}): M2_E {g('M2_E'):.4f}")
            print(f"  clean decoder correct, conflict vs matched same: {g('dec_ok_conflict'):.3f} vs "
                  f"{g('dec_ok_same'):.3f}; difference {sign([x['dec_ok_same'] - x['dec_ok_conflict'] for x in rs])} "
                  f"(same more reliable)")
            print(f"  agent report head correct, conflict vs matched same: {g('agent_ok_conflict'):.3f} vs "
                  f"{g('agent_ok_same'):.3f}")
            print(f"  all conflict trials: agent correct {g('agent_ok_all_conflict'):.3f}, clean decoder correct "
                  f"{g('dec_ok_all_conflict'):.3f}; agent minus decoder "
                  f"{sign([x['agent_ok_all_conflict'] - x['dec_ok_all_conflict'] for x in rs])}")
            print(f"  own margin, conflict vs matched same: {g('own_conflict'):.3f} vs {g('own_same'):.3f}; "
                  f"same minus conflict {sign([x['own_same'] - x['own_conflict'] for x in rs])}")
            print("  M2_E by K: " + ", ".join(f"{k}: {med([x['M2_E_k'][str(k)] for x in rs]):.4f}"
                                             if med([x['M2_E_k'][str(k)] for x in rs]) is not None else f"{k}: n/a"
                                             for k in KS_G))
            print("  clean decoder correct on matched conflicts by K: " + ", ".join(
                f"{k}: {med([x['dec_ok_conflict_k'][str(k)] for x in rs]):.3f}"
                if med([x['dec_ok_conflict_k'][str(k)] for x in rs]) is not None else f"{k}: n/a" for k in KS_G))
            rho = [x["rho_trace_own_given_ev"] for x in rs]
            print(f"  rank correlation of trace score with own margin on matched conflicts, evidence partialled: "
                  f"median {med(rho):.3f}; {sign([-v for v in rho if v is not None])} (negative)")
