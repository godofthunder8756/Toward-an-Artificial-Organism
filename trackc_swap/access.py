"""P1l: is the integrity variable accessible to a second consumer, and is it the same variable?

Additive module; every earlier module is imported, never modified. Protocol: P1L_ACCESS_PROTOCOL.md.

P1j/P1k: a content-free direction d in the damage-trained agent's state is produced by anomalous damage to its
memory (also damage never seen in training) and causally sets its confidence. Its only shown consumer is the
policy's own report confidence. P1l adds a second consumer and asks whether it gets the same variable.

The second consumer: a linear read-out on the state at the readout step (delay step 9, the state the policy
reads), trained to say "my memory was corrupted": label 1 on clear trials whose memory took a donor overwrite
with the other value (conflict), label 0 on clear undamaged trials and on same-value overwrites. It is fitted
on the frozen agent's states from one pass of the trained damage only (logistic regression, standardized
state, L2 1e-3). Being linear in the state it cannot use the value-signed content (whose sign flips with the
stored value), so it must read value-independent structure.

Tests (fresh passes; value-balanced AUC = mean of the within-value AUCs):
- held-out validity: AUC conflict vs none on the trained damage;
- generality: AUC damaged vs none under scramble, noise and zero (never seen in training, never seen by
  the read-out), and same-value overwrites vs none (a perturbation leaving a valid state);
- shared variable: in a P1j steering pass (d and the random control r at natural size at delay step 5;
  same trials +d / +r, conflict trials -d / -r), the read-out's score at step 9:
    induce_rep = score(same, +d) - score(same, +r); rescue_rep = score(conflict, -r) - score(conflict, -d);
    signed_rep = induce_rep + rescue_rep  (> 0: moving d moves the second consumer as the variable implies)
  and, as a check, the same pass's confidence effects (P1j's induce and rescue);
- alignment: on the held-out trained-damage pass (clear trials), the within-value correlation of the read-out's
  score with the state's projection on d9 (P1j's direction computed at the readout step) and, as a check, on
  the content direction c9.
Simulated variables only.
"""
from __future__ import annotations

import copy
from typing import Dict, Optional

import numpy as np
import torch

from .calibdisc import auc
from .gradmon import EVAL_TAG_G, KS_G
from .secondorder import own_margin
from .selfmon import EARLY, KIND_CONFLICT, KIND_NONE, KIND_SAME, SPLIT_P
from .steerint import C_D, C_NONE, C_R, S_INJ, SteerRunner, directions
from .transfer import NOVEL, TransferRunner, damaged_group, none_group

ACCESS_TAG = EVAL_TAG_G + 80
STEER_TAG_L = EVAL_TAG_G + 100
L2 = 1e-3
N_FIT_MIN = 50


def fit_readout(H: np.ndarray, y: np.ndarray, l2: float = L2) -> Dict[str, np.ndarray]:
    """Logistic regression on the standardized state (LBFGS). Returns mu, sd, w, b."""
    mu, sd = H.mean(0), H.std(0) + 1e-6
    X = torch.tensor((H - mu) / sd, dtype=torch.float64)
    Y = torch.tensor(y.astype(np.float64))
    w = torch.zeros(H.shape[1], dtype=torch.float64, requires_grad=True)
    b = torch.zeros(1, dtype=torch.float64, requires_grad=True)
    opt = torch.optim.LBFGS([w, b], max_iter=500, line_search_fn="strong_wolfe")

    def closure():
        opt.zero_grad()
        loss = torch.nn.functional.binary_cross_entropy_with_logits(X @ w + b, Y) + l2 * (w * w).sum()
        loss.backward()
        return loss
    opt.step(closure)
    return {"mu": mu, "sd": sd, "w": w.detach().numpy(), "b": float(b.detach())}


def score_readout(ro: Dict[str, np.ndarray], H: np.ndarray) -> np.ndarray:
    return ((H - ro["mu"]) / ro["sd"]) @ ro["w"] + ro["b"]


def vb_auc(s: np.ndarray, val: np.ndarray, pos: np.ndarray, neg: np.ndarray, n_min: int = 20) -> Optional[float]:
    """Mean over the stored value of the within-value AUC of s for pos against neg."""
    out = []
    for v in (0, 1):
        p, n = pos & (val == v), neg & (val == v)
        if p.sum() < n_min or n.sum() < n_min:
            return None
        out.append(auc(s[p], s[n]))
    return float(np.mean(out))


def _vb(x, val, m, n_min=20):
    vs = []
    for v in (0, 1):
        mm = m & (val == v)
        if mm.sum() < n_min:
            return None
        vs.append(float(x[mm].mean()))
    return 0.5 * (vs[0] + vs[1])


def _vb_corr(x, z, val, m) -> Optional[float]:
    """Mean over the stored value of the within-value Pearson correlation of x and z on m."""
    out = []
    for v in (0, 1):
        mm = m & (val == v)
        if mm.sum() < 20 or x[mm].std() == 0 or z[mm].std() == 0:
            return None
        out.append(float(np.corrcoef(x[mm], z[mm])[0, 1]))
    return float(np.mean(out))


def _cat(rows):
    return {k: np.concatenate([r[k] for r in rows]) for k in rows[0]} if rows else None


