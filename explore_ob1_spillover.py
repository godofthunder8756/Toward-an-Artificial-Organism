"""EXPLORATORY post hoc check on E3-OB1: how many repairs reached deprioritized cues?

OB1 used soft deprioritization: deprioritized cues were still repaired when
budget remained. This counts those repairs, split by whether the cue was
obsolete, on OB1 final seeds 300-307 for both configurations. It first checks
that each run reproduces the frozen OB1 row (recall and obsolete-repair share)
exactly. It does not modify OB1 or its outcome.
"""

from __future__ import annotations

import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

import e3_obsolescence_world as ob

OUT = Path("e3_fep_seed_results/ob1/exploratory_spillover.json")
POLICIES = ("depth_flag", "depth_timeout_400", "depth_timeout_2000", "depth_learned")
SEEDS = tuple(range(300, 308))


def _count(args):
    cfg, policy_name, seed = args
    w = ob.WorldParams(**cfg)
    env = ob.generate_environment(seed, w)
    base = ob.POLICY_CLASSES[policy_name]
    counts = {"repairs": 0, "to_deprioritized": 0, "to_deprioritized_obsolete": 0, "to_deprioritized_live": 0}

    class Counting(base):
        def choose(self, obs):
            chosen = super().choose(obs)
            dep = self.deprioritized()
            obsolete = env.state[obs.t] == ob.OBSOLETE  # evaluator-side only, after the decision
            for cue in chosen:
                counts["repairs"] += 1
                if dep[cue]:
                    counts["to_deprioritized"] += 1
                    counts["to_deprioritized_obsolete" if obsolete[cue] else "to_deprioritized_live"] += 1
            return chosen

    ob.POLICY_CLASSES["_counting"] = Counting
    try:
        row = ob.run_one("_counting", seed, w, env=env)
    finally:
        del ob.POLICY_CLASSES["_counting"]
    return cfg, policy_name, seed, counts, row["overall_accuracy"], row["obsolete_repair_share"]


def main():
    final = json.loads(Path("e3_fep_seed_results/ob1/final_results.json").read_text())
    reference = {(c["params"]["budget"], r["policy"], r["seed"]): r for c in final["configs"] for r in c["rows"]}
    jobs = [(c["params"], p, s) for c in final["configs"] for p in POLICIES for s in SEEDS]
    with ProcessPoolExecutor(max_workers=7) as pool:
        results = list(pool.map(_count, jobs))
    report, reproduced = {}, True
    for cfg, p, s, counts, acc, share in results:
        ref = reference[(cfg["budget"], p, s)]
        reproduced &= ref["overall_accuracy"] == acc and ref["obsolete_repair_share"] == share
        agg = report.setdefault(f"budget{cfg['budget']}_p{cfg['corrupt_p']}:{p}", dict.fromkeys(counts, 0))
        for k, v in counts.items():
            agg[k] += v
    print(f"reproduces frozen OB1 rows exactly: {reproduced}")
    for key, agg in report.items():
        r = agg["repairs"]
        print(f"  {key:<38} repairs to deprioritized {agg['to_deprioritized'] / r:.3f} "
              f"(obsolete {agg['to_deprioritized_obsolete'] / r:.3f}, live {agg['to_deprioritized_live'] / r:.3f})")
    OUT.write_text(json.dumps({"exploratory": True, "seeds": SEEDS, "reproduced": bool(reproduced), "counts": report}, indent=1))


if __name__ == "__main__":
    main()
