"""AC76 recovery-envelope probe: do buffer / staging / cheaper-write extend the corruption boundary?

AC76 (frozen) found >=16-bit sudden corruption economically unrecoverable: the corruption idles the
program (no income) while the paid re-instantiation starves (504 writes for a full flip, material out
in ~2 ticks, normal metabolism spending in parallel). The task asks, as an optional diagnostic: does
a starvation buffer, staged regeneration, or a cheaper write extend the recovery envelope?

Three single-declared-change variants of the frozen reg_from_priority, each measured across the
corruption-size sweep (8, 16, 32, 64, 126 bits):

  full      -- the frozen re-instantiation: rewrite EVERY disagreeing replica (4 per corrupted bit).
  majority  -- cheaper write: rewrite only the minimum replicas needed to flip the majority back to
               correct (1 per 4-of-7 flip, 4x cheaper). Leaves the minority replicas wrong but the
               decoded bit correct. This is the "cheaper write" candidate.
  staged    -- full re-instantiation, but the sites are ordered income-first: the material-acquisition
               rule (rule 1, bits 14-27) then the fuel rule (rule 0) before anything else, so the
               paid write restores its own income stream before spending on non-income rules.

A fourth condition measures the buffer hypothesis as a diagnostic: hold more material at the
corruption tick (the organism's stock is what regeneration competes with metabolism for).

Engineering only. No protocol, no final seeds, no claim. This is a diagnostic of WHERE the frozen
boundary sits, not a new freeze.
"""
import numpy as np
from types import SimpleNamespace
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog
import ac76_compressed_probe as cp

CORRUPT_TICK = 8192
TICKS = 16384
SEEDS = (0, 1, 2, 3)


def _sites_and_target(o):
    b = o.body
    bits = (b.traces[1, :8].sum(axis=-1) > 3).astype(np.uint8)
    priority = cp.decode_priority(bits)
    if sorted(priority) != list(range(4)):
        return None, None, None
    target = prog.program(priority)
    dead_idx = 4 + priority.index(3)
    exclude = {14 * dead_idx + 1 + k for k in range(4)}
    sites = np.argwhere(b.traces[0, :prog.PROGRAM_BITS] != target[:, None])
    sites = sites[[i for i in range(len(sites)) if int(sites[i, 0]) not in exclude]]
    return sites, target, exclude


