"""Constructed codec conformance fixtures, not target draws or experiment data.

Literal golden bytes and field-by-field independent layouts test wire order;
round trips alone cannot prove that order. No files or live worker state are
created. Hash tests cover supplied bytes, not original-run provenance/replay.
"""

from collections import defaultdict
from dataclasses import FrozenInstanceError, fields, replace
import hashlib
import json
import struct
import unittest

from e3 import archive as ar


RAW = bytes(range(256)) + bytes(range(20))
DIGEST = bytes(range(32))
ZERO5 = (0, 0, 0, 0, 0)
STOCKS = ar.Stocks(0x1234, 1, 2, 3, 4)

# Independent SCALAR_IN B event; aux occupies bytes 116..119, not padding.
SCALAR_EVENT_GOLDEN = (
    bytes.fromhex("0600 0101 0000 0402 00000000 ffff 0801 "
                  "341201020304 341201020304 00000000 01000000")
    + bytes(80) + bytes.fromhex("ff030000") + bytes(72))


def capsule():
    # Defaults are fixture-only; production API requires every field explicitly.
    values = {field.name: 0 for field in fields(ar.TickCapsule)}
    values.update(outer_ordinal=31, action=3)
    return ar.TickCapsule(**values)


def response():
    return ar.ResponseRecord(3, ar.ResponseStatus.EMITTED_0, 0x87,
                             1, 0, 1, 0, 1, 1, 1, 1, -64, 0,
                             1, 1, 1, 1, 1, 1, 1, 1, 3)


def snapshot():
    return ar.SnapshotRecord(284592, 258, ar.BoundaryKind.TICK_ANCHOR,
                             ar.Lifecycle.LIVE, 0x1234, 255, 2, None,
                             0, 7, 0x100000002, RAW)


def reset_audit():
    return ar.ResetAuditRecord(0, 1, 2, 3, 4, None, ar.Lifecycle.MINIMUM_DEATH,
                               127, 0x01020304, DIGEST)


def template():
    return ar.TemplateRecord(284592, 2, ar.LessonStatus.COMPLETE, 1,
                             12, 15, 20, 20, 20, 3, 139,
                             ar.Stocks(65535, 255, 255, 255, 255),
                             ar.Stocks(62001, 255, 255, 255, 235),
                             3, 3534, (0, 0, 0, 20), 400, 0xFFFFF, 0xFFFFF)


def event():
    return ar.PrimitiveEvent(258, 1, 1, 0, ar.EventKind.METER,
                             ar.PathStatus.REJECTED_OR_INELIGIBLE, 0, None, None, 0,
                             STOCKS, ar.Stocks(0x1200, 1, 2, 3, 4),
                             0, 0, (52, 0, 0, 0, 0), (8, 1, 2, 3, 4),
                             (4096, 4, 3, 2, 1), (0, 0, 0, 0, 0), 0,
                             bytes(range(32)), bytes(reversed(range(32))))


def scalar_event():
    return ar.PrimitiveEvent(6, 1, 1, 0, ar.EventKind.SCALAR_IN,
                             ar.PathStatus.COMPLETE, 0, None, 8, 1,
                             STOCKS, STOCKS, 0, 1, ZERO5, ZERO5, ZERO5, ZERO5,
                             1023, bytes(32), bytes(32))


def schedule():
    return ar.ScheduleRecord(34, 1, 1, 0, 34, 4, 512, 507,
                              0x00FF, 0xFF00, 255, 11, tuple(i % 16 for i in range(512)))


def phase():
    return ar.PhaseDescriptor(284592, 0, 29695, 403, 34, None,
                              1, 1, 0, 1, 1, ar.Policy.SCRIPT_ALL, ar.Product.SCRIPTED,
                              8, 8, 3, 0, 512, 36, 2,
                              3818368, 129338400, 111393280, None, None, None, 34)


def class_mapping():
    return ar.ClassMapping(29951, 285614, 285615, 403, 28, 29,
                            1, 1, 1, 1, 1, 29695)


def directory():
    return ar.DirectoryEntry(ar.Table.TICK, ar.Codec.DENSE, 48,
                              129338400, 361728, 1 << 40, 361728 * 48, DIGEST)


def specimens():
    return (STOCKS, response(), capsule(), ar.TickRecord(DIGEST, capsule()),
            snapshot(), reset_audit(), ar.LessonRecord(12, 1, 3, 5, 4, 3, 0, 0, 51),
            ar.CommitRecord(0xAB, 4, 20, 19, 18, 1), template(),
            ar.SummaryCounters.from_values(tuple(range(62))),
            ar.SummaryRecord(STOCKS, STOCKS, 0, 15, ar.SummaryCounters.from_values(tuple(range(62)))),
            directory(), event(), ar.TraceCommitment(1 << 40, 1 << 39, DIGEST),
            schedule(), phase(), class_mapping(), ar.GRecord.from_id(403))


def field_bytes(value, width):
    return int(value).to_bytes(width, "little")


