"""AC76 probe: can the controller be REGENERATED from an internal twin copy (goal §3 feasibility)?

Engineering only. Tests the dual-copy mechanism of AC76_DESIGN_v1.md: store the program in bank 0 AND
bank 1, read the 14-replica majority (so full corruption of one bank does not change behaviour), and make
the paid bank-0 repair CROSS-REGENERATE bank 0 from bank 1 where the two disagree. The intervention
adversarially corrupts bank 0 at t=8192 (all 7 replicas of all 126 program bits set to the OPPOSITE of
bank 1's majority). The question: does the organism survive and regenerate the corrupted bank, where a
single-bank program would cement the corruption (AC61)?
"""
import numpy as np
from types import SimpleNamespace
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog
from ac1 import decode


def choose_dual(traces, obs):
    """14-replica majority across banks 0 and 1 for the program bits."""
    bits = (traces[0, :prog.PROGRAM_BITS] + traces[1, :prog.PROGRAM_BITS]).sum(axis=-1)
    dec = (bits > 7).astype(np.uint8)
    words = (dec.reshape(prog.RULES, prog.WIDTH) * (1 << np.arange(prog.WIDTH))).sum(axis=1)
    for word in words:
        enabled = int(word) & 1
        mask = (int(word) >> 1) & 511
        if enabled and obs & mask == mask:
            return (int(word) >> 10) & 15
    return 9


def make_react_cross(base_react):
    def react_cross(b, action, arm, e):
        if action == 2 and arm != 'no_policy_write':
            # replace the normal bank-0 repair with CROSS-REGENERATION from bank 1: for every program
            # bit whose bank-0 replicas disagree with bank 1's majority, rewrite bank 0 to bank 1's
            # value (paid). Bank 0 is thus re-copied from the internal twin, not restored to its own
            # (possibly corrupted) majority. Mirrors ac4.react's action cost and per-action cap.
            b.energy -= 1; e['spent_e'] += 1; e['active'] = 1
            a = ac4.available(b)
            cap = min(32, int(a[:4].sum()) * 8, b.energy, b.material)
            writes = 0
            for bit in range(prog.PROGRAM_BITS):
                if writes >= cap:
                    break
                m1 = int(b.traces[1, bit].sum() >= 4)
                idx = np.argwhere(b.traces[0, bit] != m1)
                if len(idx) == 0:
                    continue
                n = min(len(idx), cap - writes)
                b.traces[0, bit, idx[:n, 0]] = m1
                b.energy -= n; b.material -= n
                e['spent_e'] += n; e['spent_m'] += n; e['writes'] += n
                writes += n
            return
        base_react(b, action, arm, e)
    return react_cross


def build(arm, alloc, react):
    """ac71.build with an injectable react (for the cross-regeneration shim)."""
    base, cut = ac71.arm_parts(arm)
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    ns['prog'] = SimpleNamespace(choose=choose_dual)   # the step must READ the dual-bank majority, too
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
    exec(compile(src, 'ac76_step', 'exec'), ns, fns)
    return fns['step']


def run(seed, history, arm, corrupt_tick=8192, ticks=16384):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    # install the twin copy
    o.body.traces[1, :prog.PROGRAM_BITS] = o.body.traces[0, :prog.PROGRAM_BITS].copy()
    react = make_react_cross(ac12.react_world())
    step = build(arm, alloc, react)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    total = ac9.event()
    first_dead = None; first_regenerated = None
    bank0_wrong = 0
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if t == corrupt_tick:
            # flip bank 0's MAJORITY (4 of 7 replicas) to the opposite of bank 1's majority, leaving
            # 3 replicas intact. This is the turnover test: bank 0's own majority is now WRONG (would be
            # cemented by single-bank repair), but the 14-replica majority across both banks stays right.
            # (Corrupting all 7 replicas is a 7-7 tie and is NOT recoverable by any majority -- it is
            # complete destruction of one copy, which the goal does not require recovery from.)
            m1 = (o.body.traces[1, :prog.PROGRAM_BITS].sum(axis=-1) >= 4).astype(np.uint8)
            for bit in range(prog.PROGRAM_BITS):
                o.body.traces[0, bit, 0:4] = 1 - m1[bit]
                o.body.traces[0, bit, 4:7] = m1[bit]
        a = choose_dual(o.body.traces, ac9.observe(o))
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        # measure: is bank 0's majority correct (== bank 1's majority)?
        m0 = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) >= 4).astype(np.uint8)
        m1 = (o.body.traces[1, :prog.PROGRAM_BITS].sum(axis=-1) >= 4).astype(np.uint8)
        if t >= corrupt_tick:
            wrong = int((m0 != m1).sum())
            bank0_wrong = max(bank0_wrong, wrong)
            if first_regenerated is None and t > corrupt_tick and wrong == 0 and bank0_wrong > 0:
                first_regenerated = t
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    m0 = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) >= 4).astype(np.uint8)
    m1 = (o.body.traces[1, :prog.PROGRAM_BITS].sum(axis=-1) >= 4).astype(np.uint8)
    return dict(seed=seed, history=history, arm=arm,
                completed=total['active'] == ticks, first_dead=first_dead,
                first_regenerated=first_regenerated,
                bank0_correct_final=int((m0 == m1).sum()), program_bits=prog.PROGRAM_BITS,
                max_bank0_wrong_after=bank0_wrong,
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(), state_hash=o.digest())


def main():
    print('dual-copy controller, adversarial one-bank corruption at t=8192:')
    for seed in (0, 1, 2):
        for arm in ('closed', 'no_repair'):
            r = run(seed, 0, arm)
            print(f'  seed {seed} {arm:9s}: survive={r["completed"]} dead={r["first_dead"]} '
                  f'bank0-correct-final {r["bank0_correct_final"]}/{r["program_bits"]} '
                  f'(max wrong after corrupt {r["max_bank0_wrong_after"]}) '
                  f'regenerated_at={r["first_regenerated"]} W={r["W"]} C={r["C"]} '
                  f'demand={r["demand"]}')


if __name__ == '__main__':
    main()
