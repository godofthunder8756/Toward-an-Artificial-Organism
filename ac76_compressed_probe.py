"""AC76 compressed-description probe: re-instantiate the program from its acquired content.

The genuine §3 regeneration mechanism: the 126-bit program's acquired content is only the 4-bank
priority (24 values). Store that priority as a small redundant description (8 bits x 7 replicas, in the
dead legacy bank 1), and when the organism's own corruption observation (obs bit 2) fires, re-instantiate
the full program from `priority + fixed rules` (a decode, the inverse of the interpreter) as a paid write.
This recovers corruption past the self-repair threshold -- where majority-restore cements (AC61) and where
the AC76 dual-copy only re-copies -- because the 126 bits are re-DERIVED from a 26x-smaller description.

Engineering. No protocol, no final seeds, no claim.
"""
import numpy as np
from types import SimpleNamespace
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog


def encode_priority(priority):
    """4 values (0-3) -> 8 bits (2 per value)."""
    out = np.zeros(8, dtype=np.uint8)
    for i, v in enumerate(priority):
        out[2 * i] = (v >> 1) & 1
        out[2 * i + 1] = v & 1
    return out


def decode_priority(bits):
    return tuple(int((bits[2 * i] << 1) | bits[2 * i + 1]) for i in range(4))


def reg_from_priority(o, e):
    """Re-instantiate the 126-bit program from the stored priority description, when the organism's own
    corruption observation (obs bit 2) is set. Paid, per changed replica, under the frozen per-action
    cap. The register (4 bits in the dead rule's low mask bits) is EXCLUDED: it is dynamic decision
    state, not program content, and is maintained by the normal bank-0 repair."""
    b = o.body
    if not (ac9.observe(o) & 4):
        return
    bits = (b.traces[1, :8].sum(axis=-1) > 3).astype(np.uint8)   # majority of 7 replicas
    priority = decode_priority(bits)
    if sorted(priority) != list(range(4)):
        return                                                    # description corrupted: cannot
    target = prog.program(priority)                               # 126 bits from priority + fixed rules
    dead_idx = 5 + priority.index(3)                              # the mask-32 rule (bank 3)
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
        e['reg_writes'] = e.get('reg_writes', 0) + n      # reconciled before ac4.balance


ACTION_LINE = "        action=prog.choose(b.traces,observe(o))"
BALANCE_LINE = "    ac4.balance(before,b,e)"


def build(arm, alloc):
    base, cut = ac71.arm_parts(arm)
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    ns['reg_from_priority'] = (lambda o, e: None) if cut else reg_from_priority
    assert src.count(ac12.RENEW_BLOCK) == 1
    src = src.replace(ac12.RENEW_BLOCK, ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory'] = ac12.m12
    ns['allowance'] = alloc.allowance
    assert src.count(ac12.OUTCOME_LINE) == 1
    src = src.replace(ac12.OUTCOME_LINE, ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e)")
    ns['alloc'] = alloc
    assert src.count(ac71.DAMAGE_LINE) == 1
    src = src.replace(ac71.DAMAGE_LINE, ac71.DAMAGE_LINE_STICKY)
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
    exec(compile(src, 'ac76c_step', 'exec'), ns, fns)
    return fns['step']


def run(seed, history, arm, corrupt=True, corrupt_tick=8192, ticks=16384):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)          # the acquired content (deterministic)
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    # store the description (8 bits x 7 replicas) in the dead legacy bank 1
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
        if t == corrupt_tick and corrupt:
            # flip the MAJORITY of all 126 program bits (4 of 7 replicas to the wrong value) --
            # the corruption past the self-repair threshold that majority-restore would cement
            correct = prog.program(priority)                     # 126 bits
            for bit in range(prog.PROGRAM_BITS):
                w = 1 - int(correct[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(correct[bit])
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    # is the program correct now (== the priority-derived program)?
    target = prog.program(priority)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    correct_bits = int((decoded == target).sum())
    return dict(seed=seed, history=history, arm=arm, corrupt=corrupt,
                completed=total['active'] == ticks, first_dead=first_dead,
                program_correct=correct_bits, program_bits=prog.PROGRAM_BITS,
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], demand=o.memory.demand().tolist())


def main():
    print('compressed-description regeneration (re-instantiate from stored priority), 16,384 ticks:')
    for corrupt in (True, False):
        label = 'corrupt program majority at t=8192' if corrupt else 'no corruption (control)'
        for arm in ('closed', 'no_repair'):
            res = [run(s, 0, arm, corrupt) for s in (0, 1, 2)]
            surv = sum(1 for r in res if r['completed'])
            ok = [f"{r['program_correct']}/{r['program_bits']}" for r in res]
            deaths = [r['first_dead'] for r in res]
            print(f'  {label:34s} {arm:9s}: survive {surv}/3  program-correct {ok}  deaths {deaths}')


if __name__ == '__main__':
    main()
