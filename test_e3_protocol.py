"""ABI-9 codec component fixtures, not production isolation or METER proofs.

Only synthetic raw bytes and public constants are used. No targets, generators,
state/runtime components, simulator, learned history, or files are consulted.
"""

from dataclasses import FrozenInstanceError, fields, replace
import struct
import unittest

from e3.protocol import (
    ABI, GENERIC_FORMAT, STATE_BYTES, BeginFrame, BindFrame, Capability, Code,
    ExitFrame, Family, FrameCodec, Kind, Permission, Phase, Policy,
    ProtocolError, PublicConfiguration, ScalarFrame, ScalarTag, ShutdownFrame,
    Service, encode_frame, parse_frame, scalar_from_value, sign_extend,
)


ZERO_STATE = b"\x00" * 276
RAW_STATE = bytes(range(256)) + bytes(range(20))
SHUTDOWN_STATE = RAW_STATE[:225] + b"\x00\x00" + RAW_STATE[227:]

# Literal header/payload bytes are independent of the production encoder and
# its struct formats. Multiplication below constructs only the opaque state.
GOLDEN_FRAMES = (
    (BindFrame(403, Capability.TEMPLATE), b"\x00\x08\x00\x09\x00\x01\x00\x93\x01\x01\x00"),
    (BeginFrame(Phase.DEVELOPMENT, 258, Service.RESPONSE, 2, 7, RAW_STATE),
     b"\x01\x1c\x01\x09\x00\x01\x02\x01\x02\x02\x07" + RAW_STATE),
    (ScalarFrame(ScalarTag.LEARNER_RETURN, 16, 65472),
     b"\x02\x06\x00\x11\x10\xc0\xff\x00\x00"),
    (ExitFrame(RAW_STATE), b"\x03\x14\x01" + RAW_STATE),
    (ShutdownFrame(SHUTDOWN_STATE), b"\x04\x14\x01" + SHUTDOWN_STATE),
)

# tag, width, logical value, six literal payload bytes
SCALAR_GOLDENS = (
    (0, 16, 0x1234, b"\x00\x10\x34\x12\x00\x00"),
    (1, 8, 255, b"\x01\x08\xff\x00\x00\x00"),
    (2, 8, 128, b"\x02\x08\x80\x00\x00\x00"),
    (3, 8, 64, b"\x03\x08\x40\x00\x00\x00"),
    (4, 8, 0, b"\x04\x08\x00\x00\x00\x00"),
    (5, 5, 31, b"\x05\x05\x1f\x00\x00\x00"),
    (6, 16, 65535, b"\x06\x10\xff\xff\x00\x00"),
    (7, 8, 255, b"\x07\x08\xff\x00\x00\x00"),
    (8, 1, 1, b"\x08\x01\x01\x00\x00\x00"),
    (9, 2, 2, b"\x09\x02\x02\x00\x00\x00"),
    (10, 4, 15, b"\x0a\x04\x0f\x00\x00\x00"),
    (11, 6, 31, b"\x0b\x06\x1f\x00\x00\x00"),
    (12, 16, 64, b"\x0c\x10\x40\x00\x00\x00"),
    (13, 8, 8, b"\x0d\x08\x08\x00\x00\x00"),
    (14, 1, 1, b"\x0e\x01\x01\x00\x00\x00"),
    (15, 1, 0, b"\x0f\x01\x00\x00\x00\x00"),
    (16, 16, 64, b"\x10\x10\x40\x00\x00\x00"),
    (17, 16, -64, b"\x11\x10\xc0\xff\x00\x00"),
    (18, 4, 15, b"\x12\x04\x0f\x00\x00\x00"),
    (19, 4, 15, b"\x13\x04\x0f\x00\x00\x00"),
    (20, 1, 1, b"\x14\x01\x01\x00\x00\x00"),
    (21, 4, 12, b"\x15\x04\x0c\x00\x00\x00"),
    (22, 4, 15, b"\x16\x04\x0f\x00\x00\x00"),
)


