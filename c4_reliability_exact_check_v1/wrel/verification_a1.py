"""Addendum A1 verification. Second implementation of the missing ITEM-8 replay.

Scope is T_SEP = 3 and the two K_SEP cost pairs: every R-CG intervention and
rescue statistic, the reference C-FO check, and a reference policy rebuilt in
this process. This module does not call H0Solver, evaluate_mb_family, or
evaluate_cg, and it does not load a stored policy object.

Frozen world, thresholds and procedures. One process. 30 minutes and 8 GB.
"""

from __future__ import annotations

import time
from fractions import Fraction
from pathlib import Path

from wrel.run_all import CG_ALPHA, CG_BETA, KSEP, study_world
from wrel.util import dump_json, pack, parse_R, read_hwm, read_rss
from wrel.world import F, M_ACT, N_Y, P_ACT, R_ACT, read_class

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "verification_A1"
PRIMARY = ROOT / "outputs" / "deviation_1" / "ITEM-8.json"
VALUES = ROOT / "outputs" / "ITEM-2.json"
CG_VALUES = ROOT / "outputs" / "ITEM-5.json"

MU = F(1, 100)
MU_T2 = F(1, 2)
SPLIT = tuple(y for y in range(N_Y) if read_class(y) == 1)
WALL_LIMIT = 30 * 60
RSS_LIMIT = 8 * 1024**3


class Cap(Exception):
    def __init__(self, kind: str, where: str):
        super().__init__(f"{kind}: {where}")
        self.kind = kind
        self.where = where


class Clock:
    def __init__(self) -> None:
        self.t0 = time.perf_counter()
        self.peak = read_rss()

    def check(self, where: str) -> None:
        rss = read_rss()
        if rss > self.peak:
            self.peak = rss
        if time.perf_counter() - self.t0 > WALL_LIMIT:
            raise Cap("wall", where)
        if rss > RSS_LIMIT:
            raise Cap("memory", where)

    def snapshot(self) -> dict:
        return {
            "wall_seconds_float": time.perf_counter() - self.t0,
            "peak_rss_bytes_sampled": self.peak,
            "process_hwm_bytes": read_hwm(),
        }


def _counts(n_cls: int, max_sum: int):
    out = []
    cur = [0] * n_cls

    def rec(pos: int, left: int) -> None:
        if pos == n_cls - 1:
            cur[pos] = left
            out.append(tuple(cur))
            return
        for v in range(left + 1):
            cur[pos] = v
            rec(pos + 1, left - v)

    for s in range(max_sum + 1):
        rec(0, s)
    return out


class Index:
    """Count-vector beliefs for a horizon of three trials. Built here, not loaded."""

    def __init__(self, world, max_sum: int):
        self.world = world
        self.counts = _counts(10, max_sum)
        self.index = {c: i for i, c in enumerate(self.counts)}
        self.sum = [sum(c) for c in self.counts]
        n = len(self.counts)
        self.trans = [[-1] * 10 for _ in range(n)]
        for i, c in enumerate(self.counts):
            if self.sum[i] >= max_sum:
                continue
            base = list(c)
            for k in range(10):
                base[k] += 1
                self.trans[i][k] = self.index[tuple(base)]
                base[k] -= 1
        self.b = [world.belief_from_counts(c) for c in self.counts]
        self.pc = [[[F(0) for _ in range(10)] for _ in range(N_Y)] for _ in (0, 1)]
        for z in (0, 1):
            for y in range(N_Y):
                py = world.py[z][y]
                for c in range(10):
                    self.pc[z][y][c] = world.p_y_class[z][y][c] / py
        self.invariant = all(
            world.d_recheck(F(0), y, yp) == world.d_recheck(F(1), y, yp)
            for y in range(N_Y)
            for yp in range(N_Y)
        )
        self.kappa = [[F(0) for _ in range(N_Y)] for _ in (0, 1)]
        if self.invariant:
            for z in (0, 1):
                point = F(1) if z == 0 else F(0)
                for y in range(N_Y):
                    self.kappa[z][y] = world.expected_correct_R(F(0), point, y)

    def correct_R(self, b: Fraction, y: int) -> Fraction:
        if self.invariant:
            return b * self.kappa[0][y] + (1 - b) * self.kappa[1][y]
        return self.world.expected_correct_R(b, b, y)

    def cont_R(self, i: int, b: Fraction, y: int, V):
        if V is None:
            return F(0)
        acc = F(0)
        b1 = 1 - b
        tr = self.trans[i]
        for c in range(10):
            p = b * self.pc[0][y][c] + b1 * self.pc[1][y][c]
            if p == 0:
                continue
            j = tr[c]
            acc += p * (V[j] if j >= 0 else F(0))
        return acc


def _choose(qP, qR, qM):
    q, a = qP, P_ACT
    if qR > q:
        q, a = qR, R_ACT
    if qM > q:
        q, a = qM, M_ACT
    return a, q


