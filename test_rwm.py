"""Unit tests for the RWM design package (python -m unittest -v test_rwm)."""
import math
import random
import unittest
from fractions import Fraction
from itertools import product

import numpy as np

from rwm import world as W
from rwm.gate import _has_free_directed_cut, structural_checks
from rwm.integration import causal_density, phi_s, uniform_weight
from rwm.neural import RWMNet, macro_skeleton, rollout
from rwm.primitives import (AND, COPY, MAJ, MUX, OR, TABLE, THRESHOLD, XOR, Gate, Network,
                            strongly_connected_components)
from rwm.topology import (control_chain, control_copy_loop, control_two_islands, rivals,
                          rival_detached_monitor, rwm8, unroll, _net)


# ---------------------------------------------------------------------------
# Independent brute-force replay of Phi_s (dict loops, no numpy, no caching)
# ---------------------------------------------------------------------------

def _ref_phi(net, full_state, ext):
    m = net.n
    nodes = net.nodes
    cur = net.state_bits(full_state)

    def p_node(j, past_bits, cut_from):
        ins = net.inputs[nodes[j]]
        free = [k for k, src in enumerate(ins) if src in cut_from]
        tot = 0.0
        for combo in product((0, 1), repeat=len(free)):
            vals = []
            for k, src in enumerate(ins):
                if k in free:
                    vals.append(combo[free.index(k)])
                elif src in ext:
                    vals.append(ext[src])
                else:
                    vals.append(past_bits[nodes.index(src)])
            tot += net.gates[nodes[j]].p1(vals)
        return tot / (2 ** len(free))

    states = list(product((0, 1), repeat=m))

    def T(past, fut, A=frozenset(), B=frozenset()):
        pr = 1.0
        for j in range(m):
            cf = A if nodes[j] in B else frozenset()
            p = p_node(j, past, cf)
            pr *= p if fut[j] else 1 - p
        return pr

    q = {f: sum(T(p, f) for p in states) / len(states) for f in states}
    pe = {f: T(cur, f) for f in states}
    col = {p: T(p, cur) for p in states}
    z = sum(col.values())
    if z == 0:
        return 0.0
    pc = {p: col[p] / z for p in states}
    iie = {f: pe[f] * math.log2(pe[f] / q[f]) for f in states if pe[f] > 0}
    iic = {p: pc[p] * math.log2(col[p] / q[cur]) for p in states if pc[p] > 0}
    be, bc = max(iie.values()), max(iic.values())
    effs = [f for f, v in iie.items() if v >= be - 1e-12]
    caus = [p for p, v in iic.items() if v >= bc - 1e-12]
    parts = []
    for mask in range(1, 2 ** m - 1):
        A = frozenset(nodes[k] for k in range(m) if mask >> k & 1)
        parts.append((A, frozenset(nodes) - A))
    best = 0.0
    for sc in caus:
        for se in effs:
            mip = None
            for A, B in parts:
                phe = max(0.0, pe[se] * math.log2(pe[se] / T(cur, se, A, B)))
                phc = max(0.0, pc[sc] * math.log2(col[sc] / T(sc, cur, A, B)))
                v = min(phe, phc)
                key = v / (len(A) * len(B))
                if mip is None or key < mip[0] - 1e-12:
                    mip = (key, v)
            best = max(best, mip[1])
    return best


def _random_net(rng, n=3, noisy=False):
    names = [f"n{k}" for k in range(n)]
    spec = []
    for k in range(n):
        ins = tuple(rng.sample(names, rng.choice([1, 2])))
        table = tuple(float(rng.random() < 0.5) for _ in range(2 ** len(ins)))
        if noisy:
            table = tuple(0.1 + 0.8 * v for v in table)
        spec.append((names[k], ins, Gate("RND", len(ins), table)))
    return _net("rnd", spec, external=[])


class TestGates(unittest.TestCase):
    def test_truth_tables(self):
        self.assertEqual([MAJ(3).p1(b) for b in product((0, 1), repeat=3)],
                         [0, 0, 0, 1, 0, 1, 1, 1])
        self.assertEqual([XOR(2).p1(b) for b in product((0, 1), repeat=2)], [0, 1, 1, 0])
        self.assertEqual(MUX().p1((1, 0, 1)), 1.0)
        self.assertEqual(MUX().p1((0, 0, 1)), 0.0)
        g = THRESHOLD([2, 1, 1, 1], 2, negated=[False, False, True, False])
        self.assertEqual(g.p1((1, 0, 1, 0)), 1.0)   # 2*I alone ignites
        self.assertEqual(g.p1((0, 1, 1, 0)), 0.0)   # E with C=1 does not
        self.assertEqual(g.p1((0, 1, 0, 0)), 1.0)   # E + NOT C does
        self.assertAlmostEqual(COPY(0.25).p1((1,)), 0.75)

    def test_network_validation(self):
        with self.assertRaises(ValueError):
            Network("bad", ["a"], {"a": ("zz",)}, {"a": COPY()})
        with self.assertRaises(ValueError):
            Network("bad", ["a"], {"a": ("a", "a")}, {"a": COPY()})

    def test_scc(self):
        comps = strongly_connected_components(list("abc"), [("a", "b"), ("b", "a"), ("b", "c")])
        self.assertEqual(sorted(map(sorted, comps)), [["a", "b"], ["c"]])


