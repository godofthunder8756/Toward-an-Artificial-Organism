"""Combine an exact lower bound with a constructive deployed-Arm upper bound."""

from __future__ import annotations

from fractions import Fraction
import hashlib
from itertools import product
from math import comb, prod
from pathlib import Path
import argparse
import json
import sys

import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "phase3b_r10_v1"))
from verify import COUNTS, DENOMINATOR, POLICIES, full_costs
from decoder_capacity import shared_context_witness
from encoder_witness import HISTORIES, construct
from verify_bounds import verify


def install_heads(arm, codebook) -> list[dict]:
    witnesses = []
    with torch.no_grad():
        for consumer, actions in enumerate((2, 3, 2)):
            table = [[word[consumer] for word in codebook] for _ in range(4)]
            witness = shared_context_witness(table, actions)
            if witness is None:
                raise AssertionError("selected codebook cannot be implemented by shared affine heads")
            head = arm.heads[consumer]
            head.weight.zero_()
            head.bias.zero_()
            for action in range(actions):
                head.weight[action, :8] = torch.tensor(
                    [float(v) for v in witness["message"][action]])
                head.weight[action, 8:12] = torch.tensor(
                    [float(v) for v in witness["context"][action]])
                head.weight[action, 12] = float(witness["slope"][action])
            witnesses.append(witness)
    return witnesses


@torch.no_grad()
def certify(bounds_path: Path, output: Path) -> None:
    torch.set_num_threads(1)
    document = json.loads(bounds_path.read_text(encoding="utf-8"))
    lower = verify(document)
    variant = document["variants"]["positive"]
    book = [variant["policies"][j] for j in variant["selected"]]
    arm, encoder_proof = construct(book)
    decoder_proofs = install_heads(arm, book)
    common = torch.tensor(HISTORIES, dtype=torch.long).repeat_interleave(8, 0)
    cases = tuple(product(range(2), repeat=3))
    local = torch.tensor(cases, dtype=torch.long).repeat(256, 1).unsqueeze(1).expand(-1, 4, -1)
    trace = arm.eval()(common, local)
    words = trace.word.reshape(256, 8, 4)[:, :, 3]
    if not torch.equal(words, words[:, :1].expand_as(words)):
        raise AssertionError("encoder sees local readings")
    if words[:, 0].tolist() != encoder_proof["mapping"]:
        raise AssertionError("analytic encoder and runtime mapping differ")
    actions = [a.reshape(256, 8, 4)[:, :, 3] for a in trace.actions]
    for h in range(256):
        word = int(words[h, 0])
        for case, bits in enumerate(cases):
            for consumer in range(3):
                if int(actions[consumer][h, case]) != book[word][consumer][bits[consumer]]:
                    raise AssertionError("actual affine decoder does not implement the selected policy")
    full = full_costs()
    numerator = 0
    for h, history in enumerate(HISTORIES):
        counts = [history[j] + history[j + 4] for j in range(4)]
        canonical = tuple(counts[(3 + j) % 4] for j in range(4))
        row = full[COUNTS.index(canonical)]
        costs = [row[POLICIES.index(tuple(tuple(p) for p in word))] for word in book]
        selected = int(words[h, 0])
        if costs[selected] != min(costs):
            raise AssertionError("runtime assignment has excess exact risk")
        multiplicity = prod(comb(2, n) for n in canonical)
        if costs[selected] % multiplicity:
            raise AssertionError("history mass is not on the integer lattice")
        numerator += costs[selected] // multiplicity
    if numerator != variant["numerator"]:
        raise AssertionError("deployed upper bound does not meet exact lower bound")
    loss = Fraction(numerator, DENOMINATOR)
    bayes, r10, learned = Fraction(96, 625), Fraction(5101889, 29296875), Fraction(2003, 6000)
    gaps = {"capacity": r10 - bayes, "expressivity": loss - r10, "learning": learned - loss}
    result = {
        "schema": 1, "scope": "exact context3 population optimum, nonclone deployed width56 R9",
        "certified": True, "training": False, "lower": lower,
        "lower_upper_equal_numerator": numerator, "denominator": DENOMINATOR,
        "class_exact": str(loss), "class_loss": float(loss),
        "codebook": book, "encoder_witness": encoder_proof,
        "decoder_witnesses": [
            {key: ([[str(v) for v in row] for row in values] if key != "slope"
                   else [str(v) for v in values]) for key, values in proof.items()}
            for proof in decoder_proofs],
        "rational_analytic_parameters": {
            "trunk_gain": encoder_proof["gain"],
            "rule": "encoder_witness.construct; no fitted parameters",
            "exact_real_and_float32_exhaustive_checks": True,
        },
        "losses": {"bayes": str(bayes), "r10": str(r10), "class": str(loss), "learned": str(learned)},
        "gaps": {key: {"exact": str(v), "decimal": float(v),
                       "percent_of_total_excess": float(100 * v / (learned - bayes))}
                 for key, v in gaps.items()},
        "provenance": {name: hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest()
                       for name in ("solve.py", "verify_bounds.py", "encoder_witness.py",
                                    "decoder_capacity.py", "certify_class.py", "decoder_bounds.json")},
    }
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"certified": True, "class_exact": str(loss), "gaps": result["gaps"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bounds", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    certify(args.bounds, args.output)
