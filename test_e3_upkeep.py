"""Finite constructed paid AGE/ISOLATE fixtures, not full-service conformance.

Byte oracles and callbacks here are TEST observers only. No target/root draw,
production callback, experiment, freeze, archive, scheduler or CONDITION/TICK.
"""

from collections import Counter
from dataclasses import FrozenInstanceError, fields, replace
import inspect
from typing import Any, cast
import unittest
from unittest.mock import patch

from e3 import machine, meter, physical, upkeep
from e3.machine import Charge, Opcode, Operand, OperandKind
from e3.protocol import Service
from e3.state import Scratch, State
from e3.upkeep import UpkeepStatus, make_upkeep_program, run_upkeep


SERVICES = (Service.AGE_LOW, Service.AGE_HIGH, Service.ISOLATE)


def fixture(energy=65535, material=(255, 255, 255, 255), pattern=None):
    # Includes noncanonical code, metadata, reserved TD bits and reserve.
    raw = bytearray((i * 37 + 19) % 256 for i in range(276))
    if pattern is not None:
        raw[:] = bytes([pattern]) * 276
    raw[225:227] = energy.to_bytes(2, "little")
    raw[227:231] = bytes(material)
    return State(raw), Scratch()


def stocks(state):
    return state.energy, state.P0, state.P1, state.P2, state.P3


def price(service):
    return (meter.Cost(1120, (13, 13, 13, 13)) if service is Service.ISOLATE
            else meter.Cost(952, (5, 5, 5, 5)))


def source_unit(hub: int) -> meter.Material4:
    return int(hub == 0), int(hub == 1), int(hub == 2), int(hub == 3)


def expected_image(before, service):
    # Independent byte/nibble oracle, never called by the service compiler.
    raw = bytearray(before)
    cost = price(service)
    raw[225:227] = (int.from_bytes(raw[225:227], "little") - cost.energy).to_bytes(2, "little")
    raw[227:231] = bytes(raw[227 + j] - cost.material[j] for j in range(4))
    if service is Service.ISOLATE:
        raw[212:225] = bytes(13)
    else:
        first = 0 if service is Service.AGE_LOW else 10
        for d in range(first, first + 10):
            byte, shift = 231 + d // 2, 4 * (d % 2)
            old = (before[byte] >> shift) & 15
            raw[byte] = (raw[byte] & ~(15 << shift)) | (min(old + 1, 15) << shift)
    return bytes(raw)


def total_paid(result):
    total = result.outer_meter.paid
    if result.trace is not None:
        for event in (*result.trace.envelopes, *result.trace.steps):
            total = meter.add_cost(total, event.paid)
    return total


