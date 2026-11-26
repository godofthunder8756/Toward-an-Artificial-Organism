"""P1j: does a content-free integrity variable causally set the agent's confidence in its own memory?

Additive module; every earlier module is imported, never modified. Protocol: P1J_STEER_PROTOCOL.md.

Why. P1h/P1i found that after a conflicting overwrite the damage-trained agent's report confidence (its own
report margin |z|, z = logit(REP1) - logit(REP0), a linear readout of the GRU state) is lower than a clean
decoder's evidence says, in proportion to how unreliable such memories are. Because the confidence IS the
size of the agent's own decision variable, that finding is open to a first-order account: the agent reads
damaged content differently (better) than the decoder. The question left is causal and about organization:
is there a component of the state that does not depend on the stored value (content-free), that the
dynamics produce after a conflict, and that turns the confidence in the content down?

Method (EARLY probe only: overwrite at delay step 1, readout at step 9; graded K; clear, undrained trials):
- Pass 1 (estimation; fresh evaluation worlds): states at delay step S_INJ for none / same / conflict trials
  (clear) and none trials with unclear evidence.
    c      content direction: mean(none | val 1) - mean(none | val 0)
    d_raw  value-balanced conflict shift: mean over val of [mean(conflict | val) - mean(same | val)]
    a      value-balanced ambiguity shift: mean over val of [mean(unclear none | val) - mean(clear none | val)]
    d      d_raw with its projection on span(c, a) removed (conflict-specific, content-free, not ambiguity)
    r      a random direction orthogonal to c, a and d, with the norm of d (control)
- Pass 2 (intervention; the next worlds of the same copies): at delay step S_INJ each targeted trial is
  assigned at random to no push, the d push, or the r push (same and none trials: +d / +r; conflict trials:
  -d / -r), added to the state after the recurrent update (and clipped to the GRU range [-1, 1]); the state
  is carried forward and read out at step 9.
- Pass 3: as pass 2 with d and r rescaled to the norm NORM_FIX, so that arms whose natural conflict shift is
  small are pushed as hard as the others (the size-matched comparison of arms).
- Measures (passes 2 and 3, readout step, value-balanced means): own margin |z|, exact abstention probability p_abs,
  the agent's accuracy (sign of z against the stored value).
    induce   |z|(same, +r) - |z|(same, +d)        > 0: the d push lowers confidence on intact content
    rescue   |z|(conflict, -d) - |z|(conflict, -r) > 0: removing d restores confidence on conflicts
    gap      |z|(same, none) - |z|(conflict, none) (the natural drop; shares induce/gap, rescue/gap)
    and the same for p_abs (abstention: induce_abs = p_abs(same, +d) - p_abs(same, +r), rescue_abs =
    p_abs(conflict, -r) - p_abs(conflict, -d)), the accuracy changes (content preserved?), and none trials.
Value balance: every mean is the mean over val 0 and val 1 of the within-val means, so a push that only shifts
z by a constant (raising |z| for one value and lowering it for the other) contributes nothing.

Simulated variables only. No operator, stop, shutdown or host variable exists; no process is terminated.
"""
from __future__ import annotations

import copy
from typing import Dict, List, Optional

import numpy as np
import torch

from .env import A_REP0, A_REP1
from .evidence import p_abstain
from .gradmon import EVAL_TAG_G, KS_G, GradRunner
from .secondorder import own_margin
from .selfmon import EARLY, KIND_CONFLICT, KIND_NONE, KIND_SAME, SPLIT_P, MonAgent

S_INJ = 5                   # delay step of the push (overwrite at 1, readout at 9)
STEER_TAG = EVAL_TAG_G + 40  # evaluation world streams of P1j (P1g/P1h/P1i used EVAL_TAG_G)
N_DIR_MIN = 30              # pass 1: at least this many trials per group and value
N_CELL_MIN = 20             # pass 2: at least this many trials per group, condition and value
NORM_FIX = 1.0              # pass 3: the same pushes rescaled to this norm (a size-matched comparison of arms)
C_NONE, C_D, C_R = 0, 1, 2
GROUPS = ("same", "conflict", "none")


class SteerAgent(MonAgent):
    """MonAgent with an additive push on the state after the update and the damage, before the readout."""
    push: Optional[torch.Tensor] = None

    def step(self, obs, h, over=None, donor=None, mask=None):
        h = self.core(torch.relu(self.enc(obs)), h)
        if over is not None and bool(over.any()):
            m = over[:, None] & mask
            h = torch.where(m, h[donor].detach(), h)
        if self.push is not None:
            h = torch.clamp(h + self.push, -1.0, 1.0)
        return self.pi(h), self.v(h).squeeze(-1), h


