"""One terminal category per scheduled propagation, fit, and B3 stack (E39-7)."""

from __future__ import annotations

from ckappa_oracle.io import integrity_stop
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
            integrity_stop("negative accounting increment", system=system, stage=stage, unit=unit, n=n)
        if n == 0:
            return
        key = (system, stage, unit)
        if key not in self.counts:
            integrity_stop("accounting key is not scheduled", system=system, stage=stage, unit=unit)
        if category not in self.counts[key]:
            integrity_stop("unknown accounting category", system=system, stage=stage, unit=unit, category=category)
        if n > self.remaining[key]:
            integrity_stop(
                "accounting overrun",
                system=system,
                stage=stage,
                unit=unit,
                n=n,
                remaining=self.remaining[key],
            )
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

    def attempted_totals(self) -> dict:
        """M-3. Partition ATTEMPTED into exact propagations, float propagations, and SVDs."""
        exact = 0
        floats = 0
        svds = 0
        other = 0
        for (system, stage, unit), counts in self.counts.items():
            n = int(counts["ATTEMPTED"])
            del system
            if unit == "propagation" and stage == "S1":
                exact += n
            elif unit == "propagation" and stage in ("S2", "S6"):
                floats += n
            elif unit in ("fit", "b3_stack"):
                svds += n
            else:
                other += n
        return {"exact": exact, "float": floats, "svd": svds, "other": other}
