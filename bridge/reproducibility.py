"""Seed control and deterministic execution flags.

``seed_all`` pins Python, NumPy and PyTorch RNGs and applies the deterministic
backend flags the CPU runtime supports. NumPy and PyTorch are seeded only when
they are importable, so this module remains usable (and testable) against a
bare venv while being fully wired once the CPU torch wheel is installed.

Determinism is best-effort and CPU-scoped, exactly as the bridge needs:
CUDA flags are never referenced (the bridge is CPU-only), and
``OPENBLAS_NUM_THREADS`` is forced to 1 for the small-matrix runs this project
favours (repo convention, see the research skill).
"""

from __future__ import annotations

import importlib
import os
import random
from typing import Any, Dict, Optional, Tuple

__all__ = ["seed_all", "deterministic_context", "available_backends"]


def _import_optional(name: str):
    """Import a module if present, else return None (never raises)."""
    try:
        return importlib.import_module(name)
    except Exception:
        return None


def available_backends() -> Dict[str, bool]:
    """Which RNG backends are importable in the current interpreter."""
    return {
        "python": True,
        "numpy": _import_optional("numpy") is not None,
        "torch": _import_optional("torch") is not None,
    }


def seed_all(seed: int) -> int:
    """Pin every available RNG and set deterministic flags. Returns the seed.

    Idempotent and cheap; call at the top of any run or test that must replay.
    """
    random.seed(seed)

    np = _import_optional("numpy")
    if np is not None:
        np.random.seed(seed)

    torch = _import_optional("torch")
    if torch is not None:
        torch.manual_seed(seed)
        # CPU-only determinism: no CUDA backend is ever referenced.
        torch.use_deterministic_algorithms(True, warn_only=True)

    # Small-matrix determinism (repo convention).
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("OMP_NUM_THREADS", "1")

    return seed


class deterministic_context:
    """Context manager: seeds inside the block and restores prior RNG state.

    Use around a full run so a study's RNG consumption is contained and a
    follow-on computation cannot depend on how many draws the run made.
    """

    def __init__(self, seed: int):
        self.seed = seed
        self._py_state: Optional[Any] = None
        self._backend_state: Dict[str, Any] = {}

    def __enter__(self):
        self._py_state = random.getstate()
        np = _import_optional("numpy")
        if np is not None:
            self._backend_state["numpy"] = np.random.get_state()
        torch = _import_optional("torch")
        if torch is not None:
            self._backend_state["torch"] = torch.random.get_rng_state()
        seed_all(self.seed)
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._py_state is not None:
            random.setstate(self._py_state)
        np = _import_optional("numpy")
        if np is not None and "numpy" in self._backend_state:
            np.random.set_state(self._backend_state["numpy"])
        torch = _import_optional("torch")
        if torch is not None and "torch" in self._backend_state:
            torch.random.set_rng_state(self._backend_state["torch"])
        return False
