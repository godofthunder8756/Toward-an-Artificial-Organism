"""Independent read-only raw artifact audit; no training, no silent exclusions.

Raw format (future H16): one compressed .npz per final seed/family containing
components:uint8[4096,4,3], actions:uint8[4096,4,3], words:uint8[4096,4]
for word arms (empty [0,4] otherwise). A UTF-8 manifest.json contains a
SHA-256 for every raw file, code hashes, costs, routes and checkpoint paths.
The caller must create a fresh results directory with exclusive creation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import torch

from phase3b import PRIMARY
from phase3b.execution import clone_check, r4_training_route, source_hashes
from phase3b.models import Arm
from phase3b.resources import require_fit
from phase3b.statistics import final_gate
from phase3b.world import generate, loss_units


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_raw_fresh(path: Path, arrays: dict[str, np.ndarray]) -> str:
    """Exclusive file creation; H16 owns external authorization and directory."""
    if path.suffix != ".npz" or set(arrays) != {"components", "actions", "words"}:
        raise ValueError("invalid raw artifact schema")
    with path.open("xb") as stream:
        np.savez_compressed(stream, components=arrays["components"],
                            actions=arrays["actions"], words=arrays["words"])
    return _sha(path)


def validate_raw_arrays(arm: str, episode, arrays: dict[str, np.ndarray]) -> np.ndarray:
    """Validate exact on-wire values and recompute component losses from truth."""
    if set(arrays) != {"components", "actions", "words"}:
        raise ValueError("raw artifact missing arrays; STOP")
    component, action, word = (arrays[key] for key in ("components", "actions", "words"))
    size = episode.common.shape[0]
    if component.shape != (size, 4, 3) or action.shape != (size, 4, 3):
        raise ValueError("raw episode/context shape invalid; STOP")
    if any(a.dtype != np.uint8 for a in arrays.values()):
        raise ValueError("raw loss/action/word dtype invalid; STOP")
    if np.any(action[:, :, (0, 2)] > 1) or np.any(action[:, :, 1] > 2):
        raise ValueError("action out of range; STOP")
    expected_word_shape = (size, 4) if arm in ("candidate", "R4", "R9") else (0, 4)
    if word.shape != expected_word_shape or (word.size and np.any(word > 7)):
        raise ValueError("word alphabet/shape invalid; STOP")
    reconstructed = loss_units(tuple(torch.from_numpy(action[:, :, i].astype(np.int64))
                                     for i in range(3)), episode.truth).numpy()
    if not np.array_equal(component, reconstructed):
        raise ValueError("raw losses do not match truth/actions; STOP")
    return component[:, 3, :].sum(1, dtype=np.int64)


def validate_resource_snapshot(reported: dict, model: Arm) -> None:
    """Replay deterministic dry-run counts; time and incomplete traffic are not parity."""
    if not isinstance(reported, dict):
        raise ValueError("missing resource log; STOP")
    expected = require_fit(model)
    for key, value in expected.items():
        if key == "dry_run_wall_seconds":
            if not isinstance(reported.get(key), (int, float)) or reported[key] <= 0:
                raise ValueError("missing dry-run latency; STOP")
        elif reported.get(key) != value:
            raise ValueError(f"resource {key} disagrees with whole-arm dry run; STOP")


def validate_r4_route(info: dict) -> tuple[int, int, int, int]:
    route = info.get("route")
    search = info.get("route_search")
    if (not isinstance(route, list) or len(route) != 4
            or any(type(v) is not int or v not in range(4) for v in route)
            or route[3] != (route[2] + 1) % 4
            or not isinstance(search, dict)
            or search.get("routes_enumerated") != 256
            or search.get("search_exposure_per_address") != 8192
            or search.get("training_exposure_per_address") != 2048
            or not isinstance(search.get("search_forward_macs"), int)
            or search["search_forward_macs"] <= 0
            or not isinstance(search.get("search_wall_seconds"), (int, float))
            or search["search_wall_seconds"] <= 0):
        raise ValueError("R4 training-only route search/fallback not documented; STOP")
    table = search.get("training_loss_table_units")
    if (not isinstance(table, list) or len(table) != 3
            or any(not isinstance(row, list) or len(row) != 4
                   or any(type(v) is not int or v < 0 for v in row) for row in table)
            or r4_training_route(torch.tensor(table)) != tuple(route)):
        raise ValueError("R4 route does not minimize recorded training table; STOP")
    return tuple(route)


def audit(root: Path) -> dict:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema") != 1 or manifest.get("source_sha256") != source_hashes():
        raise ValueError("missing/mismatched source hashes; STOP")
    from phase3b.freeze import verify_preflight_snapshot

    snapshot_hash = manifest.get("preflight_snapshot_sha256")
    if not isinstance(snapshot_hash, str):
        raise ValueError("missing preflight snapshot hash; STOP")
    verify_preflight_snapshot(root / "preflight_snapshot.json", snapshot_hash)
    if set(manifest.get("seeds", {})) != {str(s) for s in range(1000, 1016)}:
        raise ValueError("final seed family incomplete; STOP")
    per_seed: dict[int, dict[str, np.ndarray]] = {}
    clone_inputs = 0
    for seed_text, entries in manifest["seeds"].items():
        seed = int(seed_text)
        if set(entries) != set(PRIMARY):
            raise ValueError("missing compulsory family or EXTERNAL in envelope; STOP")
        ep = generate(20_000 + seed, 4096)
        per_seed[seed] = {}
        for arm, info in entries.items():
            path = root / f"{seed}_{arm}.npz"
            if info.get("sha256") != _sha(path):
                raise ValueError(f"{path.name}: raw hash mismatch; STOP")
            with np.load(path, allow_pickle=False) as data:
                arrays = {key: data[key] for key in data.files}
            per_seed[seed][arm] = validate_raw_arrays(arm, ep, arrays)
            action, word = arrays["actions"], arrays["words"]
            config = info.get("configuration")
            if not isinstance(config, dict) or config.get("learning_rate") not in (0.0003, 0.001):
                raise ValueError("missing frozen configuration; STOP")
            if arm == "R4":
                validate_r4_route(info)
            model = Arm(arm, config["width"])
            validate_resource_snapshot(info.get("resources", {}), model)
            checkpoint = root / f"{seed}_{arm}.pt"
            if info.get("checkpoint_sha256") != _sha(checkpoint):
                raise ValueError("missing/mismatched checkpoint; STOP")
            model.load_state_dict(torch.load(checkpoint, map_location="cpu", weights_only=True))
            if arm == "R4":
                model.route = validate_r4_route(info)
            if arm == "candidate":
                clone_inputs += clone_check(model)
            # Reproduce every reported decision on the original seed stream.
            model.eval()
            with torch.no_grad():
                for offset in range(0, 4096, 128):
                    trace = model(ep.common[offset:offset+128], ep.local[offset:offset+128])
                    if not np.array_equal(torch.stack(trace.actions, -1).numpy(),
                                          action[offset:offset+128]):
                        raise ValueError("checkpoint action replay failed; STOP")
                    if trace.word is not None and not np.array_equal(trace.word.numpy(), word[offset:offset+128]):
                        raise ValueError("checkpoint message replay failed; STOP")
    return {"gate": final_gate(per_seed), "r9_clone_decisions": clone_inputs,
            "audit": "raw and checkpoints verified; independent resource completeness still required",
            "authorization": "STOP: physical memory traffic, torch peak, backward nonlinear "
                     "work and whole-arm resource parity not independently validated"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read-only Phase III-B raw audit")
    parser.add_argument("results", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.results), indent=2))