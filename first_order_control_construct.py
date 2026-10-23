"""First-order-matched path construction.

g_k is never overwritten. Orthogonality uses gh_k. r_k = ||d_k - p_k|| is the
radius that enters the gate. The square-root form is stored and does not gate.
A failure returns ok=False and no paths. This module does not draw randomness.
"""

from __future__ import annotations

import math

import numpy as np
import torch

from graded_reversion_spec import EPS0, GATE_ROWS
from first_order_control_spec import (
    BLOCKS,
    FO_REL_TOL,
    G_ZERO,
    N_PATHS,
    NORM_REL_TOL,
    ORTH_TOL,
    PROJECTION_FAIL_REL,
    RADIUS_REL_TOL,
    RHO_COLLAPSE,
    RHO_NEAR,
)


def _as_f64(matrix) -> torch.Tensor:
    if isinstance(matrix, torch.Tensor):
        tensor = matrix.detach().to(dtype=torch.float64).cpu().contiguous()
    else:
        tensor = torch.from_numpy(np.ascontiguousarray(matrix, dtype=np.float64))
    return tensor


def _vec(block: torch.Tensor) -> torch.Tensor:
    return block.contiguous().reshape(-1)


def exactly_zero(vector: torch.Tensor) -> bool:
    return bool(torch.all(vector == 0))


def radius_quantities(d_vec: torch.Tensor, g_vec: torch.Tensor) -> dict:
    """Authoritative residual radius and the cancellation-safe gate.

    The sqrt form is descriptive. A negative inside value is reported as None
    for the square root and does not decide the gate.
    """
    d_norm2 = torch.dot(d_vec, d_vec)
    g_norm2 = torch.dot(g_vec, g_vec)
    if float(g_norm2) == 0.0:
        raise ValueError("radius quantities require a nonzero gradient")
    a_k = torch.dot(g_vec, d_vec) / g_norm2
    p_vec = a_k * g_vec
    residual_vec = d_vec - p_vec
    r_k = torch.linalg.vector_norm(residual_vec)
    p_norm2 = torch.dot(p_vec, p_vec)
    gate_abs = torch.abs(d_norm2 - p_norm2 - r_k * r_k)
    gate_tol = RADIUS_REL_TOL * d_norm2
    inside = d_norm2 - (a_k * a_k) * g_norm2
    inside_f = float(inside)
    if inside_f < 0.0:
        sqrt_form = None
    else:
        sqrt_form = float(torch.sqrt(inside))
    return {
        "a_k": float(a_k),
        "p_vec": p_vec,
        "r_k": float(r_k),
        "gate_abs": float(gate_abs),
        "gate_tol": float(gate_tol),
        "gate_ok": bool(float(gate_abs) <= float(gate_tol)),
        "sqrt_inside": inside_f,
        "sqrt_form": sqrt_form,
    }


def _sign(a_k: float) -> str:
    if a_k < 0.0:
        return "negative"
    if a_k > 0.0:
        return "positive"
    return "zero"


def _empty_block(name: str) -> dict:
    return {
        "block": name,
        "zero_displacement": False,
        "exactly_zero_gradient": False,
        "negligible_first_order_scale": False,
        "collapsed": False,
        "near_collapse": False,
        "fixed": False,
        "fallback_isotropic": False,
        "a_k": None,
        "a_k_sign": None,
        "rho": None,
        "r_k": None,
        "g_norm": None,
        "d_norm": None,
        "g_dot_d": None,
        "cos": None,
        "radius_gate_abs": None,
        "radius_ok": None,
        "sqrt_inside": None,
        "sqrt_form": None,
        "norm_ok": None,
        "fo_ok": None,
        "orth_ok": None,
        "orth_applicable": False,
        "worst_norm_relative": None,
        "worst_fo_relative": None,
        "worst_orth_abs": None,
    }


