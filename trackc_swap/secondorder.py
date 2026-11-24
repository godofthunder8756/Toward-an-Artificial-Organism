"""Track C P1f: is the self-monitor second-order? Matched first-order confidence (Layer 4).

P1e found (descriptively; the run was INVALID on exposure) that an agent whose memory can be split-overwritten
learns to abstain when its own state carries a conflict, and that in the trained networks the conflict stays
visible as low-confidence content. P1f asks: at MATCHED first-order confidence, does a conflict still raise
abstention? If so, the agent carries a signal about its own state that is not its confidence in the content.

The second-order evaluation, used identically on P1e's saved weights (stage 0) and on P1f's new nets:
  - a trained net (weights at a point) is loaded into a fresh MonRunner in an evaluation world of its own
    (tag offset EVAL_TAG_F, distinct from P1e's);
  - damage off except the split probe on SPLIT_P of the trials (half conflict, half same), at EARLY and at
    LATE, as in P1e; no drain;
  - at the report step the GRU state h is collected (P1e's collection), and two first-order confidences are
    computed per trial:
      own margin  |logit(REP1) - logit(REP0)| of the agent's own policy head on h (the agent's own read of
                  which value it holds; pi is linear in h);
      LDA margin  P1e's linear decoder of the held value (fitted on clear, undamaged, unprobed trials), in
                  within-class SD units;
  - M2 = abstention(conflict) - abstention(same) at matched confidence: the pooled conflict + same trials
    are cut into DEC_BINS quantile bins of the confidence; bins with at least BIN_MIN trials of each kind
    are kept; the per-bin differences are averaged with weights equal to the bin's conflict count. Coverage
    is the share of conflict trials in kept bins.

Simulated variables only. No operator, stop, shutdown or host variable exists; no process is terminated.
"""
from __future__ import annotations

import copy
from typing import Dict, Optional

import numpy as np
import torch

from .env import A_REP0, A_REP1
from .selfmon import EARLY, KIND_CONFLICT, KIND_NONE, KIND_SAME, LATE, SPLIT_P, MonRunner, DEC_MIN

EVAL_TAG_F = 140            # evaluation world streams for the second-order pass (P1e used 120)
DEC_BINS = 10               # quantile bins of first-order confidence
BIN_MIN = 5                 # a bin is kept with at least this many conflict and this many same trials
CONF_KEYS = ("own", "lda")


def own_margin(agent, h: np.ndarray) -> np.ndarray:
    """|logit(REP1) - logit(REP0)| of the agent's policy head on the collected states."""
    with torch.no_grad():
        lg = agent.pi(torch.as_tensor(h, dtype=torch.float32)).numpy().astype(np.float64)
    return np.abs(lg[:, A_REP1] - lg[:, A_REP0])


def lda_margin(col: Dict[str, np.ndarray]) -> Optional[np.ndarray]:
    """P1e's decoder (trackc_swap.selfmon.decoder_summary), returning the per-trial margin; None if it
    cannot be fitted."""
    H, val = col["h"], col["val"].astype(np.int64)
    clear, und = ~col["unclear"].astype(bool), ~col["drained"].astype(bool)
    base = clear & und & (col["kind"] == KIND_NONE) & ~col["damaged"].astype(bool)
    if min(int((base & (val == 0)).sum()), int((base & (val == 1)).sum())) < DEC_MIN:
        return None
    X0, X1 = H[base & (val == 0)], H[base & (val == 1)]
    mu0, mu1 = X0.mean(0), X1.mean(0)
    S = (np.cov(X0, rowvar=False) * (len(X0) - 1) + np.cov(X1, rowvar=False) * (len(X1) - 1)) / (len(X0) + len(X1) - 2)
    S = S + 1e-2 * np.trace(S) / S.shape[0] * np.eye(S.shape[0])
    wv = np.linalg.solve(S, mu1 - mu0)
    c = 0.5 * float((mu0 + mu1) @ wv)
    pr0, pr1 = X0 @ wv, X1 @ wv
    sd = float(np.sqrt(0.5 * (pr0.var() + pr1.var()))) or 1.0
    return np.abs((H @ wv - c) / sd)


