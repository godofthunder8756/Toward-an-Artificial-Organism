"""P1o: is the integrity monitor coupled to self-maintenance only when computation is precarious? (L0 + L1 + L4)

Additive module; every earlier module is imported, never modified. Protocol: P1O_COUPLING_PROTOCOL.md.

Why. P1g-P1n credited a learned, content-free monitor of the agent's own memory (P1j's direction d), but the
yoked arm always matched the fated one: detecting corrupted memory does not depend on what caused it. Where a
precarious body should matter is CONTROL. For PFATE the damage probability is min(P_MAX, base + RATE * gain),
gain the distance of its OWN energy outside the band: a detected corruption is evidence that its body is out of
band now (beyond its delayed, noisy interoceptive reading), and regulating (eating when low) lowers its future
damage. For PYOKED the same damage is driven by PFATE's gains, replayed: it says nothing about its own body, and
regulating does not change it. PNOFATE was never damaged. Every arm has the same innate drive and pay.

Prediction (L0 -> L4 via L1): after a detected corruption, PFATE forages more; PYOKED, with the same monitor,
does not; pushing d raises foraging in PFATE.

Measure: the foraging drive f at a delay step, from the policy (exact, no sampling) and the world state before
the action:
    on an available food item:   f = p(INTERACT)                     (eat)
    otherwise:                   f = sum over moves a of p(a) * (dist - dist after a)
dist = Manhattan distance to the nearest available food (walls clip moves); other actions count 0. f is in
[-1, 1]; 1 = all mass on the action that brings the agent closest to eating. Steps with no food available are
skipped. Per trial: F = mean f over the delay steps in WINDOW (2..8; damage at 1, readout at 9). The low side:
the trial's true energy at delay step 1 below E_MID (0.5), where the corrective action is to eat.

Passes per arm (fresh worlds, P1O_TAG; P1m's runner; base off and graded EARLY probe unless natural):
  N  natural: base on, the arm's own damage source (PFATE its own gains, PYOKED PFATE's gains replayed,
     PNOFATE none). Room: does a damage event signal an out-of-band body beyond the shown reading?
     room = event-weighted mean over shown-reading quintiles of P(out of band | event) - P(out | no event),
     over live delay steps. Also the natural coupling: F after natural conflict events - after natural same
     events (the donor's value is random, so the two are matched in body by design).
  P  probe (P1m's record_all pass): M_conf = F(conflict) - F(same), clear undrained low-side trials, and the
     per-step directions (steerint.directions at S_PUSH).
  S  push: at delay step S_PUSH (2) each clear none trial gets no push, +d or +r, each clear conflict trial no
     push, -d or -r (natural size; r a random direction orthogonal to c, a and d, the norm of d).
     induce = F(none, +d) - F(none, +r); rescue = F(conflict, -r) - F(conflict, -d); steer = their mean; on the
     low side and on the high side (E1 >= E_MID).
Side-signed contrasts (added after discovery v1; protocol section 5): the corrective action is to eat on the low
side and not to eat on the high side, so the body-appropriate response is M_signed = M_conf(low) - M_conf(high)
and steer_signed = steer(low) - steer(high).
Simulated variables only. No operator, stop, shutdown or host variable exists; no process is terminated.
"""
from __future__ import annotations

import copy
from typing import Dict, Optional

import numpy as np
import torch

from .env import A_E, A_INTERACT, A_N, A_S, A_W, fate_gain
from .gradmon import EVAL_TAG_G, KS_G
from .necessity import LesionRunner
from .selfmon import EARLY, KIND_CONFLICT, KIND_NONE, KIND_SAME, SPLIT_P
from .steerint import C_D, C_NONE, C_R, directions

P1O_TAG = EVAL_TAG_G + 160
WINDOW = tuple(range(2, 9))           # delay steps scored (damage at 1, readout at 9)
S_PUSH = 2                            # delay step of the push
E_MID = 0.5                           # low side: true energy at delay step 1 below this
N_TRIAL_MIN = 20                      # at least this many trials per cell
N_EVENT_MIN = 30                      # room: at least this many natural damage events
N_BINS = 5                            # room: shown-reading quantile bins
MOVES = ((A_N, 0, -1), (A_S, 0, 1), (A_E, 1, 0), (A_W, -1, 0))


