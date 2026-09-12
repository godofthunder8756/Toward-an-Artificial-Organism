"""Differential host optimization checks; fixed component fixtures, not E3 runs.

Run tests with Python -B -m unittest test_e3_fast_machine test_e3_machine.
Run the bounded timing CLI with Python -B test_e3_fast_machine.py --benchmark
--repeats 4 (default 1, hard maximum 4). No dependencies or output files.
Both timed APIs include ROM construction, validation, full trace and the same
post-S observation traversal; fixture setup and equality checks are excluded.
"""

from __future__ import annotations

import argparse
from dataclasses import FrozenInstanceError, fields, replace
from itertools import product
import json
import platform
import statistics
import sys
from time import perf_counter
from typing import Any, cast
import unittest
from unittest.mock import patch

from e3 import fast_machine as fast, kernels, machine, meter, physical
from e3.machine import (
    ADDRESS, PC, R0, R1, R2, R3, Charge, FragmentFailure, Instruction,
    NumberType, Opcode, Operand, OperandKind, Program, immediate,
)
from e3.state import Scratch, State


S = Instruction(Opcode.S, charge=Charge.EXIT)
SIGNED = NumberType.SIGNED
MASK32 = (1 << 32) - 1


def fixture(energy=65535, material=(255, 255, 255, 255), dirty=True):
    # Every byte, including inaccessible reserve and invalid code, participates
    # in the final byte-equality assertion. No private experimental input.
    state = State(bytes((13 * i + 17) & 255 for i in range(276)))
    state.energy = energy
    for hub, amount in enumerate(material):
        state.write_material(hub, amount)
    scratch = Scratch(b"\xa5" * 32 if dirty else bytes(32))
    put(scratch, PC, 0)
    return state, scratch


def put(scratch, arg, value):
    scratch.write_bits(machine._partition(arg.kind)[0] + arg.offset, arg.width,
                       value & ((1 << arg.width) - 1))


def alu(op, dst, *args, number=NumberType.UNSIGNED, charge=Charge.KERNEL):
    return Instruction(op, dst, args, number=number, charge=charge)


def n(value):
    return immediate(value, number=SIGNED)


def outcome(execute, program, state, scratch, kwargs):
    try:
        return execute(program, state, scratch, **kwargs), None, None
    except (TypeError, ValueError, OverflowError, PermissionError, FragmentFailure) as error:
        prefix = error.prefix if type(error) is FragmentFailure else None
        cause = error.__cause__
        return prefix, (type(error), str(error)), (type(cause), str(cause))


