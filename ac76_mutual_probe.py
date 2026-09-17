"""AC76 mutual probe: controller turnover with BOTH banks damaged and mutually regenerated.

Extends ac76_probe.py to the full §3 design: the twin (bank 1) is now IN the damage stream, and the paid
regeneration action (action 2) rewrites BOTH banks to the 14-replica consensus (so each bank is the
internal template for the other — neither is a pristine backup). Tests whether the controller survives
adversarial corruption of EITHER bank and ongoing natural damage, with regeneration load-bearing.

Engineering. No protocol, no final seeds, no claim.
"""
import numpy as np
from types import SimpleNamespace
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog


def choose_dual(traces, obs):
    bits = (traces[0, :prog.PROGRAM_BITS] + traces[1, :prog.PROGRAM_BITS]).sum(axis=-1)
    dec = (bits > 7).astype(np.uint8)
    words = (dec.reshape(prog.RULES, prog.WIDTH) * (1 << np.arange(prog.WIDTH))).sum(axis=1)
    for word in words:
        enabled = int(word) & 1
        mask = (int(word) >> 1) & 511
        if enabled and obs & mask == mask:
            return (int(word) >> 10) & 15
    return 9


def make_react_mutual(base_react):
    def react_mutual(b, action, arm, e):
        if action == 2 and arm != 'no_policy_write':
            b.energy -= 1; e['spent_e'] += 1; e['active'] = 1
            a = ac4.available(b)
            cap = min(32, int(a[:4].sum()) * 8, b.energy, b.material)
            writes = 0
            for bit in range(prog.PROGRAM_BITS):
                if writes >= cap:
                    break
                total = int(b.traces[0, bit].sum()) + int(b.traces[1, bit].sum())
                m = 1 if total >= 8 else 0          # 14-replica consensus
                for bank in (0, 1):
                    idx = np.argwhere(b.traces[bank, bit] != m)
                    if len(idx) == 0:
                        continue
                    n = min(len(idx), cap - writes)
                    if n <= 0:
                        break
                    b.traces[bank, bit, idx[:n, 0]] = m
                    b.energy -= n; b.material -= n
                    e['spent_e'] += n; e['spent_m'] += n; e['writes'] += n
                    writes += n
            return
        base_react(b, action, arm, e)
    return react_mutual


def build(arm, alloc, react):
    base, cut = ac71.arm_parts(arm)
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    ns['prog'] = SimpleNamespace(choose=choose_dual)
    assert src.count(ac12.RENEW_BLOCK) == 1
    src = src.replace(ac12.RENEW_BLOCK, ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory'] = ac12.m12
    ns['allowance'] = alloc.allowance
    assert src.count(ac12.OUTCOME_LINE) == 1
    src = src.replace(ac12.OUTCOME_LINE, ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e)")
    ns['alloc'] = alloc
    assert src.count(ac71.DAMAGE_LINE) == 1
    src = src.replace(ac71.DAMAGE_LINE, ac71.DAMAGE_LINE_STICKY)
    shim = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    if cut:
        react = (lambda b, action, a, e, _f=react: _f(b, action, 'no_policy_write', e))
    shim['react'] = react
    ns['ac4'] = SimpleNamespace(**shim)
    fns = {}
    exec(compile(src, 'ac76m_step', 'exec'), ns, fns)
    return fns['step']


def corrupt_bank_majority(o, bank, other):
    """Flip `bank`'s majority (4 of 7 replicas of every program bit) to the opposite of `other`'s
    majority, leaving 3 replicas intact -- the corruption past the self-repair threshold."""
    m_other = (o.body.traces[other, :prog.PROGRAM_BITS].sum(axis=-1) >= 4).astype(np.uint8)
    for bit in range(prog.PROGRAM_BITS):
        o.body.traces[bank, bit, 0:4] = 1 - m_other[bit]
        o.body.traces[bank, bit, 4:7] = m_other[bit]


def run(seed, history, arm, corrupt_bank=None, corrupt_tick=8192, ticks=16384):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    o.body.traces[1, :prog.PROGRAM_BITS] = o.body.traces[0, :prog.PROGRAM_BITS].copy()
    react = make_react_mutual(ac12.react_world())
    step = build(arm, alloc, react)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])      # independent damage stream for bank 1
    total = ac9.event()
    first_dead = None
    for t in range(ticks):
        alloc.now = t
        core0 = (rng.random((126, 7)) < .0001).astype(np.uint8)
        core1 = (rng1.random((126, 7)) < .0001).astype(np.uint8)
        o.body.traces[1, :prog.PROGRAM_BITS] |= core1      # twin is IN the damage stream now
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if t == corrupt_tick and corrupt_bank is not None:
            corrupt_bank_majority(o, corrupt_bank, 1 - corrupt_bank)
        e = step(o, core0, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    m0 = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) >= 4).astype(np.uint8)
    m1 = (o.body.traces[1, :prog.PROGRAM_BITS].sum(axis=-1) >= 4).astype(np.uint8)
    return dict(seed=seed, history=history, arm=arm, corrupt_bank=corrupt_bank,
                completed=total['active'] == ticks, first_dead=first_dead,
                bank0_ok=int((m0 == m1).sum()), program_bits=prog.PROGRAM_BITS,
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], demand=o.memory.demand().tolist())


def main():
    print('mutual regeneration (both banks damaged, regenerate-to-consensus), 16,384 ticks:')
    for corrupt_bank in (0, 1, None):
        label = f'corrupt bank {corrupt_bank}' if corrupt_bank is not None else 'no corruption (control)'
        for arm in ('closed', 'no_repair'):
            res = [run(s, 0, arm, corrupt_bank) for s in (0, 1, 2)]
            surv = sum(1 for r in res if r['completed'])
            ok = [r['bank0_ok'] for r in res]
            deaths = [r['first_dead'] for r in res]
            print(f'  {label:28s} {arm:9s}: survive {surv}/3  banks-agree {ok}  deaths {deaths}')


if __name__ == '__main__':
    main()