class GoldenTests(unittest.TestCase):
    def test_reset_independent_64_byte_fromhex(self):
        raw = bytes.fromhex(
            "00000000 01000000 02000000 03000000 04000000 ffffffff "
            "02 7f 0000 04030201 "
            "000102030405060708090a0b0c0d0e0f "
            "101112131415161718191a1b1c1d1e1f")
        self.assertEqual(len(raw), 64)
        self.assertEqual(ar.marshal(reset_audit()), raw)
        self.assertEqual(ar.unmarshal(ar.ResetAuditRecord, raw), reset_audit())

    def test_response_signed_flags_and_zero_not_absent(self):
        raw = bytes.fromhex("13 87 f5 c0ff 00 ff 03")
        self.assertEqual(ar.marshal(response()), raw)
        self.assertEqual(ar.unmarshal(ar.ResponseRecord, raw), response())
        received_zero = replace(response(), learner_b=0, ecological_yield=0)
        absent = replace(received_zero, b_present=0, yield_present=0)
        self.assertNotEqual(ar.marshal(received_zero), ar.marshal(absent))
        self.assertEqual(ar.marshal(received_zero)[3:6], ar.marshal(absent)[3:6])

    def test_capsule_independent_all_field_offsets(self):
        c = ar.TickCapsule(26, 2, 1, 20, 19, 18, 2, 3, 1, 1, 1, 1, 3, 1, 1, 11,
                           0xA5, 5, 2, 1, 2, 3, 1, 3, 12, 3, 1, 0, 1, 1,
                           0xABCDE, 3, 7, 13, 1, -18, 0)
        # Explicit shifts derive from the contract, not production layout lists.
        word1 = (20 | 19 << 5 | 18 << 10 | 2 << 15 | 3 << 17 | 1 << 19 |
                 1 << 20 | 1 << 21 | 1 << 22 | 3 << 23 | 1 << 25 | 1 << 26 | 11 << 27)
        word2 = (0xA5 | 5 << 8 | 2 << 11 | 1 << 13 | 2 << 14 | 3 << 16 |
                 1 << 18 | 3 << 20 | 12 << 22 | 3 << 26 | 1 << 28 | 1 << 30 | 1 << 31)
        word3 = 0xABCDE | 3 << 20 | 7 << 22 | 13 << 27 | 1 << 31
        raw = (bytes((26 | 2 << 5 | 1 << 7,)) + field_bytes(word1, 4) +
               field_bytes(word2, 4) + field_bytes(word3, 4) + b"\xee\xff\x00")
        self.assertEqual(len(raw), 16)
        self.assertEqual(ar.marshal(c), raw)
        self.assertEqual(ar.unmarshal(ar.TickCapsule, raw), c)
        self.assertEqual(ar.marshal(ar.TickRecord(DIGEST, c)), DIGEST + raw)

    def test_capsule_independent_malformed_presence_bytes_reject(self):
        # First row is the exact CCI-001 witness; none use the encoder.
        cases = (
            ("80 00800100 0000000c 00000000 0000 00", "controller observations require admitted DECIDE"),
            ("80 00800100 00000010 00000000 0000 00", "controller observations require admitted DECIDE"),
            ("80 00800100 00000020 00000000 0000 00", "controller observations require admitted DECIDE"),
            ("80 00000000 00000000 00000000 1000 40", "accepted yield requires admitted action"),
            ("80 00800000 00000000 00000000 1000 08", "accepted yield requires admitted action"),
            ("80 00800100 00000080 00000000 0000 00", "absent action cannot be admitted"),
        )
        for hex_bytes, reason in cases:
            with self.subTest(raw=hex_bytes):
                raw = bytes.fromhex(hex_bytes)
                self.assertEqual(len(raw), 16)
                with self.assertRaisesRegex(ar.ArchiveError, reason):
                    ar.unmarshal(ar.TickCapsule, raw)
                with self.assertRaisesRegex(ar.ArchiveError, reason):
                    ar.unmarshal(ar.TickRecord, DIGEST + raw)

    def test_snapshot_independent_header_order_raw_reserved_state(self):
        s = snapshot()
        raw = (field_bytes(284592, 4) + b"\x02\x01\x07\x00\x34\x12\xff\x02" +
               b"\xff" * 4 + bytes(4) + b"\x07\x00\x00\x00" +
               b"\x02\x00\x00\x00\x01\x00\x00\x00" + RAW)
        self.assertEqual(len(raw), 308)
        self.assertEqual(ar.marshal(s), raw)
        self.assertEqual(ar.unmarshal(ar.SnapshotRecord, raw).payload, RAW)

    def test_directory_independent_72_byte_layout(self):
        raw = (b"\x00\x00\x30\x00" + field_bytes(129338400, 8) + field_bytes(361728, 8)
               + field_bytes(1 << 40, 8) + field_bytes(361728 * 48, 8) + DIGEST + bytes(4))
        self.assertEqual(len(raw), 72)
        self.assertEqual(ar.marshal(directory()), raw)

    def test_summary_all_62_slots_integer_not_double(self):
        values = tuple((1 << 54) + i * 1000003 for i in range(62))
        row = ar.SummaryRecord(STOCKS, ar.Stocks(65535, 255, 254, 253, 252), 3, 15,
                               ar.SummaryCounters.from_values(values))
        expected = bytes.fromhex("3412 01020304 ffff fffefdfc 030f0000")
        expected += b"".join(v.to_bytes(8, "little") for v in values)
        self.assertEqual(len(expected), 512)
        self.assertEqual(ar.marshal(row), expected)
        for i, value in enumerate(values):
            self.assertEqual(int.from_bytes(expected[16 + 8*i:24 + 8*i], "little"), value)
        self.assertEqual(ar.unmarshal(ar.SummaryRecord, expected), row)
        self.assertEqual(len(ar.SUMMARY_COUNTER_NAMES), 62)
        self.assertEqual(ar.SUMMARY_COUNTER_NAMES[24:29],
                         ("paid_debits_e", "paid_debits_p0", "paid_debits_p1", "paid_debits_p2", "paid_debits_p3"))
        self.assertEqual(ar.SUMMARY_COUNTER_NAMES[53], "external_supplied_p3")
        self.assertEqual(ar.SUMMARY_COUNTER_NAMES[61], "paid_code_prefix_stops")

    def test_ieee_nan_bit_patterns_are_uint64_not_missing(self):
        bits = 0x7FF8000000000000
        counters = ar.SummaryCounters.from_values((bits,) * 62)
        parsed = ar.unmarshal(ar.SummaryCounters, ar.marshal(counters))
        self.assertEqual(parsed.values, (bits,) * 62)
        self.assertEqual(parsed.planned_ticks, bits)

    def test_template_independent_64_byte_layout(self):
        raw = (field_bytes(284592, 4) + bytes.fromhex("0200 0301 0c0f14141403 8b00")
               + bytes.fromhex("ffff ffffffff 31f2 ffffffeb 0300 0000")
               + field_bytes(3534, 8) + bytes.fromhex("0000 0000 0000 1400")
               + field_bytes(400, 8) + field_bytes(0xFFFFF, 4) * 2)
        self.assertEqual(len(raw), 64)
        self.assertEqual(ar.marshal(template()), raw)

    def test_lesson_commit_independent_packing(self):
        lesson = ar.LessonRecord(12, 1, 3, 5, 4, 3, 0, 0, 51)
        self.assertEqual(ar.marshal(lesson), bytes.fromhex("0c0103 850c 000033"))
        commit = ar.CommitRecord(0xAB, 4, 20, 19, 18, 1)
        self.assertEqual(ar.marshal(commit), bytes.fromhex("ab04 74ca"))

    def test_primitive_independent_192_byte_offsets(self):
        e = event()
        raw = bytes.fromhex("0201 0101 0000 0601 00000000 ffff ff00")
        raw += bytes.fromhex("341201020304 001201020304")
        raw += bytes(8)
        for vector in ((52, 0, 0, 0, 0), (8, 1, 2, 3, 4),
                       (4096, 4, 3, 2, 1), (0, 0, 0, 0, 0)):
            raw += b"".join(field_bytes(v, 4) for v in vector)
        raw += bytes(12) + bytes(range(32)) + bytes(reversed(range(32)))
        self.assertEqual(len(raw), 192)
        self.assertEqual(ar.marshal(e), raw)
        self.assertEqual(ar.unmarshal(ar.PrimitiveEvent, raw), e)

    def test_schedule_independent_nibbles(self):
        expected = bytes.fromhex("2200 0100 01002204 0002 fb01 ff00 00ff ff0b")
        expected += bytes(14) + bytes.fromhex("1032547698badcfe") * 32 + bytes(1024)
        self.assertEqual(len(expected), 1312)
        self.assertEqual(ar.marshal(schedule()), expected)

    def test_phase_independent_field_order(self):
        expected = b"".join(field_bytes(v, 4) for v in (284592, 0, 29695))
        expected += field_bytes(403, 2) + field_bytes(34, 2) + b"\xff" * 4
        expected += bytes.fromhex("0100 0100 0101060d08080300 0002 2402")
        expected += b"".join(field_bytes(v, 4) for v in (3818368, 129338400, 111393280))
        expected += b"\xff" * 12 + bytes.fromhex("2200 0000")
        self.assertEqual(len(expected), 64)
        self.assertEqual(ar.marshal(phase()), expected)

    def test_g_class_commitment_independent_layouts(self):
        g = bytes.fromhex("0900 01060140 0080 0000 03000300 0100") + bytes(112)
        self.assertEqual(len(g), 128)
        self.assertEqual(ar.marshal(ar.GRecord.from_id(403)), g)
        c = b"".join(field_bytes(v, 4) for v in (29951, 285614, 285615))
        c += b"".join(field_bytes(v, 2) for v in (403, 28, 29, 1))
        c += bytes((1, 1, 1, 1)) + field_bytes(29695, 4) + bytes(4)
        self.assertEqual(ar.marshal(class_mapping()), c)
        self.assertEqual(ar.marshal(ar.TraceCommitment(1 << 40, 1 << 39, DIGEST)),
                         field_bytes(1 << 40, 8) + field_bytes(1 << 39, 8) + DIGEST)


