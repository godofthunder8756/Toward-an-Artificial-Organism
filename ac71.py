"""AC71: reading the decision state by majority closes all three closure gaps at once.

AC69 found the route lapse (AC68 gap a) is a read/repair threshold mismatch: the register read at
single-replica (threshold 1) flips to "relinquished" on one sticky-damaged replica and stops the
renewal, while the repair fires only at >=4 minority replicas. AC70 measured both single-threshold
fixes and found neither reconciles the tension. AC71 declares the reconciled configuration: register
read at MAJORITY (4), the same convention the program bank's rules use, so a lone damaged replica
cannot relinquish a route, while the repair remains load-bearing through the observation-hijack path.

Engineering (6 seeds, 16,384 ticks): closed arm holds routes (demand [42,0]), no bimodality, register
intact; no_repair arm dies by hijack. AC71 freezes this on fresh seeds.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import numpy as np
import ac9
import ac12
import ac4
from ac1 import decode

ARMS = ('closed', 'no_repair')
TICKS = 16384
DEV = 512
DAMAGE_LINE = "b.traces[0,:126]^=core_flips"
DAMAGE_LINE_STICKY = "b.traces[0,:126]|=core_flips"


def arm_parts(arm):
    return ('allocate', 'no_repair' in arm)


def build(arm, alloc):
    base, cut = arm_parts(arm)
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    assert src.count(ac12.RENEW_BLOCK) == 1
    src = src.replace(ac12.RENEW_BLOCK, ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory'] = ac12.m12
    ns['allowance'] = alloc.allowance
    assert src.count(ac12.OUTCOME_LINE) == 1
    src = src.replace(ac12.OUTCOME_LINE, ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e)")
    ns['alloc'] = alloc
    assert src.count(DAMAGE_LINE) == 1
    src = src.replace(DAMAGE_LINE, DAMAGE_LINE_STICKY)
    shim = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    react = ac12.react_world()
    if cut:
        react = (lambda b, action, a, e, _f=react: _f(b, action, 'no_policy_write', e))
    shim['react'] = react
    ns['ac4'] = SimpleNamespace(**shim)
    fns = {}
    exec(compile(src, 'ac71_step', 'exec'), ns, fns)
    return fns['step']


def run(seed, history, arm):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4            # the declared change: majority read, aligned with repair
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    step = build(arm, alloc)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    total = ac9.event(); actions = {}
    first_dead = None
    for t in range(TICKS):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        a = int(ac12.prog.choose(o.body.traces, ac9.observe(o)))
        actions[a] = actions.get(a, 0) + 1
        e = step(o, core, noise, directions, coin, base_map, [t < DEV] * 2, t < DEV)
        for k in total:
            total[k] += e.get(k, 0)
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    return dict(seed=seed, history=history, arm=arm, ticks=TICKS,
                activity=total['active'] / TICKS, completed=total['active'] == TICKS,
                first_dead=first_dead,
                energy=inv[0], material=inv[1], fuel=inv[2],
                W_live=int((o.body.life[:4] > 0).sum()), C_live=int((o.body.life[16:20] > 0).sum()),
                B_live=int((o.body.boundary > 0).sum()),
                register=[ac12.bit_value(o, off) for off in offs],
                routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(), occupied=int(o.memory.occupied().sum()),
                actions=actions, state_hash=o.digest())


NAMES = ['ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py',
         'ac5.py', 'ac5_program.py', 'ac4.py', 'ac4_transport.py', 'ac1.py',
         'test_ac71.py', 'AC71_PROTOCOL_v1.md']


def collect(root, seeds):
    root = Path(root); root.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in NAMES if Path(n).exists()}
    (root / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (root / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for arm in ARMS:
                    r = run(seed, history, arm); rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['history'], r['arm'], r['completed'], r['first_dead'],
                 r['energy'], r['W_live'], r['C_live'], r['occupied'])
                for r in rows[-2 * len(ARMS):]]), default=str), flush=True)
    (root / 'results.json').write_text(json.dumps(dict(hashes=hashes, rows=rows), indent=2))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac71_engineering_v1', [0, 1, 2]); return
    collect('ac71_results_v1', [2800, 2801, 2802, 2803])


if __name__ == '__main__':
    main()
