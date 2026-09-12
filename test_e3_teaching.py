"""Deterministic teaching fixtures, no targets, scheduler or hypothesis runs.

Byte oracles, parity, injected corruption and observer counters exist only in
these tests. No fixture payload or observation is passed back as worker state.
"""

from copy import copy
from dataclasses import FrozenInstanceError
import inspect
from typing import Any, cast
import unittest
from unittest.mock import patch

from e3 import machine, meter, teaching
from e3.machine import Charge, Opcode, StepResult, StepStatus
from e3.protocol import BeginFrame, Code, Phase, ScalarTag, Service
from e3.services import EventKind, ServiceEvent, ServiceStatus
from e3.state import Scratch, State
from e3.teaching import GateEvent, GateKind, TeachingFailure, make_teaching_image, run_commit, run_lesson


def fixture(code=Code.BLOCK, *, commit=False, block=0, tick=None,
            energy=65535, material=(255, 255, 255, 255), raw_stage=0):
    raw = bytearray((37 * i + 19) % 256 for i in range(276))
    raw[217 + block] = raw_stage
    raw[225:227], raw[227:231] = energy.to_bytes(2, "little"), bytes(material)
    state, scratch = State(raw), Scratch()
    service = Service.COMMIT if commit else (
        Service.BLOCK_LESSON if code is Code.BLOCK else Service.REP_LESSON)
    begin = BeginFrame(Phase.ACQUISITION, (4 if commit else 1) if tick is None else tick,
                       service, block if commit else 0, 0, state.snapshot())
    return state, scratch, begin


def paid(result):
    total = meter.ZERO
    for event in result.trace:
        total = meter.add_cost(total, event.paid)
    return total


def steps(result, op=None):
    return [e for e in result.trace if isinstance(e, StepResult)
            and (op is None or e.opcode is op)]