class TestFastDifferential(unittest.TestCase):
    def compare(self, program, state=None, scratch=None, **kwargs):
        if state is None:
            state, scratch = fixture()
        assert scratch is not None
        other, work = State(state.snapshot()), Scratch(scratch.snapshot())
        expected = outcome(machine.execute, program, state, scratch, kwargs)
        actual = outcome(fast.execute_fast, program, other, work, kwargs)
        self.assertEqual(actual, expected)  # full nested typed records + causes
        self.assertEqual(other.snapshot(), state.snapshot())
        self.assertEqual(work.snapshot(), scratch.snapshot())
        if actual[0] is not None:
            self.assertIs(type(actual[0]), machine.FragmentResult)
            for event in actual[0].steps:
                self.assertIs(type(event), machine.StepResult)
                self.assertIs(type(event.paid), meter.Cost)
        return actual[0], other, work

    def test_every_opcode_signed_and_unsigned_with_mixed_forward_control(self):
        pred = Operand(OperandKind.D, 55, 1)
        source = Operand(OperandKind.R2, 14, 2)
        reply = Operand(OperandKind.R0, width=2)
        sites = [alu(Opcode.MOV, R0, immediate(0x80000001)),
                 Instruction(Opcode.EX, R1, (R0,), number=SIGNED,
                             extract_offset=1, extract_width=16)]
        for op in (Opcode.ADD, Opcode.SUB, Opcode.AND, Opcode.OR, Opcode.XOR,
                   Opcode.SHL, Opcode.SHR, Opcode.LT, Opcode.LE, Opcode.GT,
                   Opcode.GE, Opcode.EQ, Opcode.NE):
            sites.append(alu(op, R2, R0, immediate(1)))
        for op in (Opcode.ADD, Opcode.SUB, Opcode.LT, Opcode.LE, Opcode.GT,
                   Opcode.GE, Opcode.EQ, Opcode.NE):
            sites.append(alu(op, R2, n(-4), n(3), number=SIGNED))
        sites.extend((alu(Opcode.NEG, R1, n(-7), number=SIGNED),
                      alu(Opcode.NOT, R2, R1),
                      alu(Opcode.SELECT, R3, pred, R1, R2),
                      alu(Opcode.MOV, ADDRESS, immediate(83, 11)),
                      Instruction(Opcode.WRITE2, args=(ADDRESS, source), charge=Charge.ACCESS),
                      Instruction(Opcode.READ2, reply, (ADDRESS,), charge=Charge.ACCESS,
                                  capture=Operand(OperandKind.D, 31, 2)),
                      Instruction(Opcode.PAD, charge=Charge.PADDING)))
        start = len(sites)
        sites.extend((Instruction(Opcode.BR, args=(pred,), target=start + 2),
                      alu(Opcode.MOV, R3, immediate(8)),
                      Instruction(Opcode.STAGE, target=start + 4), None,
                      Instruction(Opcode.JUMP, target=start + 6), None,
                      alu(Opcode.MOV, PC, immediate(start + 8, 16)), None, S))
        program = Program(tuple(sites))
        seen = set()
        for value in (0, 1):
            state, scratch = fixture()
            put(scratch, pred, value)
            result, _, _ = self.compare(program, state, scratch)
            seen.update(event.opcode for event in result.steps)
        self.assertEqual(seen, set(Opcode))

    def test_narrow_slices_neighbors_all_widths_and_partition_ends(self):
        for kind, size in ((OperandKind.D, 96), (OperandKind.R0, 32),
                           (OperandKind.R1, 32), (OperandKind.R2, 32),
                           (OperandKind.R3, 32), (OperandKind.ADDRESS, 11),
                           (OperandKind.FLAGS, 5)):
            for width in range(1, min(size, 32) + 1):
                for offset in sorted({0, size - width, min(7, size - width)}):
                    dst = Operand(kind, offset, width)
                    program = Program((alu(Opcode.MOV, dst, immediate((1 << width) - 1, width)),
                                       alu(Opcode.ADD, dst, dst, immediate(1, width)),
                                       alu(Opcode.MOV, R0, dst), S))
                    # Last MOV fails AFTER narrow writes: compare dirty scratch,
                    # not merely the eventual all-zero S image.
                    state, scratch = fixture(11)
                    result, _, _ = self.compare(program, state, scratch)
                    self.assertEqual(len(result.steps), 2)

    def test_packed_w_increment_ex_and_signed_shift_counts(self):
        word = Operand(OperandKind.D, 32, 32)
        for w in (15, 19):
            state, scratch = fixture(10)
            put(scratch, word, (w << 27) | ((1 << 27) - 137))
            result, _, _ = self.compare(Program((alu(Opcode.ADD, word, word, immediate(1 << 27)),
                                                 alu(Opcode.MOV, R0, word), S)), state, scratch)
            self.assertEqual(result.steps[0].value >> 27, w + 1)
        for shift in range(32):
            self.compare(Program((alu(Opcode.SHR, R0, n(-12345), immediate(shift, 5),
                                      number=SIGNED), S)))
        for width in range(1, 33):
            source = Operand(OperandKind.D, 64, width)
            self.compare(Program((Instruction(Opcode.EX, R0, (source,), number=SIGNED,
                                               extract_width=width), S)))

    def test_signed_overflow_and_bad_dynamic_operands_precede_shortage(self):
        bad = (
            alu(Opcode.ADD, R0, n((1 << 31) - 1), n(1), number=SIGNED),
            alu(Opcode.SUB, R0, n(-(1 << 31)), n(1), number=SIGNED),
            alu(Opcode.NEG, R0, n(-(1 << 31)), number=SIGNED),
            alu(Opcode.SHL, R0, n(1 << 30), immediate(1), number=SIGNED),
            alu(Opcode.SELECT, R0, R1, immediate(1), immediate(0)),
            alu(Opcode.SHL, R0, R0, R1), alu(Opcode.SHR, R0, R0, R1),
            Instruction(Opcode.BR, args=(R1,), target=2),
        )
        for ins, energy in product(bad, (10, 65535)):
            state, scratch = fixture(energy)
            put(scratch, R1, 32)
            self.compare(Program((alu(Opcode.MOV, R3, immediate(7)), ins, S)), state, scratch)

    def test_all_dynamic_address_encodings_permissions_and_paid_prefix(self):
        reply = Operand(OperandKind.R0, width=2)
        for op in (Opcode.READ2, Opcode.WRITE2):
            access = (Instruction(op, reply, (ADDRESS,), charge=Charge.ACCESS,
                                  capture=Operand(OperandKind.D, 30, 2))
                      if op is Opcode.READ2 else
                      Instruction(op, args=(ADDRESS, reply), charge=Charge.ACCESS))
            # Every dynamic encoding, including all four material sources and
            # all invalid/reserved/address-space neighbors. One short fragment.
            program = Program((alu(Opcode.MOV, R0, immediate(3), charge=Charge.CONTROL_A),
                               alu(Opcode.MOV, R1, immediate(5)), access, S))
            for lane in range(2048):
                state, scratch = fixture(1024, (5, 6, 7, 8))
                put(scratch, ADDRESS, lane)
                result, _, _ = self.compare(program, state, scratch)
                self.assertEqual(len(result.steps), 4 if lane < 900 or 924 <= lane < 972 else 2)

    def test_literal_access_raw_symbols_capture_and_same_value_writes(self):
        reply = Operand(OperandKind.R0, width=2)
        capture = Operand(OperandKind.D, 31, 2)
        for lane, symbol in product((0, 19, 20, 40, 60, 79, 80, 81, 82, 83, 899, 924, 971),
                                    range(4)):
            state, scratch = fixture()
            state.write_lane(lane, symbol)
            program = Program((Instruction(Opcode.READ2, reply, (immediate(lane, 11),),
                                             charge=Charge.ACCESS, capture=capture),
                               Instruction(Opcode.WRITE2, args=(immediate(lane, 11), reply),
                                           charge=Charge.ACCESS), S))
            self.compare(program, state, scratch)

    def test_sourcewise_floors_material_equality_and_nonexact_local_remainders(self):
        source = Operand(OperandKind.R0, width=2)
        for lane in (0, 20, 40, 60, 80, 81, 82, 83):
            hub = physical.DEFAULT_CONFIG.lane_to_hub[lane]
            program = Program((Instruction(Opcode.WRITE2, args=(immediate(lane, 11), source),
                                           charge=Charge.ACCESS), S))
            for energy, stock in product((1, 8, 31, 32, 39, 50, 65535), (0, 1, 3, 4)):
                state, scratch = fixture(energy)
                state.write_material(hub, stock)
                local = (meter.Cost(8, tuple(int(j == hub) for j in range(4))), meter.ZERO)
                tail = meter.Cost(7, tuple(2 * int(j == hub) for j in range(4)))
                self.compare(program, state, scratch, local_remainders=local, public_tail=tail)
            # A large bound at an unvisited site is validated, not charged or
            # treated as a newly inferred exact suffix on the path to S.
            self.compare(Program((S, *program.instructions)),
                         local_remainders=(meter.ZERO, meter.Cost(500), meter.ZERO))

    def test_control_a_b_limits_unvisited_regions_and_reserve_tail(self):
        ca = alu(Opcode.MOV, R0, immediate(3), charge=Charge.CONTROL_A)
        cb = replace(ca, charge=Charge.CONTROL_B)
        for count in (1, 256):
            program = Program((ca,) * count + (cb,) * count + (S,))
            for energy in (520, 521, 527, 528):
                state, scratch = fixture(energy, (0, 2, 0, 0))
                self.compare(program, state, scratch, public_tail=meter.Cost(7, (0, 2, 0, 0)))
        program = Program((Instruction(Opcode.JUMP, target=2, charge=Charge.CONTROL_A), cb, S))
        result, _, _ = self.compare(program)
        self.assertEqual(len(result.envelopes), 2)
        self.assertEqual([event.pc for event in result.steps], [0, 2])
        branch = Instruction(Opcode.BR, args=(Operand(OperandKind.D, width=1),),
                             target=202, charge=Charge.CONTROL_A)
        jump = Instruction(Opcode.JUMP, target=402, charge=Charge.CONTROL_A)
        self.compare(Program((branch,) + (ca,) * 200 + (jump,) + (ca,) * 200 + (S,)))

    def test_nonzero_base_holes_max_pc_and_s_failures(self):
        for base in (7, 65000):
            for op in (Opcode.STAGE, Opcode.JUMP, Opcode.MOV):
                ins = (alu(op, PC, immediate(base + 2, 16)) if op is Opcode.MOV else
                       Instruction(op, target=base + 2))
                state, scratch = fixture()
                put(scratch, PC, base)
                self.compare(Program((ins, None, S), base=base), state, scratch)
        for energy in (0, 8, 9):
            state, scratch = fixture(energy)
            put(scratch, PC, 65534)
            self.compare(Program((S,), base=65534), state, scratch)
        self.compare(Program((S,), base=5))

    def test_td_reward_promotion_terminal_zero_and_selection_packet_trap(self):
        reward = Operand(OperandKind.D, 64, 16)
        program = Program((Instruction(Opcode.EX, R1, (reward,), number=SIGNED, extract_width=16),
                           alu(Opcode.MOV, R2, immediate(0)), *machine.td_program().instructions))
        state, scratch = fixture()
        put(scratch, R0, 127)
        put(scratch, R2, 32767)
        put(scratch, reward, -1)
        self.compare(program, state, scratch)
        core = machine.selection_program().instructions
        rank = Operand(OperandKind.D, 64, 7)
        pred = Operand(OperandKind.D, 55, 1)
        program = Program((Instruction(Opcode.EX, R3, (rank,), charge=Charge.CONTROL_A,
                                       extract_offset=1, extract_width=2),
                           alu(Opcode.EQ, pred, R3, immediate(3), charge=Charge.CONTROL_A),
                           Instruction(Opcode.BR, args=(pred,), target=3 + len(core) - 1,
                                       charge=Charge.CONTROL_A), *core))
        for t in range(4):
            state, scratch = fixture()
            scratch.write_bits(64, 7, t << 1)
            for reg in (R0, R1, R2):
                put(scratch, reg, -1)
            result, _, _ = self.compare(program, state, scratch)
            self.assertEqual(len(result.steps), 4 if t == 3 else 31)

    def test_eight_q_reads_signed_ex_and_paid_persistent_bit_merge(self):
        state, scratch = fixture()
        sites = []
        for i in range(8):
            state.write_lane(80 + i, 3)
            sites.extend((alu(Opcode.MOV, ADDRESS, immediate(80 + i, 11)),
                          Instruction(Opcode.READ2, Operand(OperandKind.R0, 2 * i, 2),
                                      (ADDRESS,), charge=Charge.ACCESS)))
        sites.extend((Instruction(Opcode.EX, R0, (R0,), number=SIGNED, extract_width=16), S))
        result, _, _ = self.compare(Program(tuple(sites)), state, scratch)
        self.assertEqual(result.steps[-2].value, MASK32)
        reply = Operand(OperandKind.R0, width=2)
        program = Program((Instruction(Opcode.READ2, reply, (immediate(80, 11),), charge=Charge.ACCESS),
                           alu(Opcode.AND, reply, reply, immediate(2, 2)),
                           alu(Opcode.OR, reply, reply, immediate(1, 2)),
                           Instruction(Opcode.WRITE2, args=(immediate(80, 11), reply),
                                       charge=Charge.ACCESS), S))
        for symbol in range(4):
            state, scratch = fixture()
            state.write_lane(80, symbol)
            state.write_lane(81, 2)
            result, other, _ = self.compare(program, state, scratch)
            self.assertEqual(other.read_lane(80), symbol | 1)
            self.assertEqual(other.read_lane(81), 2)
            self.assertEqual([event.paid.energy for event in result.steps], [10, 1, 1, 14, 8])

    def test_malformed_forged_rom_bounds_and_ordering_are_revalidated(self):
        program = Program((alu(Opcode.MOV, R0, immediate(0), charge=Charge.CONTROL_A), S))
        for kwargs in ({"local_remainders": [meter.Cost(8), meter.ZERO]},
                       {"local_remainders": (meter.ZERO, meter.ZERO)},
                       {"local_remainders": (meter.Cost(8),)},
                       {"local_remainders": (meter.Cost(meter.INT32_MAX), meter.ZERO)},
                       {"public_tail": meter.Cost(meter.INT32_MAX)},
                       {"public_tail": lambda: meter.ZERO}, {"mode": True},
                       {"mode": meter.GateResult(True, True)}):
            self.compare(program, **kwargs)
        for value in (None, True, (), lambda: program, fast.compile_program(program)):
            self.compare(value)
        # Frozen is not a proof. Recheck forged unreachable instructions too.
        ins = alu(Opcode.MOV, R0, immediate(1))
        forged = Program((S, ins, S))
        object.__setattr__(ins, "args", (True,))
        self.compare(forged)
        for field, value in (("energy", True), ("material", [0, 0, 0, 0]),
                             ("material", (0, 0, 0, meter.INT32_MAX + 1))):
            bound = meter.Cost(8)
            object.__setattr__(bound, field, value)
            self.compare(program, local_remainders=(bound, meter.ZERO))
        # _bounds must still reject its reference worst-address arithmetic,
        # even though this actual fixed-source write costs much less.
        source = Operand(OperandKind.R0, width=2)
        write = Program((Instruction(Opcode.WRITE2, args=(immediate(80, 11), source),
                                      charge=Charge.ACCESS), S))
        self.compare(write, local_remainders=(meter.Cost(meter.INT32_MAX - 20), meter.ZERO))
        self.compare(write, public_tail=meter.Cost(0, (0, meter.INT32_MAX, 0, 0)))

    def test_td_all_reference_boundaries_and_remainders(self):
        program = machine.td_program()
        words = (-32768, -257, -256, -12, -4, -1, 0, 1, 4, 12, 256, 257, 32767)
        for q, reward, maximum in product(words, repeat=3):
            state, scratch = fixture(32)
            for reg, value in zip((R0, R1, R2), (q, reward, maximum)):
                put(scratch, reg, value)
            self.compare(program, state, scratch)
        for maximum in range(-256, 257):
            state, scratch = fixture(32)
            for reg, value in zip((R0, R1, R2), (0, 0, maximum)):
                put(scratch, reg, value)
            self.compare(program, state, scratch)

    def test_selection_all_seven_subsets_and_96_ranks(self):
        program = machine.selection_program()
        for mask, b, t, x in product(range(1, 8), range(2), range(3), range(16)):
            state, scratch = fixture(289)
            for i, reg in enumerate((R0, R1, R2)):
                put(scratch, reg, -1 if mask & (1 << i) else -32768)
            scratch.write_bits(64, 7, b | t << 1 | x << 3)
            self.compare(program, state, scratch)

    def test_fixed_benchmark_fixtures_and_generated_public_scans(self):
        from benchmark_e3_components import construct, fixtures
        from e3.protocol import Code

        for case in fixtures():
            state, scratch = construct(case)
            self.compare(kernels.make_scan_program(case.code), state, scratch)
        # Deterministic arithmetic symbols only, never seeds/roots/targets.
        for code, cue in product(Code, (0, 15)):
            program = kernels.make_scan_program(code)
            state, scratch = fixture()
            for lane in range(80):
                state.write_lane(lane, (lane * lane + 3 * lane + 1) % 4)
            scratch.write_bits(64, 4, cue)
            scratch.write_bits(68, 1, cue % 2)
            self.compare(program, state, scratch)
        # Exact public suffix fixture (as distinct from default S-only bounds).
        program = kernels.make_scan_program(Code.REP)
        remaining = 0
        local = []
        for ins in reversed(program.instructions):
            assert ins is not None
            local.append(meter.Cost(remaining))
            remaining += (8 if ins.opcode is Opcode.S else 17 if ins.opcode is Opcode.READ2
                          else 1 if ins.charge is Charge.KERNEL else 0)
        state, scratch = fixture(391, (0, 2, 0, 0))
        self.compare(program, state, scratch, local_remainders=tuple(reversed(local)),
                     public_tail=meter.Cost(7, (0, 2, 0, 0)))


