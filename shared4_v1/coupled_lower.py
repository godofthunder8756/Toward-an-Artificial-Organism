"""Bounded analytic investigation; never constructs or fits a neural network.

Run from the repository root with:
    python -B shared4_v1\\coupled_lower.py --seconds 30

The four MILPs are necessary-condition relaxations, not representations of the
complete Arm graph. Floating MILP bounds are diagnostics only. Exact arithmetic
replays the established global bound and checks each proposed LP dual.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from math import comb, prod
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "phase3b_r10_v1"))
sys.path.insert(0, str(ROOT / "r10a_v1"))

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp
from scipy.sparse import coo_matrix

from verify import COUNTS, DENOMINATOR, POLICIES, full_costs
from verify_bounds import verify as verify_prior


def rotate(n, c):
    return tuple(n[(c + j) % 4] for j in range(4))


class Model:
    def __init__(self):
        self.cost = []
        self.integer = []
        self.rows = []
        self.columns = []
        self.values = []
        self.rhs = []
        self.equal = []
        self.root_dual = []

    def variable(self, cost=0, integer=False):
        index = len(self.cost)
        self.cost.append(int(cost))
        self.integer.append(int(integer))
        return index

    def row(self, terms, rhs, equal=False, multiplier=0):
        r = len(self.rhs)
        for column, value in terms:
            if value:
                self.rows.append(r)
                self.columns.append(column)
                self.values.append(value)
        self.rhs.append(rhs)
        self.equal.append(equal)
        self.root_dual.append(multiplier)

    def finish(self):
        self.matrix = coo_matrix(
            (np.asarray(self.values, dtype=np.float64),
             (self.rows, self.columns)),
            shape=(len(self.rhs), len(self.cost)),
        ).tocsc()
        self.rhs = np.asarray(self.rhs, dtype=np.float64)
        self.equal = np.asarray(self.equal, dtype=bool)
        self.cost = np.asarray(self.cost, dtype=np.int64)
        self.integer = np.asarray(self.integer, dtype=np.uint8)
        return self


def build_relaxation(s1_positive, s3_positive, full, document):
    """Keep encoder 2-cycles and binary-head 2-cycles; relax S2 sharing.

    Per cell, S2 maps may be replaced by a pointwise-dominating retained map.
    This is safe ONLY because all shared-S2 constraints have been dropped.
    No such replacement is performed for S1 or S3.
    """
    binary = lambda positive: ((0, 0), (0, 1) if positive else (1, 0), (1, 1))
    policies = list(product(binary(s1_positive), ((0, 2), (2, 1), (2, 2)),
                            binary(s3_positive)))
    indices = [POLICIES.index(p) for p in policies]
    prior = document["variants"]["positive" if s3_positive else "negative"]
    source_indices = [POLICIES.index(tuple(tuple(t) for t in p))
                      for p in prior["policies"]]
    source = prior["certificate"]
    scale = source["scale"]
    alpha = source["nodes"][0]["alpha"]
    source_offsets = [min(row[k] for k in source_indices) for row in full]
    absolute_alpha = [source_offsets[h] * scale + 5 * alpha[h] for h in range(81)]
    prices = [sum(max(0, absolute_alpha[h] - full[h][k] * scale)
                  for h in range(81)) for k in source_indices]
    beta = max(prices)
    model = Model()
    p = {(c, m, k): model.variable(integer=True)
         for c in range(4) for m in range(8) for k in range(27)}
    x = {(h, c, m): model.variable(integer=True)
         for h in range(81) for c in range(4) for m in range(8)}
    q = {(j, c, m, bit): model.variable()
         for j in (0, 2) for c in range(4) for m in range(8) for bit in (0, 1)}
    offsets = []
    for c in range(4):
        for m in range(8):
            model.row([(p[c, m, k], 1) for k in range(27)], 1, True, -beta)
            for j in (0, 2):
                for bit in (0, 1):
                    model.row([(q[j, c, m, bit], 1)] +
                              [(p[c, m, k], -1) for k, policy in enumerate(policies)
                               if policy[j][bit] == 1], 0, True)
    for h, n in enumerate(COUNTS):
        for c in range(4):
            row = full[COUNTS.index(rotate(n, c))]
            offset = min(row[k] for k in indices)
            offsets.append(offset)
            price = absolute_alpha[COUNTS.index(rotate(n, c))] - offset * scale
            model.row([(x[h, c, m], 1) for m in range(8)], 1, True, price)
            for m in range(8):
                ys = []
                for k, policy_index in enumerate(indices):
                    y = model.variable(row[policy_index] - offset)
                    ys.append((y, 1))
                    model.row([(y, 1), (p[c, m, k], -1)], 0, False,
                              -max(0, price - (row[policy_index] - offset) * scale))
                model.row(ys + [(x[h, c, m], -1)], 0, True, price)
    encoder_cycles = 0
    for c, d in combinations(range(4), 2):
        for m, n in combinations(range(8), 2):
            z = model.variable(integer=True)
            for h in range(81):
                model.row([(x[h, c, m], 1), (x[h, d, n], 1), (z, -1)], 1)
                model.row([(x[h, c, n], 1), (x[h, d, m], 1), (z, 1)], 2)
                encoder_cycles += 2
    decoder_cycles = 0
    for j in (0, 2):
        for m, n in combinations(range(8), 2):
            z = model.variable(integer=True)
            for c in range(4):
                for bit in (0, 1):
                    model.row([(q[j, c, m, bit], 1),
                               (q[j, c, n, bit], -1), (z, -1)], 0)
                    model.row([(q[j, c, n, bit], 1),
                               (q[j, c, m, bit], -1), (z, 1)], 1)
                    decoder_cycles += 2
        for c, d in combinations(range(4), 2):
            z = model.variable(integer=True)
            for m in range(8):
                for bit in (0, 1):
                    model.row([(q[j, c, m, bit], 1),
                               (q[j, d, m, bit], -1), (z, -1)], 0)
                    model.row([(q[j, d, m, bit], 1),
                               (q[j, c, m, bit], -1), (z, 1)], 1)
                    decoder_cycles += 2
    return model.finish(), sum(offsets), {
        "s1_positive": s1_positive, "s3_positive": s3_positive,
        "encoder_cycle_inequalities": encoder_cycles,
        "binary_decoder_cycle_inequalities": decoder_cycles,
    }


def exact_dual(model, offset, scale=1_000_000):
    """Bounded-variable Lagrangian witness, checked with integer arithmetic.

    For min c.x, 0<=x<=1, Ax<=b, Ex=f, any lambda<=0 and any mu
    give b.lambda+f.mu+sum_j min(0,c_j-(A^T lambda+E^T mu)_j).
    Multipliers are algebraically lifted from the old rational root prices.
    """
    denominator = 4 * DENOMINATOR
    proposed = list(model.root_dual)
    for r in range(len(proposed)):
        if not model.equal[r]:
            proposed[r] = min(0, proposed[r])
    reduced = [int(c) * scale for c in model.cost]
    constant = offset * scale
    for r, multiplier in enumerate(proposed):
        constant += int(model.rhs[r]) * multiplier
    for r, c, coefficient in zip(model.rows, model.columns, model.values):
        reduced[c] -= int(coefficient) * proposed[r]
    correction = sum(min(0, value) for value in reduced)
    bound = Fraction(constant + correction, denominator * scale)
    proof = {
        "scale": scale,
        "nonzero_row_multipliers": [[r, v] for r, v in enumerate(proposed) if v],
        "reduced_cost_box_correction": correction,
        "exact_lower": str(bound),
    }
    return bound, proof


def replay_dual(model, offset, proof):
    scale = proof["scale"]
    assert type(scale) is int and scale > 0
    multipliers = dict(proof["nonzero_row_multipliers"])
    assert len(multipliers) == len(proof["nonzero_row_multipliers"])
    assert all(0 <= r < len(model.rhs) and isinstance(v, int)
               and (model.equal[r] or v <= 0) for r, v in multipliers.items())
    reduced = [int(c) * scale for c in model.cost]
    constant = offset * scale + sum(int(model.rhs[r]) * v
                                   for r, v in multipliers.items())
    for r, c, coefficient in zip(model.rows, model.columns, model.values):
        reduced[c] -= int(coefficient) * multipliers.get(r, 0)
    correction = sum(min(0, v) for v in reduced)
    assert correction == proof["reduced_cost_box_correction"]
    bound = Fraction(constant + correction, 4 * DENOMINATOR * scale)
    assert str(bound) == proof["exact_lower"]
    return bound


def slot_lp_diagnostic(s1, s3, full, seconds):
    """Small equivalent symmetry lift for an LP primal proposal, not a proof."""
    binary = lambda positive: ((0, 0), (0, 1) if positive else (1, 0), (1, 1))
    policies = list(product(binary(s1), ((0, 2), (2, 1), (2, 2)), binary(s3)))
    indices = [POLICIES.index(p) for p in policies]
    model = Model()
    t = [model.variable() for _ in policies]
    model.row([(v, 1) for v in t], 8, True)
    for h in range(81):
        ys = []
        for k, index in enumerate(indices):
            y = model.variable(full[h][index])
            ys.append((y, 1))
            model.row([(y, 1), (t[k], -1)], 0)
        model.row(ys, 1, True)
    model.finish()
    upper = np.ones(len(model.cost))
    upper[:27] = 8
    result = linprog(model.cost.astype(float) / DENOMINATOR,
                     A_ub=model.matrix[~model.equal], b_ub=model.rhs[~model.equal],
                     A_eq=model.matrix[model.equal], b_eq=model.rhs[model.equal],
                     bounds=list(zip(np.zeros(len(upper)), upper)), method="highs",
                     options={"time_limit": max(10.0, seconds)})
    return {"status": int(result.status), "message": result.message,
            "objective": None if result.fun is None else float(result.fun),
            "lift": "p[c,m,k]=t[k]/8; y[h,c,m,k]=assignment[rotate(h,c),k]/8; x=1/8; orientation variables=1/2",
            "certificate": False}


def run_relaxation(s1, s3, full, seconds, document):
    started = time.monotonic()
    model, offset, metadata = build_relaxation(s1, s3, full, document)
    denominator = 4 * DENOMINATOR
    objective = model.cost.astype(np.float64) / denominator
    metadata.update({"variables": len(model.cost), "rows": len(model.rhs),
                     "integer_variables": int(model.integer.sum())})
    bound, proof = exact_dual(model, offset)
    assert replay_dual(model, offset, proof) == bound
    metadata["rational_lp_certificate"] = proof
    metadata["symmetry_lift_lp_diagnostics_NOT_CERTIFICATE"] = slot_lp_diagnostic(
        s1, s3, full, seconds)
    print(f"Root rational witness checked for S1={s1}, S3={s3}: {bound}", flush=True)
    if seconds > 0:
        integer = milp(objective, integrality=model.integer,
                       bounds=Bounds(0, 1),
                       constraints=LinearConstraint(
                           model.matrix, np.where(model.equal, model.rhs, -np.inf),
                           model.rhs),
                       options={"time_limit": seconds, "mip_rel_gap": 0.0})
        metadata["milp_diagnostics_NOT_CERTIFICATE"] = {
            "status": int(integer.status), "message": integer.message,
            "objective": (None if integer.fun is None else
                          float(integer.fun + offset / denominator)),
            "dual_bound": (None if getattr(integer, "mip_dual_bound", None) is None else
                           float(integer.mip_dual_bound + offset / denominator)),
            "nodes": getattr(integer, "mip_node_count", None),
        }
    metadata["elapsed_seconds"] = round(time.monotonic() - started, 3)
    print(json.dumps({k: v for k, v in metadata.items()
                      if k != "rational_lp_certificate"}), flush=True)
    return metadata


def fixed_book_obstruction(document, full):
    """Exact, deliberately CONDITIONAL lower bound for one fixed codebook."""
    variant = document["variants"]["positive"]
    book = [tuple(tuple(p) for p in variant["policies"][k])
            for k in variant["selected"]]
    indices = [POLICIES.index(p) for p in book]
    cells = {}
    for h, n in enumerate(COUNTS):
        for c in range(4):
            costs = [full[COUNTS.index(rotate(n, c))][k] for k in indices]
            best = min(costs)
            winners = [m for m, value in enumerate(costs) if value == best]
            cells[h, c] = (costs, best, winners)
    obstructions = []
    for c, d in combinations(range(4), 2):
        switches = {}
        for h in range(81):
            a, b = cells[h, c][2], cells[h, d][2]
            if len(a) == len(b) == 1 and a[0] != b[0]:
                switches.setdefault((a[0], b[0]), []).append(h)
        for (a, b), histories in switches.items():
            if a > b:
                continue
            for h in histories:
                for g in switches.get((b, a), ()):
                    positions = ((h, c), (h, d), (g, c), (g, d))
                    regret = min(
                        min(value - cells[pos][1] for m, value in enumerate(cells[pos][0])
                            if m != cells[pos][2][0]) for pos in positions)
                    obstructions.append((regret, positions, a, b))
    # Disjoint cells allow the four-cell regret inequalities to be summed.
    used = set()
    accepted = []
    for regret, positions, a, b in sorted(obstructions, reverse=True):
        if used.isdisjoint(positions):
            used.update(positions)
            accepted.append({
                "contexts": [positions[0][1], positions[1][1]],
                "beliefs": [list(COUNTS[positions[0][0]]),
                            list(COUNTS[positions[2][0]])],
                "opposite_messages": [a, b],
                "regret_numerator": regret,
            })
    base = sum(cell[1] for cell in cells.values())
    extra = sum(v["regret_numerator"] for v in accepted)
    return {
        "scope": "ONLY the published positive codebook, identical in all contexts",
        "not_a_global_Arm_lower_bound": True,
        "independent_context_exact": str(Fraction(base, 4 * DENOMINATOR)),
        "certified_conditional_lower": str(Fraction(base + extra, 4 * DENOMINATOR)),
        "regret_sum": extra, "denominator": 4 * DENOMINATOR,
        "disjoint_crossing_witnesses": accepted,
        "available_forced_crossings": len(obstructions),
    }


def verify_s2_dominance(full):
    retained = ((0, 2), (2, 1), (2, 2))
    for policy in POLICIES:
        source = POLICIES.index(policy)
        assert any(all(row[POLICIES.index((policy[0], pair, policy[2]))] <= row[source]
                       for row in full) for pair in retained)
    return True


def published_upper_components():
    certificate = json.loads((ROOT / "r10a_v1" / "class_certificate.json").read_text())
    mapping = certificate["encoder_witness"]["mapping"]
    histories = list(product((0, 1), repeat=8))
    assert len(mapping) == len(histories) == 256
    totals = [[Fraction(0) for _ in range(3)] for _ in range(4)]
    for h, history in enumerate(histories):
        n = tuple(history[j] + history[j + 4] for j in range(4))
        probability = prod(Fraction((17, 16, 17)[count], 50) /
                           comb(2, count) for count in n)
        belief = [Fraction((1, 1, 16)[count], (17, 2, 17)[count]) for count in n]
        policy = certificate["codebook"][mapping[h]]
        for c in range(4):
            for j in range(3):
                f = (c + j) % 4
                q = belief[f]
                for bit in (0, 1):
                    one = q * Fraction(4 if bit else 1, 5)
                    zero = (1 - q) * Fraction(1 if bit else 4, 5)
                    action = policy[j][bit]
                    if j == 1 and action == 2:
                        risk = Fraction(9, 50) * (one + zero)
                    else:
                        target_one = (one if j != 2 else
                                      one * (1 - belief[(c + 3) % 4]) +
                                      zero * belief[(c + 3) % 4])
                        risk = target_one if action == 0 else one + zero - target_one
                    totals[c][j] += probability * risk
    joint = sum(sum(row) for row in totals) / 12
    assert joint == Fraction(8921732, 29296875)
    return {
        "joint_exact": str(joint),
        "mean_specialist_losses_exact":
            [str(sum(row[j] for row in totals) / 4) for j in range(3)],
        "context_joint_exact": [str(sum(row) / 3) for row in totals],
    }


def report(result):
    fixed = result["fixed_codebook_attempt"]
    cases = result["global_necessary_condition_attempt"]["cases"]
    lp_rows = "\n".join(
        f"| {'+' if v['s1_positive'] else '-'} | "
        f"{'+' if v['s3_positive'] else '-'} | "
        f"{v.get('rational_lp_certificate', {}).get('exact_lower', 'not available')} | "
        f"{v.get('milp_diagnostics_NOT_CERTIFICATE', {}).get('status', 'not run')} |"
        for v in cases)
    return f"""# Shared four-context R9: bounded coupled lower-bound investigation