def write_byte(raw, lane, symbol):
    shift = 2 * (lane % 4)
    raw[lane // 4] = (raw[lane // 4] & ~(3 << shift)) | (symbol << shift)


def vector(source, amount, base=0) -> meter.Material4:
    return (base + amount * int(source == 0), base + amount * int(source == 1),
            base + amount * int(source == 2), base + amount * int(source == 3))


def expected_final(begin, spend, *, stage=None, writes=()):
    raw = bytearray(begin.state)
    if stage is not None:
        raw[217 + stage[0]] = stage[1]
    for lane, symbol in writes:
        write_byte(raw, lane, symbol)
    raw[225:227] = (int.from_bytes(raw[225:227], "little") - spend.energy).to_bytes(2, "little")
    raw[227:231] = bytes(p - c for p, c in zip(raw[227:231], spend.material))
    return bytes(raw)


class TestTeaching(unittest.TestCase):
    def assert_exit(self, result, scratch, control, cost):
        self.assertIs(result.status, ServiceStatus.EXIT)
        self.assertEqual(paid(result), cost)
        self.assertEqual(scratch.snapshot(), bytes(32))
        actual = steps(result)
        self.assertEqual(sum(e.charge is Charge.CONTROL_A for e in actual), control)
        self.assertFalse(any(e.opcode is Opcode.PAD for e in actual))
        if actual:
            self.assertIs(actual[-1].status, StepStatus.HALT)
            self.assertIsNone(actual[-1].next_pc)
        self.assertEqual(sum(isinstance(e, ServiceEvent) and e.kind is EventKind.CONTROL
                             for e in result.trace), int(control > 0))

    def test_fixed_catalog_literal_sites_projection_and_immutable_gates(self):
        for service, length, control, body, gates in (
            (Service.BLOCK_LESSON, 44, 33, meter.Cost(362, (1, 1, 1, 1)), []),
            (Service.REP_LESSON, 56, 38, meter.Cost(911), [18 + 8 * i for i in range(5)]),
            (Service.COMMIT, 291, 121, meter.Cost(488, (1, 1, 1, 1)),
             [15, *[28 + 13 * i for i in range(20)]]),
        ):
            for argument in range(4 if service is Service.COMMIT else 1):
                image = make_teaching_image(service, argument)
                self.assertEqual(len(image.sites), length)
                self.assertEqual(machine.validate(image.program).control_path_bound, (control, 0))
                self.assertEqual(image.outer_body, body)
                self.assertEqual(list(image.gates), gates)
                self.assertEqual(list(image.scalars), [] if service is Service.COMMIT else [1, 3])
                for pc, ins in enumerate(image.sites):
                    projected = image.program.instructions[pc]
                    assert projected is not None
                    if type(ins) is machine.Instruction:
                        self.assertIs(ins, projected)
                        self.assertIsNot(ins.opcode, Opcode.PAD)
                    else:
                        self.assertIs(projected.opcode, Opcode.PAD)
                if gates:
                    with self.assertRaises(TypeError):
                        cast(Any, image.gates)[gates[0]] = image.gates[gates[0]]
                    with self.assertRaises(FrozenInstanceError):
                        setattr(image.gates[gates[0]], "kind", GateKind.WRITE)
        for service, argument in ((Service.TEMPLATE, 0), (Service.COMMIT, 4),
                                  (Service.REP_LESSON, 1), (5, 0), (Service.COMMIT, True)):
            with self.assertRaises((TypeError, ValueError)):
                make_teaching_image(cast(Any, service), argument)

    def test_block_all_cues_and_raw_staging_merge_exact_trace(self):
        cases = [(cue, label, raw) for cue in range(16) for label in range(2)
                 for raw in (0, 15, 85, 170, 255)]
        cases += [(raw % 16, (raw >> 4) & 1, raw) for raw in range(256)]
        for cue, label, raw in cases:
            block, bit = divmod(cue, 4)
            state, scratch, begin = fixture(block=block, raw_stage=raw)
            result = run_lesson(state, scratch, begin, Code.BLOCK, (cue, label))
            spend = meter.Cost(490, (1, 1, 1, 1))
            merged = (raw & ~(1 << bit)) | (label << bit) | (1 << (4 + bit))
            self.assertEqual(state.snapshot(), expected_final(begin, spend, stage=(block, merged)))
            self.assert_exit(result, scratch, 33, spend)
            self.assertEqual(result.vaw, (0, 0, 0))
            self.assertEqual([e.pc for e in result.trace[2:]], list(range(44)))
            self.assertEqual(len(result.trace), 46)
            reads, writes = steps(result, Opcode.READ2), steps(result, Opcode.WRITE2)
            self.assertEqual([e.lane for e in reads], list(range(868 + 4 * block, 872 + 4 * block)))
            self.assertEqual([e.lane for e in writes], [e.lane for e in reads])
            self.assertEqual([e.value for e in reads], [(raw >> (2 * k)) & 3 for k in range(4)])
            self.assertEqual([e.value for e in writes], [(merged >> (2 * k)) & 3 for k in range(4)])
            self.assertEqual(sum(e.paid.energy for e in reads), 40)
            self.assertEqual(sum(e.paid.energy for e in writes), 56)
            self.assertFalse(any(e.charge is Charge.KERNEL for e in steps(result)))

    def test_rep_sixteen_current_lessons_no_code_reads(self):
        for cue in range(16):
            for label in (0, 1):
                source = cue // 4
                material = vector(source, 5)
                state, scratch, begin = fixture(Code.REP, energy=1155, material=material)
                with patch.object(State, "read_lane", side_effect=AssertionError("REP reads code")):
                    result = run_lesson(state, scratch, begin, Code.REP, (cue, label))
                lanes = [20 * source + cue % 4 + 4 * i for i in range(5)]
                spend = meter.Cost(1154, material)
                self.assertEqual(state.snapshot(), expected_final(begin, spend,
                                                                 writes=[(a, label) for a in lanes]))
                self.assert_exit(result, scratch, 38, spend)
                self.assertEqual(result.vaw, (5, 5, 5))
                self.assertEqual([e.pc for e in result.trace[2:]], list(range(56)))
                self.assertEqual(len(result.trace), 58)
                self.assertEqual([e.lane for e in steps(result, Opcode.WRITE2)], lanes)
                self.assertEqual(sum(e.charge is Charge.KERNEL for e in steps(result)), 5)
                self.assertEqual(state.energy, 1)

    def test_commit_all_raw_staging_stored_validity_only_and_paid_clear(self):
        for raw in range(256):
            block = raw % 4
            state, scratch, begin = fixture(commit=True, block=block, raw_stage=raw)
            result = run_commit(state, scratch, begin, Code.BLOCK)
            eligible = raw >= 240
            cost = meter.Cost(3756, vector(block, 20, 1)) if eligible else meter.Cost(616, (1, 1, 1, 1))
            words = [(20 * block + i, ((raw & 15) & column).bit_count() % 2)
                     for i, column in enumerate((*range(1, 16), 1, 2, 4, 8, 15))] if eligible else []
            self.assertEqual(state.snapshot(), expected_final(begin, cost, stage=(block, 0), writes=words))
            self.assert_exit(result, scratch, 121 if eligible else 20, cost)
            self.assertEqual(result.vaw, (20, 20, 20) if eligible else (0, 0, 0))
            reads = steps(result, Opcode.READ2)
            self.assertEqual([e.value for e in reads], [(raw >> (2 * k)) & 3 for k in range(4)])
            self.assertEqual([e.value for e in steps(result, Opcode.WRITE2)[-4:]], [0] * 4)
            self.assertEqual(sum(e.charge is Charge.KERNEL for e in steps(result)), 120 if eligible else 0)
            encoding = [e for e in result.trace if isinstance(e, GateEvent) and e.site.kind is GateKind.ENCODING]
            self.assertEqual(len(encoding), 1)
            self.assertEqual(encoding[0].paid, meter.FEE)
            if eligible:
                self.assertEqual(len(result.trace), 293)
                self.assertEqual([e.pc for e in result.trace[2:]], list(range(291)))

    def test_false_validity_encodes_corrupt_labels_after_rejected_fourth_lesson(self):
        state, scratch, begin = fixture(block=3, energy=490, raw_stage=255, tick=4)
        rejected = run_lesson(state, scratch, begin, Code.BLOCK, None)
        self.assertEqual(paid(rejected), meter.Cost(136))
        self.assertEqual(state.snapshot()[220], 255)
        # External engineering refill, not an internal retry or teacher check.
        state.energy = 65535
        begin = BeginFrame(Phase.ACQUISITION, 4, Service.COMMIT, 3, 0, state.snapshot())
        result = run_commit(state, scratch, begin, Code.BLOCK)
        self.assertEqual(result.vaw, (20, 20, 20))
        self.assertEqual([e.value for e in steps(result, Opcode.WRITE2)[:20]],
                         [(15 & column).bit_count() % 2 for column in (*range(1, 16), 1, 2, 4, 8, 15)])
        self.assertTrue(all(e.lane is not None and 60 <= e.lane < 80
                    for e in steps(result, Opcode.WRITE2)[:20]))
        self.assertEqual(state.snapshot()[220], 0)

    def test_block_minimum_and_full_thresholds(self):
        for energy, cost, controls in ((137, 136, 0), (490, 136, 0), (491, 490, 33)):
            state, scratch, begin = fixture(energy=energy, material=(1, 1, 1, 1))
            result = run_lesson(state, scratch, begin, Code.BLOCK, (0, 0) if controls else None)
            spend = meter.Cost(cost, (1, 1, 1, 1) if controls else (0, 0, 0, 0))
            self.assert_exit(result, scratch, controls, spend)
            self.assertEqual(state.energy, energy - cost)

    def test_rejections_ignore_packet_entirely_no_c_no_read_no_write(self):
        class ForbiddenPacket:
            def __len__(self):
                raise AssertionError("inspected rejected packet")

            def __getitem__(self, index):
                del index
                raise AssertionError("inspected rejected packet")

        for code, energy, material in ((Code.BLOCK, 490, (1, 1, 1, 1)),
                                       (Code.BLOCK, 65535, (0, 255, 255, 255)),
                                       (Code.REP, 1039, (255, 255, 255, 255))):
            state, scratch, begin = fixture(code, energy=energy, material=material, raw_stage=213)
            with patch.object(machine, "_step", side_effect=AssertionError("unpaid C")), \
                    patch.object(State, "read_lane", side_effect=AssertionError("rejected read")), \
                    patch.object(State, "write_lane", side_effect=AssertionError("rejected write")), \
                    patch.object(teaching, "scalar_from_value", side_effect=AssertionError("rejected scalar")):
                result = run_lesson(state, scratch, begin, code, cast(Any, ForbiddenPacket()))
            self.assertEqual([e.kind for e in result.trace if isinstance(e, ServiceEvent)],
                             [EventKind.METER, EventKind.S])
            self.assertEqual(len(result.trace), 2)
            self.assertEqual(state.snapshot(), expected_final(begin, meter.Cost(136)))
            self.assert_exit(result, scratch, 0, meter.Cost(136))

    def test_minimum_failures_energy_or_local_material_no_cleanup(self):
        for commit, energy, material, tail in (
            (False, 0, (255,) * 4, meter.ZERO), (False, 136, (255,) * 4, meter.ZERO),
            (True, 616, (255,) * 4, meter.ZERO), (True, 65535, (0, 255, 255, 255), meter.ZERO),
            (False, 65535, (0, 255, 255, 255), meter.Cost(0, (1, 0, 0, 0))),
            (True, 65535, (1, 255, 255, 255), meter.Cost(0, (1, 0, 0, 0))),
        ):
            state, scratch, begin = fixture(commit=commit, energy=energy, material=material, raw_stage=255)
            with patch.object(Scratch, "clear", side_effect=AssertionError("unpaid S")), \
                    patch.object(machine, "_step", side_effect=AssertionError("unpaid body")):
                result = (run_commit(state, scratch, begin, Code.BLOCK, tail) if commit else
                          run_lesson(state, scratch, begin, Code.BLOCK, None, tail))
            expected = bytearray(begin.state)
            expected[225:227] = bytes(2)
            self.assertEqual(state.snapshot(), bytes(expected))
            self.assertTrue(scratch.is_zero())
            self.assertIs(result.status, ServiceStatus.SHUTDOWN)
            self.assertEqual(paid(result), meter.ZERO)
            self.assertEqual(len(result.trace), 1)
            outer = result.trace[0]
            assert isinstance(outer, ServiceEvent)
            self.assertEqual(outer.outcome, meter.GateResult(False, False, energy))

    def test_commit_encoding_fee_even_invalid_and_encoding_threshold(self):
        for raw in (0, 15, 240, 255):
            for energy in (617, 3296, 3297):
                state, scratch, begin = fixture(commit=True, energy=energy, raw_stage=raw, material=(1,) * 4)
                result = run_commit(state, scratch, begin, Code.BLOCK)
                gate = next(e for e in result.trace if isinstance(e, GateEvent))
                self.assertEqual(gate.outcome.enough, energy == 3297)
                visited = int(raw >= 240 and energy == 3297)
                control = 20 if raw < 240 else 21 + 5 * visited
                self.assert_exit(result, scratch, control, meter.Cost(616 + 134 * visited, (1, 1, 1, 1)))
                self.assertEqual(result.vaw, (visited, visited, 0))
                self.assertEqual(state.snapshot()[217], 0)

    def test_every_material_limited_prefix_retains_clear_and_tail_sourcewise(self):
        tail = meter.Cost(952, (5, 5, 5, 5))  # Cold AGE reserve; no global scheduler claim.
        for commit, n, g in ((False, 5, 1), (True, 20, 6)):
            for source in range(4):
                for count in range(n + 1):
                    p = [255] * 4
                    p[source] = count + 5 + int(commit)
                    state, scratch, begin = fixture(Code.BLOCK if commit else Code.REP, commit=commit,
                                                    block=source, raw_stage=245, material=tuple(p))
                    result = (run_commit(state, scratch, begin, Code.BLOCK, tail) if commit else
                              run_lesson(state, scratch, begin, Code.REP, (4 * source + 2, 1), tail))
                    visits = min(count + 1, n)
                    cost = (616 if commit else 394) + visits * (g + 128) + count * 23
                    material = vector(source, count, int(commit))
                    control = (21 if commit else 13) + visits * 5
                    self.assert_exit(result, scratch, control, meter.Cost(cost, material))
                    self.assertEqual(result.vaw, (visits, visits, count))
                    self.assertEqual(state.read_material(source), 5)
                    if commit:
                        self.assertEqual(state.snapshot()[217 + source], 0)
                    self.assertTrue(meter.require_cost(state, tail))
                    gates = [e for e in result.trace if isinstance(e, GateEvent) and e.site.kind is GateKind.WRITE]
                    self.assertEqual([e.outcome.enough for e in gates], [True] * count + [False] * int(count < n))

    def test_every_energy_limited_prefix_release_not_refund(self):
        for commit, n, fixed in ((False, 5, 1039), (True, 20, 3296)):
            for count in range(n + 1):
                state, scratch, begin = fixture(Code.BLOCK if commit else Code.REP, commit=commit,
                                                raw_stage=255, energy=fixed + 23 * count + 1)
                result = (run_commit(state, scratch, begin, Code.BLOCK) if commit else
                          run_lesson(state, scratch, begin, Code.REP, (0, 1)))
                self.assertEqual(result.vaw, (min(count + 1, n), min(count + 1, n), count))
                self.assertEqual(state.energy, 1 + (n - min(count + 1, n)) * (134 if commit else 129))
                self.assertTrue(scratch.is_zero())

    def test_actual_gate_arguments_and_pc_flag_handoff_no_fake_padding(self):
        original_gate, original_step = meter.gate, machine._step
        for commit, n, g in ((False, 5, 1), (True, 20, 6)):
            source = 2
            state, scratch, begin = fixture(Code.BLOCK if commit else Code.REP, commit=commit,
                                            block=source, raw_stage=250)
            image = make_teaching_image(begin.service, begin.argument)
            observed = []

            def gate(s, current, local_remainder=meter.ZERO, public_tail=meter.ZERO,
                     *, minimum_exit=None, residue=1):
                pc = scratch.read_bits(224, 16)
                if pc in image.gates:
                    site = image.gates[pc]
                    self.assertEqual(local_remainder, site.local_remainder)
                    self.assertEqual(minimum_exit, local_remainder)
                    self.assertEqual(residue, 1)
                    if site.kind is GateKind.WRITE:
                        i = len(observed)
                        self.assertEqual(current, meter.Cost(23, (0, 0, 1, 0)))
                        self.assertEqual(local_remainder, meter.Cost((n - i - 1) * (g + 128) + (64 if commit else 8),
                                                                                    (1, 1, 1, 1) if commit else (0, 0, 0, 0)))
                        observed.append(pc)
                return original_gate(s, current, local_remainder, public_tail,
                                     minimum_exit=minimum_exit, residue=residue)

            def step(program, s, d, local, tail):
                pc = d.read_bits(224, 16)
                self.assertIsNot(program.instructions[pc].opcode, Opcode.PAD)
                self.assertNotIn(pc, image.gates)
                return original_step(program, s, d, local, tail)

            with patch.object(meter, "gate", side_effect=gate), patch.object(machine, "_step", side_effect=step), \
                    patch.object(machine, "execute", side_effect=AssertionError("second C")), \
                    patch.object(machine, "step", side_effect=AssertionError("unpaid public core")):
                result = (run_commit(state, scratch, begin, Code.BLOCK) if commit else
                          run_lesson(state, scratch, begin, Code.REP, (8, 1)))
            self.assertEqual(len(observed), n)
            for event in result.trace:
                if isinstance(event, GateEvent):
                    self.assertEqual(event.next_pc, event.pc + 1)
                    self.assertEqual(event.paid, meter.FEE)

    def test_block_each_debit_reserves_exact_suffix_and_tail(self):
        tail = meter.Cost(952, (5, 5, 5, 5))
        state, scratch, begin = fixture(energy=1443, material=(6, 6, 6, 6))
        original = meter.debit

        def checked(s, current, local_remainder=meter.ZERO, public_tail=meter.ZERO, residue=1):
            self.assertEqual(public_tail, tail)
            self.assertEqual(meter.Cost(s.energy, (s.P0, s.P1, s.P2, s.P3)),
                             meter.floor_quote(current, local_remainder, public_tail, residue))
            return original(s, current, local_remainder, public_tail, residue)

        with patch.object(meter, "debit", side_effect=checked):
            run_lesson(state, scratch, begin, Code.BLOCK, (0, 0), tail)
        meter.debit(state, tail)
        self.assertEqual((state.energy, state.P0, state.P1, state.P2, state.P3), (1, 0, 0, 0, 0))

    def test_paid_scalar_order_narrow_ram_reads_and_no_host_payload_after_capture(self):
        original_read, original_step = State.read_bits, machine._step
        original_scalar = teaching.scalar_from_value
        state, scratch, begin = fixture(energy=491, material=(1,) * 4, raw_stage=170)
        scalar_observations = []

        def read(s, offset, width, signed=False):
            self.assertEqual(width, 2)
            return original_read(s, offset, width, signed)

        def scalar(tag, value):
            scalar_observations.append((tag, value, state.energy, scratch.read_bits(224, 16)))
            return original_scalar(tag, value)

        def step(program, s, d, local, tail):
            if d.read_bits(224, 16) >= 4:
                current_frame = inspect.currentframe()
                assert current_frame is not None
                frame = current_frame.f_back
                while frame is not None:
                    if frame.f_globals.get("__name__") == "e3.teaching":
                        self.assertNotIn("begin", frame.f_locals)
                        self.assertIsNone(frame.f_locals.get("packet"))
                        self.assertNotIn("value", frame.f_locals)
                        if "handoff" in frame.f_locals:
                            self.assertEqual(frame.f_locals["handoff"], [])
                    frame = frame.f_back
            return original_step(program, s, d, local, tail)

        with patch.object(State, "read_bits", read), patch.object(machine, "_step", side_effect=step), \
                patch.object(teaching, "scalar_from_value", side_effect=scalar):
            run_lesson(state, scratch, begin, Code.BLOCK, (0, 0))
        self.assertEqual(scalar_observations, [(ScalarTag.LESSON_CUE, 0, 106, 1),
                                              (ScalarTag.LESSON_LABEL, 0, 105, 3)])

    def test_bad_packet_deferred_per_scalar_and_technical_prefix_not_cleanup(self):
        for packet, energy, pc, scalars in ((None, 384, 1, 0), ((True, 0), 384, 1, 0),
                                          ((16, 0), 384, 1, 0), ((0, None), 385, 3, 1),
                                          ((0, True), 385, 3, 1), ((0, 2), 385, 3, 1),
                                          ((0, -1), 385, 3, 1), ([0, 1], 384, 1, 0)):
            state, scratch, begin = fixture()
            with patch.object(Scratch, "clear", side_effect=AssertionError("technical S")), \
                    self.assertRaises(TeachingFailure) as caught:
                run_lesson(state, scratch, begin, Code.BLOCK, cast(Any, packet))
            result = caught.exception.prefix
            self.assertIs(result.status, ServiceStatus.INTERRUPTED)
            self.assertEqual(paid(result), meter.Cost(energy))
            self.assertEqual(state.snapshot(), expected_final(begin, meter.Cost(energy)))
            self.assertEqual(scratch.read_bits(224, 16), pc)
            self.assertEqual(sum(isinstance(e, ServiceEvent) and e.kind is EventKind.SCALAR
                                 for e in result.trace), scalars)

    def test_read_and_encoding_failures_leave_actual_prefix_no_free_clear(self):
        state, scratch, begin = fixture(commit=True, raw_stage=255)
        with patch.object(State, "read_lane", side_effect=ValueError("technical read fault")), \
                self.assertRaises(TeachingFailure) as caught:
            run_commit(state, scratch, begin, Code.BLOCK)
        # The failed READ2 debited first; its incomplete event is NOT invented.
        self.assertEqual(paid(caught.exception.prefix), meter.Cost(384))
        self.assertEqual(state.energy, 65535 - 394)
        self.assertEqual(state.snapshot()[217], 255)
        self.assertFalse(scratch.is_zero())

        state, scratch, begin = fixture(commit=True, raw_stage=255)
        original = machine._step

        def fail_kernel(program, s, d, local, tail):
            if d.read_bits(224, 16) == 19:
                raise ValueError("technical parity fault")
            return original(program, s, d, local, tail)

        with patch.object(machine, "_step", side_effect=fail_kernel), self.assertRaises(TeachingFailure) as caught:
            run_commit(state, scratch, begin, Code.BLOCK)
        self.assertEqual(paid(caught.exception.prefix), meter.Cost(552))
        self.assertEqual(state.energy, 65535 - 552)
        self.assertEqual(state.snapshot()[217], 255)

    def test_entry_validation_before_any_payment(self):
        cases = (("code", Code.REP), ("code", 1), ("tail", None),
                 ("tail", meter.Cost(meter.INT32_MAX)), ("phase", Phase.DEVELOPMENT),
                 ("service", Service.REP_LESSON), ("argument", 1), ("mask", 4),
                 ("planned_tick", 0), ("state", bytes(276)), ("abi", 8), ("scratch", True))
        for field, value in cases:
            state, scratch, original = fixture()
            begin, code, tail = copy(original), Code.BLOCK, meter.ZERO
            if field == "code":
                code = value
            elif field == "tail":
                tail = value
            elif field == "scratch":
                scratch.write_bits(255, 1, 1)
            else:
                object.__setattr__(begin, field, value)
            before = state.snapshot(), scratch.snapshot()
            with patch.object(meter, "gate", side_effect=AssertionError("invalid entry paid")), \
                    self.assertRaises((TypeError, ValueError, OverflowError)):
                run_lesson(state, scratch, begin, cast(Any, code), None, cast(Any, tail))
            self.assertEqual((state.snapshot(), scratch.snapshot()), before)
        for tick, block, code in ((3, 0, Code.BLOCK), (4, 4, Code.BLOCK), (4, 0, Code.REP)):
            state, scratch, begin = fixture(commit=True)
            object.__setattr__(begin, "planned_tick", tick)
            object.__setattr__(begin, "argument", block)
            with self.assertRaises(ValueError):
                run_commit(state, scratch, begin, code)
            self.assertEqual(state.snapshot(), begin.state)


    def test_commit_all_payloads_at_each_public_block_including_same_value_writes(self):
        for block in range(4):
            for payload in range(16):
                state, scratch, begin = fixture(commit=True, block=block, raw_stage=240 | payload)
                word = [(payload & column).bit_count() % 2
                        for column in (*range(1, 16), 1, 2, 4, 8, 15)]
                for i, value in enumerate(word):
                    state.write_lane(20 * block + i, value)
                begin = BeginFrame(Phase.ACQUISITION, 4, Service.COMMIT, block, 0, state.snapshot())
                result = run_commit(state, scratch, begin, Code.BLOCK)
                self.assertEqual([e.value for e in steps(result, Opcode.WRITE2)[:20]], word)
                self.assertEqual(state.snapshot()[:217], begin.state[:217])
                self.assertEqual(result.vaw, (20, 20, 20))
                self.assert_exit(result, scratch, 121, meter.Cost(3756, vector(block, 20, 1)))

    def test_sixteen_literal_lessons_then_public_commits_no_host_label_buffer(self):
        # One small constructed pass, deliberately not the 256-lesson schedule.
        state, scratch, _ = fixture()
        for j in range(4):
            state.write_bits(1736 + 8 * j, 8, 0)
        for ordinal, block in enumerate((3, 1, 0, 2)):  # Not derivable from tick alone.
            for bit in range(4):
                cue = 4 * block + bit
                tick = 1 + ordinal * 4 + bit
                begin = BeginFrame(Phase.ACQUISITION, tick, Service.BLOCK_LESSON, 0, 0, state.snapshot())
                run_lesson(state, scratch, begin, Code.BLOCK, (cue, bit & 1))
            begin = BeginFrame(Phase.ACQUISITION, 4 * (ordinal + 1), Service.COMMIT, block, 0, state.snapshot())
            result = run_commit(state, scratch, begin, Code.BLOCK)
            self.assertEqual([e.value for e in steps(result, Opcode.WRITE2)[:20]],
                             [(10 & column).bit_count() % 2 for column in (*range(1, 16), 1, 2, 4, 8, 15)])
            self.assertEqual(state.snapshot()[217 + block], 0)
        self.assertEqual(state.energy, 65535 - 16 * 490 - 4 * 3756)
        self.assertEqual((state.P0, state.P1, state.P2, state.P3), (215,) * 4)

    def test_gate_register_clobber_does_not_destroy_payload_address_or_validity(self):
        original = meter.gate
        for commit in (False, True):
            state, scratch, begin = fixture(Code.BLOCK if commit else Code.REP, commit=commit,
                                            block=1, raw_stage=246)
            image = make_teaching_image(begin.service, begin.argument)

            def clobber(s, current, local_remainder=meter.ZERO, public_tail=meter.ZERO,
                        *, minimum_exit=None, residue=1):
                result = original(s, current, local_remainder, public_tail,
                                  minimum_exit=minimum_exit, residue=residue)
                if scratch.read_bits(224, 16) in image.gates:
                    for offset in (96, 128, 160, 192):
                        scratch.write_bits(offset, 32, 0xFFFFFFFF)
                return result

            with patch.object(meter, "gate", side_effect=clobber):
                result = (run_commit(state, scratch, begin, Code.BLOCK) if commit else
                          run_lesson(state, scratch, begin, Code.REP, (4, 1)))
            code_writes = [e for e in steps(result, Opcode.WRITE2) if e.lane is not None and e.lane < 80]
            self.assertEqual([e.value for e in code_writes],
                             [(6 & column).bit_count() % 2 for column in (*range(1, 16), 1, 2, 4, 8, 15)]
                             if commit else [1] * 5)
            self.assertTrue(scratch.is_zero())

    def test_block_source_holes_preserve_whole_stage_without_inspecting_label(self):
        tail = meter.Cost(952, (5, 5, 5, 5))
        for source in range(4):
            p = [255] * 4
            p[source] = 5
            state, scratch, begin = fixture(block=3, raw_stage=219, material=tuple(p))
            with patch.object(State, "read_lane", side_effect=AssertionError("partial staging")):
                result = run_lesson(state, scratch, begin, Code.BLOCK, None, tail)
            self.assertEqual(paid(result), meter.Cost(136))
            self.assertEqual(state.snapshot(), expected_final(begin, meter.Cost(136)))
            self.assertTrue(scratch.is_zero())

    def test_every_prefix_debit_local_is_exact_fixed_suffix_with_clear_and_tail(self):
        original = meter.debit
        tail = meter.Cost(952, (5, 5, 5, 5))
        for commit, n, g, fixed in ((False, 5, 1, 1039), (True, 20, 6, 3296)):
            for count in range(n + 1):
                energy = fixed + 23 * count + 1 + tail.energy
                state, scratch, begin = fixture(Code.BLOCK if commit else Code.REP, commit=commit,
                                                block=2, raw_stage=255, energy=energy)
                image = make_teaching_image(begin.service, begin.argument)
                f = 64 if commit else 8
                p = (1, 1, 1, 1) if commit else (0, 0, 0, 0)
                start, stride, kernel_start = (18, 13, 1) if commit else (13, 8, 0)

                def checked(s, current, local_remainder=meter.ZERO, public_tail=meter.ZERO, residue=1):
                    pc = scratch.read_bits(224, 16)
                    self.assertEqual(public_tail, tail)
                    self.assertTrue(meter.require_cost(s, current, local_remainder, tail))
                    if start <= pc < start + n * stride:
                        i, offset = divmod(pc - start, stride)
                        base = meter.Cost((n - i - 1) * (g + 128) + f, p)
                        if kernel_start <= offset < kernel_start + g:
                            generation_left = g - (offset - kernel_start) - 1
                            self.assertEqual(local_remainder, meter.add_cost(base, meter.Cost(128 + generation_left)))
                        elif pc in image.cell_branches:
                            self.assertEqual(local_remainder, meter.Cost(f, p) if i == count else
                                             meter.add_cost(base, meter.Cost(23, (0, 0, 1, 0))))
                        elif offset == stride - 1:
                            self.assertEqual(local_remainder, base)
                    return original(s, current, local_remainder, public_tail, residue)

                with patch.object(meter, "debit", side_effect=checked):
                    result = (run_commit(state, scratch, begin, Code.BLOCK, tail) if commit else
                              run_lesson(state, scratch, begin, Code.REP, (8, 1), tail))
                self.assertEqual(result.vaw[2], count)
                meter.debit(state, tail)
                self.assertGreaterEqual(state.energy, 1)

    def test_commit_only_paid_two_bit_reads_clear_paid_before_s_no_pc_restore(self):
        original_read, original_write = State.read_bits, Scratch.write_bits
        original_clear = Scratch.clear
        for raw in (0, 15, 255):
            state, scratch, begin = fixture(commit=True, block=3, raw_stage=raw)
            cleared = []

            def read(s, offset, width, signed=False):
                self.assertEqual(width, 2)
                self.assertIn(offset, (1760, 1762, 1764, 1766))
                return original_read(s, offset, width, signed)

            def clear(d):
                self.assertEqual(state.snapshot()[220], 0)
                self.assertEqual(state.energy, 65535 - (3756 if raw == 255 else 616))
                cleared.append(True)
                return original_clear(d)

            def put(d, offset, width, value, signed=False):
                self.assertFalse(cleared, "scratch written after S")
                return original_write(d, offset, width, value, signed)

            with patch.object(State, "read_bits", read), patch.object(Scratch, "clear", clear), \
                    patch.object(Scratch, "write_bits", put):
                run_commit(state, scratch, begin, Code.BLOCK)
            self.assertEqual(cleared, [True])
            self.assertTrue(scratch.is_zero())


if __name__ == "__main__":
    unittest.main()