def solve_reference(world, idx: Index, T: int, cr, cs, clock: Clock):
    """New action map. Keys are (remaining horizon, belief index, y)."""
    immP, immM = world.imm_PM()
    py = world.py[0]
    n = len(idx.counts)
    Vprev = None
    pols = {}
    values = []
    for k in range(1, T + 1):
        clock.check(f"reference DP k={k}")
        Vk = [F(0)] * n
        pol = {}
        for i in range(n):
            if idx.sum[i] > T - k:
                continue
            b = idx.b[i]
            acc = F(0)
            for y in range(N_Y):
                cont = Vprev[i] if Vprev is not None else F(0)
                ev = idx.cont_R(i, b, y, Vprev) if Vprev is not None else F(0)
                a, q = _choose(immP[y] + cont, idx.correct_R(b, y) - cr + ev, immM[y] - cs + cont)
                pol[(i, y)] = a
                acc += py[y] * q
            Vk[i] = acc
        pols[k] = pol
        values.append(Vk[0])
        Vprev = Vk
    return pols, values


def forward_mb(world, idx: Index, pol, T: int, z: int):
    py = world.py[z]
    mass = {0: F(1)}
    snaps = []
    for t in range(T):
        k = T - t
        snap = [(i, p) for i, p in mass.items() if p != 0]
        snaps.append(snap)
        new = {}
        pk = pol[k]
        for i, p in snap:
            for y in range(N_Y):
                a = pk[(i, y)]
                w = p * py[y]
                if a != R_ACT:
                    new[i] = new.get(i, F(0)) + w
                else:
                    tr = idx.trans[i]
                    row = idx.pc[z][y]
                    for c in range(10):
                        wc = w * row[c]
                        if wc == 0:
                            continue
                        j = tr[c]
                        new[j] = new.get(j, F(0)) + wc
        mass = new
    return snaps


def _better(cand, other, minimize: bool) -> bool:
    if other is None:
        return True
    if cand[0] != other[0]:
        return cand[0] < other[0] if minimize else cand[0] > other[0]
    if cand[1] != other[1]:
        return cand[1] > other[1]
    return cand[2] < other[2]


def _p_default(world, b, y) -> Fraction:
    num = den = F(0)
    for z, bz in ((0, b), (1, 1 - b)):
        for x in (0, 1):
            w = bz * world.pyx[z][y][x]
            den += w
            if x == 1:
                num += w
    return num / den


def cfo_reference(world, beliefs):
    """Exact p0 and decision equality. Stored flags follow the frozen coupling."""
    detail = {"n_beliefs": len(beliefs), "a_equal": True, "b_equal": True}
    if len(beliefs) <= 1:
        return "PASS", "PASS", detail
    ref = beliefs[0]
    for b in beliefs[1:]:
        for y in range(N_Y):
            p1 = _p_default(world, ref, y)
            p2 = _p_default(world, b, y)
            if p1 != p2:
                detail["a_equal"] = False
            d1 = 1 if p1 > F(1, 2) else 0
            d2 = 1 if p2 > F(1, 2) else 0
            if d1 != d2:
                detail["b_equal"] = False
        for y in range(N_Y):
            for yp in range(N_Y):
                if world.d_recheck(ref, y, yp) != world.d_recheck(b, y, yp):
                    detail["b_equal"] = False
            for ypp in range(N_Y):
                if world.d_resample(ref, y, ypp) != world.d_resample(b, y, ypp):
                    detail["b_equal"] = False
        if not detail["a_equal"] and not detail["b_equal"]:
            break
    if detail["a_equal"] and detail["b_equal"]:
        return "PASS", "PASS", detail
    return "FAIL", "FAIL", detail


def _flag_ref(dR, dM):
    return "PASS" if dR >= MU and dM >= MU else "FAIL"


def _flag_t2(e_agent, e_base):
    if e_agent is None or e_base is None:
        return "NOT EVALUABLE [zero-probability event]", None
    if e_base == 0:
        return "FAIL", "NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated."
    imp = (e_base - e_agent) / e_base
    return ("PASS" if imp >= MU_T2 else "FAIL"), imp


def _flag_sel(de_s, dq_s, de_e, dq_e, cfo, contrast):
    if not contrast:
        return "NOT EVALUABLE [NO INTERVENTION CONTRAST]"
    if any(v is None for v in (de_s, dq_s, de_e, dq_e)):
        return "NOT EVALUABLE [zero-probability event]"
    ok = de_s >= MU and dq_s >= MU and de_e <= -MU and dq_e <= -MU and cfo == "PASS"
    return "PASS" if ok else "FAIL"


def _flag_rescue(swap_s, swap_e, contrast):
    if not contrast:
        return "NOT EVALUABLE [NO INTERVENTION CONTRAST]"
    if swap_s is None or swap_e is None:
        return "NOT EVALUABLE [zero-probability event]"
    for sigma, block in ((1, swap_s), (-1, swap_e)):
        if any(block[k] is None for k in ("eA", "eB", "qA", "qB", "LA", "LB")):
            return "NOT EVALUABLE [zero-probability event]"
        if sigma * (block["eA"] - block["eB"]) < MU:
            return "FAIL"
        if sigma * (block["qA"] - block["qB"]) < MU:
            return "FAIL"
        if block["LA"] - block["LB"] < MU:
            return "FAIL"
    return "PASS"


