"""Post-run exploratory failure chronology; observer-only, no interventions."""
import json
from pathlib import Path
import numpy as np
import ac2


def main():
    saved = json.loads(Path("ac2_results_v1/results.json").read_text())["configs"][-1]
    c = ac2.Config(**saved["config"])
    rows = []
    for seed in range(16):
        body, targets, target_policy, _ = ac2.acquire(seed, c)
        flips, _ = ac2.world(seed, c)
        first_error = first_wrong_action = first_empty_bank = death = None
        min_energy = body.energy
        for t, f in enumerate(flips):
            event = ac2.step(body, c, f)
            accuracy = float(np.mean(ac2.policy(body.traces) == target_policy))
            if first_error is None and accuracy < 1:
                first_error = t
            if first_wrong_action is None and event["active"] and event["action"] != target_policy[event["obs"]]:
                first_wrong_action = t
            if first_empty_bank is None and (np.count_nonzero(body.catalysts, axis=1) == 0).any():
                first_empty_bank = t
            min_energy = min(min_energy, body.energy)
            if body.dead and death is None:
                death = t
        original = next(r for r in saved["rows"] if r["seed"] == seed and r["arm"] == "self")
        assert original["state_digest"] == body.digest()
        rows.append(dict(seed=seed, first_policy_error=first_error, first_wrong_action=first_wrong_action,
                         first_empty_catalyst_bank=first_empty_bank, death_tick=death,
                         final_policy_accuracy=accuracy, minimum_energy=min_energy,
                         final_catalysts=list(map(int, np.count_nonzero(body.catalysts, axis=1)))))
    report = dict(kind="post_hoc_exploratory_observer_chronology", config=saved["config"], rows=rows,
        limits="Chronology is not a causal mediation experiment. Post-step policy scoring can follow the action that was computed before writes.")
    with Path("AC2_FAILURE_CHRONOLOGY_v1.json").open("x", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(rows))


if __name__ == "__main__":
    main()
