"""AC50 tests: the frozen record, its declared gates, and its registered source hashes."""
import hashlib
import json
import pathlib
import unittest
import numpy as np
import ac50_heterogeneous as a50
import ac38_variance as ac38

ROOT = pathlib.Path('ac50_results_v1')


def load():
    rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines() if l.strip()]
    res = json.loads((ROOT / 'results.json').read_text())
    snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
    return rows, res, snap


class TestProtocolWasRegisteredFirst(unittest.TestCase):
    def test_declared_sources_equal_the_hashed_set(self):
        declared = a50.preflight()
        self.assertEqual(sorted(set(declared)), sorted(set(a50.SOURCES)))
        self.assertEqual(len(set(declared)), 6)

    def test_sources_unchanged_since_registration(self):
        _, _, snap = load()
        changed = [n for n, sha in snap.items()
                   if not pathlib.Path(n).exists()
                   or hashlib.sha256(pathlib.Path(n).read_bytes()).hexdigest() != sha]
        self.assertEqual(changed, [], f'edited after registration: {changed}')

    def test_result_dir_frozen(self):
        self.assertTrue(ROOT.is_dir())
        self.assertTrue((ROOT / 'rows.jsonl').exists())


class TestFrozenGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.res, cls.snap = load()
        cls.gates = cls.res['gates']

    def test_all_nine_gates_pass(self):
        self.assertEqual(len(self.gates), 9)
        self.assertTrue(all(self.gates.values()), self.gates)

    def test_contrast_resolves_at_the_power_floor(self):
        learner = [r['learner_both']['post'] for r in self.rows]
        no_rel = [r['no_release']['post'] for r in self.rows]
        d = [a - b for a, b in zip(learner, no_rel)]
        t = ac38.sign_flip_test(d)
        self.assertEqual(t['n'], 12)
        self.assertAlmostEqual(t['p'], 2 / 2**12, delta=0.001)

    def test_stability_and_steady_state(self):
        self.assertEqual(self.res['summary']['dead'], 0)
        self.assertGreaterEqual(self.res['summary']['steady_state_ratio'], a50.STEADY_LO)
        self.assertLessEqual(self.res['summary']['steady_state_ratio'], a50.STEADY_HI)

    def test_effect_size_clears_bar(self):
        self.assertGreaterEqual(self.res['summary']['median_difference'], a50.BAR)

    def test_oracle_b_is_the_ceiling(self):
        ob = min(r['oracle_b']['post'] for r in self.rows)
        lb = min(r['learner_both']['post'] for r in self.rows)
        self.assertGreaterEqual(ob, lb)

    def test_seeds_disjoint(self):
        used = {r['seed'] for r in self.rows}
        self.assertEqual(used, set(range(4800, 4812)))
        self.assertEqual(used & set(range(4600, 4612)), set())


class TestClaimDiscipline(unittest.TestCase):
    def test_no_claim_of_experience_or_life(self):
        text = (ROOT / 'results.json').read_text().lower()
        for banned in ('conscious', 'experience', 'sentien', 'autopoi', 'alive', 'life'):
            self.assertNotIn(banned, text, f'results.json mentions {banned!r}')

    def test_protocol_states_heterogeneous_value(self):
        proto = pathlib.Path('AC50_PROTOCOL_v1.md').read_text()
        self.assertIn('heterogeneous site value', proto)
        self.assertIn('stable', proto)


if __name__ == '__main__':
    unittest.main()
