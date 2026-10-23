"""Finite-horizon exact values for R-HAC-MB and R-HAC-MB-myopic.

H0 state: multiset of RECHECK likelihood-ratio classes (a count vector).
H1 state: the exact posterior, because the hazard mixes beliefs between trials
and the order of evidence matters. Non-recheck emissions must match across
regimes; that is checked, not assumed silently at runtime.
"""

from __future__ import annotations

from fractions import Fraction

from .world import F, M_ACT, N_Y, P_ACT, R_ACT, World

# P, R, M tie order is implemented by strict updates: P is the default,
# R replaces only if strictly better, M replaces only if strictly better.


def _enumerate_counts(n_cls: int, max_sum: int):
    counts = []
    cur = [0] * n_cls

    def rec(pos: int, remaining: int) -> None:
        if pos == n_cls - 1:
            cur[pos] = remaining
            counts.append(tuple(cur))
            return
        for v in range(remaining + 1):
            cur[pos] = v
            rec(pos + 1, remaining - v)

    for s in range(max_sum + 1):
        rec(0, s)
    return counts


class BeliefIndex:
    """Count vectors with total rechecks <= max_sum."""

    def __init__(self, world: World, max_sum: int):
        if not world.emissions_match:
            raise RuntimeError("H0 count state requires matched P/M emissions")
        self.world = world
        self.max_sum = max_sum
        self.counts = _enumerate_counts(10, max_sum)
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
        # P(class | z, y)
        self.pc = [[[F(0) for _ in range(10)] for _ in range(N_Y)] for _ in (0, 1)]
        for z in (0, 1):
            for y in range(N_Y):
                py = world.py[z][y]
                for c in range(10):
                    self.pc[z][y][c] = world.p_y_class[z][y][c] / py
        self.invariant = self._decision_invariant()
        self.kappa = [[F(0) for _ in range(N_Y)] for _ in (0, 1)]
        if self.invariant:
            for z in (0, 1):
                bt = F(1) if z == 0 else F(0)
                for y in range(N_Y):
                    self.kappa[z][y] = world.expected_correct_R(F(0), bt, y)

    def _decision_invariant(self) -> bool:
        w = self.world
        for y in range(N_Y):
            for yp in range(N_Y):
                if w.d_recheck(F(0), y, yp) != w.d_recheck(F(1), y, yp):
                    return False
        return True

    def correct_R(self, b: Fraction, y: int) -> Fraction:
        if self.invariant:
            return b * self.kappa[0][y] + (1 - b) * self.kappa[1][y]
        return self.world.expected_correct_R(b, b, y)

    def cont_R(self, i: int, b: Fraction, y: int, V) -> Fraction:
        """E[V(next) | belief i, y, do R]. V is a list or None (then 0)."""
        if V is None:
            return F(0)
        acc = F(0)
        pcS = self.pc[0][y]
        pcE = self.pc[1][y]
        tr = self.trans[i]
        b1 = 1 - b
        for c in range(10):
            p = b * pcS[c] + b1 * pcE[c]
            if p == 0:
                continue
            j = tr[c]
            acc += p * (V[j] if j >= 0 else F(0))
        return acc


def _choose(qP, qR, qM):
    q = qP
    a = P_ACT
    if qR > q:
        q = qR
        a = R_ACT
    if qM > q:
        q = qM
        a = M_ACT
    return a, q


