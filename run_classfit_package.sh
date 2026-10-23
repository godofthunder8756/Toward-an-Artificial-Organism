#!/bin/bash
# Clock first. Interpreter startup, imports, and reporting stay inside this interval.
# This wrapper writes classfit_outputs/ and classfit_post_run_index.json only.
T0=$(date +%s.%N)
export CKAPPA_CLASSFIT_T0="$T0"
cd "$(dirname "$(readlink -f "$0")")"
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1

# RL-9 / B-6. Refuse before launch. A refusal writes nothing and does not start Python.
pre_reason=$(python3 - << 'PY'
import sys
from pathlib import Path
from ckappa_classfit.outputs_gate import index_refusal, outputs_refusal

root = Path(".").resolve()
reason = outputs_refusal(root)
if reason is None:
    index_reason = index_refusal(root)
    if index_reason is not None:
        reason = "post_run_index:" + index_reason
if reason:
    sys.stdout.write(reason)
PY
)
pre_status=$?
if [ "$pre_status" -ne 0 ]; then
  echo "INTEGRITY STOP: classfit_outputs pre-check failed" >&2
  exit 7
fi
if [ -n "$pre_reason" ]; then
  echo "INTEGRITY STOP: classfit_outputs refused: ${pre_reason}" >&2
  exit 7
fi

NOW=$(date +%s.%N)
REM=$(awk -v t0="$T0" -v now="$NOW" 'BEGIN { r = 595 - (now - t0); if (r < 0) r = 0; printf "%.9f", r }')
status=0
if awk -v r="$REM" 'BEGIN { exit !(r > 0) }'; then
  prlimit --as=4000000000 -- taskset -c 0 timeout --signal=KILL "${REM}s" python3 -m ckappa_classfit
  status=$?
else
  status=137
fi

python3 - "$status" "$T0" "$REM" << 'PY'
import hashlib
import json
import os
import sys
from pathlib import Path

status = int(sys.argv[1])
t0 = sys.argv[2]
remaining = sys.argv[3]
root = Path(".").resolve()
from ckappa_classfit.outputs_gate import index_refusal, outputs_refusal

reason = outputs_refusal(root)
if reason == "nonempty":
    reason = None
if reason is None:
    index_reason = index_refusal(root)
    if index_reason is not None:
        reason = "post_run_index:" + index_reason
if reason is not None:
    sys.stderr.write(f"INTEGRITY STOP: classfit_outputs refused: {reason}\n")
    raise SystemExit(7)
outputs = root / "classfit_outputs"
outputs.mkdir(parents=True, exist_ok=True)

def sha256(path: Path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()

manifest_path = "classfit_manifest.json" if (root / "classfit_manifest.json").is_file() else None

if status in (124, 137):
    stop_kind = "CAP REACHED"
    stop_source = "wrapper"
    incomplete = True
else:
    stop_file = outputs / "stop_kind.json"
    if stop_file.is_file():
        recorded = json.loads(stop_file.read_text(encoding="utf-8"))
        stop_kind = recorded.get("stop_kind", "UNRECORDED")
        stop_source = "classfit_outputs/stop_kind.json"
    else:
        stop_kind = "UNRECORDED"
        stop_source = "absent"
    incomplete = status != 0

log_path = outputs / "run.log"
last_counters = None
if log_path.is_file():
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("COUNTERS "):
            last_counters = line

def write_if_missing(path: Path, payload: dict) -> None:
    if path.is_file():
        return
    text = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)

write_if_missing(
    outputs / "results.json",
    {
        "exit_code": status,
        "incomplete": incomplete,
        "package": "ckappa-classfit",
        "stop_kind": stop_kind,
        "writer": "wrapper",
    },
)
write_if_missing(
    outputs / "stop_kind.json",
    {"exit_code": status, "stop_kind": stop_kind},
)