**Status: UNRESOLVED. Stage A only. No neural training, gradient fitting,
optimizer sweep, or Stage B was run.**

The certified global bracket remains
`{result['certified_global_lower_exact']}` <= optimum <=
`{result['known_legal_shared_upper']['joint_exact']}`.
The prospective joint gate is `{result['gate']['joint_limit_exact']}`
(`{result['gate']['joint_limit_decimal']:.12f}`).
The bracket straddles that limit. Neither a global lower bound excluding the
gate nor a legal shared upper satisfying it was established. Failure of the
published upper to pass is **not** proof that every deployed arm fails.

## Actual graph and the legitimate relaxation

The trunk processes the eight common readings and fixed schedule without context.
The selector is `argmax_m (r_m(H) + U[m,c])`, with lowest-index ties.
Each specialist has logits `b[a,m] + d[a,c] + s[a]*local_bit`;
all three see the same word in a given context. The word may change with context.
No claim here identifies S1/S3 words across contexts.

The MILPs replace `r_m(H)` by arbitrary scores. Eighty-one belief cells suffice
for this relaxation: for fixed U and decoders, each same-belief history has
the same **four-context total** cost for a given selector pattern. Select the
least-total-cost history's pattern and copy it to all histories in that cell.
Its arbitrary-score witness remains feasible and cannot increase expected
cost. This does not assert that the RNN itself depends only on belief counts.

