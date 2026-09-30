import json
from pathlib import Path

from ladder import binary_pair


def test_minimal_one_feature_upgrade():
    document = json.loads((Path(__file__).parent / "decoder_bounds.json").read_text())
    v = document["variants"]["unrestricted"]
    book = [v["policies"][j] for j in v["selected"]]
    for nonlinear in (False, True):
        for word in range(8):
            for bit in (0, 1):
                assert binary_pair(word, bit, book, nonlinear) == book[word][2][bit]