class H0Solver:
    def __init__(self, world: World, T: int):
        self.world = world
        self.T = T
        # max_sum=T so the last RECHECK has a landing state. Decisions are
        # computed only for sums <= T-k <= T-1.
        self.idx = BeliefIndex(world, T)
        self.immP, self.immM = world.imm_PM()
        self.py = world.py[0]

    def solve_cost(self, cr: Fraction, cs: Fraction, budget=None, myopic: bool = False):
        """Return pol[k][i] as a bytearray of length n*8 (k = 1..T) and value of empty belief.

        pol[0] unused. Action for (k, i, y) at offset i*8+y.
        If myopic, the argmax ignores continuation but the returned value includes it.
        """
        idx = self.idx
        n = len(idx.counts)
        T = self.T
        immP, immM, py = self.immP, self.immM, self.py
        # V for previous horizon, list of Fraction or 0
        Vprev = None
        values = []  # values[k-1] = V_k(empty) for the optimal or myopic-policy value
        pols = [None]
        for k in range(1, T + 1):
            if budget and k % 1 == 0:
                budget.check(f"H0 k={k}")
            max_sum = T - k
            Vk = [F(0)] * n
            pol = bytearray(n * 8)
            use_cont = (k > 1) and (not myopic)
            # policy evaluation continuation always uses Vprev when k>1
            for i in range(n):
                if idx.sum[i] > max_sum:
                    continue
                b = idx.b[i]
                acc = F(0)
                base = i * 8
                for y in range(N_Y):
                    cont_same = Vprev[i] if (k > 1 and Vprev is not None) else F(0)
                    qP = immP[y] + (cont_same if not myopic else F(0))
                    qM = immM[y] - cs + (cont_same if not myopic else F(0))
                    ec = idx.correct_R(b, y)
                    ev_for_choice = idx.cont_R(i, b, y, Vprev) if use_cont else F(0)
                    qR = ec - cr + ev_for_choice
                    # myopic choice drops continuation; policy-evaluation value adds it back
                    a, q_choice = _choose(
                        immP[y] if myopic else qP,
                        (ec - cr) if myopic else qR,
                        (immM[y] - cs) if myopic else qM,
                    )
                    pol[base + y] = a
                    if myopic:
                        if a == P_ACT:
                            q = immP[y] + cont_same
                        elif a == R_ACT:
                            q = ec - cr + (idx.cont_R(i, b, y, Vprev) if k > 1 else F(0))
                        else:
                            q = immM[y] - cs + cont_same
                    else:
                        q = q_choice
                    acc += py[y] * q
                Vk[i] = acc
            values.append(Vk[0])
            pols.append(pol)
            Vprev = Vk
        return {"values": values, "pol": pols, "invariant": idx.invariant}

    def forward(self, pol, T: int, cr: Fraction, cs: Fraction, z: int, budget=None):
        """Simulate the stored policy for horizon T under true regime z.

        pol is indexed by remaining horizon k.
        Returns value, E[n_R], E[n_R on unanimous], E[n_M], E[cost], first-recheck distribution.
        """
        idx = self.idx
        world = self.world
        py = world.py[z]
        costs = (F(0), cr, cs)
        mass = {0: F(1)}
        # mass_new flag split for first recheck: pair (i, seen)
        mass_u = {0: F(1)}  # not yet rechecked
        value = F(0)
        nR = F(0)
        nR_u = F(0)
        nM = F(0)
        cost = F(0)
        first = [F(0) for _ in range(T + 1)]  # index t (1-based) and [0] unused; never in last
        never = F(0)
        for t in range(T):
            if budget and t % 2 == 0:
                budget.check(f"H0 forward t={t}")
            k = T - t
            pol_k = pol[k]
            new = {}
            new_u = {}
            pR_here = F(0)
            for i, p in mass.items():
                base = i * 8
                b = idx.b[i]
                for y in range(N_Y):
                    a = pol_k[base + y]
                    w = p * py[y]
                    if a == P_ACT:
                        value += w * self.immP[y]
                        new[i] = new.get(i, F(0)) + w
                    elif a == M_ACT:
                        value += w * (self.immM[y] - cs)
                        nM += w
                        cost += w * cs
                        new[i] = new.get(i, F(0)) + w
                    else:
                        # Predictor uses the agent's belief; the expectation uses the true regime.
                        ec = world.expected_correct_R(b, F(1) if z == 0 else F(0), y)
                        value += w * (ec - cr)
                        nR += w
                        if y == 0 or y == N_Y - 1:
                            nR_u += w
                        cost += w * cr
                        pR_here += w
                        for c in range(10):
                            wc = w * idx.pc[z][y][c]
                            if wc == 0:
                                continue
                            j = idx.trans[i][c]
                            new[j] = new.get(j, F(0)) + wc
            # first-recheck bookkeeping on the unseen mass
            seen_now = F(0)
            for i, p in mass_u.items():
                base = i * 8
                for y in range(N_Y):
                    a = pol_k[base + y]
                    w = p * py[y]
                    if a == R_ACT:
                        seen_now += w
                        for c in range(10):
                            wc = w * idx.pc[z][y][c]
                            if wc == 0:
                                continue
                            j = idx.trans[i][c]
                            # seen, so do not keep in unseen
                            _ = j
                    else:
                        new_u[i] = new_u.get(i, F(0)) + w
            first[t + 1] = seen_now
            mass = new
            mass_u = new_u
        never = sum(mass_u.values(), F(0))
        return {
            "value": value,
            "n_R": nR,
            "n_R_unanimous": nR_u,
            "n_M": nM,
            "exploration_cost": cost,
            "first_R": first[1:],
            "never_R": never,
        }


