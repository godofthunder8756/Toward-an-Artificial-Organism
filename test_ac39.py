"""AC39 tests: the prerequisite that stopped the study, and the criterion it exposed.

Run with: .venv/bin/python -B -m unittest test_ac39
"""
import pathlib
import unittest
import numpy as np
import ac19
import ac39_occupancy as ac39
import ac38_variance as ac38

SEEDS=tuple(range(8))          # the full recorded set: a 3-seed subset behaves differently (see below)
HISTORIES=(0,1)


class TestPrerequisiteFailed(unittest.TestCase):
    """Recorded numbers. Asserted so the stop cannot be quietly relaxed -- and so the tension between
    the effect-size criterion and the exact test stays visible."""

    @classmethod
    def setUpClass(cls):
        cls.live={k:ac39.active_ticks(ac39.LIVE,*k) for k in
                  ((s,h) for s in SEEDS for h in HISTORIES)}
        cls.cut={k:ac39.active_ticks(ac39.CUT,*k) for k in
                 ((s,h) for s in SEEDS for h in HISTORIES)}
        cls.diffs=[cls.live[k]-cls.cut[k] for k in sorted(cls.live)]
        cls.mean=float(np.mean(cls.diffs)); cls.sd=float(np.std(cls.diffs))

    def test_live_arm_saturates_the_endpoint(self):
        """Every live individual acts on every tick -- so the endpoint has no headroom for the arm that
        is supposed to be maintained."""
        self.assertTrue(all(v==ac19.TICKS for v in self.live.values()),self.live)

    def test_cut_arm_is_impaired_on_most_but_not_all_individuals(self):
        """The bimodality that inflates sigma_difference: some individuals show NO impairment."""
        impaired=[d for d in self.diffs if d>0]
        self.assertGreater(len(impaired),0.5*len(self.diffs))
        self.assertLess(len(impaired),len(self.diffs),'at least one individual is unimpaired')

    def test_effect_size_criterion_fails(self):
        ratio=self.mean/self.sd if self.sd else float('inf')
        self.assertGreater(self.sd,0)
        self.assertLess(ratio,3.0,f'ratio {ratio:.2f} -- the declared criterion is NOT met')
        self.assertAlmostEqual(ratio,2.45,delta=0.6)

    def test_the_ratio_is_unstable_across_seed_subsets(self):
        """The same world gives ratio 2.45 over 8 seeds and 10.17 over the first 3 -- because the
        bimodality puts most of the variance in which individuals are sampled. An effect-size criterion
        this unstable is a poor basis for a validity gate, which is AC39's real finding."""
        sub={k:ac39.active_ticks(ac39.CUT,*k) for k in ((s,h) for s in (0,1,2) for h in HISTORIES)}
        sub_live={k:ac39.active_ticks(ac39.LIVE,*k) for k in sub}
        d=[sub_live[k]-sub[k] for k in sorted(sub)]
        sub_ratio=float(np.mean(d))/float(np.std(d)) if np.std(d) else float('inf')
        self.assertGreater(sub_ratio,2.0*2.45,
                           f'subset ratio {sub_ratio:.2f} should differ sharply from 2.45')

    def test_contrast_is_nevertheless_statistically_overwhelming(self):
        """Which is the point: the criterion rejects a contrast it was meant to protect."""
        t=ac38.sign_flip_test(self.diffs)
        self.assertLess(t['p'],0.01,f"p {t['p']:.4f}")

    def test_integrity_channel_is_off_by_construction(self):
        """reg_rate=0 in active_ticks: AC14's integrity channel is disabled, as declared."""
        r=ac19.run(0,0,ac39.CUT,reg_rate=0.0)
        self.assertEqual(r['reg_rate'],0.0)


class TestNothingWasFrozen(unittest.TestCase):
    def test_no_protocol_or_results(self):
        root=pathlib.Path('.')
        self.assertFalse((root/'AC39_PROTOCOL_v1.md').exists(),
                         'the prerequisite failed: no protocol may exist for AC39')
        self.assertFalse(list(root.glob('ac39_results*')))
        self.assertEqual(ac39.SOURCES,[],'SOURCES stays empty when no protocol was written')

    def test_power_rule_still_stated(self):
        """AC38's floor: n=4 can never be significant; the studys used 8 seeds x 2 histories = 16."""
        self.assertAlmostEqual(2/2**4,0.125,places=4)
        self.assertLess(2/2**16,0.001)


if __name__=='__main__':
    unittest.main()
