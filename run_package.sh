#!/bin/bash
# Clock first. Interpreter startup, imports, and the run are inside this interval.
T0=$(date +%s.%N)
export CKAPPA_T0="$T0"
cd "$(dirname "$(readlink -f "$0")")"
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1

NOW=$(date +%s.%N)
REM=$(awk -v t0="$T0" -v now="$NOW" 'BEGIN { r = 595 - (now - t0); if (r < 0) r = 0; printf "%.9f", r }')
status=0
if awk -v r="$REM" 'BEGIN { exit !(r > 0) }'; then
  prlimit --as=4000000000 -- taskset -c 0 timeout --signal=KILL "${REM}s" python3 -m ckappa_oracle
  status=$?
else
  # timeout 0 disables the kill, so the interpreter is not started.
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

def sha256(path: Path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()

if (root / "manifest.json").is_file():
    manifest_path = "manifest.json"
    sealed_file_present = True
elif (root / "manifest_DRAFT.json").is_file():
    manifest_path = "manifest_DRAFT.json"
    sealed_file_present = False
else:
    manifest_path = None
    sealed_file_present = False

output_names = [
    "outputs/stage_O1.json",
    "outputs/stage_O2.json",
    "outputs/stage_O6.json",
    "outputs/stage_O7.json",
    "outputs/stage_O3.json",
    "outputs/stage_O4.json",
    "outputs/stage_O5.json",
    "outputs/results.json",
    "outputs/REPORT.md",
    "outputs/run.log",
    "outputs/drawn_arrays.npz",
    "outputs/drawn_array_hashes.json",
    "outputs/fit_freeze_O6.json",
    "outputs/fit_freeze_O7.json",
    "outputs/stop_kind.json",
]
output_sha256 = {}
for name in output_names:
    path = root / name
    output_sha256[name] = sha256(path) if path.is_file() else None

if status in (124, 137):
    stop_kind = "CAP REACHED"
    stop_source = "wrapper"
else:
    stop_file = root / "outputs" / "stop_kind.json"
    if stop_file.is_file():
        recorded = json.loads(stop_file.read_text(encoding="utf-8"))
        stop_kind = recorded.get("stop_kind", "UNRECORDED")
        stop_source = "outputs/stop_kind.json"
    else:
        stop_kind = "UNRECORDED"
        stop_source = "absent"

index = {
    "t0": t0,
    "wrapper_kill_budget_s": remaining,
    "exit_status": status,
    "stop_kind": stop_kind,
    "stop_source": stop_source,
    "manifest_path": manifest_path,
    "manifest_sha256": sha256(root / manifest_path) if manifest_path else None,
    "manifest_sealed_file_present": sealed_file_present,
    "output_sha256": output_sha256,
    "drawn_arrays_npz_file_hash_is_reproducibility_check": False,
    "reproducibility_check": "per-array raw-byte sha256, shape, and dtype in outputs/drawn_array_hashes.json and results.json",
}
text = json.dumps(index, indent=2, sort_keys=True, allow_nan=False) + "\n"
tmp = root / "post_run_index.json.tmp"
with open(tmp, "w", encoding="utf-8") as handle:
    handle.write(text)
    handle.flush()
    os.fsync(handle.fileno())
os.replace(tmp, root / "post_run_index.json")
directory = os.open(root, os.O_RDONLY)
try:
    os.fsync(directory)
finally:
    os.close(directory)
PY
exit "$status"
