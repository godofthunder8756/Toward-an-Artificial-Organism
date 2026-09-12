"""E3 ABI-9 structural frame codec and immutable public-context checks.

No interpreter, METER, session, packet queue, target generator, or state model
is implemented here. ``parse_frame`` / ``encode_frame`` handle ONE structural
frame. ``FrameCodec`` additionally checks an immutable BIND and, for SCALAR,
an explicitly supplied current BEGIN. Neither API certifies paid admission,
direction at a live opcode, order, uniqueness, completeness, scalar-count caps,
S termination, or process isolation. No acquired-dependent context is retained.

Raw persistent bytes, including corrupt/reserved storage, remain untouched.
Only protocol reserved fields are rejected. Width-valid TEMPLATE semantic
errors are reported by the contextual checker; a future interpreter must take
the specified paid BAD path, not turn this checker into a free gate/cleanup.
"""

from dataclasses import dataclass
from enum import IntEnum, IntFlag
import struct
from typing import ClassVar


ABI = 9
GENERIC_FORMAT = 1
STATE_BYTES = 276  # Deliberately no dependency on another component's state.
PUBLIC_CONFIG_CAPACITY = 512


class ProtocolError(ValueError):
    """A frame, public configuration, or explicit context violates the codec."""


class Kind(IntEnum):
    BIND = 0
    BEGIN = 1
    SCALAR = 2
    EXIT = 3
    SHUTDOWN = 4


class Phase(IntEnum):
    ACQUISITION = 0
    DEVELOPMENT = 1
    RECOVERY = 2
    ASSAY = 3
    ECOLOGY = 4
    ORACLE = 5


class Service(IntEnum):
    TICK = 0
    CONTROLLER = 1
    RESPONSE = 2
    ADMIT = 3
    BLOCK_LESSON = 4
    REP_LESSON = 5
    COMMIT = 6
    TERMINAL = 7
    ISOLATE = 8
    AGE_LOW = 9
    AGE_HIGH = 10
    CONDITION = 11
    TEMPLATE = 12


class Permission(IntFlag):
    LEARNING = 1
    CORRECTIVE = 2
    DUE = 4


class Capability(IntEnum):
    ORDINARY = 0
    TEMPLATE = 1


class Code(IntEnum):
    REP = 0
    BLOCK = 1


class Family(IntEnum):
    H1 = 0
    H2 = 1


class Policy(IntEnum):
    RL = 0
    PERIODIC = 1
    THRESHOLD = 2
    DRIVE = 3
    FROZEN = 4  # Public mode only: BIND uses the underlying RL ID.
    SCRIPT_U = 5
    SCRIPT_ALL = 6


class ScalarTag(IntEnum):
    GRANT_E = 0
    GRANT_P0 = 1
    GRANT_P1 = 2
    GRANT_P2 = 3
    GRANT_P3 = 4
    OFFER = 5
    SENSE_E = 6
    SENSE_P = 7
    B = 8
    T = 9
    X = 10
    ACTION_REQUEST = 11
    FORAGE_YIELD = 12
    COLLECT_YIELD = 13
    GUESS = 14
    RESPONSE_BIT = 15
    ECOLOGY_YIELD = 16
    LEARNER_RETURN = 17
    ADMIT_CUE = 18
    LESSON_CUE = 19
    LESSON_LABEL = 20
    TEMPLATE_CUE = 21
    TEMPLATE_PAYLOAD = 22


_HEADER = struct.Struct("<BH")
_BIND = struct.Struct("<HHHH")
_BEGIN = struct.Struct("<HBHBBB")
_SCALAR = struct.Struct("<BBI")
_PAYLOAD_LENGTHS = (8, 284, 6, 276, 276)
_HORIZONS = (256, 2048, 128, 261, 512, 0)
_WIDTHS = (16, 8, 8, 8, 8, 5, 16, 8, 1, 2, 4, 6,
           16, 8, 1, 1, 16, 16, 4, 4, 1, 4, 4)
_MAX_VALUES = (65535, 255, 255, 255, 255, 31, 65535, 255, 1, 2, 15,
               31, 64, 8, 1, 1, 64, 65535, 15, 15, 1, 15, 15)
