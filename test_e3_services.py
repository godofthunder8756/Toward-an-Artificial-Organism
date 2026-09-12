"""Constructed service foundations only; no targets, experiment or full VM.

Snapshots, age oracles, mocks and trace reductions are TEST observers. Production
services cannot query these, keep their arrays or accept their callbacks.
"""

from collections import Counter
from dataclasses import FrozenInstanceError, fields
import inspect
from typing import Any, cast
import unittest
from unittest.mock import patch

from e3 import machine, meter, physical, services, upkeep
from e3.machine import Charge, Opcode, StepResult, StepStatus
from e3.protocol import ScalarTag, Service
from e3.services import (
    CurrentGrant, EventKind, MeterStage, ServiceEvent, ServiceFailure,
    ServiceStatus, run_condition, run_tick,
)
from e3.state import SCRATCH_PC_OFFSET, Scratch, State


def fixture(energy=65535, material=(255, 255, 255, 255)):
    raw = bytearray((i * 37 + 19) % 256 for i in range(276))
    raw[225:227] = energy.to_bytes(2, "little")
    raw[227:231] = bytes(material)
    return State(raw), Scratch()


def stocks(state):
    return meter.Cost(state.energy, (state.P0, state.P1, state.P2, state.P3))


def paid(result):
    total = meter.ZERO
    for event in result.trace:
        total = meter.add_cost(total, event.paid)
    return total


