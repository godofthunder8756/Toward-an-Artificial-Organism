"""AC81: replacement across generations of components.

Milestone 2 of the internalize-the-recipe goal. AC80 froze that the reconstruction recipe is
internalized (78-bit description + generic decode). This study establishes the next claim: the
organism's PHYSICAL COMPONENTS (W catalysts, C converters, B boundary) are constructed, used and
replaced across multiple turnover cycles, driven by that internally retained recipe. A partial
loss (one killed converter + five killed boundary sites) is rebuilt; the components are used
(repair, conversion, retention); and the recipe is maintained against damage, so its loss
(unmaintained description) halts the organism.

Arms reuse AC80 exactly (internalized, pristine, unmaintained, no_repair). The intervention is a
partial component loss at t=8192, not a program corruption and not a catastrophic destruction.

No new primitives. The mechanism is AC80's: the production rules (W/C/B birth) are the
description's words 3-5; the program is rebuilt from the description by the generic decode; the
description is maintained by its own DESC_TRIGGER.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import numpy as np
import ac80
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog

TICKS = ac76.TICKS
LOSS_TICK = ac76.CORRUPT_TICK        # 8192
LOSS_C = (16,)                       # kill one C converter (slot 16)
LOSS_B = (0, 1, 2, 3, 4)             # kill five B boundary sites

ARMS = ac80.ARMS
ARM_PARTS = ac80.ARM_PARTS

SOURCES = ['ac81.py', 'ac80.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC81_PROTOCOL_v1.md']

# Gate floors (declared in the protocol, engineering-informed and categorical):
#   turnover  -> each component class born many times over the horizon
#   recovery  -> the killed C and B are rebuilt and populations restored
W_BIRTH_FLOOR = 100
C_BIRTH_FLOOR = 20
B_BIRTH_FLOOR = 100
C_POST_FLOOR = 1
B_POST_FLOOR = 5
C_LIVE_FLOOR = 2
B_LIVE_FULL = 20


def run(seed, history, arm, loss=True, ticks=TICKS):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    encoded = ac80.description_bits(priority)
    o.body.traces[1, :ac80.DESC_BITS] = encoded[:, None]
    ac_arm, damage_desc, maintained = ac80.ARM_PARTS[arm]
    reg_fn = ac80.reg_maintained if maintained else (ac80.reg_pristine if ac_arm == 'regen' else None)
    step = ac80.build(ac_arm, alloc, reg_fn)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])      # independent damage stream for bank 1
    total = ac9.event()
    first_dead = None
    alive_at_loss = None
    births_at_loss = (0, 0, 0)
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage_desc:
            o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
        if t == LOSS_TICK and loss:
            for idx in LOSS_C:
                o.body.life[idx] = 0
            for j in LOSS_B:
                o.body.boundary[j] = 0
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t == LOSS_TICK:
            alive_at_loss = not o.body.dead
            births_at_loss = (int(total['W_birth']), int(total['C_birth']), int(total['B_birth']))
        if first_dead is None and o.body.dead:
            first_dead = t
    desc_bits = ac80.read_description(o)
    desc_priority = ac80.decode_perm(desc_bits[ac80.PERM_OFFSET:ac80.PERM_OFFSET + 8])
    inv = ac4.inventory(o.body)
    return dict(seed=seed, history=history, arm=arm, loss=loss, ticks=ticks,
                completed=total['active'] == ticks, first_dead=first_dead,
                alive_at_loss=alive_at_loss,
                W_birth=int(total['W_birth']), C_birth=int(total['C_birth']),
                B_birth=int(total['B_birth']),
                C_birth_post=int(total['C_birth']) - births_at_loss[1],
                B_birth_post=int(total['B_birth']) - births_at_loss[2],
                writes=int(total['writes']), converted=int(total['converted']),
                W_live=int((o.body.life[:16] > 0).sum()), C_live=int((o.body.life[16:20] > 0).sum()),
                B_live=int((o.body.boundary > 0).sum()),
                routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(),
                description_correct=int((desc_bits == encoded).sum()),
                description_same=int(desc_priority == tuple(priority)),
                energy=inv[0], material=inv[1], fuel=inv[2], state_hash=o.digest())


def gates(rows):
    def pick(arm, loss):
        return [r for r in rows if r['arm'] == arm and r['loss'] == loss]

    internalized = pick('internalized', True)
    pristine = pick('pristine', True)
    unmaintained = pick('unmaintained', True)
    no_repair = pick('no_repair', True)
    internalized_ctrl = pick('internalized', False)
    pristine_ctrl = pick('pristine', False)
    return {
        # recovery/description endpoints are clean only for survivors: the paid maintenance stops
        # at death (AC79/AC80). Survival is a bimodality-aware lower bound, not gated.
        'G1_turnover': all(
            r['W_birth'] >= W_BIRTH_FLOOR and r['C_birth'] >= C_BIRTH_FLOOR
            and r['B_birth'] >= B_BIRTH_FLOOR
            for r in internalized if r['completed']),
        'G2_use': all(
            r['writes'] > 0 and r['converted'] > 0
            and r['routes'][0] is not None and r['routes'][1] is not None
            for r in internalized if r['completed']),
        'G3_partial_loss_recovery': all(
            r['C_birth_post'] >= C_POST_FLOOR and r['B_birth_post'] >= B_POST_FLOOR
            and r['C_live'] >= C_LIVE_FLOOR and r['B_live'] == B_LIVE_FULL
            for r in internalized if r['completed']),
        'G4_recipe_maintained': (
            all(r['description_correct'] == 78 for r in internalized if r['completed'])
            and all(r['description_correct'] < 78 for r in unmaintained)),
        'G5_maintenance_load_bearing': (
            all(not r['completed'] for r in unmaintained)
            and any(r['completed'] for r in internalized)),
        'G6_no_repair_dies': all(not r['completed'] for r in no_repair),
        'G7_control_clean': (
            all(r['description_correct'] == 78 and r['W_birth'] >= W_BIRTH_FLOOR
                for r in internalized_ctrl if r['completed'])
            and all(r['description_correct'] == 78 and r['W_birth'] >= W_BIRTH_FLOOR
                    for r in pristine_ctrl if r['completed'])),
        'G8_completeness_determinism': None,
    }


def preflight(protocol='AC81_PROTOCOL_v1.md'):
    text = Path(protocol).read_text()
    marker = 'SOURCES (declared):'
    line = [l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line, f'{protocol} declares no source list'
    declared = [w.strip() for w in line[0].split(marker, 1)[1].split() if w.strip()]
    assert set(declared) == set(SOURCES), \
        f'runner hashes {sorted(set(SOURCES))} but protocol declares {sorted(set(declared))}'
    missing = [s for s in declared if not Path(s).exists()]
    assert not missing, f'declared sources missing: {missing}'
    return declared


def collect(root, seeds):
    preflight()
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES if Path(n).exists()}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for arm in ARMS:
                    for loss in (True, False):
                        r = run(seed, history, arm, loss)
                        rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['arm'], r['loss'], r['completed'], r['first_dead'],
                 r['W_birth'], r['C_birth'], r['B_birth'],
                 r['C_birth_post'], r['B_birth_post'], r['description_correct'],
                 r['routes'])
                for r in rows[-2 * len(ARMS) * 2:]]), default=str), flush=True)
    g = gates(rows)
    g['G8_completeness_determinism'] = (
        len(rows) == len(seeds) * 2 * len(ARMS) * 2
        and all(run(s, h, a, l) == orig for s, h, a, l, orig in
                [(rows[0]['seed'], rows[0]['history'], rows[0]['arm'], rows[0]['loss'], rows[0])]))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows), indent=2))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect('ac81_engineering_v1', [0, 1, 2, 3, 4, 5, 6, 7]); return
    collect('ac81_results_v1', [4012, 4013, 4014, 4015])


if __name__ == '__main__':
    main()
