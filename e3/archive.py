"""Pure observer-side E3 ABI-9 fixed records with the v0.11 catalog extension.

No files, targets, generators, pickle, worker objects, or mutable execution
state are used. This is a byte codec, not a writer, replay engine, original
execution witness, COMPLETE-manifest certifier, or isolation boundary.
Reserved wire bytes must be zero; opaque persistent/scratch bytes are NEVER
sanitized. Supplied audit flags and hashes remain assertions until externally
checked against original execution and independent whole-phase replay.

``marshal`` / ``unmarshal`` accept a closed record union. References use None
for all-ones absence; zero is a real global ordinal. Directory validation is
structural only for compressed ranges. Snapshot records here are the dense
308-byte form; compact alias/RLE expansion and the remaining ROM/provenance
table codecs are intentionally not implemented.
"""

from dataclasses import dataclass, fields
from enum import IntEnum
import hashlib
import json
import struct
from types import MappingProxyType
from typing import ClassVar, Iterable, Self, TypeAlias, TypeVar, cast


class ArchiveError(ValueError):
    """Invalid encoding, reserved value, unresolved reference, or overflow."""


U64_MAX = (1 << 64) - 1
ABSENT_U32 = (1 << 32) - 1
STATE_BYTES = 276
PHASE_LIMIT = 285616
SNAPSHOT_LIMIT = 3829888
CLASS_LIMIT = 29952
TRUNK_LIMIT = 29696
SCHEDULE_LIMIT = 20480
G_CAPACITY = 512
SHARED_BYTES = 71303168
CORE_CEILING = 8567308288
EXTENSION_CEILING = 28263424
ARCHIVE_CEILING = 8595571712


class Table(IntEnum):
    TICK = 0
    RESPONSE = 1
    SNAPSHOT = 2
    RESET_AUDIT = 3
    SUMMARY = 4
    LESSON = 5
    COMMIT = 6
    TEMPLATE = 7
    SCHEDULE = 8
    PHASE = 9
    CLASS = 10
    TRACE_COMMITMENT = 11
    G = 12
    PROVENANCE = 13


class Codec(IntEnum):
    DENSE = 0
    DEAD_RLE = 1
    EXACT_ALIAS = 2


class Lifecycle(IntEnum):
    LIVE = 0
    DEAD_AT_ENTRY = 1
    MINIMUM_DEATH = 2
    FINAL_LEAK_DEATH = 3


class PathStatus(IntEnum):
    UNREACHED = 0
    REJECTED_OR_INELIGIBLE = 1
    COMPLETE = 2
    PAID_PREFIX_STOP = 3


class ResponseStatus(IntEnum):
    UNREACHED = 0
    EMITTED_0 = 1
    EMITTED_1 = 2
    INVALID_SLOT = 3
    DECODE_REJECTED = 4
    MINIMUM_DEATH = 5
    DEAD_ENTRY = 6


class LessonStatus(IntEnum):
    DEAD_ENTRY = 0
    MINIMUM_DEATH = 1
    OUTER_REJECT = 2
    COMPLETE = 3
    PAID_PREFIX_STOP = 4


class CommitStatus(IntEnum):
    DEAD_ENTRY = 0
    MINIMUM_DEATH = 1
    INVALID_STAGING = 2
    ENCODING_REJECTED = 3
    COMPLETE = 4
    PAID_PREFIX_STOP = 5


class BoundaryKind(IntEnum):
    CANONICAL = 0
    ACTIVATION = 1
    RAW_FORK = 2
    FULL_SOURCE_ENTRY = 3
    ISOLATE = 4
    LESION = 5
    INTERVENTION = 6
    TICK_ANCHOR = 7
    PHASE_END = 8
    SHUTDOWN = 9
    PRE_TEMPLATE_SUPPLY = 10
    POST_TEMPLATE = 11
    EXACT_CODE_ASSERTION = 12
    RESET_CANONICAL = 13
    RESET_ACTIVATION = 14


class EventKind(IntEnum):
    CONTROL = 0
    KERNEL = 1
    READ2 = 2
    WRITE2 = 3
    SCALAR_IN = 4
    SCALAR_OUT = 5
    METER = 6
    C = 7
    S = 8
    SENSE = 9
    ATTEMPT = 10
    TRANSPORT = 11
    LIVING = 12
    RENT = 13
    DUES = 14
    MINIMUM_FAIL = 15
    PASSIVE = 16
    FAULT_BOUNDARY = 17
    BOUNDARY = 18


class Product(IntEnum):
    TRUNK = 0
    SCREEN = 1
    SELECTED_CONTROL = 2
    CORE = 3
    LL13 = 4
    FLIP = 5
    HUB = 6
    RESOURCE = 7
    G_DIAG = 8
    HS_REFERENCE = 9
    MIXED = 10
    RESET = 11
    ORACLE = 12
    SCRIPTED = 13


class Policy(IntEnum):
    RL = 0
    PERIODIC = 1
    THRESHOLD = 2
    DRIVE = 3
    FROZEN = 4
    SCRIPT_U = 5
    SCRIPT_ALL = 6


TABLE_WIDTHS = MappingProxyType(dict(enumerate(
    (48, 8, 308, 64, 512, 8, 4, 64, 1312, 64, 32, 48, 128, 128))))
TABLE_LIMITS = MappingProxyType(dict(enumerate(
    (129700128, 111718400, SNAPSHOT_LIMIT, 225712, PHASE_LIMIT,
     7602176, 950272, 160, SCHEDULE_LIMIT, PHASE_LIMIT, CLASS_LIMIT,
     PHASE_LIMIT, G_CAPACITY, 54))))
CORE_COUNTS = MappingProxyType({
    "ticks": 129338400, "responses": 111393280, "summaries": 284592,
    "maximum_snapshots": 3818368, "source_reset_audits": 225200,
    "canonical_future_roster": 29696, "paid_isolate_slots": 254896,
    "offered_controllers": 94633984, "planned_outer_services": 3311370832,
    "teaching_rows": 7602176, "block_commit_slots": 950272,
    "privileged_templates": 160,
})
COMBINED_COUNTS = MappingProxyType({
    "ticks": 129700128, "responses": 111718400, "summaries": 285616,
    "maximum_snapshots": 3829888, "source_reset_audits": 225712,
    "canonical_future_roster": 29952, "paid_isolate_slots": 255920,
    "offered_controllers": 94928896, "planned_outer_services": 3320673872,
    "teaching_rows": 7602176, "block_commit_slots": 950272,
    "privileged_templates": 160,
})
EXTENSION_COUNTS = MappingProxyType({
    name: count - CORE_COUNTS[name] for name, count in COMBINED_COUNTS.items()
})


def _int(value: object, name: str, low: int = 0, high: int = U64_MAX) -> int:
    if type(value) is not int or not low <= value <= high:
        raise ArchiveError(f"{name} must be a built-in integer in {low}..{high}")
    return value


_EnumT = TypeVar("_EnumT", bound=IntEnum)


def _enum(value: object, enum: type[_EnumT], name: str) -> _EnumT:
    if type(value) not in (int, enum):
        raise ArchiveError(f"{name} must use its declared enum")
    try:
        return enum(cast(int, value))  # Exact int/declared IntEnum checked above.
    except ValueError:
        raise ArchiveError(f"unknown {name}") from None


def _bytes(value: object, size: int, name: str = "payload") -> bytes:
    if type(value) is not bytes or len(value) != size:
        raise ArchiveError(f"{name} must be exactly {size} immutable bytes")
    return value


def _vector(value: object, size: int = 5, high: int = U64_MAX,
            name: str = "vector") -> tuple[int, ...]:
    if type(value) is not tuple or len(value) != size:
        raise ArchiveError(f"{name} must be an immutable {size}-tuple")
    for item in value:
        _int(item, name, high=high)
    return cast(tuple[int, ...], value)  # Tuple shape and every integer validated.


def _ref(value: int | None, limit: int, name: str = "reference") -> int | None:
    if value is not None:
        _int(value, name, high=limit - 1)
    return value


def _wire_ref(value: int | None, width: int = 32) -> int:
    return (1 << width) - 1 if value is None else value


def _read_ref(value: int, width: int = 32) -> int | None:
    return None if value == (1 << width) - 1 else value


def checked_sum(values: Iterable[int]) -> int:
    """Stream an exact uint64 sum; no wrapping, saturation, floats, or bools."""
    total = 0
    for value in values:
        total += _int(value, "summand")
        if total > U64_MAX:
            raise ArchiveError("uint64 aggregate overflow")
    return total


