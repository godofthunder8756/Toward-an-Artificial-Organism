"""Paid mandatory AGE-LOW/HIGH and ISOLATE instruction foundations only.

The selected service/ROM traces are expanded into immutable, generic Program
instructions, rebased to entry zero for machine.execute's ENGINEERING_FRAGMENT
mode. M128 is actually paid here; C256, each routed access, kernel ALU and S8
are actually paid by that engine. This is not a linked full-service VM, frozen
runtime, scheduler, CONDITION, TICK, fault window or complete upkeep pass.

The public service is the ONLY compiler input. Before execution, the wrapper's
METER minimum includes the ENTIRE fixed body and a caller-supplied immutable
G-derived public tail, plus one energy residue. No age discovery, optional body,
per-lane gate, acquisition, callback, hidden loop counter or host ALU on RAM is
used. The engine's default local bound is S8, not the whole service suffix:
full admission suffices here because every fixed instruction executes, all
four-bit ages are valid, and no fault/interleaving is allowed inside this call.
All future debits therefore remain funded sourcewise. The tail is also passed
to the engine; its provenance/sufficiency remains the trusted caller's duty.

Caller owns the sole State and an explicit 32-byte Scratch, initially zero
(fresh allocation or a completed paid S). Dirty entry is NOT cleared for free.
Dynamic operands live only in Scratch; compilation temporaries contain G only.
Results are one-way observer events returned after completion/shutdown, not
worker inputs, receipts, continuations, custody contexts or full primitive
archives. Technical FragmentFailure propagates with its actual paid prefix;
there is no rollback, implicit cleanup, fabricated shutdown or resume API.
Python privacy is not a process isolation or capability-security boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Final

from . import machine, meter, physical
from .machine import (
    ADDRESS, PC, R0, R1, R2, Charge, FragmentResult, Instruction, Opcode,
    Operand, OperandKind, Program, immediate,
)
from .protocol import Service
from .state import Scratch, State


_SERVICES: Final = (Service.AGE_LOW, Service.AGE_HIGH, Service.ISOLATE)


def _service(service: Service) -> None:
    if type(service) is not Service:
        raise TypeError("service must be an exact public Service member")
    if service not in _SERVICES:
        raise ValueError("only mandatory AGE_LOW, AGE_HIGH and ISOLATE are implemented")


def _control(op: Opcode, dst: Operand, *args: Operand) -> Instruction:
    return Instruction(op, dst, args, charge=Charge.CONTROL_A)


def _stage(sites: list[Instruction]) -> None:
    sites.append(Instruction(Opcode.STAGE, target=len(sites) + 1,
                             charge=Charge.CONTROL_A))


def _address(lane: int) -> Instruction:
    return _control(Opcode.MOV, ADDRESS, immediate(lane, 11))


def _write(source: Operand) -> Instruction:
    return Instruction(Opcode.WRITE2, args=(ADDRESS, source), charge=Charge.ACCESS)


def _age_words(sites: list[Instruction], first: int) -> None:
    # Static literal ROM expansion. No State/Scratch or acquired value enters
    # this compiler; first is the fixed public LOW/HIGH range, not a cursor.
    low_raw, high_raw = Operand(OperandKind.D, 0, 2), Operand(OperandKind.D, 2, 2)
    domain_slot, output = Operand(OperandKind.D, 4, 5), Operand(OperandKind.D, 10, 4)
    reply = Operand(OperandKind.R0, 0, 2)
    for domain in range(first, first + 10):
        low, high = physical.age_lanes(domain)
        sites.extend((
            _control(Opcode.MOV, domain_slot, immediate(domain, 5)),
            _address(low),
            Instruction(Opcode.READ2, reply, (ADDRESS,), charge=Charge.ACCESS,
                        capture=low_raw),
            _address(high),
            Instruction(Opcode.READ2, reply, (ADDRESS,), charge=Charge.ACCESS,
                        capture=high_raw),
        ))
        _stage(sites)
        sites.extend((
            Instruction(Opcode.EX, R0, (low_raw,), extract_width=2),
            Instruction(Opcode.EX, R1, (high_raw,), extract_width=2),
            Instruction(Opcode.SHL, R1, (R1, immediate(2))),
            Instruction(Opcode.XOR, R0, (R0, R1)),
            Instruction(Opcode.EQ, R2, (R0, immediate(15))),
            Instruction(Opcode.ADD, R0, (R0, immediate(1))),
            Instruction(Opcode.SELECT, R0, (R2, immediate(15), R0)),
            Instruction(Opcode.AND, output, (R0, immediate(15))),
            _address(low), _write(Operand(OperandKind.D, 10, 2)),
            _address(high), _write(Operand(OperandKind.D, 12, 2)),
        ))


def make_upkeep_program(service: Service) -> Program:
    """Fresh immutable fixed ROM; no program, target, domain or state injection.

    AGE has exactly 63 CONTROL, 80 kernel, 20 READ2, 20 WRITE2 and S.
    ISOLATE has 59 CONTROL, 52 WRITE2 and S. M/C are outside the ROM.
    Every transfer names the following occupied site. There are no dynamic
    branches, instruction macros, runtime loops, padding ops or return PC.
    """
    _service(service)
    sites = [_control(Opcode.MOV, PC, immediate(1, 16))]
    if service is Service.ISOLATE:
        sites.append(_control(Opcode.MOV, R0, immediate(0)))
        for start, stop in ((848, 868), (868, 884), (884, 900)):
            _stage(sites)
            for lane in range(start, stop):
                sites.extend((_address(lane), _write(Operand(OperandKind.R0, 0, 2))))
    else:
        _age_words(sites, 0 if service is Service.AGE_LOW else 10)
    _stage(sites)
    sites.extend((
        Instruction(Opcode.BR, args=(immediate(1, 1),), target=len(sites) + 1,
                    charge=Charge.CONTROL_A),
        Instruction(Opcode.S, charge=Charge.EXIT),
    ))
    return Program(tuple(sites))


def _body_cost(service: Service) -> meter.Cost:
    # Static exact G quote, not stock/age discovery or an arbitrary-program
    # quote engine. Costs include routes ONCE; writes retain their own sources.
    if service is Service.ISOLATE:
        lanes = tuple(range(848, 900))
        reads_and_kernel = 0
    else:
        first = 0 if service is Service.AGE_LOW else 10
        lanes = tuple(lane for d in range(first, first + 10) for lane in physical.age_lanes(d))
        reads_and_kernel = 80 + sum(physical.lane_read_cost(lane) for lane in lanes)
    writes = physical.write_quote(lanes)
    return meter.Cost(256 + reads_and_kernel + writes.energy + 8, writes.material)


class UpkeepStatus(Enum):
    EXIT = auto()
    SHUTDOWN = auto()


@dataclass(frozen=True, slots=True)
class MeterEvent:
    """Observer-only outer M event; failure loss is not operation spending."""

    outcome: meter.GateResult
    paid: meter.Cost


@dataclass(frozen=True, slots=True)
class UpkeepResult:
    """Completed observation, without state copies, resume handles or inputs."""

    service: Service
    status: UpkeepStatus
    outer_meter: MeterEvent
    trace: FragmentResult | None


def run_upkeep(service: Service, state: State, scratch: Scratch, *,
               public_tail: meter.Cost) -> UpkeepResult:
    """Run one named mandatory service; explicitly supply G-derived T (or ZERO).

    AGE pays 952 energy/(5,5,5,5), ISOLATE 1120/(13,13,13,13).
    Funding must cover that price PLUS T and one energy. Unfunded minimum
    sinks only E, pays no fee, and executes no instruction or scratch write.
    Invalid inputs/dirty scratch fail technically before any debit/mutation.
    This entry does not validate public scheduling, own scalar custody, accept
    prior results, revive dead states, or claim full BEGIN/EXIT wire semantics.
    """
    _service(service)
    if type(state) is not State or type(scratch) is not Scratch:
        raise TypeError("upkeep requires the exact State and Scratch containers")
    if type(public_tail) is not meter.Cost:
        raise TypeError("public_tail must be an immutable G-derived Cost, not None or a callback")
    public_tail.__post_init__()
    if not scratch.is_zero():
        raise ValueError("mandatory service entry requires all 256 scratch bits zero")
    program = make_upkeep_program(service)
    machine.validate(program)  # All sites and the one CONTROL region, before M.
    body = _body_cost(service)
    # Identical minimum and body quotes make optional rejection impossible in
    # this fault-free call. Gate validates all arithmetic before touching E/P.
    admission = meter.gate(state, body, public_tail=public_tail, minimum_exit=body)
    if not admission.paid:
        return UpkeepResult(service, UpkeepStatus.SHUTDOWN,
                            MeterEvent(admission, meter.ZERO), None)
    # Immediately consume the paid gate outcome; never pass it to the engine
    # as CONTROL authority, keep a second balance, or select acquired work.
    if not admission.enough:
        raise RuntimeError("mandatory full-body minimum did not guarantee its body")
    trace = machine.execute(program, state, scratch, public_tail=public_tail)
    return UpkeepResult(service, UpkeepStatus.EXIT, MeterEvent(admission, meter.FEE), trace)