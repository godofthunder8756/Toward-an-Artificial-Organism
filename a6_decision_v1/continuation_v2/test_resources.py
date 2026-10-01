import pytest

from a6_decision_v1.continuation_v2.runner import normalize_counts, REMAINING
from a6_decision_v1.runner import JOBS


def test_unknown_is_not_zero_and_all_formulations_accounted():
    record = {"job": "f2_positive", "milp_NOT_CERTIFICATE": {
        "nodes_reported": None, "aggregate_nodes": 0}}
    normalized = normalize_counts(record)
    assert normalized["milp_NOT_CERTIFICATE"]["aggregate_nodes"] is None
    assert normalized["milp_NOT_CERTIFICATE"]["raw_internal_aggregate_counter"] == 0
    assert normalize_counts({"job": "f3_bank", "nodes_reported": None})["aggregate_nodes"] is None
    assert normalize_counts({"job": "f3_bank", "nodes_reported": 0})["aggregate_nodes"] == 0
    assert tuple(JOBS[:2]) + tuple(REMAINING) == JOBS


def test_exclusive_journal_lock_refuses_second_owner(tmp_path):
    lock = tmp_path / "supervisor.lock"
    with lock.open("x") as first:
        first.write("owner")
    with pytest.raises(FileExistsError):
        lock.open("x")


def test_gate_reduction_and_unrestricted_capacity():
    from a6_decision_v1.analytic_corollaries import verify
    result = verify()
    assert result["r9_full_gate_equivalent_to_joint_gate"]
    assert result["r10_joint_optimum_implies_all_strict_specialist_gates"]


@pytest.mark.parametrize("positive", (True, False))
def test_compact_offset_dual_and_smaller_formulation(positive):
    from fractions import Fraction as F
    from a6_decision_v1.continuation_v2.compact import relaxation
    from shared4_v1.coupled_lower import exact_dual, replay_dual
    model, offset, _, _ = relaxation(positive)
    bound, proof = exact_dual(model, offset)
    assert replay_dual(model, offset, proof) == bound == F(102, 625)
    assert len(model.cost) < 30000
