"""Actual instruction execution fixtures, not experiments or pure side counters.

All inputs are constructed finite fixtures; no targets, roots, draws or service
admission. Independent Fraction/reference helpers exist only in this test file.
Mock callbacks observe host ordering in tests; no instruction accepts callbacks.
"""

from collections import Counter
from dataclasses import FrozenInstanceError, fields, replace
from fractions import Fraction
from itertools import product
from typing import Any, cast
import unittest
from unittest.mock import patch

from e3 import arithmetic, machine, meter, physical
from e3.machine import (
    ADDRESS, PC, R0, R1, R2, R3, Charge, ExecutionMode, FragmentFailure,
    Instruction, NumberType, Opcode, Operand, OperandKind, Program, StepStatus,
    execute, immediate, selection_program, step, td_program, validate,
)
from e3.state import Scratch, State


S = Instruction(Opcode.S, charge=Charge.EXIT)
SIGNED = NumberType.SIGNED
MASK32 = (1 << 32) - 1


def signed(value: int | None) -> int:
    assert value is not None
    return value - (1 << 32) if value & (1 << 31) else value


def unchecked(value: object) -> Any:
    """Deliberately bypass static typing ONLY for runtime rejection fixtures."""
    return cast(Any, value)


def n(value):
    return immediate(value, number=SIGNED)


def fixture(energy=65535, material=(255, 255, 255, 255)):
    state, scratch = State(), Scratch()
    state.energy = energy
    for hub, amount in enumerate(material):
        state.write_material(hub, amount)
    return state, scratch


def put(scratch, operand, value):
    bases = {OperandKind.D: 0, OperandKind.R0: 96, OperandKind.R1: 128,
             OperandKind.R2: 160, OperandKind.R3: 192, OperandKind.PC: 224,
             OperandKind.ADDRESS: 240, OperandKind.FLAGS: 251}
    scratch.write_bits(bases[operand.kind] + operand.offset, operand.width,
                       value & ((1 << operand.width) - 1))


def get(scratch, operand):
    bases = {OperandKind.D: 0, OperandKind.R0: 96, OperandKind.R1: 128,
             OperandKind.R2: 160, OperandKind.R3: 192, OperandKind.PC: 224,
             OperandKind.ADDRESS: 240, OperandKind.FLAGS: 251}
    return scratch.read_bits(bases[operand.kind] + operand.offset, operand.width)


def alu(op, dst, *args, number=NumberType.UNSIGNED, charge=Charge.KERNEL):
    return Instruction(op, dst, args, number=number, charge=charge)


def one(ins, *, scratch=None):
    state, blank = fixture()
    scratch = blank if scratch is None else scratch
    event = step(Program((ins, S)), state, scratch)
    return event, state, scratch


def reference_td(q, reward, maximum):
    clipped = sorted((-256, reward, 256))[1]
    update = round((Fraction(clipped) + Fraction(15, 16) * maximum - q) / 8)
    return sorted((-32768, q + update, 32767))[1]


