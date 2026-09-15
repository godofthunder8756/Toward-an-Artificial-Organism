import unittest
import numpy as np
import ac2


class TestAC2(unittest.TestCase):
    def test_acquisition_and_state(self):
        b, targets, p, _ = ac2.acquire(0, ac2.Config())
        np.testing.assert_array_equal(ac2.decode(b.traces), targets)
        np.testing.assert_array_equal(ac2.policy(b.traces), p)
        self.assertEqual(set(ac2.Body.__slots__), {"traces", "catalysts", "energy", "material", "dead"})

    def test_zero_catalyst_prevents_write(self):
        c = ac2.Config()
        b, _, _, _ = ac2.acquire(0, c)
        b.traces[0, :10, 0] ^= 1
        a = b.copy()
        b.catalysts[:] = 0
        ea, eb = ac2.event_zero(), ac2.event_zero()
        ac2.react(a, c, 2, ea, "self")
        ac2.react(b, c, 2, eb, "self")
        self.assertEqual(ea["writes"], 10)
        self.assertEqual(eb["writes"], 0)
        self.assertEqual(eb["write_e"], 0)

    def test_birth_requires_parent_and_substrate(self):
        c = ac2.Config()
        b, _, _, _ = ac2.acquire(0, c)
        parents = b.catalysts.copy()
        e = ac2.event_zero()
        ac2.react(b, c, 6, e, "self")
        self.assertEqual(e["births"], 4)
        self.assertEqual(e["synthesis_m"], 16)
        self.assertEqual(e["synthesis_e"], 8)
        np.testing.assert_array_equal(b.catalysts[:, :3], parents[:, :3])
        for no_parent, no_material in ((True, False), (False, True)):
            a, _, _, _ = ac2.acquire(0, c)
            if no_parent:
                a.catalysts[:] = 0
            if no_material:
                a.material = 0
            e = ac2.event_zero()
            ac2.react(a, c, 6, e, "self")
            self.assertEqual(e["births"], 0)

    def test_lifetime_and_no_production(self):
        c = ac2.Config(ticks=70)
        b, _, _, _ = ac2.acquire(0, c)
        expired = 0
        for _ in range(64):
            e = ac2.step(b, c, np.zeros_like(b.traces), "no_synthesis_clamp")
            expired += e["expired"]
        self.assertEqual(expired, 12)
        self.assertEqual(np.count_nonzero(b.catalysts), 0)
        self.assertFalse(b.dead)

    def test_policy_controls_catalyst_production(self):
        c = ac2.Config()
        a, _, _, _ = ac2.acquire(0, c)
        a.catalysts[:, 1:] = 0
        a.catalysts[:, 0] = 60
        b = a.copy()
        obs = ac2.observe(b)
        self.assertEqual(ac2.policy(b.traces)[obs], 6)
        for k in range(3):
            i = obs * 3 + k
            b.traces[i // 192, i % 192] = 1  # rest instead of synthesis
        ea = ac2.step(a, c, np.zeros_like(a.traces))
        eb = ac2.step(b, c, np.zeros_like(b.traces))
        self.assertEqual(ea["births"], 4)
        self.assertEqual(eb["births"], 0)

    def test_complete_erasure_and_external_template_rejection(self):
        c = ac2.Config(ticks=80)
        a, _, _, _ = ac2.acquire(1, c)
        b, _, _, _ = ac2.acquire(2, c)
        for x in (a, b):
            x.traces[:] = 0
            x.catalysts[:] = 0
            x.energy, x.material, x.dead = 64, 128, False
        flips, _ = ac2.world(4, c)
        for f in flips:
            self.assertEqual(ac2.step(a, c, f), ac2.step(b, c, f))
            self.assertEqual(a.digest(), b.digest())
        with self.assertRaises(ValueError):
            ac2.step(a, c, flips[0], protected_policy=np.zeros(128))

    def test_atomic_and_total_ledgers_replay(self):
        c = ac2.Config(ticks=160)
        inputs = ac2.world(0, c)
        rows = [ac2.run_one(0, c, arm, inputs) for arm in ac2.ARMS]
        self.assertEqual(len({r["env_digest"] for r in rows}), 1)
        self.assertEqual(rows[0], ac2.run_one(0, c, "self", inputs))
        for r in rows:
            e = r["ledger"]
            self.assertEqual(c.material_start + 12 * 4 + e["in_m"] + e["clamp_m"] + 4 * e["external_births"],
                             r["final_material"] + 4 * r["final_catalysts"] + e["write_m"] + 4 * e["expired"] + e["overflow_m"])
            self.assertEqual(c.energy_start + e["in_e"] + e["clamp_e"],
                             r["final_energy"] + e["living_e"] + e["write_e"] + e["synthesis_e"] + e["overflow_e"])


if __name__ == "__main__":
    unittest.main()
