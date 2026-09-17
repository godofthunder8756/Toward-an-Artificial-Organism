"""AC76: controller turnover via a compressed internal description.

The §3 milestone, frozen. The program's acquired content is the 4-bank priority; storing it as a small
redundant description (8 bits, dead legacy bank 1) and re-instantiating the 126-bit program from
`priority + fixed rules` when the organism's own corruption observation fires, re-DERIVES the controller
from a description rather than restoring it to its own (possibly corrupted) majority. The single-bank
majority-restore architecture cements a flipped majority (AC61); this recovers it.

Arms: `regen` (re-instantiation + repair), `baseline` (repair only -- AC71, cements), `no_repair`
(neither -- the loop cut).
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import numpy as np
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog

TICKS = 16384
CORRUPT_TICK = 8192
CORRUPT_BITS = 8                       # flip the majority of the first 8 program bits (rule 0)
ARMS = ('regen', 'baseline', 'no_repair')

SOURCES = ['ac76.py', 'ac12.py', 'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py',
           'ac5.py', 'ac5_program.py', 'ac4.py', 'ac4_transport.py', 'ac1.py', 'AC76_PROTOCOL_v1.md']


def encode_priority(priority):
    out = np.zeros(8, dtype=np.uint8)
    for i, v in enumerate(priority):
        out[2 * i] = (v >> 1) & 1
        out[2 * i + 1] = v & 1
    return out


def decode_priority(bits):
    return tuple(int((bits[2 * i] << 1) | bits[2 * i + 1]) for i in range(4))


def reg_from_priority(o, e):
    """Re-instantiate the program from the priority description when obs bit 2 fires. Paid per changed
    replica under the frozen cap. The 4 register bits (dead rule's low mask bits) are excluded -- they
    are dynamic decision state, not program content."""
    b = o.body
    if not (ac9.observe(o) & 4):
        return
    bits = (b.traces[1, :8].sum(axis=-1) > 3).astype(np.uint8)
    priority = decode_priority(bits)
    if sorted(priority) != list(range(4)):
        return
    target = prog.program(priority)
    dead_idx = 4 + priority.index(3)                              # mask-32 rule (bank 3), at position
                                                                  # 4..7 after ac9_priority_v2's rule
                                                                  # reorder [[0,1,2,3,5,6,7,8,4]]
    exclude = {14 * dead_idx + 1 + k for k in range(4)}           # its 4 register bits
    sites = np.argwhere(b.traces[0, :prog.PROGRAM_BITS] != target[:, None])
    sites = sites[[i for i in range(len(sites)) if int(sites[i, 0]) not in exclude]]
    cap = min(32, int(ac4.available(b)[:4].sum()) * 8, b.energy, b.material)
    n = min(cap, len(sites))
    if n:
        idx = sites[:n]
        b.traces[0, idx[:, 0], idx[:, 1]] = target[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n


ACTION_LINE = "        action=prog.choose(b.traces,observe(o))"
BALANCE_LINE = "    ac4.balance(before,b,e)"


def build(arm, alloc):
    base, cut = ac71.arm_parts(arm)
    regen = 'regen' in arm
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    ns['reg_from_priority'] = (reg_from_priority if regen else (lambda o, e: None))
    assert src.count(ac12.RENEW_BLOCK) == 1
    src = src.replace(ac12.RENEW_BLOCK, ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory'] = ac12.m12
    ns['allowance'] = alloc.allowance
    assert src.count(ac12.OUTCOME_LINE) == 1
    src = src.replace(ac12.OUTCOME_LINE, ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e)")
    ns['alloc'] = alloc
    assert src.count(ac71.DAMAGE_LINE) == 1
    src = src.replace(ac71.DAMAGE_LINE, ac71.DAMAGE_LINE_STICKY)
    if regen:
        assert src.count(ACTION_LINE) == 1
        src = src.replace(ACTION_LINE, "        reg_from_priority(o,e)\n" + ACTION_LINE)
        assert src.count(BALANCE_LINE) == 1
        src = src.replace(BALANCE_LINE, "    e['writes']+=e.get('reg_writes',0)\n" + BALANCE_LINE)
    shim = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    react = ac12.react_world()
    if cut:
        react = (lambda b, action, a, e, _f=react: _f(b, action, 'no_policy_write', e))
    shim['react'] = react
    ns['ac4'] = SimpleNamespace(**shim)
    fns = {}
    exec(compile(src, 'ac76_step', 'exec'), ns, fns)
    return fns['step']


def run(seed, history, arm, corrupt=True, ticks=TICKS):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    o.body.traces[1, :8] = encode_priority(priority)[:, None]
    step = build(arm, alloc)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    total = ac9.event()
    first_dead = None
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if t == CORRUPT_TICK and corrupt:
            correct = prog.program(priority)
            for bit in range(CORRUPT_BITS):
                w = 1 - int(correct[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(correct[bit])
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    target = prog.program(priority)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    return dict(seed=seed, history=history, arm=arm, corrupt=corrupt, ticks=ticks,
                completed=total['active'] == ticks, first_dead=first_dead,
                program_correct=int((decoded == target).sum()), program_bits=prog.PROGRAM_BITS,
                flipped_still_wrong=int((decoded[:CORRUPT_BITS] != target[:CORRUPT_BITS]).sum()),
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2],
                routes=[o.memory.read(k) for k in (0, 1)], demand=o.memory.demand().tolist(),
                register=[ac12.bit_value(o, off) for off in offs], state_hash=o.digest())


def preflight(protocol='AC76_PROTOCOL_v1.md'):
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


def gates(rows):
    def pick(arm, corrupt):
        return [r for r in rows if r['arm'] == arm and r['corrupt'] == corrupt]
    regen = pick('regen', True)
    base = pick('baseline', True)
    norep = pick('no_repair', True)
    regen_ctrl = pick('regen', False)
    base_ctrl = pick('baseline', False)
    return {
        'G1_regen_recovers': all(r['completed'] and r['flipped_still_wrong'] == 0 for r in regen),
        'G2_baseline_cements': all(r['flipped_still_wrong'] > 0 for r in base),
        'G3_regeneration_load_bearing': all(not r['completed'] for r in norep),
        'G4_control_clean': (all(r['completed'] and r['flipped_still_wrong'] == 0 for r in regen_ctrl)
                             and all(r['completed'] and r['flipped_still_wrong'] == 0 for r in base_ctrl)),
        'G5_completeness_determinism': None,
    }


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
                    for corrupt in (True, False):
                        r = run(seed, history, arm, corrupt)
                        rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['arm'], r['corrupt'], r['completed'], r['first_dead'], r['program_correct'],
                 r['flipped_still_wrong'])
                for r in rows[-2 * len(ARMS) * 2:]]), default=str), flush=True)
    g = gates(rows)
    g['G5_completeness_determinism'] = (
        len(rows) == len(seeds) * 2 * len(ARMS) * 2
        and all(run(s, h, a, c) == orig for s, h, a, c, orig in
                [(rows[0]['seed'], rows[0]['history'], rows[0]['arm'], rows[0]['corrupt'], rows[0])]))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows), indent=2))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect('ac76_engineering_v1', [0, 1, 2]); return
    collect('ac76_results_v1', [3000, 3001, 3002, 3003])


if __name__ == '__main__':
    main()
