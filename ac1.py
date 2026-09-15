"""AC1 engineering model: a vulnerable demonstrated table repairs its own bits.

Only Body.traces, energy, material and dead persist in the live agent. Targets,
teacher and observer are deliberately outside step(). Generic decoding/sensing,
actuation and the simulator remain protected: this is not full autopoiesis.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import itertools
import json
from pathlib import Path
import platform
import time

import numpy as np


ARMS = ("self", "no_policy_write", "no_write", "protected", "fixed", "random",
        "policy_scramble", "resource_rescue")


@dataclass(frozen=True)
class Config:
    ticks: int = 3000
    replicas: int = 7
    bits_per_bank: int = 96
    flip_p: float = 0.001
    pulse: bool = False
    pulse_tick: int = 200
    energy_start: int = 64
    material_start: int = 128
    energy_cap: int = 128
    material_cap: int = 256
    food_gain: int = 32
    precursor_gain: int = 64
    low_energy: int = 48
    low_material: int = 64
    damage_threshold: int = 4
    write_cap: int = 32

    def __post_init__(self):
        if self.replicas != 7 or self.bits_per_bank != 96:
            raise ValueError("This version fixes the representation to 4x96x7")
        if not 0 <= self.flip_p <= 1 or self.ticks < 1:
            raise ValueError("invalid dynamics")


@dataclass(slots=True)
class Body:
    traces: np.ndarray
    energy: int
    material: int
    dead: bool = False

    def copy(self):
        return Body(self.traces.copy(), self.energy, self.material, self.dead)

    def digest(self):
        raw = self.traces.tobytes() + bytes([self.energy & 255])
        raw += self.material.to_bytes(2, "little") + bytes([self.dead])
        return hashlib.sha256(raw).hexdigest()


def decode(traces):
    return (traces.sum(axis=-1) > 3).astype(np.uint8)


def decode_actions(traces):
    bits = decode(traces[:2]).reshape(64, 3)
    return (bits * np.array([1, 2, 4], dtype=np.uint8)).sum(axis=1)


def teacher_action(obs: int, priority=(0, 1, 2, 3)) -> int:
    if obs & 1:
        return 0
    if obs & 2:
        return 1
    for bank in priority:
        if obs & (1 << (2 + bank)):
            return 2 + bank
    return 7


def acquire(seed: int, c: Config):
    """Tabular supervised acquisition; teacher/targets returned to observer only.

Each of 64 contexts is demonstrated exactly once, in random order. Not RL,
not spontaneous needs. Priority is a permutation (only log2(24) history bits).
"""
    rng = np.random.default_rng([seed, 101])
    priority = tuple(map(int, rng.permutation(4)))
    targets = rng.integers(0, 2, (4, 96), dtype=np.uint8)
    target_policy = np.array([teacher_action(o, priority) for o in range(64)])
    traces = np.zeros((4, 96, 7), dtype=np.uint8)
    for obs in rng.permutation(64):
        action = int(target_policy[obs])
        for k in range(3):
            index = int(obs) * 3 + k
            targets[index // 96, index % 96] = (action >> k) & 1
            traces[index // 96, index % 96, :] = (action >> k) & 1
    traces[2:] = targets[2:, :, None]
    return Body(traces, c.energy_start, c.material_start), targets, target_policy, priority


def observe(body: Body, c: Config):
    ones = body.traces.sum(axis=-1)
    depth = np.minimum(ones, c.replicas - ones).sum(axis=1)
    obs = int(body.energy <= c.low_energy) + 2 * int(body.material <= c.low_material)
    for bank in range(4):
        obs |= int(depth[bank] >= c.damage_threshold) << (bank + 2)
    return obs


def step(body: Body, c: Config, flips: np.ndarray, *, arm="self",
         protected_action: int | None = None, random_action: int = 7):
    """No truth, seed, teacher, policy cache or observer available to this function.

