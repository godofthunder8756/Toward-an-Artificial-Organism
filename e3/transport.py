"""Trusted-HOST ABI-9 transport flow validation, not an acquired worker state.

OperationSession belongs outside the isolated interpreter/policy process. Its
current BEGIN (including the 276-byte input snapshot), counters, pending permit
and few scalar consistency fields are HOST validation metadata, never additional
worker registers. Never pass this object, its pointers, or its BEGIN to policy
code. The worker must adopt the current body as its sole actual State and drop
serialization/input references; this module neither constructs State nor keeps
a worker-side old-body mirror. Completion/failure drops the host BEGIN too.

accept() consumes exactly one frame and returns None, never a scalar, state,
receipt or target. No packet queue, producer callback, key/root/schedule, file
reader, acquired-program selector, or state accessor is provided. Only BIND
survives normal operations; a reset/rebind requires a NEW host session (ordinary
capability for a canonical reset), plus external cancellation of old contexts.

Permits name the scalar sites in the adopted v0.9 service traces and specialize
their order using immutable G/public BEGIN and observed outbound traffic. They
are single-use HOST tokens, NOT paid receipts or evidence of a live scratch PC.
The machine currently has no full scalar/service/gate executor to attest those
sites. M/C/S, SENSE charges, scan/selection, BAD execution, actual state ownership,
sourcewise budgets, process isolation and economic proof remain integration
obligations. No caller-supplied 'paid' boolean can establish any of them here.

EXIT validates a complete scalar path and positive raw E, not paid S or the
truth of rejection. SHUTDOWN validates E=0 after any proper scalar prefix,
including a pending yield/feedback; it proves no physical cause. Interruption
must call abort()/finish(), never fabricate an empty successful service. This
is a structural validator only; it does not execute services or certify G-INFO.
"""

from dataclasses import dataclass
from enum import Enum, auto

from .protocol import (
    BeginFrame, BindFrame, Code, ExitFrame, FrameCodec, Permission, Phase,
    Policy, ProtocolError, ScalarFrame, ScalarTag, Service, ShutdownFrame,
    parse_frame,
)


class TransportError(ProtocolError):
    """Terminal technical failure of this host session, not biological death."""


class Direction(Enum):
    IN = auto()   # Host -> worker.
    OUT = auto()  # Worker -> host.


class SessionStage(Enum):
    UNBOUND = auto()
    READY = auto()
    ACTIVE = auto()
    CLOSED = auto()
    FAILED = auto()


class ScalarOpcode(Enum):
    """Named trace sites, NOT new machine opcodes or generic callable hooks."""

    TICK_GRANT_E = ScalarTag.GRANT_E
    TICK_GRANT_P0 = ScalarTag.GRANT_P0
    TICK_GRANT_P1 = ScalarTag.GRANT_P1
    TICK_GRANT_P2 = ScalarTag.GRANT_P2
    TICK_GRANT_P3 = ScalarTag.GRANT_P3
    CONTROLLER_OFFER = ScalarTag.OFFER
    SENSE_E = ScalarTag.SENSE_E
    SENSE_P = ScalarTag.SENSE_P
    SELECT_B = ScalarTag.B
    SELECT_T = ScalarTag.T
    SELECT_X = ScalarTag.X
    ACTION_REQUEST = ScalarTag.ACTION_REQUEST
    FORAGE_YIELD = ScalarTag.FORAGE_YIELD
    COLLECT_YIELD = ScalarTag.COLLECT_YIELD
    RESPONSE_GUESS = ScalarTag.GUESS
    RESPONSE_BIT = ScalarTag.RESPONSE_BIT
    ECOLOGY_YIELD = ScalarTag.ECOLOGY_YIELD
    LEARNER_RETURN = ScalarTag.LEARNER_RETURN
    ADMIT_CUE = ScalarTag.ADMIT_CUE
    LESSON_CUE = ScalarTag.LESSON_CUE
    LESSON_LABEL = ScalarTag.LESSON_LABEL
    TEMPLATE_CUE = ScalarTag.TEMPLATE_CUE
    TEMPLATE_PAYLOAD = ScalarTag.TEMPLATE_PAYLOAD