def _product(a: int, b: int) -> int:
    result = _int(a, "factor") * _int(b, "factor")
    return _int(result, "uint64 product")


def validate_row_range(table: Table | int, first_row: int, count: int) -> None:
    """Check global ordinals without allocating or visiting the represented rows."""
    table = _enum(table, Table, "table")
    _int(first_row, "first_row", high=TABLE_LIMITS[table] - 1)
    _int(count, "logical_count")
    if checked_sum((first_row, count)) > TABLE_LIMITS[table]:
        raise ArchiveError("range exceeds the combined table catalog")


def _vaw(v: int, a: int, w: int) -> None:
    for name, value in (("V", v), ("A", a), ("W", w)):
        _int(value, name, high=20)
    if not w <= a <= v:
        raise ArchiveError("require 0 <= W <= A <= V <= 20")


def _pack_bits(values: Iterable[int], widths: Iterable[int]) -> int:
    result = offset = 0
    for value, width in zip(values, widths, strict=True):
        result |= int(value) << offset
        offset += width
    return result


def _unpack_bits(value: int, widths: Iterable[int]) -> tuple[int, ...]:
    result = []
    for width in widths:
        result.append(value & ((1 << width) - 1))
        value >>= width
    return tuple(result)


class _Record:
    __slots__ = ()
    SIZE: ClassVar[int]

    def _validate(self) -> None:
        raise NotImplementedError

    def _encode(self) -> bytes:
        raise NotImplementedError

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        del raw  # Only concrete record classes have a payload layout.
        raise NotImplementedError

    def __post_init__(self) -> None:
        self._validate()


_RecordT = TypeVar("_RecordT", bound=_Record)
_Int4: TypeAlias = tuple[int, int, int, int]
_Int5: TypeAlias = tuple[int, int, int, int, int]
_Int8: TypeAlias = tuple[int, int, int, int, int, int, int, int]


@dataclass(frozen=True, slots=True)
class Stocks(_Record):
    energy: int
    p0: int
    p1: int
    p2: int
    p3: int
    SIZE: ClassVar[int] = 6

    def _validate(self) -> None:
        _int(self.energy, "E", high=65535)
        _vector(self.values[1:], 4, 255, "P")

    @property
    def values(self) -> _Int5:
        return self.energy, self.p0, self.p1, self.p2, self.p3

    def _encode(self) -> bytes:
        return struct.pack("<H4B", *self.values)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        return cls(*cast(_Int5, struct.unpack("<H4B", raw)))


def _stocks(value: object) -> None:
    if type(value) is not Stocks:
        raise ArchiveError("stocks must be a Stocks record")
    value._validate()


@dataclass(frozen=True, slots=True)
class ResponseRecord(_Record):
    actual_cue: int
    status: ResponseStatus | int
    raw_slot: int
    target: int
    correct: int
    u: int
    o: int
    usefulness: int
    routing_match: int
    endpoint: int
    planned_due: int
    learner_b: int
    ecological_yield: int
    b_present: int
    yield_present: int
    guessed: int
    slot_read: int
    alive_before: int
    alive_after: int
    active_tick: int
    record_finalized: int
    scheduled_cue: int
    SIZE: ClassVar[int] = 8

    def _validate(self) -> None:
        _enum(self.status, ResponseStatus, "response status")
        for name in ("actual_cue", "scheduled_cue"):
            _int(getattr(self, name), name, high=15)
        _int(self.raw_slot, "raw slot", high=255)
        for name in _RESPONSE_BITS + _RESPONSE_FLAGS:
            _int(getattr(self, name), name, high=1)
        _int(self.learner_b, "learner b", -64, 64)
        if self.learner_b not in (-64, 0, 64):
            raise ArchiveError("learner b is -64, 0, or 64")
        _int(self.ecological_yield, "ecological yield", high=64)
        if self.ecological_yield not in (0, 64):
            raise ArchiveError("ecological yield is 0 or 64")
        if not self.b_present and self.learner_b:
            raise ArchiveError("absent b must be zero")
        if not self.yield_present and self.ecological_yield:
            raise ArchiveError("absent yield must be zero")
        if not self.slot_read and (self.raw_slot or self.actual_cue or self.routing_match):
            raise ArchiveError("unread slot fields must be zero")
        emitted = self.status in (1, 2)
        if not emitted and (self.correct or self.b_present or self.yield_present or self.guessed):
            raise ArchiveError("missing response cannot have correctness or received feedback")
        if emitted and not self.slot_read:
            raise ArchiveError("emission requires a fully read slot")
        if self.slot_read and self.routing_match != int(self.actual_cue == self.scheduled_cue):
            raise ArchiveError("routing-match disagrees with actual/scheduled cues")
        if emitted and self.correct != int(int(self.status) - 1 == self.target):
            raise ArchiveError("correct bit disagrees with emitted bit and scheduled target")
        if self.u and self.o:
            raise ArchiveError("U and O are disjoint")
        if self.planned_due != 1:
            raise ArchiveError("response table contains planned due rows only")

    def _encode(self) -> bytes:
        truth = _pack_bits(tuple(getattr(self, n) for n in _RESPONSE_BITS), (1,) * 8)
        flags = _pack_bits(tuple(getattr(self, n) for n in _RESPONSE_FLAGS), (1,) * 8)
        return struct.pack("<BBBhBBB", self.actual_cue | int(self.status) << 4,
                           self.raw_slot, truth, self.learner_b,
                           self.ecological_yield, flags, self.scheduled_cue)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        cue, slot, truth, b, income, flags, scheduled = cast(
            tuple[int, ...], struct.unpack("<BBBhBBB", raw))
        # Each fixed width list produces exactly eight integer fields.
        truth_bits = cast(_Int8, _unpack_bits(truth, (1,) * 8))
        flag_bits = cast(_Int8, _unpack_bits(flags, (1,) * 8))
        return cls(cue & 15, cue >> 4, slot, *truth_bits, b, income, *flag_bits, scheduled)


_RESPONSE_BITS = ("target", "correct", "u", "o", "usefulness", "routing_match",
                  "endpoint", "planned_due")
_RESPONSE_FLAGS = ("b_present", "yield_present", "guessed", "slot_read",
                   "alive_before", "alive_after", "active_tick", "record_finalized")


@dataclass(frozen=True, slots=True)
class TickCapsule(_Record):
    outer_ordinal: int
    lifecycle: Lifecycle | int
    funded_tick: int
    v: int
    a: int
    w: int
    action: int
    td: int
    stored_terminal: int
    decide_admitted: int
    eligibility: int
    old_valid: int
    source: int
    new_store: int
    offer_consumed: int
    correct_writes: int
    raw_due_slot: int
    decode: int
    emission: int
    record_finalized: int
    admit: PathStatus | int
    lesson: PathStatus | int
    commit: PathStatus | int
    terminal: int
    decoded_payload: int
    health: int
    e_bin: int
    p_bin: int
    guessed: int
    action_admitted: int
    condition_mask: int
    age_mask: int
    incorrect_writes: int
    offered_cue: int
    offer_usefulness: int
    action_return: int
    accepted_yield: int
    SIZE: ClassVar[int] = 16

    def _validate(self) -> None:
        _int(self.outer_ordinal, "outer ordinal", high=31)
        if 27 <= self.outer_ordinal < 31:
            raise ArchiveError("unassigned outer ordinal")
        _enum(self.lifecycle, Lifecycle, "lifecycle")
        for names, widths in _CAPSULE_GROUPS:
            for name, width in zip(names, widths, strict=True):
                if name in ("admit", "lesson", "commit"):
                    _enum(getattr(self, name), PathStatus, name)
                else:
                    _int(getattr(self, name), name, high=(1 << width) - 1)
        _int(self.funded_tick, "funded tick", high=1)
        _vaw(self.v, self.a, self.w)
        if self.correct_writes + self.incorrect_writes != self.w:
            raise ArchiveError("correct plus incorrect writes must equal W")
        if self.decode > 5 or self.emission > 2:
            raise ArchiveError("reserved decode/emission")
        if not self.decide_admitted and (self.health or self.e_bin or self.p_bin):
            raise ArchiveError("controller observations require admitted DECIDE")
        _int(self.action_return, "action return", -32768, 32767)
        _int(self.accepted_yield, "accepted yield", high=64 if self.action == 0 else 8)
        if not self.action_admitted and self.accepted_yield:
            raise ArchiveError("accepted yield requires admitted action")
        if self.action == 3 and self.action_admitted:
            raise ArchiveError("absent action cannot be admitted")
        if self.action in (2, 3) and self.accepted_yield:
            raise ArchiveError("scrub/absent action has no resource yield")
        if self.action == 3 and self.action_return:
            raise ArchiveError("absent action return must be zero")
        if not self.offer_consumed and (self.offered_cue or self.offer_usefulness):
            raise ArchiveError("absent offer fields must be zero")

    def validate_action_return(self, objective: int) -> None:
        """Check with an explicit immutable-G objective: main=0, DRIVE=1.

        The capsule has no objective field. Do not reject legitimate DRIVE
        returns by assuming every row uses the main accepted-income objective.
        """
        self._validate()
        _int(objective, "objective", high=1)
        if objective == 1:
            expected = 16 if self.action == 2 else 0
        else:
            expected = (self.accepted_yield // 4 if self.action == 0 else
                        2 * self.accepted_yield if self.action == 1 else
                        -self.w if self.action == 2 else 0)
        if self.action_return != expected:
            raise ArchiveError("action return disagrees with G objective and realized work")

    def _encode(self) -> bytes:
        words = [_pack_bits(tuple(getattr(self, name) for name in names), widths)
                 for names, widths in _CAPSULE_GROUPS]
        return struct.pack("<BIIIhB", self.outer_ordinal | int(self.lifecycle) << 5 |
                           self.funded_tick << 7, *words, self.action_return, self.accepted_yield)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        head, x, y, z, ret, income = cast(tuple[int, ...], struct.unpack("<BIIIhB", raw))
        values = sum((_unpack_bits(word, group[1]) for word, group in
                      zip((x, y, z), _CAPSULE_GROUPS, strict=True)), ())
        # The frozen groups contain 13 + 14 + 5 fields, in constructor order.
        packed_fields = cast(tuple[
            int, int, int, int, int, int, int, int, int, int, int, int, int,
            int, int, int, int, int, int, int, int, int, int, int, int, int, int,
            int, int, int, int, int], values)
        return cls(head & 31, (head >> 5) & 3, head >> 7, *packed_fields, ret, income)


