"""P1h: is P1g's second-order residue explained by a non-linear read of the content evidence?

Additive module; every earlier module is imported, never modified. Protocol: P1H_EVIDENCE_PROTOCOL.md.

P1g found that, at matched own report-logit gap, a conflict in the agent's memory still raises abstention a
little (M2_nn_own 0.005, 25/27 seeds); post-hoc, about half of it went when the LDA margin was matched too.
The open question: is the rest first-order information in a non-linear form?

Two changes against P1g's measure, both fixed before the analysis is run:
1. **Outcome:** the policy's exact abstention probability at the report step, p_abs = 1 - p(REP0) - p(REP1)
   from the policy head on the collected GRU state (the state the action was sampled from), instead of the
   sampled action. Same quantity in expectation; no sampling noise on a rare event.
2. **Confidence matched:** an *evidence* decoder: a small MLP reading the stored value from the state,
   trained only on trials whose content is unambiguous (undamaged trials without an event, and trials
   overwritten with the same value), five-fold cross-fitted; every trial (conflict trials included) is scored
   by exactly one fold model, assigned at random. It never sees a conflict, so its margin is how strongly
   the state points to a value, read non-linearly, without any knowledge of conflicts. (A decoder trained on
   conflicts would learn that conflicted states are less reliable and so absorb, by construction, the very
   signal under test.)
The primary match is joint: own report-logit gap and evidence margin, each within 0.1 SD (in synthetic
first-order-only controls the evidence margin alone leaks up to about 2% of the unmatched gap, the joint match
at most 0.4%; test_p1h_evidence.py).
"""
from __future__ import annotations

import copy
from typing import Dict, Optional, Sequence

import numpy as np
import torch

from .env import A_REP0, A_REP1, WorldConfig
from .gradmon import CALIPER, EVAL_TAG_G, KS_G, NN_MIN, GradRunner, matched_nn
from .secondorder import lda_margin, own_margin
from .selfmon import ARMS_M, EARLY, KIND_CONFLICT, KIND_NONE, KIND_SAME, LATE, LEADS_M, P_MAX_M, RATE_M, SPLIT_P
from .train import TrainConfig

FOLDS_E = 5
HIDDEN_E = 64
EPOCHS_E = 50          # chosen on one P1g seed (3200, PFATE, EARLY) from held-out decoder loss only
WD_E = 1e-3
LR_E = 3e-3
BATCH_E = 512
JOINT_CAL = 0.1        # joint (own, evidence) match: within 0.1 SD on each
DEC_VALID = 0.95       # evidence decoder: held-out accuracy on none and same trials


def p_abstain(agent, h: np.ndarray) -> np.ndarray:
    """Exact probability of not reporting (any action other than REP0 / REP1) under the policy head."""
    with torch.no_grad():
        pr = torch.softmax(agent.pi(torch.as_tensor(h, dtype=torch.float32)), -1).numpy().astype(np.float64)
    return 1.0 - pr[:, A_REP0] - pr[:, A_REP1]


def _mlp(d_in: int, hidden: int) -> torch.nn.Module:
    return torch.nn.Sequential(torch.nn.Linear(d_in, hidden), torch.nn.ReLU(), torch.nn.Linear(hidden, hidden),
                               torch.nn.ReLU(), torch.nn.Linear(hidden, 1))


def evidence_logit(H: np.ndarray, y: np.ndarray, fit: np.ndarray, score: np.ndarray, seed: int = 0,
                   hidden: int = HIDDEN_E, epochs: int = EPOCHS_E, folds: int = FOLDS_E) -> np.ndarray:
    """Cross-fitted MLP logit of the value. Fit trials are split into `folds` parts; each fold model is
    trained on the other parts and scores its own part. Every other trial in `score` is assigned to one
    fold model at random. Returns a logit for each trial in fit | score (NaN elsewhere)."""
    g = np.random.default_rng(seed)
    fi = np.flatnonzero(fit)
    g.shuffle(fi)
    fold_of = np.full(len(y), -1)
    for f, part in enumerate(np.array_split(fi, folds)):
        fold_of[part] = f
    other = np.flatnonzero(score & ~fit)
    fold_of[other] = g.integers(0, folds, len(other))
    mu, sd = H[fit].mean(0), H[fit].std(0) + 1e-6
    X = torch.tensor((H - mu) / sd, dtype=torch.float32)
    Y = torch.tensor(y, dtype=torch.float32)
    out = np.full(len(y), np.nan)
    gen = torch.Generator().manual_seed(seed)
    for f in range(folds):
        tr = torch.as_tensor(np.flatnonzero(fit & (fold_of != f)))
        te = np.flatnonzero((fit | score) & (fold_of == f))
        torch.manual_seed(seed * 1000 + f)
        net = _mlp(H.shape[1], hidden)
        opt = torch.optim.Adam(net.parameters(), lr=LR_E, weight_decay=WD_E)
        Xt, Yt = X[tr], Y[tr]
        for _ in range(epochs):
            perm = torch.randperm(len(tr), generator=gen)
            for b in range(0, len(tr), BATCH_E):
                bi = perm[b:b + BATCH_E]
                opt.zero_grad()
                torch.nn.functional.binary_cross_entropy_with_logits(net(Xt[bi]).squeeze(-1), Yt[bi]).backward()
                opt.step()
        with torch.no_grad():
            out[te] = net(X[te]).squeeze(-1).numpy()
    return out


