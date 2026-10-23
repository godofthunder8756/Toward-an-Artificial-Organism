"""S-MSG route certificate.

Decoder enumeration is exact: for a fixed decoder the sender's optimum is an
independent argmax at each (evidence, cue), and the two consumers separate.
L at or above K_dec,base is the §5.6 constructive zero (the optimal action
profile is a function of evidence only) and is not enumerated.
"""

from __future__ import annotations

from fractions import Fraction
from math import lcm

from common import DASH, bits_of, evidence_probs, field_payoff, fmt, k_dec_base, query_probs

ACTIONS = (0, 1, DASH)


def _scaled(value: Fraction, den: int) -> int:
    scaled = value * den
    if scaled.denominator != 1:
        raise RuntimeError(f"scale is not integral: {value} * {den}")
    return int(scaled)


def _deranged_query(c: int, v: Fraction, shift: int):
    """Uniform average of the query laws at c' ≠ c."""
    acc = [Fraction(0), Fraction(0), Fraction(0)]
    n = 0
    for c2 in range(3):
        if c2 == c:
            continue
        qp = query_probs(c2, v, shift)
        for j in range(3):
            acc[j] += qp[j]
        n += 1
    return tuple(x / n for x in acc)


def _prep(kind: str, a, v: Fraction, r: Fraction, shift: int):
    """Integer tables. A decoder score equals sum_q qp_i[q] * pay_i[action]."""
    v = Fraction(v)
    r = Fraction(r)
    cues = []
    deranged = []
    for c in range(3):
        cues.append(query_probs(c, v, shift))
        deranged.append(_deranged_query(c, v, shift))
    if kind == "clean":
        states = []
        den = 1
        den = lcm(den, 24)
        for c in range(3):
            for q in range(3):
                den = lcm(den, cues[c][q].denominator)
                den = lcm(den, deranged[c][q].denominator)
                den = lcm(den, r.denominator)
        pay = []  # pay[state][q][action_index]
        weights = []
        for x in range(8):
            bits = bits_of(x)
            for c in range(3):
                table = []
                for q in range(3):
                    row = []
                    for action in ACTIONS:
                        if action == DASH:
                            value = r
                        elif action == bits[q]:
                            value = Fraction(1)
                        else:
                            value = Fraction(0)
                        scaled = value * den
                        if scaled.denominator != 1:
                            raise RuntimeError("clean payoff scale is not integral")
                        row.append(int(scaled))
                    table.append(row)
                pay.append(table)
                w = Fraction(1, 24) * den
                if w.denominator != 1:
                    raise RuntimeError("clean weight scale is not integral")
                weights.append(int(w))
                states.append((x, c))
        qp = []
        qd = []
        for c in range(3):
            qp.append([_scaled(cues[c][q], den) for q in range(3)])
            qd.append([_scaled(deranged[c][q], den) for q in range(3)])
            if sum(qp[-1]) != den or sum(qd[-1]) != den:
                raise RuntimeError("query rows must sum to the scale")
        return {
            "pay": pay,
            "weights": weights,
            "qp": qp,  # indexed by cue, and state cue is states[s][1]
            "qd": qd,
            "cues": [st[1] for st in states],
            "den": den,
            # weight ~ den, conditional score ~ den^2, product ~ den^3.
            "scale": den ** 3,
        }
    pe = evidence_probs(a)
    den = 1
    for e in range(27):
        den = lcm(den, pe[e].denominator)
        for q in range(3):
            for action in ACTIONS:
                den = lcm(den, field_payoff("graded", e, q, action, r, a).denominator)
    for c in range(3):
        for q in range(3):
            den = lcm(den, cues[c][q].denominator)
            den = lcm(den, deranged[c][q].denominator)
    pay = []
    weights = []
    cues_of = []
    for e in range(27):
        row = [[_scaled(field_payoff("graded", e, q, action, r, a), den) for action in ACTIONS] for q in range(3)]
        w = _scaled(pe[e], den)
        for c in range(3):
            pay.append(row)
            weights.append(w)
            cues_of.append(c)
    qp = [[_scaled(cues[c][q], den) for q in range(3)] for c in range(3)]
    qd = [[_scaled(deranged[c][q], den) for q in range(3)] for c in range(3)]
    for c in range(3):
        if sum(qp[c]) != den or sum(qd[c]) != den:
            raise RuntimeError("query rows must sum to the scale")
    # Each (e,c) weight is pe[e]/3. The extra factor 3 sits in the denominator.
    return {
        "pay": pay,
        "weights": weights,
        "qp": qp,
        "qd": qd,
        "cues": cues_of,
        "den": den,
        "scale": den * den * den * 3,
    }