core = [
    "classfit_outputs/stage_S0_preflight.json",
    "classfit_outputs/stage_S1_O1.json",
    "classfit_outputs/stage_S2_O2.json",
    "classfit_outputs/stage_S3_construction.json",
    "classfit_outputs/stage_S4_P0.json",
    "classfit_outputs/fit_freeze_SYS-O6.json",
    "classfit_outputs/fit_freeze_SYS-PC.json",
    "classfit_outputs/fit_freeze_SYS-FK.json",
    "classfit_outputs/fit_freeze_SYS-NC1.json",
    "classfit_outputs/fit_freeze_SYS-NC2.json",
    "classfit_outputs/fit_freeze_SYS-NC3.json",
    "classfit_outputs/fit_freeze_SYS-LIM.json",
    "classfit_outputs/eval_SYS-O6.json",
    "classfit_outputs/eval_SYS-PC.json",
    "classfit_outputs/eval_SYS-FK.json",
    "classfit_outputs/eval_SYS-NC1.json",
    "classfit_outputs/eval_SYS-NC2.json",
    "classfit_outputs/eval_SYS-NC3.json",
    "classfit_outputs/eval_SYS-LIM.json",
    "classfit_outputs/results.json",
    "classfit_outputs/REPORT.md",
]
extra = [
    "classfit_outputs/run.log",
    "classfit_outputs/stop_kind.json",
]
output_sha256 = {}
for name in core + extra:
    path = root / name
    output_sha256[name] = sha256(path) if path.is_file() else None
leftover_tmp = sorted(path.name for path in outputs.glob("*.tmp"))

oracle_rehash_stops = False
oracle_artifact_rehash = {}
oracle_rehash_error = None
try:
    from ckappa_classfit.pinned import (
        ORACLE_SEALED_MANIFEST_SHA256,
        ORACLE_SEALED_OUTPUT_SHA256,
        ORACLE_SEALED_POST_RUN_INDEX_SHA256,
        oracle_rehash_row,
    )

    def file_sha(relative):
        path = root / relative
        return sha256(path) if path.is_file() else None

    oracle_artifact_rehash["manifest.json"] = oracle_rehash_row(
        file_sha("manifest.json"),
        ORACLE_SEALED_MANIFEST_SHA256,
    )
    for name in sorted(ORACLE_SEALED_OUTPUT_SHA256):
        oracle_artifact_rehash[name] = oracle_rehash_row(
            file_sha(name),
            ORACLE_SEALED_OUTPUT_SHA256[name],
        )
    oracle_artifact_rehash["post_run_index.json"] = oracle_rehash_row(
        file_sha("post_run_index.json"),
        ORACLE_SEALED_POST_RUN_INDEX_SHA256,
    )
except Exception as exc:
    oracle_rehash_error = str(exc)

index = {
    "t0": t0,
    "t0_source": "date +%s.%N assigned to CKAPPA_CLASSFIT_T0 before the interpreter",
    "wrapper_kill_budget_s": remaining,
    "exit_status": status,
    "stop_kind": stop_kind,
    "stop_source": stop_source,
    "incomplete": incomplete,
    "manifest_path": manifest_path,
    "manifest_sha256": sha256(root / manifest_path) if manifest_path else None,
    "output_sha256": output_sha256,
    "leftover_tmp": leftover_tmp,
    "last_durable_counters_line": last_counters,
    "counts_after_last_durable": "UNKNOWN_AFTER_LAST_DURABLE" if status in (124, 137) else None,
    "counts_fabricated": False,
    "oracle_artifact_rehash": oracle_artifact_rehash,
    "oracle_rehash_error": oracle_rehash_error,
    "oracle_rehash_stops": oracle_rehash_stops,
}
text = json.dumps(index, indent=2, sort_keys=True, allow_nan=False) + "\n"
tmp = root / "classfit_post_run_index.json.tmp"
with open(tmp, "w", encoding="utf-8") as handle:
    handle.write(text)
    handle.flush()
    os.fsync(handle.fileno())
os.replace(tmp, root / "classfit_post_run_index.json")
directory = os.open(root, os.O_RDONLY)
try:
    os.fsync(directory)
finally:
    os.close(directory)
PY
post=$?
if [ "$post" -eq 7 ]; then
  exit 7
fi
exit "$status"
