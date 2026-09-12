"""Pure selectors for the engineering-only E3 v0.11 design.

Inputs are ephemeral values, not state objects, Q tables, packets or histories.
The caller supplies the current damaged Q row AFTER any admitted TD update.
Fixed/script callers may supply local placeholders for unused Q/rank arguments;
validation here is NOT a requirement to read Q or consume rank packets. Every
admitted controller still owes its common scan. Paid CONTROL, ACTION gates,
script padding, TD/record work and permission checks belong to a future service.
These functions do none of that work and certify no paid-VM conformance.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Final

from . import arithmetic


class Policy(str, Enum):
    """Component names, deliberately NOT binary protocol policy/configuration IDs.

    FROZEN is a learning permission mode using RL, not another selector.
    NO_MAINT is an unlisted diagnostic comparator, not runner/BIND permission.
    SCRIPT_U/ALL are separately authorized diagnostics, not ordinary fixed arms.
    """

    RL = "RL"
    PERIODIC = "PERIODIC"
    THRESHOLD = "THRESHOLD"
    NO_MAINT = "NO_MAINT"
    DRIVE = "DRIVE"
    SCRIPT_U = "SCRIPT_U"
    SCRIPT_ALL = "SCRIPT_ALL"


ENERGY_CUTS: Final = (24576, 32768, 40960)
MATERIAL_CUTS: Final = (32, 64, 96)
PERIODS: Final = (1, 2, 4, 8, 16, 32, 64, 128, 256)


def _integer(name: str, value: int, lower: int, upper: int) -> None:
    if type(value) is not int:
        raise TypeError(f"{name} must be a built-in integer, not bool")
    if not lower <= value <= upper:
        raise ValueError(f"{name} must be in {lower}..{upper}")


@dataclass(frozen=True, slots=True)
class PolicyConfig:
    """Inherited public constants only; no learned encoding or mutable state.

    Cuts use the v0.5 nine-pair grid; DRIVE and scripts retain the default pair.
    An omitted interval becomes 8 for PERIODIC, otherwise 0 (ABI convention).
    h=3 is a rule, not a parameter. Cuts describe upstream paid observation
    binning and never rebucket a supplied state_index in decide(). Validation
    restricts constants, but cannot prove their provenance or generic-G/reset
    invariance. A future integrator must hold G fixed and freeze engineering
    selections before independent final targets; this API authorizes neither.
    """

    policy: Policy = Policy.RL
    energy_cut: int = 32768
    material_cut: int = 64
    interval: int | None = None

    def __post_init__(self) -> None:
        if type(self.policy) is not Policy:
            raise TypeError("policy must be a Policy member, not a codec ID")
        _integer("energy_cut", self.energy_cut, 0, 65535)
        _integer("material_cut", self.material_cut, 0, 255)
        if self.energy_cut not in ENERGY_CUTS or self.material_cut not in MATERIAL_CUTS:
            raise ValueError("cuts must use the frozen nine-pair engineering grid")
        if self.policy in (Policy.DRIVE, Policy.SCRIPT_U, Policy.SCRIPT_ALL):
            if (self.energy_cut, self.material_cut) != (32768, 64):
                raise ValueError("DRIVE and scripts require default cuts 32768/64")
        interval = self.interval
        if interval is None:
            interval = 8 if self.policy is Policy.PERIODIC else 0
        _integer("interval", interval, 0, 256)
        if self.policy is Policy.PERIODIC:
            if interval not in PERIODS:
                raise ValueError("PERIODIC interval must be a power of two in 1..256")
        elif interval != 0:
            raise ValueError("interval must be zero outside PERIODIC")
        object.__setattr__(self, "interval", interval)


def _config(config: PolicyConfig) -> None:
    if type(config) is not PolicyConfig:
        raise TypeError("config must be a PolicyConfig")


def decide(
    config: PolicyConfig,
    state_index: int,
    q_values: tuple[int, int, int],
    phase_tick: int,
    b: int,
    t: int,
    x: int,
) -> int:
    """Return forage=0, collect=1 or scrub=2 without storing or paying anything.

    state_index is the already paid observation 16*u+8*e+4*p+h (0..31).
    phase_tick is positive uint16 planned phase time, not an action counter;
    phase-specific horizons/admission belong to the caller. All arguments are
    strictly validated even when semantically unused. A returned scrub does
    not imply decoding eligibility, ACTION success, writes or another retry.
    """
    _config(config)
    _integer("state_index", state_index, 0, 31)
    if type(q_values) is not tuple:
        raise TypeError("q_values must be an immutable tuple")
    if len(q_values) != 3:
        raise ValueError("q_values must contain exactly three values")
    for q in q_values:
        _integer("q value", q, arithmetic.SIGNED16_MIN, arithmetic.SIGNED16_MAX)
    _integer("phase_tick", phase_tick, 1, 65535)
    _integer("b", b, 0, 1)
    _integer("t", t, 0, 2)
    _integer("x", x, 0, 15)

    if config.policy in (Policy.RL, Policy.DRIVE):
        return arithmetic.select_action(q_values, b, t, x)
    if state_index & 8 == 0:
        return 0
    if state_index & 4 == 0:
        return 1
    if config.policy is Policy.PERIODIC:
        interval = config.interval
        assert interval is not None  # Canonicalized by immutable configuration.
        trigger = ((phase_tick - 1) & (interval - 1)) == 0
    elif config.policy in (Policy.THRESHOLD, Policy.SCRIPT_ALL):
        trigger = (state_index & 3) == 3
    elif config.policy is Policy.SCRIPT_U:
        trigger = (state_index & 3) == 3 and (state_index & 16) != 0
    else:  # NO_MAINT; PolicyConfig rejects unknown selector values.
        trigger = False
    return 2 if trigger else 0


def policy_action_return(
    config: PolicyConfig,
    action: int | None,
    *,
    accepted_energy: int = 0,
    accepted_material: int = 0,
    completed_writes: int = 0,
    n: int = 20,
) -> int:
    """Return informational a, using arithmetic.action_return's prefix contract.

    DRIVE replaces a by 16 for selected scrub, even for zero completed writes
    or a rejected ACTION, and zero for resource actions regardless of yield.
    Supply action=None for no admitted selection, not for a rejected ACTION.
    No record is created here; None's zero is not an instruction to create one.
    Counts still require valid completed prefixes, including for DRIVE.
    All other policies, including scripts, retain the main action return.
    Task b and final clamping remain separate arithmetic operations.
    """
    _config(config)
    result = arithmetic.action_return(
        action,
        accepted_energy=accepted_energy,
        accepted_material=accepted_material,
        completed_writes=completed_writes,
        n=n,
    )
    if config.policy is Policy.DRIVE:
        return 16 if action == 2 else 0
    return result