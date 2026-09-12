"""Independent pure-policy fixtures, not paid services or experimental runs."""

from dataclasses import FrozenInstanceError, fields, replace
from itertools import product
import unittest
from unittest.mock import patch

from e3.policy import (
    ENERGY_CUTS,
    MATERIAL_CUTS,
    PERIODS,
    Policy,
    PolicyConfig,
    decide,
    policy_action_return,
)
from e3.protocol import Policy as CodecPolicy, PublicConfiguration


# Literal actions at s=0..31, independent of production predicates/bit unpacking.
# Each group of four fixes (u,e,p), with h=0,1,2,3 in that order.
NO_MAINT = (
    0, 0, 0, 0,  0, 0, 0, 0,  1, 1, 1, 1,  0, 0, 0, 0,
    0, 0, 0, 0,  0, 0, 0, 0,  1, 1, 1, 1,  0, 0, 0, 0,
)
PERIODIC_DUE = (
    0, 0, 0, 0,  0, 0, 0, 0,  1, 1, 1, 1,  2, 2, 2, 2,
    0, 0, 0, 0,  0, 0, 0, 0,  1, 1, 1, 1,  2, 2, 2, 2,
)
THRESHOLD = (
    0, 0, 0, 0,  0, 0, 0, 0,  1, 1, 1, 1,  0, 0, 0, 2,
    0, 0, 0, 0,  0, 0, 0, 0,  1, 1, 1, 1,  0, 0, 0, 2,
)
SCRIPT_U = (
    0, 0, 0, 0,  0, 0, 0, 0,  1, 1, 1, 1,  0, 0, 0, 0,
    0, 0, 0, 0,  0, 0, 0, 0,  1, 1, 1, 1,  0, 0, 0, 2,
)
SCRIPT_ALL = (
    0, 0, 0, 0,  0, 0, 0, 0,  1, 1, 1, 1,  0, 0, 0, 2,
    0, 0, 0, 0,  0, 0, 0, 0,  1, 1, 1, 1,  0, 0, 0, 2,
)


