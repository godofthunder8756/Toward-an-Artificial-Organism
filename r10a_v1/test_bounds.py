from copy import deepcopy
from pathlib import Path
import json

import pytest

from verify_bounds import verify


def test_exact_bounds():
    document = json.loads((Path(__file__).parent / "decoder_bounds.json").read_text())
    results = verify(document)
    assert results["positive"]["exact"] == results["negative"]["exact"] == "5159249/29296875"
    assert results["unrestricted"]["exact"] == "5101889/29296875"


@pytest.mark.parametrize("change", ["upper", "leaf", "branch"])
def test_bound_tampering(change):
    document = deepcopy(json.loads((Path(__file__).parent / "decoder_bounds.json").read_text()))
    variant = document["variants"]["positive"]
    if change == "upper":
        variant["numerator"] -= 5
    elif change == "leaf":
        leaf = next(n for n in variant["certificate"]["nodes"] if n["kind"] == "dual")
        leaf["alpha"] = [0] * 81
        leaf["lower_micro_units"] = 0
    else:
        variant["certificate"]["nodes"].append({"kind": "exhausted", "value": 0})
    with pytest.raises((ValueError, AssertionError)):
        verify(document)