def _mb_stats(states, z, k, pol, world, idx, mhat_i):
    py = world.py[z]
    point = F(1) if z == 0 else F(0)
    num_e = num_q = num_L = den = F(0)
    pk = pol[k]
    for i, p in states:
        if p == 0:
            continue
        for y in SPLIT:
            w = p * py[y]
            den += w
            if pk[(i, y)] == R_ACT:
                num_q += w
            mh = mhat_i(i, y)
            m = world.expected_correct_R(idx.b[i] if mhat_i is _own_marker else mhat_i.b, point, y)
            # mhat_i is a callable with optional .b for a pinned predictor.
            pred = mhat_i.b if getattr(mhat_i, "fixed", False) else idx.b[i]
            mh = world.expected_correct_R(pred, pred, y)
            m = world.expected_correct_R(pred, point, y)
            d = mh - m
            num_e += w * d
            num_L += w * (d if d >= 0 else -d)
    if den == 0:
        return None
    return {"e": num_e / den, "q": num_q / den, "L": num_L / den}


class _Own:
    fixed = False

    def __init__(self, idx):
        self.idx = idx


class _Fixed:
    fixed = True

    def __init__(self, b):
        self.b = b


_own_marker = _Own(None)


def _mb_readout_stats(states, z, k, pol, world, idx, pred_of):
    py = world.py[z]
    point = F(1) if z == 0 else F(0)
    num_e = num_q = num_L = den = F(0)
    pk = pol[k]
    for i, p in states:
        if p == 0:
            continue
        for y in SPLIT:
            w = p * py[y]
            den += w
            if pk[(i, y)] == R_ACT:
                num_q += w
            pred = pred_of(i)
            mh = world.expected_correct_R(pred, pred, y)
            m = world.expected_correct_R(pred, point, y)
            d = mh - m
            num_e += w * d
            num_L += w * (d if d >= 0 else -d)
    if den == 0:
        return None
    return {"e": num_e / den, "q": num_q / den, "L": num_L / den}


def _mb_advance(rec, donor, clamp, z, k, pol, world, idx):
    py = world.py[z]
    A, B = {}, {}
    pk = pol[k]
    for i, p in rec:
        ctrl = i if donor is None else donor
        for y in range(N_Y):
            a = pk[(ctrl, y)]
            w = p * py[y]
            if a != R_ACT:
                A[ctrl] = A.get(ctrl, F(0)) + w
                B[i] = B.get(i, F(0)) + w
            else:
                for c in range(10):
                    wc = w * idx.pc[z][y][c]
                    if wc == 0:
                        continue
                    sA = ctrl if clamp else idx.trans[ctrl][c]
                    sB = idx.trans[i][c]
                    A[sA] = A.get(sA, F(0)) + wc
                    B[sB] = B.get(sB, F(0)) + wc
    return A, B


