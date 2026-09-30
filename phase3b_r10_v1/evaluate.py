"""Read-only frozen R9 replay and fixed R10 scoring; no optimization or fitting."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
from math import comb, prod
from pathlib import Path
import json
import sys

import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from phase3b.execution import source_hashes
from phase3b.freeze import dependency_hashes, repository_head
from phase3b.models import Arm
from phase3b.world import generate, loss_units
from verify import COUNTS, DENOMINATOR, POLICIES, full_costs, verify


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixed_actions(document: dict, common: torch.Tensor,
                  local: torch.Tensor) -> tuple[tuple[torch.Tensor, ...], torch.Tensor]:
    counts = (common[:, :4] + common[:, 4:]).numpy()
    decoder = np.array(document["policies"], dtype=np.int64)[document["selected"]]
    encoder = np.array(document["encoder"], dtype=np.int64)
    words = np.zeros((len(common), 4), dtype=np.int64)
    actions = np.zeros((len(common), 4, 3), dtype=np.int64)
    for context in range(4):
        rotated = np.roll(counts, -context, axis=1)
        rows = rotated @ np.array([27, 9, 3, 1])
        words[:, context] = encoder[rows]
        for consumer in range(3):
            actions[:, context, consumer] = decoder[
                words[:, context], consumer, local[:, context, consumer].numpy()
            ]
    return tuple(torch.from_numpy(actions[:, :, i]) for i in range(3)), torch.from_numpy(words)


@torch.no_grad()
def population_r9(model: Arm, table: list[list[int]]) -> Fraction:
    histories = torch.tensor(list(product((0, 1), repeat=8)), dtype=torch.long)
    cases = torch.tensor(list(product((0, 1), repeat=3)), dtype=torch.long)
    common = histories.repeat_interleave(8, dim=0)
    local = cases.repeat(256, 1).unsqueeze(1).expand(-1, 4, -1).clone()
    trace = model(common, local)
    if trace.word is None:
        raise AssertionError("R9 missing eight-symbol wire")
    words = trace.word.reshape(256, 8, 4)
    if not torch.equal(words, words[:, :1].expand_as(words)):
        raise AssertionError("encoder sees private local readings")
    acts = [a.reshape(256, 8, 4) for a in trace.actions]
    for i, action in enumerate(acts):
        expected = torch.stack([action[:, 7 if case[i] else 0] for case in cases], 1)
        if not torch.equal(action, expected):
            raise AssertionError("decoder sees another specialist's local reading")
    total = 0
    for h, history in enumerate(histories):
        counts = (history[:4] + history[4:]).tolist()
        canonical = tuple(counts[(3 + j) % 4] for j in range(4))
        policy = tuple((int(action[h, 0, 3]), int(action[h, 7, 3])) for action in acts)
        cost = table[COUNTS.index(canonical)][POLICIES.index(policy)]
        multiplicity = prod(comb(2, n) for n in canonical)
        if cost % multiplicity:
            raise AssertionError("history aggregation failed")
        total += cost // multiplicity
    return Fraction(total, DENOMINATOR)


@torch.no_grad()
def evaluate(certificate: Path, output: Path) -> None:
    torch.set_num_threads(1)
    document = json.loads(certificate.read_text(encoding="utf-8"))
    certified = verify(document)
    if document["script_sha256"] != sha(certificate.parent / "r10.py"):
        raise AssertionError("certificate proposer source changed")
    finals = ROOT / "phase3b_results_v1" / "finals"
    freeze = json.loads((finals / "execution_freeze.json").read_text(encoding="utf-8"))
    manifest = json.loads((finals / "manifest.json").read_text(encoding="utf-8"))
    frozen_sources = source_hashes()
    if frozen_sources != freeze["source_sha256"] or dependency_hashes() != freeze["dependencies"]:
        raise AssertionError("frozen source or execution dependencies changed")
    if sha(finals / "manifest.json") != "5ba90ee9e6f2d734b0ab2eadf9906edea30b52c66e24cf093dd802cd0b4091a9":
        raise AssertionError("primary manifest changed")
    protected = {str(p.relative_to(ROOT)): sha(p) for p in finals.iterdir()}
    protected["PHASE3B_VERDICT_v1.md"] = sha(ROOT / "PHASE3B_VERDICT_v1.md")
    output.mkdir(exist_ok=False)
    table = full_costs()
    per_seed = {}
    population = []
    for seed in range(1000, 1016):
        info = manifest["seeds"][str(seed)]["R9"]
        raw_path, checkpoint = finals / f"{seed}_R9.npz", finals / f"{seed}_R9.pt"
        if sha(raw_path) != info["sha256"] or sha(checkpoint) != info["checkpoint_file_sha256"]:
            raise AssertionError("R9 frozen raw or checkpoint hash mismatch")
        model = Arm("R9", info["configuration"]["width"]).eval()
        model.load_state_dict(torch.load(checkpoint, map_location="cpu", weights_only=True))
        episode = generate(20_000 + seed, 4096)
        replay = model(episode.common, episode.local)
        with np.load(raw_path, allow_pickle=False) as raw:
            if (not np.array_equal(torch.stack(replay.actions, -1).numpy(), raw["actions"])
                    or not np.array_equal(replay.word.numpy(), raw["words"])
                    or not np.array_equal(loss_units(replay.actions, episode.truth).numpy(),
                                          raw["components"])):
                raise AssertionError("frozen R9 episode replay diverged")
            r9_units = int(raw["components"][:, 3].sum())
        actions, words = fixed_actions(document, episode.common, episode.local)
        components = loss_units(actions, episode.truth)
        raw_output = output / f"{seed}_R10.npz"
        with raw_output.open("xb") as stream:
            np.savez_compressed(stream, actions=torch.stack(actions, -1).numpy().astype(np.uint8),
                                components=components.numpy().astype(np.uint8),
                                words=words.numpy().astype(np.uint8))
        r10_units = int(components[:, 3].sum())
        r9_population = population_r9(model, table)
        population.append(r9_population)
        per_seed[str(seed)] = {
            "r9_units_context3": r9_units, "r10_units_context3": r10_units,
            "paired_gap": str(Fraction(r9_units - r10_units, 4096 * 150)),
            "r9_population_exact": str(r9_population),
            "r9_population_loss": float(r9_population),
            "r10_component_mean_context3": [
                float(components[:, 3, i].sum()) / (4096 * 50) for i in range(3)],
            "r10_raw_sha256": sha(raw_output),
        }
    for name, digest in protected.items():
        if sha(ROOT / name) != digest:
            raise AssertionError(f"protected artifact changed: {name}")
    if source_hashes() != frozen_sources:
        raise AssertionError("frozen source changed during scoring")
    mean_r9 = sum(population) / 16
    r10 = Fraction(document["numerator"], DENOMINATOR)
    floor = Fraction(certified["full_information_exact"])
    sample_r9 = Fraction(sum(v["r9_units_context3"] for v in per_seed.values()), 16 * 4096 * 150)
    sample_r10 = Fraction(sum(v["r10_units_context3"] for v in per_seed.values()), 16 * 4096 * 150)
    summary = {
        "schema": 1, "scope": "EXTERNAL post-final R10; verdict B unchanged; no neural training",
        "certificate_sha256": sha(certificate), "verification": certified,
        "provenance": {
            "supplement_head": repository_head(), "frozen_execution_head": freeze["head"],
            "head_match": repository_head() == freeze["head"],
            "frozen_sources_match": True, "dependencies_match": True,
            "protected_sha256": protected,
            "scripts": {name: sha(certificate.parent / name)
                        for name in ("r10.py", "verify.py", "evaluate.py")},
        },
        "per_seed": per_seed,
        "comparison": {
            "r9_population_mean_exact": str(mean_r9), "r9_population_mean": float(mean_r9),
            "r9_minus_r10_population_exact": str(mean_r9 - r10),
            "r9_minus_r10_population": float(mean_r9 - r10),
            "capacity_excess": float(r10 - floor),
            "noncapacity_fraction_of_r9_excess": float((mean_r9 - r10) / (mean_r9 - floor)),
            "r9_sample_mean": float(sample_r9), "r10_sample_mean": float(sample_r10),
            "paired_sample_gap": float(sample_r9 - sample_r10),
            "seeds_r10_strictly_better": sum(v["r10_units_context3"] < v["r9_units_context3"]
                                           for v in per_seed.values()),
        },
    }
    with (output / "evaluation.json").open("x", encoding="utf-8") as stream:
        json.dump(summary, stream, sort_keys=True, separators=(",", ":"), allow_nan=False)
        stream.write("\n")
    print(json.dumps({"verification": certified, "comparison": summary["comparison"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    evaluate(args.certificate, args.output)