_CAPSULE_GROUPS = (
    (("v", "a", "w", "action", "td", "stored_terminal", "decide_admitted",
      "eligibility", "old_valid", "source", "new_store", "offer_consumed", "correct_writes"),
     (5, 5, 5, 2, 2, 1, 1, 1, 1, 2, 1, 1, 5)),
    (("raw_due_slot", "decode", "emission", "record_finalized", "admit", "lesson",
      "commit", "terminal", "decoded_payload", "health", "e_bin", "p_bin", "guessed",
      "action_admitted"), (8, 3, 2, 1, 2, 2, 2, 2, 4, 2, 1, 1, 1, 1)),
    (("condition_mask", "age_mask", "incorrect_writes", "offered_cue", "offer_usefulness"),
     (20, 2, 5, 4, 1)),
)


@dataclass(frozen=True, slots=True)
class TickRecord(_Record):
    state_sha256: bytes
    capsule: TickCapsule
    SIZE: ClassVar[int] = 48

    def _validate(self) -> None:
        _bytes(self.state_sha256, 32, "state SHA256")
        if type(self.capsule) is not TickCapsule:
            raise ArchiveError("tick requires a TickCapsule")
        self.capsule._validate()

    def _encode(self) -> bytes:
        return self.state_sha256 + self.capsule._encode()

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        return cls(raw[:32], TickCapsule._decode(raw[32:]))

    @classmethod
    def from_state(cls, state: bytes, capsule: TickCapsule) -> Self:
        return cls(hashlib.sha256(_bytes(state, 276)).digest(), capsule)

    def verify_state(self, state: bytes) -> None:
        if self.state_sha256 != hashlib.sha256(_bytes(state, 276)).digest():
            raise ArchiveError("tick state hash mismatch")


@dataclass(frozen=True, slots=True)
class SnapshotRecord(_Record):
    phase: int
    tick: int
    kind: BoundaryKind | int
    lifecycle: Lifecycle | int
    ordinal: int
    next_service: int
    flags: int
    payload_ref: int | None
    context_row: int | None
    boundary_rule: int
    payload_offset: int
    payload: bytes
    SIZE: ClassVar[int] = 308

    def _validate(self) -> None:
        _int(self.phase, "phase", high=PHASE_LIMIT - 1)
        _int(self.tick, "tick", high=2048)
        _enum(self.kind, BoundaryKind, "boundary kind")
        _enum(self.lifecycle, Lifecycle, "lifecycle")
        _int(self.ordinal, "ordinal", high=65535)
        _int(self.next_service, "next service", high=255)
        if self.next_service not in (*range(13), 254, 255):
            raise ArchiveError("unknown next service")
        _int(self.flags, "snapshot flags", high=3)
        _ref(self.payload_ref, SNAPSHOT_LIMIT, "payload ref")
        _ref(self.context_row, PHASE_LIMIT, "context row")
        _int(self.boundary_rule, "boundary rule", high=14)
        _int(self.payload_offset, "payload offset")
        checked_sum((self.payload_offset, 276))
        _bytes(self.payload, 276)
        if self.flags & 1 and self.payload_ref is None:
            raise ArchiveError("alias requires a payload reference")

    def _encode(self) -> bytes:
        return struct.pack("<IHBBHBBIIIQ", self.phase, self.tick, self.kind, self.lifecycle,
                           self.ordinal, self.next_service, self.flags,
                           _wire_ref(self.payload_ref), _wire_ref(self.context_row),
                           self.boundary_rule, self.payload_offset) + self.payload

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        phase, tick, kind, lifecycle, ordinal, next_service, flags, payload_ref, context_row, rule, offset = cast(
            tuple[int, ...], struct.unpack("<IHBBHBBIIIQ", raw[:32]))
        return cls(phase, tick, kind, lifecycle, ordinal, next_service, flags,
                   _read_ref(payload_ref), _read_ref(context_row), rule, offset, raw[32:])


@dataclass(frozen=True, slots=True)
class ResetAuditRecord(_Record):
    source_phase: int
    source_snapshot: int
    canonical_snapshot: int
    activation_snapshot: int
    class_id: int
    representative_recovery_phase: int | None
    source_lifecycle: Lifecycle | int
    checks: int
    ordinal: int
    source_sha256: bytes
    SIZE: ClassVar[int] = 64

    def _validate(self) -> None:
        _int(self.source_phase, "source phase", high=PHASE_LIMIT - 1)
        for name in ("source_snapshot", "canonical_snapshot", "activation_snapshot"):
            _int(getattr(self, name), name, high=SNAPSHOT_LIMIT - 1)
        _int(self.class_id, "class", high=CLASS_LIMIT - 1)
        _ref(self.representative_recovery_phase, PHASE_LIMIT)
        _enum(self.source_lifecycle, Lifecycle, "source lifecycle")
        _int(self.checks, "checks", high=127)
        _int(self.ordinal, "ordinal", high=ABSENT_U32)
        _bytes(self.source_sha256, 32, "source SHA256")

    def require_complete_checks(self) -> None:
        """Check asserted bits only; cannot prove cancellation or actual-source work."""
        self._validate()
        if self.checks != 127:
            raise ArchiveError("all seven reset audit checks are required")

    def _encode(self) -> bytes:
        return struct.pack("<6IBB2xI32s", self.source_phase, self.source_snapshot,
                           self.canonical_snapshot, self.activation_snapshot, self.class_id,
                           _wire_ref(self.representative_recovery_phase), self.source_lifecycle,
                           self.checks, self.ordinal, self.source_sha256)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        source, snapshot, canonical, activation, class_id, recovery, lifecycle, checks, ordinal, digest = cast(
            tuple[int, int, int, int, int, int, int, int, int, bytes],
            struct.unpack("<6IBB2xI32s", raw))
        return cls(source, snapshot, canonical, activation, class_id, _read_ref(recovery),
                   lifecycle, checks, ordinal, digest)


