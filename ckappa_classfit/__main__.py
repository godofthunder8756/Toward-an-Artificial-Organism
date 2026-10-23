"""Process entry. Thread limits are set before NumPy is imported."""

from __future__ import annotations

import os
import sys


def _thread_stop(name: str, value: str) -> None:
    import json
    from pathlib import Path

    from ckappa_classfit.outputs_gate import claim_output_dir

    root = Path(__file__).resolve().parents[1]
    reason = claim_output_dir(root)
    if reason is not None:
        sys.stderr.write(f"INTEGRITY STOP: classfit_outputs refused: {reason}\n")
        raise SystemExit(7)
    outputs = root / "classfit_outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    detail = {"reason": "thread environment", "value": value, "variable": name}
    results = {
        "detail": detail,
        "exit_code": 5,
        "package": "ckappa-classfit",
        "stop_kind": "PREFLIGHT FAILED",
        "writer": "thread-check",
    }
    stop = {"exit_code": 5, "stop_kind": "PREFLIGHT FAILED"}
    for path, payload in (
        (outputs / "results.json", results),
        (outputs / "stop_kind.json", stop),
    ):
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        tmp = path.with_name(path.name + ".tmp")
        with open(tmp, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)


for _name in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    _value = os.environ.get(_name)
    if _value is None:
        os.environ[_name] = "1"
    elif _value != "1":
        sys.stderr.write(f"{_name}={_value}, expected 1\n")
        _thread_stop(_name, _value)
        raise SystemExit(5)

from ckappa_classfit.driver import main

raise SystemExit(main())