protected_action is admitted ONLY for explicit protected/fixed controls. Atomic
copy operations pay per actual attempted bit, including sham writes. Host-only
observer records are returned, never consumed on a future tick.
"""
    if arm not in ARMS:
        raise ValueError(arm)
    if protected_action is not None and arm not in ("protected", "fixed"):
        raise ValueError("protected action forbidden for this arm")
    if body.dead:
        return {"active": 0, "action": -1, "spent_e": 0, "spent_m": 0,
                "in_e": 0, "in_m": 0, "overflow_e": 0, "overflow_m": 0,
                "attempts": 0, "writes": 0, "bank": -1, "rescue_e": 0, "rescue_m": 0}
    body.traces ^= flips
    rescue_e = rescue_m = 0
    if arm == "resource_rescue":
        rescue_e, rescue_m = c.energy_cap - body.energy, c.material_cap - body.material
        body.energy, body.material = c.energy_cap, c.material_cap
    obs = observe(body, c)
    if arm in ("protected", "fixed"):
        if protected_action is None:
            raise ValueError("explicit control action required")
        action = int(protected_action)
    elif arm == "random":
        action = int(random_action)
    else:
        action = int(decode_actions(body.traces)[obs])
    event = dict(active=1, action=action, observation=obs, spent_e=1, spent_m=0,
                 in_e=0, in_m=0, overflow_e=0, overflow_m=0, attempts=0, writes=0,
                 bank=-1, rescue_e=rescue_e, rescue_m=rescue_m)
    if body.energy <= 0:
        raise AssertionError("live body has no energy")
    body.energy -= 1
    if action == 0:
        event["in_e"] = c.food_gain
        event["overflow_e"] = max(0, body.energy + c.food_gain - c.energy_cap)
        body.energy = min(c.energy_cap, body.energy + c.food_gain)
    elif action == 1:
        event["in_m"] = c.precursor_gain
        event["overflow_m"] = max(0, body.material + c.precursor_gain - c.material_cap)
        body.material = min(c.material_cap, body.material + c.precursor_gain)
    elif 2 <= action <= 5:
        bank = action - 2
        majority = decode(body.traces[bank])
        locations = np.argwhere(body.traces[bank] != majority[:, None])
        count = min(len(locations), c.write_cap, body.energy, body.material)
        event.update(bank=bank, attempts=count, spent_m=count, spent_e=1 + count)
        body.energy -= count
        body.material -= count
        sham = arm == "no_write" or (arm == "no_policy_write" and bank < 2)
        if not sham and count:
            chosen = locations[:count]
            body.traces[bank, chosen[:, 0], chosen[:, 1]] = majority[chosen[:, 0]]
            event["writes"] = count
    body.dead = body.energy == 0
    return event


def world(seed: int, c: Config):
    rng = np.random.default_rng([seed, 202])
    flips = (rng.random((c.ticks, 4, 96, 7)) < c.flip_p).astype(np.uint8)
    # Exactly two distinct pulse sites per code bit; background noise retained.
    if c.pulse and c.pulse_tick < c.ticks:
        order = np.argsort(rng.random((4, 96, 7)), axis=-1)[..., :2]
        pulse = np.zeros((4, 96, 7), dtype=np.uint8)
        np.put_along_axis(pulse, order, 1, axis=-1)
        flips[c.pulse_tick] ^= pulse
    actions = np.random.default_rng([seed, 303]).integers(0, 8, c.ticks)
    return flips, actions, hashlib.sha256(flips.tobytes() + actions.tobytes()).hexdigest()


def run_one(seed: int, c: Config, arm: str, inputs=None):
    body, targets, target_policy, priority = acquire(seed, c)
    if arm == "policy_scramble":
        body.traces[:2] = np.random.default_rng([seed, 404]).integers(
            0, 2, body.traces[:2].shape, dtype=np.uint8)
    flips, random_actions, env_digest = world(seed, c) if inputs is None else inputs
    totals = dict(active=0, spent_e=0, spent_m=0, in_e=0, in_m=0,
                  overflow_e=0, overflow_m=0, attempts=0, writes=0, rescue_e=0, rescue_m=0)
    writes = [0] * 4
    correct_actions = 0
    action_digest = hashlib.sha256()
    snapshots = []
    for t in range(c.ticks):
        override = None
        if not body.dead and arm in ("protected", "fixed"):
            # Controls see the same post-corruption observation as the live agent.
            probe = body.copy()
            probe.traces ^= flips[t]
            obs = observe(probe, c)
            override = int(target_policy[obs]) if arm == "protected" else teacher_action(obs)
        before_e, before_m = body.energy, body.material
        event = step(body, c, flips[t], arm=arm, protected_action=override,
                     random_action=int(random_actions[t]))
        assert body.energy == before_e + event["in_e"] + event["rescue_e"] - event["spent_e"] - event["overflow_e"]
        assert body.material == before_m + event["in_m"] + event["rescue_m"] - event["spent_m"] - event["overflow_m"]
        for key in totals:
            totals[key] += event[key]
        if event["active"]:
            correct_actions += int(event["action"] == target_policy[event["observation"]])
        if event["bank"] >= 0:
            writes[event["bank"]] += event["writes"]
        action_digest.update(bytes([event["action"] + 1]))
        if t % 100 == 0 or t == c.ticks - 1:
            snapshots.append(dict(tick=t, energy=body.energy, material=body.material,
                dead=body.dead, policy_accuracy=float(np.mean(decode_actions(body.traces) == target_policy)),
                payload_accuracy=float(np.mean(decode(body.traces[2:]) == targets[2:])),
                state_digest=body.digest()))
    policy_accuracy = float(np.mean(decode_actions(body.traces) == target_policy))
    payload_accuracy = float(np.mean(decode(body.traces[2:]) == targets[2:]))
    return dict(seed=seed, arm=arm, config=asdict(c), env_digest=env_digest,
        priority=list(priority), active_fraction=totals["active"] / c.ticks,
        completed=not body.dead, final_energy=body.energy, final_material=body.material,
        policy_accuracy=policy_accuracy, payload_accuracy=payload_accuracy,
        functional_policy_accuracy=policy_accuracy * int(not body.dead),
        functional_payload_accuracy=payload_accuracy * int(not body.dead),
        correct_decisions_per_planned_tick=correct_actions / c.ticks,
        bank_writes=writes, ledger=totals, snapshots=snapshots,
        action_digest=action_digest.hexdigest(), final_state_digest=body.digest())


def contrast(a, b):
    x = np.asarray(a) - np.asarray(b)
    rng = np.random.default_rng(20260914)
    samples = x[rng.integers(0, len(x), (10000, len(x)))].mean(axis=1)
    return dict(mean=float(x.mean()), interval=list(map(float, np.quantile(samples, [.025, .975]))),
                per_seed=list(map(float, x)), n=len(x), positive=int((x > 0).sum()))


def study(out: Path):
    out.mkdir(exist_ok=False)
    started = time.monotonic()
    result = dict(kind="engineering_only", seeds=list(range(8)), configs=[],
                  python=platform.python_version(), numpy=np.__version__,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  protocol_sha256=hashlib.sha256(Path("AC1_RESEARCH_AND_PROTOCOL_v1.md").read_bytes()).hexdigest())
    for p, pulse in itertools.product((.0005, .001, .002), (False, True)):
        c = Config(flip_p=p, pulse=pulse)
        rows = []
        for seed in result["seeds"]:
            inputs = world(seed, c)
            for arm in ARMS:
                rows.append(run_one(seed, c, arm, inputs))
        means = {arm: {metric: float(np.mean([r[metric] for r in rows if r["arm"] == arm]))
                          for metric in ("active_fraction", "completed", "policy_accuracy", "payload_accuracy",
                                         "functional_policy_accuracy", "functional_payload_accuracy",
                                         "correct_decisions_per_planned_tick")}
                 for arm in ARMS}
        differences = {other: contrast([r["active_fraction"] for r in rows if r["arm"] == "self"],
                                       [r["active_fraction"] for r in rows if r["arm"] == other])
                       for other in ("no_policy_write", "no_write", "protected", "fixed", "resource_rescue")}
        support = (means["self"]["active_fraction"] >= .9 and
                   differences["no_policy_write"]["mean"] >= .2 and
                   means["protected"]["active_fraction"] >= .9 and
                   all(all(v > 0 for v in r["bank_writes"]) for r in rows if r["arm"] == "self"))
        entry = dict(config=asdict(c), means=means, paired_activity=differences,
                     behavioral_engineering_criteria=support, rows=rows)
        result["configs"].append(entry)
        print(json.dumps(dict(p=p, pulse=pulse, activity={a: round(means[a]["active_fraction"], 3) for a in ARMS},
                              engineering_criteria=support)), flush=True)
        (out / "results.json").write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    result["wall_seconds"] = time.monotonic() - started
    (out / "results.json").write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    study(args.out)
