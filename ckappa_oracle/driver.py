"""Run the oracle package. Step 0 may begin only when manifest.json is sealed."""

from __future__ import annotations

import json
import traceback
from pathlib import Path

from ckappa_oracle.draws import draw_arrays
from ckappa_oracle.inputs import load_inputs
from ckappa_oracle.io import INTEGRITY_STOP_KIND, PackageStop, atomic_write_json, atomic_write_text
from ckappa_oracle.pinned import NUMPY, PYTHON
from ckappa_oracle.preflight import preflight
from ckappa_oracle.report import render
from ckappa_oracle.runstate import Run, write_stop
from ckappa_oracle.stages import _embed, stage_o1, stage_o2, stage_o3, stage_o4, stage_o5, stage_o6, stage_o7
from ckappa_oracle import world

ROOT = Path(__file__).resolve().parents[1]


def _package_section5(o6_section5, kind: str, detail: dict):
    """PIPELINE INVALID is an N1 label. Other stop kinds do not replace the O6 label."""
    if kind == INTEGRITY_STOP_KIND:
        return None
    if kind == "PIPELINE INVALID":
        return {
            "label": "PIPELINE INVALID",
            "reason": detail.get("reason", "fixture failure"),
            "detail": detail,
            "o6_outcome": o6_section5,
        }
    return o6_section5


def _results_body(run: Run, kind: str, exit_code: int, detail: dict, section5, o6_section5) -> dict:
    return {
        "package": "ckappa-oracle",
        "phase": "unsealed-implementation",
        "stop_kind": kind,
        "exit_code": exit_code,
        "detail": detail,
        "t0": run.t0,
        "t_elapsed_s": run.elapsed(),
        "versions": {"python": PYTHON, "numpy": NUMPY},
        "drawn_arrays": run.drawn_records,
        "float_propagations": run.float_count,
        "exact_propagations": run.exact_count,
        "bucket": dict(run.bucket),
        "projection": run.projection,
        "sample_n": run.sample_n,
        "t_sample_s": run.sample_seconds,
        "T_O1_s": run.t_o1,
        "n_O1": run.n_o1,
        "retained_o6_sample": run.retained,
        "stages_completed": list(run.completed),
        "stages": run.stages,
        "section5": section5,
        "o6_section5": o6_section5,
        "oracle_edit_field": "eps_syn",
    }


def _text_stop(root: Path, kind: str, exit_code: int) -> None:
    outputs = root / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    text = json.dumps({"exit_code": exit_code, "stop_kind": kind}, indent=2, sort_keys=True) + "\n"
    atomic_write_text(outputs / "stop_kind.json", text)


