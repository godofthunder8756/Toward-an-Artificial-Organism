"""Freeze, phase A, and phase B for the first-order and isotropic control study.

Phase A is evaluation only. Phase B trains only after the approval record, a
matching freeze, and a phase A run with no blocking engineering flag.
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

from first_order_control_draws import all_manifests
from first_order_control_eval import evaluate_seed
from first_order_control_report import render_phase_a, render_phase_b
from first_order_control_spec import (
    APPROVAL_FILENAME,
    CODE_FILES,
    CODE_VERSION,
    FREEZE_FILENAME,
    PHASE_A_DIR,
    PHASE_A_PR7_SEEDS,
    PHASE_A_PR8_SEEDS,
    PHASE_A_PREFIX,
    PHASE_B_DIR,
    PHASE_B_SEEDS,
    PROTOCOL_FILENAME,
    PROTOCOL_SHA256,
    TARGETS,
)
from first_order_control_train import (
    build_inits,
    configure_runtime,
    missing_evaluation,
    train_confirmation_seed,
)
from first_order_control_verdicts import verdict_paragraph, primary_label
from twostream_acquisition_oracle import World

ROOT = Path(__file__).resolve().parent

# Printed Appendix B ranges. They are a rounded draft summary, not a tolerance.
_APPENDIX_RANGES = {
    "100-109": {"cos": (-0.340, 0.075), "dot": (-2.31e-3, 4.2e-4)},
    "200-209": {"cos": (-0.397, 0.129), "dot": (-2.20e-3, 6.8e-4)},
}


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
    temporary.write_text(json.dumps(to_jsonable(payload), indent=2, allow_nan=False) + "\n", encoding="utf-8")
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


def approval_text_ok(text: str) -> bool:
    required = (
        "Aidan Ahern",
        "2026-10-21",
        "1:05 AM ET",
        "widget t23s2",
        "Grok Bot chat",
        "Approve fresh-seed GRU-8 training (seeds 300-309, 30 runs) for the first-order-matched control confirmation once Astra clears the protocol?",
        "Yes, approve it once Astra clears it.",
        PROTOCOL_SHA256,
    )
    return all(piece in text for piece in required)


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
    return approval_text_ok(path.read_text(encoding="utf-8"))


def engineering_status():
    path = ROOT / PHASE_A_DIR / "ENGINEERING_STATUS.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def phase_b_block_reason() -> str | None:
    if not approval_ok():
        return "Phase B training approval record is missing or does not match the required text."
    if not freeze_matches():
        return "Freeze manifest does not match the current code."
    status = engineering_status()
    if status is None:
        return "Phase A has not been completed."
    if status.get("code_version") != CODE_VERSION:
        return "Phase A engineering status is from a different code version."
    if status.get("blocking_engineering_issue"):
        return "Phase A surfaced an engineering issue that must be versioned and hashed before phase B."
    return None


def write_freeze() -> None:
    phase_a_results = ROOT / PHASE_A_DIR / "phase_a_results.json"
    phase_b_results = ROOT / PHASE_B_DIR / "phase_b_results.json"
    if phase_a_results.exists() or phase_b_results.exists():
        raise SystemExit("refuse to rewrite the freeze after study results exist")
    protocol = sha256_file(ROOT / PROTOCOL_FILENAME)
    if protocol != PROTOCOL_SHA256:
        raise SystemExit("protocol hash does not match the reviewed file")
    code = {name: sha256_file(ROOT / name) for name in CODE_FILES}
    manifests = all_manifests()
    document = {
        "study": "Graded recurrent reversion against both first-order-matched and isotropic controls",
        "status": "FREEZE. No phase A output and no phase B training is part of this freeze.",
        "code_version": CODE_VERSION,
        "protocol_file": PROTOCOL_FILENAME,
        "protocol_sha256": protocol,
        "approval_file": APPROVAL_FILENAME,
        "approval_sha256": code[APPROVAL_FILENAME],
        "code_sha256": code,
        "manifests": manifests,
        "generator_seeds": {
            "training_init": "s",
            "training_episodes": "1000+s",
            "training_readout": "5000+s",
            "iso": "40000+100*s",
            "fo_base": "1000000+100*s",
            "gradient_check": "2000000+100*s",
            "manifest_seeds": [int(seed) for seed in manifests],
        },
        "tolerances": {
            "eps0": 1e-12,
            "IDENTITY_TOL": 1e-9,
            "NORM_REL_TOL": 1e-12,
            "FO_REL_TOL": 1e-12,
            "ORTH_TOL": 1e-12,
            "radius_gate": "abs(||d||^2 - ||p||^2 - r^2) <= 1e-12 * ||d||^2",
            "fd": "abs(FD - dot(G, direction)) <= 1e-10 + 1e-6*||G||",
            "G_ZERO": 1e-10,
            "RHO_COLLAPSE": 1e-3,
            "RHO_NEAR": 0.10,
            "THIN_REL": 0.10,
            "unevaluable_bound": 2,
        },
        "phase_A": "not run",
        "phase_B_training": "approved in the approval record; not executed as part of this freeze",
        "appendix": "none; no rival grid is approved or executed",
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "numpy": np.__version__,
        },
    }
    write_json(ROOT / FREEZE_FILENAME, document)
    print("wrote %s" % FREEZE_FILENAME, flush=True)


def _reference(seed: int) -> dict:
    if seed in PHASE_A_PR7_SEEDS:
        payload = json.loads((ROOT / "graded_reversion_phaseA_exploratory" / "seeds" / ("s%d.json" % seed)).read_text(encoding="utf-8"))
        targets = payload["targets"]
        hashes = payload["checkpoint_sha256"]
        checkpoint_dir = ROOT / "recurrent_core_results_v1" / "checkpoints"
    elif seed in PHASE_A_PR8_SEEDS:
        payload = json.loads((ROOT / "graded_reversion_results_v1" / "seeds" / ("s%d.json" % seed)).read_text(encoding="utf-8"))
        targets = payload["evaluation"]["targets"]
        hashes = payload["evaluation"]["checkpoint_sha256"]
        checkpoint_dir = ROOT / "graded_reversion_results_v1" / "checkpoints"
    else:
        raise ValueError(seed)
    curves = {target: targets[target]["delta_rev"] for target in TARGETS}
    return {"checkpoint_dir": checkpoint_dir, "hashes": hashes, "curves": curves}


def _span(records, key):
    values = []
    for record in records:
        geometry = record.get("geometry") or {}
        if geometry.get(key) is not None:
            values.append(float(geometry[key]))
    if not values:
        return None
    return min(values), max(values)


def _inside(span, bounds) -> bool:
    if span is None:
        return False
    return bool(bounds[0] <= span[0] and span[1] <= bounds[1])


def appendix_b_note(group_pr7, group_pr8) -> str:
    parts = [
        "The scratch files named in protocol Appendix B are not in this checkout. No per-seed draft finite-difference number is invented. Autograd inner products and cosines are listed per seed above.",
    ]
    for label, records in (("100-109", group_pr7), ("200-209", group_pr8)):
        bounds = _APPENDIX_RANGES[label]
        cos_span = _span(records, "cos_G_delta")
        dot_span = _span(records, "G_dot_delta")
        parts.append(
            "Seeds %s autograd cos span %s (printed range %s; inside=%s). Autograd inner-product span %s (printed range %s; inside=%s)."
            % (label, cos_span, bounds["cos"], _inside(cos_span, bounds["cos"]), dot_span, bounds["dot"], _inside(dot_span, bounds["dot"]))
        )
    return " ".join(parts)


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


def _load_seed(path: Path):
    if not path.exists():
        return None
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("code_version") != CODE_VERSION and record.get("evaluation", {}).get("code_version") != CODE_VERSION:
        raise SystemExit("existing seed file has a different code version: %s" % path)
    return record


def run_phase_a() -> None:
    manifest = load_freeze()
    fresh = all_manifests(tuple(PHASE_A_PR7_SEEDS) + tuple(PHASE_A_PR8_SEEDS))
    for key, item in fresh.items():
        stored = manifest["manifests"][key]
        if item["fo_sha256"] != stored["fo_sha256"] or item["iso_sha256"] != stored["iso_sha256"] or item["grad_sha256"] != stored["grad_sha256"]:
            _write_engineering(True, ["draw manifest mismatch for seed %s before any dose curve" % key])
            raise SystemExit("draw manifest does not match the freeze")
    configure_runtime()
    world = World()
    out = ROOT / PHASE_A_DIR
    seed_dir = out / "seeds"
    seed_dir.mkdir(parents=True, exist_ok=True)
    grouped = {"100-109": [], "200-209": []}
    issues = []
    for seed in tuple(PHASE_A_PR7_SEEDS) + tuple(PHASE_A_PR8_SEEDS):
        path = seed_dir / ("s%d.json" % seed)
        existing = _load_seed(path)
        if existing is not None and existing.get("code_version") == CODE_VERSION and "summary" in existing:
            record = existing
            print("phase A resume seed %d" % seed, flush=True)
        else:
            reference = _reference(seed)
            print("phase A evaluate seed %d" % seed, flush=True)
            record = evaluate_seed(
                seed,
                world,
                reference["checkpoint_dir"],
                reference["hashes"],
                manifest["manifests"][str(seed)],
                committed_delta_rev=reference["curves"],
                phase="A",
            )
            record["header"] = PHASE_A_PREFIX
            write_json(path, record)
        group = "100-109" if seed < 200 else "200-209"
        grouped[group].append(record)
        summary = (record.get("summary") or {}).get("weight_hh") or {}
        print(
            "phase A seed %d valid=%s D_FO=%s D_ISO=%s M=%s joint=%s"
            % (seed, record.get("valid"), summary.get("D_FO"), summary.get("D_ISO"), summary.get("M"), summary.get("joint")),
            flush=True,
        )
        for flag in record.get("engineering_flags") or []:
            issues.append("seed %s: %s" % (seed, flag))
    metadata = {
        "protocol_sha256": PROTOCOL_SHA256,
        "freeze_commit": git_head(),
        "appendix_b_note": appendix_b_note(grouped["100-109"], grouped["200-209"]),
    }
    document = {
        "header": PHASE_A_PREFIX,
        "development_only": True,
        "confirmatory": False,
        "pooled": False,
        "code_version": CODE_VERSION,
        "protocol_sha256": PROTOCOL_SHA256,
        "freeze_commit": metadata["freeze_commit"],
        "groups": {
            "seeds_100_109": grouped["100-109"],
            "seeds_200_209": grouped["200-209"],
        },
    }
    markdown = render_phase_a(grouped["100-109"], grouped["200-209"], metadata)
    write_json(out / "phase_a_results.json", document)
    (out / "PHASE_A_RESULTS.md").write_text(markdown, encoding="utf-8")
    blocking = len(issues) > 0
    _write_engineering(blocking, issues)
    if blocking:
        note = (
            "# Engineering note\n\n"
            "Phase A surfaced an engineering issue. It is not fixed here.\n\n"
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
    fresh = all_manifests(PHASE_B_SEEDS)
    for key, item in fresh.items():
        stored = manifest["manifests"][key]
        if item["fo_sha256"] != stored["fo_sha256"] or item["iso_sha256"] != stored["iso_sha256"] or item["grad_sha256"] != stored["grad_sha256"]:
            raise SystemExit("phase B draw manifest does not match the freeze for seed %s" % key)
    configure_runtime()
    world = World()
    out = ROOT / PHASE_B_DIR
    checkpoint_dir = out / "checkpoints"
    seed_dir = out / "seeds"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    seed_dir.mkdir(parents=True, exist_ok=True)
    phase_a = json.loads((ROOT / PHASE_A_DIR / "phase_a_results.json").read_text(encoding="utf-8"))
    freeze_commit = phase_a["freeze_commit"]
    inits = build_inits(PHASE_B_SEEDS)
    records = []
    for seed in PHASE_B_SEEDS:
        path = seed_dir / ("s%d.json" % seed)
        existing = _load_seed(path)
        if existing is not None and existing.get("complete") and existing.get("code_version") == CODE_VERSION:
            records.append(existing)
            print("phase B resume seed %d" % seed, flush=True)
            if (existing.get("evaluation") or {}).get("engineering_flags"):
                raise SystemExit("phase B engineering issue on resumed seed %d" % seed)
            continue
        print("phase B train seed %d" % seed, flush=True)
        trained = train_confirmation_seed(seed, world, inits[seed], checkpoint_dir)
        print("phase B seed %d trained ready=%s e1=%s" % (seed, trained["training_ready"], trained["e1_pass"]), flush=True)
        if not trained["training_ready"]:
            evaluation = missing_evaluation(seed, ["training"])
        else:
            evaluation = evaluate_seed(
                seed,
                world,
                checkpoint_dir,
                trained["expected_hashes"],
                manifest["manifests"][str(seed)],
                committed_delta_rev=None,
                phase="B",
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
        summary = (evaluation.get("summary") or {}).get("weight_hh") or {}
        print(
            "phase B seed %d valid=%s D_FO=%s D_ISO=%s M=%s joint=%s"
            % (seed, evaluation.get("valid"), summary.get("D_FO"), summary.get("D_ISO"), summary.get("M"), summary.get("joint")),
            flush=True,
        )
        if evaluation.get("engineering_flags"):
            note = (
                "# Engineering note\n\nPhase B evaluation surfaced an engineering issue on seed %d. "
                "The code is not changed.\n\n%s\n"
                % (seed, "\n".join("- %s" % flag for flag in evaluation["engineering_flags"]))
            )
            (out / "ENGINEERING_NOTE.md").write_text(note, encoding="utf-8")
            raise SystemExit("phase B engineering issue on seed %d" % seed)
    e1_flags = [bool(record["e1_pass"]) for record in records]
    valid_flags = [bool(record["evaluation"]["valid"]) for record in records]
    collapsed_flags = [bool(record["evaluation"].get("primary_collapsed")) for record in records]
    joint_flags = [bool((record["evaluation"].get("summary") or {}).get("weight_hh", {}).get("joint")) for record in records]
    label = primary_label(e1_flags, valid_flags, collapsed_flags, joint_flags)
    paragraph = verdict_paragraph(label)
    metadata = {
        "protocol_sha256": PROTOCOL_SHA256,
        "freeze_commit": freeze_commit,
        "phase_a_dir": PHASE_A_DIR,
    }
    document = {
        "header": "PHASE B confirmation seeds 300-309. Not pooled with phase A.",
        "code_version": CODE_VERSION,
        "protocol_sha256": PROTOCOL_SHA256,
        "freeze_commit": freeze_commit,
        "phase_a_commit_at_training": git_head(),
        "label": label,
        "verdict_paragraph": paragraph,
        "pooled_with_phase_a": False,
        "seeds": records,
    }
    markdown = render_phase_b(records, metadata)
    write_json(out / "phase_b_results.json", document)
    (out / "PHASE_B_RESULTS.md").write_text(markdown, encoding="utf-8")
    print("phase B complete", flush=True)
    print(label, flush=True)
    print(paragraph, flush=True)


def main(argv: list[str]) -> None:
    if len(argv) != 2:
        raise SystemExit("usage: first_order_control_study.py [write-freeze|phase-a|phase-b]")
    command = argv[1]
    if command == "write-freeze":
        write_freeze()
    elif command == "phase-a":
        run_phase_a()
    elif command == "phase-b":
        run_phase_b()
    else:
        raise SystemExit("unknown command %s" % command)


if __name__ == "__main__":
    main(sys.argv)