def begin_frame(phase=Phase.DEVELOPMENT, tick=6, service=Service.CONTROLLER,
                argument=0, mask=None):
    if mask is None:
        mask = 4 if phase in (Phase.DEVELOPMENT, Phase.ASSAY, Phase.ECOLOGY) and tick >= 6 else 0
    return BeginFrame(phase, tick, service, argument, mask, ZERO_STATE)


class WireTests(unittest.TestCase):
    def test_frozen_constants_and_enum_values(self):
        self.assertEqual((ABI, GENERIC_FORMAT, STATE_BYTES), (9, 1, 276))
        for enum, size in ((Kind, 5), (Phase, 6), (Service, 13), (ScalarTag, 23),
                           (Capability, 2), (Code, 2), (Family, 2), (Policy, 7)):
            self.assertEqual([int(value) for value in enum], list(range(size)))
        self.assertEqual([int(value) for value in Permission], [1, 2, 4])

    def test_independent_golden_bytes_every_kind(self):
        for frame, raw in GOLDEN_FRAMES:
            with self.subTest(kind=frame.kind):
                self.assertEqual(encode_frame(frame), raw)
                self.assertEqual(parse_frame(raw), frame)
                self.assertIs(type(parse_frame(raw)), type(frame))

    def test_every_wrong_u16_declared_length_for_every_kind(self):
        for kind, expected in enumerate((8, 284, 6, 276, 276)):
            for length in range(65536):
                if length != expected:
                    with self.assertRaises(ProtocolError):
                        parse_frame(struct.pack("<BH", kind, length))

    def test_unknown_kinds(self):
        for kind in range(5, 256):
            with self.assertRaises(ProtocolError):
                parse_frame(bytes((kind, 0, 0)))

    def test_all_truncations_and_trailing_or_concatenated_frames(self):
        for _, raw in GOLDEN_FRAMES:
            for length in range(len(raw)):
                with self.assertRaises(ProtocolError):
                    parse_frame(raw[:length])
            for tail in (b"\x00", b"private_key=not-a-secret", raw):
                with self.assertRaises(ProtocolError):
                    parse_frame(raw + tail)

    def test_wrong_actual_state_lengths_even_with_adjusted_header(self):
        for kind, prefix in ((1, b"\x09\x00\x01\x01\x00\x00\x00\x00"),
                             (3, b""), (4, b"")):
            for size in (0, 275, 277, 512):
                payload = prefix + b"\x00" * size
                with self.assertRaises(ProtocolError):
                    parse_frame(struct.pack("<BH", kind, len(payload)) + payload)
        for factory in (ExitFrame, ShutdownFrame):
            for size in (0, 275, 277):
                with self.assertRaises(ProtocolError):
                    factory(b"\x00" * size)

    def test_little_endian_not_native_or_network_order(self):
        for _, raw in GOLDEN_FRAMES:
            with self.assertRaises(ProtocolError):
                parse_frame(raw[:1] + raw[1:3][::-1] + raw[3:])
        with self.assertRaises(ProtocolError):
            parse_frame(b"\x00\x08\x00" + struct.pack(">HHHH", 9, 1, 4, 0))
        raw = b"\x01\x1c\x01\x09\x00\x01\x02\x01\x00\x00\x04" + ZERO_STATE
        self.assertEqual(parse_frame(raw).planned_tick, 258)
        swapped = raw[:6] + raw[6:8][::-1] + raw[8:]
        self.assertEqual(parse_frame(swapped).planned_tick, 513)
        self.assertNotEqual(parse_frame(raw), parse_frame(swapped))

    def test_raw_state_preserves_corruption_and_reserved_storage(self):
        raw = b"\xff" * 276
        frame = begin_frame()
        frame = replace(frame, state=raw)
        self.assertEqual(parse_frame(encode_frame(frame)).state, raw)
        self.assertEqual(parse_frame(encode_frame(ExitFrame(raw))).state, raw)
        self.assertEqual(parse_frame(encode_frame(ShutdownFrame(SHUTDOWN_STATE))).state,
                         SHUTDOWN_STATE)

    def test_shutdown_requires_both_energy_bytes_zero_only(self):
        for energy in (1, 256, 65535):
            state = ZERO_STATE[:225] + struct.pack("<H", energy) + ZERO_STATE[227:]
            with self.assertRaises(ProtocolError):
                parse_frame(b"\x04\x14\x01" + state)
        self.assertEqual(ExitFrame(ZERO_STATE).state, ZERO_STATE)

    def test_no_mutable_buffers_dicts_callbacks_or_private_metadata(self):
        for bad in (bytearray(276), memoryview(ZERO_STATE), "x" * 276, [], None):
            with self.assertRaises(ProtocolError):
                ExitFrame(bad)
        for bad in ({"kind": 0, "private_key": "fixture"}, [], None,
                    bytearray(GOLDEN_FRAMES[0][1]), lambda: None):
            with self.assertRaises(ProtocolError):
                parse_frame(bad)
            with self.assertRaises(ProtocolError):
                encode_frame(bad)
        with self.assertRaises(TypeError):
            BindFrame(4, private_key="fixture")
        with self.assertRaises(TypeError):
            BeginFrame(1, 1, 0, 0, 0, ZERO_STATE, runner="fixture")

    def test_closed_frozen_slotted_records(self):
        for frame, _ in GOLDEN_FRAMES:
            self.assertFalse(hasattr(frame, "__dict__"))
            field = fields(frame)[0].name
            with self.assertRaises(FrozenInstanceError):
                setattr(frame, field, getattr(frame, field))
        class ExtraFrame(ExitFrame):
            pass
        with self.assertRaises(ProtocolError):
            encode_frame(ExtraFrame(ZERO_STATE))


