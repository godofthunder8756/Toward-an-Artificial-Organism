"""Phase-III (T3/N2) implementation — the Shared Latent Workspace candidate and
its five reduction rivals (G4), on the G2 hidden-state inference task.

This package realizes ``ACI_PHASE3_PROTOCOL_v1.md``: the candidate (SLW) and
rivals R1-R5, the three invariance-class specialists (G3), the five canonical
interventions I1-I5 plus the pi-cut and the leakage ablations (G5/G8), the
coordination manifold (G6), the novel-consumer test (G7), and the leakage
audit (G8). It reuses the bridge harness conventions (``.venv-bridge`` torch
env, exact sign-flip stats, JSONL episode storage, deterministic seeding).

The torch-backed submodules are re-exported lazily so the pure-config parts
import without torch; the full package is used under ``.venv-bridge``.
"""

from phase3.config import Phase3Config, parameter_counts
from phase3.task import Quantizer, sample_episodes, token_stream_to_s

__all__ = [
    "Phase3Config",
    "parameter_counts",
    "Quantizer",
    "sample_episodes",
    "token_stream_to_s",
    # torch-backed (lazy):
    "Encoder",
    "Maintenance",
    "Arm",
    "compute_thresholds",
    "apply_specialists",
    "train_encoder",
    "train_r2",
    "train_r3",
]

_LAZY = {
    "Encoder": ("phase3.model", "Encoder"),
    "Maintenance": ("phase3.model", "Maintenance"),
    "Arm": ("phase3.arms", "Arm"),
    "compute_thresholds": ("phase3.arms", "compute_thresholds"),
    "apply_specialists": ("phase3.arms", "apply_specialists"),
    "train_encoder": ("phase3.train", "train_encoder"),
    "train_r2": ("phase3.train", "train_r2"),
    "train_r3": ("phase3.train", "train_r3"),
}


def __getattr__(name):
    if name in _LAZY:
        import importlib

        module_name, attr = _LAZY[name]
        obj = getattr(importlib.import_module(module_name), attr)
        globals()[name] = obj
        return obj
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
