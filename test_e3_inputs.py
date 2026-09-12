"""Public, deterministic input-component fixtures, not engineering experiments.

No random roots, target draws, full bootstrap, worker execution or paid reset.
Literal payloads/digests and a separate RFC 2104 construction test the input law.
Run with Python -B -m unittest test_e3_inputs.
"""

import ast
from collections import Counter
from dataclasses import FrozenInstanceError, MISSING, fields, replace
from fractions import Fraction
import hashlib
import inspect
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from e3 import inputs as p
from e3 import physical, protocol
from verify_e3_design import verify


KEY = bytes.fromhex("8f6c2a19d4b730e5a1c9087f62de4b03c5a87910ef26d4b7930a1e65c8f247bd")
ANALYSIS = bytes.fromhex("37b4e0a1c9625df80a7e413bd6982fc54e0137a965c2bd084fae1763908dc25b")
BASE = p.InputTuple("E3-EVAL-0.8", "engineering", 1, 1, "H1-SCREEN", "RECOVERY",
                    "T", 17, 0, 0, 0, 0)
BAD_INTS = (True, False, 1.0, float("nan"), float("inf"), "1", None, b"1")


def reference_hmac(key, payload):
    """RFC 2104 ipad/opad construction without production/hmac helpers."""
    if len(key) > 64:
        key = hashlib.sha256(key).digest()
    block = key + bytes(64 - len(key))
    inner = hashlib.sha256(bytes(v ^ 0x36 for v in block) + payload).digest()
    return hashlib.sha256(bytes(v ^ 0x5c for v in block) + inner).digest()