class ConfigurationTests(unittest.TestCase):
    def test_all_400_grid_ids_against_independent_forward_formula(self):
        for code in (0, 1):
            for family in (0, 1):
                base = 200 * code + 100 * family
                for e, energy in enumerate((24576, 32768, 40960)):
                    for p, material in enumerate((32, 64, 96)):
                        rows = [(3 * e + p, Policy.RL, 0),
                                (90 + 3 * e + p, Policy.THRESHOLD, 0)]
                        rows += [(9 + 9 * (3 * e + p) + i, Policy.PERIODIC, interval)
                                 for i, interval in enumerate((1, 2, 4, 8, 16, 32, 64, 128, 256))]
                        for k, policy, interval in rows:
                            config = BindFrame(base + k).configuration
                            self.assertEqual((config.code, config.family, config.policy,
                                              config.energy_cut, config.material_cut,
                                              config.interval, config.objective, config.variant),
                                             (code, family, policy, energy, material, interval, 0, code))
                config = BindFrame(base + 99).configuration
                self.assertEqual((config.policy, config.energy_cut, config.material_cut,
                                  config.interval, config.objective), (Policy.DRIVE, 32768, 64, 0, 1))

    def test_script_ids_no_new_worker_family_and_no_frozen_selector(self):
        for code in (0, 1):
            for script in (0, 1):
                config = PublicConfiguration(400 + 2 * code + script)
                self.assertEqual((config.code, config.policy, config.energy_cut,
                                  config.material_cut, config.health_threshold, config.objective),
                                 (code, 5 + script, 32768, 64, 3, 0))
                self.assertIsNone(config.family)
                self.assertTrue(config.is_script)
        self.assertFalse(any(PublicConfiguration(i).policy == Policy.FROZEN for i in range(404)))

    def test_reserved_catalog_slots_and_out_of_range_ids(self):
        for index in (-1, *range(404, 512), 512, 65535, True, 4.0, "4"):
            with self.assertRaises(ProtocolError):
                BindFrame(index)

    def test_bind_abi_format_capability_validation(self):
        for abi, fmt, cap in ((8, 1, 0), (10, 1, 0), (9, 0, 0),
                              (9, 2, 0), (9, 1, 2), (9, 1, 65535)):
            with self.assertRaises(ProtocolError):
                parse_frame(b"\x00\x08\x00" + struct.pack("<HHHH", abi, fmt, 4, cap))
        for kwargs in ({"abi": True}, {"generic_format": True},
                       {"capability": True}, {"capability": Phase.DEVELOPMENT}):
            with self.assertRaises(ProtocolError):
                BindFrame(4, **kwargs)


