"""Phase-III task (G2): the latent-cause evidence-accumulation generative model.

z in {0=A, 1=B} is drawn uniform per episode and never emitted as an
observation. The token stream x_1..x_H is conditionally i.i.d. given z with
mirror distributions and per-token log-likelihood ratios lambda (G2 §1.2);
steps 1..(H-K) are informative and steps (H-K+1)..H are the probe window where
every token is the neutral t3. The minimal sufficient statistic is the scalar
running sum S_t = sum lambda(x_i) (G2 §2.1).

This module also owns the b-bit quantization of that scalar (G2 §4.2): W is
the scalar LLR quantized to ``bits`` levels over [lo, hi]. Every RNG draw is
seeded through ``bridge.reproducibility.seed_all`` so an episode stream is
deterministic given its seed — the observation-equality-across-arms guarantee.
"""

from __future__ import annotations

from typing import List, Tuple

import numpy as np

from phase3.config import TaskConfig, WConfig

__all__ = [
    "Quantizer",
    "sample_episodes",
    "true_log_odds",
    "token_stream_to_s",
]


class Quantizer:
    """b-bit uniform quantization of a scalar over [lo, hi].

    ``quantize(s)`` returns the nearest level; ``dequantize(idx)`` returns the
    level's float value. Levels are ``lo + k*(hi-lo)/(2**bits - 1)``, so the
    resolution is ``(hi-lo)/(2**bits-1)`` (G2 §4.2's 5-bit range [-6,+6]).
    """

    def __init__(self, w: WConfig):
        self.bits = w.bits
        self.lo = w.lo
        self.hi = w.hi
        self.n_levels = 2 ** w.bits
        self._step = (w.hi - w.lo) / (self.n_levels - 1)
        self.levels = np.linspace(w.lo, w.hi, self.n_levels, dtype=np.float64)

    def quantize(self, s: np.ndarray) -> np.ndarray:
        """Map real scalar(s) to the nearest level index in [0, n_levels)."""
        s = np.asarray(s, dtype=np.float64)
        idx = np.rint((s - self.lo) / self._step).astype(np.int64)
        return np.clip(idx, 0, self.n_levels - 1)

    def dequantize(self, idx: np.ndarray) -> np.ndarray:
        """Map level index(es) to the level's float value."""
        idx = np.asarray(idx, dtype=np.int64)
        return self.levels[idx]

    def round_trip(self, s: np.ndarray) -> np.ndarray:
        """Quantize then dequantize (the value a specialist reads for W)."""
        return self.dequantize(self.quantize(s))


def true_log_odds(cfg: TaskConfig, s: np.ndarray) -> np.ndarray:
    """Posterior P(A | S) = sigmoid(S + log(pi_A/pi_B)); pi uniform => sigmoid(S)."""
    return 1.0 / (1.0 + np.exp(-np.asarray(s, dtype=np.float64)))


def token_stream_to_s(cfg: TaskConfig, x: np.ndarray) -> np.ndarray:
    """S_t = sum_{i<=t} lambda(x_i) for a token-index array x of shape (..., H)."""
    lam = np.asarray(cfg.token_lambda, dtype=np.float64)
    return np.cumsum(lam[np.asarray(x, dtype=np.int64)], axis=-1)


def true_bayes_ceiling(cfg: TaskConfig, n_episodes: int = 20000, seed: int = 0) -> float:
    """The *empirical* Bayes-optimal accuracy of sign(S_H) for this model.

    The protocol's 0.812 is the Chernoff *bound* 1 - exp(-t*C), a loose lower
    bound; the true accuracy is ~0.97 (see config.BAYES_CEILING note). Used as
    the equivalence anchor for H1.2 / H5.2 instead of the loose bound.
    """
    z, x = sample_episodes(cfg, n_episodes, seed)
    s = token_stream_to_s(cfg, x)[..., -1]
    zhat = np.where(s > 0.0, 0, 1)          # A=0 iff S>0
    return float(np.mean(zhat == z))


def sample_episodes(
    cfg: TaskConfig,
    n_episodes: int,
    seed: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """Draw ``n_episodes`` independent (z, x) pairs, balanced A/B.

    Returns ``(z, x)`` where z in {0,1} (shape (n,)), x token indices (shape
    (n, H)). z is balanced (half A, half B) and the token stream is drawn from
    P(·|z); the probe window (last K steps) is forced to the neutral token t3.
    Deterministic given ``seed`` (Python/numpy RNG seeded via
    ``bridge.reproducibility.seed_all``).
    """
    import bridge.reproducibility as _rep

    _rep.seed_all(seed)
    rng = np.random.default_rng(seed)
    n = n_episodes
    n_a = n // 2
    n_b = n - n_a
    z = np.concatenate([np.zeros(n_a, dtype=np.int64), np.ones(n_b, dtype=np.int64)])
    rng.shuffle(z)

    p_a = np.asarray(cfg.p_x_given_a, dtype=np.float64)
    p_b = np.asarray(cfg.p_x_given_b, dtype=np.float64)
    H = cfg.horizon
    K = cfg.probe_window
    n_tok = cfg.n_tokens
    neutral = 2  # t3

    x = np.empty((n, H), dtype=np.int64)
    a_mask = z == 0
    b_mask = z == 1
    # vectorized draw: A and B token streams separately, then merge
    x[a_mask, : H - K] = rng.choice(n_tok, size=(int(a_mask.sum()), H - K), p=p_a)
    x[b_mask, : H - K] = rng.choice(n_tok, size=(int(b_mask.sum()), H - K), p=p_b)
    x[:, H - K:] = neutral
    return z, x