For S1 and S3, both global slope orientations are included, giving four cases.
Within an orientation the complete binary local-bit policy alphabet is
constants 0/1 and follow (positive) or reverse (negative). Equal slopes are
covered by the constant maps. For S2, sharing is dropped and every policy is
replaced, when necessary, by a pointwise-dominating member of
`(0,2), (2,1), (2,2)`; the code exhaustively checks that dominance using exact
population costs. This replacement is valid only because S2 sharing is dropped.
S1/S3 sharing is retained as necessary two-cycle constraints, not falsely
asserted to be a sufficient affine-head characterization.

## Correct no-cross revealed preference

For two contexts c,d and distinct words m,n, a history choosing (m,n)
implies
`U[m,c]-U[n,c] >= U[m,d]-U[n,d]`.
A history choosing (n,m) implies the reverse inequality.
If both patterns occurred, all four selection inequalities would be ties.
Lowest-index tie-breaking would then require both m<n and n<m. Thus the two
opposite switches cannot both occur. The MILPs enforce these inequalities
with binary orientation variables, without a numerical big-M.

Binary decoder logits have difference `B[m]+D[c]+S*bit`. Their threshold
tables cannot reverse the ordering of a word pair across contexts/local bits,
or the ordering of a context pair across words/local bits. Those necessary
two-cycle constraints are also enforced. Longer revealed-preference cycles,
complete affine-decoder feasibility, S2 sharing, and the RNN constraints are
not enforced; dropping them is a relaxation, never a legal upper witness.

