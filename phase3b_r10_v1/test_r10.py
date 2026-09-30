"""Exact risk cross-checks, certificate tamper rejection and legal wire tests."""

from copy import deepcopy
import json
from pathlib import Path

import numpy as np
import pytest
import torch

from r10 import costs
from verify import POLICIES, full_costs, verify
from evaluate import fixed_actions
from phase3b.world import generate


HERE = Path(__file__).resolve().parent


@pytest.fixture(scope="module")
def document():
    return json.loads((HERE / "certificate.json").read_text(encoding="utf-8"))


def test_independent_exact_risks():
    proposed, policies = costs()
    independent = full_costs()
    assert np.array_equal(proposed, np.array(independent)[:, [POLICIES.index(p) for p in policies]])


def test_exact_certificate(document):
    result = verify(document)
    assert result["certified"]
    assert result["r10_exact"] == "5101889/29296875"
    assert result["full_information_exact"] == "96/625"
    assert result["nodes"] == 11


@pytest.mark.parametrize("change", ["objective", "encoder", "dual", "tree", "coverage"])
def test_reject_tampered_certificate(document, change):
    altered = deepcopy(document)
    if change == "objective":
        altered["numerator"] -= 5
    elif change == "encoder":
        altered["encoder"][0] = (altered["encoder"][0] + 1) % 8
    elif change == "dual":
        leaf = next(n for n in altered["certificate"]["nodes"] if n["kind"] == "dual")
        leaf["alpha"] = [0] * 81
        leaf["lower_micro_units"] = 0
    elif change == "tree":
        altered["certificate"]["nodes"][0]["zero"] = altered["certificate"]["nodes"][0]["one"]
    else:
        altered["policies"] = altered["policies"][:-1]
    with pytest.raises((ValueError, AssertionError)):
        verify(altered)


def test_local_isolation_and_context_rotation(document):
    episode = generate(47, 256)
    actions, words = fixed_actions(document, episode.common, episode.local)
    assert words.min() >= 0 and words.max() < 8
    for consumer in range(3):
        changed = episode.local.clone()
        changed[:, :, consumer] = 1 - changed[:, :, consumer]
        other_actions, other_words = fixed_actions(document, episode.common, changed)
        assert torch.equal(words, other_words)
        for other in range(3):
            if other != consumer:
                assert torch.equal(actions[other], other_actions[other])
    for context in range(4):
        common = torch.cat((episode.common[:, context:4], episode.common[:, :context],
                            episode.common[:, context + 4:], episode.common[:, 4:context + 4]), 1)
        local = episode.local[:, context:context + 1].expand(-1, 4, -1)
        rotated_actions, rotated_words = fixed_actions(document, common, local)
        assert torch.equal(words[:, context], rotated_words[:, 0])
        assert all(torch.equal(actions[i][:, context], rotated_actions[i][:, 0]) for i in range(3))
