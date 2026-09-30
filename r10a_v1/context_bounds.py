"""Exact all-context achievable upper bound, not a claimed all-context optimum."""

from fractions import Fraction
from itertools import product
from math import prod
from pathlib import Path
import argparse
import json
import sys

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from encoder_witness import HISTORIES, construct
from certify_class import install_heads


@torch.no_grad()
def run(certificate: Path, output: Path) -> None:
    document = json.loads(certificate.read_text())
    arm, _ = construct(document["codebook"])
    install_heads(arm, document["codebook"])
    histories = torch.tensor(HISTORIES)
    local = torch.zeros(256, 4, 3, dtype=torch.long)
    zero, one = arm(histories, local), arm(histories, 1 - local)
    totals = [0] * 4
    for h, history in enumerate(HISTORIES):
        n = [history[j] + history[j + 4] for j in range(4)]
        for truth in product((0, 1), repeat=4):
            mass = prod(4 ** (count if z else 2 - count) for count, z in zip(n, truth))
            for c in range(4):
                for i in range(3):
                    factor = (c + i) % 4
                    target = truth[factor] if i < 2 else truth[factor] ^ truth[(c + 3) % 4]
                    for bit, trace in enumerate((zero, one)):
                        action = int(trace.actions[i][h, c])
                        units = 9 if i == 1 and action == 2 else 50 * (action != target)
                        totals[c] += mass * (4 if bit == truth[factor] else 1) * units
    denominator = 16 * 25**4 * 5 * 150
    losses = [Fraction(v, denominator) for v in totals]
    result = {
        "scope": "deployed four-context average bracket, NOT exact joint optimum",
        "context_losses_exact": [str(v) for v in losses],
        "oracle_all_context_R10_exact": "5101889/29296875",
        "deployed_all_context_lower_exact": document["class_exact"],
        "deployed_all_context_upper_exact": str(sum(losses) / 4),
        "upper_witness": "same published context3-optimized Arm, all parameters shared",
        "optimality_gap_resolved": False,
        "train_context_extension_ambiguity": {
            "exact_possible_heldout_risks": ["59/150", "1/2"],
            "gap": "8/75",
            "reason": "for ANY optimal train-context weights, free heldout offsets can force all heads constant without changing contexts0..2",
            "not_claimed": "these are not the extrema of all possible heldout extensions",
        },
    }
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    torch.set_num_threads(1)
    run(args.certificate, args.output)