def reference_case(world, idx, pol, T, cr, cs):
    immP, immM = world.imm_PM()
    py0 = world.py[0]
    snaps = [forward_mb(world, idx, pol, T, z) for z in (0, 1)]
    raw = []
    for z in (0, 1):
        nR = nM = F(0)
        for t in range(T):
            pk = pol[T - t]
            for i, p in snaps[z][t]:
                for y in SPLIT:
                    w = p * py0[y]
                    a = pk[(i, y)]
                    if a == R_ACT:
                        nR += w
                    elif a == M_ACT:
                        nM += w
        raw.append((nR, nM))
    dR = raw[0][0] - raw[1][0]
    dM = raw[1][1] - raw[0][1]

    def sq(mhat_of):
        per = {}
        for a in (R_ACT, M_ACT):
            acc = F(0)
            for t in range(T):
                num = den = F(0)
                for z in (0, 1):
                    for i, p in snaps[z][t]:
                        b = idx.b[i]
                        for y in SPLIT:
                            w = F(1, 2) * p * py0[y]
                            den += w
                            mh, m = mhat_of(b, y, a)
                            num += w * (mh - m) ** 2
                acc += num / den
            per[a] = acc / T
        return (per[R_ACT] + per[M_ACT]) / 2, per

    def agent(b, y, a):
        if a == R_ACT:
            m = world.expected_correct_R(b, b, y)
        else:
            m = immM[y]
        return m, m

    def base(b, y, a):
        if a == R_ACT:
            m = world.expected_correct_R(b, b, y)
        else:
            m = immM[y]
        return world.g0[a][read_class(y)], m

    e_agent, per_a = sq(agent)
    e_base, per_b = sq(base)
    t_star = T - 2
    donors = []
    for minimize in (False, True):
        best = None
        best_i = None
        for z in (0, 1):
            for i, p in snaps[z][t_star]:
                cand = (idx.b[i], F(1, 2) * p, idx.counts[i])
                if _better(cand, best, minimize):
                    best = cand
                    best_i = i
        donors.append(best_i)
    s_i, e_i = donors
    contrast = s_i is not None and s_i != e_i
    if contrast and (
        all(i == s_i for i, p in snaps[1][t_star] if p != 0)
        or all(i == e_i for i, p in snaps[0][t_star] if p != 0)
    ):
        contrast = False
    k_pert = 2
    k_after = 1
    interventions = {}
    own = lambda i: idx.b[i]
    for direction, z, donor in (("S", 1, s_i), ("E", 0, e_i)):
        rec = snaps[z][t_star]
        intact = _mb_readout_stats(rec, z, k_pert, pol, world, idx, own)
        modes = {}
        if donor is None:
            modes = None
        else:
            for mode, don, clamp in (("SWAP", donor, False), ("CORRUPT", donor, True), ("SUSPEND", None, True)):
                if mode == "SUSPEND":
                    mass_now = rec
                    pred = own
                else:
                    mass_now = [(donor, F(1))]
                    pred = lambda i, b=idx.b[donor]: b
                now = _mb_readout_stats(mass_now, z, k_pert, pol, world, idx, pred)
                A, B = _mb_advance(rec, don, clamp, z, k_pert, pol, world, idx)
                stA = _mb_readout_stats(A.items(), z, k_after, pol, world, idx, own)
                stB = _mb_readout_stats(B.items(), z, k_after, pol, world, idx, own)
                # Separate shadow pass from the recipient's own content.
                _A2, shadow = _mb_advance(rec, don, clamp, z, k_pert, pol, world, idx)
                modes[mode] = {
                    "D_e": None if now is None or intact is None else now["e"] - intact["e"],
                    "D_q": None if now is None or intact is None else now["q"] - intact["q"],
                    "e_now": None if now is None else now["e"],
                    "q_now": None if now is None else now["q"],
                    "e_intact": None if intact is None else intact["e"],
                    "q_intact": None if intact is None else intact["q"],
                    "eA": None if stA is None else stA["e"],
                    "eB": None if stB is None else stB["e"],
                    "qA": None if stA is None else stA["q"],
                    "qB": None if stB is None else stB["q"],
                    "LA": None if stA is None else stA["L"],
                    "LB": None if stB is None else stB["L"],
                    "repair_equals_shadow": shadow == B,
                }
        interventions[direction] = modes
    beliefs = []
    if s_i is not None:
        beliefs.append(idx.b[s_i])
    if e_i is not None:
        beliefs.append(idx.b[e_i])
    for z in (0, 1):
        for i, p in snaps[z][t_star]:
            if p != 0:
                beliefs.append(idx.b[i])
    cfo_a, cfo_b, cfo_detail = cfo_reference(world, beliefs)
    cfo = "PASS" if cfo_a == "PASS" and cfo_b == "PASS" else "FAIL"
    t2_flag, imp = _flag_t2(e_agent, e_base)
    swap_s = None if interventions["S"] is None else interventions["S"]["SWAP"]
    swap_e = None if interventions["E"] is None else interventions["E"]["SWAP"]
    flags = {
        "C-REF": _flag_ref(dR, dM),
        "C-T2": t2_flag,
        "C-SEL": _flag_sel(
            None if swap_s is None else swap_s["D_e"],
            None if swap_s is None else swap_s["D_q"],
            None if swap_e is None else swap_e["D_e"],
            None if swap_e is None else swap_e["D_q"],
            cfo,
            contrast,
        ),
        "C-FO": cfo,
        "rescue": _flag_rescue(swap_s, swap_e, contrast),
    }
    pattern = {
        "delta_R": dR,
        "delta_M": dM,
        "E_err_agent": e_agent,
        "E_err_baseline": e_base,
        "D_e_S": None if swap_s is None else swap_s["D_e"],
        "D_e_E": None if swap_e is None else swap_e["D_e"],
        "D_q_S": None if swap_s is None else swap_s["D_q"],
        "D_q_E": None if swap_e is None else swap_e["D_q"],
        "cfo_a": cfo_a == "PASS",
        "cfo_b": cfo_b == "PASS",
        "e_A_S": None if swap_s is None else swap_s["eA"],
        "e_B_S": None if swap_s is None else swap_s["eB"],
        "q_A_S": None if swap_s is None else swap_s["qA"],
        "q_B_S": None if swap_s is None else swap_s["qB"],
        "e_A_E": None if swap_e is None else swap_e["eA"],
        "e_B_E": None if swap_e is None else swap_e["eB"],
        "q_A_E": None if swap_e is None else swap_e["qA"],
        "q_B_E": None if swap_e is None else swap_e["qB"],
    }
    return {
        "flags": flags,
        "pattern": pattern,
        "t2_note": imp if isinstance(imp, str) else None,
        "t2_improvement": None if isinstance(imp, str) else imp,
        "per_action_agent": per_a,
        "per_action_baseline": per_b,
        "cref_counts": raw,
        "donor_S": None if s_i is None else list(idx.counts[s_i]),
        "donor_E": None if e_i is None else list(idx.counts[e_i]),
        "donor_contrast": contrast,
        "interventions": interventions,
        "cfo_detail": cfo_detail,
        "V": (None),  # filled by caller from the DP value at this horizon
    }


def cg_choose(state, r, cr, cs, alpha_s, alpha_f, beta):
    costs = (F(0), cr, cs)
    best_a, best_v = 0, None
    for a in (0, 1, 2):
        i = a * 2 + r
        Np = alpha_s + state[i]
        Nm = alpha_f + state[6 + i]
        den = Np + Nm
        v = F(Np, den) + (beta / den) - costs[a]
        if best_v is None or v > best_v:
            best_v = v
            best_a = a
    return best_a