class HeaderTests(unittest.TestCase):
    def test_explicit_legal_service_phase_matrix(self):
        # Matrix is stated independently, not imported from the implementation.
        allowed = (
            {0, 4, 5, 6, 9, 10, 11},
            {0, 1, 2, 3, 7, 8, 9, 10, 11},
            {0, 1, 2, 8, 9, 10, 11},
            {0, 2, 3, 8, 9, 10, 11},
            {0, 1, 2, 3, 7, 8, 9, 10, 11},
            {8, 12},
        )
        for phase in Phase:
            for service in Service:
                tick = 0 if service == Service.ISOLATE or phase == Phase.ORACLE else 4
                if service == Service.TERMINAL:
                    tick = (256, 2048, 128, 261, 512, 0)[phase]
                arg = (tick - 1) % 5 if service in (Service.RESPONSE, Service.ADMIT) else 0
                mask = 5 if service == Service.TERMINAL else 0
                with self.subTest(phase=phase, service=service):
                    if service in allowed[phase]:
                        self.assertIsInstance(begin_frame(phase, tick, service, arg, mask), BeginFrame)
                    else:
                        with self.assertRaises(ProtocolError):
                            begin_frame(phase, tick, service, arg, mask)

    def test_tick_limits_entry_and_oracle(self):
        for phase, limit in zip(tuple(Phase)[:5], (256, 2048, 128, 261, 512)):
            for tick in (1, limit):
                self.assertEqual(begin_frame(phase, tick, Service.TICK).planned_tick, tick)
            for tick in (-1, 0, limit + 1, 65536, True, 1.0):
                with self.assertRaises(ProtocolError):
                    begin_frame(phase, tick, Service.TICK)
        begin_frame(Phase.ORACLE, 0, Service.TEMPLATE)
        for tick in (1, 65535):
            with self.assertRaises(ProtocolError):
                begin_frame(Phase.ORACLE, tick, Service.TEMPLATE)

    def test_unknown_enums_abi_and_all_reserved_mask_encodings(self):
        base = b"\x01\x1c\x01\x09\x00\x01\x01\x00\x00\x00\x00" + ZERO_STATE
        for offset, values in ((5, range(6, 256)), (8, range(13, 256)), (10, range(8, 256))):
            for value in values:
                raw = base[:offset] + bytes((value,)) + base[offset + 1:]
                with self.assertRaises(ProtocolError):
                    parse_frame(raw)
        with self.assertRaises(ProtocolError):
            replace(begin_frame(), abi=10)
        for name in ("phase", "service", "mask", "argument", "planned_tick"):
            with self.assertRaises(ProtocolError):
                replace(begin_frame(), **{name: True})

    def test_permissions_and_due_calendar(self):
        for phase in (Phase.ACQUISITION, Phase.RECOVERY, Phase.ASSAY, Phase.ORACLE):
            service = Service.TEMPLATE if phase == Phase.ORACLE else Service.TICK
            tick = 0 if phase == Phase.ORACLE else 1
            with self.assertRaises(ProtocolError):
                begin_frame(phase, tick, service, mask=1)
        with self.assertRaises(ProtocolError):
            begin_frame(Phase.ASSAY, 1, Service.TICK, mask=2)
        for phase in (Phase.DEVELOPMENT, Phase.ASSAY, Phase.ECOLOGY):
            for tick, bad in ((5, 4), (6, 0)):
                with self.assertRaises(ProtocolError):
                    begin_frame(phase, tick, Service.TICK, mask=bad)
        for mask in (1, 3, 4, 5, 6, 7):
            with self.assertRaises(ProtocolError):
                begin_frame(Phase.DEVELOPMENT, 0, Service.ISOLATE, mask=mask)
        begin_frame(Phase.DEVELOPMENT, 0, Service.ISOLATE, mask=2)
        for mask in range(1, 8):
            with self.assertRaises(ProtocolError):
                begin_frame(Phase.ORACLE, 0, Service.ISOLATE, mask=mask)

    def test_slots_drains_and_unused_arguments(self):
        for tick in range(1, 11):
            for service in (Service.RESPONSE, Service.ADMIT):
                slot = (tick - 1) % 5
                begin_frame(tick=tick, service=service, argument=slot)
                for bad in set(range(6)) - {slot}:
                    with self.assertRaises(ProtocolError):
                        begin_frame(tick=tick, service=service, argument=bad)
        for phase, last in ((Phase.DEVELOPMENT, 2043), (Phase.ASSAY, 256), (Phase.ECOLOGY, 507)):
            begin_frame(phase, last, Service.ADMIT, (last - 1) % 5)
            with self.assertRaises(ProtocolError):
                begin_frame(phase, last + 1, Service.ADMIT, last % 5)
        for service in (Service.TICK, Service.CONTROLLER, Service.AGE_LOW, Service.AGE_HIGH):
            with self.assertRaises(ProtocolError):
                begin_frame(service=service, argument=1)
        begin_frame(service=Service.CONDITION, argument=19)
        for bad in (-1, 20, 255):
            with self.assertRaises(ProtocolError):
                begin_frame(service=Service.CONDITION, argument=bad)

    def test_commit_group_boundary_not_invented_private_block_order(self):
        for tick in (4, 8, 256):
            for block in range(4):
                begin_frame(Phase.ACQUISITION, tick, Service.COMMIT, block)
        for tick, block in ((3, 0), (5, 0), (4, 4)):
            with self.assertRaises(ProtocolError):
                begin_frame(Phase.ACQUISITION, tick, Service.COMMIT, block)

    def test_terminal_only_at_last_learning_tick(self):
        for phase, tick in ((Phase.DEVELOPMENT, 2048), (Phase.ECOLOGY, 512)):
            begin_frame(phase, tick, Service.TERMINAL, mask=5)
            for bad_tick, mask in ((tick - 1, 5), (tick, 4)):
                with self.assertRaises(ProtocolError):
                    begin_frame(phase, bad_tick, Service.TERMINAL, mask=mask)


