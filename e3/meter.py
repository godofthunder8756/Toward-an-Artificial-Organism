"""Stateless, engineering-only implementation of the selected METER128 tariff.

State's packed E/P are the sole authoritative resources. Bounds and results are
ephemeral current-operation values, not escrow, receipts permitting later work,
VM state, sensors, or resumable audit records. No function reads acquired RAM,
clears scratch/records, receives callbacks, or keeps a log/balance/history.

The caller supplies G-derived current cost, local remainder, and public tail.
Before paid address discovery it must supply maxima over *all* encodings for
energy and EACH source. It must enforce paid reads, bounded loops, current-packet
ownership, branch eligibility, and one-shot deposits. This module cannot prove
those properties: it is neither a VM nor a capability/process sandbox.

Updates are validation-atomic in the contract's fault-free operation window:
all arguments/affordability are checked before the nonthrowing typed setters.
They are not a thread-synchronization primitive. METER128 is an approved abstract
price, not a claim that these Python functions execute 128 hardware instructions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal, NamedTuple

from .state import ENERGY_MAX, MATERIAL_COUNT, MATERIAL_MAX, State


INT32_MAX: Final = (1 << 31) - 1
METER_FEE: Final = 128
Material4 = tuple[int, int, int, int]
ZERO_MATERIAL: Final[Material4] = (0, 0, 0, 0)
MAX_MATERIAL: Final[Material4] = (MATERIAL_MAX, MATERIAL_MAX, MATERIAL_MAX, MATERIAL_MAX)


def _integer(value: int, name: str, maximum: int = INT32_MAX) -> None:
    if type(value) is not int:
        raise TypeError(f"{name} must be a built-in int, not bool")
    if value < 0:
        raise ValueError(f"{name} must be nonnegative")
    if value > maximum:
        raise OverflowError(f"{name} exceeds {maximum}")


def _material(value: Material4, name: str, maximum: int = INT32_MAX) -> None:
    if type(value) is not tuple:
        raise TypeError(f"{name} must be an immutable tuple")
    if len(value) != MATERIAL_COUNT:
        raise ValueError(f"{name} must contain exactly four source quantities")
    for amount in value:
        _integer(amount, name, maximum)


@dataclass(frozen=True, slots=True)
class Cost:
    """Checked signed-32 nonnegative energy and source-local material vector.

    The same immutable value type represents an actual cost or a bound. It
    never represents a reservation object or stores a reference to a State.
    Bounds can exceed physical stocks, but no component may exceed INT32_MAX.
    """

    energy: int = 0
    material: Material4 = ZERO_MATERIAL

    def __post_init__(self) -> None:
        _integer(self.energy, "energy")
        _material(self.material, "material")


Bound = Cost
ZERO: Final = Cost()
FEE: Final = Cost(METER_FEE)


def _cost(value: Cost, name: str) -> None:
    if type(value) is not Cost:
        raise TypeError(f"{name} must be a Cost/Bound")
    # Recheck at the public boundary, including deliberately malformed objects.
    _integer(value.energy, f"{name}.energy")
    _material(value.material, f"{name}.material")


def _state(state: State) -> None:
    if type(state) is not State:
        raise TypeError("state must be the packed State, not a proxy or subclass")


def add_cost(left: Cost, right: Cost) -> Cost:
    """Componentwise addition using wide temporaries, rejecting int32 overflow."""
    _cost(left, "left")
    _cost(right, "right")
    a, b = left.material, right.material
    return Cost(left.energy + right.energy,
                (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3]))


def sub_cost(left: Cost, right: Cost) -> Cost:
    """Componentwise subtraction; negative components are errors, not credit."""
    _cost(left, "left")
    _cost(right, "right")
    a, b = left.material, right.material
    return Cost(left.energy - right.energy,
                (a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3]))


def floor_quote(
    current_cost: Cost,
    local_remainder: Bound = ZERO,
    public_tail: Bound = ZERO,
    residue: int = 1,
) -> Bound:
    """Compute c+L+T+rho without debiting or retaining a future tail.

    L excludes c and any already-paid work; T excludes the current service.
    A caller may request a larger positive residue, never zero/last-energy work.
    This preflight arithmetic is not a free policy sensor or body-admission gate.
    """
    _integer(residue, "residue")
    if residue == 0:
        raise ValueError("a live operation requires positive energy residue")
    return add_cost(add_cost(add_cost(current_cost, local_remainder), public_tail),
                    Cost(residue))


def _covers(state: State, required: Cost) -> bool:
    return state.energy >= required.energy and all(
        state.read_material(j) >= required.material[j] for j in range(MATERIAL_COUNT)
    )


def require_cost(
    state: State,
    current_cost: Cost,
    local_remainder: Bound = ZERO,
    public_tail: Bound = ZERO,
    residue: int = 1,
) -> bool:
    """Pure current-reservoir affordability predicate; material equality passes."""
    _state(state)
    return _covers(state, floor_quote(current_cost, local_remainder, public_tail, residue))


class GateResult(NamedTuple):
    """Consume immediately for a VM branch or one-way observer, never resume it."""

    paid: bool
    enough: bool
    shutdown_loss: int = 0

    @property
    def status(self) -> Literal["admitted", "rejected", "shutdown"]:
        if not self.paid:
            return "shutdown"
        return "admitted" if self.enough else "rejected"


def gate(
    state: State,
    current_cost: Cost,
    local_remainder: Bound = ZERO,
    public_tail: Bound = ZERO,
    *,
    minimum_exit: Bound | None = None,
    residue: int = 1,
) -> GateResult:
    """Check minimum, pay exactly 128, then test the optional body.

    Minimum is fee+minimum_exit+T+rho; default minimum_exit is L. Optional body
    is c+L+T+rho AFTER paying the fee. All vector arithmetic is checked before
    mutation, so malformed/overflowing G is not reported as physical death.
    Minimum failure sinks only E and reports that physical loss, without paying
    a fee or changing P/RAM/flags. Optional rejection pays only the fee: the
    caller still executes/pays its required retirement, CONTROL and final S.
    Nested gates never implicitly clear or close the owning operation.
    """
    _state(state)
    minimum = floor_quote(FEE, local_remainder if minimum_exit is None else minimum_exit,
                          public_tail, residue)
    body = floor_quote(current_cost, local_remainder, public_tail, residue)
    if not _covers(state, minimum):
        loss = state.energy
        state.energy = 0
        return GateResult(False, False, loss)
    state.energy = state.energy - METER_FEE
    return GateResult(True, _covers(state, body))


class InsufficientResources(ValueError):
    """A requested debit cannot preserve its mandatory remainder and residue."""


def debit(
    state: State,
    current_cost: Cost,
    local_remainder: Bound = ZERO,
    public_tail: Bound = ZERO,
    residue: int = 1,
) -> Cost:
    """Debit BEFORE work/output, returning only the actual cost for observation.

    No repeated METER fee, bound prepayment, cleanup, deposit or implicit sink.
    Shortage raises without mutation; only a failed gate minimum sinks E.
    A prior successful gate result is never accepted as proof of affordability.
    """
    if not require_cost(state, current_cost, local_remainder, public_tail, residue):
        raise InsufficientResources("debit would consume mandatory resources or live residue")
    energy = state.energy - current_cost.energy
    a = current_cost.material
    material = (state.P0 - a[0], state.P1 - a[1], state.P2 - a[2], state.P3 - a[3])
    _assign(state, energy, material)
    return current_cost


def _assign(state: State, energy: int, material: Material4) -> None:
    # All values are proven within physical widths before entering this helper.
    state.energy = energy
    for j, amount in enumerate(material):
        state.write_material(j, amount)


class DepositResult(NamedTuple):
    """Inline accepted/cap-overflow/ignored flows; no stock mirror or receipt."""

    accepted: Cost
    overflow: Cost
    ignored: Cost = ZERO


def _deposit_inputs(
    state: State, packet: Cost, permitted: Bound,
    energy_cap: int, material_caps: Material4,
) -> None:
    _state(state)
    _cost(packet, "packet")
    _cost(permitted, "permitted")
    _integer(packet.energy, "packet energy", ENERGY_MAX)
    _material(packet.material, "packet material", MATERIAL_MAX)
    _integer(permitted.energy, "permitted energy", ENERGY_MAX)
    _material(permitted.material, "permitted material", MATERIAL_MAX)
    _integer(energy_cap, "energy_cap", ENERGY_MAX)
    if energy_cap == 0:
        raise ValueError("energy_cap must be positive")
    _material(material_caps, "material_caps", MATERIAL_MAX)
    if packet.energy > permitted.energy or any(
        packet.material[j] > permitted.material[j] for j in range(MATERIAL_COUNT)
    ):
        raise ValueError("packet exceeds the current permitted yield")
    if state.energy > energy_cap or any(
        state.read_material(j) > material_caps[j] for j in range(MATERIAL_COUNT)
    ):
        raise ValueError("current stock exceeds the supplied physical configuration")


def _deposit_live(
    state: State, packet: Cost, energy_cap: int, material_caps: Material4,
) -> DepositResult:
    energy = state.energy
    a = min(packet.energy, energy_cap - energy)
    p = (state.P0, state.P1, state.P2, state.P3)
    q, cap = packet.material, material_caps
    accepted = Cost(a, (min(q[0], cap[0] - p[0]), min(q[1], cap[1] - p[1]),
                        min(q[2], cap[2] - p[2]), min(q[3], cap[3] - p[3])))
    m = accepted.material
    overflow = sub_cost(packet, accepted)
    _assign(state, energy + a, (p[0] + m[0], p[1] + m[1], p[2] + m[2], p[3] + m[3]))
    return DepositResult(accepted, overflow)


def deposit(
    state: State,
    packet: Cost,
    *,
    permitted: Bound,
    energy_cap: int = ENERGY_MAX,
    material_caps: Material4 = MAX_MATERIAL,
) -> DepositResult:
    """Consume an explicit current yield in the already-paid gate continuation.

    Caller must first pay attempt/I/O and accepted-material transport, reserving
    maximum transport BEFORE accepting yield. No additional METER fee is due.
    This trusted typed command does not establish packet provenance, one-shot
    delivery or prior admission. Ordinary deposits at E=0 (even zero) are errors.
    Excess beyond physical caps is returned as overflow, not stored for later.
    """
    _deposit_inputs(state, packet, permitted, energy_cap, material_caps)
    if state.energy == 0:
        raise InsufficientResources("ordinary deposits cannot revive an unpowered state")
    return _deposit_live(state, packet, energy_cap, material_caps)


class TransferResult(NamedTuple):
    paid: Cost
    flows: DepositResult


def debit_and_deposit(
    state: State,
    current_cost: Cost,
    packet: Cost,
    local_remainder: Bound = ZERO,
    public_tail: Bound = ZERO,
    *,
    permitted: Bound,
    energy_cap: int = ENERGY_MAX,
    material_caps: Material4 = MAX_MATERIAL,
    residue: int = 1,
) -> TransferResult:
    """Paid gate continuation with input validation, debit, THEN capped deposit.

    c must include actual attempt/transport work, not unspent worst-case bounds.
    The upstream gate must already have admitted the maximum allowed transport.
    Income cannot finance this debit. No callbacks or extra scalar are accepted.
    """
    _deposit_inputs(state, packet, permitted, energy_cap, material_caps)
    paid = debit(state, current_cost, local_remainder, public_tail, residue)
    return TransferResult(paid, _deposit_live(state, packet, energy_cap, material_caps))


def passive_grant(
    state: State,
    packet: Cost,
    *,
    permitted: Bound,
    energy_cap: int = ENERGY_MAX,
    material_caps: Material4 = MAX_MATERIAL,
) -> DepositResult:
    """TICK-only external support exception BEFORE its minimum/fee.

    Initial E must be positive. E=0 ignores the entire grant, including material;
    ignored flows are distinct from cap overflow. Caller must subsequently pay
    TICK's fee, five scalar occurrences (including zeros), transport, living/rent
    and S. A grant followed by failed minimum is support then shutdown loss,
    never a free active tick. No prior state/record is revived.
    """
    _deposit_inputs(state, packet, permitted, energy_cap, material_caps)
    if state.energy == 0:
        return DepositResult(ZERO, ZERO, packet)
    return _deposit_live(state, packet, energy_cap, material_caps)


def canonical_activation(
    energy: int,
    material: Material4 = ZERO_MATERIAL,
    *,
    energy_cap: int = ENERGY_MAX,
    material_caps: Material4 = MAX_MATERIAL,
) -> State:
    """Named experimental activation of a FRESH canonical State, never old RAM.

    Configuration must specify positive initial E within caps. No old State,
    history, scratch, event or callback parameter exists. Cancellation of old
    external capabilities belongs to the future boundary supervisor.
    """
    initial = Cost(energy, material)
    fresh = State.reset()
    _deposit_inputs(fresh, initial, initial, energy_cap, material_caps)
    if energy == 0 or energy > energy_cap or any(
        material[j] > material_caps[j] for j in range(MATERIAL_COUNT)
    ):
        raise ValueError("initial resources must fit caps with positive energy")
    _assign(fresh, energy, material)
    return fresh