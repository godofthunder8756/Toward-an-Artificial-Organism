"""AC43 tests: the frozen record, its declared gates, and its registered source hashes.

Run with: .venv/bin/python -B -m unittest test_ac43
"""
import hashlib
import json
import pathlib
import unittest
import numpy as np
import ac43_capability as ac43
import ac38_variance as ac38

ROOT=pathlib.Path('ac43_results_v1')


def load():
    rows=[json.loads(l) for l in (ROOT/'rows.jsonl').read_text().splitlines() if l.strip()]
    res=json.loads((ROOT/'results.json').read_text())
    snap=json.loads((ROOT/'pre_run_snapshot.json').read_text())
    return rows,res,snap


class TestProtocolWasRegisteredFirst(unittest.TestCase):
    def test_declared_sources_equal_the_hashed_set(self):
        """AC32's failure was a MISSING source; the protocol's list must equal what the runner hashes."""
        declared=ac43.preflight()
        self.assertEqual(sorted(set(declared)),sorted(set(ac43.SOURCES)))
        self.assertEqual(len(set(declared)),4)

    def test_declared_sources_are_unchanged_since_registration(self):
        _,_,snap=load()
        changed=[n for n,sha in snap.items()
                 if not pathlib.Path(n).exists()
                 or hashlib.sha256(pathlib.Path(n).read_bytes()).hexdigest()!=sha]
        self.assertEqual(changed,[],f'edited after registration: {changed}')

    def test_result_dir_is_frozen(self):
        self.assertTrue(ROOT.is_dir())
        self.assertTrue((ROOT/'pre_run_snapshot.json').exists())
        self.assertTrue((ROOT/'rows.jsonl').exists())


class TestFrozenGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows,cls.res,cls.snap=load()
        cls.d=np.asarray([r['difference'] for r in cls.rows],dtype=float)

    def test_all_seven_gates_passed_and_are_true(self):
        gates=self.res['gates']
        self.assertEqual(sorted(gates),['G1_resolvable','G2_median_effect_in_endpoint_units',
                                        'G3_impaired_fraction_at_or_above_floor',
                                        'G4_heterogeneity_present',
                                        'G5_protected_variant_also_above_cut',
                                        'G6_all_individuals_complete','G7_determinism'])
        self.assertTrue(all(gates.values()),gates)

    def test_recorded_summary_matches_the_rows(self):
        s=self.res['summary']
        self.assertEqual(s['n'],16)
        self.assertAlmostEqual(s['median_difference'],float(np.median(self.d)),places=6)
        self.assertAlmostEqual(s['impaired_fraction'],float(np.mean(self.d>0)),places=6)
        self.assertAlmostEqual(s['impaired_fraction'],0.875,places=6)

    def test_effect_size_clears_the_declared_bar_in_endpoint_units(self):
        self.assertGreaterEqual(float(np.median(self.d)),ac43.MEDIAN_BAR)
        self.assertEqual(ac43.MEDIAN_BAR,150.0)

    def test_contrast_is_resolvable_at_the_power_floor(self):
        t=ac38.sign_flip_test(list(self.d))
        self.assertEqual(t['n'],16)
        self.assertLessEqual(t['p'],ac43.P_BAR)
        self.assertAlmostEqual(t['p'],2/2**16,delta=0.001)

    def test_the_bimodality_prediction_holds_on_fresh_seeds(self):
        """AC39's prediction, relocated to the metabolic family by AC42, confirmed here: the response is
        heterogeneous, so a uniformity claim is not permitted to pass (G4)."""
        impaired=float(np.mean(self.d>0))
        self.assertGreater(impaired,0.0)
        self.assertLess(impaired,1.0)

    def test_seeds_are_disjoint_from_the_engineering_seeds(self):
        used={r['seed'] for r in self.rows}
        self.assertEqual(used,set(range(8,16)))
        self.assertEqual(used & set(range(0,8)),set(),'finals must not reuse engineering seeds')

    def test_every_individual_is_present_once(self):
        keys=[(r['seed'],r['history']) for r in self.rows]
        self.assertEqual(len(keys),16)
        self.assertEqual(len(set(keys)),16)


class TestClaimDiscipline(unittest.TestCase):
    def test_no_claim_of_experience_or_life_is_recorded(self):
        text=(ROOT/'results.json').read_text().lower()
        for banned in ('conscious','experience','sentien','autopoi','alive','life'):
            self.assertNotIn(banned,text,f'results.json mentions {banned!r}')

    def test_protocol_states_the_corruption_condition(self):
        proto=pathlib.Path('AC43_PROTOCOL_v1.md').read_text()
        self.assertIn('reg_rate = 0.0',proto)
        self.assertIn('absent',proto)


if __name__=='__main__':
    unittest.main()
