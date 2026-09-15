import unittest
import numpy as np
import ac3


class TestAC3(unittest.TestCase):
    def test_acquisition_and_state(self):
        b, targets, p, _ = ac3.acquire(0, ac3.Config())
        np.testing.assert_array_equal(ac3.decode(b.traces), targets)
        np.testing.assert_array_equal(ac3.policy(b.traces), p)
        self.assertEqual(set(ac3.Body.__slots__), {"traces", "catalysts", "converters", "fuel", "energy", "material", "dead"})

    def test_fuel_collection_not_energy(self):
        c = ac3.Config()
        b, _, _, _ = ac3.acquire(0, c)
        e = ac3.event_zero()
        initial_energy, initial_fuel = b.energy, b.fuel
        ac3.react(b, c, 0, e, "self")
        self.assertEqual(b.energy, initial_energy - 1)
        self.assertEqual(b.fuel, initial_fuel + c.fuel_gain)
        self.assertEqual(e["in_e"], 0)

    def test_conversion_dependency_and_zero_energy_restart(self):
        c = ac3.Config()
        b, _, _, _ = ac3.acquire(0, c)
        b.energy = 0
        a = b.copy()
        a.converters[:] = 0
        ea = ac3.step(a, c, np.zeros_like(a.traces))
        eb = ac3.step(b, c, np.zeros_like(b.traces))
        self.assertEqual(ea["converted"], 0)
        self.assertTrue(a.dead)
        self.assertGreater(eb["converted"], 0)
        self.assertEqual(eb["active"], 1)
        self.assertFalse(b.dead)

    def test_converter_requires_W_material_energy(self):
        c = ac3.Config()
        for missing in (None, "W", "M", "E"):
            b, _, _, _ = ac3.acquire(0, c)
            if missing == "W": b.catalysts[:] = 0
            if missing == "M": b.material = 0
            if missing == "E": b.energy = 1
            e = ac3.event_zero()
            ac3.react(b, c, 7, e, "self")
            self.assertEqual(e["C_births"], int(missing is None))
            self.assertEqual(e["C_synthesis_m"], 4 * int(missing is None))
            self.assertEqual(e["C_synthesis_e"], 4 * int(missing is None))

    def test_policy_controls_converter_production(self):
        c = ac3.Config()
        a, _, _, _ = ac3.acquire(0, c)
        a.converters[:] = [100, 0, 0, 0]
        b = a.copy()
        obs = ac3.observe(b)
        self.assertEqual(ac3.policy(b.traces)[obs], 7)
        for k in range(4):
            i = obs * 4 + k
            b.traces[i // 512, i % 512] = (8 >> k) & 1
        ea = ac3.step(a, c, np.zeros_like(a.traces))
        eb = ac3.step(b, c, np.zeros_like(b.traces))
        self.assertEqual(ea["C_births"], 1)
        self.assertEqual(eb["C_births"], 0)

    def test_C_expires_without_production(self):
        c = ac3.Config()
        b, _, _, _ = ac3.acquire(0, c)
        total = 0
        for _ in range(128):
            e = ac3.step(b, c, np.zeros_like(b.traces), "no_C_energy")
            total += e["C_expired"]
        self.assertEqual(total, 3)
        self.assertEqual(np.count_nonzero(b.converters), 0)
        self.assertFalse(b.dead)

    def test_full_reset_no_template(self):
        c = ac3.Config(ticks=80)
        a, _, _, _ = ac3.acquire(1, c)
        b, _, _, _ = ac3.acquire(2, c)
        for x in (a, b):
            x.traces[:] = 0
            x.catalysts[:] = 0
            x.converters[:] = 0
            x.fuel, x.energy, x.material, x.dead = 0, 64, 128, False
        flips, _ = ac3.world(3, c)
        for f in flips:
            self.assertEqual(ac3.step(a, c, f), ac3.step(b, c, f))
            self.assertEqual(a.digest(), b.digest())
        with self.assertRaises(ValueError):
            ac3.step(a, c, flips[0], protected_policy=np.zeros(256))

    def test_total_ledgers_and_replay(self):
        c = ac3.Config(ticks=160)
        inputs = ac3.world(0, c)
        rows = [ac3.run_one(0, c, a, inputs) for a in ac3.ARMS]
        self.assertEqual(len({r["env_digest"] for r in rows}), 1)
        self.assertEqual(rows[0], ac3.run_one(0, c, "self", inputs))
        for r in rows:
            e = r["ledger"]
            self.assertEqual(c.fuel_start + e["in_f"], r["final_fuel"] + e["converted"] + e["overflow_f"])
            self.assertEqual(c.energy_start + e["clamp_e"] + 8 * e["converted"], r["final_energy"] + e["living_e"] + e["write_e"] + e["synthesis_e"] + e["C_synthesis_e"])
            self.assertEqual(c.material_start + 4 * 15 + e["in_m"] + 4 * e["external_C"], r["final_material"] + 4 * (r["final_W"] + r["final_C"]) + e["write_m"] + 4 * (e["expired"] + e["C_expired"]) + e["overflow_m"])


if __name__ == "__main__":
    unittest.main()
