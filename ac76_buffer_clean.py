"""Buffer effect on the clean family: does extra material at the corruption tick extend the frozen
`full` re-instantiation's envelope? First sweep (confounded by pre-corruption death) hinted a buffer
helps at n=16 only. Re-measure on viable seeds.
"""
import ac76_recovery_probe as rp

VIABLE_SEEDS = (0, 1, 3, 4, 5, 6, 7)

if __name__ == '__main__':
    print('buffer effect on viable family, frozen `full` re-instantiation:')
    for nbits in (16, 32):
        for buf in (0, 128, 256):
            rows = [rp.run(s, h, 'full', nbits, buf) for s in VIABLE_SEEDS for h in (0, 1)]
            post = [r for r in rows if r['first_dead'] is None or r['first_dead'] >= 8192]
            rec = [r for r in post if r['completed'] and r['corrupted_still_wrong'] == 0]
            print(f'  n={nbits:3d} buffer={buf:3d}: survive+recover={len(rec)}/{len(post)} '
                  f'(pre-corruption-dead={len(rows)-len(post)})')
