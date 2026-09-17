"""AC79: description maintenance through paid vulnerable machinery (no hidden pristine backup).

AC76's frozen controller turnover re-instantiates the 126-bit program from an 8-bit priority
description stored in dead legacy bank 1 -- where the damage stream never reaches it and no action
repairs it, i.e. a HIDDEN PRISTINE BACKUP, which the goal rules out as evidence of endogenous
reconstruction. AC78 falsified the "self-produced priority" premise, but the core question is
independent of where the priority's content comes from:

    Can the 8-bit priority description be stored in the vulnerable substrate, PUT IN the damage
    stream, and maintained through the organism's own paid vulnerable machinery -- so the
    compressed-description turnover does not rely on a hidden pristine backup?

Mechanism (single declared change from AC76): (1) apply the same sticky 1e-4 damage to bank 1's
8 description bits, from an independent stream; (2) when the program's own corruption observation
(obs bit 2) fires, the re-instantiation step first repairs the description's 7-replica minority
back to its majority (paid, same primitive, same per-action cap), then re-instantiates the program
from the repaired description, exactly as AC76 does.

Arms: `maintained` (desc damaged + repaired + re-instantiated), `pristine` (AC76 regen as-is -- the
hidden-backup baseline), `unmaintained` (desc damaged, no repair), `no_repair` (loop cut -- AC76's
load-bearing control). Plus a no-corruption control for the inertness gate.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import numpy as np
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog

TICKS = ac76.TICKS
CORRUPT_TICK = ac76.CORRUPT_TICK
CORRUPT_BITS = ac76.CORRUPT_BITS

ARMS = ('maintained', 'pristine', 'unmaintained', 'no_repair')

# each arm -> (ac_arm for ac71.build-style surgery, damage the description?, maintain (repair) it?)
ARM_PARTS = {
    'maintained':   ('regen',    True,  True),   # desc damaged + repaired + re-instantiated
    'pristine':     ('regen',    False, False),  # AC76 as-is: desc never damaged (hidden backup)
    'unmaintained': ('regen',    True,  False),  # desc damaged, NO repair
    'no_repair':    ('no_repair', True,  False),  # loop cut (load-bearing control)
}

SOURCES = ['ac79.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC79_PROTOCOL_v1.md']

# the frozen AC76 re-instantiation (no description repair) -- the pristine/unmaintained reg_fn
ORIG = ac76.reg_from_priority


def reg_description(o, e):
    """Paid majority-restore of the 8-bit description in bank 1; return decoded priority.

    VERBATIM from ac79_engineering.py.
    """
    b = o.body
    bits = (b.traces[1, :8].sum(axis=-1) > 3).astype(np.uint8)
    sites = np.argwhere(b.traces[1, :8] != bits[:, None])
    cap = min(32, int(ac4.available(b)[:4].sum()) * 8, b.energy, b.material)
    n = min(cap, len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, idx[:, 0], idx[:, 1]] = bits[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n
    return ac76.decode_priority(bits)


def reg_maintained(o, e):
    """Description-maintained re-instantiation: repair description, then re-instantiate program.

    VERBATIM from ac79_engineering.py.
    """
    b = o.body
    if not (ac9.observe(o) & 4):
        return
    priority = reg_description(o, e)
    if sorted(priority) != list(range(4)):
        return
    target = prog.program(priority)
    dead_idx = 4 + priority.index(3)
    exclude = {14 * dead_idx + 1 + k for k in range(4)}
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


def build(ac_arm, alloc, reg_fn):
    """Build the AC76-style step, injecting `reg_fn` as the re-instantiation called on obs bit 2.

    `reg_fn` is reg_maintained (maintained arm), ORIG (pristine/unmaintained), or None (no_repair --
    the loop is cut and the injected call is a no-op with no regen surgery).
    """
    base, cut = ac71.arm_parts(ac_arm)
    regen = reg_fn is not None
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    ns['reg_from_priority'] = (reg_fn if regen else (lambda o, e: None))
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
    exec(compile(src, 'ac79_step', 'exec'), ns, fns)
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
    encoded = ac76.encode_priority(priority)
    o.body.traces[1, :8] = encoded[:, None]
    ac_arm, damage_desc, maintained = ARM_PARTS[arm]
    reg_fn = reg_maintained if maintained else (ORIG if ac_arm == 'regen' else None)
    step = build(ac_arm, alloc, reg_fn)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])      # independent damage stream for bank 1
    total = ac9.event()
    first_dead = None
    alive_at_corruption = None
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage_desc:
            o.body.traces[1, :8] |= (rng1.random((8, 7)) < .0001).astype(np.uint8)
        if t == CORRUPT_TICK and corrupt:
            correct = prog.program(priority)
            for bit in range(CORRUPT_BITS):
                w = 1 - int(correct[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(correct[bit])
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t == CORRUPT_TICK:
            alive_at_corruption = not o.body.dead
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    target = prog.program(priority)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    desc_bits = (o.body.traces[1, :8].sum(axis=-1) > 3).astype(np.uint8)
    desc_priority = ac76.decode_priority(desc_bits)
    return dict(seed=seed, history=history, arm=arm, damage_desc=damage_desc,
                maintained=maintained, corrupt=corrupt, ticks=ticks,
                completed=total['active'] == ticks, first_dead=first_dead,
                alive_at_corruption=alive_at_corruption,
                program_correct=int((decoded == target).sum()), program_bits=prog.PROGRAM_BITS,
                flipped_still_wrong=int((decoded[:CORRUPT_BITS] != target[:CORRUPT_BITS]).sum()),
                description_correct=int((desc_bits == encoded).sum()),
                description_valid=int(sorted(desc_priority) == list(range(4))),
                description_same=int(desc_priority == tuple(priority)),
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2],
                routes=[o.memory.read(k) for k in (0, 1)], demand=o.memory.demand().tolist(),
                register=[ac12.bit_value(o, off) for off in offs], state_hash=o.digest())


def gates(rows):
    def pick(arm, corrupt):
        return [r for r in rows if r['arm'] == arm and r['corrupt'] == corrupt]

    def alive8192(rs):
        return [r for r in rs if r['alive_at_corruption']]

    maintained = pick('maintained', True)
    pristine = pick('pristine', True)
    unmaintained = pick('unmaintained', True)
    no_repair = pick('no_repair', True)
    maintained_ctrl = pick('maintained', False)
    pristine_ctrl = pick('pristine', False)
    return {
        # recovery + description integrity are clean only for survivors: the paid maintenance stops
        # at death, and the AC68 W/C collapse kills maintained and pristine alike, leaving a dying
        # organism unable to fund the re-instantiation. Survival is reported as a bimodality-aware
        # lower bound, not gated to an exact count.
        'G1_maintained_recovers': all(
            r['flipped_still_wrong'] == 0 and r['description_same'] == 1
            for r in maintained if r['completed']),
        'G2_unmaintained_fails': all(
            r['flipped_still_wrong'] > 0 and r['description_valid'] == 0
            for r in alive8192(unmaintained)),
        'G3_maintenance_load_bearing': (
            all(not r['completed'] and r['first_dead'] is not None
                for r in alive8192(unmaintained))
            and any(r['completed'] for r in maintained)),
        'G4_no_repair_dies': all(not r['completed'] for r in no_repair),
        'G5_control_clean': (
            all(r['flipped_still_wrong'] == 0 for r in maintained_ctrl + pristine_ctrl)
            and all(r['description_same'] == 1 for r in pristine_ctrl)
            and all(r['description_same'] == 1 for r in maintained_ctrl if r['completed'])),
        'G6_completeness_determinism': None,
    }


def preflight(protocol='AC79_PROTOCOL_v1.md'):
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
                    for corrupt in (True, False):
                        r = run(seed, history, arm, corrupt)
                        rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['arm'], r['corrupt'], r['completed'], r['first_dead'],
                 r['flipped_still_wrong'], r['description_same'], r['description_valid'])
                for r in rows[-2 * len(ARMS) * 2:]]), default=str), flush=True)
    g = gates(rows)
    g['G6_completeness_determinism'] = (
        len(rows) == len(seeds) * 2 * len(ARMS) * 2
        and all(run(s, h, a, c) == orig for s, h, a, c, orig in
                [(rows[0]['seed'], rows[0]['history'], rows[0]['arm'], rows[0]['corrupt'], rows[0])]))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows), indent=2))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect('ac79_engineering_v1', [0, 1, 2, 3, 4, 5, 6, 7]); return
    collect('ac79_results_v1', [4004, 4005, 4006, 4007])


if __name__ == '__main__':
    main()
