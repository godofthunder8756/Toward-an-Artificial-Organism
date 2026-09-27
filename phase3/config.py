"""Phase-III (T3/N2) config — deterministic run specification.

A single versioned :class:`Phase3Config` records every constant that
determines a Phase-III run: the inference task (G2), the W quantization, the
paid-persistence substrate (decay delta, refresh cost c), the fixed/reactive
maintenance rule A, the specialist thresholds (SPRT boundaries derived from the
cost model; S_reg threshold), the six arms (G4), and the seed structure.

Serialization is stdlib-first (JSON), matching the bridge harness. The frozen
defaults come from ``ACI_PHASE3_PROTOCOL_v1.md`` (G10); values the protocol
deferred to implementation (delta, c, the S_plan cost model, theta's reactive
form) are fixed here as explicit, documented engineering choices — never left
to the runtime.

All RNGs are seeded with the model seed (``bridge.reproducibility.seed_all``);
a run is deterministic given its seed.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict, fields, is_dataclass
from typing import Any, Dict, List, Tuple, get_type_hints

__all__ = [
    "TaskConfig",
    "WConfig",
    "PersistenceConfig",
    "MaintenanceConfig",
    "SpecialistConfig",
    "ArmConfig",
    "TrainingConfig",
    "SeedConfig",
    "Phase3Config",
    "parameter_counts",
    "TOKEN_LAMBDA",
    "P_X_GIVEN_A",
    "P_X_GIVEN_B",
]

# -- G2 §1.2 frozen observation model -------------------------------------- #
# Token indices 0..4 map to {t1, t2, t3, t4, t5}; lambda(x) is the log-likelihood
# ratio log P(x|A)/P(x|B). P(x|A) and P(x|B) are mirror images.
TOKEN_LAMBDA: Tuple[float, ...] = (2.00, 0.35, 0.00, -0.35, -2.00)
P_X_GIVEN_A: Tuple[float, ...] = (0.1500, 0.2800, 0.3524, 0.1973, 0.0203)
P_X_GIVEN_B: Tuple[float, ...] = (0.0203, 0.1973, 0.3524, 0.2800, 0.1500)

# Anchors (G2 §2.3). NOTE: the protocol's "Bayes ceiling 0.812" is the Chernoff
# *bound* 1 - exp(-t*C) (C = 0.0695/step), which is a loose LOWER bound on
# accuracy at finite t — the true Bayes-optimal accuracy of sign(S_24) for this
# model is ~0.97 (drift 0.288/step x 24 steps = 6.9 nats mean |S|, error ~0.03).
# The implementation uses the *empirical* ceiling (``true_bayes_ceiling``) for
# equivalence anchors, and reports the protocol's 0.812 as the documented bound.
BAYES_CEILING = 0.812
MEMORYLESS_CLEAN = 0.606
MEMORYLESS_PROBE = 0.500


@dataclass(frozen=True)
class TaskConfig:
    """The G2 inference task constants (frozen)."""
    horizon: int = 32                 # H
    probe_window: int = 8             # K; steps H-K+1..H are neutral t3
    n_tokens: int = 5                 # |Omega|
    token_lambda: Tuple[float, ...] = TOKEN_LAMBDA
    p_x_given_a: Tuple[float, ...] = P_X_GIVEN_A
    p_x_given_b: Tuple[float, ...] = P_X_GIVEN_B

    @property
    def informative_steps(self) -> int:
        return self.horizon - self.probe_window


@dataclass(frozen=True)
class WConfig:
    """W — the b-bit quantized scalar log-likelihood ratio (G2 §4.2)."""
    bits: int = 5                     # b
    lo: float = -6.0                  # quantized range lower bound
    hi: float = 6.0                   # quantized range upper bound


@dataclass(frozen=True)
class PersistenceConfig:
    """Decay delta and refresh cost c (G0 §3.6; computed at implementation).

    Between acquisition writes the stored W relaxes toward neutral by the
    multiplicative factor ``(1 - delta)`` per unrefreshed step; the paid refresh
    pi (cost ``c`` per step) holds it (no decay that transition). ``delta`` is
    chosen so that cutting pi leaves the probe belief within noise of neutral
    (0.1**8 ~ 1e-8 over the probe window), while the maintained arm holds the
    full accumulation (delta_eff = 0 every step A refreshes).
    """
    delta: float = 1.0                # per-step multiplicative leak when unrefreshed
    cost: float = 1.0                 # c: energy per paid refresh
    e_proc: float = 0.05              # per-step forward-pass energy
    e0: float = 64.0                  # initial energy budget
    e_crit: float = 8.0               # A's energy gate (refresh only when E >= e_crit)


@dataclass(frozen=True)
class MaintenanceConfig:
    """The fixed/reactive maintenance rule A (verdict D).

    A reads only the raw bookkeeping ``(s, E, d)`` — never W — and decides the
    refresh vector. The default rule refreshes every step while affordable
    (energy-gated), which holds W's accumulation and lets the candidate reach
    the Bayes ceiling; cutting it (I_pi) is the persistence contrast.
    """
    refresh_interval: int = 0         # d >= interval; 0 => refresh every step while affordable
    probe_always: bool = True         # always refresh in the probe (W is the only carrier)


@dataclass(frozen=True)
class SpecialistConfig:
    """Specialist thresholds (G3 §7; S_plan boundaries derived from the cost
    model, S_reg theta reactive and bounded above by the SPRT boundary a).

    The S_plan cost model is a documented implementation choice (G3 §2.2 leaves
    R_correct/R_wrong/c_obs to implementation and sweeps them): symmetric
    R_correct = R_wrong = 1, c_obs = 0.1, abstain payoff 0. The SPRT boundaries
    a, b are derived (``phase3.specialists.sprt_boundaries``), never tuned.
    """
    r_correct: float = 1.0
    r_wrong: float = 1.0
    c_obs: float = 0.1
    abstain_payoff: float = 0.0
    # S_reg threshold theta(E, d, s) = min(a, max(theta_lo, theta_base
    #   - theta_probe*[s==probe] + theta_energy*max(0, E_crit - E)))
    theta_base: float = 0.5            # well below the SPRT boundary a (~0.97): theta < a
    theta_probe: float = 0.3           # theta falls in the probe (W more valuable)
    theta_energy: float = 0.1          # theta rises as E falls
    theta_lo: float = 0.2
    # S_bias (G7 §2.2): theta_bias = log(c_BA / c_AB) for c_AB:c_BA = 3:1.
    c_ab: float = 3.0
    c_ba: float = 1.0


@dataclass(frozen=True)
class ArmConfig:
    """Architecture dims and the parameter budget P (G4 §8 rule 3).

    The candidate's single shared encoder carries the full budget P; R1 splits
    P across n private encoders; R2/R3 spend P on their recurrent readers plus
    learned heads. R4/R5 have no learned inference (fixed accumulator). The
    specialist *function forms* are fixed (zero parameters) in every arm; R2/R3
    additionally learn heads to implement those functions from their rich state
    (their capacity advantage, disclosed, G4 §8 rule 4).
    """
    n_specialists: int = 3
    # GRU hidden widths for the P level family {small, mid, large}.
    p_levels: Dict[str, int] = field(default_factory=lambda: {
        "small": 8, "mid": 16, "large": 32,
    })
    p_level: str = "small"            # the budget member used by default
    r2_hidden: int = 16               # R2 RNN hidden dim (>= b bits)
    r3_hidden: int = 16               # R3 reader hidden dim


@dataclass(frozen=True)
class TrainingConfig:
    """Training schedule (encoder supervised toward the running LLR)."""
    lr: float = 1e-3
    steps: int = 2000
    batch_size: int = 256
    episodes_per_step: int = 32        # fresh episodes per training step
    encoder_objective: str = "bce"     # BCE(sigma(W_raw_t), z), summed over t
    weight_decay: float = 0.0


@dataclass(frozen=True)
class SeedConfig:
    """Seed families (frozen §11): engineering 0-7, finals 100-111."""
    engineering_seeds: List[int] = field(default_factory=lambda: list(range(8)))
    final_seeds: List[int] = field(default_factory=lambda: [100 + i for i in range(12)])
    eval_episodes_per_seed: int = 1024  # balanced A/B episodes per model seed


@dataclass(frozen=True)
class Phase3Config:
    """Full Phase-III run configuration."""
    name: str = "phase3"
    version: str = "1"
    task: TaskConfig = field(default_factory=TaskConfig)
    w: WConfig = field(default_factory=WConfig)
    persistence: PersistenceConfig = field(default_factory=PersistenceConfig)
    maintenance: MaintenanceConfig = field(default_factory=MaintenanceConfig)
    specialist: SpecialistConfig = field(default_factory=SpecialistConfig)
    arm: ArmConfig = field(default_factory=ArmConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    seed: SeedConfig = field(default_factory=SeedConfig)

    # -- serialization ----------------------------------------------------- #

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Phase3Config":
        return cls(**reconstruct(d, cls))

    @classmethod
    def from_json(cls, text: str) -> "Phase3Config":
        return cls.from_dict(json.loads(text))


def reconstruct(d: Dict[str, Any], cls) -> Dict[str, Any]:
    """Rebuild constructor kwargs from a plain dict (nested dataclasses, tuples)."""
    hints = get_type_hints(cls)
    field_map = {f.name: f for f in fields(cls)}
    kwargs: Dict[str, Any] = {}
    for key, value in d.items():
        if key not in field_map:
            continue
        typ = hints.get(key)
        if is_dataclass(typ):
            kwargs[key] = typ(**reconstruct(value, typ))
        elif typ is tuple or getattr(typ, "__origin__", None) is tuple:
            kwargs[key] = tuple(value)
        else:
            kwargs[key] = value
    return kwargs


def gru_parameters(input_size: int, hidden_size: int) -> int:
    """Trainable params of a bias=True GRU: 3 * (in*h + h*h + 2*h)."""
    return 3 * hidden_size * (input_size + hidden_size + 2)


def parameter_counts(cfg: Phase3Config) -> Dict[str, int]:
    """Trainable-parameter counts per arm (capacity-matching audit, G4 §8.3)."""
    d_h = cfg.arm.p_levels[cfg.arm.p_level]
    enc_input = cfg.task.n_tokens + 1          # one-hot x_t + scalar W_{t-1}
    encoder = gru_parameters(enc_input, d_h) + (d_h + 1)  # GRU + linear(d_h -> 1)
    d_h_r1 = r1_split_hidden(cfg)              # each private encoder ~ P/n
    encoder_r1 = gru_parameters(enc_input, d_h_r1) + (d_h_r1 + 1)
    # R2: one RNN at the same input width (no W feedback) + 3 learned heads.
    r2_rnn = gru_parameters(cfg.task.n_tokens, cfg.arm.r2_hidden)
    r2_heads = 3 * (cfg.arm.r2_hidden + 1) * 3   # 3 heads x (h+1) x ~3-class out
    # R3: three readers (GRU over raw history) + 3 heads.
    r3_readers = 3 * gru_parameters(cfg.task.n_tokens, cfg.arm.r3_hidden)
    r3_heads = r2_heads
    return {
        "candidate_encoder": encoder,
        "r1_per_copy": encoder_r1,
        "r1_three_encoders": cfg.arm.n_specialists * encoder_r1,
        "r1_robustness_nP": cfg.arm.n_specialists * encoder,
        "r2_total": r2_rnn + r2_heads,
        "r3_total": r3_readers + r3_heads,
        "r4_total": 0,
        "r5_total": 0,
    }


def r1_split_hidden(cfg: Phase3Config) -> int:
    """Largest hidden dim h such that n * encoder(h) <= encoder(d_h): the
    private-copy budget split (each of n encoders gets ~ P/n, G4 §8 rule 3)."""
    d_h = cfg.arm.p_levels[cfg.arm.p_level]
    enc_input = cfg.task.n_tokens + 1
    full = gru_parameters(enc_input, d_h) + (d_h + 1)
    h = d_h
    while h > 1 and cfg.arm.n_specialists * (gru_parameters(enc_input, h) + (h + 1)) > full:
        h -= 1
    return h