@dataclass(frozen=True, slots=True)
class LessonRecord(_Record):
    scheduled_cue: int
    received_label: int
    status: LessonStatus | int
    v: int
    a: int
    w: int
    staging_before: int
    staging_after: int
    flags: int
    SIZE: ClassVar[int] = 8

    def _validate(self) -> None:
        _int(self.scheduled_cue, "scheduled cue", high=15)
        _int(self.received_label, "received label", high=1)
        _enum(self.status, LessonStatus, "lesson status")
        _vaw(self.v, self.a, self.w)
        _int(self.staging_before, "staging before", high=255)
        _int(self.staging_after, "staging after", high=255)
        _int(self.flags, "lesson flags", high=63)
        if not self.flags & 2 and self.received_label:
            raise ArchiveError("absent label must be zero")
        if not self.flags & 4 and self.staging_before:
            raise ArchiveError("unread staging must be zero")
        if not self.flags & 8 and self.staging_after:
            raise ArchiveError("unwritten staging must be zero")

    def _encode(self) -> bytes:
        return struct.pack("<BBBHBBB", self.scheduled_cue, self.received_label, self.status,
                           self.v | self.a << 5 | self.w << 10,
                           self.staging_before, self.staging_after, self.flags)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        cue, label, status, packed, before, after, flags = cast(
            tuple[int, ...], struct.unpack("<BBBHBBB", raw))
        v, a, w = _unpack_bits(packed, (5, 5, 5))
        return cls(cue, label, status, v, a, w, before, after, flags)


@dataclass(frozen=True, slots=True)
class CommitRecord(_Record):
    raw_staging: int
    status: CommitStatus | int
    v: int
    a: int
    w: int
    staging_read: int
    SIZE: ClassVar[int] = 4

    def _validate(self) -> None:
        _int(self.raw_staging, "raw staging", high=255)
        _enum(self.status, CommitStatus, "COMMIT status")
        _vaw(self.v, self.a, self.w)
        _int(self.staging_read, "staging read", high=1)
        if not self.staging_read and self.raw_staging:
            raise ArchiveError("unread staging must be zero")

    def _encode(self) -> bytes:
        return struct.pack("<BBH", self.raw_staging, self.status,
                           self.v | self.a << 5 | self.w << 10 | self.staging_read << 15)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        staging, status, packed = cast(tuple[int, ...], struct.unpack("<BBH", raw))
        return cls(staging, status, *cast(_Int4, _unpack_bits(packed, (5, 5, 5, 1))))


@dataclass(frozen=True, slots=True)
class TemplateRecord(_Record):
    phase: int
    ordinal: int
    status: LessonStatus | int
    code: int
    cue: int
    payload: int
    v: int
    a: int
    w: int
    flags: int
    executed_c: int
    pre_stocks: Stocks
    post_stocks: Stocks
    scalar_presence: int
    paid_energy: int
    paid_material: tuple[int, int, int, int]
    event_count: int
    visited_mask: int
    written_mask: int
    SIZE: ClassVar[int] = 64

    def _validate(self) -> None:
        _int(self.phase, "phase", high=PHASE_LIMIT - 1)
        _int(self.ordinal, "ordinal", high=65535)
        _enum(self.status, LessonStatus, "template status")
        _int(self.code, "code", high=1)
        _int(self.cue, "cue", high=15)
        _int(self.payload, "template payload", high=15)
        # Width-valid semantic BAD packets belong to technical failure evidence;
        # validating their legality needs the paid harness, not masking here.
        _vaw(self.v, self.a, self.w)
        if self.v > (5 if self.code == 0 else 20):
            raise ArchiveError("template V exceeds its code width")
        _int(self.flags, "template flags", high=3)
        _int(self.executed_c, "executed C", high=256)
        _stocks(self.pre_stocks)
        _stocks(self.post_stocks)
        _int(self.scalar_presence, "scalar presence", high=3)
        if not self.scalar_presence & 1 and self.cue:
            raise ArchiveError("absent template cue must be zero")
        if not self.scalar_presence & 2 and self.payload:
            raise ArchiveError("absent template payload must be zero")
        _int(self.paid_energy, "paid energy")
        _vector(self.paid_material, 4, 65535, "paid material")
        _int(self.event_count, "event count")
        # The field widths are frozen; local/global mask-coordinate semantics
        # are not explicitly defined in v0.9. Do not invent a bit-to-cell map.
        _int(self.visited_mask, "visited mask", high=ABSENT_U32)
        _int(self.written_mask, "written mask", high=ABSENT_U32)

    def _encode(self) -> bytes:
        return (struct.pack("<IH8BH", self.phase, self.ordinal, self.status, self.code,
                            self.cue, self.payload, self.v, self.a, self.w, self.flags,
                            self.executed_c) + self.pre_stocks._encode() + self.post_stocks._encode()
                + struct.pack("<H2xQ4HQII", self.scalar_presence, self.paid_energy,
                              *self.paid_material, self.event_count,
                              self.visited_mask, self.written_mask))

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        head = cast(tuple[int, int, int, int, int, int, int, int, int, int, int],
                    struct.unpack("<IH8BH", raw[:16]))
        scalar, energy, p0, p1, p2, p3, count, visited, written = cast(
            tuple[int, ...], struct.unpack("<H2xQ4HQII", raw[28:]))
        return cls(*head, Stocks._decode(raw[16:22]), Stocks._decode(raw[22:28]),
                   scalar, energy, (p0, p1, p2, p3), count, visited, written)


@dataclass(frozen=True, slots=True)
class SummaryCounters(_Record):
    planned_ticks: int
    entered_ticks: int
    active_ticks: int
    planned_responses: int
    emitted_responses: int
    correct_responses: int
    endpoint_u_planned: int
    endpoint_u_correct: int
    endpoint_o_planned: int
    endpoint_o_correct: int
    completed_code_writes: int
    target_correct_code_writes: int
    target_incorrect_code_writes: int
    q_lane_writes: int
    age_lane_writes: int
    condition_age_lane_writes: int
    other_ram_lane_writes: int
    admitted_conditioners: int
    executed_c_a: int
    executed_c_b: int
    executed_other_c: int
    paid_c_a_envelopes: int
    paid_c_b_envelopes: int
    paid_other_c_envelopes: int
    paid_debits: tuple[int, ...]
    accepted_passive_grants: tuple[int, ...]
    accepted_action_income: tuple[int, ...]
    physical_losses: tuple[int, ...]
    external_removed: tuple[int, ...]
    external_supplied: tuple[int, ...]
    ecological_offered_e: int
    ecological_accepted_e: int
    ecological_overflow_e: int
    external_dispatch_energy: int
    forage_offered_e: int
    collect_offered_material: int
    admitted_terminal_td: int
    paid_code_prefix_stops: int
    SIZE: ClassVar[int] = 496

    def _validate(self) -> None:
        for i, field in enumerate(fields(self)):
            value = getattr(self, field.name)
            if 24 <= i < 30:
                _vector(value, name=field.name)
            else:
                _int(value, field.name)

    @property
    def values(self) -> tuple[int, ...]:
        return tuple(value for field in fields(self)
                     for value in (getattr(self, field.name) if type(getattr(self, field.name)) is tuple
                                   else (getattr(self, field.name),)))

    @classmethod
    def from_values(cls, values: tuple[int, ...]) -> Self:
        _vector(values, 62, name="summary counters")
        # These fixed shapes are trusted only after the 62-integer validation.
        head = cast(tuple[
            int, int, int, int, int, int, int, int, int, int, int, int,
            int, int, int, int, int, int, int, int, int, int, int, int], values[:24])
        tail = cast(_Int8, values[54:])
        return cls(*head, values[24:29], values[29:34], values[34:39], values[39:44],
                   values[44:49], values[49:54], *tail)

    def _encode(self) -> bytes:
        return struct.pack("<62Q", *self.values)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        return cls.from_values(cast(tuple[int, ...], struct.unpack("<62Q", raw)))

    def padding(self) -> tuple[int, ...]:
        result = tuple(_product(256, envelopes) - instructions for envelopes, instructions in
                       zip(self.values[21:24], self.values[18:21], strict=True))
        if any(value < 0 for value in result):
            raise ArchiveError("executed C exceeds paid envelope capacity")
        return result


SUMMARY_COUNTER_NAMES = tuple(
    name for i, field in enumerate(fields(SummaryCounters))
    for name in (tuple(f"{field.name}_{source}" for source in ("e", "p0", "p1", "p2", "p3"))
                 if 24 <= i < 30 else (field.name,)))


