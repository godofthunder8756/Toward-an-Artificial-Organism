"""Unpaid S-DIRECT cells: SEL and ACC, exact codebook optima and signatures."""

from __future__ import annotations

from fractions import Fraction

from codebook import search_codebooks
from common import (
    DASH,
    N_WORDS,
    WORDS,
    WORD_INDEX,
    bin_ratio,
    evidence_probs,
    field_payoff,
    fmt,
    k_dec_base,
    query_probs,
    scale_rows,
    word_payoff,
)

# Adopted reading: an O-ACC flip is applicable only when the flipped field
# vector is already in the policy image. Tie products above this are not
# expanded; the signature is then UNRESOLVED for that codebook.
TIE_ENUM_LIMIT = 8192


def _sources(kind: str, a, v: Fraction, r: Fraction, cue_blind: bool):
    rows = []
    weights = []
    meta = []
    if kind == "clean":
        if cue_blind:
            for x in range(8):
                row = []
                for word in WORDS:
                    row.append(sum(word_payoff("clean", x, c, word, v, r, None) for c in range(3)) / 3)
                rows.append(row)
                weights.append(Fraction(1, 8))
                meta.append({"evidence": x, "cue": None, "weight": Fraction(1, 8)})
        else:
            for x in range(8):
                for c in range(3):
                    row = [word_payoff("clean", x, c, word, v, r, None) for word in WORDS]
                    rows.append(row)
                    weights.append(Fraction(1, 24))
                    meta.append({"evidence": x, "cue": c, "weight": Fraction(1, 24)})
    else:
        pe = evidence_probs(a)
        if cue_blind:
            for e in range(27):
                row = []
                for word in WORDS:
                    row.append(sum(word_payoff("graded", e, c, word, v, r, a) for c in range(3)) / 3)
                rows.append(row)
                weights.append(pe[e])
                meta.append({"evidence": e, "cue": None, "weight": pe[e]})
        else:
            for e in range(27):
                for c in range(3):
                    row = [word_payoff("graded", e, c, word, v, r, a) for word in WORDS]
                    rows.append(row)
                    weights.append(pe[e] * Fraction(1, 3))
                    meta.append({"evidence": e, "cue": c, "weight": pe[e] * Fraction(1, 3)})
    return rows, weights, meta


def _search(rows, weights, k: int, time_ms: int):
    if k >= 27:
        # The alphabet has 27 vectors. Reachable count cannot exceed 27.
        k = 27
    ri, wi, den = scale_rows(rows, weights)
    for row in ri:
        for value in row:
            if value < 0 or value >= 2**63:
                raise OverflowError("reward scale does not fit int64")
    for w in wi:
        if w < 0 or w >= 2**63:
            raise OverflowError("weight scale does not fit int64")
    out = search_codebooks(ri, wi, k, time_limit_ms=time_ms, collect_limit=20000)
    out["value"] = Fraction(out["best"], den * den) if out["status"] == "complete" else None
    out["den"] = den
    return out


def _flip_word(index: int, mask: int) -> int:
    word = WORDS[index]
    flipped = []
    for j in range(3):
        if word[j] == DASH:
            flipped.append(DASH)
        else:
            flipped.append(word[j] ^ ((mask >> j) & 1))
    return WORD_INDEX[tuple(flipped)]


def orbit_count(sets) -> int:
    seen = set()
    for codebook in sets:
        best = None
        for mask in range(8):
            key = tuple(sorted(_flip_word(w, mask) for w in codebook))
            if best is None or key < best:
                best = key
        seen.add(best)
    return len(seen)


def _dash_pattern(index: int):
    return tuple(int(sym == DASH) for sym in WORDS[index])


def _query_avg_derangement(c: int, v: Fraction, shift: int = 0):
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


def _payoff_dist(kind, evidence, word, dist, r, a):
    return sum(dist[j] * field_payoff(kind, evidence, j, word[j], r, a) for j in range(3))


