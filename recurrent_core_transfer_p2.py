"""P2 synthetic harness. Analytic. No training.

State seen by the E3 suite is z in R^8. When s = 0, the nuisance ν is carried
beside z and is not written into z. P2+ forecasts do not depend on ν.
"""

from __future__ import annotations

import numpy as np
import torch
from torch import nn

from recurrent_core_transfer_e3 import (
    angles_to_subspace,
    instrument,
    largest_angle,
    pack_suite,
    zero_effect_gap,
)
from recurrent_core_transfer_spec import KAPPA, NUISANCE_SPECTRAL, P2_DRAWS, P2_SCALES
from twostream_chart import forecasts as chart_forecasts
from twostream_constants import A, BX, BY, E, ETA


def draw_matrices(draw: int) -> dict:
    rng = np.random.default_rng(30000 + draw)
    gram = rng.standard_normal((8, 8))
    raw = rng.standard_normal((5, 5))
    drive = rng.normal(0.0, np.sqrt(1.0 / 5.0), size=5)
    readout = rng.normal(0.0, np.sqrt(1.0 / 5.0), size=(5, 8))
    orthogonal, triangular = np.linalg.qr(gram)
    signs = np.sign(np.diag(triangular))
    signs[signs == 0.0] = 1.0
    orthogonal = orthogonal * signs
    triangular = triangular * signs[:, None]
    radius = float(np.max(np.abs(np.linalg.eigvals(raw))))
    if radius == 0.0:
        raise RuntimeError("spectral radius 0 at draw %d" % draw)
    return {
        "Q": np.ascontiguousarray(orthogonal[:, :3], dtype=np.float64),
        "R": np.ascontiguousarray(orthogonal[:, 3:], dtype=np.float64),
        "A": np.ascontiguousarray(NUISANCE_SPECTRAL * raw / radius, dtype=np.float64),
        "a": np.ascontiguousarray(drive, dtype=np.float64),
        "C": np.ascontiguousarray(readout, dtype=np.float64),
        "diag_T": np.diag(triangular).astype(np.float64).copy(),
        "spectral_radius": float(np.max(np.abs(np.linalg.eigvals(NUISANCE_SPECTRAL * raw / radius)))),
    }


def observe_batch(mx, my, c, variable: str, bit):
    e = float(E)
    eta = float(ETA)
    bit = np.asarray(bit, dtype=np.float64)
    if variable == "X":
        observed, other = mx, my
    else:
        observed, other = my, mx
    p1 = e + eta * observed
    positive = bit >= 0.5
    predictive = np.where(positive, p1, 1.0 - p1)
    observed_2 = np.where(positive, (1.0 - e) * observed / predictive, e * observed / predictive)
    other_2 = np.where(positive, other + eta * c / predictive, other - eta * c / predictive)
    c_2 = e * (1.0 - e) * c / np.square(predictive)
    if variable == "X":
        return observed_2, other_2, c_2
    return other_2, observed_2, c_2


def transit_batch(mx, my, c):
    a = float(A)
    bx = float(BX)
    by = float(BY)
    mx2 = 0.5 + a * bx * (mx - 0.5)
    my2 = 0.5 + a * by * (my - 0.5)
    created = (1.0 - a * a) * (mx - 0.5) * (my - 0.5)
    c2 = bx * by * (c + created)
    return mx2, my2, c2


def repair_batch(mx, my, c):
    mx2 = np.clip(mx, 0.0, 1.0)
    my2 = np.clip(my, 0.0, 1.0)
    lower = np.maximum(-mx2 * my2, -(1.0 - mx2) * (1.0 - my2))
    upper = np.minimum(mx2 * (1.0 - my2), my2 * (1.0 - mx2))
    c2 = np.clip(c, lower, upper)
    changed = (mx2 != mx) | (my2 != my) | (c2 != c)
    return mx2, my2, c2, changed


def _forecast_rows(mx, my, c):
    out = np.zeros((len(mx), 3), dtype=np.float64)
    for index in range(len(mx)):
        qx, qy, qxor = chart_forecasts(float(mx[index]), float(my[index]), float(c[index]))
        out[index, 0] = float(qx)
        out[index, 1] = float(qy)
        out[index, 2] = float(qxor)
    return out


