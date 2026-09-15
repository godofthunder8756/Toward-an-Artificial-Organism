"""Causal/information/resource tests for the AC1 engineering construction."""
import unittest
import numpy as np

from ac1 import ARMS, Body, Config, acquire, decode, decode_actions, observe, run_one, step, world


class TestAC1(unittest.TestCase):
    def test_acquisition_and_no_hidden_body_state(self):
        body, targets, policy, _ = acquire(1, Config())
        np.testing.assert_array_equal(decode(body.traces), targets)
        np.testing.assert_array_equal(decode_actions(body.traces), policy)
        self.assertEqual(set(Body.__slots__), {"traces", "energy", "material", "dead"})
        self.assertFalse(np.shares_memory(targets, body.traces))
        self.assertFalse(np.shares_memory(policy, body.traces))

    def test_all_patterns_majority_repair_without_truth(self):
        c = Config()
        for pattern in range(128):
            body, _, _, _ = acquire(0, c)
            body.traces[2] = 0
            body.traces[2, 0] = [(pattern >> k) & 1 for k in range(7)]
            expected = int(pattern.bit_count() >= 4)
            before = body.traces[2].copy()
            event = step(body, c, np.zeros_like(body.traces), arm="protected", protected_action=4)
            self.assertTrue(np.all(body.traces[2, 0] == expected))
            self.assertEqual(event["writes"], min(pattern.bit_count(), 7 - pattern.bit_count()))
            np.testing.assert_array_equal(decode(before), decode(body.traces[2]))

    def test_no_policy_writes_and_cost_matching(self):
        c = Config()
        original, _, _, _ = acquire(2, c)
        # Current obs maps to repair bank 0 in this teacher when only bank 0 flagged.
        original.traces[0, :6, 0] ^= 1
        a, b = original.copy(), original.copy()
        ea = step(a, c, np.zeros_like(a.traces))
        eb = step(b, c, np.zeros_like(b.traces), arm="no_policy_write")
        self.assertEqual(ea["action"], 2)
        self.assertEqual(ea["spent_e"], eb["spent_e"])
        self.assertEqual(ea["spent_m"], eb["spent_m"])
        self.assertGreater(ea["writes"], 0)
        self.assertEqual(eb["writes"], 0)
        np.testing.assert_array_equal(b.traces, original.traces)

    def test_policy_is_causally_used(self):
        c = Config()
        a, _, _, _ = acquire(3, c)
        a.energy = 40
        obs = observe(a, c)
        b = a.copy()
        for k in range(3):
            i = obs * 3 + k
            b.traces[i // 96, i % 96] = 1  # replace acquired food action with rest
        x = step(a, c, np.zeros_like(a.traces))
        y = step(b, c, np.zeros_like(b.traces))
        self.assertEqual(x["action"], 0)
        self.assertEqual(y["action"], 7)
        self.assertEqual(a.energy - b.energy, c.food_gain)

    def test_erasure_counterfactual_noninterference(self):
        c = Config(ticks=120)
        a, targets_a, _, _ = acquire(1, c)
        b, targets_b, _, _ = acquire(4, c)
        self.assertFalse(np.array_equal(targets_a, targets_b))
        for body in (a, b):
            body.traces[:] = 0
            body.energy, body.material, body.dead = 64, 128, False
        flips, actions, _ = world(9, c)
        for f in flips:
            self.assertEqual(step(a, c, f), step(b, c, f))
            self.assertEqual(a.digest(), b.digest())
        output = decode(a.traces[2:])
        balanced_accuracy = (np.mean(output == targets_a[2:]) + np.mean(output == (1 - targets_a[2:]))) / 2
        self.assertEqual(balanced_accuracy, .5)

    def test_reservoir_rescue_does_not_restore_information(self):
        c = Config()
        a, _, _, _ = acquire(1, c)
        a.traces[:] = 0
        before = a.traces.copy()
        step(a, c, np.zeros_like(a.traces), arm="resource_rescue")
        np.testing.assert_array_equal(before, a.traces)

    def test_no_external_action_for_self(self):
        a, _, _, _ = acquire(0, Config())
        with self.assertRaises(ValueError):
            step(a, Config(), np.zeros_like(a.traces), protected_action=0)

    def test_replay_pairing_and_ledgers(self):
        c = Config(ticks=250, pulse=True)
        inputs = world(3, c)
        rows = [run_one(3, c, arm, inputs) for arm in ARMS]
        self.assertEqual(len({r["env_digest"] for r in rows}), 1)
        self.assertEqual(rows[0], run_one(3, c, "self", inputs))
        for r in rows:
            ledger = r["ledger"]
            self.assertEqual(r["final_energy"], c.energy_start + ledger["in_e"] + ledger["rescue_e"] - ledger["spent_e"] - ledger["overflow_e"])
            self.assertEqual(r["final_material"], c.material_start + ledger["in_m"] + ledger["rescue_m"] - ledger["spent_m"] - ledger["overflow_m"])


if __name__ == "__main__":
    unittest.main()