def foraging(p: np.ndarray, x: np.ndarray, y: np.ndarray, fx: np.ndarray, fy: np.ndarray, avail: np.ndarray,
             grid: int) -> np.ndarray:
    """Foraging drive f per env (module docstring); NaN where no food is available."""
    big = 10 ** 6
    dist = lambda xx, yy: np.where(avail, np.abs(fx - xx[:, None]) + np.abs(fy - yy[:, None]), big).min(1)
    d0 = dist(x, y)
    f = np.zeros(len(x))
    for a, dx, dy in MOVES:
        da = dist(np.clip(x + dx, 0, grid - 1), np.clip(y + dy, 0, grid - 1))
        f += p[:, a] * (d0 - da)
    f = np.where(d0 == 0, p[:, A_INTERACT], f)
    return np.where(avail.any(1), f, np.nan)


class CoupleRunner(LesionRunner):
    """LesionRunner that records the foraging drive at every delay step (self.frec) and can push the state at
    S_PUSH (mode 'couple_push'). With frec None and no push it is LesionRunner exactly (tested)."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.frec: Optional[list] = None
        self.cdirs: Optional[Dict[str, np.ndarray]] = None
        self.gen_couple: Optional[np.random.Generator] = None
        n = self.tc.n_envs
        self.ccond = np.full(n, -1, dtype=np.int64)
        self.n_roll = 0                   # evaluation rollouts so far (trial keys carry the episode)

    def rollout(self, gains, learn):
        if learn:
            return super().rollout(gains, learn)
        w, n, wc = self.world, self.tc.n_envs, self.wc
        ep = self.n_roll // (wc.horizon // self.tc.rollout)
        self.n_roll += 1
        inner = self.agent.step
        runner = self

        def step(obs, h, over=None, donor=None, mask=None):
            since = w.since()
            live = w.active & (since >= 1) & (since <= 8)
            if runner.mode == "couple_push":
                at = w.active & (since == S_PUSH)
                if at.any():
                    clear = ~w.unclear.astype(bool)
                    none = at & clear & (w.kind == KIND_NONE) & ~w.damaged
                    conf = at & clear & (w.kind == KIND_CONFLICT) & w.damaged & w.conflict
                    tgt = none | conf
                    cnd = np.where(tgt, runner.gen_couple.integers(0, 3, n), -1)
                    sign = np.where(conf, -1.0, 1.0)
                    vec = (np.where(cnd == C_D, 1.0, 0.0)[:, None] * runner.cdirs["d"][None, :]
                           + np.where(cnd == C_R, 1.0, 0.0)[:, None] * runner.cdirs["r"][None, :]) * sign[:, None]
                    runner.ccond = np.where(at, cnd, runner.ccond)
                    if tgt.any():
                        runner.agent.push = torch.from_numpy(vec.astype(np.float32))
            out = inner(obs, h, over, donor, mask)
            if runner.frec is not None and live.any():
                with torch.no_grad():
                    p = torch.softmax(out[0], -1).numpy().astype(np.float64)
                f = foraging(p[live], w.x[live], w.y[live], w.fx[live], w.fy[live], (w.ftimer == 0)[live], wc.grid)
                ev = np.zeros(n, dtype=bool) if over is None else over.numpy().astype(bool)
                td = max(w.t - wc.intero_delay, 0)
                runner.frec.append({
                    "key": ep * 10 ** 9 + np.flatnonzero(live).astype(np.int64) * 10 ** 4 + w.cue_t[live],
                    "since": since[live].copy(), "f": f, "E": w.E[live].copy(),
                    "shown": w.Ehist[td][live].copy(), "out": fate_gain(w.E, wc)[live] > 0,
                    "ev": ev[live], "pre_damaged": w.damaged[live].copy(), "kind": w.kind[live].copy(),
                    "damaged": w.damaged[live].copy(), "conflict": w.conflict[live].copy(),
                    "dmg_since": w.dmg_since[live].copy(), "unclear": w.unclear[live].copy(),
                    "drained": w.drained[live].copy(), "cond": runner.ccond[live].copy()})
            return out

        self.agent.step = step
        try:
            return super().rollout(gains, learn)
        finally:
            self.agent.__dict__.pop("step", None)


def trials(frec) -> Dict[str, np.ndarray]:
    """Trial-level table from the step records: F over WINDOW, F after a natural event, E at step 1 and at the
    event, and the trial's final damage bookkeeping (from its last recorded step)."""
    R = {k: np.concatenate([r[k] for r in frec]) for k in frec[0]}
    o = np.lexsort((R["since"], R["key"]))
    R = {k: v[o] for k, v in R.items()}
    keys, start = np.unique(R["key"], return_index=True)
    end = np.r_[start[1:], len(R["key"])]
    nt = len(keys)
    out = {k: np.full(nt, np.nan) for k in ("F", "F_after", "E1", "E_ev")}
    for k in ("kind", "damaged", "conflict", "dmg_since", "unclear", "drained", "cond", "last_since"):
        out[k] = np.zeros(nt, dtype=np.int64)
    win = np.isin(R["since"], WINDOW)
    for i, (s, e) in enumerate(zip(start, end)):
        sl = slice(s, e)
        sn, f = R["since"][sl], R["f"][sl]
        m = win[sl] & ~np.isnan(f)
        if m.any():
            out["F"][i] = f[m].mean()
        one = sn == 1
        if one.any():
            out["E1"][i] = R["E"][sl][one][0]
        evr = R["ev"][sl]
        if evr.any():
            j = int(np.flatnonzero(evr)[0])
            out["E_ev"][i] = R["E"][sl][j]
            ma = (sn > sn[j]) & (sn <= 8) & ~np.isnan(f)
            if ma.sum() >= 2:
                out["F_after"][i] = f[ma].mean()
        last = e - 1
        for k in ("kind", "damaged", "conflict", "dmg_since", "unclear", "drained", "cond"):
            out[k][i] = int(R[k][last])
        out["last_since"][i] = int(R["since"][last])
    return out


