"""Engineering-only E3 codec tests; no target draws, VM, or history worker.

Run this module explicitly with Python 3.13 -B -m unittest test_e3_state.
The random fixture is a local deterministic stdlib PRNG, not an E3 input stream.
"""

import gc
import random
import unittest
from typing import cast

from e3 import Scratch, State, reset
from e3 import state as layout


CANONICAL = b"\xaa" * 20 + bytes(256)
BAD_INTS: tuple[object, ...] = (True, False, 1.0, float("inf"), float("nan"), "1", None)


def reference_read(raw: bytes, offset: int, width: int, signed: bool = False) -> int:
    """Independent per-bit oracle, deliberately not the implementation codec."""
    value = sum(((raw[bit // 8] >> (bit % 8)) & 1) << i
                for i, bit in enumerate(range(offset, offset + width)))
    if signed and value >= 2 ** (width - 1):
        value -= 2 ** width
    return value


def reference_write(raw: bytes, offset: int, width: int, value: int) -> bytes:
    result = bytearray(raw)
    for i, bit in enumerate(range(offset, offset + width)):
        mask = 1 << (bit % 8)
        result[bit // 8] = (result[bit // 8] & ~mask) | (((value >> i) & 1) * mask)
    return bytes(result)


class TestE3State(unittest.TestCase):
    """Component checks only, not G-INFO/G-ERASURE or implementation conformance."""

    def assert_shape(self, body: State | Scratch, size: int) -> None:
        self.assertEqual(len(body.snapshot()), size)
        self.assertIs(type(body.snapshot()), bytes)
        buffers = [item for item in gc.get_referents(body) if type(item) is bytearray]
        self.assertEqual(len(buffers), 1)
        self.assertEqual(len(buffers[0]), size)
        self.assertFalse(hasattr(body, "__dict__"))

    def test_01_exact_selected_layout(self) -> None:
        expected = {
            "STATE_BYTES": 276, "STATE_BITS": 2208, "LANE_COUNT": 1104,
            "CODE_BITS": 160, "CODE_BYTES": 20, "CODE_LANES": 80,
            "AUX_BITS": 2048, "AUX_BYTES": 256, "CODE_OFFSET": 0,
            "Q_OFFSET": 160, "Q_COUNT": 96, "Q_WIDTH": 16,
            "QUERY_OFFSET": 1696, "QUERY_COUNT": 5, "QUERY_WIDTH": 8,
            "STAGING_OFFSET": 1736, "STAGING_COUNT": 4, "STAGING_WIDTH": 8,
            "TRANSITION_OFFSET": 1768, "TRANSITION_WIDTH": 32,
            "TRANSITION_VALID_OFFSET": 1768, "TRANSITION_OBSERVATION_OFFSET": 1769,
            "TRANSITION_ACTION_OFFSET": 1774, "TRANSITION_REWARD_OFFSET": 1776,
            "TRANSITION_TERMINAL_OFFSET": 1792, "TRANSITION_RESERVED_OFFSET": 1793,
            "ENERGY_OFFSET": 1800, "ENERGY_WIDTH": 16, "ENERGY_BYTE": 225,
            "MATERIAL_OFFSET": 1816, "MATERIAL_COUNT": 4, "MATERIAL_WIDTH": 8,
            "MATERIAL_BYTE": 227, "AGE_OFFSET": 1848, "AGE_COUNT": 20,
            "AGE_WIDTH": 4, "METADATA_OFFSET": 1928, "METADATA_WIDTH": 16,
            "CURSOR_OFFSET": 1928, "COUNTER_OFFSET": 1933, "DEAD_OFFSET": 1941,
            "ACQUISITION_FAILED_OFFSET": 1942, "OPERATION_FAILED_OFFSET": 1943,
            "RESERVE_OFFSET": 1944, "RESERVE_BITS": 264, "RESERVE_BYTE": 243,
            "RESOURCE_START_LANE": 900, "RESOURCE_END_LANE": 924,
            "RESERVE_START_LANE": 972, "ENERGY_MAX": 65535, "MATERIAL_MAX": 255,
            "SCRATCH_BYTES": 32, "SCRATCH_BITS": 256,
            "SCRATCH_DECODER_OFFSET": 0, "SCRATCH_DECODER_BITS": 96,
            "SCRATCH_R0_OFFSET": 96, "SCRATCH_R1_OFFSET": 128,
            "SCRATCH_R2_OFFSET": 160, "SCRATCH_R3_OFFSET": 192,
            "SCRATCH_REGISTER_BITS": 32, "SCRATCH_CONTROL_OFFSET": 224,
            "SCRATCH_PC_OFFSET": 224, "SCRATCH_PC_BITS": 16,
            "SCRATCH_ADDRESS_OFFSET": 240, "SCRATCH_ADDRESS_BITS": 11,
            "SCRATCH_FLAGS_OFFSET": 251, "SCRATCH_FLAGS_BITS": 5,
        }
        for name, value in expected.items():
            with self.subTest(name=name):
                self.assertEqual(getattr(layout, name), value)

    def test_02_canonical_image_and_unpowered_resources(self) -> None:
        body = State()
        self.assertEqual(body.snapshot(), CANONICAL)
        self.assertEqual([body.read_lane(i) for i in range(80)], [2] * 80)
        self.assertEqual((body.energy, body.P0, body.P1, body.P2, body.P3), (0,) * 5)
        self.assertIs(layout.SYMBOL_INVALID, 3)
        self.assert_shape(body, 276)
        self.assertEqual(Scratch().snapshot(), bytes(32))

    def test_03_all_byte_patterns_roundtrip_without_sanitization(self) -> None:
        # Every byte position takes every possible value across this fixture.
        for pattern in range(256):
            for raw in (bytes([pattern]) * 276,
                        bytes((pattern + index * 37) % 256 for index in range(276))):
                with self.subTest(pattern=pattern, first=raw[:3]):
                    body = State(raw)
                    self.assertEqual(body.snapshot(), raw)
                    self.assertEqual(State(body.snapshot()).snapshot(), raw)
                    self.assertEqual(body.reset().snapshot(), CANONICAL)
                    self.assertEqual(body.snapshot(), raw)
                    self.assert_shape(body, 276)

    def test_04_every_2208_bit_roundtrip_and_fresh_reset(self) -> None:
        for bit in range(2208):
            raw = bytearray(276)
            raw[bit // 8] = 1 << (bit % 8)
            body = State(raw)
            self.assertEqual(body.snapshot(), bytes(raw))
            child = body.reset()
            self.assertIsNot(child, body)
            self.assertEqual(child.snapshot(), CANONICAL)
            self.assertEqual(body.snapshot(), bytes(raw))
            child.write_bits(0, 1, 1)
            self.assertEqual(body.snapshot(), bytes(raw))

    def test_05_constructor_snapshot_and_clone_do_not_alias(self) -> None:
        source = bytearray((i * 23) % 256 for i in range(276))
        original = bytes(source)
        body = State(source)
        snapshot = body.snapshot()
        clone = State(snapshot)
        source[:] = bytes(276)
        self.assertEqual(body.snapshot(), original)
        body.write_lane(0, body.read_lane(0) ^ 3)
        body.energy = 0
        body.P3 = 0
        self.assertEqual(snapshot, original)
        self.assertEqual(clone.snapshot(), original)
        clone._physics_write_lane(1103, clone._physics_read_lane(1103) ^ 3)
        self.assertNotEqual(clone.snapshot(), body.snapshot())
        self.assertEqual(snapshot, original)

    def test_06_reset_accepts_no_history_and_retains_no_source(self) -> None:
        body = State(b"\xff" * 276)
        source_size = body.__sizeof__()
        children = (body.reset(), State.reset(), reset())
        for child in children:
            self.assertEqual(child.snapshot(), CANONICAL)
            self.assertNotIn(body, gc.get_referents(child))
            self.assertEqual(child.__sizeof__(), source_size)
        self.assertEqual(len({id(child) for child in children}), 3)
        body.write_lane(0, 0)
        for child in children:
            self.assertEqual(child.snapshot(), CANONICAL)
        self.assertEqual(body.snapshot()[1:], b"\xff" * 275)

    def test_07_exact_instance_storage_and_no_hidden_fields(self) -> None:
        for body, size in ((State(), 276), (Scratch(), 32)):
            self.assertEqual(type(body).__slots__, ("__buffer",))
            refs = gc.get_referents(body)
            self.assertEqual(len(refs), 2)  # Its class and exactly one bytearray.
            self.assertIn(type(body), refs)
            self.assert_shape(body, size)
            for name in ("labels", "history", "cached_q", "energy_mirror", "scratch", "alive"):
                with self.assertRaises(AttributeError):
                    setattr(body, name, 1)

    def test_08_little_endian_named_fields_and_packed_metadata(self) -> None:
        body = State()
        body.set_field(160, 16, 0x1234)
        body.set_field(1768, 32, 0xF123ABCD)
        self.assertEqual(body.snapshot()[20:22], b"\x34\x12")
        self.assertEqual(body.snapshot()[221:225], b"\xcd\xab\x23\xf1")
        body.set_field(1776, 16, -32768, signed=True)
        self.assertEqual(body.get_field(1776, 16, signed=True), -32768)
        self.assertEqual(body.snapshot()[222:224], b"\x00\x80")
        body.set_field(1928, 5, 31)  # Invalid cursor is preserved, not normalized.
        body.set_field(1933, 8, 255)
        body.set_field(1941, 3, 7)
        self.assertEqual(body.snapshot()[241:243], b"\xff\xff")

    def test_09_all_widths_alignments_and_signed_extremes(self) -> None:
        for width in range(1, 33):
            for offset in range(160, 168):
                for signed in (False, True):
                    low = -(2 ** (width - 1)) if signed else 0
                    high = 2 ** (width - 1) - 1 if signed else 2 ** width - 1
                    for value in {low, high, 0, -1 if signed else 1}:
                        body = State(b"\xa5" * 276)
                        before = body.snapshot()
                        body.write_bits(offset, width, value, signed)
                        self.assertEqual(body.read_bits(offset, width, signed), value)
                        self.assertEqual(body.snapshot(), reference_write(before, offset, width, value))
                    for value in (low - 1, high + 1):
                        before = body.snapshot()
                        with self.assertRaises(ValueError):
                            body.write_bits(offset, width, value, signed)
                        self.assertEqual(body.snapshot(), before)

    def test_10_deterministic_random_differential_and_constant_storage(self) -> None:
        rng = random.Random(0xE3_020409)
        initial = bytes(rng.randrange(256) for _ in range(276))
        body = State(initial)
        expected = initial
        allocation = body.__sizeof__()
        for _ in range(2000):
            width = rng.randrange(1, 33)
            start, stop = rng.choice(((0, 1800), (1848, 1944)))
            offset = rng.randrange(start, stop - width + 1)
            signed = bool(rng.randrange(2))
            value = rng.randrange(-(1 << (width - 1)), 1 << (width - 1)) if signed else rng.randrange(1 << width)
            body.write_bits(offset, width, value, signed)
            expected = reference_write(expected, offset, width, value)
            self.assertEqual(body.read_bits(offset, width, signed), reference_read(expected, offset, width, signed))
            self.assertEqual(body.snapshot(), expected)
            self.assertEqual(body.snapshot()[225:231], initial[225:231])
            self.assertEqual(body.snapshot()[243:], initial[243:])
            self.assertEqual(body.__sizeof__(), allocation)
            self.assert_shape(body, 276)

    def test_11_sub_two_bit_codec_preserves_neighbors(self) -> None:
        for lane in (0, 79, 80, 848, 899, 924, 971):
            for symbol in range(4):
                for bit in range(2):
                    for value in range(2):
                        body = State(b"\x69" * 276)
                        body.write_lane(lane, symbol)
                        before = body.snapshot()
                        body.write_bits(lane * 2 + bit, 1, value)
                        self.assertEqual(body.snapshot(), reference_write(before, lane * 2 + bit, 1, value))
                        self.assertEqual(body.read_bits(lane * 2 + (1 - bit), 1), (symbol >> (1 - bit)) & 1)

    def test_12_every_accessible_lane_and_all_raw_symbols(self) -> None:
        body = State(b"\x5a" * 276)
        count = 0
        for lane in range(1104):
            if 900 <= lane < 924 or lane >= 972:
                continue
            count += 1
            for symbol in range(4):
                before = body.snapshot()
                body.write_lane(lane, symbol)
                self.assertEqual(body.read_lane(lane), symbol)
                self.assertEqual(body.snapshot(), reference_write(before, lane * 2, 2, symbol))
        self.assertEqual(count, 948)
        self.assert_shape(body, 276)

    def test_13_every_typed_and_reserve_lane_and_bit_rejected_as_ram(self) -> None:
        body = State(b"\xff" * 276)
        before = body.snapshot()
        for lane in (*range(900, 924), *range(972, 1104)):
            with self.assertRaises(PermissionError):
                body.read_lane(lane)
            with self.assertRaises(PermissionError):
                body.write_lane(lane, 0)
            for offset in (2 * lane, 2 * lane + 1):
                with self.assertRaises(PermissionError):
                    body.get_field(offset, 1)
                with self.assertRaises(PermissionError):
                    body.set_field(offset, 1, 0)
            self.assertEqual(body.snapshot(), before)

    def test_14_straddling_restricted_fields_fails_without_mutation(self) -> None:
        body = State(b"\x6d" * 276)
        before = body.snapshot()
        for offset, width in ((1799, 2), (1784, 32), (1847, 2), (1832, 32), (1943, 2), (1928, 32)):
            for signed in (False, True):
                with self.assertRaises(PermissionError):
                    body.read_bits(offset, width, signed)
                with self.assertRaises(PermissionError):
                    body.write_bits(offset, width, 0, signed)
                self.assertEqual(body.snapshot(), before)
        for offset, width in ((1768, 32), (1848, 32), (1928, 16), (1943, 1)):
            self.assertEqual(body.read_bits(offset, width), reference_read(before, offset, width))

    def test_15_typed_resources_are_sole_packed_checked_values(self) -> None:
        body = State(b"\x33" * 276)
        for value in (0, 1, 255, 256, 32767, 32768, 65535):
            before = body.snapshot()
            body.energy = value
            self.assertEqual(body.energy, value)
            self.assertEqual(body.snapshot(), reference_write(before, 1800, 16, value))
        for index in range(4):
            for value in range(256):
                before = body.snapshot()
                setattr(body, f"P{index}", value)
                self.assertEqual(body.read_material(index), value)
                self.assertEqual(getattr(body, f"P{index}"), value)
                self.assertEqual(body.snapshot(), reference_write(before, 1816 + 8 * index, 8, value))
            body.write_material(index, 128)
            self.assertEqual(getattr(body, f"P{index}"), 128)
        self.assertEqual(body.snapshot()[225:231], b"\xff\xff\x80\x80\x80\x80")
        restored = State(body.snapshot())
        self.assertEqual((restored.energy, restored.P0, restored.P1, restored.P2, restored.P3), (65535, 128, 128, 128, 128))
        self.assert_shape(body, 276)

    def test_16_invalid_resource_types_and_overflows_are_atomic(self) -> None:
        body = State(b"\x77" * 276)
        before = body.snapshot()
        for name, cap in (("energy", 65535), ("P0", 255), ("P1", 255), ("P2", 255), ("P3", 255)):
            for value in BAD_INTS:
                with self.assertRaises(TypeError):
                    setattr(body, name, value)
            for value in (-1, cap + 1, 1 << 4096, -(1 << 4096)):
                with self.assertRaises(ValueError):
                    setattr(body, name, value)
            self.assertEqual(body.snapshot(), before)
        for index in BAD_INTS:
            with self.assertRaises(TypeError):
                body.read_material(cast(int, index))
            with self.assertRaises(TypeError):
                body.write_material(cast(int, index), 0)
        for index in (-1, 4, 1 << 4096):
            with self.assertRaises(ValueError):
                body.write_material(index, 0)
            with self.assertRaises(ValueError):
                body.read_material(index)
        for value in (*BAD_INTS, -1, 256):
            with self.assertRaises((TypeError, ValueError)):
                body.write_material(0, cast(int, value))
        self.assertEqual(body.snapshot(), before)

    def test_17_raw_invalid_fields_are_not_cleaned_by_unrelated_operations(self) -> None:
        body = State(b"\xff" * 276)
        self.assertEqual(body.read_lane(0), 3)
        self.assertEqual(body.read_bits(160, 16, True), -1)
        self.assertEqual(body.read_bits(1928, 5), 31)
        self.assertEqual(body.read_bits(1774, 2), 3)
        for offset, width in ((0, 2), (160, 16), (1696, 8), (1736, 8), (1768, 32), (1848, 4), (1928, 16)):
            before = body.snapshot()
            body.write_bits(offset, width, 0)
            self.assertEqual(body.snapshot(), reference_write(before, offset, width, 0))
        body.energy = 7
        body.P0 = 6
        body.P1 = 5
        body.P2 = 4
        body.P3 = 3
        self.assertEqual(body.snapshot()[243:], b"\xff" * 33)
        self.assertEqual(State(body.snapshot()).snapshot(), body.snapshot())

    def test_18_all_resource_bits_never_become_ram_fault_targets(self) -> None:
        for bit in range(1800, 1848):
            raw = bytearray(276)
            raw[bit // 8] = 1 << (bit % 8)
            body = State(raw)
            before = body.snapshot()
            with self.assertRaises(PermissionError):
                body._physics_read_lane(bit // 2)
            with self.assertRaises(PermissionError):
                body._physics_write_lane(bit // 2, 0)
            with self.assertRaises(PermissionError):
                body.write_bits(bit, 1, 0)
            self.assertEqual(body.snapshot(), before)
            # Typed getters interpret high bits as unsigned stock, not a sign.
            self.assertEqual(body.energy, int.from_bytes(raw[225:227], "little"))
            self.assertEqual([body.read_material(i) for i in range(4)], list(raw[227:231]))

    def test_19_trusted_physics_lane_access_preserves_stocks(self) -> None:
        body = State(b"\xa5" * 276)
        before_stocks = body.snapshot()[225:231]
        count = 0
        for lane in range(1104):
            if 900 <= lane < 924:
                continue
            count += 1
            for symbol in range(4):
                before = body.snapshot()
                body._physics_write_lane(lane, symbol)
                self.assertEqual(body._physics_read_lane(lane), symbol)
                self.assertEqual(body.snapshot(), reference_write(before, lane * 2, 2, symbol))
                self.assertEqual(body.snapshot()[225:231], before_stocks)
        self.assertEqual(count, 1080)
        self.assertEqual(State(body.snapshot()).snapshot(), body.snapshot())
        self.assert_shape(body, 276)

    def test_20_invalid_bit_arguments_and_values_are_atomic(self) -> None:
        for body, bits in ((State(), 2208), (Scratch(), 256)):
            before = body.snapshot()
            for bad in BAD_INTS:
                with self.assertRaises(TypeError):
                    body.read_bits(cast(int, bad), 1)
                with self.assertRaises(TypeError):
                    body.write_bits(cast(int, bad), 1, 0)
                with self.assertRaises(TypeError):
                    body.read_bits(0, cast(int, bad))
                with self.assertRaises(TypeError):
                    body.write_bits(0, cast(int, bad), 0)
                with self.assertRaises(TypeError):
                    body.write_bits(0, 1, cast(int, bad))
            for signed in (0, 1, None, "False"):
                with self.assertRaises(TypeError):
                    body.read_bits(0, 1, cast(bool, signed))
                with self.assertRaises(TypeError):
                    body.write_bits(0, 1, 0, cast(bool, signed))
            for offset, width in ((-1, 1), (bits, 1), (bits - 1, 2), (1 << 4096, 1), (0, 0), (0, -1), (0, 33), (0, 1 << 4096)):
                with self.assertRaises(ValueError):
                    body.read_bits(offset, width)
                with self.assertRaises(ValueError):
                    body.write_bits(offset, width, 0)
            for value in (-1, 4, 1 << 4096, -(1 << 4096)):
                with self.assertRaises(ValueError):
                    body.write_bits(0, 2, value)
            self.assertEqual(body.snapshot(), before)
        body = State()
        before = body.snapshot()
        for index in (*BAD_INTS, -1, 1104, 1 << 4096):
            for reader in (body.read_lane, body._physics_read_lane):
                with self.assertRaises((TypeError, ValueError)):
                    reader(cast(int, index))
            for writer in (body.write_lane, body._physics_write_lane):
                with self.assertRaises((TypeError, ValueError)):
                    writer(cast(int, index), 0)
        for invalid_symbol in (*BAD_INTS, -1, 4, 1 << 4096):
            for writer in (body.write_lane, body._physics_write_lane):
                with self.assertRaises((TypeError, ValueError)):
                    writer(0, cast(int, invalid_symbol))
        self.assertEqual(body.snapshot(), before)

    def test_21_constructor_payload_types_and_exact_lengths(self) -> None:
        for cls, size in ((State, 276), (Scratch, 32)):
            for length in (0, 1, size - 1, size + 1, size * 2):
                for raw in (bytes(length), bytearray(length)):
                    with self.assertRaises(ValueError):
                        cls(raw)
            for value in (True, 276, "x" * size, [0] * size, memoryview(bytes(size))):
                with self.assertRaises(TypeError):
                    cls(cast(bytes, value))
            self.assert_shape(cls(), size)

    def test_22_every_scratch_bit_and_boundary_zeroing(self) -> None:
        for bit in range(256):
            scratch = Scratch()
            scratch.write_bits(bit, 1, 1)
            self.assertEqual(scratch.read_bits(bit, 1), 1)
            self.assertEqual(scratch.snapshot(), reference_write(bytes(32), bit, 1, 1))
            self.assertFalse(scratch.is_zero())
            scratch.boundary()
            self.assertTrue(scratch.is_zero())
            self.assertEqual(scratch.snapshot(), bytes(32))
            self.assert_shape(scratch, 32)
        for name in ("operation", "checkpoint", "isolation", "erasure"):
            with self.subTest(boundary=name):
                scratch = Scratch(b"\xff" * 32)
                scratch.boundary()
                self.assertEqual(scratch.snapshot(), bytes(32))
                scratch.boundary()
                self.assertEqual(scratch.snapshot(), bytes(32))

    def test_23_scratch_codec_partitions_and_no_alias(self) -> None:
        source = bytearray(b"\x55" * 32)
        scratch = Scratch(source)
        source[:] = bytes(32)
        before = scratch.snapshot()
        self.assertEqual(before, b"\x55" * 32)
        for offset in (0, 32, 64, 96, 128, 160, 192):
            scratch.set_field(offset, 32, -(1 << 31), signed=True)
            self.assertEqual(scratch.get_field(offset, 32, signed=True), -(1 << 31))
        scratch.write_bits(224, 16, 65535)
        scratch.write_bits(240, 11, 2047)
        scratch.write_bits(251, 5, 31)
        self.assertEqual(scratch.snapshot()[28:], b"\xff" * 4)
        dirty = scratch.snapshot()
        clone = Scratch(dirty)
        scratch.clear()
        self.assertEqual(clone.snapshot(), dirty)
        self.assertEqual(before, b"\x55" * 32)
        self.assertEqual(scratch.snapshot(), bytes(32))
        # Unaligned maximum-width writes, including scratch's final bit.
        for offset in (1, 95, 97, 191, 223, 224):
            previous = clone.snapshot()
            clone.write_bits(offset, 32, (1 << 32) - 1)
            self.assertEqual(clone.snapshot(), reference_write(previous, offset, 32, (1 << 32) - 1))
            self.assert_shape(clone, 32)

    def test_24_component_has_no_implicit_meter_or_full_boundary_claim(self) -> None:
        body = State()
        scratch = Scratch(b"\xff" * 32)
        body.energy = 1000
        body.P0 = 200
        stocks = body.snapshot()[225:231]
        body.write_lane(0, 1)
        body.write_bits(160, 1, 1)
        body.read_lane(0)
        self.assertEqual(body.snapshot()[225:231], stocks)  # Codec, not paid VM.
        self.assertEqual(scratch.snapshot(), b"\xff" * 32)
        raw = body.snapshot()  # Raw codec does not certify scratch-zero.
        child = body.reset()
        self.assertEqual(child.snapshot(), CANONICAL)
        self.assertEqual(body.snapshot(), raw)
        self.assertEqual(scratch.snapshot(), b"\xff" * 32)
        scratch.boundary()  # Future supervisor must explicitly perform this.
        self.assertEqual(scratch.snapshot(), bytes(32))
        self.assertEqual(body.snapshot(), raw)
        self.assert_shape(body, 276)
        self.assert_shape(scratch, 32)


if __name__ == "__main__":
    unittest.main()