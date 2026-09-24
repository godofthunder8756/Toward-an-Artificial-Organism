"""Level-1 + level-2 tests for AC114 (the SR-2 boundary-exchange successor).

Level 1 verifies the implemented transport law directly on the compiled react
and the puncture machinery: admission is a function of the LOCAL live-state of
the channel's gate links (site gate), the aggregate gate is count-only, the
puncture zeroes exactly its target and is booked, and the gate is inert when
the gate links are live (the successor's ordinary operation is byte-identical
to the frozen world).

Level 2 asserts the organism-level consequences on engineering seeds: retention
continuity (T1), exchange mediation via the admission ledger (T2), the
site-vs-count discrimination (D1/T4), local admission (D2), the semipermeability
mirror (permeant), and the labelled external rescue (T6).

The tuple/list JSON round-trip is normalised with `norm()` before comparing
final_inventory/ledger (the AC15/AC79 lesson); `state_hash` is the real
equality test and needs no normalisation.
"""
import json
import unittest
import numpy as np
import ac9
import ac10
import ac4
import ac114
from ac1 import decode


def norm(x):
    return json.loads(json.dumps(x))


def fresh_body(seed=0):
    """A valid ac4.Body with controllable boundary/reservoir state."""
    b, bits, target, priority = ac4.acquire(seed)
    return b


def react_for(gate, puncture_links=()):
    mask = np.zeros(20, dtype=bool)
    for link in puncture_links:
        mask[link] = True
    return ac114.make_react(ac114.ADMIT_FN[gate], mask)


def admit_result(gate, action, boundary_lives=(), channel=None):
    """Run the compiled react for one contact action on a controlled boundary."""
    react = react_for(gate)
    b = fresh_body()
    b.boundary[:] = 0
    for link in boundary_lives:
        b.boundary[link] = 100
    e = ac4.empty_event()
    react(b, action, 'self', e)
    return e, b


class TransportLaw(unittest.TestCase):
    """Level 1: the imposed gate behaves as declared (site local, count global)."""

    def test_site_gate_admits_when_gate_link_live(self):
        e, _ = admit_result('site', 0, boundary_lives=(0,))
        self.assertEqual(e['in_f'], 32)

    def test_site_gate_blocks_when_gate_link_dead(self):
        e, b = admit_result('site', 0, boundary_lives=())
        self.assertEqual(e['in_f'], 0)
        self.assertEqual(e['spent_e'], 1)   # contact cost still paid
        self.assertEqual(e['active'], 1)

    def test_site_gate_ignores_a_non_gate_hole(self):
        e, _ = admit_result('site', 0, boundary_lives=(0,))
        self.assertEqual(e['in_f'], 32)

    def test_site_gate_blocks_action1_on_its_own_gate_link(self):
        e, _ = admit_result('site', 1, boundary_lives=())
        self.assertEqual(e['in_m'], 0)
        e2, _ = admit_result('site', 1, boundary_lives=(1,))
        self.assertEqual(e2['in_m'], 64)

    def test_count_gate_blocks_below_threshold(self):
        e, _ = admit_result('count', 0, boundary_lives=tuple(range(ac114.B_MIN - 1)))
        self.assertEqual(e['in_f'], 0)

    def test_count_gate_admits_at_threshold(self):
        e, _ = admit_result('count', 0, boundary_lives=tuple(range(ac114.B_MIN)))
        self.assertEqual(e['in_f'], 32)

    def test_count_gate_is_site_indifferent(self):
        # 19 links live but the gate link (0) is dead: count gate still admits.
        lives = tuple(l for l in range(20) if l != 0)
        e, _ = admit_result('count', 0, boundary_lives=lives)
        self.assertEqual(e['in_f'], 32)

    def test_disabled_gate_reproduces_frozen_yield(self):
        e, _ = admit_result('none', 0, boundary_lives=())
        self.assertEqual(e['in_f'], 32)


class PunctureLaw(unittest.TestCase):
    """Level 1: the puncture zeroes exactly its target and is booked."""

    def _run(self, step, seed=0):
        o = ac114.v2.acquire(seed)
        o.body.boundary[:] = 100
        e = step(o, np.zeros((126, 7), np.uint8), np.zeros((2, 2, 3, 7), np.uint8),
                 np.zeros(20, np.uint8), False, (0, 0), [True, True], False)
        return o, e

    def test_puncture_zeroes_only_the_target_link(self):
        _, post = ac114.build('puncture')
        o, _ = self._run(post)
        self.assertEqual(o.body.boundary[0], 0)
        for link in range(1, 20):
            self.assertGreater(o.body.boundary[link], 0)

    def test_puncture_books_a_discard(self):
        _, post = ac114.build('puncture')
        _, e = self._run(post)
        self.assertGreaterEqual(e['B_discard'], 1)

    def test_puncture_arm_is_normal_before_onset(self):
        pre, _ = ac114.build('puncture')
        # pre-onset step must NOT be the punctured step: link 0 stays alive.
        o, _ = self._run(pre)
        self.assertGreater(o.body.boundary[0], 0)


