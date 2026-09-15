"""AC40 tests: the split criterion, and the defect it found in its own stability metric.

Run with: .venv/bin/python -B -m unittest test_ac40
"""
import json
from pathlib import Path
import unittest
import ac40_criterion as ac40


def rows(root):
    return [json.loads(l) for l in (Path(root)/'rows.jsonl').read_text().splitlines() if l.strip()]


def diffs(root):
    return [r['learner_both']['post']-r['no_release']['post'] for r in rows(root)]


class TestResolvability(unittest.TestCase):
    """All four recorded contrasts are resolved at the exact test -- including AC32's, which failed on
    gate SHAPE rather than on contrast."""

    def test_frozen_contrasts_are_all_resolved(self):
        for root in ('ac33_results_v1','ac36_results_v1','ac32_results_v1'):
            r=ac40.resolvability(diffs(root))
            self.assertTrue(r['resolved'],root)
            self.assertEqual(r['n'],12)
            self.assertAlmostEqual(r['p'],2.0/2**12,places=6)

    def test_power_floor_is_stated(self):
        r=ac40.resolvability([1.0]*4)
        self.assertFalse(r['power_ok'],'n=4 cannot be significant')
        self.assertAlmostEqual(r['floor'],2.0/16,places=6)

    def test_a_null_contrast_is_not_resolved(self):
        r=ac40.resolvability([1.0,-1.0]*6)
        self.assertFalse(r['resolved'])


class TestEffectSizeAndItsNoise(unittest.TestCase):
    def test_effect_size_reports_units_not_just_a_ratio(self):
        e=ac40.effect_size(diffs('ac36_results_v1'))
        self.assertGreater(e['mean'],1.0)
        self.assertAlmostEqual(e['impaired_fraction'],1.0,places=2)
        self.assertGreater(e['ratio'],3.0)

    def test_the_ratio_is_noisy_across_half_samples_in_EVERY_study(self):
        """AC40's own defect, asserted: the half-sample stability check flags the passing studies too,
        so a mean/sd ratio resampled this way discriminates nothing."""
        for root in ('ac33_results_v1','ac36_results_v1','ac32_results_v1'):
            s=ac40.stability(diffs(root))
            self.assertFalse(s['stable'],f'{root} flagged unstable like the rest')
            self.assertGreater(s['spread'],1.0)

    def test_stability_is_reported_but_not_trusted(self):
        """The module declares the bar; this test records that the bar does not do its job."""
        self.assertEqual(ac40.STABILITY_BAR,1.5)
        s=ac40.stability([1,2,3,4,5,6,7,8])
        self.assertIn('spread',s)


class TestHeadroom(unittest.TestCase):
    def test_a_saturated_endpoint_is_flagged(self):
        h=ac40.headroom([4096]*16,4096)
        self.assertTrue(h['saturated'])
        self.assertAlmostEqual(h['at_ceiling_fraction'],1.0,places=6)

    def test_an_endpoint_with_headroom_is_not_flagged(self):
        h=ac40.headroom([100,200,300,400,500,600,700,800,900,1000,1100,1200],4096)
        self.assertFalse(h['saturated'])

    def test_audit_includes_headroom_only_when_given(self):
        d=[1.0]*12
        self.assertNotIn('headroom',ac40.audit(d))
        self.assertIn('headroom',ac40.audit(d,live_values=[4096]*12,ceiling=4096))


class TestFrameworkNotAStudy(unittest.TestCase):
    def test_no_protocol_or_results_dir(self):
        root=Path('.')
        self.assertFalse((root/'AC40_PROTOCOL_v1.md').exists())
        self.assertFalse(list(root.glob('ac40_results*')))
        self.assertFalse((root/'ac40_results_v1').exists())


if __name__=='__main__':
    unittest.main()