def encode_psi(phi: np.ndarray) -> np.ndarray:
    psi = np.zeros(phi.shape[:-1] + (5,), dtype=np.float64)
    psi[..., 0] = KAPPA * (phi[..., 0] - 0.5) ** 3
    psi[..., 1] = KAPPA * (phi[..., 1] - 0.5) ** 3
    psi[..., 2] = KAPPA * (4.0 * phi[..., 2]) ** 3
    return psi


def decode_psi(psi: np.ndarray) -> np.ndarray:
    mx = 0.5 + np.cbrt(psi[..., 0] / KAPPA)
    my = 0.5 + np.cbrt(psi[..., 1] / KAPPA)
    c = np.cbrt(psi[..., 2] / KAPPA) / 4.0
    return np.stack([mx, my, c], axis=-1)


class ChartHarness(nn.Module):
    def __init__(self, matrices: dict, scale: float, mode: str):
        super().__init__()
        if mode not in ("plus", "minus"):
            raise ValueError(mode)
        self.mode = mode
        self.scale = float(scale)
        self.Q = matrices["Q"]
        self.R = matrices["R"]
        self.A = matrices["A"]
        self.a = matrices["a"]
        self.C = matrices["C"]
        self._anchor = nn.Parameter(torch.zeros(1, dtype=torch.float64), requires_grad=False)
        self.reset_repairs()
        self._nu = None
        self._last_z = None
        self._psi_cache = {}

    def reset_repairs(self):
        self.repairs = np.zeros(8, dtype=np.int64)
        self.readout_repairs = 0

    def repair_snapshot(self):
        return self.repairs.copy(), int(self.readout_repairs)

    def initial_state(self, batch: int, dtype, device):
        phi = np.array([0.5, 0.5, 0.0], dtype=np.float64)
        if self.mode == "plus":
            nu = np.zeros(5, dtype=np.float64)
            z0 = self.Q @ phi + self.scale * (self.R @ nu)
        else:
            z0 = self.Q @ phi + self.R @ encode_psi(phi)
        z = np.repeat(z0[None, :], batch, axis=0)
        self._nu = np.zeros((batch, 5), dtype=np.float64)
        self._psi_cache = {}
        if self.mode == "minus":
            self._remember_psi(np.repeat(encode_psi(phi)[None, :], batch, axis=0), z)
        tensor = torch.from_numpy(np.ascontiguousarray(z)).to(dtype=dtype, device=device)
        self._last_z = tensor.detach().cpu().numpy()
        return tensor

    @staticmethod
    def _psi_key(row: np.ndarray):
        return tuple(np.round(row, decimals=8))

    def _remember_psi(self, psi: np.ndarray, z: np.ndarray) -> None:
        leaked = z @ self.R
        for exact, approx in zip(psi, leaked):
            stored = np.array(exact, dtype=np.float64, copy=True)
            self._psi_cache[self._psi_key(exact)] = stored
            self._psi_cache[self._psi_key(approx)] = stored

    def _recall_psi(self, z: np.ndarray) -> np.ndarray:
        approx = z @ self.R
        out = np.empty_like(approx)
        for index in range(z.shape[0]):
            stored = self._psi_cache.get(self._psi_key(approx[index]))
            if stored is not None and float(np.linalg.norm(stored - approx[index])) <= 1e-8:
                out[index] = stored
            else:
                out[index] = approx[index]
        return out

    def _nuisance(self, z, stage_idx: int):
        if self.scale > 0.0:
            return z @ self.R / self.scale
        if (
            self._nu is not None
            and self._last_z is not None
            and self._last_z.shape == z.shape
            and np.array_equal(self._last_z, z)
        ):
            return self._nu
        return np.zeros((z.shape[0], 5), dtype=np.float64)

    def step(self, state, bit, stage_idx: int):
        z = state.detach().cpu().numpy().astype(np.float64, copy=False)
        k = stage_idx + 1
        variable = "X" if (k % 2) == 1 else "Y"
        bit_np = bit.detach().cpu().numpy().astype(np.float64, copy=False)
        if self.mode == "plus":
            phi = z @ self.Q
            nu = self._nuisance(z, stage_idx)
            mx, my, c, changed = repair_batch(phi[:, 0], phi[:, 1], phi[:, 2])
            self.repairs[stage_idx] += int(np.sum(changed))
            if k > 1:
                mx, my, c = transit_batch(mx, my, c)
            mx, my, c = observe_batch(mx, my, c, variable, bit_np)
            phi = np.stack([mx, my, c], axis=1)
            rhat = bit_np * 2.0 - 1.0
            nu = np.tanh(nu @ self.A.T + rhat[:, None] * self.a[None, :] + self.C[:, k - 1][None, :])
            z_new = phi @ self.Q.T + self.scale * (nu @ self.R.T)
            self._nu = nu
        else:
            psi = self._recall_psi(z)
            phi = decode_psi(psi)
            phi_c = z @ self.Q
            mx, my, c, changed = repair_batch(phi[:, 0], phi[:, 1], phi[:, 2])
            self.repairs[stage_idx] += int(np.sum(changed))
            if k > 1:
                mx, my, c = transit_batch(mx, my, c)
            mx, my, c = observe_batch(mx, my, c, variable, bit_np)
            phi = np.stack([mx, my, c], axis=1)
            if k <= 4:
                phi_c = phi
            psi_new = encode_psi(phi)
            z_new = phi_c @ self.Q.T + psi_new @ self.R.T
            self._remember_psi(psi_new, z_new)
        tensor = torch.from_numpy(np.ascontiguousarray(z_new))
        self._last_z = tensor.detach().cpu().numpy()
        return tensor

    def readout(self, state):
        z = state.detach().cpu().numpy().astype(np.float64, copy=False)
        if self.mode == "plus":
            phi = z @ self.Q
        else:
            phi = decode_psi(self._recall_psi(z))
        mx, my, c, changed = repair_batch(phi[:, 0], phi[:, 1], phi[:, 2])
        self.readout_repairs += int(np.sum(changed))
        forecasts = _forecast_rows(mx, my, c)
        return torch.from_numpy(np.ascontiguousarray(forecasts))


