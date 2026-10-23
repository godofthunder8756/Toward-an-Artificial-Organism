"""Exact-rational helpers, caps, and JSON rendering. No study quantities."""

from __future__ import annotations

import json
import os
import time
from fractions import Fraction

F = Fraction


def R(x) -> str:
    """Exact rational as a string. Integers render as n/1."""
    if not isinstance(x, Fraction):
        x = Fraction(x)
    return f"{x.numerator}/{x.denominator}"


def parse_R(s: str) -> Fraction:
    if "/" not in s:
        return Fraction(int(s), 1)
    a, b = s.split("/")
    return Fraction(int(a), int(b))


class CapExceeded(Exception):
    def __init__(self, kind: str, detail: str = ""):
        super().__init__(kind if not detail else f"{kind}: {detail}")
        self.kind = kind
        self.detail = detail


class Budget:
    """One CPU process. 4 h total, 1 h per item, 8 GB resident."""

    def __init__(self, total_s: float = 4 * 3600, item_s: float = 3600, rss_bytes: int = 8 * 1024**3):
        self.t0 = time.perf_counter()
        self.item_t0 = self.t0
        self.total_s = total_s
        self.item_s = item_s
        self.rss_bytes = rss_bytes
        self.item_rss_peak = 0
        self.item_name = ""

    def start_item(self, name: str) -> None:
        self.item_name = name
        self.item_t0 = time.perf_counter()
        self.item_rss_peak = read_rss()

    def elapsed_item(self) -> float:
        return time.perf_counter() - self.item_t0

    def elapsed_total(self) -> float:
        return time.perf_counter() - self.t0

    def check(self, where: str = "") -> None:
        rss = read_rss()
        if rss > self.item_rss_peak:
            self.item_rss_peak = rss
        if self.elapsed_total() > self.total_s:
            raise CapExceeded("total-wall", where)
        if self.elapsed_item() > self.item_s:
            raise CapExceeded("item-wall", where)
        if rss > self.rss_bytes:
            raise CapExceeded("memory", f"{where} rss={rss}")

    def snapshot(self) -> dict:
        return {
            "wall_seconds": R(Fraction(self.elapsed_item()).limit_denominator(10**9)),
            "wall_seconds_float": self.elapsed_item(),
            "total_wall_seconds_float": self.elapsed_total(),
            "peak_rss_bytes_sampled": self.item_rss_peak,
            "process_hwm_bytes": read_hwm(),
        }


def read_rss() -> int:
    try:
        with open("/proc/self/status", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1]) * 1024
    except OSError:
        return 0
    return 0


def read_hwm() -> int:
    try:
        with open("/proc/self/status", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("VmHWM:"):
                    return int(line.split()[1]) * 1024
    except OSError:
        return 0
    return 0


def pack(obj):
    """JSON-ready tree. Fractions become exact rational strings. Floats stay floats."""
    if isinstance(obj, Fraction):
        return R(obj)
    if isinstance(obj, dict):
        return {str(k): pack(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [pack(v) for v in obj]
    if isinstance(obj, (bool, int, str)) or obj is None:
        return obj
    if isinstance(obj, float):
        return obj
    raise TypeError(type(obj))


def dump_json(path: str, obj: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=False)
        f.write("\n")
    os.replace(tmp, path)


def sha256_file(path: str) -> str:
    import hashlib

    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()
