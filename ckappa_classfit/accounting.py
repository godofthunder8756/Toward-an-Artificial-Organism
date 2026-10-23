"""One terminal category per scheduled propagation, fit, and B3 stack (E39-7)."""

from __future__ import annotations

from ckappa_classfit.pinned import SYSTEM_ORDER
from ckappa_classfit.rankcats import TERMINAL_CATEGORIES
from ckappa_classfit.schedule import STAGES, UNITS, scheduled_count


class Ledger:
    def __init__(self) -> None:
        self.scheduled = {}
        self.counts = {}
        self.remaining = {}
        self.attempted_detail = {}
        self.closed = {}
        for system in SYSTEM_ORDER:
            for stage in STAGES:
                for unit in UNITS:
                    key = (system, stage, unit)
                    scheduled = scheduled_count(system, stage, unit)
                    self.scheduled[key] = scheduled
                    self.remaining[key] = scheduled
                    self.counts[key] = {name: 0 for name in TERMINAL_CATEGORIES}
                    self.attempted_detail[key] = {
                        "valid_finite": 0,
                        "guard_invalid": 0,
                        "value_error": 0,
                        "non_finite": 0,
                    }
                    self.closed[key] = False

    def add(self, system: str, stage: str, unit: str, category: str, n: int = 1, detail: str | None = None) -> None:
        if n < 0:
            raise ValueError("negative accounting increment")
        if n == 0:
            return
        key = (system, stage, unit)
        if category not in self.counts[key]:
            raise KeyError(category)
        if n > self.remaining[key]:
            raise RuntimeError(f"accounting overrun at {key}: {n} > {self.remaining[key]}")
        self.remaining[key] -= n
        self.counts[key][category] += n
        if category == "ATTEMPTED" and detail is not None:
            self.attempted_detail[key][detail] += n

    def dump_remaining(self, category: str, system: str | None = None, stage: str | None = None, unit: str | None = None) -> None:
        """Assign every still-unattempted call in the selected slice."""
        for key, left in list(self.remaining.items()):
            if left == 0:
                continue
            sys_name, stage_name, unit_name = key
            if system is not None and sys_name != system:
                continue
            if stage is not None and stage_name != stage:
                continue
            if unit is not None and unit_name != unit:
                continue
            self.add(sys_name, stage_name, unit_name, category, left)

    def close_all(self) -> bool:
        ok = True
        for key, left in self.remaining.items():
            total = sum(self.counts[key].values())
            exact = left == 0 and total == self.scheduled[key]
            self.closed[key] = exact
            if not exact:
                ok = False
        return ok

    def records(self) -> list:
        rows = []
        for system in SYSTEM_ORDER:
            for stage in STAGES:
                for unit in UNITS:
                    key = (system, stage, unit)
                    rows.append(
                        {
                            "system": system,
                            "stage": stage,
                            "unit": unit,
                            "scheduled": self.scheduled[key],
                            "counts": dict(self.counts[key]),
                            "attempted_detail": dict(self.attempted_detail[key]),
                            "remaining": self.remaining[key],
                            "closed": self.closed[key],
                        }
                    )
        return rows

    def snapshot(self) -> dict:
        return {"records": self.records()}
