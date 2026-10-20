"""Oracle for the acquisition study.

Terminal forecasts and history probabilities are the frozen
``twostream_results_v1/results.json`` values. Prefix beliefs used as analysis
decoders are the same filter that produced that file. Nothing here trains.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np

from twostream_chart import forecasts, marginals_covariance
from twostream_constants import variable_at
from twostream_filter import filter_prefix, fraction_transition
from twostream_score import current_only_terminal
from twostream_acquisition_spec import is_test_history

ROOT = Path(__file__).resolve().parent
RESULTS_PATH = ROOT / "twostream_results_v1" / "results.json"

QUERIES = ("X", "Y", "XOR")


def _frac(record) -> Fraction:
    return Fraction(record["exact"])


def popcount(value: int) -> int:
    return bin(value).count("1")


def parity_fold(prefix: int) -> int:
    """Fold 0 = even bit count, fold 1 = odd bit count."""
    return popcount(prefix) & 1


class World:
    """Frozen W2 quantities needed by evaluation. Built once per process."""

    def __init__(self, results_path: Path = RESULTS_PATH):
        payload = json.loads(results_path.read_text(encoding="utf-8"))
        self.results_path = results_path
        self.payload = payload
        n = 256
        self.probability_fraction = [Fraction(0) for _ in range(n)]
        self.q_fraction = [(Fraction(0), Fraction(0), Fraction(0)) for _ in range(n)]
        self.chart_fraction = [(Fraction(0), Fraction(0), Fraction(0)) for _ in range(n)]
        probability = np.zeros(n, dtype=np.float64)
        q = np.zeros((n, 3), dtype=np.float64)
        chart = np.zeros((n, 3), dtype=np.float64)
        for row in payload["per_history"]:
            h = int(row["history"])
            p = _frac(row["probability"])
            mx = _frac(row["marginal_x"])
            my = _frac(row["marginal_y"])
            c = _frac(row["covariance"])
            qx, qy, qz = mx, my, mx + my - 2 * (mx * my + c)
            stored = _frac(row["xor_joint"])
            if qz != stored:
                raise ValueError("results.json XOR forecast disagrees with the chart at %d" % h)
            self.probability_fraction[h] = p
            self.q_fraction[h] = (qx, qy, qz)
            self.chart_fraction[h] = (mx, my, c)
            probability[h] = float(p)
            q[h] = (float(qx), float(qy), float(qz))
            chart[h] = (float(mx), float(my), float(c))
        self.probability = probability
        self.q = q
        self.chart = chart
        self.is_test = np.array([is_test_history(h) for h in range(n)], dtype=bool)
        self.p_test = sum(self.probability_fraction[h] for h in range(n) if self.is_test[h])
        self.p_train = sum(self.probability_fraction[h] for h in range(n) if not self.is_test[h])
        self.e_cur = {
            "TEST": self._current_only_excess(True),
            "TRAIN": self._current_only_excess(False),
        }
        self.e_prod = {
            "TEST": self._four_c2(True),
            "TRAIN": self._four_c2(False),
        }
        self.afit_threshold = {
            split: {
                "total": self.e_cur[split]["total"] * Fraction(1, 4),
                "XOR": self.e_prod[split] * Fraction(1, 4),
            }
            for split in ("TEST", "TRAIN")
        }
        self.stage4_chart, self.stage4_belief = self._stage4()
        self.nearest_posterior, self.nearest_tv = self._nearest_posterior()
        self.train_prefixes = self._train_prefixes()
        self.reference_forecasts = {
            "K-EXACT": q.copy(),
            "K-PROD*": self._product_forecasts(),
            "K-CUR": self._current_observation_forecasts(),
        }
        self.published = self._published(payload)
        self._trial_cache = None

    def _published(self, payload):
        risks = payload["risks"]
        total = (
            _frac(risks["X"]["current_only_excess"])
            + _frac(risks["Y"]["current_only_excess"])
            + _frac(risks["XOR"]["current_only_excess"])
        )
        return {
            "oracle_brier": {name: _frac(risks[name]["oracle_brier"]) for name in QUERIES},
            "current_only_excess": {
                name: _frac(risks[name]["current_only_excess"]) for name in QUERIES
            },
            "current_only_excess_total": total,
            "four_c2": _frac(payload["covariance"]["four_second_moment"]),
            "alias_k1": payload["alias_summary"]["K1_outcome"],
            "min_marginal_separation": {
                "7": payload["descriptive_min_marginal_separation"]["7"],
                "8": payload["descriptive_min_marginal_separation"]["8"],
            },
        }

    def _split_rows(self, test: bool):
        for h in range(256):
            if bool(self.is_test[h]) == test:
                yield h

    def _current_only_excess(self, test: bool):
        """Optimal forecast that depends only on reading 8, inside one split."""
        rows = list(self._split_rows(test))
        mass = sum(self.probability_fraction[h] for h in rows)
        means = {}
        for bit in (0, 1):
            group = [h for h in rows if ((h >> 7) & 1) == bit]
            group_mass = sum(self.probability_fraction[h] for h in group)
            acc = [Fraction(0), Fraction(0), Fraction(0)]
            for h in group:
                weight = self.probability_fraction[h]
                for i in range(3):
                    acc[i] += weight * self.q_fraction[h][i]
            means[bit] = tuple(value / group_mass for value in acc)
        excess = [Fraction(0), Fraction(0), Fraction(0)]
        for h in rows:
            bit = (h >> 7) & 1
            weight = self.probability_fraction[h] / mass
            for i in range(3):
                gap = means[bit][i] - self.q_fraction[h][i]
                excess[i] += weight * gap * gap
        return {
            "X": excess[0],
            "Y": excess[1],
            "XOR": excess[2],
            "total": excess[0] + excess[1] + excess[2],
            "forecast_by_reading8": {str(bit): means[bit] for bit in (0, 1)},
        }

    def _four_c2(self, test: bool):
        rows = list(self._split_rows(test))
        mass = sum(self.probability_fraction[h] for h in rows)
        total = Fraction(0)
        for h in rows:
            c = self.chart_fraction[h][2]
            total += (self.probability_fraction[h] / mass) * (4 * c * c)
        return total

    def _stage4(self):
        matrix = fraction_transition()
        chart = np.zeros((16, 3), dtype=np.float64)
        beliefs = []
        for prefix in range(16):
            belief, _prob = filter_prefix(prefix, 4, matrix)
            mx, my, c = marginals_covariance(belief)
            beliefs.append(tuple(belief))
            chart[prefix] = (float(mx), float(my), float(c))
        return chart, beliefs

    def _nearest_posterior(self):
        donor = np.zeros(16, dtype=np.int64)
        distances = []
        for recipient in range(16):
            best = None
            best_tv = None
            for other in range(16):
                if other == recipient:
                    continue
                tv = _tv(self.stage4_belief[recipient], self.stage4_belief[other])
                if best_tv is None or tv < best_tv or (tv == best_tv and other < best):
                    best = other
                    best_tv = tv
            donor[recipient] = best
            distances.append(best_tv)
        return donor, distances

    def _train_prefixes(self):
        prefixes = {}
        for stage in range(1, 9):
            mask = (1 << stage) - 1
            found = sorted({h & mask for h in range(256) if not self.is_test[h]})
            prefixes[stage] = found
        return prefixes

    def _product_forecasts(self):
        out = np.zeros((256, 3), dtype=np.float64)
        for h in range(256):
            mx, my, _c = self.chart_fraction[h]
            qz = mx + my - 2 * mx * my
            out[h] = (float(mx), float(my), float(qz))
        return out

    def _current_observation_forecasts(self):
        """PR #4 current-observation arm, not the split-specific optimal."""
        out = np.zeros((256, 3), dtype=np.float64)
        for h in range(256):
            bit = (h >> 7) & 1
            mx, my, c = current_only_terminal(bit)
            qx, qy, qz = forecasts(mx, my, c)
            out[h] = (float(qx), float(qy), float(qz))
        return out

    def split_weights(self, test: bool) -> np.ndarray:
        mask = self.is_test if test else ~self.is_test
        mass = float(self.p_test if test else self.p_train)
        weights = np.zeros(256, dtype=np.float64)
        weights[mask] = self.probability[mask] / mass
        return weights

    def oracle_trials(self):
        """Cross-fitted T4^H trials with oracle wrong-donor candidates.

        A trial is (a, b, u) with a and b distinct, in the same parity fold,
        and b·u in TEST. Candidates c already satisfy the oracle separation
        tests. Norm matching is seed-dependent and is not applied here.
        """
        if self._trial_cache is not None:
            return self._trial_cache
        trials = []
        folds = {0: [p for p in range(16) if parity_fold(p) == 0],
                 1: [p for p in range(16) if parity_fold(p) == 1]}
        for fold, members in folds.items():
            for a in members:
                for b in members:
                    if a == b:
                        continue
                    for u in range(16):
                        hb = b | (u << 4)
                        if not self.is_test[hb]:
                            continue
                        ha = a | (u << 4)
                        d_xor = abs(self.q_fraction[hb][2] - self.q_fraction[ha][2])
                        cands = []
                        if d_xor >= Fraction(1, 100):
                            for c in members:
                                if c == a or c == b:
                                    continue
                                hc = c | (u << 4)
                                if _inf_forecast_gap(self, hc, hb) < Fraction(1, 10):
                                    continue
                                if _inf_forecast_gap(self, hc, ha) < Fraction(1, 10):
                                    continue
                                cands.append(c)
                        trials.append(
                            {
                                "a": a,
                                "b": b,
                                "u": u,
                                "ha": ha,
                                "hb": hb,
                                "fold": fold,
                                "xor_separated": d_xor >= Fraction(1, 100),
                                "candidates": cands,
                            }
                        )
        self._trial_cache = trials
        return trials

    def reference_export(self):
        """Held-out references recorded at freeze, before any training."""
        published = self.published

        def pack(value: Fraction):
            return {
                "exact": "%s/%s" % (value.numerator, value.denominator),
                "float64": float(value),
            }

        return {
            "source": "twostream_results_v1/results.json",
            "protocol_printed": {
                "oracle_brier_X": 0.212406,
                "oracle_brier_Y": 0.155028,
                "oracle_brier_XOR": 0.214954,
                "current_only_excess_total": 0.077612,
                "analytic_factorized_xor_excess": 0.0079539,
                "alias": "A0",
                "min_marginal_separation_stage7": 4.4e-4,
                "min_marginal_separation_stage8": 5.2e-4,
            },
            "oracle_brier": {name: pack(published["oracle_brier"][name]) for name in QUERIES},
            "current_only_excess": {
                name: pack(published["current_only_excess"][name]) for name in QUERIES
            },
            "current_only_excess_total": pack(published["current_only_excess_total"]),
            "analytic_4Ec2": pack(published["four_c2"]),
            "alias_k1": published["alias_k1"],
            "test_count": int(self.is_test.sum()),
            "train_count": int((~self.is_test).sum()),
            "P_TEST": pack(self.p_test),
            "P_TRAIN": pack(self.p_train),
            "E_CUR": {
                split: {key: pack(self.e_cur[split][key]) for key in ("X", "Y", "XOR", "total")}
                for split in ("TEST", "TRAIN")
            },
            "E_PROD_XOR": {split: pack(self.e_prod[split]) for split in ("TEST", "TRAIN")},
            "A_FIT_thresholds": {
                split: {key: pack(self.afit_threshold[split][key]) for key in ("total", "XOR")}
                for split in ("TEST", "TRAIN")
            },
        }


def _tv(left, right) -> Fraction:
    return sum(abs(a - b) for a, b in zip(left, right)) / 2


def _inf_forecast_gap(world: World, left: int, right: int) -> Fraction:
    return max(abs(world.q_fraction[left][i] - world.q_fraction[right][i]) for i in range(3))


def filter_disagreements(world: World | None = None):
    """Exact differences between results.json and the frozen filter. Empty means agreement."""
    world = world or load_world()
    matrix = fraction_transition()
    failures = []
    for h in range(256):
        belief, probability = filter_prefix(h, 8, matrix)
        mx, my, c = marginals_covariance(belief)
        if probability != world.probability_fraction[h]:
            failures.append("probability %d" % h)
        if (mx, my, c) != world.chart_fraction[h]:
            failures.append("chart %d" % h)
        qx, qy, qz = forecasts(mx, my, c)
        if (qx, qy, qz) != world.q_fraction[h]:
            failures.append("forecast %d" % h)
        if len(failures) >= 8:
            break
    return failures


def reading_variable_order():
    return [variable_at(t) for t in range(8)]


_WORLD = None


def load_world() -> World:
    global _WORLD
    if _WORLD is None:
        _WORLD = World()
    return _WORLD
