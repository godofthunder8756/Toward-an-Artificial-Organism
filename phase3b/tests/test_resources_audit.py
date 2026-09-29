"""Focused H15 meters, R4 routing and raw-audit rejection tests; no fitting."""

from __future__ import annotations

import itertools
import unittest

import numpy as np
import torch

from phase3b.audit import (validate_r4_route, validate_raw_arrays,
                           validate_resource_snapshot, validate_engineering_selection,
                           validate_state_digest)
from phase3b.execution import require_authorization, r4_training_route
from phase3b.models import Arm, Recurrent, _token
from phase3b.resources import Meter, count, linear_meter, observed, profile_dry_run, python_peak
from phase3b.transfer import _state_bytes
from phase3b.world import generate, loss_units


class ResourceAuditTests(unittest.TestCase):
    def test_executed_model_operations_and_hook_cleanup(self):
        cell = Recurrent(1, 2)
        meter = Meter()
        with linear_meter(cell, meter):
            cell(torch.ones(1, 2, 1))
            token, _ = _token(torch.tensor([[1., 0., -1.]]), False)
        self.assertEqual(token.item(), 0)
        self.assertEqual((meter.forward_macs, meter.tanh_elements), (12, 4))
        self.assertEqual(meter.argmax_comparisons, 2)
        self.assertEqual((meter.log_softmax_exp_elements, meter.log_softmax_log_rows), (3, 1))
        self.assertGreater(meter.indexed_elements, 0)
        self.assertGreater(meter.modeled_tensor_bytes, 0)
        previous = observed(meter)
        cell(torch.ones(1, 2, 1))
        self.assertEqual(observed(meter), previous)

    def test_sampling_counts_draws_and_peak_discloses_blind_spots(self):
        meter = Meter()
        with linear_meter(torch.nn.Identity(), meter):
            _token(torch.zeros(4, 3), True)
        self.assertEqual(meter.categorical_draws, 4)
        self.assertEqual(meter.log_softmax_exp_elements, 12)
        with python_peak() as measured:
            values = list(range(100))
            self.assertEqual(len(values), 100)
        self.assertGreater(measured["python_tracemalloc_peak_bytes"], 0)
        self.assertIn("torch", measured["peak_memory_limitations"])

    def test_operator_profile_is_unscored_and_has_real_process_peak(self):
        model = Arm("candidate", 4)
        before = {k: v.detach().clone() for k, v in model.state_dict().items()}
        rng_before = torch.get_rng_state().clone()
        trained = profile_dry_run(model, batch=2)
        evaluated = profile_dry_run(model, batch=2, training=False)
        self.assertTrue(torch.equal(rng_before, torch.get_rng_state()))
        self.assertGreater(trained["observed_linear_backward_macs"], 0)
        self.assertEqual(evaluated["observed_linear_backward_macs"], 0)
        self.assertGreater(trained["torch_aten_operator_calls"], 0)
        self.assertGreater(trained["process_peak_working_set_bytes"], 0)
        self.assertGreater(trained["optimizer_state_bytes"], 0)
        self.assertEqual(evaluated["optimizer_state_bytes"], 0)
        self.assertIn("NOT physical bus traffic", trained["coverage"])
        self.assertTrue(all(torch.equal(before[k], v) for k, v in model.state_dict().items()))

    def test_synthetic_full_update_profile_covers_all_primary_families(self):
        for family in ("candidate", "R1", "R2", "R3", "R4", "R8", "R9"):
            with self.subTest(family=family):
                measured = profile_dry_run(Arm(family, 4), batch=1)
                self.assertGreater(measured["observed_linear_forward_macs"], 0)
                self.assertGreater(measured["observed_linear_backward_macs"], 0)
                self.assertGreater(measured["torch_aten_operator_calls"], 0)
                self.assertGreater(measured["optimizer_state_bytes"], 0)
                self.assertEqual(measured["contexts"], 3)

    def test_whole_arm_resource_replay_rejects_fake_zero_and_missing_fields(self):
        for family in ("candidate", "R1", "R2", "R3", "R4", "R8", "R9"):
            model = Arm(family, 4)
            snapshot = count(model)
            self.assertGreater(snapshot["forward_macs_per_episode"], 0)
            self.assertGreater(snapshot["nonlinear_tanh_elements"], 0)
            self.assertGreater(snapshot["annotated_logical_tensor_bytes_estimate"], 0)
            self.assertEqual(snapshot["parameter_bytes"], sum(p.numel() * p.element_size()
                                                              for p in model.parameters()))
            validate_resource_snapshot(snapshot, model)
            changed = dict(snapshot, nonlinear_tanh_elements=0)
            with self.assertRaisesRegex(ValueError, "nonlinear_tanh_elements"):
                validate_resource_snapshot(changed, model)
            self.assertEqual(snapshot, count(model))
            with self.assertRaisesRegex(ValueError, "resource log"):
                validate_resource_snapshot(None, model)
        with self.assertRaisesRegex(RuntimeError, "STOP"):
            require_authorization(None)

    def test_r4_factorized_search_is_full_training_route_argmin(self):
        table = torch.tensor([[8, 2, 5, 9], [5, 6, 0, 8], [1, 4, 3, 5]])
        route = r4_training_route(table)
        exhaustive = min(itertools.product(range(4), repeat=3),
                         key=lambda choices: (sum(table[c, choices[c]].item() for c in range(3)), choices))
        self.assertEqual(route, (*exhaustive, (exhaustive[2] + 1) % 4))
        search = {"routes_enumerated": 256, "search_exposure_per_address": 8192,
                  "training_exposure_per_address": 2048, "search_forward_macs": 1,
                  "search_wall_seconds": 0.1, "training_loss_table_units": table.tolist()}
        self.assertEqual(validate_r4_route({"route": list(route), "route_search": search}), route)
        for invalid in ([0, 2, -1, 0], [0, 2, 4, 1], [0, 2, 0, 0], [True, 2, 0, 1]):
            with self.assertRaisesRegex(ValueError, "route"):
                validate_r4_route({"route": invalid, "route_search": search})
        with self.assertRaisesRegex(ValueError, "route"):
            validate_r4_route({"route": list(route), "route_search": dict(search, routes_enumerated=64)})
        with self.assertRaisesRegex(ValueError, "training table"):
            validate_r4_route({"route": [0, 0, 0, 1], "route_search": search})
        model = Arm("R4", 4)
        model.route = route
        output = model(torch.zeros(2, 8, dtype=torch.long), torch.zeros(2, 4, 3, dtype=torch.long))
        self.assertEqual(output.address.tolist(), [list(route), list(route)])

    def test_raw_validator_recomputes_losses_and_rejects_bad_wire_data(self):
        ep = generate(83, 3)
        actions = np.zeros((3, 4, 3), dtype=np.uint8)
        components = loss_units(tuple(torch.from_numpy(actions[:, :, i].astype(np.int64))
                                      for i in range(3)), ep.truth).numpy().astype(np.uint8)
        raw = {"components": components, "actions": actions, "words": np.zeros((3, 4), dtype=np.uint8)}
        self.assertEqual(validate_raw_arrays("R4", ep, raw).shape, (3,))
        for key, replacement in (("components", np.zeros_like(components)),
                                 ("actions", np.full_like(actions, 255)),
                                 ("words", np.full((3, 4), 8, dtype=np.uint8))):
            broken = dict(raw, **{key: replacement})
            with self.assertRaisesRegex(ValueError, "STOP"):
                validate_raw_arrays("R4", ep, broken)
        with self.assertRaisesRegex(ValueError, "word alphabet"):
            validate_raw_arrays("R2", ep, raw)
        with self.assertRaisesRegex(ValueError, "missing arrays"):
            validate_raw_arrays("R4", ep, {"actions": actions})

    def test_selection_checks_every_config_seed_and_tie_break(self):
        configs = []
        grid = [[4, 0.0003], [4, 0.001]]
        for width, rate in grid:
            configs.append({"width": width, "learning_rate": rate,
                            "seeds": list(range(4)), "seed_scores": [1, 2, 3, 4],
                            "training_context_loss_units": 10,
                            "parameters": count(Arm("R1", 4))["trainable_parameters"],
                            "spends": [{"episodes": 8192, "updates": 256} for _ in range(4)],
                            "checkpoint_sha256": ["a" * 64] * 4})
        row = {"schema": 1, "family": "R1", "freeze_sha256": "f",
               "engineering_approval_sha256": "e", "configurations": configs,
               "selected": {"width": 4, "learning_rate": 0.0003}}
        validate_engineering_selection(row, "R1", grid, "f", "e")
        for broken in (dict(row, selected={"width": 4, "learning_rate": 0.001}),
                       dict(row, configurations=[dict(configs[0], seeds=[0, 1, 2, 1000]), configs[1]]),
                       dict(row, configurations=[dict(configs[0], seed_scores=[1, 2, 3, 5]), configs[1]])):
            with self.assertRaisesRegex(ValueError, "STOP"):
                validate_engineering_selection(broken, "R1", grid, "f", "e")

    def test_tensor_state_digest_is_transfer_compatible_not_file_hash(self):
        model = Arm("candidate", 4)
        digest = _state_bytes(model)
        validate_state_digest({"state_digest": digest}, model)
        with self.assertRaisesRegex(ValueError, "state digest"):
            validate_state_digest({"state_digest": "0" * 64}, model)
        with torch.no_grad():
            next(model.parameters()).add_(1)
        with self.assertRaisesRegex(ValueError, "state digest"):
            validate_state_digest({"state_digest": digest}, model)


if __name__ == "__main__":
    unittest.main()