class TestPolicyConfig(unittest.TestCase):
    def test_defaults_and_exact_grid(self):
        self.assertEqual(ENERGY_CUTS, (24576, 32768, 40960))
        self.assertEqual(MATERIAL_CUTS, (32, 64, 96))
        self.assertEqual(PERIODS, (1, 2, 4, 8, 16, 32, 64, 128, 256))
        self.assertEqual(PolicyConfig(), PolicyConfig(Policy.RL, 32768, 64, 0))
        self.assertEqual(PolicyConfig(Policy.PERIODIC).interval, 8)
        for policy in (Policy.RL, Policy.THRESHOLD, Policy.NO_MAINT):
            configs = {PolicyConfig(policy, e, p) for e, p in product(ENERGY_CUTS, MATERIAL_CUTS)}
            self.assertEqual(len(configs), 9)
            self.assertTrue(all(config.interval == 0 for config in configs))
        configs = {PolicyConfig(Policy.PERIODIC, e, p, i)
                   for e, p, i in product(ENERGY_CUTS, MATERIAL_CUTS, PERIODS)}
        self.assertEqual(len(configs), 81)
        for policy in (Policy.DRIVE, Policy.SCRIPT_U, Policy.SCRIPT_ALL):
            for e, p in product(ENERGY_CUTS, MATERIAL_CUTS):
                if (e, p) == (32768, 64):
                    self.assertEqual(PolicyConfig(policy, e, p).interval, 0)
                else:
                    with self.assertRaises(ValueError):
                        PolicyConfig(policy, e, p)

    def test_immutable_inherited_constants_no_acquired_storage(self):
        config = PolicyConfig(Policy.PERIODIC)
        self.assertFalse(hasattr(config, "__dict__"))
        self.assertEqual(tuple(field.name for field in fields(config)),
                         ("policy", "energy_cut", "material_cut", "interval"))
        for name, value in (("policy", Policy.DRIVE), ("energy_cut", 24576),
                            ("material_cut", 32), ("interval", 16)):
            with self.assertRaises(FrozenInstanceError):
                setattr(config, name, value)
        for name in ("q_values", "history", "seed", "target", "counter"):
            with self.assertRaises((AttributeError, TypeError)):
                setattr(config, name, ())
        changed = replace(config, interval=16)
        self.assertEqual(config.interval, 8)
        self.assertEqual(changed.interval, 16)
        with self.assertRaises(ValueError):
            replace(config, interval=3)

    def test_component_names_are_not_codec_ids_or_frozen_permission(self):
        self.assertEqual({item.name: item.value for item in Policy}, {
            "RL": "RL", "PERIODIC": "PERIODIC", "THRESHOLD": "THRESHOLD",
            "NO_MAINT": "NO_MAINT", "DRIVE": "DRIVE", "SCRIPT_U": "SCRIPT_U",
            "SCRIPT_ALL": "SCRIPT_ALL",
        })
        self.assertEqual({item.name: item.value for item in CodecPolicy}, {
            "RL": 0, "PERIODIC": 1, "THRESHOLD": 2, "DRIVE": 3,
            "FROZEN": 4, "SCRIPT_U": 5, "SCRIPT_ALL": 6,
        })
        self.assertNotIn("NO_MAINT", CodecPolicy.__members__)
        self.assertNotIn("FROZEN", Policy.__members__)
        for member in CodecPolicy:
            with self.assertRaises(TypeError):
                PolicyConfig(member)
        for identifier in range(404):
            # Catalog authority remains in the existing codec, not this component.
            self.assertNotEqual(PublicConfiguration(identifier).policy.name, "NO_MAINT")

    def test_reject_noninteger_nonmember_and_out_of_grid_constants(self):
        class IntSubclass(int):
            pass

        for bad in (True, False, "RL", 0, None, object()):
            with self.assertRaises(TypeError):
                PolicyConfig(bad)
        for field in ("energy_cut", "material_cut", "interval"):
            bad_values = (True, False, 1.0, "1", IntSubclass(1))
            if field != "interval":
                bad_values += (None,)
            for bad in bad_values:
                with self.assertRaises(TypeError):
                    PolicyConfig(Policy.PERIODIC, **{field: bad})
        for field, bad_values in (("energy_cut", (-1, 0, 32767, 65535, 65536)),
                                  ("material_cut", (-1, 0, 63, 255, 256)),
                                  ("interval", (-1, 0, 3, 7, 255, 257, 512))):
            for bad in bad_values:
                with self.assertRaises(ValueError):
                    PolicyConfig(Policy.PERIODIC, **{field: bad})
        for policy in Policy:
            if policy is not Policy.PERIODIC:
                with self.assertRaises(ValueError):
                    PolicyConfig(policy, interval=8)


