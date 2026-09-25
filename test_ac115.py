"""Level-1 + level-2 tests for AC115 (I4, the integrated successor).

Level 1 verifies the admission gate + puncture machinery on the compiled gated
react, at AC105's yields (64/64): the gate wraps actions 0/1, `site` is local to
the channel's gate link, `count` is the aggregate rival, `none` is the
always-admit bypass, and the intake is 64 (NOT AC114's frozen 32 — the AC115
integration-point rule: never gate ac4.react directly, which would silently drop
the yield and break the AC105 byte-identity license).

Level 2 asserts the organism-level consequences: the G1 single-change license
(`keep` byte-identical to AC105 `persistent_budget` at `simult` on a sampled
final seed), the four admission discriminations on engineering seed 0, and the
observer-discard (state-sufficiency) byte-identity.

The final-gate verdicts are pinned as recorded-outcome regressions (see
`FinalGateRegressions`), so a future code change that alters the recorded outcome
is caught instead of silently absorbed. Tuple/list and int/str-key JSON
round-trips are normalised with `norm()`; `state_hash` needs no normalisation
(the AC15/AC79 lesson).

Verification-tool: NOT in the frozen source hash set (AC16/AC17's rule).
"""
import json
import unittest
from pathlib import Path
import numpy as np
import ac4
import ac12
import ac104
import ac114
import ac115
from ac115 import ADMIT_FN, make_react_gated


def norm(x):
    return json.loads(json.dumps(x))


def setUpModule():
    # Pin every ambient module global the study depends on, so test order cannot
    # change the world an arm runs in (the AC16 unit-test lesson).
    ac12.PORTS = 4
    ac12.YIELD_M = 64
    ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None
    ac12.POST_YIELD_F = None
    ac12.REGISTER_THRESHOLD = 4
    ac104.DECISION_ALLOWANCE = 42


def fresh_body(seed=0):
    return ac4.acquire(seed)[0]


def run_contact(admit, action, boundary_lives=(), no_B=False):
    react = make_react_gated(ADMIT_FN[admit], np.zeros(20, dtype=bool), no_B=no_B)
    b = fresh_body()
    b.boundary[:] = 0
    for link in boundary_lives:
        b.boundary[link] = 100
    e = ac4.empty_event()
    react(b, action, 'self', e)
    return e, b


class AdmissionGateLaw(unittest.TestCase):
    """Level 1: the imposed gate behaves as declared, at AC105's yields."""

    def test_none_gate_yields_64_fuel(self):
        # The gated react uses AC105's yield (64), NOT AC114's frozen in_f=32.
        e, _ = run_contact('none', 0)
        self.assertEqual(e['in_f'], 64)

    def test_none_gate_yields_64_material(self):
        e, _ = run_contact('none', 1)
        self.assertEqual(e['in_m'], 64)

    def test_site_gate_blocks_dead_gate_link(self):
        # Gate link 0 (channel 0's declared link) dead -> no fuel intake.
        e, _ = run_contact('site', 0, boundary_lives=())
        self.assertEqual(e['in_f'], 0)

    def test_site_gate_admits_live_gate_link(self):
        e, _ = run_contact('site', 0, boundary_lives=(0,))
        self.assertEqual(e['in_f'], 64)

    def test_site_gate_channel1_material(self):
        e, _ = run_contact('site', 1, boundary_lives=(1,))
        self.assertEqual(e['in_m'], 64)

    def test_count_gate_blocks_no_live_links(self):
        e, _ = run_contact('count', 0, boundary_lives=())
        self.assertEqual(e['in_f'], 0)

    def test_count_gate_admits_at_B_MIN(self):
        e, _ = run_contact('count', 0, boundary_lives=tuple(range(ac114.B_MIN)))
        self.assertEqual(e['in_f'], 64)

    def test_puncture_candidate_restriction_is_in_source(self):
        # The puncture must restrict the action-8 candidate set to ~PUNCTURE
        # (AC114's surgery, composed unchanged). A missing restriction would let
        # a punctured hole re-heal.
        self.assertIn('& ~PUNCTURE', ac114.CANDIDATES_LINE_PUNCTURED)


