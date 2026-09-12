"""Actual scan instruction fixtures, not experiments or full-service admission.

Independent references and pre-S hooks are test observers only. Inputs are
finite constructed symbols/cues, not final targets, roots, training or draws.
No pure decoder supplies an interpreter output or worker continuation.
"""

from collections import Counter
from dataclasses import FrozenInstanceError, fields
from itertools import product
from typing import Any, cast
import unittest
from unittest.mock import patch

from e3 import coding, kernels, machine, meter, policy
from e3.kernels import make_scan_program, run_scan_fragment
from e3.machine import Charge, Opcode, Operand, OperandKind
from e3.protocol import Code
from e3.state import Scratch, State


def reference_word(payload):
    # Four explicit binary dot-product terms, independent of parity folding.
    return tuple(sum(((payload >> k) & 1) * ((column >> k) & 1)
                     for k in range(4)) % 2
                 for column in (*range(1, 16), 1, 2, 4, 8, 15))


WORDS = tuple(reference_word(payload) for payload in range(16))


def reference(code, symbols):
    words = WORDS if code is Code.BLOCK else ((0,) * 5, (1,) * 5)
    observed = sum(symbol < 2 for symbol in symbols)
    distances = tuple(sum(a < 2 and a != b for a, b in zip(symbols, word))
                      for word in words)
    minimum = min(distances)
    winners = tuple(i for i, distance in enumerate(distances) if distance == minimum)
    tied = len(winners) > 1
    health = (0 if not observed else 1 if tied else
              2 if observed == len(symbols) and minimum == 0 else 3)
    return (None if health < 2 else winners[0], health, observed, tied), distances