A legal context-changing counterexample has zero trunk and state-code weights,
`U[m,c]=2` for m=c and zero otherwise. Its chosen words are 0,1,2,3, even for
one fixed H. Zero heads always choose action 0. It is a legal width56 R9 and
invalidates any assumption that one H must keep one word across all contexts.

## Attempt 1: exact obstruction for the published fixed codebook

Using the published positive codebook identically at every context, independent
context minimizers would reach `{fixed['independent_context_exact']}`.
There are {fixed['available_forced_crossings']} forced opposite-switch witnesses.
Each selected witness comprises four uniquely minimizing belief/context cells.
At least one cell must incur its exact minimum positive regret; the report
stores {len(fixed['disjoint_crossing_witnesses'])} cell-disjoint witnesses, whose
regret inequalities can be summed. The resulting rational conditional bound is
`{fixed['certified_conditional_lower']}`.

**This is not a global Arm lower bound.** Other shared decoder weights can
change the codebook across contexts, and even a different constant codebook
is outside this conditional result. No case-A decision uses it.

## Attempt 2: finite coupled necessary-condition MILP/LP

Each model has {cases[0]['variables']} bounded variables,
{cases[0]['integer_variables']} binary variables, and {cases[0]['rows']} rows.
Policy choices and word assignments are binary; assignment/policy product
variables are continuous but forced to the correct values at binary solutions.
The solver was bounded to {result['global_necessary_condition_attempt']['seconds_per_case']}
seconds per MILP case. It fits no neural parameters. An initial direct large
root-LP/MILP pipeline produced no output within 240 seconds and was stopped;
no result from that aborted run was accepted. The
replacement uses exact algebraic dual-price lifting and a small symmetric
slot-capacity LP for floating primal diagnostics; its time limit is at least
10 seconds. The slot-LP proposal lifts to the large root LP with uniform word
assignment and identical fractional policy mixtures in every context/word.