def vector(d):
    counts = [0, 0, 0, 0]
    for j in (d // 5, (924 + 2 * d) % 4, (925 + 2 * d) % 4):
        counts[j] += 1
    return tuple(counts)


def unit(j):
    return tuple(int(k == j) for k in range(4))


def gates(result):
    return [e for e in result.trace if isinstance(e, ServiceEvent)
            and e.kind is EventKind.METER and e.stage is not MeterStage.PASSIVE]


def condition_image(before, d, admitted):
    raw = bytearray(before)
    raw[225:227] = (int.from_bytes(raw[225:227], "little")
                    - (552 if admitted else 520)).to_bytes(2, "little")
    if admitted:
        raw[227:231] = bytes(raw[227 + j] - vector(d)[j] for j in range(4))
        raw[231 + d // 2] &= ~(15 << (4 * (d % 2)))
    return bytes(raw)


class TestTick(unittest.TestCase):
    def test_grant_caps_costs_and_nonresource_image_are_exact(self):
        cases = (
            (1, (0, 0, 0, 0), CurrentGrant(30000, (48,) * 4)),
            (65535, (255,) * 4, CurrentGrant(30000, (66,) * 4)),
            (50000, (254, 250, 100, 0), CurrentGrant(30000, (255,) * 4)),
            (178, (0,) * 4, CurrentGrant(0, (0,) * 4)),
            (1, (0,) * 4, CurrentGrant(30000, (255,) * 4)),
            (12345, (1, 2, 3, 4), CurrentGrant(30000, (0, 1, 2, 3))),
        )
        for energy, material, grant in cases:
            with self.subTest(energy=energy, material=material, grant=grant):
                state, scratch = fixture(energy, material)
                before = state.snapshot()
                a = min(grant.energy, 65535 - energy)
                p = tuple(min(grant.material[j], 255 - material[j]) for j in range(4))
                result = run_tick(state, scratch, grant, public_tail=meter.ZERO)
                self.assertIs(result.status, ServiceStatus.EXIT)
                self.assertEqual(paid(result), meter.Cost(177 + sum(p)))
                flow = result.trace[0]
                assert isinstance(flow, ServiceEvent) and flow.flows is not None
                self.assertEqual(flow.flows.accepted, meter.Cost(a, p))
                self.assertEqual(flow.flows.overflow,
                                 meter.Cost(grant.energy - a,
                                            tuple(grant.material[j] - p[j] for j in range(4))))
                self.assertEqual(flow.flows.ignored, meter.ZERO)
                expected = bytearray(before)
                expected[225:227] = (energy + a - 177 - sum(p)).to_bytes(2, "little")
                expected[227:231] = bytes(material[j] + p[j] for j in range(4))
                self.assertEqual(state.snapshot(), bytes(expected))
                self.assertEqual(scratch.snapshot(), bytes(32))

    def test_literal_closed_trace_zero_control_and_actual_scalar_encodings(self):
        state, scratch = fixture(1000, (0,) * 4)
        grant = CurrentGrant(0, (0, 1, 2, 3))
        actual_write = Scratch.write_bits
        scalar_seen = []

        def write(s, offset, width, value, signed=False):
            pc = s.read_bits(SCRATCH_PC_OFFSET, 16)
            if offset == 96:
                scalar_seen.append((pc, width, value, state.energy))
            return actual_write(s, offset, width, value, signed)

        with patch.object(Scratch, "write_bits", write), \
                patch.object(machine, "execute", side_effect=AssertionError("fake machine trace")), \
                patch.object(machine, "_step", side_effect=AssertionError("fake ALU")):
            result = run_tick(state, scratch, grant, public_tail=meter.ZERO)
        self.assertEqual([e.kind for e in result.trace],
                         [EventKind.METER] * 2 + [EventKind.SCALAR] * 5
                         + [EventKind.TRANSPORT] * 4
                         + [EventKind.LIVING, EventKind.RENT, EventKind.S])
        self.assertEqual([e.pc for e in result.trace], list(range(14)))
        self.assertEqual([e.next_pc for e in result.trace], [*range(1, 14), None])
        self.assertTrue(all(type(e) is ServiceEvent for e in result.trace))
        self.assertEqual(scalar_seen,
                         [(pc, 32, value, 1000 - 128 - (pc - 1))
                          for pc, value in enumerate((0, 0, 1, 2, 3), 2)])
        for i, event in enumerate(result.trace[2:7]):
            assert isinstance(event, ServiceEvent) and event.scalar is not None
            self.assertIs(event.scalar.tag, ScalarTag(i))
            self.assertEqual(event.scalar.width, 16 if i == 0 else 8)
            self.assertEqual(event.paid, meter.Cost(1))
        self.assertEqual([e.paid.energy for e in result.trace[7:11]], [0, 1, 2, 3])
        self.assertEqual([e.paid.energy for e in result.trace[11:]], [16, 20, 8])

    def test_every_uint8_material_offer_is_current_bounded_and_charged(self):
        for g in range(256):
            state, scratch = fixture(1, (0,) * 4)
            result = run_tick(state, scratch, CurrentGrant(30000, (g,) * 4),
                              public_tail=meter.ZERO)
            self.assertEqual(paid(result), meter.Cost(177 + 4 * g))
            self.assertEqual(stocks(state), meter.Cost(30001 - 177 - 4 * g, (g,) * 4))

    def test_minimum_entire_tick_plus_tail_plus_one_and_source_equality(self):
        tail = meter.Cost(123, (4, 3, 2, 1))
        state, scratch = fixture(1, (0,) * 4)
        result = run_tick(state, scratch, CurrentGrant(310, (4, 3, 2, 1)), public_tail=tail)
        self.assertEqual(paid(result), meter.Cost(187))
        self.assertEqual(stocks(state), meter.Cost(124, tail.material))
        meter.debit(state, tail)
        self.assertEqual(stocks(state), meter.Cost(1))

    def test_minimum_failure_retains_accepted_material_no_fictitious_fees_or_clear(self):
        cases = [(177, (0,) * 4, CurrentGrant(0, (0,) * 4), meter.ZERO),
                 (1, (0,) * 4, CurrentGrant(176, (0,) * 4), meter.ZERO),
                 (1, (0,) * 4, CurrentGrant(30000, (10, 20, 30, 40)),
                  meter.Cost(0, (11, 0, 0, 0))),
                 (1, (0,) * 4, CurrentGrant(30000, (0,) * 4), meter.Cost(30000))]
        for energy, material, grant, tail in cases:
            state, scratch = fixture(energy, material)
            expected = bytearray(state.snapshot())
            expected[225:227] = bytes(2)
            expected[227:231] = bytes(material[j] + grant.material[j] for j in range(4))
            with patch.object(Scratch, "clear", side_effect=AssertionError("unpaid S")), \
                    patch.object(meter, "debit", side_effect=AssertionError("unfunded work")):
                result = run_tick(state, scratch, grant, public_tail=tail)
            self.assertIs(result.status, ServiceStatus.SHUTDOWN)
            self.assertEqual(paid(result), meter.ZERO)
            self.assertEqual(len(result.trace), 2)
            self.assertEqual(gates(result)[0].outcome,
                             meter.GateResult(False, False, energy + grant.energy))
            self.assertEqual(state.snapshot(), bytes(expected))
            self.assertEqual(scratch.read_bits(224, 16), 1)
            for j in range(4):
                self.assertEqual(scratch.read_bits(8 * j, 8), grant.material[j])

    def test_initial_zero_ignores_every_quantity_without_reviving_or_scratch_mutation(self):
        for grant in (CurrentGrant(30000, (255,) * 4), CurrentGrant(0, (0,) * 4)):
            state, scratch = fixture(0, (0, 3, 7, 255))
            before = state.snapshot(), scratch.snapshot()
            with patch.object(meter, "gate", side_effect=AssertionError("dead admission")), \
                    patch.object(Scratch, "write_bits", side_effect=AssertionError("dead scratch")), \
                    patch.object(Scratch, "clear", side_effect=AssertionError("dead S")):
                result = run_tick(state, scratch, grant, public_tail=meter.ZERO)
            self.assertIs(result.status, ServiceStatus.SHUTDOWN)
            self.assertEqual(len(result.trace), 1)
            event = result.trace[0]
            assert isinstance(event, ServiceEvent)
            self.assertEqual(event.flows, meter.DepositResult(meter.ZERO, meter.ZERO,
                                                             meter.Cost(grant.energy, grant.material)))
            self.assertEqual((state.snapshot(), scratch.snapshot()), before)


class TestCondition(unittest.TestCase):
    def test_all_domains_all_age_encodings_exact_image_and_source_vectors(self):
        for d in range(20):
            for age in range(16):
                state, scratch = fixture()
                state.write_bits(1848 + 4 * d, 4, age)
                before = state.snapshot()
                with patch.object(physical, "read_age", side_effect=AssertionError("age read")), \
                        patch.object(physical, "write_age", side_effect=AssertionError("free reset")), \
                        patch.object(State, "read_lane", side_effect=AssertionError("RAM read")):
                    result = run_condition(d, state, scratch, public_tail=meter.ZERO)
                self.assertIs(result.status, ServiceStatus.EXIT)
                self.assertEqual(state.snapshot(), condition_image(before, d, True))
                self.assertEqual(paid(result), meter.Cost(552, vector(d)))
                self.assertEqual(scratch.snapshot(), bytes(32))

    def test_real_literal_control_9_or_5_and_only_two_machine_writes(self):
        for d in range(20):
            for admitted in (True, False):
                state, scratch = fixture(553 if admitted else 521)
                result = run_condition(d, state, scratch, public_tail=meter.ZERO)
                steps = [e for e in result.trace if isinstance(e, StepResult)]
                counts = Counter(e.charge for e in steps)
                self.assertEqual(counts[Charge.CONTROL_A], 9 if admitted else 5)
                self.assertEqual(counts[Charge.KERNEL], 0)
                self.assertEqual(counts[Charge.ACCESS], 2 if admitted else 0)
                self.assertEqual(counts[Charge.EXIT], 1)
                self.assertEqual([e.pc for e in steps],
                                 list(range(12)) if admitted else [0, 1, 2, 9, 10, 11])
                self.assertEqual(steps[2].next_pc, 3 if admitted else 9)
                self.assertEqual([e.lane for e in steps if e.opcode is Opcode.WRITE2],
                                 [924 + 2 * d, 925 + 2 * d] if admitted else [])
                for e in steps:
                    if e.opcode is Opcode.WRITE2:
                        self.assertEqual(e.value, 0)
                        self.assertEqual(e.paid, meter.Cost(14, unit(e.lane % 4)))
                    elif e.charge is Charge.CONTROL_A:
                        self.assertEqual(e.paid, meter.ZERO)
                self.assertIs(steps[-1].opcode, Opcode.S)
                self.assertIs(steps[-1].status, StepStatus.HALT)
                self.assertIsNone(steps[-1].next_pc)
                primitives = [e for e in result.trace if isinstance(e, ServiceEvent)]
                self.assertEqual([e.kind for e in primitives],
                                 [EventKind.METER, EventKind.CONTROL, EventKind.METER]
                                 + ([EventKind.DUES] if admitted else []))
                self.assertEqual([e.paid.energy for e in primitives],
                                 [128, 256, 128] + ([4] if admitted else []))
                self.assertEqual(gates(result)[-1].outcome, meter.GateResult(True, admitted))
                self.assertEqual(scratch.snapshot(), bytes(32))

    def test_material_holes_at_each_needed_source_reject_without_touching_age(self):
        tail = meter.Cost(37, (3, 2, 1, 4))
        for d in range(20):
            for j, need in enumerate(vector(d)):
                if need == 0:
                    continue
                material = [255] * 4
                material[j] = tail.material[j] + need - 1
                state, scratch = fixture(material=material)
                before = state.snapshot()
                with patch.object(State, "read_lane", side_effect=AssertionError("optional read")), \
                        patch.object(State, "write_lane", side_effect=AssertionError("optional write")):
                    result = run_condition(d, state, scratch, public_tail=tail)
                self.assertEqual(gates(result)[-1].outcome, meter.GateResult(True, False))
                self.assertEqual(paid(result), meter.Cost(520))
                self.assertEqual(state.snapshot(), condition_image(before, d, False))
                self.assertTrue(scratch.is_zero())

    def test_exact_minimum_body_and_tail_energy_thresholds(self):
        tail = meter.Cost(71, (1, 2, 3, 4))
        for d in range(20):
            for price, admitted in ((520, False), (551, False), (552, True)):
                amount = meter.floor_quote(meter.Cost(price, vector(d)), public_tail=tail)
                state, scratch = fixture(amount.energy, amount.material)
                result = run_condition(d, state, scratch, public_tail=tail)
                self.assertEqual(gates(result)[-1].outcome, meter.GateResult(True, admitted))
                self.assertEqual(paid(result), meter.Cost(552, vector(d)) if admitted else meter.Cost(520))
                if admitted:
                    self.assertEqual(stocks(state), meter.Cost(72, tail.material))
                    meter.debit(state, tail)
                    self.assertEqual(stocks(state), meter.Cost(1))

    def test_mandatory_minimum_failure_before_c_or_s_or_any_scratch_or_ram(self):
        for d in range(20):
            for energy, material, tail in ((0, (255,) * 4, meter.ZERO),
                                            (520, (255,) * 4, meter.ZERO),
                                            (65535, (0,) * 4, meter.Cost(0, (0, 1, 0, 0)))):
                state, scratch = fixture(energy, material)
                expected = bytearray(state.snapshot())
                expected[225:227] = bytes(2)
                with patch.object(machine, "_step", side_effect=AssertionError("unpaid instruction")), \
                        patch.object(Scratch, "write_bits", side_effect=AssertionError("scratch write")), \
                        patch.object(Scratch, "clear", side_effect=AssertionError("unpaid S")):
                    result = run_condition(d, state, scratch, public_tail=tail)
                self.assertIs(result.status, ServiceStatus.SHUTDOWN)
                self.assertEqual(paid(result), meter.ZERO)
                self.assertEqual(gates(result)[0].outcome, meter.GateResult(False, False, energy))
                self.assertEqual(state.snapshot(), bytes(expected))
                self.assertTrue(scratch.is_zero())

    def test_sealed_executor_prepays_c_once_before_actual_private_steps(self):
        state, scratch = fixture(553, vector(0))
        calls = []
        original_step, original_debit, original_gate = machine._step, meter.debit, meter.gate

        def debit(s, c, local=meter.ZERO, public_tail=meter.ZERO, residue=1):
            calls.append(("debit", c, local, stocks(s)))
            return original_debit(s, c, local, public_tail, residue)

        def gate(s, c, local=meter.ZERO, public_tail=meter.ZERO, **kwargs):
            calls.append(("gate", c, local, stocks(s)))
            return original_gate(s, c, local, public_tail, **kwargs)

        def step(p, s, w, local, tail):
            if w.read_bits(224, 16) == 0:
                self.assertEqual(s.energy, 169)  # 553-128-256, not another C.
            return original_step(p, s, w, local, tail)

        with patch.object(machine, "_step", side_effect=step), \
                patch.object(meter, "debit", side_effect=debit), \
                patch.object(meter, "gate", side_effect=gate), \
                patch.object(machine, "execute", side_effect=AssertionError("double C")), \
                patch.object(machine, "step", side_effect=AssertionError("unproven C")):
            result = run_condition(0, state, scratch, public_tail=meter.ZERO)
        self.assertEqual(calls[0][:3], ("gate", meter.Cost(392), meter.ZERO))
        self.assertEqual(calls[1][:3], ("debit", meter.Cost(256), meter.Cost(136)))
        self.assertEqual([c[1] for c in calls if c[0] == "gate"],
                         [meter.Cost(392), meter.Cost(32, (2, 1, 0, 0))])
        self.assertEqual(paid(result), meter.Cost(552, (2, 1, 0, 0)))


class TestServiceBoundaries(unittest.TestCase):
    def test_constructed_tick_then_real_age_and_twenty_conditioners_with_public_tails(self):
        # Fixed engineering fixture, NOT a calendar builder, experiment, fault
        # loop or schedule inferred from any earlier gate/result/age value.
        state, scratch = fixture()
        before = state.snapshot()
        result = run_tick(state, scratch, CurrentGrant(30000, (48,) * 4),
                          public_tail=meter.Cost(12304, (10,) * 4))
        total = paid(result)
        for service, tail in ((Service.AGE_LOW, meter.Cost(11352, (5,) * 4)),
                              (Service.AGE_HIGH, meter.Cost(10400))):
            age = upkeep.run_upkeep(service, state, scratch, public_tail=tail)
            assert age.trace is not None
            total = meter.add_cost(total, age.outer_meter.paid)
            for event in (*age.trace.envelopes, *age.trace.steps):
                total = meter.add_cost(total, event.paid)
        for d in range(20):
            condition = run_condition(d, state, scratch, public_tail=meter.Cost(520 * (19 - d)))
            self.assertEqual(gates(condition)[-1].outcome, meter.GateResult(True, True))
            total = meter.add_cost(total, paid(condition))
        self.assertEqual(total, meter.Cost(177 + 12944, (25,) * 4))
        expected = bytearray(before)
        expected[225:227] = (65535 - total.energy).to_bytes(2, "little")
        expected[227:231] = bytes([230] * 4)
        expected[231:241] = bytes(10)
        self.assertEqual(state.snapshot(), bytes(expected))
        self.assertTrue(scratch.is_zero())

    def test_body_quote_int32_overflow_is_technical_before_mandatory_minimum(self):
        # This domain's body needs two P0. A malformed G quote must not
        # silently turn into ordinary material rejection/physical shutdown.
        state, scratch = fixture()
        before = state.snapshot(), scratch.snapshot()
        tail = meter.Cost(0, (meter.INT32_MAX, 0, 0, 0))
        with patch.object(meter, "gate", side_effect=AssertionError("debit before G validation")):
            with self.assertRaises(OverflowError):
                run_condition(0, state, scratch, public_tail=tail)
        self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_private_program_validated_before_fee_and_public_step_refuses_its_control(self):
        program = services._condition_program(0)
        self.assertEqual(machine.validate(program).control_path_bound, (9, 0))
        state, scratch = fixture()
        before = state.snapshot(), scratch.snapshot()
        with self.assertRaises(ValueError):
            machine.step(program, state, scratch)
        terminal = program.instructions[-1]
        assert terminal is not None
        object.__setattr__(terminal, "charge", Charge.KERNEL)
        with patch.object(services, "_condition_program", return_value=program), \
                patch.object(meter, "gate", side_effect=AssertionError("fee before ROM validation")):
            with self.assertRaises(ValueError):
                run_condition(0, state, scratch, public_tail=meter.ZERO)
        self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_every_debit_preserves_exact_executed_suffix_tail_and_residue(self):
        tail = meter.Cost(83, (4, 1, 3, 2))
        for which in ("tick", "accepted", "rejected"):
            cost = (meter.Cost(177) if which == "tick" else meter.Cost(520)
                    if which == "rejected" else meter.Cost(552, vector(11)))
            required = meter.floor_quote(cost, public_tail=tail)
            state, scratch = fixture(required.energy, required.material)
            before_each = []
            original_debit = meter.debit

            def debit(s, c, local=meter.ZERO, public_tail=meter.ZERO, residue=1):
                self.assertIs(public_tail, tail)
                before_each.append((stocks(s), c, local))
                return original_debit(s, c, local, public_tail, residue)

            with patch.object(meter, "debit", side_effect=debit):
                result = (run_tick(state, scratch, CurrentGrant(0, (0,) * 4), public_tail=tail)
                          if which == "tick" else run_condition(11, state, scratch, public_tail=tail))
            self.assertEqual(stocks(state), meter.floor_quote(tail))
            for stock, c, local in before_each:
                # No accumulated spent/remaining ledger enters production.
                floor = meter.floor_quote(c, local, tail)
                self.assertGreaterEqual(stock.energy, floor.energy)
                for j in range(4):
                    self.assertGreaterEqual(stock.material[j], floor.material[j])
            self.assertEqual(paid(result), cost)

    def test_terminal_s_debit_then_clear_then_no_pc_restore(self):
        for fn in (lambda s, w: run_tick(s, w, CurrentGrant(0, (0,) * 4), public_tail=meter.ZERO),
                   lambda s, w: run_condition(3, s, w, public_tail=meter.ZERO)):
            state, scratch = fixture()
            original_clear, original_write = Scratch.clear, Scratch.write_bits
            cleared = []

            def write(w, offset, width, value, signed=False):
                self.assertFalse(cleared, "PC or scratch changed after terminal S")
                return original_write(w, offset, width, value, signed)

            # Record terminal PC rather than assuming the callable's identity.
            def checked_clear(w):
                self.assertFalse(w.is_zero())
                self.assertIn(w.read_bits(224, 16), (11, 13))
                cleared.append(state.energy)
                original_clear(w)

            with patch.object(Scratch, "clear", checked_clear), patch.object(Scratch, "write_bits", write):
                result = fn(state, scratch)
            self.assertEqual(cleared, [65535 - paid(result).energy])
            self.assertEqual(result.trace[-1].paid, meter.Cost(8))
            self.assertTrue(scratch.is_zero())

    def test_no_state_snapshot_age_helpers_or_worker_reads(self):
        for tick in (True, False):
            state, scratch = fixture()
            with patch.object(State, "snapshot", side_effect=AssertionError("backup")), \
                    patch.object(State, "read_bits", side_effect=AssertionError("RAM read")), \
                    patch.object(physical, "read_age", side_effect=AssertionError("age sensor")), \
                    patch.object(physical, "write_age", side_effect=AssertionError("free age write")):
                if tick:
                    run_tick(state, scratch, CurrentGrant(0, (0,) * 4), public_tail=meter.ZERO)
                else:
                    run_condition(19, state, scratch, public_tail=meter.ZERO)

    def test_dirty_scratch_all_bits_is_pre_mutation_technical_error(self):
        for bit in range(256):
            state, scratch = fixture()
            scratch.write_bits(bit, 1, 1)
            before = state.snapshot(), scratch.snapshot()
            with self.assertRaises(ValueError):
                run_tick(state, scratch, CurrentGrant(30000, (255,) * 4), public_tail=meter.ZERO)
            with self.assertRaises(ValueError):
                run_condition(0, state, scratch, public_tail=meter.ZERO)
            self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_malformed_grants_domains_and_tails_are_atomic_including_dead_input(self):
        bad_grants = [None, True, (30000, (48,) * 4), lambda: CurrentGrant(30000, (48,) * 4)]
        for field, value in (("energy", -1), ("energy", True), ("energy", 30001),
                             ("material", [1, 2, 3, 4]), ("material", (0, 0, 0)),
                             ("material", (0, 0, 0, 256)), ("material", (0, 0, 0, True))):
            grant = CurrentGrant(30000, (48,) * 4)
            object.__setattr__(grant, field, value)
            bad_grants.append(grant)
        for energy in (0, 1, 65535):
            for grant in bad_grants:
                state, scratch = fixture(energy)
                before = state.snapshot(), scratch.snapshot()
                with self.assertRaises((TypeError, ValueError, OverflowError)):
                    run_tick(state, scratch, cast(Any, grant), public_tail=meter.ZERO)
                self.assertEqual((state.snapshot(), scratch.snapshot()), before)
        for domain in (None, True, -1, 20, 1.0, "0", lambda: 0):
            state, scratch = fixture()
            before = state.snapshot(), scratch.snapshot()
            with self.assertRaises((TypeError, ValueError)):
                run_condition(cast(Any, domain), state, scratch, public_tail=meter.ZERO)
            self.assertEqual((state.snapshot(), scratch.snapshot()), before)
        bad_tail = meter.Cost()
        object.__setattr__(bad_tail, "material", (0, 0, 0, True))
        for tail in (None, 0, {}, lambda: meter.ZERO, bad_tail, meter.Cost(meter.INT32_MAX)):
            state, scratch = fixture(1)
            before = state.snapshot(), scratch.snapshot()
            with self.assertRaises((TypeError, ValueError, OverflowError)):
                run_tick(state, scratch, CurrentGrant(30000, (255,) * 4), public_tail=cast(Any, tail))
            with self.assertRaises((TypeError, ValueError, OverflowError)):
                run_condition(0, state, scratch, public_tail=cast(Any, tail))
            self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_no_input_program_history_callback_receipt_or_proxy(self):
        self.assertEqual(tuple(inspect.signature(run_tick).parameters),
                         ("state", "scratch", "grant", "public_tail"))
        self.assertEqual(tuple(inspect.signature(run_condition).parameters),
                         ("domain", "state", "scratch", "public_tail"))
        state, scratch = fixture()
        grant = CurrentGrant(30000, (48,) * 4)
        for name in ("program", "callback", "history", "receipt", "resume", "local_remainders"):
            with self.assertRaises(TypeError):
                cast(Any, run_tick)(state, scratch, grant, public_tail=meter.ZERO, **{name: object()})
            with self.assertRaises(TypeError):
                cast(Any, run_condition)(0, state, scratch, public_tail=meter.ZERO, **{name: object()})
        StateProxy = type("StateProxy", (State,), {})
        ScratchProxy = type("ScratchProxy", (Scratch,), {})
        for s, w in ((StateProxy(), scratch), (state, ScratchProxy()), (None, scratch), (state, None)):
            with self.assertRaises(TypeError):
                run_tick(cast(Any, s), cast(Any, w), grant, public_tail=meter.ZERO)
            with self.assertRaises(TypeError):
                run_condition(0, cast(Any, s), cast(Any, w), public_tail=meter.ZERO)

    def test_immutable_observer_results_not_consumable_and_no_retained_service_state(self):
        state, scratch = fixture()
        grant = CurrentGrant(30000, (48,) * 4)
        result = run_tick(state, scratch, grant, public_tail=meter.ZERO)
        self.assertEqual({f.name for f in fields(result)}, {"service", "status", "domain", "trace"})
        for obj, name in ((grant, "energy"), (result, "trace"), (result.trace[0], "paid")):
            self.assertFalse(hasattr(obj, "__dict__"))
            with self.assertRaises(FrozenInstanceError):
                setattr(obj, name, None)
        with self.assertRaises(TypeError):
            run_tick(state, scratch, cast(Any, result), public_tail=meter.ZERO)
        with self.assertRaises(TypeError):
            run_condition(0, state, scratch, public_tail=cast(Any, result))
        for _ in range(2):
            before = state.energy
            second = run_condition(0, state, scratch, public_tail=meter.ZERO)
            self.assertEqual(before - state.energy, 552)
            self.assertEqual(paid(second), meter.Cost(552, vector(0)))
        self.assertEqual(len(State.__slots__), 1)
        self.assertEqual(len(Scratch.__slots__), 1)
        self.assertEqual(len(state.snapshot()), 276)
        self.assertEqual(len(scratch.snapshot()), 32)

    def test_technical_write_interruption_preserves_actual_prefix_and_cannot_resume(self):
        state, scratch = fixture()
        before = state.snapshot()
        original = State.write_lane
        count = 0

        def write(s, lane, value):
            nonlocal count
            count += 1
            if count == 2:
                raise ValueError("injected technical interruption, not physical shutdown")
            original(s, lane, value)

        with patch.object(State, "write_lane", write), \
                patch.object(Scratch, "clear", side_effect=AssertionError("unpaid cleanup")):
            with self.assertRaises(ServiceFailure) as caught:
                run_condition(0, state, scratch, public_tail=meter.ZERO)
        self.assertIs(caught.exception.prefix.status, ServiceStatus.INTERRUPTED)
        self.assertIsInstance(caught.exception.__cause__, ValueError)
        self.assertEqual(state.energy, 65535 - 544)  # M+C+M+dues+both debits, no S.
        self.assertEqual((state.P0, state.P1, state.P2, state.P3), (253, 254, 255, 255))
        expected = bytearray(before)
        expected[231] &= ~3
        expected[225:227] = state.energy.to_bytes(2, "little")
        expected[227:231] = bytes((253, 254, 255, 255))
        self.assertEqual(state.snapshot(), bytes(expected))
        self.assertFalse(scratch.is_zero())
        self.assertNotIn(Opcode.S, [e.opcode for e in caught.exception.prefix.trace
                                   if isinstance(e, StepResult)])
        with self.assertRaises(ValueError):
            run_condition(0, state, scratch, public_tail=meter.ZERO)


if __name__ == "__main__":
    unittest.main()