def _decoder_public(decoder: dict, q_matrix: np.ndarray) -> dict:
    angles = {}
    for fold in (0, 1):
        to_q = angles_to_subspace(decoder["bases"][fold], q_matrix)
        angles[str(fold)] = {
            "to_span_Q_deg": to_q,
            "largest_to_span_Q_deg": largest_angle(to_q),
            "r2": decoder["folds"][fold]["r2"],
            "rmse": decoder["folds"][fold]["rmse"],
            "singular_values": decoder["folds"][fold]["singular_values"],
            "rank": decoder["folds"][fold]["rank"],
        }
    return {
        "folds": angles,
        "interfold_angles_deg": decoder["interfold_angles_deg"],
        "largest_interfold_angle_deg": decoder["largest_interfold_angle_deg"],
        "label": None,
    }


def run_draw_scale(matrices: dict, scale: float, world, mode: str = "plus") -> dict:
    harness = ChartHarness(matrices, scale, mode)
    fitted = instrument(harness, world, basis_override=None)
    known = None
    if mode == "plus":
        known_harness = ChartHarness(matrices, scale, mode)
        known = instrument(known_harness, world, basis_override=matrices["Q"])
    public_decoder = _decoder_public(fitted["decoder"], matrices["Q"])
    from recurrent_core_transfer_e3 import decoder_label

    public_decoder["label"] = decoder_label(fitted["decoder"])
    record = {
        "scale": scale,
        "mode": mode,
        "decoder": public_decoder,
        "fitted": pack_suite(fitted["suite"]),
        "rollout_repairs": _pack_repairs(fitted["rollout_repairs"]),
    }
    if known is not None:
        record["known_q"] = pack_suite(known["suite"])
        record["known_q_rollout_repairs"] = _pack_repairs(known["rollout_repairs"])
    if mode == "minus":
        # The required check transplants along Q, not along the fitted basis.
        q_harness = ChartHarness(matrices, 0.0, "minus")
        q_run = instrument(q_harness, world, basis_override=matrices["Q"])
        gap = zero_effect_gap(q_run["suite"], q_run["predictions"])
        record["zero_effect_gap"] = gap
        record["zero_effect_ok"] = bool(gap is not None and gap <= 1e-12)
        record["fitted_descriptive_localized"] = bool(fitted["suite"]["localized"])
    return record