| S1 slope | S3 slope | Exact checked root-LP lower | MILP status |
|---|---|---|---|
{lp_rows}

The JSON stores sparse rational LP multipliers and the bounded-variable
reduced-cost correction. For `0<=x<=1`, the verifier computes, exactly,
`offset + b*lambda + sum min(0,c-A^T*lambda)`, with nonpositive multipliers
on upper-bound inequalities and free equality multipliers. The integer
multipliers are lifted algebraically from the old root certificate; they are
not floating MILP output. The box correction makes the verification robust
even to a merely approximate dual proposal.
Rebuilding the model and replaying those witnesses requires no solver.
The minimum over all four cases is a global lower bound for the original arm.
It did not improve the replayed prior certificate sufficiently to resolve the
gate. Floating MILP incumbent/dual bounds and 'optimal' labels are diagnostics,
**not certificates**. A relaxed incumbent is not an attainable deployed arm.

## Certificate and gate bookkeeping

The old positive/negative decoder certificates are replayed with exact integer
arithmetic, yielding `{result['certified_global_lower_exact']}`. Context symmetry
and the fixed global S3 slope sign transfer that valid one-context relaxation
bound to every context, hence their mean. This argument never constrains
the encoder's word to be context-invariant.

The previously certified shared upper is independently summed over all 256
histories using its published mapping and exact posterior costs. Mean individual
specialist losses (not their contributions divided by three) are
`{', '.join(result['known_legal_shared_upper']['mean_specialist_losses_exact'])}`.
The gate requires joint <= R10+0.01 **and strict** individual losses below
0.2, 0.18, 0.5. The published witness does not satisfy the full gate.

