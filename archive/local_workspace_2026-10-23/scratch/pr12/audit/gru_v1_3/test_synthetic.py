"""Synthetic checks for the frozen audit. No roster checkpoint is loaded.

The real certificate may be read for weights, groups and executable constants.
No ridge fit against the certificate's q is performed here.
"""

from __future__ import annotations

import json
import unittest

import numpy as np

from audit.gru_v1_3.accounting import quota_status
from audit.gru_v1_3.domain import (
    LAMBDA_GRID,
    PRIMARY_LAMBDA,
    VAR_MAX,
    history_bits,
    load_world,
)
from audit.gru_v1_3.forward import numpy_forward, torch_batched_forward, torch_step_forward
from audit.gru_v1_3.replay_map import GRID_GB, selection_index
from audit.gru_v1_3.ridge import (
    combine_labels,
    comparison_label,
    dhat_identity_ok,
    ep_reconstruction_ok,
    fit_design,
    identity_holds,
    prepare,
    select_lambda,
    squared_error,
)
from audit.gru_v1_3.run_audit import declare_pairs


class SyntheticTests(unittest.TestCase):
    def test_lambda_grid_and_primary(self):
        self.assertEqual(PRIMARY_LAMBDA, float("1e-3"))
        self.assertEqual(len(LAMBDA_GRID), 8)
        self.assertEqual(LAMBDA_GRID[0], float("1e-6"))
        self.assertEqual(LAMBDA_GRID[-1], float("1e1"))
        self.assertIn(PRIMARY_LAMBDA, LAMBDA_GRID)

    def test_forward_agreement(self):
        rng = np.random.default_rng(1)
        bits = history_bits()
        weights = {
            "w_ih": rng.standard_normal((24, 9)).astype(np.float32).astype(np.float64),
            "w_hh": rng.standard_normal((24, 8)).astype(np.float32).astype(np.float64),
            "b_ih": rng.standard_normal(24).astype(np.float32).astype(np.float64),
            "b_hh": rng.standard_normal(24).astype(np.float32).astype(np.float64),
            "w1": rng.standard_normal((32, 8)).astype(np.float32).astype(np.float64),
            "b1": rng.standard_normal(32).astype(np.float32).astype(np.float64),
            "w2": rng.standard_normal((3, 32)).astype(np.float32).astype(np.float64),
            "b2": rng.standard_normal(3).astype(np.float32).astype(np.float64),
        }
        n_state, n_out = numpy_forward(weights, bits)
        s_state, s_out = torch_step_forward(weights, bits)
        b_state, b_out = torch_batched_forward(weights, bits)
        self.assertLessEqual(np.max(np.abs(n_state - s_state)), 1e-10)
        self.assertLessEqual(np.max(np.abs(n_out - s_out)), 1e-10)
        self.assertLessEqual(np.max(np.abs(n_state - b_state)), 1e-10)
        self.assertLessEqual(np.max(np.abs(n_out - b_out)), 1e-10)
        self.assertTrue(np.all((n_out > 0) & (n_out < 1)))

    def test_zero_variance_rule_and_ridge_normal_equation(self):
        rng = np.random.default_rng(2)
        n, p, k = 40, 5, 3
        x = rng.normal(size=(n, p))
        x[:, 1] = 3.0  # exact zero variance
        # a column with variance exactly at the cutoff is excluded
        x[:, 2] = rng.normal(size=n) * np.sqrt(VAR_MAX) * 0.1
        y = rng.normal(size=(n, k))
        w = rng.random(n)
        names = ["a", "const", "tiny", "d", "e"]
        model = prepare(x, y, w, names)
        self.assertIn("const", model.excluded)
        self.assertIn("tiny", model.excluded)
        lam = 1e-3
        beta = model.beta(lam)
        self.assertEqual(beta.shape[0], int(model.keep.sum()))
        pred = model.predict(x, lam)
        self.assertTrue(np.isfinite(pred).all())
        # unclipped predictions are allowed outside [0, 1]
        self.assertTrue(np.any(pred < 0) or np.any(pred > 1) or np.all(np.isfinite(pred)))
        weight = w / w.sum()
        z = (x[:, model.keep] - model.mu) / model.sd
        gram = z.T @ (weight[:, None] * z)
        b = weight @ y
        rhs = z.T @ (weight[:, None] * (y - b))
        solved = np.linalg.solve(gram + lam * np.eye(gram.shape[0]), rhs)
        self.assertLess(np.max(np.abs(solved - beta)), 1e-8)

    def test_lambda_tie_picks_largest(self):
        losses = {lam: 1.0 for lam in LAMBDA_GRID}
        self.assertEqual(select_lambda(losses), max(LAMBDA_GRID))
        losses = {lam: 1.0 + (0 if lam == LAMBDA_GRID[0] else 1.0) for lam in LAMBDA_GRID}
        self.assertEqual(select_lambda(losses), LAMBDA_GRID[0])

    def test_labels_and_quota(self):
        floor = 0.005823877685694766
        self.assertEqual(comparison_label(floor + 2e-10, floor), "meets-floor")
        self.assertEqual(comparison_label(floor - 2e-10, floor), "below-floor")
        self.assertEqual(comparison_label(floor, floor), "BOUNDARY")
        self.assertEqual(comparison_label(floor + 5e-11, floor), "BOUNDARY")
        self.assertEqual(combine_labels("meets-floor", "meets-floor"), "meets-floor")
        self.assertEqual(combine_labels("meets-floor", "below-floor"), "below-floor")
        self.assertEqual(combine_labels("meets-floor", "BOUNDARY"), "BOUNDARY")
        self.assertEqual(combine_labels("BOUNDARY", "BOUNDARY"), "BOUNDARY")
        self.assertEqual(quota_status(7, 1, 0, 2, 0), "quota attainment is UNRESOLVED")
        self.assertEqual(quota_status(8, 0, 0, 2, 0), "quota is attained")
        self.assertEqual(quota_status(5, 4, 1, 0, 0), "quota is not attained")
        self.assertEqual(quota_status(3, 3, 0, 4, 0), "UNRESOLVED (insufficient verified checkpoints)")

    def test_identities(self):
        rng = np.random.default_rng(3)
        f = rng.random((20, 3))
        q = rng.random((20, 3))
        qhat = rng.normal(size=(20, 3))
        ok, worst = dhat_identity_ok(f, q, qhat)
        self.assertTrue(ok)
        self.assertLessEqual(worst, 0)
        ok, _worst = ep_reconstruction_ok(f, q)
        self.assertTrue(ok)
        self.assertTrue(identity_holds(1.0, 1.0 + 5e-13))
        self.assertFalse(identity_holds(1.0, 1.0 + 1e-8))

    def test_depth5_partition_and_bin_rank(self):
        world = load_world()
        self.assertEqual(repr(world.R_oracle), "0.5823877685694766")
        self.assertEqual(repr(world.floor), "0.005823877685694766")
        self.assertEqual(world.bin_plus.shape[1], 36)
        expected = {
            "AB|CD": ("r1r3", 35, 28),
            "CD|AB": ("r1r3", 35, 28),
            "AC|BD": ("r0r2", 35, 28),
            "BD|AC": ("r0r2", 35, 28),
            "AD|BC": (None, 36, 33),
            "BC|AD": (None, 36, 33),
        }
        for fold in world.folds:
            design = fit_design(world.bin_plus, world.probability, fold["fit"], world.bin_plus_names)
            name, kept, rank = expected[fold["name"]]
            self.assertEqual(design.rank_info["features_after_exclusion"], kept)
            self.assertEqual(design.rank_info["rank"], rank)
            self.assertTrue(design.rank_info["rank_deficient"])
            if name is None:
                self.assertEqual(design.excluded, [])
            else:
                self.assertEqual(design.excluded, [name])

    def test_roster_arms_and_pairs_without_loading_checkpoints(self):
        roster = json.loads(open("/workspace/review/gru_own_error_audit_roster_v1.json", encoding="utf-8").read())
        self.assertEqual(roster["counts"], {"INIT": 60, "TRAINED": 230, "total": 290})
        trained = [row for row in roster["roster"] if row["role"] == "TRAINED"]
        self.assertEqual(len(declare_pairs(trained)), 2035)
        sel = sorted({row["arm"] for row in trained if row["pr"] == 7 and row["arm"].startswith("sel_")})
        self.assertEqual(len(sel), 9)
        for arm in sel:
            self.assertIsNotNone(selection_index(arm))
        self.assertEqual(len(GRID_GB), 9)

    def test_squared_error_shape(self):
        pred = np.zeros((4, 1))
        y = np.ones(4)
        err = squared_error(pred, y)
        self.assertEqual(err.shape, (4,))
        self.assertTrue(np.allclose(err, 1))


if __name__ == "__main__":
    unittest.main()
