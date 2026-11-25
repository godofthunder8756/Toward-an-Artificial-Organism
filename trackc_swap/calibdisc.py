"""P1i: confirmation of the calibrated integrity discount (P1h's secondary and post-hoc finding) on fresh seeds.

Additive module; every earlier module is imported, never modified. Protocol: P1I_CALIB_PROTOCOL.md.

Per graded-probe run (P1g's probe B, clear undrained trials; conflict = damaged with a different value, same =
damaged with the same value, none = undamaged without an event):
- evidence: P1h's cross-fitted evidence decoder (never sees a conflict), margin |logit|;
- evidence-matched pairs: each conflict trial against its nearest same trial in evidence margin (caliper 0.05
  pooled SD, with replacement, at least 20 pairs):
    M2_E      mean p_abs(conflict) - p_abs(matched same)          (the discount in abstention)
    rel_gap   share of matched same trials the decoder reads right minus the share of conflict trials
              (is the discount warranted: is a conflicted memory less reliable at the same evidence?)
    own_gap   mean own margin(matched same) - own margin(conflict)   (the discount in report confidence)
    per K     M2_E and decoder reliability on matched conflicts
- type-2 sensitivity beyond evidence (type2_resid): on conflict trials, does the agent's report confidence (own
  margin) separate the trials its report head gets right from those it gets wrong, within strata of evidence?
  AUC within each of 10 evidence-quantile strata (strata with at least 5 right and 5 wrong), of the confidence
  after removing its linear trend on evidence inside the stratum (without this, a purely first-order
  confidence scores about 0.535 in the synthetic test), combined with weights n_right x n_wrong. 0.5: confidence carries nothing about its own errors beyond the evidence.
- trace_rho: rank correlation, on matched conflicts with evidence partialled out, between a cross-fitted
  conflict-vs-same classifier score on the state and own margin (as P1h's post-hoc).
"""
from __future__ import annotations

from typing import Dict, Optional

import numpy as np
import torch

from .env import A_REP0, A_REP1
from .evidence import evidence_logit, p_abstain
from .gradmon import CALIPER, KS_G, NN_MIN
from .secondorder import own_margin
from .selfmon import KIND_CONFLICT, KIND_NONE, KIND_SAME

STRATA = 10
STRATUM_MIN = 5
K_MIN = 10