class TestFastHostBoundary(unittest.TestCase):
    def test_compiled_data_is_frozen_static_and_never_an_execution_receipt(self):
        program = Program((alu(Opcode.MOV, R0, immediate(5)), S))
        compiled = fast.compile_program(program)
        self.assertEqual({field.name for field in fields(compiled)}, {"base", "sites", "regions"})
        for obj, name in ((compiled, "base"), (compiled.sites[0], "target"),
                          (compiled.sites[0].args[0], "mask")):
            self.assertFalse(hasattr(obj, "__dict__"))
            with self.assertRaises(FrozenInstanceError):
                setattr(obj, name, 0)
        object.__setattr__(compiled, "sites", ())
        state, scratch = fixture()
        with self.assertRaises(TypeError):
            fast.execute_fast(cast(Any, compiled), state, scratch)
        with patch.object(machine, "validate", wraps=machine.validate) as validate, \
                patch.object(machine, "_bounds", wraps=machine._bounds) as bounds:
            fast.execute_fast(program, state, scratch)
        validate.assert_called_once()
        bounds.assert_called_once()
        arg = immediate(7)
        program = Program((alu(Opcode.MOV, R0, arg), S))
        fast.compile_program(program)
        object.__setattr__(arg, "width", 33)
        with self.assertRaises(ValueError):
            fast.execute_fast(program, *fixture())

    def test_exact_containers_and_backing_buffers_no_proxy_hooks(self):
        # Bypass @final intentionally: runtime rejection is the property tested.
        class StateProxy(cast(Any, State)):
            pass

        class ScratchProxy(cast(Any, Scratch)):
            pass

        for state, scratch in ((StateProxy(), Scratch()), (State(), ScratchProxy()),
                               (bytes(276), Scratch()), (State(), bytes(32))):
            with self.assertRaises(TypeError):
                fast.execute_fast(Program((S,)), cast(Any, state), cast(Any, scratch))
        for owner, attr in ((State(), "_State__buffer"), (Scratch(), "_Scratch__buffer")):
            original = getattr(owner, attr)
            for bad in (bytes(original), list(original), bytearray(1)):
                setattr(owner, attr, bad)
                state, scratch = (owner, Scratch()) if type(owner) is State else (State(), owner)
                with self.assertRaises((TypeError, ValueError)):
                    fast.execute_fast(Program((S,)), cast(Any, state), cast(Any, scratch))

    def test_no_snapshots_public_codecs_or_repeated_validation_in_steps(self):
        program = Program((alu(Opcode.ADD, R0, immediate(2), immediate(3)),) * 20 + (S,))
        state, scratch = fixture()
        state_buffer, scratch_buffer = getattr(state, "_State__buffer"), getattr(scratch, "_Scratch__buffer")
        with patch.object(State, "snapshot", side_effect=AssertionError("snapshot")), \
                patch.object(Scratch, "snapshot", side_effect=AssertionError("snapshot")), \
                patch.object(Scratch, "read_bits", side_effect=AssertionError("public validation")), \
                patch.object(Scratch, "write_bits", side_effect=AssertionError("public validation")), \
                patch.object(meter, "debit", side_effect=AssertionError("repeated meter validation")), \
                patch.object(State, "read_bits", side_effect=AssertionError("unpaid RAM")):
            result = fast.execute_fast(program, state, scratch)
        self.assertEqual(result.steps[0].value, 5)
        self.assertIs(state_buffer, getattr(state, "_State__buffer"))
        self.assertIs(scratch_buffer, getattr(scratch, "_Scratch__buffer"))
        self.assertEqual(len(state_buffer), 276)
        self.assertEqual(len(scratch_buffer), 32)

    def test_read_payload_is_after_debit_and_not_compiled_or_peeked(self):
        reply = Operand(OperandKind.R0, width=2)
        program = Program((Instruction(Opcode.READ2, reply, (immediate(0, 11),),
                                         charge=Charge.ACCESS), S))
        state, scratch = fixture()
        state.write_lane(0, 1)
        debit = fast._debit

        def observe(data, payment):
            debit(data, payment)
            if payment.cost.energy == 17:
                self.assertEqual(state.energy, 65535 - 17)
                self.assertEqual(scratch.read_bits(224, 16), 0)
                state.write_lane(0, 3)  # test-only fault-free ordering probe

        with patch.object(fast, "_debit", observe):
            result = fast.execute_fast(program, state, scratch)
        self.assertEqual(result.steps[0].value, 3)
        state, scratch = fixture(25)
        before = state.snapshot(), scratch.snapshot()
        with self.assertRaises(FragmentFailure) as caught:
            fast.execute_fast(program, state, scratch)
        self.assertIs(type(caught.exception.__cause__), meter.InsufficientResources)
        self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_write_payload_after_source_debit_and_pc_reloaded_from_scratch(self):
        reply = Operand(OperandKind.R0, width=2)
        program = Program((Instruction(Opcode.WRITE2, args=(immediate(40, 11), reply),
                                         charge=Charge.ACCESS), S))
        state, scratch = fixture()
        put(scratch, reply, 3)
        state.write_lane(40, 1)
        debit = fast._debit

        def observe(data, payment):
            if payment.cost.energy == 23:
                self.assertEqual(state.read_lane(40), 1)
            debit(data, payment)
            if payment.cost.energy == 23:
                self.assertEqual(state.P2, 254)
                self.assertEqual(state.read_lane(40), 1)
                put(scratch, reply, 0)  # write must use its predebit operand

        with patch.object(fast, "_debit", observe):
            result = fast.execute_fast(program, state, scratch)
        self.assertEqual(result.steps[0].value, 3)
        self.assertEqual(state.read_lane(40), 3)
        # No public callback API: this test-only wrapper intervenes between
        # instructions and proves that last event.next_pc is not a PC shadow.
        program = Program((alu(Opcode.MOV, R0, immediate(1)),
                           alu(Opcode.MOV, R0, immediate(2)), S))
        state, scratch = fixture()
        step = fast._step

        def intervene(compiled, data, work):
            event = step(compiled, data, work)
            if event.pc == 0:
                work[28] = 2
            return event

        with patch.object(fast, "_step", intervene):
            result = fast.execute_fast(program, state, scratch)
        self.assertEqual([event.pc for event in result.steps], [0, 2])

    def test_unrelated_errors_are_not_wrapped(self):
        program = Program((alu(Opcode.MOV, R0, immediate(1)), S))
        for error in (TypeError("internal"), OSError("internal"), RuntimeError("internal"),
                      KeyboardInterrupt(), SystemExit(2)):
            with patch.object(fast, "_debit", side_effect=error):
                with self.assertRaises(type(error)) as caught:
                    fast.execute_fast(program, *fixture())
            self.assertIs(caught.exception, error)

    def test_each_step_reloads_resources_and_registers_not_previous_events(self):
        program = Program((alu(Opcode.MOV, R0, immediate(1)),
                           alu(Opcode.ADD, R1, R0, immediate(1)), S))
        state, scratch = fixture()
        step = fast._step

        def alter_register(compiled, data, work):
            event = step(compiled, data, work)
            if event.pc == 0:
                put(scratch, R0, 9)
            return event

        with patch.object(fast, "_step", alter_register):
            result = fast.execute_fast(program, state, scratch)
        self.assertEqual([event.value for event in result.steps], [1, 10, None])
        state, scratch = fixture()

        def alter_stock(compiled, data, work):
            event = step(compiled, data, work)
            if event.pc == 0:
                state.energy = 9
            return event

        with patch.object(fast, "_step", alter_stock):
            with self.assertRaises(FragmentFailure) as caught:
                fast.execute_fast(program, state, scratch)
        self.assertIs(type(caught.exception.__cause__), meter.InsufficientResources)
        self.assertEqual(len(caught.exception.prefix.steps), 1)
        self.assertEqual(state.energy, 9)
        self.assertEqual(scratch.read_bits(224, 16), 1)


