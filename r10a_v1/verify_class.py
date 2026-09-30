"""Independent risk replay for the deployed constructive class certificate."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import prod
from pathlib import Path
import argparse
import hashlib
import json
import sys

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from encoder_witness import HISTORIES, construct
from verify_bounds import verify


@torch.no_grad()
def check(path: Path) -> dict:
    certificate = json.loads(path.read_text())
    bounds = json.loads((path.parent / "decoder_bounds.json").read_text())
    for name, digest in certificate["provenance"].items():
        if hashlib.sha256((path.parent / name).read_bytes()).hexdigest() != digest:
            raise AssertionError(f"constructive source changed: {name}")
    lower = verify(bounds)
    if lower["positive"]["exact"] != lower["negative"]["exact"]:
        raise AssertionError("S3 orientation envelope is not accounted for")
    arm, metadata = construct(certificate["codebook"])
    if metadata != certificate["encoder_witness"]:
        raise AssertionError("encoder witness changed")
    for head, witness in zip(arm.heads, certificate["decoder_witnesses"]):
        head.bias.zero_()
        for action in range(head.out_features):
            head.weight[action, :8] = torch.tensor(
                [float(Fraction(v)) for v in witness["message"][action]])
            head.weight[action, 8:12] = torch.tensor(
                [float(Fraction(v)) for v in witness["context"][action]])
            head.weight[action, 12] = float(Fraction(witness["slope"][action]))
    common = torch.tensor(HISTORIES).repeat_interleave(8, 0)
    bits = tuple(product((0, 1), repeat=3))
    local = torch.tensor(bits).repeat(256, 1).unsqueeze(1).expand(-1, 4, -1)
    trace = arm.eval()(common, local)
    words = trace.word.reshape(256, 8, 4)[:, :, 3]
    if words[:, 0].tolist() != metadata["mapping"] or not torch.equal(words, words[:, :1].expand_as(words)):
        raise AssertionError("encoder replay or local-bit isolation failed")
    actions = [a.reshape(256, 8, 4)[:, :, 3] for a in trace.actions]
    numerator = 0
    for h, history in enumerate(HISTORIES):
        n = [history[j] + history[j + 4] for j in range(4)]
        for case, readings in enumerate(bits):
            for i in range(3):
                if int(actions[i][h, case]) != certificate["codebook"][int(words[h, 0])][i][readings[i]]:
                    raise AssertionError("decoder witness replay failed")
        for truth in product((0, 1), repeat=4):
            mass = prod(4 ** (count if z else 2 - count) for count, z in zip(n, truth))
            for i, factor in enumerate((3, 0, 1)):
                target = truth[factor] if i < 2 else truth[1] ^ truth[2]
                for bit in (0, 1):
                    action = int(actions[i][h, 7 if bit else 0])
                    units = 9 if i == 1 and action == 2 else 50 * (action != target)
                    numerator += mass * (4 if bit == truth[factor] else 1) * units
    upper = Fraction(numerator, 16 * 25**4 * 5 * 150)
    if (str(upper) != lower["positive"]["exact"] or str(upper) != certificate["class_exact"]
            or numerator != certificate["lower_upper_equal_numerator"]):
        raise AssertionError("constructive upper bound and global class lower bound differ")
    return {"certified": True, "class_exact": str(upper), "upper_numerator": numerator,
            "context": 3, "histories": 256, "private_bit_triples": 8,
            "scope": "fixed-width deployed functional class; not four-context joint optimum"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    torch.set_num_threads(1)
    print(json.dumps(check(args.certificate), indent=2))