class CodecRejectionTests(unittest.TestCase):
    def test_sizes_roundtrip_closed_frozen_slots(self):
        sizes = (6, 8, 16, 48, 308, 64, 8, 4, 64, 496, 512, 72, 192, 48, 1312, 64, 32, 128)
        for record, size in zip(specimens(), sizes, strict=True):
            with self.subTest(record=type(record).__name__):
                raw = ar.marshal(record)
                self.assertEqual(len(raw), size)
                self.assertEqual(ar.unmarshal(type(record), raw), record)
                self.assertFalse(hasattr(record, "__dict__"))
                with self.assertRaises(FrozenInstanceError):
                    setattr(record, fields(record)[0].name, 0)

    def test_every_truncation_and_trailing_bytes(self):
        for record in specimens():
            raw = ar.marshal(record)
            for length in range(len(raw)):
                with self.assertRaises(ar.ArchiveError):
                    ar.unmarshal(type(record), raw[:length])
            for tail in (b"\x00", raw):
                with self.assertRaises(ar.ArchiveError):
                    ar.unmarshal(type(record), raw + tail)

    def test_all_reserved_padding_bytes_and_bits(self):
        cases = (
            (response(), {7: 0xF0}), (snapshot(), {11: 0xFC}),
            (reset_audit(), {25: 0x80, 26: 0xFF, 27: 0xFF}),
            (ar.LessonRecord(0, 0, 0, 0, 0, 0, 0, 0, 0), {4: 0x80, 7: 0xC0}),
            (template(), {13: 0xFC, 28: 0xFC, 29: 0xFF, 30: 0xFF, 31: 0xFF}),
            (ar.SummaryRecord(STOCKS, STOCKS, 0, 0, ar.SummaryCounters.from_values((0,) * 62)),
             {13: 0xF0, 14: 0xFF, 15: 0xFF}),
            (directory(), {i: 0xFF for i in range(68, 72)}),
            (event(), {i: 0xFF for i in range(120, 128)}),
            (schedule(), {17: 0xE0, **{i: 0xFF for i in range(18, 32)}, 288: 0xFF, 1311: 0xFF}),
            (phase(), {62: 0xFF, 63: 0xFF}),
            (class_mapping(), {23: 0xFE, **{i: 0xFF for i in range(28, 32)}}),
            (ar.GRecord.from_id(403), {13: 0xFF, **{i: 0xFF for i in range(32, 128)}}),
        )
        for record, offsets in cases:
            for offset, mask in offsets.items():
                for bit in range(8):
                    if not mask & (1 << bit):
                        continue
                    raw = bytearray(ar.marshal(record))
                    raw[offset] |= 1 << bit
                    with self.subTest(record=type(record).__name__, offset=offset, bit=bit):
                        with self.assertRaises(ar.ArchiveError):
                            ar.unmarshal(type(record), bytes(raw))

    def test_no_boolean_coercion_in_any_integer_field(self):
        for record in specimens():
            for field in fields(record):
                if type(getattr(record, field.name)) is int or isinstance(getattr(record, field.name), ar.IntEnum):
                    with self.subTest(record=type(record).__name__, field=field.name):
                        with self.assertRaises(ar.ArchiveError):
                            replace(record, **{field.name: True})

    def test_nonintegers_negative_overflow_and_float_reject(self):
        for value in (-1, 65536, True, 1.0, float("nan"), float("inf"), "1"):
            with self.assertRaises(ar.ArchiveError):
                ar.Stocks(value, 0, 0, 0, 0)
        for value in (True, -1, 1 << 64, 1.0, float("nan"), float("inf"), None):
            with self.assertRaises(ar.ArchiveError):
                ar.SummaryCounters.from_values((value,) + (0,) * 61)
        for value in (-32769, 32768, True, 1.0):
            with self.assertRaises(ar.ArchiveError):
                replace(capsule(), action_return=value)

    def test_mutable_buffers_objects_subclasses_reject(self):
        for record in specimens():
            raw = ar.marshal(record)
            for bad in (bytearray(raw), memoryview(raw), [], {}, None, lambda: raw):
                with self.assertRaises(ar.ArchiveError):
                    ar.unmarshal(type(record), bad)
                with self.assertRaises(ar.ArchiveError):
                    ar.marshal(bad)
        class Extra(ar.Stocks):
            pass
        with self.assertRaises(ar.ArchiveError):
            ar.marshal(Extra(0, 0, 0, 0, 0))
        with self.assertRaises(ar.ArchiveError):
            replace(snapshot(), payload=bytearray(RAW))
        with self.assertRaises(ar.ArchiveError):
            ar.SummaryCounters.from_values([0] * 62)

    def test_encoder_rechecks_bypassed_frozen_validation(self):
        value = ar.Stocks(0, 0, 0, 0, 0)
        object.__setattr__(value, "energy", 65536)
        with self.assertRaises(ar.ArchiveError):
            ar.marshal(value)

    def test_unknown_enums_and_cross_enum_types(self):
        for record, field, bads in (
            (response(), "status", (7, 15, ar.Lifecycle.LIVE)),
            (capsule(), "lifecycle", (4, 255, ar.PathStatus.COMPLETE)),
            (capsule(), "decode", (6, 7)), (capsule(), "emission", (3,)),
            (capsule(), "outer_ordinal", (27, 28, 29, 30)),
            (snapshot(), "kind", (15, 255)), (snapshot(), "next_service", (13, 253)),
            (event(), "kind", (19, 255)), (event(), "status", (4, 255)),
            (directory(), "table", (14, 255)), (directory(), "codec", (3, 255)),
            (phase(), "product", (14, 255)), (phase(), "policy", (7, 255)),
            (phase(), "namespace", (35, 65535)),
        ):
            for value in bads:
                with self.assertRaises(ar.ArchiveError):
                    replace(record, **{field: value})

    def test_absent_scalar_and_missing_response_rejections(self):
        for changes in ({"b_present": 0}, {"yield_present": 0, "ecological_yield": 64},
                        {"slot_read": 0}, {"status": 6}, {"u": 1, "o": 1},
                        {"planned_due": 0}, {"learner_b": 1}, {"ecological_yield": 63}):
            with self.assertRaises(ar.ArchiveError):
                replace(response(), **changes)
        missing = ar.ResponseRecord(0, 6, 0, 1, 0, 0, 0, 1, 0, 1, 1,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3)
        self.assertEqual(ar.unmarshal(ar.ResponseRecord, ar.marshal(missing)), missing)

    def test_capsule_write_order_masks_and_yield(self):
        for changes in ({"v": 21}, {"a": 1}, {"w": 1}, {"correct_writes": 1},
                        {"condition_mask": 1 << 20}, {"age_mask": 4},
                        {"offered_cue": 1}, {"offer_usefulness": 1},
                        {"accepted_yield": 1}, {"action_return": 1},
                        {"action": 1, "accepted_yield": 9}):
            with self.assertRaises(ar.ArchiveError):
                replace(capsule(), **changes)
        ar.marshal(replace(capsule(), action=0, accepted_yield=0, action_return=0))
        ar.marshal(replace(capsule(), action=0, decide_admitted=1, action_admitted=1,
                           accepted_yield=64, action_return=16))

    def test_capsule_presence_constructor_and_marshal_reject(self):
        cases = [({name: value}, "controller observations require admitted DECIDE")
                 for name, values in (("health", (1, 2, 3)), ("e_bin", (1,)), ("p_bin", (1,)))
                 for value in values]
        cases += [({"action": action, "decide_admitted": 1,
                    "accepted_yield": income, "action_return": 16},
                   "accepted yield requires admitted action")
                  for action, income in ((0, 64), (1, 8))]
        cases.append(({"action_admitted": 1}, "absent action cannot be admitted"))
        for changes, reason in cases:
            with self.subTest(changes=changes):
                with self.assertRaisesRegex(ar.ArchiveError, reason):
                    replace(capsule(), **changes)
                # Revalidation must also catch objects forged after construction.
                forged = capsule()
                tick = ar.TickRecord(DIGEST, forged)
                for name, value in changes.items():
                    object.__setattr__(forged, name, value)
                for record in (forged, tick):
                    with self.assertRaisesRegex(ar.ArchiveError, reason):
                        ar.marshal(record)
                for objective in (0, 1):
                    with self.assertRaisesRegex(ar.ArchiveError, reason):
                        forged.validate_action_return(objective)

    def test_capsule_admitted_zero_and_nonzero_observations(self):
        for health in range(4):
            for e_bin in (0, 1):
                for p_bin in (0, 1):
                    with self.subTest(health=health, e_bin=e_bin, p_bin=p_bin):
                        row = replace(capsule(), outer_ordinal=1, funded_tick=1,
                                      decide_admitted=1, health=health, e_bin=e_bin, p_bin=p_bin)
                        self.assertEqual(ar.unmarshal(ar.TickCapsule, ar.marshal(row)), row)
        absent = capsule()
        observed_zero = replace(absent, decide_admitted=1)
        self.assertNotEqual(ar.marshal(absent), ar.marshal(observed_zero))

    def test_capsule_admitted_resource_yields_and_selected_zero_are_not_absence(self):
        for action, incomes in ((0, (0, 1, 63, 64)), (1, (0, 1, 7, 8))):
            for income in incomes:
                for objective in (0, 1):
                    with self.subTest(action=action, income=income, objective=objective):
                        reward = (income // 4 if action == 0 else 2 * income) if objective == 0 else 0
                        row = replace(capsule(), outer_ordinal=1, funded_tick=1, action=action,
                                      decide_admitted=1, action_admitted=1,
                                      accepted_yield=income, action_return=reward)
                        row.validate_action_return(objective)
                        self.assertEqual(ar.unmarshal(ar.TickCapsule, ar.marshal(row)), row)
        rejected = replace(capsule(), action=0, decide_admitted=1)
        admitted_zero = replace(rejected, action_admitted=1)
        for row in (rejected, admitted_zero):
            row.validate_action_return(0)
            self.assertEqual(ar.unmarshal(ar.TickCapsule, ar.marshal(row)).action, 0)
            self.assertNotEqual(ar.marshal(row), ar.marshal(capsule()))
        self.assertNotEqual(ar.marshal(rejected), ar.marshal(admitted_zero))

    def test_capsule_acquisition_writes_without_controller_or_action(self):
        for path, ordinal, width in (("lesson", 1, 5), ("commit", 2, 20)):
            for status in (ar.PathStatus.COMPLETE, ar.PathStatus.PAID_PREFIX_STOP):
                with self.subTest(path=path, status=status):
                    count = width if status == ar.PathStatus.COMPLETE else width - 2
                    row = replace(capsule(), outer_ordinal=ordinal, funded_tick=1,
                                  v=width, a=count, w=count, correct_writes=count - 1,
                                  incorrect_writes=1, **{path: status})
                    parsed = ar.unmarshal(ar.TickCapsule, ar.marshal(row))
                    self.assertEqual(parsed, row)
                    self.assertEqual((parsed.decide_admitted, parsed.action_admitted,
                                      parsed.action, parsed.accepted_yield), (0, 0, 3, 0))
                    parsed.validate_action_return(0)

    def test_main_and_drive_returns_require_explicit_g_objective(self):
        main = replace(capsule(), action=2, decide_admitted=1, action_admitted=1,
                       v=5, a=4, w=3, correct_writes=3, action_return=-3)
        drive = replace(main, action_return=16)
        main.validate_action_return(0)
        drive.validate_action_return(1)
        for record in (main, drive):
            self.assertEqual(ar.unmarshal(ar.TickCapsule, ar.marshal(record)), record)
        with self.assertRaises(ar.ArchiveError):
            drive.validate_action_return(0)
        with self.assertRaises(ar.ArchiveError):
            main.validate_action_return(1)
        forage = replace(capsule(), action=0, decide_admitted=1, action_admitted=1,
                 accepted_yield=63, action_return=15)
        forage.validate_action_return(0)
        replace(forage, action_return=0).validate_action_return(1)
        with self.assertRaises(ar.ArchiveError):
            main.validate_action_return(True)

    def test_teaching_absence_and_template_width_failures(self):
        for changes in ({"flags": 0}, {"paid_material": (0, 0, 0, 65536)},
                        {"scalar_presence": 0}, {"executed_c": 257}, {"code": 0}):
            if changes == {"flags": 0}:
                # Alive flags are observations, not a substitute for lifecycle replay.
                ar.marshal(replace(template(), **changes))
            else:
                with self.assertRaises(ar.ArchiveError):
                    replace(template(), **changes)
        with self.assertRaises(ar.ArchiveError):
            ar.LessonRecord(1, 1, 0, 0, 0, 0, 0, 0, 0)
        with self.assertRaises(ar.ArchiveError):
            ar.CommitRecord(1, 0, 0, 0, 0, 0)


class ReferenceCatalogTests(unittest.TestCase):
    def test_exact_integrated_counts_and_byte_ceiling(self):
        expected = {"ticks": 129700128, "responses": 111718400, "summaries": 285616,
                    "maximum_snapshots": 3829888, "source_reset_audits": 225712,
                    "canonical_future_roster": 29952, "paid_isolate_slots": 255920,
                    "offered_controllers": 94928896, "planned_outer_services": 3320673872,
                    "teaching_rows": 7602176, "block_commit_slots": 950272, "privileged_templates": 160}
        self.assertEqual(dict(ar.COMBINED_COUNTS), expected)
        self.assertEqual(ar.CORE_COUNTS["planned_outer_services"], 3311370832)
        for key, count in expected.items():
            self.assertEqual(ar.CORE_COUNTS[key] + ar.EXTENSION_COUNTS[key], count)
        self.assertEqual(ar.EXTENSION_COUNTS["ticks"], 361728)
        self.assertEqual(ar.EXTENSION_COUNTS["source_reset_audits"], 512)
        total = sum(count * size for count, size in (
            (129700128, 48), (111718400, 8), (3829888, 308), (225712, 64),
            (285616, 512), (7602176, 8), (950272, 4), (160, 64))) + 71303168
        self.assertEqual(total, 8595571712)
        self.assertEqual(ar.ARCHIVE_CEILING, ar.CORE_CEILING + ar.EXTENSION_CEILING)
        with self.assertRaises(TypeError):
            ar.COMBINED_COUNTS["ticks"] = 1

    def test_combined_global_ranges_not_shard_local(self):
        for table, start, count in ((ar.Table.TICK, 129338400, 361728),
                                    (ar.Table.RESPONSE, 111393280, 325120),
                                    (ar.Table.SNAPSHOT, 3818368, 11520),
                                    (ar.Table.SUMMARY, 284592, 1024),
                                    (ar.Table.RESET_AUDIT, 225200, 512),
                                    (ar.Table.CLASS, 29696, 256)):
            ar.validate_row_range(table, start, count)
            with self.assertRaises(ar.ArchiveError):
                ar.validate_row_range(table, start, count + 1)
        with self.assertRaises(ar.ArchiveError):
            ar.validate_row_range(ar.Table.TICK, 0, ar.U64_MAX)

    def test_reference_zero_none_and_explicit_all_ones(self):
        s = replace(snapshot(), payload_ref=0)
        self.assertEqual(ar.marshal(s)[12:16], bytes(4))
        self.assertEqual(ar.marshal(snapshot())[12:16], b"\xff" * 4)
        self.assertEqual(ar.unmarshal(ar.SnapshotRecord, ar.marshal(s)).payload_ref, 0)
        self.assertIsNone(ar.unmarshal(ar.SnapshotRecord, ar.marshal(snapshot())).payload_ref)
        for value in (ar.ABSENT_U32, -1, ar.SNAPSHOT_LIMIT, True):
            with self.assertRaises(ar.ArchiveError):
                replace(snapshot(), payload_ref=value)
        with self.assertRaises(ar.ArchiveError):
            replace(snapshot(), flags=3)  # Missing alias payload ref.
        self.assertEqual(ar.marshal(replace(reset_audit(), representative_recovery_phase=0))[20:24], bytes(4))

    def test_snapshot_finalized_bytes_missing_mismatch_bounds(self):
        s = replace(snapshot(), phase=0, payload_ref=0, payload_offset=32, flags=3)
        ar.validate_snapshot_links(s, {0: (32, RAW)}, phase_count=1, physical_size=308)
        for mapping, count, size in (({}, 1, 308), ({0: (32, bytes(276))}, 1, 308),
                                     ({0: (33, RAW)}, 1, 309), ({0: (32, RAW)}, 0, 308),
                                     ({0: (32, RAW)}, 1, 307),
                                     ({0: (32, bytearray(RAW))}, 1, 308)):
            with self.assertRaises(ar.ArchiveError):
                ar.validate_snapshot_links(s, mapping, phase_count=count, physical_size=size)
        with self.assertRaises(ar.ArchiveError):
            ar.validate_snapshot_links(s, defaultdict(lambda: (32, RAW)), phase_count=1, physical_size=308)

    def test_directory_dense_lengths_hashes_and_large_offsets(self):
        raw = ar.marshal(ar.TickRecord(DIGEST, capsule()))
        d = ar.DirectoryEntry(0, 0, 48, 129700127, 1, 1 << 50, 48, hashlib.sha256(raw).digest())
        d.verify_payload(raw)
        ar.validate_directory((d,), (1 << 50) + 48)
        for changes in ({"logical_count": 2}, {"record_bytes": 49},
                        {"physical_length": 47}, {"physical_offset": ar.U64_MAX},
                        {"logical_count": 0}):
            with self.assertRaises(ar.ArchiveError):
                replace(d, **changes)
        with self.assertRaises(ar.ArchiveError):
            d.verify_payload(raw[:-1] + b"\x01")
        with self.assertRaises(ar.ArchiveError):
            ar.validate_directory((d,), 48)
        with self.assertRaises(ar.ArchiveError):
            ar.validate_directory((d, d), (1 << 50) + 48)

    def test_reset_checks_are_assertions_not_automatic_passes(self):
        reset_audit().require_complete_checks()
        for bit in range(7):
            row = replace(reset_audit(), checks=127 ^ (1 << bit))
            self.assertEqual(ar.unmarshal(ar.ResetAuditRecord, ar.marshal(row)), row)
            with self.assertRaises(ar.ArchiveError):
                row.require_complete_checks()

    def test_all_404_g_ids_forward_grid(self):
        for code in (0, 1):
            for family in (0, 1):
                for e, ecut in enumerate((24576, 32768, 40960)):
                    for p, pcut in enumerate((32, 64, 96)):
                        cases = [(3*e+p, 0, 0), (90+3*e+p, 2, 0)]
                        cases += [(9+9*(3*e+p)+i, 1, interval)
                                  for i, interval in enumerate((1, 2, 4, 8, 16, 32, 64, 128, 256))]
                        for k, policy, interval in cases:
                            config = 200*code + 100*family + k
                            row = ar.GRecord.from_id(config)
                            self.assertEqual((row.code, row.family, row.policy, row.e_cut, row.p_cut, row.interval),
                                             (code, family, policy, ecut, pcut, interval))
                            ar.unmarshal(ar.GRecord, ar.marshal(row)).validate_id(config)
                self.assertEqual(ar.GRecord.from_id(200*code+100*family+99).objective, 1)
            for script in (0, 1):
                config = 400 + 2*code + script
                row = ar.GRecord.from_id(config)
                self.assertEqual((row.code, row.policy, row.family, row.objective), (code, 5+script, 1, 0))
                row.validate_id(config)
        for config in (-1, *range(404, 513), True, 1.0):
            with self.assertRaises(ar.ArchiveError):
                ar.GRecord.from_id(config)
        with self.assertRaises(ar.ArchiveError):
            ar.GRecord.from_id(403).validate_id(402)

    def test_phase_links_extents_and_reserved_catalog_values(self):
        p = phase()
        counts = {ar.Table.PHASE: 285616, ar.Table.SCHEDULE: 35,
                  ar.Table.SNAPSHOT: 3829888, ar.Table.TICK: 129700128, ar.Table.RESPONSE: 111718400}
        ar.validate_phase_links(p, counts)
        for table in counts:
            changed = dict(counts)
            changed[table] = 0
            with self.assertRaises(ar.ArchiveError):
                ar.validate_phase_links(p, changed)
        for changes in ({"phase": 285616}, {"first_tick": 129700128}, {"config": 404},
                        {"policy": 5}, {"schedule": None}, {"schedule": 33}, {"namespace": 35}):
            with self.assertRaises(ar.ArchiveError):
                replace(p, **changes)

    def test_schedule_tail_nibbles_and_identity(self):
        row = ar.ScheduleRecord(4, 1, 1, 0, 4, 3, 1, 0, 0, 0, 255, 1, (15,))
        raw = ar.marshal(row)
        self.assertEqual(raw[32:34], b"\x0f\x00")
        with self.assertRaises(ar.ArchiveError):
            ar.unmarshal(ar.ScheduleRecord, raw[:32] + b"\xff" + raw[33:])
        for changes in ({"namespace": 35}, {"schedule_id": 0}, {"cohort": 1},
                        {"u_mask": 1}, {"hub_permutation": 4}, {"cues": (16,)}):
            with self.assertRaises(ar.ArchiveError):
                replace(row, **changes)


class AccountingTests(unittest.TestCase):
    def test_large_unsigned_sum_and_overflow(self):
        self.assertEqual(ar.checked_sum((10**12 for _ in range(10000))), 10**16)
        self.assertEqual(ar.checked_sum((ar.U64_MAX, 0)), ar.U64_MAX)
        for values in ((ar.U64_MAX, 1), (1, -1), (True,), (1.0,)):
            with self.assertRaises(ar.ArchiveError):
                ar.checked_sum(values)

    def test_aggregate_thousands_of_counter_records_without_u16_truncation(self):
        c = ar.SummaryCounters.from_values((10**12,) * 62)
        result = ar.sum_counters(c for _ in range(3000))
        self.assertEqual(result.values, (3 * 10**15,) * 62)
        with self.assertRaises(ar.ArchiveError):
            ar.sum_counters((ar.SummaryCounters.from_values((ar.U64_MAX,) * 62), c))

    def test_sourcewise_conservation_and_original_totals(self):
        c = ar.SummaryCounters.from_values((0,) * 62)
        c = replace(c, planned_ticks=10, entered_ticks=10, active_ticks=9,
                    planned_responses=5, emitted_responses=4, correct_responses=3,
                    completed_code_writes=4, target_correct_code_writes=3,
                    target_incorrect_code_writes=1, executed_c_a=255, paid_c_a_envelopes=1,
                    paid_debits=(100, 10, 20, 30, 40),
                    accepted_passive_grants=(100, 10, 20, 30, 40),
                    ecological_offered_e=64, ecological_accepted_e=32, ecological_overflow_e=32)
        s = ar.SummaryRecord(STOCKS, replace(STOCKS, energy=STOCKS.energy+32), 0, 1, c)
        s.validate_accounting()
        self.assertEqual(c.padding(), (1, 0, 0))
        for changes in ({"correct_responses": 6}, {"active_ticks": 11},
                        {"target_incorrect_code_writes": 2}, {"ecological_overflow_e": 31},
                        {"paid_debits": (100, 20, 10, 30, 40)}, {"executed_c_a": 257},
                        {"paid_c_a_envelopes": ar.U64_MAX}):
            with self.assertRaises(ar.ArchiveError):
                replace(s, counters=replace(c, **changes)).validate_accounting()

    def test_gross_replacement_never_nets_removal_and_supply(self):
        original = ar.Stocks(1000, 1, 2, 3, 4)
        final = ar.Stocks(2000, 5, 6, 7, 8)
        c = replace(ar.SummaryCounters.from_values((0,) * 62),
                    external_removed=original.values, external_supplied=final.values,
                    external_dispatch_energy=1020)
        record = ar.SummaryRecord(original, final, 0, 8, c)
        record.validate_accounting()
        wire = ar.marshal(record)
        self.assertEqual(struct.unpack_from("<5Q", wire, 16 + 44 * 8), original.values)
        self.assertEqual(struct.unpack_from("<5Q", wire, 16 + 49 * 8), final.values)
        self.assertEqual(struct.unpack_from("<Q", wire, 16 + 57 * 8), (1020,))


class TraceTests(unittest.TestCase):
    def test_original_whole_phase_commitment_exact_prefix(self):
        first = ar.marshal(event())
        second = ar.marshal(replace(event(), event_index=1))
        result = ar.commit_trace(284592, DIGEST, iter((first, second)))
        expected = hashlib.sha256(b"E3TRACE9" + field_bytes(284592, 4) + DIGEST + first + second).digest()
        self.assertEqual(result, ar.TraceCommitment(2, 0, expected))
        self.assertNotEqual(ar.commit_trace(284593, DIGEST, (first,)).sha256, result.sha256)
        self.assertNotEqual(ar.commit_trace(284592, DIGEST, (first,)).sha256, result.sha256)

    def test_boundary_extra_states_required_and_committed(self):
        e = replace(event(), kind=ar.EventKind.FAULT_BOUNDARY, local_quote=ZERO5, tail_quote=ZERO5)
        raw = ar.encode_trace_event(e, pre_state=RAW, post_state=bytes(276))
        self.assertEqual(len(raw), 744)
        self.assertEqual(ar.decode_trace_event(raw), (e, RAW, bytes(276)))
        self.assertEqual(ar.commit_trace(0, DIGEST, (raw,)).sha256,
                         hashlib.sha256(b"E3TRACE9" + bytes(4) + DIGEST + raw).digest())
        for bad in (raw[:192], raw[:-1], raw + b"\x00", ar.marshal(event()) + RAW + RAW):
            with self.assertRaises(ar.ArchiveError):
                ar.decode_trace_event(bad)
        with self.assertRaises(ar.ArchiveError):
            ar.encode_trace_event(e)
        with self.assertRaises(ar.ArchiveError):
            ar.encode_trace_event(event(), pre_state=RAW, post_state=RAW)

    def test_trace_scalar_count_and_encoding(self):
        e = replace(event(), kind=ar.EventKind.SCALAR_IN, tag=17, width=16,
                    raw_before=0, raw_after=65472, aux=1023, local_quote=ZERO5, tail_quote=ZERO5)
        result = ar.commit_trace(0, DIGEST, (ar.marshal(e),))
        self.assertEqual((result.event_count, result.scalar_count), (1, 1))
        for changes in ({"tag": None}, {"width": 15}, {"raw_after": 65536}, {"raw_after": 65473}):
            with self.assertRaises(ar.ArchiveError):
                replace(e, **changes)

    def test_scalar_attempt_endpoints_golden_bytes_and_commitment(self):
        self.assertEqual(len(SCALAR_EVENT_GOLDEN), 192)
        self.assertEqual(ar.marshal(scalar_event()), SCALAR_EVENT_GOLDEN)
        for kind in (ar.EventKind.SCALAR_IN, ar.EventKind.SCALAR_OUT):
            for tag, width in ((8, 1), (9, 2)):
                for attempt in (0, 1023):
                    with self.subTest(kind=kind, tag=tag, attempt=attempt):
                        row = replace(scalar_event(), kind=kind, tag=tag, width=width, aux=attempt)
                        raw = bytearray(SCALAR_EVENT_GOLDEN)
                        raw[6] = kind
                        raw[14:16] = bytes((tag, width))
                        raw[116:120] = attempt.to_bytes(4, "little")
                        raw = bytes(raw)
                        self.assertEqual(ar.marshal(row), raw)
                        self.assertEqual(ar.unmarshal(ar.PrimitiveEvent, raw), row)
                        self.assertEqual(ar.encode_trace_event(row), raw)
                        self.assertEqual(ar.decode_trace_event(raw), (row, None, None))
                        expected = hashlib.sha256(b"E3TRACE9" + bytes(4) + DIGEST + raw).digest()
                        self.assertEqual(ar.commit_trace(0, DIGEST, (raw,)),
                                         ar.TraceCommitment(1, 1, expected))

    def test_scalar_attempt_out_of_range_rejects_every_codec_boundary(self):
        for kind in (ar.EventKind.SCALAR_IN, ar.EventKind.SCALAR_OUT):
            for tag, width in ((8, 1), (9, 2)):
                for attempt in (1024, 0xFFFFFFFF):
                    with self.subTest(kind=kind, tag=tag, attempt=attempt):
                        valid = replace(scalar_event(), kind=kind, tag=tag, width=width)
                        reason = r"scalar generation attempt must be a built-in integer in 0\.\.1023"
                        with self.assertRaisesRegex(ar.ArchiveError, reason):
                            replace(valid, aux=attempt)
                        object.__setattr__(valid, "aux", attempt)
                        with self.assertRaisesRegex(ar.ArchiveError, reason):
                            ar.marshal(valid)
                        with self.assertRaisesRegex(ar.ArchiveError, reason):
                            ar.encode_trace_event(valid)
                        # Corrupt independent golden bytes, never serialize the bad object.
                        raw = bytearray(SCALAR_EVENT_GOLDEN)
                        raw[6] = kind
                        raw[14:16] = bytes((tag, width))
                        raw[116:120] = attempt.to_bytes(4, "little")
                        raw = bytes(raw)
                        self.assertEqual(len(raw), 192)
                        with self.assertRaisesRegex(ar.ArchiveError, reason):
                            ar.unmarshal(ar.PrimitiveEvent, raw)
                        with self.assertRaisesRegex(ar.ArchiveError, reason):
                            ar.decode_trace_event(raw)
                        with self.assertRaisesRegex(ar.ArchiveError, reason):
                            ar.commit_trace(0, DIGEST, (raw,))

    def test_scalar_attempt_requires_built_in_integer(self):
        class IntSubclass(int):
            pass
        for kind in (ar.EventKind.SCALAR_IN, ar.EventKind.SCALAR_OUT):
            for attempt in (-1, True, False, 0.0, IntSubclass(0), ar.PathStatus.UNREACHED, 1 << 32):
                with self.subTest(kind=kind, attempt=repr(attempt), type=type(attempt).__name__):
                    with self.assertRaises(ar.ArchiveError):
                        replace(scalar_event(), kind=kind, aux=attempt)

    def test_non_scalar_aux_retains_kind_specific_meanings(self):
        cases = ((ar.EventKind.C, (0, 1, 2)), (ar.EventKind.CONTROL, (0, 1, 2)),
                 (ar.EventKind.TRANSPORT, (0, 1)),
                 (ar.EventKind.BOUNDARY, (0, int(ar.BoundaryKind.INTERVENTION) | (5 << 8))),
                 (ar.EventKind.METER, (1024, 0xFFFFFFFF)))
        for kind, values in cases:
            for aux in values:
                with self.subTest(kind=kind, aux=aux):
                    row = replace(event(), kind=kind, local_quote=ZERO5, tail_quote=ZERO5, aux=aux)
                    fixed = ar.marshal(row)
                    self.assertEqual(fixed[116:120], aux.to_bytes(4, "little"))
                    self.assertEqual(ar.unmarshal(ar.PrimitiveEvent, fixed), row)
                    attachments = ({"pre_state": RAW, "post_state": RAW}
                                   if kind == ar.EventKind.BOUNDARY else {})
                    raw = ar.encode_trace_event(row, **attachments)
                    self.assertEqual(ar.commit_trace(0, DIGEST, (raw,)), ar.TraceCommitment(
                        1, 0, hashlib.sha256(b"E3TRACE9" + bytes(4) + DIGEST + raw).digest()))
        for kind, aux in ((ar.EventKind.C, 3), (ar.EventKind.CONTROL, 3),
                          (ar.EventKind.TRANSPORT, 2), (ar.EventKind.BOUNDARY, 6 << 8)):
            with self.assertRaises(ar.ArchiveError):
                replace(event(), kind=kind, local_quote=ZERO5, tail_quote=ZERO5, aux=aux)

    def test_primitive_nonapplicable_fields_and_symbol_widths(self):
        for changes in ({"kind": ar.EventKind.C}, {"c": (1 << 31, 0, 0, 0, 0)},
                        {"tag": 0}, {"lane": 1104}, {"site": 65535}, {"service": 13}):
            with self.assertRaises(ar.ArchiveError):
                replace(event(), **changes)
        base = replace(event(), local_quote=ZERO5, tail_quote=ZERO5)
        for changes in ({"kind": ar.EventKind.READ2},
                        {"kind": ar.EventKind.WRITE2, "lane": 0, "raw_after": 4},
                        {"kind": ar.EventKind.S},
                        {"kind": ar.EventKind.ATTEMPT, "raw_after": 1},
                        {"kind": ar.EventKind.BOUNDARY, "aux": 6 << 8}):
            with self.assertRaises(ar.ArchiveError):
                replace(base, **changes)

    def test_trace_order_indices_and_bytes_only(self):
        for stream in ((ar.marshal(replace(event(), event_index=1)),),
                       (ar.marshal(event()), ar.marshal(event())),
                       (ar.marshal(event()), ar.marshal(replace(event(), tick=257))),
                       (event(),), (bytearray(ar.marshal(event())),)):
            with self.assertRaises(ar.ArchiveError):
                ar.commit_trace(0, DIGEST, stream)
        ar.commit_trace(0, DIGEST, (ar.marshal(event()), ar.marshal(replace(event(), tick=259))))

    def test_tick_hash_preserves_exact_bytes(self):
        tick = ar.TickRecord.from_state(RAW, capsule())
        self.assertEqual(tick.state_sha256, hashlib.sha256(RAW).digest())
        tick.verify_state(RAW)
        with self.assertRaises(ar.ArchiveError):
            tick.verify_state(RAW[:-1] + b"\x00")


class CanonicalMetadataTests(unittest.TestCase):
    def test_restricted_canonical_json_literal(self):
        value = {"z": ar.uint64_string(ar.U64_MAX), "a": [True, False, None, -1, "\n\t\"\\/"]}
        expected = b'{"a":[true,false,null,-1,"\\n\\t\\\"\\\\/"],"z":"18446744073709551615"}'
        self.assertEqual(ar.canonical_json(value), expected)
        self.assertEqual(ar.parse_canonical_json(expected), value)

    def test_floats_unicode_custom_containers_cycles_reject(self):
        cycle = []
        cycle.append(cycle)
        for value in (1.0, float("nan"), float("inf"), float("-inf"), 1 << 53,
                      "\u00e9", {"\U0001f600": 1}, {True: 0}, (1, 2),
                      defaultdict(int, {"a": 1}), cycle, b"abc"):
            with self.assertRaises(ar.ArchiveError):
                ar.canonical_json(value)

    def test_duplicate_noncanonical_and_json_nonfinite_reject(self):
        for raw in (b'{"a":1,"a":2}', b'{"b":0,"a":1}', b'{ "a":1}', b'-0',
                    b'1.0', b'1e0', b'NaN', b'Infinity', b'"\\u0061"',
                    b'{"a":true}\n', b'{}{}', b'\xff', b'"\\ud800"'):
            with self.assertRaises(ar.ArchiveError):
                ar.parse_canonical_json(raw)

    def test_uint64_string_canonical_zero_and_boundaries(self):
        for value in (0, 65536, 1 << 53, ar.U64_MAX):
            self.assertEqual(ar.parse_uint64_string(ar.uint64_string(value)), value)
        for value in ("", "00", "01", "+1", "-1", " 1", "1.0", "1e0", "\u0661",
                      str(1 << 64), True, 0):
            with self.assertRaises(ar.ArchiveError):
                ar.parse_uint64_string(value)

    def test_count_schema_is_closed_and_uses_decimal_strings(self):
        raw = ar.count_catalog_json(dict(ar.COMBINED_COUNTS))
        parsed = json.loads(raw)
        self.assertEqual(set(parsed), set(ar.COMBINED_COUNTS))
        self.assertTrue(all(type(v) is str for v in parsed.values()))
        self.assertEqual(parsed["planned_outer_services"], "3320673872")
        for counts in ({}, {**ar.COMBINED_COUNTS, "extra": 1},
                       {**ar.COMBINED_COUNTS, "ticks": True},
                       defaultdict(int, ar.COMBINED_COUNTS), list(ar.COMBINED_COUNTS)):
            with self.assertRaises(ar.ArchiveError):
                ar.count_catalog_json(counts)


if __name__ == "__main__":
    unittest.main()