def auc(pos: np.ndarray, neg: np.ndarray) -> Optional[float]:
    """P(pos > neg) + 0.5 P(tie), by ranks."""
    if len(pos) == 0 or len(neg) == 0:
        return None
    allv = np.r_[pos, neg]
    o = np.argsort(allv, kind="stable")
    r = np.empty(len(allv))
    sv = allv[o]
    i = 0
    while i < len(sv):                                   # average ranks over ties
        j = i
        while j + 1 < len(sv) and sv[j + 1] == sv[i]:
            j += 1
        r[o[i:j + 1]] = 0.5 * (i + j) + 1
        i = j + 1
    rp = r[:len(pos)].sum()
    return float((rp - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def type2_resid(conf: np.ndarray, right: np.ndarray, ev: np.ndarray, strata: int = STRATA,
                n_min: int = STRATUM_MIN) -> Dict[str, object]:
    """Type-2 AUC of `conf` (linearly detrended on `ev` within each stratum) for right vs wrong, within quantile
    strata of `ev`; weights n_right x n_wrong."""
    out = {"auc": None, "auc_raw": auc(conf[right], conf[~right]), "auc_ev_raw": auc(ev[right], ev[~right]),
           "strata_used": 0}
    if len(ev) < 2 * strata:
        return out
    edges = np.unique(np.quantile(ev, np.linspace(0, 1, strata + 1)))
    b = np.clip(np.searchsorted(edges, ev, side="right") - 1, 0, len(edges) - 2)
    num = w = 0.0
    used = 0
    for k in range(len(edges) - 1):
        m = b == k
        r, x = right[m], conf[m]
        nr, nw = int(r.sum()), int((~r).sum())
        if nr >= n_min and nw >= n_min:
            e = ev[m]
            if e.std() > 0:                              # remove the evidence trend left inside the stratum
                x = x - np.polyval(np.polyfit(e, x, 1), e)
            num += auc(x[r], x[~r]) * nr * nw
            w += nr * nw
            used += 1
    out["auc"] = num / w if w else None
    out["strata_used"] = used
    return out


def rank(x: np.ndarray) -> np.ndarray:
    r = np.empty(len(x))
    r[np.argsort(x, kind="stable")] = np.arange(len(x))
    return r


def trace_scores(Hs: np.ndarray, is_conf: np.ndarray, is_same: np.ndarray, seed: int, folds: int = 5) -> np.ndarray:
    m = is_conf | is_same
    idx = np.flatnonzero(m)
    g = np.random.default_rng(seed + 1)
    g.shuffle(idx)
    mu, sd = Hs[m].mean(0), Hs[m].std(0) + 1e-6
    X = torch.tensor((Hs - mu) / sd, dtype=torch.float32)
    Y = torch.tensor(is_conf.astype(np.float32))
    sc = np.full(len(Hs), np.nan)
    for te in np.array_split(idx, folds):
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
    return sc


def calib_summary(agent, col: Optional[Dict[str, np.ndarray]], seed: int = 0) -> Dict[str, object]:
    if not col:
        return {"fitted": False}
    clear, und = ~col["unclear"].astype(bool), ~col["drained"].astype(bool)
    K, DM = col["kind"], col["damaged"].astype(bool)
    cf = clear & und & (K == KIND_CONFLICT) & DM
    sm = clear & und & (K == KIND_SAME) & DM
    none = clear & und & (K == KIND_NONE) & ~DM
    Hs, y = col["h"], col["val"].astype(np.int64)
    fit = none | sm
    if min(int((fit & (y == 0)).sum()), int((fit & (y == 1)).sum())) < 50 or cf.sum() < NN_MIN:
        return {"fitted": False}
    lg = evidence_logit(Hs, y, fit, cf, seed=seed)
    ev = np.abs(np.nan_to_num(lg))
    pab = p_abstain(agent, Hs)
    own = own_margin(agent, Hs)
    with torch.no_grad():
        pl = agent.pi(torch.as_tensor(Hs, dtype=torch.float32)).numpy()
    agent_ok = ((pl[:, A_REP1] - pl[:, A_REP0]) > 0) == (y == 1)
    dec_ok = (lg > 0) == (y == 1)
    out: Dict[str, object] = {"fitted": True, "dec_acc_none": float(dec_ok[none].mean()),
                              "dec_acc_same": float(dec_ok[sm].mean()),
                              "agent_acc_conflict": float(agent_ok[cf].mean()),
                              "dec_acc_conflict": float(dec_ok[cf].mean())}
    # evidence-matched pairs
    pool = cf | sm
    sd = float(ev[pool].std()) or 1.0
    si = np.flatnonzero(sm)
    si = si[np.argsort(ev[si], kind="stable")]
    xs = ev[si]
    ci = np.flatnonzero(cf)
    j = np.clip(np.searchsorted(xs, ev[ci]), 1, len(xs) - 1)
    nn = np.where(np.abs(xs[j - 1] - ev[ci]) <= np.abs(xs[j] - ev[ci]), j - 1, j)
    ok = np.abs(xs[nn] - ev[ci]) <= CALIPER * sd
    c, s = ci[ok], si[nn[ok]]
    out["n_pairs"], out["coverage"] = int(len(c)), float(ok.mean())
    if len(c) >= NN_MIN:
        out["M2_E"] = float((pab[c] - pab[s]).mean())
        out["rel_gap"] = float(dec_ok[s].mean() - dec_ok[c].mean())
        out["own_gap"] = float(own[s].mean() - own[c].mean())
        kk = col["k"]
        out["M2_E_k"] = {str(k): (float((pab[c[kk[c] == k]] - pab[s[kk[c] == k]]).mean())
                                  if (kk[c] == k).sum() >= K_MIN else None) for k in KS_G}
        out["rel_k"] = {str(k): (float(dec_ok[c[kk[c] == k]].mean()) if (kk[c] == k).sum() >= K_MIN else None)
                        for k in KS_G}
        tsc = trace_scores(Hs, cf, sm, seed)
        rc = lambda v: rank(v[c]) - np.polyval(np.polyfit(rank(ev[c]), rank(v[c]), 1), rank(ev[c]))
        a1, a2 = rc(tsc), rc(own)
        out["trace_rho"] = float(np.corrcoef(a1, a2)[0, 1]) if a1.std() > 0 and a2.std() > 0 else None
    else:
        out.update({"M2_E": None, "rel_gap": None, "own_gap": None, "M2_E_k": None, "rel_k": None,
                    "trace_rho": None})
    t2 = type2_resid(own[cf], agent_ok[cf], ev[cf])
    t2p = type2_resid(-pab[cf], agent_ok[cf], ev[cf])
    out["type2_resid"], out["type2_raw"], out["type2_ev_raw"] = t2["auc"], t2["auc_raw"], t2["auc_ev_raw"]
    out["type2_resid_pabs"], out["type2_strata"] = t2p["auc"], t2["strata_used"]
    return out