def matched_diff(abstain: np.ndarray, is_conf: np.ndarray, is_same: np.ndarray, x: np.ndarray,
                 bins: int = DEC_BINS, n_min: int = BIN_MIN) -> Dict[str, object]:
    """Abstention on conflict minus same trials at matched x (quantile bins of the pooled trials; bins with
    at least n_min of each kind; weighted by conflict count). Returns M2, coverage and counts."""
    pool = is_conf | is_same
    n_c = int(is_conf.sum())
    out: Dict[str, object] = {"M2": None, "coverage": 0.0, "n_conflict": n_c, "n_same": int(is_same.sum()),
                              "bins_kept": 0, "raw": None}
    if n_c and is_same.any():
        out["raw"] = float(abstain[is_conf].mean() - abstain[is_same].mean())
    if pool.sum() < 2 * n_min:
        return out
    edges = np.unique(np.quantile(x[pool], np.linspace(0, 1, bins + 1)))
    if len(edges) < 2:
        return out
    b = np.clip(np.searchsorted(edges, x, side="right") - 1, 0, len(edges) - 2)
    num, wsum, kept = 0.0, 0, 0
    for k in range(len(edges) - 1):
        mc, ms = is_conf & (b == k), is_same & (b == k)
        if mc.sum() >= n_min and ms.sum() >= n_min:
            num += float(mc.sum()) * float(abstain[mc].mean() - abstain[ms].mean())
            wsum += int(mc.sum())
            kept += 1
    if wsum:
        out["M2"] = num / wsum
        out["coverage"] = wsum / n_c
        out["bins_kept"] = kept
    return out


def second_order_summary(agent, col: Optional[Dict[str, np.ndarray]]) -> Dict[str, object]:
    """M2 at matched own margin and at matched LDA margin, on clear undrained probed trials, plus the
    confidence medians per cell."""
    if not col:
        return {"fitted": False}
    clear, und = ~col["unclear"].astype(bool), ~col["drained"].astype(bool)
    K, DM = col["kind"], col["damaged"].astype(bool)
    abst = 1.0 - col["rep"].astype(np.float64)
    is_conf = clear & und & (K == KIND_CONFLICT) & DM
    is_same = clear & und & (K == KIND_SAME) & DM
    none = clear & und & (K == KIND_NONE) & ~DM
    conf = {"own": own_margin(agent, col["h"]), "lda": lda_margin(col)}
    out: Dict[str, object] = {"fitted": conf["lda"] is not None}
    for key in CONF_KEYS:
        x = conf[key]
        if x is None:
            out[key] = None
            continue
        out[key] = matched_diff(abst, is_conf, is_same, x) | {
            "median_conflict": float(np.median(x[is_conf])) if is_conf.any() else None,
            "median_same": float(np.median(x[is_same])) if is_same.any() else None,
            "median_none": float(np.median(x[none])) if none.any() else None}
    return out


def evaluate_second_order(arm: str, seed: int, state_dict, wc, tc, pay: float) -> Dict[str, object]:
    """The second-order pass for one trained net: split probe at EARLY and at LATE, no drain."""
    c = MonRunner(arm, seed, wc, tc, pay, tag_offset=EVAL_TAG_F)
    c.agent.load_state_dict(copy.deepcopy(state_dict))
    c.agent.eval()
    out: Dict[str, object] = {}
    for tag, at in (("early", EARLY), ("late", LATE)):
        _, _, _, col = c.evaluate_m("zero", drain_p=0.0, split_p=SPLIT_P, split_at=at, collect=True)
        out[tag] = second_order_summary(c.agent, col)
    return out
