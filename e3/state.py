"""Fixed-size E3 state codecs under the engineering-only v0.11 design freeze.

The sole persistent payload is one private 276-byte bytearray. There are no
resource mirrors, decoded labels, histories, or attached scratch buffers.
Bit offsets are global, LSB-first; lane indices address aligned two-bit words.
Signed fields are two's complement. Snapshots preserve ALL raw encodings.

These trusted-host codecs do NOT implement READ2/WRITE2 services, metering,
permissions, physical laws, or a sandbox. A future interpreter must charge
reads/merges/writes even for sub-two-bit changes; it must never hand a State,
snapshot, typed stock setter, or physics helper to an interpreted policy.
"""

from __future__ import annotations

from typing import Final, final

STATE_BYTES: Final = 276
STATE_BITS: Final = STATE_BYTES * 8
LANE_BITS: Final = 2
LANE_COUNT: Final = STATE_BITS // LANE_BITS
CODE_BITS: Final = 160
CODE_BYTES: Final = 20
CODE_LANES: Final = 80
AUX_BITS: Final = 2048
AUX_BYTES: Final = 256
MAX_FIELD_BITS: Final = 32

# All offsets below are GLOBAL BIT offsets, not auxiliary-relative offsets.
CODE_OFFSET: Final = 0
Q_OFFSET: Final = 160
Q_COUNT: Final = 96
Q_WIDTH: Final = 16
QUERY_OFFSET: Final = 1696
QUERY_COUNT: Final = 5
QUERY_WIDTH: Final = 8
STAGING_OFFSET: Final = 1736
STAGING_COUNT: Final = 4
STAGING_WIDTH: Final = 8
TRANSITION_OFFSET: Final = 1768
TRANSITION_WIDTH: Final = 32
TRANSITION_VALID_OFFSET: Final = TRANSITION_OFFSET
TRANSITION_OBSERVATION_OFFSET: Final = TRANSITION_OFFSET + 1
TRANSITION_ACTION_OFFSET: Final = TRANSITION_OFFSET + 6
TRANSITION_REWARD_OFFSET: Final = TRANSITION_OFFSET + 8
TRANSITION_TERMINAL_OFFSET: Final = TRANSITION_OFFSET + 24
TRANSITION_RESERVED_OFFSET: Final = TRANSITION_OFFSET + 25
ENERGY_OFFSET: Final = 1800
ENERGY_WIDTH: Final = 16
MATERIAL_OFFSET: Final = 1816
MATERIAL_COUNT: Final = 4
MATERIAL_WIDTH: Final = 8
AGE_OFFSET: Final = 1848
AGE_COUNT: Final = 20
AGE_WIDTH: Final = 4
METADATA_OFFSET: Final = 1928
METADATA_WIDTH: Final = 16
CURSOR_OFFSET: Final = METADATA_OFFSET
COUNTER_OFFSET: Final = METADATA_OFFSET + 5
DEAD_OFFSET: Final = METADATA_OFFSET + 13
ACQUISITION_FAILED_OFFSET: Final = METADATA_OFFSET + 14
OPERATION_FAILED_OFFSET: Final = METADATA_OFFSET + 15
RESERVE_OFFSET: Final = 1944
RESERVE_BITS: Final = 264

ENERGY_BYTE: Final = ENERGY_OFFSET // 8
MATERIAL_BYTE: Final = MATERIAL_OFFSET // 8
RESERVE_BYTE: Final = RESERVE_OFFSET // 8
RESOURCE_START_LANE: Final = ENERGY_OFFSET // LANE_BITS
RESOURCE_END_LANE: Final = AGE_OFFSET // LANE_BITS  # Exclusive.
RESERVE_START_LANE: Final = RESERVE_OFFSET // LANE_BITS
ENERGY_MAX: Final = 65535
MATERIAL_MAX: Final = 255

SYMBOL_ZERO: Final = 0
SYMBOL_ONE: Final = 1
SYMBOL_ERASED: Final = 2
SYMBOL_INVALID: Final = 3

SCRATCH_BYTES: Final = 32
SCRATCH_BITS: Final = SCRATCH_BYTES * 8
SCRATCH_DECODER_OFFSET: Final = 0
SCRATCH_DECODER_BITS: Final = 96
SCRATCH_R0_OFFSET: Final = 96
SCRATCH_R1_OFFSET: Final = 128
SCRATCH_R2_OFFSET: Final = 160
SCRATCH_R3_OFFSET: Final = 192
SCRATCH_REGISTER_BITS: Final = 32
SCRATCH_CONTROL_OFFSET: Final = 224
SCRATCH_PC_OFFSET: Final = 224
SCRATCH_PC_BITS: Final = 16
SCRATCH_ADDRESS_OFFSET: Final = 240
SCRATCH_ADDRESS_BITS: Final = 11
SCRATCH_FLAGS_OFFSET: Final = 251
SCRATCH_FLAGS_BITS: Final = 5


