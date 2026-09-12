"""Isolated E3 meter fixtures; no worker, target draws, E3 seeds or file output.

Run with Python -B -m unittest test_e3_meter. Audit lists below belong only to
the observer fixture and are never passed back to meter functions or State.
Static tariffs and AN-001 are specification witnesses, not full VM traces.
"""

import gc
import operator
import unittest
from dataclasses import FrozenInstanceError
from typing import cast
from unittest.mock import patch

from e3 import meter
from e3.meter import (
    Bound, Cost, DepositResult, FEE, INT32_MAX, InsufficientResources,
    Material4, ZERO, add_cost, canonical_activation, debit, debit_and_deposit,
    deposit, floor_quote, gate, passive_grant, require_cost, sub_cost,
)
from e3.state import ENERGY_BYTE, MATERIAL_BYTE, STATE_BYTES, State


BAD_INTS: tuple[object, ...] = (True, False, 1.0, "1", None, float("nan"))


def four(value: int) -> Material4:
    return value, value, value, value


def stocks(state: State) -> tuple[int, int, int, int, int]:
    return state.energy, state.P0, state.P1, state.P2, state.P3


def resource_image(raw: bytes, energy: int, material: Material4) -> bytes:
    """Independent byte-level oracle, not a meter or field-codec call."""
    result = bytearray(raw)
    result[ENERGY_BYTE:MATERIAL_BYTE] = energy.to_bytes(2, "little")
    result[MATERIAL_BYTE:MATERIAL_BYTE + 4] = bytes(material)
    return bytes(result)


def fixture(energy: int = 10000, material: Material4 = (20, 20, 20, 20)) -> State:
    raw = bytes((i * 37 + 19) % 256 for i in range(STATE_BYTES))
    return State(resource_image(raw, energy, material))


class TestCost(unittest.TestCase):
    def test_immutable_energy_and_four_source_tuple(self) -> None:
        c = Cost(4, (1, 2, 3, 4))
        self.assertIs(Bound, Cost)
        self.assertFalse(hasattr(c, "__dict__"))
        self.assertEqual(hash(c), hash(Cost(4, (1, 2, 3, 4))))
        with self.assertRaises(FrozenInstanceError):
            setattr(c, "energy", 7)
        with self.assertRaises(TypeError):
            operator.setitem(cast(list[int], c.material), 0, 7)

    def test_strict_numeric_inputs_in_all_components(self) -> None:
        for bad in BAD_INTS:
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    Cost(cast(int, bad))
                with self.assertRaises(TypeError):
                    Cost(0, (0, 0, 0, cast(int, bad)))
        for bad, exception in ((-1, ValueError), (INT32_MAX + 1, OverflowError),
                               (1 << 1000, OverflowError)):
            with self.assertRaises(exception):
                Cost(bad)
            with self.assertRaises(exception):
                Cost(0, (0, bad, 0, 0))
        for bad in ([0, 0, 0, 0], (0,) * 3, (0,) * 5, None):
            with self.assertRaises((TypeError, ValueError)):
                Cost(0, cast(Material4, bad))

    def test_checked_vector_arithmetic(self) -> None:
        a, b = Cost(10, (2, 3, 4, 5)), Cost(20, (1, 1, 1, 1))
        self.assertEqual(add_cost(a, b), Cost(30, (3, 4, 5, 6)))
        self.assertEqual(sub_cost(add_cost(a, b), b), a)
        self.assertEqual(add_cost(Cost(INT32_MAX), ZERO), Cost(INT32_MAX))
        with self.assertRaises(OverflowError):
            add_cost(Cost(INT32_MAX), Cost(1))
        with self.assertRaises(OverflowError):
            add_cost(Cost(0, (INT32_MAX, 0, 0, 0)), Cost(0, (1, 0, 0, 0)))
        with self.assertRaises(ValueError):
            sub_cost(ZERO, Cost(1))
        with self.assertRaises(ValueError):
            sub_cost(Cost(1, (9, 0, 0, 0)), Cost(1, (0, 1, 0, 0)))
        with self.assertRaises(TypeError):
            add_cost(cast(Cost, (1, 0, 0, 0, 0)), ZERO)

    def test_floor_quote_is_ephemeral_and_checks_sums(self) -> None:
        self.assertEqual(floor_quote(Cost(10), Cost(20), Cost(30)), Cost(61))
        self.assertEqual(floor_quote(Cost(10), residue=3), Cost(13))
        with self.assertRaises(OverflowError):
            floor_quote(Cost(INT32_MAX))
        with self.assertRaises(OverflowError):
            floor_quote(ZERO, Cost(0, (0, 0, INT32_MAX, 0)), Cost(0, (0, 0, 1, 0)))
        for bad in (0, -1, True, 1.0):
            with self.assertRaises((TypeError, ValueError)):
                floor_quote(ZERO, residue=cast(int, bad))


