"""Run the oracle package. Step 0 may begin only when manifest.json is sealed."""

from __future__ import annotations

import traceback
from pathlib import Path

from ckappa_oracle.draws import draw_arrays
from ckappa_oracle.inputs import load_inputs
from ckappa_oracle.io import PackageStop, atomic_write_json, atomic_write_text
from ckappa_oracle.pinned import NUMPY, PYTHON
from ckappa_oracle.preflight import preflight
from ckappa_oracle.report import render
from ckappa_oracle.runstate import Run, write_stop
from ckappa_oracle.stages import _embed, stage_o1, stage_o2, stage_o3, stage_o4, stage_o5, stage_o6, stage_o7
from ckappa_oracle import world

ROOT = Path(__file__).resolve().parents[1]


def _write_outputs(run: Run, kind: str, exit_code: int, detail: dict, section5) -> None:
    results = {
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
        "oracle_edit_field": "eps_syn",
    }
    run.write_json("outputs/results.json", results)
    atomic_write_text(run.outputs / "REPORT.md", render(results))
    write_stop(run.root, kind, exit_code)
    run.log(f"stop {kind} exit {exit_code}")


def _preflight_outputs(exc: PackageStop) -> None:
    outputs = ROOT / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    results = {
        "package": "ckappa-oracle",
        "phase": "unsealed-implementation",
        "stop_kind": exc.kind,
        "exit_code": exc.exit_code,
        "detail": exc.detail,
        "stages_completed": [],
        "section5": None,
        "oracle_edit_field": "eps_syn",
    }
    atomic_write_json(outputs / "results.json", results)
    atomic_write_text(outputs / "REPORT.md", render(results))
    atomic_write_text(outputs / "run.log", f"0.000000 {exc.kind} {exc.detail}\n")
    write_stop(ROOT, exc.kind, exc.exit_code)


def _package_section5(o6_section5, kind: str, detail: dict):
    if kind == "COMPLETED":
        return o6_section5
    if kind == "PIPELINE INVALID":
        return {
            "label": "PIPELINE INVALID",
            "reason": detail.get("reason", "fixture or integrity failure"),
            "detail": detail,
        }
    return {
        "label": kind,
        "reason": "section 5 is not the package outcome for this stop",
        "detail": detail,
    }


def main() -> int:
    try:
        t0, _manifest = preflight(ROOT)
    except PackageStop as exc:
        _preflight_outputs(exc)
        return exc.exit_code

    run = Run(ROOT, t0, ROOT / "outputs" / "run.log")
    o6_section5 = None
    try:
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
        _write_outputs(run, "COMPLETED", 0, {}, o6_section5)
        return 0
    except PackageStop as exc:
        _write_outputs(run, exc.kind, exc.exit_code, exc.detail, _package_section5(o6_section5, exc.kind, exc.detail))
        return exc.exit_code
    except Exception as exc:
        detail = {"reason": "uncaught exception", "error": str(exc), "traceback": traceback.format_exc()}
        _write_outputs(run, "EXECUTION ERROR", 1, detail, _package_section5(o6_section5, "EXECUTION ERROR", detail))
        return 1
    finally:
        run.close()
