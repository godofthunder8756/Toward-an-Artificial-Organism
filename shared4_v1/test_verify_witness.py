from fractions import Fraction

import pytest
import torch

from verify_witness import evaluate
from phase3b.models import Arm


def zero_arm():
    arm = Arm("R9", 56)
    with torch.no_grad():
        for parameter in arm.parameters():
            parameter.zero_()
    return arm


def test_constant_decisions_exact_population():
    result = evaluate(zero_arm())
    assert result["shared_joint_exact"] == "1/2"
    assert result["components_exact"] == ["1/2"] * 3
    assert not result["prospective_gate"]["pass"]


def test_local_and_abstention_baselines():
    arm = zero_arm()
    with torch.no_grad():
        for i in (0, 2):
            arm.heads[i].bias[1] = -1
            arm.heads[i].weight[1, 12] = 2
        arm.heads[1].bias[2] = 1
    result = evaluate(arm)
    assert result["components_exact"] == ["1/5", "9/50", "1/2"]
    assert Fraction(result["shared_joint_exact"]) == Fraction(22, 75)
    assert result["prospective_gate"]["specialist_pass"] == [False] * 3


def test_message_can_change_with_context():
    arm = zero_arm()
    with torch.no_grad():
        for c in range(4):
            arm.code.weight[c, 56 + c] = 1
    common = torch.zeros(1, 8, dtype=torch.long)
    local = torch.zeros(1, 4, 3, dtype=torch.long)
    assert arm(common, local).word.tolist() == [[0, 1, 2, 3]]
    assert evaluate(arm)["shared_joint_exact"] == "1/2"


def test_published_witness_cannot_be_overwritten():
    from shared_witness import generate

    with pytest.raises(FileExistsError, match="immutable"):
        generate()
