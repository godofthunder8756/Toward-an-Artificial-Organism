"""AC80 engineering: internalized reconstruction recipe — trigger-margin measurement.

Before any protocol, the first question the task requires answering: AC79's description repair
"rides the program's corruption trigger (obs bit 2)", which is conservative only because the
program (126 bits) is 16x the 8-bit description, so it degrades 16x faster and the signal fires
~45x before the description could approach a majority flip. At 78 bits the program is only ~1.6x
larger, so obs bit 2 no longer fires ~45x early. This probe measures whether the trigger still
precedes a description-majority flip, or whether the rule-word storage needs its own/widened
trigger.

Also checks the standard recovery table (internalized recovers, unmaintained degrades, no_repair
dies) with the 78-bit description and the generic decode.
"""
import numpy as np
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog
import ac80


def run_traced(seed, history, arm, corrupt=True, ticks=ac76.TICKS):
    """Run one individual and record the description's trigger-margin over the whole horizon.

    Instrumentation point is INSIDE the re-instantiation, at the moment the description repair is
    about to run (obs bit 2 set, after the tick's program damage has been applied). Records:
      - max_desc_minority: max number of SET replicas on any correct-0 description bit, measured
        at every repair opportunity. Reaching 4 = a majority flip that the repair would cement
        (trigger too late).
      - desc_flip_tick: first tick any correct-0 description bit reached >=4 set replicas at any
        moment (run-loop check, right after the description damage is applied) — the worst-case
        damage level independent of the trigger.
    """
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
    base_reg = ac80.reg_maintained if maintained else (ac80.reg_pristine if ac_arm == 'regen' else None)

    at_risk = np.flatnonzero(encoded == 0)     # correct-0 description bits (sticky-set can flip them)
    trace = {'now': 0, 'max_minority': 0, 'fires': 0, 'flip_tick': None, 'at_repair_flip': 0}

    def traced_reg(o, e):
        trigger = bool(ac9.observe(o) & 4)
        if maintained:
            trigger = trigger or (ac80.desc_minority(o) >= ac80.DESC_TRIGGER)
        if not trigger:
            return
        sets = o.body.traces[1, at_risk].sum(axis=-1)
        mx = int(sets.max()) if len(sets) else 0
        trace['max_minority'] = max(trace['max_minority'], mx)
        if mx >= 4:
            trace['at_repair_flip'] += 1
            if trace['flip_tick'] is None:
                trace['flip_tick'] = trace['now']
        trace['fires'] += 1
        if base_reg is not None:
            return base_reg(o, e)

    reg_fn = traced_reg if (maintained or ac_arm == 'regen') else None
    step = ac80.build(ac_arm, alloc, reg_fn)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])
    total = ac9.event()
    first_dead = None
    alive_at_corruption = None
    for t in range(ticks):
        alloc.now = t
        trace['now'] = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage_desc:
            o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
        if t == ac76.CORRUPT_TICK and corrupt:
            correct = prog.program(priority)
            for bit in range(ac76.CORRUPT_BITS):
                w = 1 - int(correct[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(correct[bit])
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t == ac76.CORRUPT_TICK:
            alive_at_corruption = not o.body.dead
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    target = prog.program(priority)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    desc_bits = ac80.read_description(o)
    desc_priority = ac80.decode_perm(desc_bits[ac80.PERM_OFFSET:ac80.PERM_OFFSET + 8])
    return dict(seed=seed, history=history, arm=arm, corrupt=corrupt,
                completed=total['active'] == ticks, first_dead=first_dead,
                alive_at_corruption=alive_at_corruption,
                program_correct=int((decoded == target).sum()),
                flipped_still_wrong=int((decoded[:ac76.CORRUPT_BITS] != target[:ac76.CORRUPT_BITS]).sum()),
                description_correct=int((desc_bits == encoded).sum()),
                description_word_correct=int((desc_bits[:ac80.PERM_OFFSET] == encoded[:ac80.PERM_OFFSET]).sum()),
                description_valid=int(sorted(desc_priority) == list(range(4))),
                description_same=int(desc_priority == tuple(priority)),
                max_desc_minority=trace['max_minority'], desc_flip_tick=trace['flip_tick'],
                at_repair_flip=trace['at_repair_flip'], trigger_fires=trace['fires'],
                n_at_risk=int(len(at_risk)),
                energy=inv[0], material=inv[1], fuel=inv[2])


def main():
    seeds = tuple(range(8))
    print('AC80 engineering — internalized recipe (78-bit description + generic decode), 16,384 ticks')
    print('program corruption at t=8192: majority of program bits 0-7 flipped (AC76 intervention)\n')

    # run every individual exactly once and cache
    cache = {}
    for arm in ('internalized', 'pristine', 'unmaintained', 'no_repair'):
        for s in seeds:
            for h in (0, 1):
                for c in (True, False):
                    cache[(arm, s, h, c)] = run_traced(s, h, arm, corrupt=c)
    def rows(arm, corrupt):
        return [cache[(arm, s, h, corrupt)] for s in seeds for h in (0, 1)]

    alive = {(r['seed'], r['history']) for r in rows('internalized', False) if r['alive_at_corruption']}
    print(f'viability scan (no corruption): {len(alive)}/{2*len(seeds)} alive at t=8192\n')

    print('TRIGGER-MARGIN (internalized arm, corruption on): does obs bit 2 precede a desc majority flip?')
    print(f'{"seed/h":8s} {"maxMinority@repair":>17s} {"flipTick":>8s} {"atRepairFlip":>12s} {"triggers":>8s} {"descCorrect":>11s}')
    all_ok = True
    for r in rows('internalized', True):
        ok = r['max_desc_minority'] < 4
        all_ok &= ok
        print(f'{str(r["seed"])+"/"+str(r["history"]):8s} {r["max_desc_minority"]:17d} '
              f'{str(r["desc_flip_tick"]):>8s} {r["at_repair_flip"]:12d} {r["trigger_fires"]:8d} '
              f'{r["description_correct"]}/78')
    print(f'\ntrigger precedes description-majority flip in all individuals: {"YES" if all_ok else "NO"}')

    print('\nRECOVERY TABLE (corruption at t=8192):')
    print(f'{"arm":14s} {"survive":>8s} {"died<8192":>9s} {"alive@8192":>10s} '
          f'{"recover":>8s} {"descOK":>7s} {"wordOK":>7s}')
    for arm in ('internalized', 'pristine', 'unmaintained', 'no_repair'):
        rr = rows(arm, True)
        survived = sum(1 for r in rr if r['completed'])
        pre_dead = sum(1 for r in rr if not r['alive_at_corruption'])
        alive_rows = [r for r in rr if r['alive_at_corruption']]
        recovered = sum(1 for r in alive_rows if r['flipped_still_wrong'] == 0 and r['completed'])
        dok = sum(1 for r in rr if r['description_correct'] == 78)
        wok = sum(1 for r in rr if r['description_word_correct'] == 70)
        print(f'{arm:14s} {survived:4d}/{len(rr)} {pre_dead:9d} {len(alive_rows):10d} '
              f'{recovered:4d}/{len(alive_rows)} {dok:4d}/{len(rr)} {wok:4d}/{len(rr)}')

    print('\nper-individual detail (alive@8192 individuals only):')
    for arm in ('internalized', 'pristine', 'unmaintained'):
        rr = [r for r in rows(arm, True) if r['alive_at_corruption']]
        fw = [r['flipped_still_wrong'] for r in rr]
        ds = [r['description_same'] for r in rr]
        dv = [r['description_valid'] for r in rr]
        dd = [r['first_dead'] for r in rr]
        print(f'  {arm:14s} flipWrong {fw}  descSame {ds}  descValid {dv}  deaths {dd}')

    print('\ncontrol (no corruption at t=8192): mechanism must introduce no spurious change')
    for arm in ('internalized', 'pristine'):
        rr = rows(arm, False)
        surv = sum(1 for r in rr if r['completed'])
        fw = [r['flipped_still_wrong'] for r in rr]
        ds = [r['description_same'] for r in rr]
        print(f'  {arm:14s} survive {surv}/{len(rr)}  flippedStillWrong {fw}  descSame {ds}')


if __name__ == '__main__':
    main()