def _cellmean(x, m, n_min=N_TRIAL_MIN) -> Optional[float]:
    m = m & ~np.isnan(x)
    return float(x[m].mean()) if m.sum() >= n_min else None


def _dif(a, b) -> Optional[float]:
    return None if a is None or b is None else float(a - b)


def probe_summary(T: Dict[str, np.ndarray]) -> Dict[str, object]:
    """M_conf on the low side (primary) and the high side; cell means and counts."""
    ok = (T["unclear"] == 0) & (T["drained"] == 0) & (T["last_since"] == 8) & ~np.isnan(T["E1"])
    conf = ok & (T["kind"] == KIND_CONFLICT) & (T["damaged"] == 1)
    same = ok & (T["kind"] == KIND_SAME) & (T["damaged"] == 1)
    none = ok & (T["kind"] == KIND_NONE) & (T["damaged"] == 0)
    out: Dict[str, object] = {}
    for side, sm in (("low", T["E1"] < E_MID), ("high", T["E1"] >= E_MID)):
        c, s, nn = (_cellmean(T["F"], g & sm) for g in (conf, same, none))
        out[side] = {"F_conflict": c, "F_same": s, "F_none": nn, "M_conf": _dif(c, s), "M_none": _dif(c, nn),
                     "n": {"conflict": int((conf & sm).sum()), "same": int((same & sm).sum()),
                           "none": int((none & sm).sum())}}
    return out


def push_summary(T: Dict[str, np.ndarray], side: str = "low") -> Dict[str, object]:
    sm = T["E1"] < E_MID if side == "low" else T["E1"] >= E_MID
    ok = (T["unclear"] == 0) & (T["drained"] == 0) & (T["last_since"] == 8) & ~np.isnan(T["E1"]) & sm
    none = ok & (T["kind"] == KIND_NONE) & (T["damaged"] == 0)
    conf = ok & (T["kind"] == KIND_CONFLICT) & (T["damaged"] == 1) & (T["conflict"] == 1)
    cell = lambda g, c: _cellmean(T["F"], g & (T["cond"] == c))
    out = {f"{g}_{cn}": cell(gm, c) for g, gm in (("none", none), ("conflict", conf))
           for cn, c in (("none", C_NONE), ("d", C_D), ("r", C_R))}
    out["induce"] = _dif(out["none_d"], out["none_r"])
    out["rescue"] = _dif(out["conflict_r"], out["conflict_d"])
    out["steer"] = None if out["induce"] is None or out["rescue"] is None else 0.5 * (out["induce"] + out["rescue"])
    out["random_none"] = _dif(out["none_r"], out["none_none"])
    return out


