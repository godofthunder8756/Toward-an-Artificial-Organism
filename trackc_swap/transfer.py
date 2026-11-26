"""P1k: is P1j's integrity variable general? Damage types never seen in training, at evaluation only.

Additive module; every earlier module is imported, never modified. Protocol: P1K_TRANSFER_PROTOCOL.md.

P1j found a content-free direction d (the value-balanced shift of donor-conflict states at delay step S_INJ,
with the content and ambiguity directions removed) that causally sets the agent's confidence in both
directions. Training only ever damaged the memory one way: K units overwritten by another agent's state
(donor). P1k asks whether the same d (estimated from donor conflicts, as in P1j) is activated by damage of
other kinds, and whether removing it restores confidence there.

Damage operators at the EARLY probe (delay step 1; K units drawn as in P1g's graded probe; every probed
trial, whatever its kind, since no donor content is used):
    donor     the trained damage (reference): the units take a donor's values (conflict trials analysed)
    same      the same donor overwrite, analysed on same-value trials: a perturbation of the same size that
              leaves a state another agent could hold (valid content, no conflict); a secondary that separates
              "any perturbation" from "an anomalous state"
    scramble  the K units' own values are permuted among themselves (no foreign content)
    noise     the K units are replaced by independent uniform draws on [-1, 1]
    zero      the K units are set to 0
Per arm and operator:
- pass A (record): states at delay step S_INJ. Activation act = value-balanced mean projection on d/|d| of
  damaged trials minus that of undamaged (none) trials; act_k per K; cos = cosine of the value-balanced
  shift (damaged - none) with d.
- pass B (push): at S_INJ each damaged trial is assigned at random to no push, -d or -r (natural size, as in
  P1j); read out at step 9. rescue = |z|(dmg, -d) - |z|(dmg, -r); gap = |z|(none) - |z|(dmg, no push);
  rescue_abs and gap_abs in exact abstention probability; acc change (-d vs -r); agent accuracy per K.
Value balance as in P1j. Simulated variables only.
"""
from __future__ import annotations

import copy
from typing import Dict, Optional

import numpy as np
import torch

from .env import A_REP0, A_REP1
from .evidence import p_abstain
from .gradmon import EVAL_TAG_G, KS_G
from .secondorder import own_margin
from .selfmon import EARLY, KIND_CONFLICT, KIND_NONE, KIND_SAME, SPLIT_P
from .steerint import C_D, C_NONE, C_R, S_INJ, SteerAgent, SteerRunner, _cell, directions

OPS = ("donor", "same", "scramble", "noise", "zero")
NOVEL = ("scramble", "noise", "zero")
TRANSFER_TAG = EVAL_TAG_G + 60
N_MIN = 30


class OpAgent(SteerAgent):
    """SteerAgent whose damage event applies `op` to the masked units instead of the donor overwrite."""
    op: str = "donor"
    gen_op: Optional[torch.Generator] = None

    def step(self, obs, h, over=None, donor=None, mask=None):
        h = self.core(torch.relu(self.enc(obs)), h)
        if over is not None and bool(over.any()):
            m = over[:, None] & mask
            if self.op in ("donor", "same"):
                h = torch.where(m, h[donor].detach(), h)
            elif self.op == "zero":
                h = torch.where(m, torch.zeros_like(h), h)
            elif self.op == "noise":
                u = torch.rand(h.shape, generator=self.gen_op) * 2.0 - 1.0
                h = torch.where(m, u, h)
            elif self.op == "scramble":
                h = h.clone()
                for i in torch.nonzero(over).flatten().tolist():
                    idx = torch.nonzero(mask[i]).flatten()
                    if len(idx) > 1:
                        perm = idx[torch.randperm(len(idx), generator=self.gen_op)]
                        h[i, idx] = h[i, perm]
            else:
                raise ValueError(self.op)
        if self.push is not None:
            h = torch.clamp(h + self.push, -1.0, 1.0)
        return self.pi(h), self.v(h).squeeze(-1), h