def solve_h1(world: World, T: int, cr: Fraction, cs: Fraction, budget=None, myopic: bool = False):
    """Backward values V_k(b) for k=1..T at every belief reachable in T-k steps.

    Returns values[k-1] = V_k(prior), and a policy dict (k, b, y) -> action.
    """
    if not world.emissions_match:
        raise RuntimeError("H1 solver requires matched P/M emissions")
    # Reuse invariance / kappa / class probabilities via a tiny index of max_sum 0
    # only for the helper methods that do not need trans. Build a BeliefIndex of
    # max_sum 0 for kappa, and use world tables for transitions on Fraction b.
    helper = BeliefIndex(world, 0)
    immP, immM = world.imm_PM()
    py = world.py[0]
    # layers[d] = set of beliefs after d completed trials
    layers = [{F(1, 2)}]
    for d in range(T - 1):
        if budget:
            budget.check(f"H1 beliefs d={d}")
        nxt = set()
        for b in layers[-1]:
            nxt.add(world.mix_h1(b))
            for c in range(10):
                nxt.add(world.mix_h1(world.update_belief(b, c)))
        layers.append(nxt)
    # Vprev: dict belief -> value at horizon k-1
    Vprev = {}
    values = []
    pol = {}
    pc = helper.pc

    def cont(b, y, Vp):
        if not Vp:
            return F(0)
        acc = F(0)
        b1 = 1 - b
        # no: continuation is class-dependent. P(c|b,y) then mix(update(b,c))
        for c in range(10):
            p = b * pc[0][y][c] + b1 * pc[1][y][c]
            if p == 0:
                continue
            bn = world.mix_h1(world.update_belief(b, c))
            acc += p * Vp.get(bn, F(0))
        return acc

    def cont_same(b, Vp):
        if not Vp:
            return F(0)
        return Vp.get(world.mix_h1(b), F(0))

    for k in range(1, T + 1):
        if budget:
            budget.check(f"H1 k={k}")
        # beliefs that occur with remaining horizon k under total horizon <= T:
        # depth d with d <= T-k
        beliefs = set()
        for d in range(T - k + 1):
            beliefs |= layers[d]
        Vk = {}
        for b in beliefs:
            acc = F(0)
            csame = cont_same(b, Vprev) if k > 1 else F(0)
            for y in range(N_Y):
                ec = helper.correct_R(b, y)
                ev = cont(b, y, Vprev) if (k > 1 and not myopic) else F(0)
                if myopic:
                    a, _ = _choose(immP[y], ec - cr, immM[y] - cs)
                    if a == P_ACT:
                        q = immP[y] + (csame if k > 1 else F(0))
                    elif a == R_ACT:
                        q = ec - cr + (cont(b, y, Vprev) if k > 1 else F(0))
                    else:
                        q = immM[y] - cs + (csame if k > 1 else F(0))
                else:
                    qP = immP[y] + (csame if k > 1 else F(0))
                    qM = immM[y] - cs + (csame if k > 1 else F(0))
                    qR = ec - cr + ev
                    a, q = _choose(qP, qR, qM)
                pol[(k, b, y)] = a
                acc += py[y] * q
            Vk[b] = acc
        values.append(Vk[F(1, 2)])
        Vprev = Vk
    return {"values": values, "pol": pol, "layers": layers, "invariant": helper.invariant, "helper": helper}


