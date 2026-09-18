import ac83
for design, ticks in ac83.DESIGNS.items():
    for seed in (0, 1):
        for history in (0, 1):
            r = ac83.run(seed, history, 'pristine', 'perm', True, ticks['corrupt_tick'], ticks['move_tick'])
            print(f"{design} s{seed}h{history} pristine: done={int(r['completed'])} dead={r['first_dead']} "
                  f"fw={r['flipped_still_wrong']} routes={r['routes']} r1c={int(r['route1_correct'])} "
                  f"demand={r['demand']} rel={r['relinquishments']} rst={r['restorations']} "
                  f"W={r['W']} C={r['C']} mat={r['material']} reg={r['register']}")