class TestOperandAndProgram(unittest.TestCase):
    def test_closed_immutable_slotted_values(self):
        ins = alu(Opcode.MOV, R0, immediate(1))
        program = Program((ins, S))
        for obj, field, value in ((R0, "width", 1), (ins, "args", ()),
                                  (program, "base", 1)):
            with self.assertRaises(FrozenInstanceError):
                setattr(obj, field, value)
            self.assertFalse(hasattr(obj, "__dict__"))
        self.assertEqual({f.name for f in fields(Program)}, {"instructions", "base"})
        self.assertEqual(len(State.__slots__), 1)
        self.assertEqual(len(Scratch.__slots__), 1)
        self.assertEqual(len(State().snapshot()), 276)
        self.assertEqual(len(Scratch().snapshot()), 32)
        self.assertFalse(hasattr(machine, "Machine"))

    def test_all_operand_widths_partition_edges(self):
        partitions = ((OperandKind.D, 96), (OperandKind.R0, 32),
                      (OperandKind.R1, 32), (OperandKind.R2, 32),
                      (OperandKind.R3, 32), (OperandKind.PC, 16),
                      (OperandKind.ADDRESS, 11), (OperandKind.FLAGS, 5))
        for kind, size in partitions:
            for width in range(1, min(size, 32) + 1):
                Operand(kind, size - width, width)
                with self.assertRaises(ValueError):
                    Operand(kind, size - width + 1, width)
        for width in (0, -1, 33, 40):
            with self.assertRaises(ValueError):
                Operand(OperandKind.D, width=width)

    def test_strict_numbers_and_immediate_ranges(self):
        class Integer(int):
            pass

        for value in (True, 1.0, "1", Integer(1), None):
            for kwargs in ({"offset": value}, {"width": value}, {"value": value}):
                with self.assertRaises(TypeError):
                    unchecked(Operand)(OperandKind.D, **kwargs)
            with self.assertRaises(TypeError):
                immediate(unchecked(value))
            with self.assertRaises(TypeError):
                Program((S,), base=unchecked(value))
        for width in range(1, 33):
            for number in NumberType:
                low = -(1 << (width - 1)) if number is SIGNED else 0
                high = (1 << (width - int(number is SIGNED))) - 1
                immediate(low, width, number)
                immediate(high, width, number)
                for outside in (low - 1, high + 1):
                    with self.assertRaises(ValueError):
                        immediate(outside, width, number)
        with self.assertRaises(ValueError):
            Operand(OperandKind.R0, number=SIGNED)

    def test_no_callable_containers_or_unknown_enum_fields(self):
        callback = lambda: 0
        constructors = (
            lambda: Instruction(unchecked("MOV"), R0, (immediate(0),)),
            lambda: Instruction(Opcode.MOV, R0, (unchecked(callback),)),
            lambda: Instruction(Opcode.MOV, R0, unchecked([immediate(0)])),
            lambda: Instruction(Opcode.MOV, R0, (immediate(0),), charge=unchecked(True)),
            lambda: Instruction(Opcode.ADD, R0, (R0, R1), number=unchecked("signed")),
            lambda: Operand(unchecked("R4")), lambda: Program(unchecked([S])),
            lambda: Program((unchecked(callback), S)), lambda: Program((unchecked({}), S)),
        )
        for constructor in constructors:
            with self.assertRaises(TypeError):
                constructor()

    def test_opcode_shapes_and_semantic_types(self):
        bad = (
            lambda: Instruction(Opcode.ADD, R0, (R1,)),
            lambda: Instruction(Opcode.MOV, None, (R0,)),
            lambda: Instruction(Opcode.S, R0, charge=Charge.EXIT),
            lambda: Instruction(Opcode.MOV, immediate(0), (R0,)),
            lambda: alu(Opcode.MOV, R0, R1, number=SIGNED),
            lambda: alu(Opcode.ADD, Operand(OperandKind.D, 0, 5), R0, R1, number=SIGNED),
            lambda: alu(Opcode.ADD, R0, Operand(OperandKind.D, 0, 16), R1, number=SIGNED),
            lambda: alu(Opcode.ADD, R0, R1, immediate(1), number=SIGNED),
            lambda: alu(Opcode.MOV, Operand(OperandKind.D, 0, 5), R0),
            lambda: alu(Opcode.SELECT, R0, immediate(2), R0, R1),
            lambda: alu(Opcode.EQ, Operand(OperandKind.D, 0, 2), R0, R1),
            lambda: alu(Opcode.SHL, R0, R0, immediate(32)),
            lambda: Instruction(Opcode.EX, R0, (R1,)),
            lambda: Instruction(Opcode.EX, R0, (R1,), extract_offset=31, extract_width=2),
            lambda: Instruction(Opcode.MOV, R0, (R1,), extract_width=1),
            lambda: Instruction(Opcode.MOV, R0, (R1,), target=1),
            lambda: Instruction(Opcode.BR, args=(immediate(1),)),
            lambda: Instruction(Opcode.READ2, R0, (ADDRESS,), charge=Charge.ACCESS),
            lambda: Instruction(Opcode.WRITE2, args=(ADDRESS, R0), charge=Charge.ACCESS),
            lambda: Instruction(Opcode.READ2, Operand(OperandKind.R0, 0, 2), (R0,),
                                charge=Charge.ACCESS),
            lambda: Instruction(Opcode.READ2, Operand(OperandKind.R3, 0, 2), (ADDRESS,),
                                charge=Charge.ACCESS, capture=Operand(OperandKind.D, 0, 2)),
            lambda: Instruction(Opcode.MOV, R0, (R1,), capture=R2),
            lambda: Instruction(Opcode.PAD), lambda: Instruction(Opcode.S),
            lambda: alu(Opcode.ADD, R0, R0, R1, charge=Charge.ACCESS),
        )
        for constructor in bad:
            with self.assertRaises(ValueError):
                constructor()

    def test_pc_cannot_be_aliased_saved_or_dynamically_written(self):
        for dst, src in ((PC, R0), (PC, immediate(1)),
                         (Operand(OperandKind.PC, 1, 15), immediate(1, 15))):
            with self.assertRaises(ValueError):
                alu(Opcode.MOV, dst, src)
        with self.assertRaises(ValueError):
            alu(Opcode.MOV, R0, PC)
        with self.assertRaises(ValueError):
            alu(Opcode.ADD, PC, immediate(1), immediate(1))

    def test_dag_occupied_forward_targets_and_rom_limits(self):
        for target in (0, 1, 3, 65535):
            with self.assertRaises(ValueError):
                Program((Instruction(Opcode.JUMP, target=target), None, S))
        with self.assertRaises(ValueError):
            Program((Instruction(Opcode.BR, args=(immediate(1),), target=2), None, S))
        with self.assertRaises(ValueError):
            Program((alu(Opcode.MOV, R0, immediate(0)),))
        with self.assertRaises(ValueError):
            Program((S, Instruction(Opcode.JUMP, target=0)))
        for sites in ((), (None,), (None, S)):
            with self.assertRaises(ValueError):
                Program(sites)
        validate(Program((S,), base=65534))
        with self.assertRaises(ValueError):
            Program((S, S), base=65534)
        program = Program((Instruction(Opcode.STAGE, target=4), None, None, None, S))
        self.assertEqual(validate(program).max_steps, 2)

    def test_all_sites_revalidated_before_payment_even_unreachable(self):
        ins = alu(Opcode.MOV, R0, immediate(1))
        program = Program((S, ins, S))
        object.__setattr__(ins, "args", (True,))
        state, scratch = fixture()
        before = state.snapshot(), scratch.snapshot()
        with self.assertRaises(TypeError):
            execute(program, state, scratch)
        self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_control_path_bound_not_stored_address_count(self):
        ca = alu(Opcode.MOV, R0, immediate(0), charge=Charge.CONTROL_A)
        cb = replace(ca, charge=Charge.CONTROL_B)
        program = Program((ca,) * 256 + (cb,) * 256 + (S,))
        proof = validate(program)
        self.assertEqual(proof.control_path_bound, (256, 256))
        self.assertEqual(proof.max_steps, 513)
        with self.assertRaises(ValueError):
            Program((ca,) * 257 + (S,))
        with self.assertRaises(ValueError):
            Program((ca, cb, ca, S))
        with self.assertRaises(ValueError):
            Program((cb, S))
        # Two alternatives share A, using 402 CONTROL sites but only 202 on a path.
        branch = Instruction(Opcode.BR, args=(Operand(OperandKind.D, 0, 1),),
                             target=202, charge=Charge.CONTROL_A)
        jump = Instruction(Opcode.JUMP, target=402, charge=Charge.CONTROL_A)
        program = Program((branch,) + (ca,) * 200 + (jump,) + (ca,) * 200 + (S,))
        self.assertEqual(validate(program).control_path_bound, (202, 0))
        self.assertEqual(validate(program).max_steps, 203)