def _integer(value: int, name: str) -> int:
    # bool is an int subclass, but is not an integer encoding in this API.
    if type(value) is not int:
        raise TypeError(f"{name} must be a built-in int, not bool or a coercible value")
    return value


def _index(value: int, count: int, name: str) -> int:
    _integer(value, name)
    if not 0 <= value < count:
        raise ValueError(f"{name} must be in [0, {count})")
    return value


def _range(offset: int, width: int, signed: bool, size_bits: int) -> None:
    _integer(offset, "offset")
    _integer(width, "width")
    if type(signed) is not bool:
        raise TypeError("signed must be bool")
    if not 1 <= width <= MAX_FIELD_BITS:
        raise ValueError("width must be in [1, 32]")
    if offset < 0 or offset > size_bits - width:
        raise ValueError("field is outside the buffer")


def _encoded(value: int, width: int, signed: bool = False) -> int:
    _integer(value, "value")
    lower = -(1 << (width - 1)) if signed else 0
    upper = (1 << (width - 1)) - 1 if signed else (1 << width) - 1
    if not lower <= value <= upper:
        raise ValueError("value is outside the field's representable range")
    return value & ((1 << width) - 1)


def _ram_range(offset: int, width: int, signed: bool) -> None:
    _range(offset, width, signed, STATE_BITS)
    if offset < AGE_OFFSET and offset + width > ENERGY_OFFSET:
        raise PermissionError("typed resource bytes are not RAM")
    if offset + width > RESERVE_OFFSET:
        raise PermissionError("reserve is inaccessible to RAM operations")


def _physical_lane(index: int) -> int:
    _index(index, LANE_COUNT, "lane")
    if RESOURCE_START_LANE <= index < RESOURCE_END_LANE:
        raise PermissionError("resource faults must use typed sinks, not RAM mutation")
    return index * LANE_BITS


def _read(buffer: bytearray, offset: int, width: int, signed: bool = False) -> int:
    start = offset // 8
    stop = (offset + width + 7) // 8
    value = (int.from_bytes(buffer[start:stop], "little") >> (offset % 8))
    value &= (1 << width) - 1
    if signed and value & (1 << (width - 1)):
        value -= 1 << width
    return value


def _write(buffer: bytearray, offset: int, width: int, encoded: int) -> None:
    start = offset // 8
    stop = (offset + width + 7) // 8
    shift = offset % 8
    mask = ((1 << width) - 1) << shift
    current = int.from_bytes(buffer[start:stop], "little")
    replacement = (current & ~mask) | (encoded << shift)
    # Equal-length replacement only: the authoritative buffer never resizes.
    buffer[start:stop] = replacement.to_bytes(stop - start, "little")


def _copy_payload(raw: bytes | bytearray, size: int) -> bytearray:
    if type(raw) not in (bytes, bytearray):
        raise TypeError("payload must be bytes or bytearray")
    if len(raw) != size:
        raise ValueError(f"payload must contain exactly {size} bytes")
    return bytearray(raw)


