"""Corrected recovery envelope on a viability-clean seed family.

The first sweep (seeds 0-3) was confounded by pre-corruption death (AC68 bimodality): seed 2 dies
at t=5040, before the t=8192 corruption, so its 'still_wrong=nbits' is an artifact of corrupting an
already-dead body. This run uses only seeds whose individuals survive to the corruption tick, and
records, per variant and individual, whether death preceded corruption (excluded from recovery
accounting) or followed it.

Also separates the two things the frozen `full` regen does that a majority-only write does not:
(f) recover explicit majority-flip corruption, and (d) prevent natural sticky-SET drift by rewriting
every disagreeing replica whenever the corruption observation fires. A majority-only write drops (d),
so its survival includes drift deaths that `full` prevents -- reported, not hidden.

Engineering. No protocol, no final seeds, no claim.
"""
import ac76_recovery_probe as rp
from collections import Counter

VIABLE_SEEDS = (0, 1, 3, 4, 5, 6, 7)
NBITS = (8, 16, 32, 64)

if __name__ == '__main__':
    print(f'corrected envelope, viable seeds {VIABLE_SEEDS} '
          f'({len(VIABLE_SEEDS)*2} individuals), corruption at t=8192:')
    for variant in ('full', 'majority', 'staged'):
        print(f'  variant={variant}:')
        for nbits in NBITS:
            rows = [rp.run(s, h, variant, nbits) for s in VIABLE_SEEDS for h in (0, 1)]
            pre = [r for r in rows if r['first_dead'] is not None and r['first_dead'] < 8192]
            post = [r for r in rows if r['first_dead'] is None or r['first_dead'] >= 8192]
            rec = [r for r in post if r['completed']]
            # among those who survived the corruption, did they recover the corrupted content?
            recovered = [r for r in rec if r['corrupted_still_wrong'] == 0]
            print(f'    n={nbits:3d}: pre-corruption-dead={len(pre)}/{len(rows)}  '
                  f'survive={len(rec)}/{len(post)}  recover-content={len(recovered)}/{len(post)}')