class TestAdmissionAndDebit(unittest.TestCase):
    def test_source_equality_and_energy_plus_one(self) -> None:
        s = fixture(11, (1, 2, 3, 4))
        c = Cost(10, (1, 2, 3, 4))
        before = s.snapshot()
        self.assertTrue(require_cost(s, c))
        self.assertEqual(s.snapshot(), before)
        s.energy = 10
        self.assertFalse(require_cost(s, c))
        before = s.snapshot()
        with self.assertRaises(InsufficientResources):
            debit(s, c)
        self.assertEqual(s.snapshot(), before)
        s.energy = 11
        self.assertEqual(debit(s, c), c)
        self.assertEqual(stocks(s), (1, 0, 0, 0, 0))

    def test_source_shortage_does_not_borrow_other_pools(self) -> None:
        for j in range(4):
            s = fixture(1000, (255, 255, 255, 255))
            s.write_material(j, 0)
            c = Cost(23, cast(Material4, tuple(int(k == j) for k in range(4))))
            before = s.snapshot()
            self.assertFalse(require_cost(s, c))
            with self.assertRaises(InsufficientResources):
                debit(s, c)
            self.assertEqual(s.snapshot(), before)

    def test_gate_fee_is_paid_before_optional_body_comparison(self) -> None:
        c, local, tail = Cost(10), Cost(8), Cost(20)
        # Before fee the body fits; after fee it is short by exactly one.
        s = fixture(166)
        result = gate(s, c, local, tail)
        self.assertEqual(result, (True, False, 0))
        self.assertEqual(result.status, "rejected")
        self.assertEqual(s.energy, 38)
        debit(s, local, public_tail=tail)
        self.assertEqual(s.energy, 30)
        s = fixture(167)
        result = gate(s, c, local, tail)
        self.assertTrue(result.enough)
        self.assertEqual(s.energy, 39)
        debit(s, c, local, tail)
        debit(s, local, public_tail=tail)
        debit(s, tail)
        self.assertEqual(s.energy, 1)

    def test_nested_gate_floor_fee_cleanup_and_no_implicit_clear(self) -> None:
        s = fixture(129)
        before = s.snapshot()
        self.assertEqual(gate(s, Cost(1)), (True, False, 0))
        self.assertEqual(s.snapshot(), resource_image(before, 1, four(20)))
        s = fixture(130)
        before = s.snapshot()
        self.assertEqual(gate(s, Cost(2), Cost(1)), (True, False, 0))
        self.assertEqual(s.energy, 2)
        debit(s, Cost(1))  # Caller owns the one-energy minimal cleanup fixture.
        self.assertEqual(s.snapshot(), resource_image(before, 1, four(20)))

    def test_minimum_failure_is_only_energy_sink_not_fee_or_flag_write(self) -> None:
        for energy, material in ((0, four(20)), (128, four(20)),
                     (136, four(20)), (500, four(0))):
            s = fixture(energy, material)
            before = s.snapshot()
            result = gate(s, ZERO, Cost(8, (1, 0, 0, 0)))
            self.assertEqual(result, (False, False, energy))
            self.assertEqual(result.status, "shutdown")
            self.assertEqual(s.snapshot(), resource_image(before, 0, material))
            self.assertEqual(gate(s, ZERO).shutdown_loss, 0)

    def test_minimum_exit_and_body_remainder_are_distinct(self) -> None:
        s = fixture(137)
        result = gate(s, ZERO, Cost(264), minimum_exit=Cost(8))
        self.assertEqual(result, (True, False, 0))
        self.assertEqual(s.energy, 9)
        debit(s, Cost(8))  # Rejected ordinary operation runs S only, not CONTROL.
        self.assertEqual(s.energy, 1)

    def test_rejected_optional_material_body_only_pays_fee(self) -> None:
        s = fixture(1000, (4, 4, 4, 4))
        before = s.snapshot()
        result = gate(s, Cost(217, four(2)), Cost(232, four(4)))
        self.assertEqual(result, (True, False, 0))
        self.assertEqual(s.snapshot(), resource_image(before, 872, four(4)))
        debit(s, Cost(232, four(4)))
        self.assertEqual(stocks(s), (640, 0, 0, 0, 0))

    def test_malformed_cost_or_overflow_never_mutates_or_means_death(self) -> None:
        s = fixture()
        before = s.snapshot()
        for c, local, tail in ((Cost(INT32_MAX), ZERO, ZERO),
                               (ZERO, Cost(INT32_MAX), ZERO),
                               (ZERO, ZERO, Cost(INT32_MAX))):
            with self.assertRaises(OverflowError):
                gate(s, c, local, tail)
            with self.assertRaises(OverflowError):
                debit(s, c, local, tail)
            self.assertEqual(s.snapshot(), before)
        malformed = Cost(1)
        object.__setattr__(malformed, "material", (0, 0, 0, True))
        with self.assertRaises(TypeError):
            debit(s, malformed)
        self.assertEqual(s.snapshot(), before)
        with self.assertRaises(TypeError):
            require_cost(cast(State, object()), ZERO)

    def test_both_controller_control_budgets_are_debited_only_once(self) -> None:
        s = fixture()
        # v0.6 routed learning minimum: M,C_A,C_B,DECIDE M,16W,S.
        clear, scratch = Cost(224, four(4)), Cost(8)
        local = add_cost(Cost(512 + 128), add_cost(clear, scratch))
        self.assertTrue(gate(s, ZERO, local).enough)
        local = sub_cost(local, Cost(256))
        debit(s, Cost(256), local)
        local = sub_cost(local, Cost(256))
        debit(s, Cost(256), local)
        local = sub_cost(local, FEE)
        self.assertFalse(gate(s, Cost(10000), local).enough)
        debit(s, clear, scratch)
        debit(s, scratch)
        self.assertEqual(s.energy, 10000 - (128 + 512 + 128 + 224 + 8))
        self.assertEqual(stocks(s)[1:], (16,) * 4)

    def test_loop_bound_is_not_escrow_or_prepaid_fee(self) -> None:
        s = fixture(3000, four(0))
        loop = Cost(20 * (6 + 128))
        exit_cost = Cost(8)
        before = s.snapshot()
        self.assertTrue(require_cost(s, loop, exit_cost))
        self.assertEqual(s.snapshot(), before)
        # First generation executes, then needed-write gate rejects material.
        debit(s, Cost(6), Cost(128 + 19 * 134 + 8))
        rejected = gate(s, Cost(23, (1, 0, 0, 0)), Cost(19 * 134 + 8))
        self.assertEqual(rejected, (True, False, 0))
        debit(s, exit_cost)  # Paid branch terminates suffix; no refund/deposit.
        self.assertEqual(s.energy, 3000 - 6 - 128 - 8)

    def test_bounds_are_current_inputs_not_success_receipts(self) -> None:
        s = fixture(1000)
        self.assertTrue(gate(s, Cost(50), Cost(8)).enough)
        s.energy = 50  # Independent physical loss; old admission is not credit.
        with self.assertRaises(InsufficientResources):
            debit(s, Cost(50))
        self.assertEqual(s.energy, 50)
        self.assertFalse(require_cost(s, Cost(1), public_tail=Cost(49)))
        self.assertTrue(require_cost(s, Cost(1), public_tail=Cost(48)))

    def test_unknown_address_maxima_are_caller_supplied_per_source(self) -> None:
        s = fixture(1000, (2, 0, 2, 2))
        self.assertFalse(require_cost(s, Cost(23, (1, 1, 1, 1))))
        # Only the caller's separately paid address discovery can justify this.
        self.assertTrue(require_cost(s, Cost(14, (1, 0, 0, 0))))


