"""AC2 engineering: vulnerable policy and locally produced repair catalysts.

Catalysts are finite model constituents, not biological molecules. The generic
interpreter, sensing and reaction rules remain protected. No boundary or converter
is implemented. Original policy is present only in the observer/protected arm.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import platform
import time

import numpy as np
from ac1 import contrast, decode

ARMS = ("self", "no_synthesis", "no_policy_write", "protected",
        "no_synthesis_rescue", "self_clamp", "no_synthesis_clamp")


@dataclass(frozen=True)
class Config:
    ticks: int = 4096
    flip_p: float = .0005
    life: int = 64
    slots: int = 4
    catalytic_capacity: int = 8
    write_cap: int = 32
    catalyst_material: int = 4
    catalyst_energy: int = 2
    food_gain: int = 32
    material_gain: int = 64
    energy_start: int = 64
    material_start: int = 128
    energy_cap: int = 128
    material_cap: int = 256

    def __post_init__(self):
        if self.life != 64 or self.slots != 4 or not 0 <= self.flip_p <= 1:
            raise ValueError("Invalid or unversioned model configuration")


@dataclass(slots=True)
class Body:
    traces: np.ndarray
    catalysts: np.ndarray
    energy: int
    material: int
    dead: bool = False

    def copy(self):
        return Body(self.traces.copy(), self.catalysts.copy(), self.energy, self.material, self.dead)

    def digest(self):
        return hashlib.sha256(self.traces.tobytes() + self.catalysts.tobytes()
            + int(self.energy).to_bytes(2, "little") + int(self.material).to_bytes(2, "little")
            + bytes([self.dead])).hexdigest()


def policy(traces):
    return (decode(traces[:2]).reshape(128, 3) * np.array([1, 2, 4], dtype=np.uint8)).sum(axis=1)


def demonstration(obs, priority):
    if obs & 1:
        return 0
    if obs & 2:
        return 1
    if obs & 64:
        return 6
    for bank in priority:
        if obs & (4 << bank):
            return 2 + bank
    return 7


def acquire(seed, c):
    rng = np.random.default_rng([seed, 502])
    priority = tuple(map(int, rng.permutation(4)))
    actions = np.array([demonstration(o, priority) for o in range(128)])
    targets = rng.integers(0, 2, (4, 192), dtype=np.uint8)
    traces = np.zeros((4, 192, 7), dtype=np.uint8)
    for obs in rng.permutation(128):
        for k in range(3):
            i = int(obs) * 3 + k
            targets[i // 192, i % 192] = (int(actions[obs]) >> k) & 1
            traces[i // 192, i % 192] = targets[i // 192, i % 192]
    traces[2:] = targets[2:, :, None]
    catalysts = np.tile(np.array([32, 48, 64, 0], dtype=np.uint8), (4, 1))
    return Body(traces, catalysts, c.energy_start, c.material_start), targets, actions, priority


def observe(body):
    ones = body.traces.sum(axis=-1)
    damage = np.minimum(ones, 7 - ones).sum(axis=1)
    obs = int(body.energy <= 48) + 2 * int(body.material <= 64)
    for bank in range(4):
        obs |= int(damage[bank] >= 4) << (bank + 2)
    obs |= int(np.min(np.count_nonzero(body.catalysts, axis=1)) < 2) << 6
    return obs


def event_zero():
    return dict(active=0, in_e=0, in_m=0, clamp_e=0, clamp_m=0, overflow_e=0,
        overflow_m=0, living_e=0, write_e=0, write_m=0, synthesis_e=0,
        synthesis_m=0, births=0, expired=0, external_births=0, writes=0,
        action=-1, obs=-1, bank=-1)


def prepare(body, c, flips, arm, event):
    body.traces ^= flips
    event["expired"] = int(np.count_nonzero(body.catalysts == 1))
    body.catalysts[body.catalysts > 0] -= 1
    if arm == "no_synthesis_rescue":
        for bank in range(4):
            while np.count_nonzero(body.catalysts[bank]) < 3:
                slot = int(np.flatnonzero(body.catalysts[bank] == 0)[0])
                body.catalysts[bank, slot] = c.life
                event["external_births"] += 1
    if arm in ("self_clamp", "no_synthesis_clamp"):
        event["clamp_e"] = c.energy_cap - body.energy
        event["clamp_m"] = c.material_cap - body.material
        body.energy, body.material = c.energy_cap, c.material_cap


def react(body, c, action, event, arm):
    """Generic reaction law; no target, teacher or acquisition seed."""
    body.energy -= 1
    event.update(active=1, living_e=1, action=int(action))
    if action == 0:
        event["in_e"] = c.food_gain
        event["overflow_e"] = max(0, body.energy + c.food_gain - c.energy_cap)
        body.energy = min(c.energy_cap, body.energy + c.food_gain)
    elif action == 1:
        event["in_m"] = c.material_gain
        event["overflow_m"] = max(0, body.material + c.material_gain - c.material_cap)
        body.material = min(c.material_cap, body.material + c.material_gain)
    elif 2 <= action <= 5:
        bank = int(action) - 2
        event["bank"] = bank
        capacity = int(np.count_nonzero(body.catalysts[bank])) * c.catalytic_capacity
        if arm == "no_policy_write" and bank < 2:
            capacity = 0
        majority = decode(body.traces[bank])
        sites = np.argwhere(body.traces[bank] != majority[:, None])
        n = min(capacity, len(sites), c.write_cap, body.energy, body.material)
        if n:
            sites = sites[:n]
            body.traces[bank, sites[:, 0], sites[:, 1]] = majority[sites[:, 0]]
        body.energy -= n
        body.material -= n
        event.update(writes=n, write_e=n, write_m=n)
    elif action == 6 and arm not in ("no_synthesis", "no_synthesis_rescue", "no_synthesis_clamp"):
        for bank in range(4):
            parents = np.count_nonzero(body.catalysts[bank])
            empty = np.flatnonzero(body.catalysts[bank] == 0)
            if parents and len(empty) and body.energy >= c.catalyst_energy and body.material >= c.catalyst_material:
                body.energy -= c.catalyst_energy
                body.material -= c.catalyst_material
                body.catalysts[bank, empty[0]] = c.life
                event["births"] += 1
                event["synthesis_e"] += c.catalyst_energy
                event["synthesis_m"] += c.catalyst_material
    body.dead = body.energy == 0


def step(body, c, flips, arm="self", protected_policy=None):
    if arm not in ARMS:
        raise ValueError(arm)
    if protected_policy is not None and arm != "protected":
        raise ValueError("Target-specific protected controller forbidden")
    event = event_zero()
    if body.dead:
        return event
    prepare(body, c, flips, arm, event)
    event["obs"] = observe(body)
    if arm == "protected":
        if protected_policy is None:
            raise ValueError("Explicit control template missing")
        action = int(protected_policy[event["obs"]])
    else:
        action = int(policy(body.traces)[event["obs"]])
    react(body, c, action, event, arm)
    return event


def world(seed, c):
    rng = np.random.default_rng([seed, 603])
    flips = (rng.random((c.ticks, 4, 192, 7), dtype=np.float32) < c.flip_p).astype(np.uint8)
    return flips, hashlib.sha256(flips.tobytes()).hexdigest()


def run_one(seed, c, arm, inputs=None):
    body, targets, target_policy, priority = acquire(seed, c)
    flips, env_digest = world(seed, c) if inputs is None else inputs
    total = {k: 0 for k in event_zero() if k not in ("action", "obs", "bank")}
    banks = [0] * 4
    correct = 0
    digest = hashlib.sha256()
    snapshots = []
    for t, f in enumerate(flips):
        before_e, before_m, before_w = body.energy, body.material, int(np.count_nonzero(body.catalysts))
        event = step(body, c, f, arm, target_policy if arm == "protected" else None)
        assert body.energy == before_e + event["in_e"] + event["clamp_e"] - event["overflow_e"] - event["living_e"] - event["write_e"] - event["synthesis_e"]
        assert body.material == before_m + event["in_m"] + event["clamp_m"] - event["overflow_m"] - event["write_m"] - event["synthesis_m"]
        assert np.count_nonzero(body.catalysts) == before_w + event["births"] + event["external_births"] - event["expired"]
        for key in total:
            total[key] += event[key]
        if event["active"]:
            correct += int(event["action"] == target_policy[event["obs"]])
        if event["bank"] >= 0:
            banks[event["bank"]] += event["writes"]
        digest.update(bytes([event["action"] + 1]))
        if t % 128 == 0 or t == c.ticks - 1:
            snapshots.append(dict(t=t, energy=body.energy, material=body.material,
                catalysts=list(map(int, np.count_nonzero(body.catalysts, axis=1))),
                policy_accuracy=float(np.mean(policy(body.traces) == target_policy)),
                payload_accuracy=float(np.mean(decode(body.traces[2:]) == targets[2:])), dead=body.dead,
                state_digest=body.digest()))
    pa = float(np.mean(policy(body.traces) == target_policy))
    da = float(np.mean(decode(body.traces[2:]) == targets[2:]))
    return dict(seed=seed, arm=arm, config=asdict(c), priority=list(priority),
        active_fraction=total["active"] / c.ticks, completed=not body.dead,
        policy_accuracy=pa, payload_accuracy=da, functional_policy=pa * int(not body.dead),
        functional_payload=da * int(not body.dead), correct_decisions_per_planned=correct / c.ticks,
        final_energy=body.energy, final_material=body.material,
        final_catalysts=int(np.count_nonzero(body.catalysts)), bank_writes=banks,
        ledger=total, snapshots=snapshots, env_digest=env_digest,
        action_digest=digest.hexdigest(), state_digest=body.digest())


def study(out):
    out.mkdir(exist_ok=False)
    paths = ("ac2.py", "test_ac2.py", "ac1.py", "AC2_PROTOCOL_v1.md")
    result = dict(kind="engineering_only", seeds=list(range(16)), configs=[],
        python=platform.python_version(), numpy=np.__version__,
        source_hashes={p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths})
    (out / "pre_run_snapshot.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    started = time.monotonic()
    for p in (.00025, .0005, .001):
        c = Config(flip_p=p)
        rows = []
        for seed in result["seeds"]:
            inputs = world(seed, c)
            rows.extend(run_one(seed, c, arm, inputs) for arm in ARMS)
        means = {arm: {key: float(np.mean([r[key] for r in rows if r["arm"] == arm]))
                       for key in ("active_fraction", "completed", "policy_accuracy", "payload_accuracy",
                                   "functional_policy", "functional_payload", "correct_decisions_per_planned",
                                   "final_catalysts")}
                 for arm in ARMS}
        pairs = (("self", "no_synthesis", "active_fraction"),
                 ("self", "no_policy_write", "active_fraction"),
                 ("no_synthesis_rescue", "no_synthesis", "active_fraction"),
                 ("self_clamp", "no_synthesis_clamp", "policy_accuracy"))
        contrasts = {a + "-" + b: contrast([r[k] for r in rows if r["arm"] == a],
                                           [r[k] for r in rows if r["arm"] == b]) for a, b, k in pairs}
        criteria = dict(self_viable=means["self"]["active_fraction"] >= .9,
            protected_viable=means["protected"]["active_fraction"] >= .9,
            catalyst_rescue=means["no_synthesis_rescue"]["active_fraction"] >= .9,
            synthesis_dependence=contrasts["self-no_synthesis"]["mean"] >= .2,
            clamped_information_dependence=contrasts["self_clamp-no_synthesis_clamp"]["mean"] >= .2,
            turnover=all(r["ledger"]["births"] > 120 and all(n > 0 for n in r["bank_writes"])
                         for r in rows if r["arm"] == "self"))
        result["configs"].append(dict(config=asdict(c), means=means, contrasts=contrasts,
                                      engineering_criteria=criteria, rows=rows))
        print(json.dumps(dict(p=p, activity={a: round(means[a]["active_fraction"], 3) for a in ARMS}, criteria=criteria)), flush=True)
        (out / "results.json").write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    result["wall_seconds"] = time.monotonic() - started
    (out / "results.json").write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    study(parser.parse_args().out)
