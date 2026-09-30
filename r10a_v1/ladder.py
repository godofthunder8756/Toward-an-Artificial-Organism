"""Construct minimal S3-only analytic extensions and publish their exact bounds."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json
import sys

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from encoder_witness import HISTORIES, construct
from verify_bounds import verify


def binary_pair(word: int, bit: int, book: list, nonlinear: bool) -> int:
    pair = tuple(book[word][2])
    intercept = {(0, 0): Fraction(-2), (1, 1): Fraction(1),
                 (0, 1): Fraction(-1, 2), (1, 0): Fraction(1, 2)}[pair]
    inverse = [j for j, p in enumerate(book) if tuple(p[2]) == (1, 0)]
    if len(inverse) != 1:
        raise ValueError("minimal witness requires exactly one inverse symbol")
    indicator = int(word == inverse[0])
    interaction = max(0, indicator + bit - 1) if nonlinear else indicator * bit
    delta = intercept + bit - 2 * interaction
    return int(delta > 0)


@torch.no_grad()
def run(bounds: Path, output: Path) -> None:
    document = json.loads(bounds.read_text())
    certified = verify(document)
    variant = document["variants"]["unrestricted"]
    book = [variant["policies"][j] for j in variant["selected"]]
    if any(binary_pair(w, bit, book, nonlinear) != book[w][2][bit]
           for nonlinear in (False, True) for w in range(8) for bit in (0, 1)):
        raise AssertionError("one-feature D1/D2 witness fails")
    arm, encoder_proof = construct(book)
    common = torch.tensor(HISTORIES)
    words = arm.write(arm.encode(common), 4)[0][:, 3].tolist()
    if words != encoder_proof["mapping"]:
        raise AssertionError("unrestricted-code analytic encoder fails")
    current, unrestricted = certified["positive"]["exact"], certified["unrestricted"]["exact"]
    result = {
        "schema": 1, "scope": "context3 only; constructive hypothetical decoders, no fitting",
        "decoder_ladder": {"D0": current, "D1": unrestricted, "D2": unrestricted, "D3": unrestricted},
        "minimal_D1": {
            "consumer": "S3", "new_features": 1,
            "feature": "indicator(word == inverse_word) * local_bit",
            "inverse_word": next(j for j, p in enumerate(book) if tuple(p[2]) == (1, 0)),
            "new_logit_difference_coefficient": -2,
        },
        "minimal_D2": {
            "consumer": "S3", "hidden_units": 1,
            "feature": "ReLU(indicator(word == inverse_word) + local_bit - 1)",
            "scope": "one optimal table; not universal arbitrary lookup",
        },
        "encoder_witness": encoder_proof, "optimal_codebook": book,
        "specialist_lesions": {
            "deployed_all": current,
            "unrestricted_S1_only": current,
            "unrestricted_S2_only": current,
            "unrestricted_S3_only": unrestricted,
            "unrestricted_S2_S3": unrestricted,
            "all_unrestricted": unrestricted,
        },
        "joint_penalty_removed_S3": str(Fraction(current) - Fraction(unrestricted)),
        "proof": "S1/S2 pointwise dominance plus jointly feasible retained maps; S3 global orientation bound; constructive encoders",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "bounds_sha256": hashlib.sha256(bounds.read_bytes()).hexdigest(),
    }
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps(result["decoder_ladder"], indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bounds", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.bounds, args.output)
