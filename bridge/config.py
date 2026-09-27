"""Reproducibility config for the neural bridge.

A single versioned :class:`BridgeConfig` records every dimension, budget and
schedule that determines a bridge run, so that a run is fully specified by its
config file plus a seed. The field names and defaults follow the frozen v3
protocol (``ACI_BRIDGE_PROTOCOL_v3.md``); where the protocol leaves a value
free (GRU width, learning rates, initializer gain) the default is an explicit,
documented engineering choice, not an accident of the runtime.

Serialization is stdlib-first: ``to_json``/``from_json`` always work, and
``to_yaml``/``from_yaml`` use PyYAML when it is installed and otherwise fall
back to the built-in JSON text (still round-trippable, and documented as such).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict, fields, is_dataclass
from typing import Any, Dict, List, Tuple, get_type_hints


# --------------------------------------------------------------------------- #
# Sub-configs
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class ArchConfig:
    """Architecture dimensions (v3 §6).

    The bridge is: a GRU controller ``h_t``; a paid, non-recurrent maintained
    workspace ``W`` (the 1-bit cue slot); a discrete self-resource estimate
    ``V`` (energy + integrity fields); a homeostatic maintenance allocator
    ``A``; a probe readout ``S_pol``; and a paid refresh action ``pi``.
    """
    gru_hidden: int = 16                 # h_t dimensionality
    distractor_dim: int = 4              # x_t (distractor stream) width
    w_bits: int = 1                      # W: the 1-bit cue slot (v3 §6)
    v_energy_bits: int = 2               # V's energy field (2-3 bit; v3 §6)
    v_integrity_bits: int = 1            # V's integrity field (re-encoding of d_t)
    regime_dim: int = 2                  # s in {stable, volatile} one-hot
    # Derived input/output widths (kept explicit so counts are auditable):
    #   S_pol reads (W, x_t); A reads (v_t, s_t); V reads (v_{t-1}, h_{t-1}, b_t).


@dataclass(frozen=True)
class EnergyConfig:
    """Resource economy (v3 §3, made exact).

    E_t is earned by correctly processing the distractor stream (metabolic
    task), spent on E_proc (forward pass) + E_pi (paid refresh), with
    E_pi + E_proc <= B_t; death at E_t <= 0. Reward r_t is paid only on the
    probe, only in the stable regime, only if the cue was held.
    """
    e0: float = 8.0                      # initial energy
    e_proc: float = 0.1                  # per-tick forward-pass cost
    e_pi: float = 1.0                    # per-refresh paid cost (the maintenance price)
    budget_b: float = 2.0                # per-tick total spend cap (E_pi + E_proc <= B_t)
    e_crit: float = 4.0                  # A's set-point threshold (v3 §7.2)
    e_earn: float = 0.2                  # energy earned per correct distractor tick
    death_floor: float = 0.0             # death at E_t <= floor


@dataclass(frozen=True)
class DecayConfig:
    """Decay / free-permanence parameters (v3 §3, §6; N6 §3.2).

    Deterministic countdown decay: the cue slot's readout flips to neutral once
    the decay age reaches ``lifetime`` since the last refresh, and a paid
    refresh (age reset) restores it. Without the paid refresh the cue is
    unrecoverable at the probe (the free-permanence gate: ``lifetime <=
    delay_d``). ``lifetime`` is the decay-age deadline (L); ``delay_d`` is the
    number of distractor ticks before the probe; ``announce_m`` is the tick the
    regime is announced.
    """
    lifetime: int = 16                   # decay-age deadline (L); readout neutral at age >= L
    delay_d: int = 32                    # probe delay (distractor ticks, D)
    announce_m: int = 16                 # regime announcement tick (m <= D)


@dataclass(frozen=True)
class EpisodeConfig:
    """Episode horizon and replication structure (v3 §3, §11)."""
    horizon_t: int = 64                  # total ticks per episode (T)
    histories_per_seed: int = 2          # repeated measures within a seed (v3 §11)


@dataclass(frozen=True)
class OptimizerConfig:
    """Optimizer and per-component learning rates (v3 §7, N4)."""
    name: str = "adam"                   # optimizer for all trainable components
    lr_s_pol: float = 1e-3               # probe readout S_pol (reward-trained)
    lr_v: float = 1e-3                   # integrity/energy estimator f_V
    lr_a_policy: float = 1e-2            # maintenance allocator A (policy)
    lr_a_critic: float = 1e-3            # A's learned baseline / critic
    weight_decay: float = 0.0
    betas: Tuple[float, float] = (0.9, 0.999)


@dataclass(frozen=True)
class InitConfig:
    """Initialization scheme (v3 leaves this free; default is explicit)."""
    scheme: str = "xavier_uniform"       # GRU + linear layers
    gain: float = 1.0                    # init gain (identity for xavier_uniform)


@dataclass(frozen=True)
class LossConfig:
    """Losses (v3 §7, N4 exact).

    L_V supervises V against the *measured* state; J_A is REINFORCE over the
    homeostatic cost toward the supplied set point. Continued operation (E5)
    appears in no loss.
    """
    v_energy_weight: float = 1.0         # lambda_E (v3 §7.1)
    v_integrity_weight: float = 1.0      # lambda_I
    a_discount: float = 0.9              # gamma (v3 §7.2, default, swept)
    a_entropy_weight: float = 0.1        # Bernoulli entropy bonus on J_A (REINFORCE stabilization)
    probe_loss: str = "nll"              # S_pol objective on the cue answer


@dataclass(frozen=True)
class TrainingConfig:
    """Training schedule and seeds (v3 §5, §11).

    Engineering seeds are excluded from the final sample (disjoint families,
    AC39); the final sample is N=12 (v3 §11, re-derived from the sign-flip
    gate). The two lists must be disjoint by convention, not by accident.
    """
    engineering_seeds: List[int] = field(default_factory=lambda: [0, 1, 2])
    final_seeds: List[int] = field(default_factory=lambda: [2000 + i for i in range(12)])
    training_episodes: int = 64000       # training rollouts (1000 steps x 64)
    eval_episodes: int = 2048            # held-out evaluation episodes per seed
    batch_size: int = 64                 # episodes per training step
    num_workers: int = 1                 # CPU-only; keep single-threaded for determinism


# --------------------------------------------------------------------------- #
# The top-level config
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class BridgeConfig:
    """Full bridge run configuration.

    Records architecture dimensions, parameter counts (computed), optimizer,
    learning rates, initialization, seeds, training steps, episode horizon,
    losses, gradient paths, energy parameters and decay parameters — everything
    the N9 card's RECORD clause requires.
    """
    name: str = "bridge"
    version: str = "1"                   # bump on any frozen-protocol change
    arch: ArchConfig = field(default_factory=ArchConfig)
    energy: EnergyConfig = field(default_factory=EnergyConfig)
    decay: DecayConfig = field(default_factory=DecayConfig)
    episode: EpisodeConfig = field(default_factory=EpisodeConfig)
    optimizer: OptimizerConfig = field(default_factory=OptimizerConfig)
    init: InitConfig = field(default_factory=InitConfig)
    losses: LossConfig = field(default_factory=LossConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    # The N4 §7.3 gradient-path table, recorded verbatim so the wiring is
    # auditable: which component receives which gradient, and where it stops.
    gradient_paths: Dict[str, str] = field(default_factory=lambda: {
        "W": "reads; stop-gradient through content; hard write",
        "V": "target -> f_V (L_V); stop-gradient on V->A edge; argmax non-diff",
        "pi": "substrate primitive (no gradient)",
        "energy/decay": "substrate law (no gradient)",
        "S_pol": "reward gradient; reads (W, x_t) only",
        "A": "J_A policy gradient; reads (v_t, s_t) only",
        "h_t (GRU)": "content-blind L_V only; never reward",
        "reward r_t": "source; S_pol objective only; never V or A",
    })

    # -- serialization ----------------------------------------------------- #

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "BridgeConfig":
        return cls(**_reconstruct(d, cls))

    @classmethod
    def from_json(cls, text: str) -> "BridgeConfig":
        return cls.from_dict(json.loads(text))

    def to_yaml(self) -> str:
        """YAML text if PyYAML is importable, else JSON (still round-trips)."""
        yaml = _try_import_yaml()
        if yaml is not None:
            return yaml.safe_dump(self.to_dict(), sort_keys=False)
        return self.to_json()

    @classmethod
    def from_yaml(cls, text: str) -> "BridgeConfig":
        yaml = _try_import_yaml()
        if yaml is not None:
            return cls.from_dict(yaml.safe_load(text))
        return cls.from_json(text)

    # -- derived quantities ------------------------------------------------ #

    def parameter_counts(self) -> Dict[str, int]:
        """Parameter counts per trainable component, derived from the arch dims.

        The named components follow v3 §6. Counts are the *trainable* weights of
        each module; the substrate (energy/decay law, the paid refresh pi) has
        none, and W is storage, not parameters.
        """
        a = self.arch
        h, x, w, ve, vi, r = a.gru_hidden, a.distractor_dim, a.w_bits, \
            a.v_energy_bits, a.v_integrity_bits, a.regime_dim
        v_in = (ve + vi) + h + 2                  # v_{t-1} + h_{t-1} + b_t(E,d)
        v_out = (2 ** ve) + (2 ** vi)           # softmax heads over discrete codes
        counts = {
            # 3 gates * (W_ih + W_hh + b_ih + b_hh) for a bias=True GRU
            "gru": 3 * h * (x + h + 2),
            "f_V": v_in * v_out + v_out,        # integrity/energy estimator
            "A_policy": (ve + vi + r) * 1 + 1,  # A reads (v_t, s_t); scalar refresh logit
            "A_critic": (ve + vi + r) * 1 + 1,  # learned baseline, same input restriction
            "S_pol": (w + x) * 2 + 2,           # probe readout over (W, x_t)
        }
        counts["total"] = sum(counts.values())
        return counts


def _reconstruct(d: Dict[str, Any], cls) -> Dict[str, Any]:
    """Rebuild constructor kwargs for a dataclass from a plain dict.

    Handles nested dataclass fields recursively and tuple fields (betas).
    ``get_type_hints`` resolves the string annotations that
    ``from __future__ import annotations`` stores in ``Field.type``.
    """
    hints = get_type_hints(cls)
    field_map = {f.name: f for f in fields(cls)}
    kwargs: Dict[str, Any] = {}
    for key, value in d.items():
        if key not in field_map:
            continue
        typ = hints.get(key)
        if is_dataclass(typ):
            kwargs[key] = typ(**_reconstruct(value, typ))  # type: ignore[operator]
        elif key == "betas":
            kwargs[key] = tuple(value)
        else:
            kwargs[key] = value
    return kwargs


def _try_import_yaml():
    try:
        import yaml  # type: ignore
        return yaml
    except Exception:
        return None