class TestPolicyDecision(unittest.TestCase):
    def test_full_32_state_fixed_and_script_literal_truth_tables(self):
        cases = ((Policy.NO_MAINT, 1, NO_MAINT),
                 (Policy.PERIODIC, 1, PERIODIC_DUE),
                 (Policy.PERIODIC, 2, NO_MAINT),
                 (Policy.THRESHOLD, 1, THRESHOLD),
                 (Policy.SCRIPT_U, 1, SCRIPT_U),
                 (Policy.SCRIPT_ALL, 1, SCRIPT_ALL))
        with patch("e3.arithmetic.select_action", side_effect=AssertionError("unused selection")):
            for policy, tick, expected in cases:
                self.assertEqual(len(expected), 32)
                for row, ranks in product(((-32768, 0, 32767), (32767, 32767, -32768)),
                                           ((0, 0, 0), (1, 2, 15))):
                    with self.subTest(policy=policy, tick=tick, row=row, ranks=ranks):
                        actual = tuple(decide(PolicyConfig(policy), s, row, tick, *ranks)
                                       for s in range(32))
                        self.assertEqual(actual, expected)
                        self.assertTrue(all(type(action) is int for action in actual))

    def test_every_period_with_independent_due_tick_sets(self):
        for interval in PERIODS:
            config = PolicyConfig(Policy.PERIODIC, interval=interval)
            due_ticks = set(range(1, 2050, interval))  # Not the production bit predicate.
            for tick in range(1, 2050):
                expected = PERIODIC_DUE if tick in due_ticks else NO_MAINT
                actual = tuple(decide(config, s, (0, 0, 0), tick, 0, 0, 1)
                               for s in range(32))
                self.assertEqual(actual, expected)
            due_ticks = set(range(1, 65536, interval))
            for tick in (255, 256, 257, 512, 513, 2048, 2049, 32769, 65535):
                self.assertEqual(decide(config, 31, (0, 0, 0), tick, 0, 0, 1),
                                 2 if tick in due_ticks else 0)

    def test_planned_clock_has_no_cursor_retry_or_history(self):
        config = PolicyConfig(Policy.PERIODIC)
        # Repeats, skipped offers, out-of-order fixture calls and phase restarts.
        ticks = (17, 2, 9, 9, 8, 10, 1, 2048, 2049, 1)
        expected = (2, 0, 2, 2, 0, 0, 2, 0, 2, 2)
        self.assertEqual(tuple(decide(config, 12, (0, 0, 0), tick, 1, 2, 15)
                               for tick in ticks), expected)

    def test_rl_and_drive_full_32_states_and_all_rank_inputs(self):
        # Explicit maximizing sets via B lookup; three-way ties use T.
        rows = (((32767, -32768, -32768), (0, 0)),
                ((-32768, 32767, -32768), (1, 1)),
                ((-32768, -32768, 32767), (2, 2)),
                ((32767, 32767, -32768), (0, 1)),
                ((32767, -32768, 32767), (0, 2)),
                ((-32768, 32767, 32767), (1, 2)),
                ((-32768, -32768, -32768), None))
        for policy, (row, exploit), b, t, x in product(
                (Policy.RL, Policy.DRIVE), rows, range(2), range(3), range(16)):
            expected = t if x == 0 or exploit is None else exploit[b]
            actual = tuple(decide(PolicyConfig(policy), s, row, 1, b, t, x)
                           for s in range(32))
            self.assertEqual(actual, (expected,) * 32)

    def test_current_damaged_row_delegation_without_cache_or_override(self):
        for policy in (Policy.RL, Policy.DRIVE):
            config = PolicyConfig(policy)
            rows = ((0, 2, 0), (0, 2, 3), (-32768, 32767, -1), (5, 0, 5))
            self.assertEqual(tuple(decide(config, 0, row, 1, 1, 1, 1) for row in rows),
                             (1, 2, 1, 2))
            with patch("e3.arithmetic.select_action", return_value=2) as select:
                self.assertEqual(decide(config, 0, rows[0], 1, 1, 2, 15), 2)
                select.assert_called_once_with(rows[0], 1, 2, 15)
            self.assertEqual(rows[0], (0, 2, 0))

    def test_cuts_are_upstream_constants_not_another_observation(self):
        for policy, expected in ((Policy.NO_MAINT, NO_MAINT),
                                 (Policy.PERIODIC, PERIODIC_DUE),
                                 (Policy.THRESHOLD, THRESHOLD)):
            for e, p in product(ENERGY_CUTS, MATERIAL_CUTS):
                config = PolicyConfig(policy, e, p)
                self.assertEqual(tuple(decide(config, s, (0, 0, 0), 1, 0, 0, 1)
                                       for s in range(32)), expected)

    def test_strict_inputs_even_for_nonlearning_and_unused_paths(self):
        for policy in Policy:
            config = PolicyConfig(policy)
            good = {"state_index": 0, "q_values": (0, 0, 0), "phase_tick": 1,
                    "b": 0, "t": 0, "x": 1}
            for name in ("state_index", "phase_tick", "b", "t", "x"):
                for bad in (True, False, 1.0, "1", None):
                    with self.assertRaises(TypeError):
                        decide(config, **{**good, name: bad})
            for name, bads in (("state_index", (-1, 32)), ("phase_tick", (0, -1, 65536)),
                               ("b", (-1, 2)), ("t", (-1, 3)), ("x", (-1, 16))):
                for bad in bads:
                    with self.assertRaises(ValueError):
                        decide(config, **{**good, name: bad})
            for row in ([0, 0, 0], "000", None, iter((0, 0, 0))):
                with self.assertRaises(TypeError):
                    decide(config, **{**good, "q_values": row})
            for row in ((), (0,), (0, 0), (0, 0, 0, 0)):
                with self.assertRaises(ValueError):
                    decide(config, **{**good, "q_values": row})
            for position in range(3):
                for bad in (True, False, 0.0, "0", None, -32769, 32768):
                    row = [0, 0, 0]
                    row[position] = bad
                    error = ValueError if type(bad) is int else TypeError
                    with self.assertRaises(error):
                        decide(config, **{**good, "q_values": tuple(row)})
            for name in ("history", "target", "seed", "individual_id", "success", "h"):
                with self.assertRaises(TypeError):
                    decide(config, **{**good, name: 0})
        for config in (None, Policy.RL, "RL", 0):
            with self.assertRaises(TypeError):
                decide(config, 0, (0, 0, 0), 1, 0, 0, 1)


