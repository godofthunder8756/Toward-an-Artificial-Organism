"""Literal scan ROM for the engineering-only E3 v0.11 instruction component.

make_scan_program accepts ONLY the public representation. Cue D64:4 and
usefulness D68:1 are acquired scratch inputs, never compiler arguments. Tests
construct these fixtures; a future paid input adapter must supply them in a
real service. PC must already name entry zero. No target, clean copy, decode
callback, policy helper, packet, or acquired table is used by this compiler.

The service-traces witness is expanded into elemental machine instructions:
BLOCK has 3699 kernel ALUs + 20 READ2 = 4039 routed energy; REP has 34 + 5
READ2 = 119. B3 administration is respectively 39/8 CONTROL instructions;
base calculation/save adds 5/7. execute prepays one actual C256 and pays S8,
so these standalone fragments cost 4303/383, NOT a complete service tariff.

There is no M128, DECIDE, sensor, scalar ownership, response/output/yield,
repair, policy action, service-suffix admission, or full-worker conformance.
Default remainders retain S only. Failures retain the machine's paid prefix;
there is no rollback, implicit cleanup, death classification, or resume token.
All dynamic working values stay within the existing Scratch. Returned traces
and summaries are observer-only AFTER S; no result is handed back to a worker.
No fault is scheduled inside this component's fault-free operation window.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from . import machine, meter
from .coding import GENERATOR_COLUMNS
from .machine import (
    ADDRESS, R0, R1, R2, R3, Charge, FragmentResult, Instruction, Opcode,
    Operand, OperandKind, Program, immediate,
)
from .protocol import Code
from .state import Scratch, State


# Literal ABI slots, not stored acquired values. Raw is NEVER a 40-bit operand.
CUE: Final = Operand(OperandKind.D, 64, 4)
USEFULNESS: Final = Operand(OperandKind.D, 68, 1)
BASE: Final = Operand(OperandKind.D, 69, 7)
PAYLOAD: Final = Operand(OperandKind.D, 40, 4)
HEALTH: Final = Operand(OperandKind.D, 55, 2)
RAW_LOW: Final = Operand(OperandKind.D, 0, 32)
RAW_HIGH: Final = Operand(OperandKind.D, 32, 8)
_BEST: Final = Operand(OperandKind.D, 44, 4)
_LOW_COUNT: Final = Operand(OperandKind.D, 48, 5)
_MID_COUNT: Final = Operand(OperandKind.D, 53, 5)
_HIGH_COUNT: Final = Operand(OperandKind.D, 58, 5)
_TIE: Final = Operand(OperandKind.D, 63, 1)
_REPLY: Final = Operand(OperandKind.R0, 0, 2)
_REP_BEST: Final = Operand(OperandKind.D, 44, 1)
_S: Final = Instruction(Opcode.S, charge=Charge.EXIT)


def _code(code: Code) -> None:
    if type(code) is not Code:
        raise TypeError("code must be a Code member, not an integer or agent label")


def _alu(op: Opcode, dst: Operand, *args: Operand,
         charge: Charge = Charge.KERNEL) -> Instruction:
    return Instruction(op, dst, args, charge=charge)


def _control(op: Opcode, dst: Operand, *args: Operand) -> Instruction:
    return _alu(op, dst, *args, charge=Charge.CONTROL_A)


def _base(code: Code) -> list[Instruction]:
    # B2: 20*j = (j<<4)+(j<<2), j=cue>>2. Directly use the named
    # four-bit cue input; do not assume a free fixture copy into R0.
    sites = [
        _control(Opcode.SHR, R1, CUE, immediate(2)),
        _control(Opcode.SHL, R2, R1, immediate(4)),
        _control(Opcode.SHL, R1, R1, immediate(2)),
        _control(Opcode.ADD, R3, R2, R1),
    ]
    if code is Code.REP:
        sites.extend((
            _control(Opcode.AND, R0, CUE, immediate(3)),
            _control(Opcode.ADD, R3, R3, R0),
        ))
    # The computed base is proven 0..63. Name its seven-bit result view:
    # no illegal wide-to-narrow MOV, extra ALU, or host scratch write.
    sites.append(_control(Opcode.MOV, BASE, Operand(OperandKind.R3, 0, 7)))
    return sites


def _capture(index: int, stride: int) -> tuple[Instruction, Instruction]:
    return (
        _control(Opcode.ADD, ADDRESS, R3, immediate(stride * index)),
        Instruction(Opcode.READ2, _REPLY, (ADDRESS,), charge=Charge.ACCESS,
                    capture=Operand(OperandKind.D, 2 * index, 2)),
    )


def _block() -> list[Instruction]:
    observed, distance, best_distance = _LOW_COUNT, _MID_COUNT, _HIGH_COUNT
    sites = [
        _alu(Opcode.MOV, observed, immediate(0, 5)),
        _alu(Opcode.MOV, best_distance, immediate(21, 5)),
        _alu(Opcode.MOV, _BEST, immediate(0, 4)),
        _alu(Opcode.MOV, _TIE, immediate(0, 1)),
    ]
    for index in range(20):
        sites.extend(_capture(index, 1))
        sites.extend((
            _alu(Opcode.LT, R1, _REPLY, immediate(2)),
            _alu(Opcode.ADD, observed, observed, R1),
        ))
    # All twenty paid reads precede every candidate comparison. Expansion is
    # generic ROM, not a runtime Python candidate loop or cached codeword.
    for candidate in range(16):
        sites.extend((
            _control(Opcode.MOV, PAYLOAD, immediate(candidate, 4)),
            _alu(Opcode.MOV, distance, immediate(0, 5)),
            _alu(Opcode.MOV, R3, PAYLOAD),
        ))
        for index, column in enumerate(GENERATOR_COLUMNS):
            sites.extend((
                _alu(Opcode.AND, R0, R3, immediate(column)),
                _alu(Opcode.SHR, R1, R0, immediate(2)),
                _alu(Opcode.XOR, R0, R0, R1),
                _alu(Opcode.SHR, R1, R0, immediate(1)),
                _alu(Opcode.XOR, R0, R0, R1),
                _alu(Opcode.AND, R0, R0, immediate(1)),
                Instruction(Opcode.EX, R1, (RAW_LOW if index < 16 else RAW_HIGH,),
                            extract_offset=2 * (index if index < 16 else index - 16),
                            extract_width=2),
                _alu(Opcode.LT, R2, R1, immediate(2)),
                _alu(Opcode.NE, R1, R1, R0),
                _alu(Opcode.AND, R1, R1, R2),
                _alu(Opcode.ADD, distance, distance, R1),
            ))
        sites.extend((
            _alu(Opcode.LT, R0, distance, best_distance),
            _alu(Opcode.EQ, R1, distance, best_distance),
            _alu(Opcode.OR, R2, _TIE, R1),
            # OR of two predicates is canonical. Its named one-bit result
            # fits SELECT's strict arms without concealed wide truncation.
            _alu(Opcode.SELECT, _TIE, R0, immediate(0, 1),
                 Operand(OperandKind.R2, 0, 1)),
            _alu(Opcode.SELECT, _BEST, R0, immediate(candidate, 4), _BEST),
            _alu(Opcode.SELECT, best_distance, R0, distance, best_distance),
        ))
    sites.extend((
        _alu(Opcode.EQ, R0, observed, immediate(20)),
        _alu(Opcode.EQ, R1, best_distance, immediate(0)),
        _alu(Opcode.AND, R0, R0, R1),
        _alu(Opcode.SELECT, R0, R0, immediate(2), immediate(3)),
        _alu(Opcode.SELECT, R0, _TIE, immediate(1), R0),
        _alu(Opcode.EQ, R1, observed, immediate(0)),
        _alu(Opcode.SELECT, R0, R1, immediate(0), R0),
    ))
    return sites


def _repetition() -> list[Instruction]:
    zeros, ones, observed = _LOW_COUNT, _MID_COUNT, _HIGH_COUNT
    sites = [
        _alu(Opcode.MOV, zeros, immediate(0, 5)),
        _alu(Opcode.MOV, ones, immediate(0, 5)),
    ]
    for index in range(5):
        sites.extend(_capture(index, 4))
        sites.extend((
            _alu(Opcode.EQ, R1, _REPLY, immediate(0)),
            _alu(Opcode.EQ, R2, _REPLY, immediate(1)),
            _alu(Opcode.ADD, zeros, zeros, R1),
            _alu(Opcode.ADD, ones, ones, R2),
        ))
    sites.extend((
        _alu(Opcode.ADD, observed, zeros, ones),
        _alu(Opcode.EQ, R0, observed, immediate(0)),
        _alu(Opcode.EQ, _TIE, zeros, ones),
        # A repetition result is ONE bit. Unwritten D45..47 are dead,
        # never read as a predicate; final MOV zero-extends into PAYLOAD.
        _alu(Opcode.GT, _REP_BEST, ones, zeros),
        _alu(Opcode.SELECT, R1, _REP_BEST, ones, zeros),
        _alu(Opcode.EQ, R2, observed, immediate(5)),
        _alu(Opcode.EQ, R3, R1, immediate(5)),
        _alu(Opcode.AND, R2, R2, R3),
        _alu(Opcode.SELECT, R2, R2, immediate(2), immediate(3)),
        _alu(Opcode.SELECT, R2, _TIE, immediate(1), R2),
        _alu(Opcode.SELECT, R2, R0, immediate(0), R2),
        _alu(Opcode.MOV, R0, R2),
    ))
    return sites


def make_scan_program(code: Code) -> Program:
    """Compile one immutable, branchless, target-independent representation ROM.

    D64:4=cue, D68:1=usefulness; neither is compiled into G. B2 computes and
    retains base D69:7 and R3. B3 captures D0:32/D32:8, scans, then relocates
    payload to D40:4 and health to D55:2 after counters die. REP uses D0:10.
    Health 0/1 means abstain, 2/3 means a unique payload; the earliest tied
    BLOCK candidate and REP's tied zero are NOT valid decoded answers.

    The last two CONTROL instructions expose these result writes in the
    machine's post-effect observer trace. S then destroys all scratch. Health
    MOV uses R0's named two-bit canonical result, not an implicit truncation.
    The program does not preserve counters overwritten by that relocation.
    """
    _code(code)
    sites = _base(code)
    sites.append(Instruction(Opcode.STAGE, target=len(sites) + 1,
                             charge=Charge.CONTROL_A))
    sites.extend(_block() if code is Code.BLOCK else _repetition())
    sites.extend((
        _control(Opcode.MOV, PAYLOAD, _BEST if code is Code.BLOCK else _REP_BEST),
        _control(Opcode.MOV, HEALTH, Operand(OperandKind.R0, 0, 2)),
        _S,
    ))
    return Program(tuple(sites))


@dataclass(frozen=True, slots=True)
class ScanObservation:
    """One-way interpretation of actual result events, not a worker value.

    tied is a predicate (also true when empty), NOT a minimizer count. The
    frozen scan has no ties_count output, so none is invented. No reference
    decoder is invoked to enrich this summary or to reconstruct lost scratch.
    """

    payload: int | None
    health: int
    observed: int
    tied: bool


@dataclass(frozen=True, slots=True)
class ScanFragmentResult:
    """Observer summary and original paid trace; never an execution receipt."""

    observation: ScanObservation
    trace: FragmentResult


def run_scan_fragment(code: Code, state: State, scratch: Scratch, *,
                      local_remainders: tuple[meter.Cost, ...] | None = None,
                      public_tail: meter.Cost = meter.ZERO) -> ScanFragmentResult:
    """Execute constructed inputs, then summarize completed post-effect events.

    Does not seed scratch, read RAM, copy a target, bypass CONTROL prepayment,
    call a decoder, or install an observer callback inside execution. Only
    after execute returns (and S has cleared scratch) are events inspected.
    FragmentFailure propagates unchanged; no partial decode is returned.
    """
    program = make_scan_program(code)
    trace = machine.execute(program, state, scratch,
                            local_remainders=local_remainders, public_tail=public_tail)
    payload, health = trace.steps[-3].value, trace.steps[-2].value
    assert payload is not None and health is not None
    observed_slot = _LOW_COUNT if code is Code.BLOCK else _HIGH_COUNT
    observed = tied = None
    # This traversal is observer work AFTER execution, never worker scratch.
    for event in trace.steps:
        ins = program.instructions[event.pc - program.base]
        assert ins is not None
        if ins.dst == observed_slot:
            observed = event.value
        elif ins.dst == _TIE:
            tied = event.value
    assert observed is not None and tied is not None
    return ScanFragmentResult(
        ScanObservation(payload if health >= 2 else None, health, observed, bool(tied)),
        trace,
    )