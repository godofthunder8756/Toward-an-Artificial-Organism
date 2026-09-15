"""AC3 engineering: produced converters turn fuel into usable energy.

Uses unchanged AC2 generic W/write reactions. No direct food-to-energy action;
no produced boundary or autonomous learning of the demonstrated policy yet.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import hashlib
import json
import platform
import time

import numpy as np
import ac2
from ac1 import decode, contrast

ARMS = ("self", "no_C", "no_C_rescue", "no_C_energy", "no_W",
        "self_energy", "no_W_energy", "no_policy_write", "protected")


@dataclass(frozen=True)
class Config:
    ticks: int = 4096
    flip_p: float = .0002
    life: int = 64
    slots: int = 4
    catalytic_capacity: int = 8
    write_cap: int = 32
    catalyst_material: int = 4
    catalyst_energy: int = 2
    converter_life: int = 128
    converter_material: int = 4
    converter_energy: int = 4
    fuel_yield: int = 8
    fuel_gain: int = 32
    fuel_cap: int = 64
    fuel_start: int = 32
    material_gain: int = 64
    energy_start: int = 64
    material_start: int = 128
    energy_cap: int = 128
    material_cap: int = 256

    def __post_init__(self):
        if self.life != 64 or self.slots != 4 or self.converter_life != 128 or not 0 <= self.flip_p <= 1:
            raise ValueError("Invalid or unversioned configuration")


@dataclass(slots=True)
class Body:
    traces: np.ndarray
    catalysts: np.ndarray
    converters: np.ndarray
    fuel: int
    energy: int
    material: int
    dead: bool = False

    def copy(self):
        return Body(self.traces.copy(), self.catalysts.copy(), self.converters.copy(),
                    self.fuel, self.energy, self.material, self.dead)

    def digest(self):
        raw = self.traces.tobytes() + self.catalysts.tobytes() + self.converters.tobytes()
        raw += b"".join(int(v).to_bytes(2, "little") for v in (self.fuel, self.energy, self.material))
        return hashlib.sha256(raw + bytes([self.dead])).hexdigest()


def policy(traces):
    return (decode(traces[:2]).reshape(256, 4) * np.array([1, 2, 4, 8], dtype=np.uint8)).sum(axis=1)


def demonstration(obs, priority):
    if obs & 1:
        return 0
    if obs & 2:
        return 1
    if obs & 64:
        return 6
    if obs & 128:
        return 7
    for bank in priority:
        if obs & (4 << bank):
            return 2 + bank
    return 8


def acquire(seed, c):
    rng = np.random.default_rng([seed, 702])
    priority = tuple(map(int, rng.permutation(4)))
    target_policy = np.array([demonstration(o, priority) for o in range(256)])
    targets = rng.integers(0, 2, (4, 512), dtype=np.uint8)
    traces = np.zeros((4, 512, 7), dtype=np.uint8)
    for obs in rng.permutation(256):
        for k in range(4):
            i = int(obs) * 4 + k
            targets[i // 512, i % 512] = (int(target_policy[obs]) >> k) & 1
            traces[i // 512, i % 512] = targets[i // 512, i % 512]
    traces[2:] = targets[2:, :, None]
    w = np.tile(np.array([32, 48, 64, 0], dtype=np.uint8), (4, 1))
    converters = np.array([64, 96, 128, 0], dtype=np.uint8)
    return Body(traces, w, converters, c.fuel_start, c.energy_start, c.material_start), targets, target_policy, priority


def observe(body):
    ones = body.traces.sum(axis=-1)
    damage = np.minimum(ones, 7 - ones).sum(axis=1)
    obs = int(body.fuel <= 8) + 2 * int(body.material <= 64)
    for bank in range(4):
        obs |= int(damage[bank] >= 4) << (bank + 2)
    obs |= int(np.min(np.count_nonzero(body.catalysts, axis=1)) < 2) << 6
    obs |= int(np.count_nonzero(body.converters) < 2) << 7
    return obs


def event_zero():
    e = ac2.event_zero()
    e.update(in_f=0, overflow_f=0, converted=0, C_births=0, C_expired=0,
             external_C=0, C_synthesis_e=0, C_synthesis_m=0)
    return e


def convert(body, c, event):
    units = min(int(np.count_nonzero(body.converters)), body.fuel,
                (c.energy_cap - body.energy) // c.fuel_yield)
    body.fuel -= units
    body.energy += c.fuel_yield * units
    event["converted"] += units


def prepare(body, c, flips, arm, event):
    body.traces ^= flips
    event["expired"] = int(np.count_nonzero(body.catalysts == 1))
    body.catalysts[body.catalysts > 0] -= 1
    event["C_expired"] = int(np.count_nonzero(body.converters == 1))
    body.converters[body.converters > 0] -= 1
    if arm == "no_C_rescue":
        while np.count_nonzero(body.converters) < 3:
            body.converters[np.flatnonzero(body.converters == 0)[0]] = c.converter_life
            event["external_C"] += 1
    if arm in ("no_C_energy", "self_energy", "no_W_energy"):
        event["clamp_e"] = c.energy_cap - body.energy
        body.energy = c.energy_cap
    convert(body, c, event)


def react(body, c, action, event, arm):
    if 1 <= action <= 6:
        translated = "no_synthesis" if arm in ("no_W", "no_W_energy") else arm
        ac2.react(body, c, action, event, translated)
        # AC3 has autonomous conversion before the next decision. E=0 at the end
        # of an action is not terminal if fuel/C can restart activity next tick.
        body.dead = False
        return
    body.energy -= 1
    event.update(active=1, living_e=1, action=int(action))
    if action == 0:
        event["in_f"] = c.fuel_gain
        event["overflow_f"] = max(0, body.fuel + c.fuel_gain - c.fuel_cap)
        body.fuel = min(c.fuel_cap, body.fuel + c.fuel_gain)
    elif action == 7 and arm not in ("no_C", "no_C_rescue", "no_C_energy"):
        empty = np.flatnonzero(body.converters == 0)
        if np.count_nonzero(body.catalysts[0]) and len(empty) and body.material >= c.converter_material and body.energy >= c.converter_energy:
            body.material -= c.converter_material
            body.energy -= c.converter_energy
            body.converters[empty[0]] = c.converter_life
            event.update(C_births=1, C_synthesis_m=c.converter_material, C_synthesis_e=c.converter_energy)


def step(body, c, flips, arm="self", protected_policy=None):
    if arm not in ARMS:
        raise ValueError(arm)
    if protected_policy is not None and arm != "protected":
        raise ValueError("Protected learned template forbidden")
    e = event_zero()
    if body.dead:
        return e
    prepare(body, c, flips, arm, e)
    if body.energy < 1:
        body.dead = True
        return e
    e["obs"] = observe(body)
    if arm == "protected":
        if protected_policy is None:
            raise ValueError("Missing explicit control")
        action = int(protected_policy[e["obs"]])
    else:
        action = int(policy(body.traces)[e["obs"]])
    react(body, c, action, e, arm)
    return e


def world(seed, c):
    rng = np.random.default_rng([seed, 803])
    flips = (rng.random((c.ticks, 4, 512, 7), dtype=np.float32) < c.flip_p).astype(np.uint8)
    return flips, hashlib.sha256(flips.tobytes()).hexdigest()


def check_balance(c, before, body, e):
    E, M, F, W, C = before
    assert body.energy == E + e["in_e"] + e["clamp_e"] + c.fuel_yield * e["converted"] - e["overflow_e"] - e["living_e"] - e["write_e"] - e["synthesis_e"] - e["C_synthesis_e"]
    assert body.material == M + e["in_m"] + e["clamp_m"] - e["overflow_m"] - e["write_m"] - e["synthesis_m"] - e["C_synthesis_m"]
    assert body.fuel == F + e["in_f"] - e["converted"] - e["overflow_f"]
    assert np.count_nonzero(body.catalysts) == W + e["births"] + e["external_births"] - e["expired"]
    assert np.count_nonzero(body.converters) == C + e["C_births"] + e["external_C"] - e["C_expired"]


def run_one(seed, c, arm, inputs=None):
    body, targets, target_policy, priority = acquire(seed, c)
    flips, env_digest = world(seed, c) if inputs is None else inputs
    total = {k: 0 for k in event_zero() if k not in ("action", "obs", "bank")}
    banks, correct, snapshots = [0] * 4, 0, []
    digest = hashlib.sha256()
    for t, f in enumerate(flips):
        before = body.energy, body.material, body.fuel, int(np.count_nonzero(body.catalysts)), int(np.count_nonzero(body.converters))
        e = step(body, c, f, arm, target_policy if arm == "protected" else None)
        check_balance(c, before, body, e)
        for key in total:
            total[key] += e[key]
        if e["active"]:
            correct += int(e["action"] == target_policy[e["obs"]])
        if e["bank"] >= 0:
            banks[e["bank"]] += e["writes"]
        digest.update(bytes([e["action"] + 1]))
        if t % 128 == 0 or t == c.ticks - 1:
            snapshots.append(dict(t=t, energy=body.energy, material=body.material, fuel=body.fuel,
                W=list(map(int, np.count_nonzero(body.catalysts, axis=1))), C=int(np.count_nonzero(body.converters)),
                policy_accuracy=float(np.mean(policy(body.traces) == target_policy)),
                payload_accuracy=float(np.mean(decode(body.traces[2:]) == targets[2:])),
                dead=body.dead, state_digest=body.digest()))
    pa = float(np.mean(policy(body.traces) == target_policy))
    da = float(np.mean(decode(body.traces[2:]) == targets[2:]))
    return dict(seed=seed, arm=arm, config=asdict(c), priority=list(priority),
        active_fraction=total["active"] / c.ticks, completed=total["active"] == c.ticks,
        policy_accuracy=pa, payload_accuracy=da, functional_policy=pa * int(not body.dead),
        functional_payload=da * int(not body.dead), correct_decisions_per_planned=correct / c.ticks,
        final_energy=body.energy, final_material=body.material, final_fuel=body.fuel,
        final_W=int(np.count_nonzero(body.catalysts)), final_C=int(np.count_nonzero(body.converters)),
        bank_writes=banks, ledger=total, snapshots=snapshots, env_digest=env_digest,
        action_digest=digest.hexdigest(), state_digest=body.digest())


PAIRS = (("self", "no_C", "active_fraction"), ("no_C_rescue", "no_C", "active_fraction"),
         ("no_C_energy", "no_C", "active_fraction"), ("self", "no_policy_write", "active_fraction"),
         ("self_energy", "no_W_energy", "policy_accuracy"))


def study(out):
    out.mkdir(exist_ok=False)
    paths = ("ac3.py", "test_ac3.py", "ac2.py", "ac1.py", "AC3_PROTOCOL_v1.md")
    result = dict(kind="engineering_only", seeds=list(range(8)), configs=[],
        python=platform.python_version(), numpy=np.__version__,
        source_hashes={p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths})
    (out / "pre_run_snapshot.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    started = time.monotonic()
    for p in (.0001, .0002, .0004):
        c = Config(flip_p=p)
        rows = []
        for seed in result["seeds"]:
            inputs = world(seed, c)
            rows.extend(run_one(seed, c, arm, inputs) for arm in ARMS)
        means = {a: {k: float(np.mean([r[k] for r in rows if r["arm"] == a]))
                     for k in ("active_fraction", "completed", "policy_accuracy", "payload_accuracy",
                               "functional_policy", "functional_payload", "correct_decisions_per_planned",
                               "final_W", "final_C")}
                 for a in ARMS}
        contrasts = {a + "-" + b: contrast([r[k] for r in rows if r["arm"] == a],
                                           [r[k] for r in rows if r["arm"] == b]) for a, b, k in PAIRS}
        criteria = dict(self_viable=means["self"]["active_fraction"] >= .9,
            protected_viable=means["protected"]["active_fraction"] >= .9,
            C_rescue=means["no_C_rescue"]["active_fraction"] >= .9,
            energy_rescue=means["no_C_energy"]["active_fraction"] >= .9,
            C_dependence=contrasts["self-no_C"]["mean"] >= .2,
            W_information_dependence=contrasts["self_energy-no_W_energy"]["mean"] >= .2,
            turnover=all(r["ledger"]["births"] > 120 and r["ledger"]["C_births"] > 30
                         and r["ledger"]["converted"] > 0 and all(n > 0 for n in r["bank_writes"])
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
