"""Post-v1 favorable-ablation diagnostic using the unchanged AC1 model."""
import argparse
from dataclasses import asdict
import hashlib
import itertools
import json
from pathlib import Path
import time

import numpy as np
import ac1


def free_ablation_step(body, c, flips):
    event = ac1.step(body, c, flips, arm="no_policy_write")
    refund = event["attempts"] if 0 <= event["bank"] < 2 else 0
    body.energy += refund
    body.material += refund
    event["spent_e"] -= refund
    event["spent_m"] -= refund
    event["refunded_e"] = event["refunded_m"] = refund
    # Equivalent to immediate cost cancellation before the termination decision.
    body.dead = body.energy == 0
    return event


def run_free(seed, c, inputs):
    body, targets, policy, priority = ac1.acquire(seed, c)
    flips, _, digest = inputs
    totals = dict(active=0, spent_e=0, spent_m=0, in_e=0, in_m=0,
                  overflow_e=0, overflow_m=0, attempts=0, writes=0, rescue_e=0,
                  rescue_m=0, refunded_e=0, refunded_m=0)
    writes = [0] * 4
    correct = 0
    decisions = hashlib.sha256()
    for f in flips:
        before_e, before_m = body.energy, body.material
        event = free_ablation_step(body, c, f)
        assert body.energy == before_e + event["in_e"] - event["spent_e"] - event["overflow_e"]
        assert body.material == before_m + event["in_m"] - event["spent_m"] - event["overflow_m"]
        for key in totals:
            totals[key] += event[key]
        if event["active"]:
            correct += int(event["action"] == policy[event["observation"]])
        if event["bank"] >= 0:
            writes[event["bank"]] += event["writes"]
        decisions.update(bytes([event["action"] + 1]))
    pa = float(np.mean(ac1.decode_actions(body.traces) == policy))
    da = float(np.mean(ac1.decode(body.traces[2:]) == targets[2:]))
    return dict(seed=seed, arm="free_policy_ablation", config=asdict(c), env_digest=digest,
                priority=list(priority), active_fraction=totals["active"] / c.ticks,
                completed=not body.dead, final_energy=body.energy, final_material=body.material,
                policy_accuracy=pa, payload_accuracy=da,
                functional_policy_accuracy=pa * int(not body.dead),
                functional_payload_accuracy=da * int(not body.dead),
                correct_decisions_per_planned_tick=correct / c.ticks,
                bank_writes=writes, ledger=totals, action_digest=decisions.hexdigest(),
                final_state_digest=body.digest())


def checks():
    c = ac1.Config()
    a, _, _, _ = ac1.acquire(1, c)
    a.traces[0, :8, 0] ^= 1
    b = a.copy()
    ea = ac1.step(a, c, np.zeros_like(a.traces), arm="no_policy_write")
    eb = free_ablation_step(b, c, np.zeros_like(b.traces))
    assert ea["bank"] == 0 and ea["writes"] == 0
    assert eb["spent_e"] == 1 and eb["spent_m"] == 0
    assert b.energy - a.energy == ea["attempts"]
    assert b.material - a.material == ea["attempts"]
    np.testing.assert_array_equal(a.traces, b.traces)
    c = ac1.Config(ticks=50)
    run_free(1, c, ac1.world(1, c))
    return {"refund_equivalence": True, "short_ledger_check": True}


def study(out):
    verification = checks()
    out.mkdir(exist_ok=False)
    result = dict(kind="exploratory_validation", checks=verification, seeds=list(range(1000, 1032)), configs=[])
    result["source_hashes"] = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
        for p in ("ac1.py", "ac1_followup.py", "AC1_FOLLOWUP_PROTOCOL_v1.md")}
    (out / "pre_run_snapshot.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    started = time.monotonic()
    arms = ("self", "no_policy_write", "free_policy_ablation", "protected")
    for p, pulse in itertools.product((.0005, .001, .002), (False, True)):
        c = ac1.Config(flip_p=p, pulse=pulse)
        rows = []
        for seed in result["seeds"]:
            inputs = ac1.world(seed, c)
            for arm in arms:
                rows.append(run_free(seed, c, inputs) if arm == "free_policy_ablation"
                            else ac1.run_one(seed, c, arm, inputs))
        means = {a: {k: float(np.mean([r[k] for r in rows if r["arm"] == a]))
                     for k in ("active_fraction", "completed", "policy_accuracy", "payload_accuracy",
                               "functional_policy_accuracy", "functional_payload_accuracy",
                               "correct_decisions_per_planned_tick")}
                 for a in arms}
        contrasts = {a: ac1.contrast([r["active_fraction"] for r in rows if r["arm"] == "self"],
                                    [r["active_fraction"] for r in rows if r["arm"] == a])
                     for a in arms if a != "self"}
        result["configs"].append(dict(config=asdict(c), means=means, paired_activity=contrasts, rows=rows))
        (out / "results.json").write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
        print(json.dumps(dict(p=p, pulse=pulse, activity={a: round(means[a]["active_fraction"], 4) for a in arms})), flush=True)
    result["wall_seconds"] = time.monotonic() - started
    (out / "results.json").write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    study(args.out)
