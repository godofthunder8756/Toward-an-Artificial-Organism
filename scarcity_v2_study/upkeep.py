"""Clean S-DIRECT upkeep certificate: closed forms, counts, withdrawals.

Below K_suff the per-input upper bound is infeasible. Those cells stay
UNRESOLVED; the search of arbitrary I-configurations is not claimed complete.
"""

from __future__ import annotations

from fractions import Fraction

from common import DASH, bits_of, evidence_probs, fmt, posterior_agree

# partner bit 0/1 -> fragile field, for each cue.
# partner is the other durable field.
_FRAGILE = {
    # c: (fragile if partner is the lower other index, fragile if partner is the higher)
    0: (2, 1),  # partners 1 then 2 -> fragile 2 (pair 01) or 1 (pair 02)
    1: (2, 0),  # partners 0 then 2 -> fragile 2 (pair 01) or 0 (pair 12)
    2: (1, 0),  # partners 0 then 1 -> fragile 1 (pair 02) or 0 (pair 12)
}


def _proj_table():
    table = [[0] * 8 for _ in range(3)]
    for f in range(3):
        for x in range(8):
            b = bits_of(x)
            others = [b[j] for j in range(3) if j != f]
            table[f][x] = others[0] * 2 + others[1]
    return table


PROJ = _proj_table()


def patterns_of_choice(choice: int):
    """choice in 0..7, bit c is the partner alternative at cue c. Returns the set of fragile fields."""
    frags = set()
    for c in range(3):
        bit = (choice >> c) & 1
        frags.add(_FRAGILE[c][bit])
    return frags


def q_count(users) -> int:
    """users[f] is a bitmask of items that use fragile-field pattern f."""
    q = 8  # intact copies of every item
    for f in range(3):
        mask = users[f]
        if mask == 0:
            continue
        projs = set()
        bit = mask
        x = 0
        while bit:
            if bit & 1:
                projs.add(PROJ[f][x])
            bit >>= 1
            x += 1
        q += len(projs)
    return q


_BUP2_CACHE: dict[int, tuple[int, None]] = {}


def enumerate_bup2(k: int):
    """Count value-optimal B_up=2 policies with I<=k and Q<=k.

    Each item has 8 partner-choices. A choice is value-optimal for every
    (item, cue). Feasibility is the configuration cap.
    """
    if k >= 24:
        # I <= 24 and Q <= 20 for every partner policy, so the cap does not bind.
        return 1 << 24, None
    if k in _BUP2_CACHE:
        return _BUP2_CACHE[k]
    count = 0
    # users bitmasks, mutated along the recursion
    users = [0, 0, 0]

    def rec(x: int, i_count: int):
        nonlocal count
        if i_count > k:
            return
        if x == 8:
            if i_count <= k and q_count(users) <= k:
                count += 1
            return
        for choice in range(8):
            frags = patterns_of_choice(choice)
            added = []
            for f in frags:
                bit = 1 << x
                if users[f] & bit:
                    continue
                users[f] |= bit
                added.append(f)
            rec(x + 1, i_count + len(added))
            for f in added:
                users[f] ^= 1 << x

    rec(0, 0)
    _BUP2_CACHE[k] = (count, None)
    return _BUP2_CACHE[k]


def burnside_bup2(k: int, raw_count: int) -> int:
    """Orbits under item bit-label flips. At K>=24 every policy is feasible."""
    if k >= 24:
        # (2^24 + 7 * 2^12) / 8
        return ((1 << 24) + 7 * (1 << 12)) // 8
    fixed = raw_count  # identity
    # Nonzero masks: policies constant on pairs {x, x xor m}. 12 free bits.
    for mask in range(1, 8):
        pairs = []
        seen = set()
        for x in range(8):
            if x in seen:
                continue
            pairs.append(x)
            seen.add(x)
            seen.add(x ^ mask)
        # 4 pairs, each a choice in 0..7
        n_fixed = 0
        for code in range(1 << 12):
            users = [0, 0, 0]
            i_count = 0
            ok = True
            for p_i, x in enumerate(pairs):
                choice = (code >> (3 * p_i)) & 7
                for y in (x, x ^ mask):
                    frags = patterns_of_choice(choice)
                    before = i_count
                    for f in frags:
                        bit = 1 << y
                        if not (users[f] & bit):
                            users[f] |= bit
                            i_count += 1
                    if i_count - before != len(frags) and False:
                        pass
            if i_count <= k and q_count(users) <= k:
                n_fixed += 1
        fixed += n_fixed
    return fixed // 8


