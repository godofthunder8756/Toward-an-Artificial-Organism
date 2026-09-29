"""Bounded read-only post-final H8/H10 diagnostic. Never fits a primary arm.

Run with --self-test, then without arguments. The exclusive JSON output is
written only after the frozen provenance, checkpoint, and replay checks pass.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import log2
from pathlib import Path
import sys

import numpy as np
import torch

FILES = Path(r"C:\Users\aahern\.copilot\session-state\3ffce2fd-a108-4f2c-a6cd-03497b39eee4\files")
ROOT = FILES / "phase3b_finals_v1"
OUTPUT = FILES / "phase3b_h10_diagnostics_v1.json"
REPO = Path(r"C:\Users\aahern\Documents\GitHub\Toward-an-Artificial-Organism")
SEEDS = range(1000, 1016)
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(FILES))

from phase3b.audit import validate_r4_route, validate_state_digest  # noqa: E402
from phase3b.models import Arm  # noqa: E402
from phase3b.proof import bayes_action, verify_h3  # noqa: E402
from phase3b.world import generate, posterior_counts  # noqa: E402
from phase3b_interventions_runner_v1 import sha, verify_inputs  # noqa: E402


def frac(value: Fraction) -> str:
    return str(value)


def entropy(values: np.ndarray, size: int) -> float:
    counts = np.bincount(values.astype(np.int64), minlength=size)
    p = counts[counts > 0] / len(values)
    return float(-(p * np.log2(p)).sum())


def mi(values: np.ndarray, truth: np.ndarray, size: int) -> float:
    joint = np.bincount(values.astype(np.int64) * 2 + truth.astype(np.int64),
                        minlength=size * 2).reshape(size, 2)
    n = joint.sum()
    px, py = joint.sum(1) / n, joint.sum(0) / n
    return float(sum(joint[x, y] / n * log2((joint[x, y] / n) / (px[x] * py[y]))
                     for x in range(size) for y in range(2) if joint[x, y]))


def information(address: np.ndarray, payload: np.ndarray, truth: np.ndarray) -> list[dict]:
    rows = []
    for c in range(4):
        a, p = address[:, c], payload[:, c]
        w = a * 2 + p
        rows.append({
            "context": c, "episodes": len(a),
            "port_occupancy": np.bincount(a, minlength=4).tolist(),
            "address_entropy_bits": entropy(a, 4),
            "payload_entropy_bits": entropy(p, 2),
            "word_entropy_bits": entropy(w, 8),
            "address_truth_mi_bits": [mi(a, truth[:, j], 4) for j in range(4)],
            "word_truth_mi_bits": [mi(w, truth[:, j], 8) for j in range(4)],
        })
    return rows


def posterior_common(history: tuple[int, ...]) -> tuple[Fraction, ...]:
    return tuple(Fraction((1, 8, 16)[history[j] + history[j + 4]],
                          (17, 16, 17)[history[j] + history[j + 4]]) for j in range(4))


def conditional_risk(history: tuple[int, ...], maps: tuple[tuple[int, int], ...]
                     ) -> tuple[Fraction, tuple[tuple[Fraction, Fraction], ...]]:
    """Exact Bayes expectation over factor truth and each independent local BSC."""
    q = posterior_common(history)
    weighted = Fraction(0)
    conditional = []
    for i in range(3):
        target = i
        bit_risks = []
        for bit in (0, 1):
            probability = q[target] * (Fraction(4, 5) if bit else Fraction(1, 5))
            probability += (1 - q[target]) * (Fraction(1, 5) if bit else Fraction(4, 5))
            updated = list(q)
            updated[target] = q[target] * (Fraction(4, 5) if bit else Fraction(1, 5)) / probability
            correct = (updated[0] if i == 0 else updated[1] if i == 1 else
                       updated[2] * (1 - updated[3]) + (1 - updated[2]) * updated[3])
            action = maps[i][bit]
            risk = (Fraction(9) if i == 1 and action == 2 else
                    50 * (correct if action == 0 else 1 - correct))
            bit_risks.append(risk / 150)
            weighted += probability * risk / 150
        conditional.append(tuple(bit_risks))
    return weighted, tuple(conditional)


def response_maps(model: Arm, words: torch.Tensor, context: int
                  ) -> list[tuple[tuple[int, int], ...]]:
    with torch.no_grad():
        return [tuple(tuple(model.read(words[:, context], torch.full_like(words[:, context], b),
                                       context, i).argmax(-1).tolist()[k]
                            for b in (0, 1)) for i in range(3))
                for k in range(len(words))]


def groups() -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    all_histories = list(product((0, 1), repeat=8))
    a = [h for h in all_histories if tuple(h[j] + h[j + 4] for j in range(4)) == (2, 1, 1, 1)]
    b = [h for h in all_histories if tuple(h[j] + h[j + 4] for j in range(4)) == (1, 2, 1, 1)]
    if len(a) != 8 or len(b) != 8:
        raise AssertionError("H3 positive-support enumeration changed; STOP")
    return a, b


def matched(model: Arm, r4: Arm) -> dict:
    ga, gb = groups()
    histories = ga + gb
    common = torch.tensor(histories, dtype=torch.long)
    with torch.no_grad():
        states = model.encode(common)
        words, addresses, payloads, _ = model.write(states, 4)
        r4_words = r4.write(r4.encode(common), 4)[0]
        forced = [model.write(states, 4, forced=torch.full((16, 4), port, dtype=torch.long))[0]
                  for port in range(4)]
    own = response_maps(model, words, 0)
    fixed = response_maps(r4, r4_words, 0)
    forced_maps = [response_maps(model, w, 0) for w in forced]
    substituted = [response_maps(model, (port * 2 + payloads).long(), 0)
                   for port in range(4)]
    records = []
    for k, history in enumerate(histories):
        def entry(mapping: tuple[tuple[int, int], ...]) -> tuple[str, list[list[str]]]:
            risk, by_bit = conditional_risk(history, mapping)
            return frac(risk), [[frac(v) for v in row] for row in by_bit]
        records.append({
            "history": "".join(map(str, history)), "group": "A" if k < 8 else "B",
            "candidate_word": int(words[k, 0]), "candidate_address": int(addresses[k, 0]),
            "r4_word": int(r4_words[k, 0]), "r4_address": int(r4_words[k, 0] // 2),
            "candidate_map": own[k], "r4_map": fixed[k],
            "candidate_risk_and_conditional_bits": entry(own[k]),
            "r4_risk_and_conditional_bits": entry(fixed[k]),
            "i1_address_only_risks": [entry(sm[k])[0] for sm in substituted],
            "i3_forced_source_risks": [entry(fm[k])[0] for fm in forced_maps],
        })
    pairs = []
    for a in range(8):
        for b in range(8, 16):
            base_a = conditional_risk(histories[a], own[a])[0]
            base_b = conditional_risk(histories[b], own[b])[0]
            i1_a = conditional_risk(histories[a], substituted[int(addresses[b, 0])][a])[0]
            i1_b = conditional_risk(histories[b], substituted[int(addresses[a, 0])][b])[0]
            r4_a = conditional_risk(histories[a], fixed[a])[0]
            r4_b = conditional_risk(histories[b], fixed[b])[0]
            pairs.append({
                "a": a, "b": b - 8,
                "candidate_address_changed": bool(addresses[a, 0] != addresses[b, 0]),
                "r4_address_changed": bool(r4_words[a, 0] // 2 != r4_words[b, 0] // 2),
                "candidate_map_changed": own[a] != own[b],
                "r4_map_changed": fixed[a] != fixed[b],
                "candidate_risk": [frac(base_a), frac(base_b)],
                "r4_risk": [frac(r4_a), frac(r4_b)],
                "i1_swap_address_only_risk": [frac(i1_a), frac(i1_b)],
                "i1_swap_delta": frac((i1_a + i1_b) - (base_a + base_b)),
                "zero_effect_pair": (base_a == i1_a and base_b == i1_b),
                "tie_candidate_r4": (base_a + base_b == r4_a + r4_b),
            })
    return {
        "context": 0, "groups": {"A": len(ga), "B": len(gb)}, "pairs_enumerated": len(pairs),
        "histories": records, "pairs": pairs,
        "counts": {key: sum(bool(p[key]) for p in pairs) for key in (
            "candidate_address_changed", "r4_address_changed", "candidate_map_changed",
            "r4_map_changed", "zero_effect_pair", "tie_candidate_r4")},
    }


def decode(model: Arm, seed: int, heldout) -> dict:
    train = torch.cat([generate(100_000 + seed * 256 + u, 32).common for u in range(256)])
    if train.shape != (8192, 8):
        raise AssertionError("decoder training histories changed; STOP")
    with torch.no_grad():
        states = model.encode(train).numpy()
        test = model.encode(heldout.common).numpy()
    y = posterior_counts(train).numpy()
    actual = posterior_counts(heldout.common).numpy()
    per_port = []
    for j in range(4):
        baseline = int(np.bincount(y[:, j], minlength=3).argmax())
        # Fixed nearest-centroid lookup: one centroid for each count, no tuned hyperparameters.
        if any(not np.any(y[:, j] == count) for count in range(3)):
            raise ValueError("decoder missing training count; STOP")
        centers = np.stack([states[y[:, j] == count, j].mean(0) for count in range(3)])
        pred = ((test[:, j, None, :] - centers[None, :, :]) ** 2).sum(-1).argmin(-1)
        per_port.append({"port": j, "train_count_occupancy": np.bincount(y[:, j], minlength=3).tolist(),
                         "baseline_count": baseline, "correct": int((pred == actual[:, j]).sum()),
                         "baseline_correct": int((actual[:, j] == baseline).sum()),
                         "accuracy": float((pred == actual[:, j]).mean()),
                         "baseline_accuracy": float((actual[:, j] == baseline).mean())})
    return {"method": "Euclidean nearest of three training-only per-count port-state centroids",
            "training_histories": 8192, "heldout_histories": 4096, "ports": per_port}


def load(root: Path, manifest: dict, seed: int, family: str, ep) -> Arm:
    info = manifest["seeds"][str(seed)][family]
    checkpoint = root / f"{seed}_{family}.pt"
    raw = root / f"{seed}_{family}.npz"
    if sha(checkpoint) != info["checkpoint_file_sha256"] or sha(raw) != info["sha256"]:
        raise ValueError(f"{seed} {family}: final checkpoint/raw SHA mismatch; STOP")
    if info["training"]["episodes"] != 8192 or info["training"]["updates"] != 256:
        raise ValueError("training contract mismatch; STOP")
    model = Arm(family, info["configuration"]["width"])
    model.load_state_dict(torch.load(checkpoint, map_location="cpu", weights_only=True))
    validate_state_digest(info, model)
    if family == "R4":
        model.route = validate_r4_route(info)
    model.eval()
    with np.load(raw, allow_pickle=False) as data:
        actions, expected_words = data["actions"], data["words"]
    with torch.no_grad():
        for start in range(0, 4096, 128):
            trace = model(ep.common[start:start + 128], ep.local[start:start + 128])
            if (not np.array_equal(torch.stack(trace.actions, -1).numpy(), actions[start:start + 128])
                    or not np.array_equal(trace.word.numpy(), expected_words[start:start + 128])):
                raise ValueError(f"{seed} {family}: final raw replay mismatch; STOP")
    return model


def self_test() -> None:
    a, b = groups()
    assert len(list(product(a, b))) == 64
    h = (0,) * 8
    assert posterior_common(h) == (Fraction(1, 17),) * 4
    assert conditional_risk(h, ((0, 0), (2, 2), (0, 0)))[0] > 0
    arr = np.array([0, 0, 1, 1])
    assert entropy(arr, 2) == 1 and mi(arr, arr, 2) == 1
    assert mi(arr, np.array([0, 1, 0, 1]), 2) == 0
    assert verify_h3()["policy_triples"] == 27
    for h in a + b:
        n = tuple(h[j] + h[j + 4] for j in range(4))
        bayes = tuple(tuple(bayes_action(i, n, bit) for bit in (0, 1)) for i in range(3))
        best, _ = conditional_risk(h, bayes)
        q = posterior_common(h)
        brute = Fraction(0)
        for truth in product((0, 1), repeat=4):
            p_truth = np.prod([q[j] if truth[j] else 1 - q[j] for j in range(4)])
            for local in product((0, 1), repeat=3):
                p_local = np.prod([Fraction(4, 5) if local[i] == truth[i] else Fraction(1, 5)
                                   for i in range(3)])
                actions = [bayes[i][local[i]] for i in range(3)]
                loss = (50 * (actions[0] != truth[0]) +
                        (9 if actions[1] == 2 else 50 * (actions[1] != truth[1])) +
                        50 * (actions[2] != (truth[2] ^ truth[3])))
                brute += p_truth * p_local * loss / 150
        assert best == brute


def main() -> None:
    if OUTPUT.exists():
        raise FileExistsError(f"exclusive result exists: {OUTPUT}")
    manifest, freeze, mh, ah = verify_inputs(ROOT, FILES / "phase3b_final_audit_v1.json")
    report = {
        "schema": 1, "phase": "POST-FINAL read-only H8/H10 secondary analysis",
        "manifest_sha256": mh, "audit_sha256": ah, "freeze_sha256": manifest["freeze_sha256"],
        "source_sha256": freeze["source_sha256"], "runner_sha256": sha(Path(__file__)),
        "witness": {"kind": "analytic factor-truthful menu, NOT an actual learned policy",
                    "h3": verify_h3(),
                    "group_A_counts": [2, 1, 1, 1], "group_B_counts": [1, 2, 1, 1],
                    "group_A_bayes_map": [[bayes_action(i, (2, 1, 1, 1), b) for b in (0, 1)]
                                          for i in range(3)],
                    "group_B_bayes_map": [[bayes_action(i, (1, 2, 1, 1), b) for b in (0, 1)]
                                          for i in range(3)]},
        "risk_units": "exact fractions of joint loss (component units / 150); group histories and 64 Cartesian pairs unweighted",
        "limitations": [
            "Empirical MI and decoder accuracy describe frozen endpoints, not causal necessity.",
            "Decoder labels are evaluator-only training-history counts; no decoder or truth is passed to primary forward.",
            "H3 matched histories are observational counterfactuals; I1 swaps address bits at read, retains the original payload; I3 recomputes payload for forced source.",
            "Matched-pair baseline and I1 risks integrate independent factor truth and local BSC exactly; no intervention changes trained weights.",
            "R4 is the frozen training-selected public route, not a newly optimized route.",
            "Audit attestation is hash-bound, not independently cryptographically signed by this runner.",
        ], "seeds": {},
    }
    for seed in SEEDS:
        ep = generate(20_000 + seed, 4096)
        candidate = load(ROOT, manifest, seed, "candidate", ep)
        r4 = load(ROOT, manifest, seed, "R4", ep)
        with torch.no_grad():
            trace = candidate(ep.common, ep.local)
        report["seeds"][str(seed)] = {
            "candidate": {"information": information(trace.address.numpy(), trace.payload.numpy(),
                                                       ep.truth.numpy()),
                          "decoder": decode(candidate, seed, ep)},
            "r4_route": list(r4.route), "h3": matched(candidate, r4),
        }
    rows = [report["seeds"][str(s)] for s in SEEDS]
    report["aggregate"] = {
        "heldout_episodes_per_seed": 4096, "training_histories_per_seed": 8192,
        "seeds": len(rows), "matched_pairs": sum(row["h3"]["pairs_enumerated"] for row in rows),
        "pair_counts": {key: sum(row["h3"]["counts"][key] for row in rows)
                        for key in rows[0]["h3"]["counts"]},
        "decoder_accuracy": sum(port["correct"] for row in rows
                                for port in row["candidate"]["decoder"]["ports"]) / (16 * 4 * 4096),
        "decoder_baseline_accuracy": sum(port["baseline_correct"] for row in rows
                                         for port in row["candidate"]["decoder"]["ports"]) / (16 * 4 * 4096),
        "information_by_context": [{
            "context": c,
            "port_occupancy": [sum(row["candidate"]["information"][c]["port_occupancy"][j]
                                   for row in rows) for j in range(4)],
            **{key: sum(row["candidate"]["information"][c][key] for row in rows) / 16
               for key in ("address_entropy_bits", "payload_entropy_bits", "word_entropy_bits")},
            **{key: [sum(row["candidate"]["information"][c][key][j] for row in rows) / 16
                     for j in range(4)]
               for key in ("address_truth_mi_bits", "word_truth_mi_bits")},
        } for c in range(4)],
        "h3_group_equal_history_mean_risks": {
            group: {
                family: frac(sum((Fraction(h[field][0]) for row in rows
                                  for h in row["h3"]["histories"] if h["group"] == group),
                                 Fraction(0)) / (16 * 8))
                for family, field in (("candidate", "candidate_risk_and_conditional_bits"),
                                      ("R4", "r4_risk_and_conditional_bits"))
            } for group in ("A", "B")
        },
    }
    raw = (json.dumps(report, sort_keys=True, allow_nan=False, separators=(",", ":")) + "\n").encode()
    with OUTPUT.open("xb") as stream:
        stream.write(raw)
    print(json.dumps({"output": str(OUTPUT), "result_sha256": hashlib.sha256(raw).hexdigest(),
                      "runner_sha256": report["runner_sha256"], "aggregate": report["aggregate"]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("synthetic checks passed")
    else:
        main()
