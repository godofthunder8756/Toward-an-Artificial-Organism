"""One engineering ADMIT operation, not transport, a scheduler or a full VM.

The trusted host supplies its scheduled current cue fixture before this call;
the wrapper neither inspects nor validates it until admitted M128 and C256.
Its actual one-energy SCALAR occurrence inserts R0 before the literal ALUs.
This is not paid IPC/current(tag) enforcement. Caller FrameCodec owns G-specific
mask checks; caller scheduler owns schedule provenance and prior RESPONSE slot
retirement. No slot read, implicit pre-clear, history or retirement proof exists.

BEGIN's image is compared only to bind the sole State at entry, never as policy
RAM. Scratch must already be zero. Public tail provenance remains caller-owned.
No faults/interleaving are allowed inside the call. Observer events are returned
only afterward, never payment authority or resumable inputs. Technical failure
keeps actual effects without rollback, S, or fabricated physical shutdown.
"""

from dataclasses import dataclass
from typing import Final

from . import machine, meter
from .machine import (
    ADDRESS, PC, R0, Charge, Instruction, Opcode, Operand, OperandKind,
    Program, StepResult, StepStatus, immediate,
)
from .protocol import BeginFrame, ScalarTag, Service, scalar_from_value
from .services import EventKind, MeterStage, ServiceEvent, ServiceStatus
from .state import SCRATCH_PC_OFFSET, SCRATCH_R0_OFFSET, Scratch, State


_EXIT: Final = meter.Cost(8)
_AFTER_C: Final = meter.Cost(65, (1, 1, 1, 1))
_AFTER_SCALAR: Final = meter.Cost(64, (1, 1, 1, 1))
_BODY: Final = meter.Cost(321, (1, 1, 1, 1))
_FULL: Final = meter.add_cost(meter.FEE, _BODY)
# Exact public post-instruction suffixes, not acquired counters or stock peeks.
_LOCAL: Final = (
    _AFTER_C, *(_AFTER_SCALAR,) * 5,
    meter.Cost(50, (0, 1, 1, 1)), meter.Cost(50, (0, 1, 1, 1)),
    meter.Cost(36, (0, 0, 1, 1)), meter.Cost(36, (0, 0, 1, 1)),
    meter.Cost(22, (0, 0, 0, 1)), meter.Cost(22, (0, 0, 0, 1)),
    _EXIT, _EXIT, _EXIT, meter.ZERO,
)


def _program(slot: int) -> Program:
    """Fresh literal 11-CONTROL witness; M/C/I are real wrapper boundaries.

    Rebases machine sites to zero; I executes at PC1 before SHL, after entry
    MOV. No fake SCALAR opcode, PAD, arbitrary program or extra C envelope.
    """
    c = Charge.CONTROL_A
    sites = [
        Instruction(Opcode.MOV, PC, (immediate(1, 16),), charge=c),
        Instruction(Opcode.SHL, R0, (R0, immediate(1)), charge=c),
        Instruction(Opcode.OR, R0, (R0, immediate(1)), charge=c),
        # R0 is 1..31 here: copying its explicit low byte preserves zero
        # reserved bits without concealing a truncating full-word MOV.
        Instruction(Opcode.MOV, Operand(OperandKind.D, 0, 8),
                    (Operand(OperandKind.R0, 0, 8),), charge=c),
        Instruction(Opcode.STAGE, target=5, charge=c),
    ]
    for k in range(4):  # Public ROM expansion only, not a worker loop.
        sites.extend((
            Instruction(Opcode.MOV, ADDRESS, (immediate(848 + 4 * slot + k, 11),), charge=c),
            Instruction(Opcode.WRITE2, args=(ADDRESS, Operand(OperandKind.D, 2 * k, 2)),
                        charge=Charge.ACCESS),
        ))
    sites.extend((Instruction(Opcode.STAGE, target=14, charge=c),
                  Instruction(Opcode.BR, args=(immediate(1, 1),), target=15, charge=c),
                  Instruction(Opcode.S, charge=Charge.EXIT)))
    return Program(tuple(sites))


@dataclass(frozen=True, slots=True)
class AdmissionResult:
    status: ServiceStatus
    trace: tuple[ServiceEvent | StepResult, ...]


