"""Independent exact population evaluator for one deployed shared R9 model."""

from fractions import Fraction
from itertools import product
from math import prod
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from phase3b.models import Arm


@torch.no_grad()
def evaluate(model):
    # Use the repository graph, not a constructor's custom forward implementation.
    legal = Arm("R9", 56).eval()
    legal.load_state_dict(model.state_dict(), strict=True)
    if any(not torch.isfinite(p).all() for p in legal.parameters()):
        raise ValueError("nonfinite analytic parameters")
    histories = tuple(product((0, 1), repeat=8))
    cases = tuple(product((0, 1), repeat=3))
    common = torch.tensor(histories).repeat_interleave(8, 0)
    local = torch.tensor(cases).repeat(256, 1).unsqueeze(1).expand(-1, 4, -1)
    trace = legal(common, local)
    if any(not torch.isfinite(x).all() for x in trace.logits):
        raise ValueError("nonfinite decoder logits")
    if trace.token_logp is not None and not torch.isfinite(trace.token_logp).all():
        raise ValueError("nonfinite encoder logits or probabilities")
    if trace.word is None:
        raise AssertionError("missing bounded wire")
    words = trace.word.reshape(256, 8, 4)
    if not torch.equal(words, words[:, :1].expand_as(words)):
        raise AssertionError("encoder depends on private readings")
    actions = [a.reshape(256, 8, 4) for a in trace.actions]
    for i, action in enumerate(actions):
        expected = torch.stack([action[:, 7 if case[i] else 0] for case in cases], 1)
        if not torch.equal(action, expected):
            raise AssertionError("consumer sees other private bits")
    numerators = [[0] * 3 for _ in range(4)]
    for h, history in enumerate(histories):
        counts = [history[j] + history[j + 4] for j in range(4)]
        for truth in product((0, 1), repeat=4):
            mass = prod(4 ** (n if z else 2 - n) for n, z in zip(counts, truth))
            for context in range(4):
                for consumer in range(3):
                    factor = (context + consumer) % 4
                    target = truth[factor] if consumer < 2 else (
                        truth[factor] ^ truth[(context + 3) % 4])
                    for bit in (0, 1):
                        action = int(actions[consumer][h, 7 if bit else 0, context])
                        units = 9 if consumer == 1 and action == 2 else 50 * (action != target)
                        numerators[context][consumer] += mass * (4 if bit == truth[factor] else 1) * units
    base = 16 * 25**4 * 5
    components = [Fraction(sum(row[i] for row in numerators), base * 50 * 4)
                  for i in range(3)]
    joint = sum(components) / 3
    threshold = Fraction(5101889, 29296875) + Fraction(1, 100)
    baselines = (Fraction(1, 5), Fraction(9, 50), Fraction(1, 2))
    return {
        "scope": "exact upper for one literal shared deployed R9; not global lower/optimum",
        "shared_joint_exact": str(joint), "shared_joint_loss": float(joint),
        "components_exact": [str(v) for v in components],
        "components": [float(v) for v in components],
        "context_joint_exact": [str(Fraction(sum(row), base * 150)) for row in numerators],
        "prospective_gate": {
            "joint_threshold_exact": str(threshold),
            "joint_pass": joint <= threshold,
            "specialist_pass": [a < b for a, b in zip(components, baselines)],
            "pass": joint <= threshold and all(a < b for a, b in zip(components, baselines)),
        },
        "histories": 256, "private_bit_triples": 8, "contexts": 4,
        "parameters": sum(p.numel() for p in legal.parameters()),
        "training": False,
    }


def main(source, output):
    spec = importlib.util.spec_from_file_location("shared_analytic_constructor", source)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load analytic constructor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    result = evaluate(module.build_model())
    result["constructor_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    result["verifier_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("constructor", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    torch.set_num_threads(1)
    main(args.constructor, args.output)