@dataclass(frozen=True, slots=True)
class SummaryRecord(_Record):
    start_stocks: Stocks
    end_stocks: Stocks
    lifecycle: Lifecycle | int
    flags: int
    counters: SummaryCounters
    SIZE: ClassVar[int] = 512

    def _validate(self) -> None:
        _stocks(self.start_stocks)
        _stocks(self.end_stocks)
        _enum(self.lifecycle, Lifecycle, "lifecycle")
        _int(self.flags, "summary flags", high=15)
        if type(self.counters) is not SummaryCounters:
            raise ArchiveError("summary needs exactly the frozen 62 counters")
        self.counters._validate()

    def _encode(self) -> bytes:
        return (self.start_stocks._encode() + self.end_stocks._encode()
                + struct.pack("<BB2x", self.lifecycle, self.flags) + self.counters._encode())

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        return cls(Stocks._decode(raw[:6]), Stocks._decode(raw[6:12]), raw[12], raw[13],
                   SummaryCounters._decode(raw[16:]))

    def validate_accounting(self) -> None:
        """Check internal equalities, not truth or original execution provenance."""
        self._validate()
        c = self.counters
        c.padding()
        if not c.correct_responses <= c.emitted_responses <= c.planned_responses:
            raise ArchiveError("response count ordering")
        if not c.active_ticks <= c.entered_ticks <= c.planned_ticks:
            raise ArchiveError("tick count ordering")
        if (c.endpoint_u_correct > c.endpoint_u_planned or
                c.endpoint_o_correct > c.endpoint_o_planned):
            raise ArchiveError("endpoint correct exceeds planned")
        if checked_sum((c.target_correct_code_writes, c.target_incorrect_code_writes)) != c.completed_code_writes:
            raise ArchiveError("code-write truth totals disagree")
        if checked_sum((c.ecological_accepted_e, c.ecological_overflow_e)) != c.ecological_offered_e:
            raise ArchiveError("ecological offered != accepted + overflow")
        for i, (start, end) in enumerate(zip(self.start_stocks.values, self.end_stocks.values, strict=True)):
            income = checked_sum((start, c.accepted_passive_grants[i], c.accepted_action_income[i],
                                  c.external_supplied[i], c.ecological_accepted_e if i == 0 else 0))
            spend = checked_sum((c.paid_debits[i], c.physical_losses[i], c.external_removed[i], end))
            if income != spend:
                raise ArchiveError(f"source {i} conservation failure")


def sum_counters(counters: Iterable[SummaryCounters]) -> SummaryCounters:
    """Aggregate many original counter records without reservoir-width truncation."""
    totals = [0] * 62
    for item in counters:
        if type(item) is not SummaryCounters:
            raise ArchiveError("expected SummaryCounters")
        item._validate()
        totals = [checked_sum((a, b)) for a, b in zip(totals, item.values, strict=True)]
    return SummaryCounters.from_values(tuple(totals))


@dataclass(frozen=True, slots=True)
class DirectoryEntry(_Record):
    table: Table | int
    codec: Codec | int
    record_bytes: int
    first_row: int
    logical_count: int
    physical_offset: int
    physical_length: int
    sha256: bytes
    SIZE: ClassVar[int] = 72

    def _validate(self) -> None:
        table = _enum(self.table, Table, "table")
        _enum(self.codec, Codec, "codec")
        _int(self.record_bytes, "record width", TABLE_WIDTHS[table], TABLE_WIDTHS[table])
        validate_row_range(table, self.first_row, self.logical_count)
        if not self.logical_count:
            raise ArchiveError("directory ranges must contain records")
        _int(self.physical_offset, "offset")
        _int(self.physical_length, "length")
        checked_sum((self.physical_offset, self.physical_length))
        _bytes(self.sha256, 32, "range SHA256")
        if self.codec == Codec.DENSE and self.physical_length != _product(self.logical_count, self.record_bytes):
            raise ArchiveError("dense physical length must equal count * width")

    def _encode(self) -> bytes:
        return struct.pack("<BBH4Q32s4x", self.table, self.codec, self.record_bytes,
                           self.first_row, self.logical_count, self.physical_offset,
                           self.physical_length, self.sha256)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        return cls(*cast(tuple[int, int, int, int, int, int, int, bytes],
                         struct.unpack("<BBH4Q32s4x", raw)))

    def verify_payload(self, payload: bytes) -> None:
        """Check only this finalized range's bytes, not logical expansion/completeness."""
        self._validate()
        _bytes(payload, self.physical_length)
        if hashlib.sha256(payload).digest() != self.sha256:
            raise ArchiveError("directory payload SHA256 mismatch")


def validate_directory(entries: tuple[DirectoryEntry, ...], physical_size: int) -> None:
    """Validate one shard's bounds/nonoverlapping logical ranges without expansion."""
    _int(physical_size, "physical size")
    if type(entries) is not tuple:
        raise ArchiveError("directory must be an immutable tuple")
    previous: dict[Table | int, int] = {}
    for entry in entries:
        if type(entry) is not DirectoryEntry:
            raise ArchiveError("directory entries must be exact records")
        entry._validate()
        if checked_sum((entry.physical_offset, entry.physical_length)) > physical_size:
            raise ArchiveError("directory range exceeds supplied finalized file size")
    for entry in sorted(entries, key=lambda e: (e.table, e.first_row)):
        if entry.first_row < previous.get(entry.table, 0):
            raise ArchiveError("overlapping logical directory ranges")
        previous[entry.table] = entry.first_row + entry.logical_count


def validate_snapshot_links(snapshot: SnapshotRecord, payloads: dict[int, tuple[int, bytes]],
                            *, phase_count: int, physical_size: int) -> None:
    """Resolve against caller-supplied finalized (offset, bytes), never live objects.

    This does not read a file or establish file authenticity. Absence of an
    actually referenced payload is an error even when its row ID is zero.
    """
    if type(snapshot) is not SnapshotRecord or type(payloads) is not dict:
        raise ArchiveError("require SnapshotRecord and a plain finalized-payload dictionary")
    snapshot._validate()
    _int(phase_count, "phase count", high=PHASE_LIMIT)
    _int(physical_size, "physical size")
    if snapshot.phase >= phase_count or (snapshot.context_row is not None and snapshot.context_row >= phase_count):
        raise ArchiveError("phase/context row is not present")
    for key, value in payloads.items():
        _int(key, "payload row", high=SNAPSHOT_LIMIT - 1)
        if type(value) is not tuple or len(value) != 2:
            raise ArchiveError("payload resolution requires (offset, immutable bytes)")
        _int(value[0], "payload offset")
        _bytes(value[1], 276)
        if checked_sum((value[0], 276)) > physical_size:
            raise ArchiveError("resolved payload lies outside finalized bytes")
    if checked_sum((snapshot.payload_offset, 276)) > physical_size:
        raise ArchiveError("snapshot payload exceeds finalized bytes")
    if snapshot.payload_ref is not None:
        if snapshot.payload_ref not in payloads:
            raise ArchiveError("referenced finalized payload is missing")
        if payloads[snapshot.payload_ref] != (snapshot.payload_offset, snapshot.payload):
            raise ArchiveError("referenced payload bytes/offset disagree")