def _text_results(root: Path, kind: str, exit_code: int) -> None:
    outputs = root / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    payload = {
        "exit_code": exit_code,
        "oracle_edit_field": "eps_syn",
        "package": "ckappa-oracle",
        "phase": "unsealed-implementation",
        "section5": None,
        "stop_kind": kind,
        "writer": "fallback-text",
    }
    atomic_write_text(outputs / "results.json", json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _fallback_outputs(root: Path, kind: str, exit_code: int, detail: dict, section5) -> None:
    outputs = root / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    safe_detail = {}
    if isinstance(detail, dict):
        for key, value in detail.items():
            safe_detail[str(key)] = value if isinstance(value, (str, int, float, bool)) or value is None else str(value)
    minimal = {
        "package": "ckappa-oracle",
        "phase": "unsealed-implementation",
        "stop_kind": kind,
        "exit_code": exit_code,
        "detail": safe_detail,
        "section5": section5 if kind == "PIPELINE INVALID" else None,
        "oracle_edit_field": "eps_syn",
        "writer": "fallback",
    }
    try:
        atomic_write_json(outputs / "results.json", minimal)
    except Exception:
        _text_results(root, kind, exit_code)
    try:
        write_stop(root, kind, exit_code)
    except Exception:
        _text_stop(root, kind, exit_code)


def write_stop_pair(root: Path, kind: str, exit_code: int, detail: dict, section5) -> None:
    """Write results.json and stop_kind.json. Used before a Run exists."""
    outputs = root / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    results = {
        "package": "ckappa-oracle",
        "phase": "unsealed-implementation",
        "stop_kind": kind,
        "exit_code": exit_code,
        "detail": detail,
        "stages_completed": [],
        "section5": section5,
        "o6_section5": None,
        "oracle_edit_field": "eps_syn",
    }
    try:
        atomic_write_json(outputs / "results.json", results)
        atomic_write_text(outputs / "REPORT.md", render(results))
        atomic_write_text(outputs / "run.log", f"0.000000 {kind} {detail}\n")
        write_stop(root, kind, exit_code)
    except Exception:
        _fallback_outputs(root, kind, exit_code, detail if isinstance(detail, dict) else {"reason": str(detail)}, section5)


def _write_outputs(run: Run, kind: str, exit_code: int, detail: dict, section5, o6_section5) -> None:
    try:
        results = _results_body(run, kind, exit_code, detail, section5, o6_section5)
        run.write_json("outputs/results.json", results)
        atomic_write_text(run.outputs / "REPORT.md", render(results))
        write_stop(run.root, kind, exit_code)
        run.log(f"stop {kind} exit {exit_code}")
    except Exception:
        _fallback_outputs(run.root, kind, exit_code, detail, section5)


def main() -> int:
    run = None
    o6_section5 = None
    try:
        try:
            t0, _manifest = preflight(ROOT)
        except PackageStop as exc:
            write_stop_pair(ROOT, exc.kind, exc.exit_code, exc.detail, None)
            return exc.exit_code
        try:
            run = Run(ROOT, t0, ROOT / "outputs" / "run.log")
        except Exception as exc:
            detail = {"reason": "uncaught exception", "error": str(exc), "traceback": traceback.format_exc()}
            write_stop_pair(ROOT, "EXECUTION ERROR", 1, detail, None)
            return 1
        run.log("preflight passed; sealed manifest loaded")
        run.check_deadline("draws")
        draws = draw_arrays(ROOT)
        run.drawn_records = draws["records"]
        run.log("draws hashed")
        stored = load_inputs(ROOT)
        run.log("inputs hashed")
        run.transition = world.column_transition_float()
        ctx = stage_o1(run, stored["by_history"])
        _embed(ctx, draws)
        stage_o2(run, ctx)
        o6_section5 = stage_o6(run, ctx, draws)
        if not run.sample_closed:
            raise PackageStop(
                "STEP 0 SAMPLE SHORT",
                6,
                {"sample_n": run.sample_n, "required": 1000},
            )
        stage_o7(run, ctx, draws)
        stage_o3(run, ctx)
        stage_o4(run, ctx, draws)
        stage_o5(run, ctx, draws)
        _write_outputs(run, "COMPLETED", 0, {}, o6_section5, o6_section5)
        return 0
    except PackageStop as exc:
        section5 = _package_section5(o6_section5, exc.kind, exc.detail)
        if run is None:
            write_stop_pair(ROOT, exc.kind, exc.exit_code, exc.detail, section5)
        else:
            _write_outputs(run, exc.kind, exc.exit_code, exc.detail, section5, o6_section5)
        return exc.exit_code
    except Exception as exc:
        detail = {"reason": "uncaught exception", "error": str(exc), "traceback": traceback.format_exc()}
        section5 = _package_section5(o6_section5, "EXECUTION ERROR", detail)
        if run is None:
            write_stop_pair(ROOT, "EXECUTION ERROR", 1, detail, section5)
        else:
            _write_outputs(run, "EXECUTION ERROR", 1, detail, section5, o6_section5)
        return 1
    finally:
        if run is not None:
            try:
                run.close()
            except Exception:
                pass