def _score(pay_row, qp, actions_for_mu):
    total = 0
    for q in range(3):
        total += qp[q] * pay_row[q][actions_for_mu[q]]
    return total


def _enumerate(prep, L: int):
    """Return best full value, best static value, and per-optimal-decoder tie intervals.

    Values are Fractions. Tie intervals are (lo, hi) of the O-ROUTE numerator
    before dividing by the consumer mean: intervened minus normal, in Fraction.
    """
    pay = prep["pay"]
    weights = prep["weights"]
    qp = prep["qp"]
    qd = prep["qd"]
    cues = prep["cues"]
    n = len(pay)
    # decoder: L messages × 3 queries, action index 0,1,2
    n_dec = 3 ** (3 * L)
    best_full = None
    best_static = None
    full_opts = []
    static_opts = []

    def consider(dec_id, full_int, static_int, full_lo, full_hi):
        nonlocal best_full, best_static
        if best_full is None or full_int > best_full:
            best_full = full_int
            full_opts.clear()
            full_opts.append((dec_id, full_lo, full_hi))
        elif full_int == best_full:
            full_opts.append((dec_id, full_lo, full_hi))
        if best_static is None or static_int > best_static:
            best_static = static_int
            static_opts.clear()
            static_opts.append(dec_id)
        elif static_int == best_static:
            static_opts.append(dec_id)

    # Mixed radix over action indices.
    actions = [0] * (3 * L)
    for dec_id in range(n_dec):
        # decode id into actions
        x = dec_id
        for i in range(3 * L):
            actions[i] = x % 3
            x //= 3
        # per message, action index per query
        msgs = [actions[3 * mu: 3 * mu + 3] for mu in range(L)]
        full_int = 0
        full_lo = 0
        full_hi = 0
        # static accumulates, per evidence, the best message's cue-sum
        # states are grouped as consecutive cues 0,1,2 for each evidence
        static_int = 0
        static_iv = 0
        s = 0
        while s < n:
            # one evidence, three cues, for the static choice
            cue_scores = []  # [mu][local cue]
            for local in range(3):
                row = pay[s + local]
                c = cues[s + local]
                per_mu = []
                for mu in range(L):
                    per_mu.append(_score(row, qp[c], msgs[mu]))
                cue_scores.append(per_mu)
                best = max(per_mu)
                w = weights[s + local]
                full_int += w * best
                # tie interval for the intervention
                lo = None
                hi = None
                for mu in range(L):
                    if per_mu[mu] != best:
                        continue
                    iv = _score(row, qd[c], msgs[mu])
                    if lo is None or iv < lo:
                        lo = iv
                    if hi is None or iv > hi:
                        hi = iv
                full_lo += w * lo
                full_hi += w * hi
            # static: one message for all three cues. The deranged score of that
            # same message is accumulated so the O-ROUTE identity can be checked.
            best_static_here = None
            best_static_iv = None
            for mu in range(L):
                total = 0
                iv = 0
                for local in range(3):
                    row = pay[s + local]
                    c = cues[s + local]
                    total += weights[s + local] * cue_scores[local][mu]
                    iv += weights[s + local] * _score(row, qd[c], msgs[mu])
                if best_static_here is None or total > best_static_here:
                    best_static_here = total
                    best_static_iv = iv
            static_int += best_static_here
            static_iv += best_static_iv
            s += 3
        if static_iv != static_int:
            raise RuntimeError("static_route O-ROUTE identity failed for a decoder")
        consider(dec_id, full_int, static_int, full_lo, full_hi)
    scale = prep["scale"]
    def to_frac(value):
        return Fraction(value, scale)
    return {
        "V_full": to_frac(best_full),
        "V_static": to_frac(best_static),
        "n_full": len(full_opts),
        "n_static": len(static_opts),
        "full_intervals": [(to_frac(lo) - to_frac(best_full), to_frac(hi) - to_frac(best_full), to_frac(best_full)) for _i, lo, hi in full_opts],
    }


def _signature(intervals_a, intervals_b):
    """intervals are (Δlo, Δhi) per optimal decoder, already Fractions of value."""
    kinds = []
    for lo_a, hi_a in intervals_a:
        for lo_b, hi_b in intervals_b:
            lo = (lo_a + lo_b) / 2
            hi = (hi_a + hi_b) / 2
            if hi < 0:
                kinds.append("all")
            elif lo >= 0:
                kinds.append("none")
            else:
                kinds.append("mix")
    if not kinds:
        return "UNRESOLVED"
    if all(k == "all" for k in kinds):
        return "ROBUST"
    if all(k == "none" for k in kinds):
        return "NONE"
    return "PERMITTED"