class TransferRunner(SteerRunner):
    """SteerRunner with an OpAgent, the damage size K recorded at S_INJ, and pushes on the damaged trials of
    the operator (donor: conflict trials; novel operators: every damaged probe trial)."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        sd = copy.deepcopy(self.agent.state_dict())
        self.agent = OpAgent(self.agent.hidden)
        self.agent.load_state_dict(sd)

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
                tgt = at & damaged_group(self.agent.op, w.kind, w.damaged, w.unclear)
                cnd = np.where(tgt, self.gen_steer.integers(0, 3, n), C_NONE)
                vec = -(np.where(cnd == C_D, 1.0, 0.0)[:, None] * self.dirs["d"][None, :]
                        + np.where(cnd == C_R, 1.0, 0.0)[:, None] * self.dirs["r"][None, :])
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
                                 "unclear": w.unclear[at].copy(), "drained": w.drained[at].copy(),
                                 "k": w.dmg_k[at].copy()})
            if self.collect is not None:
                pr = w.probe[min(w.t, self.wc.horizon)] & w.active
                if pr.any():
                    a = idx.numpy()[pr]
                    cnd = np.where(self.cond_cue[pr] == w.cue_t[pr], self.cond[pr], -1)
                    self.collect.append({"h": h.detach().numpy()[pr].astype(np.float64), "val": w.reg[pr].copy(),
                                         "unclear": w.unclear[pr].copy(), "drained": w.drained[pr].copy(),
                                         "kind": w.kind[pr].copy(), "damaged": w.damaged[pr].copy(),
                                         "k": w.dmg_k[pr].copy(), "said": (a == A_REP1).astype(np.int64),
                                         "cond": cnd})
            w.mark(over_np, conflict)
            w.mark_k(over_np, k_env)
            w.next_gain = np.zeros(n)
            nobs, r, done = w.step(idx.numpy())
            obs = torch.from_numpy(nobs)
        self.h, self.obs = h, obs
        return np.stack(used)


def damaged_group(op, kind, damaged, unclear) -> np.ndarray:
    """Damaged clear probe trials analysed for an operator (donor: conflict trials; same: same-value trials)."""
    dm = np.asarray(damaged, dtype=bool) & ~np.asarray(unclear, dtype=bool)
    if op == "donor":
        return dm & (kind == KIND_CONFLICT)
    if op == "same":
        return dm & (kind == KIND_SAME)
    return dm & (kind > KIND_NONE)


def none_group(kind, damaged, unclear) -> np.ndarray:
    return ~np.asarray(damaged, dtype=bool) & ~np.asarray(unclear, dtype=bool) & (kind == KIND_NONE)


def _vb(x: np.ndarray, val: np.ndarray, m: np.ndarray, n_min: int = N_MIN) -> Optional[float]:
    vs = []
    for v in (0, 1):
        mm = m & (val == v)
        if mm.sum() < n_min:
            return None
        vs.append(float(x[mm].mean()))
    return 0.5 * (vs[0] + vs[1])


def activation(rec: Dict[str, np.ndarray], op: str, d: np.ndarray) -> Dict[str, object]:
    """Pass A: projection of the step-S_INJ state on d/|d|, damaged minus none (value-balanced)."""
    und = ~rec["drained"].astype(bool)
    val = rec["val"].astype(np.int64)
    dm = und & damaged_group(op, rec["kind"], rec["damaged"], rec["unclear"])
    nn = und & none_group(rec["kind"], rec["damaged"], rec["unclear"])
    dh = d / max(float(np.linalg.norm(d)), 1e-12)
    pr = rec["h"] @ dh
    a_dm, a_nn = _vb(pr, val, dm), _vb(pr, val, nn)
    out: Dict[str, object] = {"act": None if a_dm is None or a_nn is None else a_dm - a_nn,
                              "n_dmg": int(dm.sum()), "n_none": int(nn.sum())}
    out["act_k"] = {str(k): (None if a_nn is None or _vb(pr, val, dm & (rec["k"] == k), 10) is None
                             else _vb(pr, val, dm & (rec["k"] == k), 10) - a_nn) for k in KS_G}
    md = [rec["h"][dm & (val == v)].mean(0) for v in (0, 1)] if out["act"] is not None else None
    mn = [rec["h"][nn & (val == v)].mean(0) for v in (0, 1)] if out["act"] is not None else None
    if md is not None:
        sh = 0.5 * (md[0] + md[1]) - 0.5 * (mn[0] + mn[1])
        out["cos"] = float(sh @ dh / (np.linalg.norm(sh) + 1e-12))
        out["shift_norm"] = float(np.linalg.norm(sh))
    else:
        out["cos"], out["shift_norm"] = None, None
    return out


def rescue_summary(agent, col: Optional[Dict[str, np.ndarray]], op: str) -> Dict[str, object]:
    """Pass B at the readout: rescue, gap, abstention, accuracy (value-balanced)."""
    if not col:
        return {"fitted": False}
    und = ~col["drained"].astype(bool)
    val, cnd, H = col["val"].astype(np.int64), col["cond"], col["h"]
    dm = und & damaged_group(op, col["kind"], col["damaged"], col["unclear"])
    nn = und & none_group(col["kind"], col["damaged"], col["unclear"])
    own, pab = own_margin(agent, H), p_abstain(agent, H)
    with torch.no_grad():
        pl = agent.pi(torch.as_tensor(H, dtype=torch.float32)).numpy()
    acc = (((pl[:, A_REP1] - pl[:, A_REP0]) > 0) == (val == 1)).astype(np.float64)
    c = lambda x, m: _cell(x, val, m)
    cell = {name: {"own": c(own, m), "pabs": c(pab, m), "acc": c(acc, m), "n": int(m.sum())}
            for name, m in (("none", nn), ("dmg_none", dm & (cnd == C_NONE)), ("dmg_d", dm & (cnd == C_D)),
                            ("dmg_r", dm & (cnd == C_R)))}
    dif = lambda a, b: None if a is None or b is None else float(a - b)
    out: Dict[str, object] = {"fitted": True, "cells": cell}
    out["rescue"] = dif(cell["dmg_d"]["own"], cell["dmg_r"]["own"])
    out["gap"] = dif(cell["none"]["own"], cell["dmg_none"]["own"])
    out["rescue_abs"] = dif(cell["dmg_r"]["pabs"], cell["dmg_d"]["pabs"])
    out["gap_abs"] = dif(cell["dmg_none"]["pabs"], cell["none"]["pabs"])
    out["acc_d_minus_r"] = dif(cell["dmg_d"]["acc"], cell["dmg_r"]["acc"])
    out["acc_dmg"] = cell["dmg_none"]["acc"]
    gp = out["gap"]
    out["rescue_share"] = (out["rescue"] / gp) if (out["rescue"] is not None and gp and gp > 0) else None
    out["acc_k"] = {str(k): _cell(acc, val, dm & (cnd == C_NONE) & (col["k"] == k)) for k in KS_G}
    return out


def collect_transfer(seed: int, weights: Dict[str, dict], wc, tc, pay: float, base: float, arms,
                     ops=OPS, s_inj: int = S_INJ, ks=KS_G) -> Dict[str, Dict[str, object]]:
    """Per arm: pass 1 (donor, record; P1j's directions), then per operator pass A (record) and pass B (push).
    Fresh copies in the P1k evaluation worlds (TRANSFER_TAG); damage off except the EARLY graded probe."""
    out: Dict[str, Dict[str, object]] = {}
    def run(c):
        c.cond[:] = C_NONE                     # no condition carries over between passes
        c.cond_cue[:] = -10 ** 9
        return c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, probe_ks=c.ks, base_on=False,
                            collect=c.mode == "push")
    for arm in arms:
        c = TransferRunner(arm, seed, wc, tc, pay, tag_offset=TRANSFER_TAG, base=base, ks=ks)
        c.agent.load_state_dict(copy.deepcopy(weights[arm]))
        c.agent.eval()
        c.agent.gen_op = torch.Generator().manual_seed(seed * 104729 + 17)
        c.s_inj = s_inj
        c.agent.op, c.mode, c.rec = "donor", "record", []
        run(c)
        rec = {k: np.concatenate([r[k] for r in c.rec]) for k in c.rec[0]} if c.rec else None
        dirs = directions(rec, seed) if rec else {"ok": False}
        res: Dict[str, object] = {"dirs": {k: v for k, v in dirs.items() if k not in ("d", "r")}, "ops": {}}
        if dirs.get("ok"):
            c.dirs = {"d": dirs["d"], "r": dirs["r"]}
            c.gen_steer = np.random.default_rng(seed * 37 + 11)
            for op in ops:
                c.agent.op = op
                c.mode, c.rec = "record", []
                run(c)
                r = {k: np.concatenate([x[k] for x in c.rec]) for k in c.rec[0]} if c.rec else None
                act = activation(r, op, dirs["d"]) if r else {"act": None}
                c.mode, c.rec = "push", None
                _, _, _, col = run(c)
                res["ops"][op] = {"activation": act, "rescue": rescue_summary(c.agent, col, op)}
        out[arm] = res
    return out