def phase_counts_displayed_bup2():
    """Protocol display: {0,1} for c in {0,1}, {0,2} for c=2, all items."""
    i_states = set()
    q_states = set()
    for x in range(8):
        b = bits_of(x)
        for c, durable in ((0, (1, 1, 0)), (1, (1, 1, 0)), (2, (1, 0, 1))):
            # durable flag 1 means D, 0 means F. All fields answered.
            i_states.add((b, durable))
            fragile = [j for j in range(3) if durable[j] == 0]
            # both survival and decay of the single fragile field
            for decay in (0, 1):
                word = []
                for j in range(3):
                    if durable[j] == 0 and decay:
                        word.append(DASH)
                    else:
                        word.append(b[j])
                q_states.add(tuple(word))
    return len(i_states), len(q_states)


def phase_counts_bup1():
    i_states = set()
    q_states = set()
    for x in range(8):
        b = bits_of(x)
        for c in range(3):
            durable = tuple(1 if j == c else 0 for j in range(3))
            i_states.add((b, durable))
            # two fragile fields, every decay subset
            frags = [j for j in range(3) if j != c]
            for mask in range(4):
                word = []
                for j in range(3):
                    if j == c:
                        word.append(b[j])
                    else:
                        slot = frags.index(j)
                        word.append(DASH if (mask >> slot) & 1 else b[j])
                q_states.add(tuple(word))
    return len(i_states), len(q_states)


def phase_counts_fixed(b_up: int, field: int = 0):
    """All-answer fixed D-set. b_up=1 protects `field`; b_up=2 protects all but `field`."""
    i_states = set()
    q_states = set()
    if b_up == 1:
        durable_fields = {field}
    elif b_up == 2:
        durable_fields = {j for j in range(3) if j != field}
    else:
        raise ValueError(b_up)
    for x in range(8):
        b = bits_of(x)
        durable = tuple(1 if j in durable_fields else 0 for j in range(3))
        i_states.add((b, durable))
        frags = [j for j in range(3) if j not in durable_fields]
        for mask in range(1 << len(frags)):
            word = []
            for j in range(3):
                if j in durable_fields:
                    word.append(b[j])
                else:
                    slot = frags.index(j)
                    word.append(DASH if (mask >> slot) & 1 else b[j])
            q_states.add(tuple(word))
    return len(i_states), len(q_states)


def full_value(b_up: int, delta: Fraction, v: Fraction, r: Fraction) -> Fraction:
    """Per-input upper bound. Achievable at the K_suff stated by the protocol."""
    if b_up <= 0:
        return 1 - delta * (1 - r)
    if b_up >= 3:
        return Fraction(1)
    if b_up == 1:
        p_frag = 1 - v
    else:
        p_frag = (1 - v) / 2
    return 1 - delta * (1 - r) * p_frag


def fixed_value(b_up: int, delta: Fraction, r: Fraction) -> Fraction:
    if b_up <= 0:
        return 1 - delta * (1 - r)
    if b_up >= 3:
        return Fraction(1)
    p_frag = Fraction(2, 3) if b_up == 1 else Fraction(1, 3)
    return 1 - delta * (1 - r) * p_frag


def k_suff(b_up: int) -> int | None:
    if b_up == 1:
        return 26
    if b_up == 2:
        return 16
    return 0


