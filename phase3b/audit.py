"""Independent read-only raw artifact audit; no training, no silent exclusions.

Raw format (future H16): one compressed .npz per final seed/family containing
components:uint8[4096,4,3], actions:uint8[4096,4,3], words:uint8[4096,4]
for word arms (empty [0,4] otherwise). A UTF-8 manifest.json contains a
SHA-256 for every raw and checkpoint file, an H10-compatible tensor state
digest, code hashes, costs and routes.
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
from phase3b.execution import clone_check, r4_training_route, source_hashes, training_context_score
from phase3b.models import Arm
from phase3b.resources import require_fit
from phase3b.statistics import final_gate
from phase3b.transfer import _state_bytes
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
        if reported.get(key) != value:
            raise ValueError(f"resource {key} disagrees with whole-arm dry run; STOP")


def validate_state_digest(reported: dict, model: Arm) -> None:
    """H10-compatible tensor digest, distinct from serialized .pt file SHA."""
    if (not isinstance(reported.get("state_digest"), str)
            or reported["state_digest"] != _state_bytes(model)):
        raise ValueError("checkpoint tensor state digest mismatch; STOP")


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


def validate_engineering_selection(row: dict, family: str, grid: list[list],
                                   freeze_digest: str, approval_digest: str) -> None:
    if (not isinstance(row, dict) or row.get("schema") != 1 or row.get("family") != family
            or row.get("freeze_sha256") != freeze_digest
            or row.get("engineering_approval_sha256") != approval_digest
            or not isinstance(row.get("configurations"), list)
            or len(row["configurations"]) != len(grid)):
        raise ValueError("engineering selection provenance incomplete; STOP")
    for config, (width, lr) in zip(row["configurations"], grid):
        if (not isinstance(config, dict) or config.get("width") != width
                or config.get("learning_rate") != lr
                or config.get("seeds") != list(range(4))
                or not isinstance(config.get("seed_scores"), list)
                or len(config["seed_scores"]) != 4
                or any(type(v) is not int or v < 0 for v in config["seed_scores"])
                or config.get("training_context_loss_units") != sum(config["seed_scores"])
                or not isinstance(config.get("spends"), list) or len(config["spends"]) != 4
                or any(not isinstance(v, dict) or v.get("episodes") != 8192
                       or v.get("updates") != 256 for v in config["spends"])
                or not isinstance(config.get("checkpoint_sha256"), list)
                or len(config["checkpoint_sha256"]) != 4
                or any(not isinstance(v, str) or len(v) != 64
                       for v in config["checkpoint_sha256"])
                or config.get("parameters") != require_fit(Arm(family, width))["trainable_parameters"]):
            raise ValueError("engineering grid/seed/score incomplete; STOP")
    best = min(row["configurations"],
               key=lambda r: (r["training_context_loss_units"], r["parameters"], r["learning_rate"]))
    if row.get("selected") != {"width": best["width"], "learning_rate": best["learning_rate"]}:
        raise ValueError("engineering winner inconsistent with training-only scores; STOP")


def audit(root: Path) -> dict:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema") != 2 or manifest.get("source_sha256") != source_hashes():
        raise ValueError("missing/mismatched source hashes; STOP")
    from phase3b.freeze import verify_preflight_snapshot, verify_execution_freeze, verify_approval

    snapshot_hash = manifest.get("preflight_snapshot_sha256")
    if not isinstance(snapshot_hash, str):
        raise ValueError("missing preflight snapshot hash; STOP")
    verify_preflight_snapshot(root / "preflight_snapshot.json", snapshot_hash)
    freeze_hash = manifest.get("freeze_sha256")
    frozen = verify_execution_freeze(root / "execution_freeze.json", freeze_hash)
    if frozen["preflight_snapshot_sha256"] != snapshot_hash:
        raise ValueError("preflight/execution freeze mismatch; STOP")
    approvals = {}
    for phase in ("engineering", "final"):
        digest = manifest.get(f"{phase}_approval_sha256")
        approvals[phase] = verify_approval(
            {"freeze_path": str(root / "execution_freeze.json"), "freeze_sha256": freeze_hash,
             "approval_path": str(root / f"{phase}_approval.json"), "approval_sha256": digest}, phase)
    if set(manifest.get("selections_sha256", {})) != set(PRIMARY):
        raise ValueError("engineering selections missing; STOP")
    if (approvals["final"]["approval"]["selections_sha256"]
            != manifest["selections_sha256"]):
        raise ValueError("final approval did not bind engineering selection; STOP")
    selections = {}
    for family in PRIMARY:
        path = root / f"selection_{family}.json"
        if _sha(path) != manifest["selections_sha256"][family]:
            raise ValueError("engineering selection digest mismatch; STOP")
        row = json.loads(path.read_text(encoding="utf-8"))
        validate_engineering_selection(row, family, frozen["contract"]["grids"][family],
                                       freeze_hash, manifest["engineering_approval_sha256"])
        selections[family] = row["selected"]
        for config in row["configurations"]:
            for seed, expected, score in zip(config["seeds"], config["checkpoint_sha256"],
                                             config["seed_scores"]):
                checkpoint = root / f"engineering_{family}_{config['width']}_{config['learning_rate']}_{seed}.pt"
                if _sha(checkpoint) != expected:
                    raise ValueError("engineering checkpoint hash mismatch; STOP")
                model = Arm(family, config["width"])
                model.load_state_dict(torch.load(checkpoint, map_location="cpu", weights_only=True))
                if family == "R4":
                    route_search = config["spends"][seed].get("route_search")
                    model.route = validate_r4_route({"route": route_search.get("route"),
                                                      "route_search": route_search})
                if training_context_score(model, seed) != score:
                    raise ValueError("engineering training-only score replay failed; STOP")
    if set(manifest.get("seeds", {})) != {str(s) for s in range(1000, 1016)}:
        raise ValueError("final seed family incomplete; STOP")
    expected_files = {"manifest.json", "execution_freeze.json", "preflight_snapshot.json",
                      "final_approval.json", "engineering_approval.json"}
    expected_files.update(f"selection_{family}.json" for family in PRIMARY)
    for family in PRIMARY:
        for width, lr in frozen["contract"]["grids"][family]:
            expected_files.update(f"engineering_{family}_{width}_{lr}_{seed}.pt"
                                  for seed in range(4))
    for seed in range(1000, 1016):
        for family in PRIMARY:
            expected_files.update((f"{seed}_{family}.npz", f"{seed}_{family}.pt"))
    if {path.name for path in root.iterdir()} != expected_files:
        raise ValueError("unexpected/missing results or unreported failed runs; STOP")
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
            if config != selections[arm]:
                raise ValueError("missing frozen configuration; STOP")
            training = info.get("training")
            if (not isinstance(training, dict) or training.get("episodes") != 8192
                    or training.get("updates") != 256):
                raise ValueError("final training spend incomplete; STOP")
            if arm == "R4":
                validate_r4_route(info)
            model = Arm(arm, config["width"])
            validate_resource_snapshot(info.get("resources", {}), model)
            checkpoint = root / f"{seed}_{arm}.pt"
            if info.get("checkpoint_file_sha256") != _sha(checkpoint):
                raise ValueError("missing/mismatched checkpoint file SHA; STOP")
            model.load_state_dict(torch.load(checkpoint, map_location="cpu", weights_only=True))
            validate_state_digest(info, model)
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
                    if trace.word is None and word.size:
                        raise ValueError("unexpected checkpoint message; STOP")
    return {"gate": final_gate(per_seed), "r9_clone_decisions": clone_inputs,
            "audit": "raw decisions, checkpoint state and engineering selection scores replayed",
            "coverage_limitations": [
                "physical memory bus traffic unmeasured; not a hard equality gate",
                "isolated per-arm OS peak unmeasured; not a hard equality gate",
                "training trajectories and measured resource observations not independently replayed",
            ]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read-only Phase III-B raw audit")
    parser.add_argument("results", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.results), indent=2))