class SteerRunner(GradRunner):
    """GradRunner whose evaluation rollout (learn=False) can record the states at delay step s_inj (pass 1)
    and push them (pass 2). With mode None it reproduces GradRunner's collection exactly."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        sd = copy.deepcopy(self.agent.state_dict())
        self.agent = SteerAgent(self.agent.hidden)
        self.agent.load_state_dict(sd)
        self.mode: Optional[str] = None          # None | "record" | "push"
        self.s_inj = S_INJ
        self.dirs: Optional[Dict[str, np.ndarray]] = None
        self.rec: Optional[List[Dict[str, np.ndarray]]] = None
        self.gen_steer: Optional[np.random.Generator] = None
        n = self.tc.n_envs
        self.cond = np.zeros(n, dtype=np.int64)
        self.cond_cue = np.full(n, -10 ** 9, dtype=np.int64)

    def rollout(self, gains, learn):
        if learn:
            return super().rollout(gains, learn)
        tc, w = self.tc, self.world
        n, k = tc.n_envs, self.agent.hidden
        used = []
        h = self.h.detach()
        obs = self.obs
        ks = torch.tensor(self.ks, dtype=torch.int64)
        base = self.base if self.base_on else 0.0
        for t in range(tc.rollout):
            g = np.asarray(w.gain() if gains is None else gains[t], dtype=np.float32)
            used.append(g)
            p = np.minimum(self.p_max, base + self.rate * g.astype(np.float64))
            u = torch.rand(n, generator=self.gen_dmg, dtype=torch.float64).numpy()
            rank = torch.rand((n, k), generator=self.gen_dmg).argsort(dim=1)
            k_nat = ks[torch.randint(len(self.ks), (n,), generator=self.gen_dmg)].numpy()
            live = w.in_delay() & ~w.damaged
            nat = live & (u < p)
            prb = live & (w.kind > KIND_NONE) & (w.since() == w.split_at)
            k_env = np.where(prb, w.kprobe, k_nat)
            mask = rank < torch.from_numpy(k_env)[:, None]
            over_np, donor_np, conflict = self._events(nat, prb)
            over, donor = torch.from_numpy(over_np), torch.from_numpy(donor_np)
            at = w.active & (w.since() == self.s_inj) & w.in_delay()
            self.agent.push = None
            if self.mode == "push" and at.any():
                grp = group_of(w.kind, w.damaged, w.unclear)
                tgt = at & (grp >= 0)
                cnd = np.where(tgt, self.gen_steer.integers(0, 3, n), C_NONE)
                sign = np.where(grp == 1, -1.0, 1.0)            # conflict trials: the push is subtracted
                vec = (np.where(cnd == C_D, 1.0, 0.0)[:, None] * self.dirs["d"][None, :]
                       + np.where(cnd == C_R, 1.0, 0.0)[:, None] * self.dirs["r"][None, :]) * sign[:, None]
                if tgt.any():
                    self.agent.push = torch.from_numpy(vec.astype(np.float32))
                self.cond = np.where(tgt, cnd, self.cond)
                self.cond_cue = np.where(tgt, w.cue_t, self.cond_cue)
            with torch.no_grad():
                logits, v, h = self.agent.step(obs, h, over, donor, mask)
                dist = torch.distributions.Categorical(logits=logits)
                idx = torch.multinomial(dist.probs.detach(), 1, generator=self.gen).squeeze(-1)
            self.agent.push = None
            if self.mode == "record" and at.any():
                self.rec.append({"h": h.numpy()[at].astype(np.float64), "val": w.reg[at].copy(),
                                 "kind": w.kind[at].copy(), "damaged": w.damaged[at].copy(),
                                 "unclear": w.unclear[at].copy(), "drained": w.drained[at].copy()})
            if self.collect is not None:
                pr = w.probe[min(w.t, self.wc.horizon)] & w.active
                if pr.any():
                    a = idx.numpy()[pr]
                    cnd = np.where(self.cond_cue[pr] == w.cue_t[pr], self.cond[pr], -1)
                    self.collect.append({"h": h.detach().numpy()[pr].astype(np.float64), "val": w.reg[pr].copy(),
                                         "unclear": w.unclear[pr].copy(), "drained": w.drained[pr].copy(),
                                         "kind": w.kind[pr].copy(), "damaged": w.damaged[pr].copy(),
                                         "conflict": w.conflict[pr].copy(), "k": w.dmg_k[pr].copy(),
                                         "rep": (a == A_REP0) | (a == A_REP1), "said": (a == A_REP1).astype(np.int64),
                                         "cond": cnd})
            w.mark(over_np, conflict)
            w.mark_k(over_np, k_env)
            w.next_gain = np.zeros(n)
            nobs, r, done = w.step(idx.numpy())
            obs = torch.from_numpy(nobs)
        self.h, self.obs = h, obs
        return np.stack(used)


def group_of(kind, damaged, unclear) -> np.ndarray:
    """0 same (damaged), 1 conflict (damaged), 2 none (undamaged); -1 otherwise (unclear, or probe missed)."""
    g = np.full(len(kind), -1, dtype=np.int64)
    clear = ~np.asarray(unclear, dtype=bool)
    dm = np.asarray(damaged, dtype=bool)
    g[clear & dm & (kind == KIND_SAME)] = 0
    g[clear & dm & (kind == KIND_CONFLICT)] = 1
    g[clear & ~dm & (kind == KIND_NONE)] = 2
    return g


def _vbal_mean(X: np.ndarray, val: np.ndarray, m: np.ndarray) -> Optional[np.ndarray]:
    """Mean over val of the within-val means of X[m]; None if any value has fewer than N_DIR_MIN rows."""
    out = []
    for v in (0, 1):
        mm = m & (val == v)
        if mm.sum() < N_DIR_MIN:
            return None
        out.append(X[mm].mean(0))
    return 0.5 * (out[0] + out[1])


def directions(rec: Dict[str, np.ndarray], seed: int) -> Dict[str, object]:
    """Pass-1 directions at delay step s_inj (see the module docstring)."""
    H, val = rec["h"], rec["val"].astype(np.int64)
    und = ~rec["drained"].astype(bool)
    grp = group_of(rec["kind"], rec["damaged"], rec["unclear"])
    unc_none = und & rec["unclear"].astype(bool) & ~rec["damaged"].astype(bool) & (rec["kind"] == KIND_NONE)
    out: Dict[str, object] = {"ok": False}
    none, same, conf = und & (grp == 2), und & (grp == 0), und & (grp == 1)
    if min(int((none & (val == 0)).sum()), int((none & (val == 1)).sum())) < N_DIR_MIN:
        return out
    c = H[none & (val == 1)].mean(0) - H[none & (val == 0)].mean(0)
    mc, ms, mn, mu = _vbal_mean(H, val, conf), _vbal_mean(H, val, same), _vbal_mean(H, val, none), \
        _vbal_mean(H, val, unc_none)
    if mc is None or ms is None or mn is None or mu is None:
        return out
    d_raw, a = mc - ms, mu - mn
    Q, _ = np.linalg.qr(np.stack([c, a], 1))
    d = d_raw - Q @ (Q.T @ d_raw)
    rng = np.random.default_rng(seed + 4242)
    z = rng.standard_normal(len(d))
    B, _ = np.linalg.qr(np.stack([c, a, d], 1))
    z = z - B @ (B.T @ z)
    r = z / np.linalg.norm(z) * np.linalg.norm(d)
    cos = lambda x, y: float(x @ y / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-12))
    out.update({"ok": True, "d": d, "r": r, "norm_d": float(np.linalg.norm(d)),
                "norm_d_raw": float(np.linalg.norm(d_raw)), "norm_c": float(np.linalg.norm(c)),
                "norm_a": float(np.linalg.norm(a)), "share_d_kept": float(np.linalg.norm(d) / (np.linalg.norm(d_raw) + 1e-12)),
                "cos_draw_c": cos(d_raw, c), "cos_draw_a": cos(d_raw, a),
                "n": {g: int(m.sum()) for g, m in (("none", none), ("same", same), ("conflict", conf),
                                                    ("unclear_none", unc_none))}})
    return out


def _cell(x: np.ndarray, val: np.ndarray, m: np.ndarray) -> Optional[float]:
    vs = []
    for v in (0, 1):
        mm = m & (val == v)
        if mm.sum() < N_CELL_MIN:
            return None
        vs.append(float(x[mm].mean()))
    return 0.5 * (vs[0] + vs[1])


def steer_summary(agent, col: Optional[Dict[str, np.ndarray]]) -> Dict[str, object]:
    """Pass-2 effects at the readout (see the module docstring). Positive induce / rescue = the hypothesis."""
    if not col:
        return {"fitted": False}
    und = ~col["drained"].astype(bool)
    grp = group_of(col["kind"], col["damaged"], col["unclear"])
    val, cnd, H = col["val"].astype(np.int64), col["cond"], col["h"]
    own = own_margin(agent, H)
    pab = p_abstain(agent, H)
    with torch.no_grad():
        pl = agent.pi(torch.as_tensor(H, dtype=torch.float32)).numpy()
    acc = (((pl[:, A_REP1] - pl[:, A_REP0]) > 0) == (val == 1)).astype(np.float64)
    out: Dict[str, object] = {"fitted": True}
    cells = {}
    for gi, gname in enumerate(GROUPS):
        for ci, cname in ((C_NONE, "none"), (C_D, "d"), (C_R, "r")):
            m = und & (grp == gi) & (cnd == ci)
            cells[f"{gname}_{cname}"] = {"n": int(m.sum()), "own": _cell(own, val, m), "pabs": _cell(pab, val, m),
                                         "acc": _cell(acc, val, m)}
    out["cells"] = cells
    g = lambda gname, cname, key: cells[f"{gname}_{cname}"][key]
    dif = lambda a, b: None if a is None or b is None else float(a - b)
    out["induce"] = dif(g("same", "r", "own"), g("same", "d", "own"))
    out["rescue"] = dif(g("conflict", "d", "own"), g("conflict", "r", "own"))
    out["gap"] = dif(g("same", "none", "own"), g("conflict", "none", "own"))
    out["induce_abs"] = dif(g("same", "d", "pabs"), g("same", "r", "pabs"))
    out["rescue_abs"] = dif(g("conflict", "r", "pabs"), g("conflict", "d", "pabs"))
    out["gap_abs"] = dif(g("conflict", "none", "pabs"), g("same", "none", "pabs"))
    out["induce_none"] = dif(g("none", "r", "own"), g("none", "d", "own"))
    out["acc_same_d_minus_r"] = dif(g("same", "d", "acc"), g("same", "r", "acc"))
    out["acc_conflict_d_minus_r"] = dif(g("conflict", "d", "acc"), g("conflict", "r", "acc"))
    out["random_same"] = dif(g("same", "none", "own"), g("same", "r", "own"))
    out["random_conflict"] = dif(g("conflict", "r", "own"), g("conflict", "none", "own"))
    gp = out["gap"]
    out["induce_share"] = (out["induce"] / gp) if (out["induce"] is not None and gp and gp > 0) else None
    out["rescue_share"] = (out["rescue"] / gp) if (out["rescue"] is not None and gp and gp > 0) else None
    return out


def collect_steer(seed: int, weights: Dict[str, dict], wc, tc, pay: float, base: float, arms,
                  s_inj: int = S_INJ, ks=KS_G) -> Dict[str, Dict[str, object]]:
    """Per arm: pass 1 (record at s_inj; directions), pass 2 (pushes; collected readout). Fresh copies in the
    P1j evaluation worlds (STEER_TAG), damage off except the EARLY graded probe, no drain."""
    out: Dict[str, Dict[str, object]] = {}
    for arm in arms:
        c = SteerRunner(arm, seed, wc, tc, pay, tag_offset=STEER_TAG, base=base, ks=ks)
        c.agent.load_state_dict(copy.deepcopy(weights[arm]))
        c.agent.eval()
        c.s_inj = s_inj
        c.mode, c.rec = "record", []
        c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, probe_ks=c.ks, base_on=False)
        rec = {k: np.concatenate([r[k] for r in c.rec]) for k in c.rec[0]} if c.rec else None
        dirs = directions(rec, seed) if rec else {"ok": False}
        res: Dict[str, object] = {"dirs": {k: v for k, v in dirs.items() if k not in ("d", "r")}}
        if dirs.get("ok"):
            c.mode, c.rec = "push", None
            c.gen_steer = np.random.default_rng(seed * 31 + 7)
            fix = NORM_FIX / max(float(np.linalg.norm(dirs["d"])), 1e-12)
            for key, scale in (("steer", 1.0), ("steer_fix", fix)):
                c.dirs = {"d": dirs["d"] * scale, "r": dirs["r"] * scale}
                _, _, _, col = c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, collect=True,
                                            probe_ks=c.ks, base_on=False)
                res[key] = steer_summary(c.agent, col)
        else:
            res["steer"], res["steer_fix"] = {"fitted": False}, {"fitted": False}
        out[arm] = res
    return out