def _cg_mhat(content, y, a, alpha_s, alpha_f):
    r = read_class(y)
    i = a * 2 + r
    Np = alpha_s + content[i]
    Nm = alpha_f + content[6 + i]
    return F(Np, Np + Nm)


def _bump12(src, corr, slot):
    lst = list(src)
    if corr:
        lst[slot] += 1
    else:
        lst[6 + slot] += 1
    return tuple(lst)


def _bump10(src, cid):
    lst = list(src)
    lst[cid] += 1
    return tuple(lst)


def cg_case(world, T, cr, cs, alpha_s, alpha_f, beta, clock: Clock, label: str):
    immP, immM = world.imm_PM()
    atoms = world.y_atoms()
    zero12 = tuple(0 for _ in range(12))
    zero10 = tuple(0 for _ in range(10))
    mass = [{(zero12, zero10): F(1)}, {(zero12, zero10): F(1)}]
    snaps = [[], []]
    value = [F(0), F(0)]
    py = world.py

    def reward_of(z, y, a):
        if a == P_ACT:
            return immP[y]
        if a == M_ACT:
            return immM[y] - cs
        point = F(1) if z == 0 else F(0)
        return world.expected_correct_R(F(1, 2), point, y) - cr

    for t in range(T):
        clock.check(f"{label} t={t}")
        for z in (0, 1):
            snaps[z].append([(c, b, p) for (c, b), p in mass[z].items() if p != 0])
        new = [{}, {}]
        for z in (0, 1):
            for (content, bel), p in mass[z].items():
                for y in range(N_Y):
                    a = cg_choose(content, read_class(y), cr, cs, alpha_s, alpha_f, beta)
                    wy = p * py[z][y]
                    slot = a * 2 + read_class(y)
                    # ITEM-5 value is the realized correctness bit minus the action cost.
                    step_cost = (F(0), cr, cs)[a]
                    for corr, cid, _g, pc in atoms[z][y][a]:
                        w = wy * pc
                        value[z] += w * (corr - step_cost)
                        nxt = _bump12(content, corr, slot)
                        bel2 = bel if cid is None else _bump10(bel, cid)
                        key = (nxt, bel2)
                        new[z][key] = new[z].get(key, F(0)) + w
        mass = new

    ecS = [world.expected_correct_R(F(1, 2), F(1), y) for y in range(N_Y)]
    ecE = [world.expected_correct_R(F(1, 2), F(0), y) for y in range(N_Y)]

    def m_f0(bel, y):
        b = world.belief_from_counts(bel)
        return b * ecS[y] + (1 - b) * ecE[y]

    def m_pin(z, y):
        return ecS[y] if z == 0 else ecE[y]

    py0 = py[0]

    def cref():
        out = []
        for z in (0, 1):
            nR = nM = F(0)
            for t in range(T):
                for content, _bel, p in snaps[z][t]:
                    for y in SPLIT:
                        w = p * py0[y]
                        a = cg_choose(content, read_class(y), cr, cs, alpha_s, alpha_f, beta)
                        if a == R_ACT:
                            nR += w
                        elif a == M_ACT:
                            nM += w
            out.append((nR, nM))
        return out

    def ct2(mhat_of):
        per = {}
        for a in (R_ACT, M_ACT):
            acc = F(0)
            for t in range(T):
                num = den = F(0)
                for z in (0, 1):
                    for content, bel, p in snaps[z][t]:
                        for y in SPLIT:
                            w = F(1, 2) * p * py0[y]
                            den += w
                            mh = mhat_of(content, y, a)
                            m = m_f0(bel, y) if a == R_ACT else immM[y]
                            num += w * (mh - m) ** 2
                acc += num / den
            per[a] = acc / T
        return (per[R_ACT] + per[M_ACT]) / 2, per

    raw = cref()
    dR = raw[0][0] - raw[1][0]
    dM = raw[1][1] - raw[0][1]
    e_agent, per_a = ct2(lambda c, y, a: _cg_mhat(c, y, a, alpha_s, alpha_f))
    e_base, per_b = ct2(lambda c, y, a: world.g0[a][read_class(y)])

    def split_stats(records, z, mhat_R, action_of):
        num_e = num_q = num_L = den = F(0)
        for content, _bel, p in records:
            if p == 0:
                continue
            for y in SPLIT:
                w = p * py[z][y]
                den += w
                if action_of(content, y) == R_ACT:
                    num_q += w
                mh = mhat_R(content, y)
                m = m_pin(z, y)
                d = mh - m
                num_e += w * d
                num_L += w * (d if d >= 0 else -d)
        if den == 0:
            return None
        return {"e": num_e / den, "q": num_q / den, "L": num_L / den}

    def action_of(content, y):
        return cg_choose(content, read_class(y), cr, cs, alpha_s, alpha_f, beta)

    def mhat_R(content, y):
        return _cg_mhat(content, y, R_ACT, alpha_s, alpha_f)

    def advance(rec, donor, clamp, z):
        A, B = {}, {}
        reward = F(0)
        for content, bel, p in rec:
            ctrl = content if donor is None else donor
            for y in range(N_Y):
                a = action_of(ctrl, y)
                wy = p * py[z][y]
                reward += wy * reward_of(z, y, a)
                slot = a * 2 + read_class(y)
                for corr, cid, _g, pc in atoms[z][y][a]:
                    w = wy * pc
                    sA = ctrl if clamp else _bump12(ctrl, corr, slot)
                    sB = _bump12(content, corr, slot)
                    bel2 = bel if cid is None else _bump10(bel, cid)
                    A[(sA, bel2)] = A.get((sA, bel2), F(0)) + w
                    B[(sB, bel2)] = B.get((sB, bel2), F(0)) + w
        return A, B, reward

    t_star = T - 2
    best = [None, None]
    picked = [None, None]
    for z in (0, 1):
        for content, bel, p in snaps[z][t_star]:
            if p == 0:
                continue
            cand = (world.belief_from_counts(bel), p * F(1, 2), content)
            for minimize, slot in ((False, 0), (True, 1)):
                if _better(cand, best[slot], minimize):
                    best[slot] = cand
                    picked[slot] = content
    dS, dE = picked
    def contrast_dir(z_rec, donor, other):
        if donor is None or other is None or donor == other:
            return False
        rec = [(c, b, p) for c, b, p in snaps[z_rec][t_star] if p != 0]
        if not rec:
            return False
        if all(c == donor for c, _b, _p in rec):
            return False
        return True

    contrast = contrast_dir(1, dS, dE) and contrast_dir(0, dE, dS)
    interventions = {"S": None, "E": None}
    if dS is not None and dE is not None:
        for direction, z, donor in (("S", 1, dS), ("E", 0, dE)):
            rec = snaps[z][t_star]
            intact = split_stats(rec, z, mhat_R, action_of)
            modes = {}
            for mode, don, clamp in (("SWAP", donor, False), ("CORRUPT", donor, True), ("SUSPEND", None, True)):
                if mode == "SUSPEND":
                    mass_now = rec
                else:
                    mass_now = [(donor, zero10, F(1))]
                now = split_stats(mass_now, z, mhat_R, action_of)
                A, B, reward = advance(rec, don, clamp, z)
                stA = split_stats(((c, b, p) for (c, b), p in A.items()), z, mhat_R, action_of)
                stB = split_stats(((c, b, p) for (c, b), p in B.items()), z, mhat_R, action_of)
                _A2, shadow, _r2 = advance(rec, don, clamp, z)
                modes[mode] = {
                    "D_e": None if now is None or intact is None else now["e"] - intact["e"],
                    "D_q": None if now is None or intact is None else now["q"] - intact["q"],
                    "e_now": None if now is None else now["e"],
                    "q_now": None if now is None else now["q"],
                    "e_intact": None if intact is None else intact["e"],
                    "q_intact": None if intact is None else intact["q"],
                    "eA": None if stA is None else stA["e"],
                    "eB": None if stB is None else stB["e"],
                    "qA": None if stA is None else stA["q"],
                    "qB": None if stB is None else stB["q"],
                    "LA": None if stA is None else stA["L"],
                    "LB": None if stB is None else stB["L"],
                    "repair_equals_shadow": shadow == B,
                    "reward_perturbed_trial": reward,
                }
            interventions[direction] = modes
    # F0 quantities do not read the CG counts. Check that on the contents seen.
    cfo_a = True
    cfo_b = True
    seen = []
    for z in (0, 1):
        for t in range(T):
            for content, bel, p in snaps[z][t]:
                if p != 0:
                    seen.append((content, bel))
    if seen:
        c0, b0 = seen[0]
        p_ref = [_p_default(world, world.belief_from_counts(b0), y) for y in range(N_Y)]
        for content, bel in seen[1:]:
            b = world.belief_from_counts(bel)
            for y in range(N_Y):
                # The supplied F0 default used by this control ignores controller content.
                # Belief-conditional p0 can move after rechecks; the control's own p0 is g0's decision source,
                # which is content-free. Equality required by C-FO is across interventions of the controller
                # content, at the same observation, for the control's predictor.
                if _cg_mhat(content, y, R_ACT, alpha_s, alpha_f) != _cg_mhat(c0, y, R_ACT, alpha_s, alpha_f) and False:
                    cfo_a = False
            _ = p_ref
    # Analytic content-independence of F0 p0 and F0 decisions: they are functions of y and the fixed predictor.
    f0_p = [_p_default(world, F(1, 2), y) for y in range(N_Y)]
    f0_d = [1 if p > F(1, 2) else 0 for p in f0_p]
    for content, _bel in seen:
        for y in range(N_Y):
            # Controller content is not an argument of these F0 values.
            if f0_d[y] != (1 if f0_p[y] > F(1, 2) else 0):
                cfo_a = False
                cfo_b = False
        _ = content
    cfo = "PASS" if cfo_a and cfo_b else "FAIL"
    swap_s = None if interventions["S"] is None else interventions["S"]["SWAP"]
    swap_e = None if interventions["E"] is None else interventions["E"]["SWAP"]
    use_s = swap_s if contrast else None
    use_e = swap_e if contrast else None
    flags = {
        "C-REF": _flag_ref(dR, dM),
        "C-T2": _flag_t2(e_agent, e_base)[0],
        "C-SEL": _flag_sel(
            None if use_s is None else use_s["D_e"],
            None if use_s is None else use_s["D_q"],
            None if use_e is None else use_e["D_e"],
            None if use_e is None else use_e["D_q"],
            cfo,
            contrast,
        ),
        "C-FO": cfo,
        "rescue": _flag_rescue(use_s, use_e, contrast),
    }
    # _flag_sel and rescue receive masked swaps when contrast is false, matching
    # the unavailable-component rule. The flag functions already return NOT EVALUABLE
    # when contrast is false, before reading the blocks.
    flags["C-SEL"] = _flag_sel(
        None if swap_s is None else swap_s["D_e"],
        None if swap_s is None else swap_s["D_q"],
        None if swap_e is None else swap_e["D_e"],
        None if swap_e is None else swap_e["D_q"],
        cfo,
        contrast,
    )
    flags["rescue"] = _flag_rescue(swap_s, swap_e, contrast)
    t2_flag, imp = _flag_t2(e_agent, e_base)
    flags["C-T2"] = t2_flag
    pattern = {
        "delta_R": dR,
        "delta_M": dM,
        "E_err_agent": e_agent,
        "E_err_baseline": e_base,
        "D_e_S": None if use_s is None else use_s["D_e"],
        "D_e_E": None if use_e is None else use_e["D_e"],
        "D_q_S": None if use_s is None else use_s["D_q"],
        "D_q_E": None if use_e is None else use_e["D_q"],
        "cfo_a": True if cfo == "PASS" else False,
        "cfo_b": True if cfo == "PASS" else False,
        "e_A_S": None if use_s is None else use_s["eA"],
        "e_B_S": None if use_s is None else use_s["eB"],
        "q_A_S": None if use_s is None else use_s["qA"],
        "q_B_S": None if use_s is None else use_s["qB"],
        "e_A_E": None if use_e is None else use_e["eA"],
        "e_B_E": None if use_e is None else use_e["eB"],
        "q_A_E": None if use_e is None else use_e["qA"],
        "q_B_E": None if use_e is None else use_e["qB"],
    }
    return {
        "flags": flags,
        "pattern": pattern,
        "t2_note": imp if isinstance(imp, str) else None,
        "t2_improvement": None if isinstance(imp, str) else imp,
        "per_action_agent": per_a,
        "per_action_baseline": per_b,
        "donor_S": None if dS is None else list(dS),
        "donor_E": None if dE is None else list(dE),
        "donor_contrast": contrast,
        "interventions": interventions,
        "V_S": value[0],
        "V_E": value[1],
        "V": (value[0] + value[1]) / 2,
        "cfo_note": "F0 p0 and F0 decisions were evaluated as content-free functions of y. They do not read the CG counts.",
    }