def _argmax(row, codebook):
    best = None
    chosen = []
    for w in codebook:
        value = row[w]
        if best is None or value > best:
            best = value
            chosen = [w]
        elif value == best:
            chosen.append(w)
    return best, chosen


def sel_interval(kind, a, v, r, meta, rows, codebook):
    """Min/max O-SEL ΔV over greedy tie-breaks. Derangement kernel, uniform cue."""
    lo = Fraction(0)
    hi = Fraction(0)
    for meta_s, row in zip(meta, rows):
        if meta_s["cue"] is None:
            continue
        _, ties = _argmax(row, codebook)
        c = meta_s["cue"]
        evidence = meta_s["evidence"]
        weight = meta_s["weight"]
        base_dist = query_probs(c, v, 0)
        base = _payoff_dist(kind, evidence, WORDS[ties[0]], base_dist, r, a)
        int_dist = _query_avg_derangement(c, v, 0)
        ints = [_payoff_dist(kind, evidence, WORDS[w], int_dist, r, a) for w in ties]
        lo += weight * (min(ints) - base)
        hi += weight * (max(ints) - base)
    return lo, hi


def _acc_sources(kind, a, v, r, meta):
    """Integer (pr, p1_mass) per source and query. True mass = integer / den.

    r is carried as (numerator, denominator) for exact sign tests.
    """
    from math import lcm

    from common import ns_of, posterior_agree

    posts = None if kind == "clean" else posterior_agree(a)
    raw = []
    den = 1
    for meta_s in meta:
        if meta_s["cue"] is None:
            raw.append(None)
            continue
        qp = query_probs(meta_s["cue"], v, 0)
        if kind == "clean":
            ev = meta_s["evidence"]
            p1 = (Fraction((ev >> 2) & 1), Fraction((ev >> 1) & 1), Fraction(ev & 1))
        else:
            ns = ns_of(meta_s["evidence"])
            p1 = (posts[ns[0]], posts[ns[1]], posts[ns[2]])
        triples = []
        for q in range(3):
            pr = meta_s["weight"] * qp[q]
            p1m = pr * p1[q]
            den = lcm(den, pr.denominator, p1m.denominator)
            triples.append((pr, p1m))
        raw.append(triples)
    prepared = []
    for triples in raw:
        if triples is None:
            prepared.append(None)
            continue
        prepared.append(tuple((int(pr * den), int(p1m * den)) for pr, p1m in triples))
    return prepared, (r.numerator, r.denominator)