class ScalarTests(unittest.TestCase):
    def test_every_tag_independent_golden_and_zero(self):
        for tag, width, value, payload in SCALAR_GOLDENS:
            raw = b"\x02\x06\x00" + payload
            frame = scalar_from_value(ScalarTag(tag), value)
            self.assertEqual((frame.tag, frame.width, frame.value), (tag, width, value))
            self.assertEqual(encode_frame(frame), raw)
            self.assertEqual(parse_frame(raw), frame)
            self.assertEqual(scalar_from_value(ScalarTag(tag), 0).low_bits, 0)

    def test_unknown_tags_and_every_wrong_width(self):
        for tag in range(23, 256):
            with self.assertRaises(ProtocolError):
                parse_frame(b"\x02\x06\x00" + bytes((tag, 1, 0, 0, 0, 0)))
        for tag, width, _, payload in SCALAR_GOLDENS:
            for wrong in range(256):
                if wrong != width:
                    with self.assertRaises(ProtocolError):
                        parse_frame(b"\x02\x06\x00" + bytes((tag, wrong)) + payload[2:])

    def test_every_unused_high_bit_is_rejected_for_every_tag(self):
        for tag, width, _, _ in SCALAR_GOLDENS:
            for bit in range(width, 32):
                with self.assertRaises(ProtocolError):
                    parse_frame(b"\x02\x06\x00" + struct.pack("<BBI", tag, width, 1 << bit))

    def test_width_valid_semantic_ranges(self):
        for tag, bad_values in ((9, (3,)), (11, range(32, 64)),
                                (12, (65, 255, 65535)), (13, (9, 255)),
                                (16, (1, 63, 65)), (17, (1, 63, 65, 32768, 65535))):
            for value in bad_values:
                with self.assertRaises(ProtocolError):
                    ScalarFrame(tag, SCALAR_GOLDENS[tag][1], value)
        for tag in ScalarTag:
            for bad in (-1, 1 << 32, True, False, 0.0, "0"):
                with self.assertRaises(ProtocolError):
                    ScalarFrame(tag, SCALAR_GOLDENS[tag][1], bad)
            with self.assertRaises(ProtocolError):
                ScalarFrame(tag, True, 0)
        with self.assertRaises(ProtocolError):
            ScalarFrame(True, 8, 0)

    def test_signed_low_bits_not_32_bit_sign_extension(self):
        for value, low, literal in ((-64, 65472, b"\xc0\xff\x00\x00"),
                                    (0, 0, b"\x00\x00\x00\x00"),
                                    (64, 64, b"\x40\x00\x00\x00")):
            frame = scalar_from_value(ScalarTag.LEARNER_RETURN, value)
            self.assertEqual((frame.low_bits, frame.value), (low, value))
            self.assertEqual(encode_frame(frame), b"\x02\x06\x00\x11\x10" + literal)
        with self.assertRaises(ProtocolError):
            parse_frame(b"\x02\x06\x00\x11\x10\xc0\xff\xff\xff")
        for bad in (-65, -1, 1, 65, True):
            with self.assertRaises(ProtocolError):
                scalar_from_value(ScalarTag.LEARNER_RETURN, bad)
        for low in range(65536):
            expected = low if low < 32768 else low - 65536
            self.assertEqual(sign_extend(low, 16), expected)
        for low, width in ((65536, 16), (-1, 16), (0, 0), (0, 33), (True, 1)):
            with self.assertRaises(ProtocolError):
                sign_extend(low, width)