def _apply(o, e, sites, target):
    b = o.body
    cap = min(32, int(ac4.available(b)[:4].sum()) * 8, b.energy, b.material)
    n = min(cap, len(sites))
    if n:
        idx = sites[:n]
        b.traces[0, idx[:, 0], idx[:, 1]] = target[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n


def reg_full(o, e):
    if not (ac9.observe(o) & 4):
        return
    sites, target, _ = _sites_and_target(o)
    if sites is None:
        return
    _apply(o, e, sites, target)


def reg_majority(o, e):
    """Cheaper write: rewrite only the minimum replicas to restore a correct majority per bit."""
    if not (ac9.observe(o) & 4):
        return
    b = o.body
    sites, target, exclude = _sites_and_target(o)
    if sites is None:
        return
    t0 = b.traces[0, :prog.PROGRAM_BITS]
    wrong = (t0 != target[:, None]).sum(axis=1)
    keep = []
    for bit in range(prog.PROGRAM_BITS):
        if bit in exclude:
            continue
        w = int(wrong[bit])
        if w > 3:                                   # majority wrong: flip w-3 replicas -> 3 wrong
            disagree = np.argwhere(t0[bit] != target[bit])[:w - 3]
            for r in disagree:
                keep.append([bit, int(r[0])])
    _apply(o, e, np.asarray(keep, dtype=int).reshape(-1, 2) if keep else np.zeros((0, 2), dtype=int),
           target)


def reg_staged(o, e):
    """Income-first staging: rule 1 (material) and rule 0 (fuel) re-instantiated before non-income
    rules, so the paid write restores its own income stream before spending on the rest."""
    if not (ac9.observe(o) & 4):
        return
    sites, target, _ = _sites_and_target(o)
    if sites is None:
        return
    if len(sites):
        def rank(bit):
            rule = bit // 14
            return 0 if rule == 1 else (1 if rule == 0 else 2)   # material first, then fuel, then rest
        sites = sites[np.argsort([rank(int(s[0])) for s in sites])]
    _apply(o, e, sites, target)


VARIANTS = {'full': reg_full, 'majority': reg_majority, 'staged': reg_staged}


def build(arm, alloc, regfn):
    base, cut = ac71.arm_parts(arm)
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    ns['reg_from_priority'] = (lambda o, e: None) if cut else regfn
    assert src.count(ac12.RENEW_BLOCK) == 1
    src = src.replace(ac12.RENEW_BLOCK, ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory'] = ac12.m12
    ns['allowance'] = alloc.allowance
    assert src.count(ac12.OUTCOME_LINE) == 1
    src = src.replace(ac12.OUTCOME_LINE, ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e)")
    ns['alloc'] = alloc
    assert src.count(ac71.DAMAGE_LINE) == 1
    src = src.replace(ac71.DAMAGE_LINE, ac71.DAMAGE_LINE_STICKY)
    assert src.count(cp.ACTION_LINE) == 1
    src = src.replace(cp.ACTION_LINE, "        reg_from_priority(o,e)\n" + cp.ACTION_LINE)
    assert src.count(cp.BALANCE_LINE) == 1
    src = src.replace(cp.BALANCE_LINE, "    e['writes']+=e.get('reg_writes',0)\n" + cp.BALANCE_LINE)
    shim = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    react = ac12.react_world()
    if cut:
        react = (lambda b, action, a, e, _f=react: _f(b, action, 'no_policy_write', e))
    shim['react'] = react
    ns['ac4'] = SimpleNamespace(**shim)
    fns = {}
    exec(compile(src, 'ac76e_step', 'exec'), ns, fns)
    return fns['step']


def run(seed, history, variant='full', nbits=16, buffer_m=0, arm='closed'):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    o.body.traces[1, :8] = cp.encode_priority(priority)[:, None]
    step = build(arm, alloc, VARIANTS[variant])
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    total = ac9.event()
    first_dead = None
    for t in range(TICKS):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if t == CORRUPT_TICK:
            correct = prog.program(priority)
            for bit in range(nbits):
                w = 1 - int(correct[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(correct[bit])
            if buffer_m:
                o.body.material = min(256, o.body.material + buffer_m)   # diagnostic reserve
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    target = prog.program(priority)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    return dict(seed=seed, variant=variant, nbits=nbits, buffer_m=buffer_m,
                completed=total['active'] == TICKS, first_dead=first_dead,
                program_correct=int((decoded == target).sum()),
                corrupted_still_wrong=int((decoded[:nbits] != target[:nbits]).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2],
                reg_writes=int(total.get('reg_writes', 0)), in_m_total=int(total['in_m']))


if __name__ == '__main__':
    print('recovery envelope: nbits corrupted vs survive (4 seeds x 2 histories = 8 individuals)')
    print(f'{"variant":9s} {"buffer":>6s} | ' +
          ' '.join(f'n={n:3d}' for n in (8, 16, 32, 64, 126)))
    for variant in ('full', 'majority', 'staged'):
        for buffer_m in (0, 128, 256):
            cells = []
            for nbits in (8, 16, 32, 64, 126):
                res = [run(s, h, variant, nbits, buffer_m) for s in SEEDS for h in (0, 1)]
                surv = sum(1 for r in res if r['completed'])
                cells.append(f'{surv:2d}/8')
            label = variant if buffer_m == 0 else f'{variant}+b{buffer_m}'
            buf = '-' if buffer_m == 0 else str(buffer_m)
            print(f'{label:14s} {buf:>6s} | ' + '  '.join(cells))