@dataclass(frozen=True, slots=True)
class PrimitiveEvent(_Record):
    tick: int
    service: int
    outer_ordinal: int
    site: int | None
    kind: EventKind | int
    status: PathStatus | int
    event_index: int
    lane: int | None
    tag: int | None
    width: int
    pre_stocks: Stocks
    post_stocks: Stocks
    raw_before: int
    raw_after: int
    c: tuple[int, ...]
    local_quote: tuple[int, ...]
    tail_quote: tuple[int, ...]
    flow: tuple[int, ...]
    aux: int
    scratch_before: bytes
    scratch_after: bytes
    SIZE: ClassVar[int] = 192

    def _validate(self) -> None:
        _int(self.tick, "tick", high=2048)
        _int(self.service, "service", high=12)
        _int(self.outer_ordinal, "outer ordinal", high=26)
        _ref(self.site, 65535, "site")
        _enum(self.kind, EventKind, "event kind")
        _enum(self.status, PathStatus, "event status")
        _int(self.event_index, "event index", high=ABSENT_U32)
        _ref(self.lane, 1104, "lane")
        _ref(self.tag, 23, "tag")
        _int(self.width, "width", high=32)
        _stocks(self.pre_stocks)
        _stocks(self.post_stocks)
        _int(self.raw_before, "raw before", high=ABSENT_U32)
        _int(self.raw_after, "raw after", high=ABSENT_U32)
        for name in ("c", "local_quote", "tail_quote"):
            _vector(getattr(self, name), high=(1 << 31) - 1, name=name)
        _vector(self.flow, high=ABSENT_U32, name="flow")
        _int(self.aux, "aux", high=ABSENT_U32)
        _bytes(self.scratch_before, 32, "scratch before")
        _bytes(self.scratch_after, 32, "scratch after")
        if self.kind != EventKind.METER and (any(self.local_quote) or any(self.tail_quote)):
            raise ArchiveError("non-METER L/T must be zero")
        if self.kind in (EventKind.READ2, EventKind.WRITE2):
            if self.raw_before > 3 or self.raw_after > 3 or self.lane is None:
                raise ArchiveError("READ2/WRITE2 require actual lane and two-bit symbols")
        if self.kind in (EventKind.SCALAR_IN, EventKind.SCALAR_OUT):
            _int(self.aux, "scalar generation attempt", high=1023)
            if self.tag is None or self.width != _SCALAR_WIDTHS[self.tag]:
                raise ArchiveError("scalar event requires its exact tag width")
            for raw in (self.raw_before, self.raw_after):
                _int(raw, "scalar encoding", high=(1 << self.width) - 1)
                if raw > _SCALAR_MAX[self.tag]:
                    raise ArchiveError("scalar outside its tag range")
                if self.tag == 16 and raw not in (0, 64):
                    raise ArchiveError("yield scalar must be 0/64")
                if self.tag == 17 and raw not in (0, 64, 65472):
                    raise ArchiveError("b scalar must be signed16 -64/0/64")
        elif self.tag is not None:
            raise ArchiveError("non-scalar event tag must be absent")
        if self.kind in (EventKind.C, EventKind.CONTROL) and self.aux > 2:
            raise ArchiveError("C/CONTROL budget must be A/B/other")
        if self.kind == EventKind.S and self.scratch_after != bytes(32):
            raise ArchiveError("completed S must have zero scratch after")
        if self.kind == EventKind.ATTEMPT and (self.raw_before or self.raw_after):
            raise ArchiveError("ATTEMPT raw fields must be zero")
        if self.kind == EventKind.SENSE and (self.raw_before > 0xFFFFFF or self.raw_after):
            raise ArchiveError("invalid SENSE stock packing")
        if self.kind == EventKind.TRANSPORT and self.aux > 1:
            raise ArchiveError("TRANSPORT aux is action/ecological")
        if self.kind == EventKind.BOUNDARY:
            if self.aux >> 16 or (self.aux & 255) > 14 or ((self.aux >> 8) & 255) > 5:
                raise ArchiveError("invalid boundary kind/substep encoding")
            # Whether a particular kind/substep pair is legal depends on the
            # named external boundary rule. No rule interpreter is provided.

    def _encode(self) -> bytes:
        return (struct.pack("<HBBHBBIHBB", self.tick, self.service, self.outer_ordinal,
                            _wire_ref(self.site, 16), self.kind, self.status, self.event_index,
                            _wire_ref(self.lane, 16), _wire_ref(self.tag, 8), self.width)
                + self.pre_stocks._encode() + self.post_stocks._encode()
                + struct.pack("<23I8x", self.raw_before, self.raw_after,
                              *self.c, *self.local_quote, *self.tail_quote, *self.flow, self.aux)
                + self.scratch_before + self.scratch_after)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        tick, service, ordinal, site, kind, status, index, lane, tag, width = cast(
            tuple[int, ...], struct.unpack("<HBBHBBIHBB", raw[:16]))
        v = cast(tuple[int, ...], struct.unpack("<23I8x", raw[28:128]))
        return cls(tick, service, ordinal, _read_ref(site, 16), kind, status, index,
                   _read_ref(lane, 16), _read_ref(tag, 8), width,
                   Stocks._decode(raw[16:22]), Stocks._decode(raw[22:28]),
                   v[0], v[1], v[2:7], v[7:12], v[12:17], v[17:22], v[22], raw[128:160], raw[160:])


_SCALAR_WIDTHS = (16, 8, 8, 8, 8, 5, 16, 8, 1, 2, 4, 6, 16, 8, 1, 1, 16, 16, 4, 4, 1, 4, 4)
_SCALAR_MAX = (65535, 255, 255, 255, 255, 31, 65535, 255, 1, 2, 15, 31,
               64, 8, 1, 1, 64, 65535, 15, 15, 1, 15, 15)


@dataclass(frozen=True, slots=True)
class TraceCommitment(_Record):
    event_count: int
    scalar_count: int
    sha256: bytes
    SIZE: ClassVar[int] = 48

    def _validate(self) -> None:
        _int(self.event_count, "event count")
        _int(self.scalar_count, "scalar count", high=self.event_count)
        _bytes(self.sha256, 32, "trace SHA256")

    def _encode(self) -> bytes:
        return struct.pack("<QQ32s", self.event_count, self.scalar_count, self.sha256)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        return cls(*cast(tuple[int, int, bytes], struct.unpack("<QQ32s", raw)))


def encode_trace_event(event: PrimitiveEvent, *, pre_state: bytes | None = None,
                       post_state: bytes | None = None) -> bytes:
    """Append both exact 276-byte states only for BOUNDARY/FAULT_BOUNDARY."""
    if type(event) is not PrimitiveEvent:
        raise ArchiveError("expected PrimitiveEvent")
    raw = marshal(event)
    if event.kind in (EventKind.BOUNDARY, EventKind.FAULT_BOUNDARY):
        return raw + _bytes(pre_state, 276, "pre-state") + _bytes(post_state, 276, "post-state")
    if pre_state is not None or post_state is not None:
        raise ArchiveError("ordinary event cannot carry persistent attachments")
    return raw


def decode_trace_event(raw: bytes) -> tuple[PrimitiveEvent, bytes | None, bytes | None]:
    """Return (fixed header, pre bytes or None, post bytes or None)."""
    if type(raw) is not bytes or len(raw) not in (192, 744):
        raise ArchiveError("trace event must contain exactly 192 or 744 immutable bytes")
    event = unmarshal(PrimitiveEvent, raw[:192])
    boundary = event.kind in (EventKind.BOUNDARY, EventKind.FAULT_BOUNDARY)
    if len(raw) != (744 if boundary else 192):
        raise ArchiveError("missing or extraneous boundary state bytes")
    return event, raw[192:468] if boundary else None, raw[468:] if boundary else None


def commit_trace(phase: int, g_sha256: bytes, event_bytes: Iterable[bytes]) -> TraceCommitment:
    """Hash supplied ORIGINAL bytes once in order; never clone/re-serialize events.

    No origin claim is made by this helper. A replay digest alone is not original
    evidence. A suffix cannot certify a phase. Input is streamed in bounded memory.
    """
    _int(phase, "phase", high=PHASE_LIMIT - 1)
    _bytes(g_sha256, 32, "G digest")
    digest = hashlib.sha256(b"E3TRACE9" + struct.pack("<I", phase) + g_sha256)
    events = scalars = 0
    previous_tick = None
    expected_index = 0
    for raw in event_bytes:
        event, _, _ = decode_trace_event(raw)
        # Tick zero contains separate off-clock operations; each starts at zero.
        if event.tick != previous_tick or (event.tick == 0 and event.event_index == 0):
            if previous_tick is not None and event.tick < previous_tick:
                raise ArchiveError("trace ticks are out of order")
            expected_index = 0
        if event.event_index != expected_index:
            raise ArchiveError("event index must start at zero and be contiguous within a tick")
        expected_index += 1
        previous_tick = event.tick
        events = checked_sum((events, 1))
        scalars = checked_sum((scalars, int(event.kind in (EventKind.SCALAR_IN, EventKind.SCALAR_OUT))))
        digest.update(raw)
    return TraceCommitment(events, scalars, digest.digest())


def _identity(individual: int, panel: int, cohort: int) -> None:
    _int(cohort, "cohort", high=1)
    _int(panel, "panel", 1, 8)
    _int(individual, "individual", 1 if cohort == 0 else 300, 8 if cohort == 0 else 331)


def _configuration(config: int) -> None:
    _int(config, "public G ID", high=403)  # 404..511 are reserved, not arbitrary G.