def reference_uniform(values, m):
    # Caller builds all eleven semantic fields independently of production.
    for attempt in range(1024):
        raw = json.dumps([*values, attempt], ensure_ascii=False,
                         separators=(",", ":")).encode("utf-8")
        digest = reference_hmac(KEY, raw)
        number = sum(digest[i] * 256 ** i for i in range(16))
        if number < ((2 ** 128) // m) * m:
            return number % m
    raise AssertionError("public reference exhausted")


def reference_shuffle(values, family, phase, purpose, location=0, slot=0):
    values = list(values)
    for ordinal, position in enumerate(range(len(values) - 1, 0, -1)):
        index = reference_uniform(["E3-EVAL-0.8", "engineering", 1, 1,
                                   family, phase, purpose, 0, location, slot, ordinal],
                                  position + 1)
        values[position], values[index] = values[index], values[position]
    return tuple(values)


def context(family="H1", product="SCREEN", stage="RECOVERY"):
    return p.phase_context("engineering", 1, 1, family, product, stage)


class TestE3Inputs(unittest.TestCase):
    def test_01_rfc4231_independent_primitive_vectors(self):
        # RFC 4231 sections 4.2, 4.3 and 4.7; primitive accepts arbitrary RFC
        # keys privately. The E3 public API below still requires exactly32.
        vectors = (
            (b"\x0b" * 20, b"Hi There",
             "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"),
            (b"Jefe", b"what do ya want for nothing?",
             "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843"),
            (b"\xaa" * 131, b"Test Using Larger Than Block-Size Key - Hash Key First",
             "60e431591ee0b67f0d8a26aacbf5b77f8e0bc6213728c5140546040f0ee37f54"),
        )
        for key, payload, digest in vectors:
            self.assertEqual(reference_hmac(key, payload).hex(), digest)
            self.assertEqual(p._digest(key, payload).hex(), digest)

    def test_02_literal_protocol_vectors(self):
        vectors = (
            (KEY, BASE,
             b'["E3-EVAL-0.8","engineering",1,1,"H1-SCREEN","RECOVERY","T",17,0,0,0,0]',
             "8001d90cc0d7c1a98bf43ec2010be526ec435f752e119650fd4fc00fe35b6a78",
             51699923066281281519825745026615935360),
            (KEY, p.InputTuple("E3-EVAL-0.8", "engineering", 8, 8, "H2-SCRIPTED",
                               "ECOLOGY", "aux_bit1", 512, 1103, 1, 0, 1023),
             b'["E3-EVAL-0.8","engineering",8,8,"H2-SCRIPTED","ECOLOGY","aux_bit1",512,1103,1,0,1023]',
             "c141d57beed152dd03729f6f9077123314139e0911ea857f161ffb48f2c682a0",
             67886514178628166734808120282049757633),
            (ANALYSIS, p.bootstrap_coordinate(9999, 31, 0),
             b'["E3-EVAL-0.8","final",0,0,"analysis","bootstrap","individual-index",0,0,0,319999,0]',
             "3877220f95f357863fe5ebd376a4478917c3945f875e2a9b8173290e22423967",
             182476224229174140140251770780205086520),
        )
        for key, coordinate, payload, digest, number in vectors:
            self.assertEqual(p.canonical_tuple(coordinate), payload)
            self.assertEqual(reference_hmac(key, payload).hex(), digest)
            self.assertEqual(p.indexed_digest(key, coordinate).hex(), digest)
            self.assertEqual(int.from_bytes(bytes.fromhex(digest)[:16], "little"), number)
        self.assertEqual(p.uniform(KEY, BASE, 3).value, 2)
        self.assertEqual(p.uniform(ANALYSIS, p.bootstrap_coordinate(9999, 31, 0), 32).value, 24)
        self.assertEqual(p.CONFORMANCE_KEY, KEY)
        self.assertEqual(p.ANALYSIS_KEY, ANALYSIS)
        self.assertNotEqual(KEY, ANALYSIS)

    def test_03_restricted_jcs_escape_and_maximum_integer(self):
        coord = p.InputTuple("E3-EVAL-0.8", "", 0, 0, "", '"\\/\b\t\n\f\r\x00\x1f\x7f',
                             "", 9007199254740991, 9007199254740991,
                             9007199254740991, 9007199254740991, 1023)
        raw = (b'["E3-EVAL-0.8","",0,0,"","\\\"\\\\/\\b\\t\\n\\f\\r\\u0000\\u001f\x7f","",'
               b'9007199254740991,9007199254740991,9007199254740991,9007199254740991,1023]')
        self.assertEqual(p.canonical_tuple(coord), raw)
        self.assertNotIn(b"9007199254740991\"", raw)
        for name in ("individual", "panel", "tick", "location", "slot", "draw_index"):
            self.assertEqual(getattr(replace(BASE, **{name: (1 << 53) - 1}), name), (1 << 53) - 1)
            for invalid in (-1, 1 << 53, (1 << 64) - 1):
                with self.assertRaises(ValueError):
                    replace(BASE, **{name: invalid})

    def test_04_strict_field_types_and_attempts(self):
        for name in ("individual", "panel", "tick", "location", "slot", "draw_index", "attempt"):
            for value in BAD_INTS:
                with self.subTest(name=name, value=value), self.assertRaises(TypeError):
                    replace(BASE, **{name: value})
        for name in ("version", "cohort", "family", "phase", "purpose"):
            for value in (0, True, None, b"H1"):
                with self.assertRaises(TypeError):
                    replace(BASE, **{name: value})
            for value in ("\u00e9", "e\u0301", "\ud800", "\U0001f600"):
                with self.assertRaises(ValueError):
                    replace(BASE, **{name: value})
        for value in (-1, 1024, 1 << 53):
            with self.assertRaises(ValueError):
                replace(BASE, attempt=value)
        with self.assertRaises(ValueError):
            replace(BASE, version="E3-EVAL-0.9")
        for value in ([], (), {}, None, b"[]"):
            with self.assertRaises(TypeError):
                p.canonical_tuple(value)

    def test_05_strict_keys_and_uniform_bounds(self):
        class BytesSubclass(bytes):
            pass
        for key in (True, 32, "00" * 32, bytearray(KEY), memoryview(KEY), None, BytesSubclass(KEY)):
            with self.assertRaises(TypeError):
                p.uniform(key, BASE, 3)
        for size in (0, 1, 20, 31, 33, 64):
            with self.assertRaises(ValueError):
                p.indexed_digest(bytes(size), BASE)
        for m in BAD_INTS:
            with self.assertRaises(TypeError):
                p.uniform(KEY, BASE, m)
        for m in (0, -1, (1 << 128) + 1):
            with self.assertRaises(ValueError):
                p.uniform(KEY, BASE, m)
        with self.assertRaises(ValueError):
            p.uniform(KEY, replace(BASE, attempt=1), 3)
        for invalid in (b"", bytes(16), bytes(31), bytes(33), bytearray(32), None):
            with patch.object(p, "_digest", return_value=invalid), self.assertRaises(p.InputGenerationError):
                p.uniform(KEY, BASE, 3)

    def test_06_schema_required_frozen_and_no_worker_objects(self):
        self.assertEqual(tuple(f.name for f in fields(p.InputTuple)), (
            "version", "cohort", "individual", "panel", "family", "phase", "purpose",
            "tick", "location", "slot", "draw_index", "attempt"))
        self.assertTrue(all(f.default is MISSING and f.default_factory is MISSING
                            for f in fields(p.InputTuple)))
        with self.assertRaises(TypeError):
            p.InputTuple()
        with self.assertRaises(FrozenInstanceError):
            BASE.tick = 99
        self.assertFalse(hasattr(BASE, "__dict__"))
        record = p.uniform(KEY, BASE, 3)
        with self.assertRaises((TypeError, protocol.ProtocolError)):
            protocol.encode_frame(record)
        self.assertEqual(tuple(f.name for f in fields(record)), ("coordinates", "bound", "value"))
        with self.assertRaises(ValueError):
            p.InputRecord(BASE, 3, 3)
        with self.assertRaises(TypeError):
            p.InputRecord(BASE, 3, True)

    def test_07_categorical_three_rejects_boundary_without_bias(self):
        # 2^128 % 3 == 1; the all-ones uint128 MUST reject, not become zero.
        limit = (1 << 128) - 1
        digests = (limit.to_bytes(16, "little") + bytes(16),
                   (limit - 1).to_bytes(16, "little") + b"\xff" * 16)
        with patch.object(p, "_digest", side_effect=digests) as digest:
            record = p.uniform(KEY, BASE, 3)
        self.assertEqual((record.value, record.attempt), (2, 1))
        self.assertEqual(len(digest.call_args_list), 2)
        expected = b'["E3-EVAL-0.8","engineering",1,1,"H1-SCREEN","RECOVERY","T",17,0,0,0,'
        self.assertEqual([call.args[1] for call in digest.call_args_list],
                         [expected + b"0]", expected + b"1]"])
        for x in range(9):
            with patch.object(p, "_digest", return_value=x.to_bytes(16, "little") + bytes(16)):
                self.assertEqual(p.uniform(KEY, BASE, 3).value, x % 3)

    def test_08_last_attempt_and_exhaustion_are_exact(self):
        rejection = b"\xff" * 32
        with patch.object(p, "_digest", side_effect=[rejection] * 1023 + [bytes(32)]) as digest:
            record = p.uniform(KEY, BASE, 3)
        self.assertEqual((record.value, record.attempt, digest.call_count), (0, 1023, 1024))
        with patch.object(p, "_digest", return_value=rejection) as digest:
            with self.assertRaises(p.InputGenerationError):
                p.uniform(KEY, BASE, 3)
        self.assertEqual(digest.call_count, 1024)
        self.assertEqual(json.loads(digest.call_args.args[1])[-1], 1023)
        self.assertEqual(BASE.attempt, 0)

    def test_09_uint128_window_endianness_and_max_bound(self):
        prefix = bytes(range(16))
        number = sum(i << (8 * i) for i in range(16))
        for tail in (bytes(16), b"\xff" * 16):
            with patch.object(p, "_digest", return_value=prefix + tail):
                self.assertEqual(p.uniform(KEY, BASE, 1 << 128).value, number)
                self.assertEqual(p.uniform(KEY, BASE, 10000).value, number % 10000)
        with patch.object(p, "_digest", return_value=b"\xff" * 32):
            self.assertEqual(p.uniform(KEY, BASE, 1 << 128).value, (1 << 128) - 1)
            self.assertEqual(p.uniform(KEY, BASE, 1).value, 0)

    def test_10_query_order_is_stateless_and_all_fields_committed(self):
        coordinates = tuple(replace(BASE, tick=tick, draw_index=tick * 3) for tick in range(1, 10))
        expected = {c: p.uniform(KEY, c, 10000) for c in coordinates}
        for c in reversed(coordinates):
            self.assertEqual(p.uniform(KEY, c, 10000), expected[c])
        p.uniform(KEY, replace(BASE, draw_index=999), 3)  # Unrelated unused draw.
        self.assertEqual(p.uniform(KEY, coordinates[0], 10000), expected[coordinates[0]])
        for name in ("cohort", "family", "phase", "purpose", "individual", "panel",
                     "tick", "location", "slot", "draw_index", "attempt"):
            value = getattr(BASE, name)
            changed = replace(BASE, **{name: value + "X" if type(value) is str else value + 1})
            self.assertNotEqual(p.canonical_tuple(BASE), p.canonical_tuple(changed))
            self.assertEqual(p.indexed_digest(KEY, changed), reference_hmac(KEY, p.canonical_tuple(changed)))

    def test_11_all_35_schedule_slots_and_ids(self):
        expected = (
            ("H1", "TRUNK", "ACQUISITION"), ("H1", "TRUNK", "DEVELOPMENT"),
            ("H2", "TRUNK", "ACQUISITION"), ("H2", "TRUNK", "DEVELOPMENT"),
            ("H1", "TRUNK", "PRE"), ("H2", "TRUNK", "PREREQUISITE"),
            ("H1", "SCREEN", "RECOVERY"), ("H1", "SCREEN", "FINAL"), ("H2", "SCREEN", "ECOLOGY"),
            ("H1", "SELECTED-CONTROL", "RECOVERY"), ("H1", "SELECTED-CONTROL", "FINAL"),
            ("H2", "SELECTED-CONTROL", "ECOLOGY"), ("H1", "CORE", "RECOVERY"),
            ("H1", "CORE", "FINAL"), ("H2", "CORE", "ECOLOGY"),
            ("H1", "SELECTED-CONTROL", "ACUTE"), ("H1", "SELECTED-CONTROL", "POST"),
            ("H1", "LL13", "RECOVERY"), ("H1", "LL13", "FINAL"),
            ("H1", "FLIP", "RECOVERY"), ("H1", "FLIP", "FINAL"),
            ("H1", "HUB", "RECOVERY"), ("H1", "HUB", "FINAL"),
            ("H1", "RESOURCE", "RECOVERY"), ("H1", "RESOURCE", "FINAL"),
            ("H2", "G-DIAG", "ECOLOGY"), ("H2", "HS-REFERENCE", "ECOLOGY"),
            ("H2", "MIXED", "ECOLOGY"), ("H1", "RESET", "RECOVERY"),
            ("H1", "RESET", "FINAL"), ("H2", "RESET", "RECOVERY"), ("H2", "RESET", "FINAL"),
            ("H1", "ORACLE", "ZERO-FAULT"), ("H1", "ORACLE", "LIVE-WEAR"),
            ("H2", "SCRIPTED", "ECOLOGY"),
        )
        self.assertEqual(len(p.SCHEDULE_CATALOG), 35)
        for slot, triple in enumerate(expected):
            row = p.SCHEDULE_CATALOG[slot]
            self.assertEqual((row.slot, row.family, row.product, row.stage), (slot, *triple))
            cohort, individual = ("final", 300) if row.product == "CORE" else ("engineering", 1)
            c = p.phase_context(cohort, individual, 1, *triple)
            self.assertEqual(c.schedule_slot, slot)
            self.assertEqual(c.schedule_id, (4096 if cohort == "final" else 0) + slot)
        self.assertEqual(p.PhaseContext("engineering", 8, 8, 34).schedule_id, 4066)
        self.assertEqual(p.PhaseContext("final", 331, 8, 31).schedule_id, 20447)
        self.assertEqual(context("H2", "SCRIPTED", "ECOLOGY").family, "H2-SCRIPTED")

    def test_12_catalog_rejects_invalid_combinations_and_widths(self):
        for slot in (-1, 35, 63, 64, 65535):
            with self.assertRaises(ValueError):
                p.PhaseContext("engineering", 1, 1, slot)
        for name in ("individual", "panel", "schedule_slot"):
            for value in BAD_INTS:
                with self.assertRaises(TypeError):
                    replace(context(), **{name: value})
        for args in (("engineering", 0, 1, 0), ("engineering", 9, 1, 0),
                     ("final", 299, 1, 0), ("final", 332, 1, 0),
                     ("engineering", 1, 0, 0), ("engineering", 1, 9, 0),
                     ("engineering", 1, 2, 32), ("final", 300, 1, 34),
                     ("engineering", 1, 1, 12), ("0", 1, 1, 0)):
            with self.assertRaises(ValueError):
                p.PhaseContext(*args)
        for triple in (("H1", "SCREEN", "ECOLOGY"), ("H2", "SCREEN", "RECOVERY"),
                       ("H1", "SCREEN", "POST"), ("H2-SCRIPTED", "RESET", "FINAL"),
                       ("H1", "TRUNK", "unknown")):
            with self.assertRaises(ValueError):
                context(*triple)

    def test_13_pairing_and_reset_omit_history_axes_not_complete_G(self):
        source_contexts = (context(), context(product="SELECTED-CONTROL"),
                           context(product="RESOURCE"), context("H1", "TRUNK", "DEVELOPMENT"),
                           context("H1", "ORACLE", "LIVE-WEAR"))
        future = p.reset_context("engineering", 1, 1, "H1", "RECOVERY")
        expected = b'["E3-EVAL-0.8","engineering",1,1,"H1","RESET-RECOVERY","guess",17,0,1,0,0]'
        for history_id, source in enumerate(source_contexts):
            with self.subTest(history_id=history_id, product=source.rule.product):
                reset = p.reset_context(source.cohort, source.individual, source.panel,
                                        source.rule.family, "RECOVERY")
                self.assertEqual(reset, future)
                self.assertEqual(p.canonical_tuple(p.guess_input(KEY, reset, 17).coordinates), expected)
        # Archive axes have no input-builder parameter. No source object is
        # accepted/retained, and this is NOT an actual-body cancellation audit.
        for forbidden in ("history_id", "source_id", "branch", "code", "policy", "candidate", "outcome", "g"):
            with self.assertRaises(TypeError):
                p.reset_context("engineering", 1, 1, "H1", "FINAL", **{forbidden: 0})
            with self.assertRaises(TypeError):
                p.phase_context("engineering", 1, 1, "H1", "SCREEN", "RECOVERY", **{forbidden: 0})
        namespaces = {p.guess_input(KEY, c, 17).coordinates.family for c in source_contexts}
        self.assertEqual(len(namespaces), len(source_contexts))
        script = context("H2", "SCRIPTED", "ECOLOGY")
        self.assertEqual(p.reset_context(script.cohort, script.individual, script.panel, "H2", "FINAL").family, "H2")
        # G is deliberately not claimed equal: public script IDs400/401 differ.
        self.assertNotEqual(protocol.PublicConfiguration(400), protocol.PublicConfiguration(401))
        self.assertNotEqual(future, p.reset_context("engineering", 1, 2, "H1", "RECOVERY"))
        self.assertNotEqual(future, p.reset_context("engineering", 1, 1, "H2", "RECOVERY"))

    def test_14_h1_probes_and_recovery_balance(self):
        cases = ((context(), 0, 128), (context(stage="FINAL"), 256, 261),
                 (context("H1", "TRUNK", "PRE"), 256, 261),
                 (context("H2", "TRUNK", "PREREQUISITE"), 256, 261),
                 (context("H1", "SELECTED-CONTROL", "ACUTE"), 256, 261),
                 (context("H1", "SELECTED-CONTROL", "POST"), 256, 261),
                 (context("H1", "ORACLE", "ZERO-FAULT"), 256, 261),
                 (context("H1", "ORACLE", "LIVE-WEAR"), 256, 261))
        for c, count, length in cases:
            result = p.generate_schedule(KEY, c)
            self.assertEqual((len(result.admissions), len(result.offers)), (count, length))
            self.assertEqual(result.lessons, ())
            self.assertEqual(result.commit_blocks, ())
            self.assertEqual(Counter(result.admissions if count else result.offers),
                             {cue: 16 if count else 8 for cue in range(16)})
            self.assertEqual(result.offers[:count], result.admissions)

    def test_15_independent_fisher_yates_expected_order(self):
        c = context()
        result = p.generate_schedule(KEY, c)
        initial = tuple(cue for cue in range(16) for _ in range(8))
        expected = reference_shuffle(initial, "H1-SCREEN", "RECOVERY", "recovery-offers")
        self.assertEqual(result.offers, expected)
        self.assertEqual(len(result.records), 127)
        self.assertEqual([r.bound for r in result.records], list(range(128, 1, -1)))
        self.assertEqual([r.coordinates.draw_index for r in result.records], list(range(127)))
        self.assertEqual(p.generate_schedule(KEY, c), result)

    def test_16_acquisition_grouped_pass_matrix_and_independent_expected(self):
        result = p.generate_schedule(KEY, context("H1", "TRUNK", "ACQUISITION"))
        self.assertEqual((len(result.lessons), len(result.commit_blocks), len(result.records)), (256, 64, 240))
        self.assertEqual(Counter(result.lessons), {cue: 16 for cue in range(16)})
        expected = []
        for pass_index in range(16):
            order = reference_shuffle(range(4), "H1-TRUNK", "ACQUISITION", "acquisition-blocks", pass_index)
            self.assertEqual(result.commit_blocks[4 * pass_index:4 * pass_index + 4], order)
            for block in order:
                expected.extend(reference_shuffle(range(block * 4, block * 4 + 4), "H1-TRUNK",
                                                   "ACQUISITION", "acquisition-cues", pass_index, block))
        self.assertEqual(result.lessons, tuple(expected))
        for index, block in enumerate(result.commit_blocks):
            self.assertEqual(set(result.lessons[4 * index:4 * index + 4]), set(range(4 * block, 4 * block + 4)))
        self.assertEqual((result.admissions, result.offers), ((), ()))
        self.assertEqual(len({r.coordinates for r in result.records}), 240)

    def test_17_development_extras_and_independent_drains(self):
        result = p.generate_schedule(KEY, context("H2", "TRUNK", "DEVELOPMENT"))
        self.assertEqual((len(result.admissions), len(result.offers)), (2043, 2048))
        self.assertEqual(Counter(Counter(result.admissions).values()), {128: 11, 127: 5})
        extra = reference_shuffle(range(16), "H2-TRUNK", "DEVELOPMENT", "extra-cues")[:11]
        expected = reference_shuffle(tuple(c for c in range(16) for _ in range(127)) + extra,
                                     "H2-TRUNK", "DEVELOPMENT", "admissions")
        self.assertEqual(result.admissions, expected)
        for tick in range(2044, 2049):
            value = reference_uniform(["E3-EVAL-0.8", "engineering", 1, 1, "H2-TRUNK",
                                       "DEVELOPMENT", "drain-offer", tick, 0, 0, 0], 16)
            self.assertEqual(result.offers[tick - 1], value)
        self.assertEqual([r.coordinates.tick for r in result.records[-5:]], list(range(2044, 2049)))

    def test_18_h2_exact_endpoint_and_script_schedule(self):
        for product in ("SCREEN", "SCRIPTED"):
            c = context("H2", product, "ECOLOGY")
            result = p.generate_schedule(KEY, c)
            self.assertEqual((len(result.admissions), len(result.offers)), (507, 512))
            self.assertEqual(Counter(Counter(result.admissions[:251]).values()), {16: 11, 15: 5})
            self.assertEqual(Counter(result.admissions[251:507]), {cue: 16 for cue in range(16)})
            assignment = p.usefulness_assignment(KEY, c)
            self.assertEqual(sum(cue in assignment.useful for cue in result.admissions[251:]), 128)
            self.assertEqual(sum(cue in assignment.obsolete for cue in result.admissions[251:]), 128)
            expected = reference_shuffle(tuple(cue for cue in range(16) for _ in range(16)),
                                         "H2-" + product, "ECOLOGY", "endpoint-admissions")
            self.assertEqual(result.admissions[251:], expected)
            self.assertEqual([r.coordinates.tick for r in result.records[-5:]], [508, 509, 510, 511, 512])
            self.assertEqual(len({r.coordinates for r in result.records}), len(result.records))

    def test_19_all_fault_indices_reservoir_exclusion_and_physical_compatibility(self):
        c = context()
        coordinates = p.fault_coordinates(c, 128)
        expected = tuple((lane, purpose, local) for lane in range(1104) if not 900 <= lane < 924
                         for local, purpose in enumerate(("code_flip", "code_erase") if lane < 80
                                                         else ("aux_bit0", "aux_bit1", "aux_erase")))
        self.assertEqual(len(coordinates), 3160)
        self.assertEqual(len(set(coordinates)), 3160)
        self.assertEqual(tuple((r.location, r.purpose, r.slot) for r in coordinates), expected)
        self.assertEqual(tuple((r.location, r.purpose) for r in coordinates), physical.FAULT_SLOTS)
        self.assertTrue(all(r.tick == 128 and r.draw_index == r.attempt == 0 for r in coordinates))
        self.assertEqual(Counter(r.purpose for r in coordinates), {
            "code_flip": 80, "code_erase": 80, "aux_bit0": 1000, "aux_bit1": 1000, "aux_erase": 1000})
        self.assertEqual(sum(r.location >= 972 for r in coordinates), 396)
        records = p.fault_inputs(KEY, c, 128)
        frame = physical.FaultFrame(tuple(r.value for r in records))
        self.assertEqual(len(frame), 3160)
        self.assertTrue(all(r.bound == 10000 for r in records))
        for index in (0, 159, 160, 2619, 3159):
            lane, purpose, slot = expected[index]
            values = ["E3-EVAL-0.8", "engineering", 1, 1, "H1-SCREEN", "RECOVERY", purpose, 128, lane, slot, 0]
            self.assertEqual(records[index].value, reference_uniform(values, 10000))

    def test_20_exact_hazard_thresholds_all_ages(self):
        for age in range(16):
            flip, erase = p.fault_thresholds(age)
            self.assertEqual((flip, erase), physical.fault_thresholds(age))
            self.assertEqual(Fraction(flip, 10000), Fraction(1 + age, 1000))
            self.assertEqual(Fraction(erase, 10000), Fraction(age, 10000))
            self.assertEqual(sum(x < flip for x in range(10000)), flip)
            self.assertEqual(sum(x < erase for x in range(10000)), erase)
        for age in (-1, 16):
            with self.assertRaises(ValueError):
                p.fault_thresholds(age)
        for age in BAD_INTS:
            with self.assertRaises(TypeError):
                p.fault_thresholds(age)

    def test_21_planned_ranks_guesses_challenges_and_no_action_indices(self):
        records = p.exploration_inputs(KEY, context(), 17)
        self.assertEqual([(r.coordinates.purpose, r.bound) for r in records], [("B", 2), ("T", 3), ("X", 16)])
        self.assertEqual(records[1].value, 2)
        for tick in (1, 5, 6, 128):
            r = p.guess_input(KEY, context(), tick)
            self.assertEqual((r.bound, r.coordinates.tick, r.coordinates.slot), (2, tick, (tick - 1) % 5))
        for c in (context(stage="FINAL"), p.reset_context("engineering", 1, 1, "H2", "FINAL"),
                  context(product="FLIP")):
            draws = p.challenge_inputs(KEY, c)
            self.assertEqual(len(draws), 80)
            self.assertEqual([r.coordinates.location for r in draws], list(range(80)))
            self.assertTrue(all(r.bound == 10 and r.coordinates.tick == 0 for r in draws))
            self.assertEqual(sum(value == 0 for value in range(10)), 1)
        for c in (context(), context("H2", "SCREEN", "ECOLOGY"), context("H1", "TRUNK", "PRE")):
            with self.assertRaises(ValueError):
                p.challenge_inputs(KEY, c)
        for tick in (0, 129):
            with self.assertRaises(ValueError):
                p.guess_input(KEY, context(), tick)
        for c in (context("H2", "SCRIPTED", "ECOLOGY"), context(stage="FINAL")):
            with self.assertRaises(ValueError):
                p.exploration_inputs(KEY, c, 1)
        with self.assertRaises(ValueError):
            p.guess_input(KEY, context("H1", "TRUNK", "ACQUISITION"), 1)

    def test_22_UO_hub_independent_group_maps_and_purpose_roots(self):
        for product in ("SCREEN", "G-DIAG", "HS-REFERENCE", "SCRIPTED", "MIXED"):
            c = context("H2", product, "ECOLOGY")
            assignment = p.usefulness_assignment(KEY, c)
            self.assertEqual((len(assignment.useful), len(assignment.obsolete)), (8, 8))
            self.assertEqual(set(assignment.useful) | set(assignment.obsolete), set(range(16)))
            self.assertFalse(set(assignment.useful) & set(assignment.obsolete))
            counts = sorted(Counter(cue // 4 for cue in assignment.obsolete).values())
            self.assertEqual(counts, [2, 2, 2, 2] if product == "MIXED" else [4, 4])
            if product != "MIXED":
                blocks = reference_shuffle(range(4), "H2-" + product, "ECOLOGY", "whole-block-UO")[:2]
                self.assertEqual(assignment.obsolete, tuple(cue for cue in range(16) if cue // 4 in blocks))
        hubs = p.hub_assignment(KEY, "engineering", 1)
        self.assertEqual(Counter(hubs), {0: 2, 1: 2, 2: 2, 3: 2})
        self.assertEqual(hubs, p.hub_assignment(KEY, "engineering", 1))
        with self.assertRaises(ValueError):
            p.hub_assignment(KEY, "final", 300)
        self.assertEqual(p.PURPOSE_ROOTS["T"], "exploration")
        self.assertEqual(p.PURPOSE_ROOTS["guess"], "guess")
        self.assertEqual(p.PURPOSE_ROOTS["FLIP"], "injury")
        self.assertEqual(p.PURPOSE_ROOTS["challenge"], "challenge")
        self.assertEqual(set(p.PURPOSE_ROOTS.values()), {
            "schedule", "fault", "challenge", "exploration", "guess", "UO", "injury", "analysis"})
        with self.assertRaises(TypeError):
            p.PURPOSE_ROOTS["T"] = "guess"

    def test_23_no_generator_worker_imports_or_freeze_changes(self):
        tree = ast.parse(inspect.getsource(p))
        imports = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
        imports |= {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        self.assertEqual(imports, {"dataclasses", "hmac", "json", "types"})
        for name in ("draw_target", "generate_target", "generate_root", "BCryptGenRandom", "secrets", "random", "os"):
            self.assertFalse(hasattr(p, name))
        for fn in (p.uniform, p.indexed_digest, p.generate_schedule, p.fault_inputs, p.guess_input):
            self.assertNotIn("digest", inspect.signature(fn).parameters)
            self.assertNotIn("callback", inspect.signature(fn).parameters)
        root = Path(__file__).resolve().parent
        digest = hashlib.sha256((root / "E3_DESIGN_FREEZE_v0_11.json").read_bytes()).hexdigest()
        self.assertEqual(digest, "3678d797dc17485fcc823cb7f83696e4ba20c9a69921d709291cad50c3f878d4")
        result = verify(root)
        self.assertTrue(result["ok"], result)
        self.assertEqual((result["file_count"], result["files_checked"]), (23, 23))


if __name__ == "__main__":
    unittest.main()