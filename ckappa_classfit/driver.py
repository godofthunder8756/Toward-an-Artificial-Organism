"""Wire stages S0–S8. One attempt. No retry. Writes only classfit_outputs/."""

from __future__ import annotations

import json
import traceback
from pathlib import Path

from ckappa_oracle.io import PackageStop, atomic_write_json, atomic_write_text, integrity_stop
from ckappa_oracle import world
from ckappa_classfit.aggregate import stage_s7
from ckappa_classfit.arrays import load_drawn_arrays
from ckappa_classfit.construction import stage_s3
from ckappa_classfit.evaluate import stage_s6
from ckappa_classfit.fits import stage_s5
from ckappa_classfit.gate import sha256_file
from ckappa_classfit.inputs import load_committed_g, load_world_inputs
from ckappa_classfit.o1o2 import stage_s1, stage_s2
from ckappa_classfit.p0 import stage_s4
from ckappa_classfit.pinned import ANNEX_V1_SHA256, FROZEN_RUNTIME, SCOPE_SHA256
from ckappa_classfit.preflight import MANIFEST_NAME, preflight
from ckappa_classfit.report import render
from ckappa_classfit.runstate import Run, write_stop

ROOT = Path(__file__).resolve().parents[1]


def _safe_detail(detail) -> dict:
    if not isinstance(detail, dict):
        return {"reason": str(detail)}
    safe = {}
    for key, value in detail.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            safe[str(key)] = value
        else:
            safe[str(key)] = json.dumps(value, default=str, sort_keys=True)
    return safe


def _results(run: Run | None, kind: str, exit_code: int, detail: dict, science: dict | None) -> dict:
    body = {
        "package": "ckappa-classfit",
        "stop_kind": kind,
        "exit_code": exit_code,
        "detail": _safe_detail(detail),
        "float_propagations": None if run is None else run.float_count,
        "exact_propagations": None if run is None else run.exact_count,
        "svd_count": None if run is None else run.svd_count,
        "projection": None if run is None else run.projection,
        "timing_sample": [] if run is None else run.retained,
        "timing_sample_source": "first 1000 stage-S6 Phi calls; key and q; perf_counter sample in projection",
        "t_elapsed_s": None if run is None else run.elapsed(),
        "t_elapsed_s_source": "time.time() minus CKAPPA_CLASSFIT_T0",
        "accounting": [] if run is None else run.ledger.records(),
        "memory_observation": None if run is None else run.memory_observation(),
    }
    if science:
        body.update(science)
    else:
        body["pooled"] = []
        body["labels"] = []
        body["VALIDATION"] = None
        body["HEADROOM"] = None
        body["d7_investigate"] = []
    return body


def _write_pair(run: Run | None, kind: str, exit_code: int, detail: dict, science: dict | None) -> None:
    results = _results(run, kind, exit_code, detail, science)
    outputs = ROOT / "classfit_outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    try:
        if run is None:
            atomic_write_json(outputs / "results.json", results)
            atomic_write_text(outputs / "REPORT.md", render(results))
            atomic_write_text(outputs / "run.log", f"0.000000 {kind}\n")
            write_stop(ROOT, kind, exit_code)
        else:
            run.write_json("results.json", results)
            run.write_text("REPORT.md", render(results))
            write_stop(run.root, kind, exit_code)
            run.log(f"stop {kind} exit {exit_code}")
            run.checkpoint("stop")
    except Exception:
        minimal = {
            "package": "ckappa-classfit",
            "stop_kind": kind,
            "exit_code": exit_code,
            "writer": "fallback",
        }
        atomic_write_text(outputs / "results.json", json.dumps(minimal, indent=2, sort_keys=True) + "\n")
        atomic_write_text(outputs / "stop_kind.json", json.dumps({"exit_code": exit_code, "stop_kind": kind}, indent=2, sort_keys=True) + "\n")


def _annex_sha(manifest: dict, name: str) -> tuple[str | None, str | None]:
    for entry in (manifest.get("items") or {}).get("governing") or []:
        path = entry.get("path") or ""
        if path.endswith(name):
            file = ROOT / path
            if not file.is_file():
                return path, None
            return path, sha256_file(file)
    return None, None