class TestInstructionEffects(unittest.TestCase):
    def test_narrow_mov_add_preserve_neighbors_all_widths(self):
        for width in range(1, 33):
            dst = Operand(OperandKind.D, 7, width)
            scratch = Scratch(b"\xff" * 32)
            put(scratch, PC, 0)
            event, _, scratch = one(alu(Opcode.MOV, dst, immediate(0, width)), scratch=scratch)
            expected = (MASK32 | (MASK32 << 32) | (MASK32 << 64)) & ~(((1 << width) - 1) << 7)
            self.assertEqual(int.from_bytes(scratch.snapshot()[:12], "little"), expected)
            self.assertEqual(event.paid, meter.Cost(1))
            put(scratch, PC, 0)
            put(scratch, dst, (1 << width) - 1)
            event, _, _ = one(alu(Opcode.ADD, dst, dst, immediate(1, width)), scratch=scratch)
            self.assertEqual(event.value, 0)

    def test_packed_unsigned_w_increment_across_sign_bit(self):
        word = Operand(OperandKind.D, 32, 32)
        for w in (15, 19):
            scratch = Scratch()
            lower = (1 << 27) - 137
            put(scratch, word, (w << 27) | lower)
            result, _, _ = one(alu(Opcode.ADD, word, word, immediate(1 << 27)), scratch=scratch)
            self.assertEqual(result.value, ((w + 1) << 27) | lower)
            self.assertEqual(scratch.read_bits(59, 5), w + 1)
            self.assertEqual(scratch.read_bits(32, 27), lower)

    def test_signed_ex_not_mov_and_nonzero_bit_extraction(self):
        raw = Operand(OperandKind.D, 64, 16)
        scratch = Scratch()
        put(scratch, raw, 65535)
        result, _, _ = one(alu(Opcode.MOV, R0, raw), scratch=scratch)
        self.assertEqual(result.value, 65535)
        put(scratch, PC, 0)
        ins = Instruction(Opcode.EX, R0, (raw,), number=SIGNED, extract_width=16)
        result, _, _ = one(ins, scratch=scratch)
        self.assertEqual(signed(result.value), -1)
        put(scratch, PC, 0)
        put(scratch, R1, 0b10110100)
        result, _, _ = one(Instruction(Opcode.EX, R0, (R1,), extract_offset=2,
                                      extract_width=4), scratch=scratch)
        self.assertEqual(result.value, 13)

    def test_arithmetic_and_logical_shift(self):
        for number, expected in ((SIGNED, MASK32), (NumberType.UNSIGNED, 0x7fffffff)):
            scratch = Scratch()
            put(scratch, R1, -1)
            result, _, _ = one(alu(Opcode.SHR, R0, R1, immediate(1), number=number),
                               scratch=scratch)
            self.assertEqual(result.value, expected)
        for width in (1, 2, 8, 16, 32):
            for shift in (0, 31):
                result, _, _ = one(alu(Opcode.SHR, R0, immediate((1 << width) - 1, width),
                                      immediate(shift)))
                self.assertEqual(result.value, ((1 << width) - 1) >> shift)
        for shift in range(32):
            scratch = Scratch()
            put(scratch, R1, -12345)
            result, _, _ = one(alu(Opcode.SHR, R0, R1, immediate(shift, 5), number=SIGNED),
                               scratch=scratch)
            self.assertEqual(signed(result.value), -12345 >> shift)

    def test_unsigned_wrap_and_checked_signed_overflow(self):
        for ins, expected in ((alu(Opcode.ADD, R0, immediate(MASK32), immediate(1)), 0),
                              (alu(Opcode.SUB, R0, immediate(0), immediate(1)), MASK32),
                              (alu(Opcode.NEG, R0, immediate(1)), MASK32),
                              (alu(Opcode.SHL, R0, immediate(1 << 31), immediate(1)), 0)):
            self.assertEqual(one(ins)[0].value, expected)
        for ins in (alu(Opcode.ADD, R0, n((1 << 31) - 1), n(1), number=SIGNED),
                    alu(Opcode.SUB, R0, n(-(1 << 31)), n(1), number=SIGNED),
                    alu(Opcode.NEG, R0, n(-(1 << 31)), number=SIGNED),
                    alu(Opcode.SHL, R0, n(1 << 30), immediate(1), number=SIGNED)):
            state, scratch = fixture()
            before = state.snapshot(), scratch.snapshot()
            with self.assertRaises(OverflowError):
                step(Program((ins, S)), state, scratch)
            self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_boolean_comparison_and_select(self):
        for op, expected in ((Opcode.AND, 8), (Opcode.OR, 14), (Opcode.XOR, 6)):
            self.assertEqual(one(alu(op, R0, immediate(12), immediate(10)))[0].value, expected)
        self.assertEqual(one(alu(Opcode.NOT, R0, immediate(0)))[0].value, MASK32)
        for op, expected in ((Opcode.LT, 1), (Opcode.LE, 1), (Opcode.GT, 0),
                             (Opcode.GE, 0), (Opcode.EQ, 0), (Opcode.NE, 1)):
            self.assertEqual(one(alu(op, R0, n(-1), n(0), number=SIGNED))[0].value, expected)
        self.assertEqual(one(alu(Opcode.LT, R0, immediate(MASK32), immediate(0)))[0].value, 0)
        for pred in (0, 1):
            self.assertEqual(one(alu(Opcode.SELECT, R0, immediate(pred), n(-3), n(9)))[0].value,
                             (-3 if pred else 9) & MASK32)

    def test_runtime_bad_predicate_shift_are_predebit(self):
        for ins in (alu(Opcode.SELECT, R0, R1, immediate(1), immediate(0)),
                    alu(Opcode.SHL, R0, R0, R1),
                    Instruction(Opcode.BR, args=(R1,), target=1)):
            state, scratch = fixture()
            put(scratch, R1, 32)
            before = state.snapshot(), scratch.snapshot()
            with self.assertRaises(ValueError):
                step(Program((ins, S)), state, scratch)
            self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_stage_jump_and_literal_pc_mov_exact_next_semantics(self):
        for ins in (Instruction(Opcode.STAGE, target=2), Instruction(Opcode.JUMP, target=2),
                    alu(Opcode.MOV, PC, immediate(2, 16))):
            state, scratch = fixture()
            program = Program((ins, None, alu(Opcode.MOV, R0, immediate(99)), S))
            result = step(program, state, scratch)
            self.assertEqual(result.next_pc, 2)
            self.assertEqual(get(scratch, PC), 2)
            self.assertEqual(step(program, state, scratch).value, 99)

    def test_taken_and_untaken_branch_both_pay_and_use_only_scratch_pc(self):
        program = Program((Instruction(Opcode.BR, args=(Operand(OperandKind.D, 0, 1),),
                                       target=2), alu(Opcode.MOV, R0, immediate(7)), S))
        for pred in (0, 1):
            state, scratch = fixture()
            scratch.write_bits(0, 1, pred)
            result = step(program, state, scratch)
            self.assertEqual(result.paid.energy, 1)
            self.assertEqual(get(scratch, PC), 2 if pred else 1)
            # A trusted fixture changes the only authoritative PC. No saved
            # result, counter or host continuation can override this field.
            put(scratch, PC, 2)
            self.assertIs(step(program, state, scratch).status, StepStatus.HALT)

    def test_s_clears_all_scratch_and_never_writes_pc_afterward(self):
        program = Program((S, alu(Opcode.MOV, R0, immediate(42)), S), base=10)
        state, _ = fixture(energy=9)
        scratch = Scratch(b"\xff" * 32)
        put(scratch, PC, 10)
        before = state.snapshot()
        with patch.object(Scratch, "write_bits", side_effect=AssertionError("post-S write")):
            result = execute(program, state, scratch)
        self.assertEqual(len(result.steps), 1)
        self.assertIs(result.steps[0].status, StepStatus.HALT)
        self.assertIsNone(result.steps[0].next_pc)
        self.assertEqual(scratch.snapshot(), bytes(32))
        self.assertEqual(state.energy, 1)
        self.assertEqual(state.snapshot()[:225], before[:225])

    def test_trace_is_post_effect_immutable_and_not_an_input(self):
        state, scratch = fixture()
        program = Program((alu(Opcode.MOV, R0, immediate(17)), S))
        event = step(program, state, scratch)
        self.assertEqual(event.value, get(scratch, R0))
        self.assertEqual(event.next_pc, get(scratch, PC))
        with self.assertRaises(FrozenInstanceError):
            setattr(event, "value", 42)
        with self.assertRaises(TypeError):
            step(unchecked(event), state, scratch)
        with self.assertRaises(TypeError):
            execute(program, state, scratch, mode=unchecked(meter.GateResult(True, True)))

    def test_alu_has_no_state_ram_snapshot_or_resource_operand(self):
        state, scratch = fixture()
        with patch.object(State, "read_bits", side_effect=AssertionError("unpaid RAM")), \
                patch.object(State, "snapshot", side_effect=AssertionError("snapshot")), \
                patch.object(Scratch, "snapshot", side_effect=AssertionError("snapshot")):
            event = step(Program((alu(Opcode.ADD, R0, immediate(2), immediate(3)), S)),
                         state, scratch)
        self.assertEqual(event.value, 5)
        self.assertEqual(set(OperandKind), {OperandKind.D, OperandKind.R0, OperandKind.R1,
                                         OperandKind.R2, OperandKind.R3, OperandKind.PC,
                                         OperandKind.ADDRESS, OperandKind.FLAGS,
                                         OperandKind.IMMEDIATE})


