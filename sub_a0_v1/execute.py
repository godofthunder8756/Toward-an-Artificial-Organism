from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError("Refusing to overwrite engineering results")
    stdout_path = output.with_suffix(".stdout.log")
    stderr_path = output.with_suffix(".stderr.log")
    started = time.monotonic()
    timed_out = False
    with stdout_path.open("x", encoding="utf-8") as stdout, stderr_path.open("x", encoding="utf-8") as stderr:
        process = subprocess.Popen(
            [sys.executable, "-m", "sub_a0_v1.run", "run", str(output)],
            stdout=stdout, stderr=stderr,
            cwd=Path(__file__).resolve().parents[1],
        )
        try:
            code = process.wait(timeout=max(0.0, 1200 - (time.monotonic() - started)))
        except subprocess.TimeoutExpired:
            timed_out = True
            process.kill()
            code = process.wait()
    if output.is_dir():
        with (output / "watchdog.json").open("x", encoding="utf-8") as handle:
            json.dump({
                "wall_limit_seconds": 1200,
                "launch_to_exit_seconds": time.monotonic() - started,
                "owned_worker_pid": process.pid, "timed_out": timed_out,
                "exit_code": code,
                "scope": "Owned Python worker; no child workers launched",
            }, handle, indent=2)
            handle.write("\n")
        stdout_path.rename(output / "stdout.log")
        stderr_path.rename(output / "stderr.log")
    if timed_out or code != 0:
        raise RuntimeError(f"Engineering worker failed: timeout={timed_out}, exit={code}")
    print((output / "stdout.log").read_text(encoding="utf-8"))
    print(f"Completed owned worker in {time.monotonic() - started:.3f} seconds")


if __name__ == "__main__":
    main()
