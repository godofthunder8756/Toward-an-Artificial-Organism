import sys
import ac83

seeds = [int(x) for x in sys.argv[1:]] or list(range(8))

for design, ticks in ac83.DESIGNS.items():
    print(f"\n===== {design} =====")
    for arm in ac83.ARMS:
        rs = []
        for seed in seeds:
            for history in (0, 1):
                r = ac83.run(seed, history, arm, 'perm', True, ticks['corrupt_tick'], ticks['move_tick'])
                rs.append(r)
        surv = sum(r['completed'] for r in rs)
        recov = sum(r['completed'] and r['flipped_still_wrong'] == 0
                    and r['description_correct'] == 78 for r in rs)
        both = sum(ac83._holds_both(r) for r in rs)
        # unconditional (survivor-free) recovery+reacquire: fw=0, desc=78, both routes held
        uncond = sum(r['flipped_still_wrong'] == 0 and r['description_correct'] == 78
                     and ac83._holds_both(r) for r in rs)
        print(f"{arm:13s} survive {surv}/{len(rs)}  recover(surv) {recov}/{len(rs)}  "
              f"hold-both {both}/{len(rs)}  UNCOND(surv+rec+both, no-survivor-filter) {uncond}/{len(rs)}  "
              f"deaths {[r['first_dead'] for r in rs if not r['completed']]}")
        if arm == 'internalized':
            for r in rs:
                if not (r['flipped_still_wrong'] == 0 and r['description_correct'] == 78
                        and ac83._holds_both(r)):
                    print(f"   s{r['seed']}h{r['history']} done={int(r['completed'])} dead={r['first_dead']} "
                          f"fw={r['flipped_still_wrong']} desc={r['description_correct']}/78 "
                          f"routes={r['routes']} r1c={int(r['route1_correct'])} demand={r['demand']} "
                          f"W={r['W']} C={r['C']} mat={r['material']} rel={r['relinquishments']}")
