"""Run the frozen two-stream acquisition study and write its report.

``--freeze-only`` writes TWOSTREAM_ACQUISITION_FREEZE_v1.json and does not train.
The default command runs the 120-run study and must be used only after the
freeze commit.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
import torch

from twostream_acquisition_metrics import _empty_suite, full_analysis, reference_arm_report
from twostream_acquisition_models import build_model, snapshot_state
from twostream_acquisition_oracle import RESULTS_PATH, load_world
from twostream_acquisition_spec import (
    BATCH,
    B_GRID,
    DEVIATIONS,
    E2_RATIO,
    PROTOCOL_SHA256,
    RATIO_TIE,
    SEEDS,
    SHOWN_MIN,
    STEPS,
    Spec,
    iter_specs,
)
from twostream_acquisition_train import train_model
from twostream_acquisition_verdicts import (
    assemble_claim,
    e1_label,
    e2_label,
    e3_label,
    e3_qualifier,
    observation_labels,
    study_verdict,
)

ROOT = Path(__file__).resolve().parent
FREEZE_PATH = ROOT / "TWOSTREAM_ACQUISITION_FREEZE_v1.json"
RESULTS_DIR = ROOT / "acquisition_results_v1"
CODE_FILES = (
    "TWOSTREAM_ACQUISITION_PROTOCOL_v1.md",
    "twostream_acquisition_spec.py",
    "twostream_acquisition_oracle.py",
    "twostream_acquisition_verdicts.py",
    "twostream_acquisition_models.py",
    "twostream_acquisition_train.py",
    "twostream_acquisition_metrics.py",
    "twostream_acquisition_study.py",
    "test_twostream_acquisition.py",
)
ORACLE_FILES = (
    "twostream_results_v1/results.json",
    "twostream_filter.py",
    "twostream_chart.py",
    "twostream_constants.py",
    "twostream_score.py",
    "twostream_moments.py",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def environment_record() -> dict:
    return {
        "python": sys.version,
        "torch": torch.__version__,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "threads": 1,
        "device": "cpu",
    }


def freeze_document() -> dict:
    protocol_hash = sha256_file(ROOT / "TWOSTREAM_ACQUISITION_PROTOCOL_v1.md")
    if protocol_hash != PROTOCOL_SHA256:
        raise SystemExit("protocol hash %s does not match the reviewed file" % protocol_hash)
    world = load_world()
    return {
        "study": "two-stream acquisition v1",
        "status": "FREEZE. No training run is part of this file.",
        "protocol_sha256": protocol_hash,
        "code_sha256": {name: sha256_file(ROOT / name) for name in CODE_FILES},
        "oracle_sha256": {name: sha256_file(ROOT / name) for name in ORACLE_FILES},
        "results_json": str(RESULTS_PATH.relative_to(ROOT)),
        "held_out_references": world.reference_export(),
        "seeds": list(SEEDS),
        "sampler_seed": "1000+s",
        "sham_seed": "7000+s",
        "torch_seed": "s",
        "steps": STEPS,
        "batch": BATCH,
        "episodes": STEPS * BATCH,
        "configurations": [spec.configuration() + " seed %d" % spec.seed for spec in iter_specs()],
        "n_runs": sum(1 for _spec in iter_specs()),
        "b_grid": list(B_GRID),
        "implementation_clarifications": list(DEVIATIONS),
        "environment": environment_record(),
    }


def write_freeze() -> None:
    document = freeze_document()
    FREEZE_PATH.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print("wrote %s (%d runs recorded, no training)" % (FREEZE_PATH.name, document["n_runs"]), flush=True)


def configure_runtime() -> None:
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def execute(spec: Spec, world, steps: int = STEPS) -> dict:
    torch.manual_seed(spec.seed)
    model = build_model(spec)
    init_state = snapshot_state(model)
    from twostream_acquisition_metrics import predict_only

    init_eval = predict_only(model, world)
    train_info = train_model(model, spec, steps=steps, batch=BATCH)
    train_info = dict(train_info)
    train_info["budget_steps"] = steps
    train_info["batch"] = BATCH
    if not train_info["integrity_training"]:
        return _failed_training_record(spec, init_eval, train_info)
    record = full_analysis(model, spec, world, init_state, init_eval, train_info)
    record["budget_steps"] = steps
    return record


def _failed_training_record(spec, init_eval, train_info) -> dict:
    return {
        "arm": spec.arm,
        "cell": spec.cell,
        "hidden": spec.hidden,
        "seed": spec.seed,
        "configuration": spec.configuration(),
        "freeze_recurrent": spec.freeze_recurrent,
        "training": train_info,
        "init": {
            "errors": init_eval["errors"],
            "afit_test": init_eval["afit_test"],
            "afit_train": init_eval["afit_train"],
            "outputs_valid": init_eval["outputs_valid"],
        },
        "final": {"errors": None, "afit_test": False, "afit_train": False, "outputs_valid": False},
        "change": None,
        "alearn": (not init_eval["afit_test"]),
        "integrity": False,
        "identity": {"ok": False},
        "recurrent_change": None,
        "geometry_correlation": None,
        "precision": {"applicable": False, "b_sel": None, "confirmation": "NOT CONFIRMED"},
        "ledger": {},
        "interventions": _empty_suite("training integrity failure"),
        "chart_probe": {"applicable": False, "accessible": False},
        "complete": True,
        "budget_steps": train_info["budget_steps"],
    }


def to_jsonable(value):
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return to_jsonable(value.tolist())
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, (np.floating, float)):
        number = float(value)
        if not np.isfinite(number):
            return None
        return number
    return value


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(to_jsonable(payload), indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def run_study() -> None:
    if not FREEZE_PATH.exists():
        raise SystemExit("freeze file is missing; refuse to train")
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    if freeze.get("protocol_sha256") != PROTOCOL_SHA256:
        raise SystemExit("freeze protocol hash does not match the reviewed protocol")
    configure_runtime()
    world = load_world()
    run_dir = RESULTS_DIR / "runs"
    run_dir.mkdir(parents=True, exist_ok=True)
    specs = list(iter_specs())
    if len(specs) != 120:
        raise SystemExit("spec count %d" % len(specs))
    for index, spec in enumerate(specs, start=1):
        path = run_dir / ("%s.json" % spec.file_stem())
        if path.exists():
            print("skip %s" % path.name, flush=True)
            continue
        print("run %d/120 %s" % (index, spec.configuration()), flush=True)
        record = execute(spec, world, STEPS)
        _write_json(path, record)
        final = record["final"]["errors"]
        total = None if not final else final["TEST"]["total"]
        print(
            "done %s integrity=%s E_total(TEST)=%s"
            % (path.name, record["integrity"], total),
            flush=True,
        )
    records = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(run_dir.glob("*.json"))]
    references = reference_arm_report(world)
    _write_json(RESULTS_DIR / "reference_arms.json", references)
    summary = summarize(records, references)
    _write_json(RESULTS_DIR / "summary.json", summary)
    (RESULTS_DIR / "RESULTS.md").write_text(render_markdown(records, references, summary), encoding="utf-8")
    print("verdict %s E1 %s E2 %s E3 %s" % (summary["study"], summary["e1"], summary["e2"], summary["e3"]), flush=True)


def _match(records, arm, cell, hidden, seed):
    for record in records:
        if (
            record["arm"] == arm
            and record["cell"] == cell
            and record["hidden"] == hidden
            and record["seed"] == seed
        ):
            return record
    return None


def _missing(spec: Spec) -> dict:
    return {
        "arm": spec.arm,
        "cell": spec.cell,
        "hidden": spec.hidden,
        "seed": spec.seed,
        "configuration": spec.configuration(),
        "freeze_recurrent": spec.freeze_recurrent,
        "final": {"errors": None, "afit_test": False, "afit_train": False, "outputs_valid": False},
        "init": {"errors": None, "afit_test": False, "afit_train": False, "outputs_valid": False},
        "change": None,
        "alearn": False,
        "integrity": False,
        "interventions": _empty_suite("UNRESOLVED: run missing"),
        "chart_probe": {"applicable": False, "accessible": False},
        "precision": {"b_sel": None, "confirmation": "NOT CONFIRMED", "curve": []},
        "complete": False,
        "missing": True,
    }


def _records_by_spec(records):
    found = []
    for spec in iter_specs():
        record = _match(records, spec.arm, spec.cell, spec.hidden, spec.seed)
        found.append(record if record is not None else _missing(spec))
    return found


def _err(record, phase, split, key):
    block = record.get(phase) or {}
    errors = block.get("errors")
    if not errors:
        return None
    return errors[split][key]


def summarize(records, references) -> dict:
    rows = _records_by_spec(records)
    primary = [row for row in rows if row["arm"] == "CAND" and row["cell"] == "gru" and row["hidden"] == 8]
    frozen = [row for row in rows if row["arm"] == "K-FR" and row["cell"] == "gru" and row["hidden"] == 8]
    e1_rows = [
        {"afit": bool(row["final"]["afit_test"]), "alearn": bool(row["alearn"]), "integrity": bool(row["integrity"])}
        for row in primary
    ]
    e2_rows = []
    pair_details = []
    for cand, kfr in zip(primary, frozen):
        cand_total = _err(cand, "final", "TEST", "total")
        kfr_total = _err(kfr, "final", "TEST", "total")
        cand_xor = _err(cand, "final", "TEST", "XOR")
        kfr_xor = _err(kfr, "final", "TEST", "XOR")
        tie = kfr_total is not None and kfr_total <= RATIO_TIE
        intact = bool(cand["integrity"] and kfr["integrity"])
        ratio = None
        if kfr_total is not None and not tie and kfr_total != 0:
            ratio = cand_total / kfr_total
        xor_tie = kfr_xor is not None and kfr_xor <= RATIO_TIE
        xor_ratio = None if kfr_xor is None or xor_tie or kfr_xor == 0 else cand_xor / kfr_xor
        e2_rows.append(
            {
                "intact": intact,
                "tie": bool(tie or kfr_total is None),
                "ratio_le_half": bool(ratio is not None and ratio <= E2_RATIO),
                "kfr_afit": bool(kfr["final"]["afit_test"]),
            }
        )
        pair_details.append(
            {
                "seed": cand["seed"],
                "intact": intact,
                "tie": bool(tie),
                "ratio_total": ratio,
                "ratio_xor": xor_ratio,
                "xor_tie": bool(xor_tie),
                "cand_total": cand_total,
                "kfr_total": kfr_total,
                "cand_xor": cand_xor,
                "kfr_xor": kfr_xor,
                "difference_total": None if cand_total is None or kfr_total is None else cand_total - kfr_total,
                "difference_xor": None if cand_xor is None or kfr_xor is None else cand_xor - kfr_xor,
            }
        )
    def e3_rows(group):
        packed = []
        for row in group:
            intervention = row.get("interventions") or {}
            packed.append(
                {
                    "localized": bool(intervention.get("localized")) and bool(row["integrity"]),
                    "coverage_ok": bool(intervention.get("coverage_ok")),
                    "rank_ok": bool(intervention.get("rank_ok")),
                }
            )
        return packed

    e1 = e1_label(e1_rows)
    e2 = e2_label(e2_rows)
    cand_e3 = e3_rows(primary)
    kfr_e3 = e3_rows(frozen)
    e3 = e3_label(cand_e3)
    qualifier = e3_qualifier(kfr_e3) if e3 == "LOCALIZED BY THE CHART-DECODER INTERVENTION" else False
    integrity_count = sum(1 for row in primary if row["integrity"])
    verdict = study_verdict(e1, integrity_count)
    facts = _label_facts(rows)
    labels = observation_labels(facts)
    claim = assemble_claim(verdict, e2, e3, qualifier, labels)
    return {
        "e1": e1,
        "e2": e2,
        "e3": e3,
        "e3_qualifier": qualifier,
        "kfr_e3": e3_label(kfr_e3),
        "study": verdict,
        "integrity_count_gru8_cand": integrity_count,
        "claim": claim,
        "literal_labels": labels,
        "label_facts": facts,
        "e1_rows": e1_rows,
        "e2_rows": e2_rows,
        "pairs": pair_details,
        "e3_cand": cand_e3,
        "e3_kfr": kfr_e3,
        "medians": _medians(rows),
        "missing_runs": [row["configuration"] + " s%d" % row["seed"] for row in rows if row.get("missing")],
        "reference_afit_test": {name: references[name]["afit_test"] for name in ("K-EXACT", "K-PROD*", "K-CUR")},
        "freeze_commit": _git_head(),
    }


def _label_facts(rows) -> dict:
    def afit_count(arm, cell, hidden):
        return sum(
            1
            for row in rows
            if row["arm"] == arm and row["cell"] == cell and row["hidden"] == hidden and row["final"]["afit_test"]
        )

    weak = 0
    accessible = 0
    for seed in SEEDS:
        cand = _match(rows, "CAND", "gru", 8, seed)
        table = _match(rows, "K-TAB", "table", 0, seed)
        cand_xor = _err(cand, "final", "TEST", "XOR") if cand else None
        table_xor = _err(table, "final", "TEST", "XOR") if table else None
        cand_test = _err(cand, "final", "TEST", "total") if cand else None
        cand_train = _err(cand, "final", "TRAIN", "total") if cand else None
        xor_clause = (
            cand_xor is not None and table_xor is not None and cand_xor >= 0.5 * table_xor
        )
        train_clause = cand_test is not None and cand_train is not None and cand_test >= 4.0 * cand_train
        if xor_clause or train_clause:
            weak += 1
        probe = (cand or {}).get("chart_probe") or {}
        if probe.get("accessible"):
            accessible += 1
    return {
        "k2d_afit_at_least_8": afit_count("K-2D", "gru", 2) >= SHOWN_MIN,
        "k2dmlp_afit_at_least_8": afit_count("K-2D-MLP", "mlp", 2) >= SHOWN_MIN,
        "kfr_afit_at_least_8": afit_count("K-FR", "gru", 8) >= SHOWN_MIN,
        "generalization_weak": weak >= SHOWN_MIN,
        "chart_accessible": accessible >= SHOWN_MIN,
        "k2d_afit_count": afit_count("K-2D", "gru", 2),
        "k2dmlp_afit_count": afit_count("K-2D-MLP", "mlp", 2),
        "kfr_afit_count": afit_count("K-FR", "gru", 8),
        "weak_count": weak,
        "accessible_count": accessible,
    }


def _median_range(values):
    clean = sorted(value for value in values if value is not None and np.isfinite(value))
    if not clean:
        return {"median": None, "min": None, "max": None, "n": 0}
    n = len(clean)
    if n % 2:
        median = clean[n // 2]
    else:
        median = 0.5 * (clean[n // 2 - 1] + clean[n // 2])
    return {"median": median, "min": clean[0], "max": clean[-1], "n": n}


def _medians(rows) -> dict:
    out = {}
    for row in rows:
        key = "%s|%s|%s" % (row["arm"], row["cell"], row["hidden"])
        out.setdefault(key, []).append(_err(row, "final", "TEST", "total"))
    return {key: _median_range(values) for key, values in out.items()}


def _git_head() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def _fmt(value) -> str:
    if value is None:
        return "NA"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not np.isfinite(number):
        return "NA"
    return "%.8g" % number


def _metric_table(rows) -> str:
    lines = [
        "| configuration | seed | phase | split | E_X | E_Y | E_XOR | E_total |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        for phase in ("init", "final"):
            for split in ("TRAIN", "TEST"):
                lines.append(
                    "| %s | %d | %s | %s | %s | %s | %s | %s |"
                    % (
                        row["configuration"],
                        row["seed"],
                        phase,
                        split,
                        _fmt(_err(row, phase, split, "X")),
                        _fmt(_err(row, phase, split, "Y")),
                        _fmt(_err(row, phase, split, "XOR")),
                        _fmt(_err(row, phase, split, "total")),
                    )
                )
    return "\n".join(lines)


def _change_table(rows) -> str:
    lines = [
        "| configuration | seed | split | dE_X | dE_Y | dE_XOR | dE_total |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        change = row.get("change") or {}
        for split in ("TRAIN", "TEST"):
            block = change.get(split) or {}
            lines.append(
                "| %s | %d | %s | %s | %s | %s | %s |"
                % (
                    row["configuration"],
                    row["seed"],
                    split,
                    _fmt(block.get("X")),
                    _fmt(block.get("Y")),
                    _fmt(block.get("XOR")),
                    _fmt(block.get("total")),
                )
            )
    return "\n".join(lines)


def _precision_table(rows) -> str:
    header = "| configuration | seed | b_sel | confirmation | " + " | ".join("b=%d E_total" % b for b in B_GRID) + " |"
    rule = "| --- | --- | --- | --- | " + " | ".join("---" for _ in B_GRID) + " |"
    lines = [header, rule]
    for row in rows:
        precision = row.get("precision") or {}
        curve = {entry["b"]: entry for entry in precision.get("curve") or []}
        cells = []
        for bits in B_GRID:
            entry = curve.get(bits)
            if not entry or not entry.get("errors"):
                cells.append("NA")
            else:
                cells.append(_fmt(entry["errors"]["TEST"]["total"]))
        lines.append(
            "| %s | %d | %s | %s | %s |"
            % (
                row["configuration"],
                row["seed"],
                precision.get("b_sel"),
                precision.get("confirmation"),
                " | ".join(cells),
            )
        )
    return "\n".join(lines)


def _error_line(summary) -> str:
    if not summary:
        return "NA"
    return "L2sq=%s abs=%s norm=%s below_tau=%s" % (
        _fmt(summary.get("squared_l2_mean")),
        _fmt(summary.get("absolute_summed_mean")),
        _fmt(summary.get("normalized_summed_mean")),
        summary.get("n_below_tau"),
    )


def _intervention_section(rows) -> str:
    lines = []
    for row in rows:
        intervention = row.get("interventions") or {}
        ratios = intervention.get("ratios") or {}
        errors = intervention.get("errors") or {}
        lines.append("### %s seed %d" % (row["configuration"], row["seed"]))
        lines.append("")
        lines.append(
            "- applicable: %s; descriptive_only: %s; localized: %s; coverage_ok: %s; rank_ok: %s"
            % (
                intervention.get("applicable"),
                intervention.get("descriptive_only"),
                intervention.get("localized"),
                intervention.get("coverage_ok"),
                intervention.get("rank_ok"),
            )
        )
        coverage = intervention.get("coverage") or {}
        if coverage:
            lines.append(
                "- coverage fraction %s (%s/%s); dropped for no wrong donor: %s"
                % (
                    _fmt(coverage.get("fraction")),
                    coverage.get("n_eligible"),
                    coverage.get("n_cross_fitted"),
                    intervention.get("n_dropped_no_wrong_donor"),
                )
            )
        for name in ("partial", "complement", "wrong"):
            ratio = ratios.get(name) or {}
            lines.append(
                "- %s rho vector %s, rho XOR %s; %s"
                % (name, _fmt(ratio.get("vector")), _fmt(ratio.get("xor")), _error_line(errors.get(name)))
            )
        nearest = intervention.get("nearest_posterior") or {}
        if nearest:
            lines.append("- nearest whole: %s" % _error_line(nearest.get("whole")))
            lines.append("- nearest partial: %s" % _error_line(nearest.get("partial")))
        tracking = intervention.get("donor_tracking") or {}
        if tracking:
            lines.append(
                "- whole-state donor-tracking rho vector %s, XOR %s"
                % (_fmt(tracking.get("vector")), _fmt(tracking.get("xor")))
            )
        lines.append("")
    return "\n".join(lines)


def render_markdown(records, references, summary) -> str:
    rows = _records_by_spec(records)
    lines = []
    lines.append("# Two-stream acquisition results v1")
    lines.append("")
    lines.append("One study run after the freeze commit. Thresholds, seeds, the split, the budget, the arms, and the claim wording are the protocol's.")
    lines.append("")
    lines.append("- Study verdict: **%s**" % summary["study"])
    lines.append("- E1 (GRU-8 predictive acquisition): **%s**" % summary["e1"])
    lines.append("- E2 (GRU-8 recurrent adaptation): **%s**" % summary["e2"])
    lines.append("- E3 (GRU-8 chart-decoder intervention): **%s**" % summary["e3"])
    lines.append("- E3 qualifier applied: %s" % ("yes" if summary["e3_qualifier"] else "no"))
    lines.append("- K-FR E3 label: **%s**" % summary["kfr_e3"])
    lines.append("- GRU-8 CAND integrity count: %d/10" % summary["integrity_count_gru8_cand"])
    lines.append("- Freeze commit: `%s`" % summary["freeze_commit"])
    lines.append("")
    lines.append("## Claim ceiling")
    lines.append("")
    lines.append(summary["claim"])
    lines.append("")
    lines.append("Literal observation labels whose conditions hold: %s." % (
        ", ".join(summary["literal_labels"]) if summary["literal_labels"] else "none"
    ))
    lines.append("")
    lines.append("Not established by this study: where a localized subspace came from; an independently manipulable natural module; irreducible joint state; marginal-filter or mean-field identification; C4; consciousness; organism claims. A probe is not identification of the candidate's mechanism.")
    lines.append("")
    lines.append("## Literal observation counts")
    lines.append("")
    facts = summary["label_facts"]
    lines.append("- K-2D A-FIT seeds: %d/10" % facts["k2d_afit_count"])
    lines.append("- K-2D-MLP A-FIT seeds: %d/10" % facts["k2dmlp_afit_count"])
    lines.append("- K-FR GRU-8 A-FIT seeds: %d/10" % facts["kfr_afit_count"])
    lines.append("- Held-out generalization weak seeds: %d/10" % facts["weak_count"])
    lines.append("- Chart linearly accessible seeds: %d/10" % facts["accessible_count"])
    lines.append("")
    lines.append("## Paired GRU-8 CAND and K-FR")
    lines.append("")
    lines.append("| seed | intact | tie | ratio_total | ratio_XOR | CAND total | K-FR total | CAND − K-FR total | CAND XOR | K-FR XOR |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for pair in summary["pairs"]:
        lines.append(
            "| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
            % (
                pair["seed"],
                pair["intact"],
                pair["tie"],
                _fmt(pair["ratio_total"]),
                _fmt(pair["ratio_xor"]),
                _fmt(pair["cand_total"]),
                _fmt(pair["kfr_total"]),
                _fmt(pair["difference_total"]),
                _fmt(pair["cand_xor"]),
                _fmt(pair["kfr_xor"]),
            )
        )
    lines.append("")
    lines.append("## Median and range of final TEST E_total")
    lines.append("")
    lines.append("| arm | median | min | max | n |")
    lines.append("| --- | --- | --- | --- | --- |")
    for key in sorted(summary["medians"]):
        stats = summary["medians"][key]
        lines.append("| %s | %s | %s | %s | %d |" % (key, _fmt(stats["median"]), _fmt(stats["min"]), _fmt(stats["max"]), stats["n"]))
    lines.append("")
    lines.append("## Per-seed continuous metrics")
    lines.append("")
    lines.append(_metric_table(rows))
    lines.append("")
    lines.append("## Change from initialization to final")
    lines.append("")
    lines.append(_change_table(rows))
    lines.append("")
    lines.append("## Recurrent weight change and stage-4 geometry correlation")
    lines.append("")
    lines.append("| configuration | seed | relative weight change | absolute weight change | geometry correlation |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in rows:
        change = row.get("recurrent_change") or {}
        lines.append(
            "| %s | %d | %s | %s | %s |"
            % (
                row["configuration"],
                row["seed"],
                _fmt(change.get("relative")),
                _fmt(change.get("absolute")),
                _fmt(row.get("geometry_correlation")),
            )
        )
    lines.append("")
    lines.append("## Precision curves")
    lines.append("")
    lines.append("b_sel is the smallest grid precision at which TRAIN meets A-FIT. Confirmation is A-FIT on TEST at that precision. Curve entries are TEST E_total at each b and are descriptive.")
    lines.append("")
    lines.append(_precision_table(rows))
    lines.append("")
    lines.append("## Absolute and normalized intervention errors")
    lines.append("")
    lines.append("Ratios are sums over the common eligible trial subset. Squared L2 is the mean of ||(F' − F(a)) − Delta-star||^2. Absolute and normalized figures follow the prespecified rule: per-query absolute deviations are summed, and the normalized value divides by ||Delta-star||_2 only when that norm is at least 1/100.")
    lines.append("")
    lines.append(_intervention_section(rows))
    lines.append("## Reference arms")
    lines.append("")
    lines.append("| arm | split | E_X | E_Y | E_XOR | E_total | A-FIT |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for name in ("K-EXACT", "K-PROD*", "K-CUR"):
        for split in ("TRAIN", "TEST"):
            errors = references[name]["errors"][split]
            afit = references[name]["afit_test"] if split == "TEST" else references[name]["afit_train"]
            lines.append(
                "| %s | %s | %s | %s | %s | %s | %s |"
                % (name, split, _fmt(errors["X"]), _fmt(errors["Y"]), _fmt(errors["XOR"]), _fmt(errors["total"]), afit)
            )
    exact = references["K-EXACT"].get("precision") or {}
    lines.append("")
    lines.append("K-EXACT b_sel: %s. Confirmation: %s." % (exact.get("b_sel"), exact.get("confirmation")))
    lines.append("")
    lines.append("## DEVIATIONS")
    lines.append("")
    lines.append("Readings chosen before training, because the protocol left an implementation detail unspecified. No threshold, seed, split, budget, arm, or claim wording was changed.")
    lines.append("")
    for item in DEVIATIONS:
        lines.append("- %s" % item)
    if summary["missing_runs"]:
        lines.append("- UNRESOLVED cells that were not run: %s." % ", ".join(summary["missing_runs"]))
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> None:
    if "--freeze-only" in argv:
        write_freeze()
        return
    run_study()


if __name__ == "__main__":
    main(sys.argv[1:])