def _acc_one(prepared, assignment, r_pair):
    """One tie-break. Masses are integers; only the sign of each flip is required."""
    rn, rd = r_pair
    mass = [0] * (N_WORDS * 3)
    mass1 = [0] * (N_WORDS * 3)
    image = 0
    for prep, choice in zip(prepared, assignment):
        if prep is None:
            continue
        image |= 1 << choice
        base = choice * 3
        for q in range(3):
            pr, p1m = prep[q]
            mass[base + q] += pr
            mass1[base + q] += p1m
    # Dash-pattern count on the image.
    seen = 0
    npat = 0
    bitset = image
    m = 0
    while bitset:
        if bitset & 1:
            pat = _dash_pattern(m)
            key = pat[0] | (pat[1] << 1) | (pat[2] << 2)
            if (seen >> key) & 1 == 0:
                seen |= 1 << key
                npat += 1
        bitset >>= 1
        m += 1
    neg = 0
    applicable = 0
    bitset = image
    m = 0
    while bitset:
        if bitset & 1:
            word = WORDS[m]
            base = m * 3
            for q in range(3):
                p_mq = mass[base + q]
                if p_mq == 0:
                    continue
                p1 = mass1[base + q]
                flipped = (word[0], word[1], word[2])
                if word[q] == DASH:
                    # guess 1 iff p1/p_mq >= 1/2 iff 2*p1 >= p_mq
                    if 2 * p1 >= p_mq:
                        p_guess_num = p1  # / p_mq
                        guess = 1
                        # sign(p_guess - r) = sign(rd*p1 - rn*p_mq)
                        gap = rd * p_guess_num - rn * p_mq
                    else:
                        guess = 0
                        # p_guess = (p_mq - p1)/p_mq; sign = sign(rd*(p_mq-p1) - rn*p_mq)
                        gap = rd * (p_mq - p1) - rn * p_mq
                    new_word = (flipped[0], flipped[1], flipped[2])
                    if q == 0:
                        new_word = (guess, flipped[1], flipped[2])
                    elif q == 1:
                        new_word = (flipped[0], guess, flipped[2])
                    else:
                        new_word = (flipped[0], flipped[1], guess)
                else:
                    bit = word[q]
                    # p_correct = p1/p_mq if bit==1 else (p_mq-p1)/p_mq
                    # sign(r - p_correct) = sign(rn*p_mq - rd*p_correct_num)
                    p_num = p1 if bit == 1 else p_mq - p1
                    gap = rn * p_mq - rd * p_num
                    if q == 0:
                        new_word = (DASH, word[1], word[2])
                    elif q == 1:
                        new_word = (word[0], DASH, word[2])
                    else:
                        new_word = (word[0], word[1], DASH)
                idx = WORD_INDEX.get(new_word)
                if idx is not None and (image >> idx) & 1:
                    applicable += 1
                    if gap < 0:
                        neg += 1
                    elif gap > 0:
                        return {"patterns": npat, "applicable": applicable, "neg": neg, "positive_flip": True}
        bitset >>= 1
        m += 1
    return {"patterns": npat, "applicable": applicable, "neg": neg, "positive_flip": False}


def _tie_product(choice_lists):
    prod = 1
    for choices in choice_lists:
        prod *= len(choices)
        if prod > TIE_ENUM_LIMIT:
            return prod
    return prod


def _enumerate_assignments(choice_lists):
    total = _tie_product(choice_lists)
    if total > TIE_ENUM_LIMIT:
        return None
    out = []
    current = [None] * len(choice_lists)

    def rec(i):
        if i == len(choice_lists):
            out.append(list(current))
            return
        for w in choice_lists[i]:
            current[i] = w
            rec(i + 1)

    rec(0)
    return out