def _stage_s0(run: Run, manifest: dict, observation: dict, draws: dict, inputs: dict, committed: dict) -> None:
    run.check_deadline("S0")
    manifest_path = ROOT / MANIFEST_NAME
    application = manifest.get("standing_approval_application") or {}
    annex_v3_path, annex_v3_sha = _annex_sha(manifest, "ckappa_classfit_implementation_annex_v3.md")
    annex_v2_path, annex_v2_sha = _annex_sha(manifest, "ckappa_classfit_implementation_annex_v2.md")
    annex_path = annex_v3_path or annex_v2_path
    annex_sha = annex_v3_sha if annex_v3_path is not None else annex_v2_sha
    payload = {
        "stage": "S0",
        "sealed": manifest.get("sealed"),
        "manifest_sha256": sha256_file(manifest_path),
        "annex_sha256": annex_sha,
        "annex_path": annex_path,
        "annex_v3_sha256": annex_v3_sha,
        "annex_v3_path": annex_v3_path,
        "annex_v2_sha256": annex_v2_sha,
        "annex_v2_path": annex_v2_path,
        "annex_v1_sha256": ANNEX_V1_SHA256,
        "scope_sha256": SCOPE_SHA256,
        "application_sha256": application.get("sha256"),
        "input_hashes": inputs.get("input_shas"),
        "reused_arrays": draws.get("checked"),
        "committed_g_sha256": committed.get("sha256"),
        "runtime_observed": observation.get("runtime_observed"),
        "runtime_observed_source": observation.get("runtime_observed_source"),
        "rlimit_as_observed": observation.get("rlimit_as_observed"),
        "cpu_affinity_observed": observation.get("cpu_affinity_observed"),
        "classfit_outputs_state": observation.get("classfit_outputs_state"),
        "b0": observation.get("b0"),
        "input_allow_list": observation.get("input_allow_list"),
        "t_elapsed_s": run.elapsed(),
        "t_elapsed_s_source": "time.time() minus CKAPPA_CLASSFIT_T0",
        "memory": run.memory_observation(),
    }
    if payload["scope_sha256"] != SCOPE_SHA256:
        integrity_stop("scope sha256 drifted")
    run.write_json("stage_S0_preflight.json", payload)
    run.checkpoint("S0")
    run.log("stage S0 written")


def _finish_accounting(run: Run, kind: str) -> None:
    if kind == "COMPLETED":
        if run.float_count > int(FROZEN_RUNTIME["classfit_scheduled_float_propagations"]):
            integrity_stop("float propagation overrun", float_count=run.float_count)
        if not run.ledger.close_all():
            integrity_stop("accounting-closure failure", remaining=_remaining(run))
        return
    run.stopped = True
    run.ledger.dump_remaining("SKIPPED_PRIOR_STOP")
    run.ledger.close_all()


def _remaining(run: Run) -> list:
    rows = []
    for row in run.ledger.records():
        if row["remaining"]:
            rows.append({"system": row["system"], "stage": row["stage"], "unit": row["unit"], "remaining": row["remaining"]})
    return rows


def _science(run: Run, ctx: dict, kind: str) -> dict:
    try:
        return stage_s7(run, ctx, kind)
    except PackageStop:
        raise
    except Exception:
        return {
            "pooled": [],
            "labels": [],
            "VALIDATION": {"label": "CLASS-FIT VALIDATION NOT MET (NOT EVALUATED)", "met": False, "first_failing_reason": kind},
            "HEADROOM": {},
            "d7_investigate": [],
        }


def main() -> int:
    run = None
    ctx: dict = {}
    try:
        try:
            t0, manifest, observation = preflight(ROOT)
        except PackageStop as exc:
            _write_pair(None, exc.kind, exc.exit_code, exc.detail, None)
            return exc.exit_code
        run = Run(ROOT, t0)
        run.log("preflight passed")
        draws = load_drawn_arrays(ROOT)
        stored = load_world_inputs(ROOT)
        committed = load_committed_g(ROOT)
        run.transition = world.column_transition_float()
        _stage_s0(run, manifest, observation, draws, stored, committed)
        ctx = stage_s1(run, stored["by_history"])
        stage_s2(run, ctx)
        stage_s3(run, ctx, draws, committed["g_coefficients"])
        stage_s4(run, ctx)
        stage_s5(run, ctx)
        stage_s6(run, ctx, draws)
        if not run.sample_closed:
            raise PackageStop("STEP 0 SAMPLE SHORT", 6, {"sample_n": run.sample_n, "required": 1000})
        _finish_accounting(run, "COMPLETED")
        science = stage_s7(run, ctx, "COMPLETED")
        run.check_deadline("S8")
        _write_pair(run, "COMPLETED", 0, {}, science)
        run.close()
        return 0
    except PackageStop as exc:
        if run is not None and exc.kind != "INTEGRITY STOP":
            try:
                _finish_accounting(run, exc.kind)
            except PackageStop as second:
                exc = second
        elif run is not None and exc.kind == "INTEGRITY STOP":
            detail = dict(exc.detail)
            detail["remaining_before_terminal_category"] = _remaining(run)
            exc = PackageStop(exc.kind, exc.exit_code, detail)
            run.stopped = True
            run.ledger.dump_remaining("SKIPPED_PRIOR_STOP")
            run.ledger.close_all()
        science = None
        if run is not None:
            try:
                science = _science(run, ctx, exc.kind)
            except PackageStop:
                science = None
        _write_pair(run, exc.kind, exc.exit_code, exc.detail, science)
        if run is not None:
            run.close()
        return exc.exit_code
    except Exception as exc:
        detail = {"reason": "uncaught exception", "error": str(exc), "traceback": traceback.format_exc()}
        if run is not None:
            run.stopped = True
            try:
                run.ledger.dump_remaining("SKIPPED_PRIOR_STOP")
            except Exception:
                pass
        _write_pair(run, "EXECUTION ERROR", 1, detail, None)
        if run is not None:
            run.close()
        return 1
