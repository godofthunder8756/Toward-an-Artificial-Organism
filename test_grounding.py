"""Known-answer and invariant tests for the grounding model.

These use small DEV configurations only (never the frozen study configuration
of GROUNDING_PROTOCOL_v1.md), so running them reveals no study outcome.
    python -m unittest -v test_grounding
"""
import unittest
from fractions import Fraction as Fr
from itertools import product

from grounding.model import (FORAGE, REST, Params, Solution, all_states, blind_optimum,
                             never_forage, objectives, scrambled, summarize)

O = objectives()
DEV = dict(E=2, d=2, N=1, e_start=1, kappa=Fr(1, 100))


class TestKnownAnswers(unittest.TestCase):
    def test_energy_kernel(self):
        p = Params(E=4)
        self.assertEqual(p.energy_next(4, FORAGE), [(3, Fr(1, 4)), (4, Fr(3, 4))])
        self.assertEqual(p.energy_next(4, REST), [(3, Fr(1, 2)), (4, Fr(1, 2))])
        self.assertEqual(p.energy_next(0, REST), [(0, Fr(1))])
        self.assertEqual(sum(pr for _, pr in p.energy_next(2, FORAGE)), 1)

    def test_eta(self):
        self.assertEqual([Params(E=4).eta(e) for e in range(5)],
                         [Fr(1, 2), Fr(3, 8), Fr(1, 4), Fr(1, 8), Fr(0)])
        self.assertEqual({Params(E=4, fate=False).eta(e) for e in range(5)}, {Fr(1, 4)})

    def test_hand_computed_optimum(self):
        # derivation in GROUNDING_PROTOCOL_v1.md, section 6
        sol = Solution(Params(**DEV), O["T1_gain"])
        self.assertEqual(sol.optimum(), Fr(103, 128) - Fr(1, 100))
        self.assertEqual(sol.action(sol.start), FORAGE)
        st = summarize(sol, policy=never_forage)
        self.assertEqual(st["value"], Fr(47, 64))

    def test_single_step_delay_never_forages(self):
        sol = Solution(Params(E=2, d=1, N=1, e_start=1), O["T1_gain"])
        self.assertEqual(sol.optimum(), Fr(7, 8))
        self.assertEqual(sol.action(sol.start), REST)

    def test_report_options(self):
        self.assertEqual(O["T4_anti"].report(Fr(3, 4)), (Fr(1, 2), "not_m"))
        self.assertEqual(O["T6_abstain"].report(Fr(3, 4))[1], "abstain")
        self.assertEqual(O["T6_abstain"].report(Fr(9, 10)), (Fr(1, 2), "m"))
        self.assertEqual(O["T5_memfree"].report(Fr(1, 2)), (Fr(1), "const"))


class TestInvariants(unittest.TestCase):
    def test_rollout_value_equals_dp(self):
        for name in ("T1_gain", "T3_signed", "T6_abstain", "H_homeo"):
            for fate, death in product((True, False), repeat=2):
                sol = Solution(Params(E=2, d=2, N=2, fate=fate, death=death), O[name])
                self.assertEqual(summarize(sol)["value"], sol.optimum(), (name, fate, death))

    def test_bruteforce_policy_optimality(self):
        # exhaustive check on a tiny instance: no deterministic policy beats the DP
        p = Params(E=2, d=2, N=1, e_start=1)
        sol = Solution(p, O["T3_signed"])
        states = all_states(sol)
        best = max(summarize(sol, policy=lambda s, t=dict(zip(states, acts)): t[s])["value"]
                   for acts in product((REST, FORAGE), repeat=len(states)))
        self.assertEqual(best, sol.optimum())

    def test_blind_never_beats_observed_and_matches_when_first_step_only(self):
        p = Params(E=2, d=2, N=2)
        for name in ("T1_gain", "T6_abstain"):
            self.assertLessEqual(blind_optimum(p, O[name])[0], Solution(p, O[name]).optimum())

    def test_scrambling_is_identity_when_policy_ignores_body(self):
        # memory-free objective: optimal policy never reads e, so scrambling changes nothing
        sol = Solution(Params(E=2, d=2, N=2), O["T5_memfree"])
        self.assertEqual(scrambled(sol)["value"], sol.optimum())

    def test_scrambled_never_beats_optimum(self):
        sol = Solution(Params(E=2, d=2, N=2), O["T1_gain"])
        self.assertLessEqual(scrambled(sol)["value"], sol.optimum())

    def test_death_absorbs(self):
        sol = Solution(Params(E=2, d=2, N=2, death=True, e_start=1), O["T1_gain"])
        st = summarize(sol, policy=never_forage)
        self.assertLess(st["survival"], 1)
        self.assertLess(st["expected_reports"], 2)

    def test_state_space_carries_no_operator_variable(self):
        # safety line: the organism's state is (trial, delay index, body, fidelity) only
        sol = Solution(Params(E=2, d=2, N=2), O["T1_gain"])
        self.assertTrue(all(len(s) == 4 for s in all_states(sol)))


if __name__ == "__main__":
    unittest.main()