_ENERGY_CUTS = (24576, 32768, 40960)
_MATERIAL_CUTS = (32, 64, 96)
_INTERVALS = (1, 2, 4, 8, 16, 32, 64, 128, 256)
_UPKEEP = (Service.AGE_LOW, Service.AGE_HIGH, Service.CONDITION)
_QUERY = (Service.TICK, Service.RESPONSE, Service.ISOLATE) + _UPKEEP
_SERVICES = (
    (Service.TICK, Service.BLOCK_LESSON, Service.REP_LESSON, Service.COMMIT)
    + _UPKEEP,
    _QUERY + (Service.CONTROLLER, Service.ADMIT, Service.TERMINAL),
    _QUERY + (Service.CONTROLLER,),
    _QUERY + (Service.ADMIT,),
    _QUERY + (Service.CONTROLLER, Service.ADMIT, Service.TERMINAL),
    (Service.ISOLATE, Service.TEMPLATE),
)
_SERVICE_TAGS = (
    (0, 1, 2, 3, 4),
    (5, 6, 7, 8, 9, 10, 11, 12, 13),
    (14, 15, 16, 17),
    (18,),
    (19, 20),
    (19, 20),
    (), (), (), (), (), (),
    (21, 22),
)


def _integer(value: int, name: str, low: int, high: int) -> None:
    # bool is an int subclass, but is not a protocol integer/bit encoding.
    if type(value) is not int or not low <= value <= high:
        raise ProtocolError(f"{name} must be an integer in {low}..{high}")


def _enum(value: int, enum_type: type[IntEnum], name: str) -> IntEnum:
    if type(value) not in (int, enum_type):
        raise ProtocolError(f"{name} must use its declared enumeration")
    try:
        return enum_type(value)
    except ValueError:
        raise ProtocolError(f"unknown {name}") from None


def _state(value: bytes) -> None:
    if type(value) is not bytes or len(value) != STATE_BYTES:
        raise ProtocolError("persistent state must be exactly 276 immutable bytes")


def sign_extend(low_bits: int, width: int) -> int:
    """Interpret an already canonical low-bit encoding, without masking errors."""
    _integer(width, "width", 1, 32)
    _integer(low_bits, "low_bits", 0, (1 << width) - 1)
    sign = 1 << (width - 1)
    return (low_bits ^ sign) - sign


