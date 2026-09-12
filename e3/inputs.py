"""Private-domain E3 indexed inputs, not a worker API or a root generator.

Retains evaluation v0.7/v0.8, interface v0.9 and the v0.11 slot extension.
All keys are supplied explicitly; only the two published constants live here.
There is no target draw, entropy source, live-key loader, global cursor, state
reader, worker frame, callback parameter, filesystem or experiment launcher.
Do not import this module into an isolated worker or send its objects over IPC.
Only later paid adapters may deliver current scalar *values*, never coordinates,
attempt counts, schedules, keys, digests or original due cues.

Root provenance/independent requests remain the external owner's obligation.
These functions implement a computational input law, not information-theoretic
independence. Frozen Python values are not an access-control boundary. Reset
namespace equality does not prove actual-parent reset, cancellation, complete G
equality or permission to share executions; those need integration evidence.
"""

from dataclasses import dataclass, replace
import hmac
import json
from types import MappingProxyType


VERSION = "E3-EVAL-0.8"
MAX_COORDINATE = (1 << 53) - 1
UINT128_SIZE = 1 << 128
ATTEMPT_LIMIT = 1024
CONFORMANCE_KEY = bytes.fromhex(
    "8f6c2a19d4b730e5a1c9087f62de4b03c5a87910ef26d4b7930a1e65c8f247bd")
ANALYSIS_KEY = bytes.fromhex(
    "37b4e0a1c9625df80a7e413bd6982fc54e0137a965c2bd084fae1763908dc25b")
CUE_POOL = tuple(range(16))


def _integer(value: int, name: str, low: int, high: int) -> None:
    if type(value) is not int:
        raise TypeError(f"{name} must be a built-in int, not bool or a string")
    if not low <= value <= high:
        raise ValueError(f"{name} must be in {low}..{high}")


def _ascii(value: str, name: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in str")
    if not value.isascii():
        raise ValueError(f"{name} must be ASCII; no Unicode normalization")


def _key(key: bytes) -> None:
    if type(key) is not bytes:
        raise TypeError("key must be immutable built-in bytes")
    if len(key) != 32:
        raise ValueError("key must contain exactly 32 bytes")


@dataclass(frozen=True, slots=True)
class InputTuple:
    """Required twelve-field syntax, with no inferred or omitted coordinates.

    This low-level codec checks types, ASCII, version and exact-integer bounds;
    phase_context supplies the narrower experiment catalog. Empty strings/zero
    are explicit unused fields, not nulls. Cohort is a string, not archive u8.
    Manifest uint64 decimal-string rules do NOT apply to these coordinates.
    """

    version: str
    cohort: str
    individual: int
    panel: int
    family: str
    phase: str
    purpose: str
    tick: int
    location: int
    slot: int
    draw_index: int
    attempt: int

    def __post_init__(self) -> None:
        for name in ("version", "cohort", "family", "phase", "purpose"):
            _ascii(getattr(self, name), name)
        if self.version != VERSION:
            raise ValueError("unsupported input-law version")
        for name in ("individual", "panel", "tick", "location", "slot", "draw_index"):
            _integer(getattr(self, name), name, 0, MAX_COORDINATE)
        _integer(self.attempt, "attempt", 0, ATTEMPT_LIMIT - 1)


def canonical_tuple(coordinates: InputTuple) -> bytes:
    """RFC 8785 for this restricted array only, not a general JCS serializer.

    ASCII string escaping and nonnegative integers <=2^53-1 have identical
    stdlib/ECMAScript encodings. There are no objects, floats, nulls, booleans,
    custom serializers, exponent-form integers or UTF-16 key-sorting issues.
    """
    if type(coordinates) is not InputTuple:
        raise TypeError("coordinates must be an InputTuple")
    coordinates.__post_init__()
    c = coordinates
    values = (c.version, c.cohort, c.individual, c.panel, c.family, c.phase,
              c.purpose, c.tick, c.location, c.slot, c.draw_index, c.attempt)
    return json.dumps(values, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":")).encode("utf-8")


def _digest(key: bytes, payload: bytes) -> bytes:
    """Standard primitive; private seam for RFC vectors and local test patches."""
    return hmac.new(key, payload, "sha256").digest()


def indexed_digest(key: bytes, coordinates: InputTuple) -> bytes:
    """Exact HMAC digest for an explicit attempt, private/archive use only."""
    _key(key)
    digest = _digest(key, canonical_tuple(coordinates))
    if type(digest) is not bytes or len(digest) != 32:
        raise InputGenerationError("HMAC must return exactly 32 bytes")
    return digest


