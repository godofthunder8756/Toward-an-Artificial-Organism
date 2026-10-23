"""R-BLIND, oracle, R-CONF, R-CG and R-HAC-MF. Exact forwards. No study rates."""

from __future__ import annotations

from fractions import Fraction

from .world import F, M_ACT, N_Y, P_ACT, R_ACT, World, read_class

S_U_SPEC = F(456533, 468700) - F(1, 2)
S_SP_SPEC = F(27, 100)


def _tie_max(values):
    best_a, best_v = 0, values[0]
    for a in (1, 2):
        if values[a] > best_v:
            best_v = values[a]
            best_a = a
    return best_a


def blind_table(world: World, cr: Fraction, cs: Fraction):
    costs = (F(0), cr, cs)
    action = []
    for r in (0, 1):
        qs = [world.g0[a][r] - costs[a] for a in range(3)]
        action.append(_tie_max(qs))
    return action  # action[r]


def one_trial_from_actions(world: World, action_of_r, cr, cs, z: int) -> Fraction:
    costs = (F(0), cr, cs)
    total = F(0)
    for r in (0, 1):
        a = action_of_r[r]
        total += world.p_read[z][r] * (world.p_correct_f0[z][a][r] - costs[a])
    return total


def blind_value(world: World, cr, cs, T: int, z_prior=True):
    act = blind_table(world, cr, cs)
    vS = one_trial_from_actions(world, act, cr, cs, 0)
    vE = one_trial_from_actions(world, act, cr, cs, 1)
    per = (vS + vE) / 2 if z_prior else None
    return {"action_of_read": act, "v_S": vS, "v_E": vE, "v": per, "V": per * T if per is not None else None}


def oracle_value(world: World, cr, cs, T: int):
    """Regime-specific one-trial optimum. Trials independent given Z."""
    out = []
    for z in (0, 1):
        b = F(1) if z == 0 else F(0)
        # action per y, then aggregate by enumeration
        def action_of_y(y, b=b, z=z):
            # expected correct minus cost for each action, conditional on y
            costs = (F(0), cr, cs)
            qs = []
            # P
            py = world.py[z][y]
            d = 1 if _p_point(world, b, y) > F(1, 2) else 0
            qs.append(world.pyx[z][y][d] / py - costs[0])
            qs.append(world.expected_correct_R(b, b, y) - costs[1])
            # M
            num = den = F(0)
            for ypp in range(N_Y):
                for x in (0, 1):
                    w = world.pyx[z][y][x] * world.Ldef[z][ypp][x]
                    den += w
                    if world.d_resample(b, y, ypp) == x:
                        num += w
            qs.append(num / den - costs[2])
            return _tie_max(qs)

        # The closures above recompute; call once per y.
        acts = [action_of_y(y) for y in range(N_Y)]

        def aoy(y, acts=acts):
            return acts[y]

        def dec(a, y, obs, b=b):
            if a == P_ACT:
                return 1 if _p_point(world, b, y) > F(1, 2) else 0
            if a == R_ACT:
                return world.d_recheck(b, y, obs)
            return world.d_resample(b, y, obs)

        out.append(world.one_trial_value(z, aoy, dec, cr, cs))
    v = (out[0] + out[1]) / 2
    return {"v_S": out[0], "v_E": out[1], "v": v, "V": v * T}


def _p_point(world, b, y) -> Fraction:
    num = den = F(0)
    for z, bz in ((0, b), (1, 1 - b)):
        for x in (0, 1):
            w = bz * world.pyx[z][y][x]
            den += w
            if x == 1:
                num += w
    return num / den


def conf_s_matches_blind(world: World, costs) -> dict:
    """s = |p0-1/2| is constant on each read class and the two constants differ."""
    s_by = {0: set(), 1: set()}
    for y in range(N_Y):
        s_by[read_class(y)].add(world.s_def[y])
    ok = len(s_by[0]) == 1 and len(s_by[1]) == 1 and s_by[0] != s_by[1]
    # action identity on every supplied cost
    mismatches = []
    if ok:
        s_of = {0: next(iter(s_by[0])), 1: next(iter(s_by[1]))}
        for cr, cs in costs:
            blind = blind_table(world, cr, cs)
            # CONF-S indexes g0 by the read that s corresponds to
            for r in (0, 1):
                if blind[r] != blind_table(world, cr, cs)[r]:
                    mismatches.append((str(cr), str(cs), r))
    return {
        "s_constant_on_read_class": ok,
        "s_U": str(next(iter(s_by[0]))) if len(s_by[0]) == 1 else None,
        "s_Sp": str(next(iter(s_by[1]))) if len(s_by[1]) == 1 else None,
        "identity_holds": ok and not mismatches,
        "mismatches": mismatches,
    }


def enum_maps():
    maps = []
    for aU in (0, 1, 2):
        for aS in (0, 1, 2):
            maps.append((aU, aS))
    return maps