class TestDepositsAndActivation(unittest.TestCase):
    def test_capped_energy_and_source_local_deposit_inline_flows(self) -> None:
        s = fixture(65530, (254, 250, 255, 0))
        before = s.snapshot()
        packet = Cost(20, (8, 8, 8, 8))
        result = deposit(s, packet, permitted=packet)
        self.assertEqual(result.accepted, Cost(5, (1, 5, 0, 8)))
        self.assertEqual(result.overflow, Cost(15, (7, 3, 8, 0)))
        self.assertEqual(add_cost(result.accepted, result.overflow), packet)
        self.assertEqual(result.ignored, ZERO)
        self.assertEqual(s.snapshot(), resource_image(before, 65535, (255, 255, 255, 8)))
        with self.assertRaises(AttributeError):
            setattr(result, "accepted", ZERO)

    def test_debit_before_work_and_yield_never_self_funds(self) -> None:
        s = fixture(17)
        before = s.snapshot()
        with self.assertRaises(InsufficientResources):
            debit_and_deposit(s, Cost(17), Cost(100), permitted=Cost(100))
        self.assertEqual(s.snapshot(), before)
        result = debit_and_deposit(s, Cost(16), Cost(100), permitted=Cost(100))
        self.assertEqual(result.paid, Cost(16))
        self.assertEqual(s.energy, 101)
        s = fixture(65535)
        result = debit_and_deposit(s, Cost(20), Cost(20), permitted=Cost(20))
        self.assertEqual(result.flows.accepted.energy, 20)
        self.assertEqual(result.flows.overflow, ZERO)
        self.assertEqual(s.energy, 65535)

    def test_rejected_action_has_no_automatic_yield_or_fallback(self) -> None:
        s = fixture(137)
        before = s.snapshot()
        result = gate(s, Cost(16), Cost(8))
        self.assertFalse(result.enough)
        debit(s, Cost(8))
        self.assertEqual(s.snapshot(), resource_image(before, 1, four(20)))

    def test_negative_bool_and_invalid_yields_validate_before_any_debit(self) -> None:
        s = fixture()
        before = s.snapshot()
        for value in (*BAD_INTS, -1, INT32_MAX + 1):
            for material in (False, True):
                # Deliberately bypass frozen construction to test API revalidation.
                packet = Cost()
                object.__setattr__(packet, "material" if material else "energy",
                                   (0, 0, 0, value) if material else value)
                for operation in (deposit, passive_grant):
                    with self.assertRaises((TypeError, ValueError, OverflowError)):
                        operation(s, packet, permitted=Cost(100, four(100)))
                with self.assertRaises((TypeError, ValueError, OverflowError)):
                    debit_and_deposit(s, Cost(10), packet, permitted=Cost(100, four(100)))
                self.assertEqual(s.snapshot(), before)

    def test_packet_permitted_bounds_caps_and_configuration_mismatch(self) -> None:
        s = fixture()
        before = s.snapshot()
        for packet, permitted in ((Cost(11), Cost(10)),
                                   (Cost(0, (0, 0, 0, 2)), Cost(0, (9, 9, 9, 1))),
                                   (Cost(65536), Cost(65536)),
                                   (Cost(0, (256, 0, 0, 0)), Cost(0, (256, 0, 0, 0)))):
            with self.assertRaises((ValueError, OverflowError)):
                debit_and_deposit(s, Cost(1), packet, permitted=permitted)
            self.assertEqual(s.snapshot(), before)
        for cap in (0, -1, True, 1.0, 65536, 9999):
            with self.assertRaises((TypeError, ValueError, OverflowError)):
                deposit(s, ZERO, permitted=ZERO, energy_cap=cast(int, cap))
            self.assertEqual(s.snapshot(), before)
        for caps in ((256,) * 4, (True,) * 4, (0, 1), [255] * 4, (19,) * 4):
            with self.assertRaises((TypeError, ValueError, OverflowError)):
                deposit(s, ZERO, permitted=ZERO, material_caps=cast(Material4, caps))
            self.assertEqual(s.snapshot(), before)

    def test_configured_caps_are_dynamic_not_imported_from_physical(self) -> None:
        s = fixture(99, (3, 4, 5, 0))
        packet = Cost(100, four(20))
        result = deposit(s, packet, permitted=packet, energy_cap=100,
                         material_caps=(4, 5, 6, 0))
        self.assertEqual(result.accepted, Cost(1, (1, 1, 1, 0)))
        self.assertEqual(stocks(s), (100, 4, 5, 6, 0))
        self.assertFalse(hasattr(meter, "physical"))

    def test_ordinary_deposit_cannot_revive_zero_even_with_zero_packet(self) -> None:
        s = fixture(0)
        before = s.snapshot()
        for packet in (ZERO, Cost(65535, four(255))):
            with self.assertRaises(InsufficientResources):
                deposit(s, packet, permitted=packet)
            with self.assertRaises(InsufficientResources):
                debit_and_deposit(s, ZERO, packet, permitted=packet)
            self.assertEqual(s.snapshot(), before)

    def test_passive_grant_is_pre_fee_exception_but_not_revival(self) -> None:
        packet = Cost(200, four(10))
        s = fixture(1)
        result = passive_grant(s, packet, permitted=packet)
        self.assertEqual(result.accepted, packet)
        self.assertEqual(s.energy, 201)
        self.assertTrue(gate(s, ZERO, Cost(49)).enough)  # TICK remainder fixture.
        debit(s, Cost(49))
        self.assertEqual(s.energy, 24)
        s = fixture(0)
        before = s.snapshot()
        self.assertEqual(passive_grant(s, packet, permitted=packet),
                         DepositResult(ZERO, ZERO, packet))
        self.assertEqual(s.snapshot(), before)

    def test_passive_full_cap_and_grant_then_shutdown_conservation(self) -> None:
        s = fixture(65535, four(255))
        packet = Cost(30000, four(66))
        before = s.snapshot()
        flows = passive_grant(s, packet, permitted=packet)
        self.assertEqual(flows, DepositResult(ZERO, packet))
        self.assertEqual(s.snapshot(), before)
        s = fixture(1, four(0))
        flows = passive_grant(s, Cost(100, four(2)), permitted=Cost(100, four(2)))
        loss = gate(s, ZERO, Cost(49))
        self.assertEqual(loss, (False, False, 101))
        self.assertEqual(s.energy, 1 + flows.accepted.energy - loss.shutdown_loss)
        self.assertEqual(stocks(s)[1:], (2,) * 4)
        self.assertEqual(passive_grant(s, Cost(1000), permitted=Cost(1000)).accepted, ZERO)

    def test_canonical_activation_only_constructs_fresh_state(self) -> None:
        old = fixture(0, four(99))
        before = old.snapshot()
        fresh = canonical_activation(100, (1, 2, 3, 4))
        canonical = b"\xaa" * 20 + bytes(256)
        self.assertEqual(fresh.snapshot(), resource_image(canonical, 100, (1, 2, 3, 4)))
        self.assertEqual(old.snapshot(), before)
        self.assertNotIn(old, gc.get_referents(fresh))
        for energy in (0, -1, True, 65536):
            with self.assertRaises((TypeError, ValueError, OverflowError)):
                canonical_activation(cast(int, energy))
        with self.assertRaises(ValueError):
            canonical_activation(101, energy_cap=100)
        with self.assertRaises(ValueError):
            canonical_activation(1, four(2), material_caps=four(1))


