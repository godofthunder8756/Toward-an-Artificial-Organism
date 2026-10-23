"""Stage-B ADAPT certificate.

Controls KNOWN-FIXED and IID-REGIME are the §5.7 construction: the register is
held at η0, the encoder reproduces the best slice, and collapsing the register
does not increase the configuration count. Experimental SWITCHING and
UNKNOWN-FIXED are exact on the declared subclass and are left UNRESOLVED when
that subclass does not meet the regime-known upper bound.

Literal timing reading: the hazard h is the probability that the regime flips
after the update and before the next episode. IID-REGIME redraws the regime
independently; it is not the h = 1/2 flip chain.
"""

from __future__ import annotations

from fractions import Fraction

from common import fmt

CHOICES = (0, 1, 2, "eta", "none")


def _gauss(rows):
    """Solve a square system. rows are augmented [A | b]. Returns None if singular."""
    n = len(rows)
    M = [list(row) for row in rows]
    for col in range(n):
        pivot = None
        for r in range(col, n):
            if M[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            return None
        M[col], M[pivot] = M[pivot], M[col]
        div = M[col][col]
        for j in range(col, n + 1):
            M[col][j] /= div
        for r in range(n):
            if r == col or M[r][col] == 0:
                continue
            factor = M[r][col]
            for j in range(col, n + 1):
                M[r][j] -= factor * M[col][j]
    return [M[i][n] for i in range(n)]


def _sccs(succ):
    n = len(succ)
    index = 0
    stack = []
    on = [False] * n
    idx = [-1] * n
    low = [0] * n
    comps = []

    def strong(v):
        nonlocal index
        idx[v] = low[v] = index
        index += 1
        stack.append(v)
        on[v] = True
        for w in succ[v]:
            if idx[w] < 0:
                strong(w)
                low[v] = min(low[v], low[w])
            elif on[w]:
                low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = stack.pop()
                on[w] = False
                comp.append(w)
                if w == v:
                    break
            comps.append(comp)

    for v in range(n):
        if idx[v] < 0:
            strong(v)
    return comps


def _stationary(P, states):
    """Unique stationary on an irreducible component. Cesàro limit."""
    m = len(states)
    if m == 1:
        return {states[0]: Fraction(1)}
    pos = {s: i for i, s in enumerate(states)}
    rows = []
    for j in range(m - 1):
        row = [Fraction(0)] * m
        sj = states[j]
        row[j] -= 1
        for i, si in enumerate(states):
            row[i] += P[si][sj]
        row.append(Fraction(0))
        rows.append(row)
    rows.append([Fraction(1)] * m + [Fraction(1)])
    sol = _gauss(rows)
    if sol is None:
        raise RuntimeError("irreducible component has no unique stationary distribution")
    return {states[i]: sol[i] for i in range(m)}


def limit_from(P, start):
    """Cesàro limit from one start state. Exact on a finite chain."""
    n = len(P)
    succ = [[j for j in range(n) if P[i][j] != 0] for i in range(n)]
    comps = _sccs(succ)
    comp_of = [0] * n
    for ci, comp in enumerate(comps):
        for s in comp:
            comp_of[s] = ci
    recurrent = []
    for ci, comp in enumerate(comps):
        if all(comp_of[j] == ci for s in comp for j in succ[s]):
            recurrent.append(ci)
    rec_index = {ci: k for k, ci in enumerate(recurrent)}
    # Absorption probabilities into each recurrent component.
    transient = [s for s in range(n) if comp_of[s] not in rec_index]
    absorb = []
    for ci in recurrent:
        known = {}
        for s in range(n):
            if comp_of[s] == ci:
                known[s] = Fraction(1)
            elif comp_of[s] in rec_index:
                known[s] = Fraction(0)
        if not transient:
            absorb.append(known)
            continue
        rows = []
        for s in transient:
            row = []
            for t in transient:
                coef = (P[s][t] if t != s else P[s][t] - 1)
                # a_s = sum_j P_sj a_j, so a_s - sum_{t transient} P_st a_t = sum_{j known} P_sj known
                row.append(Fraction(1) - P[s][s] if t == s else -P[s][t])
            rhs = Fraction(0)
            for j, value in known.items():
                rhs += P[s][j] * value
            row.append(rhs)
            rows.append(row)
        sol = _gauss(rows)
        if sol is None:
            raise RuntimeError("absorption system is singular")
        for t, value in zip(transient, sol):
            known[t] = value
        absorb.append(known)
    mix = [Fraction(0)] * n
    for k, ci in enumerate(recurrent):
        weight = absorb[k][start]
        if weight == 0:
            continue
        stat = _stationary(P, comps[ci])
        for s, prob in stat.items():
            mix[s] += weight * prob
    if sum(mix) != 1:
        raise RuntimeError(f"limit does not sum to 1 ({sum(mix)})")
    return mix


def _hit_prob(choice, rho, v):
    if choice in ("eta", "none"):
        return Fraction(0)
    if choice == rho:
        return v
    return (1 - v) / 2


def _reward(choice, rho, v, delta, r):
    """Correct-bit S-DIRECT reward given the protected offset."""
    p = _hit_prob(choice, rho, v)
    fragile = 1 - delta * (1 - r)
    return p * 1 + (1 - p) * fragile


def omni_value(b_up, delta, v, r):
    """Regime-known upper bound. A field answers only its own query."""
    delta = Fraction(delta)
    v = Fraction(v)
    r = Fraction(r)
    if delta == 0 or b_up >= 3:
        return Fraction(1)
    if b_up <= 0:
        return 1 - delta * (1 - r)
    if b_up == 1:
        p_frag = 1 - v
    else:
        p_frag = (1 - v) / 2
    return 1 - delta * (1 - r) * p_frag


def memoryless_value(b_up, delta, v, r, regime_known=False):
    """Best correct-bit value with no informative register."""
    if regime_known:
        return omni_value(b_up, delta, v, r)
    # IID / stationary-unknown: P(q = c) = P(q = c+1) = (v + (1-v)/2)/2, P(q = c+2) = (1-v)/2.
    v = Fraction(v)
    delta = Fraction(delta)
    r = Fraction(r)
    p_side = (v + (1 - v) / 2) / 2
    p_rare = (1 - v) / 2
    if b_up >= 3 or delta == 0:
        return Fraction(1)
    if b_up <= 0:
        return 1 - delta * (1 - r)
    if b_up == 1:
        p_hit = p_side
    else:
        # Protect both elevated fields; the rare field is exposed under both regimes.
        p_hit = 1 - p_rare
    return p_hit * 1 + (1 - p_hit) * (1 - delta * (1 - r))


def build_chain(encoder, g, H, eta0, delta, v, r, mode, h):
    """Transition matrix on (rho, eta) with eta in 1..H and rho in {0,1}.

    mode: known (regime 0 fixed), switching (flip h), unknown (h = 0), iid (redraw).
    """
    delta = Fraction(delta)
    v = Fraction(v)
    r = Fraction(r)
    h = Fraction(h)
    n = 2 * H
    P = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    reward = [Fraction(0)] * n

    def sid(rho, eta):
        return rho * H + (eta - 1)

    rhos = (0,) if mode == "known" else (0, 1)
    for rho in rhos:
        for eta in range(1, H + 1):
            choice = encoder(eta)
            reward[sid(rho, eta)] = _reward(choice, rho, v, delta, r)
            if choice == "eta" or delta == 0:
                tilde = {eta: Fraction(1)}
            else:
                # Survive and reset can land on the same register value.
                tilde = {}
                tilde[eta] = tilde.get(eta, 0) + (1 - delta)
                tilde[eta0] = tilde.get(eta0, 0) + delta
            for eta_t, pt in tilde.items():
                if pt == 0:
                    continue
                for d in range(3):
                    pd = v if d == rho else (1 - v) / 2
                    eta_p = g(eta_t, d)
                    if mode == "known":
                        kernel = ((0, Fraction(1)),)
                    elif mode == "unknown":
                        kernel = ((rho, Fraction(1)),)
                    elif mode == "iid":
                        kernel = ((0, Fraction(1, 2)), (1, Fraction(1, 2)))
                    else:
                        kernel = ((rho, 1 - h), (1 - rho, h))
                    for rho_p, pr in kernel:
                        P[sid(rho, eta)][sid(rho_p, eta_p)] += pt * pd * pr
    if mode == "known":
        # Regime 1 is unreachable. Give it a self-loop so the matrix is a chain
        # on the whole index set; limits are taken from regime 0.
        for eta in range(1, H + 1):
            P[sid(1, eta)][sid(1, eta)] = Fraction(1)
            reward[sid(1, eta)] = reward[sid(0, eta)]
    for row in P:
        if sum(row) != 1:
            raise RuntimeError(f"transition row sums to {sum(row)}")
    return P, reward


def chain_value(encoder, g, H, eta0, delta, v, r, mode, h=Fraction(1, 4)):
    P, reward = build_chain(encoder, g, H, eta0, delta, v, r, mode, h)
    if mode == "known":
        dist = limit_from(P, 0 * H + (eta0 - 1))
        return sum(dist[s] * reward[s] for s in range(len(reward)))
    # Initial law: regime uniform, register at η0. Unknown-fixed must NOT be
    # collapsed to one stationary of the reducible chain.
    total = Fraction(0)
    for rho in (0, 1):
        dist = limit_from(P, rho * H + (eta0 - 1))
        total += sum(dist[s] * reward[s] for s in range(len(reward)))
    return total / 2


def g_T2(eta_tilde, d):
    if d == 0:
        return 1
    if d == 1:
        return 2
    return eta_tilde


def encoder_natural(eta):
    return 0 if eta == 1 else 1


def g_const(eta_tilde, d, eta0=1):
    return eta0


def encoder_const(offset):
    return lambda eta: offset


def _g_from_bits(index, H=2):
    def g(eta_tilde, d):
        bit = (index >> ((eta_tilde - 1) * 3 + d)) & 1
        return 2 if bit else 1
    return g


def _encoder_from_index(index):
    c1 = CHOICES[index // 5]
    c2 = CHOICES[index % 5]
    table = {1: c1, 2: c2}
    return lambda eta: table[eta]


_EQ_CACHE = {}


def best_equivariant(mode, delta, v, r, h, H=2, eta0=1):
    """Max value over cue-equivariant correct-bit encoders and outcome-blind g."""
    key = (mode, Fraction(delta), Fraction(v), Fraction(r), Fraction(h), H, eta0)
    if key in _EQ_CACHE:
        return _EQ_CACHE[key]
    best = None
    best_desc = None
    n = 0
    for ei in range(25):
        encoder = _encoder_from_index(ei)
        for gi in range(64):
            g = _g_from_bits(gi, H)
            value = chain_value(encoder, g, H, eta0, delta, v, r, mode, h)
            n += 1
            if best is None or value > best:
                best = value
                best_desc = (CHOICES[ei // 5], CHOICES[ei % 5], gi)
    _EQ_CACHE[key] = (best, best_desc, n)
    return _EQ_CACHE[key]


def config_count(encoder, g, H, eta0, delta, mode):
    """Reachable (E, I, Q) counts for a correct-bit policy, all 8 items.

    E is the number of register values with positive limiting mass.
    """
    # Use the chain support. Items and cues are redrawn every episode, so every
    # (x, c) occurs with every positively recurrent (rho, eta).
    P, _reward = build_chain(encoder, g, H, eta0, Fraction(delta), Fraction(3, 4), Fraction(3, 4), mode, Fraction(1, 4))
    dist = [Fraction(0)] * (2 * H)
    starts = [eta0 - 1] if mode == "known" else [eta0 - 1, H + (eta0 - 1)]
    for s in starts:
        lim = limit_from(P, s)
        for i, p in enumerate(lim):
            dist[i] += p
    etas = set()
    for rho in range(2):
        for eta in range(1, H + 1):
            if dist[rho * H + (eta - 1)] > 0:
                etas.add(eta)
    if mode == "known":
        etas = {eta for eta in range(1, H + 1) if dist[eta - 1] > 0}
    i_states = set()
    q_states = set()
    for eta in etas:
        choice = encoder(eta)
        for c in range(3):
            if choice in ("eta", "none"):
                durable = frozenset()
                eta_d = choice == "eta"
            else:
                durable = frozenset({(c + choice) % 3})
                eta_d = False
            for x in range(8):
                i_states.add((x, durable, eta_d, eta))
                frags = [j for j in range(3) if j not in durable]
                # eta after decay
                eta_after = (eta,) if eta_d or delta == 0 else ((eta, eta0) if eta != eta0 else (eta,))
                nmask = 1 << len(frags) if delta != 0 else 1
                for mask in range(nmask):
                    word = []
                    for j in range(3):
                        bit = (x >> (2 - j)) & 1
                        if j in durable or delta == 0:
                            word.append(bit)
                        else:
                            slot = frags.index(j)
                            word.append(-1 if (mask >> slot) & 1 else bit)
                    for ea in eta_after:
                        q_states.add((tuple(word), ea))
    e_count = len(etas)
    return e_count, len(i_states), len(q_states)


def collapse_register(encoder, H, eta0):
    """§5.7 step 3: fix the register at η0 and drop its durability payment."""
    choice = encoder(eta0)
    if choice == "eta":
        choice = "none"
    return (lambda eta, choice=choice: choice)


def zero_adapt_report(delta=Fraction(1, 2), v=Fraction(3, 4), r=Fraction(3, 4)):
    """Numeric check of the §5.7 construction at B_up = 1 and B_up = 2."""
    out = {}
    for b_up, enc in (
        (1, encoder_natural),
        (2, lambda eta: 0 if eta == 1 else 1),  # replaced below for B_up=2
    ):
        pass
    # B_up = 1, two slices. Best slice under KNOWN-FIXED is "protect c".
    known_slice = memoryless_value(1, delta, v, r, regime_known=True)
    t_const = chain_value(encoder_const(0), g_const, 2, 1, delta, v, r, "known", 0)
    # A register-using policy, then the collapsed T_const policy.
    e_full, i_full, q_full = config_count(encoder_natural, g_T2, 2, 1, delta, "switching")
    collapsed = collapse_register(encoder_natural, 2, 1)
    e_c, i_c, q_c = config_count(collapsed, g_const, 2, 1, delta, "known")
    iid_slice = memoryless_value(1, delta, v, r, regime_known=False)
    iid_const = chain_value(encoder_const(0), g_const, 2, 1, delta, v, r, "iid", Fraction(1, 2))
    iid_hist = chain_value(encoder_natural, g_T2, 2, 1, delta, v, r, "iid", Fraction(1, 2))
    # Spending the only slot on the register is a legal slice and must not beat the best slice.
    iid_eta = chain_value(lambda eta: "eta", g_T2, 2, 1, delta, v, r, "iid", Fraction(1, 2))
    out["B1"] = {
        "known_slice": known_slice,
        "T_const": t_const,
        "iid_slice": iid_slice,
        "iid_T_const": iid_const,
        "iid_history": iid_hist,
        "iid_eta_spend": iid_eta,
        "full_counts": (e_full, i_full, q_full),
        "collapsed_counts": (e_c, i_c, q_c),
        "capacity_nonincrease": max(e_c, i_c, q_c) <= max(e_full, i_full, q_full),
        "values_match": t_const == known_slice and iid_const == iid_slice and iid_hist <= iid_slice and iid_eta <= iid_slice,
    }
    # B_up = 2: protecting both elevated fields matches the regime-known bound.
    b2 = memoryless_value(2, delta, v, r, regime_known=False)
    b2_omni = omni_value(2, delta, v, r)
    out["B2"] = {"memoryless": b2, "omni": b2_omni, "equal": b2 == b2_omni}
    return out


def _finish_zero(cell, reason, value=None):
    status = "DEGENERATE" if cell["K"] == 1 else "CERT-ZERO"
    payload = {"gap": "0", "status": status, "signature": "not-evaluated", "reason": reason}
    if value is not None:
        text = fmt(value)
        payload["V_full_B"] = text
        payload["V_T_const"] = text
        payload["V_T_H"] = text
    cell["ADAPT"] = payload
    cell["cpu_ms"] = 0
    return cell


def _closed_control_value(condition, b_up, delta, v, r, k):
    """Numeric value of a zero-ADAPT control when the displayed policy fits."""
    known = condition != "IID-REGIME"
    if delta == 0 or b_up >= 3:
        return Fraction(1) if k >= 8 else None
    if b_up <= 0:
        return (1 - delta * (1 - r)) if k >= 27 else None
    if b_up == 2 and k >= 16:
        return memoryless_value(2, delta, v, r, regime_known=False)
    if b_up == 1 and k >= 26:
        return memoryless_value(1, delta, v, r, regime_known=known)
    return None


def adapt_cell(condition, b_up, delta, v, r, k, H=2, decision=True):
    delta = Fraction(delta)
    v = Fraction(v)
    r = Fraction(r)
    eta0 = 1 if H == 2 else (2 if H == 3 else 1)
    cell = {
        "id": f"adapt/{condition}/H={H}/B={b_up}/d={delta}/v={fmt(v)}/r={fmt(r)}/K={k}",
        "condition": condition,
        "H": H,
        "B_up": b_up,
        "delta": fmt(delta),
        "v": fmt(v),
        "r": fmt(r),
        "K": k,
        "decision": decision,
        "bin": None,
    }
    if H == 1 or condition in ("KNOWN-FIXED", "IID-REGIME"):
        why = (
            "ADAPT-Z1: H=1, both arms coincide"
            if H == 1
            else "ADAPT-Z2: T_const reproduces the best feasible slice and collapsing the register does not increase the configuration count"
        )
        return _finish_zero(cell, why, _closed_control_value(condition, b_up, delta, v, r, k))
    if b_up == 0:
        if k >= 27:
            return _finish_zero(
                cell,
                "B_up=0: no field can be protected, so writing the true bits is optimal for every regime and both arms match",
                1 - delta * (1 - r),
            )
        cell["ADAPT"] = {
            "gap": None,
            "status": "UNRESOLVED",
            "signature": "not-evaluated",
            "reason": f"K={k} < 27: the unprotected correct-bit policy does not fit, and the residual search was not exhausted",
        }
        cell["cpu_ms"] = 0
        return cell
    if delta == 0 or b_up >= 3:
        if k >= 8:
            cell["ADAPT"] = {
                "gap": "0",
                "status": "CERT-ZERO",
                "signature": "not-evaluated",
                "V_full_B": "1",
                "V_T_const": "1",
                "reason": "answers can be stored durably or decay is off, so every arm has value 1",
            }
        else:
            cell["ADAPT"] = {"gap": None, "status": "UNRESOLVED", "signature": "not-evaluated", "reason": f"K={k} below the 8-configuration correct-bit policy"}
        cell["cpu_ms"] = 0
        return cell
    if b_up == 2:
        if k >= 16:
            value = memoryless_value(2, delta, v, r, regime_known=False)
            bound = omni_value(2, delta, v, r)
            if value != bound:
                cell["ADAPT"] = {"gap": None, "status": "UNRESOLVED", "signature": "not-evaluated", "reason": "B_up=2 memoryless value missed the regime-known bound"}
            else:
                cell["ADAPT"] = {
                    "gap": "0",
                    "status": "CERT-ZERO",
                    "signature": "not-evaluated",
                    "V_full_B": fmt(value),
                    "V_T_const": fmt(value),
                    "V_T_H": fmt(value),
                    "reason": "protecting {c, c+1} leaves only the never-preferred field exposed, matching the regime-known bound; T_const attains it",
                }
        else:
            cell["ADAPT"] = {"gap": None, "status": "UNRESOLVED", "signature": "not-evaluated", "reason": f"K={k} < 16, the displayed B_up=2 policy is not feasible and the residual search was not exhausted"}
        cell["cpu_ms"] = 0
        return cell
    if b_up != 1:
        cell["ADAPT"] = {"gap": None, "status": "UNRESOLVED", "signature": "not-evaluated", "reason": "no certified policy at this B_up"}
        cell["cpu_ms"] = 0
        return cell
    # B_up = 1.
    if k < 26:
        cell["ADAPT"] = {
            "gap": None,
            "status": "UNRESOLVED",
            "signature": "not-evaluated",
            "reason": f"K={k} < 26: the B_up=1 correct-bit policy needs I=24 and Q=26 before the register is even varied. Residual search not exhausted.",
        }
        cell["cpu_ms"] = 0
        return cell
    import time
    t0 = time.process_time()
    if condition == "KNOWN-FIXED":
        value = memoryless_value(1, delta, v, r, regime_known=True)
        got = chain_value(encoder_const(0), g_const, H, eta0, delta, v, r, "known", 0)
        if got != value:
            cell["ADAPT"] = {"gap": None, "status": "UNRESOLVED", "signature": "not-evaluated", "reason": "KNOWN-FIXED T_const missed the best slice"}
        else:
            cell["ADAPT"] = {
                "gap": "0",
                "status": "CERT-ZERO",
                "signature": "not-evaluated",
                "V_full_B": fmt(value),
                "V_T_const": fmt(value),
                "V_T_H": fmt(value),
                "reason": "ADAPT-Z2: T_const reproduces the known-regime slice and the register is not durable",
            }
        cell["cpu_ms"] = int((time.process_time() - t0) * 1000)
        return cell
    if condition == "IID-REGIME":
        value = memoryless_value(1, delta, v, r, regime_known=False)
        got = chain_value(encoder_const(0), g_const, H, eta0, delta, v, r, "iid", Fraction(1, 2))
        if got != value:
            cell["ADAPT"] = {"gap": None, "status": "UNRESOLVED", "signature": "not-evaluated", "reason": "IID T_const missed the memoryless slice"}
        else:
            cell["ADAPT"] = {
                "gap": "0",
                "status": "CERT-ZERO",
                "signature": "not-evaluated",
                "V_full_B": fmt(value),
                "V_T_const": fmt(value),
                "V_T_H": fmt(value),
                "reason": "ADAPT-Z2: W_t is independent of η_t, so no register update beats the best slice, which T_const attains",
            }
        cell["cpu_ms"] = int((time.process_time() - t0) * 1000)
        return cell
    # Experimental.
    mode = "switching" if condition == "SWITCHING" else "unknown"
    h = Fraction(1, 4) if condition == "SWITCHING" else Fraction(0)
    v_const = chain_value(encoder_const(0), g_const, H, eta0, delta, v, r, mode, h)
    v_t2 = chain_value(encoder_natural, g_T2, H, eta0, delta, v, r, mode, h)
    # Feasibility of the T2 lower bound at this K.
    _e, i_count, q_count = config_count(encoder_natural, g_T2, H, eta0, delta, mode)
    tracker = max(v_const, v_t2)
    upper = omni_value(1, delta, v, r)
    if k < max(_e, i_count, q_count):
        cell["ADAPT"] = {
            "gap": None,
            "status": "UNRESOLVED",
            "signature": "not-evaluated",
            "V_T_const": fmt(v_const),
            "V_T_H": fmt(v_t2),
            "V_omni": fmt(upper),
            "policy_counts": {"E": _e, "I": i_count, "Q": q_count},
            "reason": f"K={k} does not fit the natural T2 policy (E,I,Q)=({_e},{i_count},{q_count}). The correct-bit equivariant class was not claimed feasible here.",
        }
        cell["cpu_ms"] = int((time.process_time() - t0) * 1000)
        return cell
    v_eq, desc, n_eval = best_equivariant(mode, delta, v, r, h, H, eta0)
    lower = max(v_eq, v_t2, v_const)
    gap_lo = lower - tracker
    gap_hi = upper - tracker
    if gap_lo > 0 and gap_hi > 0:
        status = "CERT-POS"
        reason = "every value between the equivariant lower bound and the regime-known upper bound exceeds both trackers"
    elif gap_hi == 0 and gap_lo == 0:
        status = "CERT-ZERO"
        reason = "lower and upper bounds meet at the tracker value"
    elif gap_lo == 0 and gap_hi > 0:
        status = "UNRESOLVED"
        reason = (
            "correct-bit cue-equivariant policies do not beat the better tracker, "
            "and the regime-known upper bound is strictly higher. Wrong-bit outcome "
            "signalling was not enumerated, so the optimum is not pinned."
        )
    elif gap_lo < 0:
        status = "UNRESOLVED"
        reason = "tracker exceeded the searched subclass; not a certified sign"
    else:
        status = "UNRESOLVED"
        reason = "bounds do not pin a sign"
    cell["ADAPT"] = {
        "gap": None if status == "UNRESOLVED" else fmt(gap_lo),
        "gap_interval": [fmt(gap_lo), fmt(gap_hi)],
        "status": status,
        "signature": "not-evaluated",
        "V_T_const": fmt(v_const),
        "V_T_H": fmt(v_t2),
        "V_equivariant": fmt(v_eq),
        "V_omni": fmt(upper),
        "equivariant_encoder": [str(desc[0]), str(desc[1])],
        "equivariant_g_index": desc[2],
        "n_subclass": n_eval,
        "policy_counts": {"E": _e, "I": i_count, "Q": q_count},
        "reason": reason,
    }
    cell["cpu_ms"] = int((time.process_time() - t0) * 1000)
    return cell


def iter_adapt_cells():
    """Decision cells are clean, δ=1/2, v=r=3/4. H=3 and δ=1/4 are not decision-bearing."""
    conditions_control = ("KNOWN-FIXED", "IID-REGIME")
    conditions_exp = ("SWITCHING", "UNKNOWN-FIXED")
    # H = 1 control at the primary point, one K.
    yield ("KNOWN-FIXED", 1, Fraction(1, 2), Fraction(3, 4), Fraction(3, 4), 26, 1, True)
    for condition in conditions_control + conditions_exp:
        for b_up in (0, 1, 2, 3):
            for k in (1, 16, 26, 48, 64, 125):
                yield (condition, b_up, Fraction(1, 2), Fraction(3, 4), Fraction(3, 4), k, 2, True)
    # δ = 0 unpaid control, one ample K, both experimental and the zero controls.
    for condition in conditions_control + conditions_exp:
        yield (condition, 1, Fraction(0), Fraction(3, 4), Fraction(3, 4), 26, 2, True)
