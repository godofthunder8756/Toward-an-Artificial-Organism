"""Independent checks of the scarcity certificate (stdlib unittest; pytest-compatible).

The brute-force replay below re-derives expected rewards directly from the
world definition instead of reusing ``utility_table`` or ``best_codebook``.
"""
from __future__ import annotations

import itertools
import json
import unittest
from fractions import Fraction
from pathlib import Path

from scarcity_v1 import certificate as cert

CERT_PATH = Path(__file__).with_name("certificate.json")


def direct_value(book, v, r, cue_visible=True):
    """Expected reward of a codebook with its best-response encoder."""
    total = Fraction(0)
    for x in itertools.product((0, 1), repeat=3):
        cue_sets = [(c,) for c in range(3)] if cue_visible else [tuple(range(3))]
        for cues in cue_sets:
            best = None
            for cw in book:
                u = Fraction(0)
                for c in cues:
                    for q in range(3):
                        pq = v if q == c else (1 - v) / 2
                        a = cw[q]
                        u += pq * (r if a == 2 else Fraction(int(a == x[q]))) / len(cues)
                best = u if best is None else max(best, u)
            total += best / 8 / len(cue_sets)
    return total


def brute_force(policy, k, v, r):
    words = list(itertools.product((0, 1, 2), repeat=3))
    if policy == "no_opt":
        words = [w for w in words if 2 not in w]
    best = Fraction(-1)
    for book in itertools.combinations(words, k):
        if policy == "static" and len({tuple(a == 2 for a in w) for w in book}) > 1:
            continue
        best = max(best, direct_value(book, v, r, cue_visible=(policy != "cue_blind")))
    return best


def cells():
    return json.loads(CERT_PATH.read_text())["cells"]


def ex(d):
    return Fraction(d["exact"])


class BranchAndBoundReplay(unittest.TestCase):
    def test_matches_brute_force_small_capacity(self):
        for v in cert.GRID_V:
            for r in cert.GRID_R:
                for k in (1, 2, 3):
                    for policy in cert.CLASSES:
                        with self.subTest(v=v, r=r, k=k, policy=policy):
                            self.assertEqual(cert.solve(policy, k, v, r)[0],
                                             brute_force(policy, k, v, r))

    def test_class_ordering(self):
        for cell in cells():
            val = {p: ex(cell["value"][p]) for p in cert.CLASSES}
            self.assertLessEqual(val["no_opt"], val["static"])
            self.assertLessEqual(val["static"], val["full"])
            self.assertLessEqual(val["cue_blind"], val["full"])


class StoredCertificate(unittest.TestCase):
    def test_grid_is_complete(self):
        got = {(c["v"]["exact"], c["r"]["exact"], c["K"]) for c in cells()}
        want = {(f"{v.numerator}/{v.denominator}", f"{r.numerator}/{r.denominator}", k)
                for v in cert.GRID_V for r in cert.GRID_R for k in cert.GRID_K}
        self.assertEqual(got, want)

    def test_stored_codebook_attains_stored_value(self):
        sym = {"0": 0, "1": 1, "-": 2}
        for cell in cells():
            book = [tuple(sym[ch] for ch in w) for w in cell["optimal_codebook"]]
            self.assertLessEqual(len(book), cell["K"])
            self.assertEqual(direct_value(book, ex(cell["v"]), ex(cell["r"])),
                             ex(cell["value"]["full"]))

    def test_stored_values_replay_small_capacity(self):
        for cell in cells():
            if cell["K"] <= 2:
                v, r = ex(cell["v"]), ex(cell["r"])
                for policy in cert.CLASSES:
                    self.assertEqual(ex(cell["value"][policy]),
                                     brute_force(policy, cell["K"], v, r))


class CollapseAndScarcity(unittest.TestCase):
    def test_sufficiency_collapse(self):
        """K = 8 stores every item: all agent-referent quantities vanish."""
        full_book = list(itertools.product((0, 1), repeat=3))
        for v in cert.GRID_V:
            for r in cert.GRID_R:
                self.assertEqual(direct_value(full_book, v, r), 1)
                self.assertEqual(direct_value(full_book, v, r, cue_visible=False), 1)
        for cell in cells():
            if cell["K"] == cert.SUFFICIENT_K:
                self.assertEqual(ex(cell["access_value"]), 0)
                self.assertEqual(ex(cell["selection_value"]), 0)
                self.assertEqual(ex(cell["diagnostics"]["self_induced_uncertainty_mass"]), 0)
                self.assertEqual(ex(cell["diagnostics"]["opt_out_mass"]), 0)

    def test_scarcity_forces_self_induced_uncertainty(self):
        """Pigeonhole: K < 8 merges two item vectors under one cue."""
        for cell in cells():
            if cell["K"] < cert.SUFFICIENT_K:
                self.assertGreater(
                    ex(cell["diagnostics"]["self_induced_uncertainty_mass"]), 0)

    def test_uninformative_cue_has_no_selection_value(self):
        for cell in cells():
            if ex(cell["v"]) == Fraction(1, 3):
                self.assertEqual(ex(cell["selection_value"]), 0)

    def test_break_even_opt_out_has_no_access_value(self):
        for cell in cells():
            if ex(cell["r"]) == Fraction(1, 2):
                self.assertEqual(ex(cell["access_value"]), 0)

    def test_headline_counts(self):
        sc = [c for c in cells() if c["K"] < cert.SUFFICIENT_K]
        access = [c for c in sc if ex(c["access_value"]) > 0]
        select = [c for c in sc if ex(c["selection_value"]) > 0]
        both = [c for c in access if ex(c["selection_value"]) > 0]
        self.assertEqual((len(sc), len(access), len(select), len(both)), (63, 14, 24, 2))
        self.assertEqual(max(ex(c["access_value"]) for c in sc), Fraction(1, 24))
        self.assertEqual(max(ex(c["selection_value"]) for c in sc), Fraction(1, 8))
        self.assertTrue(all(c["K"] not in (1, 2, 4) for c in access))

    def test_no_partial_access_signature_in_clean_world(self):
        """Opted-out trials carry no residual content (forced choice = 1/2)."""
        for cell in cells():
            fc = cell["diagnostics"]["forced_choice_accuracy_on_opted_trials"]
            if fc is not None:
                self.assertEqual(ex(fc), Fraction(1, 2))


if __name__ == "__main__":
    unittest.main()