def construct_fo_paths(delta, gradient, draws) -> dict:
    """Build 32 assembled displacements E_j, or ok=False with paths None."""
    delta_t = _as_f64(delta)
    grad_t = _as_f64(gradient)
    draw_t = _as_f64(draws)
    if tuple(delta_t.shape) != (24, 8) or tuple(grad_t.shape) != (24, 8):
        raise ValueError("delta and gradient must be 24x8")
    if tuple(draw_t.shape) != (N_PATHS, 24, 8):
        raise ValueError("draws must be (32, 24, 8)")
    reasons = []
    if not bool(torch.isfinite(delta_t).all() and torch.isfinite(grad_t).all() and torch.isfinite(draw_t).all()):
        reasons.append("nonfinite input")
    paths = torch.zeros((N_PATHS, 24, 8), dtype=torch.float64)
    blocks = {}
    g_before = {name: grad_t[GATE_ROWS[name][0]:GATE_ROWS[name][1], :].clone() for name in BLOCKS}
    for name in BLOCKS:
        row0, row1 = GATE_ROWS[name]
        d_block = delta_t[row0:row1, :]
        g_block = grad_t[row0:row1, :]
        d_vec = _vec(d_block)
        g_vec = _vec(g_block)
        info = _empty_block(name)
        d_norm = float(torch.linalg.vector_norm(d_vec))
        g_norm = float(torch.linalg.vector_norm(g_vec))
        g_dot_d = float(torch.dot(g_vec, d_vec))
        info["d_norm"] = d_norm
        info["g_norm"] = g_norm
        info["g_dot_d"] = g_dot_d
        info["cos"] = None if d_norm == 0.0 or g_norm == 0.0 else float(g_dot_d / (g_norm * d_norm))
        info["negligible_first_order_scale"] = bool(g_norm * d_norm <= G_ZERO)
        e_rows = torch.zeros((N_PATHS, row1 - row0, 8), dtype=torch.float64)
        if reasons:
            blocks[name] = info
            continue
        if d_norm <= EPS0:
            info["zero_displacement"] = True
            info["norm_ok"] = True
            info["fo_ok"] = True
            info["r_k"] = 0.0
            info["rho"] = None
            blocks[name] = info
            paths[:, row0:row1, :] = e_rows
            continue
        z_rows = draw_t[:, row0:row1, :]
        if exactly_zero(g_vec):
            info["exactly_zero_gradient"] = True
            info["fallback_isotropic"] = True
            info["r_k"] = d_norm
            info["rho"] = 1.0
            info["near_collapse"] = False
            info["collapsed"] = False
            norm_ok = True
            fo_ok = True
            worst_norm = 0.0
            for index in range(N_PATHS):
                z_vec = _vec(z_rows[index])
                z_norm = float(torch.linalg.vector_norm(z_vec))
                if z_norm == 0.0 or not math.isfinite(z_norm):
                    reasons.append("%s: zero base draw" % name)
                    norm_ok = False
                    break
                e_vec = (d_norm / z_norm) * z_vec
                e_rows[index] = e_vec.reshape(row1 - row0, 8)
                e_norm = float(torch.linalg.vector_norm(e_vec))
                relative = abs(e_norm - d_norm) / d_norm
                worst_norm = max(worst_norm, relative)
                if relative > NORM_REL_TOL:
                    norm_ok = False
                    reasons.append("%s: isotropic norm" % name)
                # Both inner products are exactly zero when g is exactly zero.
                if float(torch.dot(g_vec, e_vec)) != 0.0 or g_dot_d != 0.0:
                    fo_ok = False
                    reasons.append("%s: isotropic derivative" % name)
            info["norm_ok"] = norm_ok
            info["fo_ok"] = fo_ok
            info["worst_norm_relative"] = worst_norm
            info["worst_fo_relative"] = 0.0
            blocks[name] = info
            paths[:, row0:row1, :] = e_rows
            continue
        try:
            radius = radius_quantities(d_vec, g_vec)
        except ValueError as exc:
            reasons.append("%s: %s" % (name, exc))
            blocks[name] = info
            continue
        info["a_k"] = radius["a_k"]
        info["a_k_sign"] = _sign(radius["a_k"])
        info["r_k"] = radius["r_k"]
        info["rho"] = radius["r_k"] / d_norm
        info["radius_gate_abs"] = radius["gate_abs"]
        info["radius_ok"] = radius["gate_ok"]
        info["sqrt_inside"] = radius["sqrt_inside"]
        info["sqrt_form"] = radius["sqrt_form"]
        info["near_collapse"] = bool(info["rho"] <= RHO_NEAR)
        info["collapsed"] = bool(info["rho"] <= RHO_COLLAPSE)
        info["fixed"] = info["collapsed"]
        if not radius["gate_ok"]:
            reasons.append("%s: radius gate" % name)
            blocks[name] = info
            continue
        gh = g_vec / torch.linalg.vector_norm(g_vec)
        p_vec = radius["p_vec"]
        r_k = radius["r_k"]
        norm_ok = True
        fo_ok = True
        orth_ok = True
        worst_norm = 0.0
        worst_fo = 0.0
        worst_orth = 0.0
        if info["collapsed"]:
            for index in range(N_PATHS):
                e_rows[index] = d_block.clone()
            info["orth_applicable"] = False
            info["norm_ok"] = True
            info["fo_ok"] = True
            info["orth_ok"] = None
            info["worst_norm_relative"] = 0.0
            info["worst_fo_relative"] = 0.0
            blocks[name] = info
            paths[:, row0:row1, :] = e_rows
            continue
        info["orth_applicable"] = True
        for index in range(N_PATHS):
            z_vec = _vec(z_rows[index])
            z_norm = float(torch.linalg.vector_norm(z_vec))
            if z_norm == 0.0 or not math.isfinite(z_norm):
                reasons.append("%s: zero base draw j=%d" % (name, index + 1))
                norm_ok = False
                break
            y_vec = z_vec - torch.dot(z_vec, gh) * gh
            y_vec = y_vec - torch.dot(y_vec, gh) * gh
            y_norm = float(torch.linalg.vector_norm(y_vec))
            if y_norm <= PROJECTION_FAIL_REL * z_norm:
                reasons.append("%s: projection failure j=%d" % (name, index + 1))
                norm_ok = False
                break
            u_vec = y_vec / y_norm
            orth_abs = abs(float(torch.dot(u_vec, gh)))
            unit_gap = abs(float(torch.linalg.vector_norm(u_vec)) - 1.0)
            worst_orth = max(worst_orth, orth_abs, unit_gap)
            if orth_abs > ORTH_TOL or unit_gap > ORTH_TOL:
                orth_ok = False
                reasons.append("%s: orthogonality j=%d" % (name, index + 1))
            e_vec = p_vec + r_k * u_vec
            e_rows[index] = e_vec.reshape(row1 - row0, 8)
            e_norm = float(torch.linalg.vector_norm(e_vec))
            norm_rel = abs(e_norm - d_norm) / d_norm
            fo_scale = g_norm * d_norm
            fo_abs = abs(float(torch.dot(g_vec, e_vec)) - g_dot_d)
            fo_rel = fo_abs / fo_scale if fo_scale > 0.0 else fo_abs
            worst_norm = max(worst_norm, norm_rel)
            worst_fo = max(worst_fo, fo_rel)
            if norm_rel > NORM_REL_TOL:
                norm_ok = False
                reasons.append("%s: norm j=%d" % (name, index + 1))
            if fo_abs > FO_REL_TOL * fo_scale:
                fo_ok = False
                reasons.append("%s: derivative j=%d" % (name, index + 1))
        info["norm_ok"] = norm_ok
        info["fo_ok"] = fo_ok
        info["orth_ok"] = orth_ok
        info["worst_norm_relative"] = worst_norm
        info["worst_fo_relative"] = worst_fo
        info["worst_orth_abs"] = worst_orth
        blocks[name] = info
        paths[:, row0:row1, :] = e_rows
    for name in BLOCKS:
        if not torch.equal(g_before[name], grad_t[GATE_ROWS[name][0]:GATE_ROWS[name][1], :]):
            reasons.append("%s: g_k overwritten" % name)
    full_norm = float(torch.linalg.vector_norm(delta_t))
    r_eff2 = 0.0
    fixed = []
    negligible = []
    for name in BLOCKS:
        info = blocks[name]
        if info["collapsed"]:
            fixed.append(name)
        if info["negligible_first_order_scale"]:
            negligible.append(name)
        if info["collapsed"] or info["zero_displacement"]:
            continue
        if info["r_k"] is None:
            continue
        r_eff2 += float(info["r_k"]) ** 2
    r_eff = math.sqrt(r_eff2)
    if full_norm <= EPS0:
        r_ratio = None
        primary_collapsed = False
        primary_near = False
    else:
        r_ratio = r_eff / full_norm
        primary_collapsed = bool(r_ratio <= RHO_COLLAPSE)
        primary_near = bool(r_ratio <= RHO_NEAR)
    assembled_norm_ok = False
    assembled_fo_ok = False
    if not reasons:
        got = torch.linalg.vector_norm(paths, dim=(1, 2))
        if full_norm <= EPS0:
            assembled_norm_ok = bool(torch.all(got <= EPS0))
        else:
            assembled_norm_ok = bool(torch.max(torch.abs(got - full_norm) / full_norm) <= NORM_REL_TOL)
        g_flat = _vec(grad_t)
        d_flat = _vec(delta_t)
        target_dot = float(torch.dot(g_flat, d_flat))
        dots = paths.reshape(N_PATHS, -1) @ g_flat
        scale = float(torch.linalg.vector_norm(grad_t) * full_norm)
        if scale <= 0.0:
            assembled_fo_ok = bool(torch.max(torch.abs(dots - target_dot)) == 0)
        else:
            assembled_fo_ok = bool(torch.max(torch.abs(dots - target_dot)) <= FO_REL_TOL * scale)
        if not assembled_norm_ok:
            reasons.append("assembled norm")
        if not assembled_fo_ok:
            reasons.append("assembled derivative")
    ok = len(reasons) == 0
    return {
        "ok": ok,
        "reasons": reasons,
        "paths": None if not ok else paths.numpy(),
        "blocks": blocks,
        "fixed_blocks": fixed,
        "negligible_blocks": negligible,
        "R_eff": r_eff,
        "R_eff_over_delta": r_ratio,
        "primary_collapsed": primary_collapsed,
        "primary_near_collapse": primary_near,
        "delta_norm": full_norm,
        "assembled_norm_ok": assembled_norm_ok,
        "assembled_fo_ok": assembled_fo_ok,
        "g_preserved": all(
            torch.equal(g_before[name], grad_t[GATE_ROWS[name][0]:GATE_ROWS[name][1], :]) for name in BLOCKS
        ),
    }