def joint_nn(outcome: np.ndarray, is_conf: np.ndarray, is_same: np.ndarray, xs: Sequence[np.ndarray],
             cal: float = JOINT_CAL, n_min: int = NN_MIN) -> Dict[str, object]:
    """Nearest same trial in standardized multi-d distance (with replacement), kept if within `cal` SD in
    every dimension."""
    pool = is_conf | is_same
    Z = np.stack([x / (x[pool].std() or 1.0) for x in xs], 1)
    ci, si = np.flatnonzero(is_conf), np.flatnonzero(is_same)
    out = {"M2": None, "coverage": 0.0, "n_pairs": 0}
    if len(ci) == 0 or len(si) < 2:
        return out
    Zs = torch.as_tensor(Z[si])
    pairs = []
    for b in range(0, len(ci), 1024):
        cb = ci[b:b + 1024]
        d = torch.cdist(torch.as_tensor(Z[cb]), Zs)
        j = d.argmin(1).numpy()
        ok = (np.abs(Z[si[j]] - Z[cb]) <= cal).all(1)
        pairs += list(zip(cb[ok], si[j[ok]]))
    out["n_pairs"], out["coverage"] = len(pairs), len(pairs) / len(ci)
    if len(pairs) >= n_min:
        p = np.array(pairs)
        out["M2"] = float((outcome[p[:, 0]] - outcome[p[:, 1]]).mean())
    return out


def trace_auc(H: np.ndarray, is_conf: np.ndarray, is_same: np.ndarray, x: np.ndarray, seed: int = 0,
              folds: int = FOLDS_E) -> Dict[str, object]:
    """Is there an integrity trace at matched evidence? A cross-fitted L2 logistic classifier of conflict
    against same on the standardized state; reported: its AUC over all conflict and same trials, and the share
    of evidence-matched pairs (caliper as matched_nn) in which the conflict trial scores higher."""
    m = is_conf | is_same
    idx = np.flatnonzero(m)
    if is_conf.sum() < 20 or is_same.sum() < 20:
        return {"auc": None, "pair_auc": None}
    g = np.random.default_rng(seed + 1)
    g.shuffle(idx)
    mu, sd = H[m].mean(0), H[m].std(0) + 1e-6
    X = torch.tensor((H - mu) / sd, dtype=torch.float32)
    Y = torch.tensor(is_conf.astype(np.float32))
    s = np.full(len(H), np.nan)
    for f, te in enumerate(np.array_split(idx, folds)):
        tr = torch.as_tensor(np.setdiff1d(idx, te))
        torch.manual_seed(seed * 1000 + 500 + f)
        w = torch.zeros(H.shape[1], requires_grad=True)
        b = torch.zeros(1, requires_grad=True)
        opt = torch.optim.LBFGS([w, b], max_iter=200)

        def closure():
            opt.zero_grad()
            loss = torch.nn.functional.binary_cross_entropy_with_logits(X[tr] @ w + b, Y[tr]) + 1e-3 * (w * w).sum()
            loss.backward()
            return loss
        opt.step(closure)
        with torch.no_grad():
            s[te] = (X[te] @ w + b).numpy()
    sc, ss = s[is_conf], s[is_same]
    auc = float((sc[:, None] > ss[None, :]).mean() + 0.5 * (sc[:, None] == ss[None, :]).mean())
    # pairs matched on evidence
    pool = is_conf | is_same
    sdx = float(x[pool].std()) or 1.0
    xs_i = np.flatnonzero(is_same)
    o = np.argsort(x[xs_i], kind="stable")
    xs_i = xs_i[o]
    xs = x[xs_i]
    ci = np.flatnonzero(is_conf)
    j = np.clip(np.searchsorted(xs, x[ci]), 1, len(xs) - 1)
    nn = np.where(np.abs(xs[j - 1] - x[ci]) <= np.abs(xs[j] - x[ci]), j - 1, j)
    ok = np.abs(xs[nn] - x[ci]) <= CALIPER * sdx
    pair_auc = float((s[ci[ok]] > s[xs_i[nn[ok]]]).mean()) if ok.sum() >= NN_MIN else None
    return {"auc": auc, "pair_auc": pair_auc}