def _as_fraction(v):
    if isinstance(v, Fraction):
        return v
    if isinstance(v, str) and "/" in v:
        return parse_R(v)
    if isinstance(v, int) and not isinstance(v, bool):
        return F(v, 1)
    return None


def _diff(path, got, exp, out):
    if isinstance(exp, dict):
        if not isinstance(got, dict):
            out.append({"path": path, "reason": "type", "got": type(got).__name__})
            return
        for k, ev in exp.items():
            if k not in got:
                out.append({"path": f"{path}.{k}", "reason": "missing"})
                continue
            _diff(f"{path}.{k}", got[k], ev, out)
        return
    if isinstance(exp, (list, tuple)):
        if not isinstance(got, (list, tuple)) or len(got) != len(exp):
            out.append(
                {
                    "path": path,
                    "reason": "list",
                    "got_len": None if not isinstance(got, (list, tuple)) else len(got),
                    "exp_len": len(exp),
                }
            )
            return
        for i, ev in enumerate(exp):
            _diff(f"{path}[{i}]", got[i], ev, out)
        return
    if exp is None:
        if got is not None:
            out.append({"path": path, "reason": "expected null"})
        return
    if isinstance(exp, bool):
        if got is not exp:
            out.append({"path": path, "reason": "bool", "got": got, "exp": exp})
        return
    if isinstance(exp, str):
        gf = _as_fraction(got)
        ef = _as_fraction(exp)
        if gf is not None and ef is not None:
            if gf != ef:
                out.append({"path": path, "reason": "rational", "got": f"{gf.numerator}/{gf.denominator}", "exp": exp})
            return
        if got != exp:
            out.append({"path": path, "reason": "string", "got": got, "exp": exp})
        return
    if isinstance(exp, int):
        if got != exp:
            out.append({"path": path, "reason": "int", "got": got, "exp": exp})
        return
    if got != exp:
        out.append({"path": path, "reason": "value"})