class AdmissionFailure(RuntimeError):
    """Observer-only completed prefix, never a cleanup or continuation receipt."""

    def __init__(self, prefix: AdmissionResult) -> None:
        super().__init__("ADMIT interrupted; actual paid prefix remains")
        self.prefix = prefix


def run_admit(state: State, scratch: Scratch, begin: BeginFrame,
              cue: int | None, public_tail: meter.Cost = meter.ZERO) -> AdmissionResult:
    """Pay 449/(1,1,1,1) on admission, 136/0 on rejection; retain T+one.

    Minimum E=137 (zero-material T); E=450 admits, E=449 rejects leaving 313.
    Missing/malformed admitted cue fails technically AFTER C, before I; rejected
    or unfunded calls do not inspect cue at all. Only exact integers 0..15 enter.
    Public header/container/binding errors are atomic before M, not cue preflight.
    Whole-service G overflow is also rejected before M, even on unfunded paths.
    """
    if type(state) is not State or type(scratch) is not Scratch:
        raise TypeError("ADMIT requires the exact State and Scratch containers")
    if type(begin) is not BeginFrame or type(public_tail) is not meter.Cost:
        raise TypeError("ADMIT requires BeginFrame and an immutable public Cost")
    begin.__post_init__()  # Includes the three legal phases, drain and slot rules.
    public_tail.__post_init__()
    if begin.service is not Service.ADMIT:
        raise ValueError("BEGIN must name ADMIT")
    if not scratch.is_zero() or begin.state != state.snapshot():
        raise ValueError("ADMIT requires zero scratch and the matching BEGIN image")
    # Includes M/C/I, all four source-local writes and S for every public slot.
    # The 136-energy minimum and post-M body alone do not validate the whole G.
    meter.floor_quote(_FULL, public_tail=public_tail)
    program = _program(begin.argument)
    proof = machine.validate(program)
    if proof.regions != (Charge.CONTROL_A,) or proof.control_path_bound != (11, 0):
        raise ValueError("ADMIT requires its literal single-C witness")
    events: list[ServiceEvent | StepResult] = []
    try:
        outcome = meter.gate(state, _BODY, public_tail=public_tail, minimum_exit=_EXIT)
        events.append(ServiceEvent(EventKind.METER, 0, 0 if outcome.paid else None,
                                   meter.FEE if outcome.paid else meter.ZERO,
                                   MeterStage.OUTER, outcome))
        if not outcome.paid:
            return AdmissionResult(ServiceStatus.SHUTDOWN, tuple(events))
        if not outcome.enough:
            # Outer paid admission dispatch goes straight to physical S. No
            # worker BR/PC insertion/C or fabricated machine step on rejection.
            paid = meter.debit(state, _EXIT, public_tail=public_tail)
            scratch.clear()
            events.append(ServiceEvent(EventKind.S, 0, None, paid))
            return AdmissionResult(ServiceStatus.EXIT, tuple(events))
        del outcome
        paid = meter.debit(state, meter.Cost(256), _AFTER_C, public_tail)
        events.append(ServiceEvent(EventKind.CONTROL, 0, 0, paid))
        # Only THIS actual C payment reaches the private engine. The validated
        # forward DAG terminates; no acquired loop counter or prepayment flag.
        while True:
            if scratch.read_bits(SCRATCH_PC_OFFSET, 16) == 1:
                if type(cue) is not int:
                    raise TypeError("admitted cue must be a built-in int")
                if not 0 <= cue <= 15:
                    raise ValueError("admitted cue must be in 0..15")
                paid = meter.debit(state, meter.Cost(1), _AFTER_SCALAR, public_tail)
                scalar = scalar_from_value(ScalarTag.ADMIT_CUE, cue)
                scratch.write_bits(SCRATCH_R0_OFFSET, 32, scalar.low_bits)
                events.append(ServiceEvent(EventKind.SCALAR, 1, 1, paid, scalar=scalar))
                cue = None  # Drop the consumed payload; subsequent work uses Scratch.
                del scalar
            event = machine._step(program, state, scratch, _LOCAL, public_tail)
            events.append(event)
            if event.status is StepStatus.HALT:
                return AdmissionResult(ServiceStatus.EXIT, tuple(events))
    except (TypeError, ValueError, OverflowError, PermissionError) as error:
        raise AdmissionFailure(AdmissionResult(ServiceStatus.INTERRUPTED, tuple(events))) from error