def forward_h1(world: World, pol, T: int, cr: Fraction, cs: Fraction, budget=None):
    """Forward joint on (belief, Z) for an H1 policy. pol[(k,b,y)] -> action.

    Z transition after each trial. Returns the marginal value and recheck stats.
    """
    helper = BeliefIndex(world, 0)
    immP, immM = world.imm_PM()
    # mass: (b, z) -> prob. Start Z prior 1/2, b=1/2.
    mass = {(F(1, 2), 0): F(1, 2), (F(1, 2), 1): F(1, 2)}
    value = F(0)
    nR = F(0)
    nR_u = F(0)
    nM = F(0)
    cost = F(0)
    first = []
    unseen = {(F(1, 2), 0): F(1, 2), (F(1, 2), 1): F(1, 2)}
    h = world.h
    for t in range(T):
        if budget:
            budget.check(f"H1 forward t={t}")
        k = T - t
        new = {}
        new_u = {}
        seen_now = F(0)
        for (b, z), p in mass.items():
            bt = F(1) if z == 0 else F(0)
            for y in range(N_Y):
                a = pol[(k, b, y)]
                w = p * world.py[z][y]
                if a == P_ACT:
                    value += w * immP[y]
                    bn = world.mix_h1(b)
                    for zp, pz in _h_trans(z, h):
                        key = (bn, zp)
                        new[key] = new.get(key, F(0)) + w * pz
                elif a == M_ACT:
                    value += w * (immM[y] - cs)
                    nM += w
                    cost += w * cs
                    bn = world.mix_h1(b)
                    for zp, pz in _h_trans(z, h):
                        key = (bn, zp)
                        new[key] = new.get(key, F(0)) + w * pz
                else:
                    ec = world.expected_correct_R(b, bt, y)
                    value += w * (ec - cr)
                    nR += w
                    if y == 0 or y == N_Y - 1:
                        nR_u += w
                    cost += w * cr
                    for c in range(10):
                        wc = w * helper.pc[z][y][c]
                        if wc == 0:
                            continue
                        bn = world.mix_h1(world.update_belief(b, c))
                        for zp, pz in _h_trans(z, h):
                            key = (bn, zp)
                            new[key] = new.get(key, F(0)) + wc * pz
        for (b, z), p in unseen.items():
            for y in range(N_Y):
                a = pol[(k, b, y)]
                w = p * world.py[z][y]
                if a == R_ACT:
                    seen_now += w
                else:
                    bn = world.mix_h1(b)
                    for zp, pz in _h_trans(z, h):
                        key = (bn, zp)
                        new_u[key] = new_u.get(key, F(0)) + w * pz
        first.append(seen_now)
        mass = new
        unseen = new_u
    return {
        "value": value,
        "n_R": nR,
        "n_R_unanimous": nR_u,
        "n_M": nM,
        "exploration_cost": cost,
        "first_R": first,
        "never_R": sum(unseen.values(), F(0)),
    }


def solve_h0_schedule(solver: H0Solver, schedule, budget=None):
    """Known cost schedule. schedule[t] = (cr, cs) for 0-based trial t.

    Returns (value at the empty belief, pol_by_t) where pol_by_t[t] is a bytearray.
    """
    T = len(schedule)
    idx = solver.idx
    n = len(idx.counts)
    immP, immM, py = solver.immP, solver.immM, solver.py
    Vnext = None
    pols = [None] * T
    value = F(0)
    for t in range(T - 1, -1, -1):
        if budget:
            budget.check(f"H0 schedule t={t}")
        cr, cs = schedule[t]
        Vk = [F(0)] * n
        pol = bytearray(n * N_Y)
        for i in range(n):
            if idx.sum[i] > t:
                continue
            b = idx.b[i]
            acc = F(0)
            base = i * N_Y
            for y in range(N_Y):
                cont = Vnext[i] if Vnext is not None else F(0)
                ev = idx.cont_R(i, b, y, Vnext) if Vnext is not None else F(0)
                a, q = _choose(immP[y] + cont, idx.correct_R(b, y) - cr + ev, immM[y] - cs + cont)
                pol[base + y] = a
                acc += py[y] * q
            Vk[i] = acc
        pols[t] = pol
        Vnext = Vk
        value = Vk[0]
    return value, pols


def forward_schedule(solver: H0Solver, pol_by_t, schedule, z: int, budget=None):
    """pol_by_t[t] is the policy used at 0-based trial t. Rewards use schedule[t]."""
    idx = solver.idx
    world = solver.world
    py = world.py[z]
    T = len(schedule)
    mass = {0: F(1)}
    value = F(0)
    nR = F(0)
    nM = F(0)
    cost = F(0)
    for t in range(T):
        cr, cs = schedule[t]
        pol = pol_by_t[t]
        new = {}
        for i, p in mass.items():
            b = idx.b[i]
            base = i * N_Y
            for y in range(N_Y):
                a = pol[base + y]
                w = p * py[y]
                if a == P_ACT:
                    value += w * solver.immP[y]
                    new[i] = new.get(i, F(0)) + w
                elif a == M_ACT:
                    value += w * (solver.immM[y] - cs)
                    nM += w
                    cost += w * cs
                    new[i] = new.get(i, F(0)) + w
                else:
                    ec = world.expected_correct_R(b, F(1) if z == 0 else F(0), y)
                    value += w * (ec - cr)
                    nR += w
                    cost += w * cr
                    for c in range(10):
                        wc = w * idx.pc[z][y][c]
                        if wc == 0:
                            continue
                        j = idx.trans[i][c]
                        new[j] = new.get(j, F(0)) + wc
        mass = new
    return {"value": value, "n_R": nR, "n_M": nM, "exploration_cost": cost}


