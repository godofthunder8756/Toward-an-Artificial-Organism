"""Ordinary neural and tabular Q learners, with explicit energy objectives."""
import copy
import numpy as np
from .circuits import Adam

OBS_SIZE = 6


class NeuralQ:
    def __init__(self, cfg, rng, frozen=False, fixed_drive=False):
        self.cfg = cfg
        self.p = {'w': rng.normal(0, .25, (OBS_SIZE, cfg.policy_hidden)),
                  'b': np.zeros(cfg.policy_hidden),
                  'v': rng.normal(0, .15, (cfg.policy_hidden, 3)),
                  'd': np.zeros(3)}
        self.target = copy.deepcopy(self.p)
        self.opt = Adam(self.p, cfg.learning_rate)
        self.frozen = frozen
        self.fixed_drive = fixed_drive
        self.buf = []
        self.cursor = 0
        self.updates = 0

    def values(self, x, target=False):
        p = self.target if target else self.p
        h = np.tanh(np.asarray(x) @ p['w'] + p['b'])
        return h @ p['v'] + p['d'], h

    def act(self, obs, explore_u, random_action, training):
        if training and explore_u < self.cfg.exploration:
            return int(random_action)
        return int(np.argmax(self.values(obs)[0]))

    def learn(self, obs, action, reward, next_obs, done, rng):
        if self.frozen:
            return
        item = (obs.copy(), action, reward, next_obs.copy(), done)
        if len(self.buf) < 512:
            self.buf.append(item)
        else:
            self.buf[self.cursor] = item
        self.cursor = (self.cursor + 1) % 512
        if len(self.buf) < 24:
            return
        chosen = rng.integers(0, len(self.buf), 24)
        batch = [self.buf[i] for i in chosen]
        x = np.array([b[0] for b in batch])
        a = np.array([b[1] for b in batch])
        r = np.array([b[2] for b in batch])
        nx = np.array([b[3] for b in batch])
        d = np.array([b[4] for b in batch])
        v, h = self.values(x)
        nv, _ = self.values(nx, target=True)
        target = r + self.cfg.gamma * (1 - d) * nv.max(-1)
        dz = np.zeros_like(v)
        dz[np.arange(len(a)), a] = np.clip(v[np.arange(len(a)), a] - target, -1, 1) / len(a)
        dh = dz @ self.p['v'].T * (1 - h * h)
        g = {'w': x.T @ dh, 'b': dh.sum(0), 'v': h.T @ dz, 'd': dz.sum(0)}
        self.opt.step(self.p, g)
        self.updates += 1
        if self.updates % 40 == 0:
            self.target = copy.deepcopy(self.p)

    def begin_phase(self):
        # Neither a phase-change flag nor a replay reset announces the intervention.
        pass

    @property
    def parameter_count(self):
        return sum(p.size for p in self.p.values())


class TabularQ:
    def __init__(self, cfg):
        self.cfg = cfg
        self.q = np.zeros((6, 2, 3))
        self.frozen = False
        self.fixed_drive = False
        self.updates = 0

    @staticmethod
    def key(obs):
        return min(5, int((obs[0] + 1) * 3)), int(obs[2] > -.5)

    def act(self, obs, explore_u, random_action, training):
        if training and explore_u < self.cfg.exploration:
            return int(random_action)
        return int(np.argmax(self.q[self.key(obs)]))

    def learn(self, obs, action, reward, next_obs, done, rng):
        key = self.key(obs) + (action,)
        target = reward + self.cfg.gamma * (not done) * self.q[self.key(next_obs)].max()
        self.q[key] += .025 * (target - self.q[key])
        self.updates += 1

    def begin_phase(self):
        pass

    @property
    def parameter_count(self):
        return self.q.size
