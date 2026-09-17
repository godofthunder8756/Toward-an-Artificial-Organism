"""Viability scan + corrected recovery envelope.

The first sweep used engineering seeds 0-3 and was confounded: seeds 2 and 3 die naturally at
t=4083/4738 (AC68 bimodality), BEFORE the corruption tick (8192), so their 'still_wrong=nbits' is an
artifact of corrupting an already-dead body. This scan finds a seed family where every individual is
alive at the corruption tick, then measures the envelope on that clean family only.

Engineering. No protocol, no final seeds, no claim.
"""
import ac76_recovery_probe as rp

if __name__ == '__main__':
    # 1) viability scan: which (seed, history) are alive at t=8192 with NO corruption?
    print('viability scan (no corruption, alive at t=8192):')
    viable = []
    for s in range(0, 24):
        for h in (0, 1):
            r = rp.run(s, h, 'full', nbits=0)
            alive = r['first_dead'] is None or r['first_dead'] > 8192
            if alive:
                viable.append((s, h))
            if r['first_dead'] is not None and r['first_dead'] < 8192:
                print(f'  seed={s} hist={h}: PRE-CORRUPTION death t={r["first_dead"]}')
    print(f'  viable individuals (alive at 8192): {len(viable)} / 48 = {viable}')
    # group viable by seed
    from collections import Counter
    byseed = Counter(s for s, h in viable)
    print(f'  viable seeds (both histories alive): {sorted(s for s, c in byseed.items() if c == 2)}')