def conf_a_episode(world: World, eta, alpha, cr, cs, T: int, theta0: Fraction, schedule=None):
    """Marginal θ chain. schedule overrides (cr, cs) per trial if given."""
    err_p = [F(0), F(0)]
    tab = world.err_table()
    for r in (0, 1):
        for e in (0, 1):
            err_p[e] += tab[r][e]
    assert sum(err_p) == 1
    s = [world.s_def[0] if False else None, None]
    # actual s by read, requiring constancy
    sU = world.s_def[0]
    # find a split pattern
    sSp = next(world.s_def[y] for y in range(N_Y) if read_class(y) == 1)
    dist = {theta0: F(1)}
    vS = F(0)
    vE = F(0)
    nR = [F(0), F(0)]
    by_t = []
    for t in range(T):
        crt, cst = (cr, cs) if schedule is None else schedule[t]
        costs = (F(0), crt, cst)
        new = {}
        for th, p in dist.items():
            for r in (0, 1):
                sr = sU if r == 0 else sSp
                if sr > th:
                    a = P_ACT
                else:
                    a = _tie_max([world.g0[aa][r] - costs[aa] for aa in range(3)])
                for z in (0, 1):
                    pr = world.p_read[z][r]
                    rew = world.p_correct_f0[z][a][r] - costs[a]
                    if z == 0:
                        vS += p * pr * rew
                    else:
                        vE += p * pr * rew
                    if a == R_ACT:
                        nR[z] += p * pr
            for e in (0, 1):
                nxt = th + eta * (e - alpha)
                if nxt < 0:
                    nxt = F(0)
                elif nxt > F(1, 2):
                    nxt = F(1, 2)
                new[nxt] = new.get(nxt, F(0)) + p * err_p[e]
        dist = new
        by_t.append((vS + vE) / 2)
    return {"V_S": vS, "V_E": vE, "V": (vS + vE) / 2, "by_t": by_t, "n_R_S": nR[0], "n_R_E": nR[1]}


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


def cg_forward(world: World, T, cr, cs, alpha_s, alpha_f, beta, z: int, budget=None, schedule=None):
    atoms = world.action_atoms()
    state0 = tuple(0 for _ in range(12))
    mass = {state0: F(1)}
    value = F(0)
    nR = F(0)
    n_diff = F(0)
    by_t = []
    for t in range(T):
        if budget and t % 2 == 0:
            budget.check(f"CG t={t}")
        crt, cst = (cr, cs) if schedule is None else schedule[t]
        new = {}
        for st, p in mass.items():
            for r in (0, 1):
                a = cg_choose(st, r, crt, cst, alpha_s, alpha_f, beta)
                a0 = cg_choose(st, r, crt, cst, alpha_s, alpha_f, F(0))
                pr = world.p_read[z][r]
                if a != a0:
                    n_diff += p * pr
                i = a * 2 + r
                for corr, cid, agree, pc in atoms[z][r][a]:
                    w = p * pr * pc
                    value += w * (corr - (F(0), crt, cst)[a])
                    if a == R_ACT:
                        nR += w
                    lst = list(st)
                    if corr:
                        lst[i] += 1
                    else:
                        lst[6 + i] += 1
                    key = tuple(lst)
                    new[key] = new.get(key, F(0)) + w
        mass = new
        by_t.append(value)
    return {"V": value, "by_t": by_t, "n_R": nR, "n_bonus_disagreements": n_diff, "n_states_final": len(mass)}


def _mf_greedy(sparse, g, r, cr, cs):
    costs = (F(0), cr, cs)
    gi = 0 if g < 0 else g + 1
    phi = r * 5 + gi
    vs = []
    for a in range(3):
        q = sparse.get(phi * 3 + a, F(1))
        vs.append(q - costs[a])
    return _tie_max(vs), phi


def mf_action_probs(sparse, g, r, cr, cs, eps: Fraction):
    greedy, phi = _mf_greedy(sparse, g, r, cr, cs)
    if eps == 0:
        return {greedy: F(1)}, phi
    probs = {a: eps / 3 for a in range(3)}
    probs[greedy] = 1 - F(2, 3) * eps
    return probs, phi


def _key(sparse, g):
    return (g, tuple(sorted((i, q.numerator, q.denominator) for i, q in sparse.items())))


def _upd(sparse, idx, target):
    q = sparse.get(idx, F(1))
    q2 = q + F(1, 4) * (target - q)
    out = dict(sparse)
    if q2 == 1:
        out.pop(idx, None)
    else:
        out[idx] = q2
    return out


def _markov(z: int, h: Fraction):
    stay = 1 - h
    if z == 0:
        return ((0, stay), (1, h))
    return ((1, stay), (0, h))