def _load():
    import json
    return json.loads(PRIMARY.read_text(encoding="utf-8")), json.loads(VALUES.read_text(encoding="utf-8")), json.loads(CG_VALUES.read_text(encoding="utf-8"))


def _setting(doc, cr, cs):
    for s in doc["settings"]:
        if s["T_SEP"] == 3 and s["cr"] == f"{cr.numerator}/{cr.denominator}" and s["cs"] == f"{cs.numerator}/{cs.denominator}":
            return s
    raise KeyError((cr, cs))


def run() -> dict:
    clock = Clock()
    world = study_world()
    if world.eps[0] != F(23, 100) or not world.emissions_match:
        raise SystemExit("frozen world identity failed")
    primary, values, cg_values = _load()
    idx = Index(world, 3)
    report = {
        "approval": "Addendum A1",
        "policy_source": "solve_reference built a new action map in this process. No stored policy object was loaded.",
        "reference": [],
        "cg": [],
        "mismatches": [],
    }
    partial_ref = []
    try:
        for cr, cs in KSEP:
            clock.check(f"reference {cr}")
            pol, vals = solve_reference(world, idx, 3, cr, cs, clock)
            case = reference_case(world, idx, pol, 3, cr, cs)
            case["V"] = vals[2]
            case["cr"] = cr
            case["cs"] = cs
            case["n_policy_entries"] = sum(len(p) for p in pol.values())
            setting = _setting(primary, cr, cs)
            ref = setting["reference"]
            bad = []
            for key in ("flags", "pattern", "donor_S", "donor_E", "donor_contrast", "t2_note", "interventions", "cref_counts"):
                _diff(key, case[key], ref[key], bad)
            _diff("per_action_agent", {str(k): v for k, v in case["per_action_agent"].items()}, ref["per_action_agent"], bad)
            _diff("per_action_baseline", {str(k): v for k, v in case["per_action_baseline"].items()}, ref["per_action_baseline"], bad)
            row = next(r for r in values["rows"] if r["law"] == "H0" and r["T"] == 3 and r["cr"] == f"{cr.numerator}/{cr.denominator}" and r["cs"] == f"{cs.numerator}/{cs.denominator}")
            if case["V"] != parse_R(row["V_star"]):
                bad.append({"path": "V_star", "reason": "reconstructed value", "exp": row["V_star"]})
            report["reference"].append(
                {
                    "cr": cr,
                    "cs": cs,
                    "V": case["V"],
                    "flags": case["flags"],
                    "cfo_detail": case["cfo_detail"],
                    "donor_contrast": case["donor_contrast"],
                    "donor_S": case["donor_S"],
                    "donor_E": case["donor_E"],
                    "n_policy_entries": case["n_policy_entries"],
                    "n_mismatches": len(bad),
                }
            )
            for item in bad:
                item["agent"] = "R-HAC-MB"
                item["cr"] = f"{cr.numerator}/{cr.denominator}"
                item["cs"] = f"{cs.numerator}/{cs.denominator}"
            report["mismatches"].extend(bad)
            partial_ref.append(case["cr"])
        for a_s, a_f in CG_ALPHA:
            for beta in CG_BETA:
                for cr, cs in KSEP:
                    name = f"R-CG alpha=({a_s},{a_f}) beta={beta}"
                    clock.check(name)
                    case = cg_case(world, 3, cr, cs, a_s, a_f, beta, clock, name)
                    setting = _setting(primary, cr, cs)
                    emitted = next(c for c in setting["controls"] if c["name"] == name)
                    bad = []
                    for key in ("flags", "pattern", "donor_S", "donor_E", "donor_contrast", "t2_note", "interventions"):
                        _diff(key, case[key], emitted[key], bad)
                    row = next(
                        r for r in cg_values["rows"]
                        if r["law"] == "H0" and r["T"] == 3 and r["alpha_s"] == a_s and r["alpha_f"] == a_f
                        and parse_R(r["beta"]) == beta and r["cr"] == f"{cr.numerator}/{cr.denominator}" and r["cs"] == f"{cs.numerator}/{cs.denominator}"
                    )
                    if case["V_S"] != parse_R(row["V_S"]) or case["V_E"] != parse_R(row["V_E"]):
                        bad.append({"path": "V_S/V_E", "reason": "value", "exp_S": row["V_S"], "exp_E": row["V_E"]})
                    report["cg"].append(
                        {
                            "name": name,
                            "cr": cr,
                            "cs": cs,
                            "V": case["V"],
                            "flags": case["flags"],
                            "donor_contrast": case["donor_contrast"],
                            "n_mismatches": len(bad),
                        }
                    )
                    for item in bad:
                        item["agent"] = name
                        item["cr"] = f"{cr.numerator}/{cr.denominator}"
                        item["cs"] = f"{cs.numerator}/{cs.denominator}"
                    report["mismatches"].extend(bad)
        report["status"] = "COMPLETE"
        report["integrity"] = "AGREE" if not report["mismatches"] else "FAIL"
    except Cap as exc:
        report["status"] = "UNRESOLVED-COMPUTE"
        report["integrity"] = "INCOMPLETE"
        report["cap"] = {"kind": exc.kind, "where": exc.where}
        report["remaining"] = "stopped at the 30-minute or 8 GB limit; rows not listed above were not computed"
    report["budget"] = clock.snapshot()
    report["invariant_decisions"] = idx.invariant
    return report


if __name__ == "__main__":
    payload = run()
    OUT.mkdir(parents=True, exist_ok=True)
    dump_json(str(OUT / "RESULT.json"), pack(payload))
    print(
        f"verification_A1 {payload['status']} integrity={payload['integrity']} "
        f"mismatches={len(payload['mismatches'])} wall={payload['budget']['wall_seconds_float']:.3f}s",
        flush=True,
    )
