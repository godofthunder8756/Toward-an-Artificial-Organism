"""Unit tests for AC113 (P6): the frozen confirmation of the heterogeneous-LR two-counter.

These pin (1) the runner mechanics inherited from AC112 (re-verified at q=0.9), (2) the
ac113 == ac112 byte-identity (income tracking is observational), and (3) the recorded
frozen verdict/gates — so a future code change that alters the record is caught rather than
silently absorbed (AC16's rule). Mechanics tests run before the freeze; the recorded-gate
test reads the frozen results dir.
"""

import json
import unittest
from pathlib import Path

import numpy as np

import ac112
import ac113

ROOT = Path(__file__).parent


class TestEquivalence(unittest.TestCase):
    """ac113 must reproduce ac112 byte-for-byte at the same parameters (income is observational)."""

    def test_byte_identical_to_ac112(self):
        for arm, cond in [('two_counter', 'move'), ('two_counter', 'cut'),
                          ('single_counter', 'move'), ('single_counter', 'cut'),
                          ('immediate', 'move'), ('scramble', 'cut')]:
            a = ac112.run(0, 0, arm, cond, q=0.7, eps=0.08)
            b = ac113.run(0, 0, arm, cond, q=0.7, eps=0.08)
            self.assertEqual(a['state_hash'], b['state_hash'], f'{arm}/{cond}')


class TestWorldConstants(unittest.TestCase):
    def test_high_occlusion_and_grids(self):
        self.assertEqual(ac113.Q, 0.9)
        self.assertIn(0.66, ac113.THETA_GRID)
        self.assertIn((-6, 1), ac113.SINGLE_GRID)
        self.assertTrue(ac113.FINALS[0] >= 6400 and ac113.FINALS[-1] <= 6407)

    def test_weights_heterogeneous_at_primary_eps(self):
        w_u, w_p = ac113.weights(ac113.EPS)
        self.assertGreater(w_u, 0)
        self.assertLess(w_p, 0)
        self.assertNotAlmostEqual(w_u, -w_p)


class TestDecisionBehavior(unittest.TestCase):
    def test_no_cause_no_relinquish(self):
        for arm in ('two_counter', 'single_counter', 'immediate', 'scramble'):
            r = ac113.run(0, 0, arm, 'no_cause', q=0.9, eps=0.08)
            self.assertEqual(r['relinquishments'], 0, arm)

    def test_move_relinquishes(self):
        for arm in ('two_counter', 'single_counter', 'immediate', 'scramble'):
            r = ac113.run(0, 0, arm, 'move', q=0.9, eps=0.08)
            self.assertGreaterEqual(r['relinquishments'], 1, arm)


class TestRecordedGates(unittest.TestCase):
    """Pin the frozen verdict and gates from the saved results (post-freeze).

    Asserts the RECORDED falsification (F1 equivalence) so a future code change that
    silently alters the record is caught instead of absorbed (AC16's rule).
    """

    RESULTS_DIR = 'ac113_results_v1'

    def _load(self):
        d = ROOT / self.RESULTS_DIR
        if not d.exists():
            self.skipTest('frozen results not yet present')
        rows = [json.loads(l) for l in (d / 'rows.jsonl').read_text().splitlines() if l.strip()]
        snap = json.loads((d / 'pre_run_snapshot.json').read_text())
        return rows, snap

    def test_frozen_snapshot_hashes_present(self):
        rows, snap = self._load()
        self.assertIn('hashes', snap)
        self.assertIn('AC113_PROTOCOL_v1.md', snap['hashes'])
        self.assertIn('ac113.py', snap['hashes'])
        self.assertIn('ac112.py', snap['hashes'])

    def test_cohort_coverage(self):
        rows, snap = self._load()
        cohort = [r for r in rows if 'param' not in r]
        self.assertEqual(len(cohort), 16 * 3 * 4)
        self.assertEqual(len(rows), 736)   # 192 cohort + 512 sweep + 32 causal-role

    def test_recorded_verdict_is_F1_equivalence(self):
        # recompute the fixed-parameter verdict from rows.jsonl and pin it
        rows, snap = self._load()
        cohort = [r for r in rows if 'param' not in r]
        tc = {(r['seed'], r['history']): r['income_post']
              for r in cohort if r['arm'] == 'two_counter' and r['theta'] == 0.5
              and r['condition'] in ('move', 'cut')}
        sc = {(r['seed'], r['history']): r['income_post']
              for r in cohort if r['arm'] == 'single_counter' and r['w'] == -6
              and r['n_thr'] == 4 and r['condition'] in ('move', 'cut')}
        # combined move+cut income per individual
        def comb(d):
            out = {}
            for (s, h), v in d.items():
                out.setdefault((s, h), 0)
                out[(s, h)] += v
            return out
        a, b = comb(tc), comb(sc)
        diffs = sorted(a[k] - b[k] for k in a)
        mean_d = sum(diffs) / len(diffs)
        # the recorded finding: no significant advantage, mean negative (equivalence, F1)
        self.assertLess(mean_d, 0)
        # the two-counter's aggressive optimum carries a seed-dependent collapse tail
        self.assertLess(min(diffs), -10000)
        self.assertGreater(max(diffs), 100)

    def test_recorded_V2_causal_role(self):
        rows, snap = self._load()
        causal = [r for r in rows if r.get('param') == 'scramble theta=0.60']
        sweep = [r for r in rows if 'param' in r and r.get('theta') == 0.6
                 and r['arm'] == 'two_counter']
        sc_cut = sum(r['relinquishments'] >= 1 for r in causal if r['condition'] == 'cut')
        tc_cut = sum(r['relinquishments'] >= 1 for r in sweep if r['condition'] == 'cut')
        self.assertEqual(sc_cut, 0)       # scramble holds under cut (reads (0,0))
        self.assertGreaterEqual(tc_cut, 1)  # the accumulated content drives a false relinquish


if __name__ == '__main__':
    unittest.main()
