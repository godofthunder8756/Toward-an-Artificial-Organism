"""Exact bounded-access world: when does a self-referring access variable exist?

Analytic card, no learner, no neural model, no organism simulation.

World (frozen before enumeration; every grid cell is reported):

* ``N_ITEMS = 3`` independent uniform binary world items ``x``, observed
  cleanly and completely at encoding time.  A full-history ideal observer is
  therefore certain about every item: its first-order confidence is always 1.
* A goal cue ``c`` (uniform over items) is seen at encoding time.  The later
  query ``q`` equals ``c`` with probability ``v`` and each other item with
  probability ``(1 - v) / 2``.  ``v = 1/3`` makes the cue uninformative.
* The agent writes ONE of ``K`` memory states, then sees ``q`` and must answer
  0/1 (reward 1 if correct, 0 if wrong) or opt out (sure reward ``r``).

``K = 8`` holds the complete sufficient statistic (all item values).  ``K < 8``
is the scarcity regime: memory is a strict Blackwell garbling of the history.

A memory state is identified with its *codeword*: the action it takes for each
possible query (27 possibilities).  Given a codebook, the optimal encoder picks,
for each input, the codeword with the highest expected reward, so the global
optimum over all deterministic encoder/decoder pairs is an exact facility-
location problem.  It is solved by exhaustive branch-and-bound in integer
arithmetic and independently replayed by plain enumeration in the tests.

Policy classes compared at identical capacity ``K``:

* ``full``      unrestricted codebook (the candidate organization).
* ``static``    whether to opt out may depend on the query only, never on the
                memory state (the agent knows its fixed policy, but holds no
                state-dependent representation of its own access).
* ``no_opt``    never opts out: wagering by the full-history (ideal-observer)
                confidence, which is always certain in this world.
* ``cue_blind`` the encoder may not read the goal cue (fixed allocation; no
                goal-dependent selection).

Claim ceiling: exact optimal-policy facts for this finite decision problem.
Not a learning, neural, organism, metacognition or consciousness result.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

N_ITEMS = 3
ITEMS = tuple(range(N_ITEMS))
VALUES = tuple(itertools.product((0, 1), repeat=N_ITEMS))
OPT = 2  # action code for opting out; 0/1 answer the item value
CODEWORDS = tuple(itertools.product((0, 1, OPT), repeat=N_ITEMS))
SUFFICIENT_K = len(VALUES)

# Frozen prospective grid.  Every cell is computed and reported; none is
# selected after the fact.
GRID_V = (Fraction(1, 3), Fraction(1, 2), Fraction(3, 4))
GRID_R = (Fraction(1, 2), Fraction(5, 8), Fraction(3, 4))
GRID_K = tuple(range(1, SUFFICIENT_K + 1))
CLASSES = ("full", "static", "no_opt", "cue_blind")


def query_prob(q: int, c: int, v: Fraction) -> Fraction:
    return v if q == c else (1 - v) / (N_ITEMS - 1)


def reward(action: int, value: int, r: Fraction) -> Fraction:
    if action == OPT:
        return r
    return Fraction(int(action == value))


def inputs(cue_visible: bool) -> list[tuple]:
    """Encoder inputs.  A cue-blind encoder sees only the item values."""
    if cue_visible:
        return [(x, c) for x in VALUES for c in ITEMS]
    return [(x,) for x in VALUES]


def utility_table(v: Fraction, r: Fraction, cue_visible: bool):
    """Exact expected reward of each codeword for each encoder input.

    Returns (rows, denominator): rows[i][j] is an integer numerator for input i
    and codeword j, so that sums are exact integers over a common denominator.
    """
    fr = []
    for inp in inputs(cue_visible):
        x = inp[0]
        cues = (inp[1],) if cue_visible else ITEMS
        p_cue = Fraction(1) if cue_visible else Fraction(1, N_ITEMS)
        p_inp = Fraction(1, len(VALUES)) * (Fraction(1, N_ITEMS) if cue_visible else 1)
        row = []
        for cw in CODEWORDS:
            u = Fraction(0)
            for c in cues:
                for q in ITEMS:
                    u += p_inp * p_cue * query_prob(q, c, v) * reward(cw[q], x[q], r)
            row.append(u)
        fr.append(row)
    den = 1
    for row in fr:
        for u in row:
            den = den * u.denominator // math.gcd(den, u.denominator)
    rows = [[int(u * den) for u in row] for row in fr]
    return rows, den


def allowed_codebooks(policy: str):
    """Yield codeword-index pools; the optimum is the max over all pools."""
    if policy in ("full", "cue_blind"):
        yield list(range(len(CODEWORDS)))
    elif policy == "no_opt":
        yield [j for j, cw in enumerate(CODEWORDS) if OPT not in cw]
    elif policy == "static":
        for mask in itertools.product((False, True), repeat=N_ITEMS):
            yield [j for j, cw in enumerate(CODEWORDS)
                   if all((cw[q] == OPT) == mask[q] for q in ITEMS)]
    else:
        raise ValueError(policy)


def best_codebook(rows: list[list[int]], pool: list[int], k: int):
    """Exact max over codebooks of size <= k drawn from pool (branch-and-bound).

    Value of a codebook = sum over inputs of the best codeword's utility.
    Duplicated codewords never help, so subsets suffice.  Ties keep the
    lexicographically first codebook in pool order.
    """
    k = min(k, len(pool))
    n = len(rows)
    # Order the pool by stand-alone value to find strong incumbents early.
    pool = sorted(pool, key=lambda j: (-sum(row[j] for row in rows), j))
    # suffix_best[t][i] = best utility for input i among pool[t:]
    suffix_best = [[0] * n for _ in range(len(pool) + 1)]
    for t in range(len(pool) - 1, -1, -1):
        j = pool[t]
        suffix_best[t] = [max(suffix_best[t + 1][i], rows[i][j]) for i in range(n)]
    best = [-1, ()]

    def dfs(start: int, chosen: tuple, cur: list[int]) -> None:
        val = sum(cur) if chosen else -1
        if val > best[0]:
            best[0], best[1] = val, chosen
        if len(chosen) == k or start == len(pool):
            return
        bound = sum(max(c, s) for c, s in zip(cur, suffix_best[start])) if chosen \
            else sum(suffix_best[start])
        if bound <= best[0]:
            return
        for t in range(start, len(pool)):
            j = pool[t]
            nxt = [max(c, row[j]) for c, row in zip(cur, rows)] if chosen \
                else [row[j] for row in rows]
            dfs(t + 1, chosen + (j,), nxt)

    dfs(0, (), [0] * n)
    return best[0], tuple(sorted(best[1]))


def solve(policy: str, k: int, v: Fraction, r: Fraction):
    rows, den = utility_table(v, r, cue_visible=(policy != "cue_blind"))
    best_val, best_book = -1, ()
    for pool in allowed_codebooks(policy):
        val, book = best_codebook(rows, pool, k)
        if val > best_val:
            best_val, best_book = val, book
    return Fraction(best_val, den), best_book


def encoder(book: tuple, v: Fraction, r: Fraction):
    """Optimal cue-visible encoder for a codebook (first index wins ties)."""
    rows, _ = utility_table(v, r, cue_visible=True)
    enc = {}
    for inp, row in zip(inputs(True), rows):
        enc[inp] = max(book, key=lambda j: (row[j], -j))
    return enc


def access_diagnostics(book: tuple, v: Fraction, r: Fraction) -> dict:
    """Agent-referent quantities of an optimal full-class policy.

    The ideal observer is certain of every item, so any posterior uncertainty
    held by the bounded agent is produced by its own garbling, not the world.
    """
    enc = encoder(book, v, r)
    # joint mass over (state, query, queried value)
    mass: dict[tuple, Fraction] = {}
    for (x, c), j in enc.items():
        p_inp = Fraction(1, len(VALUES) * N_ITEMS)
        for q in ITEMS:
            key = (j, q, x[q])
            mass[key] = mass.get(key, Fraction(0)) + p_inp * query_prob(q, c, v)
    self_uncertain = Fraction(0)   # mass where 0 < P(x_q = 1 | m, q) < 1
    opted = Fraction(0)
    opted_forced_correct = Fraction(0)
    for j in set(enc.values()):
        for q in ITEMS:
            p0 = mass.get((j, q, 0), Fraction(0))
            p1 = mass.get((j, q, 1), Fraction(0))
            if p0 + p1 == 0:
                continue
            if p0 and p1:
                self_uncertain += p0 + p1
            if CODEWORDS[j][q] == OPT:
                opted += p0 + p1
                opted_forced_correct += max(p0, p1)
    per_query_opt_varies = [
        len({CODEWORDS[j][q] == OPT for j in set(enc.values())}) > 1 for q in ITEMS]
    return {
        "states_used": len(set(enc.values())),
        "self_induced_uncertainty_mass": self_uncertain,
        "opt_out_mass": opted,
        "forced_choice_accuracy_on_opted_trials":
            (opted_forced_correct / opted) if opted else None,
        "opt_out_depends_on_state_for_query": per_query_opt_varies,
    }


def fmt(x):
    if isinstance(x, Fraction):
        return {"exact": f"{x.numerator}/{x.denominator}", "float": float(x)}
    if isinstance(x, dict):
        return {k: fmt(val) for k, val in x.items()}
    if isinstance(x, (list, tuple)):
        return [fmt(val) for val in x]
    return x


def certificate() -> dict:
    cells = []
    for v in GRID_V:
        for r in GRID_R:
            for k in GRID_K:
                vals, books = {}, {}
                for policy in CLASSES:
                    vals[policy], books[policy] = solve(policy, k, v, r)
                cells.append({
                    "v": v, "r": r, "K": k,
                    "value": vals,
                    "access_value": vals["full"] - vals["static"],
                    "ideal_observer_wager_loss": vals["full"] - vals["no_opt"],
                    "selection_value": vals["full"] - vals["cue_blind"],
                    "optimal_codebook": ["".join("01-"[a] for a in CODEWORDS[j])
                                         for j in books["full"]],
                    "diagnostics": access_diagnostics(books["full"], v, r),
                })
    return {
        "card": "SCARCITY_v1 analytic admission certificate",
        "claim_ceiling": "exact optimal-policy facts for one finite decision "
                         "problem; no learning, neural, organism or "
                         "consciousness inference",
        "world": {"items": N_ITEMS, "sufficient_K": SUFFICIENT_K,
                  "codewords": len(CODEWORDS),
                  "reward": "correct 1, wrong 0, opt-out r",
                  "codeword_notation": "per-query action, '-' = opt out"},
        "grid": {"v": GRID_V, "r": GRID_R, "K": GRID_K},
        "cells": cells,
    }


def main(argv: list[str]) -> int:
    out = Path(argv[1]) if len(argv) > 1 else Path(__file__).with_name("certificate.json")
    cert = certificate()
    out.write_text(json.dumps(fmt(cert), indent=1) + "\n")
    print(f"{'v':>5} {'r':>5} {'K':>2} {'V_full':>9} {'access':>9} "
          f"{'select':>9} {'self_unc':>9} {'opt_mass':>9} {'fc_acc':>7}  book")
    for cell in cert["cells"]:
        d = cell["diagnostics"]
        fc = d["forced_choice_accuracy_on_opted_trials"]
        print(f"{str(cell['v']):>5} {str(cell['r']):>5} {cell['K']:>2} "
              f"{float(cell['value']['full']):9.5f} {float(cell['access_value']):9.5f} "
              f"{float(cell['selection_value']):9.5f} "
              f"{float(d['self_induced_uncertainty_mass']):9.5f} "
              f"{float(d['opt_out_mass']):9.5f} "
              f"{'   -   ' if fc is None else f'{float(fc):7.4f}'}  "
              f"{' '.join(cell['optimal_codebook'])}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
