"""Two-dimensional Gray--Scott reaction--diffusion environment for Block I B1.

This environment is a driven-pattern baseline only.  Its metrics describe spatial
patterning and persistence; they are not interpreted as measures of life,
self-maintenance, viability, or organisational closure.
"""

from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from .base import BaseEnvironment, EnvironmentOperationError, StepResult


class GrayScottEnvironment(BaseEnvironment):
    """Deterministic Gray--Scott PDE discretisation with registered manipulations."""

    def __init__(self, config: Mapping[str, Any]):
        self.environment_id = str(config["id"])
        self.version = str(config["version"])
        self.grid_size = int(config.get("grid_size", 64))
        self.du = float(config.get("du", 0.16))
        self.dv = float(config.get("dv", 0.08))
        self.feed = float(config["feed"])
        self.kill = float(config["kill"])
        self.dt = float(config.get("dt", 1.0))
        self.total_steps = int(config.get("total_steps", 4000))
        self.steps_per_observation = int(config.get("steps_per_observation", 20))
        self.boundary = str(config.get("boundary", "periodic"))
        self.initial_patch_fraction = float(config.get("initial_patch_fraction", 0.10))
        self.initial_noise = float(config.get("initial_noise", 0.01))
        self.interventions = list(config.get("scheduled_interventions", []))
        self.metric_bins = int(config.get("mutual_information_bins", 12))
        self.pattern_metric_floor = float(config.get("pattern_metric_floor", 1e-5))
        self.center_probe_fraction = float(config.get("center_probe_fraction", 0.25))
        self._validate_config()
        self._rng = np.random.default_rng(0)
        self._u = np.ones((self.grid_size, self.grid_size), dtype=np.float64)
        self._v = np.zeros_like(self._u)
        self._step = 0
        self._feed_active = True
        self._active_boundary = self.boundary
        self._fired: set[str] = set()

    def _validate_config(self) -> None:
        if self.grid_size < 16:
            raise ValueError("grid_size must be >= 16")
        if not (0.0 < self.du <= 1.0 and 0.0 < self.dv <= 1.0):
            raise ValueError("diffusion coefficients must lie in (0,1]")
        if not (0.0 <= self.feed <= 0.2 and 0.0 <= self.kill <= 0.2):
            raise ValueError("feed and kill must lie in [0,0.2]")
        if self.dt <= 0 or self.dt > 1.0:
            raise ValueError("dt must lie in (0,1]")
        if self.total_steps <= 0 or self.steps_per_observation <= 0:
            raise ValueError("step counts must be positive")
        if self.boundary not in {"periodic", "no_flux", "reservoir"}:
            raise ValueError("boundary must be periodic, no_flux, or reservoir")
        if not (0.02 <= self.initial_patch_fraction <= 0.5):
            raise ValueError("initial_patch_fraction outside supported range")
        if self.pattern_metric_floor < 0:
            raise ValueError("pattern_metric_floor must be non-negative")
        if not (0.05 <= self.center_probe_fraction <= 0.75):
            raise ValueError("center_probe_fraction outside supported range")
        ids = [str(x.get("id")) for x in self.interventions]
        if len(ids) != len(set(ids)):
            raise ValueError("scheduled intervention ids must be unique")

    def reset(self, seed: int) -> Mapping[str, float]:
        if not isinstance(seed, int) or seed < 0:
            raise ValueError("seed must be a non-negative integer")
        self._rng = np.random.default_rng(seed)
        n = self.grid_size
        self._u = np.ones((n, n), dtype=np.float64)
        self._v = np.zeros((n, n), dtype=np.float64)
        width = max(2, int(round(n * self.initial_patch_fraction)))
        lo = n // 2 - width // 2
        hi = lo + width
        self._u[lo:hi, lo:hi] = 0.50
        self._v[lo:hi, lo:hi] = 0.25
        if self.initial_noise > 0:
            noise = self._rng.normal(0.0, self.initial_noise, size=(n, n))
            self._v = np.clip(self._v + noise, 0.0, 1.0)
            self._u = np.clip(self._u - 0.5 * noise, 0.0, 1.0)
        self._step = 0
        self._feed_active = True
        self._active_boundary = self.boundary
        self._fired = set()
        self._apply_boundary_values()
        return self.observe()

    def observe(self) -> Mapping[str, float]:
        return self._metrics()

    def _laplacian(self, a: np.ndarray) -> np.ndarray:
        if self._active_boundary == "periodic":
            return (
                np.roll(a, 1, 0) + np.roll(a, -1, 0)
                + np.roll(a, 1, 1) + np.roll(a, -1, 1)
                - 4.0 * a
            )
        if self._active_boundary == "no_flux":
            p = np.pad(a, 1, mode="edge")
        elif self._active_boundary == "reservoir":
            # Reservoir values are imposed after every step; edge padding is fixed
            # to the external bath state for the Laplacian calculation.
            p = np.pad(a, 1, mode="constant", constant_values=0.0)
            if a is self._u:
                p[0, :] = p[-1, :] = p[:, 0] = p[:, -1] = 1.0
        else:  # pragma: no cover - protected by validation
            raise RuntimeError(self._active_boundary)
        return p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:] - 4.0 * a

    def _apply_boundary_values(self) -> None:
        if self._active_boundary == "reservoir":
            self._u[0, :] = self._u[-1, :] = 1.0
            self._u[:, 0] = self._u[:, -1] = 1.0
            self._v[0, :] = self._v[-1, :] = 0.0
            self._v[:, 0] = self._v[:, -1] = 0.0

    def _apply_scheduled_interventions(self) -> None:
        for spec in self.interventions:
            iid = str(spec["id"])
            if iid in self._fired or int(spec["step"]) != self._step:
                continue
            op = str(spec["operation"])
            if op == "remove_driving":
                self._feed_active = False
            elif op == "local_damage":
                fraction = float(spec.get("fraction", 0.20))
                width = max(2, int(round(self.grid_size * fraction)))
                lo = self.grid_size // 2 - width // 2
                hi = lo + width
                self._u[lo:hi, lo:hi] = 1.0
                self._v[lo:hi, lo:hi] = 0.0
            elif op == "set_boundary":
                boundary = str(spec["boundary"])
                if boundary not in {"periodic", "no_flux", "reservoir"}:
                    raise EnvironmentOperationError(f"Unsupported boundary {boundary!r}")
                self._active_boundary = boundary
                self._apply_boundary_values()
            else:
                raise EnvironmentOperationError(f"Unknown Gray-Scott operation {op!r}")
            self._fired.add(iid)

    def _advance_one(self) -> None:
        self._apply_scheduled_interventions()
        u = self._u
        v = self._v
        reaction = u * v * v
        f = self.feed if self._feed_active else 0.0
        du_dt = self.du * self._laplacian(u) - reaction + f * (1.0 - u)
        dv_dt = self.dv * self._laplacian(v) + reaction - (f + self.kill) * v
        self._u = np.clip(u + self.dt * du_dt, 0.0, 1.5)
        self._v = np.clip(v + self.dt * dv_dt, 0.0, 1.5)
        self._step += 1
        self._apply_boundary_values()
        if not (np.isfinite(self._u).all() and np.isfinite(self._v).all()):
            raise FloatingPointError("Non-finite Gray-Scott field value")

    def step(self, action: Any) -> StepResult:
        del action
        target = min(self._step + self.steps_per_observation, self.total_steps)
        while self._step < target:
            self._advance_one()
        metrics = self._metrics()
        return StepResult(
            observation=metrics,
            outcome={"pattern_amplitude": metrics["v_std"]},
            terminated=self._step >= self.total_steps,
            info={
                "pde_step": self._step,
                "feed_active": self._feed_active,
                "boundary": self._active_boundary,
                "fired_interventions": sorted(self._fired),
            },
        )

    def _mutual_information(self) -> float:
        # Adjacent-cell MI for binned V concentration, averaged horizontally and vertically.
        # The amplitude gate prevents floating-point remnants of an effectively homogeneous
        # field from being assigned a large normalised structure score.
        v = self._v
        if float(v.std()) < self.pattern_metric_floor:
            return 0.0
        lo = float(v.min())
        hi = float(v.max())
        if hi - lo < 1e-12:
            return 0.0
        edges = np.linspace(lo, hi, self.metric_bins + 1)

        def mi_pair(x: np.ndarray, y: np.ndarray) -> float:
            h, _, _ = np.histogram2d(x.ravel(), y.ravel(), bins=(edges, edges))
            total = h.sum()
            if total <= 0:
                return 0.0
            pxy = h / total
            px = pxy.sum(axis=1, keepdims=True)
            py = pxy.sum(axis=0, keepdims=True)
            denom = px @ py
            mask = pxy > 0
            return float(np.sum(pxy[mask] * np.log(pxy[mask] / denom[mask])))

        if self._active_boundary == "periodic":
            right = np.roll(v, -1, axis=1)
            down = np.roll(v, -1, axis=0)
            return 0.5 * (mi_pair(v, right) + mi_pair(v, down))
        return 0.5 * (mi_pair(v[:, :-1], v[:, 1:]) + mi_pair(v[:-1, :], v[1:, :]))

    def _spectral_peak_fraction(self) -> float:
        if float(self._v.std()) < self.pattern_metric_floor:
            return 0.0
        centered = self._v - float(self._v.mean())
        power = np.abs(np.fft.rfft2(centered)) ** 2
        total = float(power.sum())
        if total <= 1e-20:
            return 0.0
        power[0, 0] = 0.0
        return float(power.max() / max(float(power.sum()), 1e-20))

    def _metrics(self) -> dict[str, float]:
        v = self._v
        width = max(2, int(round(self.grid_size * self.center_probe_fraction)))
        lo = self.grid_size // 2 - width // 2
        hi = lo + width
        center_v = v[lo:hi, lo:hi]
        metrics = {
            # `state` exists only for backwards-compatible common-runner terminal aggregation.
            # It is explicitly the descriptive V-field standard deviation, not viability.
            "state": float(v.std()),
            "pde_step": float(self._step),
            "u_mean": float(self._u.mean()),
            "v_mean": float(v.mean()),
            "v_std": float(v.std()),
            "v_max": float(v.max()),
            "center_v_mean": float(center_v.mean()),
            "center_v_std": float(center_v.std()),
            "active_fraction_v_gt_0_05": float(np.mean(v > 0.05)),
            "spatial_mutual_information": self._mutual_information(),
            "spectral_peak_fraction": self._spectral_peak_fraction(),
        }
        return metrics


    def raw_state(self) -> Mapping[str, Any]:
        """Return copies of the primary concentration fields for archival storage."""
        return {
            "pde_step": int(self._step),
            "u": self._u.astype(np.float32, copy=True),
            "v": self._v.astype(np.float32, copy=True),
        }

    def snapshot(self) -> Mapping[str, Any]:
        return {
            **self._metrics(),
            "feed_active": self._feed_active,
            "boundary": self._active_boundary,
            "fired_interventions": sorted(self._fired),
        }

    def intervene(self, intervention_id: str) -> Mapping[str, Any]:
        if intervention_id == "GS_REMOVE_DRIVING_NOW":
            self._feed_active = False
        elif intervention_id == "GS_LOCAL_DAMAGE_NOW":
            width = max(2, int(round(self.grid_size * 0.20)))
            lo = self.grid_size // 2 - width // 2
            hi = lo + width
            self._u[lo:hi, lo:hi] = 1.0
            self._v[lo:hi, lo:hi] = 0.0
        else:
            raise EnvironmentOperationError(f"Unknown Gray-Scott intervention {intervention_id!r}")
        return dict(self.snapshot())

    def ablate(self, ablation_id: str) -> Mapping[str, Any]:
        return self.intervene(ablation_id)

    def corrupt(self, corruption_id: str) -> Mapping[str, Any]:
        raise EnvironmentOperationError(f"Gray-Scott B1 does not define corruption {corruption_id!r}")

    def restore(self, rescue_id: str) -> Mapping[str, Any]:
        if rescue_id == "GS_RESTORE_DRIVING_NOW":
            self._feed_active = True
            return dict(self.snapshot())
        raise EnvironmentOperationError(f"Unknown Gray-Scott rescue {rescue_id!r}")