Run `python -B shared4_v1\\coupled_lower.py --verify-only` to replay the
persisted exact witnesses without any LP/MILP solve. Full bounded investigation:
`python -B shared4_v1\\coupled_lower.py --seconds 30`.
No inference about training learnability or Stage B follows from these results.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.seconds < 0:
        parser.error("--seconds must be nonnegative")
    output = Path(__file__).with_name("coupled_lower_result.json")
    document = json.loads((ROOT / "r10a_v1" / "decoder_bounds.json").read_text())
    prior = verify_prior(document)
    lower = min(Fraction(prior[name]["exact"]) for name in ("positive", "negative"))
    assert lower == Fraction(5159249, 29296875)
    full = full_costs()
    assert verify_s2_dominance(full)
    fixed = fixed_book_obstruction(document, full)
    upper = published_upper_components()
    if args.verify_only:
        result = json.loads(output.read_text(encoding="utf-8"))
        assert result["schema"] == 1 and result["stage"] == "A"
        assert result["training"] is False and result["status"] == "unresolved"
        assert result["fixed_codebook_attempt"] == fixed
        assert result["known_legal_shared_upper"] == upper
        cases = result["global_necessary_condition_attempt"]["cases"]
        assert len(cases) == 4
        assert {(v["s1_positive"], v["s3_positive"]) for v in cases} == set(
            product((True, False), repeat=2))
        checked = []
        for case in cases:
            model, offset, _ = build_relaxation(
                case["s1_positive"], case["s3_positive"], full, document)
            checked.append(replay_dual(model, offset, case["rational_lp_certificate"]))
        combined = max(lower, min(checked))
        assert str(combined) == result["certified_global_lower_exact"]
        limit = Fraction(5101889, 29296875) + Fraction(1, 100)
        assert str(limit) == result["gate"]["joint_limit_exact"]
        assert combined <= Fraction(result["gate"]["joint_limit_exact"])
        assert result["gate"]["StageB_authorized"] is False
        assert Fraction(upper["joint_exact"]) > limit
        print("Exact prior, fixed-codebook, four LP-dual, upper, and gate checks passed.")
        return
    cases = [run_relaxation(s1, s3, full, args.seconds, document)
             for s1, s3 in product((True, False), repeat=2)]
    duals = [Fraction(v["rational_lp_certificate"]["exact_lower"])
             for v in cases if "rational_lp_certificate" in v]
    combined = max(lower, min(duals)) if len(duals) == 4 else lower
    r10 = Fraction(5101889, 29296875)
    limit = r10 + Fraction(1, 100)
    specialist_limits = (Fraction(1, 5), Fraction(9, 50), Fraction(1, 2))
    components = [Fraction(v) for v in upper["mean_specialist_losses_exact"]]
    result = {
        "schema": 1, "status": "unresolved", "stage": "A", "training": False,
        "scope": "one shared deployed nonclone R9 Arm('R9',56), four-context mean joint population loss",
        "certified_global_lower_exact": str(combined),
        "prior_exact_certificate_replayed": prior,
        "known_legal_shared_upper": upper,
        "gate": {
            "r10_exact": str(r10), "joint_limit_exact": str(limit),
            "joint_limit_decimal": float(limit),
            "strict_specialist_limits_exact": [str(v) for v in specialist_limits],
            "known_upper_passes_joint": Fraction(upper["joint_exact"]) <= limit,
            "known_upper_passes_specialists":
                [a < b for a, b in zip(components, specialist_limits)],
            "class_excluded_by_certified_lower": combined > limit,
            "StageB_authorized": False,
            "reason": "No certified legal shared upper satisfying every prospective condition.",
        },
        "fixed_codebook_attempt": fixed,
        "global_necessary_condition_attempt": {
            "seconds_per_case": args.seconds, "cases": cases,
            "s2_pointwise_dominance_verified": True,
            "exact_complete_Arm_model": False,
        },
        "context_change_counterexample": {
            "trunk_and_state_code_weights": 0,
            "context_code_weights": "U[m,c]=2 if m=c, else 0",
            "words_for_any_history": [0, 1, 2, 3],
            "all_head_weights_and_biases": 0, "all_actions": [0, 0, 0],
        },
        "not_proved": [
            "exact joint deployed optimum", "gate attainable",
            "gate impossible", "global lower from a fixed codebook",
            "MILP floating bounds as certificates",
        ],
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
                      encoding="utf-8")
    Path(__file__).with_name("COUPLED_LOWER.md").write_text(report(result), encoding="utf-8")
    print(json.dumps({"status": result["status"], "lower": str(combined),
                      "upper": upper["joint_exact"], "gate": str(limit)}, indent=2))


if __name__ == "__main__":
    main()
