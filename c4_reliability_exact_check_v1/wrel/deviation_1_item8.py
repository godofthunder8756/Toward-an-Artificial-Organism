"""Deviation D1. Rerun ITEM-8 and ITEM-9 after the freeze.

Frozen item7 stores well_defined on the ITEM-7 report and not on the in-memory
machine record. Frozen item8 reads mach["well_defined"] and raised KeyError on
the first setting. This module does not edit any frozen file. It rebuilds the
in-memory dependency state by calling the frozen item functions, copies the
already computed well_defined flag onto each machine record, then calls the
frozen item8 and item9.

Original outputs/ITEM-*.json and outputs/SUMMARY.json are not overwritten.
Corrected payloads are written under outputs/deviation_1/.
"""

from __future__ import annotations

import traceback
from pathlib import Path

from wrel.run_all import (
    item1,
    item2,
    item3,
    item4,
    item5,
    item6,
    item7,
    item8,
    item9,
    study_world,
)
from wrel.util import Budget, CapExceeded, dump_json, pack

ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / "outputs"
OUT = ROOT / "outputs" / "deviation_1"


def _stage(ctx, key, fn, budget):
    budget.start_item(key)
    print(f"rebuild {key} start", flush=True)
    payload = fn()
    payload = dict(payload)
    payload["status"] = payload.get("status", "COMPLETE")
    ctx[key] = payload
    snap = budget.snapshot()
    print(
        f"rebuild {key} {payload['status']} wall={snap['wall_seconds_float']:.1f}s rss={snap['peak_rss_bytes_sampled']}",
        flush=True,
    )
    return payload


def _write(name, payload, budget, status):
    payload = dict(payload)
    payload["item"] = name
    payload["status"] = status
    payload["deviation"] = "D1"
    payload["budget"] = budget.snapshot()
    payload["note"] = (
        "Rerun after deviation D1. Original outputs/ITEM-8.json and outputs/ITEM-9.json "
        "from the freeze run are unchanged."
    )
    dump_json(str(OUT / f"{name}.json"), pack(payload))
    print(f"wrote {name} {status}", flush=True)


def main() -> None:
    for name in ("ITEM-1.json", "ITEM-7.json", "ITEM-8.json", "ITEM-9.json", "SUMMARY.json"):
        if not (ORIG / name).is_file():
            raise SystemExit(f"original output missing, refuse to rerun: {name}")
    OUT.mkdir(parents=True, exist_ok=True)
    budget = Budget()
    world = study_world()
    ctx = {"anomalies": []}
    _stage(ctx, "item1", lambda: item1(world, budget), budget)
    _stage(ctx, "item2", lambda: item2(world, budget, ctx), budget)
    _stage(ctx, "item3", lambda: item3(world, budget, ctx), budget)
    _stage(ctx, "item4", lambda: item4(world, budget, ctx), budget)
    _stage(ctx, "item5", lambda: item5(world, budget, ctx), budget)
    _stage(ctx, "item6", lambda: item6(world, budget, ctx), budget)
    _stage(ctx, "item7", lambda: item7(world, budget, ctx), budget)

    reports = ctx["item7"]["pm_act"]
    machines = ctx["machines"]
    if len(reports) != len(machines):
        raise SystemExit(f"machine/report length {len(machines)} != {len(reports)}")
    for mach, report in zip(machines, reports):
        if (mach["T"], mach["cr"], mach["cs"]) != (report["T"], report["cr"], report["cs"]):
            raise SystemExit("machine record is not aligned with the ITEM-7 report")
        mach["well_defined"] = report["well_defined"]
    print("D1 attached well_defined from the ITEM-7 reports", flush=True)

    budget.start_item("ITEM-8")
    try:
        payload8 = item8(world, budget, ctx)
        status8 = payload8.get("status", "COMPLETE")
    except CapExceeded as exc:
        payload8 = {"reason": str(exc)}
        status8 = "UNRESOLVED-COMPUTE"
    except Exception as exc:
        payload8 = {"error": repr(exc), "trace": traceback.format_exc()}
        status8 = "ENGINEERING-FAILURE"
    ctx["item8"] = dict(payload8)
    ctx["item8"]["status"] = status8
    _write("ITEM-8", payload8, budget, status8)

    budget.start_item("ITEM-9")
    try:
        payload9 = item9(world, budget, ctx)
        status9 = payload9.get("status", "COMPLETE")
    except CapExceeded as exc:
        payload9 = {"reason": str(exc), "partial_note": "ITEM-9 cap during the D1 rerun"}
        status9 = "UNRESOLVED-COMPUTE"
    except Exception as exc:
        payload9 = {"error": repr(exc), "trace": traceback.format_exc()}
        status9 = "ENGINEERING-FAILURE"
    _write("ITEM-9", payload9, budget, status9)
    print("D1 rerun complete", flush=True)


if __name__ == "__main__":
    main()