def _pack_repairs(snapshot) -> dict | None:
    if snapshot is None:
        return None
    stages, readout = snapshot
    return {"per_stage": [int(value) for value in stages], "readout": int(readout)}


def summarize_p2(records: list[dict]) -> dict:
    """records are P2+ results, one dict per (draw, scale) in draw-major order."""
    from recurrent_core_transfer_spec import P2_PIPELINE_SCALES, PIPELINE_NOT, PIPELINE_OK

    by_scale = {scale: [] for scale in P2_SCALES}
    for record in records:
        by_scale[record["scale"]].append(record)
    per_scale = {}
    known_ok = True
    fitted_ok = True
    for scale, rows in by_scale.items():
        known_count = sum(1 for row in rows if row["known_q"]["localized"])
        fitted_count = sum(1 for row in rows if row["fitted"]["localized"])
        angles = [
            row["decoder"]["folds"][fold]["largest_to_span_Q_deg"]
            for row in rows
            for fold in ("0", "1")
            if row["decoder"]["folds"][fold]["largest_to_span_Q_deg"] is not None
        ]
        per_scale[str(scale)] = {
            "n": len(rows),
            "known_q_localized": known_count,
            "fitted_localized": fitted_count,
            "median_largest_angle_to_span_Q_deg": float(np.median(angles)) if angles else None,
            "known_q_ratio_medians": _ratio_medians(rows, "known_q"),
            "fitted_ratio_medians": _ratio_medians(rows, "fitted"),
        }
        if known_count != len(rows):
            known_ok = False
        if scale in P2_PIPELINE_SCALES and fitted_count < 95:
            fitted_ok = False
    valid = known_ok and fitted_ok
    return {
        "per_scale": per_scale,
        "known_q_localized_all_scales": known_ok,
        "fitted_localized_low_nuisance": fitted_ok,
        "pipeline_valid": valid,
        "label": PIPELINE_OK if valid else PIPELINE_NOT,
        "note": (
            "At zero nuisance the 100 rotations are largely equivalent tests, "
            "not 100 independent demonstrations of detection power."
        ),
    }


def _ratio_medians(rows, key) -> dict:
    out = {}
    for name in ("partial", "complement", "wrong"):
        for kind in ("vector", "xor"):
            values = []
            for row in rows:
                ratios = row[key]["ratios"]
                if not ratios:
                    continue
                value = ratios[name][kind]["e3_v2"]
                if value == "UNDEFINED":
                    continue
                if value == "+inf":
                    values.append(np.inf)
                elif value == "-inf":
                    values.append(-np.inf)
                else:
                    values.append(float(value))
            out["%s_%s" % (name, kind)] = None if not values else _median_pack(values)
    return out


def _median_pack(values):
    number = float(np.median(values))
    if np.isinf(number):
        return "+inf" if number > 0 else "-inf"
    return number


def run_p2(world) -> dict:
    plus = []
    minus = []
    for draw in P2_DRAWS:
        matrices = draw_matrices(draw)
        for scale in P2_SCALES:
            plus.append({"draw": draw, **run_draw_scale(matrices, scale, world, "plus")})
        minus.append({"draw": draw, **run_draw_scale(matrices, 0.0, world, "minus")})
        if draw % 10 == 0:
            print("p2 draw %d" % draw, flush=True)
    gaps = [row["zero_effect_gap"] for row in minus]
    finite_gaps = [gap for gap in gaps if gap is not None]
    zero_ok = bool(minus) and all(row["zero_effect_ok"] for row in minus)
    summary = summarize_p2(plus)
    summary["p2_minus"] = {
        "n": len(minus),
        "zero_effect_ok": zero_ok,
        "max_abs_change": None if not finite_gaps else float(max(finite_gaps)),
        "invalid": not zero_ok,
        "fitted_localized": sum(1 for row in minus if row["fitted_descriptive_localized"]),
        "note": (
            "Fitted-decoder behavior on the unused-copy harness is descriptive only. "
            "Non-localization is not a gate. A failed zero-effect check invalidates "
            "P2− and does not by itself relabel the P2+ pipeline."
        ),
    }
    return {"summary": summary, "plus": plus, "minus": minus}