@dataclass(frozen=True, slots=True)
class ScheduleRecord(_Record):
    schedule_id: int
    individual: int
    panel: int
    cohort: int
    namespace: int
    phase: int
    length: int
    admission_count: int
    u_mask: int
    o_mask: int
    hub_permutation: int
    flags: int
    cues: tuple[int, ...]
    SIZE: ClassVar[int] = 1312

    def _validate(self) -> None:
        _int(self.schedule_id, "schedule ID", high=SCHEDULE_LIMIT - 1)
        _identity(self.individual, self.panel, self.cohort)
        _int(self.namespace, "namespace", high=34)
        _int(self.phase, "phase", high=4)
        _int(self.length, "length", high=2560)
        _int(self.admission_count, "admission count", high=self.length)
        _int(self.u_mask, "U mask", high=65535)
        _int(self.o_mask, "O mask", high=65535)
        if self.u_mask & self.o_mask:
            raise ArchiveError("U/O masks overlap")
        if self.phase != 4 and (self.u_mask or self.o_mask):
            raise ArchiveError("U/O masks are zero outside ecology")
        _int(self.hub_permutation, "HUB source", high=255)
        if self.hub_permutation not in (0, 1, 2, 3, 255):
            raise ArchiveError("HUB source must be 0..3 or 255 absent")
        _int(self.flags, "schedule flags", high=31)
        if self.flags & 8 and self.flags & 16:
            raise ArchiveError("whole-block and mixed U/O are exclusive")
        _vector(self.cues, self.length, 15, "cues")
        cell = ((self.individual - 1) if self.cohort == 0 else 8 + self.individual - 300) * 8 + self.panel - 1
        if self.schedule_id != 64 * cell + self.namespace:
            raise ArchiveError("schedule ID must be 64*cell+slot in fixed cohort order")
        if self.phase == 0 and (self.length != 256 or self.admission_count != 0):
            raise ArchiveError("acquisition schedule has length 256 and no query admissions")
        if self.namespace == 34 and (self.cohort != 0 or self.phase != 4 or self.length != 512):
            raise ArchiveError("slot 34 is the engineering SCRIPTED ecology schedule")

    def _encode(self) -> bytes:
        packed = bytearray(1280)
        for index, cue in enumerate(self.cues):
            packed[index // 2] |= cue << (4 * (index % 2))
        return struct.pack("<HHBBBB4HBB14x", self.schedule_id, self.individual, self.panel,
                           self.cohort, self.namespace, self.phase, self.length,
                           self.admission_count, self.u_mask, self.o_mask,
                           self.hub_permutation, self.flags) + bytes(packed)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        head = cast(tuple[int, int, int, int, int, int, int, int, int, int, int, int],
                    struct.unpack("<HHBBBB4HBB14x", raw[:32]))
        length = head[6]
        if length > 2560:
            raise ArchiveError("schedule length exceeds its packed capacity")
        cues = tuple((raw[32 + i // 2] >> (4 * (i % 2))) & 15 for i in range(length))
        return cls(*head, cues)


@dataclass(frozen=True, slots=True)
class PhaseDescriptor(_Record):
    phase: int
    parent_phase: int | None
    trunk: int | None
    config: int
    schedule: int | None
    reset_class: int | None
    individual: int
    panel: int
    cohort: int
    code: int
    family: int
    policy: Policy | int
    product: Product | int
    branch: int
    stage: int
    permission: int
    physics: int
    horizon: int
    g: int
    activation: int
    first_snapshot: int | None
    first_tick: int | None
    first_response: int | None
    first_lesson: int | None
    first_commit: int | None
    first_template: int | None
    namespace: int | None
    SIZE: ClassVar[int] = 64

    def _validate(self) -> None:
        _int(self.phase, "phase", high=PHASE_LIMIT - 1)
        _ref(self.parent_phase, PHASE_LIMIT, "parent phase")
        _ref(self.trunk, TRUNK_LIMIT, "trunk")
        _configuration(self.config)
        _ref(self.schedule, SCHEDULE_LIMIT, "schedule")
        _ref(self.reset_class, CLASS_LIMIT, "reset class")
        _identity(self.individual, self.panel, self.cohort)
        _int(self.code, "code", high=1)
        _int(self.family, "family", high=1)
        _enum(self.policy, Policy, "policy")
        _enum(self.product, Product, "product")
        for name, high in (("branch", 13), ("stage", 11), ("permission", 7),
                           ("physics", 2), ("horizon", 2048), ("g", 255), ("activation", 3)):
            _int(getattr(self, name), name, high=high)
        _ref(self.namespace, 35, "namespace")
        for name, table in _PHASE_LINKS:
            _ref(getattr(self, name), TABLE_LIMITS[table], name)
        if (self.schedule is None) != (self.namespace is None):
            raise ArchiveError("schedule and namespace must both be absent or present")
        if self.schedule is not None and self.schedule % 64 != self.namespace:
            raise ArchiveError("schedule slot disagrees with namespace")
        expected = GRecord.from_id(self.config)
        policy = Policy.RL if self.policy == Policy.FROZEN else self.policy
        if (self.code, self.family, policy) != (expected.code, expected.family, expected.policy):
            raise ArchiveError("phase identity disagrees with immutable G")
        if self.policy in (5, 6) and self.cohort != 0:
            raise ArchiveError("scripts are engineering only")

    def _encode(self) -> bytes:
        return struct.pack("<3I2HIH2B8BH2B6I2H", self.phase, _wire_ref(self.parent_phase),
                           _wire_ref(self.trunk), self.config, _wire_ref(self.schedule, 16),
                           _wire_ref(self.reset_class), self.individual, self.panel, self.cohort,
                           self.code, self.family, self.policy, self.product, self.branch,
                           self.stage, self.permission, self.physics, self.horizon, self.g,
                           self.activation, *(_wire_ref(getattr(self, name)) for name, _ in _PHASE_LINKS),
                           _wire_ref(self.namespace, 16), 0)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        v = cast(tuple[int, ...], struct.unpack("<3I2HIH2B8BH2B6I2H", raw)[:-1])
        return cls(v[0], _read_ref(v[1]), _read_ref(v[2]), v[3], _read_ref(v[4], 16),
                   _read_ref(v[5]), v[6], v[7], v[8], v[9], v[10], v[11], v[12],
                   v[13], v[14], v[15], v[16], v[17], v[18], v[19],
                   _read_ref(v[20]), _read_ref(v[21]), _read_ref(v[22]),
                   _read_ref(v[23]), _read_ref(v[24]), _read_ref(v[25]), _read_ref(v[26], 16))


_PHASE_LINKS = (("first_snapshot", Table.SNAPSHOT), ("first_tick", Table.TICK),
                ("first_response", Table.RESPONSE), ("first_lesson", Table.LESSON),
                ("first_commit", Table.COMMIT), ("first_template", Table.TEMPLATE))


def validate_phase_links(phase: PhaseDescriptor,
                         actual_counts: dict[Table, int] | dict[int, int]) -> None:
    """Check present global rows against supplied actual table extents, not capacities."""
    if type(phase) is not PhaseDescriptor or type(actual_counts) is not dict:
        raise ArchiveError("expected exact phase and plain actual-count dictionary")
    phase._validate()
    for table, count in actual_counts.items():
        _enum(table, Table, "table")
        _int(count, "actual count", high=TABLE_LIMITS[table])
    links = (("phase", Table.PHASE), ("parent_phase", Table.PHASE),
             ("schedule", Table.SCHEDULE), ("reset_class", Table.CLASS)) + _PHASE_LINKS
    for name, table in links:
        ref = getattr(phase, name)
        if ref is not None and (table not in actual_counts or ref >= actual_counts[table]):
            raise ArchiveError(f"{name} points to a missing row")


@dataclass(frozen=True, slots=True)
class ClassMapping(_Record):
    class_id: int
    recovery_phase: int
    final_phase: int
    config: int
    recovery_schedule: int
    final_schedule: int
    individual: int
    panel: int
    code: int
    family: int
    flags: int
    trunk: int
    SIZE: ClassVar[int] = 32

    def _validate(self) -> None:
        for name, limit in (("class_id", CLASS_LIMIT), ("recovery_phase", PHASE_LIMIT),
                            ("final_phase", PHASE_LIMIT), ("recovery_schedule", SCHEDULE_LIMIT),
                            ("final_schedule", SCHEDULE_LIMIT), ("trunk", TRUNK_LIMIT)):
            _int(getattr(self, name), name, high=limit - 1)
        _configuration(self.config)
        _int(self.individual, "individual", 1, 331)
        if self.individual not in (*range(1, 9), *range(300, 332)):
            raise ArchiveError("unknown individual")
        _int(self.panel, "panel", 1, 8)
        _int(self.code, "code", high=1)
        _int(self.family, "family", high=1)
        _int(self.flags, "class flags", high=1)

    def _encode(self) -> bytes:
        return struct.pack("<3I4H4BI4x", self.class_id, self.recovery_phase, self.final_phase,
                           self.config, self.recovery_schedule, self.final_schedule, self.individual,
                           self.panel, self.code, self.family, self.flags, self.trunk)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        return cls(*cast(tuple[int, int, int, int, int, int, int, int, int, int, int, int],
                         struct.unpack("<3I4H4BI4x", raw)))


@dataclass(frozen=True, slots=True)
class GRecord(_Record):
    abi: int
    code: int
    policy: Policy | int
    family: int
    p_cut: int
    e_cut: int
    interval: int
    h: int
    objective: int
    ordinary_permission: int
    variant: int
    scalar_rules: int
    route_rules: int
    domain_rules: int
    tail_rules: int
    SIZE: ClassVar[int] = 128

    def _validate(self) -> None:
        _int(self.abi, "ABI", 9, 9)
        _int(self.code, "code", high=1)
        _enum(self.policy, Policy, "G policy")
        if self.policy == Policy.FROZEN:
            raise ArchiveError("FROZEN G must use underlying RL")
        _int(self.family, "family", high=1)
        _int(self.p_cut, "P cut", high=255)
        _int(self.e_cut, "E cut", high=65535)
        if self.p_cut not in (32, 64, 96) or self.e_cut not in (24576, 32768, 40960):
            raise ArchiveError("cuts outside frozen public grid")
        _int(self.interval, "interval", high=256)
        if ((self.policy == Policy.PERIODIC and self.interval not in (1, 2, 4, 8, 16, 32, 64, 128, 256))
                or (self.policy != Policy.PERIODIC and self.interval != 0)):
            raise ArchiveError("invalid policy interval")
        _int(self.h, "h", 3, 3)
        _int(self.objective, "objective", int(self.policy == Policy.DRIVE), int(self.policy == Policy.DRIVE))
        _int(self.ordinary_permission, "ordinary permission", 3, 3)
        _int(self.variant, "variant", self.code, self.code)
        for name in ("scalar_rules", "route_rules", "domain_rules", "tail_rules"):
            _int(getattr(self, name), name, 0, 0)
        if self.policy in (3, 5, 6) and (self.e_cut, self.p_cut) != (32768, 64):
            raise ArchiveError("DRIVE/scripts use default cuts")
        if self.policy in (5, 6) and self.family != 1:
            raise ArchiveError("scripts are H2 catalog configurations")

    def _encode(self) -> bytes:
        return struct.pack("<H4B2H3BxH4I96x", self.abi, self.code, self.policy, self.family,
                           self.p_cut, self.e_cut, self.interval, self.h, self.objective,
                           self.ordinary_permission, self.variant, self.scalar_rules,
                           self.route_rules, self.domain_rules, self.tail_rules)

    @classmethod
    def _decode(cls, raw: bytes) -> Self:
        return cls(*cast(tuple[int, int, int, int, int, int, int, int, int, int,
                              int, int, int, int, int], struct.unpack("<H4B2H3BxH4I96x", raw)))

    @classmethod
    def from_id(cls, config: int) -> Self:
        _configuration(config)
        if config >= 400:
            return cls(9, (config - 400) // 2, 5 + (config - 400) % 2,
                       1, 64, 32768, 0, 3, 0, 3, (config - 400) // 2, 0, 0, 0, 0)
        code, family, k = config // 200, (config // 100) % 2, config % 100
        policy = 0 if k < 9 else 1 if k < 90 else 2 if k < 99 else 3
        pair = k if k < 9 else (k - 9) // 9 if k < 90 else k - 90 if k < 99 else 4
        interval = (1, 2, 4, 8, 16, 32, 64, 128, 256)[(k - 9) % 9] if policy == 1 else 0
        return cls(9, code, policy, family, (32, 64, 96)[pair % 3],
                   (24576, 32768, 40960)[pair // 3], interval, 3, int(policy == 3),
                   3, code, 0, 0, 0, 0)

    def validate_id(self, config: int) -> None:
        self._validate()
        if self != GRecord.from_id(config):
            raise ArchiveError("G record does not match its global public ID")


_SupportedRecord: TypeAlias = (
    Stocks | ResponseRecord | TickCapsule | TickRecord | SnapshotRecord | ResetAuditRecord
    | LessonRecord | CommitRecord | TemplateRecord | SummaryCounters | SummaryRecord
    | DirectoryEntry | PrimitiveEvent | TraceCommitment | ScheduleRecord | PhaseDescriptor
    | ClassMapping | GRecord
)


_RECORD_TYPES: tuple[type[_SupportedRecord], ...] = (
    Stocks, ResponseRecord, TickCapsule, TickRecord, SnapshotRecord,
    ResetAuditRecord, LessonRecord, CommitRecord, TemplateRecord,
    SummaryCounters, SummaryRecord, DirectoryEntry, PrimitiveEvent,
    TraceCommitment, ScheduleRecord, PhaseDescriptor, ClassMapping, GRecord)


def marshal(record: _SupportedRecord) -> bytes:
    """Encode exactly one supported frozen record, revalidating all fields."""
    if type(record) not in _RECORD_TYPES:
        raise ArchiveError("unsupported record object; no mappings/subclasses/callbacks")
    record._validate()
    raw = record._encode()
    if len(raw) != record.SIZE:
        raise ArchiveError("internal record width mismatch")
    return raw


def unmarshal(record_type: type[_RecordT], raw: bytes) -> _RecordT:
    """Reject every truncation, suffix, unknown enum, and nonzero reserved byte."""
    if record_type not in _RECORD_TYPES:
        raise ArchiveError("unsupported record type")
    _bytes(raw, record_type.SIZE)
    record = record_type._decode(raw)
    # Re-encoding is also an exhaustive reserved-padding check. Opaque state
    # and scratch are preserved; unused schedule nibbles must be zero.
    # The exact class was checked against the closed allowlist before decoding.
    if marshal(cast(_SupportedRecord, record)) != raw:
        raise ArchiveError("nonzero reserved bits/padding or noncanonical encoding")
    return record


def uint64_string(value: int) -> str:
    return str(_int(value, "uint64 quantity"))


def parse_uint64_string(value: str) -> int:
    if (type(value) is not str or not value or len(value) > 20
            or any(c not in "0123456789" for c in value)
            or (len(value) > 1 and value[0] == "0")):
        raise ArchiveError("uint64 must be a canonical unsigned decimal string")
    return _int(int(value), "uint64 quantity")


def count_catalog_json(counts: dict) -> bytes:
    """Serialize exactly the frozen count names as decimal strings (not a manifest)."""
    if type(counts) is not dict or set(counts) != set(COMBINED_COUNTS):
        raise ArchiveError("count catalog requires exactly the frozen quantity keys")
    return canonical_json({key: uint64_string(value) for key, value in counts.items()})


def canonical_json(value) -> bytes:
    """RFC 8785-compatible RESTRICTED domain, not a general JCS implementation.

    Only plain dict/list, ASCII keys AND strings, null, bool, and integers with
    abs(value)<2**53 are supported. Floats (including finite floats), Unicode,
    custom containers, and cycles reject. In this domain Python's key ordering,
    string escapes, and decimal integers agree with JCS. uint64/rational
    quantities must be supplied as canonical decimal strings by schema owners.
    This helper does NOT invent or validate the unresolved nested manifest or
    gate schemas and must not be used to authorize COMPLETE status.
    """
    active = set()

    def check(item):
        kind = type(item)
        if item is None or kind is bool:
            return
        if kind is str:
            if not item.isascii():
                raise ArchiveError("canonical subset requires ASCII strings")
            return
        if kind is int:
            _int(item, "JSON safe integer", -(1 << 53) + 1, (1 << 53) - 1)
            return
        if kind not in (dict, list):
            raise ArchiveError("unsupported canonical JSON value (floats/custom objects forbidden)")
        if id(item) in active:
            raise ArchiveError("cyclic JSON container")
        active.add(id(item))
        if kind is dict:
            for key, child in item.items():
                if type(key) is not str or not key.isascii():
                    raise ArchiveError("JSON keys must be plain ASCII strings")
                check(child)
        else:
            for child in item:
                check(child)
        active.remove(id(item))

    try:
        check(value)
        return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
                          allow_nan=False).encode("utf-8")
    except RecursionError:
        raise ArchiveError("JSON nesting too deep") from None


def parse_canonical_json(raw: bytes):
    """Parse only canonical bytes in the restricted domain; duplicates reject."""
    if type(raw) is not bytes:
        raise ArchiveError("canonical JSON must be immutable bytes")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ArchiveError("duplicate JSON key")
            result[key] = value
        return result

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ArchiveError("invalid JSON") from exc
    if canonical_json(value) != raw:
        raise ArchiveError("noncanonical JSON bytes")
    return value