def signatures_for_codebooks(kind, a, v, r, meta, rows, sets):
    """Aggregate P_SEL and P_ACC over every stored optimal codebook and tie-break.

    Returns labels in {ROBUST, PERMITTED, NONE, SIG-UNDEFINED, UNRESOLVED}.
    """
    if not sets:
        return {"SEL": "UNRESOLVED", "ACC": "UNRESOLVED", "reason": "no codebook stored"}
    prepared, r_pair = _acc_sources(kind, a, v, r, meta)
    sel_flags = []  # True if ΔV<0 for every tie of this codebook, False if for none, None if mixed
    acc_flags = []
    acc_applicable_somewhere = False
    unresolved = False
    positive_flip = False
    for codebook in sets:
        lists = []
        for row in rows:
            _, ties = _argmax(row, codebook)
            lists.append(ties)
        lo, hi = sel_interval(kind, a, v, r, meta, rows, codebook)
        if hi < 0:
            sel_flags.append(True)
        elif lo >= 0:
            sel_flags.append(False)
        else:
            sel_flags.append(None)
        assignments = _enumerate_assignments(lists)
        if assignments is None:
            unresolved = True
            acc_flags.append(None)
            continue
        goods = []
        any_app = False
        for assignment in assignments:
            info = _acc_one(prepared, assignment, r_pair)
            if info.get("positive_flip"):
                positive_flip = True
            if info["applicable"]:
                any_app = True
                acc_applicable_somewhere = True
            goods.append(info["patterns"] >= 2 and info["neg"] > 0 and not info.get("positive_flip"))
        if any(goods) and all(goods):
            acc_flags.append(True)
        elif any(goods):
            acc_flags.append(None)
        else:
            acc_flags.append(False)
        if not any_app:
            # keep False; applicability is tracked globally
            pass
    def collapse(flags, applicable_exists, acc=False):
        if unresolved or any(f is None for f in flags):
            # Mixed within a codebook is PERMITTED if we know some pass and some fail.
            if any(f is None for f in flags) and not unresolved:
                return "PERMITTED"
            if unresolved:
                return "UNRESOLVED"
        if flags and all(flags):
            return "ROBUST"
        if any(flags):
            return "PERMITTED"
        if acc and not applicable_exists:
            return "SIG-UNDEFINED"
        return "NONE"

    # sel_flags None means mixed ties -> PERMITTED contribution
    if any(f is None for f in sel_flags):
        sel_label = "PERMITTED"
    elif all(sel_flags):
        sel_label = "ROBUST"
    elif any(sel_flags):
        sel_label = "PERMITTED"
    else:
        sel_label = "NONE"
    if unresolved:
        acc_label = "UNRESOLVED"
    elif any(f is None for f in acc_flags):
        acc_label = "PERMITTED"
    elif acc_flags and all(acc_flags):
        acc_label = "ROBUST"
    elif any(acc_flags):
        acc_label = "PERMITTED"
    elif not acc_applicable_somewhere:
        acc_label = "SIG-UNDEFINED"
    else:
        acc_label = "NONE"
    return {
        "SEL": sel_label,
        "ACC": acc_label,
        "positive_applicable_flip": positive_flip,
    }


def _static_best(rows, weights, k: int):
    from collections import defaultdict
    from itertools import combinations

    groups = defaultdict(list)
    for index, word in enumerate(WORDS):
        groups[tuple(int(sym == DASH) for sym in word)].append(index)
    best = None
    best_set = None
    n_opt = 0
    opt_sets = []
    for idxs in groups.values():
        size = min(k, len(idxs))
        if size <= 0:
            continue
        # Adding a codeword cannot hurt, so only subsets of size `size` can be optimal
        # inside this pattern. Across patterns the values are compared exactly.
        for subset in combinations(idxs, size):
            total = Fraction(0)
            for row, weight in zip(rows, weights):
                total += weight * max(row[w] for w in subset)
            if best is None or total > best:
                best = total
                n_opt = 1
                opt_sets = [tuple(sorted(subset))]
                best_set = opt_sets[0]
            elif total == best:
                n_opt += 1
                opt_sets.append(tuple(sorted(subset)))
    return best, n_opt, opt_sets


