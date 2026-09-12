"""Deterministic engineering-only physical component checks, not paid traces.

Run with Python -B -m unittest test_e3_physical. No random generator, final
target, hypothesis experiment, environment package, or stochastic fixture.
Independent byte/bit oracles compare exact original and final state images.
"""

import gc
import unittest
from collections import Counter, deque
from dataclasses import FrozenInstanceError, fields
from fractions import Fraction
from typing import cast

from e3 import physical as p
from e3.state import State


BAD_INTS: tuple[object, ...] = (True, False, 1.0, float("nan"), "1", None)


def bits(raw: bytes | bytearray, offset: int, width: int) -> int:
    return sum(((raw[(offset + i) // 8] >> ((offset + i) % 8)) & 1) << i
               for i in range(width))


def put(raw: bytearray, offset: int, width: int, value: int) -> None:
    for i in range(width):
        bit = offset + i
        raw[bit // 8] = (raw[bit // 8] & ~(1 << (bit % 8))) | (((value >> i) & 1) << (bit % 8))


def reference_domain(lane: int) -> int:
    if lane < 80:
        return 5 * (lane // 20)
    hub = lane % 4
    if lane < 848:
        ordered = list(range(80 + hub, 848, 4))
        return 5 * hub + 1 + ordered.index(lane) // 64
    return 5 * hub + 4


def reference_faults(raw: bytes, draws: tuple[int, ...]) -> bytes:
    """Independent byte-level physics; never use production maps or codecs."""
    result = bytearray(raw)
    if bits(raw, 1800, 16) == 0:
        return raw
    position = 0
    for lane in range(1104):
        if 900 <= lane < 924:
            continue
        domain = reference_domain(lane)
        age = bits(raw, 1848 + 4 * domain, 4)
        old = bits(raw, lane * 2, 2)
        if lane < 80:
            new = 1 - old if old in (0, 1) and draws[position] < 10 * (age + 1) else old
            if draws[position + 1] < age:
                new = 2
            position += 2
        else:
            low = (old & 1) ^ (draws[position] < 10 * (age + 1))
            high = (old >> 1) ^ (draws[position + 1] < 10 * (age + 1))
            new = low + 2 * high
            if draws[position + 2] < age:
                new = 0
            position += 3
        put(result, lane * 2, 2, new)
    put(result, 1800, 16, bits(raw, 1800, 16) - 1)
    for hub in range(4):
        stock = bits(raw, 1816 + 8 * hub, 8)
        put(result, 1816 + 8 * hub, 8, max(0, stock - 1))
    return bytes(result)


def body_fixture(energy: int = 201, ages: int | None = None) -> State:
    raw = bytearray((index * 73 + 19) % 256 for index in range(276))
    put(raw, 1800, 16, energy)
    for hub, stock in enumerate((0, 1, 129, 255)):
        put(raw, 1816 + 8 * hub, 8, stock)
    for domain in range(20):
        put(raw, 1848 + domain * 4, 4, (domain * 7) % 16 if ages is None else ages)
    return State(raw)


class TestE3Physical(unittest.TestCase):
    def assert_ledger(self, old: bytes, new: bytes, ledger: p.LossLedger) -> None:
        code = auxiliary = changed_bits = 0
        for lane in range(1104):
            if 900 <= lane < 924:
                continue
            old_lane = bits(old, lane * 2, 2)
            new_lane = bits(new, lane * 2, 2)
            if old_lane != new_lane:
                code += int(lane < 80)
                auxiliary += int(lane >= 80)
            changed_bits += sum(bits(old, 2 * lane + bit, 1) != bits(new, 2 * lane + bit, 1)
                                for bit in range(2))
        self.assertEqual(ledger.changed_code_lanes, code)
        self.assertEqual(ledger.changed_aux_lanes, auxiliary)
        self.assertEqual(ledger.changed_lanes, code + auxiliary)
        self.assertEqual(ledger.changed_bits, changed_bits)
        self.assertEqual(ledger.energy_loss, bits(old, 1800, 16) - bits(new, 1800, 16))
        self.assertEqual(ledger.material_loss, tuple(
            bits(old, 1816 + 8 * hub, 8) - bits(new, 1816 + 8 * hub, 8) for hub in range(4)))
        self.assertEqual(ledger.energy_delta, -ledger.energy_loss)
        self.assertEqual(ledger.material_delta, tuple(-loss for loss in ledger.material_loss))

    def test_01_fixed_tree_and_all_routes(self) -> None:
        config = p.PhysicalConfig()
        self.assertEqual((config.hub_count, config.domain_count, config.vertex_count,
                          config.diameter, config.lane_count, config.ram_lane_count),
                         (4, 20, 25, 4, 1104, 1080))
        self.assertEqual(len(config.edges), 24)
        adjacency: dict[int, list[int]] = {vertex: [] for vertex in range(25)}
        for a, b in config.edges:
            adjacency[a].append(b)
            adjacency[b].append(a)
        distances: dict[int, dict[int, int]] = {}
        for source in range(25):
            distance = {source: 0}
            queue = deque([source])
            while queue:
                current = queue.popleft()
                for neighbor in adjacency[current]:
                    if neighbor not in distance:
                        distance[neighbor] = distance[current] + 1
                        queue.append(neighbor)
            self.assertEqual(len(distance), 25)
            distances[source] = distance
        self.assertEqual(max(max(row.values()) for row in distances.values()), 4)
        for row in config.lane_rows:
            vertex = config.lane_to_vertex[row.lane]
            self.assertEqual(row.read_route, distances[0][vertex])
            self.assertEqual(row.write_route, row.read_route)
            if row.flags != p.TYPED_RESERVOIR:
                self.assertEqual(row.material_route, distances[1 + row.hub][vertex])
        for block in range(4):
            for layer in range(5):
                for bit in range(4):
                    lane = 20 * block + 4 * layer + bit
                    self.assertEqual(config.lane_to_vertex[lane], 5 + 5 * block + layer)

    def test_02_all_lane_domains_and_source_assignments(self) -> None:
        config = p.PhysicalConfig()
        self.assertEqual(len(config.lane_rows), 1104)
        self.assertEqual(tuple(row.lane for row in config.lane_rows), tuple(range(1104)))
        self.assertEqual(len(set(config.ram_lanes)), 1080)
        self.assertEqual(config.ram_lanes, tuple(lane for lane in range(1104) if not 900 <= lane < 924))
        self.assertEqual(Counter(row.flags for row in config.lane_rows), {0: 948, 1: 132, 2: 24})
        self.assertEqual(Counter(config.lane_to_hub[lane] for lane in config.ram_lanes),
                         {hub: 270 for hub in range(4)})
        for lane in config.ram_lanes:
            row = config.lane_rows[lane]
            hub = lane // 20 if lane < 80 else lane % 4
            self.assertEqual((row.hub, row.domain), (hub, reference_domain(lane)))
            self.assertEqual(config.lane_to_domain[lane], row.domain)
            self.assertEqual(config.material_source[lane], hub)
            self.assertEqual(config.lane_distance[lane], 2 if lane < 80 else 1)
            self.assertEqual(config.material_hops[lane], 1 if lane < 80 else 0)
            self.assertIs(config.lane_is_code[lane], lane < 80)
        domains = Counter(config.lane_to_domain[lane] for lane in config.ram_lanes)
        for hub in range(4):
            self.assertEqual(tuple(domains[5 * hub + k] for k in range(5)), (20, 64, 64, 64, 58))

    def test_03_every_auxiliary_field_has_exact_source_balance(self) -> None:
        config = p.PhysicalConfig()
        for start, stop, per_source in ((80, 848, 192), (848, 868, 5),
                                        (868, 884, 4), (884, 900, 4),
                                        (924, 964, 10), (964, 972, 2), (972, 1104, 33)):
            self.assertEqual(Counter(config.lane_to_hub[lane] for lane in range(start, stop)),
                             {hub: per_source for hub in range(4)})
        for hub in range(4):
            self.assertEqual(sum(row.hub == hub and row.flags == 0 and row.lane >= 80
                                 for row in config.lane_rows), 217)

    def test_04_typed_resource_rows_cannot_authorize_ram_access(self) -> None:
        config = p.PhysicalConfig()
        for lane in range(900, 924):
            row = config.lane_rows[lane]
            hub = 255 if lane < 908 else (lane - 908) // 4
            self.assertEqual((row.hub, row.domain, row.flags), (hub, 4 if hub == 255 else 5 * hub + 4, 2))
            self.assertIsNone(config.material_source[lane])
            for function in (p.lane_read_cost, p.lane_write_cost, p.fault_slot_indices):
                with self.assertRaises(PermissionError):
                    function(lane)
            with self.assertRaises(PermissionError):
                p.write_quote((0, lane))
        for lane in range(972, 1104):
            for function in (p.lane_read_cost, p.lane_write_cost):
                with self.assertRaises(PermissionError):
                    function(lane)
            self.assertEqual(len(p.fault_slot_indices(lane)), 3)

    def test_05_config_is_inherited_immutable_and_contains_no_state(self) -> None:
        left, right = p.PhysicalConfig(), p.PhysicalConfig()
        self.assertEqual(fields(left), ())
        self.assertFalse(hasattr(left, "__dict__"))
        self.assertEqual(p.PhysicalConfig.__slots__, ())
        for name in ("edges", "lane_rows", "domain_rows", "ram_lanes", "lane_to_hub",
                     "lane_to_domain", "material_source", "lane_distance", "material_hops",
                     "lane_is_code", "lane_to_vertex"):
            self.assertIs(getattr(left, name), getattr(right, name))
            self.assertIs(type(getattr(left, name)), tuple)
            with self.assertRaises((AttributeError, TypeError)):
                setattr(left, name, ())
        with self.assertRaises(FrozenInstanceError):
            setattr(left.lane_rows[0], "hub", 3)
        with self.assertRaises(TypeError):
            p.PhysicalConfig(cast(int, 1))  # type: ignore[call-arg]
        self.assertEqual(gc.get_referents(left), [p.PhysicalConfig])

    def test_06_read_write_quotes_and_repeated_addresses(self) -> None:
        self.assertEqual((p.lane_read_cost(0), p.lane_write_cost(0)), (17, 23))
        self.assertEqual((p.lane_read_cost(80), p.lane_write_cost(80)), (10, 14))
        for hub in range(4):
            quote = p.write_quote(tuple(range(20 * hub, 20 * hub + 20)))
            self.assertEqual(quote.energy, 460)
            self.assertEqual(quote.material, tuple(20 if j == hub else 0 for j in range(4)))
        quote = p.write_quote([0, 0, 20, 80, 81, 82, 83])
        self.assertEqual(quote.components, (3 * 23 + 4 * 14, 3, 2, 1, 1))
        self.assertEqual(p.write_quote(tuple(range(80, 88))).components, (112, 2, 2, 2, 2))
        self.assertEqual(p.write_quote(()).components, (0, 0, 0, 0, 0))
        self.assertEqual(p.write_quote([0] * 1104).components, (25392, 1104, 0, 0, 0))
        with self.assertRaises(ValueError):
            p.write_quote([0] * 1105)

    def test_07_age_storage_domains_and_low_level_codecs(self) -> None:
        config = p.PhysicalConfig()
        self.assertEqual(len(config.domain_rows), 20)
        body = body_fixture()
        for domain in range(20):
            low, high = p.age_lanes(domain)
            self.assertEqual((low, high), (924 + 2 * domain, 925 + 2 * domain))
            row = config.domain_rows[domain]
            self.assertEqual((row.domain, row.hub, row.low_age_lane, row.high_age_lane),
                             (domain, domain // 5, low, high))
            for lane in (low, high):
                self.assertEqual(config.lane_to_domain[lane], 5 * (lane % 4) + 4)
            for age in range(16):
                expected = bytearray(body.snapshot())
                put(expected, 1848 + 4 * domain, 4, age)
                p.write_age(body, domain, age)
                self.assertEqual(body.snapshot(), bytes(expected))
                self.assertEqual(p.read_age(body, domain), age)
        # Codec construction is permitted at E=0, not a free paid upkeep pass.
        blank = State()
        p.write_age(blank, 19, 15)
        self.assertEqual(blank.energy, 0)
        self.assertEqual(p.read_age(blank, 19), 15)

    def test_08_conditioning_vectors_and_age_source_totals(self) -> None:
        full = [0, 0, 0, 0]
        for domain in range(20):
            vector = p.conditioning_vector(domain)
            expected = [0, 0, 0, 0]
            for hub in (domain // 5, (924 + 2 * domain) % 4, (925 + 2 * domain) % 4):
                expected[hub] += 1
            self.assertEqual(vector, tuple(expected))
            self.assertEqual(sum(vector), 3)
            self.assertEqual(p.conditioning_quote(domain).components, (32, *expected))
            full = [total + value for total, value in zip(full, vector)]
        self.assertEqual(full, [15] * 4)
        self.assertEqual(p.conditioning_vector(0), (2, 1, 0, 0))
        self.assertEqual(p.conditioning_vector(1), (1, 0, 1, 1))
        self.assertEqual(p.conditioning_vector(5), (0, 1, 1, 1))
        for start in (924, 944):
            self.assertEqual(p.write_quote(tuple(range(start, start + 20))).material, (5,) * 4)
        ages = p.write_quote(tuple(range(924, 964)))
        self.assertEqual(ages.material, (10,) * 4)
        self.assertEqual(tuple(a + b for a, b in zip(ages.material, full)), (25,) * 4)
        self.assertEqual(2 * (392 + 20 * 10 + 20 * 14 + 80) + 20 * (520 + 32), 12944)
        # Arithmetic only: no claim that AGE or CONDITION was executed/paid.

    def test_09_exact_hazard_counts_all_sixteen_ages(self) -> None:
        for age in range(16):
            flip, erase = p.fault_thresholds(age)
            self.assertEqual(Fraction(sum(u < flip for u in range(10000)), 10000), Fraction(age + 1, 1000))
            self.assertEqual(Fraction(sum(u < erase for u in range(10000)), 10000), Fraction(age, 10000))
        self.assertEqual(p.fault_thresholds(0), (10, 0))
        self.assertEqual(p.fault_thresholds(15), (160, 15))

    def test_10_fault_frame_shape_clone_and_every_slot(self) -> None:
        mutable = [9999] * 3160
        frame = p.FaultFrame(cast(tuple[int, ...], mutable))
        mutable[0] = 0
        self.assertEqual((len(frame), len(frame.draws), frame[0], frame[3159]), (3160, 3160, 9999, 9999))
        self.assertIs(type(frame.draws), tuple)
        self.assertFalse(hasattr(frame, "__dict__"))
        with self.assertRaises(FrozenInstanceError):
            setattr(frame, "draws", ())
        self.assertEqual(len(p.FAULT_SLOTS), 3160)
        self.assertEqual(len(set(p.FAULT_SLOTS)), 3160)
        expected: list[tuple[int, str]] = []
        for lane in range(1104):
            if 900 <= lane < 924:
                continue
            purposes = ("code_flip", "code_erase") if lane < 80 else ("aux_bit0", "aux_bit1", "aux_erase")
            start = len(expected)
            expected.extend((lane, purpose) for purpose in purposes)
            self.assertEqual(p.fault_slot_indices(lane), tuple(range(start, len(expected))))
        self.assertEqual(p.FAULT_SLOTS, tuple(expected))
        self.assertEqual(p.fault_slot_indices(79), (158, 159))
        self.assertEqual(p.fault_slot_indices(80), (160, 161, 162))
        self.assertEqual(p.fault_slot_indices(924), (2620, 2621, 2622))
        self.assertEqual(p.fault_slot_indices(1103), (3157, 3158, 3159))

    def test_11_no_fault_extreme_still_has_typed_leakage(self) -> None:
        body = body_fixture()
        before = body.snapshot()
        ledger = p.apply_faults(body, p.FaultFrame((9999,) * 3160))
        self.assertEqual(body.snapshot(), reference_faults(before, (9999,) * 3160))
        self.assertEqual(ledger, p.LossLedger(1, (0, 1, 1, 1)))
        self.assertEqual(before[:225], body.snapshot()[:225])
        self.assertEqual(before[231:], body.snapshot()[231:])
        self.assert_ledger(before, body.snapshot(), ledger)

    def test_12_all_zero_draws_at_age_zero_preserve_empty_invalid_code(self) -> None:
        body = body_fixture(ages=0)
        for lane in range(80):
            body.write_lane(lane, lane % 4)
        before = body.snapshot()
        ledger = p.apply_faults(body, p.FaultFrame((0,) * 3160))
        self.assertEqual(body.snapshot(), reference_faults(before, (0,) * 3160))
        for lane in range(80):
            self.assertEqual(body.read_lane(lane), (1, 0, 2, 3)[lane % 4])
        self.assertEqual(ledger.changed_code_lanes, 40)
        self.assertEqual(ledger.changed_aux_lanes, 1000)
        self.assertEqual(ledger.changed_bits, 2040)
        self.assertEqual(tuple(p.read_age(body, d) for d in range(20)), (15,) * 20)
        self.assertEqual(body.snapshot()[243:], bytes(byte ^ 255 for byte in before[243:]))
        self.assert_ledger(before, body.snapshot(), ledger)

    def test_13_erasure_overrides_all_code_and_auxiliary_flips(self) -> None:
        body = body_fixture(ages=15)
        for lane in range(80):
            body.write_lane(lane, lane % 4)
        before = body.snapshot()
        ledger = p.apply_faults(body, p.FaultFrame((0,) * 3160))
        self.assertEqual(body.snapshot(), reference_faults(before, (0,) * 3160))
        self.assertEqual(body.snapshot()[:20], b"\xaa" * 20)
        self.assertEqual(body.snapshot()[20:225], bytes(205))
        self.assertEqual(body.snapshot()[231:], bytes(45))
        self.assertEqual(ledger.changed_code_lanes, 60)  # Already erased sites do not change.
        self.assert_ledger(before, body.snapshot(), ledger)

    def test_14_independent_auxiliary_bit_and_erasure_purposes(self) -> None:
        for bit in (0, 1):
            body = body_fixture(ages=0)
            body.write_lane(80, 0)
            draws = [9999] * 3160
            draws[160 + bit] = 0
            before = body.snapshot()
            ledger = p.apply_faults(body, p.FaultFrame(tuple(draws)))
            self.assertEqual(body.read_lane(80), 1 << bit)
            self.assertEqual(ledger.changed_bits, 1)
            self.assertEqual(ledger.changed_aux_lanes, 1)
            self.assert_ledger(before, body.snapshot(), ledger)

    def test_15_exact_boundaries_executed_for_all_ages(self) -> None:
        for age in range(16):
            for below in (False, True):
                body = body_fixture(ages=age)
                body.write_lane(0, 0)
                body.write_lane(80, 0)
                body.write_lane(81, 3)
                draws = [9999] * 3160
                draws[0] = 10 * (age + 1) - int(below)
                draws[160] = 10 * (age + 1) - int(below)
                draws[165] = max(0, age - int(below))  # Lane 81 erasure slot.
                before = body.snapshot()
                ledger = p.apply_faults(body, p.FaultFrame(tuple(draws)))
                self.assertEqual(body.read_lane(0), int(below))
                self.assertEqual(body.read_lane(80), int(below))
                self.assertEqual(body.read_lane(81), 0 if below and age else 3)
                self.assertEqual(body.snapshot(), reference_faults(before, tuple(draws)))
                self.assert_ledger(before, body.snapshot(), ledger)

    def test_16_faults_use_one_prestate_even_when_ages_change_early(self) -> None:
        # All age bits flip at old age 0. Later reserve draws=10 must NOT use
        # the newly corrupted ages (15), which would wrongly flip the reserve.
        body = body_fixture(ages=0)
        draws = [9999] * 3160
        for lane in range(924, 964):
            start = 2620 + 3 * (lane - 924)
            draws[start] = draws[start + 1] = 0
        for lane in range(972, 1104):
            start = 2620 + 3 * (lane - 924)
            draws[start] = draws[start + 1] = 10
        before = body.snapshot()
        ledger = p.apply_faults(body, p.FaultFrame(tuple(draws)))
        self.assertEqual(body.snapshot(), reference_faults(before, tuple(draws)))
        self.assertEqual(body.snapshot()[243:], before[243:])
        self.assertEqual(tuple(p.read_age(body, d) for d in range(20)), (15,) * 20)
        self.assert_ledger(before, body.snapshot(), ledger)
        # The next physical step must use those actual now-stored ages.
        before = body.snapshot()
        next_draws = [9999] * 3160
        next_draws[3157] = 10
        ledger = p.apply_faults(body, p.FaultFrame(tuple(next_draws)))
        self.assertEqual(body.snapshot(), reference_faults(before, tuple(next_draws)))
        self.assertEqual(bits(body.snapshot(), 2206, 2), bits(before, 2206, 2) ^ 1)
        self.assert_ledger(before, body.snapshot(), ledger)

    def test_17_nonuniform_prestate_ages_all_lanes_reference(self) -> None:
        for pattern in range(8):
            body = body_fixture()
            boundary = (0, 9, 10, 14, 15, 19, 20, 29, 30, 149, 150, 159, 160, 9999)
            draws = tuple(boundary[(slot * 5 + pattern) % len(boundary)] for slot in range(3160))
            before = body.snapshot()
            ledger = p.apply_faults(body, p.FaultFrame(draws))
            self.assertEqual(body.snapshot(), reference_faults(before, draws))
            self.assert_ledger(before, body.snapshot(), ledger)

    def test_18_age_faults_follow_storage_domain_not_described_domain(self) -> None:
        body = body_fixture(ages=0)
        p.write_age(body, 0, 15)  # Described code-domain age is old 15.
        p.write_age(body, 4, 0)  # Storage domains B0/B1 both remain old 0.
        p.write_age(body, 9, 0)
        draws = [9999] * 3160
        draws[2620] = draws[2623] = 10
        before = body.snapshot()
        ledger = p.apply_faults(body, p.FaultFrame(tuple(draws)))
        self.assertEqual(p.read_age(body, 0), 15)
        self.assertEqual(ledger.changed_lanes, 0)
        self.assertEqual(body.snapshot(), reference_faults(before, tuple(draws)))

    def test_19_frame_validation_is_complete_before_any_state_write(self) -> None:
        body = body_fixture(ages=15)
        original = body.snapshot()
        for bad in (*BAD_INTS, -1, 10000, 1 << 100):
            draws = [0] * 3160
            draws[-1] = cast(int, bad)
            with self.assertRaises((TypeError, ValueError)):
                p.apply_faults(body, p.FaultFrame(tuple(draws)))
            self.assertEqual(body.snapshot(), original)
            # Deliberate host corruption is still rejected before mutation.
            frame = p.FaultFrame((0,) * 3160)
            object.__setattr__(frame, "draws", tuple(draws))
            with self.assertRaises((TypeError, ValueError)):
                p.apply_faults(body, frame)
            self.assertEqual(body.snapshot(), original)
        for length in (0, 1, 3159, 3161):
            with self.assertRaises(ValueError):
                p.FaultFrame((0,) * length)
        for bad_frame in (None, b"\0" * 3160, "0" * 3160, [0] * 3160, object()):
            with self.assertRaises(TypeError):
                p.apply_faults(body, cast(p.FaultFrame, bad_frame))
            self.assertEqual(body.snapshot(), original)
        for bad_draws in (None, b"\0" * 3160, "0" * 3160, iter([0] * 3160)):
            with self.assertRaises(TypeError):
                p.FaultFrame(cast(tuple[int, ...], bad_draws))

    def test_20_dead_states_are_absorbing_and_final_leak_has_no_late_writes(self) -> None:
        frame = p.FaultFrame((0,) * 3160)
        for energy in (0, 1):
            body = body_fixture(energy=energy, ages=15)
            before = body.snapshot()
            ledger = p.apply_faults(body, frame)
            self.assertEqual(body.energy, 0)
            self.assertEqual(body.snapshot(), reference_faults(before, frame.draws))
            self.assert_ledger(before, body.snapshot(), ledger)
            after = body.snapshot()
            for transition in (lambda: p.apply_faults(body, frame),
                               lambda: p.apply_primary_lesion(body),
                               lambda: p.apply_hub_lesion(body, 2),
                               lambda: p.apply_global_resource_injury(body)):
                self.assertEqual(transition(), p.LossLedger())
                self.assertEqual(body.snapshot(), after)
        # Corrupt diagnostic flags are not a survival switch.
        body = body_fixture(energy=2, ages=0)
        body.write_bits(1941, 3, 7)
        ledger = p.apply_faults(body, p.FaultFrame((9999,) * 3160))
        self.assertEqual(body.energy, 1)
        self.assertEqual(body.read_bits(1941, 3), 7)
        self.assertEqual(ledger.energy_loss, 1)

    def test_21_primary_lesion_exact_layers_all_blocks(self) -> None:
        body = body_fixture()
        for lane in range(80):
            body.write_lane(lane, lane % 2)
        before = body.snapshot()
        expected = bytearray(before)
        for block in range(4):
            for position in range(12, 20):
                put(expected, 2 * (20 * block + position), 2, 2)
        ledger = p.apply_primary_lesion(body)
        self.assertEqual(body.snapshot(), bytes(expected))
        self.assertEqual(ledger.changed_code_lanes, 32)
        self.assertEqual((ledger.energy_loss, ledger.material_loss), (0, (0,) * 4))
        self.assert_ledger(before, body.snapshot(), ledger)
        self.assertEqual(p.apply_primary_lesion(body), p.LossLedger())

    def test_22_hub_lesion_clears_270_sites_including_33_reserve(self) -> None:
        for hub in range(4):
            raw = bytearray(b"\xff" * 276)
            put(raw, 1800, 16, 201)
            body = State(raw)
            before = body.snapshot()
            expected = bytearray(before)
            for lane in range(1104):
                if 900 <= lane < 924:
                    continue
                owner = lane // 20 if lane < 80 else lane % 4
                if owner == hub:
                    put(expected, 2 * lane, 2, 2 if lane < 80 else 0)
            put(expected, 1800, 16, 101)
            put(expected, 1816 + 8 * hub, 8, 0)
            ledger = p.apply_hub_lesion(body, hub)
            self.assertEqual(body.snapshot(), bytes(expected))
            self.assertEqual((ledger.changed_code_lanes, ledger.changed_aux_lanes), (20, 250))
            self.assertEqual(sum(bits(before, 2 * lane, 2) != bits(body.snapshot(), 2 * lane, 2)
                                 for lane in range(972, 1104)), 33)
            self.assertEqual(ledger.energy_loss, 100)
            self.assert_ledger(before, body.snapshot(), ledger)

    def test_23_global_injury_floor_sinks_never_modify_ram(self) -> None:
        for energy in (1, 2, 3, 65535):
            body = body_fixture(energy=energy)
            before = body.snapshot()
            expected = bytearray(before)
            put(expected, 1800, 16, energy - energy // 2)
            for hub in range(4):
                stock = bits(before, 1816 + 8 * hub, 8)
                put(expected, 1816 + 8 * hub, 8, stock - stock // 2)
            ledger = p.apply_global_resource_injury(body)
            self.assertEqual(body.snapshot(), bytes(expected))
            self.assertEqual(ledger.changed_lanes, 0)
            self.assertEqual(ledger.material_loss, (0, 0, 64, 127))
            self.assert_ledger(before, body.snapshot(), ledger)

    def test_24_strict_integer_arguments_and_invalid_calls_are_atomic(self) -> None:
        body = body_fixture()
        before = body.snapshot()
        for bad in BAD_INTS:
            number = cast(int, bad)
            for action in (lambda: p.lane_read_cost(number), lambda: p.lane_write_cost(number),
                           lambda: p.age_lanes(number), lambda: p.read_age(body, number),
                           lambda: p.write_age(body, number, 0), lambda: p.write_age(body, 0, number),
                           lambda: p.fault_thresholds(number), lambda: p.conditioning_vector(number),
                           lambda: p.conditioning_quote(number), lambda: p.apply_hub_lesion(body, number),
                           lambda: p.fault_slot_indices(number), lambda: p.write_quote([number]),
                           lambda: p.FaultFrame((0,) * 3160)[number]):
                with self.assertRaises(TypeError):
                    action()
                self.assertEqual(body.snapshot(), before)
        for domain in (-1, 20):
            for action in (lambda: p.read_age(body, domain), lambda: p.write_age(body, domain, 0),
                           lambda: p.conditioning_quote(domain)):
                with self.assertRaises(ValueError):
                    action()
        for age in (-1, 16):
            with self.assertRaises(ValueError):
                p.write_age(body, 0, age)
            with self.assertRaises(ValueError):
                p.fault_thresholds(age)
        for lane in (-1, 1104):
            with self.assertRaises(ValueError):
                p.lane_read_cost(lane)
            with self.assertRaises(ValueError):
                p.fault_slot_indices(lane)
        for hub in (-1, 4):
            with self.assertRaises(ValueError):
                p.apply_hub_lesion(body, hub)
        with self.assertRaises(TypeError):
            p.apply_faults(cast(State, before), p.FaultFrame((0,) * 3160))
        with self.assertRaises(TypeError):
            p.apply_faults(body, p.FaultFrame((0,) * 3160), cast(p.PhysicalConfig, None))
        with self.assertRaises(TypeError):
            p.write_quote(cast(tuple[int, ...], iter([0])))
        self.assertEqual(body.snapshot(), before)

    def test_25_no_snapshots_or_worker_state_retained_by_results(self) -> None:
        body = body_fixture()
        frame = p.FaultFrame((0,) * 3160)
        result = p.apply_faults(body, frame)
        self.assertFalse(hasattr(result, "__dict__"))
        self.assertEqual(tuple(field.name for field in fields(result)),
                         ("energy_loss", "material_loss", "changed_code_lanes", "changed_aux_lanes", "changed_bits"))
        self.assertNotIn(body, gc.get_referents(result))
        self.assertNotIn(frame, gc.get_referents(result))
        self.assertEqual(len(body.snapshot()), 276)
        self.assertEqual(len(gc.get_referents(body)), 2)
        self.assertFalse(any(isinstance(value, (State, bytearray, p.FaultFrame, p.LossLedger))
                             for value in vars(p).values()))
        with self.assertRaises(FrozenInstanceError):
            setattr(result, "energy_loss", 0)


if __name__ == "__main__":
    unittest.main()