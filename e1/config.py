from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Config:
    seeds: int = 20
    seed_start: int = 100
    memory_batches: int = 700
    memory_batch_size: int = 64
    pre_trials: int = 768
    dependency_trials: int = 1536
    branch_trials: int = 1536
    episode_length: int = 128
    eval_worlds: int = 8
    eval_trials: int = 128
    hidden: int = 16
    gap_min: int = 3
    gap_max: int = 6
    neural_noise: float = 0.06
    wear: float = 0.095
    repair: float = 0.78
    energy_initial: float = 2.0
    energy_cap: float = 4.0
    basal_yield: float = 0.045
    task_yield: float = 0.30
    living_cost: float = 0.09
    precursor_cost: float = 0.015
    activity_cost: float = 0.01
    gamma: float = 0.85
    exploration: float = 0.18
    learning_rate: float = 0.002
    policy_hidden: int = 16
    drive_weight: float = 0.15

    def to_dict(self):
        return asdict(self)


VARIANTS = ('neural_q', 'frozen_neural_q', 'tabular_q', 'fixed_drive_q')
BRANCHES = ('dependency', 'rescue', 'sham', 'lost_usefulness')
