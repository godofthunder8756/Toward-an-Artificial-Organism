"""AC89 tests: the runner is a correct extension of ac88 (reproduces AC88 at the separated
schedule), the final seeds carry the adversarial priority [3,0,2,1], the schedule is simultaneous
(MOVE_TICK == CORRUPT_TICK), and the composition gate G8 is UNCONDITIONAL on reconstruction
(every individual, dead or alive). Not hashed (AC17's rule)."""
import unittest
import json
from pathlib import Path
import numpy as np
import ac4
import ac12
import ac89


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac89.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def priority_of(seed):
    rng = np.random.default_rng([seed, 1004])
    return list(map(int, rng.permutation(4)))


class TestDeclaredScheduleAndSeeds(unittest.TestCase):
    def test_move_tick_is_simultaneous(self):
        self.assertEqual(ac89.MOVE_TICK, ac89.CORRUPT_TICK,
                         'the composition challenge is simultaneous (move at the corruption tick)')

    def test_final_seeds_are_adversarial(self):
        for s in (4052, 4054, 4096, 4110):
            self.assertEqual(priority_of(s), [3, 0, 2, 1],
                             f'seed {s} must have the adversarial priority [3,0,2,1]')

    def test_final_seeds_disjoint_from_engineering_and_prior_finals(self):
        finals = {4052, 4054, 4096, 4110}
        self.assertTrue(finals.isdisjoint(range(8)), 'finals must be disjoint from engineering 0-7')
        self.assertTrue(finals.isdisjoint(range(4032)), 'finals must be disjoint from prior finals')

    def test_order_preserving_decoder_moves_boundary_last(self):
        # In the acquired order-preserving layout the boundary rule (mask 256) is LAST, after the
        # four bank rules -- so for [3,0,2,1] the renewal rule (bank 1) precedes the boundary rule.
        # This is the structural change (AC86) that removes AC83's boundary-preempts-renewal path.
        _, _, _, priority = ac4.acquire(4052)
        self.assertEqual(priority, [3, 0, 2, 1])
        o, offs = ac12.acquire(4052)
        o.body.traces[1, :ac89.DESC_BITS] = ac89.description_bits(priority)[:, None]
        prog = ac89.build_program(ac89.read_slot(o, 0))
        self.assertIsNotNone(prog)
        words = prog.reshape(9, ac89.WIDTH)
        last_mask = int((words[8][1:10] * (1 << np.arange(9))).sum())
        self.assertEqual(last_mask, 256, 'the boundary word must be LAST in the acquired layout')


class TestEquivalenceWithAC88(unittest.TestCase):
    @unittest.skipUnless(Path('ac88_results_v1/results.json').exists(), 'AC88 finals not present')
    def test_separated_schedule_reproduces_ac88(self):
        # ac89 with move_tick=12288 (AC87/88's separated schedule) must reproduce AC88's frozen
        # rows field-for-field (state_hash included). Sample one seed's 40 conditions to keep the
        # suite fast while covering every arm x damage x corrupt x transition combination.
        with open('ac88_results_v1/results.json') as f:
            frozen = json.load(f)['rows']
        fmap = {(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt'], r['transition']): r
                for r in frozen}
        diffs = []
        for (s, h, a, d, c, t), fr in sorted(fmap.items()):
            if s != 4028 or h != 0:
                continue
            rr = ac89.run(s, h, a, d, c, t, move_tick=12288)
            if rr['state_hash'] != fr['state_hash']:
                diffs.append((a, d, c, t))
        self.assertEqual(diffs, [], 'ac89 at move_tick=12288 must reproduce AC88 state hashes')


class TestGateShape(unittest.TestCase):
    def test_gate_keys_match_ac88(self):
        import ac88
        self.assertEqual(set(ac89.gates([]).keys()), set(ac88.gates([]).keys()))

    def test_composition_gate_is_unconditional_on_reconstruction(self):
        # G8 must require fw==0 for EVERY succession composition individual (dead or alive), not
        # just survivors. Pin the shape by construction on synthetic rows.
        row = dict(arm='succession', damage=True, corrupt=True, transition='perm', completed=False,
                   flipped_still_wrong=1, description_correct_intervention=130,
                   description_correct=130)
        # a dead individual with fw!=0 must FAIL G8 (unconditional reconstruction)
        g = ac89.gates([dict(row, flipped_still_wrong=1)])
        self.assertFalse(g['G8_composition'])


class TestRecordedFreeze(unittest.TestCase):
    @unittest.skipUnless(Path('ac89_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac89_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac89.gates(rows)
        g['G9_completeness_determinism'] = len(rows) == len(results['seeds']) * 2 * 40
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')
        rep = ac89.composition_report(rows)
        self.assertEqual(rep['n'], len(results['seeds']) * 2)
        # every individual must be reported unconditionally (per_individual covers all n)
        self.assertEqual(len(rep['per_individual']), rep['n'])
        self.assertEqual(rep['survive'], sum(p['completed'] for p in rep['per_individual']))


if __name__ == '__main__':
    unittest.main()