class ContextTests(unittest.TestCase):
    def test_rep_block_and_fixed_policy_restrictions(self):
        rep, block = FrameCodec(BindFrame(4)), FrameCodec(BindFrame(204))
        for codec, service in ((rep, Service.REP_LESSON), (block, Service.BLOCK_LESSON),
                                (block, Service.COMMIT)):
            frame = begin_frame(Phase.ACQUISITION, 4, service)
            codec.validate(frame)
            other = block if codec is rep else rep
            with self.assertRaises(ProtocolError):
                other.validate(frame)
        for index in (9, 90):
            codec = FrameCodec(BindFrame(index))
            with self.assertRaises(ProtocolError):
                codec.validate(begin_frame(mask=5))

    def test_script_ecology_and_reset_future_headers(self):
        for index in range(400, 404):
            codec = FrameCodec(BindFrame(index))
            for phase, service, tick, mask in (
                    (Phase.ECOLOGY, Service.CONTROLLER, 6, 5),
                    (Phase.ECOLOGY, Service.ISOLATE, 0, 2),
                    (Phase.RECOVERY, Service.CONTROLLER, 6, 2),
                    (Phase.ASSAY, Service.RESPONSE, 6, 4)):
                codec.validate(begin_frame(phase, tick, service, mask=mask))
            for phase in (Phase.ACQUISITION, Phase.DEVELOPMENT):
                with self.assertRaises(ProtocolError):
                    codec.validate(begin_frame(phase, 1, Service.TICK))

    def test_every_scalar_tag_has_explicit_valid_context(self):
        for tag, _, value, _ in SCALAR_GOLDENS:
            codec = FrameCodec(BindFrame(204, Capability.TEMPLATE))
            if tag <= 4:
                begin = begin_frame(service=Service.TICK)
            elif tag <= 13:
                begin = begin_frame()
            elif tag <= 17:
                begin = begin_frame(Phase.ECOLOGY, 6, Service.RESPONSE, mask=5)
            elif tag == 18:
                begin = begin_frame(service=Service.ADMIT)
            elif tag <= 20:
                begin = begin_frame(Phase.ACQUISITION, 4, Service.BLOCK_LESSON)
            else:
                begin = begin_frame(Phase.ORACLE, 0, Service.TEMPLATE)
            scalar = scalar_from_value(ScalarTag(tag), value)
            raw = codec.encode_frame(scalar, begin=begin)
            self.assertEqual(codec.parse_frame(raw, begin=begin), scalar)
            with self.assertRaises(ProtocolError):
                codec.validate(scalar, begin=begin_frame(service=Service.AGE_LOW))

    def test_scripts_cannot_disable_ecological_learning(self):
        for index in range(400, 404):
            codec = FrameCodec(BindFrame(index))
            for tick, disabled, enabled in ((1, 2, 3), (6, 6, 7)):
                for service in (Service.CONTROLLER, Service.RESPONSE, Service.TICK):
                    with self.subTest(index=index, tick=tick, service=service):
                        bad = begin_frame(Phase.ECOLOGY, tick, service, mask=disabled)
                        with self.assertRaises(ProtocolError):
                            codec.validate(bad)
                        with self.assertRaises(ProtocolError):
                            codec.encode_frame(bad)
                        with self.assertRaises(ProtocolError):
                            codec.parse_frame(encode_frame(bad))
                        good = begin_frame(Phase.ECOLOGY, tick, service, mask=enabled)
                        self.assertEqual(codec.parse_frame(codec.encode_frame(good)), good)
            codec.validate(begin_frame(Phase.ECOLOGY, 0, Service.ISOLATE, mask=2))
            codec.validate(begin_frame(Phase.RECOVERY, 6, Service.CONTROLLER, mask=2))
            codec.validate(begin_frame(Phase.ASSAY, 6, Service.RESPONSE, mask=4))
        FrameCodec(BindFrame(104)).validate(
            begin_frame(Phase.ECOLOGY, 6, Service.CONTROLLER, mask=6))

    def test_rank_inputs_absent_for_fixed_and_script_but_present_frozen_rl(self):
        begin = begin_frame(mask=4)  # Learning disabled, RL inference retained.
        for tag in (ScalarTag.B, ScalarTag.T, ScalarTag.X):
            scalar = scalar_from_value(tag, 0)
            rl = FrameCodec(BindFrame(4))
            for phase in (Phase.DEVELOPMENT, Phase.ECOLOGY):
                with self.subTest(rl_phase=phase, tag=tag):
                    frozen = begin_frame(phase, 6, Service.CONTROLLER, mask=4)
                    rl.validate(frozen)
                    rl.validate(scalar, begin=frozen)
                    raw = rl.encode_frame(scalar, begin=frozen)
                    self.assertEqual(rl.parse_frame(raw, begin=frozen), scalar)
            for index in (9, 90, *range(400, 404)):
                with self.subTest(index=index, tag=tag):
                    codec = FrameCodec(BindFrame(index))
                    current = (begin_frame(Phase.ECOLOGY, 6, Service.CONTROLLER, mask=7)
                               if index >= 400 else begin)
                    # Prove BEGIN is valid before testing rank-specific rejection.
                    codec.validate(current)
                    self.assertEqual(codec.parse_frame(codec.encode_frame(current)), current)
                    with self.assertRaisesRegex(ProtocolError, "rank scalars require RL selection"):
                        codec.validate(scalar, begin=current)
                    with self.assertRaisesRegex(ProtocolError, "rank scalars require RL selection"):
                        codec.encode_frame(scalar, begin=current)
                    with self.assertRaisesRegex(ProtocolError, "rank scalars require RL selection"):
                        codec.parse_frame(encode_frame(scalar), begin=current)

    def test_feedback_phase_due_and_learning_restrictions(self):
        codec = FrameCodec(BindFrame(104))
        for tag in (ScalarTag.ECOLOGY_YIELD, ScalarTag.LEARNER_RETURN):
            scalar = scalar_from_value(tag, 0)
            for phase in (Phase.RECOVERY, Phase.ASSAY):
                with self.assertRaises(ProtocolError):
                    codec.validate(scalar, begin=begin_frame(phase, 6, Service.RESPONSE))
            for phase in (Phase.DEVELOPMENT, Phase.ECOLOGY):
                with self.assertRaises(ProtocolError):
                    codec.validate(scalar, begin=begin_frame(phase, 1, Service.RESPONSE, mask=1))
                codec.validate(scalar, begin=begin_frame(phase, 6, Service.RESPONSE, mask=5))
        with self.assertRaises(ProtocolError):
            codec.validate(scalar_from_value(ScalarTag.LEARNER_RETURN, 0),
                           begin=begin_frame(Phase.ECOLOGY, 6, Service.RESPONSE))

    def test_template_capability_and_code_specific_semantic_bad_packets(self):
        begin = begin_frame(Phase.ORACLE, 0, Service.TEMPLATE)
        for index in (4, 204):
            with self.assertRaises(ProtocolError):
                FrameCodec(BindFrame(index)).validate(begin)
            codec = FrameCodec(BindFrame(index, Capability.TEMPLATE))
            codec.validate(begin)
            for cue in range(16):
                scalar = scalar_from_value(ScalarTag.TEMPLATE_CUE, cue)
                if index == 204 and cue % 4:
                    with self.assertRaises(ProtocolError):
                        codec.validate(scalar, begin=begin)
                else:
                    codec.validate(scalar, begin=begin)
            for payload in range(16):
                scalar = scalar_from_value(ScalarTag.TEMPLATE_PAYLOAD, payload)
                # Width-valid packet parses structurally even when paid BAD is needed.
                self.assertEqual(parse_frame(encode_frame(scalar)), scalar)
                if index == 4 and payload > 1:
                    with self.assertRaises(ProtocolError):
                        codec.validate(scalar, begin=begin)
                else:
                    codec.validate(scalar, begin=begin)
        for arg, mask in ((1, 0), (0, 1), (0, 2), (0, 4)):
            with self.assertRaises(ProtocolError):
                begin_frame(Phase.ORACLE, 0, Service.TEMPLATE, arg, mask)

    def test_context_is_immutable_not_a_session_or_paid_gate_proof(self):
        codec = FrameCodec(BindFrame(4))
        self.assertEqual([field.name for field in fields(codec)], ["binding"])
        self.assertFalse(hasattr(codec, "__dict__"))
        with self.assertRaises(FrozenInstanceError):
            codec.binding = BindFrame(204)
        with self.assertRaises(ProtocolError):
            codec.validate(BindFrame(204))
        with self.assertRaises(ProtocolError):
            FrameCodec({"public_config_id": 4})
        scalar = scalar_from_value(ScalarTag.OFFER, 31)
        with self.assertRaises(ProtocolError):
            codec.validate(scalar)
        with self.assertRaises(ProtocolError):
            codec.validate(scalar, begin={"private_key": "fixture"})
        with self.assertRaises(ProtocolError):
            codec.validate(ExitFrame(ZERO_STATE), begin=begin_frame())
        before = repr(codec)
        # Deliberately no sequence/count/missing-frame enforcement or saved BEGIN.
        for _ in range(9):
            codec.validate(scalar, begin=begin_frame())
        codec.validate(BindFrame(4))
        codec.validate(BindFrame(4))
        codec.validate(ExitFrame(ZERO_STATE))
        self.assertEqual(repr(codec), before)


if __name__ == "__main__":
    unittest.main()