def evidence_summary(agent, col: Optional[Dict[str, np.ndarray]], seed: int = 0) -> Dict[str, object]:
    """All P1h measures on one graded-probe run (clear, undrained trials)."""
    if not col:
        return {"fitted": False}
    clear, und = ~col["unclear"].astype(bool), ~col["drained"].astype(bool)
    K, DM = col["kind"], col["damaged"].astype(bool)
    is_conf = clear & und & (K == KIND_CONFLICT) & DM
    is_same = clear & und & (K == KIND_SAME) & DM
    none = clear & und & (K == KIND_NONE) & ~DM
    H, y = col["h"], col["val"].astype(np.int64)
    pab = p_abstain(agent, H)
    sampled = 1.0 - col["rep"].astype(np.float64)
    own = own_margin(agent, H)
    fit = none | is_same
    if min(int((fit & (y == 0)).sum()), int((fit & (y == 1)).sum())) < 50 or is_conf.sum() < NN_MIN:
        return {"fitted": False}
    lg = evidence_logit(H, y, fit, is_conf, seed=seed)
    ev = np.abs(np.nan_to_num(lg))
    lg2 = evidence_logit(H, y, fit, is_conf, seed=seed + 7, hidden=32)
    ev2 = np.abs(np.nan_to_num(lg2))
    acc = lambda m: float(((lg[m] > 0) == y[m]).mean()) if m.any() else None
    lda = lda_margin(col)
    out: Dict[str, object] = {
        "fitted": True,
        "dec_acc_none": acc(none), "dec_acc_same": acc(is_same), "dec_acc_conflict": acc(is_conf),
        "ev_conflict": float(np.median(ev[is_conf])), "ev_same": float(np.median(ev[is_same])),
        "pabs_conflict": float(pab[is_conf].mean()), "pabs_same": float(pab[is_same].mean()),
        "pabs_none": float(pab[none].mean()) if none.any() else None,
        "E": matched_nn(pab, is_conf, is_same, ev),
        "E_sampled": matched_nn(sampled, is_conf, is_same, ev),
        "E_alt": matched_nn(pab, is_conf, is_same, ev2),
        "own_p": matched_nn(pab, is_conf, is_same, own),
        "own_sampled": matched_nn(sampled, is_conf, is_same, own),
        "lda_p": matched_nn(pab, is_conf, is_same, lda) if lda is not None else {"M2": None},
        "joint_p": joint_nn(pab, is_conf, is_same, [own, ev]),
        "trace": trace_auc(H, is_conf, is_same, ev, seed=seed),
    }
    return out


def collect_graded(seed: int, weights: Dict[str, dict], wc: WorldConfig, tc: TrainConfig, pay: float,
                   base: float, ks: Sequence[int] = KS_G) -> Dict[str, Dict[str, object]]:
    """Re-collects P1g's graded probe B at one point exactly as gradmon.evaluate_point_g does (fresh copies,
    tag offset 160; natural running, then per arm split probe A and graded probe B at EARLY and LATE) and
    returns {arm: {"early": (agent, col), "late": (agent, col)}}."""
    copies = {}
    for a in ARMS_M:
        c = GradRunner(a, seed, wc, tc, pay, tag_offset=EVAL_TAG_G, rate=RATE_M, p_max=P_MAX_M, base=base, ks=ks)
        c.agent.load_state_dict(copy.deepcopy(weights[a]))
        c.agent.eval()
        copies[a] = c
    lead = {}
    for a, c in copies.items():
        if a not in LEADS_M:
            _, g, _, _ = c.evaluate_g("own" if a == "PFATE" else "zero")
            lead[a] = g
    for a, c in copies.items():
        if a in LEADS_M:
            c.evaluate_g("replay", lead[LEADS_M[a]])
    out: Dict[str, Dict[str, object]] = {}
    for a, c in copies.items():
        out[a] = {}
        for tag, at in (("early", EARLY), ("late", LATE)):
            c.evaluate_g("zero", drain_p=0.5, split_p=SPLIT_P, split_at=at, collect=True, base_on=False)
            _, _, _, col = c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=at, collect=True,
                                        probe_ks=c.ks, base_on=False)
            out[a][tag] = (c.agent, col)
    return out
