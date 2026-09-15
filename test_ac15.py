"""AC15 unit tests: the graded access law, its faithfulness, and the protocol's gates.

Run with: .venv/bin/python -B -m unittest test_ac15
"""
import json
import statistics
import unittest
from pathlib import Path
import numpy as np
import ac15, ac12, ac9, ac4
from ac1 import decode


class TestPrimitiveIsFaithful(unittest.TestCase):
    """GRADE=0 must be the frozen world, not a variant of it."""

    def drive(self, step, seed, history, ticks, base_map):
        alloc=ac12.Alloc('preserve',seed,history)
        o,offs=ac12.acquire(seed); alloc.offs=offs; alloc.shadow=o.body.traces[0].copy()
        rng=np.random.default_rng([seed,1509])
        for t in range(ticks):
            alloc.now=t
            step(o,(rng.random((126,7))<.0001).astype(np.uint8),
                 (rng.random(o.memory.bits.shape)<.0001).astype(np.uint8),
                 rng.integers(0,4,20,dtype=np.uint8),bool(rng.random()<.5),
                 base_map,[t<512]*2,t<512)
        return o.digest()

    def test_grade_zero_reproduces_the_ac12_harness(self):
        """The surgery is a no-op at GRADE=0: same state hash as the AC12 step."""
        ac15.set_world()
        for seed in (0,1):
            base_map=(seed%2,(seed//2)%2)
            a=ac12.Alloc('preserve',seed,0); o,offs=ac12.acquire(seed)
            a.offs=offs; a.shadow=o.body.traces[0].copy()
            frozen=self.drive(ac12.build('preserve',a),seed,0,192,base_map)
            ac15.GRADE=0
            graded=self.drive(ac15.build('preserve',ac12.Alloc('preserve',seed,0)),seed,0,192,base_map)
            self.assertEqual(frozen,graded,f'GRADE=0 diverged from the AC12 harness at seed {seed}')

    def test_grade_zero_miss_yields_nothing(self):
        """A miss at GRADE=0 must reproduce the frozen branch exactly: cost paid, no intake."""
        ac15.set_world(); ac15.GRADE=0
        b=ac4.Body(np.zeros((4,1024,7),dtype=np.uint8),np.zeros((4,1024,7),dtype=np.int16),
                   np.zeros((20,2),dtype=np.int16),np.zeros(20,dtype=np.int16))
        e=ac4.empty_event(); before=(b.energy,b.material,b.fuel)
        ac15.make_contact(ac4.react)(b,1,0,1,e)     # port 0, true port 1 -> miss
        self.assertEqual((b.energy,b.material,b.fuel),(before[0]-1,before[1],before[2]))
        self.assertEqual(e['in_m'],0); self.assertEqual(e['in_f'],0)
        self.assertEqual(e['productive'],0); self.assertEqual(e['spent_e'],1); self.assertEqual(e['active'],1)


class TestGradedEconomics(unittest.TestCase):
    """The declared incentive structure, measured on the primitive itself."""

    def body(self, seed=0):
        """A real organism body from the frozen acquisition path, not a hand-built one:
        `ac4.available` needs the body's own array shapes."""
        return ac12.acquire(seed)[0].body

    def contact_yield(self, action, port, true, grade, ticks=8):
        """Per-contact yield. A fresh event dict per call, as the step does: the frozen
        convention is that `in_m`/`in_f` hold *this* step's intake, not a running total."""
        ac15.set_world(); ac15.GRADE=grade
        b=self.body()
        contact=ac15.make_contact(ac4.react); total=0
        for _ in range(ticks):
            e=ac4.empty_event(); contact(b,action,port,true,e)
            total += e['in_m'] if action==1 else e['in_f']
        return total/ticks

    def test_match_earns_full_yield_in_both_grades(self):
        for grade in (0,1):
            self.assertEqual(self.contact_yield(1,0,0,grade),64.0)
            self.assertEqual(self.contact_yield(0,1,1,grade),32.0)

    def test_miss_earns_a_quarter_only_under_the_graded_law(self):
        self.assertEqual(self.contact_yield(1,1,0,0),0.0)      # frozen: nothing
        self.assertEqual(self.contact_yield(1,1,0,1),16.0)     # graded: a quarter
        self.assertEqual(self.contact_yield(0,0,1,0),0.0)
        self.assertEqual(self.contact_yield(0,0,1,1),8.0)

    def test_dropping_a_stale_route_beats_keeping_it_under_the_graded_law(self):
        """The property the AC11/AC12/AC13 line needed: 16 kept vs 36 blind, and 16 > 0."""
        kept=self.contact_yield(1,1,0,1)                 # stale entry, always misses -> 16
        match=self.contact_yield(1,1,1,1)                # correct entry -> 64
        blind=0.5*match+0.5*kept                         # a coin, ~1/2
        self.assertEqual(kept,16.0); self.assertEqual(match,64.0)
        self.assertGreater(blind,kept)
        self.assertGreater(kept,0)                       # survivable, not fatal

    def test_productivity_is_defined_by_the_match_not_by_intake(self):
        """A stale route must never register as productive, or the drop rule can never fire."""
        ac15.set_world(); ac15.GRADE=1
        b=self.body()
        e=ac4.empty_event()
        ac15.make_contact(ac4.react)(b,1,1,0,e)          # stale miss: intake 16, not productive
        self.assertEqual(e['in_m'],16); self.assertEqual(e['productive'],0)

class TestProtocolGates(unittest.TestCase):
    """The prespecified gates, re-derived from the frozen final table."""

    @classmethod
    def setUpClass(cls):
        p=Path('ac15_results_v1/results.json')
        if not p.exists(): raise unittest.SkipTest('final table not collected yet')
        cls.rows=json.loads(p.read_text())['rows']
        cls.by={}
        for r in cls.rows: cls.by.setdefault(r['arm'],[]).append(r)

    def mean(self, arm, key):
        return statistics.mean(r[key] for r in self.by[arm])

    def test_g1_learner_beats_both_blind_extremes(self):
        L=self.mean('allocate','mean_chan_productivity')
        self.assertGreaterEqual(L-self.mean('preserve','mean_chan_productivity'),0.08)
        self.assertGreaterEqual(L-self.mean('relinquish','mean_chan_productivity'),0.08)

    def test_g3_consistency_arms_reproduce_preserve_exactly(self):
        for other in ('fixed_period_1','streak_never'):
            for a,b in zip(self.by['preserve'],self.by[other]):
                self.assertEqual(a['state_hash'],b['state_hash'])
                self.assertEqual(a['demand'],b['demand'])

    def test_g4_no_arm_dies(self):
        self.assertTrue(all(r['completed'] for r in self.rows))

    def test_g5_kept_what_was_valid_and_not_what_was_not(self):
        self.assertGreaterEqual(self.mean('allocate','productivity_kept'),0.95)
        self.assertGreater(self.mean('allocate','productivity_moved'),0.0)

    def test_frozen_table_covers_every_arm_and_seed(self):
        self.assertEqual(len(self.rows),8*8)
        for arm in ac15.ARMS:
            self.assertEqual(len(self.by[arm]),8)


class TestConstantsAreDeclared(unittest.TestCase):
    def test_world_constants(self):
        self.assertEqual((ac15.FULL_M,ac15.FULL_F),(64,32))
        self.assertEqual((ac15.GRADE_M,ac15.GRADE_F),(16,8))
        self.assertEqual(ac15.MOVE_ACTIONS,(1,),'the move must stay asymmetric to discriminate')
        self.assertEqual(ac15.FINALS,(1900,1901,1902,1903))

    def test_sources_hashed_including_the_protocol(self):
        h=json.loads(Path('ac15_results_v1/results.json').read_text())['hashes']
        self.assertIn('AC15_PROTOCOL_v1.md',h)
        self.assertIn('ac15.py',h)


if __name__=='__main__':
    unittest.main()
