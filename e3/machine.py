"""Bounded instruction foundation for the engineering-only v0.11 design.

The only acquired storage is explicit State(276 bytes) and Scratch(32 bytes).
PC is ALWAYS Scratch[224:16]; host temporaries last one instruction. Programs
are immutable generic ROM, not callbacks, macros, target roots or services.

step() charges kernels/accesses/S and refuses programs containing CONTROL.
execute() is an ENGINEERING_FRAGMENT algorithm: validate the whole forward DAG,
prepay 256 per declared CONTROL region (at most A/B), then run the instructions.
It does NOT charge outer M128, execute DECIDE, or claim an admitted controller,
full worker, service tariff, scalar ownership, or full B02 conformance. No prior
GateResult, boolean receipt, dynamic quote callback, or execution counter grants
free CONTROL. Static path bounds are ROM facts, never acquired fuel slots.

Default remainders retain only the final S=8, not a complete service suffix.
Additional local/public remainders must be immutable, externally constructed
G-derived inputs. Their provenance and sufficiency are trusted obligations.
Failure preserves the actually paid prefix; there is no program rollback,
automatic retirement/clear, shutdown classification, or resumable receipt.

Trace values are returned AFTER payload/PC effects, only to the observer. No
instruction can read a trace, stock, snapshot or ledger. Python encapsulation
is not a sandbox: noninterference, permissions beyond ordinary RAM exclusion,
process isolation, compiled full services and their gates remain pending.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Final

from . import meter, physical
from .state import Scratch, State


class OperandKind(Enum):
    D = auto()
    R0 = auto()
    R1 = auto()
    R2 = auto()
    R3 = auto()
    PC = auto()
    ADDRESS = auto()
    FLAGS = auto()
    IMMEDIATE = auto()


class NumberType(Enum):
    UNSIGNED = auto()
    SIGNED = auto()


class Opcode(Enum):
    MOV = auto()
    EX = auto()
    ADD = auto()
    SUB = auto()
    NEG = auto()
    SHL = auto()
    SHR = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    NOT = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    EQ = auto()
    NE = auto()
    SELECT = auto()
    BR = auto()
    JUMP = auto()
    STAGE = auto()
    READ2 = auto()
    WRITE2 = auto()
    PAD = auto()
    S = auto()


class Charge(Enum):
    KERNEL = auto()
    CONTROL_A = auto()
    CONTROL_B = auto()
    ACCESS = auto()
    PADDING = auto()
    EXIT = auto()


class ExecutionMode(Enum):
    ENGINEERING_FRAGMENT = auto()


class StepStatus(Enum):
    CONTINUE = auto()
    HALT = auto()


def _int(value: int, name: str, low: int, high: int) -> None:
    if type(value) is not int:
        raise TypeError(f"{name} must be a built-in int")
    if not low <= value <= high:
        raise ValueError(f"{name} must be in {low}..{high}")


def _partition(kind: OperandKind) -> tuple[int, int]:
    # Literal ABI, not acquired routing or a worker-visible lookup table.
    match kind:
        case OperandKind.D: return 0, 96
        case OperandKind.R0: return 96, 32
        case OperandKind.R1: return 128, 32
        case OperandKind.R2: return 160, 32
        case OperandKind.R3: return 192, 32
        case OperandKind.PC: return 224, 16
        case OperandKind.ADDRESS: return 240, 11
        case OperandKind.FLAGS: return 251, 5
        case _: raise ValueError("immediate has no scratch partition")


@dataclass(frozen=True, slots=True)
class Operand:
    """Fixed partition slice, or an explicitly typed <=32-bit immediate.

    number describes immediate encoding only. Instructions explicitly select
    signed arithmetic/EX/SHR; a slot has no host-level signed cached value.
    """

    kind: OperandKind
    offset: int = 0
    width: int = 32
    value: int = 0
    number: NumberType = NumberType.UNSIGNED

    def __post_init__(self) -> None:
        if type(self.kind) is not OperandKind or type(self.number) is not NumberType:
            raise TypeError("operand kind/number must be closed enums")
        _int(self.offset, "offset", 0, 95)
        _int(self.width, "width", 1, 32)
        if self.kind is OperandKind.IMMEDIATE:
            if self.offset != 0:
                raise ValueError("immediates have no offset")
            signed = self.number is NumberType.SIGNED
            _int(self.value, "immediate", -(1 << (self.width - 1)) if signed else 0,
                 (1 << (self.width - int(signed))) - 1)
        else:
            _int(self.value, "slot literal", 0, 0)
            if self.number is not NumberType.UNSIGNED:
                raise ValueError("slot interpretation belongs to the instruction")
            if self.offset + self.width > _partition(self.kind)[1]:
                raise ValueError("operand crosses a scratch partition")


def immediate(value: int, width: int = 32,
              number: NumberType = NumberType.UNSIGNED) -> Operand:
    return Operand(OperandKind.IMMEDIATE, width=width, value=value, number=number)


PC: Final = Operand(OperandKind.PC, width=16)
ADDRESS: Final = Operand(OperandKind.ADDRESS, width=11)
R0: Final = Operand(OperandKind.R0)
R1: Final = Operand(OperandKind.R1)
R2: Final = Operand(OperandKind.R2)
R3: Final = Operand(OperandKind.R3)
_CONTROLS: Final = (Charge.CONTROL_A, Charge.CONTROL_B)
_COMPARE: Final = (Opcode.LT, Opcode.LE, Opcode.GT, Opcode.GE, Opcode.EQ, Opcode.NE)
_BINARY: Final = (Opcode.ADD, Opcode.SUB, Opcode.SHL, Opcode.SHR,
                  Opcode.AND, Opcode.OR, Opcode.XOR, *_COMPARE)
_UNARY: Final = (Opcode.MOV, Opcode.EX, Opcode.NEG, Opcode.NOT)


@dataclass(frozen=True, slots=True)
class Instruction:
    """One elemental instruction; no runtime expansion or executable fields.

    EX extracts extract_width bits at extract_offset from its ONE source.
    Signed EX promotes two's complement; MOV always copies/zero-extends bits.
    Signed ADD/SUB/NEG/SHL are checked signed-32 (destination must be 32 bits).
    Unsigned arithmetic wraps modulo destination width, including narrow ADD.
    Signed SHR is arithmetic; unsigned SHR is logical. Shift counts are 0..31.
    Boolean operations/MOV/SELECT preserve raw bits, not implicit sign extension.
    Comparisons produce 0/1, SELECT and BR require a canonical 0/1 predicate.

    BR takes one predicate and a literal taken target; false means pc+1.
    STAGE/JUMP, and MOV PC from a literal uint16, set that EXACT next PC, not
    target+1. All transfers must be forward to occupied sites. READ2 inserts in
    one R two-bit slot and optionally a D two-bit capture slot in the same paid
    access. WRITE2 extracts exactly its declared two-bit scratch source.
    """

    opcode: Opcode
    dst: Operand | None = None
    args: tuple[Operand, ...] = ()
    charge: Charge = Charge.KERNEL
    number: NumberType = NumberType.UNSIGNED
    target: int | None = None
    extract_offset: int = 0
    extract_width: int = 0
    capture: Operand | None = None

    def __post_init__(self) -> None:
        _instruction(self)


def _operand(value: Operand) -> None:
    if type(value) is not Operand:
        raise TypeError("operands must be Operand, not callbacks or coercible values")
    value.__post_init__()


def _instruction(ins: Instruction) -> None:
    if type(ins) is not Instruction:
        raise TypeError("ROM sites must be Instruction or unoccupied None")
    if (type(ins.opcode) is not Opcode or type(ins.charge) is not Charge
            or type(ins.number) is not NumberType):
        raise TypeError("instruction opcode/charge/number must be closed enums")
    if type(ins.args) is not tuple:
        raise TypeError("instruction operands must be an immutable tuple")
    for arg in ins.args:
        _operand(arg)
        if arg.kind is OperandKind.PC:
            raise ValueError("PC cannot be saved or used as an ALU operand")
    if ins.dst is not None:
        _operand(ins.dst)
        if ins.dst.kind is OperandKind.IMMEDIATE:
            raise ValueError("an immediate cannot be a destination")
    if ins.capture is not None:
        _operand(ins.capture)
    op = ins.opcode
    arity = (2 if op in _BINARY or op is Opcode.WRITE2 else
             1 if op in _UNARY or op in (Opcode.BR, Opcode.READ2) else
             3 if op is Opcode.SELECT else 0)
    if len(ins.args) != arity:
        raise ValueError("wrong opcode arity")
    writes = op in (*_UNARY, *_BINARY, Opcode.SELECT, Opcode.READ2)
    if writes != (ins.dst is not None):
        raise ValueError("wrong destination for opcode")
    if op in (Opcode.READ2, Opcode.WRITE2):
        expected = Charge.ACCESS
    elif op is Opcode.S:
        expected = Charge.EXIT
    elif op is Opcode.PAD:
        expected = Charge.PADDING
    else:
        expected = None
    if (expected is not None and ins.charge is not expected
            or expected is None and ins.charge not in (Charge.KERNEL, *_CONTROLS)):
        raise ValueError("opcode has an invalid charge class")
    signed_ops = (Opcode.EX, Opcode.ADD, Opcode.SUB, Opcode.NEG,
                  Opcode.SHL, Opcode.SHR, *_COMPARE)
    if ins.number is NumberType.SIGNED:
        if op not in signed_ops:
            raise ValueError("opcode has no signed interpretation")
        if op not in _COMPARE and (ins.dst is None or ins.dst.width != 32):
            raise ValueError("signed arithmetic/promotion requires a 32-bit destination")
        data = ins.args[:1] if op in (Opcode.SHL, Opcode.SHR) else ins.args
        if op is not Opcode.EX and any(arg.width != 32 for arg in data):
            raise ValueError("promote narrow signed values with explicit EX first")
        if op is not Opcode.EX and any(
                arg.kind is OperandKind.IMMEDIATE and arg.number is not NumberType.SIGNED
                for arg in data):
            raise ValueError("signed arithmetic/comparison needs typed signed immediates")
    _int(ins.extract_offset, "extract offset", 0, 31)
    _int(ins.extract_width, "extract width", 0, 32)
    if op is Opcode.EX:
        if (ins.extract_width == 0
                or ins.extract_offset + ins.extract_width > ins.args[0].width
                or ins.dst is None or ins.extract_width > ins.dst.width):
            raise ValueError("invalid extraction range")
    elif ins.extract_offset or ins.extract_width:
        raise ValueError("only EX has an extraction range")
    if op in (Opcode.BR, Opcode.STAGE, Opcode.JUMP):
        if ins.target is None:
            raise ValueError("transfer requires a literal target")
        _int(ins.target, "literal target", 0, 65534)
    elif ins.target is not None:
        raise ValueError("unexpected target")
    if ins.dst is not None and ins.dst.kind is OperandKind.PC:
        if (op is not Opcode.MOV or ins.dst != PC
                or ins.args[0].kind is not OperandKind.IMMEDIATE
                or ins.args[0].width != 16
                or ins.args[0].number is not NumberType.UNSIGNED):
            raise ValueError("only full PC MOV from literal uint16 is permitted")
    if op in (Opcode.MOV, Opcode.SELECT):
        arms = ins.args if op is Opcode.MOV else ins.args[1:]
        if ins.dst is not None and any(arg.width > ins.dst.width for arg in arms):
            raise ValueError("MOV/SELECT cannot conceal truncation; use EX")
    if op in _COMPARE and ins.dst is not None and ins.dst.width not in (1, 32):
        raise ValueError("comparison destination must be a bit or a full register word")
    if op in (Opcode.SELECT, Opcode.BR):
        pred = ins.args[0]
        if pred.kind is OperandKind.IMMEDIATE and pred.value not in (0, 1):
            raise ValueError("predicate must be canonical 0/1")
    if op in (Opcode.SHL, Opcode.SHR) and ins.args[1].kind is OperandKind.IMMEDIATE:
        _int(ins.args[1].value, "shift count", 0, 31)
    if op in (Opcode.READ2, Opcode.WRITE2):
        address = ins.args[0]
        if address != ADDRESS and not (
                address.kind is OperandKind.IMMEDIATE
                and address.number is NumberType.UNSIGNED and address.width == 11):
            raise ValueError("access needs the address field or a literal uint11 lane")
        if address.kind is OperandKind.IMMEDIATE:
            physical.lane_read_cost(address.value)  # permission check; no memory read
        if op is Opcode.READ2:
            if ins.dst is None or ins.dst.width != 2 or ins.dst.kind not in (
                    OperandKind.R0, OperandKind.R1, OperandKind.R2, OperandKind.R3):
                raise ValueError("READ2 reply must be a two-bit R slot")
            if ins.capture is not None and (
                    ins.capture.kind is not OperandKind.D or ins.capture.width != 2):
                raise ValueError("READ2 capture must be a two-bit D slot")
            if ins.capture is not None and ins.dst != Operand(OperandKind.R0, 0, 2):
                raise ValueError("bundled D capture requires the designated R0 low reply slot")
        elif ins.args[1].kind is OperandKind.IMMEDIATE or ins.args[1].width != 2:
            raise ValueError("WRITE2 needs a canonical two-bit scratch source")
    if ins.capture is not None and op is not Opcode.READ2:
        raise ValueError("only READ2 has bundled capture")


@dataclass(frozen=True, slots=True)
class Program:
    """Address-indexed immutable ROM, including optional unoccupied holes.

    Entry is base. Every occupied path terminates in S; even unreachable sites
    are checked. No acquired code selector, continuation or register is stored.
    Target independence is a construction obligation, not proved by immutability.
    """

    instructions: tuple[Instruction | None, ...]
    base: int = 0

    def __post_init__(self) -> None:
        validate(self)


@dataclass(frozen=True, slots=True)
class Validation:
    max_steps: int
    control_path_bound: tuple[int, int]
    regions: tuple[Charge, ...]


def _successors(ins: Instruction, pc: int) -> tuple[int, ...]:
    if ins.opcode is Opcode.S:
        return ()
    if ins.opcode in (Opcode.STAGE, Opcode.JUMP):
        assert ins.target is not None
        return (ins.target,)
    if ins.opcode is Opcode.BR:
        assert ins.target is not None
        return pc + 1, ins.target
    if ins.dst == PC:
        return (ins.args[0].value,)
    return (pc + 1,)


def validate(program: Program) -> Validation:
    """Pure reverse-DAG path proof; storage occupancy is not execution count."""
    if type(program) is not Program or type(program.instructions) is not tuple:
        raise TypeError("program must contain an immutable instruction tuple")
    _int(program.base, "ROM base", 0, 65534)
    sites = program.instructions
    if not sites or len(sites) + program.base > 65535 or sites[0] is None:
        raise ValueError("invalid ROM occupancy or entry")
    # These arrays are temporary STATIC analysis of G, not execution state.
    paths = [(0, 0, 0)] * len(sites)
    seen_a = seen_b = False
    for index in range(len(sites) - 1, -1, -1):
        ins = sites[index]
        if ins is None:
            continue
        _instruction(ins)
        successors = _successors(ins, index + program.base)
        for target in successors:
            if (not index + program.base < target < program.base + len(sites)
                    or sites[target - program.base] is None):
                raise ValueError("all successors must be forward occupied ROM sites")
        tails = tuple(paths[target - program.base] for target in successors)
        steps = 1 + max((tail[0] for tail in tails), default=0)
        a = int(ins.charge is Charge.CONTROL_A) + max((t[1] for t in tails), default=0)
        b = int(ins.charge is Charge.CONTROL_B) + max((t[2] for t in tails), default=0)
        if a > 256 or b > 256:
            raise ValueError("CONTROL path exceeds its prepaid 256 allowance")
        if ins.charge is Charge.CONTROL_B and a:
            raise ValueError("CONTROL B cannot transfer back into region A")
        seen_a |= ins.charge is Charge.CONTROL_A
        seen_b |= ins.charge is Charge.CONTROL_B
        paths[index] = steps, a, b
    if seen_b and not seen_a:
        raise ValueError("CONTROL B requires the preceding A envelope")
    return Validation(paths[0][0], (paths[0][1], paths[0][2]),
                      tuple(region for region, seen in zip(_CONTROLS, (seen_a, seen_b))
                            if seen))


@dataclass(frozen=True, slots=True)
class StepResult:
    """Observer-only post-effect payload; NEVER a next-step input or receipt."""

    pc: int
    opcode: Opcode
    charge: Charge
    paid: meter.Cost
    status: StepStatus
    next_pc: int | None
    value: int | None = None  # raw destination encoding / WRITE2 symbol
    lane: int | None = None


@dataclass(frozen=True, slots=True)
class EnvelopePayment:
    region: Charge
    paid: meter.Cost


@dataclass(frozen=True, slots=True)
class FragmentResult:
    mode: ExecutionMode
    envelopes: tuple[EnvelopePayment, ...]
    steps: tuple[StepResult, ...]


class FragmentFailure(RuntimeError):
    """Technical fragment failure with observer-only completed prefix.

    __cause__ identifies the actual resource/operand/overflow failure. This
    object is not accepted by execute/step and cannot fund a continuation.
    """

    def __init__(self, prefix: FragmentResult) -> None:
        super().__init__("engineering fragment stopped; completed prefix remains paid")
        self.prefix = prefix


def _containers(state: State, scratch: Scratch) -> None:
    if type(state) is not State or type(scratch) is not Scratch:
        raise TypeError("execution requires the exact State and Scratch containers")


def _raw(arg: Operand, scratch: Scratch) -> int:
    if arg.kind is OperandKind.IMMEDIATE:
        return arg.value & ((1 << arg.width) - 1)
    return scratch.read_bits(_partition(arg.kind)[0] + arg.offset, arg.width)


def _signed(raw: int, width: int) -> int:
    return raw - (1 << width) if raw & (1 << (width - 1)) else raw


def _put(dst: Operand, value: int, scratch: Scratch) -> None:
    scratch.write_bits(_partition(dst.kind)[0] + dst.offset, dst.width, value)


def _cost(cost: meter.Cost) -> None:
    if type(cost) is not meter.Cost:
        raise TypeError("remainders must be immutable Cost values, not quote generators")
    cost.__post_init__()


def _bounds(program: Program, local: tuple[meter.Cost, ...] | None,
            tail: meter.Cost) -> tuple[meter.Cost, ...]:
    _cost(tail)
    if local is None:
        local = tuple(meter.ZERO if ins is None or ins.opcode is Opcode.S else meter.Cost(8)
                      for ins in program.instructions)
    if type(local) is not tuple or len(local) != len(program.instructions):
        raise TypeError("local remainders must be an immutable ROM-indexed tuple")
    for ins, bound in zip(program.instructions, local):
        _cost(bound)
        if ins is not None:
            if ins.opcode is not Opcode.S and bound.energy < 8:
                raise ValueError("local remainder must retain final S=8")
            # Validate worst-address arithmetic before any payment, never peek RAM.
            maximum = (meter.Cost(23, (1, 1, 1, 1)) if ins.opcode is Opcode.WRITE2
                       else meter.Cost(17) if ins.opcode is Opcode.READ2
                       else meter.Cost(8) if ins.opcode is Opcode.S else meter.Cost(1))
            meter.floor_quote(maximum, bound, tail)
    return local


def _alu(ins: Instruction, scratch: Scratch) -> int:
    """Current-instruction temporaries only; no memory/stock/trace reads."""
    raw = tuple(_raw(arg, scratch) for arg in ins.args)
    values = tuple(_signed(value, arg.width) for value, arg in zip(raw, ins.args)) \
        if ins.number is NumberType.SIGNED else raw
    op = ins.opcode
    assert ins.dst is not None
    if op is Opcode.EX:
        result = (raw[0] >> ins.extract_offset) & ((1 << ins.extract_width) - 1)
        if ins.number is NumberType.SIGNED:
            result = _signed(result, ins.extract_width)
    elif op is Opcode.MOV:
        result = raw[0]
    elif op is Opcode.SELECT:
        _int(raw[0], "predicate", 0, 1)
        result = raw[1] if raw[0] else raw[2]
    elif op is Opcode.ADD:
        result = values[0] + values[1]
    elif op is Opcode.SUB:
        result = values[0] - values[1]
    elif op is Opcode.NEG:
        result = -values[0]
    elif op in (Opcode.SHL, Opcode.SHR):
        # Signedness applies to the data word, not a narrow unsigned count.
        _int(raw[1], "shift count", 0, 31)
        result = values[0] << raw[1] if op is Opcode.SHL else values[0] >> raw[1]
    elif op is Opcode.AND:
        result = raw[0] & raw[1]
    elif op is Opcode.OR:
        result = raw[0] | raw[1]
    elif op is Opcode.XOR:
        result = raw[0] ^ raw[1]
    elif op is Opcode.NOT:
        result = ~raw[0]
    elif op is Opcode.LT:
        result = int(values[0] < values[1])
    elif op is Opcode.LE:
        result = int(values[0] <= values[1])
    elif op is Opcode.GT:
        result = int(values[0] > values[1])
    elif op is Opcode.GE:
        result = int(values[0] >= values[1])
    elif op is Opcode.EQ:
        result = int(values[0] == values[1])
    elif op is Opcode.NE:
        result = int(values[0] != values[1])
    else:
        raise ValueError("not an ALU opcode")
    if ins.number is NumberType.SIGNED and not -(1 << 31) <= result < (1 << 31):
        raise OverflowError("checked signed-32 arithmetic overflow")
    return result & ((1 << ins.dst.width) - 1)


def _step(program: Program, state: State, scratch: Scratch,
          local: tuple[meter.Cost, ...], tail: meter.Cost) -> StepResult:
    # This private primitive is entered only after public validation and, for
    # CONTROL, execute's own actual prepayment. It accepts no proof boolean.
    pc = _raw(PC, scratch)
    if not program.base <= pc < program.base + len(program.instructions):
        raise ValueError("scratch PC is outside this ROM")
    ins = program.instructions[pc - program.base]
    if ins is None:
        raise ValueError("scratch PC points to an unoccupied ROM site")
    value = lane = None
    next_pc: int | None = pc + 1
    if ins.opcode is Opcode.S:
        cost = meter.Cost(8)
        next_pc = None
    elif ins.opcode in (Opcode.READ2, Opcode.WRITE2):
        lane = _raw(ins.args[0], scratch)
        if ins.opcode is Opcode.READ2:
            cost = meter.Cost(physical.lane_read_cost(lane))
        else:
            quote = physical.write_quote((lane,))
            cost = meter.Cost(quote.energy, quote.material)
            value = _raw(ins.args[1], scratch)
    else:
        cost = meter.ZERO if ins.charge in _CONTROLS else meter.Cost(1)
        if ins.opcode is Opcode.BR:
            pred = _raw(ins.args[0], scratch)
            _int(pred, "predicate", 0, 1)
            if pred:
                next_pc = ins.target
        elif ins.opcode in (Opcode.STAGE, Opcode.JUMP):
            next_pc = ins.target
        elif ins.opcode is not Opcode.PAD:
            value = _alu(ins, scratch)
            if ins.dst == PC:
                next_pc = value
    # All operand, arithmetic, address/permission and quote checks precede debit.
    # READ2 does NOT read even its payload until the physical debit succeeds.
    meter.debit(state, cost, local[pc - program.base], tail)
    if ins.opcode is Opcode.S:
        scratch.clear()
        return StepResult(pc, ins.opcode, ins.charge, cost, StepStatus.HALT, None)
    if ins.opcode is Opcode.READ2:
        assert lane is not None and ins.dst is not None
        value = state.read_lane(lane)
        _put(ins.dst, value, scratch)
        if ins.capture is not None:
            _put(ins.capture, value, scratch)
    elif ins.opcode is Opcode.WRITE2:
        assert lane is not None and value is not None
        state.write_lane(lane, value)
    elif ins.dst is not None and ins.dst != PC:
        assert value is not None
        _put(ins.dst, value, scratch)
    assert next_pc is not None
    _put(PC, next_pc, scratch)
    return StepResult(pc, ins.opcode, ins.charge, cost, StepStatus.CONTINUE,
                      next_pc, value, lane)


def step(program: Program, state: State, scratch: Scratch, *,
         local_remainders: tuple[meter.Cost, ...] | None = None,
         public_tail: meter.Cost = meter.ZERO) -> StepResult:
    """Execute exactly the instruction named by Scratch PC, never a saved PC.

    No zero-cost CONTROL entry exists here. S returns HALT after clearing ALL
    scratch, and writes no next PC. Caller must stop on HALT; a later explicit
    call is a new scheduling request, not an implicit restart or continuation.
    """
    _containers(state, scratch)
    proof = validate(program)
    if proof.regions:
        raise ValueError("standalone step cannot establish CONTROL prepayment")
    local = _bounds(program, local_remainders, public_tail)
    return _step(program, state, scratch, local, public_tail)


def execute(program: Program, state: State, scratch: Scratch, *,
            mode: ExecutionMode = ExecutionMode.ENGINEERING_FRAGMENT,
            local_remainders: tuple[meter.Cost, ...] | None = None,
            public_tail: meter.Cost = meter.ZERO) -> FragmentResult:
    """Prepay declared CONTROL envelopes and run a finite engineering fragment.

    The entry PC must ALREADY be in Scratch; it is never injected for free.
    Envelope debits reserve remaining envelopes, S and public tail. Each later
    step retains its explicit local bound (default S only) and public tail.
    No per-region executed-count, acquired budget, or trace feedback is used.
    """
    _containers(state, scratch)
    if type(mode) is not ExecutionMode:
        raise TypeError("only engineering fragment execution is implemented")
    proof = validate(program)
    local = _bounds(program, local_remainders, public_tail)
    if _raw(PC, scratch) != program.base:
        raise ValueError("fragment entry must already be the scratch PC")
    # Validate envelope arithmetic before the first debit as well.
    meter.floor_quote(meter.Cost(256 * len(proof.regions)), meter.Cost(8), public_tail)
    envelopes: list[EnvelopePayment] = []
    events: list[StepResult] = []  # observer sink only; never read by instructions
    try:
        for index, region in enumerate(proof.regions):
            paid = meter.debit(state, meter.Cost(256),
                               meter.Cost(8 + 256 * (len(proof.regions) - index - 1)),
                               public_tail)
            envelopes.append(EnvelopePayment(region, paid))
        # Static DAG proves termination, so no runtime execution-count slots.
        while True:
            event = _step(program, state, scratch, local, public_tail)
            events.append(event)
            if event.status is StepStatus.HALT:
                break
    except (ValueError, OverflowError, PermissionError) as error:
        raise FragmentFailure(FragmentResult(mode, tuple(envelopes), tuple(events))) from error
    return FragmentResult(mode, tuple(envelopes), tuple(events))


def td_program() -> Program:
    """Literal CT-005 23-ALU witness followed by S, not a td_update callback.

    Entry R0=q, R1=sign-extended reward, R2=m are caller-constructed signed-16
    fixtures in full words. Real Q/reward loads and terminal R2=0 cost extra.
    The last ALU's observer value contains q'; S intentionally destroys it.
    """
    p = Operand(OperandKind.D, 55, 1)
    s = NumberType.SIGNED

    def alu(op: Opcode, dst: Operand, *args: Operand,
            number: NumberType = NumberType.UNSIGNED) -> Instruction:
        return Instruction(op, dst, args, number=number)

    def n(value: int) -> Operand:
        return immediate(value, number=s)

    return Program((
        alu(Opcode.LT, p, R1, n(-256), number=s),
        alu(Opcode.SELECT, R1, p, n(-256), R1),
        alu(Opcode.GT, p, R1, n(256), number=s),
        alu(Opcode.SELECT, R1, p, n(256), R1),
        alu(Opcode.SHL, R3, R1, n(4), number=s),
        alu(Opcode.SHL, R1, R2, n(4), number=s),
        alu(Opcode.SUB, R1, R1, R2, number=s),
        alu(Opcode.ADD, R3, R3, R1, number=s),
        alu(Opcode.SHL, R1, R0, n(4), number=s),
        alu(Opcode.SUB, R3, R3, R1, number=s),
        alu(Opcode.SHR, R1, R3, n(7), number=s),
        alu(Opcode.AND, R3, R3, immediate(127)),
        alu(Opcode.GT, R2, R3, immediate(64)),
        alu(Opcode.EQ, p, R3, immediate(64)),
        alu(Opcode.AND, R3, R1, immediate(1)),
        alu(Opcode.AND, R3, R3, p),
        alu(Opcode.OR, R2, R2, R3),
        alu(Opcode.ADD, R1, R1, R2, number=s),
        alu(Opcode.ADD, R0, R0, R1, number=s),
        alu(Opcode.LT, p, R0, n(-32768), number=s),
        alu(Opcode.SELECT, R0, p, n(-32768), R0),
        alu(Opcode.GT, p, R0, n(32767), number=s),
        alu(Opcode.SELECT, R0, p, n(32767), R0),
        Instruction(Opcode.S, charge=Charge.EXIT),
    ))


def selection_program() -> Program:
    """21 actual selection ALUs, three CONTROL EX handoffs, three paid PADs, S.

    Entry R0..R2 hold fresh signed Q values; D64=B, D65:2=T, D67:4=X.
    The full service's paid packet T!=3 check MUST precede this kernel. No
    packet admission or random draw is performed here. Invalid T=3 is not a
    fourth action; callers constructing fixtures must honor the packet ABI.
    """
    p0, p1, p2 = (Operand(OperandKind.D, offset, 1) for offset in (55, 56, 57))
    ranks = Operand(OperandKind.D, 64, 7)

    def alu(op: Opcode, dst: Operand, *args: Operand,
            number: NumberType = NumberType.UNSIGNED) -> Instruction:
        return Instruction(op, dst, args, number=number)

    def rank(dst: Operand, offset: int, width: int) -> Instruction:
        return Instruction(Opcode.EX, dst, (ranks,), charge=Charge.CONTROL_A,
                           extract_offset=offset, extract_width=width)

    return Program((
        alu(Opcode.GT, R3, R0, R1, number=NumberType.SIGNED),
        alu(Opcode.SELECT, R3, R3, R0, R1),
        alu(Opcode.GT, p0, R3, R2, number=NumberType.SIGNED),
        alu(Opcode.SELECT, R3, p0, R3, R2),
        alu(Opcode.EQ, p0, R0, R3), alu(Opcode.EQ, p1, R1, R3),
        alu(Opcode.EQ, p2, R2, R3),
        alu(Opcode.ADD, R0, p0, p1), alu(Opcode.ADD, R0, R0, p2),
        alu(Opcode.SELECT, R1, p1, immediate(1), immediate(2)),
        alu(Opcode.SELECT, R1, p0, immediate(0), R1),
        alu(Opcode.SELECT, R2, p1, immediate(1), immediate(0)),
        alu(Opcode.SELECT, R2, p2, immediate(2), R2),
        rank(R3, 0, 1),
        alu(Opcode.SELECT, R3, R3, R2, R1),
        alu(Opcode.EQ, p0, R0, immediate(2)),
        alu(Opcode.SELECT, R1, p0, R3, R1),
        rank(R2, 1, 2),
        alu(Opcode.EQ, p0, R0, immediate(3)),
        alu(Opcode.SELECT, R1, p0, R2, R1),
        rank(R3, 3, 4),
        alu(Opcode.EQ, p0, R3, immediate(0)),
        alu(Opcode.SELECT, R1, p0, R2, R1),
        alu(Opcode.MOV, R0, R1),
        Instruction(Opcode.PAD, charge=Charge.PADDING),
        Instruction(Opcode.PAD, charge=Charge.PADDING),
        Instruction(Opcode.PAD, charge=Charge.PADDING),
        Instruction(Opcode.S, charge=Charge.EXIT),
    ))