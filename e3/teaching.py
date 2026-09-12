"""Selected frozen teaching instruction foundations, not a whole-worker VM.

BLOCK LESSON, REP LESSON and COMMIT execute the ROM-closure expansion through
machine._step, only after THIS invocation pays its own C256. GateImage adds
typed METER/scalar sites without changing the core. Its Program is a structural
projection: PAD occupies those virtual slots for forward-DAG validation ONLY.
The runner never executes those PADs and never reports them as paid work.
PCs are paper offsets minus two (outer M/C are wrapper boundaries). Normalized
NE-invalid/BR-true implements the paper's EQ-valid/BR-not without a hidden NOT.

Only State and the caller's zero-entry Scratch hold acquired worker storage.
The explicit current packet is not inspected until admitted C/entry MOV; each
paid scalar destroys its consumed host reference. No callback, label queue,
old staging copy, codeword, success bitmap or worker V/A/W counter survives.
All reads are actual READ2, all merge/parity/address work actual instructions.
Gate arguments use fixed public suffixes and the current paid address only.
Failed prefixes release unvisited obligations at their CONTROL branch, not by
prepaying/refunding gates. COMMIT reserves all four retirement writes even
for invalid staging, encoding rejection, zero staging or a failed first cell.

BEGIN binds the one State, not a policy snapshot. The caller still owns the
grouped acquisition calendar, packet provenance, G-derived public_tail, and
one-shot delivery/no retry. Faults/interleaving inside a call are forbidden.
Immutable Python objects are not a sandbox or scalar-custody enforcement.
Results are one-way observations after S/shutdown/interruption, never inputs,
payment proofs or continuations. Technical failures retain actual effects and
do not fabricate S, shutdown or rollback. Full linked ABI ROM, transport and
whole-context conformance (including oracle templates) remain unimplemented.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum, auto
from types import MappingProxyType
from typing import Final

from . import machine, meter, physical
from .machine import (
    ADDRESS, PC, R0, R1, R2, R3, Charge, Instruction, Opcode, Operand,
    OperandKind, Program, StepResult, StepStatus, immediate,
)
from .protocol import BeginFrame, Code, Phase, ScalarTag, Service, scalar_from_value
from .services import EventKind, MeterStage, ServiceEvent, ServiceStatus
from .state import SCRATCH_ADDRESS_OFFSET, SCRATCH_FLAGS_OFFSET, SCRATCH_PC_OFFSET, SCRATCH_R0_OFFSET, Scratch, State


_EXIT: Final = meter.Cost(8)
_CLEAR_EXIT: Final = meter.Cost(64, (1, 1, 1, 1))
_C: Final = Charge.CONTROL_A
_COLUMNS: Final = (*range(1, 16), 1, 2, 4, 8, 15)
_F0: Final = Operand(OperandKind.FLAGS, 0, 1)  # stored validity is INVALID
_F3: Final = Operand(OperandKind.FLAGS, 3, 1)  # last gate rejected


class GateKind(Enum):
    ENCODING = auto()
    WRITE = auto()


@dataclass(frozen=True, slots=True)
class GateSite:
    """One public literal METER binding; no callback or acquired quote."""

    kind: GateKind
    local_remainder: meter.Cost


@dataclass(frozen=True, slots=True)
class ScalarSite:
    tag: ScalarTag


@dataclass(frozen=True, slots=True)
class GateImage:
    """Immutable mixed ROM and finite suffix tables, not execution authority.

    Run entrypoints accept only public service/code/header inputs, never an
    image. Gate/scalar slots have sequential edges in the validation projection;
    every CONTROL, access, kernel and S is the unchanged real core instruction.
    accepted[source] differs only at the BR immediately following a write M.
    rejected differs only at paid branches that can release the optional loop.
    """

    service: Service
    argument: int
    sites: tuple[Instruction | GateSite | ScalarSite, ...]
    program: Program
    gates: Mapping[int, GateSite]
    scalars: Mapping[int, ScalarSite]
    local: tuple[meter.Cost, ...]
    accepted: tuple[tuple[meter.Cost, ...], ...]
    rejected: tuple[meter.Cost, ...]
    cell_branches: frozenset[int]
    encoding_branches: frozenset[int]
    after_control: meter.Cost
    outer_body: meter.Cost
    minimum: meter.Cost
    full_price: meter.Cost


@dataclass(frozen=True, slots=True)
class GateEvent:
    """Actual M128 event; not a fabricated machine opcode or paid PAD."""

    pc: int
    next_pc: int
    site: GateSite
    outcome: meter.GateResult
    paid: meter.Cost


@dataclass(frozen=True, slots=True)
class TeachingResult:
    service: Service
    status: ServiceStatus
    trace: tuple[ServiceEvent | GateEvent | StepResult, ...]

    @property
    def vaw(self) -> tuple[int, int, int]:
        """Post-return observer reduction only, not worker prefix storage.

        On funded paths V=A. An interrupted generation before its M still
        contributes V, at the first actually completed generation instruction.
        No truth/teacher comparison is performed, including for corrupt labels.
        """
        visited = sum(isinstance(e, StepResult) and e.charge is Charge.KERNEL
                      and e.opcode is (Opcode.EX if self.service is Service.REP_LESSON
                                       else Opcode.AND)
                      and (self.service is Service.REP_LESSON or (e.pc - 19) % 13 == 0)
                      for e in self.trace)
        attempts = sum(isinstance(e, GateEvent) and e.site.kind is GateKind.WRITE
                       for e in self.trace)
        writes = sum(isinstance(e, StepResult) and e.opcode is Opcode.WRITE2
                     and e.lane is not None and e.lane < 80 for e in self.trace)
        return visited, attempts, writes


class TeachingFailure(RuntimeError):
    def __init__(self, prefix: TeachingResult) -> None:
        super().__init__("teaching interrupted; actual paid prefix remains")
        self.prefix = prefix


def _d(offset: int, width: int) -> Operand:
    return Operand(OperandKind.D, offset, width)


def _r0(width: int) -> Operand:
    return Operand(OperandKind.R0, 0, width)


def _control(op: Opcode, dst: Operand, *args: Operand) -> Instruction:
    return Instruction(op, dst, args, charge=_C)


def _ex(dst: Operand, src: Operand, charge: Charge = _C) -> Instruction:
    return Instruction(Opcode.EX, dst, (src,), charge=charge, extract_width=src.width)


def _stage(pc: int) -> Instruction:
    return Instruction(Opcode.STAGE, target=pc + 1, charge=_C)


def _branch(predicate: Operand, target: int) -> Instruction:
    return Instruction(Opcode.BR, args=(predicate,), target=target, charge=_C)


def _read(k: int) -> Instruction:
    # Four separately paid lane replies capture D[0:8]; no host byte read/pack.
    return Instruction(Opcode.READ2, _r0(2), (ADDRESS,), charge=Charge.ACCESS,
                       capture=_d(2 * k, 2))


def _write(src: Operand) -> Instruction:
    return Instruction(Opcode.WRITE2, args=(ADDRESS, src), charge=Charge.ACCESS)


def _unit(source: int) -> meter.Material4:
    return int(source == 0), int(source == 1), int(source == 2), int(source == 3)


def _finish(service: Service, argument: int,
            sites: list[Instruction | GateSite | ScalarSite],
            costs: list[meter.Cost], full_price: meter.Cost) -> GateImage:
    """Static public-ROM compiler only; no State/Scratch/packets enter here."""
    program = Program(tuple(ins if type(ins) is Instruction else
                            Instruction(Opcode.PAD, charge=Charge.PADDING) for ins in sites))
    expected = {Service.BLOCK_LESSON: (44, 33), Service.REP_LESSON: (56, 38),
                Service.COMMIT: (291, 121)}[service]
    proof = machine.validate(program)
    if (len(sites), proof.control_path_bound[0]) != expected or proof.regions != (_C,):
        raise ValueError("teaching ROM does not match its frozen literal CONTROL witness")
    gates = {pc: ins for pc, ins in enumerate(sites) if isinstance(ins, GateSite)}
    scalars = {pc: ins for pc, ins in enumerate(sites) if isinstance(ins, ScalarSite)}
    cells = frozenset(pc + 1 for pc, ins in gates.items() if ins.kind is GateKind.WRITE)
    encoding = frozenset(p for pc, ins in gates.items() if ins.kind is GateKind.ENCODING
                         for p in (pc + 1, pc + 2))
    local = [meter.ZERO] * len(sites)
    remaining = meter.ZERO
    for pc in reversed(range(len(sites))):
        local[pc] = remaining
        site = sites[pc]
        # Optional writes are not promised before their own M. Encoding's
        # mandatory entry similarly excludes the optional 20-cell loop.
        if isinstance(site, GateSite) and site.kind is GateKind.ENCODING:
            remaining = meter.add_cost(meter.FEE, site.local_remainder)
        else:
            remaining = meter.add_cost(costs[pc], remaining)
    accepted = []
    for source in range(4):
        row = list(local)
        for pc in cells:
            row[pc] = meter.add_cost(row[pc], meter.Cost(23, _unit(source)))
        accepted.append(tuple(row))
    rejected = list(local)
    for pc in cells | encoding:
        rejected[pc] = _CLEAR_EXIT if service is Service.COMMIT else _EXIT
    body = meter.add_cost(meter.Cost(256), remaining)
    return GateImage(service, argument, tuple(sites), program,
                     MappingProxyType(gates), MappingProxyType(scalars), tuple(local),
                     tuple(accepted), tuple(rejected), cells, encoding, remaining,
                     body, body if service is Service.COMMIT else _EXIT, full_price)


def _lesson_image(service: Service) -> GateImage:
    block = service is Service.BLOCK_LESSON
    sites: list[Instruction | GateSite | ScalarSite] = []
    costs: list[meter.Cost] = []

    def emit(ins: Instruction | GateSite | ScalarSite, cost: meter.Cost = meter.ZERO) -> None:
        sites.append(ins)
        costs.append(cost)

    cue, label = (_d(8, 4), _d(12, 1)) if block else (_d(0, 4), _d(4, 1))
    emit(_control(Opcode.MOV, PC, immediate(1, 16)))
    emit(ScalarSite(ScalarTag.LESSON_CUE), meter.Cost(1))
    emit(_control(Opcode.MOV, cue, _r0(4)))
    emit(ScalarSite(ScalarTag.LESSON_LABEL), meter.Cost(1))
    emit(_control(Opcode.MOV, label, _r0(1)))
    emit(_ex(R0, cue))
    emit(_control(Opcode.SHR, R1, R0, immediate(2)))
    if block:
        emit(_control(Opcode.SHL, R1, R1, immediate(2)))
        emit(_control(Opcode.ADD, R1, R1, immediate(868)))
        emit(_control(Opcode.MOV, _d(16, 11), Operand(OperandKind.R1, 0, 11)))
        emit(_stage(len(sites)))
        emit(_ex(ADDRESS, _d(16, 11)))
        for k in range(4):
            if k:
                emit(_control(Opcode.ADD, ADDRESS, ADDRESS, immediate(1)))
            emit(_read(k), meter.Cost(10))
        # The thirteen literal merge instructions preserve all other raw bits.
        for ins in (
            _ex(R0, _d(0, 8)), _ex(R1, cue),
            _control(Opcode.AND, R1, R1, immediate(3)),
            _control(Opcode.MOV, R2, immediate(1)),
            _control(Opcode.SHL, R2, R2, R1),
            _control(Opcode.XOR, R3, R2, immediate(255)),
            _control(Opcode.AND, R0, R0, R3), _ex(R3, label),
            _control(Opcode.SHL, R3, R3, R1), _control(Opcode.OR, R0, R0, R3),
            _control(Opcode.SHL, R2, R2, immediate(4)),
            _control(Opcode.OR, R0, R0, R2),
            _control(Opcode.MOV, _d(0, 8), _r0(8)),
        ):
            emit(ins)
        emit(_stage(len(sites)))
        emit(_ex(ADDRESS, _d(16, 11)))
        for k in range(4):
            if k:
                emit(_control(Opcode.ADD, ADDRESS, ADDRESS, immediate(1)))
            emit(_write(_d(2 * k, 2)), meter.Cost(14, _unit(k)))
    else:
        for ins in (
            _control(Opcode.SHL, R2, R1, immediate(4)),
            _control(Opcode.SHL, R1, R1, immediate(2)),
            _control(Opcode.ADD, R2, R2, R1),
            _control(Opcode.AND, R0, R0, immediate(3)),
            _control(Opcode.ADD, R2, R2, R0),
            _control(Opcode.MOV, _d(8, 7), Operand(OperandKind.R2, 0, 7)),
        ):
            emit(ins)
        for i in range(5):
            emit(_ex(R0, label, Charge.KERNEL), meter.Cost(1))
            emit(_control(Opcode.MOV, _d(16, 2), _r0(2)))
            emit(_ex(ADDRESS, _d(8, 7)))
            emit(_control(Opcode.ADD, ADDRESS, ADDRESS, immediate(4 * i)))
            emit(_stage(len(sites)))
            emit(GateSite(GateKind.WRITE, meter.Cost((4 - i) * 129 + 8)), meter.FEE)
            emit(_branch(_F3, 53))
            emit(_write(_d(16, 2)))  # Optional cost becomes live only after M.
    emit(_stage(len(sites)))
    emit(_branch(immediate(1, 1), len(sites) + 1))
    emit(Instruction(Opcode.S, charge=Charge.EXIT), _EXIT)
    return _finish(service, 0, sites, costs,
                   meter.Cost(490, (1, 1, 1, 1)) if block
                   else meter.Cost(1154, (5, 5, 5, 5)))


def _commit_image(block: int) -> GateImage:
    sites: list[Instruction | GateSite | ScalarSite] = []
    costs: list[meter.Cost] = []

    def emit(ins: Instruction | GateSite, cost: meter.Cost = meter.ZERO) -> None:
        sites.append(ins)
        costs.append(cost)

    emit(_control(Opcode.MOV, PC, immediate(1, 16)))
    emit(_stage(len(sites)))
    for k in range(4):
        emit(_control(Opcode.MOV, ADDRESS, immediate(868 + 4 * block + k, 11)))
        emit(_read(k), meter.Cost(10))
    emit(_ex(R0, _d(4, 4)))
    # Core BR has positive polarity only. NE computes the invalid predicate
    # in the paper's one comparison slot; this is not a host validity check.
    emit(_control(Opcode.NE, _F0, R0, immediate(15)))
    emit(_ex(R0, _d(0, 4)))
    emit(_control(Opcode.MOV, _d(8, 4), _r0(4)))
    emit(_stage(len(sites)))
    emit(GateSite(GateKind.ENCODING, _CLEAR_EXIT), meter.FEE)
    emit(_branch(_F0, 278))
    emit(_branch(_F3, 278))
    for i, column in enumerate(_COLUMNS):
        emit(_ex(R0, _d(8, 4)))
        for op, dst, args in (
            (Opcode.AND, R0, (R0, immediate(column))),
            (Opcode.SHR, R1, (R0, immediate(2))),
            (Opcode.XOR, R0, (R0, R1)),
            (Opcode.SHR, R1, (R0, immediate(1))),
            (Opcode.XOR, R0, (R0, R1)),
            (Opcode.AND, R0, (R0, immediate(1))),
        ):
            emit(Instruction(op, dst, args), meter.Cost(1))
        emit(_control(Opcode.MOV, _d(16, 2), _r0(2)))
        emit(_control(Opcode.MOV, ADDRESS, immediate(20 * block + i, 11)))
        emit(_stage(len(sites)))
        emit(GateSite(GateKind.WRITE, meter.Cost((19 - i) * 134 + 64, (1, 1, 1, 1))), meter.FEE)
        emit(_branch(_F3, 278))
        emit(_write(_d(16, 2)))
    emit(_control(Opcode.MOV, R0, immediate(0)))
    emit(_stage(len(sites)))
    for k in range(4):
        emit(_control(Opcode.MOV, ADDRESS, immediate(868 + 4 * block + k, 11)))
        emit(_write(_r0(2)), meter.Cost(14, _unit(k)))
    emit(_stage(len(sites)))
    emit(_branch(immediate(1, 1), len(sites) + 1))
    emit(Instruction(Opcode.S, charge=Charge.EXIT), _EXIT)
    return _finish(Service.COMMIT, block, sites, costs,
                   meter.Cost(3756, (1 + 20 * int(block == 0), 1 + 20 * int(block == 1),
                                     1 + 20 * int(block == 2), 1 + 20 * int(block == 3))))


_CATALOG: Final = MappingProxyType({
    (Service.BLOCK_LESSON, 0): _lesson_image(Service.BLOCK_LESSON),
    (Service.REP_LESSON, 0): _lesson_image(Service.REP_LESSON),
    **{(Service.COMMIT, j): _commit_image(j) for j in range(4)},
})


def make_teaching_image(service: Service, argument: int = 0) -> GateImage:
    """Return only one of the six built-in target-independent literal images.

    REP full_price.material is the pre-cue sourcewise maximum, not a promise
    or debit of five units at every source. Actual writes use one paid source.
    """
    if type(service) is not Service or type(argument) is not int:
        raise TypeError("image selection requires Service and a public integer argument")
    try:
        return _CATALOG[service, argument]
    except KeyError:
        raise ValueError("only BLOCK/REP LESSON and four public COMMIT entries exist") from None


def _entry(state: State, scratch: Scratch, begin: BeginFrame, code: Code,
           tail: meter.Cost, *, commit: bool) -> GateImage:
    if type(state) is not State or type(scratch) is not Scratch:
        raise TypeError("teaching requires the exact State and Scratch containers")
    if type(begin) is not BeginFrame or type(code) is not Code or type(tail) is not meter.Cost:
        raise TypeError("teaching requires BeginFrame, Code and an immutable public Cost")
    begin.__post_init__()
    tail.__post_init__()
    expected = Service.COMMIT if commit else (
        Service.BLOCK_LESSON if code is Code.BLOCK else Service.REP_LESSON)
    if (begin.phase is not Phase.ACQUISITION or begin.service is not expected
            or commit and code is not Code.BLOCK):
        raise ValueError("teaching requires acquisition and its matching representation/service")
    if not scratch.is_zero() or begin.state != state.snapshot():
        raise ValueError("teaching requires zero scratch and the matching BEGIN image")
    image = make_teaching_image(expected, begin.argument)
    meter.floor_quote(image.full_price, public_tail=tail)  # Worst-source G overflow preflight.
    return image


def _local(image: GateImage, scratch: Scratch, pc: int) -> tuple[meter.Cost, ...]:
    # Finite G row selection, not a branch, ALU, stock sensor or RAM read.
    # Only the following real CONTROL BR changes execution or releases work.
    if pc in image.encoding_branches:
        return (image.rejected if scratch.read_bits(SCRATCH_FLAGS_OFFSET, 1)
                or scratch.read_bits(SCRATCH_FLAGS_OFFSET + 3, 1) else image.local)
    if pc in image.cell_branches:
        if scratch.read_bits(SCRATCH_FLAGS_OFFSET + 3, 1):
            return image.rejected
        lane = scratch.read_bits(SCRATCH_ADDRESS_OFFSET, 11)
        return image.accepted[physical.DEFAULT_CONFIG.lane_to_hub[lane]]
    return image.local


def _run(state: State, scratch: Scratch, image: GateImage,
         packet: tuple[int, int | None] | None, tail: meter.Cost) -> TeachingResult:
    events: list[ServiceEvent | GateEvent | StepResult] = []  # Observer-only sink.
    try:
        outcome = meter.gate(state, image.outer_body, public_tail=tail, minimum_exit=image.minimum)
        events.append(ServiceEvent(EventKind.METER, 0, 0 if outcome.paid else None,
                                   meter.FEE if outcome.paid else meter.ZERO, MeterStage.OUTER, outcome))
        if not outcome.paid:
            return TeachingResult(image.service, ServiceStatus.SHUTDOWN, tuple(events))
        if not outcome.enough:
            paid = meter.debit(state, _EXIT, public_tail=tail)
            scratch.clear()
            events.append(ServiceEvent(EventKind.S, 0, None, paid))
            return TeachingResult(image.service, ServiceStatus.EXIT, tuple(events))
        del outcome
        paid = meter.debit(state, meter.Cost(256), image.after_control, tail)
        events.append(ServiceEvent(EventKind.CONTROL, 0, 0, paid))
        # No other call path grants CONTROL, accepts an image/receipt, resumes,
        # or invokes machine.execute (which would pay C a second time).
        while True:
            pc = scratch.read_bits(SCRATCH_PC_OFFSET, 16)
            if pc in image.scalars:
                tag = image.scalars[pc].tag
                if type(packet) is not tuple or len(packet) != 2:
                    raise TypeError("admitted teaching requires one current (cue, label) tuple")
                index = int(tag is ScalarTag.LESSON_LABEL)
                value = packet[index]  # One scalar's transient, never a later-stage cache.
                if type(value) is not int:
                    raise TypeError("current teaching scalar must be a built-in integer")
                if not 0 <= value <= (1 if index else 15):
                    raise ValueError("current teaching scalar is outside its declared width")
                paid = meter.debit(state, meter.Cost(1), image.local[pc], tail)
                scalar = scalar_from_value(tag, value)
                scratch.write_bits(SCRATCH_R0_OFFSET, 32, scalar.low_bits)
                scratch.write_bits(SCRATCH_PC_OFFSET, 16, pc + 1)
                events.append(ServiceEvent(EventKind.SCALAR, pc, pc + 1, paid, scalar=scalar))
                # Drop the consumed cue immediately; only the still-undelivered
                # label remains in the explicit packet until its own paid site.
                packet = None if index else (0, packet[1])
                del scalar, index, tag, value
            elif pc in image.gates:
                site = image.gates[pc]
                if site.kind is GateKind.ENCODING:
                    current = meter.Cost(2680)
                else:
                    # Address was formed by real CONTROL after paid discovery.
                    lane = scratch.read_bits(SCRATCH_ADDRESS_OFFSET, 11)
                    quote = physical.write_quote((lane,))
                    current = meter.Cost(quote.energy, quote.material)
                    del lane, quote
                outcome = meter.gate(state, current, site.local_remainder, tail,
                                     minimum_exit=site.local_remainder, residue=1)
                if not outcome.paid:
                    raise RuntimeError("reserved teaching gate minimum became unfunded")
                scratch.write_bits(SCRATCH_FLAGS_OFFSET + 3, 1, int(not outcome.enough))
                scratch.write_bits(SCRATCH_PC_OFFSET, 16, pc + 1)
                events.append(GateEvent(pc, pc + 1, site, outcome, meter.FEE))
                del outcome, current, site
            else:
                event = machine._step(image.program, state, scratch, _local(image, scratch, pc), tail)
                events.append(event)
                if event.status is StepStatus.HALT:
                    return TeachingResult(image.service, ServiceStatus.EXIT, tuple(events))
    except (TypeError, ValueError, OverflowError, PermissionError) as error:
        raise TeachingFailure(TeachingResult(image.service, ServiceStatus.INTERRUPTED,
                                             tuple(events))) from error


def run_lesson(state: State, scratch: Scratch, begin: BeginFrame, code: Code,
               packet: tuple[int, int | None] | None,
               public_tail: meter.Cost = meter.ZERO) -> TeachingResult:
    """Run one current lesson; 136 rejection, BLOCK 490, full REP 1154.

    BLOCK requires one material per source and admits its whole transfer.
    REP admits at E>=1040+T.energy with no write material promised, then stops
    at the first unaffordable code write. Full REP needs 1155+T and five units
    at the cue's paid source only. Failed/missing scalar delivery never retries.
    """
    image = _entry(state, scratch, begin, code, public_tail, commit=False)
    del begin
    # Move, rather than retain another packet in this suspended wrapper frame.
    # The handoff is EMPTY before the engine starts; it cannot deliver later.
    handoff = [packet]
    del packet
    return _run(state, scratch, image, handoff.pop(), public_tail)


def run_commit(state: State, scratch: Scratch, begin: BeginFrame, code: Code,
               public_tail: meter.Cost = meter.ZERO) -> TeachingResult:
    """Scheduled fourth-lesson COMMIT; mandatory 616/v, full 3756/(v+20e_j).

    j is begin.argument, NEVER a cyclic tick-derived block or past lesson table.
    E>=617+T and v+T.material fund the mandatory base. Encoding additionally
    tests 2680 energy, but no optional write material, even for invalid flags.
    Four stored validity bits alone determine eligibility. Every funded path
    clears the selected eight staging bits through four real WRITE2 operations.
    """
    image = _entry(state, scratch, begin, code, public_tail, commit=True)
    del begin
    return _run(state, scratch, image, None, public_tail)