def _direction(tag: ScalarTag) -> Direction:
    return (Direction.OUT if tag in (ScalarTag.ACTION_REQUEST, ScalarTag.RESPONSE_BIT)
            else Direction.IN)


@dataclass(frozen=True, slots=True)
class Permit:
    """One named-site descriptor; only the issuing session's identity is usable.

    Constructing/copying an equal descriptor confers no authority. Descriptors
    carry no scalar payload, BEGIN, callback, receipt, acquired state or secret.
    They must stay in the trusted host, not become worker-visible capabilities.
    """

    opcode: ScalarOpcode

    def __post_init__(self) -> None:
        if type(self.opcode) is not ScalarOpcode:
            raise TransportError("permit requires a named ScalarOpcode")

    @property
    def tag(self) -> ScalarTag:
        return self.opcode.value

    @property
    def direction(self) -> Direction:
        return _direction(self.tag)


class OperationSession:
    """BIND once, then sequential BEGIN/[SCALAR]/EXIT operations in the host.

    Call permit(named_opcode) immediately before its current scalar, then
    accept(raw, direction, permit=that_exact_token). No prefetch or retry API.
    accept(BIND/BEGIN/EXIT/SHUTDOWN) takes no permit. finish() checks EOF; abort()
    records interruption as terminal failure. All validation errors poison the
    session and release operation references; a later call cannot resume it.

    Stage/count/binding properties are external diagnostics only. There is no
    'current(tag)' worker API until an actual paid executor can consume straight
    into the trace's named scratch destination without retaining old buffers.
    """

    __slots__ = ("_codec", "_stage", "_begin", "_pending", "_count", "_last",
                 "_cue", "_action", "_yield", "_template_bad")

    def __init__(self) -> None:
        self._codec: FrameCodec | None = None
        self._stage = SessionStage.UNBOUND
        self._begin: BeginFrame | None = None
        self._pending: Permit | None = None
        self._count = 0
        self._last: ScalarTag | None = None
        self._cue: int | None = None
        self._action: int | None = None
        self._yield: int | None = None
        self._template_bad = False

    @property
    def binding(self) -> BindFrame | None:
        return None if self._codec is None else self._codec.binding

    @property
    def stage(self) -> SessionStage:
        return self._stage

    @property
    def scalar_count(self) -> int:
        """Current-operation count, both directions; zero outside an operation."""
        return self._count

    def _drop_operation(self) -> None:
        self._begin = None
        self._pending = None
        self._count = 0
        self._last = None
        self._cue = None
        self._action = None
        self._yield = None
        self._template_bad = False

    def _fail(self) -> None:
        self._drop_operation()
        self._stage = SessionStage.FAILED

    def _active(self) -> tuple[FrameCodec, BeginFrame]:
        if (self._stage is not SessionStage.ACTIVE or self._codec is None
                or self._begin is None):
            raise TransportError("no active operation")
        return self._codec, self._begin

    def _ranked(self) -> bool:
        codec, _ = self._active()
        return codec.binding.configuration.policy in (Policy.RL, Policy.DRIVE)

    def _feedback(self) -> bool:
        _, begin = self._active()
        # Match FrameCodec: development/ecology, not G's training-family ID.
        # H1 query workers are ASSAY; recovery and assay never receive feedback.
        return (begin.phase in (Phase.DEVELOPMENT, Phase.ECOLOGY)
                and bool(begin.mask & Permission.DUE))

    def _allowed(self) -> tuple[ScalarTag, ...]:
        _, begin = self._active()
        n, service = self._count, begin.service
        if n >= 8:
            return ()
        if service is Service.TICK:
            return (ScalarTag(n),) if n < 5 else ()
        if service is Service.CONTROLLER:
            base = 6 if self._ranked() else 3
            if n < base:
                return (ScalarTag(5 + n),)
            if n == base:
                return (ScalarTag.ACTION_REQUEST,)
            if n == base + 1:
                return ((ScalarTag.FORAGE_YIELD,) if self._action == 0
                        else (ScalarTag.COLLECT_YIELD,))
            return ()
        if service is Service.RESPONSE:
            if self._last is None:
                return (ScalarTag.GUESS, ScalarTag.RESPONSE_BIT)
            if self._last is ScalarTag.GUESS:
                return (ScalarTag.RESPONSE_BIT,)
            if self._last is ScalarTag.RESPONSE_BIT and self._feedback():
                return (ScalarTag.ECOLOGY_YIELD,)
            if (self._last is ScalarTag.ECOLOGY_YIELD
                    and begin.mask & Permission.LEARNING):
                return (ScalarTag.LEARNER_RETURN,)
            return ()
        if service is Service.ADMIT:
            return (ScalarTag.ADMIT_CUE,) if n == 0 else ()
        if service in (Service.BLOCK_LESSON, Service.REP_LESSON):
            return (ScalarTag(19 + n),) if n < 2 else ()
        if service is Service.TEMPLATE:
            return (ScalarTag(21 + n),) if n < 2 else ()
        return ()

    def permit(self, opcode: ScalarOpcode) -> Permit:
        """Issue one current G/path-restricted descriptor, never a paid proof."""
        try:
            self._active()
            if type(opcode) is not ScalarOpcode:
                raise TransportError("site must be a named ScalarOpcode")
            if self._pending is not None:
                raise TransportError("a current scalar permit is already outstanding")
            if self._count >= 8:
                raise TransportError("eight-scalar operation budget exhausted")
            if opcode.value not in self._allowed():
                raise TransportError("scalar site unavailable in the current G/path")
            token = Permit(opcode)
            self._pending = token
            return token
        except ProtocolError:
            self._fail()
            raise

    def _scalar(self, frame: ScalarFrame, direction: Direction,
                permit: Permit | None) -> None:
        codec, begin = self._active()
        if (type(permit) is not Permit or permit is not self._pending
                or permit.tag is not frame.tag or permit.direction is not direction):
            raise TransportError("scalar requires its current one-shot directed permit")
        if self._count >= 8 or frame.tag not in self._allowed():
            raise TransportError("scalar exceeds the current path/budget")
        if begin.service is not Service.TEMPLATE:
            codec.validate(frame, begin=begin)
        # TEMPLATE's width-valid semantic BAD must be tested by the paid local
        # G instructions AFTER both inputs. Do not use FrameCodec's contextual
        # semantic error as a free paid BAD path. Structural parsing and this
        # session's capability/header/tag/order checks still apply normally.
        tag = frame.tag
        if tag is ScalarTag.OFFER:
            self._cue = frame.low_bits & 15
        elif tag is ScalarTag.ACTION_REQUEST:
            if frame.low_bits & 15 != self._cue:
                raise TransportError("resource request cue differs from current offer")
            self._action = frame.low_bits >> 4  # Codec permits only action 0/1.
            self._cue = None
        elif tag in (ScalarTag.FORAGE_YIELD, ScalarTag.COLLECT_YIELD):
            self._action = None
        elif tag is ScalarTag.ECOLOGY_YIELD:
            if begin.mask & Permission.LEARNING:
                self._yield = frame.low_bits
        elif tag is ScalarTag.LEARNER_RETURN:
            if (self._yield, frame.value) not in ((64, 64), (0, -64), (0, 0)):
                raise TransportError("ecological yield/return pair is inconsistent")
            self._yield = None
        elif tag is ScalarTag.TEMPLATE_CUE:
            self._template_bad = (codec.binding.configuration.code is Code.BLOCK
                                  and frame.low_bits % 4 != 0)
        elif tag is ScalarTag.TEMPLATE_PAYLOAD:
            self._template_bad |= (codec.binding.configuration.code is Code.REP
                                   and frame.low_bits > 1)
        self._pending = None
        self._last = tag
        self._count += 1

    def _complete(self) -> bool:
        _, begin = self._active()
        n, service = self._count, begin.service
        if service is Service.TICK:
            return n == 5
        if service is Service.CONTROLLER:
            base = 6 if self._ranked() else 3
            # No scalars: DECIDE rejection. All selection inputs but no request:
            # scrub/abstention/rejected ACTION; no invented success predicate.
            return n in (0, base, base + 2)
        if service is Service.RESPONSE:
            return n == 0 or (self._last is not ScalarTag.GUESS and not self._allowed())
        if service is Service.ADMIT:
            return n in (0, 1)
        if service in (Service.BLOCK_LESSON, Service.REP_LESSON, Service.TEMPLATE):
            return n in (0, 2)
        return n == 0

    def accept(self, raw: bytes, direction: Direction, *,
               permit: Permit | None = None) -> None:
        """Consume one immutable wire frame; every error is terminal, no output."""
        try:
            self._accept(raw, direction, permit)
        except ProtocolError:
            self._fail()
            raise

    def _accept(self, raw: bytes, direction: Direction, permit: Permit | None) -> None:
        if self._stage in (SessionStage.CLOSED, SessionStage.FAILED):
            raise TransportError("session is terminal")
        if type(direction) is not Direction:
            raise TransportError("direction must be Direction.IN or Direction.OUT")
        frame = parse_frame(raw)
        if type(frame) is ScalarFrame:
            self._scalar(frame, direction, permit)
            return
        if permit is not None:
            raise TransportError("only SCALAR may carry a permit")
        if type(frame) in (BindFrame, BeginFrame):
            if direction is not Direction.IN:
                raise TransportError("BIND/BEGIN must be host input")
        elif direction is not Direction.OUT:
            raise TransportError("EXIT/SHUTDOWN must be worker output")
        if type(frame) is BindFrame:
            if self._stage is not SessionStage.UNBOUND:
                raise TransportError("BIND is allowed exactly once per process context")
            self._codec = FrameCodec(frame)
            self._stage = SessionStage.READY
        elif type(frame) is BeginFrame:
            if self._stage is not SessionStage.READY or self._codec is None:
                raise TransportError("BEGIN requires BIND and no active operation")
            self._codec.validate(frame)
            self._drop_operation()
            self._begin = frame
            self._stage = SessionStage.ACTIVE
        else:
            codec, _ = self._active()
            codec.validate(frame)
            # The semantic check occurs only after BOTH input sites in G.
            # A minimum failure before the second site is still a proper
            # physical prefix, even if the first width-valid cue is unaligned.
            if self._template_bad and self._count == 2:
                raise TransportError("TEMPLATE semantic BAD requires technical failure, not a result")
            if type(frame) is ExitFrame:
                if self._pending is not None or not self._complete():
                    raise TransportError("EXIT interrupts a mandatory scalar group")
                if frame.state[225:227] == b"\x00\x00":
                    raise TransportError("EXIT requires positive raw E; use SHUTDOWN for E=0")
                self._drop_operation()
                self._stage = SessionStage.READY
            else:
                assert type(frame) is ShutdownFrame
                # A real minimum failure can interrupt any proper prefix,
                # including between paired inputs or request and yield.
                self._drop_operation()
                self._stage = SessionStage.CLOSED

    def finish(self) -> None:
        """Validate EOF; a bound empty stream is allowed, an open BEGIN is not."""
        if self._stage not in (SessionStage.READY, SessionStage.CLOSED):
            self._fail()
            raise TransportError("incomplete or failed transport stream")
        self._stage = SessionStage.CLOSED

    def abort(self) -> None:
        """External interruption/BAD: no cleanup, result, retry, or receipt."""
        self._fail()
        raise TransportError("transport interrupted: external FAILED/PARTIAL required")