@dataclass(frozen=True, slots=True)
class PublicConfiguration:
    """Candidate-constant G identity, not an archive/run/target metadata record.

    Only the ID is supplied. Properties derive the frozen grid; callers cannot
    inject policy/cut/route dictionaries. Catalog slots 404..511 are reserved.
    Script IDs have no newly invented worker family enumeration.
    """

    public_config_id: int

    def __post_init__(self) -> None:
        _integer(self.public_config_id, "public_config_id", 0,
                 PUBLIC_CONFIG_CAPACITY - 1)
        if self.public_config_id > 403:
            raise ProtocolError("unassigned public configuration ID")

    @property
    def is_script(self) -> bool:
        return self.public_config_id >= 400

    @property
    def code(self) -> Code:
        index = self.public_config_id
        return Code((index - 400) // 2 if self.is_script else index // 200)

    @property
    def family(self) -> Family | None:
        return None if self.is_script else Family((self.public_config_id // 100) % 2)

    @property
    def policy(self) -> Policy:
        if self.is_script:
            return Policy(5 + (self.public_config_id - 400) % 2)
        k = self.public_config_id % 100
        if k < 9:
            return Policy.RL
        if k < 90:
            return Policy.PERIODIC
        return Policy.THRESHOLD if k < 99 else Policy.DRIVE

    @property
    def _cut_pair(self) -> int:
        k = self.public_config_id % 100
        if self.is_script or self.policy == Policy.DRIVE:
            return 4
        if self.policy == Policy.PERIODIC:
            return (k - 9) // 9
        return k - 90 if self.policy == Policy.THRESHOLD else k

    @property
    def energy_cut(self) -> int:
        return _ENERGY_CUTS[self._cut_pair // 3]

    @property
    def material_cut(self) -> int:
        return _MATERIAL_CUTS[self._cut_pair % 3]

    @property
    def interval(self) -> int:
        if self.policy != Policy.PERIODIC:
            return 0
        return _INTERVALS[(self.public_config_id % 100 - 9) % 9]

    @property
    def objective(self) -> int:
        return int(self.policy == Policy.DRIVE)

    @property
    def health_threshold(self) -> int:
        return 3

    @property
    def variant(self) -> int:
        return int(self.code)


@dataclass(frozen=True, slots=True)
class BindFrame:
    public_config_id: int
    capability: Capability = Capability.ORDINARY
    abi: int = ABI
    generic_format: int = GENERIC_FORMAT
    kind: ClassVar[Kind] = Kind.BIND

    def __post_init__(self) -> None:
        _integer(self.abi, "ABI", ABI, ABI)
        _integer(self.generic_format, "generic_format", GENERIC_FORMAT, GENERIC_FORMAT)
        PublicConfiguration(self.public_config_id)
        object.__setattr__(self, "capability",
                           _enum(self.capability, Capability, "capability"))

    @property
    def configuration(self) -> PublicConfiguration:
        return PublicConfiguration(self.public_config_id)


@dataclass(frozen=True, slots=True)
class BeginFrame:
    phase: Phase
    planned_tick: int
    service: Service
    argument: int
    mask: int
    state: bytes
    abi: int = ABI
    kind: ClassVar[Kind] = Kind.BEGIN

    def __post_init__(self) -> None:
        _integer(self.abi, "ABI", ABI, ABI)
        object.__setattr__(self, "phase", _enum(self.phase, Phase, "phase"))
        object.__setattr__(self, "service", _enum(self.service, Service, "service"))
        if type(self.mask) is Permission:
            object.__setattr__(self, "mask", int(self.mask))
        _integer(self.mask, "mask", 0, 7)
        _integer(self.argument, "argument", 0, 255)
        _integer(self.planned_tick, "planned_tick", 0, _HORIZONS[self.phase])
        _state(self.state)
        _validate_header(self)


@dataclass(frozen=True, slots=True)
class ScalarFrame:
    tag: ScalarTag
    width: int
    low_bits: int
    kind: ClassVar[Kind] = Kind.SCALAR

    def __post_init__(self) -> None:
        object.__setattr__(self, "tag", _enum(self.tag, ScalarTag, "scalar tag"))
        expected = _WIDTHS[self.tag]
        _integer(self.width, "scalar width", expected, expected)
        _integer(self.low_bits, "low_bits", 0, (1 << expected) - 1)
        if self.low_bits > _MAX_VALUES[self.tag]:
            raise ProtocolError("scalar value outside the tag's range")
        if self.tag == ScalarTag.ECOLOGY_YIELD and self.low_bits not in (0, 64):
            raise ProtocolError("ecology yield must be 0 or 64")
        if self.tag == ScalarTag.LEARNER_RETURN and self.low_bits not in (0, 64, 65472):
            raise ProtocolError("learner return must encode -64, 0, or 64")

    @property
    def value(self) -> int:
        if self.tag == ScalarTag.LEARNER_RETURN:
            return sign_extend(self.low_bits, 16)
        return self.low_bits


def scalar_from_value(tag: ScalarTag, value: int) -> ScalarFrame:
    """Construct a canonical packet from a logical integer (not a Python bool)."""
    tag = ScalarTag(_enum(tag, ScalarTag, "scalar tag"))
    if tag == ScalarTag.LEARNER_RETURN:
        _integer(value, "learner return", -64, 64)
        if value not in (-64, 0, 64):
            raise ProtocolError("learner return must be -64, 0, or 64")
        value &= 0xFFFF
    return ScalarFrame(tag, _WIDTHS[tag], value)


@dataclass(frozen=True, slots=True)
class ExitFrame:
    state: bytes
    kind: ClassVar[Kind] = Kind.EXIT

    def __post_init__(self) -> None:
        _state(self.state)


@dataclass(frozen=True, slots=True)
class ShutdownFrame:
    state: bytes
    kind: ClassVar[Kind] = Kind.SHUTDOWN

    def __post_init__(self) -> None:
        _state(self.state)
        if self.state[225:227] != b"\x00\x00":
            raise ProtocolError("SHUTDOWN requires raw E=0")


Frame = BindFrame | BeginFrame | ScalarFrame | ExitFrame | ShutdownFrame
_FRAME_TYPES = (BindFrame, BeginFrame, ScalarFrame, ExitFrame, ShutdownFrame)


def _validate_header(frame: BeginFrame) -> None:
    phase, service, tick = frame.phase, frame.service, frame.planned_tick
    mask = frame.mask
    if service not in _SERVICES[phase]:
        raise ProtocolError("service is not scheduled in this phase")
    if service == Service.ISOLATE:
        if tick != 0 or mask & (Permission.LEARNING | Permission.DUE):
            raise ProtocolError("entry ISOLATE requires tick zero and no learning/due")
    elif phase != Phase.ORACLE and tick == 0:
        raise ProtocolError("ordinary timed services require a positive planned tick")
    if phase == Phase.ORACLE and mask != 0:
        raise ProtocolError("off-clock oracle requires mask zero")
    if mask & Permission.LEARNING and phase not in (Phase.DEVELOPMENT, Phase.ECOLOGY):
        raise ProtocolError("learning is unavailable in this phase")
    if phase == Phase.ASSAY and mask & Permission.CORRECTIVE:
        raise ProtocolError("assay forbids corrective code writes")

    # This public due calendar is not the private cue/admission schedule.
    due = phase in (Phase.DEVELOPMENT, Phase.ASSAY, Phase.ECOLOGY) and tick >= 6
    if bool(mask & Permission.DUE) != due:
        raise ProtocolError("due bit disagrees with the public planned calendar")
    if service in (Service.RESPONSE, Service.ADMIT):
        if frame.argument != (tick - 1) % 5:
            raise ProtocolError("slot must be (planned_tick - 1) modulo five")
        if service == Service.ADMIT and tick > _HORIZONS[phase] - 5:
            raise ProtocolError("ADMIT is unavailable on drain ticks")
    elif service == Service.COMMIT:
        if tick % 4 or frame.argument > 3:
            raise ProtocolError("COMMIT requires a fourth lesson and block 0..3")
        # The selected block order is shuffled externally: do NOT derive it.
    elif service == Service.CONDITION:
        if frame.argument > 19:
            raise ProtocolError("CONDITION domain must be 0..19")
    elif frame.argument != 0:
        raise ProtocolError("unused argument must be zero")
    if service == Service.TERMINAL:
        if not mask & Permission.LEARNING or tick != _HORIZONS[phase]:
            raise ProtocolError("TERMINAL requires the last planned learning tick")


def parse_frame(raw: bytes) -> Frame:
    """Parse exactly one immutable byte string; no concatenation or stream state."""
    if type(raw) is not bytes:
        raise ProtocolError("frame must be immutable bytes")
    if len(raw) < _HEADER.size:
        raise ProtocolError("truncated frame header")
    kind_value, length = _HEADER.unpack_from(raw)
    kind = Kind(_enum(kind_value, Kind, "frame kind"))
    if length != _PAYLOAD_LENGTHS[kind]:
        raise ProtocolError("wrong payload length for frame kind")
    if len(raw) != _HEADER.size + length:
        raise ProtocolError("truncated payload or trailing bytes")
    payload = raw[_HEADER.size:]
    if kind == Kind.BIND:
        abi, generic_format, config, capability = _BIND.unpack(payload)
        return BindFrame(config, capability, abi, generic_format)
    if kind == Kind.BEGIN:
        abi, phase, tick, service, argument, mask = _BEGIN.unpack_from(payload)
        return BeginFrame(phase, tick, service, argument, mask, payload[8:], abi)
    if kind == Kind.SCALAR:
        return ScalarFrame(*_SCALAR.unpack(payload))
    if kind == Kind.EXIT:
        return ExitFrame(payload)
    return ShutdownFrame(payload)


def encode_frame(frame: Frame) -> bytes:
    """Encode the exact closed frame union, not mappings or duck-typed objects."""
    if type(frame) not in _FRAME_TYPES:
        raise ProtocolError("unsupported frame object")
    # Recheck even objects constructed by bypassing normal dataclass initialization.
    frame.__post_init__()
    if isinstance(frame, BindFrame):
        payload = _BIND.pack(frame.abi, frame.generic_format,
                             frame.public_config_id, frame.capability)
    elif isinstance(frame, BeginFrame):
        payload = _BEGIN.pack(frame.abi, frame.phase, frame.planned_tick,
                              frame.service, frame.argument, frame.mask) + frame.state
    elif isinstance(frame, ScalarFrame):
        payload = _SCALAR.pack(frame.tag, frame.width, frame.low_bits)
    else:
        payload = frame.state
    return _HEADER.pack(frame.kind, len(payload)) + payload


@dataclass(frozen=True, slots=True)
class FrameCodec:
    """Stateless checks against one immutable BIND, never a session/worker FSM.

    Supply the current BEGIN explicitly when checking a SCALAR. A BEGIN is a
    validation argument, not a saved continuation or paid-site authorization.
    Only BIND survives in this object. Duplicate matching BINDs and repeated
    valid scalars are intentionally not detected without a future transport FSM.
    """

    binding: BindFrame

    def __post_init__(self) -> None:
        if type(self.binding) is not BindFrame:
            raise ProtocolError("FrameCodec requires an immutable BIND")
        encode_frame(self.binding)

    def _begin(self, frame: BeginFrame) -> None:
        if type(frame) is not BeginFrame:
            raise ProtocolError("current BEGIN must be a BeginFrame")
        encode_frame(frame)
        config = self.binding.configuration
        if frame.mask & Permission.LEARNING and config.policy in (
                Policy.PERIODIC, Policy.THRESHOLD):
            raise ProtocolError("fixed policies cannot enable learning")
        if config.is_script and frame.phase not in (Phase.RECOVERY, Phase.ASSAY, Phase.ECOLOGY):
            raise ProtocolError("script G is limited to ecology and its reset futures")
        if (config.is_script and frame.phase == Phase.ECOLOGY
                and frame.service != Service.ISOLATE
                and not frame.mask & Permission.LEARNING):
            raise ProtocolError("script ecology requires genuine learning bookkeeping")
        if frame.service == Service.REP_LESSON and config.code != Code.REP:
            raise ProtocolError("REP_LESSON requires REP G")
        if frame.service in (Service.BLOCK_LESSON, Service.COMMIT) and config.code != Code.BLOCK:
            raise ProtocolError("BLOCK teaching requires BLOCK G")
        if frame.service == Service.TEMPLATE and self.binding.capability != Capability.TEMPLATE:
            raise ProtocolError("TEMPLATE requires capability one")

    def validate(self, frame: Frame, *, begin: BeginFrame | None = None) -> None:
        encode_frame(frame)
        if begin is not None and type(frame) is not ScalarFrame:
            raise ProtocolError("current BEGIN context is only an argument for SCALAR")
        if type(frame) is BindFrame:
            if frame != self.binding:
                raise ProtocolError("BIND does not match this immutable codec")
        elif type(frame) is BeginFrame:
            self._begin(frame)
        elif type(frame) is ScalarFrame:
            if begin is None:
                raise ProtocolError("contextual SCALAR checks require the current BEGIN")
            self._begin(begin)
            config = self.binding.configuration
            if frame.tag not in _SERVICE_TAGS[begin.service]:
                raise ProtocolError("scalar tag is unavailable in this service")
            if frame.tag in (ScalarTag.B, ScalarTag.T, ScalarTag.X):
                if config.policy not in (Policy.RL, Policy.DRIVE):
                    raise ProtocolError("rank scalars require RL selection")
            if frame.tag in (ScalarTag.ECOLOGY_YIELD, ScalarTag.LEARNER_RETURN):
                if begin.phase not in (Phase.DEVELOPMENT, Phase.ECOLOGY) or not begin.mask & Permission.DUE:
                    raise ProtocolError("feedback requires a planned development/ecology response")
                if frame.tag == ScalarTag.LEARNER_RETURN and not begin.mask & Permission.LEARNING:
                    raise ProtocolError("learner return requires learning permission")
            if frame.tag == ScalarTag.TEMPLATE_PAYLOAD and config.code == Code.REP:
                if frame.low_bits > 1:
                    raise ProtocolError("REP TEMPLATE semantic BAD: payload is not a bit")
            if frame.tag == ScalarTag.TEMPLATE_CUE and config.code == Code.BLOCK:
                if frame.low_bits % 4:
                    raise ProtocolError("BLOCK TEMPLATE semantic BAD: cue is not block aligned")

    def parse_frame(self, raw: bytes, *, begin: BeginFrame | None = None) -> Frame:
        frame = parse_frame(raw)
        self.validate(frame, begin=begin)
        return frame

    def encode_frame(self, frame: Frame, *, begin: BeginFrame | None = None) -> bytes:
        self.validate(frame, begin=begin)
        return encode_frame(frame)