class Inertness(unittest.TestCase):
    """Level 1/2 (T5): the gate is the only change; ordinary operation is frozen."""

    def test_reference_is_the_frozen_step(self):
        self.assertIs(ac114.build('reference')[0], ac9.step)
        self.assertIs(ac114.build('reference')[1], ac9.step)

    def test_keep_and_rival_are_byte_identical_to_reference(self):
        for seed in (1, 4, 7):
            for hist in (0, 1):
                ref = ac114.run(seed, hist, 'reference', ticks=512)
                for arm in ('keep', 'rival'):
                    r = ac114.run(seed, hist, arm, ticks=512)
                    self.assertEqual(r['state_hash'], ref['state_hash'], (seed, hist, arm))
                    self.assertEqual(r['ledger'], ref['ledger'], (seed, hist, arm))

    def test_reference_reproduces_frozen_ac10_keep(self):
        frozen = {}
        with open('ac10_results_v1/rows.jsonl') as f:
            for line in f:
                r = json.loads(line)
                if r['arm'] == 'keep':
                    frozen[(r['seed'], r['history'])] = r
        keys = ['activity', 'completed', 'routes', 'demand', 'ledger',
                'final_inventory', 'state_hash']
        for (seed, hist), ref in frozen.items():
            live = ac114.run(seed, hist, 'reference')
            for k in keys:
                self.assertEqual(norm(live[k]), norm(ref[k]), (seed, hist, k))

    def test_no_B_retention_ref_reproduces_frozen_no_B_retention(self):
        frozen = {}
        with open('ac10_results_v1/rows.jsonl') as f:
            for line in f:
                r = json.loads(line)
                if r['arm'] == 'no_B_retention':
                    frozen[(r['seed'], r['history'])] = r
        keys = ['activity', 'completed', 'routes', 'demand', 'ledger',
                'final_inventory', 'state_hash']
        for (seed, hist), ref in frozen.items():
            live = ac114.run(seed, hist, 'no_B_retention_ref')
            for k in keys:
                self.assertEqual(norm(live[k]), norm(ref[k]), (seed, hist, k))


class OrganismLevel(unittest.TestCase):
    """Level 2: the organism-level consequences, on engineering seeds."""

    def test_exchange_mediation_starvation(self):
        """T2: retention rescued but gate links dead -> intake 0 -> death."""
        for seed in (1, 3, 5, 7):
            r = ac114.run(seed, 0, 'no_B_retention')
            ref = ac114.run(seed, 0, 'no_B_retention_ref')
            self.assertFalse(r['completed'], seed)
            self.assertIsNotNone(r['chrono']['first_gate_dead'], seed)
            self.assertIsNotNone(r['chrono']['first_dead'], seed)
            self.assertTrue(ref['completed'], seed)
            # intake after gate death is at most the pre-death endowment
            self.assertLessEqual(r['ledger']['in_f'], 5 * 32, seed)
            self.assertLessEqual(r['ledger']['in_m'], 5 * 64, seed)
            self.assertGreater(ref['ledger']['in_f'], r['ledger']['in_f'], seed)

    def test_d1_site_cuts_only_the_punctured_channel(self):
        """D1/T4: on the punctured state the site gate zeroes channel 0 while
        the count gate leaves it at full yield (location-matched)."""
        for seed in (1, 3, 5, 7):
            site = ac114.run(seed, 0, 'puncture')
            count = ac114.run(seed, 0, 'rival_puncture')
            self.assertEqual(site['assay']['in_f'], 0, seed)
            self.assertGreater(count['assay']['in_f'], 0, seed)

    def test_d2_non_gate_hole_leaves_admission_unchanged(self):
        """D2: puncturing a non-gate link leaves both channels' admission full."""
        for seed in (1, 3, 5, 7):
            r = ac114.run(seed, 0, 'puncture_non_gate')
            self.assertGreater(r['assay']['in_f'], 0, seed)
            self.assertGreater(r['assay']['in_m'], 0, seed)

    def test_semipermeability_mirror(self):
        """permeant (exchange present, retention broken) dies by export, the
        mirror image of no_B_retention (retention rescued, exchange cut)."""
        for seed in (1, 3, 5, 7):
            r = ac114.run(seed, 0, 'permeant')
            self.assertFalse(r['completed'], seed)
            self.assertGreater(r['ledger']['particle_export'], 0, seed)

    def test_boundary_interruption(self):
        """no_B: no B production -> no intake (both gate links die) + export."""
        for seed in (1, 3, 5, 7):
            r = ac114.run(seed, 0, 'no_B')
            self.assertEqual(r['ledger']['B_birth'], 0, seed)
            self.assertFalse(r['completed'], seed)
            self.assertGreater(r['ledger']['particle_export'], 0, seed)
            self.assertIsNotNone(r['chrono']['first_gate_dead'], seed)

    def test_external_rescue_restores_both_functions(self):
        """T6: external B restores retention AND exchange; labelled external."""
        for seed in (1, 3, 5, 7):
            r = ac114.run(seed, 0, 'B_rescue')
            self.assertGreater(r['ledger']['external_B'], 0, seed)
            self.assertEqual(r['ledger']['B_birth'], 0, seed)
            self.assertEqual(r['ledger']['particle_export'], 0, seed)
            self.assertTrue(r['completed'], seed)
            self.assertGreater(r['ledger']['in_f'], 0, seed)


