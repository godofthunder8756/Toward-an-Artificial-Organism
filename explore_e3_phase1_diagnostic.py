"""EXPLORATORY post-phase-1 diagnostic (not prespecified; controls only).

E3_ALLOCATION_PROTOCOL_v1.md stopped at phase 1: no configuration met the
headroom criterion, because blind_oracle did not beat uniform/random. This
script asks why, using the control policies only, on engineering seeds 0-7.
No candidate allocator is run. Nothing here changes the protocol outcome.

Question: does blind_oracle's myopic loss model, which assumes no future
repairs, abandon dormant cues so that they are lost before they return?
"""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np

import e3_fep_engineering_seed_v3 as v3
from e3_allocation_study import run_rows

OUT = Path("e3_fep_seed_results/v3/exploratory_phase1_diagnostic.json")
CONFIGS = ((7, 0.02, 2), (9, 0.02, 3), (9, 0.03, 2))
KEYS = ("overall_accuracy", "post_return_accuracy", "steady_accuracy", "lost_at_return_fraction",
        "hot_wrong_fraction", "cold_wrong_fraction", "repairs_per_hot_cue_tick", "repairs_per_cold_cue_tick",
        "harmful_repair_fraction", "binding_fraction")


def main() -> None:
    if OUT.exists():
        sys.exit(f"refusing to overwrite {OUT}")
    report = []
    for bits, p_flip, budget in CONFIGS:
        params = replace(v3.Params(), trace_bits=bits, corrupt_p=p_flip, budget=budget)
        rows = run_rows(params, range(8), v3.CONTROL_POLICIES, 7)
        means = {pol: {k: float(np.nanmean([r[k] for r in rows if r["policy"] == pol])) for k in KEYS}
                 for pol in v3.CONTROL_POLICIES}
        report.append({"width": bits, "corrupt_p": p_flip, "budget": budget, "means": means})
        print(f"\nwidth {bits} p {p_flip} budget {budget}")
        print(f"{'policy':<13}" + "".join(f"{k[:12]:>13}" for k in KEYS))
        for pol, m in means.items():
            print(f"{pol:<13}" + "".join(f"{m[k]:>13.3f}" for k in KEYS))
    OUT.write_text(json.dumps({"exploratory": True, "seeds": list(range(8)), "report": report}, indent=1))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