class TestContractWitnesses(unittest.TestCase):
    def test_an001_actual_ordered_conditioning_then_optional_td_rejection(self) -> None:
        # AN-001: g=36 minus 23 current-work units/source leaves 13. This is a
        # static local worksheet, not a claim that an E3 trajectory reaches it.
        s = fixture(65535, four(13))
        before = s.snapshot()
        terminal = Cost(904, four(4))
        accepted_domains: list[int] = []  # Observer only, never worker input.
        for domain in range(20):
            vector = [0, 0, 0, 0]
            vector[domain // 5] += 1
            vector[(2 * domain) % 4] += 1
            vector[(2 * domain + 1) % 4] += 1
            body = Cost(32, cast(Material4, tuple(vector)))
            tail = add_cost(Cost((19 - domain) * 520), terminal)
            local = Cost(256 + 128 + 8)
            self.assertTrue(gate(s, ZERO, local, tail).enough)
            debit(s, Cost(256), Cost(128 + 8), tail)
            result = gate(s, body, Cost(8), tail)
            if result.enough:
                debit(s, body, Cost(8), tail)
                accepted_domains.append(domain)
            debit(s, Cost(8), public_tail=tail)
        self.assertEqual(accepted_domains, [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 13])
        self.assertEqual(stocks(s)[1:], (4, 5, 4, 6))
        self.assertEqual(s.energy, 65535 - 20 * 520 - 11 * 32)
        # Scheduled TERMINAL is independent: M,C,16R,TD M,16W,S.
        self.assertTrue(gate(s, ZERO, Cost(776, four(4))).enough)
        debit(s, Cost(256), Cost(520, four(4)))
        debit(s, Cost(160), Cost(360, four(4)))
        td = gate(s, Cost(217, four(2)), Cost(232, four(4)))
        self.assertEqual(td, (True, False, 0))
        debit(s, Cost(224, four(4)), Cost(8))
        debit(s, Cost(8))
        self.assertEqual(stocks(s)[1:], (0, 1, 0, 2))
        self.assertEqual(s.energy, 65535 - 20 * 520 - 11 * 32 - 904)
        # Meter accounts retirement but does not pretend to write the record.
        self.assertEqual(s.snapshot(), resource_image(before, s.energy, (0, 1, 0, 2)))

    def test_no_acquired_ram_reads_or_other_state_mutation(self) -> None:
        s = fixture()
        before = s.snapshot()
        with patch.object(State, "read_bits", side_effect=AssertionError("unpaid RAM")), \
             patch.object(State, "read_lane", side_effect=AssertionError("unpaid lane")), \
             patch.object(State, "snapshot", side_effect=AssertionError("hidden copy")):
            self.assertTrue(require_cost(s, Cost(1)))
            self.assertTrue(gate(s, Cost(10), Cost(8)).enough)
            debit(s, Cost(10, (1, 2, 3, 4)), Cost(8))
            deposit(s, Cost(5, (1, 1, 1, 1)), permitted=Cost(5, four(1)))
        self.assertEqual(s.snapshot(), resource_image(before, 9867, (20, 19, 18, 17)))

    def test_observer_ledger_conservation_and_snapshot_replay(self) -> None:
        s = fixture(1000, four(10))
        original = s.snapshot()
        observer: list[tuple[str, Cost]] = []
        g = gate(s, Cost(20, (1, 2, 3, 4)), Cost(8))
        self.assertTrue(g.enough)
        observer.append(("debit", FEE))
        paid = debit(s, Cost(20, (1, 2, 3, 4)), Cost(8))
        observer.append(("debit", paid))
        flows = deposit(s, Cost(50, four(1)), permitted=Cost(50, four(1)))
        observer.append(("accepted", flows.accepted))
        observer.append(("debit", debit(s, Cost(8))))
        expected = [1000, 10, 10, 10, 10]
        for kind, value in observer:
            sign = 1 if kind == "accepted" else -1
            for j, amount in enumerate((value.energy, *value.material)):
                expected[j] += sign * amount
        self.assertEqual(stocks(s), tuple(expected))
        self.assertEqual(s.snapshot(), resource_image(original, expected[0],
                                                     cast(Material4, tuple(expected[1:]))))
        replay = State(s.snapshot())  # No meter receipt/context to serialize.
        debit(s, Cost(2))
        debit(replay, Cost(2))
        self.assertEqual(s.snapshot(), replay.snapshot())
        self.assertEqual(State.__slots__, ("__buffer",))
        self.assertFalse(hasattr(s, "__dict__"))
        refs = gc.get_referents(s)
        self.assertEqual(len(refs), 2)
        self.assertEqual(sum(type(r) is bytearray for r in refs), 1)
        for name in ("ledger", "logs", "escrow", "balance", "tail", "history"):
            self.assertFalse(hasattr(meter, name))


if __name__ == "__main__":
    unittest.main()