class TestPolicyReturn(unittest.TestCase):
    def test_all_completed_prefixes_main_and_drive(self):
        for policy, n in product(Policy, (5, 20)):
            config = PolicyConfig(policy)
            for energy in range(65):
                self.assertEqual(policy_action_return(config, 0, accepted_energy=energy, n=n),
                                 0 if policy is Policy.DRIVE else energy // 4)
            for material in range(9):
                self.assertEqual(policy_action_return(config, 1, accepted_material=material, n=n),
                                 0 if policy is Policy.DRIVE else 2 * material)
            for writes in range(n + 1):
                self.assertEqual(policy_action_return(config, 2, completed_writes=writes, n=n),
                                 16 if policy is Policy.DRIVE else -writes)
            self.assertEqual(policy_action_return(config, None, n=n), 0)
            # Informational values cannot create records or certify a paid gate.
            for reason in ("rejected-action", "empty", "tied", "clean", "prohibited"):
                with self.subTest(policy=policy, reason=reason):
                    self.assertEqual(policy_action_return(config, 2, n=n),
                                     16 if policy is Policy.DRIVE else 0)

    def test_return_strict_validation_including_ignored_drive_counts(self):
        for policy in Policy:
            config = PolicyConfig(policy)
            for bad in (True, False, 1.0, "2"):
                with self.assertRaises(TypeError):
                    policy_action_return(config, bad)
            for bad in (-1, 3):
                with self.assertRaises(ValueError):
                    policy_action_return(config, bad)
            for name in ("accepted_energy", "accepted_material", "completed_writes", "n"):
                for bad in (True, False, 1.0, "1", None):
                    with self.assertRaises(TypeError):
                        policy_action_return(config, 2, **{name: bad})
            for action in (None, 0, 1, 2):
                for index, name in enumerate(("accepted_energy", "accepted_material", "completed_writes")):
                    if index != action:
                        with self.assertRaises(ValueError):
                            policy_action_return(config, action, **{name: 1})
            for kwargs in ({"accepted_energy": 65}, {"accepted_energy": -1},
                           {"accepted_material": 9}, {"accepted_material": -1},
                           {"completed_writes": 21}, {"completed_writes": -1},
                           {"completed_writes": 6, "n": 5}, {"n": 6}):
                with self.assertRaises(ValueError):
                    policy_action_return(config, 2, **kwargs)
        with self.assertRaises(TypeError):
            policy_action_return(Policy.DRIVE, 2)


if __name__ == "__main__":
    unittest.main()