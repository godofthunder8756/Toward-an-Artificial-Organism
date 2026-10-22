"""Process entry. Thread limits are set before NumPy is imported."""

import json
import os
import sys
from pathlib import Path


def _thread_stop(name: str, value: str) -> None:
    root = Path(__file__).resolve().parents[1]
    outputs = root / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    detail = {"reason": "thread environment", "value": value, "variable": name}
    results = {
        "detail": detail,
        "exit_code": 5,
        "oracle_edit_field": "eps_syn",
        "package": "ckappa-oracle",
        "phase": "unsealed-implementation",
        "section5": None,
        "stop_kind": "PREFLIGHT FAILED",
    }
    stop = {"exit_code": 5, "stop_kind": "PREFLIGHT FAILED"}
    for name_path, payload in (
        (outputs / "results.json", results),
        (outputs / "stop_kind.json", stop),
    ):
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        tmp = name_path.with_name(name_path.name + ".tmp")
        with open(tmp, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, name_path)


for _name in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    _value = os.environ.get(_name)
    if _value is None:
        os.environ[_name] = "1"
    elif _value != "1":
        sys.stderr.write(f"{_name}={_value}, expected 1\n")
        _thread_stop(_name, _value)
        raise SystemExit(5)

from ckappa_oracle.driver import main

raise SystemExit(main())
