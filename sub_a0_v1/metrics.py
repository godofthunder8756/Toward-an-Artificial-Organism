from __future__ import annotations


def allocation(wr: int, wt: int, nr: int, nt: int, horizon: int) -> dict[str, object]:
    if nr <= 0 or nt <= 0 or horizon <= 0:
        raise ValueError("UNIDENTIFIABLE: both banks need positive opportunities")
    if not 0 <= wr <= nr * horizon or not 0 <= wt <= nt * horizon:
        raise ValueError("Changed destinations exceed opportunities")
    dr = wr / (nr * horizon)
    dt = wt / (nt * horizon)
    no_allocation = dr + dt == 0
    return {
        "density_r": dr, "density_t": dt,
        "opportunities_r": nr * horizon, "opportunities_t": nt * horizon,
        "writes_r": wr, "writes_t": wt,
        "A": 0.0 if no_allocation else (dr - dt) / (dr + dt),
        "flag": "NO_ALLOCATION" if no_allocation else "ALLOCATED",
    }