def _sufficient_value(kind, a, v, r):
    """Both classes send the evidence and answer the per-query optimum. ROUTE = 0."""
    v = Fraction(v)
    r = Fraction(r)
    if kind == "clean":
        return Fraction(1)
    if a == Fraction(3, 5) and r == Fraction(3, 4):
        return r
    pe = evidence_probs(a)
    # Marginal query is uniform for every v, by cue symmetry. Use v's kernel averaged.
    total = Fraction(0)
    for e in range(27):
        for c in range(3):
            qp = query_probs(c, v, 0)
            for q in range(3):
                best = max(field_payoff("graded", e, q, action, r, a) for action in ACTIONS)
                total += pe[e] * Fraction(1, 3) * qp[q] * best
    return total


def route_cell(kind: str, a, v, r, L: int):
    v = Fraction(v)
    r = Fraction(r)
    a_f = None if kind == "clean" else Fraction(a)
    base = k_dec_base(kind, a_f, r)
    cell = {
        "id": f"route/{kind}/a={fmt(a_f) if a_f is not None else '-'}/r={fmt(r)}/v={fmt(v)}/L={L}",
        "kind": kind,
        "a": None if a_f is None else fmt(a_f),
        "r": fmt(r),
        "v": fmt(v),
        "L": L,
        "bin": str(L) if L in (2, 3) else None,
        "K_dec_base": base,
    }
    if L >= base:
        value = _sufficient_value(kind, a_f, v, r)
        cell["classes"] = {
            "full_route": {"value": fmt(value), "n_optima": None, "note": "constructive, not enumerated"},
            "static_route": {"value": fmt(value), "n_optima": None, "note": "constructive, not enumerated"},
        }
        cell["ROUTE"] = {"gap": "0", "status": "CERT-ZERO", "signature": "not-required"}
        cell["reason"] = "ROUTE-Z3: L >= K_dec,base, both classes send the evidence-only action profile"
        cell["cpu_ms"] = 0
        return cell
    import time
    t0 = time.process_time()
    preps = [_prep(kind, a_f, v, r, shift) for shift in (0, 1)]
    parts = [_enumerate(preps[shift], L) for shift in (0, 1)]
    cpu_ms = int((time.process_time() - t0) * 1000)
    v_full = (parts[0]["V_full"] + parts[1]["V_full"]) / 2
    v_static = (parts[0]["V_static"] + parts[1]["V_static"]) / 2
    gap = v_full - v_static
    intervals = []
    for part in parts:
        intervals.append([(lo, hi) for lo, hi, _vf in part["full_intervals"]])
    sig = _signature(intervals[0], intervals[1]) if gap > 0 else "not-required"
    if gap > 0:
        status = "CERT-POS"
    elif gap == 0:
        status = "CERT-ZERO"
    else:
        status = "UNRESOLVED"
    cell["classes"] = {
        "full_route": {
            "value": fmt(v_full),
            "per_consumer": [fmt(parts[0]["V_full"]), fmt(parts[1]["V_full"])],
            "n_optima_decoders": [parts[0]["n_full"], parts[1]["n_full"]],
            "n_optima": parts[0]["n_full"] * parts[1]["n_full"],
        },
        "static_route": {
            "value": fmt(v_static),
            "per_consumer": [fmt(parts[0]["V_static"]), fmt(parts[1]["V_static"])],
            "n_optima_decoders": [parts[0]["n_static"], parts[1]["n_static"]],
            "n_optima": parts[0]["n_static"] * parts[1]["n_static"],
        },
    }
    cell["ROUTE"] = {"gap": fmt(gap), "status": status, "signature": sig, "signature_raw": _signature(intervals[0], intervals[1])}
    cell["cpu_ms"] = cpu_ms
    if gap < 0:
        cell["ROUTE"]["reason"] = "static_route exceeded full_route; treated as unresolved rather than a negative certificate"
    return cell


def iter_route_cells():
    specs = [("clean", None)]
    for a in (Fraction(3, 4), Fraction(5, 6), Fraction(3, 5)):
        specs.append(("graded", a))
    for kind, a in specs:
        base = 8 if kind == "clean" else (1 if a == Fraction(3, 5) else 27)
        rs = (Fraction(3, 4),) if a == Fraction(3, 5) else (Fraction(5, 8), Fraction(3, 4))
        for r in rs:
            for v in (Fraction(1, 3), Fraction(3, 4)):
                levels = [1, 2, 3]
                if base not in levels:
                    levels.append(base)
                for L in levels:
                    yield kind, a, v, r, L
