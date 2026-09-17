"""Sampled exact reruns of the AC1-4 confirmatory study.

Replays the first seed of each study across every arm and rate through the
frozen runners, and asserts field-for-field equality with the saved rows
(JSON round-trip normalised). Writes a report; never touches the data.
"""
import json
from pathlib import Path

import ac1
import ac1_followup
import ac2
import ac3
import ac4
import ac1_4_confirm as conf

ROOT = Path("ac1_4_confirm_results_v1")


def replay_ac1(seed, cfg):
    c = ac1.Config(**cfg["config"])
    inputs = ac1.world(seed, c)
    out = []
    for arm in ("self", "no_policy_write", "free_policy_ablation", "protected"):
        row = ac1_followup.run_free(seed, c, inputs) if arm == "free_policy_ablation" \
            else ac1.run_one(seed, c, arm, inputs)
        out.append(row)
    return out


def replay_ac2(seed, cfg):
    c = ac2.Config(**cfg["config"])
    inputs = ac2.world(seed, c)
    return [ac2.run_one(seed, c, arm, inputs) for arm in
            ("self", "no_synthesis", "no_synthesis_rescue", "protected",
             "self_clamp", "no_synthesis_clamp")]


def replay_ac3(seed, cfg):
    c = ac3.Config(**cfg["config"])
    inputs = ac3.world(seed, c)
    return [ac3.run_one(seed, c, arm, inputs) for arm in
            ("self", "no_C", "no_C_rescue", "no_C_energy", "protected",
             "self_energy", "no_W_energy")]


def replay_ac4_short(seed, cfg):
    return [ac4.run(seed, cfg["config"]["p"], arm, 2048) for arm in
            ("self", "no_B", "no_B_rescue", "no_B_retention", "protected")]


def replay_ac4_long(seed, cfg):
    return [ac4.run(seed, cfg["config"]["p"], arm, 8192) for arm in
            ("self", "no_policy_write", "protected", "no_B_retention")]


REPLAYERS = {
    "ac1": replay_ac1, "ac2": replay_ac2, "ac3": replay_ac3,
    "ac4_short": replay_ac4_short, "ac4_long": replay_ac4_long,
}


def norm(row):
    return json.loads(json.dumps(row))


def main():
    results = json.loads((ROOT / "results.json").read_text())
    replays = []
    for name, configs in results["studies"].items():
        replay_fn = REPLAYERS[name]
        seed = conf.SEEDS[name][0]
        for cfg in configs:
            fresh = replay_fn(seed, cfg)
            for row in fresh:
                saved = next(r for r in cfg["rows"] if r["seed"] == seed and r["arm"] == row["arm"])
                assert norm(row) == norm(saved), (name, seed, row["arm"])
                replays.append(dict(study=name, seed=seed, arm=row["arm"], exact=True))
    report = dict(ok=True, replays=len(replays), rows=replays,
                  limits="Sampled exact reruns (first seed per study, all arms and rates).")
    with (ROOT / "replay.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    print(json.dumps(dict(ok=True, replays=len(replays))))


if __name__ == "__main__":
    main()
