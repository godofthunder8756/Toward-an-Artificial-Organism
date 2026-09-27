"""Bridge reproducibility harness.

This package is the shared, version-controlled substrate for the neural-bridge
study line. It provides:

- ``config``          — the :class:`BridgeConfig` dataclass (architecture, energy,
                        decay, optimizer, losses, gradient paths) with YAML/JSON
                        serialization and a parameter-count helper.
- ``reproducibility`` — pinned seeds and deterministic PyTorch/NumPy flags.
- ``episodes``        — save/load helpers for evaluation episodes, so every arm
                        reuses the same underlying environment and saved episodes.
- ``modules``         — the six neural modules of the frozen v3 protocol
                        (controller, workspace W, estimator V, allocator A, probe
                        S_pol, refresh action pi), CPU-only torch.
- ``substrate``       — the resource-economy / decay bookkeeping law (no gradient).
- ``agent``           — :class:`NeuralBridge`, wiring the modules to the substrate
                        and running a batch forward pass on CPU.

The package is stdlib-first where it can be: ``config`` and ``episodes`` import
nothing but the standard library, and ``reproducibility`` degrades gracefully
when NumPy/PyTorch are absent. The torch-backed submodules (``modules``,
``substrate``, ``agent``) are re-exported lazily via ``__getattr__`` so that
``import bridge`` and ``from bridge.config import BridgeConfig`` still succeed
against a bare venv (no torch) while ``from bridge import NeuralBridge`` works
once the CPU torch wheel is installed.
"""

from bridge.config import BridgeConfig
from bridge.reproducibility import seed_all, deterministic_context
from bridge.episodes import save_episodes, load_episodes, EpisodeRecorder

__all__ = [
    "BridgeConfig",
    "seed_all",
    "deterministic_context",
    "save_episodes",
    "load_episodes",
    "EpisodeRecorder",
    # torch-backed (lazy):
    "Controller",
    "Workspace",
    "IntegrityEstimator",
    "MaintenanceAllocator",
    "ProbeReadout",
    "RefreshAction",
    "Substrate",
    "NeuralBridge",
    "count_parameters",
    "BridgeEnv",
    "BridgeTrainer",
    "compute_losses",
    "quantize_energy",
    "integrity_label",
]

_LAZY = {
    "Controller": ("bridge.modules", "Controller"),
    "Workspace": ("bridge.modules", "Workspace"),
    "IntegrityEstimator": ("bridge.modules", "IntegrityEstimator"),
    "MaintenanceAllocator": ("bridge.modules", "MaintenanceAllocator"),
    "ProbeReadout": ("bridge.modules", "ProbeReadout"),
    "RefreshAction": ("bridge.modules", "RefreshAction"),
    "count_parameters": ("bridge.modules", "count_parameters"),
    "Substrate": ("bridge.substrate", "Substrate"),
    "NeuralBridge": ("bridge.agent", "NeuralBridge"),
    "BridgeEnv": ("bridge.env", "BridgeEnv"),
    "BridgeTrainer": ("bridge.trainer", "BridgeTrainer"),
    "compute_losses": ("bridge.trainer", "compute_losses"),
    "quantize_energy": ("bridge.trainer", "quantize_energy"),
    "integrity_label": ("bridge.trainer", "integrity_label"),
}


def __getattr__(name):
    if name in _LAZY:
        import importlib

        module_name, attr = _LAZY[name]
        obj = getattr(importlib.import_module(module_name), attr)
        globals()[name] = obj
        return obj
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