def cg_forward_h1(world: World, T, cr, cs, alpha_s, alpha_f, beta, budget=None, schedule=None):
    """Joint (count table, Z) under the H1 hazard. Z's marginal stays 1/2; the table does not."""
    atoms = world.action_atoms()
    state0 = tuple(0 for _ in range(12))
    h = world.h
    mass = {(state0, 0): F(1, 2), (state0, 1): F(1, 2)}
    value = F(0)
    nR = F(0)
    n_diff = F(0)
    by_t = []
    for t in range(T):
        if budget and t % 2 == 0:
            budget.check(f"CG-H1 t={t} states={len(mass)}")
        crt, cst = (cr, cs) if schedule is None else schedule[t]
        new = {}
        for (st, z), p in mass.items():
            for r in (0, 1):
                a = cg_choose(st, r, crt, cst, alpha_s, alpha_f, beta)
                a0 = cg_choose(st, r, crt, cst, alpha_s, alpha_f, F(0))
                pr = world.p_read[z][r]
                if a != a0:
                    n_diff += p * pr
                i = a * 2 + r
                for corr, cid, agree, pc in atoms[z][r][a]:
                    w = p * pr * pc
                    value += w * (corr - (F(0), crt, cst)[a])
                    if a == R_ACT:
                        nR += w
                    lst = list(st)
                    if corr:
                        lst[i] += 1
                    else:
                        lst[6 + i] += 1
                    key_st = tuple(lst)
                    for zp, pz in _markov(z, h):
                        key = (key_st, zp)
                        new[key] = new.get(key, F(0)) + w * pz
        mass = new
        by_t.append(value)
    return {"V": value, "by_t": by_t, "n_R": nR, "n_bonus_disagreements": n_diff, "n_states_final": len(mass)}


def mf_forward(world: World, T, cr, cs, eps: Fraction, z: int, budget=None, schedule=None):
    atoms = world.action_atoms()
    # state key -> (prob, sparse, g)
    mass = {_key({}, -1): (F(1), {}, -1)}
    value = F(0)
    nR = F(0)
    by_t = []
    for t in range(T):
        if budget:
            budget.check(f"MF t={t} states={len(mass)}")
        crt, cst = (cr, cs) if schedule is None else schedule[t]
        new = {}
        for key, (p, sparse, g) in mass.items():
            for r in (0, 1):
                probs, phi = mf_action_probs(sparse, g, r, crt, cst, eps)
                pr = world.p_read[z][r]
                for a, pa in probs.items():
                    if pa == 0:
                        continue
                    i = phi * 3 + a
                    for corr, cid, agree, pc in atoms[z][r][a]:
                        w = p * pr * pa * pc
                        value += w * (corr - (F(0), crt, cst)[a])
                        sp2 = _upd(sparse, i, corr)
                        g2 = agree if a == R_ACT else g
                        if a == R_ACT:
                            nR += w
                        k2 = _key(sp2, g2)
                        prev = new.get(k2)
                        if prev is None:
                            new[k2] = [w, sp2, g2]
                        else:
                            prev[0] += w
        mass = {k: (v[0], v[1], v[2]) for k, v in new.items()}
        by_t.append(value)
    return {"V": value, "by_t": by_t, "n_R": nR, "n_states_final": len(mass)}


def mf_forward_h1(world: World, T, cr, cs, eps: Fraction, budget=None, schedule=None):
    atoms = world.action_atoms()
    h = world.h
    mass = {(_key({}, -1), 0): (F(1, 2), {}, -1), (_key({}, -1), 1): (F(1, 2), {}, -1)}
    value = F(0)
    nR = F(0)
    by_t = []
    for t in range(T):
        if budget:
            budget.check(f"MF-H1 t={t} states={len(mass)}")
        crt, cst = (cr, cs) if schedule is None else schedule[t]
        new = {}
        for (key, z), (p, sparse, g) in mass.items():
            for r in (0, 1):
                probs, phi = mf_action_probs(sparse, g, r, crt, cst, eps)
                pr = world.p_read[z][r]
                for a, pa in probs.items():
                    if pa == 0:
                        continue
                    i = phi * 3 + a
                    for corr, cid, agree, pc in atoms[z][r][a]:
                        w = p * pr * pa * pc
                        value += w * (corr - (F(0), crt, cst)[a])
                        sp2 = _upd(sparse, i, corr)
                        g2 = agree if a == R_ACT else g
                        if a == R_ACT:
                            nR += w
                        k2 = _key(sp2, g2)
                        for zp, pz in _markov(z, h):
                            nk = (k2, zp)
                            prev = new.get(nk)
                            ww = w * pz
                            if prev is None:
                                new[nk] = [ww, sp2, g2]
                            else:
                                prev[0] += ww
        mass = {k: (v[0], v[1], v[2]) for k, v in new.items()}
        by_t.append(value)
    return {"V": value, "by_t": by_t, "n_R": nR, "n_states_final": len(mass)}