def collect_access(seed: int, weights: Dict[str, dict], wc, tc, pay: float, base: float, arms,
                   s_inj: int = S_INJ, ks=KS_G) -> Dict[str, Dict[str, object]]:
    out: Dict[str, Dict[str, object]] = {}
    for arm in arms:
        c = TransferRunner(arm, seed, wc, tc, pay, tag_offset=ACCESS_TAG, base=base, ks=ks)
        c.agent.load_state_dict(copy.deepcopy(weights[arm]))
        c.agent.eval()
        c.agent.gen_op = torch.Generator().manual_seed(seed * 7907 + 5)
        c.s_inj = s_inj

        def run(op, mode=None, collect=True):
            c.agent.op, c.mode = op, mode
            c.rec = [] if mode == "record" else None
            c.cond[:] = C_NONE
            c.cond_cue[:] = -10 ** 9
            _, _, _, col = c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, probe_ks=c.ks,
                                        base_on=False, collect=collect)
            return col

        run("donor", "record", collect=False)
        dirs = directions(_cat(c.rec), seed)
        res: Dict[str, object] = {"fitted": False}
        if not dirs.get("ok"):
            out[arm] = res
            continue
        tr = run("donor")
        und = ~tr["drained"].astype(bool)
        val = tr["val"].astype(np.int64)
        pos = und & damaged_group("donor", tr["kind"], tr["damaged"], tr["unclear"])
        neg = und & (none_group(tr["kind"], tr["damaged"], tr["unclear"])
                     | damaged_group("same", tr["kind"], tr["damaged"], tr["unclear"]))
        if pos.sum() < N_FIT_MIN or neg.sum() < N_FIT_MIN:
            out[arm] = res
            continue
        fit = pos | neg
        ro = fit_readout(tr["h"][fit], pos[fit].astype(np.int64))
        d9 = directions({k: tr[k] for k in ("h", "val", "kind", "damaged", "unclear", "drained")}, seed)
        res = {"fitted": True, "n_fit": int(fit.sum()), "n_pos": int(pos.sum()), "auc": {}}
        # held-out passes, one per operator
        for op in ("donor", "same") + NOVEL:
            col = run(op)
            u = ~col["drained"].astype(bool)
            v = col["val"].astype(np.int64)
            s = score_readout(ro, col["h"])
            nn = u & none_group(col["kind"], col["damaged"], col["unclear"])
            dm = u & damaged_group(op, col["kind"], col["damaged"], col["unclear"])
            res["auc"][op] = vb_auc(s, v, dm, nn)
            if op == "donor":
                sm = u & damaged_group("same", col["kind"], col["damaged"], col["unclear"])
                res["auc"]["donor_vs_same"] = vb_auc(s, v, dm, sm)
                clr = u & ~col["unclear"].astype(bool)
                c9 = (tr["h"][und & none_group(tr["kind"], tr["damaged"], tr["unclear"]) & (val == 1)].mean(0)
                      - tr["h"][und & none_group(tr["kind"], tr["damaged"], tr["unclear"]) & (val == 0)].mean(0))
                res["corr_d9"] = _vb_corr(s, col["h"] @ d9["d"], v, clr) if d9.get("ok") else None
                res["corr_c9"] = _vb_corr(s, col["h"] @ c9, v, clr)
        # steering pass (P1j's design, natural size): does moving d move the second consumer?
        sr = SteerRunner(arm, seed, wc, tc, pay, tag_offset=STEER_TAG_L, base=base, ks=ks)
        sr.agent.load_state_dict(copy.deepcopy(weights[arm]))
        sr.agent.eval()
        sr.s_inj, sr.mode, sr.dirs = s_inj, "push", {"d": dirs["d"], "r": dirs["r"]}
        sr.gen_steer = np.random.default_rng(seed * 41 + 3)
        _, _, _, col = sr.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, collect=True,
                                     probe_ks=sr.ks, base_on=False)
        u = ~col["drained"].astype(bool)
        v, cnd = col["val"].astype(np.int64), col["cond"]
        clear = ~col["unclear"].astype(bool)
        dmg = col["damaged"].astype(bool)
        same = u & clear & dmg & (col["kind"] == KIND_SAME)
        conf = u & clear & dmg & (col["kind"] == KIND_CONFLICT)
        s = score_readout(ro, col["h"])
        own = own_margin(sr.agent, col["h"])
        g = lambda x, m, cc: _vb(x, v, m & (cnd == cc))
        dif = lambda a, b2: None if a is None or b2 is None else float(a - b2)
        res["induce_rep"] = dif(g(s, same, C_D), g(s, same, C_R))
        res["rescue_rep"] = dif(g(s, conf, C_R), g(s, conf, C_D))
        res["signed_rep"] = (None if res["induce_rep"] is None or res["rescue_rep"] is None
                             else res["induce_rep"] + res["rescue_rep"])
        res["gap_rep"] = dif(g(s, conf, C_NONE), g(s, same, C_NONE))
        res["induce_conf"] = dif(g(own, same, C_R), g(own, same, C_D))
        res["rescue_conf"] = dif(g(own, conf, C_D), g(own, conf, C_R))
        out[arm] = res
    return out