class LedgerIntegrity(unittest.TestCase):
    """The frozen conservation identities hold in every arm (no law patching)."""

    def check_ledger(self, row):
        l = row['ledger']
        inv = row['final_inventory']
        m0 = 128 + 24 + 40 + l['in_m'] + 2 * l['external_B']
        m1 = inv[1] + 4 * inv[3] + 2 * inv[4] + sum(row['demand'])
        spent = l['writes'] - l['memory_writes']
        losses = (l['memory_waste'] + l['memory_expiry'] +
                  4 * (l['particle_expiry'] + l['particle_export']) +
                  2 * (l['B_expiry'] + l['B_discard']) + l['overflow_m'])
        self.assertEqual(m0, m1 + spent + losses, (row['seed'], row['arm']))
        self.assertEqual(64 + 8 * l['converted'], inv[0] + l['spent_e'],
                         (row['seed'], row['arm']))
        self.assertEqual(32 + l['in_f'], inv[2] + l['overflow_f'] + l['converted'],
                         (row['seed'], row['arm']))

    def test_every_arm_keeps_the_frozen_ledger_identity(self):
        for arm in ac114.ARMS:
            self.check_ledger(ac114.run(7, 0, arm, ticks=512))


class FinalGates(unittest.TestCase):
    """The frozen final confirmation (seeds 6500-6507) records its gate verdicts.

    Recorded-outcome regressions: they pin the SAVED table's gate verdicts (from
    `ac114_results_v1/rows.jsonl`) so a future code change that silently alters
    the record is caught. They do NOT re-run the study; audit_ac114.py re-derives
    the same verdicts independently and replay_ac114.py does the sampled reruns.
    """

    SEEDS = list(range(6500, 6508))

    @classmethod
    def setUpClass(cls):
        with open('ac114_results_v1/rows.jsonl') as f:
            cls.rows = [json.loads(l) for l in f if l.strip()]
        cls.by = {(r['seed'], r['history'], r['arm']): r for r in cls.rows}

    def test_final_table_is_complete(self):
        self.assertEqual(len(self.rows), 8 * 2 * len(ac114.ARMS))

    def test_g1_inertness_all_individuals(self):
        for s in self.SEEDS:
            for h in (0, 1):
                keep = self.by[(s, h, 'keep')]
                ref = self.by[(s, h, 'reference')]
                rival = self.by[(s, h, 'rival')]
                self.assertEqual(keep['state_hash'], ref['state_hash'], (s, h))
                self.assertEqual(keep['state_hash'], rival['state_hash'], (s, h))

    def test_g3_exchange_mediation(self):
        for s in self.SEEDS:
            for h in (0, 1):
                nb = self.by[(s, h, 'no_B_retention')]
                ref = self.by[(s, h, 'no_B_retention_ref')]
                self.assertEqual(nb['assay']['in_f'], 0, (s, h))
                self.assertEqual(nb['assay']['in_m'], 0, (s, h))
                self.assertFalse(nb['completed'], (s, h))
                self.assertTrue(ref['completed'], (s, h))

    def test_g4_d1_site_vs_count(self):
        for s in self.SEEDS:
            for h in (0, 1):
                pu = self.by[(s, h, 'puncture')]
                rp = self.by[(s, h, 'rival_puncture')]
                self.assertEqual(pu['assay']['in_f'], 0, (s, h))
                self.assertGreater(rp['assay']['in_f'], 0, (s, h))

    def test_g5_d2_local_admission(self):
        for s in self.SEEDS:
            for h in (0, 1):
                pn = self.by[(s, h, 'puncture_non_gate')]
                self.assertGreater(pn['assay']['in_f'], 0, (s, h))
                self.assertGreater(pn['assay']['in_m'], 0, (s, h))

    def test_g6_external_rescue(self):
        for s in self.SEEDS:
            for h in (0, 1):
                br = self.by[(s, h, 'B_rescue')]
                self.assertGreater(br['ledger']['external_B'], 0, (s, h))
                self.assertEqual(br['ledger']['B_birth'], 0, (s, h))
                self.assertEqual(br['ledger']['particle_export'], 0, (s, h))
                self.assertTrue(br['completed'], (s, h))

    def test_survival_separate_outcome(self):
        surv = {a: sum(1 for s in self.SEEDS for h in (0, 1)
                       if self.by[(s, h, a)]['completed']) for a in ac114.ARMS}
        for a in ('keep', 'reference', 'rival', 'no_B_retention_ref', 'B_rescue',
                  'rival_puncture', 'puncture_non_gate'):
            self.assertEqual(surv[a], 16, a)
        for a in ('no_B', 'no_B_retention', 'permeant', 'puncture'):
            self.assertEqual(surv[a], 0, a)


if __name__ == '__main__':
    unittest.main()