def fast_scan(code, state, scratch):
    """Benchmark adapter only: reproduce reference observation AFTER execution."""
    from e3.protocol import Code

    program = kernels.make_scan_program(code)
    trace = fast.execute_fast(program, state, scratch)
    payload, health = trace.steps[-3].value, trace.steps[-2].value
    assert payload is not None and health is not None
    observed_slot = kernels._LOW_COUNT if code is Code.BLOCK else kernels._HIGH_COUNT
    observed = tied = None
    for event in trace.steps:
        ins = program.instructions[event.pc - program.base]
        assert ins is not None
        if ins.dst == observed_slot:
            observed = event.value
        elif ins.dst == kernels._TIE:
            tied = event.value
    assert observed is not None and tied is not None
    return kernels.ScanFragmentResult(
        kernels.ScanObservation(payload if health >= 2 else None, health, observed, bool(tied)),
        trace,
    )


def benchmark(repeats=1):
    from benchmark_e3_components import check, construct, fixtures, require
    from verify_e3_design import verify

    require(type(repeats) is int and 1 <= repeats <= 4, "repeats must be in 1..4")
    require(sys.dont_write_bytecode, "use Python -B")
    audit = verify()
    require(audit["ok"] is True and audit["files_checked"] == audit["file_count"] == 23,
            "23-entry design verification failed")
    deadline = perf_counter() + 10.0
    counts = {"REP": 0, "BLOCK": 0}
    results = []
    for case in fixtures():
        samples = {"reference": [], "fast": []}
        conformance = None
        # One warm pair + at most four measured pairs per fixture. Exactly
        # <=20 scans per representation, <=40 total, never duration-filling.
        for repeat in range(repeats + 1):
            require(perf_counter() < deadline, "10-second scan admission budget exhausted")
            require(counts[case.code.name] + 2 <= 20, "scan count limit exceeded")
            pair = {}
            order = ("reference", "fast") if repeat % 2 == 0 else ("fast", "reference")
            for engine in order:
                require(perf_counter() < deadline, "10-second scan admission budget exhausted")
                state, scratch = construct(case)
                before = state.snapshot()
                execute = kernels.run_scan_fragment if engine == "reference" else fast_scan
                start = perf_counter()
                result = execute(case.code, state, scratch)
                elapsed = perf_counter() - start
                counts[case.code.name] += 1
                conformance = check(case, state, scratch, before, result)
                pair[engine] = result, state.snapshot(), scratch.snapshot()
                if repeat:
                    samples[engine].append(elapsed)
            require(pair["reference"] == pair["fast"], "full trace/state/scratch mismatch")
        reference = statistics.median(samples["reference"])
        optimized = statistics.median(samples["fast"])
        results.append({"fixture": case.name, "code": case.code.name,
                        "seconds": samples, "reference_median_seconds": reference,
                        "fast_median_seconds": optimized, "speedup": reference / optimized,
                        "full_differential_equal": True, "conformance": conformance})
    return {"ok": True, "kind": "host_optimization_fixed_component_fixtures_not_experiment",
            "python": platform.python_version(), "repeats": repeats,
            "design_verification": audit, "scans_including_warmups": counts,
            "admission_seconds": 10, "hard_scan_cap_per_code": 20,
            "scope": "ROM build + validation + compile (fast) + execution + full trace + observation",
            "excludes": "imports, fixture setup, checks, trace release; no tracemalloc",
            "limitations": "engineering fragments only, no full services or throughput projections",
            "timings": results}


if __name__ == "__main__":
    if "--benchmark" in sys.argv:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--benchmark", action="store_true")
        parser.add_argument("--repeats", type=int, default=1, choices=range(1, 5))
        args = parser.parse_args()
        print(json.dumps(benchmark(args.repeats), sort_keys=True))
    else:
        unittest.main()