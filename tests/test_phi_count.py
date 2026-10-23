"""Pure-helper checks for RL-13. Does not run a stage, the driver, or the wrapper."""

from __future__ import annotations

import tempfile
import time
from pathlib import Path

import numpy as np

import ckappa_classfit.runstate as runstate
from ckappa_classfit.rankcats import b3_status, rank_category_from_ratios
from ckappa_classfit.runstate import SCHEDULED_FLOAT, Run
from ckappa_oracle.io import PackageStop


def _fail(message: str) -> None:
    raise SystemExit(message)


def _run() -> Run:
    root = Path(tempfile.mkdtemp())
    run = Run(root, time.time())
    run.transition = None
    return run


def test_raising_phi_counts() -> None:
    run = _run()
    calls = {"n": 0}

    def raising(theta, u, transition):
        calls["n"] += 1
        raise ValueError("observation has predictive probability 0")

    original = runstate.phi_float
    runstate.phi_float = raising
    try:
        before = run.float_count
        try:
            run.phi(np.zeros(3), 0, "S6", ("unit", 0))
        except ValueError as exc:
            if "predictive probability 0" not in str(exc):
                _fail(f"unexpected ValueError: {exc}")
        else:
            _fail("raising phi_float did not raise")
        if run.float_count != before + 1:
            _fail(f"float_count {run.float_count} did not count the started call")
        if calls["n"] != 1:
            _fail("phi_float was not called")
        if run.sample_n != 0:
            _fail("timing sample was recorded after a raising call")
        run.ledger.add("SYS-O6", "S6", "propagation", "ATTEMPTED", 1, "value_error")
        got = run.ledger.attempted_totals()
        counters = run.exact_count + run.float_count + run.svd_count
        total = got["exact"] + got["float"] + got["svd"] + got["other"]
        if got["value_error"] != 1:
            _fail(f"value_error partition {got['value_error']}")
        if got["float"] != run.float_count or total != counters:
            _fail(f"ATTEMPTED {got} != counters float {run.float_count} total {counters}")
    finally:
        runstate.phi_float = original
        run.close()


def test_overrun_stops_before_increment() -> None:
    run = _run()
    calls = {"n": 0}

    def should_not_run(theta, u, transition):
        calls["n"] += 1
        return np.zeros(4), np.ones(4)

    original = runstate.phi_float
    runstate.phi_float = should_not_run
    run.float_count = SCHEDULED_FLOAT
    before = run.float_count
    try:
        try:
            run.phi(np.zeros(3), 0, "S6", ("unit", 1))
        except PackageStop as exc:
            if exc.kind != "INTEGRITY STOP" or exc.exit_code != 7:
                _fail(f"overrun stop {exc.kind} {exc.exit_code}")
        else:
            _fail("overrun did not stop")
        if run.float_count != before:
            _fail(f"overrun counted the call: {run.float_count}")
        if calls["n"] != 0:
            _fail("phi_float ran after the overrun stop")
    finally:
        runstate.phi_float = original
        run.close()


def test_short_stack_before_zero() -> None:
    try:
        b3_status([0.0, 0.0], True)
    except PackageStop as exc:
        if exc.kind != "INTEGRITY STOP" or exc.exit_code != 7:
            _fail(f"short zero stack {exc.kind} {exc.exit_code}")
    else:
        _fail("short zero stack returned")
    if b3_status([0.0, 0.0, 0.0], True) != "ZERO":
        _fail("three zeros did not return ZERO")


def test_missing_sigma_stops() -> None:
    try:
        rank_category_from_ratios(None, None, 3, False)
    except PackageStop as exc:
        if exc.kind != "INTEGRITY STOP" or exc.exit_code != 7:
            _fail(f"missing sigma_1 {exc.kind} {exc.exit_code}")
    else:
        _fail("missing sigma_1 returned")


if __name__ == "__main__":
    test_raising_phi_counts()
    test_overrun_stops_before_increment()
    test_short_stack_before_zero()
    test_missing_sigma_stops()
    print("phi-count checks passed")
