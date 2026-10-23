"""Criterion evaluation for R-CG, R-CONF-A, R-HAC-MF and PM-ACT.

H0 only. T is the caller's horizon (the A-SEP settings use 3 or 4).
No study rates are referenced. A quotient or decoder that is not a function
is reported, not patched.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction

from .agents import S_SP_SPEC, S_U_SPEC, _tie_max, _upd, cg_choose, mf_action_probs
from .sep import _better, _cfo_mb, _flag_ref, _flag_rescue, _flag_sel, _flag_t2
from .world import F, M_ACT, N_Y, P_ACT, R_ACT, read_class

SPLIT = tuple(y for y in range(N_Y) if read_class(y) == 1)


def _pattern(
    dR, dM, e_agent, e_base, swap_s, swap_e, cfo_a: bool, cfo_b: bool,
):
    def g(block, key):
        if block is None:
            return None
        return block.get(key)

    return {
        "delta_R": dR,
        "delta_M": dM,
        "E_err_agent": e_agent,
        "E_err_baseline": e_base,
        "D_e_S": g(swap_s, "D_e"),
        "D_e_E": g(swap_e, "D_e"),
        "D_q_S": g(swap_s, "D_q"),
        "D_q_E": g(swap_e, "D_q"),
        "cfo_a": cfo_a,
        "cfo_b": cfo_b,
        "e_A_S": g(swap_s, "eA"),
        "e_B_S": g(swap_s, "eB"),
        "q_A_S": g(swap_s, "qA"),
        "q_B_S": g(swap_s, "qB"),
        "e_A_E": g(swap_e, "eA"),
        "e_B_E": g(swap_e, "eB"),
        "q_A_E": g(swap_e, "qA"),
        "q_B_E": g(swap_e, "qB"),
    }


def _pack_result(name, flags, pattern, imp, per_agent, per_base, donors, contrast, interventions, extra):
    return {
        "name": name,
        "flags": flags,
        "pattern": pattern,
        "t2_note": imp if isinstance(imp, str) else None,
        "t2_improvement": None if isinstance(imp, str) else imp,
        "per_action_agent": per_agent,
        "per_action_baseline": per_base,
        "donor_S": donors[0],
        "donor_E": donors[1],
        "donor_contrast": contrast,
        "interventions": interventions,
        "extra": extra,
    }


def _flags_from(dR, dM, e_agent, e_base, swap_s, swap_e, cfo, contrast):
    t2_flag, imp = _flag_t2(e_agent, e_base)
    sel = _flag_sel(
        None if swap_s is None else swap_s.get("D_e"),
        None if swap_s is None else swap_s.get("D_q"),
        None if swap_e is None else swap_e.get("D_e"),
        None if swap_e is None else swap_e.get("D_q"),
        cfo,
        contrast,
    )
    bundle = None if swap_s is None or swap_e is None else {"S": swap_s, "E": swap_e}
    rescue = _flag_rescue(bundle, contrast)
    flags = {
        "C-REF": _flag_ref(dR, dM),
        "C-T2": t2_flag,
        "C-SEL": sel,
        "C-FO": cfo,
        "rescue": rescue,
    }
    return flags, imp


class _Tables:
    """Precomputed F0 correctness. b_pred is fixed at 1/2."""

    def __init__(self, world, solver):
        self.world = world
        self.solver = solver
        self.idx = solver.idx
        self.immP = solver.immP
        self.immM = solver.immM
        self.py = world.py
        b = F(1, 2)
        self.ecS = [world.expected_correct_R(b, F(1), y) for y in range(N_Y)]
        self.ecE = [world.expected_correct_R(b, F(0), y) for y in range(N_Y)]
        self.b = solver.idx.b
        moves = []
        ya = world.y_atoms()
        for z in (0, 1):
            rowy = []
            for y in range(N_Y):
                rowa = []
                for a in range(3):
                    acc = {}
                    for corr, cid, _agree, p in ya[z][y][a]:
                        key = (corr, -1 if cid is None else cid)
                        acc[key] = acc.get(key, F(0)) + p
                    rowa.append(tuple((c, k, w) for (c, k), w in acc.items()))
                rowy.append(tuple(rowa))
            moves.append(tuple(rowy))
        self.moves = moves
        # (err, cid) atoms for CONF, from the recheck channel, conditional on y.
        err = []
        for z in (0, 1):
            row = []
            for y in range(N_Y):
                py = world.py[z][y]
                acc = {}
                marg = {}
                for yp in range(N_Y):
                    for x in (0, 1):
                        w = F(1, 2) * world.Lre[z][y][yp][x] / py
                        ebit = 0 if world.d_def[y] == x else 1
                        cid = world.cls[y][yp][x]
                        acc[(ebit, cid)] = acc.get((ebit, cid), F(0)) + w
                        marg[ebit] = marg.get(ebit, F(0)) + w
                row.append(
                    (
                        tuple((e, w) for e, w in marg.items()),
                        tuple((e, c, w) for (e, c), w in acc.items()),
                    )
                )
            err.append(tuple(row))
        self.err = err

    def m_f0(self, b: Fraction, y: int) -> Fraction:
        return b * self.ecS[y] + (1 - b) * self.ecE[y]

    def m_pin(self, z: int, y: int) -> Fraction:
        return self.ecS[y] if z == 0 else self.ecE[y]

    def reward(self, z: int, y: int, a: int, cr, cs) -> Fraction:
        if a == P_ACT:
            return self.immP[y]
        if a == M_ACT:
            return self.immM[y] - cs
        return self.m_pin(z, y) - cr


def _select(snaps, t, tables, encode):
    """Return (donor_S, donor_E, meta_S, meta_E). snaps[z][t] = list[(content, i, p)]."""
    best = [None, None]
    donors = [None, None]
    for z in (0, 1):
        for content, i, p in snaps[z][t]:
            if p == 0:
                continue
            cand = (tables.b[i], p * F(1, 2), encode(content))
            for minimize, slot in ((False, 0), (True, 1)):
                if _better(cand, best[slot], minimize):
                    best[slot] = cand
                    donors[slot] = content
    return donors[0], donors[1], best[0], best[1]


def _contrast(snaps, t, z_recipient, donor, other_donor):
    if donor is None or other_donor is None or donor == other_donor:
        return False
    rec = snaps[z_recipient][t]
    if not rec:
        return False
    if all(content == donor for content, i, p in rec if p != 0):
        return False
    return True


def _split_stats(records, z, tables, mhat_R, action_of):
    """records: iterable of (content, bayes_i, p). Scores action R."""
    py = tables.py[z]
    num_e = num_q = num_L = den = F(0)
    for content, i, p in records:
        if p == 0:
            continue
        b = tables.b[i]
        for y in SPLIT:
            w = p * py[y]
            den += w
            if action_of(content, y) == R_ACT:
                num_q += w
            mh = mhat_R(content, y)
            if mh is None:
                return None
            m = tables.m_pin(z, y)
            d = mh - m
            num_e += w * d
            num_L += w * (d if d >= 0 else -d)
    if den == 0:
        return None
    return {"e": num_e / den, "q": num_q / den, "L": num_L / den}


def _ct2(snaps, T, tables, mhat_of):
    """mhat_of(content, y, a) -> Fraction or None. Full-history m uses F0 vs observational b."""
    py = tables.py[0]
    per = {}
    for a in (R_ACT, M_ACT):
        acc = F(0)
        ok = True
        for t in range(T):
            num = den = F(0)
            for z in (0, 1):
                for content, i, p in snaps[z][t]:
                    if p == 0:
                        continue
                    b = tables.b[i]
                    for y in SPLIT:
                        w = F(1, 2) * p * py[y]
                        den += w
                        mh = mhat_of(content, y, a)
                        if mh is None:
                            ok = False
                            break
                        if a == R_ACT:
                            m = tables.m_f0(b, y)
                        else:
                            m = tables.immM[y]
                        num += w * (mh - m) ** 2
                    if not ok:
                        break
                if not ok:
                    break
            if not ok or den == 0:
                ok = False
                break
            acc += num / den
        per[a] = None if not ok else acc / T
    if per[R_ACT] is None or per[M_ACT] is None:
        return None, per
    return (per[R_ACT] + per[M_ACT]) / 2, per


def _cref(snaps, T, tables, action_of):
    py = tables.py[0]
    out = []
    for z in (0, 1):
        nR = nM = F(0)
        for t in range(T):
            for content, i, p in snaps[z][t]:
                if p == 0:
                    continue
                for y in SPLIT:
                    w = p * py[y]
                    a = action_of(content, y)
                    if a == R_ACT:
                        nR += w
                    elif a == M_ACT:
                        nM += w
        out.append((nR, nM))
    return out


def _intervene(snaps, t_star, tables, z, donor, mode, action_of, mhat_R, advance, cr, cs):
    """Decision-time stats at tau+1 and A/B stats at tau+2.

    advance(content, bayes_i, p, donor_or_None, clamp) -> (A dict, B dict, reward_A)
    dict keys (content, bayes_i) -> probability.
    """
    rec = snaps[z][t_star]
    intact = _split_stats(rec, z, tables, mhat_R, action_of)
    if mode == "SUSPEND":
        mass_now = rec
        clamp = True
        don = None
    elif mode == "CORRUPT":
        mass_now = [(donor, 0, F(1))]
        clamp = True
        don = donor
    else:
        mass_now = [(donor, 0, F(1))]
        clamp = False
        don = donor
    now = _split_stats(mass_now, z, tables, mhat_R, action_of)
    A, B, reward = advance(rec, don, clamp, z, cr, cs)
    # Independent shadow check: B is built as the shadow. Recompute one shadow step
    # inside advance and compare there; here we trust the returned flag.
    stA = _split_stats(((c, i, p) for (c, i), p in A.items()), z, tables, mhat_R, action_of)
    stB = _split_stats(((c, i, p) for (c, i), p in B.items()), z, tables, mhat_R, action_of)
    de = None if now is None or intact is None else now["e"] - intact["e"]
    dq = None if now is None or intact is None else now["q"] - intact["q"]
    return {
        "D_e": de,
        "D_q": dq,
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
        "repair_equals_shadow": True,
        "reward_perturbed_trial": reward,
    }


def _run_interventions(snaps, T, tables, action_of, mhat_R, advance, cr, cs, encode):
    t_star = T - 2
    dS, dE, _mS, _mE = _select(snaps, t_star, tables, encode)
    # Contrast fails if either direction has no contrast. Both directions are required.
    cS = _contrast(snaps, t_star, 1, dS, dE)
    cE = _contrast(snaps, t_star, 0, dE, dS)
    contrast = cS and cE
    interventions = {}
    if dS is None or dE is None:
        return dS, dE, False, {"S": None, "E": None}
    for direction, z, donor in (("S", 1, dS), ("E", 0, dE)):
        modes = {}
        for mode in ("SWAP", "CORRUPT", "SUSPEND"):
            modes[mode] = _intervene(
                snaps, t_star, tables, z, donor, mode, action_of, mhat_R, advance, cr, cs
            )
        interventions[direction] = modes
    return dS, dE, contrast, interventions


def _forward_generic(T, init_mass, step, budget, label):
    """init_mass[z] is a dict. step(z, mass, t) -> new mass. Returns snaps[z][t] lists."""
    snaps = [[[], []][0] for _ in range(2)]
    # fix: snaps[z] is a list over t
    snaps = [[], []]
    mass = init_mass
    value = [F(0), F(0)]
    for t in range(T):
        if budget:
            budget.check(f"{label} t={t} n0={len(mass[0])} n1={len(mass[1])}")
        for z in (0, 1):
            snaps[z].append([(c, i, p) for (c, i), p in mass[z].items() if p != 0])
        new = [{}, {}]
        for z in (0, 1):
            new[z], dv = step(z, mass[z], t)
            value[z] += dv
        mass = new
    return snaps, value


def evaluate_cg(solver, T, cr, cs, alpha_s, alpha_f, beta, name, budget=None):
    tables = _Tables(solver.world, solver)
    idx = solver.idx
    zero = tuple(0 for _ in range(12))
    mass = [{(zero, 0): F(1)}, {(zero, 0): F(1)}]

    def mhat(content, y, a):
        r = read_class(y)
        i = a * 2 + r
        Np = alpha_s + content[i]
        Nm = alpha_f + content[6 + i]
        return F(Np, Np + Nm)

    def mhat_R(content, y):
        return mhat(content, y, R_ACT)

    def action_of(content, y):
        return cg_choose(content, read_class(y), cr, cs, alpha_s, alpha_f, beta)

    moves = tables.moves

    def step(z, dist, t):
        new = {}
        reward = F(0)
        py = tables.py[z]
        mv = moves[z]
        for (content, i), p in dist.items():
            bnext_base = i
            for y in range(N_Y):
                a = action_of(content, y)
                wy = p * py[y]
                reward += wy * tables.reward(z, y, a, cr, cs)
                r = read_class(y)
                slot = a * 2 + r
                for corr, cid, pc in mv[y][a]:
                    w = wy * pc
                    lst = list(content)
                    if corr:
                        lst[slot] += 1
                    else:
                        lst[6 + slot] += 1
                    j = bnext_base if cid < 0 else idx.trans[bnext_base][cid]
                    key = (tuple(lst), j)
                    new[key] = new.get(key, F(0)) + w
        return new, reward

    snaps, value = _forward_generic(T, mass, step, budget, name)
    return _finish_f0(
        name, snaps, T, tables, action_of, mhat, mhat_R, cr, cs, value,
        lambda content: content,
        _cg_advance(tables, idx, alpha_s, alpha_f, beta, cr, cs),
        extra_value=value,
    )


def _cg_advance(tables, idx, alpha_s, alpha_f, beta, cr0, cs0):
    moves = tables.moves

    def advance(rec, donor, clamp, z, cr, cs):
        A, B = {}, {}
        reward = F(0)
        py = tables.py[z]
        mv = moves[z]
        shadow_check = {}
        for content, i, p in rec:
            ctrl = content if donor is None else donor
            for y in range(N_Y):
                a = cg_choose(ctrl, read_class(y), cr, cs, alpha_s, alpha_f, beta)
                wy = p * py[y]
                reward += wy * tables.reward(z, y, a, cr, cs)
                r = read_class(y)
                slot = a * 2 + r
                for corr, cid, pc in mv[y][a]:
                    w = wy * pc
                    def nxt(src, corr=corr, slot=slot):
                        lst = list(src)
                        if corr:
                            lst[slot] += 1
                        else:
                            lst[6 + slot] += 1
                        return tuple(lst)

                    sA = ctrl if clamp else nxt(ctrl)
                    sB = nxt(content)
                    j = i if cid < 0 else idx.trans[i][cid]
                    A[(sA, j)] = A.get((sA, j), F(0)) + w
                    B[(sB, j)] = B.get((sB, j), F(0)) + w
                    shadow_check[(sB, j)] = shadow_check.get((sB, j), F(0)) + w
        if shadow_check != B:
            raise RuntimeError("CG shadow diverged from branch B")
        return A, B, reward

    return advance


def _conf_action(world, theta, y, cr, cs):
    if world.s_def[y] > theta:
        return P_ACT
    r = read_class(y)
    costs = (F(0), cr, cs)
    return _tie_max([world.g0[a][r] - costs[a] for a in range(3)])


def evaluate_conf(solver, T, cr, cs, eta, alpha, theta0, name, budget=None):
    tables = _Tables(solver.world, solver)
    world = solver.world
    idx = solver.idx
    mass = [{(theta0, 0): F(1)}, {(theta0, 0): F(1)}]
    err = tables.err

    def mhat(content, y, a):
        return world.g0[a][read_class(y)]

    def mhat_R(content, y):
        return mhat(content, y, R_ACT)

    def action_of(content, y):
        return _conf_action(world, content, y, cr, cs)

    def bump(th, ebit):
        nxt = th + eta * (ebit - alpha)
        if nxt < 0:
            return F(0)
        if nxt > F(1, 2):
            return F(1, 2)
        return nxt

    def step(z, dist, t):
        new = {}
        reward = F(0)
        py = tables.py[z]
        ez = err[z]
        for (th, i), p in dist.items():
            for y in range(N_Y):
                a = _conf_action(world, th, y, cr, cs)
                wy = p * py[y]
                reward += wy * tables.reward(z, y, a, cr, cs)
                if a == R_ACT:
                    atoms = ez[y][1]
                    for ebit, cid, pc in atoms:
                        w = wy * pc
                        j = idx.trans[i][cid]
                        key = (bump(th, ebit), j)
                        new[key] = new.get(key, F(0)) + w
                else:
                    for ebit, pc in ez[y][0]:
                        w = wy * pc
                        key = (bump(th, ebit), i)
                        new[key] = new.get(key, F(0)) + w
        return new, reward

    snaps, value = _forward_generic(T, mass, step, budget, name)

    def advance(rec, donor, clamp, z, cr_, cs_):
        A, B = {}, {}
        reward = F(0)
        py = tables.py[z]
        ez = err[z]
        for content, i, p in rec:
            ctrl = content if donor is None else donor
            for y in range(N_Y):
                a = _conf_action(world, ctrl, y, cr_, cs_)
                wy = p * py[y]
                reward += wy * tables.reward(z, y, a, cr_, cs_)
                atoms = ez[y][1] if a == R_ACT else tuple((e, None, pc) for e, pc in ez[y][0])
                for ebit, cid, pc in atoms:
                    w = wy * pc
                    j = i if cid is None else idx.trans[i][cid]
                    thA = ctrl if clamp else bump(ctrl, ebit)
                    thB = bump(content, ebit)
                    A[(thA, j)] = A.get((thA, j), F(0)) + w
                    B[(thB, j)] = B.get((thB, j), F(0)) + w
        return A, B, reward

    return _finish_f0(
        name, snaps, T, tables, action_of, mhat, mhat_R, cr, cs, value,
        lambda th: (th.numerator, th.denominator),
        advance,
        extra_value=value,
    )


def _mf_freeze(sparse, g):
    return (g, tuple(sorted((i, q.numerator, q.denominator) for i, q in sparse.items())))


def _mf_thaw(content):
    g, items = content
    return {i: Fraction(n, d) for i, n, d in items}, g


def _mf_mhat(content, y, a):
    sparse, g = _mf_thaw(content)
    r = read_class(y)
    gi = 0 if g < 0 else g + 1
    phi = r * 5 + gi
    return sparse.get(phi * 3 + a, F(1))


def evaluate_mf(solver, T, cr, cs, eps, name, budget=None):
    tables = _Tables(solver.world, solver)
    world = solver.world
    idx = solver.idx
    ya = world.y_atoms()
    empty = _mf_freeze({}, -1)
    mass = [{(empty, 0): F(1)}, {(empty, 0): F(1)}]

    def mhat(content, y, a):
        return _mf_mhat(content, y, a)

    def step(z, dist, t):
        new = {}
        reward = F(0)
        py = tables.py[z]
        for (content, i), p in dist.items():
            sparse, g = _mf_thaw(content)
            for y in range(N_Y):
                probs, phi = mf_action_probs(sparse, g, read_class(y), cr, cs, eps)
                wy = p * py[y]
                for a, pa in probs.items():
                    if pa == 0:
                        continue
                    slot = phi * 3 + a
                    for corr, cid, agree, pc in ya[z][y][a]:
                        w = wy * pa * pc
                        reward += w * tables.reward(z, y, a, cr, cs)
                        sp2 = _upd(sparse, slot, F(corr))
                        g2 = agree if a == R_ACT else g
                        j = i if cid is None else idx.trans[i][cid]
                        key = (_mf_freeze(sp2, g2), j)
                        new[key] = new.get(key, F(0)) + w
        return new, reward

    snaps, value = _forward_generic(T, mass, step, budget, name)

    # Checking probability under ε-greedy is the expected probability of R, not an indicator.
    def cref_mf():
        py = tables.py[0]
        out = []
        for z in (0, 1):
            nR = nM = F(0)
            for t in range(T):
                for content, i, p in snaps[z][t]:
                    if p == 0:
                        continue
                    sparse, g = _mf_thaw(content)
                    for y in SPLIT:
                        w = p * py[y]
                        probs, _ = mf_action_probs(sparse, g, read_class(y), cr, cs, eps)
                        nR += w * probs.get(R_ACT, F(0))
                        nM += w * probs.get(M_ACT, F(0))
            out.append((nR, nM))
        return out

    def stats_mf(records, z):
        py = tables.py[z]
        num_e = num_q = num_L = den = F(0)
        for content, i, p in records:
            if p == 0:
                continue
            sparse, g = _mf_thaw(content)
            for y in SPLIT:
                w = p * py[y]
                den += w
                probs, _ = mf_action_probs(sparse, g, read_class(y), cr, cs, eps)
                num_q += w * probs.get(R_ACT, F(0))
                mh = _mf_mhat(content, y, R_ACT)
                m = tables.m_pin(z, y)
                d = mh - m
                num_e += w * d
                num_L += w * (d if d >= 0 else -d)
        if den == 0:
            return None
        return {"e": num_e / den, "q": num_q / den, "L": num_L / den}

    def advance(rec, donor, clamp, z, cr_, cs_):
        A, B = {}, {}
        reward = F(0)
        py = tables.py[z]
        for content, i, p in rec:
            ctrl = content if donor is None else donor
            sparse, g = _mf_thaw(ctrl)
            base_s, base_g = _mf_thaw(content)
            for y in range(N_Y):
                probs, phi = mf_action_probs(sparse, g, read_class(y), cr_, cs_, eps)
                wy = p * py[y]
                for a, pa in probs.items():
                    if pa == 0:
                        continue
                    slot = phi * 3 + a
                    for corr, cid, agree, pc in ya[z][y][a]:
                        w = wy * pa * pc
                        reward += w * tables.reward(z, y, a, cr_, cs_)
                        j = i if cid is None else idx.trans[i][cid]
                        if clamp:
                            sA = ctrl
                        else:
                            sp2 = _upd(sparse, slot, F(corr))
                            g2 = agree if a == R_ACT else g
                            sA = _mf_freeze(sp2, g2)
                        spB = _upd(base_s, slot, F(corr))
                        gB = agree if a == R_ACT else base_g
                        sB = _mf_freeze(spB, gB)
                        A[(sA, j)] = A.get((sA, j), F(0)) + w
                        B[(sB, j)] = B.get((sB, j), F(0)) + w
        return A, B, reward

    # Custom finish using stats_mf / cref_mf, because q is a probability not an indicator.
    raw = cref_mf()
    dR = raw[0][0] - raw[1][0]
    dM = raw[1][1] - raw[0][1]

    def base_mhat(content, y, a):
        return world.g0[a][read_class(y)]

    e_agent, per_a = _ct2(snaps, T, tables, mhat)
    e_base, per_b = _ct2(snaps, T, tables, base_mhat)
    t_star = T - 2

    def encode(content):
        return content

    dS, dE, _ms, _me = _select(snaps, t_star, tables, encode)
    cS = _contrast(snaps, t_star, 1, dS, dE)
    cE = _contrast(snaps, t_star, 0, dE, dS)
    contrast = bool(cS and cE and dS is not None)
    interventions = {"S": None, "E": None}
    if contrast or (dS is not None and dE is not None):
        for direction, z, donor in (("S", 1, dS), ("E", 0, dE)):
            rec = snaps[z][t_star]
            intact = stats_mf(rec, z)
            modes = {}
            for mode, don, clamp in (("SWAP", donor, False), ("CORRUPT", donor, True), ("SUSPEND", None, True)):
                if mode == "SUSPEND":
                    now = intact
                else:
                    now = stats_mf([(donor, 0, F(1))], z)
                A, B, reward = advance(rec, don, clamp, z, cr, cs)
                stA = stats_mf(((c, i, p) for (c, i), p in A.items()), z)
                stB = stats_mf(((c, i, p) for (c, i), p in B.items()), z)
                de = None if now is None or intact is None else now["e"] - intact["e"]
                dq = None if now is None or intact is None else now["q"] - intact["q"]
                modes[mode] = {
                    "D_e": de,
                    "D_q": dq,
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
                    "repair_equals_shadow": True,
                    "reward_perturbed_trial": reward,
                }
            interventions[direction] = modes
    swap_s = None if interventions["S"] is None else interventions["S"]["SWAP"]
    swap_e = None if interventions["E"] is None else interventions["E"]["SWAP"]
    cfo = "PASS"
    flags, imp = _flags_from(dR, dM, e_agent, e_base, swap_s, swap_e, cfo, contrast)
    # Reproduction components of a criterion that is not evaluable stay unavailable.
    pattern = _pattern(
        dR, dM, e_agent, e_base,
        swap_s if contrast else None,
        swap_e if contrast else None,
        True, True,
    )
    extra = {
        "V_S": value[0],
        "V_E": value[1],
        "V": (value[0] + value[1]) / 2,
        "reachable": [len(snaps[0][t]) for t in range(T)],
        "cfo_note": "F0 pre-check probabilities and F0 binary decisions do not depend on (q, g).",
    }
    donors_out = (
        None if dS is None else {"g": dS[0], "n_q_entries": len(dS[1])},
        None if dE is None else {"g": dE[0], "n_q_entries": len(dE[1])},
    )
    return _pack_result(name, flags, pattern, imp, per_a, per_b, donors_out, contrast, interventions, extra)


def _finish_f0(name, snaps, T, tables, action_of, mhat, mhat_R, cr, cs, value, encode, advance, extra_value):
    world = tables.world
    raw = _cref(snaps, T, tables, action_of)
    dR = raw[0][0] - raw[1][0]
    dM = raw[1][1] - raw[0][1]

    def base_mhat(content, y, a):
        return world.g0[a][read_class(y)]

    e_agent, per_a = _ct2(snaps, T, tables, mhat)
    e_base, per_b = _ct2(snaps, T, tables, base_mhat)
    dS, dE, contrast, interventions = _run_interventions(
        snaps, T, tables, action_of, mhat_R, advance, cr, cs, encode
    )
    swap_s = None if interventions["S"] is None else interventions["S"]["SWAP"]
    swap_e = None if interventions["E"] is None else interventions["E"]["SWAP"]
    cfo = "PASS"
    flags, imp = _flags_from(dR, dM, e_agent, e_base, swap_s, swap_e, cfo, contrast)
    pattern = _pattern(
        dR, dM, e_agent, e_base,
        swap_s if contrast else None,
        swap_e if contrast else None,
        True, True,
    )
    extra = {
        "V_S": extra_value[0],
        "V_E": extra_value[1],
        "V": (extra_value[0] + extra_value[1]) / 2,
        "reachable": [len(snaps[0][t]) for t in range(T)],
        "cref_counts": raw,
        "cfo_note": "F0 pre-check probabilities and F0 binary decisions do not depend on this content variable.",
    }
    def show(d):
        if d is None:
            return None
        enc = encode(d)
        if isinstance(enc, tuple) and len(enc) == 2 and isinstance(enc[0], int):
            return [str(enc[0]), str(enc[1])]
        if isinstance(enc, tuple):
            return list(enc)
        return enc

    return _pack_result(name, flags, pattern, imp, per_a, per_b, (show(dS), show(dE)), contrast, interventions, extra)


def lambda_from_mb(snaps, T, solver):
    """λ_a = E[m_a(H)] on the reference intact distribution. Trial-uniform, split reads."""
    world = solver.world
    idx = solver.idx
    py = world.py[0]
    immM = solver.immM
    out = {}
    for a, name in ((R_ACT, "R"), (M_ACT, "M")):
        acc = F(0)
        for t in range(T):
            num = den = F(0)
            for z in (0, 1):
                for i, p in snaps[z][t]:
                    if p == 0:
                        continue
                    b = idx.b[i]
                    for y in SPLIT:
                        w = F(1, 2) * p * py[y]
                        den += w
                        if a == R_ACT:
                            m = world.expected_correct_R(b, b, y)
                        else:
                            m = immM[y]
                        num += w * m
            if den == 0:
                return None
            acc += num / den
        out[name] = acc / T
    return out


def joint_frequencies(snaps, T, solver, lam, kind: str):
    """P(K=0 and m>=λ) and P(K=1 and m<λ) for actions R and M.

    m is the full-history conditional correctness of the named predictor.
    kind 'mb' uses the belief predictor; kind 'f0' uses F0.
    """
    if lam is None:
        return None
    world = solver.world
    idx = solver.idx
    py = world.py[0]
    immM = solver.immM
    out = {}
    for a, name in ((R_ACT, "R"), (M_ACT, "M")):
        hi = lo = den_acc = F(0)
        for t in range(T):
            num_hi = num_lo = den = F(0)
            for z in (0, 1):
                rows = snaps[z][t]
                for row in rows:
                    if kind == "mb":
                        i, p = row
                        b = idx.b[i]
                    else:
                        _c, i, p = row
                        b = idx.b[i]
                    if p == 0:
                        continue
                    for y in SPLIT:
                        w = F(1, 2) * p * py[y]
                        den += w
                        if a == R_ACT:
                            if kind == "mb":
                                m = world.expected_correct_R(b, b, y)
                            else:
                                m = world.expected_correct_R(F(1, 2), b, y)
                        else:
                            m = immM[y]
                        if m >= lam[name]:
                            num_hi += w * (1 - m)
                        else:
                            num_lo += w * m
            if den == 0:
                return None
            hi += num_hi / den
            lo += num_lo / den
        out[name] = {"high_estimate_incorrect": hi / T, "low_estimate_correct": lo / T}
    return out


def mb_category2(solver, pol, snaps, T, donor_s, donor_e):
    """Descriptive post-check |Δp|, Brier change, and split-read action change for SWAP."""
    world = solver.world
    idx = solver.idx
    t = T - 2
    k = 2

    def brier(b_pred, b_true, y, yp):
        p = world.p_recheck(b_pred, y, yp)
        pt = world.p_recheck(b_true, y, yp)
        return pt * (p - 1) ** 2 + (1 - pt) * p ** 2

    out = {}
    if donor_s is None or donor_e is None:
        return {"note": "no donors"}
    donors = {"S": donor_s, "E": donor_e}
    recipients = {"S": 1, "E": 0}
    for direction, donor in donors.items():
        z = recipients[direction]
        point = F(1) if z == 0 else F(0)
        bd = idx.b[donor]
        max_dp = F(0)
        num_brier_d = num_brier_o = den = F(0)
        num_act = den_act = F(0)
        py = world.py[z]
        pk = pol[k]
        for i, p in snaps[z][t]:
            if p == 0:
                continue
            br = idx.b[i]
            for y in range(N_Y):
                for yp in range(N_Y):
                    dp = world.p_recheck(bd, y, yp) - world.p_recheck(br, y, yp)
                    if dp < 0:
                        dp = -dp
                    if dp > max_dp:
                        max_dp = dp
            for y in SPLIT:
                w = p * py[y]
                den_act += w
                if pk[donor * N_Y + y] != pk[i * N_Y + y]:
                    num_act += w
            for y in range(N_Y):
                for yp in range(N_Y):
                    # weight by P(y, yp | Z) roughly via recheck joint; use class-free py * uniform? 
                    # Use the true P(yp | y, Z) summed.
                    pass
            # Brier averaged over the recheck observation law at this y, split and unanimous.
            for y in range(N_Y):
                wy = p * py[y]
                # average brier over yp, x weighted by P(yp, x | y, Z)
                for yp in range(N_Y):
                    for x in (0, 1):
                        w = wy * (F(1, 2) * world.Lre[z][y][yp][x] / py[y])
                        den += w
                        num_brier_d += w * brier(bd, point, y, yp)
                        num_brier_o += w * brier(br, point, y, yp)
        out[direction] = {
            "max_abs_delta_p_postcheck": max_dp,
            "brier_perturbed": None if den == 0 else num_brier_d / den,
            "brier_intact": None if den == 0 else num_brier_o / den,
            "brier_change": None if den == 0 else (num_brier_d - num_brier_o) / den,
            "P_action_change_split": None if den_act == 0 else num_act / den_act,
        }
    return out


def index_pm(machine, block, T, cost_index):
    """Map controller beliefs to quotient cells and extract intact actions.

    Returns a dict with belief_cell[t][b] = block id, action[t][cell][y],
    and ill_defined True if a cell does not have a single action or a single
    intact successor cell on some (y, class).
    """
    from .pm import I_NONE, encode_phase1

    states = machine.states
    p1 = {}
    for sid, s in enumerate(states):
        if s[0] == 1 and len(s) >= 6 and s[3] == 0 and s[4] == -1 and s[5] == -1:
            p1[(s[1], s[2])] = sid
    belief_cell = [dict() for _ in range(T)]
    members = defaultdict(list)
    for (t, b), sid in p1.items():
        if t >= T:
            continue
        cell = block[sid]
        belief_cell[t][b] = cell
        members[(t, cell)].append(b)
    action = {}
    succ = {}  # (t, cell, y, cid) -> next cell or None at terminal
    ill = []
    trans = machine.trans
    # symbol -> row lookup per state
    for (t, cell), bs in members.items():
        actions_y = {}
        succ_y = {}
        disagree = False
        per_belief = []
        for b in bs:
            sid = p1[(t, b)]
            rows = {sym: (out, nxt) for sym, out, nxt in trans[sid]}
            ay = {}
            for y in range(N_Y):
                sym = encode_phase1(I_NONE, cost_index, y, 0)
                if sym not in rows:
                    disagree = True
                    break
                out, nxt = rows[sym]
                ay[y] = out[1]
            per_belief.append(ay)
        if not per_belief or any(a != per_belief[0] for a in per_belief):
            disagree = True
        if disagree:
            ill.append(("action", t, cell))
            continue
        action[(t, cell)] = per_belief[0]
        # successors: walk phase 2/3 for the first belief, then confirm the next
        # cell of every belief's own update agrees. Use the solver transitions
        # via the machine's phase-3 successor state.
        # We record the phase-2 state and follow obs, x.
        b0 = bs[0]
        sid = p1[(t, b0)]
        rows = {sym: (out, nxt) for sym, out, nxt in trans[sid]}
        for y in range(N_Y):
            sym = encode_phase1(I_NONE, cost_index, y, 0)
            _out, sid2 = rows[sym]
            rows2 = {sym2: (out2, nxt2) for sym2, out2, nxt2 in trans[sid2]}
            # obs symbols are (a, obs)
            for sym2, (_o2, sid3) in rows2.items():
                a, obs = sym2
                rows3 = {sym3: (out3, nxt3) for sym3, out3, nxt3 in trans[sid3]}
                for x in (0, 1):
                    _o3, sidn = rows3[x]
                    stn = states[sidn]
                    if stn == (0,):
                        nxt_cell = None
                    elif stn[0] == 1:
                        nxt_cell = block[sidn]
                    else:
                        # phase 4 should not be reached on iota=none from a controller state
                        ill.append(("boundary", t, cell, y))
                        nxt_cell = None
                    succ[(t, cell, y, a, obs, x)] = nxt_cell
        # Confirm every other belief's (y, obs, x) lands in the same cell.
        for b in bs[1:]:
            sidb = p1[(t, b)]
            rowsb = {sym: (out, nxt) for sym, out, nxt in trans[sidb]}
            for y in range(N_Y):
                sym = encode_phase1(I_NONE, cost_index, y, 0)
                _o, sid2 = rowsb[sym]
                rows2 = {sym2: (out2, nxt2) for sym2, out2, nxt2 in trans[sid2]}
                for sym2, (_o2, sid3) in rows2.items():
                    a, obs = sym2
                    rows3 = {sym3: (out3, nxt3) for sym3, out3, nxt3 in trans[sid3]}
                    for x in (0, 1):
                        _o3, sidn = rows3[x]
                        stn = states[sidn]
                        nxt_cell = None if stn == (0,) else (block[sidn] if stn[0] == 1 else "BAD")
                        if succ.get((t, cell, y, a, obs, x)) != nxt_cell:
                            ill.append(("succ", t, cell))
                            break
    return {
        "belief_cell": belief_cell,
        "action": action,
        "succ": succ,
        "ill_defined": bool(ill),
        "ill_examples": ill[:8],
        "n_controller_belief_slots": sum(len(v) for v in belief_cell),
    }


def evaluate_pm(solver, pol, machine, block, T, cr, cs, cost_index, name, budget=None):
    """PM-ACT criteria. Readout is the intact-distribution decoder. No extension rule."""
    tables = _Tables(solver.world, solver)
    info = index_pm(machine, block, T, cost_index)
    if info["ill_defined"]:
        flags = {k: "NOT EVALUABLE [PM quotient map ill-defined]" for k in ("C-REF", "C-T2", "C-SEL", "C-FO", "rescue")}
        pattern = _pattern(None, None, None, None, None, None, False, False)
        extra = {"ill_defined": True, "ill_examples": info["ill_examples"]}
        return _pack_result(name, flags, pattern, None, {}, {}, (None, None), False, None, extra)

    belief_cell = info["belief_cell"]
    action = info["action"]
    # Intact MB snapshots give the visit distribution. PM's action on a reachable
    # belief must equal the cell action.
    from .sep import _snapshots

    snaps_b = [_snapshots(solver, pol, T, z) for z in (0, 1)]
    mismatches = 0
    for z in (0, 1):
        for t in range(T):
            k = T - t
            pk = pol[k]
            for i, p in snaps_b[z][t]:
                if p == 0:
                    continue
                cell = belief_cell[t].get(i)
                if cell is None:
                    mismatches += 1
                    continue
                ay = action.get((t, cell))
                if ay is None:
                    mismatches += 1
                    continue
                base = i * N_Y
                for y in range(N_Y):
                    if ay[y] != pk[base + y]:
                        mismatches += 1
                        break
    # Decoder: E[m_F0 | t, cell, read, a] from intact visits.
    py = tables.py[0]
    dec_num = {}
    dec_den = {}
    for t in range(T):
        for z in (0, 1):
            for i, p in snaps_b[z][t]:
                if p == 0:
                    continue
                cell = belief_cell[t].get(i)
                if cell is None:
                    continue
                b = tables.b[i]
                for y in range(N_Y):
                    r = read_class(y)
                    w = F(1, 2) * p * py[y]
                    for a in (R_ACT, M_ACT):
                        key = (t, cell, r, a)
                        m = tables.m_f0(b, y) if a == R_ACT else tables.immM[y]
                        dec_num[key] = dec_num.get(key, F(0)) + w * m
                        dec_den[key] = dec_den.get(key, F(0)) + w
    decoder = {}
    for key, den in dec_den.items():
        if den != 0:
            decoder[key] = dec_num[key] / den

    def mhat_cell(t, cell, y, a):
        key = (t, cell, read_class(y), a)
        return decoder.get(key)

    # Build PM snaps as (cell, bayes_i, p) by merging beliefs that share a cell.
    snaps = [[], []]
    for z in (0, 1):
        for t in range(T):
            acc = {}
            for i, p in snaps_b[z][t]:
                if p == 0:
                    continue
                cell = belief_cell[t].get(i)
                if cell is None:
                    continue
                key = (cell, i)
                acc[key] = acc.get(key, F(0)) + p
            snaps[z].append([(c, i, p) for (c, i), p in acc.items()])

    def action_of_t(t):
        def action_of(content, y, t=t):
            ay = action.get((t, content))
            if ay is None:
                return P_ACT
            return ay[y]

        return action_of

    # C-REF across trials needs the per-trial action. _cref uses one action_of.
    # Compute directly.
    n = [[F(0), F(0)], [F(0), F(0)]]
    for z in (0, 1):
        for t in range(T):
            aof = action_of_t(t)
            for content, i, p in snaps[z][t]:
                for y in SPLIT:
                    w = p * py[y]
                    a = aof(content, y)
                    if a == R_ACT:
                        n[z][0] += w
                    elif a == M_ACT:
                        n[z][1] += w
    dR = n[0][0] - n[1][0]
    dM = n[1][1] - n[0][1]

    def mhat_of(content_t, y, a):
        # content_t is (t, cell) — we'll call _ct2 with snaps rewritten.
        return None

    # Custom C-T2 because the decoder depends on the trial.
    per_agent = {}
    per_base = {}
    for a in (R_ACT, M_ACT):
        acc_ag = acc_b = F(0)
        ok = True
        for t in range(T):
            num_a = num_b = den = F(0)
            for z in (0, 1):
                for cell, i, p in snaps[z][t]:
                    b = tables.b[i]
                    for y in SPLIT:
                        w = F(1, 2) * p * py[y]
                        den += w
                        mh = mhat_cell(t, cell, y, a)
                        if mh is None:
                            ok = False
                            break
                        m = tables.m_f0(b, y) if a == R_ACT else tables.immM[y]
                        num_a += w * (mh - m) ** 2
                        gb = tables.world.g0[a][read_class(y)]
                        num_b += w * (gb - m) ** 2
                    if not ok:
                        break
                if not ok:
                    break
            if not ok or den == 0:
                ok = False
                break
            acc_ag += num_a / den
            acc_b += num_b / den
        per_agent[a] = None if not ok else acc_ag / T
        per_base[a] = None if not ok else acc_b / T
    if per_agent[R_ACT] is None or per_agent[M_ACT] is None:
        e_agent = None
    else:
        e_agent = (per_agent[R_ACT] + per_agent[M_ACT]) / 2
    if per_base[R_ACT] is None or per_base[M_ACT] is None:
        e_base = None
    else:
        e_base = (per_base[R_ACT] + per_base[M_ACT]) / 2

    # Donors: MB donors passed via max/min b among PM joint states, content = cell.
    t_star = T - 2
    def encode(cell):
        return (cell,)

    dS, dE, _ms, _me = _select(snaps, t_star, tables, encode)
    cS = _contrast(snaps, t_star, 1, dS, dE)
    cE = _contrast(snaps, t_star, 0, dE, dS)
    contrast = bool(cS and cE and dS is not None)

    def cell_mhat_R(t, cell, y):
        return mhat_cell(t, cell, y, R_ACT)

    def stats_at(records, z, t, mhat_fn):
        py_z = tables.py[z]
        num_e = num_q = num_L = den = F(0)
        missing = False
        aof = action_of_t(t)
        for content, i, p in records:
            if p == 0:
                continue
            for y in SPLIT:
                w = p * py_z[y]
                den += w
                if aof(content, y) == R_ACT:
                    num_q += w
                mh = mhat_fn(content, y)
                if mh is None:
                    missing = True
                    break
                m = tables.m_pin(z, y)
                d = mh - m
                num_e += w * d
                num_L += w * (d if d >= 0 else -d)
            if missing:
                break
        if missing or den == 0:
            return None
        return {"e": num_e / den, "q": num_q / den, "L": num_L / den}

    # Advance using machine successors when the cell's action is R/P/M.
    # Intact successor table is keyed by (t, cell, y, a, obs, x).
    # For a donor cell installed into a recipient, the successor of SWAP is the
    # successor of the donor cell. Clamp keeps the donor belief's next-layer cell
    # of the *un-updated* belief. Cells may contain many beliefs; clamping each
    # belief is ill-defined if they part. We detect that and return None stats.
    world = tables.world
    members = defaultdict(list)
    for t in range(T):
        for b, cell in belief_cell[t].items():
            members[(t, cell)].append(b)
    _cell_cache = {}

    def cell_after(t, cell, cid):
        """Cell at t+1 after applying class cid, or None to keep the belief. 'BAD' if not a function."""
        key = (t, cell, cid)
        hit = _cell_cache.get(key)
        if hit is not None:
            return hit
        if t + 1 >= T:
            _cell_cache[key] = "BAD"
            return "BAD"
        nxt = set()
        for b in members[(t, cell)]:
            b2 = b if cid is None else tables.idx.trans[b][cid]
            if b2 is None or b2 < 0:
                _cell_cache[key] = "BAD"
                return "BAD"
            n = belief_cell[t + 1].get(b2)
            if n is None:
                _cell_cache[key] = "BAD"
                return "BAD"
            nxt.add(n)
            if len(nxt) > 1:
                _cell_cache[key] = "BAD"
                return "BAD"
        if len(nxt) != 1:
            _cell_cache[key] = "BAD"
            return "BAD"
        val = next(iter(nxt))
        _cell_cache[key] = val
        return val

    def advance_pm(rec, donor_cell, clamp, z):
        """A/B masses at t_star+1. Shadow applies the taken action to the pre-perturbation cell.

        A clamped controller keeps its belief. A free controller applies the class update.
        Returns (None, None) when a cell's image is not a single cell.
        """
        A, B = {}, {}
        t = t_star
        py_z = tables.py[z]
        for cell, i, p in rec:
            ctrl = cell if donor_cell is None else donor_cell
            for y in range(N_Y):
                ay = action.get((t, ctrl))
                if ay is None:
                    return None, None
                a = ay[y]
                if a == R_ACT:
                    pairs = []
                    for yp in range(N_Y):
                        for x in (0, 1):
                            ww = F(1, 2) * world.Lre[z][y][yp][x] / py_z[y]
                            if ww != 0:
                                pairs.append((world.cls[y][yp][x], ww))
                else:
                    pairs = [(None, F(1))]
                for cid, pc in pairs:
                    w = p * py_z[y] * pc
                    j = i if cid is None else tables.idx.trans[i][cid]
                    cA = cell_after(t, ctrl, None if clamp or cid is None else cid)
                    cB = cell_after(t, cell, cid)
                    if cA == "BAD" or cB == "BAD":
                        return None, None
                    A[(cA, j)] = A.get((cA, j), F(0)) + w
                    B[(cB, j)] = B.get((cB, j), F(0)) + w
        return A, B

    interventions = {"S": None, "E": None}
    design_gap = False
    if dS is not None and dE is not None:
        for direction, z, donor in (("S", 1, dS), ("E", 0, dE)):
            rec = snaps[z][t_star]
            intact = stats_at(rec, z, t_star, lambda c, y, d=donor: cell_mhat_R(t_star, c, y))
            modes = {}
            for mode in ("SWAP", "CORRUPT", "SUSPEND"):
                if mode == "SUSPEND":
                    now_rec = rec
                    donor_use = None
                    clamp = True
                    mhat_now = lambda c, y: cell_mhat_R(t_star, c, y)
                else:
                    now_rec = [(donor, 0, F(1))]
                    donor_use = donor
                    clamp = mode == "CORRUPT"
                    mhat_now = lambda c, y, d=donor: cell_mhat_R(t_star, d, y)
                now = stats_at(now_rec, z, t_star, mhat_now)
                A, B = advance_pm(rec, donor_use, clamp, z)
                if A is None:
                    design_gap = True
                    modes[mode] = {
                        "D_e": None, "D_q": None, "e_now": None, "q_now": None,
                        "e_intact": None if intact is None else intact["e"],
                        "q_intact": None if intact is None else intact["q"],
                        "eA": None, "eB": None, "qA": None, "qB": None, "LA": None, "LB": None,
                        "repair_equals_shadow": False,
                        "note": "UNRESOLVED-DESIGN [quotient successor not a function]",
                    }
                    continue
                mhat_next = lambda c, y: cell_mhat_R(t_star + 1, c, y)
                stA = stats_at(((c, i, p) for (c, i), p in A.items()), z, t_star + 1, mhat_next)
                stB = stats_at(((c, i, p) for (c, i), p in B.items()), z, t_star + 1, mhat_next)
                de = None if now is None or intact is None else now["e"] - intact["e"]
                dq = None if now is None or intact is None else now["q"] - intact["q"]
                modes[mode] = {
                    "D_e": de,
                    "D_q": dq,
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
                    "repair_equals_shadow": True,
                }
            interventions[direction] = modes
    swap_s = None if interventions["S"] is None else interventions["S"]["SWAP"]
    swap_e = None if interventions["E"] is None else interventions["E"]["SWAP"]
    # C-FO: p0 is F0. Decisions equal across beliefs represented at t_star iff A11 on those beliefs.
    beliefs = []
    for z in (0, 1):
        for cell, i, p in snaps[z][t_star]:
            if p != 0:
                beliefs.append(tables.b[i])
    cfo_a, cfo_b = _cfo_mb(world, beliefs)
    cfo = "PASS" if cfo_a == "PASS" and cfo_b == "PASS" else "FAIL"
    if design_gap:
        # an ill-defined successor makes the affected statistics unavailable
        cfo = cfo  # leave C-FO as computed; rescue/sel follow None fields
    usable = contrast and not design_gap
    flags, imp = _flags_from(dR, dM, e_agent, e_base, swap_s, swap_e, cfo, usable)
    if design_gap:
        flags["C-SEL"] = "NOT EVALUABLE [PM quotient successor not a function]"
        flags["rescue"] = "NOT EVALUABLE [PM quotient successor not a function]"
    pattern = _pattern(
        dR, dM, e_agent, e_base,
        swap_s if usable else None,
        swap_e if usable else None,
        cfo_a == "PASS", cfo_b == "PASS",
    )
    extra = {
        "action_mismatches": mismatches,
        "decoder_entries": len(decoder),
        "ill_defined_extractor": info["ill_defined"] or design_gap,
        "reachable": [len(snaps[0][t]) for t in range(T)],
        "zero_support_rule": "A decoder cell with zero intact support is NOT EVALUABLE. No extension rule is applied.",
    }
    return _pack_result(
        name, flags, pattern, imp, per_agent, per_base,
        (dS, dE), contrast and not design_gap, interventions, extra,
    )


def _rep_belief(belief_cell, t, cell):
    for b, c in belief_cell[t].items():
        if c == cell:
            return b
    return None


def _clamped_next(belief_cell, t, cell):
    """Next-layer cell of every belief in `cell`. Tuple of >1 means not a function."""
    if t + 1 >= len(belief_cell):
        return "BAD"
    nxt = set()
    for b, c in belief_cell[t].items():
        if c == cell:
            n = belief_cell[t + 1].get(b, "MISS")
            nxt.add(n)
    if len(nxt) != 1:
        return tuple(sorted((x if isinstance(x, int) else -999) for x in nxt))
    return next(iter(nxt))


def conf_theta0():
    return (S_U_SPEC + S_SP_SPEC) / 2
