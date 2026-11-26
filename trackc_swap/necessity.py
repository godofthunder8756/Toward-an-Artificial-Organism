"""P1m (Q-NECESSITY): does the integrity variable add value for the agent against the strongest simpler rival?

Additive module; every earlier module is imported, never modified. Protocol: P1M_NECESSITY_PROTOCOL.md.

P1h-P1l: a content-free integrity variable in the damage-trained agent sets its confidence, generalizes across
damage and is readable by a second consumer. The constitution credits a building block only on Q-NECESSITY:
what it adds against the strongest simpler rival with matched information, experience and substrate.

Currency: the probe's own payoff (P1 design): a correct report +1, a wrong report -WRONG (4), no report 0, on
clear trials (stored value = true cue). Reporting pays only above 0.8 reliability.

Lesion (online): the integrity variable is removed wherever it lives. Pass R records the state at every step
of the EARLY probe trial from the damage (delay step 1) to the readout (step 9); per step t, P1j's
direction d_t (value-balanced conflict - same shift, content and ambiguity directions removed;
steerint.directions) and mu_t, the value-balanced mean coordinate of undamaged (none) trials on d_t/|d_t|.
In the lesion pass, at every step t in 1..9 and for every trial, the coordinate on d_t/|d_t| is clamped to
mu_t (after the update and the damage, before the readout; clipped to [-1, 1]); the state is carried on.
Content, weights, experience and every other direction are untouched.

Values (readout, clear undrained trials; the probe mix of the pass, and reweighted to the natural exposure):
- as used: mean expected payoff under the agent's own policy, E[r|h] = p(report value) - WRONG p(report other);
- thresholded: V*(x) = payoff of "report sign(z) if x > tau, else abstain" with tau chosen on one half of the
  trials and scored on the other (two-fold cross-fitted; grid of quantiles of x, plus never/always report);
  x = the agent's own confidence |z|.
- the strongest simpler rival: the lesioned agent, its threshold re-tuned (V*(lesion)): the same agent, the
  same content read, uniformly as cautious as pays, without the selective integrity signal;
- the supplied flag (EXTERNAL bound, never a rival): the lesioned agent's |z| with a supplied damage flag,
  separate thresholds for flagged and unflagged trials (V*(lesion + flag)); the oracle adds the damage size K
  (thresholds per flag x K). Room: if the oracle adds no detectable value over the re-tuned lesioned agent,
  the task leaves integrity information nothing to earn and necessity is not testable in it.
- secondary: the thresholded values under a stricter payoff (wrong report -9).
Simulated variables only.
"""
from __future__ import annotations

import copy
from typing import Dict, Optional

import numpy as np
import torch

from .env import A_REP0, A_REP1
from .gradmon import EVAL_TAG_G, KS_G
from .selfeval import WRONG
from .selfmon import EARLY, KIND_CONFLICT, KIND_NONE, KIND_SAME, SPLIT_P
from .steerint import C_NONE, directions
from .transfer import NOVEL, OpAgent, TransferRunner, damaged_group, none_group

NECESS_TAG = EVAL_TAG_G + 120
STEPS = tuple(range(1, 10))           # delay step of the damage (1) to the readout (9)
NATURAL_MIX = {"none": 0.856, "same": 0.072, "conflict": 0.072}   # P1g: PFATE natural conflict share 0.072


class LesionAgent(OpAgent):
    """OpAgent with an online clamp: for flagged envs, the coordinate on the unit row of `lesion_D` is set to
    `lesion_mu` after the update and the damage."""
    lesion_D: Optional[torch.Tensor] = None
    lesion_mu: Optional[torch.Tensor] = None
    lesion_on: Optional[torch.Tensor] = None

    def step(self, obs, h, over=None, donor=None, mask=None):
        push, self.push = self.push, None
        _, _, h = super().step(obs, h, over, donor, mask)
        if self.lesion_on is not None and bool(self.lesion_on.any()):
            D = self.lesion_D
            coord = (h * D).sum(1)
            delta = torch.where(self.lesion_on, coord - self.lesion_mu, torch.zeros_like(coord))
            h = torch.clamp(h - delta[:, None] * D, -1.0, 1.0)
        if push is not None:
            h = torch.clamp(h + push, -1.0, 1.0)
        return self.pi(h), self.v(h).squeeze(-1), h