def lanes(code, cue):
    base = 20 * (cue // 4)
    return tuple(base + i for i in range(20)) if code is Code.BLOCK else \
        tuple(base + cue % 4 + 4 * i for i in range(5))


def fixture(code, symbols, cue=0, usefulness=1, energy=65535, dirty=True):
    state = State()
    state.energy = energy
    # Nonselected lanes deliberately contain different, potentially misleading
    # binary data; no pristine copy or decode supplied to the interpreter.
    for lane in range(80):
        state.write_lane(lane, (lane // 3) & 1)
    for lane, symbol in zip(lanes(code, cue), symbols):
        state.write_lane(lane, symbol)
    scratch = Scratch(b"\xff" * 32 if dirty else bytes(32))
    scratch.write_bits(64, 4, cue)
    scratch.write_bits(68, 1, usefulness)
    scratch.write_bits(224, 16, 0)
    return state, scratch


def observation_values(value):
    return value.payload, value.health, value.observed, value.tied


class TestScanPrograms(unittest.TestCase):
    def test_strict_representation_only_immutable_generic_rom(self):
        for value in (False, True, 0, 1, "REP", "BLOCK", None, {}, lambda: Code.REP):
            with self.assertRaises(TypeError):
                make_scan_program(cast(Any, value))
        with self.assertRaises(TypeError):
            cast(Any, make_scan_program)(Code.REP, cue=4)
        self.assertEqual({f.name for f in fields(machine.Program)}, {"instructions", "base"})
        for code in Code:
            program = make_scan_program(code)
            self.assertEqual(program, make_scan_program(code))
            self.assertEqual(program.base, 0)
            self.assertIs(type(program.instructions), tuple)
            with self.assertRaises(FrozenInstanceError):
                setattr(program, "base", 1)
            for ins in program.instructions:
                self.assertIs(type(ins), machine.Instruction)
                assert ins is not None
                self.assertNotIn(ins.opcode, (Opcode.PAD, Opcode.BR, Opcode.JUMP, Opcode.WRITE2))
                for operand in (*ins.args, ins.dst, ins.capture):
                    if operand is None:
                        continue
                    self.assertLessEqual(operand.width, 32)
                    if operand.kind is OperandKind.D:
                        self.assertLessEqual(operand.offset + operand.width, 76)
            self.assertEqual(len(State().snapshot()), 276)
            self.assertEqual(len(Scratch().snapshot()), 32)

    def test_exact_static_counts_bases_stage_and_relocations(self):
        for code, alus, reads, base_count, admin in (
            (Code.BLOCK, 3699, 20, 5, 39), (Code.REP, 34, 5, 7, 8),
        ):
            program = make_scan_program(code)
            proof = machine.validate(program)
            self.assertEqual(proof.control_path_bound, (base_count + admin, 0))
            self.assertEqual(proof.regions, (Charge.CONTROL_A,))
            self.assertEqual(proof.max_steps, alus + reads + base_count + admin + 1)
            self.assertLess(len(program.instructions), 65535)
            sites = tuple(ins for ins in program.instructions if ins is not None)
            self.assertEqual(Counter(ins.charge for ins in sites),
                             {Charge.KERNEL: alus, Charge.ACCESS: reads,
                              Charge.CONTROL_A: base_count + admin, Charge.EXIT: 1})
            stage = sites[base_count]
            self.assertIs(stage.opcode, Opcode.STAGE)
            self.assertEqual(stage.target, base_count + 1)
            self.assertEqual(sites[-3].dst, kernels.PAYLOAD)
            self.assertEqual(sites[-2].dst, kernels.HEALTH)
            self.assertIs(sites[-1].opcode, Opcode.S)
            for pc, ins in enumerate(sites):
                if ins.opcode is Opcode.READ2:
                    self.assertEqual(ins.args, (machine.ADDRESS,))
                    self.assertIs(sites[pc - 1].opcode, Opcode.ADD)
                    self.assertIs(sites[pc - 1].charge, Charge.CONTROL_A)
                    self.assertEqual(ins.dst, Operand(OperandKind.R0, 0, 2))
                    assert ins.capture is not None
                    self.assertEqual(ins.capture.width, 2)

    def test_all_320_generated_bits_eleven_step_cells_and_six_step_reductions(self):
        program = make_scan_program(Code.BLOCK)
        sites = tuple(ins for ins in program.instructions if ins is not None)
        self.assertEqual(len(sites), len(program.instructions))
        entries = [pc for pc, ins in enumerate(sites)
                   if ins.dst == kernels.PAYLOAD and ins.opcode is Opcode.MOV
                   and ins.args[0].kind is OperandKind.IMMEDIATE]
        self.assertEqual(len(entries), 16)
        expected_cell = (Opcode.AND, Opcode.SHR, Opcode.XOR, Opcode.SHR,
                         Opcode.XOR, Opcode.AND, Opcode.EX, Opcode.LT,
                         Opcode.NE, Opcode.AND, Opcode.ADD)
        symbols = tuple((3 * i + 1) % 4 for i in range(20))
        state, scratch = fixture(Code.BLOCK, symbols, cue=15)
        result = machine.execute(program, state, scratch)
        self.assertLess(max(e.pc for e in result.steps if e.opcode is Opcode.READ2), entries[0])
        _, distances = reference(Code.BLOCK, symbols)
        best_distance, best, tied = 21, 0, False
        for candidate, entry in enumerate(entries):
            self.assertEqual(result.steps[entry].value, candidate)
            self.assertEqual(result.steps[entry + 1].value, 0)
            self.assertEqual(result.steps[entry + 2].value, candidate)
            running_distance = 0
            for index in range(20):
                start = entry + 3 + 11 * index
                cell = sites[start:start + 11]
                self.assertEqual(tuple(ins.opcode for ins in cell), expected_cell)
                self.assertTrue(all(ins.charge is Charge.KERNEL for ins in cell))
                self.assertEqual(result.steps[start + 5].value, WORDS[candidate][index])
                self.assertEqual(cell[6].args,
                                 (kernels.RAW_LOW if index < 16 else kernels.RAW_HIGH,))
                self.assertEqual(cell[6].extract_offset, 2 * (index % 16))
                self.assertEqual(result.steps[start + 6].value, symbols[index])
                running_distance += int(symbols[index] < 2 and
                                        symbols[index] != WORDS[candidate][index])
                self.assertEqual(result.steps[start + 10].value, running_distance)
            self.assertEqual(running_distance, distances[candidate])
            reduction = entry + 3 + 220
            self.assertEqual(tuple(ins.opcode for ins in sites[reduction:reduction + 6]),
                             (Opcode.LT, Opcode.EQ, Opcode.OR,
                              Opcode.SELECT, Opcode.SELECT, Opcode.SELECT))
            if running_distance < best_distance:
                best_distance, best, tied = running_distance, candidate, False
            elif running_distance == best_distance:
                tied = True
            self.assertEqual(result.steps[reduction + 3].value, int(tied))
            self.assertEqual(result.steps[reduction + 4].value, best)
            self.assertEqual(result.steps[reduction + 5].value, best_distance)


class TestExecutedScans(unittest.TestCase):
    def check_scan(self, code, symbols, cue=0, usefulness=1, dirty=True):
        expected, _ = reference(code, symbols)
        kernel_energy = 4039 if code is Code.BLOCK else 119
        state, scratch = fixture(code, symbols, cue, usefulness,
                                 energy=256 + kernel_energy + 8 + 1, dirty=dirty)
        before = state.snapshot()
        result = run_scan_fragment(code, state, scratch)
        self.assertEqual(observation_values(result.observation), expected)
        trace = result.trace
        self.assertIs(trace.mode, machine.ExecutionMode.ENGINEERING_FRAGMENT)
        self.assertEqual(tuple((p.region, p.paid) for p in trace.envelopes),
                         ((Charge.CONTROL_A, meter.Cost(256)),))
        self.assertEqual(sum(e.paid.energy for e in trace.steps
                             if e.charge in (Charge.KERNEL, Charge.ACCESS)), kernel_energy)
        self.assertEqual(sum(e.paid.energy for e in trace.steps), kernel_energy + 8)
        self.assertEqual([e.pc for e in trace.steps], list(range(len(trace.steps))))
        self.assertEqual(tuple(e.lane for e in trace.steps if e.opcode is Opcode.READ2), lanes(code, cue))
        self.assertTrue(all(e.paid == meter.Cost(17) for e in trace.steps if e.opcode is Opcode.READ2))
        self.assertTrue(all(e.paid == meter.Cost(1) for e in trace.steps if e.charge is Charge.KERNEL))
        self.assertTrue(all(e.paid == meter.ZERO for e in trace.steps if e.charge is Charge.CONTROL_A))
        self.assertTrue(all(e.paid.material == (0, 0, 0, 0) for e in trace.steps))
        self.assertEqual(trace.steps[-2].value, expected[1])
        self.assertEqual(trace.steps[-1].paid, meter.Cost(8))
        self.assertIs(trace.steps[-1].status, machine.StepStatus.HALT)
        self.assertIsNone(trace.steps[-1].next_pc)
        self.assertTrue(scratch.is_zero())
        self.assertEqual(state.energy, 1)
        self.assertEqual(state.snapshot()[:225], before[:225])
        self.assertEqual(state.snapshot()[227:], before[227:])
        return result

    def test_all_1024_repetition_symbol_encodings_all_cues_and_usefulness(self):
        for index, symbols in enumerate(product(range(4), repeat=5)):
            result = self.check_scan(Code.REP, symbols, cue=index % 16,
                                     usefulness=(index // 16) % 2)
            pure = coding.decode_repetition(symbols)
            self.assertEqual(result.observation.payload, pure.payload)
            self.assertEqual(result.observation.health, pure.health)
            self.assertEqual(result.observation.observed, pure.observed)
            self.assertEqual(result.observation.tied, pure.ties_count > 1)

    def test_all_sixteen_block_codewords_all_cues(self):
        for payload, symbols in enumerate(WORDS):
            result = self.check_scan(Code.BLOCK, symbols, cue=payload, usefulness=payload % 2)
            self.assertEqual(result.observation.payload, payload)
            self.assertEqual(result.observation.health, 2)

    def test_block_damaged_punctured_midpoint_and_missing_fixtures(self):
        samples = [(2,) * 20, (3,) * 20, (2, 3) * 10]
        for payload, word in enumerate(WORDS):
            flipped = list(word)
            flipped[payload] ^= 1
            samples.append(tuple(flipped))
            samples.append(word[:12] + (2, 3) * 4)
        # Every raw position, including all high-subword positions, can be the
        # sole observation. Each has eight minimizers, never a forced guess.
        for index in range(20):
            symbols = [2 if i % 2 else 3 for i in range(20)]
            symbols[index] = index % 2
            samples.append(tuple(symbols))
        left, right = WORDS[0], WORDS[1]
        differing = [i for i in range(20) if left[i] != right[i]]
        self.assertEqual(len(differing), 10)
        midpoint = list(left)
        for index in differing[:5]:
            midpoint[index] = right[index]
        samples.append(tuple(midpoint))
        # Deterministic arithmetic fixtures, not random target/seed draws.
        samples.extend(tuple((i * i + k * i + k // 4) % 4 for i in range(20))
                       for k in range(16))
        for index, symbols in enumerate(samples):
            result = self.check_scan(Code.BLOCK, symbols, cue=index % 16)
            pure = coding.decode_block(symbols)
            self.assertEqual(observation_values(result.observation),
                             (pure.payload, pure.health, pure.observed, pure.ties_count > 1))

    def test_same_rom_reused_for_all_acquired_cues_without_compile_time_labels(self):
        for code in Code:
            program = make_scan_program(code)
            word = WORDS[9] if code is Code.BLOCK else (1, 0, 1, 2, 3)
            for cue in range(16):
                state, scratch = fixture(code, word, cue=cue)
                trace = machine.execute(program, state, scratch)
                self.assertEqual(tuple(e.lane for e in trace.steps if e.opcode is Opcode.READ2),
                                 lanes(code, cue))
                self.assertEqual(trace.steps[-3].value, 9 if code is Code.BLOCK else 1)
                self.assertEqual(trace.steps[-2].value, 2 if code is Code.BLOCK else 3)

    def test_pre_s_raw_slots_inputs_neighbors_and_relocations_no_40_bit_snapshot(self):
        for code in Code:
            symbols = tuple(i % 4 for i in range(20 if code is Code.BLOCK else 5))
            state, scratch = fixture(code, symbols, cue=11, usefulness=1)
            clear = Scratch.clear
            captured = []

            def observe_clear(owner):
                self.assertIs(owner, scratch)
                self.assertEqual(state.energy, 65535 - 256 - (4039 if code is Code.BLOCK else 119) - 8)
                captured.append(owner.snapshot())
                clear(owner)

            with patch.object(Scratch, "clear", observe_clear):
                result = run_scan_fragment(code, state, scratch)
            self.assertEqual(len(captured), 1)
            before_s = Scratch(captured[0])  # observer fixture, never re-executed
            for index, symbol in enumerate(symbols):
                self.assertEqual(before_s.read_bits(2 * index, 2), symbol)
            if code is Code.REP:
                self.assertEqual(before_s.read_bits(10, 30), (1 << 30) - 1)
            self.assertEqual(before_s.read_bits(64, 4), 11)
            self.assertEqual(before_s.read_bits(68, 1), 1)
            self.assertEqual(before_s.read_bits(69, 7), 40 + (3 if code is Code.REP else 0))
            self.assertEqual(before_s.read_bits(76, 20), (1 << 20) - 1)
            self.assertEqual(before_s.read_bits(251, 5), 31)
            self.assertEqual(before_s.read_bits(40, 4), result.trace.steps[-3].value)
            self.assertEqual(before_s.read_bits(55, 2), result.observation.health)
            self.assertTrue(scratch.is_zero())

    def test_dirty_registers_and_dead_rep_best_bits_cannot_supply_hidden_inputs(self):
        for code in Code:
            symbols = WORDS[6] if code is Code.BLOCK else (1, 1, 0, 3, 2)
            left = self.check_scan(code, symbols, cue=7, usefulness=0, dirty=False)
            right = self.check_scan(code, symbols, cue=7, usefulness=1, dirty=True)
            self.assertEqual(left.observation, right.observation)

    def test_observer_results_frozen_and_no_pure_helpers_or_snapshots_during_execution(self):
        for code in Code:
            symbols = WORDS[15] if code is Code.BLOCK else (1,) * 5
            state, scratch = fixture(code, symbols, cue=4)
            with patch.object(coding, "decode_block", side_effect=AssertionError("host decoder")), \
                    patch.object(coding, "decode_repetition", side_effect=AssertionError("host decoder")), \
                    patch.object(coding, "encode", side_effect=AssertionError("host encoder")), \
                    patch.object(policy, "decide", side_effect=AssertionError("host policy")), \
                    patch.object(State, "snapshot", side_effect=AssertionError("RAM snapshot")), \
                    patch.object(Scratch, "snapshot", side_effect=AssertionError("scratch snapshot")):
                result = run_scan_fragment(code, state, scratch)
            self.assertEqual(result.observation.payload, 15 if code is Code.BLOCK else 1)
            self.assertEqual(result.observation.health, 2)
            for obj, name in ((result, "observation"), (result.observation, "payload")):
                self.assertFalse(hasattr(obj, "__dict__"))
                with self.assertRaises(FrozenInstanceError):
                    setattr(obj, name, 0)
            self.assertFalse(hasattr(result.observation, "ties_count"))
            with self.assertRaises(TypeError):
                machine.execute(cast(Any, result), state, scratch)


class TestScanPaymentsAndFailures(unittest.TestCase):
    def test_each_read_is_paid_before_effect_no_rereads_or_early_abstention(self):
        for code in Code:
            count = 20 if code is Code.BLOCK else 5
            for symbol in (0, 2, 3):
                state, scratch = fixture(code, (symbol,) * count, cue=15)
                original = State.read_lane
                seen = []
                prefix = 4 if code is Code.BLOCK else 2
                per_cell_alus = 2 if code is Code.BLOCK else 4

                def observe_read(owner, lane):
                    self.assertIs(owner, state)
                    i = len(seen)
                    self.assertEqual(state.energy, 65535 - 256 - prefix -
                                     17 * (i + 1) - per_cell_alus * i)
                    self.assertEqual(lane, lanes(code, 15)[i])
                    seen.append(lane)
                    return original(owner, lane)

                with patch.object(State, "read_lane", observe_read):
                    result = run_scan_fragment(code, state, scratch)
                self.assertEqual(len(seen), count)
                self.assertEqual(result.observation.health, 2 if symbol == 0 else 0)

    def test_no_free_control_entry_and_failed_envelope_has_no_effect(self):
        for code in Code:
            state, scratch = fixture(code, (2,) * (20 if code is Code.BLOCK else 5), energy=264)
            before = state.snapshot(), scratch.snapshot()
            with self.assertRaises(ValueError):
                machine.step(make_scan_program(code), state, scratch)
            with self.assertRaises(machine.FragmentFailure) as caught:
                run_scan_fragment(code, state, scratch)
            self.assertIsInstance(caught.exception.__cause__, meter.InsufficientResources)
            self.assertEqual(caught.exception.prefix.envelopes, ())
            self.assertEqual(caught.exception.prefix.steps, ())
            self.assertEqual((state.snapshot(), scratch.snapshot()), before)

    def test_unaffordable_first_read_retains_paid_prefix_without_payload_or_cleanup(self):
        for code, init in ((Code.BLOCK, 4), (Code.REP, 2)):
            # One short of first READ2 + S + positive residue, after C/init.
            state, scratch = fixture(code, (3,) * (20 if code is Code.BLOCK else 5),
                                     cue=15, energy=256 + init + 17 + 8)
            before = state.snapshot()
            with patch.object(State, "read_lane", side_effect=AssertionError("unpaid read")), \
                    patch.object(Scratch, "clear", side_effect=AssertionError("unpaid S")):
                with self.assertRaises(machine.FragmentFailure) as caught:
                    run_scan_fragment(code, state, scratch)
            prefix = caught.exception.prefix
            self.assertIsInstance(caught.exception.__cause__, meter.InsufficientResources)
            self.assertEqual(len(prefix.envelopes), 1)
            self.assertEqual(sum(e.paid.energy for e in prefix.steps), init)
            self.assertNotIn(Opcode.READ2, [e.opcode for e in prefix.steps])
            self.assertEqual(state.energy, 25)
            self.assertEqual(scratch.read_bits(0, 10), 1023)
            self.assertEqual(scratch.read_bits(240, 11), lanes(code, 15)[0])
            self.assertEqual(scratch.read_bits(224, 16), prefix.steps[-1].next_pc)
            self.assertFalse(scratch.is_zero())
            self.assertEqual(state.snapshot()[:225], before[:225])

    def test_one_below_full_fragment_cost_cannot_return_decode_or_clear_scratch(self):
        for code, kernel in ((Code.BLOCK, 4039), (Code.REP, 119)):
            state, scratch = fixture(code, (0,) * (20 if code is Code.BLOCK else 5),
                                     energy=256 + kernel + 8)
            with self.assertRaises(machine.FragmentFailure) as caught:
                run_scan_fragment(code, state, scratch)
            self.assertIsInstance(caught.exception.__cause__, meter.InsufficientResources)
            self.assertNotIn(Opcode.S, [e.opcode for e in caught.exception.prefix.steps])
            self.assertEqual(state.energy, 9)
            self.assertFalse(scratch.is_zero())

    def test_explicit_tail_and_static_local_bounds_are_forwarded_not_paid_receipts(self):
        for code, kernel in ((Code.BLOCK, 4039), (Code.REP, 119)):
            program = make_scan_program(code)
            tail = meter.Cost(7, (0, 2, 0, 0))
            # Read-only fixed paths: exact remaining kernel/access/S costs,
            # excluding current instruction, C already prepaid and public T.
            local = []
            remaining = 0
            for ins in reversed(program.instructions):
                assert ins is not None
                local.append(meter.Cost(remaining))
                remaining += (8 if ins.opcode is Opcode.S else
                              17 if ins.opcode is Opcode.READ2 else
                              1 if ins.charge is Charge.KERNEL else 0)
            local.reverse()
            state, scratch = fixture(code, (0,) * (20 if code is Code.BLOCK else 5),
                                     energy=256 + kernel + 8 + 7 + 1)
            state.P1 = 2
            result = run_scan_fragment(code, state, scratch,
                                       local_remainders=tuple(local), public_tail=tail)
            self.assertEqual(state.energy, 8)
            self.assertEqual(state.P1, 2)
            self.assertTrue(scratch.is_zero())
            self.assertEqual(result.observation.health, 2)


if __name__ == "__main__":
    unittest.main()