"""Constructed ADMIT fixtures only; byte oracles/mocks are external observers."""

from copy import copy
from typing import Any, cast
import unittest
from unittest.mock import patch

from e3 import admission, machine, meter
from e3.admission import AdmissionFailure, run_admit
from e3.machine import Charge, Opcode, StepResult, StepStatus
from e3.protocol import BeginFrame, Phase, ScalarTag, Service
from e3.services import EventKind, ServiceEvent, ServiceStatus
from e3.state import Scratch, State


def fixture(energy=65535, material=(255, 255, 255, 255), tick=1,
            phase=Phase.DEVELOPMENT):
    raw = bytearray((37 * i + 19) % 256 for i in range(276))
    raw[225:227], raw[227:231] = energy.to_bytes(2, "little"), bytes(material)
    state, scratch = State(raw), Scratch()
    begin = BeginFrame(phase, tick, Service.ADMIT, (tick - 1) % 5,
                       4 if tick >= 6 else 0, state.snapshot())
    return state, scratch, begin


def paid(result):
    total = meter.ZERO
    for event in result.trace:
        total = meter.add_cost(total, event.paid)
    return total


class TestAdmission(unittest.TestCase):
    def test_all_cues_slots_exact_bytes_and_literal_counts(self):
        for cue in range(16):
            for slot in range(5):
                with self.subTest(cue=cue, slot=slot):
                    state, scratch, begin = fixture(tick=slot + 1)
                    expected = bytearray(begin.state)
                    expected[212 + slot] = (cue << 1) | 1
                    expected[225:227], expected[227:231] = (65086).to_bytes(2, "little"), bytes([254] * 4)
                    with patch.object(State, "read_lane", side_effect=AssertionError("unpaid slot read")):
                        result = run_admit(state, scratch, begin, cue)
                    self.assertEqual(state.snapshot(), bytes(expected))
                    self.assertEqual(scratch.snapshot(), bytes(32))
                    self.assertIs(result.status, ServiceStatus.EXIT)
                    self.assertEqual(paid(result), meter.Cost(449, (1, 1, 1, 1)))
                    steps = [e for e in result.trace if isinstance(e, StepResult)]
                    self.assertEqual([e.pc for e in steps], list(range(16)))
                    self.assertEqual(sum(e.charge is Charge.CONTROL_A for e in steps), 11)
                    self.assertFalse(any(e.opcode in (Opcode.READ2, Opcode.PAD) for e in steps))
                    self.assertFalse(any(e.charge is Charge.KERNEL for e in steps))
                    writes = [e for e in steps if e.opcode is Opcode.WRITE2]
                    self.assertEqual([e.lane for e in writes], list(range(848 + 4 * slot, 852 + 4 * slot)))
                    for k, e in enumerate(writes):
                        self.assertEqual(e.value, (((cue << 1) | 1) >> (2 * k)) & 3)
                        self.assertEqual(e.paid, meter.Cost(14, (int(k == 0), int(k == 1),
                                                               int(k == 2), int(k == 3))))
                    primitives = [e for e in result.trace if isinstance(e, ServiceEvent)]
                    self.assertEqual([e.kind for e in primitives], [EventKind.METER, EventKind.CONTROL, EventKind.SCALAR])
                    self.assertEqual(primitives[0].outcome, meter.GateResult(True, True))
                    self.assertEqual(primitives[-1].scalar, admission.scalar_from_value(ScalarTag.ADMIT_CUE, cue))
                    self.assertEqual([e.paid.energy for e in primitives], [128, 256, 1])
                    self.assertEqual(len(result.trace), 19)
                    self.assertIs(steps[-1].status, StepStatus.HALT)
                    self.assertIsNone(steps[-1].next_pc)

    def test_thresholds_and_rejection_never_consume_cue(self):
        for energy, admitted, remaining in ((137, False, 1), (449, False, 313), (450, True, 1)):
            state, scratch, begin = fixture(energy, (1,) * 4)
            result = run_admit(state, scratch, begin, 15 if admitted else None)
            self.assertEqual(state.energy, remaining)
            self.assertIs(result.status, ServiceStatus.EXIT)
            outer = result.trace[0]
            assert isinstance(outer, ServiceEvent)
            self.assertEqual(outer.outcome, meter.GateResult(True, admitted))
            self.assertEqual(paid(result), meter.Cost(449, (1, 1, 1, 1)) if admitted else meter.Cost(136))
            self.assertTrue(scratch.is_zero())
            if not admitted:
                _, exit_event = result.trace
                assert isinstance(exit_event, ServiceEvent)
                self.assertEqual([outer.kind, exit_event.kind], [EventKind.METER, EventKind.S])
                self.assertEqual(state.snapshot()[:225], begin.state[:225])

    def test_minimum_failure_sinks_only_energy_without_s_or_c(self):
        for energy, material, tail in ((0, (1,) * 4, meter.ZERO), (136, (1,) * 4, meter.ZERO),
                                       (65535, (0,) * 4, meter.Cost(0, (1, 0, 0, 0)))):
            state, scratch, begin = fixture(energy, material)
            expected = bytearray(begin.state)
            expected[225:227] = bytes(2)
            with patch.object(Scratch, "clear", side_effect=AssertionError("unpaid S")), \
                    patch.object(machine, "_step", side_effect=AssertionError("unpaid C")):
                result = run_admit(state, scratch, begin, None, tail)
            self.assertIs(result.status, ServiceStatus.SHUTDOWN)
            self.assertEqual(paid(result), meter.ZERO)
            outer = result.trace[0]
            assert isinstance(outer, ServiceEvent)
            self.assertEqual(outer.outcome, meter.GateResult(False, False, energy))
            self.assertEqual(len(result.trace), 1)
            self.assertEqual(state.snapshot(), bytes(expected))
            self.assertTrue(scratch.is_zero())

    def test_source_holes_and_public_tail_protection(self):
        for j in range(4):
            for with_tail in (False, True):
                material = [255] * 4
                material[j] = int(with_tail)
                tail = meter.Cost(0, (int(j == 0 and with_tail), int(j == 1 and with_tail),
                                      int(j == 2 and with_tail), int(j == 3 and with_tail)))
                state, scratch, begin = fixture(material=material)
                with patch.object(admission, "scalar_from_value", side_effect=AssertionError("early cue")), \
                        patch.object(State, "write_lane", side_effect=AssertionError("rejected write")):
                    result = run_admit(state, scratch, begin, cast(Any, object()), tail)
                self.assertEqual(paid(result), meter.Cost(136))
                self.assertEqual(state.snapshot()[227:231], bytes(material))
                outer = result.trace[0]
                assert isinstance(outer, ServiceEvent)
                self.assertEqual(outer.outcome, meter.GateResult(True, False))

    def test_whole_service_quote_overflow_is_atomic_before_any_gate(self):
        maximum = meter.INT32_MAX
        self.assertEqual(admission._FULL, meter.Cost(449, (1, 1, 1, 1)))

        def source_tails(amount):
            return [meter.Cost(0, material) for material in (
                (amount, 0, 0, 0), (0, amount, 0, 0),
                (0, 0, amount, 0), (0, 0, 0, amount),
                (amount, amount, amount, amount),
            )]

        # All 128 missed values, including MAX-445 and the exact MAX-322 repro;
        # MAX-321 and MAX also must fail before gate, not as AdmissionFailure.
        invalid = [meter.Cost(maximum - offset) for offset in range(449, 320, -1)]
        invalid += [meter.Cost(maximum), *source_tails(maximum)]
        valid = [meter.Cost(maximum - 451), meter.Cost(maximum - 450),
                 *source_tails(maximum - 1),
                 meter.Cost(maximum - 450, (maximum - 1, maximum - 1,
                                           maximum - 1, maximum - 1))]
        with patch.object(meter, "debit", side_effect=AssertionError("unexpected debit")), \
                patch.object(admission, "scalar_from_value", side_effect=AssertionError("early cue")), \
                patch.object(machine, "_step", side_effect=AssertionError("unexpected payload")), \
                patch.object(Scratch, "clear", side_effect=AssertionError("fake S")):
            for slot in range(5):
                for energy in (0, 450):
                    for tail in invalid:
                        with self.subTest(slot=slot, energy=energy, tail=tail, invalid=True):
                            state, scratch, begin = fixture(energy, (1, 1, 1, 1), slot + 1)
                            before = state.snapshot(), scratch.snapshot()
                            with patch.object(meter, "gate", side_effect=AssertionError("early gate")), \
                                    self.assertRaises(OverflowError):
                                run_admit(state, scratch, begin, None, tail)
                            self.assertEqual((state.snapshot(), scratch.snapshot()), before)
                    for tail in valid:
                        with self.subTest(slot=slot, energy=energy, tail=tail, invalid=False):
                            state, scratch, begin = fixture(energy, (1, 1, 1, 1), slot + 1)
                            before_scratch = scratch.snapshot()
                            expected = bytearray(state.snapshot())
                            expected[225:227] = bytes(2)
                            result = run_admit(state, scratch, begin, None, tail)
                            self.assertIs(result.status, ServiceStatus.SHUTDOWN)
                            self.assertEqual(paid(result), meter.ZERO)
                            self.assertEqual(len(result.trace), 1)
                            outer = result.trace[0]
                            assert isinstance(outer, ServiceEvent)
                            self.assertIs(outer.kind, EventKind.METER)
                            self.assertEqual(outer.outcome, meter.GateResult(False, False, energy))
                            self.assertEqual((state.snapshot(), scratch.snapshot()),
                                             (bytes(expected), before_scratch))

    def test_every_debit_retains_exact_sourcewise_suffix_and_tail(self):
        tail = meter.Cost(73, (2, 3, 4, 5))
        state, scratch, begin = fixture(523, (3, 4, 5, 6))
        debit = meter.debit

        def checked(s, c, local=meter.ZERO, public_tail=meter.ZERO, residue=1):
            self.assertEqual(public_tail, tail)
            self.assertEqual(meter.Cost(s.energy, (s.P0, s.P1, s.P2, s.P3)),
                             meter.floor_quote(c, local, public_tail, residue))
            return debit(s, c, local, public_tail, residue)

        with patch.object(meter, "debit", side_effect=checked):
            run_admit(state, scratch, begin, 6, tail)
        meter.debit(state, tail)
        self.assertEqual((state.energy, state.P0, state.P1, state.P2, state.P3), (1, 0, 0, 0, 0))

    def test_scalar_is_paid_once_into_r0_after_c_before_alu(self):
        state, scratch, begin = fixture(450, (1,) * 4)
        encode, write = admission.scalar_from_value, Scratch.write_bits
        seen = []

        def scalar(tag, value):
            self.assertEqual((state.energy, scratch.read_bits(224, 16)), (65, 1))
            return encode(tag, value)

        def put(s, offset, width, value, signed=False):
            if offset == 96:
                seen.append((state.energy, width, value))
            return write(s, offset, width, value, signed)

        with patch.object(admission, "scalar_from_value", side_effect=scalar) as received, \
                patch.object(Scratch, "write_bits", put), \
                patch.object(machine, "execute", side_effect=AssertionError("second C")), \
                patch.object(machine, "step", side_effect=AssertionError("unpaid public step")):
            run_admit(state, scratch, begin, 11)
        received.assert_called_once_with(ScalarTag.ADMIT_CUE, 11)
        self.assertEqual(seen, [(65, 32, 11), (65, 32, 22), (65, 32, 23)])

    def test_malformed_admitted_cue_has_only_actual_paid_prefix_no_cleanup(self):
        invalid_cues: tuple[Any, ...] = (None, True, False, -1, 16, 1.0, "1", (1,), object())
        for cue in invalid_cues:
            state, scratch, begin = fixture(450, (1,) * 4)
            with patch.object(Scratch, "clear", side_effect=AssertionError("technical S")), \
                    self.assertRaises(AdmissionFailure) as caught:
                run_admit(state, scratch, begin, cue)
            prefix = caught.exception.prefix
            self.assertIs(prefix.status, ServiceStatus.INTERRUPTED)
            self.assertEqual(paid(prefix), meter.Cost(384))
            self.assertEqual(state.energy, 66)
            self.assertEqual(state.snapshot()[:225], begin.state[:225])
            self.assertEqual(state.snapshot()[227:], begin.state[227:])
            self.assertEqual(scratch.read_bits(224, 16), 1)
            self.assertEqual(scratch.read_bits(96, 32), 0)
            self.assertEqual(len(prefix.trace), 3)

    def test_valid_phases_last_admissions_and_drain_declarations(self):
        for phase, last in ((Phase.DEVELOPMENT, 2043), (Phase.ASSAY, 256), (Phase.ECOLOGY, 507)):
            state, scratch, begin = fixture(tick=last, phase=phase)
            self.assertIs(run_admit(state, scratch, begin, 0).status, ServiceStatus.EXIT)
            for tick in range(last + 1, last + 6):
                with self.assertRaises(ValueError):
                    fixture(tick=tick, phase=phase)

    def test_bad_entry_is_atomic_before_meter(self):
        for field, value in (("service", Service.TICK), ("phase", Phase.RECOVERY),
                             ("phase", Phase.ACQUISITION), ("phase", Phase.ORACLE),
                             ("argument", 1), ("planned_tick", 2044), ("mask", 4),
                             ("state", bytes(276)), ("abi", 8), ("scratch", 1),
                             ("state_type", None), ("scratch_type", None),
                             ("begin_type", None), ("tail", None),
                             ("tail", meter.Cost(meter.INT32_MAX))):
            state, scratch, original = fixture()
            begin, tail = copy(original), meter.ZERO
            if field == "scratch":
                scratch.write_bits(255, 1, 1)
            elif field == "tail":
                tail = value
            elif not field.endswith("_type"):
                object.__setattr__(begin, field, value)
            before = state.snapshot(), scratch.snapshot()
            args: tuple[Any, ...] = (
                None if field == "state_type" else state,
                None if field == "scratch_type" else scratch,
                None if field == "begin_type" else begin, 0, tail,
            )
            with self.assertRaises((TypeError, ValueError, OverflowError, AdmissionFailure)):
                run_admit(*args)
            self.assertEqual((state.snapshot(), scratch.snapshot()), before)


if __name__ == "__main__":
    unittest.main()