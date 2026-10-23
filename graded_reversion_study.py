"""Freeze, phase A, and phase B entry points for graded joint recurrent reversion.

Appendix A is refused. Phase B trains only when the approval note, the freeze,
and a completed phase A with no blocking engineering issue are all present.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch

from graded_reversion_appendix_a import run_appendix_a
from graded_reversion_draws import all_draw_sha256s
from graded_reversion_eval import evaluate_seed, pr7_expected_hashes
from graded_reversion_outcomes import l_prefix
from graded_reversion_report import render_phase_a, render_phase_b
from graded_reversion_spec import (
    APPROVAL_FILENAME,
    CODE_FILES,
    CODE_VERSION,
    FREEZE_FILENAME,
    PHASE_A_DIR,
    PHASE_A_PREFIX,
    PHASE_A_SEEDS,
    PHASE_B_DIR,
    PHASE_B_SEEDS,
    PROTOCOL_FILENAME,
    PROTOCOL_SHA256,
)
from graded_reversion_train import (
    approval_text_ok,
    build_inits,
    configure_runtime,
    missing_evaluation,
    refusal_reason,
    train_phase_b_seed,
)
from graded_reversion_verdicts import claim_text
from twostream_acquisition_oracle import World

ROOT = Path(__file__).resolve().parent


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def to_jsonable(value):
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        number = float(value)
        if not math.isfinite(number):
            return None
        return number
    if isinstance(value, int):
        return int(value)
    if value is None or isinstance(value, str):
        return value
    raise TypeError(type(value))


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(to_jsonable(payload), indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git_head() -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def load_freeze() -> dict:
    path = ROOT / FREEZE_FILENAME
    if not path.exists():
        raise SystemExit("freeze manifest is missing")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("protocol_sha256") != PROTOCOL_SHA256:
        raise SystemExit("freeze protocol hash does not match")
    for name, digest in manifest["code_sha256"].items():
        actual = sha256_file(ROOT / name)
        if actual != digest:
            raise SystemExit("code changed after freeze: %s" % name)
    return manifest


def freeze_matches() -> bool:
    try:
        load_freeze()
    except SystemExit:
        return False
    return True


def approval_ok() -> bool:
    path = ROOT / APPROVAL_FILENAME
    if not path.exists():
        return False
    return approval_text_ok(path.read_text(encoding="utf-8"), PROTOCOL_SHA256)


def engineering_status():
    path = ROOT / PHASE_A_DIR / "ENGINEERING_STATUS.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def phase_b_block_reason() -> str | None:
    return refusal_reason(approval_ok(), freeze_matches(), engineering_status())


def write_freeze() -> None:
    phase_a_results = ROOT / PHASE_A_DIR / "phase_a_results.json"
    phase_b_results = ROOT / PHASE_B_DIR / "phase_b_results.json"
    if phase_a_results.exists() or phase_b_results.exists():
        raise SystemExit("refuse to rewrite the freeze after study results exist")
    protocol = sha256_file(ROOT / PROTOCOL_FILENAME)
    if protocol != PROTOCOL_SHA256:
        raise SystemExit("protocol hash does not match the reviewed file")
    code = {name: sha256_file(ROOT / name) for name in CODE_FILES}
    draws = all_draw_sha256s()
    document = {
        "study": "Graded joint recurrent reversion with oracle-referenced prefix-function loss",
        "status": "FREEZE. No phase A output and no phase B training is part of this freeze.",
        "code_version": CODE_VERSION,
        "protocol_file": PROTOCOL_FILENAME,
        "protocol_sha256": protocol,
        "approval_file": APPROVAL_FILENAME,
        "approval_sha256": code[APPROVAL_FILENAME],
        "code_sha256": code,
        "draw_sha256": draws,
        "draw_seeds": [int(seed) for seed in list(draws)],
        "draw_generator": "torch.Generator on CPU, seed 40000+100*s, 32 calls of randn((24, 8), dtype=float64), hashed before rescaling",
        "phase_A": "not run",
        "phase_B_training": "approved in the approval note; not executed as part of this freeze",
        "appendix_A": "not approved; not executed",
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "numpy": np.__version__,
        },
    }
    write_json(ROOT / FREEZE_FILENAME, document)
    print("wrote %s" % FREEZE_FILENAME, flush=True)


def _write_engineering(blocking: bool, issues: list[str]) -> None:
    write_json(
        ROOT / PHASE_A_DIR / "ENGINEERING_STATUS.json",
        {
            "header": PHASE_A_PREFIX,
            "blocking_engineering_issue": blocking,
            "code_version": CODE_VERSION,
            "issues": issues,
        },
    )


def run_phase_a() -> None:
    manifest = load_freeze()
    actual = all_draw_sha256s(PHASE_A_SEEDS)
    for seed_key, digest in actual.items():
        if manifest["draw_sha256"][seed_key] != digest:
            _write_engineering(True, ["draw sha256 mismatch for seed %s before evaluation" % seed_key])
            raise SystemExit("draw sequence does not match the freeze manifest")
    configure_runtime()
    world = World()
    if l_prefix(world.q, world.q) != 0.0:
        _write_engineering(True, ["L_prefix(q_star) is not 0"])
        raise SystemExit("L_prefix identity failed before phase A")
    out = ROOT / PHASE_A_DIR
    seed_dir = out / "seeds"
    seed_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for seed in PHASE_A_SEEDS:
        path = seed_dir / ("s%d.json" % seed)
        if path.exists():
            record = json.loads(path.read_text(encoding="utf-8"))
            if record.get("code_version") != CODE_VERSION:
                raise SystemExit("existing phase A seed file has a different code version")
            records.append(record)
            print("phase A resume seed %d" % seed, flush=True)
            continue
        try:
            record = evaluate_seed(
                seed,
                world,
                ROOT / "recurrent_core_results_v1" / "checkpoints",
                pr7_expected_hashes(ROOT, seed),
                draw_sha_expected=manifest["draw_sha256"][str(seed)],
            )
        except Exception as exc:
            _write_engineering(True, ["seed %d raised %s: %s" % (seed, type(exc).__name__, exc)])
            raise
        record["header"] = PHASE_A_PREFIX
        write_json(path, record)
        records.append(record)
        primary = record["targets"]["weight_hh"]
        print(
            "phase A seed %d valid=%s AUC_REV=%s D=%s M=%s eligible=%s"
            % (
                seed,
                record["valid"],
                primary["auc_rev"],
                primary["D"],
                primary["M"],
                record["eligible"]["weight_hh"],
            ),
            flush=True,
        )
    issues = []
    for record in records:
        for flag in record.get("engineering_flags", []):
            issues.append("seed %s: %s" % (record["seed"], flag))
    metadata = {
        "protocol_sha256": PROTOCOL_SHA256,
        "freeze_manifest_sha256": sha256_file(ROOT / FREEZE_FILENAME),
        "freeze_commit": git_head(),
    }
    document = {
        "header": PHASE_A_PREFIX,
        "development_only": True,
        "confirmatory": False,
        "code_version": CODE_VERSION,
        "protocol_sha256": PROTOCOL_SHA256,
        "freeze_manifest_sha256": metadata["freeze_manifest_sha256"],
        "freeze_commit": metadata["freeze_commit"],
        "criterion_frozen_before_results": True,
        "seeds": records,
    }
    markdown = render_phase_a(records, metadata)
    write_json(out / "phase_a_results.json", document)
    (out / "PHASE_A_RESULTS.md").write_text(markdown, encoding="utf-8")
    blocking = len(issues) > 0
    _write_engineering(blocking, issues)
    if blocking:
        note = (
            "# Engineering note\n\n"
            "Phase A surfaced an engineering issue. It is not fixed here. "
            "A new hashed version is required before phase B.\n\n"
            + "\n".join("- %s" % issue for issue in issues)
            + "\n"
        )
        (out / "ENGINEERING_NOTE.md").write_text(PHASE_A_PREFIX + "\n\n" + note, encoding="utf-8")
        raise SystemExit("phase A engineering issue; phase B must not run")
    print("phase A complete", flush=True)


def run_phase_b() -> None:
    reason = phase_b_block_reason()
    if reason:
        raise SystemExit(reason)
    manifest = load_freeze()
    for seed in PHASE_B_SEEDS:
        key = str(seed)
        if all_draw_sha256s((seed,))[key] != manifest["draw_sha256"][key]:
            raise SystemExit("phase B draw sha256 does not match the freeze for seed %d" % seed)
    configure_runtime()
    world = World()
    out = ROOT / PHASE_B_DIR
    checkpoint_dir = out / "checkpoints"
    seed_dir = out / "seeds"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    seed_dir.mkdir(parents=True, exist_ok=True)
    inits = build_inits(PHASE_B_SEEDS)
    records = []
    for seed in PHASE_B_SEEDS:
        path = seed_dir / ("s%d.json" % seed)
        if path.exists():
            record = json.loads(path.read_text(encoding="utf-8"))
            if record.get("complete") and record.get("evaluation", {}).get("code_version") == CODE_VERSION:
                records.append(record)
                print("phase B resume seed %d" % seed, flush=True)
                continue
        print("phase B train seed %d" % seed, flush=True)
        trained = train_phase_b_seed(seed, world, inits[seed], checkpoint_dir)
        print(
            "phase B seed %d trained ready=%s e1=%s" % (seed, trained["training_ready"], trained["e1_pass"]),
            flush=True,
        )
        if not trained["training_ready"]:
            evaluation = missing_evaluation(seed, ["training"])
        else:
            evaluation = evaluate_seed(
                seed,
                world,
                checkpoint_dir,
                trained["expected_hashes"],
                draw_sha_expected=manifest["draw_sha256"][str(seed)],
            )
        record = {
            "header": "PHASE B confirmation. Not pooled with phase A.",
            "seed": int(seed),
            "complete": True,
            "code_version": CODE_VERSION,
            "e1_pass": trained["e1_pass"],
            "training_ready": trained["training_ready"],
            "training": trained["training"],
            "evaluation": evaluation,
        }
        write_json(path, record)
        records.append(record)
        if evaluation.get("engineering_flags"):
            note = (
                "# Engineering note\n\n"
                "Phase B evaluation surfaced an engineering issue on seed %d. "
                "The code is not changed. No confirmatory label is issued.\n\n%s\n"
                % (seed, "\n".join("- %s" % flag for flag in evaluation["engineering_flags"]))
            )
            (out / "ENGINEERING_NOTE.md").write_text(note, encoding="utf-8")
            raise SystemExit("phase B engineering issue on seed %d" % seed)
    e1_flags = [bool(record["e1_pass"]) for record in records]
    valid_flags = [bool(record["evaluation"]["valid"]) for record in records]
    joint_flags = [bool(record["evaluation"]["joint"]["weight_hh"]) for record in records]
    directional_flags = []
    material_flags = []
    eligible_flags = []
    for record in records:
        evaluation = record["evaluation"]
        target = None if not evaluation.get("targets") else evaluation["targets"].get("weight_hh")
        directional_flags.append(bool(target and target["D"]))
        material_flags.append(bool(target and target["M"]))
        eligible_flags.append(bool(evaluation["eligible"]["weight_hh"]))
    claim = claim_text(e1_flags, valid_flags, joint_flags, directional_flags, material_flags, eligible_flags)
    metadata = {
        "protocol_sha256": PROTOCOL_SHA256,
        "freeze_commit": git_head(),
        "phase_a_dir": PHASE_A_DIR,
    }
    document = {
        "header": "PHASE B confirmation seeds 200-209. Not pooled with phase A.",
        "code_version": CODE_VERSION,
        "protocol_sha256": PROTOCOL_SHA256,
        "freeze_commit": metadata["freeze_commit"],
        "approval": {
            "name": "Aidan Ahern",
            "date": "2026-10-20",
            "time_et": "10:38 PM ET",
            "source": "Grok Bot chat",
            "words": "Yes, approve it once Astra clears it",
        },
        "claim": claim,
        "seeds": records,
    }
    markdown = render_phase_b(records, metadata, claim)
    write_json(out / "phase_b_results.json", document)
    (out / "PHASE_B_RESULTS.md").write_text(markdown, encoding="utf-8")
    print("phase B complete", flush=True)
    print(claim, flush=True)


def main(argv: list[str]) -> None:
    if len(argv) != 2:
        raise SystemExit("usage: graded_reversion_study.py [write-freeze|phase-a|phase-b|appendix-a]")
    command = argv[1]
    if command == "write-freeze":
        write_freeze()
    elif command == "phase-a":
        run_phase_a()
    elif command == "phase-b":
        run_phase_b()
    elif command == "appendix-a":
        run_appendix_a()
    else:
        raise SystemExit("unknown command %s" % command)


if __name__ == "__main__":
    main(sys.argv)
