"""AC45 tests: the frozen record, its declared gates, its recorded falsification, and its hashes.

Run with: .venv/bin/python -B -m unittest test_ac45
"""
import hashlib
import json
import pathlib
import unittest
import numpy as np
import ac45_family as ac45
import ac38_variance as ac38

ROOT = pathlib.Path('ac45_results_v1')


def load():
    rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines() if l.strip()]
    res = json.loads((ROOT / 'results.json').read_text())
    snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
    return rows, res, snap


class TestProtocolWasRegisteredFirst(unittest.TestCase):
    def test_declared_sources_equal_the_hashed_set(self):
        declared = ac45.preflight()
        self.assertEqual(sorted(set(declared)), sorted(set(ac45.SOURCES)))
        self.assertEqual(len(set(declared)), 4)

    def test_declared_sources_are_unchanged_since_registration(self):
        _, _, snap = load()
        changed = [n for n, sha in snap.items()
                   if not pathlib.Path(n).exists()
                   or hashlib.sha256(pathlib.Path(n).read_bytes()).hexdigest() != sha]
        self.assertEqual(changed, [], f'edited after registration: {changed}')

    def test_result_dir_is_frozen(self):
        self.assertTrue(ROOT.is_dir())
        self.assertTrue((ROOT / 'pre_run_snapshot.json').exists())
        self.assertTrue((ROOT / 'rows.jsonl').exists())


class TestFrozenGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.res, cls.snap = load()
        cls.gates = cls.res['gates']

    def test_family_rule_passes(self):
        """The claim itself: G1 (direction + impairment) and G2 (significance) both hold."""
        self.assertTrue(self.gates['G1_family_direction_and_impairment'])
        self.assertTrue(self.gates['G2_family_significance'])

    def test_protected_completeness_determinism_pass(self):
        self.assertTrue(self.gates['G4_protected_variant_above_cut'])
        self.assertTrue(self.gates['G5_all_individuals_complete'])
        self.assertTrue(self.gates['G6_determinism'])

    def test_g3_heterogeneity_is_recorded_false(self):
        """Prediction #3 (the ~88% bimodality) is FALSIFIED on seeds 16-23: the response is 100%
        impaired. The failure is recorded, not hidden -- a future change that flips this bit is caught."""
        self.assertFalse(self.gates['G3_heterogeneity_present'])

    def test_per_endpoint_impaired_is_unity(self):
        s = self.res['summary']['per_endpoint']
        for q in ac45.FAMILY:
            self.assertEqual(s[q]['impaired'], 1.0, f'{q} impaired != 1.0')

    def test_all_three_resolve_and_clear_the_family_criterion(self):
        s = self.res['summary']['per_endpoint']
        for q in ac45.FAMILY:
            self.assertEqual(s[q]['n'], 16)
            self.assertLessEqual(s[q]['p'], ac45.P_BAR)
            self.assertLess(s[q]['p'], 0.001, f'{q} does not clear the 0.001 family criterion')

    def test_effect_direction_is_positive_for_every_member(self):
        s = self.res['summary']['per_endpoint']
        for q in ac45.FAMILY:
            self.assertGreater(s[q]['median'], 0)

    def test_seeds_are_disjoint_from_all_prior_seed_families(self):
        used = {r['seed'] for r in self.rows}
        self.assertEqual(used, set(range(16, 24)))
        self.assertEqual(used & set(range(0, 16)), set(),
                         'finals must not reuse engineering (0-7) or AC43 finals (8-15)')

    def test_every_individual_is_present_once(self):
        keys = [(r['seed'], r['history']) for r in self.rows]
        self.assertEqual(len(keys), 16)
        self.assertEqual(len(set(keys)), 16)


class TestClaimDiscipline(unittest.TestCase):
    def test_no_claim_of_experience_or_life_is_recorded(self):
        text = (ROOT / 'results.json').read_text().lower()
        for banned in ('conscious', 'experience', 'sentien', 'autopoi', 'alive', 'life'):
            self.assertNotIn(banned, text, f'results.json mentions {banned!r}')

    def test_protocol_states_the_corruption_condition(self):
        proto = pathlib.Path('AC45_PROTOCOL_v1.md').read_text()
        self.assertIn('reg_rate = 0.0', proto)
        self.assertIn('absent', proto)


if __name__ == '__main__':
    unittest.main()