def solve_h1_schedule(world: World, schedule, budget=None):
    """Switch-aware H1. schedule[t] = (cr, cs). Value is the prior belief's value at t=0."""
    if not world.emissions_match:
        raise RuntimeError("H1 schedule requires matched P/M emissions")
    helper = BeliefIndex(world, 0)
    immP, immM = world.imm_PM()
    py = world.py[0]
    T = len(schedule)
    layers = [{F(1, 2)}]
    for d in range(T - 1):
        nxt = set()
        for b in layers[-1]:
            nxt.add(world.mix_h1(b))
            for c in range(10):
                nxt.add(world.mix_h1(world.update_belief(b, c)))
        layers.append(nxt)
    Vnext = {}
    pc = helper.pc
    pols = [None] * T
    value = F(0)

    def cont_same(b):
        return Vnext.get(world.mix_h1(b), F(0)) if Vnext else F(0)

    def cont(b, y):
        if not Vnext:
            return F(0)
        acc = F(0)
        b1 = 1 - b
        for c in range(10):
            p = b * pc[0][y][c] + b1 * pc[1][y][c]
            if p == 0:
                continue
            bn = world.mix_h1(world.update_belief(b, c))
            acc += p * Vnext.get(bn, F(0))
        return acc

    for t in range(T - 1, -1, -1):
        if budget:
            budget.check(f"H1 schedule t={t}")
        cr, cs = schedule[t]
        beliefs = set()
        for d in range(t + 1):
            beliefs |= layers[d]
        Vk = {}
        pol = {}
        for b in beliefs:
            acc = F(0)
            for y in range(N_Y):
                ec = helper.correct_R(b, y)
                a, q = _choose(
                    immP[y] + (cont_same(b) if t + 1 < T else F(0)),
                    ec - cr + (cont(b, y) if t + 1 < T else F(0)),
                    immM[y] - cs + (cont_same(b) if t + 1 < T else F(0)),
                )
                pol[(b, y)] = a
                acc += py[y] * q
            Vk[b] = acc
        pols[t] = pol
        Vnext = Vk
        value = Vk[F(1, 2)]
    return {"value": value, "pol": pols, "helper": helper}


def forward_h1_schedule(world: World, pol_by_t, schedule, budget=None):
    helper = BeliefIndex(world, 0)
    immP, immM = world.imm_PM()
    T = len(schedule)
    mass = {(F(1, 2), 0): F(1, 2), (F(1, 2), 1): F(1, 2)}
    value = F(0)
    h = world.h
    for t in range(T):
        cr, cs = schedule[t]
        pol = pol_by_t[t]
        new = {}
        for (b, z), p in mass.items():
            bt = F(1) if z == 0 else F(0)
            for y in range(N_Y):
                a = pol[(b, y)]
                w = p * world.py[z][y]
                if a == R_ACT:
                    ec = world.expected_correct_R(b, bt, y)
                    value += w * (ec - cr)
                    for c in range(10):
                        wc = w * helper.pc[z][y][c]
                        if wc == 0:
                            continue
                        bn = world.mix_h1(world.update_belief(b, c))
                        for zp, pz in _h_trans(z, h):
                            key = (bn, zp)
                            new[key] = new.get(key, F(0)) + wc * pz
                else:
                    reward = immP[y] if a == P_ACT else immM[y] - cs
                    value += w * reward
                    bn = world.mix_h1(b)
                    for zp, pz in _h_trans(z, h):
                        key = (bn, zp)
                        new[key] = new.get(key, F(0)) + w * pz
        mass = new
    return value


def _h_trans(z: int, h: Fraction):
    stay = 1 - h
    if z == 0:
        return ((0, stay), (1, h))
    return ((1, stay), (0, h))
