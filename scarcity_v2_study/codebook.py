"""Call the exact codebook branch-and-bound."""

from __future__ import annotations

import subprocess
from pathlib import Path

from common import N_WORDS

BINARY = Path("/tmp/scarcity_v2_codebook_search")


def ensure_binary() -> Path:
    src = Path(__file__).resolve().parent / "codebook_search.c"
    if not BINARY.exists() or src.stat().st_mtime > BINARY.stat().st_mtime:
        subprocess.check_call(
            ["gcc", "-O3", "-std=c11", "-o", str(BINARY), str(src)],
        )
    return BINARY


def search_codebooks(rewards, weights, k: int, time_limit_ms: int = 240000, collect_limit: int = 20000):
    """Return dict with status, best integer objective, optima as sorted tuples, node count, cpu ms.

    `rewards[s][w]` and `weights[s]` are nonnegative Python ints fitting in int64.
    """
    n_s = len(weights)
    n_w = len(rewards[0])
    if n_w != N_WORDS:
        raise ValueError(f"expected {N_WORDS} words, got {n_w}")
    if k < 1:
        raise ValueError("k")
    # K above the alphabet is the same problem as K = n_w; caller should cap.
    k_use = min(k, n_w)
    payload = [f"{n_s} {n_w} {k_use} {int(time_limit_ms)} {int(collect_limit)}\n"]
    payload.append(" ".join(str(int(w)) for w in weights) + "\n")
    for row in rewards:
        payload.append(" ".join(str(int(x)) for x in row) + "\n")
    proc = subprocess.run(
        [str(ensure_binary())],
        input="".join(payload),
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"codebook_search exit {proc.returncode}")
    lines = proc.stdout.splitlines()
    status = lines[0]
    best = int(lines[1])
    nopt = int(lines[2])
    truncated = int(lines[3])
    nodes = int(lines[4])
    cpu_ms = int(lines[5])
    show = int(lines[6])
    sets = []
    for line in lines[7:7 + show]:
        sets.append(tuple(sorted(int(x) for x in line.split())))
    return {
        "status": status,
        "best": best,
        "n_optima": nopt,
        "truncated": bool(truncated),
        "nodes": nodes,
        "cpu_ms": cpu_ms,
        "sets": sets,
        "k_used": k_use,
    }