class OrganismLevel(unittest.TestCase):
    """Level 2: organism-level consequences, sampled (engineering seed 0 + one final seed)."""

    def test_g1_keep_byte_identical_to_ac105(self):
        # The single-change license on a FINAL seed: the integrated `keep` arm is
        # byte-identical to AC105 persistent_budget at simult (the gate is inert
        # at the intact boundary).
        keep = ac115.run(6600, 0, 'keep')['state_hash']
        base = ac105_ref(6600, 0)
        self.assertEqual(keep, base)

    def test_d1_link_specific(self):
        # Paired per seed: puncture (site) zeroes alive-window ch0 admission,
        # rival_puncture (count) leaves it > 0.
        p = ac115.run(0, 0, 'puncture')
        rp = ac115.run(0, 0, 'rival_puncture')
        p_att, p_adm = ac115._alive_admission(p, 0, ac115.PUNCTURE_TICK)
        rp_att, rp_adm = ac115._alive_admission(rp, 0, ac115.PUNCTURE_TICK)
        self.assertGreater(p_att, 0)
        self.assertEqual(p_adm, 0)
        self.assertGreater(rp_adm, 0)

    def test_d2_local_admission(self):
        # A non-gate puncture blocks neither channel.
        r = ac115.run(0, 0, 'puncture_non_gate')
        c0_att, c0_adm = ac115._alive_admission(r, 0, ac115.PUNCTURE_TICK)
        c1_att, c1_adm = ac115._alive_admission(r, 1, ac115.PUNCTURE_TICK)
        self.assertGreater(c0_adm, 0)
        self.assertGreater(c1_adm, 0)

    def test_retention_vs_admission(self):
        # Retention-only rescue does NOT restore admission (gate links still dead).
        nbr = ac115.run(0, 0, 'no_B_retention')
        nr = ac115.run(0, 0, 'no_B_retention_ref')
        nbr0a, nbr0d = ac115._alive_admission(nbr, 0, nbr['gate0_dead_tick'])
        nr0a, nr0d = ac115._alive_admission(nr, 0, nr['gate0_dead_tick'])
        self.assertEqual(nbr0d, 0)
        self.assertEqual(nr0d, nr0a)
        self.assertFalse(nbr['completed'])
        self.assertTrue(nr['completed'])

    def test_observer_discard_keep(self):
        # State sufficiency: discarding the host-side observer mid-streak leaves
        # the trajectory byte-identical.
        obs = ac115.observer_discard_keep(0, 0)
        self.assertTrue(obs['per_tick_identical'])
        self.assertTrue(obs['terminal_identical'])


class FinalGateRegressions(unittest.TestCase):
    """The frozen gate verdicts, pinned as recorded-outcome regressions.

    Populated from the frozen `ac115_results_v1/results.json` after the finals
    run. These assert the recorded outcome (pass or fail) so a future code change
    that alters the record is caught; a recorded FAIL is asserted as a failure,
    never re-classified (the AC16/AC17 discipline).
    """

    @classmethod
    def setUpClass(cls):
        cls.results = json.loads(
            (Path(__file__).parent / 'ac115_results_v1' / 'results.json').read_text())
        cls.gates = cls.results['gates']

    def test_recorded_gates_match_frozen(self):
        # The recorded outcome, pinned verbatim. G4/G5/G6/G7 FAILED on the frozen
        # finals (see AC115_RESULTS_v1.md) — recorded as False, never re-classified
        # (the AC16/AC17 discipline: a failed gate keeps its measured value).
        expected = {
            'G1_single_change_license': True,
            'G2_D1_link_specific_admission': True,
            'G3_D2_local_admission': True,
            'G4_T2_boundary_supports_entry': False,
            'G5_retention_vs_admission': False,
            'G6_endogenous_vs_external': False,
            'G7_composition_under_stress': False,
            'G8_completeness_determinism': True,
        }
        for gname, want in expected.items():
            got = self.gates[gname]
            self.assertEqual(got, want, f'{gname}: recorded {got}, expected {want}')


def ac105_ref(seed, history):
    # ac105.run is imported lazily so level-1 tests do not pay the import cost.
    import ac105
    return ac105.run(seed, history, 'persistent_budget', 'simult')['state_hash']


if __name__ == '__main__':
    unittest.main()
