"""A sparse, learned recurrent circuit. Conductance gates actual recurrent edges.

Topology and repair rules are designed. Weight learning is global BPTT, not local
autopoiesis. Rewarded uniform exploration trains the initial recall capability.
Only successful attempted door choices enter the gradient, never hidden labels.
"""
import numpy as np


class Adam:
    def __init__(self, params, lr):
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t = 0
        self.lr = lr

    def step(self, params, grads, clip=5.0):
        norm = np.sqrt(sum(np.sum(g * g) for g in grads.values()))
        scale = min(1.0, clip / max(norm, 1e-12))
        self.t += 1
        for k, g in grads.items():
            g = g * scale
            self.m[k] = .9 * self.m[k] + .1 * g
            self.v[k] = .999 * self.v[k] + .001 * g * g
            params[k] -= self.lr * (self.m[k] / (1 - .9**self.t)) / (
                np.sqrt(self.v[k] / (1 - .999**self.t)) + 1e-8)


def softmax(x):
    z = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return z / z.sum(axis=-1, keepdims=True)


def stimuli(bits, gaps):
    """Two sequential bits followed by blanks; no answer in final observation."""
    n = len(bits)
    x = np.zeros((int(max(gaps)) + 2, n, 2))
    x[0, :, 0] = 2 * bits[:, 0] - 1
    x[1, :, 1] = 2 * bits[:, 1] - 1
    return x


class Circuit:
    def __init__(self, cfg, rng):
        self.cfg = cfg
        h = cfg.hidden
        self.mask = (rng.random((h, h)) < .35).astype(float)
        np.fill_diagonal(self.mask, 1)
        self.p = {
            'u': rng.normal(0, .45, (2, h)),
            'w': rng.normal(0, 1.25 / np.sqrt(h * .35), (h, h)) * self.mask,
            'b': np.zeros(h),
            'v': rng.normal(0, .20, (h, 4)),
            'd': np.zeros(4),
        }
        self.opt = Adam(self.p, .007)

    def forward(self, x, gaps, conductance, noise, lesion=False):
        n = x.shape[1]
        h = np.zeros((n, self.cfg.hidden))
        states = [h.copy()]
        active_masks = []
        effective_w = self.p['w'] * conductance * (not lesion)
        for t in range(len(x)):
            active = (t < gaps + 2)[:, None]
            proposal = np.tanh(x[t] @ self.p['u'] + h @ effective_w + self.p['b'] + noise[t])
            h = np.where(active, proposal, h)
            states.append(h.copy())
            active_masks.append(active)
        return softmax(h @ self.p['v'] + self.p['d']), states, active_masks

    def loss_grads(self, x, gaps, noise, actions, success):
        probs, states, active = self.forward(x, gaps, 1.0, noise)
        n = x.shape[1]
        # Uniform exploration propensity is 1/4. Its inverse produces an
        # unbiased estimate of the full success-conditioned classification loss.
        weight = 4.0 * success / n
        loss = -np.sum(weight * np.log(probs[np.arange(n), actions] + 1e-12))
        dz = probs.copy()
        dz[np.arange(n), actions] -= 1
        dz *= weight[:, None]
        g = {k: np.zeros_like(v) for k, v in self.p.items()}
        g['v'] = states[-1].T @ dz
        g['d'] = dz.sum(0)
        dh = dz @ self.p['v'].T
        for t in reversed(range(len(x))):
            da = dh * (1 - states[t + 1]**2) * active[t]
            g['u'] += x[t].T @ da
            g['w'] += states[t].T @ da * self.mask
            g['b'] += da.sum(0)
            dh = da @ self.p['w'].T + dh * ~active[t]
        return loss, g

    def train(self, rng, batches=None):
        cfg = self.cfg
        history = []
        for batch in range(cfg.memory_batches if batches is None else batches):
            n = cfg.memory_batch_size
            bits = rng.integers(0, 2, (n, 2))
            gaps = rng.integers(cfg.gap_min, cfg.gap_max + 1, n)
            x = stimuli(bits, gaps)
            noise = rng.normal(0, cfg.neural_noise, (len(x), n, cfg.hidden))
            attempted = rng.integers(0, 4, n)
            success = (attempted == bits[:, 0] * 2 + bits[:, 1]).astype(float)
            loss, grads = self.loss_grads(x, gaps, noise, attempted, success)
            self.opt.step(self.p, grads)
            self.p['w'] *= self.mask
            if batch % 25 == 0 or batch == cfg.memory_batches - 1:
                history.append({'batch': batch, 'loss': float(loss),
                                'successful_exploratory_trials': int(success.sum())})
        return history

    def recall(self, bits, gap, conductance, noise, lesion=False):
        gaps = np.array([gap])
        x = stimuli(np.array([bits]), gaps)
        probs, states, _ = self.forward(x, gaps, conductance, noise[:len(x), None, :], lesion)
        activity = np.mean(np.abs(np.array(states[1:])[:, 0, :]), axis=0)
        return int(np.argmax(probs[0])), activity

    def assay(self, rng, n=1024, conductance=1.0, lesion=False):
        bits = rng.integers(0, 2, (n, 2))
        gaps = rng.integers(self.cfg.gap_min, self.cfg.gap_max + 1, n)
        x = stimuli(bits, gaps)
        noise = rng.normal(0, self.cfg.neural_noise, (len(x), n, self.cfg.hidden))
        probs, _, _ = self.forward(x, gaps, conductance, noise, lesion)
        return float(np.mean(probs.argmax(-1) == bits[:, 0] * 2 + bits[:, 1]))

    @property
    def parameter_count(self):
        return int(sum(v.size for k, v in self.p.items() if k != 'w') + self.mask.sum())
