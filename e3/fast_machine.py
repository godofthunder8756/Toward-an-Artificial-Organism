"""Host-only optimization of the engineering-fragment reference interpreter.

No simulated tariff, CONTROL envelope, S, remainder or positive residue is
removed. This is NOT a full service, M128/DECIDE gate, controller, sandbox or
target-independence proof. ROM provenance remains a construction obligation.

execute_fast accepts only the original Program and recompiles/revalidates it
once per call. CompiledProgram is immutable public-G data, not a transferable
validation receipt: even a genuine compiled value is NOT an execution input.
This deliberately avoids trusting frozen dataclasses against object.__setattr__
forgery, cached proofs, digests, callbacks or generated executable code.

The two original private bytearrays remain authoritative. Only their pointers
survive between instructions; there is no whole-scratch integer, register/stock
mirror, PC continuation or acquired execution counter. Small byte slices and
arithmetic temporaries die with the current instruction. PC is read afresh from
Scratch each step. Typed E/P access below belongs solely to the trusted meter,
not the instruction operand space. READ2 payloads are fetched AFTER debit.

The complete reference result types are emitted after effects, into a one-way
observer sink. No snapshots, target inputs, filesystem, network or dependencies
are used. Fault-free, nonconcurrent execution and untampered host module globals
are the same trusted-host obligations as in the reference engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from . import machine, meter, physical
from .machine import (
    Charge, EnvelopePayment, ExecutionMode, FragmentFailure, FragmentResult,
    NumberType, Opcode, Operand, OperandKind, Program, StepResult, StepStatus,
)
from .state import (
    ENERGY_BYTE, LANE_COUNT, MATERIAL_BYTE, SCRATCH_BYTES, STATE_BYTES, Scratch, State,
)


@dataclass(frozen=True, slots=True)
class _Operand:
    start: int
    stop: int
    shift: int
    mask: int
    clear_mask: int
    sign: int
    literal: int | None


@dataclass(frozen=True, slots=True)
class _Payment:
    cost: meter.Cost
    floor: tuple[int, int, int, int, int]


@dataclass(frozen=True, slots=True)
class _Site:
    opcode: Opcode
    charge: Charge
    args: tuple[_Operand, ...]
    dst: _Operand | None
    capture: _Operand | None
    signed: bool
    pc_write: bool
    target: int | None
    extract_offset: int
    extract_mask: int
    extract_sign: int
    payments: tuple[_Payment, ...]


@dataclass(frozen=True, slots=True)
class CompiledProgram:
    """Inspectible static G only; never accepted as proof or acquired state.

    Operand descriptors contain literal bits and <=32-bit slice masks. Floors
    include the caller's validated local/public bounds, not exact-path guesses.
    All arrays are tuples of frozen closed records. Execution compiles afresh
    from Program; mutating/forging this object cannot authorize any work.
    """

    base: int
    sites: tuple[_Site | None, ...]
    regions: tuple[Charge, ...]


_UNIT: Final = meter.Cost(1)
_EXIT: Final = meter.Cost(8)
_CONTROL: Final = meter.Cost(256)
# Cost alternatives and lane indices are inherited physical-map facts only.
_READ_COSTS: Final = (meter.Cost(10), meter.Cost(17))
_WRITE_COSTS: Final = tuple(
    meter.Cost(energy, (int(hub == 0), int(hub == 1), int(hub == 2), int(hub == 3)))
    for energy in (14, 23) for hub in range(4)
)


def _lane_map() -> tuple[tuple[int, int, int, int, int], ...]:
    rows = []
    for row in physical.DEFAULT_CONFIG.lane_rows:
        code = int(row.lane < 80)
        if row.flags == physical.RAM_ACCESSIBLE:
            # Validate the small cost alphabet against the selected map once;
            # this reads no acquired data and does not authorize an access.
            quote = physical.write_quote((row.lane,))
            if (_READ_COSTS[code].energy != physical.lane_read_cost(row.lane)
                    or _WRITE_COSTS[4 * code + row.hub]
                    != meter.Cost(quote.energy, quote.material)):
                raise ValueError("selected physical map differs from compiled costs")
        rows.append((row.flags, row.lane // 4, 2 * (row.lane % 4),
                     code, 4 * code + row.hub))
    return tuple(rows)


_LANES: Final = _lane_map()


def _payment(cost: meter.Cost, local: meter.Cost, tail: meter.Cost) -> _Payment:
    # _bounds already checked signed-32 arithmetic using componentwise maxima
    # >= every actual cost. Do not infer that local is an exact remainder.
    a, b, c = cost.material, local.material, tail.material
    return _Payment(cost, (cost.energy + local.energy + tail.energy + 1,
                          a[0] + b[0] + c[0], a[1] + b[1] + c[1],
                          a[2] + b[2] + c[2], a[3] + b[3] + c[3]))


def compile_program(program: Program, *,
                    local_remainders: tuple[meter.Cost, ...] | None = None,
                    public_tail: meter.Cost = meter.ZERO) -> CompiledProgram:
    """Validate all sites (including unreachable ones) and compile static G.

    No State/Scratch, prior result, boolean proof or target selector is accepted.
    This helper is also used once inside execute_fast, not as a stable cache.
    CONTROL envelope arithmetic is checked at execute's normal entry boundary.
    """
    proof = machine.validate(program)
    local = machine._bounds(program, local_remainders, public_tail)
    operands: dict[Operand, _Operand] = {}
    payments: dict[tuple[Opcode, Charge, meter.Cost], tuple[_Payment, ...]] = {}

    def operand(arg: Operand) -> _Operand:
        if arg not in operands:
            mask = (1 << arg.width) - 1
            literal = arg.kind is OperandKind.IMMEDIATE
            offset = 0 if literal else machine._partition(arg.kind)[0] + arg.offset
            shift = offset % 8
            operands[arg] = _Operand(offset // 8, (offset + arg.width + 7) // 8,
                                     shift, mask, ~(mask << shift),
                                     1 << (arg.width - 1),
                                     arg.value & mask if literal else None)
        return operands[arg]

    sites: list[_Site | None] = []
    for ins, bound in zip(program.instructions, local):
        if ins is None:
            sites.append(None)
            continue
        key = (ins.opcode, ins.charge, bound)
        if key not in payments:
            costs = (_READ_COSTS if ins.opcode is Opcode.READ2 else
                     _WRITE_COSTS if ins.opcode is Opcode.WRITE2 else
                     (_EXIT,) if ins.opcode is Opcode.S else
                     (meter.ZERO,) if ins.charge in machine._CONTROLS else (_UNIT,))
            payments[key] = tuple(_payment(cost, bound, public_tail) for cost in costs)
        sites.append(_Site(
            ins.opcode, ins.charge, tuple(operand(arg) for arg in ins.args),
            None if ins.dst is None else operand(ins.dst),
            None if ins.capture is None else operand(ins.capture),
            ins.number is NumberType.SIGNED, ins.dst == machine.PC, ins.target,
            ins.extract_offset, (1 << ins.extract_width) - 1,
            (1 << (ins.extract_width - 1)) if ins.extract_width else 0,
            payments[key],
        ))
    return CompiledProgram(program.base, tuple(sites), proof.regions)


def _read(data: bytearray, arg: _Operand) -> int:
    if arg.literal is not None:
        return arg.literal
    raw = (data[arg.start] if arg.stop == arg.start + 1 else
           int.from_bytes(data[arg.start:arg.stop], "little"))
    return (raw >> arg.shift) & arg.mask


def _write(data: bytearray, arg: _Operand, value: int) -> None:
    # Only validated, masked, current-instruction values enter this helper.
    if arg.stop == arg.start + 1:
        data[arg.start] = (data[arg.start] & arg.clear_mask) | (value << arg.shift)
    else:
        raw = int.from_bytes(data[arg.start:arg.stop], "little")
        data[arg.start:arg.stop] = ((raw & arg.clear_mask) | (value << arg.shift)).to_bytes(
            arg.stop - arg.start, "little")


def _alu(ins: _Site, data: bytearray) -> int:
    raw = tuple(_read(data, arg) for arg in ins.args)
    values = tuple(value - 2 * arg.sign if value & arg.sign else value
                   for value, arg in zip(raw, ins.args)) if ins.signed else raw
    match ins.opcode:
        case Opcode.MOV:
            result = raw[0]
        case Opcode.EX:
            result = (raw[0] >> ins.extract_offset) & ins.extract_mask
            if ins.signed and result & ins.extract_sign:
                result -= 2 * ins.extract_sign
        case Opcode.ADD:
            result = values[0] + values[1]
        case Opcode.SUB:
            result = values[0] - values[1]
        case Opcode.NEG:
            result = -values[0]
        case Opcode.SHL | Opcode.SHR:
            machine._int(raw[1], "shift count", 0, 31)
            result = (values[0] << raw[1] if ins.opcode is Opcode.SHL
                      else values[0] >> raw[1])
        case Opcode.AND:
            result = raw[0] & raw[1]
        case Opcode.OR:
            result = raw[0] | raw[1]
        case Opcode.XOR:
            result = raw[0] ^ raw[1]
        case Opcode.NOT:
            result = ~raw[0]
        case Opcode.LT:
            result = int(values[0] < values[1])
        case Opcode.LE:
            result = int(values[0] <= values[1])
        case Opcode.GT:
            result = int(values[0] > values[1])
        case Opcode.GE:
            result = int(values[0] >= values[1])
        case Opcode.EQ:
            result = int(values[0] == values[1])
        case Opcode.NE:
            result = int(values[0] != values[1])
        case Opcode.SELECT:
            machine._int(raw[0], "predicate", 0, 1)
            result = raw[1] if raw[0] else raw[2]
        case _:
            raise ValueError("not an ALU opcode")
    if ins.signed and not -(1 << 31) <= result < (1 << 31):
        raise OverflowError("checked signed-32 arithmetic overflow")
    assert ins.dst is not None
    return result & ins.dst.mask


def _debit(data: bytearray, payment: _Payment) -> None:
    """Trusted typed-meter specialization; no resource value escapes to ALUs.

    Floors are prevalidated G; stocks are fetched anew for EACH debit. No prior
    affordability result is reused, nor is any bound paid or source pooled.
    All tests precede the first write. Successful writes fit the original ABI.
    """
    energy = data[ENERGY_BYTE] | (data[ENERGY_BYTE + 1] << 8)
    p0, p1, p2, p3 = (data[MATERIAL_BYTE], data[MATERIAL_BYTE + 1],
                      data[MATERIAL_BYTE + 2], data[MATERIAL_BYTE + 3])
    floor = payment.floor
    if (energy < floor[0] or p0 < floor[1] or p1 < floor[2]
            or p2 < floor[3] or p3 < floor[4]):
        raise meter.InsufficientResources(
            "debit would consume mandatory resources or live residue")
    energy -= payment.cost.energy
    material = payment.cost.material
    data[ENERGY_BYTE] = energy & 255
    data[ENERGY_BYTE + 1] = energy >> 8
    data[MATERIAL_BYTE] = p0 - material[0]
    data[MATERIAL_BYTE + 1] = p1 - material[1]
    data[MATERIAL_BYTE + 2] = p2 - material[2]
    data[MATERIAL_BYTE + 3] = p3 - material[3]


def _step(program: CompiledProgram, state: bytearray, scratch: bytearray) -> StepResult:
    # NO carried PC: fetch the authoritative packed uint16 for this instruction.
    pc = scratch[28] | (scratch[29] << 8)
    if not program.base <= pc < program.base + len(program.sites):
        raise ValueError("scratch PC is outside this ROM")
    ins = program.sites[pc - program.base]
    if ins is None:
        raise ValueError("scratch PC points to an unoccupied ROM site")
    value = lane = None
    next_pc: int | None = pc + 1
    payment = ins.payments[0]
    byte = shift = 0  # current access only, never a lane/payload cache
    if ins.opcode is Opcode.S:
        next_pc = None
    elif ins.opcode in (Opcode.READ2, Opcode.WRITE2):
        lane = _read(scratch, ins.args[0])
        # No negative indexing or use of typed/reserve placement as permission.
        if not 0 <= lane < LANE_COUNT:
            raise ValueError(f"lane must be in 0..{LANE_COUNT - 1}")
        flags, byte, shift, read_index, write_index = _LANES[lane]
        if flags == physical.TYPED_RESERVOIR:
            raise PermissionError("typed reservoirs are not RAM lanes")
        if flags == physical.RAM_RESERVE:
            raise PermissionError("reserve has no agent READ2/WRITE2 access")
        payment = ins.payments[read_index if ins.opcode is Opcode.READ2 else write_index]
        if ins.opcode is Opcode.WRITE2:
            value = _read(scratch, ins.args[1])
    elif ins.opcode is Opcode.BR:
        pred = _read(scratch, ins.args[0])
        machine._int(pred, "predicate", 0, 1)
        if pred:
            next_pc = ins.target
    elif ins.opcode in (Opcode.STAGE, Opcode.JUMP):
        next_pc = ins.target
    elif ins.opcode is not Opcode.PAD:
        value = _alu(ins, scratch)
        if ins.pc_write:
            next_pc = value
    # All semantics, overflow, predicate, address and permission checks precede
    # payment. In particular, quoting a READ2 never fetches its RAM payload.
    _debit(state, payment)
    if ins.opcode is Opcode.S:
        scratch[:] = bytes(SCRATCH_BYTES)
        return StepResult(pc, ins.opcode, ins.charge, payment.cost, StepStatus.HALT, None)
    if ins.opcode is Opcode.READ2:
        value = (state[byte] >> shift) & 3
        assert ins.dst is not None
        _write(scratch, ins.dst, value)
        if ins.capture is not None:
            _write(scratch, ins.capture, value)
    elif ins.opcode is Opcode.WRITE2:
        assert value is not None
        state[byte] = (state[byte] & ~(3 << shift)) | (value << shift)
    elif ins.dst is not None and not ins.pc_write:
        assert value is not None
        _write(scratch, ins.dst, value)
    assert next_pc is not None
    scratch[28] = next_pc & 255
    scratch[29] = next_pc >> 8
    return StepResult(pc, ins.opcode, ins.charge, payment.cost, StepStatus.CONTINUE,
                      next_pc, value, lane)


def execute_fast(program: Program, state: State, scratch: Scratch, *,
                 mode: ExecutionMode = ExecutionMode.ENGINEERING_FRAGMENT,
                 local_remainders: tuple[meter.Cost, ...] | None = None,
                 public_tail: meter.Cost = meter.ZERO) -> FragmentResult:
    """Reference execute API and paid-prefix errors, with host-only fast steps.

    Validation and compilation are INCLUDED on every call, never trusted from
    a caller-supplied CompiledProgram. No trace-free mode or free PC setup.
    Bounds retain exactly the reference's validation and ordering semantics.
    """
    machine._containers(state, scratch)
    if type(mode) is not ExecutionMode:
        raise TypeError("only engineering fragment execution is implemented")
    compiled = compile_program(program, local_remainders=local_remainders,
                               public_tail=public_tail)
    # Exact containers above, and exact fixed-size bytearrays here: no subclass
    # hooks/proxies. These are pointers to the original buffers, NOT copies.
    state_data = getattr(state, "_State__buffer")
    scratch_data = getattr(scratch, "_Scratch__buffer")
    if type(state_data) is not bytearray or type(scratch_data) is not bytearray:
        raise TypeError("execution requires exact bytearray backing buffers")
    if len(state_data) != STATE_BYTES or len(scratch_data) != SCRATCH_BYTES:
        raise ValueError("execution requires the original fixed-size buffers")
    if scratch_data[28] | (scratch_data[29] << 8) != compiled.base:
        raise ValueError("fragment entry must already be the scratch PC")
    meter.floor_quote(meter.Cost(256 * len(compiled.regions)), _EXIT, public_tail)
    envelopes: list[EnvelopePayment] = []
    events: list[StepResult] = []  # append-only observer sink, never worker input
    try:
        for index, region in enumerate(compiled.regions):
            remaining = meter.Cost(8 + 256 * (len(compiled.regions) - index - 1))
            _debit(state_data, _payment(_CONTROL, remaining, public_tail))
            envelopes.append(EnvelopePayment(region, _CONTROL))
        while True:
            event = _step(compiled, state_data, scratch_data)
            events.append(event)
            if event.status is StepStatus.HALT:
                break
    except (ValueError, OverflowError, PermissionError) as error:
        raise FragmentFailure(FragmentResult(mode, tuple(envelopes), tuple(events))) from error
    return FragmentResult(mode, tuple(envelopes), tuple(events))