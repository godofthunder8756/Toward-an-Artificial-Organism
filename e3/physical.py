"""Trusted, engineering-only E3 v0.11 physical values and transitions.

Placement is inherited ROM, not acquired state. Quotes and age codecs are NOT
paid READ2/WRITE2, AGE, CONDITION, rent, or upkeep services. Only a future paid
executor can authorize those services; never expose these host helpers, raw
State, fault frames, or loss ledgers as worker capabilities.

Physics receives explicit current discrete draws, never labels, seeds, keys,
callbacks, prior snapshots, worker protocol frames, or a zero-wear switch.
Simultaneous faults use a temporary copy of the current 276-byte state. No
copy, age vector, or observer count is retained after returning the ledger.
Python privacy/frozen dataclasses are not an adversarial isolation boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Final, final

from . import state as layout
from .state import State


HUB_COUNT: Final = 4
DOMAIN_COUNT: Final = 20
RAM_LANE_COUNT: Final = 1080
ACCESSIBLE_LANE_COUNT: Final = 948
RESERVE_LANE_COUNT: Final = 132
FAULT_SLOT_COUNT: Final = 3160
FAULT_UNIFORM_BOUND: Final = 10000
EXECUTOR_HUB: Final = 255  # Byte sentinel: E is at X, not an additional hub.
RAM_ACCESSIBLE: Final = 0
RAM_RESERVE: Final = 1
TYPED_RESERVOIR: Final = 2
SIGNED32_MAX: Final = (1 << 31) - 1
MaterialVector = tuple[int, int, int, int]


def _integer(value: int, name: str, lower: int, upper: int) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be a built-in int, not bool")
    if not lower <= value <= upper:
        raise ValueError(f"{name} must be in {lower}..{upper}")
    return value


def _state(state: State) -> None:
    if type(state) is not State:
        raise TypeError("state must be a State, not a snapshot or callback")


def _material(values: MaterialVector, maximum: int) -> MaterialVector:
    if type(values) is not tuple:
        raise TypeError("material vector must be an immutable tuple")
    if len(values) != HUB_COUNT:
        raise ValueError("material vector must have exactly four components")
    for value in values:
        _integer(value, "material component", 0, maximum)
    return values


@dataclass(frozen=True, slots=True)
class LanePlacement:
    """The columns of an eight-byte v0.9 map row, not a binary archive codec.

    For E, hub=255, domain=4, and all routes are zero. For Pj, hub=j,
    domain=5j+4, read/write routes are one and material route is zero.
    Typed rows describe location only; their routes never authorize RAM I/O.
    """

    lane: int
    hub: int
    domain: int
    read_route: int
    write_route: int
    material_route: int
    flags: int


@dataclass(frozen=True, slots=True)
class DomainPlacement:
    """Inherited domain owner and the two physical lanes storing its age."""

    domain: int
    hub: int
    low_age_lane: int
    high_age_lane: int


def _placement(lane: int) -> LanePlacement:
    if lane < layout.CODE_LANES:
        hub = lane // 20
        return LanePlacement(lane, hub, 5 * hub, 2, 2, 1, RAM_ACCESSIBLE)
    if layout.RESOURCE_START_LANE <= lane < layout.MATERIAL_OFFSET // 2:
        return LanePlacement(lane, EXECUTOR_HUB, 4, 0, 0, 0, TYPED_RESERVOIR)
    if layout.MATERIAL_OFFSET // 2 <= lane < layout.RESOURCE_END_LANE:
        hub = (2 * lane - layout.MATERIAL_OFFSET) // layout.MATERIAL_WIDTH
        return LanePlacement(lane, hub, 5 * hub + 4, 1, 1, 0, TYPED_RESERVOIR)
    hub = lane % HUB_COUNT
    if lane < layout.QUERY_OFFSET // 2:
        rank = (lane - layout.Q_OFFSET // 2) // HUB_COUNT
        domain = 5 * hub + 1 + rank // 64
    else:
        domain = 5 * hub + 4
    flag = RAM_RESERVE if lane >= layout.RESERVE_START_LANE else RAM_ACCESSIBLE
    return LanePlacement(lane, hub, domain, 1, 1, 0, flag)


_LANE_ROWS: Final = tuple(_placement(lane) for lane in range(layout.LANE_COUNT))
_DOMAIN_ROWS: Final = tuple(
    DomainPlacement(d, d // 5, layout.AGE_OFFSET // 2 + 2 * d,
                    layout.AGE_OFFSET // 2 + 2 * d + 1)
    for d in range(DOMAIN_COUNT)
)
_RAM_LANES: Final = tuple(row.lane for row in _LANE_ROWS if row.flags != TYPED_RESERVOIR)


@final
@dataclass(frozen=True, slots=True)
class PhysicalConfig:
    """The one selected target-independent tree; no constructor inputs/state.

    X is vertex 0, Bj vertex 1+j, and L(j,k) vertex 5+5j+k. All lookup
    tuples are class-level inherited constants, with 1,104 address-indexed
    entries including typed positions. Resource entries in material_source
    are None: they have physical hubs but no legal RAM write source.
    """

    hub_count: ClassVar[int] = HUB_COUNT
    domain_count: ClassVar[int] = DOMAIN_COUNT
    lane_count: ClassVar[int] = layout.LANE_COUNT
    ram_lane_count: ClassVar[int] = RAM_LANE_COUNT
    vertex_count: ClassVar[int] = 25
    diameter: ClassVar[int] = 4
    edges: ClassVar[tuple[tuple[int, int], ...]] = (
        tuple((0, 1 + j) for j in range(HUB_COUNT))
        + tuple((1 + j, 5 + 5 * j + k) for j in range(HUB_COUNT) for k in range(5))
    )
    lane_rows: ClassVar[tuple[LanePlacement, ...]] = _LANE_ROWS
    domain_rows: ClassVar[tuple[DomainPlacement, ...]] = _DOMAIN_ROWS
    ram_lanes: ClassVar[tuple[int, ...]] = _RAM_LANES
    lane_to_hub: ClassVar[tuple[int, ...]] = tuple(row.hub for row in _LANE_ROWS)
    lane_to_domain: ClassVar[tuple[int, ...]] = tuple(row.domain for row in _LANE_ROWS)
    lane_distance: ClassVar[tuple[int, ...]] = tuple(row.read_route for row in _LANE_ROWS)
    material_hops: ClassVar[tuple[int, ...]] = tuple(row.material_route for row in _LANE_ROWS)
    material_source: ClassVar[tuple[int | None, ...]] = tuple(
        None if row.flags == TYPED_RESERVOIR else row.hub for row in _LANE_ROWS
    )
    lane_is_code: ClassVar[tuple[bool, ...]] = tuple(
        lane < layout.CODE_LANES for lane in range(layout.LANE_COUNT)
    )
    lane_to_vertex: ClassVar[tuple[int, ...]] = tuple(
        5 + 5 * row.hub + (row.lane % 20) // 4 if row.lane < layout.CODE_LANES
        else 0 if row.hub == EXECUTOR_HUB else 1 + row.hub
        for row in _LANE_ROWS
    )


DEFAULT_CONFIG: Final = PhysicalConfig()


def _config(config: PhysicalConfig) -> None:
    if type(config) is not PhysicalConfig:
        raise TypeError("config must be the selected PhysicalConfig")


def _ram_row(lane: int, config: PhysicalConfig, *, accessible: bool) -> LanePlacement:
    _config(config)
    _integer(lane, "lane", 0, layout.LANE_COUNT - 1)
    row = config.lane_rows[lane]
    if row.flags == TYPED_RESERVOIR:
        raise PermissionError("typed reservoirs are not RAM lanes")
    if accessible and row.flags == RAM_RESERVE:
        raise PermissionError("reserve has no agent READ2/WRITE2 access")
    return row


@dataclass(frozen=True, slots=True)
class ResourceQuote:
    """Informational sourcewise debit, not payment, escrow, or an admission."""

    energy: int
    material: MaterialVector

    def __post_init__(self) -> None:
        _integer(self.energy, "energy", 0, SIGNED32_MAX)
        _material(self.material, SIGNED32_MAX)

    @property
    def components(self) -> tuple[int, int, int, int, int]:
        return (self.energy, *self.material)


def lane_read_cost(lane: int, config: PhysicalConfig = DEFAULT_CONFIG) -> int:
    """Quote 3+7d energy for one accessible lane, without reading anything."""
    row = _ram_row(lane, config, accessible=True)
    return 3 + 7 * row.read_route


def lane_write_cost(lane: int, config: PhysicalConfig = DEFAULT_CONFIG) -> int:
    """Quote 6+8d+m energy; one assigned-source material is additional."""
    row = _ram_row(lane, config, accessible=True)
    return 6 + 8 * row.write_route + row.material_route


def write_quote(
    lanes: tuple[int, ...] | list[int], config: PhysicalConfig = DEFAULT_CONFIG
) -> ResourceQuote:
    """Quote a <=1,104-access multiset, preserving repeated/same-value writes.

    This is not an unknown-address bound or a cross-source pooled allowance.
    A future executor must price discovery and select sourcewise maxima from
    all legal paths before it knows an acquired address.
    """
    _config(config)
    if type(lanes) not in (tuple, list):
        raise TypeError("lanes must be a tuple or list")
    addresses = tuple(lanes)
    if len(addresses) > layout.LANE_COUNT:
        raise ValueError("write plan exceeds 1,104 accesses")
    energy = 0
    material = [0, 0, 0, 0]
    for lane in addresses:
        row = _ram_row(lane, config, accessible=True)
        energy += 6 + 8 * row.write_route + row.material_route
        material[row.hub] += 1
    return ResourceQuote(energy, (material[0], material[1], material[2], material[3]))


def age_lanes(domain: int) -> tuple[int, int]:
    _integer(domain, "domain", 0, DOMAIN_COUNT - 1)
    row = _DOMAIN_ROWS[domain]
    return row.low_age_lane, row.high_age_lane


def read_age(state: State, domain: int) -> int:
    """Trusted current-state codec only; never a free worker age sensor."""
    _state(state)
    _integer(domain, "domain", 0, DOMAIN_COUNT - 1)
    return state.read_bits(layout.AGE_OFFSET + layout.AGE_WIDTH * domain, layout.AGE_WIDTH)


def write_age(state: State, domain: int, age: int) -> None:
    """Raw four-bit codec, not AGE/CONDITION or permission to avoid dues.

    Like State.write_bits, this may construct unpowered component fixtures.
    It performs no liveness, admission, increment, conditioning, or metering.
    """
    _state(state)
    _integer(domain, "domain", 0, DOMAIN_COUNT - 1)
    _integer(age, "age", 0, 15)
    state.write_bits(layout.AGE_OFFSET + layout.AGE_WIDTH * domain, layout.AGE_WIDTH, age)


def conditioning_vector(domain: int) -> MaterialVector:
    """Dues at the domain hub plus one write at each actual age-lane hub."""
    low, high = age_lanes(domain)
    counts = [0, 0, 0, 0]
    for hub in (domain // 5, low % HUB_COUNT, high % HUB_COUNT):
        counts[hub] += 1
    return counts[0], counts[1], counts[2], counts[3]


def conditioning_quote(domain: int) -> ResourceQuote:
    """Quote only the 32-energy optional body, not its 520-energy envelope."""
    return ResourceQuote(4 + 2 * 14, conditioning_vector(domain))


def fault_thresholds(age: int) -> tuple[int, int]:
    """Exact counts out of 10,000: h=(a+1)/1,000 and e=a/10,000."""
    _integer(age, "age", 0, 15)
    return 10 * (age + 1), age


FAULT_SLOTS: Final[tuple[tuple[int, str], ...]] = tuple(
    (lane, purpose)
    for lane in _RAM_LANES
    for purpose in (("code_flip", "code_erase") if lane < layout.CODE_LANES
                    else ("aux_bit0", "aux_bit1", "aux_erase"))
)


def fault_slot_indices(lane: int) -> tuple[int, ...]:
    """Ascending lane order, skipping reservoirs but including every reserve lane."""
    _ram_row(lane, DEFAULT_CONFIG, accessible=False)
    if lane < layout.CODE_LANES:
        return 2 * lane, 2 * lane + 1
    skipped = (layout.RESOURCE_END_LANE - layout.RESOURCE_START_LANE
               if lane >= layout.RESOURCE_END_LANE else 0)
    first = 2 * layout.CODE_LANES + 3 * (lane - layout.CODE_LANES - skipped)
    return first, first + 1, first + 2


@final
@dataclass(frozen=True, slots=True)
class FaultFrame:
    """One immutable current-physics draw array, NOT a v0.9 worker frame.

    A tuple or list input is cloned to a tuple, checked in full, and retained
    only by this explicit caller-owned frame. Every entry is a strict built-in
    int in 0..9,999, including draws unused for empty/invalid code. Slot order
    is FAULT_SLOTS: code flip/erase, then auxiliary bit0/bit1/erase, by lane.

    Future private HMAC rejection sampling must use uniform m=10,000 with
    the v0.9 twelve-field purpose coordinates. This module generates no draws
    and cannot certify their independence or provenance.
    """

    draws: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.draws) not in (tuple, list):
            raise TypeError("fault draws must be a tuple or list")
        draws = tuple(self.draws)
        if len(draws) != FAULT_SLOT_COUNT:
            raise ValueError("fault frame must contain exactly 3,160 draws")
        for draw in draws:
            _integer(draw, "fault draw", 0, FAULT_UNIFORM_BOUND - 1)
        object.__setattr__(self, "draws", draws)

    def __len__(self) -> int:
        return FAULT_SLOT_COUNT

    def __getitem__(self, index: int) -> int:
        _integer(index, "fault slot", 0, FAULT_SLOT_COUNT - 1)
        return self.draws[index]


@dataclass(frozen=True, slots=True)
class LossLedger:
    """One-way observer result only, never a worker receipt or cheap health.

    Losses are nonnegative physical sinks, not operation spending. Changed
    counts compare final versus original RAM values, not sampled flip/erase
    events. Reservoir bits are excluded from all RAM counts. No state image,
    age, fault mask, or source object is returned or stored here.
    """

    energy_loss: int = 0
    material_loss: MaterialVector = (0, 0, 0, 0)
    changed_code_lanes: int = 0
    changed_aux_lanes: int = 0
    changed_bits: int = 0

    def __post_init__(self) -> None:
        _integer(self.energy_loss, "energy loss", 0, layout.ENERGY_MAX)
        _material(self.material_loss, layout.MATERIAL_MAX)
        _integer(self.changed_code_lanes, "changed code lanes", 0, layout.CODE_LANES)
        _integer(self.changed_aux_lanes, "changed auxiliary lanes", 0, 1000)
        _integer(self.changed_bits, "changed RAM bits", 0, 2 * RAM_LANE_COUNT)

    @property
    def energy_delta(self) -> int:
        return -self.energy_loss

    @property
    def material_delta(self) -> MaterialVector:
        p0, p1, p2, p3 = self.material_loss
        return -p0, -p1, -p2, -p3

    @property
    def changed_lanes(self) -> int:
        return self.changed_code_lanes + self.changed_aux_lanes


def _sink(state: State, energy: int, material: MaterialVector) -> None:
    # Call only with validated losses <= current stocks, after all RAM changes.
    for hub, loss in enumerate(material):
        if loss:
            state.write_material(hub, state.read_material(hub) - loss)
    if energy:
        state.energy -= energy  # E=1 -> 0 is last; no post-death flag write.


def apply_faults(
    state: State, frame: FaultFrame, config: PhysicalConfig = DEFAULT_CONFIG
) -> LossLedger:
    """Apply one simultaneous live fault and typed min(stock,1) leakage.

    Validate the entire explicit frame before touching state, even at E=0.
    E=0 then skips physics completely. At E>0, use only current pre-fault
    stored ages, including storage-domain ages for the age lanes themselves.
    No increment, reset, rent, output, death flag, or resume is implied.
    """
    _state(state)
    _config(config)
    if type(frame) is not FaultFrame:
        raise TypeError("frame must be a FaultFrame, not a worker packet")
    draws = FaultFrame(frame.draws).draws  # Revalidate before any mutation.
    if state.energy == 0:
        return LossLedger()
    before = State(state.snapshot())
    changed_code = changed_aux = changed_bits = 0
    position = 0
    for lane in config.ram_lanes:
        row = config.lane_rows[lane]
        flip, erase = fault_thresholds(read_age(before, row.domain))
        old = before._physics_read_lane(lane)
        new = old
        if lane < layout.CODE_LANES:
            if old < layout.SYMBOL_ERASED and draws[position] < flip:
                new ^= 1
            if draws[position + 1] < erase:
                new = layout.SYMBOL_ERASED
            position += 2
        else:
            new ^= int(draws[position] < flip) | (int(draws[position + 1] < flip) << 1)
            if draws[position + 2] < erase:
                new = 0
            position += 3
        if new != old:
            state._physics_write_lane(lane, new)
            changed_code += int(lane < layout.CODE_LANES)
            changed_aux += int(lane >= layout.CODE_LANES)
            changed_bits += (old ^ new).bit_count()
    material = tuple(min(before.read_material(j), 1) for j in range(HUB_COUNT))
    losses: MaterialVector = (material[0], material[1], material[2], material[3])
    ledger = LossLedger(min(before.energy, 1), losses, changed_code, changed_aux, changed_bits)
    _sink(state, ledger.energy_loss, ledger.material_loss)
    return ledger


def _lesion(state: State, lanes: tuple[int, ...], energy: int,
            material: MaterialVector) -> LossLedger:
    changed_code = changed_aux = changed_bits = 0
    for lane in lanes:
        old = state._physics_read_lane(lane)
        new = layout.SYMBOL_ERASED if lane < layout.CODE_LANES else 0
        if new != old:
            state._physics_write_lane(lane, new)
            changed_code += int(lane < layout.CODE_LANES)
            changed_aux += int(lane >= layout.CODE_LANES)
            changed_bits += (old ^ new).bit_count()
    ledger = LossLedger(energy, material, changed_code, changed_aux, changed_bits)
    _sink(state, energy, material)
    return ledger


def apply_primary_lesion(state: State) -> LossLedger:
    """Code-only H1 lesion: layers k=3,4 in every block, exactly 32 sites."""
    _state(state)
    if state.energy == 0:
        return LossLedger()
    lanes = tuple(20 * block + position for block in range(HUB_COUNT)
                  for position in range(12, 20))
    return _lesion(state, lanes, 0, (0, 0, 0, 0))


def apply_hub_lesion(
    state: State, hub: int, config: PhysicalConfig = DEFAULT_CONFIG
) -> LossLedger:
    """Clear all selected-hub RAM/reserve, erase code, sink Pj and floor(E/2)."""
    _state(state)
    _config(config)
    _integer(hub, "hub", 0, HUB_COUNT - 1)
    if state.energy == 0:
        return LossLedger()
    lanes = tuple(lane for lane in config.ram_lanes if config.lane_to_hub[lane] == hub)
    values = [0, 0, 0, 0]
    values[hub] = state.read_material(hub)
    losses: MaterialVector = (values[0], values[1], values[2], values[3])
    return _lesion(state, lanes, state.energy // 2, losses)


def apply_global_resource_injury(state: State) -> LossLedger:
    """Sink floor(E/2) and floor(Pj/2) independently; touch no RAM bits."""
    _state(state)
    if state.energy == 0:
        return LossLedger()
    values = tuple(state.read_material(j) // 2 for j in range(HUB_COUNT))
    losses: MaterialVector = (values[0], values[1], values[2], values[3])
    return _lesion(state, (), state.energy // 2, losses)