def evaluate_unpaid_cell(kind, a, v, r, k: int, time_ms: int = 240000):
    """One unpaid cell. Returns quantities SEL and ACC and the class records."""
    v = Fraction(v)
    r = Fraction(r)
    a = None if kind == "clean" else Fraction(a)
    k_base = k_dec_base(kind, a, r)
    ratio_bin = bin_ratio(k, k_base)
    t_full = time_ms  # caller passes the remaining full budget
    rows, weights, meta = _sources(kind, a, v, r, cue_blind=False)
    full = _search(rows, weights, k, t_full)
    # Rivals share the cell budget. They are fast relative to full; each gets
    # the protocol split, and unused time is not needed once a search completes.
    cb_rows, cb_w, cb_meta = _sources(kind, a, v, r, cue_blind=True)
    # Two rivals: cue_blind then static_access. Split the rival budget equally.
    rival_ms = max(time_ms, 1)
    blind = _search(cb_rows, cb_w, k, rival_ms)
    static_value, static_n, static_sets = _static_best(rows, weights, min(k, 27))
    record = {
        "id": f"unpaid/{kind}/a={a if a is not None else '-'}/r={r}/v={v}/K={k}",
        "kind": kind,
        "a": fmt(a) if a is not None else None,
        "r": fmt(r),
        "v": fmt(v),
        "K": k,
        "K_dec_base": k_base,
        "bin": ratio_bin,
        "storage_attributed_ACC": kind == "clean",
        "full_status": full["status"],
        "full_cpu_ms": full["cpu_ms"],
        "full_nodes": full["nodes"],
        "blind_cpu_ms": blind["cpu_ms"],
        "blind_nodes": blind["nodes"],
    }
    if full["status"] != "complete" or blind["status"] != "complete" or full["value"] is None or blind["value"] is None:
        for name in ("SEL", "ACC"):
            record[name] = {"status": "UNRESOLVED", "reason": "class search did not complete"}
        return record
    sel_gap = full["value"] - blind["value"]
    acc_gap = full["value"] - static_value
    sig = {"SEL": "UNRESOLVED", "ACC": "UNRESOLVED"}
    orbits = None
    if not full["truncated"]:
        sig = signatures_for_codebooks(kind, a, v, r, meta, rows, full["sets"])
        orbits = orbit_count(full["sets"])
    else:
        sig["reason"] = "optimum list truncated; signature not certified"

    def value_status(gap, degenerate=False):
        if degenerate:
            return "DEGENERATE"
        if gap > 0:
            return "CERT-POS"
        if gap == 0:
            return "CERT-ZERO"
        return "UNRESOLVED"

    degenerate = k == 1
    record["classes"] = {
        "full": {"value": fmt(full["value"]), "n_optima": full["n_optima"], "n_orbits": orbits, "truncated": full["truncated"]},
        "cue_blind": {"value": fmt(blind["value"]), "n_optima": blind["n_optima"], "truncated": blind["truncated"]},
        "static_access": {"value": fmt(static_value), "n_optima": static_n, "n_stored": len(static_sets)},
    }
    record["SEL"] = {
        "gap": fmt(sel_gap),
        "status": value_status(sel_gap, degenerate and sel_gap == 0),
        "signature": sig["SEL"] if sel_gap > 0 else ("SIG-UNDEFINED" if sig["SEL"] == "SIG-UNDEFINED" else "not-required"),
        "signature_raw": sig["SEL"],
    }
    record["ACC"] = {
        "gap": fmt(acc_gap),
        "status": value_status(acc_gap, degenerate and acc_gap == 0),
        "signature": sig["ACC"] if acc_gap > 0 else "not-required",
        "signature_raw": sig["ACC"],
        "positive_applicable_flip": sig.get("positive_applicable_flip", False),
    }
    if degenerate and sel_gap == 0:
        record["SEL"]["status"] = "DEGENERATE"
    if degenerate and acc_gap == 0:
        record["ACC"]["status"] = "DEGENERATE"
    # K=1 with a nonzero gap would be surprising; keep the computed status and let controls speak.
    if degenerate and sel_gap == 0:
        record["SEL"]["counts_as_zero_for_breadth"] = True
    if degenerate and acc_gap == 0:
        record["ACC"]["counts_as_zero_for_breadth"] = True
    return record


def iter_unpaid_cells():
    """Primary unpaid grid. a=5/6 is in scope; it is not marked report-only."""
    specs = [("clean", None)]
    for a in (Fraction(3, 4), Fraction(5, 6), Fraction(3, 5)):
        specs.append(("graded", a))
    for kind, a in specs:
        rs = (Fraction(3, 4),) if a == Fraction(3, 5) else (Fraction(5, 8), Fraction(3, 4))
        vs = (Fraction(1, 3), Fraction(3, 4))
        for r in rs:
            for v in vs:
                for k in (1, 2, 3, 4, 6, 8, 12, 16, 18, 24, 26, 27, 32, 48, 64, 96, 125):
                    # Null is graded (3/5, 3/4) only. One K sweep still runs: it is a control
                    # at every K, and the search is the K=1 alphabet once values are checked.
                    yield kind, a, v, r, k