def withdrawal_cued(delta: Fraction, v: Fraction, r: Fraction) -> Fraction:
    """On every episode, downgrade the cued field. p=1, field always durable."""
    return -delta * v * (1 - r)


def withdrawal_fixed_field(delta: Fraction, v: Fraction, r: Fraction) -> Fraction:
    """Downgrade fixed field j=0 on the episodes where it is durable (c=0)."""
    # P(c=0)=1/3, P(q=0|c=0)=v, p=1.
    return -delta * Fraction(1, 3) * v * (1 - r)


def graded_ample_upk(a=Fraction(3, 4), r=Fraction(3, 4), delta=Fraction(1, 2), v=Fraction(1, 3)):
    """Direct sum of the §5.4 cell. Returns UPK, UPK_cue, UPK_ev, and the two values."""
    post = posterior_agree(a)
    pe = evidence_probs(a)
    # Per field, optimal action value and whether it is worth protecting.
    # Query is uniform, so each field is symmetric. Gain from making an answered
    # field durable: delta * (conf - r) * P(q=j), and only if conf > r.
    gain_unit = []  # for each evidence, list of per-field durability gains at P(q)=1, times later by 1/3
    base = Fraction(0)
    for e in range(27):
        ns = ((e // 9) % 3, (e // 3) % 3, e % 3)
        field_gain = []
        instant = Fraction(0)
        for n in ns:
            p = post[n]
            conf = p if p >= Fraction(1, 2) else 1 - p
            # best fragile-or-dash action
            best = r if conf <= r else (1 - delta) * conf + delta * r
            instant += best
            if conf > r:
                # durable would give `conf` instead of the fragile mixture
                field_gain.append(conf - ((1 - delta) * conf + delta * r))
            else:
                field_gain.append(Fraction(0))
        # v=1/3 => P(q=j)=1/3, and the three fields share the query
        base += pe[e] * (instant / 3)
        gain_unit.append(field_gain)
    # full protects the single best field (B_up=1). fixed protects field 0.
    v_full = base
    v_fixed = base
    for e in range(27):
        gains = gain_unit[e]
        # multiply by P(q=j)=1/3 already? field_gain is the reward difference conditional
        # on the field being queried. E[difference] = P(q=j) * field_gain = field_gain/3.
        v_full += pe[e] * (max(gains) / 3)
        v_fixed += pe[e] * (gains[0] / 3)
    upk = v_full - v_fixed
    # Cue-blind upkeep can protect argmax field of the evidence, which is what full does
    # when the cue is uninformative. So UPK_cue = 0 and UPK_ev = UPK.
    return {
        "V_full": v_full,
        "V_fixed": v_fixed,
        "UPK": upk,
        "UPK_cue": Fraction(0),
        "UPK_ev": upk,
    }


def upkeep_cell(b_up: int, delta: Fraction, v: Fraction, r: Fraction, k: int, decision: bool):
    """One clean uniform-cue UPK cell."""
    delta = Fraction(delta)
    v = Fraction(v)
    r = Fraction(r)
    cell = {
        "id": f"upk/clean/B={b_up}/d={delta}/v={v}/r={r}/K={k}",
        "decision": decision,
        "B_up": b_up,
        "delta": fmt(delta),
        "v": fmt(v),
        "r": fmt(r),
        "K": k,
        "bin": str(b_up) if b_up in (1, 2) else None,
    }
    # Controls that do not need the ample policy.
    if b_up == 0 or b_up >= 3 or delta == 0:
        cell["quantities"] = {
            "UPK": {"gap": "0", "status": "CERT-ZERO", "signature": "not-required", "n_optima": None},
            "UPK_cue": {"gap": "0", "status": "CERT-ZERO", "signature": "not-required"},
            "UPK_ev": {"gap": "0", "status": "CERT-ZERO", "signature": "not-required"},
        }
        cell["reason"] = "proved zero control (no durable distinction, or every field can be durable)"
        cell["cpu_ms"] = 0
        return cell
    need = k_suff(b_up)
    upper_full = full_value(b_up, delta, v, r)
    upper_fixed = fixed_value(b_up, delta, r)
    # v=1/3: fixed attains the per-input upper bound once its own count fits.
    z4 = 18 if b_up == 1 else 12
    if v == Fraction(1, 3) and k >= z4:
        cell["quantities"] = {
            "UPK": {"gap": "0", "status": "CERT-ZERO", "signature": "not-required", "n_optima": None},
            "UPK_cue": {"gap": "0", "status": "CERT-ZERO", "signature": "not-required"},
            "UPK_ev": {"gap": "0", "status": "CERT-ZERO", "signature": "not-required"},
        }
        cell["reason"] = f"UPK-Z4/Z4' : fixed attains the upper bound at K>={z4}"
        cell["V_full"] = fmt(upper_fixed)
        cell["V_fixed"] = fmt(upper_fixed)
        cell["cpu_ms"] = 0
        return cell
    if k >= need and v > Fraction(1, 3):
        # Family of partner / cued policies attains the upper bound and every
        # member has the cued-field withdrawal strictly negative.
        if b_up == 1:
            n_opt = 1
            n_orbits = 1
        else:
            n_opt, _ = enumerate_bup2(k)
            n_orbits = burnside_bup2(k, n_opt)
        gap = upper_full - upper_fixed
        # cue-blind upkeep matches fixed: P(q=j)=1/3 under uniform c independent of x.
        wdraw = withdrawal_cued(delta, v, r)
        sig = "ROBUST" if wdraw < 0 else "NONE"
        cell["quantities"] = {
            "UPK": {
                "gap": fmt(gap),
                "status": "CERT-POS" if gap > 0 else "CERT-ZERO",
                "signature": sig if gap > 0 else "not-required",
                "n_optima": n_opt,
                "n_orbits": n_orbits,
            },
            "UPK_cue": {
                "gap": fmt(gap),
                "status": "CERT-POS" if gap > 0 else "CERT-ZERO",
                "signature": sig if gap > 0 else "not-required",
                "n_optima": n_opt,
            },
            "UPK_ev": {"gap": "0", "status": "CERT-ZERO", "signature": "not-required"},
        }
        cell["V_full"] = fmt(upper_full)
        cell["V_fixed"] = fmt(upper_fixed)
        cell["V_cue_blind_upkeep"] = fmt(upper_fixed)
        cell["withdrawal_cued"] = fmt(wdraw)
        cell["reason"] = f"ample clean policy feasible at K>={need}; every optimum protects a cued pair/field"
        cell["cpu_ms"] = 0
        return cell
    reason = (
        f"K={k} < K_suff={need}: the per-input upper bound is infeasible "
        "(I/Q of every value-achieving policy exceeds K). The residual "
        "I-configuration search was not exhausted inside the cell budget."
    )
    # UPK-C0 is proved for every K: an uninformative cue makes the best
    # cue-blind upkeep rule a selection among full's own outputs.
    if v == Fraction(1, 3):
        cue = {"gap": "0", "status": "CERT-ZERO", "signature": "not-required", "reason": "UPK-C0"}
    else:
        cue = {"gap": None, "status": "UNRESOLVED", "signature": "UNRESOLVED", "reason": reason}
    cell["quantities"] = {
        "UPK": {
            "gap": None,
            "status": "UNRESOLVED",
            "signature": "UNRESOLVED",
            "reason": reason,
        },
        "UPK_cue": cue,
        "UPK_ev": {"gap": None, "status": "UNRESOLVED", "signature": "UNRESOLVED", "reason": reason},
    }
    cell["upper_full"] = fmt(upper_full)
    cell["upper_fixed"] = fmt(upper_fixed)
    cell["cpu_ms"] = 0
    return cell
