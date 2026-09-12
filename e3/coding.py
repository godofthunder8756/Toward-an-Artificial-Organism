"""Pure coding values for the engineering-only E3 v0.11 frozen design.

These functions return informational values, not paid-VM operations. They do
not read physical RAM, charge scans, authorize writes, retain acquired state,
or establish kernel micro-op/register/execution-trace conformance. The generic
immutable codebook contains every possible payload, not a protected acquired
copy. Callers must not use this module to bypass paid live-worker interfaces.

Symbols are integer encodings 0/1 (binary), 2 (erased), and 3 (invalid).
Invalid symbols are ignored like erasures without rewriting the input. There
is deliberately no forced guess or repair API and no target/oracle argument.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final


GENERATOR_COLUMNS: Final[tuple[int, ...]] = tuple(range(1, 16)) + (1, 2, 4, 8, 15)


def _parity(payload: int, column: int) -> int:
    value = payload & column
    value ^= value >> 2
    value ^= value >> 1
    return value & 1


CODEBOOK: Final[tuple[tuple[int, ...], ...]] = tuple(
    tuple(_parity(payload, column) for column in GENERATOR_COLUMNS)
    for payload in range(16)
)


@dataclass(frozen=True, slots=True)
class DecodeResult:
    """Immutable informational summary; never a repair authorization.

    ``payload`` is None for empty or tied scans. ``observed`` counts only
    binary symbols. ``disagreements`` is the minimum observed mismatch count,
    including on nonempty ties, but is None when empty. ``ties_count`` counts
    all minimizing candidates (16 for empty block, 2 for empty repetition).
    Health priority is empty=0, nonempty tied=1, wholly binary agreeing
    unique=2, otherwise unique=3. A self-consistent wrong word is health 2.
    """

    payload: int | None
    health: int
    observed: int
    disagreements: int | None
    ties_count: int


def _symbols(symbols: Sequence[int], length: int) -> tuple[int, ...]:
    if not isinstance(symbols, Sequence):
        raise TypeError("symbols must be a finite sequence")
    if len(symbols) != length:
        raise ValueError(f"expected exactly {length} symbols")
    snapshot = tuple(symbols)
    for symbol in snapshot:
        if type(symbol) is not int:
            raise TypeError("symbols must be built-in integers, not bools")
        if not 0 <= symbol <= 3:
            raise ValueError("symbol encoding must be in 0..3")
    return snapshot


def encode(payload4: int) -> tuple[int, ...]:
    """Return 20 informational binary symbols for an integer payload in 0..15.

    Bit k of the payload pairs with bit k of each fixed generator column.
    The returned tuple is target-independent ROM output, not a physical write.
    """
    if type(payload4) is not int:
        raise TypeError("payload4 must be a built-in integer, not bool")
    if not 0 <= payload4 <= 15:
        raise ValueError("payload4 must be in 0..15")
    return CODEBOOK[payload4]


def decode_block(symbols: Sequence[int]) -> DecodeResult:
    """Return a unique nearest payload or abstain, using only the 20 inputs.

    This host calculation returns informational values, not a priced scan.
    All sixteen candidates are compared; missing symbols never supply a bit.
    """
    snapshot = _symbols(symbols, 20)
    observed = sum(symbol < 2 for symbol in snapshot)
    if observed == 0:
        return DecodeResult(None, 0, 0, None, 16)

    best_payload = 0
    best_distance = 21
    ties_count = 0
    for payload, word in enumerate(CODEBOOK):
        distance = sum(
            symbol < 2 and symbol != bit for symbol, bit in zip(snapshot, word)
        )
        if distance < best_distance:
            best_payload = payload
            best_distance = distance
            ties_count = 1
        elif distance == best_distance:
            ties_count += 1

    if ties_count != 1:
        return DecodeResult(None, 1, observed, best_distance, ties_count)
    health = 2 if observed == 20 and best_distance == 0 else 3
    return DecodeResult(best_payload, health, observed, best_distance, 1)


def decode_repetition(symbols: Sequence[int]) -> DecodeResult:
    """Return informational five-symbol majority/health, never a guessed bit.

    Empty and tied votes abstain. The caller's inputs are neither modified
    nor checked against any hidden original payload or clean copy.
    """
    snapshot = _symbols(symbols, 5)
    zeros = snapshot.count(0)
    ones = snapshot.count(1)
    observed = zeros + ones
    if observed == 0:
        return DecodeResult(None, 0, 0, None, 2)
    disagreements = min(zeros, ones)
    if zeros == ones:
        return DecodeResult(None, 1, observed, disagreements, 2)
    payload = 1 if ones > zeros else 0
    health = 2 if observed == 5 and disagreements == 0 else 3
    return DecodeResult(payload, health, observed, disagreements, 1)