@final
class State:
    """One authoritative fixed-size persistent buffer; no other instance fields.

    ``raw`` is copied without sanitizing invalid/reserved bits. Omission creates
    the unpowered canonical image. Field/lane helpers access ordinary RAM only;
    typed stock setters reject overflow (they do not cap or account deposits).
    """

    __slots__ = ("__buffer",)

    def __init__(self, raw: bytes | bytearray | None = None) -> None:
        self.__buffer = (
            bytearray(b"\xaa" * CODE_BYTES + bytes(AUX_BYTES))
            if raw is None else _copy_payload(raw, STATE_BYTES)
        )

    def snapshot(self) -> bytes:
        """Return an immutable raw copy, including invalid and reserve bits.

        This is a trusted serialization codec, not a completed-S certificate;
        the caller must enforce scratch-zero and no-suspended-operation rules.
        """
        return bytes(self.__buffer)

    @staticmethod
    def reset() -> State:
        """Construct fresh canonical state without receiving any source history.

        Does not mutate the old body or cancel external messages, handles,
        scratch, or callbacks. The future boundary supervisor owns that work.
        """
        return State()

    def read_bits(self, offset: int, width: int, signed: bool = False) -> int:
        """Read 1..32 RAM bits; this codec performs no paid service admission."""
        _ram_range(offset, width, signed)
        return _read(self.__buffer, offset, width, signed)

    def write_bits(
        self, offset: int, width: int, value: int, signed: bool = False
    ) -> None:
        """Replace only the named RAM bits, with checked range and no truncation.

        A sub-two-bit codec write preserves neighbors. It is NOT a substitute
        for the interpreter's required paid READ2, merge ALU, and WRITE2.
        """
        _ram_range(offset, width, signed)
        _write(self.__buffer, offset, width, _encoded(value, width, signed))

    get_field = read_bits
    set_field = write_bits

    def read_lane(self, index: int) -> int:
        """Read an ordinary RAM lane as raw 0..3, including invalid code 11."""
        _index(index, LANE_COUNT, "lane")
        return self.read_bits(index * LANE_BITS, LANE_BITS)

    def write_lane(self, index: int, symbol: int) -> None:
        """Write one ordinary RAM lane; no physical resource charge is implied."""
        _index(index, LANE_COUNT, "lane")
        self.write_bits(index * LANE_BITS, LANE_BITS, symbol)

    @property
    def energy(self) -> int:
        """Current packed uint16 E, not a sensor service or shadow balance."""
        return _read(self.__buffer, ENERGY_OFFSET, ENERGY_WIDTH)

    @energy.setter
    def energy(self, value: int) -> None:
        _write(self.__buffer, ENERGY_OFFSET, ENERGY_WIDTH, _encoded(value, ENERGY_WIDTH))

    def read_material(self, index: int) -> int:
        """Read packed P[index] for trusted meter/physics integration only."""
        _index(index, MATERIAL_COUNT, "material index")
        return _read(self.__buffer, MATERIAL_OFFSET + MATERIAL_WIDTH * index, MATERIAL_WIDTH)

    def write_material(self, index: int, value: int) -> None:
        """Assign a checked uint8 stock without silently capping or wrapping."""
        _index(index, MATERIAL_COUNT, "material index")
        encoded = _encoded(value, MATERIAL_WIDTH)
        _write(self.__buffer, MATERIAL_OFFSET + MATERIAL_WIDTH * index, MATERIAL_WIDTH, encoded)

    @property
    def P0(self) -> int:
        return self.read_material(0)

    @P0.setter
    def P0(self, value: int) -> None:
        self.write_material(0, value)

    @property
    def P1(self) -> int:
        return self.read_material(1)

    @P1.setter
    def P1(self, value: int) -> None:
        self.write_material(1, value)

    @property
    def P2(self) -> int:
        return self.read_material(2)

    @P2.setter
    def P2(self, value: int) -> None:
        self.write_material(2, value)

    @property
    def P3(self) -> int:
        return self.read_material(3)

    @P3.setter
    def P3(self, value: int) -> None:
        self.write_material(3, value)

    def _physics_read_lane(self, index: int) -> int:
        """Trusted physics only: raw RAM including reserve, never reservoirs."""
        return _read(self.__buffer, _physical_lane(index), LANE_BITS)

    def _physics_write_lane(self, index: int, symbol: int) -> None:
        """Trusted physics only: replace one RAM lane, including reserve.

        No target, callback, arbitrary buffer, or fault frame is accepted.
        The physics owner computes simultaneous faults from the pre-fault image
        and owns code-specific erasure/flip rules. Resource losses remain typed.
        Python method privacy is NOT a capability boundary or a sandbox.
        """
        offset = _physical_lane(index)
        _write(self.__buffer, offset, LANE_BITS, _encoded(symbol, LANE_BITS))


@final
class Scratch:
    """Separate explicit 256-bit operation scratch, with no persistent owner.

    Call boundary() at each operation/checkpoint/isolation/erasure boundary.
    Scheduling and charging that call belong to the future executor. A dirty
    snapshot is an active audit image, never a resumable boundary checkpoint.
    """

    __slots__ = ("__buffer",)

    def __init__(self, raw: bytes | bytearray | None = None) -> None:
        self.__buffer = (
            bytearray(SCRATCH_BYTES) if raw is None else _copy_payload(raw, SCRATCH_BYTES)
        )

    def snapshot(self) -> bytes:
        return bytes(self.__buffer)

    def read_bits(self, offset: int, width: int, signed: bool = False) -> int:
        _range(offset, width, signed, SCRATCH_BITS)
        return _read(self.__buffer, offset, width, signed)

    def write_bits(
        self, offset: int, width: int, value: int, signed: bool = False
    ) -> None:
        _range(offset, width, signed, SCRATCH_BITS)
        _write(self.__buffer, offset, width, _encoded(value, width, signed))

    get_field = read_bits
    set_field = write_bits

    def clear(self) -> None:
        """Zero every scratch byte in place; no persistent bits are changed."""
        self.__buffer[:] = bytes(SCRATCH_BYTES)

    def boundary(self) -> None:
        """Explicit zero-all boundary hook; not evidence of a paid S service."""
        self.clear()

    def is_zero(self) -> bool:
        return not any(self.__buffer)


def reset() -> State:
    """Return fresh canonical persistent state without accepting history."""
    return State.reset()