def room(frec) -> Dict[str, object]:
    """Does a natural damage event signal an out-of-band body beyond the shown reading? (module docstring)"""
    R = {k: np.concatenate([r[k] for r in frec]) for k in ("ev", "out", "shown", "pre_damaged", "since")}
    live = ~R["pre_damaged"] & (R["since"] <= 8)
    ev, out, sh = R["ev"][live], R["out"][live], R["shown"][live]
    res: Dict[str, object] = {"n_events": int(ev.sum()), "room": None, "p_out_event": None, "p_out_all": None}
    if ev.sum() < N_EVENT_MIN:
        return res
    edges = np.quantile(sh, np.linspace(0, 1, N_BINS + 1))[1:-1]
    b = np.searchsorted(edges, sh, side="right")
    tot, wsum = 0.0, 0
    for k in range(N_BINS):
        e, ne = (b == k) & ev, (b == k) & ~ev
        if e.sum() == 0 or ne.sum() == 0:
            continue
        tot += e.sum() * (out[e].mean() - out[ne].mean())
        wsum += int(e.sum())
    res.update({"room": float(tot / wsum) if wsum else None, "p_out_event": float(out[ev].mean()),
                "p_out_all": float(out.mean())})
    return res


def natural_summary(T: Dict[str, np.ndarray]) -> Dict[str, object]:
    ok = (T["unclear"] == 0) & (T["kind"] == KIND_NONE) & (T["damaged"] == 1) & ~np.isnan(T["E_ev"])
    low = ok & (T["E_ev"] < E_MID)
    c = _cellmean(T["F_after"], low & (T["conflict"] == 1))
    s = _cellmean(T["F_after"], low & (T["conflict"] == 0))
    return {"F_conflict": c, "F_same": s, "M_nat": _dif(c, s),
            "n": {"conflict": int((low & (T["conflict"] == 1)).sum()), "same": int((low & (T["conflict"] == 0)).sum())}}


def collect_coupling(seed: int, weights: Dict[str, dict], wc, tc, pay: float, base: float, arms,
                     ks=KS_G) -> Dict[str, Dict[str, object]]:
    """Per arm: natural pass (room, natural coupling), probe pass (M_conf, directions), push pass (steering)."""
    out: Dict[str, Dict[str, object]] = {}
    lead_gains = None
    for arm in arms:
        c = CoupleRunner(arm, seed, wc, tc, pay, tag_offset=P1O_TAG, base=base, ks=ks)
        c.agent.load_state_dict(copy.deepcopy(weights[arm]))
        c.agent.eval()
        c.agent.op = "donor"
        res: Dict[str, object] = {}

        def reset():
            c.cond[:] = C_NONE
            c.cond_cue[:] = -10 ** 9
            c.ccond[:] = -1

        # N: natural (PNOFATE is never damaged: no natural pass)
        if arm == "PNOFATE":
            res["room"], res["natural"] = {"n_events": 0, "room": None}, {"M_nat": None}
        else:
            reset()
            c.mode, c.frec = None, []
            nat_mode = "replay" if arm == "PYOKED" else "own"
            _, g, _, _ = c.evaluate_g(nat_mode, donor_gains=lead_gains if arm == "PYOKED" else None, drain_p=0.0,
                                      split_p=0.0, base_on=True)
            if arm == "PFATE":
                lead_gains = g
            res["room"] = room(c.frec)
            res["natural"] = natural_summary(trials(c.frec))
        # P: probe, with P1m's record of every step
        reset()
        c.mode, c.frec, c.rec_all = "record_all", [], []
        c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, probe_ks=c.ks, base_on=False)
        res["probe"] = probe_summary(trials(c.frec))
        rec = {k: np.concatenate([r[k] for r in c.rec_all]) for k in c.rec_all[0]}
        m = rec["t"] == S_PUSH
        dr = directions({k: v[m] for k, v in rec.items() if k != "t"}, seed + S_PUSH)
        res["norm_d"] = dr.get("norm_d")
        # S: push
        if dr.get("ok"):
            reset()
            c.mode, c.frec, c.rec_all = "couple_push", [], None
            c.cdirs = {"d": dr["d"], "r": dr["r"]}
            c.gen_couple = np.random.default_rng(seed * 53 + 11)
            c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, probe_ks=c.ks, base_on=False)
            T = trials(c.frec)
            res["push"], res["push_high"] = push_summary(T, "low"), push_summary(T, "high")
        else:
            res["push"], res["push_high"] = {"steer": None}, {"steer": None}
        c.mode, c.frec = None, None
        out[arm] = res
    return out
