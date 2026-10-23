"""History domain, certificate weights and oracle targets, folds, feature blocks.

No checkpoint is read here. q and P(h) come from the W2 certificate.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from fractions import Fraction

import numpy as np

REPO = "/workspace"
CERTIFICATE_SPEC = "origin/pr/10:twostream_results_v1/results.json"
CERTIFICATE_SHA_PREFIX = "bf2de92c"

VAR_MAX = 1e-24  # weighted population variance; one rule for §5 and §9
PRIMARY_LAMBDA = float("1e-3")
LAMBDA_GRID = tuple(float("1e%d" % k) for k in range(-6, 2))
BOUNDARY_GUARD = 1e-10
REPLAY_ATOL = 1e-12
FORWARD_ATOL = 1e-10

GROUPS = {
    "A": frozenset({0, 5, 10, 15}),
    "B": frozenset({1, 4, 11, 14}),
    "C": frozenset({2, 7, 8, 13}),
    "D": frozenset({3, 6, 9, 12}),
}
FOLDS = (
    ("AB|CD", ("A", "B"), ("C", "D")),
    ("CD|AB", ("C", "D"), ("A", "B")),
    ("AC|BD", ("A", "C"), ("B", "D")),
    ("BD|AC", ("B", "D"), ("A", "C")),
    ("AD|BC", ("A", "D"), ("B", "C")),
    ("BC|AD", ("B", "C"), ("A", "D")),
)
ACBD_FOLDS = ("AC|BD", "BD|AC")
G_MASKS = (0x00, 0x55, 0xAA, 0xFF)

# Executable constants required by spec §7. Filled from the certificate and checked.
SPEC_R_ORACLE = "0.5823877685694766"
SPEC_VAR_W_Q = "0.16761223143052342"
SPEC_FLOOR = "0.005823877685694766"
SPEC_R2_FLOOR = "0.034746137772820054"


def history_bits() -> np.ndarray:
    bits = np.zeros((256, 8), dtype=np.float64)
    for history in range(256):
        for stage in range(8):
            bits[history, stage] = (history >> stage) & 1
    return bits


def bits_sha256(bits: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(bits, dtype=np.float64).tobytes()).hexdigest()


def is_test_history(history: int) -> bool:
    return ((history % 16) + (history // 16)) % 4 == 0


def is_val_history(history: int) -> bool:
    prefix = history % 16
    continuation = history // 16
    if (prefix + continuation) % 4 != 2:
        return False
    if continuation == (2 - prefix) % 16:
        return False
    return True


def val_histories() -> np.ndarray:
    return np.array([h for h in range(256) if is_val_history(h)], dtype=np.int64)


def depth5_orbit_key(history: int):
    prefix = history & 31
    return tuple(sorted(prefix ^ (mask & 31) for mask in G_MASKS))


def group_names() -> np.ndarray:
    names = np.empty(256, dtype=object)
    prefix = np.array([h & 15 for h in range(256)])
    for name, members in GROUPS.items():
        names[np.isin(prefix, list(members))] = name
    if any(v is None for v in names):
        raise RuntimeError("a history has no depth-4 group")
    return names


def fold_indices(names: np.ndarray):
    folds = []
    for name, fit_groups, eval_groups in FOLDS:
        fit = np.flatnonzero(np.isin(names, fit_groups))
        ev = np.flatnonzero(np.isin(names, eval_groups))
        if len(fit) != 128 or len(ev) != 128:
            raise RuntimeError("fold %s is not 128/128" % name)
        orbits = {}
        for h in fit:
            orbits.setdefault(depth5_orbit_key(int(h)), []).append(int(h))
        if len(orbits) != 4 or any(len(v) != 32 for v in orbits.values()):
            raise RuntimeError("fold %s is not four depth-5 orbits of 32" % name)
        folds.append(
            {
                "name": name,
                "fit": fit.astype(np.int64),
                "eval": ev.astype(np.int64),
                "orbits": [np.array(sorted(v), dtype=np.int64) for v in orbits.values()],
            }
        )
    return folds


def bin_plus(bits: np.ndarray) -> tuple[np.ndarray, list[str]]:
    reading = 2.0 * bits - 1.0
    names = ["r%d" % i for i in range(8)]
    cols = [reading[:, i] for i in range(8)]
    for i, j in itertools.combinations(range(8), 2):
        names.append("r%dr%d" % (i, j))
        cols.append(reading[:, i] * reading[:, j])
    return np.column_stack(cols), names


def conf_features(outputs: np.ndarray) -> tuple[np.ndarray, list[str]]:
    prod = outputs * (1.0 - outputs)
    names = ["f%d" % i for i in range(3)] + ["f%d(1-f%d)" % (i, i) for i in range(3)]
    return np.concatenate([outputs, prod], axis=1), names


def state_features(state: np.ndarray) -> tuple[np.ndarray, list[str]]:
    return np.asarray(state, dtype=np.float64), ["s%d" % i for i in range(state.shape[1])]


def fq_features(outputs: np.ndarray, q: np.ndarray) -> tuple[np.ndarray, list[str]]:
    cols = []
    names = []
    for j in range(3):
        fj = outputs[:, j]
        qj = q[:, j]
        cols.extend([fj, qj, fj * fj, qj * qj, fj * qj])
        names.extend(["f%d" % j, "q%d" % j, "f%d^2" % j, "q%d^2" % j, "f%d*q%d" % (j, j)])
    return np.column_stack(cols), names


def load_certificate_bytes() -> bytes:
    raw = subprocess.check_output(["git", "-C", REPO, "show", CERTIFICATE_SPEC])
    digest = hashlib.sha256(raw).hexdigest()
    if not digest.startswith(CERTIFICATE_SHA_PREFIX):
        raise RuntimeError("certificate sha %s does not start with %s" % (digest, CERTIFICATE_SHA_PREFIX))
    return raw


def _frac(record) -> Fraction:
    return Fraction(record["exact"])


class World:
    def __init__(self, raw: bytes):
        payload = json.loads(raw)
        self.probability_fraction = [Fraction(0) for _ in range(256)]
        self.q_fraction = [(Fraction(0), Fraction(0), Fraction(0)) for _ in range(256)]
        self.covariance_fraction = [Fraction(0) for _ in range(256)]
        probability = np.zeros(256, dtype=np.float64)
        q = np.zeros((256, 3), dtype=np.float64)
        for row in payload["per_history"]:
            h = int(row["history"])
            p = _frac(row["probability"])
            mx = _frac(row["marginal_x"])
            my = _frac(row["marginal_y"])
            c = _frac(row["covariance"])
            qx, qy, qz = mx, my, mx + my - 2 * (mx * my + c)
            stored = _frac(row["xor_joint"])
            if qz != stored:
                raise RuntimeError("XOR forecast disagrees with xor_joint at %d" % h)
            self.probability_fraction[h] = p
            self.q_fraction[h] = (qx, qy, qz)
            self.covariance_fraction[h] = c
            probability[h] = float(p)
            q[h] = (float(qx), float(qy), float(qz))
        if sum(self.probability_fraction) != 1:
            raise RuntimeError("certificate probabilities do not sum to 1")
        self.probability = probability
        self.q = q
        self.is_test = np.array([is_test_history(h) for h in range(256)], dtype=bool)
        self.bits = history_bits()
        self.bits_sha256 = bits_sha256(self.bits)
        self.names = group_names()
        self.folds = fold_indices(self.names)
        self.bin_plus, self.bin_plus_names = bin_plus(self.bits)
        ro, var_q, floor, r2_floor = executable_constants(self)
        self.R_oracle = ro
        self.Var_w_q = var_q
        self.floor = floor
        self.r2_floor = r2_floor
        self.var_q_uniform = population_variance(np.full(256, 1.0 / 256.0), q)
        self.thr_total, self.thr_xor = afit_test_thresholds(self)
        self.total_mass = float(probability.sum())

    def split_weights(self, test: bool) -> np.ndarray:
        mask = self.is_test if test else ~self.is_test
        weights = np.zeros(256, dtype=np.float64)
        mass = float(self.probability[mask].sum())
        weights[mask] = self.probability[mask] / mass
        return weights


def population_variance(w: np.ndarray, values: np.ndarray) -> float:
    weight = np.asarray(w, dtype=np.float64)
    weight = weight / weight.sum()
    array = np.asarray(values, dtype=np.float64)
    if array.ndim == 1:
        mu = float(weight @ array)
        return float(weight @ (array - mu) ** 2)
    mu = weight @ array
    return float(np.sum(weight[:, None] * (array - mu) ** 2))


def executable_constants(world: World):
    """Exact-rational R_oracle, Var_w(q), floor and R^2 floor, each floated once."""
    ro = Fraction(0)
    for p, qs in zip(world.probability_fraction, world.q_fraction):
        ro += p * sum(q * (1 - q) for q in qs)
    mu = []
    for j in range(3):
        mu.append(sum(p * qs[j] for p, qs in zip(world.probability_fraction, world.q_fraction)))
    var_q = Fraction(0)
    for p, qs in zip(world.probability_fraction, world.q_fraction):
        var_q += p * sum((qs[j] - mu[j]) ** 2 for j in range(3))
    if ro + var_q != Fraction(3, 4):
        raise RuntimeError("R_oracle + Var_w(q) is not 3/4")
    ro_f = float(ro)
    var_f = float(var_q)
    floor = float(ro / 100)
    r2_floor = float((ro / 100) / var_q)
    if repr(ro_f) != SPEC_R_ORACLE or repr(var_f) != SPEC_VAR_W_Q:
        raise RuntimeError("executable constants %r %r" % (ro_f, var_f))
    if repr(floor) != SPEC_FLOOR or repr(r2_floor) != SPEC_R2_FLOOR:
        raise RuntimeError("floor constants %r %r" % (floor, r2_floor))
    return ro_f, var_f, floor, r2_floor


def afit_test_thresholds(world: World):
    """TEST afit thresholds, matching World.afit_threshold in the source studies."""

    def rows(test: bool):
        return [h for h in range(256) if bool(world.is_test[h]) is test]

    def current_only_total(test: bool) -> Fraction:
        chosen = rows(test)
        mass = sum(world.probability_fraction[h] for h in chosen)
        means = {}
        for bit in (0, 1):
            group = [h for h in chosen if ((h >> 7) & 1) == bit]
            group_mass = sum(world.probability_fraction[h] for h in group)
            acc = [Fraction(0), Fraction(0), Fraction(0)]
            for h in group:
                weight = world.probability_fraction[h]
                for i in range(3):
                    acc[i] += weight * world.q_fraction[h][i]
            means[bit] = tuple(value / group_mass for value in acc)
        excess = [Fraction(0), Fraction(0), Fraction(0)]
        for h in chosen:
            bit = (h >> 7) & 1
            weight = world.probability_fraction[h] / mass
            for i in range(3):
                gap = means[bit][i] - world.q_fraction[h][i]
                excess[i] += weight * gap * gap
        return excess[0] + excess[1] + excess[2]

    def four_c2(test: bool) -> Fraction:
        chosen = rows(test)
        mass = sum(world.probability_fraction[h] for h in chosen)
        total = Fraction(0)
        for h in chosen:
            c = world.covariance_fraction[h]
            total += (world.probability_fraction[h] / mass) * (4 * c * c)
        return total

    return float(current_only_total(True) * Fraction(1, 4)), float(four_c2(True) * Fraction(1, 4))


def load_world() -> World:
    return World(load_certificate_bytes())