class InputGenerationError(RuntimeError):
    """Technical input failure, never death, a new cohort or a fallback draw."""


@dataclass(frozen=True, slots=True)
class InputRecord:
    """External generation evidence, NOT a scalar packet or consumption claim."""

    coordinates: InputTuple
    bound: int
    value: int

    def __post_init__(self) -> None:
        canonical_tuple(self.coordinates)
        _integer(self.bound, "bound", 1, UINT128_SIZE)
        _integer(self.value, "value", 0, self.bound - 1)

    @property
    def attempt(self) -> int:
        return self.coordinates.attempt


def uniform(key: bytes, coordinates: InputTuple, m: int) -> InputRecord:
    """Unbiased range [0,m), first16 little-endian, attempts exactly 0..1023.

    Starting at nonzero attempt is rejected, not silently rewound or extended.
    Retries change only field twelve. There is one returned value and no worker
    retry packet. All arithmetic including m=2^128 is exact Python integer work.
    """
    _key(key)
    canonical_tuple(coordinates)
    _integer(m, "m", 1, UINT128_SIZE)
    if coordinates.attempt != 0:
        raise ValueError("uniform requires attempt zero")
    limit = (UINT128_SIZE // m) * m
    for attempt in range(ATTEMPT_LIMIT):
        current = replace(coordinates, attempt=attempt)
        x = int.from_bytes(indexed_digest(key, current)[:16], "little")
        if x < limit:
            return InputRecord(current, m, x % m)
    raise InputGenerationError("all 1024 indexed generation attempts rejected")


# These are external dictionary spellings, NOT additional tuple fields. The
# contracts select purpose separation but do not spell every swap subpurpose.
# Freeze these explicit spellings/indices with source before any live execution.
PURPOSE_ROOTS = MappingProxyType({
    "admissions": "schedule", "extra-cues": "schedule",
    "early-extra-cues": "schedule", "early-admissions": "schedule",
    "endpoint-admissions": "schedule", "drain-offer": "schedule",
    "recovery-offers": "schedule", "acquisition-blocks": "schedule",
    "acquisition-cues": "schedule", "code_flip": "fault",
    "code_erase": "fault", "aux_bit0": "fault", "aux_bit1": "fault",
    "aux_erase": "fault", "challenge": "challenge",
    "B": "exploration", "T": "exploration", "X": "exploration",
    "guess": "guess", "whole-block-UO": "UO", "mixed-UO": "UO",
    "HUB-placement": "injury", "FLIP": "injury",
    "individual-index": "analysis",
})


@dataclass(frozen=True, slots=True)
class ScheduleRule:
    slot: int
    family: str
    product: str
    stage: str


# Ordered archive slot catalog, including the sole v0.11 extension. Slots are
# NOT tuple slot coordinates (which refer to current physical/query positions).
SCHEDULE_CATALOG = (
    ScheduleRule(0, "H1", "TRUNK", "ACQUISITION"),
    ScheduleRule(1, "H1", "TRUNK", "DEVELOPMENT"),
    ScheduleRule(2, "H2", "TRUNK", "ACQUISITION"),
    ScheduleRule(3, "H2", "TRUNK", "DEVELOPMENT"),
    ScheduleRule(4, "H1", "TRUNK", "PRE"),
    ScheduleRule(5, "H2", "TRUNK", "PREREQUISITE"),
    *(ScheduleRule(6 + 3 * p + s, family, product, stage)
      for p, product in enumerate(("SCREEN", "SELECTED-CONTROL", "CORE"))
      for s, (family, stage) in enumerate(
          (("H1", "RECOVERY"), ("H1", "FINAL"), ("H2", "ECOLOGY")))),
    ScheduleRule(15, "H1", "SELECTED-CONTROL", "ACUTE"),
    ScheduleRule(16, "H1", "SELECTED-CONTROL", "POST"),
    *(ScheduleRule(17 + 2 * p + s, "H1", product, stage)
      for p, product in enumerate(("LL13", "FLIP", "HUB", "RESOURCE"))
      for s, stage in enumerate(("RECOVERY", "FINAL"))),
    *(ScheduleRule(25 + p, "H2", product, "ECOLOGY")
      for p, product in enumerate(("G-DIAG", "HS-REFERENCE", "MIXED"))),
    *(ScheduleRule(28 + 2 * f + s, family, "RESET", stage)
      for f, family in enumerate(("H1", "H2"))
      for s, stage in enumerate(("RECOVERY", "FINAL"))),
    ScheduleRule(32, "H1", "ORACLE", "ZERO-FAULT"),
    ScheduleRule(33, "H1", "ORACLE", "LIVE-WEAR"),
    ScheduleRule(34, "H2", "SCRIPTED", "ECOLOGY"),
)
_HORIZONS = MappingProxyType({
    "ACQUISITION": 256, "DEVELOPMENT": 2048, "RECOVERY": 128,
    "FINAL": 261, "PRE": 261, "PREREQUISITE": 261, "ACUTE": 261,
    "POST": 261, "ECOLOGY": 512, "ZERO-FAULT": 261, "LIVE-WEAR": 261,
})


@dataclass(frozen=True, slots=True)
class PhaseContext:
    """Private planned context without code, G, branch, history or outcome IDs.

    Sharing this context means input pairing only, never execution equivalence.
    Values describe a catalog, not authority to run a final experiment.
    """

    cohort: str
    individual: int
    panel: int
    schedule_slot: int

    def __post_init__(self) -> None:
        _ascii(self.cohort, "cohort")
        if self.cohort not in ("engineering", "final"):
            raise ValueError("cohort must be engineering or final")
        low, high = (1, 8) if self.cohort == "engineering" else (300, 331)
        _integer(self.individual, "individual", low, high)
        _integer(self.panel, "panel", 1, 8)
        _integer(self.schedule_slot, "schedule_slot", 0, 34)
        if self.cohort == "final" and self.rule.product not in ("TRUNK", "CORE", "RESET"):
            raise ValueError("engineering-only schedule in final cohort")
        if self.rule.product == "CORE" and self.cohort != "final":
            raise ValueError("CORE is final-only")
        if self.rule.product == "ORACLE" and self.panel != 1:
            raise ValueError("oracle probes use engineering panel one only")

    @property
    def rule(self) -> ScheduleRule:
        return SCHEDULE_CATALOG[self.schedule_slot]

    @property
    def family(self) -> str:
        r = self.rule
        return r.family if r.product == "RESET" else f"{r.family}-{r.product}"

    @property
    def phase(self) -> str:
        r = self.rule
        return f"RESET-{r.stage}" if r.product == "RESET" else r.stage

    @property
    def horizon(self) -> int:
        return _HORIZONS[self.rule.stage]

    @property
    def schedule_id(self) -> int:
        cell = ((self.individual - 1) * 8 + self.panel - 1
                if self.cohort == "engineering"
                else 64 + (self.individual - 300) * 8 + self.panel - 1)
        return 64 * cell + self.schedule_slot


def phase_context(cohort: str, individual: int, panel: int, family: str,
                  product: str, stage: str) -> PhaseContext:
    """Explicit allowlist builder; compared branches never select namespaces."""
    for name, value in (("family", family), ("product", product), ("stage", stage)):
        _ascii(value, name)
    for rule in SCHEDULE_CATALOG:
        if (rule.family, rule.product, rule.stage) == (family, product, stage):
            return PhaseContext(cohort, individual, panel, rule.slot)
    raise ValueError("unlisted family/product/stage combination")


def reset_context(cohort: str, individual: int, panel: int,
                  family: str, stage: str) -> PhaseContext:
    """Normalized H1/H2 Z; script G remains distinct externally, uses H2 here.

    No source-history, product, policy, branch, budget, old phase or source ID is
    accepted. FROZEN -> underlying RL and full G comparison belong to supervisor.
    """
    return phase_context(cohort, individual, panel, family, "RESET", stage)


def _context(context: PhaseContext) -> None:
    if type(context) is not PhaseContext:
        raise TypeError("context must be a PhaseContext")
    context.__post_init__()


def _coordinate(context: PhaseContext, purpose: str, tick: int,
                location: int, slot: int, draw_index: int) -> InputTuple:
    return InputTuple(VERSION, context.cohort, context.individual, context.panel,
                      context.family, context.phase, purpose, tick, location,
                      slot, draw_index, 0)


def _tick(context: PhaseContext, tick: int) -> None:
    _context(context)
    _integer(tick, "planned tick", 1, context.horizon)


def _shuffle(key: bytes, base: InputTuple, values: tuple[int, ...],
             records: list[InputRecord]) -> tuple[int, ...]:
    # Descending Fisher-Yates. draw_index is ZERO-BASED swap ordinal, not i.
    result = list(values)
    for draw_index, i in enumerate(range(len(result) - 1, 0, -1)):
        record = uniform(key, replace(base, draw_index=draw_index), i + 1)
        records.append(record)
        result[i], result[record.value] = result[record.value], result[i]
    return tuple(result)


@dataclass(frozen=True, slots=True)
class Schedule:
    """Caller-owned pre-execution plan, never worker-readable query history.

    Offers include the five drain-only cues. commit_blocks are the 64 grouped
    opportunities for BLOCK (REP dispatches none), not lesson-success flags.
    Records attest generation only; actual paid consumption is logged elsewhere.
    """

    admissions: tuple[int, ...]
    offers: tuple[int, ...]
    lessons: tuple[int, ...]
    commit_blocks: tuple[int, ...]
    records: tuple[InputRecord, ...]


def generate_schedule(key: bytes, context: PhaseContext) -> Schedule:
    """Pure balanced schedule generation; no target/body/success input.

    Multisets start cue-major. Acquisition uses location=pass (0..15),
    slot=block (0..3) for within-block shuffles, separate block/cue purposes.
    All preplanned shuffle ticks are zero; drains use their actual planned tick.
    """
    _key(key)
    _context(context)
    records: list[InputRecord] = []

    def shuffle(purpose: str, values: tuple[int, ...],
                location: int = 0, slot: int = 0) -> tuple[int, ...]:
        return _shuffle(key, _coordinate(context, purpose, 0, location, slot, 0),
                        values, records)

    stage = context.rule.stage
    if stage == "ACQUISITION":
        lessons: list[int] = []
        blocks: list[int] = []
        for pass_index in range(16):
            order = shuffle("acquisition-blocks", (0, 1, 2, 3), pass_index)
            for block in order:
                lessons.extend(shuffle("acquisition-cues", tuple(range(4 * block, 4 * block + 4)),
                                       pass_index, block))
                blocks.append(block)
        return Schedule((), (), tuple(lessons), tuple(blocks), tuple(records))
    if stage == "RECOVERY":
        offers = shuffle("recovery-offers", tuple(cue for cue in CUE_POOL for _ in range(8)))
        return Schedule((), offers, (), (), tuple(records))
    if stage == "DEVELOPMENT":
        extra = shuffle("extra-cues", CUE_POOL)[:11]
        pool = tuple(cue for cue in CUE_POOL for _ in range(127)) + extra
        admissions = shuffle("admissions", pool)
    elif stage == "ECOLOGY":
        extra = shuffle("early-extra-cues", CUE_POOL)[:11]
        early = shuffle("early-admissions", tuple(cue for cue in CUE_POOL for _ in range(15)) + extra)
        endpoint = shuffle("endpoint-admissions", tuple(cue for cue in CUE_POOL for _ in range(16)))
        admissions = early + endpoint
    else:
        admissions = shuffle("admissions", tuple(cue for cue in CUE_POOL for _ in range(16)))
    drains: list[int] = []
    for tick in range(len(admissions) + 1, len(admissions) + 6):
        record = uniform(key, _coordinate(context, "drain-offer", tick, 0, 0, 0), 16)
        records.append(record)
        drains.append(record.value)
    return Schedule(admissions, admissions + tuple(drains), (), (), tuple(records))


def fault_coordinates(context: PhaseContext, tick: int) -> tuple[InputTuple, ...]:
    """3,160 stable lane-major slots; reservoirs 900..923 excluded, reserve in.

    location=physical lane; slot=local flip/erase ordinal; draw_index=0.
    Code purposes distinguish sign flip/erase, auxiliary bit0/bit1/erase.
    Stored ages affect thresholds in physics, never coordinate generation.
    """
    _tick(context, tick)
    return tuple(_coordinate(context, purpose, tick, lane, slot, 0)
                 for lane in range(1104) if not 900 <= lane < 924
                 for slot, purpose in enumerate(
                     ("code_flip", "code_erase") if lane < 80
                     else ("aux_bit0", "aux_bit1", "aux_erase")))


def fault_inputs(key: bytes, context: PhaseContext, tick: int) -> tuple[InputRecord, ...]:
    """One current private physics plan; never a worker scalar frame."""
    _key(key)
    return tuple(uniform(key, coordinate, 10000) for coordinate in fault_coordinates(context, tick))


def fault_thresholds(age: int) -> tuple[int, int]:
    """Exact integer counts /10000 for sign/bit flip and erasure."""
    _integer(age, "age", 0, 15)
    return 10 * (1 + age), age


def challenge_inputs(key: bytes, context: PhaseContext) -> tuple[InputRecord, ...]:
    """80 planned boundary draws, including empty lanes; FLIP uses injury root.

    The caller selects the separate challenge root for FINAL/RESET-FINAL and
    injury root for FLIP RECOVERY. No label/occupancy test or action index.
    """
    _key(key)
    _context(context)
    r = context.rule
    if r.stage == "FINAL":
        purpose = "challenge"
    elif r.product == "FLIP" and r.stage == "RECOVERY":
        purpose = "FLIP"
    else:
        raise ValueError("no challenge at this phase boundary")
    return tuple(uniform(key, _coordinate(context, purpose, 0, lane, 0, 0), 10)
                 for lane in range(80))


def exploration_inputs(key: bytes, context: PhaseContext, tick: int) -> tuple[InputRecord, ...]:
    """B/T/X at a planned controller tick; no ranks for SCRIPTED's selector."""
    _key(key)
    _tick(context, tick)
    if context.rule.stage not in ("DEVELOPMENT", "RECOVERY", "ECOLOGY"):
        raise ValueError("phase has no offered controller")
    if context.rule.product == "SCRIPTED":
        raise ValueError("SCRIPTED consumes no B/T/X")
    return tuple(uniform(key, _coordinate(context, purpose, tick, 0, 0, 0), bound)
                 for purpose, bound in (("B", 2), ("T", 3), ("X", 16)))


def guess_input(key: bytes, context: PhaseContext, tick: int) -> InputRecord:
    """Plan even an unused RESPONSE guess; slot=(tick-1)%5, never actual cue."""
    _key(key)
    _tick(context, tick)
    if context.rule.stage == "ACQUISITION":
        raise ValueError("acquisition has no RESPONSE")
    return uniform(key, _coordinate(context, "guess", tick, 0, (tick - 1) % 5, 0), 2)


@dataclass(frozen=True, slots=True)
class UsefulnessAssignment:
    useful: tuple[int, ...]
    obsolete: tuple[int, ...]
    records: tuple[InputRecord, ...]


def usefulness_assignment(key: bytes, context: PhaseContext) -> UsefulnessAssignment:
    """Hidden U/O, shared across paired arms even when C treats both as useful."""
    _key(key)
    _context(context)
    if context.rule.stage != "ECOLOGY":
        raise ValueError("U/O only belongs to ecology")
    records: list[InputRecord] = []
    if context.rule.product == "MIXED":
        obsolete = tuple(sorted(cue for block in range(4) for cue in _shuffle(
            key, _coordinate(context, "mixed-UO", 0, block, 0, 0),
            tuple(range(4 * block, 4 * block + 4)), records)[:2]))
    else:
        blocks = _shuffle(key, _coordinate(context, "whole-block-UO", 0, 0, 0, 0),
                          (0, 1, 2, 3), records)[:2]
        obsolete = tuple(cue for cue in CUE_POOL if cue // 4 in blocks)
    return UsefulnessAssignment(tuple(cue for cue in CUE_POOL if cue not in obsolete),
                                obsolete, tuple(records))


def hub_assignment(key: bytes, cohort: str, individual: int) -> tuple[int, ...]:
    """One balanced eight-panel list; panel=0 deliberately indexes the list.

    HUB placement precedes recovery and is shared across codes/policies/A/N.
    No current-panel-dependent shuffle and no final secondary injuries.
    """
    _key(key)
    context = phase_context(cohort, individual, 1, "H1", "HUB", "RECOVERY")
    base = replace(_coordinate(context, "HUB-placement", 0, 0, 0, 0), panel=0)
    return _shuffle(key, base, (0, 0, 1, 1, 2, 2, 3, 3), [])


def bootstrap_coordinate(replicate: int, position: int, attempt: int) -> InputTuple:
    """Exact analysis tuple only; does not generate a bootstrap matrix."""
    _integer(replicate, "replicate", 0, 9999)
    _integer(position, "position", 0, 31)
    return InputTuple(VERSION, "final", 0, 0, "analysis", "bootstrap",
                      "individual-index", 0, 0, 0, 32 * replicate + position, attempt)