class TestPaidAccessAndFragments(unittest.TestCase):
    def test_read2_reply_capture_raw_invalid_symbols_and_separate_address_alu(self):
        reply = Operand(OperandKind.R0, 0, 2)
        capture = Operand(OperandKind.D, 30, 2)
        for lane in (0, 19, 20, 79, 80, 899, 924, 971):
            for symbol in range(4):
                state, scratch = fixture()
                state.write_lane(lane, symbol)
                put(scratch, R0, MASK32)
                scratch.write_bits(0, 32, MASK32)
                program = Program((alu(Opcode.MOV, ADDRESS, immediate(lane, 11)),
                                   Instruction(Opcode.READ2, reply, (ADDRESS,),
                                               charge=Charge.ACCESS, capture=capture), S))
                event = step(program, state, scratch)
                self.assertEqual(event.paid, meter.Cost(1))
                event = step(program, state, scratch)
                self.assertEqual(event.paid, meter.Cost(physical.lane_read_cost(lane)))
                self.assertEqual(get(scratch, R0), (MASK32 & ~3) | symbol)
                self.assertEqual(scratch.read_bits(0, 32), (MASK32 & ~(3 << 30)) | symbol << 30)
                self.assertEqual(event.lane, lane)
                self.assertEqual(state.energy, 65535 - 1 - (17 if lane < 80 else 10))

    def test_eight_q_reads_then_paid_signed_ex(self):
        state, scratch = fixture()
        for i in range(8):
            state.write_lane(80 + i, 3)
        put(scratch, R0, 0x12340000)
        sites = []
        for i in range(8):
            sites.append(alu(Opcode.MOV, ADDRESS, immediate(80 + i, 11)))
            sites.append(Instruction(Opcode.READ2, Operand(OperandKind.R0, 2 * i, 2),
                                     (ADDRESS,), charge=Charge.ACCESS))
        sites.extend((Instruction(Opcode.EX, R0, (R0,), number=SIGNED, extract_width=16), S))
        result = execute(Program(tuple(sites)), state, scratch)
        self.assertEqual(result.steps[15].value, 3)
        self.assertEqual(signed(result.steps[16].value), -1)
        self.assertEqual(sum(event.paid.energy for event in result.steps), 8 + 80 + 1 + 8)

    def test_write2_actual_source_extraction_same_value_and_aux_route(self):
        source = Operand(OperandKind.R2, 14, 2)
        for lane in (0, 20, 40, 60, 80, 81, 82, 83, 924, 971):
            state, scratch = fixture(material=(10, 20, 30, 40))
            put(scratch, R2, 0xdeadbeef)
            original = get(scratch, R2)
            symbol = (original >> 14) & 3
            state.write_lane(lane, symbol)
            ins = Instruction(Opcode.WRITE2, args=(immediate(lane, 11), source), charge=Charge.ACCESS)
            quote = physical.write_quote((lane,))
            event = step(Program((ins, S)), state, scratch)
            self.assertEqual(event.paid, meter.Cost(quote.energy, quote.material))
            self.assertEqual(quote.energy, 23 if lane < 80 else 14)
            self.assertEqual(state.read_lane(lane), symbol)
            self.assertEqual(get(scratch, R2), original)
            self.assertEqual(tuple(state.read_material(i) for i in range(4)),
                             tuple(x - y for x, y in zip((10, 20, 30, 40), quote.material)))

    def test_forbidden_literal_and_dynamic_resource_reserve_lanes(self):
        reply = Operand(OperandKind.R0, 0, 2)
        forbidden = (*range(900, 924), *range(972, 1104), 1104, 2047)
        for lane, op in product(forbidden, (Opcode.READ2, Opcode.WRITE2)):
            with self.subTest(lane=lane, opcode=op):
                def access(address):
                    return (Instruction(op, reply, (address,), charge=Charge.ACCESS)
                            if op is Opcode.READ2 else
                            Instruction(op, args=(address, reply), charge=Charge.ACCESS))

                error = PermissionError if lane < 1104 else ValueError
                with self.assertRaises(error):
                    access(immediate(lane, 11))
                state, scratch = fixture()
                put(scratch, ADDRESS, lane)
                before = state.snapshot(), scratch.snapshot()
                with patch.object(meter, "debit", wraps=meter.debit) as debit:
                    with self.assertRaises(error):
                        step(Program((access(ADDRESS), S)), state, scratch)
                debit.assert_not_called()
                self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_debit_before_memory_read_and_write(self):
        state, scratch = fixture()
        reply = Operand(OperandKind.R0, 0, 2)
        read = State.read_lane

        def observed_read(owner, lane):
            self.assertEqual(owner.energy, 65535 - 17)
            self.assertEqual(get(scratch, PC), 0)
            return read(owner, lane)

        with patch.object(State, "read_lane", observed_read):
            step(Program((Instruction(Opcode.READ2, reply, (immediate(0, 11),),
                                      charge=Charge.ACCESS), S)), state, scratch)
        state, scratch = fixture()
        put(scratch, reply, 1)
        write = State.write_lane

        def observed_write(owner, lane, symbol):
            self.assertEqual(owner.energy, 65535 - 23)
            self.assertEqual(owner.P2, 254)
            self.assertEqual(owner.P0, 255)
            self.assertEqual(get(scratch, PC), 0)
            write(owner, lane, symbol)

        with patch.object(State, "write_lane", observed_write):
            step(Program((Instruction(Opcode.WRITE2, args=(immediate(40, 11), reply),
                                      charge=Charge.ACCESS), S)), state, scratch)

    def test_energy_residue_material_equality_and_wrong_source_failure(self):
        source = Operand(OperandKind.R0, 0, 2)
        ins = Instruction(Opcode.WRITE2, args=(immediate(60, 11), source), charge=Charge.ACCESS)
        program = Program((ins, S))
        for energy, stock, passes in ((32, 1, True), (31, 1, False), (65535, 0, False)):
            state, scratch = fixture(energy, (255, 255, 255, stock))
            before = state.snapshot(), scratch.snapshot()
            if passes:
                step(program, state, scratch)
                self.assertEqual(state.energy, 9)
                self.assertEqual(state.P3, 0)
                step(program, state, scratch)
                self.assertEqual(state.energy, 1)
            else:
                with self.assertRaises(meter.InsufficientResources):
                    step(program, state, scratch)
                self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_unaffordable_read_has_no_payload_read_or_pc_change(self):
        state, scratch = fixture(25)
        ins = Instruction(Opcode.READ2, Operand(OperandKind.R0, 0, 2),
                          (immediate(0, 11),), charge=Charge.ACCESS)
        before = state.snapshot(), scratch.snapshot()
        with patch.object(State, "read_lane", side_effect=AssertionError("unpaid read")):
            with self.assertRaises(meter.InsufficientResources):
                step(Program((ins, S)), state, scratch)
        self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_persistent_bit_merge_requires_read_alu_write_not_free_masking(self):
        reply = Operand(OperandKind.R0, 0, 2)
        program = Program((Instruction(Opcode.READ2, reply, (immediate(80, 11),),
                                       charge=Charge.ACCESS),
                           alu(Opcode.AND, reply, reply, immediate(2, 2)),
                           alu(Opcode.OR, reply, reply, immediate(1, 2)),
                           Instruction(Opcode.WRITE2, args=(immediate(80, 11), reply),
                                       charge=Charge.ACCESS), S))
        for symbol in range(4):
            state, scratch = fixture()
            state.write_lane(80, symbol)
            state.write_lane(81, 2)
            result = execute(program, state, scratch)
            self.assertEqual(state.read_lane(80), symbol | 1)
            self.assertEqual(state.read_lane(81), 2)
            self.assertEqual([event.paid.energy for event in result.steps], [10, 1, 1, 14, 8])
            self.assertEqual(state.P0, 254)

    def test_unaffordable_s_preserves_dirty_scratch(self):
        state, _ = fixture(8)
        scratch = Scratch(b"\xff" * 32)
        put(scratch, PC, 0)
        before = state.snapshot(), scratch.snapshot()
        with self.assertRaises(meter.InsufficientResources):
            step(Program((S,)), state, scratch)
        self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_full_control_envelopes_paid_once_not_per_instruction(self):
        ca = alu(Opcode.MOV, R0, immediate(3), charge=Charge.CONTROL_A)
        cb = replace(ca, charge=Charge.CONTROL_B)
        for count in (1, 256):
            state, scratch = fixture(521)
            result = execute(Program((ca,) * count + (cb,) * count + (S,)), state, scratch)
            self.assertEqual([payment.paid.energy for payment in result.envelopes], [256, 256])
            self.assertEqual([payment.region for payment in result.envelopes],
                             [Charge.CONTROL_A, Charge.CONTROL_B])
            self.assertTrue(all(event.paid == meter.ZERO for event in result.steps[:-1]))
            self.assertEqual(state.energy, 1)
            self.assertEqual(len(result.steps), 2 * count + 1)
            self.assertTrue(scratch.is_zero())
        state, scratch = fixture(520)
        before = state.snapshot(), scratch.snapshot()
        with self.assertRaises(FragmentFailure) as caught:
            execute(Program((ca, cb, S)), state, scratch)
        self.assertIsInstance(caught.exception.__cause__, meter.InsufficientResources)
        self.assertEqual(caught.exception.prefix.envelopes, ())
        self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_unvisited_control_region_still_prepays_no_receipt_or_free_step(self):
        program = Program((Instruction(Opcode.JUMP, target=2, charge=Charge.CONTROL_A),
                           alu(Opcode.MOV, R0, immediate(1), charge=Charge.CONTROL_B), S))
        state, scratch = fixture()
        with self.assertRaises(ValueError):
            step(program, state, scratch)
        result = execute(program, state, scratch)
        self.assertEqual(len(result.envelopes), 2)
        self.assertEqual([e.pc for e in result.steps], [0, 2])
        self.assertEqual(state.energy, 65535 - 512 - 8)
        with self.assertRaises(TypeError):
            execute(program, state, scratch, mode=unchecked(True))

    def test_failure_preserves_actual_paid_prefix_not_atomic_rollback(self):
        reply = Operand(OperandKind.R0, 0, 2)
        program = Program((alu(Opcode.MOV, ADDRESS, immediate(40, 11), charge=Charge.CONTROL_A),
                           Instruction(Opcode.WRITE2, args=(ADDRESS, reply), charge=Charge.ACCESS), S))
        state, scratch = fixture(material=(255, 255, 0, 255))
        with self.assertRaises(FragmentFailure) as caught:
            execute(program, state, scratch)
        prefix = caught.exception.prefix
        self.assertEqual(len(prefix.envelopes), 1)
        self.assertEqual(len(prefix.steps), 1)
        self.assertEqual(state.energy, 65535 - 256)
        self.assertEqual(get(scratch, ADDRESS), 40)
        self.assertEqual(get(scratch, PC), 1)
        self.assertEqual(state.read_lane(40), 2)
        with self.assertRaises(ValueError):
            step(program, state, scratch)
        with self.assertRaises(ValueError):
            execute(program, state, scratch)  # no implicit entry-PC overwrite

    def test_paid_kernel_prefix_then_overflow_or_shortage(self):
        for last, energy, error in (
            (alu(Opcode.ADD, R0, n((1 << 31) - 1), n(1), number=SIGNED), 65535, OverflowError),
            (alu(Opcode.MOV, R0, immediate(9)), 10, meter.InsufficientResources),
        ):
            state, scratch = fixture(energy)
            program = Program((alu(Opcode.MOV, R0, immediate(7)), last, S))
            with self.assertRaises(FragmentFailure) as caught:
                execute(program, state, scratch)
            self.assertIsInstance(caught.exception.__cause__, error)
            self.assertEqual(state.energy, energy - 1)
            self.assertEqual(get(scratch, PC), 1)
            self.assertEqual(get(scratch, R0), 7)
            self.assertEqual(len(caught.exception.prefix.steps), 1)

    def dynamic_access_program(self, op, lane):
        reply = Operand(OperandKind.R0, 0, 2)
        access = (Instruction(op, reply, (ADDRESS,), charge=Charge.ACCESS,
                              capture=Operand(OperandKind.D, 30, 2))
                  if op is Opcode.READ2 else
                  Instruction(op, args=(ADDRESS, reply), charge=Charge.ACCESS))
        return Program((alu(Opcode.MOV, ADDRESS, immediate(lane, 11), charge=Charge.CONTROL_A),
                        alu(Opcode.MOV, R0, immediate(3)), access, S))

    def check_dynamic_access_failure(self, op, lanes, error: type[Exception] = PermissionError):
        for lane in lanes:
            with self.subTest(opcode=op, lane=lane):
                program = self.dynamic_access_program(op, lane)
                state, _ = fixture(1024, (5, 6, 7, 8))
                scratch = Scratch(b"\xa5" * 32)
                put(scratch, PC, 0)
                expected_state = bytearray(state.snapshot())
                expected_scratch = bytearray(scratch.snapshot())
                # Independent byte oracle: only C256, KERNEL1, ADDRESS, R0
                # and the two completed PC advances may change either image.
                expected_state[225:227] = (767).to_bytes(2, "little")
                expected_scratch[12:16] = (3).to_bytes(4, "little")
                expected_scratch[28:30] = (2).to_bytes(2, "little")
                address_flags = int.from_bytes(expected_scratch[30:32], "little")
                expected_scratch[30:32] = ((address_flags & ~2047) | lane).to_bytes(2, "little")
                with patch.object(meter, "debit", wraps=meter.debit) as debit, \
                        patch.object(State, "read_lane", side_effect=AssertionError("forbidden read")), \
                        patch.object(State, "write_lane", side_effect=AssertionError("forbidden write")), \
                        patch.object(Scratch, "clear", side_effect=AssertionError("unpaid S")):
                    with self.assertRaises(FragmentFailure) as caught:
                        execute(program, state, scratch)
                self.assertIs(type(caught.exception.__cause__), error)
                prefix = caught.exception.prefix
                self.assertEqual(prefix, machine.FragmentResult(
                    ExecutionMode.ENGINEERING_FRAGMENT,
                    (machine.EnvelopePayment(Charge.CONTROL_A, meter.Cost(256)),),
                    (machine.StepResult(0, Opcode.MOV, Charge.CONTROL_A, meter.ZERO,
                                        StepStatus.CONTINUE, 1, lane),
                     machine.StepResult(1, Opcode.MOV, Charge.KERNEL, meter.Cost(1),
                                        StepStatus.CONTINUE, 2, 3)),
                ))
                self.assertEqual([call.args[1] for call in debit.call_args_list],
                                 [meter.Cost(256), meter.ZERO, meter.Cost(1)])
                paid = meter.ZERO
                for payment in prefix.envelopes:
                    paid = meter.add_cost(paid, payment.paid)
                for event in prefix.steps:
                    paid = meter.add_cost(paid, event.paid)
                self.assertEqual(paid, meter.Cost(257))
                self.assertEqual(state.energy, 1024 - paid.energy)
                self.assertEqual(tuple(state.read_material(i) for i in range(4)), (5, 6, 7, 8))
                self.assertEqual(state.snapshot(), bytes(expected_state))
                self.assertEqual(scratch.snapshot(), bytes(expected_scratch))
                self.assertEqual(get(scratch, ADDRESS), lane)
                self.assertEqual(get(scratch, PC), 2)
                self.assertEqual(get(scratch, R0), 3)

    def test_dynamic_read2_resource_failure_preserves_paid_prefix(self):
        self.check_dynamic_access_failure(Opcode.READ2, range(900, 924))

    def test_dynamic_write2_resource_failure_preserves_paid_prefix(self):
        self.check_dynamic_access_failure(Opcode.WRITE2, range(900, 924))

    def test_dynamic_read2_reserve_failure_preserves_paid_prefix(self):
        self.check_dynamic_access_failure(Opcode.READ2, range(972, 1104))

    def test_dynamic_write2_reserve_failure_preserves_paid_prefix(self):
        self.check_dynamic_access_failure(Opcode.WRITE2, range(972, 1104))

    def test_dynamic_out_of_range_neighbor_preserves_paid_prefix(self):
        for op in (Opcode.READ2, Opcode.WRITE2):
            self.check_dynamic_access_failure(op, (1104,), ValueError)

    def test_dynamic_accessible_neighbor_pays_access_and_s(self):
        for op in (Opcode.READ2, Opcode.WRITE2):
            with self.subTest(opcode=op):
                program = self.dynamic_access_program(op, 924)
                state, scratch = fixture(1024, (5, 6, 7, 8))
                state.write_lane(924, 2)
                expected = bytearray(state.snapshot())
                paid = meter.Cost(10) if op is Opcode.READ2 else meter.Cost(14, (1, 0, 0, 0))
                expected[225:227] = (1024 - 257 - paid.energy - 8).to_bytes(2, "little")
                expected[227] -= paid.material[0]
                if op is Opcode.WRITE2:
                    expected[231] = (expected[231] & ~3) | 3
                result = execute(program, state, scratch)
                self.assertEqual(result.envelopes,
                                 (machine.EnvelopePayment(Charge.CONTROL_A, meter.Cost(256)),))
                self.assertEqual([event.paid for event in result.steps],
                                 [meter.ZERO, meter.Cost(1), paid, meter.Cost(8)])
                self.assertEqual(result.steps[2], machine.StepResult(
                    2, op, Charge.ACCESS, paid, StepStatus.CONTINUE, 3,
                    2 if op is Opcode.READ2 else 3, 924))
                self.assertEqual(result.steps[3], machine.StepResult(
                    3, Opcode.S, Charge.EXIT, meter.Cost(8), StepStatus.HALT, None))
                self.assertEqual(state.snapshot(), bytes(expected))
                self.assertEqual(scratch.snapshot(), bytes(32))

    def test_fragment_does_not_wrap_unrelated_errors_or_system_exits(self):
        program = self.dynamic_access_program(Opcode.READ2, 924)
        for error in (TypeError("internal"), OSError("unrelated"), RuntimeError("internal"),
                      KeyboardInterrupt(), SystemExit(2)):
            with self.subTest(error=type(error).__name__):
                state, scratch = fixture(1024)
                with patch.object(physical, "lane_read_cost", side_effect=error):
                    with self.assertRaises(type(error)) as caught:
                        execute(program, state, scratch)
                self.assertIs(caught.exception, error)
                self.assertEqual(state.energy, 767)
                self.assertEqual(get(scratch, PC), 2)
                self.assertEqual(get(scratch, R0), 3)

    def test_immutable_external_local_and_public_tail_sourcewise_bounds(self):
        source = Operand(OperandKind.R0, 0, 2)
        program = Program((Instruction(Opcode.WRITE2, args=(immediate(20, 11), source),
                                       charge=Charge.ACCESS), S))
        tail = meter.Cost(7, (0, 2, 0, 0))
        local = (meter.Cost(8, (0, 1, 0, 0)), meter.ZERO)
        state, scratch = fixture(39, (0, 4, 0, 0))
        result = execute(program, state, scratch, local_remainders=local, public_tail=tail)
        self.assertEqual(state.energy, 8)
        self.assertEqual(state.P1, 3)
        self.assertEqual(result.steps[0].paid, meter.Cost(23, (0, 1, 0, 0)))
        state, scratch = fixture(39, (0, 3, 255, 255))
        before = state.snapshot(), scratch.snapshot()
        with self.assertRaises(meter.InsufficientResources):
            step(program, state, scratch, local_remainders=local, public_tail=tail)
        self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_bad_remainders_and_entry_validate_before_any_payment(self):
        program = Program((alu(Opcode.MOV, R0, immediate(0), charge=Charge.CONTROL_A), S))
        for kwargs in ({"local_remainders": [meter.Cost(8), meter.ZERO]},
                       {"local_remainders": (meter.ZERO, meter.ZERO)},
                       {"public_tail": lambda: meter.ZERO},
                       {"local_remainders": (meter.Cost(meter.INT32_MAX), meter.ZERO)}):
            state, scratch = fixture()
            before = state.snapshot(), scratch.snapshot()
            with self.assertRaises((TypeError, ValueError, OverflowError)):
                unchecked(execute)(program, state, scratch, **kwargs)
            self.assertEqual((state.snapshot(), scratch.snapshot()), before)
        state, scratch = fixture()
        with self.assertRaises(ValueError):
            execute(Program((S,), base=5), state, scratch)
        with self.assertRaises(ValueError):
            step(Program((S,), base=5), state, scratch)


