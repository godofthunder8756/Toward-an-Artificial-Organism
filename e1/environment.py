"""Fixed-route foraging on a 16 x 16 grid with a genuinely hidden cue sequence.

Movement is scaffolded. The agent chooses a generic collection destination, then
its neural circuit selects one of four food gates. All three resource options
are feasible every active round. The material affects computation, not a score.
"""
import numpy as np

RESOURCE_NAMES = ('basal_food', 'familiar_material', 'precursor')


class World:
    def __init__(self, cfg, circuit, seed, mode, rounds):
        if mode not in ('pre', 'dependency', 'rescue', 'sham', 'lost_usefulness'):
            raise ValueError(f'Unknown intervention: {mode}')
        self.cfg, self.circuit, self.mode = cfg, circuit, mode
        rng = np.random.default_rng(seed)
        self.bits = rng.integers(0, 2, (rounds, 2))
        self.gaps = rng.integers(cfg.gap_min, cfg.gap_max + 1, rounds)
        self.noise = rng.normal(0, cfg.neural_noise,
                                (rounds, cfg.gap_max + 2, cfg.hidden))
        self.explore = rng.random(rounds)
        self.actions = rng.integers(0, 3, rounds)
        # Mirrored placements change compass direction, while distance and action
        # semantics are held fixed. This is a limited held-out world distribution.
        self.mirror = bool(rng.integers(0, 2))
        self.layout = {'hub': (8, 8), 'basal_food': (7, 8),
                       'familiar_material': (8, 7), 'precursor': (9, 8),
                       'cue': (8, 9)}
        if self.mirror:
            self.layout = {k: (15 - x, y) for k, (x, y) in self.layout.items()}
        self.c = np.ones_like(circuit.mask)
        self.energy = cfg.energy_initial
        self.age = 0
        self.index = 0
        self.alive = True
        self.last_activity = np.ones(cfg.hidden) * .5

    @property
    def quality(self):
        return float(self.c[self.circuit.mask.astype(bool)].mean())

    @property
    def task_yield(self):
        return 0.0 if self.mode == 'lost_usefulness' else self.cfg.task_yield

    @property
    def basal_yield(self):
        return .14 if self.mode == 'lost_usefulness' else self.cfg.basal_yield

    def observation(self):
        q = self.quality
        # No mode, trial number, correct gate, next noise, or reward label.
        return np.array([2 * q - 1, 2 * self.energy / self.cfg.energy_cap - 1,
                         2 * self.task_yield / self.cfg.task_yield - 1,
                         2 * self.basal_yield / .14 - 1, 2 * q*q - 1, 1.0])

    def route(self, gap, action):
        """Actual scaffolded path, including detour and return, on the bounded grid."""
        hub = (8, 8)
        offers = ((7, 8), (8, 7), (9, 8))
        corridor = [(8, 9), (8, 10), (8, 11), (8, 12),
                    (8, 13), (8, 14), (9, 14), (10, 14)]
        outbound = corridor[:gap + 2]
        path = [hub, offers[action], hub] + outbound + list(reversed([hub] + outbound[:-1]))
        if self.mirror:
            path = [(15 - x, y) for x, y in path]
        return path

    def step(self, action):
        if not self.alive:
            raise RuntimeError('Cannot act after the simulated termination boundary')
        if action not in (0, 1, 2):
            raise ValueError('Collection action must index one of the three adjacent offers')
        cfg = self.cfg
        t = self.index
        before_q = self.quality
        # Activity-dependent edge wear and local repair allocation.
        edge_activity = np.sqrt(np.outer(self.last_activity, self.last_activity))
        wear = cfg.wear * (.7 + .6 * edge_activity)
        self.c = np.maximum(.015, self.c - wear * self.circuit.mask)
        repair_amount = np.zeros_like(self.c)
        if action == 1 and self.mode == 'pre':
            repair_amount = .25 * (.8 + .4 * edge_activity) * self.circuit.mask
        if action == 2 and self.mode != 'sham':
            repair_amount = cfg.repair * (.8 + .4 * edge_activity) * self.circuit.mask
        # Material application is automatic chemistry, not a learned repair action.
        before_repair = self.c.copy()
        self.c = np.minimum(1, self.c + repair_amount)
        used = float(np.sum(self.c - before_repair) / self.circuit.mask.sum())
        external = 0.0
        if self.mode in ('pre', 'rescue'):
            external = float(np.mean(1 - self.c[self.circuit.mask.astype(bool)]))
            self.c[:] = 1
        used_q = self.quality
        answer, activity = self.circuit.recall(self.bits[t], int(self.gaps[t]),
                                               self.c, self.noise[t])
        success = answer == int(2 * self.bits[t, 0] + self.bits[t, 1])
        # Grid path: step to adjacent offer and back; from hub to cue, along a
        # blank corridor, then return. Energy is charged per traversed cell.
        distance = len(self.route(int(self.gaps[t]), action)) - 1
        traversal_cost = .002 * distance
        gain = (self.basal_yield if action == 0 else .025 if action == 1 else 0.0)
        gain += self.task_yield * success
        cost = cfg.living_cost + traversal_cost + cfg.activity_cost * float(activity.mean())
        if action == 2:
            cost += cfg.precursor_cost
        old_energy = self.energy
        self.energy = float(np.clip(self.energy + gain - cost, 0, cfg.energy_cap))
        net_energy = gain - cost
        self.alive = self.energy > 0
        self.last_activity = activity
        self.age += 1
        self.index += 1
        row = {'trial': t, 'action': action, 'precursor': int(action == 2),
               'q_before': before_q, 'q_used': used_q, 'q_after': self.quality,
               'precursor_used': used if action == 2 else 0.0,
               'external_repair': external, 'neural_activity': float(activity.mean()),
               'gap': int(self.gaps[t]), 'distance': distance,
               'cue_a': int(self.bits[t, 0]), 'cue_b': int(self.bits[t, 1]),
               'door': answer, 'success': int(success), 'energy_before': old_energy,
               'energy_after': self.energy, 'net_energy': net_energy,
               'energy_delta': self.energy - old_energy, 'alive_after': int(self.alive)}
        return self.observation(), net_energy, not self.alive, row