class TestIntegration(unittest.TestCase):
    def test_copy_loop_analytic(self):
        for s in range(4):
            r = phi_s(control_copy_loop(), s, {})
            self.assertAlmostEqual(r["phi"], 1.0, places=12)

    def test_feedforward_and_reducible_are_zero(self):
        for s in range(8):
            self.assertEqual(phi_s(control_chain(), s, {})["phi"], 0.0)
        for s in range(16):
            self.assertEqual(phi_s(control_two_islands(), s, {})["phi"], 0.0)

    def test_independent_replay_random(self):
        rng = random.Random(1234)
        for trial in range(25):
            net = _random_net(rng, 3, noisy=(trial % 3 == 0))
            for s in range(8):
                a = phi_s(net, s, {})["phi"]
                b = _ref_phi(net, s, {})
                self.assertAlmostEqual(a, b, places=10, msg=f"trial {trial} state {s}")

    def test_independent_replay_rwm8_states(self):
        net = rwm8()
        rng = random.Random(7)
        for _ in range(6):
            s = rng.randrange(256)
            ext = {"oR": rng.randrange(2), "oH": rng.randrange(2)}
            self.assertAlmostEqual(phi_s(net, s, ext)["phi"], _ref_phi(net, s, ext), places=10)

    def test_causal_density_analytic(self):
        cd = causal_density(control_copy_loop(), uniform_weight(control_copy_loop()))
        self.assertAlmostEqual(cd["cd_weighted"], 1.0)
        spec = [("a", ("a", "b"), XOR(2)), ("b", ("b",), COPY())]
        net = _net("x", spec, external=[])
        cmi = causal_density(net, uniform_weight(net))["cmi"]
        self.assertAlmostEqual(cmi["b->a"], 1.0)
        self.assertAlmostEqual(cmi["a->b"], 0.0)
        spec = [("a", ("a", "b"), AND(2)), ("b", ("b",), COPY())]
        net = _net("y", spec, external=[])
        cmi = causal_density(net, uniform_weight(net))["cmi"]
        # I(b; a' | a) for AND under uniform inputs: 1/2 * h(1/2) = 1/2 bit
        self.assertAlmostEqual(cmi["b->a"], 0.5)

    def test_unrolled_is_equivalent_and_severable(self):
        net = rwm8()
        un = unroll(net, 2)
        self.assertTrue(_has_free_directed_cut(un))
        rng = random.Random(3)
        for _ in range(200):
            s0 = rng.randrange(256)
            seq = [(rng.randrange(2), rng.randrange(2)) for _ in range(2)]
            vals = {f"{nd}@0": b for nd, b in zip(net.nodes, net.state_bits(s0))}
            for t, (r_, h_) in enumerate(seq):
                vals[f"oR@{t}"], vals[f"oH@{t}"] = r_, h_
            for t in (1, 2):
                for nd in net.nodes:
                    vals[f"{nd}@{t}"] = int(un.node_p1(f"{nd}@{t}", vals))
            s = s0
            for r_, h_ in seq:
                s = net.step_det(s, {"oR": r_, "oH": h_})
            self.assertEqual([vals[f"{nd}@2"] for nd in net.nodes], list(net.state_bits(s)))


class TestTopology(unittest.TestCase):
    def test_rwm8_structure(self):
        s = structural_checks(rwm8())
        for key in ("T1_single_scc", "T2_bottleneck", "T3_broadcast",
                    "T4_monitor_higher_order", "T5_no_vestigial_declared_edges"):
            self.assertTrue(s[key], key)

    def test_detached_monitor_is_severable(self):
        s = structural_checks(rival_detached_monitor())
        self.assertFalse(s["T1_single_scc"])
        self.assertFalse(s["T4_monitor_higher_order"])

    def test_rivals_build(self):
        for r in rivals():
            self.assertGreaterEqual(r.n, 6)


class TestWorld(unittest.TestCase):
    def test_fraction_solver(self):
        A = [[Fraction(2), Fraction(1)], [Fraction(1), Fraction(3)]]
        x = W.solve_fraction(A, [Fraction(3), Fraction(5)])
        self.assertEqual(x, [Fraction(4, 5), Fraction(7, 5)])

    def test_dark_room_lifetime(self):
        dark = {s: 0 for s in W.LIVE}
        self.assertEqual(W.expected_lifetime(dark)[(0, W.H_MAX)], W.H_MAX)
        self.assertEqual(W.evaluate_policy(dark, 1, 0)[(0, W.H_MAX)], 0)

    def test_policy_value_matches_float(self):
        pol = {s: 1 for s in W.LIVE}
        V = W.evaluate_policy(pol, 1, 1)
        states, idx, P = W.policy_chain(pol)
        Pm = np.array([[float(v) for v in row] for row in P])
        c = np.array([float(W.step_cost(*(s if s != W.DEAD else (0, 0)), 1, 1)) for s in states])
        v = np.linalg.solve(np.eye(len(states)) - 0.9 * Pm, c)
        for s in states:
            self.assertAlmostEqual(float(V[s]), v[idx[s]], places=9)

    def test_closed_loop_stationary(self):
        r = W.closed_loop_summary(rwm8())
        self.assertAlmostEqual(sum(r["_pi"].values()), 1.0)
        self.assertGreater(r["mean_lifetime_steps"], W.H_MAX)


class TestNeural(unittest.TestCase):
    def test_population_edges_equal_discrete_topology(self):
        net = RWMNet()
        self.assertEqual(sorted(net.population_edges()), sorted(rwm8().effective_edges()))

    def test_no_training_surface(self):
        net = RWMNet()
        for attr in ("fit", "train", "backward", "optimizer"):
            self.assertFalse(hasattr(net, attr))

    def test_rollout_deterministic(self):
        a = rollout(RWMNet(), 300, np.random.default_rng(5))
        b = rollout(RWMNet(), 300, np.random.default_rng(5))
        self.assertEqual(a, b)

    def test_macro_skeleton_edges_subset(self):
        m = macro_skeleton(RWMNet())
        self.assertTrue(set(m.effective_edges()) <= set(rwm8().effective_edges()))


if __name__ == "__main__":
    unittest.main()
