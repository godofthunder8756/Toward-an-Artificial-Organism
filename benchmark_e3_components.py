"""Bounded E3 component conformance timing, NEVER an E3 phase or hypothesis run.

Run with Python -B. Only fixed public symbol fixtures enter run_scan_fragment;
no target generator, private root, bootstrap, phase runner or external dependency
is imported. stdout is one JSON object, including argument/conformance failures.
No output files, sys.path changes, monkeypatches or interpreter shortcuts exist.
The read-only 23-entry design audit must pass before importing E3 components.

--repeats defaults to 8, accepts 1..32, and is clipped by hard scan-count caps
(64 REP / 16 BLOCK, INCLUDING warmups and the one traced-memory BLOCK scan).
A 10-second admission budget stops starting new scans; it cannot interrupt an
already-running finite fragment. No duration-filling or adaptive workload loop.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
import gc
import json
import os
import platform
import statistics
import sys
from time import get_clock_info, perf_counter, process_time
import tracemalloc
from typing import TYPE_CHECKING, NoReturn, Sequence

from verify_e3_design import verify

if TYPE_CHECKING:
    from e3.kernels import ScanFragmentResult
    from e3.protocol import Code
    from e3.state import Scratch, State


DEFAULT_REPEATS = 8
MAX_REPEATS = 32
ADMISSION_SECONDS = 10.0
SCAN_CAPS = {"REP": 64, "BLOCK": 16}
# Two fixtures per code. Leave space for both warmups and one memory sample.
PER_FIXTURE_LIMITS = {"REP": 31, "BLOCK": 6}


@dataclass(frozen=True, slots=True)
class Fixture:
    name: str
    code: Code
    symbols: tuple[int, ...]
    payload: int
    health: int


def require(condition: bool, message: str) -> None:
    """Checks remain active under Python -O; failure is technical, not death."""
    if not condition:
        raise ValueError(message)


def fixtures() -> tuple[Fixture, ...]:
    from e3.protocol import Code

    return (
        Fixture("rep_one", Code.REP, (1,) * 5, 1, 2),
        Fixture("rep_one_single_corrupt", Code.REP, (0,) + (1,) * 4, 1, 3),
        Fixture("block_zero", Code.BLOCK, (0,) * 20, 0, 2),
        Fixture("block_zero_single_corrupt", Code.BLOCK, (1,) + (0,) * 19, 0, 3),
    )


def construct(case: Fixture) -> tuple[State, Scratch]:
    """Trusted one-shot test setup, not free acquisition or a live reset."""
    from e3.protocol import Code
    from e3.state import Scratch, State

    state, scratch = State(bytes(276)), Scratch()
    state.energy = (4303 if case.code is Code.BLOCK else 383) + 1
    stride = 1 if case.code is Code.BLOCK else 4
    for index, symbol in enumerate(case.symbols):
        state.write_lane(stride * index, symbol)
    scratch.write_bits(64, 4, 0)  # Literal cue zero, not a target draw.
    scratch.write_bits(68, 1, 1)  # Literal usefulness one.
    scratch.write_bits(224, 16, 0)
    return state, scratch


def check(case: Fixture, state: State, scratch: Scratch, before: bytes,
          result: ScanFragmentResult) -> dict[str, object]:
    from e3.machine import Charge, ExecutionMode, Opcode, StepStatus
    from e3.protocol import Code

    block = case.code is Code.BLOCK
    kernel, reads, control = (3699, 20, 44) if block else (34, 5, 15)
    steps = result.trace.steps
    observation = result.observation
    require((observation.payload, observation.health, observation.observed,
             observation.tied) == (case.payload, case.health, reads, False),
            f"{case.name}: observation mismatch")
    require(result.trace.mode is ExecutionMode.ENGINEERING_FRAGMENT, "wrong mode")
    expected_counts = {Charge.KERNEL: kernel, Charge.ACCESS: reads,
                       Charge.CONTROL_A: control, Charge.EXIT: 1}
    require(Counter(event.charge for event in steps) == expected_counts,
            "instruction charge counts differ from the literal fixture")
    require(tuple(event.pc for event in steps) == tuple(range(len(steps))),
            "nonliteral PC path")
    require(tuple(event.lane for event in steps if event.opcode is Opcode.READ2)
            == tuple(index * (1 if block else 4) for index in range(reads)),
            "wrong paid read lanes")
    require(tuple(event.value for event in steps if event.opcode is Opcode.READ2)
            == case.symbols, "wrong actual read symbols")
    require(len(result.trace.envelopes) == 1
            and result.trace.envelopes[0].region is Charge.CONTROL_A
            and result.trace.envelopes[0].paid.energy == 256,
            "missing actual CONTROL prepayment")
    for event in steps:
        expected = (17 if event.opcode is Opcode.READ2 else
                    8 if event.opcode is Opcode.S else
                    1 if event.charge is Charge.KERNEL else 0)
        require(event.paid.energy == expected
                and event.paid.material == (0, 0, 0, 0), "incorrect primitive debit")
    require(result.trace.envelopes[0].paid.material == (0, 0, 0, 0),
            "unexpected envelope material")
    require(steps[-1].opcode is Opcode.S and steps[-1].status is StepStatus.HALT
            and steps[-1].next_pc is None and scratch.is_zero(), "S did not terminate")
    require(steps[-3].value == case.payload and steps[-2].value == case.health,
            "pre-S result events differ")
    total_energy = 256 + sum(event.paid.energy for event in steps)
    require(total_energy == (4303 if block else 383) and state.energy == 1,
            "energy/residue mismatch")
    after = state.snapshot()
    require(after[:225] == before[:225] and after[227:] == before[227:],
            "read-only scan changed nonenergy persistent bytes")
    return {
        "passed": True,
        "instructions": len(steps),
        "charges": {charge.name: count for charge, count in expected_counts.items()},
        "read2_energy_each": 17,
        "kernel_plus_routed_reads_energy": kernel + 17 * reads,
        "control_envelope_energy": 256,
        "exit_energy": 8,
        "total_simulated_energy": total_energy,
        "total_material": [0, 0, 0, 0],
        "energy_residue": state.energy,
        "scratch_zero_after_s": True,
        "nonenergy_state_unchanged": True,
        "observation": {"payload": observation.payload, "health": observation.health,
                        "observed": observation.observed, "tied": observation.tied},
    }


def timed_scan(case: Fixture) -> tuple[float, dict[str, object]]:
    from e3.kernels import run_scan_fragment

    state, scratch = construct(case)
    before = state.snapshot()
    start = perf_counter()
    result = run_scan_fragment(case.code, state, scratch)
    elapsed = perf_counter() - start
    # Observer checks and trace release are outside the measured API interval.
    return elapsed, check(case, state, scratch, before, result)


def deep_size(root: object) -> dict[str, int]:
    """Size a closed trace graph once per identity; never traverse arbitrary objects.

    Enums are shallow leaves: module/class/global internals are excluded. Shared
    cached integers and singleton costs are counted once, not marginal ownership.
    This is approximate reachable Python storage, NOT RSS or serialized bytes.
    """
    from e3.kernels import ScanFragmentResult, ScanObservation
    from e3.machine import EnvelopePayment, FragmentResult, StepResult
    from e3.meter import Cost

    allowed = (ScanFragmentResult, ScanObservation, EnvelopePayment,
               FragmentResult, StepResult, Cost)
    seen: set[int] = set()

    def visit(value: object) -> int:
        identity = id(value)
        if identity in seen:
            return 0
        seen.add(identity)
        size = sys.getsizeof(value)
        if isinstance(value, (tuple, list)):
            require(type(value) in (tuple, list), "unsupported sequence subtype")
            return size + sum(visit(item) for item in value)
        if isinstance(value, allowed) and is_dataclass(value):
            return size + sum(visit(getattr(value, field.name)) for field in fields(value))
        if value is None or type(value) in (bool, int, float, str, bytes) or isinstance(value, Enum):
            return size
        raise TypeError("deep_size only accepts the closed trace graph and builtin leaves")

    total = visit(root)
    return {"bytes": total, "unique_objects": len(seen)}


def memory_scan(case: Fixture) -> dict[str, object]:
    from e3.kernels import run_scan_fragment
    from e3.machine import StepResult

    require(not tracemalloc.is_tracing(), "memory probe needs an untraced baseline")
    gc.collect()
    tracemalloc.start(1)
    try:
        baseline, _ = tracemalloc.get_traced_memory()
        state, scratch = construct(case)
        before_state, before_scratch = state.snapshot(), scratch.snapshot()
        before_current, _ = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        start = perf_counter()
        result = run_scan_fragment(case.code, state, scratch)
        elapsed = perf_counter() - start
        after_api_current, api_peak = tracemalloc.get_traced_memory()
        after_state, after_scratch = state.snapshot(), scratch.snapshot()
        held_current, held_peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    # Deep walking, checks and JSON construction are not part of the heap peak.
    conformance = check(case, state, scratch, before_state, result)
    return {
        "fixture": case.name,
        "scans": 1,
        "tracemalloc_frames": 1,
        "wall_seconds_with_tracemalloc_not_used_for_projection": elapsed,
        "baseline_current_bytes": baseline,
        "fixture_and_before_snapshots_current_bytes": before_current,
        "after_api_current_bytes": after_api_current,
        "api_peak_bytes": api_peak,
        "api_current_delta_bytes": after_api_current - before_current,
        "api_peak_above_fixture_bytes": api_peak - before_current,
        "held_result_and_four_snapshots_current_bytes": held_current,
        "held_peak_bytes": held_peak,
        "trace_deep_size": deep_size(result.trace),
        "returned_scan_result_deep_size": deep_size(result),
        "result_and_four_snapshots_deep_size": deep_size(
            (result, before_state, before_scratch, after_state, after_scratch)),
        "trace_step_records": len(result.trace.steps),
        "trace_envelope_records": len(result.trace.envelopes),
        "step_record_fields": [field.name for field in fields(StepResult)],
        "step_record_shallow_bytes": sys.getsizeof(result.trace.steps[0]),
        "steps_tuple_shallow_bytes": sys.getsizeof(result.trace.steps),
        "per_step_state_scratch_snapshots": 0,
        "boundary_snapshot_payload_bytes": [276, 32, 276, 32],
        "state_before_hex": before_state.hex(),
        "state_after_hex": after_state.hex(),
        "scratch_before_hex": before_scratch.hex(),
        "scratch_after_s_hex": after_scratch.hex(),
        "pre_s_values_from_returned_events_not_full_snapshot": {
            "payload": result.trace.steps[-3].value, "health": result.trace.steps[-2].value},
        "conformance": conformance,
        "limitations": [
            "tracemalloc observes Python allocations since start, not RSS or all native memory",
            "ROM construction, validation temporaries and the returned trace affect the peak",
            "preexisting interpreter objects are excluded by tracemalloc but may be deep-sized",
            "deep sizing counts shared leaves once; it is not additive marginal ownership",
            "no heap snapshot, filesystem walk, arbitrary object traversal or pre-S hook",
            "observer-only results are never fed back into execution",
        ],
    }


def reference_workload(seconds: dict[str, float]) -> dict[str, object]:
    """Prospective logical arithmetic ONLY; no histories/inputs are instantiated."""
    cells = 8 * 8
    trunks, histories, probes, ecologies, resets = 400, 496, 406, 536, 400
    core_without_oracle = cells * (
        2043 * trunks + 256 * (histories + probes + resets) + 507 * ecologies)
    core_responses = core_without_oracle + 8192
    script_responses = 512 * 507 + 256 * 256
    responses = core_responses + script_responses
    core_controllers = cells * (2048 * trunks + 128 * (histories + resets) + 512 * ecologies)
    script_controllers = 512 * 512 + 256 * 128
    controllers = core_controllers + script_controllers
    require((core_responses, script_responses, responses) ==
            (91_033_088, 325_120, 91_358_208), "selected response arithmetic changed")
    require((core_controllers, script_controllers) == (77_332_480, 294_912),
            "selected controller arithmetic changed")
    scans_per_code = (responses + controllers) // 2
    counts = {"REP": 55, "BLOCK": 3764}
    rates = {
        code: {"scans": scans_per_code, "fragment_steps": scans_per_code * counts[code],
               "seconds_per_scan_observed_mean": seconds[code],
               "hypothetical_days": scans_per_code * seconds[code] / 86400}
        for code in counts if code in seconds
    }
    return {
        "label": "hypothetical_full_coverage_naive_scan_only_NOT_a_runtime_prediction_or_lower_bound",
        "engineering_cells": cells,
        "core_due_responses_without_oracle": core_without_oracle,
        "core_oracle_due_responses": 8192,
        "core_due_responses": core_responses,
        "script_due_responses": script_responses,
        "total_due_responses": responses,
        "due_responses_per_code": responses // 2,
        "core_controller_offers": core_controllers,
        "script_controller_offers": script_controllers,
        "total_controller_offers": controllers,
        "controller_offers_per_code": controllers // 2,
        "core_reset_response_roster_included": cells * resets * 256,
        "script_reset_response_roster_included": 256 * 256,
        "per_code": rates,
        "hypothetical_combined_days": sum(scans_per_code * value / 86400 for value in seconds.values())
        if len(seconds) == 2 else None,
        "total_fragment_steps_if_full_coverage": scans_per_code * sum(counts.values()),
        "assumptions": [
            "engineering only: selected evaluation v0.8 core/oracle plus conformance v0.10 scripts",
            "every listed due slot valid and every controller admitted; one scan each",
            "half of responses and controller offers assigned to each representation",
            "all logical canonical reset roster references counted, before resolving exact-G unions",
            "use the equal-weight mean of clean and single-corrupt public fixture scan times",
            "same host, serial execution and unchanged run_scan_fragment API cost per scan",
        ],
        "limitations": [
            "not necessary actual step counts: death, invalid slots, rejection and sharing reduce scans",
            "canonical futures include negative controls; equal-G roster slots may share a representative",
            "the raw 91,358,208 logical rows do not imply that many actual physical response scans",
            "this is not a worst-case bound or a lower bound on full engineering runtime",
            "full services, controller closure, teaching, upkeep, faults, IPC and archive work are not timed",
            "fragment S/C and ROM rebuild costs do not map exactly to future fused full services",
            "no final histories, scientific gates, random inputs or experimental outcomes were executed",
        ],
    }


def benchmark(repeats: int) -> dict[str, object]:
    from e3.kernels import make_scan_program
    from e3.machine import validate

    require(type(repeats) is int and 1 <= repeats <= MAX_REPEATS, "repeats must be 1..32")
    cases = fixtures()
    counts = {"REP": 0, "BLOCK": 0}
    deadline = perf_counter() + ADMISSION_SECONDS

    def admit(case: Fixture) -> bool:
        code = case.code.name
        if perf_counter() >= deadline or counts[code] >= SCAN_CAPS[code]:
            return False
        counts[code] += 1
        return True

    rom: dict[str, object] = {}
    for case in (cases[0], cases[2]):
        start = perf_counter()
        program = make_scan_program(case.code)
        build_seconds = perf_counter() - start
        start = perf_counter()
        proof = validate(program)
        validation_seconds = perf_counter() - start
        rom[case.code.name] = {
            "instructions": len(program.instructions), "max_steps": proof.max_steps,
            "control_path_bound": list(proof.control_path_bound),
            "one_cold_rom_build_seconds_not_a_rate": build_seconds,
            "one_extra_validation_seconds_not_a_rate": validation_seconds,
        }
        del program

    # Warm EVERY fixture before recording any throughput sample.
    warmed: set[str] = set()
    for case in cases:
        if admit(case):
            timed_scan(case)
            warmed.add(case.name)

    # Keep tracemalloc separate and before throughput, then turn it off.
    memory = memory_scan(cases[3]) if cases[3].name in warmed and admit(cases[3]) else None
    timings: list[dict[str, object]] = []
    means: dict[str, list[float]] = {"REP": [], "BLOCK": []}
    complete = memory is not None and len(warmed) == len(cases)
    for case in cases:
        code = case.code.name
        requested = repeats * (4 if code == "REP" else 1)
        planned = min(requested, PER_FIXTURE_LIMITS[code])
        samples: list[float] = []
        conformance: dict[str, object] | None = None
        if case.name in warmed:
            for _ in range(planned):
                if not admit(case):
                    break
                elapsed, conformance = timed_scan(case)
                samples.append(elapsed)
        complete = complete and len(samples) == planned
        mean = statistics.mean(samples) if samples else None
        if mean is not None:
            means[code].append(mean)
        instructions = 55 if code == "REP" else 3764
        timings.append({
            "fixture": case.name, "code": code, "symbols": list(case.symbols),
            "cue": 0, "usefulness": 1, "warmups": int(case.name in warmed),
            "requested_measured_scans": requested, "bounded_planned_scans": planned,
            "measured_scans": len(samples), "wall_seconds_samples": samples,
            "mean_seconds_per_scan": mean,
            "median_seconds_per_scan": statistics.median(samples) if samples else None,
            "min_seconds_per_scan": min(samples) if samples else None,
            "max_seconds_per_scan": max(samples) if samples else None,
            "ns_per_executed_instruction_including_api_overhead":
                mean * 1e9 / instructions if mean is not None else None,
            "conformance": conformance,
        })
    rates = {code: statistics.mean(values) for code, values in means.items() if len(values) == 2}
    return {
        "ok": complete, "status": "complete" if complete else "bounded_partial",
        "repeats": repeats, "scan_caps_including_warmups_and_memory": SCAN_CAPS,
        "actual_scans_including_warmups_and_memory": counts,
        "admission_budget_seconds": ADMISSION_SECONDS,
        "budget_kind": "stop before next finite scan; not a preemptive wall-time or CPU guarantee",
        "timing_scope": "run_scan_fragment includes ROM build, validation, bounds, execution and observation",
        "timing_exclusions": "fixture setup, conformance checks, trace release, tracemalloc and JSON",
        "gc_enabled_during_timing": gc.isenabled(),
        "rom": rom, "timings": timings, "memory": memory,
        "reference_workload": reference_workload(rates),
    }


class JsonParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ValueError(message)


def main(argv: Sequence[str] | None = None) -> int:
    start, cpu_start = perf_counter(), process_time()
    report: dict[str, object] = {"kind": "bounded_component_conformance_not_hypothesis_run"}
    try:
        parser = JsonParser(add_help=False, allow_abbrev=False)
        parser.add_argument("--repeats", type=int, default=DEFAULT_REPEATS)
        parser.add_argument("--help", action="store_true")
        args = parser.parse_args(argv)
        require(1 <= args.repeats <= MAX_REPEATS, "--repeats must be in 1..32")
        if args.help:
            report.update(ok=True, help=__doc__)
        else:
            audit = verify()
            report["design_verification"] = audit
            require(audit["ok"] is True and audit["file_count"] == 23
                    and audit["files_checked"] == 23, "23-entry design verification failed")
            require(sys.dont_write_bytecode, "use Python -B to suppress bytecode file writes")
            report["host"] = {
                "python_version": platform.python_version(),
                "python_implementation": platform.python_implementation(),
                "system": platform.system(), "release": platform.release(),
                "os_version": platform.version(), "machine": platform.machine(),
                "processor": platform.processor(), "logical_cpus": os.cpu_count(),
                "pointer_bits": 64 if sys.maxsize > 2**32 else 32,
                "bytecode_writes_disabled": sys.dont_write_bytecode,
                "perf_counter_resolution_seconds": get_clock_info("perf_counter").resolution,
            }
            report.update(benchmark(args.repeats))
    except Exception as error:
        # Avoid dumping arbitrary filesystem paths/exception payloads to stdout.
        report.update(ok=False, status="technical_failure", error_type=type(error).__name__)
        if isinstance(error, ValueError):
            report["error"] = str(error)
    report["process_wall_seconds_after_imports"] = perf_counter() - start
    report["process_cpu_seconds_after_imports"] = process_time() - cpu_start
    print(json.dumps(report, sort_keys=True, allow_nan=False))
    return 0 if report.get("ok") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())