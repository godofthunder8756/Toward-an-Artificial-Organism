"""Pure integer values for the engineering-only E3 v0.11 frozen design.

Returns are informational values, not paid-VM effects, Q writes, deposits,
feedback packets, or record creation. No function retains history, draws
randomness, accesses a target or claims kernel micro-op conformance. Tests of
independent primitive counters are not execution traces of these functions.
Python integers express the bounded signed-32 intermediates without overflow;
all numeric inputs require built-in integers (bool and coercion are rejected).
"""

from collections.abc import Sequence
from typing import Final


SIGNED16_MIN: Final = -32768
SIGNED16_MAX: Final = 32767


def _integer(name: str, value: int, lower: int, upper: int) -> None:
    if type(value) is not int:
        raise TypeError(f"{name} must be a built-in integer, not bool")
    if not lower <= value <= upper:
        raise ValueError(f"{name} must be in {lower}..{upper}")


def td_update(q: int, r: int, m: int, terminal: bool = False) -> int:
    """Return informational q' with clipped reward, round-even and saturation.

    q, stored r, and m must all be signed-16 values, even when terminal=True
    ignores the validated m. Terminal must be a bool. CT-005 floor quotient
    and nonnegative remainder implement negative ties without host floats.
    No Q table, record, fractional residue or protected acquired copy is kept.
    """
    _integer("q", q, SIGNED16_MIN, SIGNED16_MAX)
    _integer("r", r, SIGNED16_MIN, SIGNED16_MAX)
    _integer("m", m, SIGNED16_MIN, SIGNED16_MAX)
    if type(terminal) is not bool:
        raise TypeError("terminal must be a bool")
    reward = min(256, max(-256, r))
    bootstrap = 0 if terminal else m
    numerator = 16 * reward + 15 * bootstrap - 16 * q
    quotient, remainder = divmod(numerator, 128)
    if remainder > 64 or (remainder == 64 and quotient % 2 != 0):
        quotient += 1
    return min(SIGNED16_MAX, max(SIGNED16_MIN, q + quotient))


def action_return(
    action: int | None,
    *,
    accepted_energy: int = 0,
    accepted_material: int = 0,
    completed_writes: int = 0,
    n: int = 20,
) -> int:
    """Return informational exact a for one selected action's completed prefix.

    Actions 0/1/2 mean forage/collect/scrub. Only that action's count may be
    nonzero; this is not a sum of income from unselected actions. Supply the
    already accepted yield, not raw offered yield, and completed writes, not
    failed gates. n is 5 or 20. All-zero counts represent rejection or no work.
    action=None with zero counts gives offline zero, never a missing record.
    """
    if action is not None:
        _integer("action", action, 0, 2)
    _integer("n", n, 5, 20)
    if n not in (5, 20):
        raise ValueError("n must be 5 or 20")
    _integer("accepted_energy", accepted_energy, 0, 64)
    _integer("accepted_material", accepted_material, 0, 8)
    _integer("completed_writes", completed_writes, 0, n)
    counts = (accepted_energy, accepted_material, completed_writes)
    if any(count != 0 and index != action for index, count in enumerate(counts)):
        raise ValueError("unselected actions must have zero counts")
    if action == 0:
        return accepted_energy // 4
    if action == 1:
        return 2 * accepted_material
    if action == 2:
        return -completed_writes
    return 0


def task_return(useful: int | None = None, correct: int | None = None) -> int:
    """Return informational scorer-side b=64*v*(2*c-1), or zero if absent.

    Both inputs must be binary integers for an emitted planned valid response.
    Both None mean no outcome (missing/invalid/unaffordable/unplanned response,
    or disabled feedback). One missing input is an error, not guessed truth.
    This external arithmetic is not a worker oracle, physical yield or packet
    delivery. In isolation/H1 callers must not supply correctness feedback.
    """
    if useful is None and correct is None:
        return 0
    if useful is None or correct is None:
        raise ValueError("supply both outcome bits or neither")
    _integer("useful", useful, 0, 1)
    _integer("correct", correct, 0, 1)
    return 64 * useful * (2 * correct - 1)


def finalize_reward(a: int, b: int = 0) -> int:
    """Return informational clamp(a+b,-256,256), without creating a record.

    a is a signed-16 stored prefix, possibly already corrupt; b is -64, 0,
    or 64. The sum lies in [-32832,32831] and is formed before clamping, never
    wrapped to sixteen bits. This function does not deliver b or finalize a
    worker record; those operations require their own paid ownership checks.
    """
    _integer("a", a, SIGNED16_MIN, SIGNED16_MAX)
    _integer("b", b, -64, 64)
    if b not in (-64, 0, 64):
        raise ValueError("b must be -64, 0, or 64")
    return min(256, max(-256, a + b))


def select_action(q_values: Sequence[int], b: int, t: int, x: int) -> int:
    """Return an informational action using supplied B/T/X categorical ranks.

    q_values is a fresh three-value signed-16 row. Every rank is validated,
    even if unused: B in 0..1, T in 0..2, X in 0..15. X=0 explores with T;
    otherwise choose the only maximum, the B-th of two ascending maxima, or
    T for three maxima. No modulo bias, rejection sampling or PRNG exists.
    This does not establish upstream independence, paid reads, or packet use.
    """
    if not isinstance(q_values, Sequence):
        raise TypeError("q_values must be a finite sequence")
    if len(q_values) != 3:
        raise ValueError("q_values must contain exactly three values")
    row = tuple(q_values)
    for q in row:
        _integer("q value", q, SIGNED16_MIN, SIGNED16_MAX)
    _integer("b", b, 0, 1)
    _integer("t", t, 0, 2)
    _integer("x", x, 0, 15)
    if x == 0:
        return t
    maximum = max(row)
    maxima = tuple(index for index, q in enumerate(row) if q == maximum)
    if len(maxima) == 1:
        return maxima[0]
    if len(maxima) == 2:
        return maxima[b]
    return t