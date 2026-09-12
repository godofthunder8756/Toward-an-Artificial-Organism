"""Mechanism and numerical tests: python -m unittest -v test_e1."""
import copy
import unittest
import numpy as np

from e1.circuits import Circuit, stimuli
from e1.config import Config
from e1.control import NeuralQ
from e1.environment import World


class Mechanisms(unittest.TestCase):
    def setUp(self):
        self.cfg = Config(hidden=5, memory_batch_size=8)
        self.circuit = Circuit(self.cfg, np.random.default_rng(5))

    def test_bptt_matches_finite_difference_with_variable_gaps(self):
        rng = np.random.default_rng(91)
        bits = rng.integers(0, 2, (4, 2))
        gaps = np.array([3, 4, 5, 6])
        x = stimuli(bits, gaps)
        noise = rng.normal(0, .06, (len(x), 4, 5))
        actions = np.array([0, 1, 2, 3])
        success = np.array([1., 0., 1., 1.])
        _, grads = self.circuit.loss_grads(x, gaps, noise, actions, success)
        for k, param in self.circuit.p.items():
            for index in list(np.ndindex(param.shape))[:12]:
                if k == 'w' and self.circuit.mask[index] == 0:
                    continue
                old = param[index]
                param[index] = old + 1e-5
                plus = self.circuit.loss_grads(x, gaps, noise, actions, success)[0]
                param[index] = old - 1e-5
                minus = self.circuit.loss_grads(x, gaps, noise, actions, success)[0]
                param[index] = old
                self.assertAlmostEqual((plus-minus)/2e-5, grads[k][index], places=5)

    def test_hidden_target_and_intervention_do_not_leak_into_observation(self):
        a = World(self.cfg, self.circuit, 8, 'pre', 20)
        b = World(self.cfg, self.circuit, 99, 'dependency', 20)
        np.testing.assert_array_equal(a.observation(), b.observation())
        a.bits[:] = 1 - a.bits
        np.testing.assert_array_equal(a.observation(), b.observation())

    def test_blanks_contain_no_target(self):
        x = stimuli(np.array([[0, 1], [1, 0]]), np.array([4, 4]))
        self.assertTrue(np.all(x[2:] == 0))
        np.testing.assert_array_equal(x[-1, 0], x[-1, 1])

    def test_causal_repair_rescue_and_sham(self):
        worlds = {m: World(self.cfg, self.circuit, 8, m, 20)
                  for m in ('dependency', 'rescue', 'sham')}
        for w in worlds.values():
            w.c[:] = .15
        rows = {k: w.step(2)[3] for k, w in worlds.items()}
        self.assertGreater(rows['dependency']['q_used'], rows['sham']['q_used'] + .5)
        self.assertEqual(rows['sham']['precursor_used'], 0)
        self.assertAlmostEqual(rows['rescue']['q_used'], 1)
        self.assertGreater(rows['rescue']['external_repair'], 0)

    def test_pairing_noise_is_not_shifted_by_different_actions(self):
        a = World(self.cfg, self.circuit, 8, 'dependency', 20)
        b = World(self.cfg, self.circuit, 8, 'sham', 20)
        a.step(0)
        b.step(2)
        np.testing.assert_array_equal(a.noise, b.noise)
        np.testing.assert_array_equal(a.bits, b.bits)

    def test_frozen_weights_and_identical_exploration(self):
        p = NeuralQ(self.cfg, np.random.default_rng(8))
        frozen = copy.deepcopy(p)
        frozen.frozen = True
        obs = np.ones(6) * .5
        self.assertEqual(p.act(obs, 0, 2, True), frozen.act(obs, 0, 2, True))
        before = copy.deepcopy(frozen.p)
        for _ in range(30):
            frozen.learn(obs, 2, 1, obs, False, np.random.default_rng(1))
        for k in before:
            np.testing.assert_array_equal(before[k], frozen.p[k])

    def test_conductance_gates_actual_recurrence(self):
        x = stimuli(np.array([[0, 1], [1, 0]]), np.array([4, 4]))
        noise = np.zeros((len(x), 2, self.cfg.hidden))
        intact = self.circuit.forward(x, np.array([4, 4]), 1., noise)[0]
        lesioned = self.circuit.forward(x, np.array([4, 4]), 1., noise, True)[0]
        no_conductance = self.circuit.forward(x, np.array([4, 4]), 0., noise)[0]
        self.assertFalse(np.allclose(intact, lesioned))
        np.testing.assert_array_equal(lesioned, no_conductance)
        # With no recurrent route and identical blank endpoint observations,
        # different hidden cue sequences yield exactly identical logits.
        np.testing.assert_array_equal(lesioned[0], lesioned[1])

    def test_replay_reward_receives_no_precursor_label(self):
        p = NeuralQ(self.cfg, np.random.default_rng(8))
        w = World(self.cfg, self.circuit, 8, 'dependency', 20)
        obs = w.observation()
        nxt, reward, done, row = w.step(2)
        p.learn(obs, 2, reward, nxt, done, np.random.default_rng(2))
        self.assertEqual(p.buf[-1][2], row['net_energy'])

    def test_dead_agent_cannot_act(self):
        w = World(self.cfg, self.circuit, 8, 'lost_usefulness', 20)
        w.energy = .0001
        w.step(2)
        self.assertFalse(w.alive)
        with self.assertRaises(RuntimeError):
            w.step(0)

    def test_scaffolded_paths_stay_inside_world_and_charge_each_step(self):
        for seed in range(4):
            w = World(self.cfg, self.circuit, seed, 'dependency', 20)
            for gap in range(self.cfg.gap_min, self.cfg.gap_max + 1):
                for action in range(3):
                    path = w.route(gap, action)
                    self.assertEqual(len(path) - 1, 2 + 2 * (gap + 2))
                    self.assertTrue(all(0 <= x < 16 and 0 <= y < 16 for x, y in path))
                    self.assertEqual(path[0], path[-1])
                    self.assertTrue(all(abs(x-a) + abs(y-b) == 1
                                        for (x, y), (a, b) in zip(path, path[1:])))


if __name__ == '__main__':
    unittest.main()