class TestLiteralMicroprograms(unittest.TestCase):
    def run_td(self, program, q, r, m):
        state, scratch = fixture(32)
        for reg, value in zip((R0, R1, R2), (q, r, m)):
            put(scratch, reg, value)
        result = execute(program, state, scratch)
        self.assertIs(result.mode, ExecutionMode.ENGINEERING_FRAGMENT)
        self.assertEqual(len(result.steps), 24)
        self.assertEqual([event.pc for event in result.steps], list(range(24)))
        self.assertEqual(Counter(event.charge for event in result.steps),
                         {Charge.KERNEL: 23, Charge.EXIT: 1})
        self.assertEqual(result.envelopes, ())
        self.assertEqual(state.energy, 1)
        self.assertTrue(scratch.is_zero())
        actual = signed(result.steps[22].value)
        self.assertEqual(actual, reference_td(q, r, m))
        self.assertEqual(actual, arithmetic.td_update(q, r, m))
        return result

    def test_td_23_literal_instructions_word_boundaries_against_fraction(self):
        program = td_program()
        words = (-32768, -257, -256, -12, -4, -1, 0, 1, 4, 12, 256, 257, 32767)
        for q, r, m in product(words, repeat=3):
            self.run_td(program, q, r, m)

    def test_td_all_128_remainders_positive_and_negative_numerators(self):
        program = td_program()
        seen = {False: set(), True: set()}
        for m in range(-256, 257):
            result = self.run_td(program, 0, 0, m)
            numerator = signed(result.steps[9].value)
            remainder = result.steps[11].value
            seen[numerator < 0].add(remainder)
            self.assertEqual(remainder, numerator % 128)
            self.assertEqual(signed(result.steps[10].value), numerator // 128)
        self.assertEqual(seen, {False: set(range(128)), True: set(range(128))})

    def test_td_negative_ties_extreme_numerators_and_live_r0(self):
        program = td_program()
        for reward, numerator, updated in ((-4, -64, 0), (-12, -192, -2), (-1, -16, 0)):
            result = self.run_td(program, 0, reward, 0)
            self.assertEqual(signed(result.steps[9].value), numerator)
            self.assertEqual(signed(result.steps[22].value), updated)
        for q, r, m, numerator in ((32767, -32768, -32768, -1019888),
                                    (-32768, 32767, 32767, 1019889)):
            result = self.run_td(program, q, r, m)
            self.assertEqual(signed(result.steps[9].value), numerator)
        state, scratch = fixture()
        for reg, value in zip((R0, R1, R2), (123, -9, 44)):
            put(scratch, reg, value)
        for _ in range(18):
            step(program, state, scratch)
            self.assertEqual(get(scratch, R0), 123)
        step(program, state, scratch)
        self.assertEqual(signed(get(scratch, R0)), arithmetic.td_update(123, -9, 44))

    def test_terminal_zero_and_signed_reward_ex_are_actual_additional_instructions(self):
        reward = Operand(OperandKind.D, 64, 16)
        program = Program((Instruction(Opcode.EX, R1, (reward,), number=SIGNED, extract_width=16),
                           alu(Opcode.MOV, R2, immediate(0)), *td_program().instructions))
        state, scratch = fixture()
        put(scratch, R0, 127)
        put(scratch, R2, 32767)
        put(scratch, reward, -1)
        result = execute(program, state, scratch)
        self.assertEqual(signed(result.steps[24].value), arithmetic.td_update(127, -1, 32767, True))
        self.assertEqual(len(result.steps), 26)
        self.assertEqual(sum(event.paid.energy for event in result.steps), 25 + 8)

    def test_td_and_selection_do_not_call_pure_reference_helpers(self):
        for program in (td_program(), selection_program()):
            state, scratch = fixture()
            put(scratch, R3, MASK32)  # dead temporary cannot act as a hidden Q/rank cache
            with patch.object(arithmetic, "td_update", side_effect=AssertionError("not microcode")), \
                    patch.object(arithmetic, "select_action", side_effect=AssertionError("not microcode")):
                execute(program, state, scratch)

    def test_selection_seven_maximal_subsets_all_96_ranks_actual_21_plus_padding(self):
        program = selection_program()
        cases = 0
        for mask, b, t, x in product(range(1, 8), range(2), range(3), range(16)):
            row = tuple(-1 if mask & (1 << i) else -32768 for i in range(3))
            state, scratch = fixture(289)
            for reg, value in zip((R0, R1, R2), row):
                put(scratch, reg, value)
            scratch.write_bits(64, 7, b | t << 1 | x << 3)
            result = execute(program, state, scratch)
            kernel = tuple(event for event in result.steps if event.charge is Charge.KERNEL)
            self.assertEqual(len(kernel), 21)
            self.assertEqual(kernel[-1].value, arithmetic.select_action(row, b, t, x))
            maxima = tuple(i for i in range(3) if mask & (1 << i))
            expected = (t if x == 0 or len(maxima) == 3 else
                        maxima[b] if len(maxima) == 2 else maxima[0])
            self.assertEqual(kernel[-1].value, expected)
            self.assertEqual(Counter(event.charge for event in result.steps),
                             {Charge.KERNEL: 21, Charge.CONTROL_A: 3,
                              Charge.PADDING: 3, Charge.EXIT: 1})
            self.assertEqual([event.value for event in result.steps if event.opcode is Opcode.EX],
                             [b, t, x])
            self.assertTrue(all(event.value is None and event.paid.energy == 1
                                for event in result.steps if event.opcode is Opcode.PAD))
            self.assertEqual(sum(p.paid.energy for p in result.envelopes), 256)
            self.assertEqual(state.energy, 1)
            self.assertTrue(scratch.is_zero())
            cases += 1
        self.assertEqual(cases, 672)

    def test_selection_packet_check_is_separate_paid_control_not_padding(self):
        # A constructed caller demonstrates the prerequisite with actual EX,
        # EQ and BR. T=3 exits to S (not a full-service packet-trap handler).
        core = selection_program().instructions
        rank_slot = Operand(OperandKind.D, 64, 7)
        p = Operand(OperandKind.D, 55, 1)
        program = Program((Instruction(Opcode.EX, R3, (rank_slot,),
                                       charge=Charge.CONTROL_A,
                                       extract_offset=1, extract_width=2),
                           alu(Opcode.EQ, p, R3, immediate(3), charge=Charge.CONTROL_A),
                           Instruction(Opcode.BR, args=(p,), target=3 + len(core) - 1,
                                       charge=Charge.CONTROL_A), *core))
        for t in range(4):
            state, scratch = fixture()
            scratch.write_bits(65, 2, t)
            result = execute(program, state, scratch)
            kernel = tuple(event for event in result.steps if event.charge is Charge.KERNEL)
            self.assertEqual(len(kernel), 0 if t == 3 else 21)
            self.assertEqual(len(result.steps), 4 if t == 3 else 31)
            if t != 3:
                self.assertEqual(kernel[-1].value, t)


if __name__ == "__main__":
    unittest.main()