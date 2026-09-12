"""Selected TICK/CONDITION trusted runtime foundations, not a full-service VM.

Only State's packed E/P and the caller's 256-bit Scratch are worker storage.
TICK executes fourteen closed physical/scalar sites with its PC in Scratch;
these are NOT machine.Opcode sites or a claim of emitted, linked ABI-9 ROM.
CONDITION executes the literal 9/5 CONTROL witness using machine._step after
THIS invocation pays C256. Its two fixed METER continuations are integrated
here, not supplied as callbacks, arbitrary programs or reusable payment proofs.

CurrentGrant is an explicit privileged scheduler packet, not an input history,
future schedule, lazy provider or custody token. Validate all five quantities
before the passive exception mutates anything. Each later scalar occurrence
actually pays its encoding and inserts into R0. Sequential BIND/BEGIN/SCALAR
transport, process isolation, the full calendar/T builder and general service
compiler remain pending. protocol is only the lower-level frame codec here.

public_tail is an immutable, caller-derived current public G bound. No acquired
RAM, prior result or apparent optional success narrows it. Faults/interleaving
are forbidden inside these synchronous calls. Python privacy is not security.
Returned traces are one-way observer metadata, never worker inputs. No state,
age backup, balance mirror, receipt, continuation or event history is retained.
S pays eight, clears ALL scratch and terminates without another PC write.
Minimum failure sinks only E, with no fabricated fees/cleanup or rollback of
accepted support. A live TICK failing after PASSIVE can leave dirty scratch;
that is terminal shutdown, not a clean, resumable service boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Final

from . import machine, meter, physical
from .machine import (
    ADDRESS, PC, R0, Charge, Instruction, Opcode, Operand, OperandKind,
    Program, StepResult, StepStatus, immediate,
)
from .protocol import ScalarFrame, ScalarTag, Service, scalar_from_value
from .state import SCRATCH_FLAGS_OFFSET, SCRATCH_PC_OFFSET, SCRATCH_R0_OFFSET, Scratch, State


_GRANT_TAGS: Final = (ScalarTag.GRANT_E, ScalarTag.GRANT_P0, ScalarTag.GRANT_P1,
                      ScalarTag.GRANT_P2, ScalarTag.GRANT_P3)


@dataclass(frozen=True, slots=True)
class CurrentGrant:
    """Five CURRENT external quantities at X; no stock or prior-event inputs.

    The selected energy offer is bounded by 30,000 (zero/reduced engineering
    fixtures are allowed); each source quantity is independently 0..255.
    The external scheduler owns phase-specific g, equality of ordinary offers,
    provenance and one-shot delivery. This record does not prove those facts.
    """

    energy: int
    material: meter.Material4

    def __post_init__(self) -> None:
        packet = meter.Cost(self.energy, self.material)
        if packet.energy > 30000 or any(p > 255 for p in packet.material):
            raise ValueError("current grant exceeds selected energy/material bounds")


class EventKind(Enum):
    METER = auto()
    CONTROL = auto()
    DUES = auto()
    LIVING = auto()
    RENT = auto()
    SCALAR = auto()
    TRANSPORT = auto()
    S = auto()


class MeterStage(Enum):
    PASSIVE = auto()
    OUTER = auto()
    CONDITION = auto()


class ServiceStatus(Enum):
    EXIT = auto()  # Includes the funded CONDITION rejection path.
    SHUTDOWN = auto()
    INTERRUPTED = auto()  # Technical failure only; never a funded exit.


@dataclass(frozen=True, slots=True)
class ServiceEvent:
    """Actual post-effect observation, not an instruction or an authorization.

    M/C/dues at CONDITION boundaries do not invent machine ALU opcodes. pc and
    next_pc are actual scratch PCs (equal at those boundaries); None denotes
    termination. TICK's S is a trusted physical primitive, not a fake StepResult.
    """

    kind: EventKind
    pc: int
    next_pc: int | None
    paid: meter.Cost
    stage: MeterStage | None = None
    outcome: meter.GateResult | None = None
    flows: meter.DepositResult | None = None
    scalar: ScalarFrame | None = None
    source: int | None = None
    units: int | None = None

    def __post_init__(self) -> None:
        if type(self.kind) is not EventKind or type(self.paid) is not meter.Cost:
            raise TypeError("events require closed kinds and immutable costs")
        self.paid.__post_init__()
        for pc in (self.pc, self.next_pc):
            if pc is not None and (type(pc) is not int or not 0 <= pc < 65535):
                raise ValueError("event PC must be an occupied-range integer")
        if self.kind is EventKind.METER:
            if type(self.stage) is not MeterStage:
                raise TypeError("METER event requires its closed stage")
            if self.stage is MeterStage.PASSIVE:
                if type(self.flows) is not meter.DepositResult or self.outcome is not None:
                    raise TypeError("PASSIVE requires actual deposit flows")
            elif type(self.outcome) is not meter.GateResult or self.flows is not None:
                raise TypeError("gate event requires its actual outcome")
        elif any(x is not None for x in (self.stage, self.outcome, self.flows)):
            raise ValueError("only METER carries gate/deposit observations")
        if self.kind is EventKind.SCALAR:
            if type(self.scalar) is not ScalarFrame:
                raise TypeError("SCALAR requires a typed current packet")
        elif self.scalar is not None:
            raise ValueError("only SCALAR carries a packet")
        if self.kind is EventKind.TRANSPORT:
            if (type(self.source) is not int or not 0 <= self.source < 4
                    or type(self.units) is not int or not 0 <= self.units <= 255):
                raise ValueError("transport requires a source and accepted uint8 quantity")
        elif self.source is not None or self.units is not None:
            raise ValueError("only TRANSPORT carries source/units")


@dataclass(frozen=True, slots=True)
class ServiceResult:
    service: Service
    status: ServiceStatus
    domain: int | None
    trace: tuple[ServiceEvent | StepResult, ...]


class ServiceFailure(RuntimeError):
    """Technical interruption: actual effects remain, no automatic S or sink.

    prefix contains completed events, not an interrupted instruction's receipt.
    Like machine.FragmentFailure, it is never accepted to resume execution.
    """

    def __init__(self, prefix: ServiceResult) -> None:
        super().__init__("service interrupted; actual paid prefix is not rolled back")
        self.prefix = prefix


def _entry(state: State, scratch: Scratch, tail: meter.Cost) -> None:
    if type(state) is not State or type(scratch) is not Scratch:
        raise TypeError("service requires the exact State and Scratch containers")
    if type(tail) is not meter.Cost:
        raise TypeError("public_tail must be an immutable current G-derived Cost")
    tail.__post_init__()
    if not scratch.is_zero():
        raise ValueError("service entry requires all 256 scratch bits zero")


def _pc(scratch: Scratch) -> int:
    return scratch.read_bits(SCRATCH_PC_OFFSET, 16)


def _advance(scratch: Scratch, pc: int) -> None:
    scratch.write_bits(SCRATCH_PC_OFFSET, 16, pc + 1)


# Literal private service sites, not input-driven macros or a scalar callback.
# METER at 0 is PASSIVE; at 1 it is the sole admission fee.
_TICK_SITES: Final = (
    EventKind.METER, EventKind.METER,
    EventKind.SCALAR, EventKind.SCALAR, EventKind.SCALAR,
    EventKind.SCALAR, EventKind.SCALAR,
    EventKind.TRANSPORT, EventKind.TRANSPORT, EventKind.TRANSPORT, EventKind.TRANSPORT,
    EventKind.LIVING, EventKind.RENT, EventKind.S,
)


def _tick_cost(pc: int, scratch: Scratch) -> meter.Cost:
    # Quote primitive: only public site and PASSIVE's current paid-accounting
    # slots. No stock peek, RAM read, old event, or worker arithmetic callback.
    kind = _TICK_SITES[pc]
    if kind is EventKind.TRANSPORT:
        return meter.Cost(scratch.read_bits(8 * (pc - 7), 8))
    return meter.Cost({EventKind.SCALAR: 1, EventKind.LIVING: 16,
                       EventKind.RENT: 20, EventKind.S: 8}[kind])


def _tick_suffix(pc: int, scratch: Scratch) -> meter.Cost:
    # Finite G suffix selection within the already named METER, not escrow.
    return meter.Cost(sum(_tick_cost(i, scratch).energy for i in range(pc + 1, 14)))


def run_tick(state: State, scratch: Scratch, grant: CurrentGrant, *,
             public_tail: meter.Cost) -> ServiceResult:
    """Pay 177+sum(accepted P), zero CONTROL/material debits, or shut down.

    Validate all inputs and worst-case arithmetic BEFORE passive mutation.
    Initial E=0 ignores all support and does no scratch/live work. Otherwise
    PASSIVE deposits once and captures accepted P in D0..31. The full minimum
    is M128 + (49+accepted transport) + T + one, sourcewise including T.
    Failure leaves accepted P and RAM intact; loss includes accepted E.
    """
    _entry(state, scratch, public_tail)
    if type(grant) is not CurrentGrant:
        raise TypeError("grant must be an immutable CurrentGrant, not a tuple/history/provider")
    grant.__post_init__()
    packet = meter.Cost(grant.energy, grant.material)
    scalars = tuple(scalar_from_value(tag, value)
                    for tag, value in zip(_GRANT_TAGS, (grant.energy, *grant.material)))
    meter.floor_quote(meter.Cost(177 + sum(grant.material)), public_tail=public_tail)
    events: list[ServiceEvent | StepResult] = []  # One-way observer sink only.
    try:
        while True:
            pc = _pc(scratch)
            kind = _TICK_SITES[pc]
            if pc == 0:
                flows = meter.passive_grant(state, packet, permitted=packet)
                if state.energy == 0:
                    events.append(ServiceEvent(kind, pc, None, meter.ZERO,
                                               MeterStage.PASSIVE, flows=flows))
                    return ServiceResult(Service.TICK, ServiceStatus.SHUTDOWN, None, tuple(events))
                for j in range(4):
                    scratch.write_bits(8 * j, 8, flows.accepted.material[j])
                _advance(scratch, pc)
                events.append(ServiceEvent(kind, pc, pc + 1, meter.ZERO,
                                           MeterStage.PASSIVE, flows=flows))
                del flows  # All subsequent grant-derived work uses current D.
            elif pc == 1:
                body = _tick_suffix(pc, scratch)
                outcome = meter.gate(state, body, public_tail=public_tail, minimum_exit=body)
                if not outcome.paid:
                    events.append(ServiceEvent(kind, pc, None, meter.ZERO,
                                               MeterStage.OUTER, outcome))
                    return ServiceResult(Service.TICK, ServiceStatus.SHUTDOWN, None, tuple(events))
                if not outcome.enough:
                    raise RuntimeError("full TICK minimum failed to fund its mandatory body")
                _advance(scratch, pc)
                events.append(ServiceEvent(kind, pc, pc + 1, meter.FEE,
                                           MeterStage.OUTER, outcome))
                del outcome
            else:
                paid = meter.debit(state, _tick_cost(pc, scratch),
                                   _tick_suffix(pc, scratch), public_tail)
                if kind is EventKind.S:
                    scratch.clear()
                    events.append(ServiceEvent(kind, pc, None, paid))
                    return ServiceResult(Service.TICK, ServiceStatus.EXIT, None, tuple(events))
                if kind is EventKind.SCALAR:
                    # Encoding/receiving occurs AFTER its actual one-energy
                    # debit; these are five occurrences, including explicit 0.
                    scalar = scalars[pc - 2]
                    scratch.write_bits(SCRATCH_R0_OFFSET, 32, scalar.low_bits)
                    _advance(scratch, pc)
                    events.append(ServiceEvent(kind, pc, pc + 1, paid, scalar=scalar))
                elif kind is EventKind.TRANSPORT:
                    _advance(scratch, pc)
                    events.append(ServiceEvent(kind, pc, pc + 1, paid,
                                               source=pc - 7, units=paid.energy))
                else:
                    _advance(scratch, pc)
                    events.append(ServiceEvent(kind, pc, pc + 1, paid))
    except (ValueError, OverflowError, PermissionError) as error:
        raise ServiceFailure(ServiceResult(Service.TICK, ServiceStatus.INTERRUPTED,
                                           None, tuple(events))) from error


def _condition_program(domain: int) -> Program:
    """Private fresh literal witness, rebased to zero, without M/C/dues sites.

    The trusted interpreter invokes nested M before PC2 and dues before PC4.
    f3=1 means rejected: METER produces that branch predicate directly, not
    a free NOT or an additional CONTROL instruction. No arbitrary input ROM.
    """
    low, high = physical.age_lanes(domain)
    c = Charge.CONTROL_A
    zero = Operand(OperandKind.R0, 0, 2)
    return Program((
        Instruction(Opcode.MOV, PC, (immediate(1, 16),), charge=c),
        Instruction(Opcode.STAGE, target=2, charge=c),
        Instruction(Opcode.BR, args=(Operand(OperandKind.FLAGS, 3, 1),), target=9, charge=c),
        Instruction(Opcode.STAGE, target=4, charge=c),
        Instruction(Opcode.MOV, R0, (immediate(0),), charge=c),
        Instruction(Opcode.MOV, ADDRESS, (immediate(low, 11),), charge=c),
        Instruction(Opcode.WRITE2, args=(ADDRESS, zero), charge=Charge.ACCESS),
        Instruction(Opcode.MOV, ADDRESS, (immediate(high, 11),), charge=c),
        Instruction(Opcode.WRITE2, args=(ADDRESS, zero), charge=Charge.ACCESS),
        Instruction(Opcode.STAGE, target=10, charge=c),
        Instruction(Opcode.BR, args=(immediate(1, 1),), target=11, charge=c),
        Instruction(Opcode.S, charge=Charge.EXIT),
    ))


def _unit(hub: int) -> meter.Material4:
    return int(hub == 0), int(hub == 1), int(hub == 2), int(hub == 3)


def run_condition(domain: int, state: State, scratch: Scratch, *,
                  public_tail: meter.Cost) -> ServiceResult:
    """Run one public domain 0..19: minimum 520, admitted 552 and b(domain).

    Outer minimum reserves C256+nested M128+S8+T+one. C is really debited
    BEFORE any CONTROL. Nested M reserves S/T then tests the COMPLETE body
    (4-energy medium and two 14-energy WRITE2 with their actual sources).
    Rejection reads/writes no RAM, pays all 520 and still executes final S.
    Full-body admission promotes its finite sourcewise suffix into L; no
    mid-body gate, saved age, rollback, callback, per-lane retry or second C.
    """
    _entry(state, scratch, public_tail)
    program = _condition_program(domain)  # Also exact built-in 0..19 validation.
    proof = machine.validate(program)
    if proof.regions != (Charge.CONTROL_A,) or proof.control_path_bound != (9, 0):
        raise ValueError("conditioner must have the selected single-C literal witness")
    low, high = physical.age_lanes(domain)
    body = meter.Cost(32, physical.conditioning_vector(domain))
    dues = meter.Cost(4, _unit(domain // 5))
    writes = meter.Cost(28, meter.add_cost(meter.Cost(0, _unit(low % 4)),
                                          meter.Cost(0, _unit(high % 4))).material)
    exit_cost = meter.Cost(8)
    after_dues = meter.add_cost(writes, exit_cost)
    after_low = meter.Cost(22, _unit(high % 4))
    full = meter.add_cost(body, exit_cost)
    # Immutable public suffixes; only the paid f3 branch distinguishes PC2.
    admitted_local = (meter.Cost(136), meter.Cost(136), full, full,
                      after_dues, after_dues, after_low, after_low,
                      exit_cost, exit_cost, exit_cost, meter.ZERO)
    rejected_local = (*admitted_local[:2], exit_cost, *admitted_local[3:])
    meter.floor_quote(meter.add_cost(meter.Cost(520), body), public_tail=public_tail)
    events: list[ServiceEvent | StepResult] = []
    try:
        outcome = meter.gate(state, meter.Cost(392), public_tail=public_tail,
                             minimum_exit=meter.Cost(392))
        events.append(ServiceEvent(EventKind.METER, 0, 0 if outcome.paid else None,
                                   meter.FEE if outcome.paid else meter.ZERO,
                                   MeterStage.OUTER, outcome))
        if not outcome.paid:
            return ServiceResult(Service.CONDITION, ServiceStatus.SHUTDOWN, domain, tuple(events))
        if not outcome.enough:
            raise RuntimeError("mandatory CONDITION minimum did not fund its base")
        del outcome
        paid = meter.debit(state, meter.Cost(256), meter.Cost(136), public_tail)
        events.append(ServiceEvent(EventKind.CONTROL, 0, 0, paid))
        # The only path into _step is THIS actual C debit. No public step API,
        # arbitrary program, prepayment flag, receipt or resumed execution.
        while True:
            pc = _pc(scratch)
            if pc == 2:
                outcome = meter.gate(state, body, exit_cost, public_tail,
                                     minimum_exit=exit_cost)
                if not outcome.paid:
                    raise RuntimeError("reserved nested CONDITION minimum became unfunded")
                scratch.write_bits(SCRATCH_FLAGS_OFFSET + 3, 1, int(not outcome.enough))
                events.append(ServiceEvent(EventKind.METER, pc, pc, meter.FEE,
                                           MeterStage.CONDITION, outcome))
                del outcome
            elif pc == 4:
                paid = meter.debit(state, dues, after_dues, public_tail)
                events.append(ServiceEvent(EventKind.DUES, pc, pc, paid))
            local = (rejected_local if scratch.read_bits(SCRATCH_FLAGS_OFFSET + 3, 1)
                     else admitted_local)
            event = machine._step(program, state, scratch, local, public_tail)
            events.append(event)
            if event.status is StepStatus.HALT:
                return ServiceResult(Service.CONDITION, ServiceStatus.EXIT, domain, tuple(events))
    except (ValueError, OverflowError, PermissionError) as error:
        raise ServiceFailure(ServiceResult(Service.CONDITION, ServiceStatus.INTERRUPTED,
                                           domain, tuple(events))) from error