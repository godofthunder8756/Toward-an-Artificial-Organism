from fractions import Fraction as F
from itertools import product
import json
import sys

import pytest

from a6_decision_v1.exact import GATE, gate
from a6_decision_v1.preservation import write_once
from a6_decision_v1.verify import verify_lemmas


def test_independent_population_and_conditional_lemmas():
    assert verify_lemmas()["verified"]


def test_strict_specialist_conjunction():
    assert not gate((F(1, 5), F(1, 10), F(1, 4)))
    assert not gate((F(1, 10), F(9, 50), F(1, 4)))
    assert not gate((F(1, 100), F(1, 100), F(1, 2)))
    assert gate((F(1, 10), F(1, 10), F(1, 4)))
    assert not gate((F(19, 100), F(17, 100), F(49, 100)))
    assert GATE == F(5101889, 29296875) + F(1, 100)


def test_no_overwrite(tmp_path):
    path = tmp_path / "certificate.json"
    write_once(path, {"first": True})
    with pytest.raises(FileExistsError):
        write_once(path, {"first": False})
    assert json.loads(path.read_text()) == {"first": True}


@pytest.mark.parametrize("positive", (True, False))
def test_mixture_relaxation_exact_dual_and_gate(positive):
    from a6_decision_v1.search import relaxation
    from shared4_v1.coupled_lower import exact_dual, replay_dual
    model, offset, metadata, _, _ = relaxation(positive, False)
    assert metadata["count_assignments_are_mixtures"]
    assert model.integer[864:864 + 81 * 4 * 8].sum() == 0
    bound, proof = exact_dual(model, offset)
    assert replay_dual(model, offset, proof) == bound
    assert F(96, 625) <= bound <= F(5159249, 29296875)
    assert len(metadata["gate_rows"]) == 4


def test_component_gate_cannot_collapse_history_mixtures():
    first = (F(3, 10), F(2, 100), F(1, 5))
    second = (F(1, 100), F(3, 10), F(1, 5))
    assert not gate(first) and not gate(second)
    assert gate(tuple((a + b) / 2 for a, b in zip(first, second)))


def test_head_cut_is_exact_and_rejects_tampering():
    from a6_decision_v1.decision import verify_cut
    policies = tuple(product(((0, 0), (0, 1), (1, 1)),
                             ((0, 2), (2, 1), (2, 2)),
                             ((0, 0), (0, 1), (1, 1))))
    selection = [0] * 32
    selection[0] = selection[9] = 18
    multipliers = ["0"] * 65
    for index in (0, 2, 16, 18):
        multipliers[index] = "1/4"
    proof = {"selection": selection, "consumer": 0, "positive": True,
             "multipliers": multipliers, "contradiction": "-1/2"}
    assert verify_cut(proof, policies)
    proof["multipliers"][0] = "1/3"
    with pytest.raises(ValueError, match="cancellation"):
        verify_cut(proof, policies)


def test_ordered_histories_are_retained():
    from a6_decision_v1.search import relaxation
    model, _, metadata, _, _ = relaxation(True, True)
    assert metadata["ordered_histories"]
    assert model.integer[-256 * 4 * 8:].sum() == 256 * 4 * 8


def test_legal_fixed_heads_have_positive_s1_slope():
    from a6_decision_v1.search import fixed_heads
    for kind in ("bank", "singleton"):
        arm = fixed_heads(kind)
        assert float(arm.heads[0].weight[1, 12] - arm.heads[0].weight[0, 12]) > 0
        assert not any(p.requires_grad for p in arm.parameters())


@pytest.mark.skipif(sys.platform != "win32", reason="Windows supervisor")
def test_memory_job_and_specific_worker_termination(tmp_path):
    import subprocess
    from a6_decision_v1.runner import MemoryJob
    marker = tmp_path / "unexpected_completion.txt"
    process = subprocess.Popen([
        sys.executable, "-c",
        f"import time; from pathlib import Path; time.sleep(300); Path({str(marker)!r}).write_text('done')",
    ])
    memory = MemoryJob(4 * 1024**3)
    try:
        memory.assign(process.pid)
        assert memory.peak() >= 0
    finally:
        memory.close()
    process.wait(timeout=10)
    assert not marker.exists()
