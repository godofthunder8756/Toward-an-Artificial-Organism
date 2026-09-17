"""AC68: the body's self-production is closed, the acquired function is open.

AC67 showed the repair loop is load-bearing: 8/8 survive with it, 8/8 die with it cut. AC68 asks
the next question in the closure line — over a long horizon, is the repair-active organism's body
*self-sustaining* (a closed production cycle reaching a steady state), and does its acquired
function (the routes) persist with it?

Long-horizon diagnostic (seed 0, history 0, 16384 ticks): the body reaches a steady state — energy
~120, W_live 2, C_live 2, B 20 — and survives the whole horizon, while both acquired routes lapse
by t=4096. The register stays intact (`[0,0,0,0]`, the repair maintains it); the routes lapse
because the program's own scheduling neglects renewal (83 renewals of region 0, zero of region 1,
against 1,137 B-births and 2,772 idle actions). The body closes; the function does not.

AC68 freezes this as a claim with the declared endpoints, on fresh seeds.
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

TICKS = 16384
DEV = 512
DAMAGE_LINE = "b.traces[0,:126]^=core_flips"
DAMAGE_LINE_STICKY = "b.traces[0,:126]|=core_flips"


def build(alloc):
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
    shim['react'] = ac12.react_world()
    ns['ac4'] = SimpleNamespace(**shim)
    fns = {}
    exec(compile(src, 'ac68_step', 'exec'), ns, fns)
    return fns['step']


def run(seed, history):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 1
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    step = build(alloc)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    total = ac9.event()
    actions = {}
    first_route_loss = None
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
        if first_route_loss is None and t > DEV and o.memory.read(0) is None and o.memory.read(1) is None:
            first_route_loss = t
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    return dict(seed=seed, history=history, ticks=TICKS,
                activity=total['active'] / TICKS, completed=total['active'] == TICKS,
                first_dead=first_dead, first_route_loss=first_route_loss,
                energy=inv[0], material=inv[1], fuel=inv[2],
                W_live=int((o.body.life[:4] > 0).sum()), C_live=int((o.body.life[16:20] > 0).sum()),
                B_live=int((o.body.boundary > 0).sum()),
                register=[ac12.bit_value(o, off) for off in offs],
                routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(), occupied=int(o.memory.occupied().sum()),
                renewals=actions.get(3, 0) + actions.get(4, 0),
                actions=actions, state_hash=o.digest())


NAMES = ['ac68.py', 'ac12.py', 'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py',
         'ac5.py', 'ac5_program.py', 'ac4.py', 'ac4_transport.py', 'ac1.py',
         'test_ac68.py', 'AC68_PROTOCOL_v1.md']


def collect(root, seeds):
    root = Path(root); root.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in NAMES if Path(n).exists()}
    (root / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (root / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                r = run(seed, history); rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['history'], r['completed'], r['first_dead'], r['first_route_loss'],
                 r['energy'], r['W_live'], r['C_live'], r['B_live'], r['occupied'], r['renewals'])
                for r in rows[-2:]]), default=str), flush=True)
    (root / 'results.json').write_text(json.dumps(dict(hashes=hashes, rows=rows), indent=2))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac68_engineering_v1', [0, 1, 2]); return
    collect('ac68_results_v1', [2700, 2701, 2702, 2703])


if __name__ == '__main__':
    main()
