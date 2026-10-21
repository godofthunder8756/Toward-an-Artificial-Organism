"""Shared exact-arithmetic objects for the scarcity_v2 certificate.

Word index is lexicographic on symbols (0, 1, dash), dash last.
Field 0 is the high bit of a clean item index.
"""

from __future__ import annotations

from fractions import Fraction
from math import lcm

DASH = -1
SYMBOLS = (0, 1, DASH)
WORDS = tuple((a, b, c) for a in SYMBOLS for b in SYMBOLS for c in SYMBOLS)
N_WORDS = 27
assert len(WORDS) == N_WORDS
WORD_INDEX = {w: i for i, w in enumerate(WORDS)}

K_GRID = (1, 2, 3, 4, 6, 8, 12, 16, 18, 24, 26, 27, 32, 48, 64, 96, 125)


def F(n, d=1) -> Fraction:
    return Fraction(n, d)


def bits_of(x: int) -> tuple[int, int, int]:
    return ((x >> 2) & 1, (x >> 1) & 1, x & 1)


def ns_of(e: int) -> tuple[int, int, int]:
    return ((e // 9) % 3, (e // 3) % 3, e % 3)


def query_probs(c: int, v: Fraction, shift: int = 0) -> tuple[Fraction, Fraction, Fraction]:
    """Single-consumer kernel. shift=0 is consumer A (prefers c); shift=1 is B."""
    pref = (c + shift) % 3
    other = (1 - v) / 2
    return tuple(v if j == pref else other for j in range(3))  # type: ignore[return-value]


def marginal_query(v: Fraction, pi=(F(1, 3), F(1, 3), F(1, 3))) -> tuple[Fraction, Fraction, Fraction]:
    acc = [F(0), F(0), F(0)]
    for c in range(3):
        qp = query_probs(c, v)
        for j in range(3):
            acc[j] += pi[c] * qp[j]
    return tuple(acc)  # type: ignore[return-value]


def posterior_agree(a: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    """P(x=1 | n) for n=0,1,2. Two independent looks, each correct with probability a."""
    den = a * a + (1 - a) * (1 - a)
    return ((1 - a) * (1 - a) / den, F(1, 2), a * a / den)


def look_prob(n: int, bit: int, a: Fraction) -> Fraction:
    p1 = a if bit == 1 else (1 - a)
    if n == 0:
        return (1 - p1) ** 2
    if n == 2:
        return p1 ** 2
    return 2 * p1 * (1 - p1)


def evidence_probs(a: Fraction) -> list[Fraction]:
    out = []
    for e in range(27):
        ns = ns_of(e)
        pe = F(0)
        for x in range(8):
            bx = bits_of(x)
            pe += F(1, 8) * look_prob(ns[0], bx[0], a) * look_prob(ns[1], bx[1], a) * look_prob(ns[2], bx[2], a)
        out.append(pe)
    return out


def field_payoff(kind: str, evidence: int, field: int, action: int, r: Fraction, a: Fraction | None) -> Fraction:
    """Expected reward of one field action given the evidence, conditional on that field being queried."""
    if kind == "clean":
        bit = bits_of(evidence)[field]
        if action == DASH:
            return r
        return F(1) if action == bit else F(0)
    post = posterior_agree(a)[ns_of(evidence)[field]]
    if action == DASH:
        return r
    return post if action == 1 else (1 - post)


def word_payoff(kind, evidence, cue, word, v, r, a, shift=0) -> Fraction:
    qp = query_probs(cue, v, shift)
    return sum(qp[j] * field_payoff(kind, evidence, j, word[j], r, a) for j in range(3))


def scale_rows(rows: list[list[Fraction]], weights: list[Fraction]):
    """Return integer rewards, integer weights, and denominator.

    Objective sum weight_int[s] * reward_int[s][w] equals true expectation * den**2,
    with weight_int = weight * den and reward_int = reward * den.
    """
    den = 1
    for row in rows:
        for value in row:
            den = lcm(den, value.denominator)
    for w in weights:
        den = lcm(den, w.denominator)
    ri = [[int(value * den) for value in row] for row in rows]
    wi = [int(w * den) for w in weights]
    return ri, wi, den


def fmt(x: Fraction | None) -> str:
    if x is None:
        return "UNRESOLVED"
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def bin_ratio(k: int, k_base: int) -> str | None:
    """SEL/ACC bin of K / K_dec,base. None when the ratio is not in (0, 1)."""
    if k_base <= 0 or k <= 0:
        return None
    ratio = Fraction(k, k_base)
    if ratio <= 0:
        return None
    if ratio <= Fraction(1, 4):
        return "(0,1/4]"
    if ratio <= Fraction(1, 2):
        return "(1/4,1/2]"
    if ratio < 1:
        return "(1/2,1)"
    return None


def k_dec_base(kind: str, a: Fraction | None, r: Fraction) -> int:
    if kind == "clean":
        return 8
    # Graded null: every answer has confidence 9/13 < 3/4 when (a,r)=(3/5,3/4).
    if a == Fraction(3, 5) and r == Fraction(3, 4):
        return 1
    return 27