class LesionRunner(TransferRunner):
    """TransferRunner with an all-steps record (mode 'record_all') and the online lesion (self.lesion)."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        sd = copy.deepcopy(self.agent.state_dict())
        self.agent = LesionAgent(self.agent.hidden)
        self.agent.load_state_dict(sd)
        self.lesion: Optional[Dict[int, Dict[str, np.ndarray]]] = None    # step -> {"u": unit d_t, "mu": mu_t}
        self.rec_all: Optional[list] = None

    def rollout(self, gains, learn):
        if learn:
            return super().rollout(gains, learn)
        w, n, H = self.world, self.tc.n_envs, self.agent.hidden
        orig_step = self.agent.step
        runner = self

        def step(obs, h, over=None, donor=None, mask=None):
            since = w.since()
            live = w.active & (since >= STEPS[0]) & (since <= STEPS[-1])
            if runner.lesion is not None and live.any():
                D = np.zeros((n, H))
                mu = np.zeros(n)
                on = np.zeros(n, dtype=bool)
                for t, v in runner.lesion.items():
                    m = live & (since == t)
                    if m.any():
                        D[m], mu[m], on[m] = v["u"], v["mu"], True
                runner.agent.lesion_D = torch.from_numpy(D.astype(np.float32))
                runner.agent.lesion_mu = torch.from_numpy(mu.astype(np.float32))
                runner.agent.lesion_on = torch.from_numpy(on)
            else:
                runner.agent.lesion_on = None
            out = orig_step(obs, h, over, donor, mask)
            if runner.mode == "record_all" and live.any():
                hh = out[2].detach().numpy()
                runner.rec_all.append({"h": hh[live].astype(np.float64), "t": since[live].copy(),
                                       "val": w.reg[live].copy(), "kind": w.kind[live].copy(),
                                       "damaged": (w.damaged | (since == w.split_at) & (w.kind > KIND_NONE))[live]
                                       .copy(), "unclear": w.unclear[live].copy(), "drained": w.drained[live].copy()})
            return out

        self.agent.step = step
        try:
            return super().rollout(gains, learn)
        finally:
            del self.agent.step
            self.agent.lesion_on = None


def step_directions(rec: Dict[str, np.ndarray], seed: int) -> Dict[int, Dict[str, np.ndarray]]:
    """Per step t: unit d_t and mu_t (value-balanced none-trial mean coordinate)."""
    out = {}
    for t in STEPS:
        m = rec["t"] == t
        sub = {k: v[m] for k, v in rec.items() if k != "t"}
        dr = directions(sub, seed + t)
        if not dr.get("ok"):
            continue
        u = dr["d"] / np.linalg.norm(dr["d"])
        nn = none_group(sub["kind"], sub["damaged"], sub["unclear"]) & ~sub["drained"].astype(bool)
        val = sub["val"].astype(np.int64)
        pr = sub["h"] @ u
        mu = 0.5 * (pr[nn & (val == 0)].mean() + pr[nn & (val == 1)].mean())
        out[t] = {"u": u, "mu": float(mu), "norm_d": float(dr["norm_d"])}
    return out


def payoff_policy(agent, H: np.ndarray, val: np.ndarray) -> np.ndarray:
    with torch.no_grad():
        p = torch.softmax(agent.pi(torch.as_tensor(H, dtype=torch.float32)), -1).numpy().astype(np.float64)
    ok = np.where(val == 1, p[:, A_REP1], p[:, A_REP0])
    bad = np.where(val == 1, p[:, A_REP0], p[:, A_REP1])
    return ok - WRONG * bad


WRONG_STRICT = 9.0                    # secondary: a stricter payoff (report only above 0.9 reliability)


def _thr_payoff(x, right, tau, wrong=WRONG):
    rep = x > tau
    return np.where(rep, np.where(right, 1.0, -wrong), 0.0)


def _best_tau(x, right, wts, wrong=WRONG):
    cands = np.r_[-np.inf, np.quantile(x, np.linspace(0, 1, 101)), np.inf]
    vals = [np.sum(wts * _thr_payoff(x, right, t, wrong)) / np.sum(wts) for t in cands]
    return cands[int(np.argmax(vals))]


def v_star(x, right, wts, seed, groups=None, wrong=WRONG) -> float:
    """Two-fold cross-fitted payoff of the best threshold rule on x (per group when groups is given)."""
    rng = np.random.default_rng(seed)
    fold = rng.integers(0, 2, len(x))
    pay = np.zeros(len(x))
    gs = np.zeros(len(x), dtype=np.int64) if groups is None else groups
    for f in (0, 1):
        tr, te = fold != f, fold == f
        for g in np.unique(gs):
            a, b = tr & (gs == g), te & (gs == g)
            if a.sum() == 0 or b.sum() == 0:
                continue
            tau = _best_tau(x[a], right[a], wts[a], wrong)
            pay[b] = _thr_payoff(x[b], right[b], tau, wrong)
    return float(np.sum(wts * pay) / np.sum(wts))


def values(agent, col, op: str, seed: int) -> Dict[str, object]:
    """Payoffs at the readout for one pass: as used and thresholded, probe mix and natural mix; per group."""
    und = ~col["drained"].astype(bool) & ~col["unclear"].astype(bool)
    val = col["val"].astype(np.int64)
    dm = und & damaged_group(op, col["kind"], col["damaged"], col["unclear"])
    sm = und & damaged_group("same", col["kind"], col["damaged"], col["unclear"]) if op == "donor" else None
    nn = und & none_group(col["kind"], col["damaged"], col["unclear"])
    keep = dm | nn | (sm if sm is not None else False)
    H, val = col["h"][keep], val[keep]
    grp = np.where(dm[keep], 2, np.where(nn[keep], 0, 1))          # 0 none, 1 same, 2 damaged (conflict / op)
    with torch.no_grad():
        lg = agent.pi(torch.as_tensor(H, dtype=torch.float32)).numpy().astype(np.float64)
    z = lg[:, A_REP1] - lg[:, A_REP0]
    right = (z > 0) == (val == 1)
    conf = np.abs(z)
    used = payoff_policy(agent, H, val)
    w_probe = np.ones(len(z))
    nat = {0: NATURAL_MIX["none"], 1: NATURAL_MIX["same"], 2: NATURAL_MIX["conflict"]}
    if op != "donor":
        nat = {0: NATURAL_MIX["none"], 2: 1.0 - NATURAL_MIX["none"]}
    counts = {g: max(int((grp == g).sum()), 1) for g in np.unique(grp)}
    w_nat = np.array([nat.get(g, 0.0) / counts[g] for g in grp])
    flag = (grp == 2).astype(np.int64)
    oracle = np.where(grp == 2, col["k"][keep], 0).astype(np.int64)      # supplied flag and damage size
    out: Dict[str, object] = {"n": {str(g): int((grp == g).sum()) for g in (0, 1, 2)},
                              "acc": {str(g): float(right[grp == g].mean()) if (grp == g).any() else None
                                      for g in (0, 1, 2)},
                              "used_by_group": {str(g): float(used[grp == g].mean()) if (grp == g).any() else None
                                                for g in (0, 1, 2)}}
    for mix, wts in (("probe", w_probe), ("natural", w_nat)):
        out[f"used_{mix}"] = float(np.sum(wts * used) / np.sum(wts))
        out[f"vstar_{mix}"] = v_star(conf, right, wts, seed)
        out[f"vstar_flag_{mix}"] = v_star(conf, right, wts, seed, groups=flag)
        out[f"vstar_oracle_{mix}"] = v_star(conf, right, wts, seed, groups=oracle)
    out["vstar_strict"] = v_star(conf, right, w_probe, seed, wrong=WRONG_STRICT)
    out["vstar_oracle_strict"] = v_star(conf, right, w_probe, seed, groups=oracle, wrong=WRONG_STRICT)
    return out


def collect_necessity(seed: int, weights: Dict[str, dict], wc, tc, pay: float, base: float, arms,
                      ops=("donor",) + NOVEL, ks=KS_G) -> Dict[str, Dict[str, object]]:
    out: Dict[str, Dict[str, object]] = {}
    for arm in arms:
        c = LesionRunner(arm, seed, wc, tc, pay, tag_offset=NECESS_TAG, base=base, ks=ks)
        c.agent.load_state_dict(copy.deepcopy(weights[arm]))
        c.agent.eval()
        c.agent.gen_op = torch.Generator().manual_seed(seed * 7919 + 23)

        def run(op, mode=None, lesion=None):
            c.agent.op, c.mode, c.lesion = op, mode, lesion
            c.rec_all = [] if mode == "record_all" else None
            c.cond[:] = C_NONE
            c.cond_cue[:] = -10 ** 9
            _, _, _, col = c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, probe_ks=c.ks,
                                        base_on=False, collect=mode != "record_all")
            return col

        run("donor", "record_all")
        rec = {k: np.concatenate([r[k] for r in c.rec_all]) for k in c.rec_all[0]}
        les = step_directions(rec, seed)
        res: Dict[str, object] = {"fitted": len(les) == len(STEPS),
                                  "norm_d": {str(t): v["norm_d"] for t, v in les.items()}, "ops": {}}
        if not res["fitted"]:
            out[arm] = res
            continue
        lesion = {t: {"u": v["u"], "mu": v["mu"]} for t, v in les.items()}
        for op in ops:
            r = {}
            for cond, lz in (("intact", None), ("lesion", lesion)):
                col = run(op, None, lz)
                r[cond] = values(c.agent, col, op, seed)
            res["ops"][op] = r
        out[arm] = res
    return out