class TestMandatoryUpkeep(unittest.TestCase):
    def test_exact_immutable_rom_counts_and_forward_targets(self):
        for service in SERVICES:
            program = make_upkeep_program(service)
            self.assertEqual(program, make_upkeep_program(service))
            self.assertIsNot(program, make_upkeep_program(service))
            self.assertEqual(program.base, 0)
            control, kernel, reads, writes = ((59, 0, 0, 52) if service is Service.ISOLATE
                                             else (63, 80, 20, 20))
            proof = machine.validate(program)
            self.assertEqual(proof.regions, (Charge.CONTROL_A,))
            self.assertEqual(proof.control_path_bound, (control, 0))
            self.assertEqual(proof.max_steps, control + kernel + reads + writes + 1)
            self.assertEqual(len(program.instructions), proof.max_steps)
            self.assertLess(len(program.instructions), 192)
            with self.assertRaises(FrozenInstanceError):
                setattr(program, "base", 1)
            for pc, ins in enumerate(program.instructions):
                assert ins is not None
                if ins.opcode in (Opcode.STAGE, Opcode.BR):
                    self.assertEqual(ins.target, pc + 1)
                if ins.opcode is Opcode.BR:
                    self.assertEqual(ins.args, (machine.immediate(1, 1),))
                self.assertNotIn(ins.opcode, (Opcode.PAD, Opcode.JUMP))
                for arg in (*ins.args, ins.dst, ins.capture):
                    if arg is not None:
                        self.assertLessEqual(arg.width, 32)
                        if arg.kind is OperandKind.D:
                            self.assertLessEqual(arg.offset + arg.width, 14)

    def test_age_literal_eight_op_kernel_and_fixed_lane_pairing(self):
        for service, first in ((Service.AGE_LOW, 0), (Service.AGE_HIGH, 10)):
            program = make_upkeep_program(service)
            sites = tuple(ins for ins in program.instructions if ins is not None)
            self.assertEqual(len(sites), len(program.instructions))
            for i, d in enumerate(range(first, first + 10)):
                word = sites[1 + 18 * i:1 + 18 * (i + 1)]
                self.assertEqual(tuple(ins.opcode for ins in word[6:14]),
                                 (Opcode.EX, Opcode.EX, Opcode.SHL, Opcode.XOR,
                                  Opcode.EQ, Opcode.ADD, Opcode.SELECT, Opcode.AND))
                self.assertEqual(word[0].dst, Operand(OperandKind.D, 4, 5))
                self.assertEqual(word[0].args[0].value, d)
                self.assertEqual(tuple(word[k].args[0].value for k in (1, 3, 14, 16)),
                                 (924 + 2 * d, 925 + 2 * d) * 2)
                self.assertEqual(word[2].capture, Operand(OperandKind.D, 0, 2))
                self.assertEqual(word[4].capture, Operand(OperandKind.D, 2, 2))
                self.assertEqual(word[13].dst, Operand(OperandKind.D, 10, 4))

    def test_every_four_bit_age_at_every_domain_and_untouched_neighbors(self):
        for service in (Service.AGE_LOW, Service.AGE_HIGH):
            for offset in range(16):
                state, scratch = fixture()
                # Each domain sees all 16 raw encodings across these fixtures;
                # adjacent nibbles differ, exposing accidental wide overwrites.
                for d in range(20):
                    state.write_bits(1848 + 4 * d, 4, (offset + 7 * d) % 16)
                before = state.snapshot()
                result = run_upkeep(service, state, scratch, public_tail=meter.ZERO)
                self.assertIs(result.status, UpkeepStatus.EXIT)
                self.assertEqual(state.snapshot(), expected_image(before, service))
                self.assertEqual(scratch.snapshot(), bytes(32))
                self.assertEqual(total_paid(result), price(service))

    def test_all_raw_byte_patterns_isolate_only_clears_52_lanes(self):
        for value in range(256):
            state, scratch = fixture(pattern=value)
            before = state.snapshot()
            result = run_upkeep(Service.ISOLATE, state, scratch, public_tail=meter.ZERO)
            self.assertEqual(state.snapshot(), expected_image(before, Service.ISOLATE))
            self.assertEqual(total_paid(result), price(Service.ISOLATE))
            self.assertEqual(scratch.snapshot(), bytes(32))

    def test_actual_traces_routed_prices_source_vectors_and_paid_s(self):
        for service in SERVICES:
            state, scratch = fixture()
            result = run_upkeep(service, state, scratch, public_tail=meter.ZERO)
            self.assertEqual(result.outer_meter.outcome, meter.GateResult(True, True))
            self.assertEqual(result.outer_meter.paid, meter.Cost(128))
            trace = result.trace
            assert trace is not None
            self.assertIs(trace.mode, machine.ExecutionMode.ENGINEERING_FRAGMENT)
            self.assertEqual(trace.envelopes, (machine.EnvelopePayment(Charge.CONTROL_A,
                                                                      meter.Cost(256)),))
            counts = Counter(e.opcode for e in trace.steps)
            is_isolate = service is Service.ISOLATE
            self.assertEqual(counts[Opcode.READ2], 0 if is_isolate else 20)
            self.assertEqual(counts[Opcode.WRITE2], 52 if is_isolate else 20)
            self.assertEqual(Counter(e.charge for e in trace.steps)[Charge.KERNEL],
                             0 if is_isolate else 80)
            self.assertEqual(Counter(e.charge for e in trace.steps)[Charge.CONTROL_A],
                             59 if is_isolate else 63)
            writes = [e for e in trace.steps if e.opcode is Opcode.WRITE2]
            first, last = ((848, 900) if is_isolate else
                           (924, 944) if service is Service.AGE_LOW else (944, 964))
            self.assertEqual(tuple(e.lane for e in writes), tuple(range(first, last)))
            for event in trace.steps:
                if event.opcode is Opcode.READ2:
                    self.assertEqual(event.paid, meter.Cost(10))
                elif event.opcode is Opcode.WRITE2:
                    assert event.lane is not None
                    self.assertEqual(event.paid, meter.Cost(14, source_unit(event.lane % 4)))
                elif event.charge is Charge.CONTROL_A:
                    self.assertEqual(event.paid, meter.ZERO)
                elif event.charge is Charge.KERNEL:
                    self.assertEqual(event.paid, meter.Cost(1))
            self.assertIs(trace.steps[-1].opcode, Opcode.S)
            self.assertIs(trace.steps[-1].status, machine.StepStatus.HALT)
            self.assertIsNone(trace.steps[-1].next_pc)
            self.assertEqual(trace.steps[-1].paid, meter.Cost(8))
            self.assertEqual(total_paid(result), price(service))

    def test_exact_price_plus_tail_plus_one_and_material_equality(self):
        for service in SERVICES:
            for tail in (meter.ZERO, meter.Cost(137, (1, 2, 3, 4))):
                cost = price(service)
                required = meter.floor_quote(cost, public_tail=tail)
                state, scratch = fixture(required.energy, required.material)
                result = run_upkeep(service, state, scratch, public_tail=tail)
                self.assertIs(result.status, UpkeepStatus.EXIT)
                self.assertEqual(stocks(state), (tail.energy + 1, *tail.material))
                self.assertEqual(scratch.snapshot(), bytes(32))
                meter.debit(state, tail)
                self.assertEqual(stocks(state), (1, 0, 0, 0, 0))

    def test_full_mandatory_suffix_stays_funded_at_every_actual_debit(self):
        for service in SERVICES:
            tail = meter.Cost(83, (4, 1, 3, 2))
            required = meter.floor_quote(price(service), public_tail=tail)
            state, scratch = fixture(required.energy, required.material)
            actual_debit = meter.debit
            before_each = []

            def debit(s, cost, local=meter.ZERO, public_tail=meter.ZERO, residue=1):
                before_each.append(meter.Cost(s.energy, (s.P0, s.P1, s.P2, s.P3)))
                return actual_debit(s, cost, local, public_tail, residue)

            with patch.object(meter, "debit", side_effect=debit):
                result = run_upkeep(service, state, scratch, public_tail=tail)
            assert result.trace is not None
            events = (*result.trace.envelopes, *result.trace.steps)
            self.assertEqual(len(before_each), len(events))
            # Pure POST-execution observer reduction, not worker fuel/history.
            remaining = meter.floor_quote(tail)
            for before, event in zip(reversed(before_each), reversed(events)):
                remaining = meter.add_cost(remaining, event.paid)
                self.assertEqual(before, remaining)
            self.assertEqual(remaining, meter.sub_cost(required, meter.FEE))

    def test_saturation_and_same_value_zero_writes_never_skip_paid_work(self):
        for service in SERVICES:
            traces = []
            for pattern in (0, 255):
                state, scratch = fixture(pattern=pattern)
                before = state.snapshot()
                result = run_upkeep(service, state, scratch, public_tail=meter.ZERO)
                self.assertEqual(state.snapshot(), expected_image(before, service))
                self.assertEqual(total_paid(result), price(service))
                assert result.trace is not None
                traces.append(tuple((e.pc, e.opcode, e.charge, e.paid, e.lane)
                                    for e in result.trace.steps))
                if pattern == 255 and service is not Service.ISOLATE:
                    self.assertEqual([e.value for e in result.trace.steps if e.opcode is Opcode.ADD],
                                     [16] * 10)
                    self.assertEqual([e.value for e in result.trace.steps if e.opcode is Opcode.SELECT],
                                     [15] * 10)
            self.assertEqual(*traces)

    def test_unfunded_full_minimum_shuts_down_before_fee_alu_or_ram(self):
        for service in SERVICES:
            cost = price(service)
            cases = [(0, (255,) * 4, meter.ZERO), (cost.energy, (255,) * 4, meter.ZERO),
                     (cost.energy + 20, (255,) * 4, meter.Cost(20))]
            for hub in range(4):
                material = [255] * 4
                material[hub] = cost.material[hub] - 1
                cases.append((65535, tuple(material), meter.ZERO))
                material[hub] = cost.material[hub]
                tail = meter.Cost(0, source_unit(hub))
                cases.append((65535, tuple(material), tail))
            for energy, material, tail in cases:
                state, scratch = fixture(energy, material)
                expected = bytearray(state.snapshot())
                expected[225:227] = bytes(2)
                with patch.object(machine, "execute", side_effect=AssertionError("execution")), \
                        patch.object(State, "read_lane", side_effect=AssertionError("RAM read")), \
                        patch.object(State, "write_lane", side_effect=AssertionError("RAM write")), \
                        patch.object(Scratch, "clear", side_effect=AssertionError("free clear")), \
                        patch.object(Scratch, "write_bits", side_effect=AssertionError("scratch write")):
                    result = run_upkeep(service, state, scratch, public_tail=tail)
                self.assertIs(result.status, UpkeepStatus.SHUTDOWN)
                self.assertEqual(result.outer_meter.outcome, meter.GateResult(False, False, energy))
                self.assertEqual(total_paid(result), meter.ZERO)
                self.assertIsNone(result.trace)
                self.assertEqual(state.snapshot(), bytes(expected))
                self.assertTrue(scratch.is_zero())

    def test_full_sourcewise_quote_precedes_any_discovery_and_debits_precede_io(self):
        for service in SERVICES:
            state, scratch = fixture()
            expected = stocks(state)
            calls = []
            actual_debit, actual_gate = meter.debit, meter.gate
            actual_read, actual_write = State.read_lane, State.write_lane

            def gate(s, body, *args, **kwargs):
                self.assertEqual(body, meter.sub_cost(price(service), meter.FEE))
                self.assertEqual(kwargs["minimum_exit"], body)
                self.assertIs(kwargs["public_tail"], tail)
                self.assertEqual(calls, [])
                answer = actual_gate(s, body, *args, **kwargs)
                calls.append("M")
                return answer

            def debit(s, cost, local=meter.ZERO, public_tail=meter.ZERO, residue=1):
                nonlocal expected
                self.assertEqual(calls[0], "M")
                self.assertIs(public_tail, tail)
                paid = actual_debit(s, cost, local, public_tail, residue)
                expected = stocks(s)
                calls.append(cost)
                return paid

            def read(s, lane):
                self.assertEqual(stocks(s), expected)
                self.assertEqual(calls[-1], meter.Cost(10))
                return actual_read(s, lane)

            def write(s, lane, value):
                self.assertEqual(stocks(s), expected)
                self.assertEqual(calls[-1], meter.Cost(14, source_unit(lane % 4)))
                return actual_write(s, lane, value)

            tail = meter.Cost(37, (1, 2, 3, 4))
            with patch.object(meter, "gate", side_effect=gate), \
                    patch.object(meter, "debit", side_effect=debit), \
                    patch.object(State, "read_lane", read), patch.object(State, "write_lane", write), \
                    patch.object(physical, "read_age", side_effect=AssertionError("age sensor")), \
                    patch.object(physical, "write_age", side_effect=AssertionError("free increment")), \
                    patch.object(State, "snapshot", side_effect=AssertionError("snapshot")):
                result = run_upkeep(service, state, scratch, public_tail=tail)
            self.assertEqual(calls[:2], ["M", meter.Cost(256)])
            self.assertEqual(total_paid(result), price(service))

    def test_pre_s_is_dirty_and_only_actual_s_clears_all_bits(self):
        for service in SERVICES:
            state, scratch = fixture()
            actual_clear = Scratch.clear
            seen = []

            def clear(s):
                self.assertFalse(s.is_zero())
                self.assertEqual(state.energy, 65535 - price(service).energy)
                seen.append(s.snapshot())
                actual_clear(s)

            with patch.object(Scratch, "clear", clear):
                run_upkeep(service, state, scratch, public_tail=meter.ZERO)
            self.assertEqual(len(seen), 1)
            self.assertEqual(scratch.snapshot(), bytes(32))

    def test_dirty_scratch_in_every_partition_is_predebit_technical_error(self):
        for service in SERVICES:
            for bit in (0, 95, 96, 127, 128, 159, 160, 191, 192, 223, 224, 239, 240, 250, 251, 255):
                state, scratch = fixture()
                scratch.write_bits(bit, 1, 1)
                before = state.snapshot(), scratch.snapshot()
                with patch.object(meter, "gate", side_effect=AssertionError("paid too soon")):
                    with self.assertRaises(ValueError):
                        run_upkeep(service, state, scratch, public_tail=meter.ZERO)
                self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_invalid_public_fields_tail_types_and_overflow_are_atomic(self):
        malformed = meter.Cost()
        object.__setattr__(malformed, "material", (0, 0, 0, True))
        bad_services = (None, True, 9, "AGE_LOW", lambda: Service.AGE_LOW,
                        Service.CONDITION, Service.TICK, Service.TEMPLATE)
        bad_tails = (None, True, 0, {}, (1, 0, 0, 0, 0), lambda: meter.ZERO,
                     malformed, meter.Cost(meter.INT32_MAX),
                     meter.Cost(0, (0, 0, 0, meter.INT32_MAX)))
        for service, tail in ([(s, meter.ZERO) for s in bad_services]
                              + [(s, t) for s in SERVICES for t in bad_tails]):
            state, scratch = fixture()
            before = state.snapshot(), scratch.snapshot()
            with self.assertRaises((TypeError, ValueError, OverflowError)):
                run_upkeep(cast(Any, service), state, scratch, public_tail=cast(Any, tail))
            self.assertEqual((state.snapshot(), scratch.snapshot()), before)
        for service in bad_services:
            with self.assertRaises((TypeError, ValueError)):
                make_upkeep_program(cast(Any, service))

    def test_exact_containers_no_custom_program_callback_context_or_resume_inputs(self):
        # Deliberately bypass @final ONLY to exercise runtime exact-type checks.
        StateProxy = type("StateProxy", (State,), {})
        ScratchProxy = type("ScratchProxy", (Scratch,), {})
        state, scratch = fixture()
        before = state.snapshot(), scratch.snapshot()
        for s, w in ((StateProxy(), scratch), (state, ScratchProxy()),
                     (object(), scratch), (state, None)):
            with self.assertRaises(TypeError):
                run_upkeep(Service.ISOLATE, cast(Any, s), cast(Any, w), public_tail=meter.ZERO)
        for name in ("program", "callback", "context", "custody", "receipt", "resume",
                     "target", "domain", "local_remainders"):
            with self.assertRaises(TypeError):
                cast(Any, run_upkeep)(Service.ISOLATE, state, scratch, public_tail=meter.ZERO,
                                     **{name: object()})
        with self.assertRaises(TypeError):
            cast(Any, run_upkeep)(Service.ISOLATE, state, scratch)
        self.assertEqual((state.snapshot(), scratch.snapshot()), before)
        self.assertEqual(tuple(inspect.signature(run_upkeep).parameters),
                         ("service", "state", "scratch", "public_tail"))

    def test_program_corruption_rejected_before_outer_fee(self):
        # Fault injection into a TEST compiler result: validation must precede M.
        program = make_upkeep_program(Service.AGE_LOW)
        ins = program.instructions[-1]
        assert ins is not None
        object.__setattr__(ins, "charge", Charge.KERNEL)
        state, scratch = fixture()
        before = state.snapshot(), scratch.snapshot()
        with patch.object(upkeep, "make_upkeep_program", return_value=program), \
                patch.object(meter, "gate", side_effect=AssertionError("paid too soon")):
            with self.assertRaises(ValueError):
                run_upkeep(Service.AGE_LOW, state, scratch, public_tail=meter.ZERO)
        self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_returned_program_is_not_reused_as_a_service_receipt(self):
        program = make_upkeep_program(Service.ISOLATE)
        first = program.instructions[0]
        assert first is not None
        object.__setattr__(program, "instructions", (replace(first, args=(machine.immediate(2, 16),)),
                                                     *program.instructions[1:]))
        state, scratch = fixture()
        result = run_upkeep(Service.ISOLATE, state, scratch, public_tail=meter.ZERO)
        assert result.trace is not None
        self.assertEqual(result.trace.steps[0].next_pc, 1)

    def test_technical_failure_keeps_paid_prefix_and_cannot_resume_dirty_scratch(self):
        state, scratch = fixture()
        before = state.snapshot()
        actual_write = State.write_lane
        count = 0

        def write(s, lane, value):
            nonlocal count
            count += 1
            if count == 2:
                raise ValueError("injected technical interruption, not physical death")
            actual_write(s, lane, value)

        with patch.object(State, "write_lane", write):
            with self.assertRaises(machine.FragmentFailure) as caught:
                run_upkeep(Service.ISOLATE, state, scratch, public_tail=meter.ZERO)
        self.assertIsInstance(caught.exception.__cause__, ValueError)
        self.assertEqual(state.energy, 65535 - 128 - 256 - 28)
        self.assertEqual((state.P0, state.P1, state.P2, state.P3), (254, 254, 255, 255))
        expected = bytearray(before)
        expected[212] &= ~3
        expected[225:227] = state.energy.to_bytes(2, "little")
        expected[227:231] = bytes((254, 254, 255, 255))
        self.assertEqual(state.snapshot(), bytes(expected))
        self.assertFalse(scratch.is_zero())
        self.assertNotIn(Opcode.S, [e.opcode for e in caught.exception.prefix.steps])
        damaged = state.snapshot(), scratch.snapshot()
        with self.assertRaises(ValueError):
            run_upkeep(Service.ISOLATE, state, scratch, public_tail=meter.ZERO)
        self.assertEqual((state.snapshot(), scratch.snapshot()), damaged)

    def test_observation_is_immutable_one_way_and_repeated_calls_pay_anew(self):
        state, scratch = fixture()
        result = run_upkeep(Service.AGE_LOW, state, scratch, public_tail=meter.ZERO)
        self.assertEqual({f.name for f in fields(result)}, {"service", "status", "outer_meter", "trace"})
        for obj, field in ((result, "trace"), (result.outer_meter, "paid")):
            self.assertFalse(hasattr(obj, "__dict__"))
            with self.assertRaises(FrozenInstanceError):
                setattr(obj, field, None)
        for s, w, tail in ((result, scratch, meter.ZERO), (state, result, meter.ZERO),
                           (state, scratch, result)):
            with self.assertRaises(TypeError):
                run_upkeep(Service.AGE_LOW, cast(Any, s), cast(Any, w), public_tail=cast(Any, tail))
        before = state.energy
        second = run_upkeep(Service.AGE_LOW, state, scratch, public_tail=meter.ZERO)
        self.assertEqual(before - state.energy, 952)
        self.assertEqual(total_paid(second), price(Service.AGE_LOW))
        self.assertEqual(len(State.__slots__), 1)
        self.assertEqual(len(Scratch.__slots__), 1)
        self.assertEqual(len(state.snapshot()), 276)
        self.assertEqual(len(scratch.snapshot()), 32)


if __name__ == "__main__":
    unittest.main()